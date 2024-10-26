# [AI6122] Text Data Management and Processing: **Review Data Analysis and Processing**

## For Users

### How to run the code

#### Conda Environment Preparation

After `git clone` this code framework, please first install the required packages **according to `environment.yml` using Conda.**
run:
```
conda env create -n <your_env_name> --file environment.yml
```

If you need additional packages during your development, please add them in `environment.yml`, then re-create `environment.yml`:
```
conda env export > environment.yml
```
If you need to update your environment (if there is new version of environment.yml), please run:
```
conda env update -f environment.yml
```
to update your environment.

#### Dataset Preparation

Consider the dataset is too large to upload to the remote repository, please download the dataset from [yelp](https://www.yelp.com/dataset) and **put `yelp_academic_dataset_business.json` and `yelp_academic_dataset_review.json` and `yelp_academic_dataset_user.json` under the `resource/data` folder.**

#### Run the code

**Firstly, you need to ensure you are in the `master` branch, and your local repository is up-to-date.**

Then, ensure **you are in the root of project directory**.
run 
```
python src/search_engine_main.py
```
to **start the search engine**.
(The same to `search_engine_demo_main.py`, which is a simple demo to test if your environment can run normally)

## For Collaborators

### Workflow (important!!!)

Please read the linked doc [workflow](docs/workflow.md)

### RoadMap

Please read the linked doc [project_structure](docs/project_structure.md)

#### 1st development cycle

Build the basic structure of the project. Accomplish basic components and functions of search engine.

| Module       | Submodule     | Current Maintainer         | Notes                                                                                    |
|--------------|---------------|----------------------------|------------------------------------------------------------------------------------------|
| preprocessor | preprocessor  | Li JiaLi                   | Tokenization, case-folding, lemmatization, stop-word removal                             |
| core         | Index_Manager | Zhou RuoHeng, Dai MengMeng | Design the manager responsible for creating or opening Index, adding documents for Index |
| core         | Schema        | Zhou RuoHeng, Dai MengMeng | Design the corresponding Schema for the specific Index                                   |
| core         | Query_Parser  | PanFeng                    | Design Customization query paraser to handle complex query raw input                     |
| Framework    |               | Zhou RuoHeng               | structure of project, the design of workflow, e.t.c                                      |

### Misc

some suggestions for the code style, please read the linked doc [code_style](docs/code_style.md)