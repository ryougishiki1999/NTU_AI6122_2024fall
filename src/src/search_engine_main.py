from searchEngine.preprocess.preprocessor import PreprocessorSingleton
from searchEngine.search_engine import SearchEngineSingleton
from searchEngine.search_engine_cmd import SearchEngineCmd


if __name__ == "__main__":
    preprocessor_instance = PreprocessorSingleton()
    preprocessor_instance.run()
    search_engine_instance = SearchEngineSingleton()
    search_engine_cmd = SearchEngineCmd(search_engine_instance)
    try:
        search_engine_cmd.cmdloop()
    except KeyboardInterrupt:
        search_engine_cmd.do_exit(None)

