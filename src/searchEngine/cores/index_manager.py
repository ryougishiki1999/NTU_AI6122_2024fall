from datetime import datetime
from typing import Generator
import os
from enum import Enum

from whoosh import index
from whoosh.fields import Schema
from whoosh.writing import AsyncWriter

from searchEngine.engine_config import INDEX_DIR


class IndexNames(Enum):
    REVIEWS = "reviews"
    BUSINESSES = "businesses"

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
            
    def create(self, \
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

    def add_documents(self, index_name: IndexNames\
        ,documents: Generator):
        def _doc_process(doc):
            match index_name:
                case IndexNames.REVIEWS:
                    doc['date'] = datetime.strptime(doc['date'], '%Y-%m-%d %H:%M:%S')
                case IndexNames.BUSINESSES:
                    # TODO, JSON item(documents) form Bussiness.json
                    # may need to be processed to fit the schema
                    pass
            return doc
        
        ix = self.open(index_name)
        with AsyncWriter(ix) as writer:
            for count, doc in enumerate(documents):
                # tmp: For test convinience,
                # limit the number of documents to be added
                if count >= 1000:
                    break
                # tmp
                doc = _doc_process(doc)
                writer.add_document(**doc)
            print(f"Added {count} documents to {index_name.value} index")
            

        