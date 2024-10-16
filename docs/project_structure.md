# project structure

## 项目文件结构

### 项目源码结构 `src/`

+ `searchEngine/`
  + `cores/`
    + `index_manager.py`: 构建索引
    + `query_parser.py`: 构建Query
    + `schema.py`：定义索引的schema
    + `searcher_ranking_sorting.py`: 搜索结果排序
  + `preprocess/`:
    + `preprocessor.py`: 预处理数据, 将原始JSON文件预处理生成新的JSON文件
+ `search_engine_main.py`: 搜索引擎程序主入口
+ `search_engine_demo_main.py`: 独立的展示demo, 用于展示搜索引擎的基本工作流程

### 项目资源`resources/`

+ `attachment/`：存放一些文档所需的图片附件等
+ `data/`：**yelp数据集放在这里，并且预处理过的JSON数据集也在这里**

### 项目文档`docs\`

记录开发过程，还有一些项目开发参考文档
代码注释也可以放在这里

### Misc

+ `out/`: 存放一些输出文件
  + `indexdir/`: 构建索引生成的索引文件存放在这里
+ `tmp/`: 临时文件夹
+ `environment.yml`: 项目依赖文件列表
+ `README.md`: **项目说明文档，各种文档入口**