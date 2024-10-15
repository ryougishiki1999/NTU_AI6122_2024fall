# project structure

## 项目文件结构

### 项目源码结构 `src\`

+ `src/preprocessor`: 文本预处理器模块, 包括tokenization, stopwords removal等, 还有REPL
+ `src/search_engine`: 搜索引擎核心core模块
+ `src/utils`: 一些公用的工具函数。预计将结果可视化的接口也放在这里
+ `src/main.py`: **主程序入口**

### 项目资源`resources\`
+ `resources\attachment`：附件文件夹，存放一些附件文件
+ `resources\data`：**yelp数据集存放在这里**

### 项目文档`docs\`

记录开发过程，还有一些项目开发参考文档
代码注释也可以放在这里

### Misc
+ `requirements.txt`: 项目依赖文件列表
+ `README.md`: 项目说明文档