from datetime import datetime
from typing import Generator
import os
from enum import Enum

from whoosh import index
from whoosh.fields import Schema
class IndexNames(Enum):
    REVIEWS = "reviews"
    BUSINESSES = "businesses"

from whoosh.writing import AsyncWriter


from src.searchEngine.engine_config import INDEX_DIR

def parse_hours(hours):
    # 示例: 假设 hours 是一个字典或字符串
    if isinstance(hours, dict):
        # 如果 hours 是字典，直接返回
        return hours
    elif isinstance(hours, str):
        # 假设 hours 是字符串格式，进行简单的解析
        return {"open": hours.split('-')[0], "close": hours.split('-')[1]}
    return None  # 如果不符合格式，返回 None

class IndexManagerSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IndexManagerSingleton, cls).__new__(cls)
            cls._instance._initialzie()
        return cls._instance
    
    def _initialzie(self):
        self._indices = {}
        if not os.path.exists(INDEX_DIR):
            os.makedirs(INDEX_DIR)
            
    def create(self,
        index_name: IndexNames, schema: Schema):
        ix = index.create_in(
            INDEX_DIR,
            schema=schema,
            indexname=index_name.value
        )
        self._indices[index_name] = ix
        
    def open(self, index_name: IndexNames):
        self._indices[index_name] = index.open_dir(
            INDEX_DIR,
            indexname=index_name.value
        )
        return self._indices[index_name]

    def add_documents(self, index_name: IndexNames, documents: Generator):
        def _doc_process(doc):
            print(f"Original document: {doc}")  # 打印原始文档，用于调试
            if index_name == IndexNames.REVIEWS:
                # 将日期字符串转换为 datetime 对象
                doc['date'] = datetime.strptime(doc['date'], '%Y-%m-%d %H:%M:%S')
            elif index_name == IndexNames.BUSINESSES:
                # 处理 hours 字段
                if 'hours' in doc:
                    doc['hours'] = parse_hours(doc['hours'])
                # 处理 'ByAppointmentOnly' 字段
                if 'ByAppointmentOnly' in doc:
                    # 如果字段是字典，提取值；如果是字符串，直接使用
                    if isinstance(doc['ByAppointmentOnly'], dict):
                        doc['ByAppointmentOnly'] = str(doc['ByAppointmentOnly'].get('ByAppointmentOnly', 'False'))
                    else:
                        doc['ByAppointmentOnly'] = str(doc['ByAppointmentOnly'])
            return doc

        ix = self.open(index_name)
        with AsyncWriter(ix) as writer:
            for count, doc in enumerate(documents):
                # tmp: For test convenience,
                # limit the number of documents to be added
                if count >= 1000:
                    break
                # tmp
                doc = _doc_process(doc)
                writer.add_document(**doc)
            print(f"Added {count} documents to {index_name.value} index")
            

        