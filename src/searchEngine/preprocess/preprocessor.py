from searchEngine.engine_config import DATA_DIR,\
    ORIGIN_REVIEW_DATA_PATH, ORIGIN_BUSSIENESS_DATA_PATH,\
    REVIEW_DATA_PATH, BUSSIENESS_DATA_PATH

class PreprocessorSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PreprocessorSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        pass
    
    def run(self):
        """TODO:
        Run the preprocessor to preprocess JSON files.
        Generate the preprocessed JSON files under DATA_DIR(`source/data/`)
        
        Args:
            DATA_DIR: data directory
            ORIGIN_REVIEW_DATA_PATH: original review data path
            ORIGIN_BUSSIENESS_DATA_PATH: original business data path
            REVIEW_DATA_PATH: preprocessed review data path
            BUSSIENESS_DATA_PATH: preprocessed business data
        """
        pass
