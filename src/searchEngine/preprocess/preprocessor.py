import json
import os.path
import string
import time

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from searchEngine.engine_config import \
    DATA_PREPROCESS_DIR, ORIGIN_REVIEW_DATA_PATH, ORIGIN_BUSINESS_DATA_PATH, \
    REVIEW_DATA_PATH, BUSINESS_DATA_PATH, CA_REVIEW_DATA_PATH, \
    CA_USER_DATA_PATH, CA_BUSINESS_DATA_PATH, ORIGIN_USER_DATA_PATH, USE_SKIP_PREPROCESSING, USER_DATA_PATH, DATA_CA_DIR, \
    BUSINESS_DOC_NUM, REVIEW_DOC_NUM, USER_DOC_NUM, \
    ORIGINAL_BUSINESS_DOC_NUM, ORIGINAL_REVIEW_DOC_NUM, ORIGINAL_USER_DOC_NUM


class PreprocessorSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PreprocessorSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.flag = False
        self.notice_flag = set(range(10, 101, 10))
        if not os.path.exists(DATA_CA_DIR):
            os.mkdir(DATA_CA_DIR)

        if not os.path.exists(DATA_PREPROCESS_DIR):
            os.mkdir(DATA_PREPROCESS_DIR)

        if os.path.exists(REVIEW_DATA_PATH) and \
                os.path.exists(BUSINESS_DATA_PATH) and \
                os.path.exists(USER_DATA_PATH):
            self.flag = True

        if not USE_SKIP_PREPROCESSING or not self.flag:
            # 下载分词包
            nltk.download('punkt_tab')
            # 下载停用词
            nltk.download('stopwords')
            # 下载 WordNet 词性表
            nltk.download('wordnet')
            nltk.download('omw-1.4')
            print("successfully download nltk resources")

    # 1.1 处理 business 文件: 筛选出CA这个州的店铺，并保留 business id
    def create_business_dataset(self, business_file, state):
        business_data = []
        # 使用集合提高检索效率，避免元素重复
        # use Set to improve searching efficiency and avoid duplicate elements
        business_id = set()
        count = 0
        percent_notice = self.notice_flag
        with open(business_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                item = json.loads(line)
                count += 1
                if item['state'] == str(state):
                    business_data.append(item)
                    business_id.add(item['business_id'])
                # 每处理10%的文件就在命令行输出提醒一下
                if (count * 100) // ORIGINAL_BUSINESS_DOC_NUM in percent_notice:
                    print("program has scanned ", (count * 100) // ORIGINAL_BUSINESS_DOC_NUM, "% items.")
                    useless_flag = (count * 100) // ORIGINAL_BUSINESS_DOC_NUM
                    percent_notice.remove(useless_flag)
        # convert the list to json file
        with open(CA_BUSINESS_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(business_data, f, ensure_ascii=False, indent=4)
        return business_id

    # 1.2 处理 review 文件：根据 business_id，在 review 文件中筛选出 CA 店铺的评价条目
    def create_review_dataset(self, review_file, business_id):
        review_data = []
        review_user_id = set()
        count = 0
        percent_notice = set(range(10, 101, 10))
        with open(review_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                item = json.loads(line)
                count += 1
                if item['business_id'] in business_id:
                    review_data.append(item)
                    review_user_id.add(item['user_id'])
                # 每处理10%的文件就在命令行输出提醒一下
                if (count * 100) // ORIGINAL_REVIEW_DOC_NUM in percent_notice:
                    print("program has scanned ", (count * 100) // ORIGINAL_REVIEW_DOC_NUM, "% items.")
                    useless_flag = (count * 100) // ORIGINAL_REVIEW_DOC_NUM
                    percent_notice.remove(useless_flag)
        with open(CA_REVIEW_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(review_data, f, ensure_ascii=False, indent=4)
        return review_user_id

    # 1.3 处理 user 文件：根据user_id，在 user 文件中筛选评价过CA这些店铺的用户信息
    def create_user_dataset(self, user_file, user_id):
        user_data = []
        count = 0
        percent_notice = set(range(10, 101, 10))
        with open(user_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                item = json.loads(line)
                count += 1
                if item['user_id'] in user_id:
                    user_data.append(item)
                # 每处理10%的文件就在命令行输出提醒一下
                if (count * 100) // ORIGINAL_USER_DOC_NUM in percent_notice:
                    print("program has scanned ", (count * 100) // ORIGINAL_USER_DOC_NUM, "% items.")
                    useless_flag = (count * 100) // ORIGINAL_USER_DOC_NUM
                    percent_notice.remove(useless_flag)
        with open(CA_USER_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)

    # 数据集预处理第2步
    # 本文件任务：根据第1步抽取的地区数据集基础上，对部分字段进行大小写转换等操作，便于后续的查询
    # 需要处理的文件包括： extracted_CA中的business,review和user三个文件
    # 处理完之后的数据集被保存在processed_CA中

    # 2.1 处理 business 文件，name 转成小写，categories 变成小写并去除标点符号,停用词，词形还原,去除词缀
    def process_business_segment(self):
        business_infile = CA_BUSINESS_DATA_PATH
        business_outfile = BUSINESS_DATA_PATH
        with open(business_infile, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            count = 0
            percent_notice = set(range(10, 101, 10))
            for item in data:
                # 将 name 转换为小写
                item['name'] = item['name'].lower()
                # 将 categories 转成小写并去除标点
                if item['categories']:
                    categories = item['categories']
                    # 进行文本分割
                    tokens = word_tokenize(categories)
                    # 加载停用词
                    stop_words = set(stopwords.words('english'))
                    # 去除停用词
                    filtered_texts = [word for word in tokens if word not in stop_words]
                    # 获取标点符号
                    punctuation = set(string.punctuation)
                    # 去除标点符号
                    clean_tokens = [word for word in filtered_texts if word not in punctuation]
                    # 词形还原
                    lemmatizer = WordNetLemmatizer()
                    lemmatized_texts = [lemmatizer.lemmatize(word) for word in clean_tokens]
                    # 去除词缀
                    stemmer = PorterStemmer()
                    stemmed_texts = [stemmer.stem(word) for word in lemmatized_texts]
                    # 统一大小写
                    processed_texts = [word.lower() for word in stemmed_texts]
                    # 还原成 string 形式
                    processed_texts = ' '.join(processed_texts)
                    item['categories'] = processed_texts
                    count = count + 1
                    progress = (count * 100) // BUSINESS_DOC_NUM
                    if progress in percent_notice:
                        print(f"program has processed {int(progress)}% business file already.")
                        percent_notice.remove(progress)
        # 将 JSON 数据格式化输出到文件
        with open(business_outfile, 'w') as outfile:
            json.dump(data, outfile, indent=4)  # 使用indent=4进行格式化输出

    # 2.2 处理 review 文件，对 text 这个属性进行：大小写转换，去除标点符号，去除停用词，词形还原
    def process_review_segment(self):
        review_infile = CA_REVIEW_DATA_PATH
        review_outfile = REVIEW_DATA_PATH
        with open(review_infile, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            count = 0
            percent_notice = set(range(10, 101, 10))
            for item in data:
                text = item['text']
                # 进行文本分割
                tokens = word_tokenize(text)
                # 加载停用词
                stop_words = set(stopwords.words('english'))
                # 去除停用词
                filtered_texts = [word for word in tokens if word not in stop_words]
                # 获取标点符号
                punctuation = set(string.punctuation)
                # 去除标点符号
                clean_tokens = [word for word in filtered_texts if word not in punctuation]
                # 词形还原
                lemmatizer = WordNetLemmatizer()
                lemmatized_texts = [lemmatizer.lemmatize(word) for word in clean_tokens]
                # 去除词缀
                # 初始化 stemmer
                stemmer = PorterStemmer()
                # 去除词缀
                stemmed_texts = [stemmer.stem(word) for word in lemmatized_texts]
                # 统一大小写
                processed_texts = [word.lower() for word in stemmed_texts]
                # 还原成 string 形式
                processed_texts = ' '.join(processed_texts)
                item['text'] = processed_texts
                count += 1
                progress = (count * 100) // REVIEW_DOC_NUM
                if progress in percent_notice:
                    print(f"program has processed {int(progress)}% review file already.")
                    percent_notice.remove(progress)

        # 将 JSON 数据格式化输出到文件
        with open(review_outfile, 'w') as outfile:
            json.dump(data, outfile, indent=4)  # 使用indent=4进行格式化输出

    # 2.3 处理 user 文件，name 转成小写
    def process_user_segment(self):
        user_infile = CA_USER_DATA_PATH
        user_outfile = USER_DATA_PATH
        with open(user_infile, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            percent_notice = set(range(10, 101, 10))
            count = 0
            for item in data:
                # 将 name 转换为小写
                item['name'] = item['name'].lower()
                count += 1
                progress = (count * 100) // USER_DOC_NUM
                if progress in percent_notice:
                    print(f"program has processed {int(progress)}% user file already.")
                    percent_notice.remove(progress)

        # 将 JSON 数据格式化输出到文件
        with open(user_outfile, 'w') as outfile:
            json.dump(data, outfile, indent=4)  # 使用indent=4进行格式化输出

    def run(self):
        """
        Run the preprocessor to preprocess JSON files.
        Generate the preprocessed JSON files under DATA_DIR(`source/data/`)
        
        Args:
            DATA_DIR: data directory
            ORIGIN_REVIEW_DATA_PATH: original review data path
            ORIGIN_BUSINESS_DATA_PATH: original business data path
            REVIEW_DATA_PATH: preprocessed review data path
            BUSINESS_DATA_PATH: preprocessed business data
        """
        if USE_SKIP_PREPROCESSING and self.flag:
            print("Preprocessing has been executed previously")
        else:
            # 1.1 处理 business 文件
            # 记录开始时间
            start_time = time.time()
            business_id = self.create_business_dataset(ORIGIN_BUSINESS_DATA_PATH, 'CA')
            # 记录结束时间
            end_time1 = time.time()
            # 计算并打印运行时间
            print("program has extracted CA from business file already, using", end_time1 - start_time, "seconds")

            # 1.2 处理 review 文件
            print("CA review document starts:....")
            CA_user_id = self.create_review_dataset(ORIGIN_REVIEW_DATA_PATH, business_id)
            end_time2 = time.time()
            print("program has extracted CA from review file already, using", end_time2 - end_time1, "seconds")

            # 1.3 处理 user 文件
            print("CA user document starts:....")
            self.create_user_dataset(ORIGIN_USER_DATA_PATH, CA_user_id)
            end_time3 = time.time()
            print("program has extracted extract CA from user file already, using", end_time3 - end_time2, "seconds")

            # 2 对字段进行处理
            print("business document starts:....")
            self.process_business_segment()
            end_time4 = time.time()
            print("business done,using ", end_time4 - end_time3, "seconds")

            print("review document starts:....")
            self.process_review_segment()
            end_time5 = time.time()
            print("review done,using ",end_time5 - end_time4, "seconds")

            print("user document starts:....")
            self.process_user_segment()
            end_time6 = time.time()
            print("user done",end_time6 - end_time5, "seconds")
