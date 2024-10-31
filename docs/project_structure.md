# project structure

## 项目文件结构

### 项目源码结构 `src/`

+ `searchEngine/`
  + `cores/`
    + `index_manager.py`: 构建索引，管理索引创建和加入文档等
    + `query_parser.py`: 构建Query，功能增强
    + `schema.py`：定义索引各自的schema
    + `weighting_scoring.py`: 搜索结果排序功能增强
  + `preprocess/`:
    + `preprocessor.py`: 预处理数据, 将原始JSON文件预处理生成新的JSON文件
  + `utils/`:
    + `result_file_manager`: 保存search results到本地文件
    + `data_analysis.py`: For section 3.2
    + `review_summary.py`: For section 3.4
    + `comparision_sentence.py`: For section 3.5
+ `search_engine_main.py`: 搜索引擎程序主入口
+ `search_engine_demo_main.py`: 独立的展示demo, 用于展示搜索引擎的基本工作流程
+ `review_summary_demo.py`: 独立的展示demo, 用于展示review_summary的工作流程

### 项目资源`resources/`

+ `attachment/`：存放一些文档所需的图片附件等
+ `data/`：**yelp数据集放在这里，并且预处理过的JSON数据集也在这里**
  + `CA/`：中间产生的数据文件
  + `preprocessed/`: 预处理后的数据文件存放在这里
    + `business.json`：**生成的预处理后的商家数据**
    + `review.json`：**生成的预处理后的评论数据**
  + `yelp_academic_dataset_business.json`：原始商家数据
  + `yelp_academic_dataset_review.json`：原始评论数据

### 项目文档`docs/`

+ `Assignment-202409.pdf`: 项目要求文档
+ `roadmap_pow.md`: 项目路线图和工作量证明
+ `code_structure.md`: 代码结构说明文档
+ `project_structure.md`: 项目结构说明文档
+ `workflow.md`: 项目工作流程说明文档
+ `user_manual.md`: 用户手册说明文档


### 项目输出`out/`

+ `indexdir/`: 构建索引生成的索引文件存放在这里
+ `data_analysis/`: 存放3.2数据分析的结果
+ `results`: 存放搜索结果的文件
+ `review_summary_distribution.png`: 存放3.4 review_summary的用户，评论量分布图


### Misc

+ `environment.yml`: **项目依赖文件列表**, 用于创建conda环境
+ `README.md`: **项目说明文档，各种文档入口**
+ + `tmp/`: 临时文件夹，存放一些临时文件或demo所关联的文件