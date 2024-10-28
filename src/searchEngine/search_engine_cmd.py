import cmd
from searchEngine.search_engine import SearchEngineSingleton


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
            self.prompt = "Search Engine(Query Mode)> "
            self.intro = "Welcome to the Query Mode. Type help or ? to list commands.\n"
            self._search_engine = search_engine
            
        def do_i(self, arg):
            """Start a new query input appending to the unsolved list"""
            raw_query_input = input("Please input your query: ")
            print(f"Query input: {raw_query_input}")
            self._search_engine.raw_queries.append(raw_query_input)
            self._search_engine.parse_raw_query_input(raw_query_input)
        
        def do_s(self, arg):
            """Execute search for all query inputs in the unsolved list"""
            start_query_idx = self._search_engine.unsolved_idx
            end_query_idx = len(self._search_engine.raw_queries)
            for query_idx in range(start_query_idx, end_query_idx):
                self._search_engine.search_query(query_idx)
            self._search_engine.unsolved_idx = end_query_idx
        
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
        self.intro = "Welcome to the Search Engine Shell. Type help or ? to list commands.\n 1) q: Enter into query mode\n 2) exit/EOF: Exit the search engine shell\n"
        self._search_engine = search_engine
        
    def do_q(self, arg):
        """Enter into query mode"""
        self.QueryInputCmd(self._search_engine).cmdloop()
        
    def do_h(self, arg):
        """List query history and let user to select a query number to get the corresponding search result"""
        print("List query history: ")
        for idx, query in enumerate(self._search_engine.raw_queries):
            print(f"{idx}): {query}")
        
        query_idx = int(input("Please input a number to get the corresponding result: "))
        
    
    def do_s(self, arg):
        """Save all search results into a file"""
        print("Save all search results into a file")
        
    def do_help(self, arg: str):
        """Show help commands"""
        return super().do_help(arg)
        
    def do_EOF(self, arg):
        """Exit the search engine shell"""
        print("Bye!")
        return True
        
    def do_exit(self, arg):
        """Exit the search engine shell"""
        print("Bye!")
        return True
        
    