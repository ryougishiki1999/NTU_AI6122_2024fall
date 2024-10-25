import ijson

from searchEngine.cores.index_manager import IndexManagerSingleton, IndexNames
from searchEngine.cores.query_parser import QueryParserAdapter
from searchEngine.cores.schema import BusinessSchema, ReviewSchema, UserSchema
from searchEngine.cores.searcher_ranking import SearcherAdpater
from searchEngine.engine_config import BUSINESS_DATA_PATH, REVIEW_DATA_PATH, USER_DATA_PATH

from whoosh.qparser import QueryParser
from whoosh.searching import Searcher
from whoosh.scoring import TF_IDF, BM25F

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
        # Create Business index
        self._index_manager.create(IndexNames.BUSINESSES, BusinessSchema)  # 创建业务索引
        with open(BUSINESS_DATA_PATH, 'r', encoding='utf-8') as f:  # 使用相对路径
            business_documents = ijson.items(f, 'item')
            self._index_manager.add_documents(IndexNames.BUSINESSES, business_documents)  # 添加业务文档
        # Create User index
        self._index_manager.create(IndexNames.USERS, UserSchema)  # 创建用户索引
        with open(USER_DATA_PATH, 'r', encoding='utf-8') as f:  # 使用相对路径
            user_documents = ijson.items(f, 'item')
            self._index_manager.add_documents(IndexNames.USERS, user_documents)  # 添加用户文档


    def run(self):
        # Example:
        # Search for the query "wonderful AND experience" for "text" filed on review.json
        # Compared to the search_engine_main_demo.py, adapters here helps us to unify the interface
        # In order to improve readability and maintainability.
        print("start review search")
        field_name = "text"
        review_idx = self._index_manager.open(IndexNames.REVIEWS)
        schema = review_idx.schema
        query_data = "wonderful AND experience"
        query_parser = QueryParser(field_name, schema)
        query_paser_adapter = QueryParserAdapter(query_parser, query_data)
        query = query_paser_adapter.parse()
        top_n = 5
        weighting = TF_IDF()
        try:    
            searcher = Searcher(review_idx.reader(), weighting=weighting) # searcher = review_idx.searcher(weighting=weighting)
            searcher_adapter = SearcherAdpater(searcher)
            results = searcher_adapter.search(query, limit=top_n)
            for i in range(results.scored_length()):
                print(f"top-{i+1}: ", results[i], '\n')
            print(results, "\n review search done\n")
        finally:
            searcher.close()
        
        # Example:
        # Search for the query "food AND restaurant" for 
        # `categories` field on bussiness.json
        print("start business search")
        field_name = "categories"
        business_idx = self._index_manager.open(IndexNames.BUSINESSES)
        schema = business_idx.schema
        query_data = "food AND restaurants"
        query_parser = QueryParser(field_name, schema)
        query_paser_adapter = QueryParserAdapter(query_parser, query_data)
        query = query_paser_adapter.parse()
        top_n = 5
        weighting = BM25F()
        try:
            searcher = Searcher(business_idx.reader(), weighting=weighting)
            searcher_adapter = SearcherAdpater(searcher)
            results = searcher_adapter.search(query, limit=top_n)
            for i in range(results.scored_length()):
                print(f"top-{i+1}: ", results[i], '\n')
            print(results, "\n business search done \n")
        finally:
            searcher.close()

        # Example:
        # Search for the query "fernanda" for `name` field on user.json
        print("start user search")
        field_name = "name"
        user_idx = self._index_manager.open(IndexNames.USERS)
        schema = user_idx.schema
        query_data = "fernanda"
        query_parser = QueryParser(field_name, schema)
        query_paser_adapter = QueryParserAdapter(query_parser, query_data)
        query = query_paser_adapter.parse()
        top_n = 5
        try:
            searcher = Searcher(user_idx.reader())
            searcher_adapter = SearcherAdpater(searcher)
            results = searcher_adapter.search(query, limit = top_n)
            for i in range(results.scored_length()):
                print(f"top-{i+1}: ", results[i], '\n')
            print(results, "\n User search done\n")
        finally:
            searcher.close()
       

