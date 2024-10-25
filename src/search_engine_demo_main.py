"""
A demo for creating a Whoosh index from a JSON file and searching it,
indicating the basic workflow of our search engine, including desgining schema, creating index, and generating query and searching.

For convenience, just load 1000 json lines from the file "yelp_academic_dataset_review.json" to create the index, 
which means 1000 indexed documents. 
Adopt the TF-IDF as our scoring function to search the index with the query "wonderful AND experience".
"""

import ijson
from whoosh.fields import SchemaClass
from whoosh.fields import ID, TEXT, DATETIME, NUMERIC
from whoosh.analysis import StemmingAnalyzer

import os, os.path
from whoosh import index
from whoosh.writing import AsyncWriter
from datetime import datetime

from searchEngine.engine_config import ORIGIN_REVIEW_DATA_PATH, TMP_DIR

# design schema
class ReviewSchema(SchemaClass):
    """
    Schema for the reviews index.
    """
    review_id = ID(stored=True, unique=True)
    user_id = ID(stored=True)
    business_id = ID(stored=True)
    stars = NUMERIC(stored=True, decimal_places=2)
    date = DATETIME(stored=True)
    text = TEXT(analyzer=StemmingAnalyzer(), stored=True)
    useful = NUMERIC(stored=True,decimal_places=0)
    funny = NUMERIC(stored=True,decimal_places=0)
    cool = NUMERIC(stored=True,decimal_places=0) 

index_dir = os.path.join(TMP_DIR, 'indexdir')
if not os.path.exists(index_dir):
    os.makedirs(index_dir)

if index.exists_in(index_dir, indexname="usages"):
    print("The index usages has already existed.")
else:
    # create index
    print("Creating index...")
    ix = index.create_in(index_dir, schema=ReviewSchema, indexname="usages")
    # create_in will delete the existing index with the same name
    ix2 = index.create_in(index_dir, ReviewSchema, indexname='test')

    json_file_path = ORIGIN_REVIEW_DATA_PATH
    num_lines_to_index = 1000

    with open(json_file_path, 'r', encoding='utf-8') as f:
        writer = AsyncWriter(ix)
        for i, line in enumerate(f):
            if i >= num_lines_to_index:
                break
            
            review = next(ijson.items(line, ''))
            
            writer.add_document(
                review_id=review['review_id'],
                user_id=review['user_id'],
                business_id=review['business_id'],
                stars=review['stars'],
                date=datetime.strptime(review['date'], '%Y-%m-%d %H:%M:%S'),
                text=review['text'],
                useful=review['useful'],
                funny=review['funny'],
                cool=review['cool']
            )
        writer.commit()
    print("After writer commit, Index created.")

# # to test whether able to directly open the index 
# # when the same name index has been created
# ix = index.open_dir(index_dir, indexname="usages")

# generate query
from whoosh.qparser import QueryParser
ix = index.open_dir(index_dir, indexname="usages")
parser = QueryParser("text", ix.schema)
query = parser.parse("wonderful AND experience")

# execute search and scoring and sorting
from whoosh.scoring import TF_IDF

with ix.searcher(weighting = TF_IDF()) as searcher:
    results = searcher.search(query, limit=5)
    print(results)
    # for i, hit in enumerate(results):
    #     print(f"top-{i+1}: ",hit,'\n')
    for i in range(results.scored_length()):
        print(f"top-{i+1}: ", results[i], '\n')
