from whoosh.query import Term, And, Every, Or
from whoosh import sorting
from searchEngine.engine_config import REVIEW_SUMMARY_USER_ID, QueryType


class ReviewSummaryRunner:
    _instance = None
    
    def __new__(cls, search_engine):
        if cls._instance is None:
            cls._instance = super(ReviewSummaryRunner, cls).__new__(cls)
            cls._instance._initialize(search_engine)
        return cls._instance
    
    def _initialize(self, search_engine):
        self._search_engine = search_engine

                
    def run(self):
        
        all_users_query_type = QueryType.REVIEW_SUMMARY_ALL_USERS
        all_users_query_field_name = all_users_query_type.value[0][0]
        all_users_query_raw_query_data = all_users_query_field_name + ": count num of reviews with respect to every user id "
        all_users_query_data = Every(all_users_query_field_name)
        
        all_users_query_order = self._search_engine.insert_query(all_users_query_raw_query_data, \
            all_users_query_type, all_users_query_data)
        self._search_engine.search_entry(all_users_query_order)
        review_count_by_user_id_dict = self._search_engine.search_results[all_users_query_order]
        
        #tmp
        print(len(review_count_by_user_id_dict))
        argmax_user_id = max(review_count_by_user_id_dict, key=review_count_by_user_id_dict.get)
        argmin_user_id = min(review_count_by_user_id_dict, key=review_count_by_user_id_dict.get)
        print(f"argmax_user_id: {argmax_user_id}, max review count: {review_count_by_user_id_dict[argmax_user_id]}")
        print(f"argmin_user_id: {argmin_user_id}, min review count: {review_count_by_user_id_dict[argmin_user_id]}")
        
        user_id = REVIEW_SUMMARY_USER_ID
        user_id_query_type = QueryType.REVIEW_SUMMARY_SPECIFIC_USER
        user_id_field_name = user_id_query_type.value[0][0]
        raw_user_id_query_data = user_id_query_type.value[0][0] + ":" + user_id
        user_id_query_data = Term(user_id_field_name, user_id)
        user_id_query_order = self._search_engine.insert_query(raw_user_id_query_data, user_id_query_type, user_id_query_data)
        self._search_engine.search_entry(user_id_query_order)
        user_id_results_dict_list = self._search_engine.search_results[user_id_query_order]
        
        # retrieve business_id set from user_id_results_dict_list and search 
        # in business index by these business_ids
        business_id_query_type = QueryType.REVIEW_SUMMARY_BUSINESS_ID
        business_id_field_name = business_id_query_type.value[0][0]
        business_id_set = set([result_dict[business_id_field_name] for result_dict in user_id_results_dict_list])
        raw_business_id_query_data = business_id_field_name + ":"
        business_id_queries = []
        for business_id in business_id_set:
            raw_business_id_query_data += " " + business_id
            business_id_queries.append(Term(business_id_field_name, business_id))
        business_id_query_data = Or(business_id_queries)
        business_id_query_order = self._search_engine.insert_query(raw_business_id_query_data, business_id_query_type, business_id_query_data)
        self._search_engine.search_entry(business_id_query_order)
        business_id_results_dict_list = self._search_engine.search_results[business_id_query_order]
        latitude_field_name = business_id_query_type.value[1][1]
        longitude_field_name = business_id_query_type.value[1][2]
        latitude_list = [result_dict[latitude_field_name] for result_dict in business_id_results_dict_list]
        longitude_list = [result_dict[longitude_field_name] for result_dict in business_id_results_dict_list]
        print(f"latitude min: {min(latitude_list)}, latitude max: {max(latitude_list)}")
        print(f"longitude min: {min(longitude_list)}, longitude max: {max(longitude_list)}")
        