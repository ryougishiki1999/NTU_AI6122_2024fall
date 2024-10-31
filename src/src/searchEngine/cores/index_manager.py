from typing import Generator
import os
from enum import Enum
import json
import time

from whoosh import index
from whoosh.fields import Schema

from searchEngine.engine_config import INDEX_DIR, INDEX_DIR_FLAG_FILE,\
    BUSINESS_DOC_NUM, REVIEW_DOC_NUM, USER_DOC_NUM, \
        USE_SKIP_INDEX_BUILDING
        
from searchEngine.engine_config import IndexNames

class IndexManagerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IndexManagerSingleton, cls).__new__(cls)
            cls._instance._initialzie()
        return cls._instance
    
    def _load_indices_flags(self):
        with open(INDEX_DIR_FLAG_FILE, 'r') as f:
            self._indices_flags = json.load(f)
    
    def _update_indices_flags_file(self):
        with open(INDEX_DIR_FLAG_FILE, 'w') as f:
            json.dump(self._indices_flags, f)

    def _initialzie(self):
        self._indices = {}
        self._indices_flags = {} # key: index_name.value: str

        if not os.path.exists(INDEX_DIR):
            os.makedirs(INDEX_DIR)
        
        # help to check whether the index has been built,
        # targeting to skip the building process if the index has already existed
        if USE_SKIP_INDEX_BUILDING and os.path.exists(INDEX_DIR_FLAG_FILE):
            self._load_indices_flags()
            for index_name in IndexNames:
                self._indices_flags[index_name.value] &= index.exists_in(INDEX_DIR, indexname=index_name.value)
        else:
            for index_name in IndexNames:
                self._indices_flags[index_name.value] = False
        self._update_indices_flags_file()

    def create(self,
               index_name: IndexNames, schema: Schema):
        if self._indices_flags[index_name.value]:
            print(f"The index {index_name.value} has already existed.")
        else:
            print(f"Creating {index_name.value} index")
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
        def dump_doc_fields(doc):
            match index_name:
                case IndexNames.REVIEWS:
                    doc['date'] = json.dumps(doc['date'])
                case IndexNames.BUSINESSES:
                    # 处理 hours 字段
                    if 'hours' in doc:
                        doc['hours'] = json.dumps(doc['hours'])
                    # 处理 'attributes' 字段
                    if 'attributes' in doc:
                        doc['attributes'] = json.dumps(doc['attributes'])
                    # solve the 'categories' field
                    if 'categories' in doc:
                        doc['categories'] = json.dumps(doc['categories'])
                case IndexNames.USERS:
                    if 'yelping_since' in doc:
                        doc['yelping_since'] = json.dumps(doc['yelping_since'])
                    if 'friends' in doc:
                        doc['friends'] = json.dumps(doc['friends'])
                    if 'elite' in doc:
                        doc['elite'] = json.dumps(','.join(map(str, doc['elite'])))
            return doc
        
        def compute_ten_percent(index_name):
            match index_name:
                case IndexNames.REVIEWS:
                    return REVIEW_DOC_NUM // 10 + 1
                case IndexNames.BUSINESSES:
                    return BUSINESS_DOC_NUM // 10 + 1
                case IndexNames.USERS:
                    return USER_DOC_NUM // 10 + 1
        
        if self._indices_flags[index_name.value]:
            print(f"The index {index_name.value} has already been built. It's unnecessary to add documents again.")
        else:
            ix = self.open(index_name)
            ten_percent = compute_ten_percent(index_name)
            
            writer = ix.writer()
            percent_count = 1
            print(f"Start building {index_name.value} index")
            start_time = percent_start_time =  time.time()
            for doc_count, doc in enumerate(documents):
                doc = dump_doc_fields(doc)
                writer.add_document(**doc)
                if doc_count == ten_percent * percent_count:
                    percent_end_time = time.time()
                    print(f"Added {percent_count * 10}% = {doc_count} documents to {index_name.value} index: Time cost: {percent_end_time - percent_start_time:.2f} seconds")
                    percent_count += 1
                    percent_start_time = time.time()
            percent_end_time = time.time()
            print(f"Added total 100% = {doc_count} documents to {index_name.value} index: Time cost: {percent_end_time - percent_start_time:.2f} seconds")
            print("Writer starts commit")
            commit_start_time = time.time()
            writer.commit()
            commit_end_time = time.time()
            print(f"Writer finishes commit to {index_name.value} index: Time cost: {commit_end_time - commit_start_time:.2f} seconds")
            end_time = time.time()
            print(f"Complete building {index_name.value} index, Time cost: {end_time - start_time:.2f} seconds")
            
            # update the index dir flag
            self._indices_flags[index_name.value] = True
            with open(INDEX_DIR_FLAG_FILE, 'w') as f:
                json.dump(self._indices_flags, f)
