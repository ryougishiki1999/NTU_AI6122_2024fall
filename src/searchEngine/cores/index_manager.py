from datetime import datetime
import shutil
from typing import Generator
import os
from enum import Enum
import json
import time

from whoosh import index
from whoosh.fields import Schema
from whoosh.writing import BufferedWriter

from searchEngine.engine_config import INDEX_DIR, INDEX_BUFFER_SIZE, INDEX_BUFFER_PERIOD


class IndexNames(Enum):
    REVIEWS = "reviews"
    BUSINESSES = "businesses"
    USERS = 'users'


class IndexManagerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IndexManagerSingleton, cls).__new__(cls)
            cls._instance._initialzie()
        return cls._instance

    def _initialzie(self):
        self._indices = {}
        if os.path.exists(INDEX_DIR):
            shutil.rmtree(INDEX_DIR)
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
            if index_name == IndexNames.REVIEWS:
                # 将日期字符串转换为 datetime 对象
                doc['date'] = datetime.strptime(doc['date'], '%Y-%m-%d %H:%M:%S')
            elif index_name == IndexNames.BUSINESSES:
                # 处理 hours 字段
                if 'hours' in doc:
                    doc['hours'] = json.dumps(doc['hours'])
                # 处理 'attributes' 字段
                if 'attributes' in doc:
                    doc['attributes'] = json.dumps(doc['attributes'])
                # solve the 'categories' field
                if 'categories' in doc:
                    doc['categories'] = json.dumps(doc['categories'])
            elif index_name == IndexNames.USERS:
                if 'yelping_since' in doc:
                    doc['yelping_since'] = datetime.strptime(doc['yelping_since'], '%Y-%m-%d %H:%M:%S')
                if 'friends' in doc:
                    doc['friends'] = json.dumps(doc['friends'])
                if 'elite' in doc:
                    doc['elite'] = ','.join(map(str, doc['elite']))
            return doc

        ix = self.open(index_name)
        start_time = time.time()
        # TODO: BufferedWriter may be better, but it can't work in expected way.
        # I don't know why.
        # TODO: load review.json too slow, need to optimize
        writer = ix.writer(buffering=INDEX_BUFFER_SIZE)
        for count, doc in enumerate(documents):
            doc = _doc_process(doc)
            writer.add_document(**doc)
            if count % INDEX_BUFFER_SIZE == 0 and count > 0:
                print(f"Added {count} documents to {index_name.value} index")
        writer.commit()
        end_time = time.time()
        print(f"Added {count} documents to {index_name.value} index, Time cost: {end_time - start_time:.2f} seconds")