# Code Style

请尽量遵循PEP8代码规范 [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/)
中文版: [PEP8代码规范](https://wangmeng-python.readthedocs.io/en/latest/readability/PEP8.html)

请尽量保持代码的可读性，变量命名请尽量有意义，函数命名请尽量有意义
1. 变量命名：所有字母小写，单词与单词之间用 ' _ ' 分割，e.g. `delete_expr`
2. 函数命名：所有字母小写，单词与单词之间用 ' _ ' 分割
3. 类名：首字母大写，采用驼峰式命名法，e.g. `MemoryState`
4. 全区变量: 所有字母大写，单词之间用'_'分割

请保证变量空间的合理使用，不要定义过多的全局变量，尽量使用局部变量
且避免`from module import *`这种导入方式

#### **请在关键得意之作添加注释，解释其功能和输入输出，方便其他collaborator对接**
