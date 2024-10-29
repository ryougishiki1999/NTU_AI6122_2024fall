import os
from datetime import datetime
from enum import Enum

from whoosh.scoring import TF_IDF

search_engine_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(search_engine_dir))
INDEX_DIR = os.path.join(PROJECT_ROOT, 'out', 'indexdir')
DATA_DIR = os.path.join(PROJECT_ROOT, 'resource', 'data')
DATA_CA_DIR = os.path.join(DATA_DIR, 'CA')
DATA_PREPROCESS_DIR = os.path.join(DATA_DIR, 'preprocessed')
OUT_DIR = os.path.join(PROJECT_ROOT, 'out')
TMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')
INDEX_DIR_FLAG_FILE = os.path.join(OUT_DIR, 'index_flag.json')

ORIGIN_REVIEW_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_review.json')
ORIGIN_BUSINESS_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_business.json')
ORIGIN_USER_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_user.json')

CA_REVIEW_DATA_PATH = os.path.join(DATA_CA_DIR, 'CA_review.json')
CA_BUSINESS_DATA_PATH = os.path.join(DATA_CA_DIR, 'CA_business.json')
CA_USER_DATA_PATH = os.path.join(DATA_CA_DIR, 'CA_user.json')

REVIEW_DATA_PATH = os.path.join(DATA_PREPROCESS_DIR, 'review.json')
BUSINESS_DATA_PATH = os.path.join(DATA_PREPROCESS_DIR, 'business.json')
USER_DATA_PATH = os.path.join(DATA_PREPROCESS_DIR, 'user.json')

ORIGINAL_BUSINESS_DOC_NUM =150346
ORIGINAL_REVIEW_DOC_NUM=6990280
ORIGINAL_USER_DOC_NUM=1987897

REVIEW_DOC_NUM = 348855
BUSINESS_DOC_NUM = 5202
USER_DOC_NUM = 155947
TOTAL_DOC_NUM = REVIEW_DOC_NUM + BUSINESS_DOC_NUM + USER_DOC_NUM

formatted_created_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
result_file_name  = f"result_{formatted_created_time}.json"
RESULT_FILE_DIR = os.path.join(OUT_DIR, 'results')
RESULT_FILE_PATH = os.path.join(RESULT_FILE_DIR, result_file_name)

MIN_MAX_SEP = "/"
TOP_K = 10
INVALID_QUERY_ORDER = -1
SEARCHING_WEIGHTING = TF_IDF()
USE_SKIP_INDEX_BUILDING = True # True: use index already existed in INDEX_DIR, False: build index from scratch
USE_QUERY_STEMMING = True # for query_parser, True: use stemming, False: not use stemming
USE_QUERY_FUZZY = True # for query_parser, True: use fuzzy search, False: not use fuzzy search
USE_QUERY_PHRASE = False # for query_parser, True: use phrase search, False: not use phrase search


class IndexNames(Enum):
    REVIEWS = "reviews"
    BUSINESSES = "businesses"
    USERS = 'users'

class QueryType(Enum):
    BUSINESS = (["name","categories"], ["name", "categories", "business_id", "latitude", "longitude"])
    REVIEW = (["text"], ["text", "review_id", "user_id", "business_id"])
    GEOSPATIAL = (["latitude", "longitude"], ["latitude", "longitude", "name", "categories", "business_id"])
    REVIEW_SUMMARY_USER = (["user_id"], ["user_id", "business_id", "text"])
    REVIEW_SUMMARY_BUSINESS = (["business_id"], ["business_id", "longitude", "latitude"])
    ILLEGAL = []
    
QUERY_NON_STEMMING_FIELDS = [
    QueryType.BUSINESS.value[0][0],
]
