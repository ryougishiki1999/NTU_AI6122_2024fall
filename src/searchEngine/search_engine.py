import json
from decimal import Decimal

import ijson
import whoosh

from searchEngine.cores.index_manager import IndexManagerSingleton
from searchEngine.cores.query_parser import QueryParserWrapper
from searchEngine.cores.schema import BusinessSchema, ReviewSchema, UserSchema
from searchEngine.engine_config import BUSINESS_DATA_PATH, FACETS_QUERY_TYPES, INVALID_QUERY_ORDER, REVIEW_DATA_PATH, SEARCHING_WEIGHTING, \
    TOP_K, \
    USER_DATA_PATH
from searchEngine.engine_config import QueryType, IndexNames
from searchEngine.utils.result_file_manager import ResultFileManager
from searchEngine.utils.review_summary import ReviewSummaryRunner


class SearchEngineSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SearchEngineSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Create the index manager
        self.index_manager = IndexManagerSingleton()
        # Create Review index
        self.index_manager.create(IndexNames.REVIEWS, ReviewSchema)
        with open(REVIEW_DATA_PATH, 'r', encoding='utf-8') as f:
            review_documents = ijson.items(f, 'item')
            self.index_manager.add_documents(IndexNames.REVIEWS, review_documents)
        # Create Business index
        self.index_manager.create(IndexNames.BUSINESSES, BusinessSchema)  # 创建业务索引
        with open(BUSINESS_DATA_PATH, 'r', encoding='utf-8') as f:  # 使用相对路径
            business_documents = ijson.items(f, 'item')
            self.index_manager.add_documents(IndexNames.BUSINESSES, business_documents)  # 添加业务文档
        # Create User index
        self.index_manager.create(IndexNames.USERS, UserSchema)  # 创建用户索引
        with open(USER_DATA_PATH, 'r', encoding='utf-8') as f:  # 使用相对路径
            user_documents = ijson.items(f, 'item')
            self.index_manager.add_documents(IndexNames.USERS, user_documents)  # 添加用户文档
            
        # Create the QueryParserWrapper
        self.query_parser_wrapper = QueryParserWrapper()
        
        # Create the result file manager
        self.result_file_manager = ResultFileManager(search_engine=self)
        
        # Create the review summary manager
        self.review_summary_manager = ReviewSummaryRunner(search_engine=self)
            
        # Create the query input list and search result list 
        # and maintain the first unsolved query input index
        self.orders = dict()
        self.next_avaliable_order = 0
        self.raw_queries = dict()
        self.queries = dict()
        self.search_results = dict()
        
    def insert_query(self, raw_query, query_type, query_data):
        conditions = [
            query_type is not QueryType.ILLEGAL,
            query_data is not None,
            isinstance(query_data, whoosh.query.Query)
        ]
        if all(conditions):
            query_order = self.next_avaliable_order
            
            self.orders[query_order] = False
            self.raw_queries[query_order] = raw_query
            self.queries[query_order] = (query_type, query_data)
            self.next_avaliable_order += 1
            return query_order
        else:
            return INVALID_QUERY_ORDER
        
    def parse_raw_query(self, raw_query):
        query_type, query_data = self.query_parser_wrapper.generate_query_and_parse(raw_query)
        conditions = [
            query_type is not QueryType.ILLEGAL,
            query_data is not None,
            isinstance(query_data, whoosh.query.Query)
        ]
        if all(conditions):
            query_order = self.next_avaliable_order
            
            self.orders[query_order] = False
            self.raw_queries[query_order] = raw_query
            self.queries[query_order] = (query_type, query_data)
            self.next_avaliable_order += 1
            return query_order
        else:
            return INVALID_QUERY_ORDER
            
            
    def _search(self, query_order, index_name: IndexNames, limit=TOP_K, scored = True, facets = None):
        query_type, query = self.queries[query_order]
        snippets_names = query_type.value[1]
        
        ix = self.index_manager.open(index_name=index_name)
        weighting = SEARCHING_WEIGHTING
        with ix.searcher(weighting=weighting) as searcher:
            results = searcher.search(query, limit = limit, scored=scored, groupedby=facets)
            print(results)
            
            if query_type not in FACETS_QUERY_TYPES:
                result_dict_list = []
                for i, hit in enumerate(results):
                    print(f"\nrank: top-{i+1}, score: {hit.score}, docID: {hit.docnum}")
                    print("snippets:")
                    hit_dict = {}
                    for snippet_name in snippets_names:
                        print(f"{snippet_name}: ", hit[snippet_name])
                        if isinstance(hit[snippet_name], Decimal):
                            hit_dict[snippet_name] = float(hit[snippet_name])
                        else:
                            hit_dict[snippet_name] = hit[snippet_name]
                    result_dict_list.append(hit_dict)
                self.search_results[query_order] = json.loads(json.dumps(result_dict_list))
            else:
                match query_type:
                    case QueryType.REVIEW_SUMMARY_ALL_USERS:
                        review_count_by_user_id = dict()
                        facet_name = list(facets.items())[0][0]
                        facet_results = results.groups(facet_name)
                        for user_id, hits in facet_results.items():
                            review_count = len(hits)
                            review_count_by_user_id[user_id] = review_count
                        self.search_results[query_order] = review_count_by_user_id
            self.orders[query_order] = True
            
        self.result_file_manager.write_result2file(query_order=query_order)
                    
    def search_entry(self, query_order, limit=TOP_K):
        conditions = [
            query_order in self.orders,
            self.orders.get(query_order, None) is False
        ]
        if all(conditions):
            query_type, _ = self.queries[query_order]    
            match query_type:
                case QueryType.REVIEW:
                    self._search(query_order=query_order, index_name=IndexNames.REVIEWS)
                case QueryType.BUSINESS:
                    self._search(query_order=query_order, index_name=IndexNames.BUSINESSES)
                case QueryType.GEOSPATIAL:
                    self._search(query_order=query_order, index_name=IndexNames.BUSINESSES)
                case QueryType.REVIEW_SUMMARY_ALL_USERS:
                    field_name = query_type.value[0][0]
                    facets = whoosh.sorting.Facets()
                    facets.add_field(field_name)
                    self._search(query_order=query_order, index_name=IndexNames.REVIEWS, limit=None, scored=False, facets=facets)
                case QueryType.REVIEW_SUMMARY_SPECIFIC_USER:
                    self._search(query_order=query_order, index_name=IndexNames.REVIEWS, limit=None)
                case QueryType.REVIEW_SUMMARY_BUSINESS_ID:
                    self._search(query_order=query_order, index_name=IndexNames.BUSINESSES, limit=None)
                case _:
                    print("query type not supported.")
        else:
            print("query unfound or has been handled.")
       

