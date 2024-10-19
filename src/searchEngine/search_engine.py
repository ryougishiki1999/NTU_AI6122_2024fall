import ijson

from searchEngine.cores.index_manager import IndexManagerSingleton, IndexNames
from searchEngine.cores.query_parser import QueryParserAdapter
from searchEngine.cores.schema import ReviewSchema, BusinessSchema, UserSchema
from searchEngine.cores.searcher_ranking_sorting import SearcherAdpater
from searchEngine.engine_config import REVIEW_DATA_PATH, BUSINESS_DATA_PATH, USER_DATA_PATH

from whoosh.qparser import QueryParser
from whoosh.searching import Searcher
from whoosh.scoring import TF_IDF
from whoosh.scoring import BM25F


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
        text = "wonderful AND experience"
        query_parser = QueryParser(field_name, schema)
        # QueryParserAdapter, initialize with QueryParser and its subclasses.
        query_paser_adapter = QueryParserAdapter(query_parser, text)
        query = query_paser_adapter.parse()

        top_n = 5
        weighting = TF_IDF()
        searcher = Searcher(review_idx.reader(), weighting=weighting) # searcher = review_idx.searcher(weighting=weighting)
        # SearcherAdpater, the same as QueryParserAdapter
        searcher_adapter = SearcherAdpater(searcher)
        results = searcher_adapter.search(query, limit=top_n)
        print(results, "\n review search done")

        # Search for the query "wonderful AND experience" for
        # `attributes` field on review.json
        print("Start business search")
        field_name = "attributes"
        business_idx = self._index_manager.open(IndexNames.BUSINESSES)
        schema = business_idx.schema
        text = "RestaurantsTakeOut AND True"
        query_parser = QueryParser(field_name, schema)
        query_paser_adapter = QueryParserAdapter(query_parser, text)
        query = query_paser_adapter.parse()
        top_n = 5
        weighting = BM25F()
        searcher = Searcher(business_idx.reader(), weighting=weighting)
        searcher_adapter = SearcherAdpater(searcher)
        results = searcher_adapter.search(query, limit=top_n)
        print(results, "\n business search done")

        print("Start user search")
        field_name = "compliment_cute"
        user_idx = self._index_manager.open(IndexNames.USERS)
        schema = user_idx.schema
        compliment_cute = "0"
        query_parser = QueryParser(field_name, schema)
        query_paser_adapter = QueryParserAdapter(query_parser, compliment_cute)
        query = query_paser_adapter.parse()
        top_n = 5
        weighting = BM25F()
        searcher = Searcher(user_idx.reader(), weighting=weighting)
        searcher_adapter = SearcherAdpater(searcher)
        results = searcher_adapter.search(query, limit=top_n)
        print(results, "\n User search done")