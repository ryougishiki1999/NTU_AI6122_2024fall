from decimal import Decimal

from searchEngine.engine_config import MIN_MAX_SEP, QUERY_NON_STEMMING_FIELDS, USE_QUERY_FUZZY, USE_QUERY_PHRASE, \
    USE_QUERY_STEMMING, USE_QUERY_TERM, QueryType
from whoosh.analysis import StemmingAnalyzer, LowercaseFilter
from whoosh.query import And, Or, NumericRange, Phrase, Term, FuzzyTerm


class SpecificQueryConstructor:
    
    def __init__(self, query_type: QueryType):
        self.query_type = query_type
        self.fieldnames = query_type.value[0]

    def _apply_text_processing(self, text):
        """Applies case folding and stemming"""
        analyzer = StemmingAnalyzer() | LowercaseFilter()
        return (" ".join([token.text for token in analyzer(text)])).strip()
        
    def _apply_fuzzy_matching(self, text, use_fuzzy=True):
        """Applies fuzzy matching based on user's need."""
        if use_fuzzy:
            return (" ".join([f"{word}~1" for word in text.split()])).strip()
        return text
        
    def _process_raw_query(self, raw_query_data: str):
        def raw_query_to_dict(raw_query_data: str):
            pairs = raw_query_data.split(",")
            stripped_pairs = [pair.strip() for pair in pairs]
            return dict(pair.split(':') for pair in stripped_pairs)
        
        raw_query_data_dict = raw_query_to_dict(raw_query_data)
        processed_query_data_dict = {}
        
        for fieldname in self.fieldnames:
            for raw_qurey_key in raw_query_data_dict:
                if raw_qurey_key.find(fieldname) != -1:
                    match self.query_type:
                        case QueryType.REVIEW | QueryType.BUSINESS:
                            content = raw_query_data_dict[raw_qurey_key]
                            if USE_QUERY_STEMMING and fieldname not in QUERY_NON_STEMMING_FIELDS:
                                content = self._apply_text_processing(content)
                            if USE_QUERY_FUZZY:
                                fuzzy_content = self._apply_fuzzy_matching(content)    
                                processed_query_data_dict[fieldname] = (content, fuzzy_content)
                            else:
                                processed_query_data_dict[fieldname] = content
                        case QueryType.GEOSPATIAL:
                            content = raw_query_data_dict[raw_qurey_key]
                            values = content.split(MIN_MAX_SEP)
                            processed_query_data_dict[fieldname] = [float(value) for value in values]

        return processed_query_data_dict
        
    def _generate_keyword_query(self, processed_query_data_dict):
        """ Consider terms and phrase queries for keyword search.
        targeted for QueryType: review and business

        Args:
            processed_query_dict (_type_): _description_
        """
        all_fields_queries = []
        for fieldname, contents in processed_query_data_dict.items():
            field_queries = []
            
            if USE_QUERY_FUZZY:
                term_contents, fuzzy_contents = contents
            else:
                term_contents = contents
                
            term_words = term_contents.split()
            if USE_QUERY_TERM:
                term_query = And([Term(fieldname, word) for word in term_words])
                field_queries.append(term_query)
            
            if USE_QUERY_PHRASE:
                phrase_query = Phrase(fieldname, term_words)
                field_queries.append(phrase_query)
            
            if USE_QUERY_FUZZY:
                fuzzy_term_words = fuzzy_contents.split()
                fuzzy_query = And([FuzzyTerm(fieldname, word) for word in fuzzy_term_words])
                field_queries.append(fuzzy_query)
                
            all_fields_queries.append(Or(field_queries))
                
        return Or(all_fields_queries)
    
    def _generate_geospatial_query(self, processed_query_data_dict):
        latitude_field = self.fieldnames[0]
        longitude_field = self.fieldnames[1]
        
        min_latitude, max_latitude = \
            min(processed_query_data_dict[latitude_field]), max(processed_query_data_dict[latitude_field])
        min_longitude, max_longitude = \
            min(processed_query_data_dict[longitude_field]), max(processed_query_data_dict[longitude_field])
        
        latitue_range_query = NumericRange(latitude_field, Decimal(min_latitude), Decimal(max_latitude))
        longitude_range_query = NumericRange(longitude_field, Decimal(min_longitude), Decimal(max_longitude))
        
        return And([latitue_range_query, longitude_range_query])
            
    
    def generate_query(self, raw_query_data: str):
        processed_query_data_dict = self._process_raw_query(raw_query_data)
        match self.query_type:
            case QueryType.REVIEW | QueryType.BUSINESS:
                return self._generate_keyword_query(processed_query_data_dict)
            case QueryType.GEOSPATIAL:
                return self._generate_geospatial_query(processed_query_data_dict)

class QueryParserWrapper:
    _instance = None 
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueryParserWrapper, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Define three query types with corresponding parsers
        self.wrapped_parsers ={
            QueryType.REVIEW: SpecificQueryConstructor(QueryType.REVIEW),
            QueryType.BUSINESS: SpecificQueryConstructor(QueryType.BUSINESS),
            QueryType.GEOSPATIAL: SpecificQueryConstructor(QueryType.GEOSPATIAL),
        }
        
    def identify_query_type(self, raw_query_data):
        """ Identify the type of query based on the user input string. """
        query_type_mapping = {
            QueryType.REVIEW: QueryType.REVIEW.value[0],
            QueryType.BUSINESS: QueryType.BUSINESS.value[0],
            QueryType.GEOSPATIAL: QueryType.GEOSPATIAL.value[0],
        }
        for query_type, keywords in query_type_mapping.items():
            if any(key in raw_query_data for key in keywords):
                return query_type
        return QueryType.ILLEGAL
    
    
    def generate_query_and_parse(self, raw_query_data):
        """
        Generate a query object based on the identified query type.
        
        Args:
            user_input (str): The input string from the user.
        
        Returns:
            tuple: (query_type, query_object) or ("Illegal", None) if not matched.
        """
        query_type = self.identify_query_type(raw_query_data)
        if query_type == QueryType.ILLEGAL:
            print("query type is illegal")
            return QueryType.ILLEGAL, None
        
        wrapped_parser = self.wrapped_parsers.get(query_type, None)
        if not wrapped_parser:
            print(f"wrapped parser for {query_type.name} is missing")
            return QueryType.ILLEGAL, None
        
        query_data = wrapped_parser.generate_query(raw_query_data)
        return query_type, query_data