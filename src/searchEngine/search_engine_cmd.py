import cmd

from searchEngine.search_engine import SearchEngineSingleton
from searchEngine.utils.compare_analysis import compare_text
from searchEngine.utils.data_analysis import execute_data_analysis


class SearchEngineCmd(cmd.Cmd):
    _instance = None

    class QueryInputCmd(cmd.Cmd):
        _instance = None

        def __new__(cls, search_engine: SearchEngineSingleton):
            if cls._instance is None:
                cls._instance = super(SearchEngineCmd.QueryInputCmd, cls).__new__(cls)
                cls._instance._initialize(search_engine)
            return cls._instance

        def _initialize(self, search_engine: SearchEngineSingleton):
            self._search_engine = search_engine
            self.prompt = "Search Engine(Query Mode)[press i to input query]> "
            self.intro = "Welcome to the Query Mode. Type help or ? to list commands.\n \
                1) i: Start a new query input and return back result\n \
                2) history: Show the search history\n \
                2) exit/EOF: Exit query mode back to the main shell\n"
            self._search_engine = search_engine

        def do_i(self, arg):
            """Start a new query input and return back result"""
            raw_query = input("Please input your query: ")
            query_order = self._search_engine.parse_raw_query(raw_query=raw_query)
            self._search_engine.search_entry(query_order=query_order)

        def do_history(self, arg):
            """Show the search history"""
            self._search_engine.show_search_history()

        def do_exit(self, arg):
            """Exit query mode back to the main shell"""
            print("Exit query mode back to the main shell")
            return True

        def do_EOF(self, arg):
            """Exit query mode back to the main shell"""
            print("Exit query mode back to the main shell")
            return True

    def __new__(cls, search_engine: SearchEngineSingleton):
        if cls._instance is None:
            cls._instance = super(SearchEngineCmd, cls).__new__(cls)
            cls._instance._initialize(search_engine)
        return cls._instance

    def _initialize(self, search_engine: SearchEngineSingleton):
        self._search_engine = search_engine
        self.prompt = "Search Engine> "
        self.intro = "Welcome to the Search Engine Shell. Type help or ? to list commands.\n \
            1) q: Enter into query mode\n \
            2) data_analysis: For 3.2 Data Analysis\n \
            2) review_summary: For 3.4 Review Summary\n \
            3) app: For 3.5 Application\n \
            4) exit/EOF: Exit the search engine shell\n"
        self._search_engine = search_engine

    def do_q(self, arg):
        """Enter into query mode"""
        try:
            self.QueryInputCmd(self._search_engine).cmdloop()
        except KeyboardInterrupt:
            self.do_exit(arg)

    def do_data_analysis(self, arg):
        """For 3.2 Data Analysis"""
        execute_data_analysis()

    def do_review_summary(self, arg):
        """For 3.4 Review Summary"""
        self._search_engine.review_summary_manager.run()

    def do_app(self, arg):
        """For 3.5 Application"""
        compare_text()

    def do_help(self, arg):
        """Show help commands"""
        return super().do_help(arg)

    def do_EOF(self, arg):
        """Exit the search engine shell"""
        self._search_engine.result_file_manager.check_result_file_empty()
        print("Bye!")
        return True

    def do_exit(self, arg):
        """Exit the search engine shell"""
        self._search_engine.result_file_manager.check_result_file_empty()
        print("Bye!")
        return True
