from searchEngine.engine_config import RESULT_FILE_DIR, RESULT_FILE_PATH
import json
import os


class ResultFileManager:
    _instance = None
    
    def __new__(cls, search_engine):
        if cls._instance is None:
            cls._instance = super(ResultFileManager, cls).__new__(cls)
            cls._instance._initialize(search_engine=search_engine)
        return cls._instance
    
    def _initialize(self, search_engine):
        if not os.path.exists(RESULT_FILE_DIR):
            os.makedirs(RESULT_FILE_DIR)
        if not os.path.exists(RESULT_FILE_PATH):
            open(RESULT_FILE_PATH, 'w').close()
        self._search_engine = search_engine
        
    def write_result2file(self, query_order):
        raw_query_data = self._search_engine.raw_queries[query_order]
        query_type, query_data = self._search_engine.queries[query_order]
        search_results = self._search_engine.search_results[query_order]
        
        json_data = {
            "order": query_order,
            "raw_query_data": raw_query_data,
            "query_type": query_type.name,
            "query_data": str(query_data),
            "results": search_results
        }
        with open(RESULT_FILE_PATH, 'a') as f:
            json.dump(json_data, f)
            f.write("\n")
    
    def check_result_file_empty(self):
        """Check if the result file is empty
        If True, return True and delete the empty file
        """
        if os.path.getsize(RESULT_FILE_PATH) == 0:
            os.remove(RESULT_FILE_PATH)
            print("The result file is empty. It has been deleted.")
            return True
        return False 