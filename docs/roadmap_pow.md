# Roadmap and Proof of Work(POW)

#### 1st development cycle

Build the basic structure of the project. Accomplish basic components and functions of search engine.

| Module       | Submodule     | Current Maintainer         | Notes                                                                                    |
|--------------|---------------|----------------------------|------------------------------------------------------------------------------------------|
| preprocessor | preprocessor  | Li JiaLi                   | Tokenization, case-folding, lemmatization, stop-word removal                             |
| core         | Index_Manager | Zhou RuoHeng, Dai MengMeng | Design the manager responsible for creating or opening Index, adding documents for Index |
| core         | Schema        | Zhou RuoHeng, Dai MengMeng | Design the corresponding Schema for the specific Index                                   |
| core         | Query_Parser  | PanFeng                    | Design Customization query paraser to handle complex query raw input                     |
| Framework    |               | Zhou RuoHeng               | structure of project, the design of workflow, e.t.c                                      |