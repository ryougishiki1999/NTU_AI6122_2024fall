# Roadmap and Proof of Work(POW)

## 1st development cycle

Build the basic structure of the project. Accomplish basic components and functions of search engine.

| Module        | Submodule     | Current Maintainer         | Notes                                                                                    |
|---------------|---------------|----------------------------|------------------------------------------------------------------------------------------|
| preprocessor  | preprocessor  | Li JiaLi                   | Tokenization, case-folding, lemmatization, stop-word removal                             |
| core          | index_manager | Zhou RuoHeng, Dai MengMeng | Design the manager responsible for creating or opening Index, adding documents for Index |
| core          | schema        | Zhou RuoHeng, Dai MengMeng | Design the corresponding Schema for the specific Index                                   |
| core          | query_parser  | PanFeng                    | Design Customization query paraser to handle complex query raw input                     |
| engine_config |               | Zhou RuoHeng               | Design the configuration file for search engine, including the path of index, e.t.c      |
| Framework     |               | Zhou RuoHeng               | structure of project, the design of workflow, e.t.c                                      |


## 2nd development cycle

Enhance the search engine with more functions and features. Integrate all subtasks into search engine, **all in one**.

| Module         | Submodule            | Current Maintainer     | Notes                                                     |
|----------------|----------------------|------------------------|-----------------------------------------------------------|
| core           | query_parser         | Zhou RuoHeng, Pan Feng | Improve QueryParser and connect it to search engine       |
| CLI            |                      | Zhou RuoHeng           | Design the CLI interface for search engine and all in one |
| core           | weighting_scoring    | Zhou RuoHeng           | develop enhancing scoring and weighting method for 3.3    |
| Framework      |                      | Zhou RuoHeng           | Integrate above modules into search engine and CLI        |
| app            | comparision_sentence | YueShaoShiBais         | For section 3.5 application                               |
| review_summary |                      | PanFeng, Zhou RuoHeng  | For section 3.4 review summary                            |
| data_analysis  |                      | Lai JunZhe             | For section 3.2 data analysis                             |