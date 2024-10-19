from whoosh.qparser import QueryParser
from whoosh.fields import Schema
from whoosh.qparser.syntax import AndGroup
from whoosh.query.positional import Phrase
from whoosh.query.spans import Term
from whoosh.query.terms import Term

class QueryParserAdapter:
    def __init__(self, query_parser: QueryParser,\
        text: str):
        self._parser = query_parser
        self._text = text
        
    def parse(self, **kwargs):
        return self._parser.parse(self._text, **kwargs)
    
class CustomizationParser(QueryParser):
    
    def __init__(self,fieldname, schema, **kwargs):
        super().__init__(fieldname, schema, **kwargs)
    
    def _process_query(self):
        """TODO
        Maybe self._query can be processed in a way that...
        """
        pass
        
    def parse(self, text, **kwargs):
        """TODO: 
        Implement a customization query parser
        Args:
            query (str): query string
        """
        pass