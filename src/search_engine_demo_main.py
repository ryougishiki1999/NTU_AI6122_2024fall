"""
A demo for creating a Whoosh index from a JSON file and searching it,
indicating the basic workflow of our search engine, including desgining schema, creating index, and generating query and searching.

For convenience, just load 1000 json lines from the file "yelp_academic_dataset_review.json" to create the index, 
which means 1000 indexed documents. 
Adopt the TF-IDF as our scoring function to search the index with the query "wonderful AND experience".
"""
from ast import And, Index, dump
from decimal import Decimal
import json
from unittest import result
import ijson
from numpy import long
from whoosh.fields import SchemaClass
from whoosh.fields import ID, TEXT, DATETIME, NUMERIC, STORED
from whoosh.analysis import StemmingAnalyzer

import os, os.path
from whoosh import index
from whoosh.writing import AsyncWriter
from datetime import datetime

from searchEngine.engine_config import INDEX_DIR, ORIGIN_REVIEW_DATA_PATH, TMP_DIR, IndexNames, QueryType

# design schema
# class UsageSchema(SchemaClass):
#     """
#     Schema for the reviews index.
#     """
#     review_id = ID(stored=True, unique=True)
#     user_id = ID(stored=True)
#     business_id = ID(stored=True)
#     stars = NUMERIC(stored=True, decimal_places=2)
#     date = STORED()
#     text = TEXT(analyzer=StemmingAnalyzer(), stored=True)
#     useful = NUMERIC(stored=True,decimal_places=0)
#     funny = NUMERIC(stored=True,decimal_places=0)
#     cool = NUMERIC(stored=True,decimal_places=0) 

# index_dir = os.path.join(TMP_DIR, 'indexdir')
# if not os.path.exists(index_dir):
#     os.makedirs(index_dir)

# if index.exists_in(index_dir, indexname="usages"):
#     print("The index usages has already existed.")
# else:
#     # create index
#     print("Creating index...")
#     ix = index.create_in(index_dir, schema=UsageSchema, indexname="usages")
#     # create_in will delete the existing index with the same name
#     ix2 = index.create_in(index_dir, UsageSchema, indexname='test')

#     json_file_path = ORIGIN_REVIEW_DATA_PATH
#     num_lines_to_index = 1000

#     with open(json_file_path, 'r', encoding='utf-8') as f:
#         writer = AsyncWriter(ix)
#         for i, line in enumerate(f):
#             if i >= num_lines_to_index:
#                 break
            
#             review = next(ijson.items(line, ''))
            
#             writer.add_document(
#                 review_id=review['review_id'],
#                 user_id=review['user_id'],
#                 business_id=review['business_id'],
#                 stars=review['stars'],
#                 date=datetime.strptime(review['date'], '%Y-%m-%d %H:%M:%S'),
#                 text=review['text'],
#                 useful=review['useful'],
#                 funny=review['funny'],
#                 cool=review['cool']
#             )
#         writer.commit()
#     print("After writer commit, Index created.")

# # # to test whether able to directly open the index 
# # # when the same name index has been created
# # ix = index.open_dir(index_dir, indexname="usages")

# # generate query
# from whoosh.qparser import QueryParser, MultifieldParser
# from whoosh.query import Term, And, Or, Not, Phrase

# ix = index.open_dir(index_dir, indexname="usages")
# parser = MultifieldParser(["text", "useful"],UsageSchema())
# #parser = QueryParser("text",UsageSchema())
# query = parser.parse("wonderful experience")
# #query = Phrase("text","wonderful")
# # print(parser.schema)
# # print(parser.fieldname)
# # parser.parse(query)
# # print(str(query))
# # print(json.dumps(str(query)))

# # execute search and scoring and sorting
# from whoosh.scoring import TF_IDF

# with ix.searcher(weighting = TF_IDF()) as searcher:
#     results = searcher.search(query, limit=5)
#     for i, hit in enumerate(results):
#         print(json.dumps(str(dict(hit))))
#     # for i, hit in enumerate(results):
#     #     # print(f"top-{i+1}: ",hit,'\n')
#     #     print(json.dumps(dict(hit)))
#     # for i in range(results.scored_length()):
#     #     print(f"top-{i+1}: ", results[i], '\n')

from whoosh.query import NumericRange
from whoosh.query import And



ix = index.open_dir(INDEX_DIR, indexname=IndexNames.BUSINESSES.value)

# with ix.searcher() as searcher:
#     #for docnum in range(searcher.doc_count()):
#         #doc = searcher.stored_fields(docnum)
#     docs = searcher.documents()
#     for i, doc in enumerate(docs):
#         if i > 100:
#             break
#         print(doc['latitude'], type(doc['latitude']))
#         print(doc['longitude'], type(doc['longitude']))

latitude_range_query = NumericRange(fieldname='latitude', start=Decimal(34), end=Decimal(36))
longitude_range_query = NumericRange(fieldname='longitude', start=Decimal(-120), end=Decimal(-118))
snippet_names = QueryType.BUSINESS.value[1]
query = And([latitude_range_query, longitude_range_query])

from whoosh.scoring import TF_IDF

with ix.searcher(weighting=TF_IDF()) as searcher:
    results = searcher.search(query, limit=5, scored=True)
    print(results)
    result_dict_list = []
    for i, hit in enumerate(results):
        # print(hit.docnum)
        # print(hit.score)
        # print(hit['latitude'])
        # print(hit["name"])
        result_dict = {}
        for snippet_name in snippet_names:
            if isinstance(hit[snippet_name], Decimal):
                result_dict[snippet_name] = float(hit[snippet_name])
            else:
                result_dict[snippet_name] = hit[snippet_name]
            #result_dict[snippet_name] = hit[snippet_name]
        result_dict_list.append(result_dict)

result_dict_list = json.loads(json.dumps(result_dict_list))
print(result_dict_list)

json_data = {
    "query_data": str(query),
    "results": result_dict_list
}

with open('tmp/result_tmp.json', 'w') as f:
    json.dump(json_data, f)
    f.write('\n')
        
