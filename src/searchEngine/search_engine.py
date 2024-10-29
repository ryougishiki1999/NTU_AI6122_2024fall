import json
from decimal import Decimal

import ijson

from searchEngine.cores.index_manager import IndexManagerSingleton
from searchEngine.cores.query_parser import QueryParserWrapper
from searchEngine.cores.schema import BusinessSchema, ReviewSchema, UserSchema
from searchEngine.engine_config import BUSINESS_DATA_PATH, INVALID_QUERY_ORDER, REVIEW_DATA_PATH, SEARCHING_WEIGHTING, \
    TOP_K, \
    USER_DATA_PATH
from searchEngine.engine_config import QueryType, IndexNames
from searchEngine.utils.result_file_manager import ResultFileManager


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
            
        # Create the query input list and search result list 
        # and maintain the first unsolved query input index
        self.orders = dict()
        self.next_avaliable_order = 0
        self.raw_queries = dict()
        self.queries = dict()
        self.search_results = dict()
        
    def parse_raw_query(self, raw_query):
        query_type, query_data = self.query_parser_wrapper.generate_query_and_parse(raw_query)
        conditions = [
            query_type is not QueryType.ILLEGAL,
            query_data is not None
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
            
            
    def _search(self, query_order, index_name: IndexNames, limit):
        query_type, query = self.queries[query_order]
        snippets_names = query_type.value[1]
        
        ix = self.index_manager.open(index_name=index_name)
        weighting = SEARCHING_WEIGHTING
        with ix.searcher(weighting=weighting) as searcher:
            results = searcher.search(query, limit = limit, scored=True)
            result_dict_list = []
            print(results)
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
                    self._search(query_order=query_order, index_name=IndexNames.REVIEWS, limit=limit)
                case QueryType.BUSINESS:
                    self._search(query_order=query_order, index_name=IndexNames.BUSINESSES, limit=limit)
                case QueryType.GEOSPATIAL:
                    self._search(query_order=query_order, index_name=IndexNames.BUSINESSES, limit=limit)
        else:
            print("query unfound or has been handled.")
       

