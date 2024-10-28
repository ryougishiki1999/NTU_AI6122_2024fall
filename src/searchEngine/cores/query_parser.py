from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser.plugins import FuzzyTermPlugin
from whoosh.query import And, Or, NumericRange
import json
from dateparser.search import search_dates
from whoosh.analysis import StemmingAnalyzer

from searchEngine.engine_config import QueryType
from searchEngine.cores.schema import BusinessSchema, ReviewSchema, UserSchema


class QueryParserWrapper:
    _instance = None 
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueryParserWrapper, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Define three query types with corresponding parsers
        self.parsers = {
            QueryType.REVIEW : QueryParser(QueryType.REVIEW.value, ReviewSchema()),
            QueryType.BUSINESS: QueryParser(QueryType.BUSINESS.value, BusinessSchema()),  
            QueryType.GEOSPATIAL: QueryParser(QueryType.GEOSPATIAL.value, BusinessSchema())  
        }
        #self._parser = query_parser
        #self._text = text
    def identify_query_type(self, user_input):
        """ Identify the type of query based on the user input string. """
        if any(key in user_input for key in QueryType.REVIEW.value):  # Include "text" as an indicator for review queries
            return QueryType.REVIEW
        elif any(key in user_input for key in QueryType.BUSINESS.value):  # Include "name" as an indicator for business queries
            return QueryType.BUSINESS
        elif all(key in user_input for key in QueryType.GEOSPATIAL.value):
            return QueryType.GEOSPATIAL
        else:
            return QueryType.ILLEGAL


    def generate_query_and_parse(self, user_input):
        """
        Generate a query object based on the identified query type.
        
        Args:
            user_input (str): The input string from the user.
        
        Returns:
            tuple: (query_type, query_object) or ("Illegal", None) if not matched.
        """
        query_type = self.identify_query_type(user_input)
        if query_type == QueryType.ILLEGAL:
            return query_type, None
        
        parser = self.parsers.get(query_type)
        if not parser:
            return QueryType.ILLEGAL, None

        target_fields = parser.fieldname if isinstance(parser.fieldname, list) else [parser.fieldname]
        
        try:
            customization_parser = CustomizationQueryParser(fieldnames=target_fields, fieldname=target_fields[0], schema=parser.schema)
            parsed_query_data = customization_parser.process_query(user_input)
            combined_query = customization_parser.combined_parse_query(**parsed_query_data)
        except ValueError:
            return QueryType.ILLEGAL, None

        return query_type, combined_query if combined_query else (query_type, None)
    
    # def _apply_fuzzy_matching(self, text, use_fuzzy=True):
    #     """Applies fuzzy matching based on user preference."""
    #     if use_fuzzy:
    #         return " ".join([f"{word}~" for word in text.split()])
    #     return text 
        
class CustomizationQueryParser(QueryParser):
    
    def __init__(self, fieldnames, schema,latitude_field="latitude", longitude_field="longitude", **kwargs):
        super().__init__(fieldnames[0], schema)# Initialize the base class with a primary field
        self.fieldnames = fieldnames #store the targeted fieldname
        self._schema = schema
        self.latitude_field = latitude_field  # Store the field name for latitude
        self.longitude_field = longitude_field  # Store the field name for longitude
        
        self.add_plugin(FuzzyTermPlugin())
        
        #self.business_column = kwargs.get("business_column", "name")
        #self.review_column = kwargs.get("review_column", "text")
        #self.latitude_column = kwargs.get("latitude_column", "latitude")
        #self.longitude_column = kwargs.get("longitude_column", "longitude")
        
        # Check if inputed columns exist in the schema
        #if self.business_column not in schema or self.review_column not in schema or self.latitude_column not in schema or self.longitude_column not in schema:
        #   raise ValueError("Schema do not have the columns for business or review or longitude or latitude search.")
          
    def process_query(self, query_data):
        """
        Process the query data, extracting relevant fields for search.
        
        Args:
            query_data (str): The input data, a JSON string 
        
        Returns:
            dict: A processed query ready for use in search.
        """
        # Convert query_data to a dictionary if it is a JSON string
        if isinstance(query_data, str):
            try:
                query_data = json.loads(query_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON input format.")
        
        processed_queries = {}
        
        # Process text field (which corresponds to search terms)
        if "text" in query_data:
            processed_queries["search_terms"] = self._apply_text_processing(query_data.get("text", "").strip())
            processed_queries["search_terms"] = self._apply_fuzzy_matching(processed_queries["search_terms"])

        # Process geospatial data separately for geospatial searches
        if self.latitude_field in query_data and self.longitude_field in query_data:
            processed_queries["min_latitude"] = query_data.get(self.latitude_field, "")
            processed_queries["max_latitude"] = query_data.get(self.latitude_field, "")
            processed_queries["min_longitude"] = query_data.get(self.longitude_field, "")
            processed_queries["max_longitude"] = query_data.get(self.longitude_field, "")

        return processed_queries
        # Process review data
        #if "review_id" in query_data:
        #    processed_queries['review_id'] = query_data.get("review_id")
        #    processed_queries['text'] = self._apply_text_processing(query_data.get("text", "").strip())
        #    processed_queries['text'] = self._apply_fuzzy_matching(processed_queries['text'])

        # Process business data
        #if "business_id" in query_data and "name" in query_data:
        #    processed_queries['business_id'] = query_data.get("business_id", "")
        #    processed_queries['business_name'] = self._apply_text_processing(query_data.get("name", "").strip())
        #    processed_queries['business_name'] = self._apply_fuzzy_matching(processed_queries['business_name'])
        #    if query_data.get("latitude") and query_data.get("longitude"): # Ensure latitude and longitude are processed only when both exist
        #        processed_queries['business_latitude'] = query_data.get("latitude", "")
        #        processed_queries['business_longitude'] = query_data.get("longitude", "")
        
        #return processed_queries
        
        
    def keyword_search(self, search_words):
        """
        Search across both business name and reviews using MultifieldParser.
        
        Args:
            search_words (str): The words to search across the business and review fields.
        
        Returns:
            query: A Whoosh query object for the combined search across multiple fields.
        """
        # Create a multifield parser for the business name and review columns
        columns = [self.fieldname]
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
        
        latitude_range = NumericRange(self.latitude_field, min_latitude, max_latitude)
        longitude_range = NumericRange(self.longitude_field, min_longitude, max_longitude)
        
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
    
        # Combine queries based on the combine_with parameter
        if len(queries) == 1:
            return queries[0]  # Return the single query without combining
        else:
            return And(queries) if combine_with.upper() == "AND" else Or(queries)

    
    def _apply_fuzzy_matching(self, text, use_fuzzy=True):
        """Applies fuzzy matching based on user's need."""
        if use_fuzzy:
            return " ".join([f"{word}~" for word in text.split()])
        return text
    
    def _apply_text_processing(self, text):
        """Applies case folding and stemming"""
        analyzer = StemmingAnalyzer()
        return " ".join([token.text for token in analyzer(text.lower())])  # Case folding and stemming
    