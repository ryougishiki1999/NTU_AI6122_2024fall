# [AI6122] Text Data Management and Processing: **Review Data Analysis and Processing**

## Introduction

**Github repository Link for this project**: https://github.com/ryougishiki1999/NTU_AI6122_2024fall

This project is a search engine for discovering Yelp dataset. It is a course project for AI6122 Text Data Management and Processing. The project is developed by a group of students from NTU MSAI. The project is developed in Python in 2024 Fall Semester.

## For Users

### Pre-requisite

- platform: win-x64
  - tests on mac-arm64 don't pass
  - tests on linux-x64 are not conducted
- python: 3.10.15

#### Conda Environment Preparation

After `git clone` this code framework, please first install the required packages **according to `environment.yml` using Conda.**

```
conda env create --file environment.yml
```

#### Dataset Preparation

Consider the dataset is too large to upload to the remote repository, please download the dataset from [yelp](https://www.yelp.com/dataset) and **put `yelp_academic_dataset_business.json` and `yelp_academic_dataset_review.json` and `yelp_academic_dataset_user.json` under the `resource/data` folder.**

#### How to run the code

**Firstly, you need to ensure you are in the `master` branch, and your local repository is up-to-date.**

Then, ensure **you are in the root of project directory**.
run 
```
python src/search_engine_main.py
```
to **start the search engine**.

please read the linked doc [user_manual](docs/user_manual.md)

## For Collaborators/Contributors

### Workflow (important!!!)

Please read the linked doc [workflow](docs/workflow.md)

### Project Structure

Please read the linked doc [project_structure](docs/project_structure.md)

### Roadmap and POW

Please read the linked doc [roadmap_and_pow](docs/roadmap_and_pow.md)

### Misc

some suggestions for the code style, please read the linked doc [code_style](docs/code_style.md)