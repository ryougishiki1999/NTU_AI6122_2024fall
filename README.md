# [AI6122] Text Data Management and Processing: **Review Data Analysis and Processing**

## For Users

### How to run the code

#### Conda Environment Preparation

After `git clone` this code framework, please first install the required packages **according to `environment.yml` using Conda.**

If you need additional packages during your development, please add them in `environment.yml`, then use `conda env update -f environment.yml` to update your environment.

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

Build the basic structure of the project. Accomplish basic components and functions.

| Module       | Submodule         | Current Maintainer | Notes |
|--------------|-------------------|--------------------|-------|
| preprocessor | tokenization      | Li JiaLi           |       |
| preprocessor | stop-word removal | Li JiaLi           |       |
| preprocessor | REPL              |                    |       |
| Core         | Index             |                    |       |
| Core         | Query             |                    |       |
| Core         | Ranking           |                    |       |
| utility      | review summary    | Pan Feng           |       |

### Misc

some suggestions for the code style, please read the linked doc [code_style](docs/code_style.md)