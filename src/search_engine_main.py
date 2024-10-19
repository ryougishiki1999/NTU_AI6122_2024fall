from searchEngine.preprocess.preprocessor import PreprocessorSingleton
from searchEngine.search_engine import SearchEngineSingleton


if __name__ == "__main__":
    preprocessor_instance = PreprocessorSingleton()
    preprocessor_instance.run()
    search_engine_instance = SearchEngineSingleton()
    search_engine_instance.run()