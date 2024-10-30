"""
A demo for creating a Whoosh index from a JSON file and searching it,
indicating the basic workflow of our search engine, including desgining schema, creating index, and generating query and searching.

For convenience, just load 1000 json lines from the file "yelp_academic_dataset_review.json" to create the index, 
which means 1000 indexed documents. 
Adopt the TF-IDF as our scoring function to search the index with the query "wonderful AND experience".
"""
import json
from decimal import Decimal

from whoosh import index
from whoosh.query import And
from whoosh.query import NumericRange

from searchEngine.engine_config import INDEX_DIR, IndexNames, QueryType

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
    results = searcher.search(query, limit=5, scored=True, groupedby=None)
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
            # result_dict[snippet_name] = hit[snippet_name]
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

from whoosh.query import Term

print("\n\n")

user_id = "uBW16OCkFKvzdezUKZFuUQ"
user_id_query = Term('user_id', user_id)

query
ix = index.open_dir(INDEX_DIR, indexname=IndexNames.REVIEWS.value)
with ix.searcher() as searcher:
    results = searcher.search(user_id_query, limit=None, groupedby=None)
    print(results)
    result_dict_list = []
    for i, hit in enumerate(results):
        result_dict = {}
        for snippet_name in QueryType.REVIEW.value[1]:
            result_dict[snippet_name] = hit[snippet_name]
        result_dict_list.append(result_dict)

print('\n')
from whoosh import sorting
from whoosh.sorting import MultiFacet
from whoosh.query import Every

user_id_facet = sorting.FieldFacet('user_id')
facets = sorting.Facets()
facets.add_field('user_id')
facets.add_field('business_id')
facets.add_facet("user_business", MultiFacet(['user_id', 'business_id']))
# facets.add_facet('user_id', user_id_facet)
print(list(facets.items())[0][0])
print(facets.items()[0])
exit(0)
query = Every(fieldname='user_id')
ix = index.open_dir(INDEX_DIR, indexname=IndexNames.REVIEWS.value)
review_num_of_user_id_dict = {}
with ix.searcher() as searcher:
    results = searcher.search(query, limit=None, groupedby=facets)
    print(results)
    for facet_name, _ in facets.items():
        groups = results.groups(facet_name)
        # print(groups)
        for user_id, hits in groups.items():
            count = len(hits)
            print(f"user_id: {user_id}, count: {count}")
            review_num_of_user_id_dict[user_id] = count
    # print(results)
    # result_dict_list = []
    # for i, hit in enumerate(results):
    #     result_dict = {}
    #     print(hit)
print(len(review_num_of_user_id_dict))
max_key = max(review_num_of_user_id_dict, key=review_num_of_user_id_dict.get)
print(f"user_id: {max_key}, count: {review_num_of_user_id_dict[max_key]}")
min_key = min(review_num_of_user_id_dict, key=review_num_of_user_id_dict.get)
print(f"user_id: {min_key}, count: {review_num_of_user_id_dict[min_key]}")
