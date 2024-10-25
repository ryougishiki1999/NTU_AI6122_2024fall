from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser.plugins import FuzzyTermPlugin
from whoosh.query import And, Or, NumericRange
import json
from dateparser.search import search_dates
from whoosh.analysis import StemmingAnalyzer


class QueryParserAdapter:
    def __init__(self, query_parser: QueryParser, text: str):
        self._parser = query_parser
        self._text = text
        
    def parse(self, **kwargs):
        return self._parser.parse(self._text, **kwargs)
    
    
class CustomizationQueryParser(QueryParser):
    
    def __init__(self, fieldname, schema, **kwargs):
        super().__init__(fieldname, schema)
        self._schema = schema
        #self.business_column = business_column
        #self.review_column = review_column
        #self.latitude_column = latitude_column
        #self.longitude_column = longitude_column
        
        self.business_column = kwargs.get("business_column", "name")
        self.review_column = kwargs.get("review_column", "text")
        self.latitude_column = kwargs.get("latitude_column", "latitude")
        self.longitude_column = kwargs.get("longitude_column", "longitude")
        
        self.add_plugin(FuzzyTermPlugin())
        
        # Check if inputed columns exist in the schema
        #if self.business_column not in schema or self.review_column not in schema or self.latitude_column not in schema or self.longitude_column not in schema:
        #   raise ValueError("Schema do not have the columns for business or review or longitude or latitude search.")
          
    def _process_query(self, query_data):
        """
        Process the query data, extracting relevant fields for search.
        
        Args:
            query_data (str): The input data, a JSON string 
        
        Returns:
            dict: A processed query ready for use in search.
        """
        
        query_data = json.loads(query_data)
        
        # Initialize processed_query to store processed results
        processed_queries = {}

        # Process review data
        if "review_id" in query_data:
            processed_queries['review_id'] = query_data.get("review_id")
            processed_queries['text'] = self._apply_text_processing(query_data.get("text", "").strip())
            processed_queries['text'] = self._apply_fuzzy_matching(processed_queries['text'])

        # Process business data
        if "business_id" in query_data and "name" in query_data:
            processed_queries['business_id'] = query_data.get("business_id", "")
            processed_queries['business_name'] = self._apply_text_processing(query_data.get("name", "").strip())
            processed_queries['business_name'] = self._apply_fuzzy_matching(processed_queries['business_name'])
            if query_data.get("latitude") and query_data.get("longitude"): # Ensure latitude and longitude are processed only when both exist
                processed_queries['business_latitude'] = query_data.get("latitude", "")
                processed_queries['business_longitude'] = query_data.get("longitude", "")
        
            # Normalize hours if present (i dont know if we need below, review,business name and location is enough right? can delete)
            if 'hours' in query_data:
                # Parse the hours using the dateparser plugin
                hours_data = query_data.get("hours", {})
                normalized_hours = {}

                for day, hours_str in hours_data.items():
                    # Example format: "Monday: 9:00 AM - 5:00 PM"
                    parsed_times = search_dates(hours_str)
                    if parsed_times:
                        # Extract start and end times from the parsed result
                        normalized_hours[day] = {
                            "open": parsed_times[0][1].strftime("%H:%M"),
                            "close": parsed_times[1][1].strftime("%H:%M") if len(parsed_times) > 1 else None
                        }
                    else:
                        normalized_hours[day] = {"open": None, "close": None}

                processed_queries['business_hours'] = normalized_hours
            else:
                processed_queries['business_hours'] = {}
        
        return processed_queries
    
        
    def keyword_search(self, search_words):
        """
        Search across both business name and reviews using MultifieldParser.
        
        Args:
            search_words (str): The words to search across the business and review fields.
        
        Returns:
            query: A Whoosh query object for the combined search across multiple fields.
        """
        # Create a multifield parser for the business name and review columns
        columns = [self.business_column, self.review_column]
        query_parser = MultifieldParser(columns, self._schema)
        query = query_parser.parse(search_words)
        return query

    
    def geospatial_search(self, min_latitude, max_latitude, min_longitude, max_longitude):
        """
        Geospatial search for businesses based on longitude,latitude within a bounding box.
        
        Args: 
            min_latitude : min latitude of the bounding box
            max_latitude : max latitude of the bounding box
            min_longitude : min longitude of the bounding box
            max_longitude : max longitude of the bounding box
        
        Returns:
            query : A Whoosh query object for the geospatial bounding box search
        """
        # Validation
        if not (-90 <= min_latitude <= 90 and -90 <= max_latitude <= 90):
            raise ValueError("Latitude must lies between -90 and 90.")
        if not (-180 <= min_longitude <= 180 and -180 <= max_longitude <= 180):
            raise ValueError("Longitude must lies between -180 and 180.")
        
        latitude_range = NumericRange(self.latitude_column, min_latitude, max_latitude)
        longitude_range = NumericRange(self.longitude_column, min_longitude, max_longitude)
        
        #using AND condiiton since the business must have a latitude within the specified range and a longitude within the specified range.
        query = And([latitude_range,longitude_range])
        
        return query
    
    
    #Example: Let's say the inputs: keyword_search="UPS, amazing service", 
    # and some given geospatial coordinates, the function will make a query that looks for 
    # businesses named "UPS", with reviews containing "amazing service", that is within the provided specific geographic area.
    def combined_parse_query(self, search_terms=None, min_latitude=None, max_latitude=None,
                             min_longitude=None, max_longitude=None, combine_with="AND"):
        """
         Parse a combined query for businesses and/or reviews with an optional geospatial filter.
    
        Args:
            business_name (str, optional): The business name to search for.
            review_keywords (str, optional): The review keyword to search for.
            min_latitude (float, optional): Minimum latitude for bounding box.
            max_latitude (float, optional): Maximum latitude for bounding box.
            min_longitude (float, optional): Minimum longitude for bounding box.
            max_longitude (float, optional): Maximum longitude for bounding box.
            combine_with (str): method ("AND" or "OR").
    
        Returns:
            query: A combined Whoosh query object.
        """
        queries = []
    
        # Append keyword search across both business and reviews if provided
        if search_terms:
            queries.append(self.keyword_search(search_terms))
    
        # append geospatial bounding box search if both latitude and longitude are provided
        if all([min_latitude, max_latitude, min_longitude, max_longitude]):
            queries.append(self.geospatial_search(min_latitude, max_latitude, min_longitude, max_longitude))
                     
        if not queries:  #if no query 
            return None
    
        return Or(queries) if combine_with.upper() == "OR" else And(queries)
    
    
    def _apply_fuzzy_matching(self, text, use_fuzzy=True):
        """Applies fuzzy matching based on user's need."""
        if use_fuzzy:
            return " ".join([f"{word}~" for word in text.split()])
        return text
    
    def _apply_text_processing(self, text):
        """Applies case folding and stemming"""
        analyzer = StemmingAnalyzer()
        return " ".join([token.text for token in analyzer(text.lower())])  # Case folding and stemming