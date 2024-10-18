import ijson

from src.searchEngine.cores.index_manager import IndexManagerSingleton, IndexNames
from src.searchEngine.cores.query_parser import QueryParserAdapter
from src.searchEngine.cores.schema import ReviewSchema, BusinessSchema
from src.searchEngine.cores.searcher_ranking_sorting import SearcherAdpater
from src.searchEngine.engine_config import REVIEW_DATA_PATH, BUSINESS_DATA_PATH


from whoosh.qparser import QueryParser
from whoosh.searching import Searcher
from whoosh.scoring import TF_IDF

class SearchEngineSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SearchEngineSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Create the index manager
        self._index_manager = IndexManagerSingleton()
        # Create Review index
        self._index_manager.create(IndexNames.REVIEWS, ReviewSchema)
        with open(REVIEW_DATA_PATH, 'r', encoding='utf-8') as f:
            review_documents = ijson.items(f, 'item')
            self._index_manager.add_documents(IndexNames.REVIEWS, review_documents)
        # TODO: Create Business index, like the above process of Review index
        # Create Business index
        self._index_manager.create(IndexNames.BUSINESSES, BusinessSchema)  # 创建业务索引
        with open(BUSINESS_DATA_PATH, 'r', encoding='utf-8') as f:  # 使用相对路径
            business_documents = ijson.items(f, 'item')
            self._index_manager.add_documents(IndexNames.BUSINESSES, business_documents)  # 添加业务文档

        
    def run(self):
        # Example:
        # Search for the query "wonderful AND experience" on review.json
        # Compared to the search_engine_main_demo.py, adapters here helps us to unify the interface
        # In order to improve readability and maintainability. 
        review_idx = self._index_manager.open(IndexNames.REVIEWS)
        
        filed_name = "text"
        schema = review_idx.schema
        text = "wonderful"
        query_parser = QueryParser(filed_name, schema)
        # QueryParserAdapter, initialize with QueryParser and its subclasses.
        query_paser_adapter = QueryParserAdapter(query_parser, text)
        query = query_paser_adapter.parse()
        
        top_n = 10
        weighting = TF_IDF()        
        searcher = Searcher(review_idx.reader(), weighting=weighting) # searcher = review_idx.searcher(weighting=weighting)
        # SearcherAdpater, the same as QueryParserAdapter
        searcher_adapter = SearcherAdpater(searcher)
        results = searcher_adapter.search(query, limit=top_n)
        print(results)
        
