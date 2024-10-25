from whoosh.searching import Searcher

class SearcherAdpater:
    def __init__(self, searcher: Searcher,\
        ):
        self._searcher = searcher
        
    def search(self, query, **kwargs):
        searcher = self._searcher
        results = searcher.search(query, **kwargs)
        return results
    
class CustomizationSearcher(Searcher):
    
    def __init__(self, reader, weighting, **kwargs):
        super().__init__(reader, weighting, **kwargs)
        
    def search(self, query,**kwargs):
        """TODO: 
        Implement a custom query parser
        Maybe query can be processed in a way that...
        Args:
            query (str): query string
        """
