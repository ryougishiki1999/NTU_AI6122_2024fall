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

ORIGINAL_BUSINESS_DOC_NUM = 150346
ORIGINAL_REVIEW_DOC_NUM = 6990280
ORIGINAL_USER_DOC_NUM = 1987897

REVIEW_DOC_NUM = 348855
BUSINESS_DOC_NUM = 5202
USER_DOC_NUM = 155947
TOTAL_DOC_NUM = REVIEW_DOC_NUM + BUSINESS_DOC_NUM + USER_DOC_NUM

formatted_created_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
result_file_name = f"result_{formatted_created_time}.json"
RESULT_FILE_DIR = os.path.join(OUT_DIR, 'results')
RESULT_FILE_PATH = os.path.join(RESULT_FILE_DIR, result_file_name)

REVIEW_SUMMARY_DISTRIBUTION_FILE_PATH = os.path.join(OUT_DIR, 'review_summary_distribution.png')

MIN_MAX_SEP = "/"
TOP_K = 10
INVALID_QUERY_ORDER = -1
SEARCHING_WEIGHTING = TF_IDF()
REVIEW_SUMMARY_USER_ID = "uBW16OCkFKvzdezUKZFuUQ"  # specific user_id for review summary
REVIEW_SUMMARY_RANDOM_REVIEW_COUNT_THRESHOLD = 10  # threshold for random user_id selection

USE_SKIP_PREPROCESSING = True  # True: use preprocessed data, False: build preprocessed data from scratch
USE_SKIP_INDEX_BUILDING = True  # True: use index already existed in INDEX_DIR, False: build index from scratch
USE_QUERY_STEMMING = True  # for query_parser, True: use stemming, False: not use stemming
# At least one of TERM, FUZZY and PHRASE must be True.
USE_QUERY_TERM = True  # for query_parser, True: use term search, False: not use term search
USE_QUERY_FUZZY = True  # for query_parser, True: use fuzzy search, False: not use fuzzy search
USE_QUERY_PHRASE = True  # for query_parser, True: use phrase search, False: not use phrase search
USE_REVIEW_SUMMARY_RANDOM_USER = False  # True: use random user_id for review summary, False: use specific user_id for review summary


class IndexNames(Enum):
    REVIEWS = "reviews"
    BUSINESSES = "businesses"
    USERS = 'users'


class QueryType(Enum):
    BUSINESS = (["name", "categories"], ["name", "categories", "business_id", "latitude", "longitude"])
    REVIEW = (["text"], ["text", "review_id", "user_id", "business_id"])
    GEOSPATIAL = (["latitude", "longitude"], ["latitude", "longitude", "name", "categories", "business_id"])
    REVIEW_SUMMARY_ALL_USERS = (["user_id"], [])
    REVIEW_SUMMARY_SPECIFIC_USER = (["user_id"], ["user_id", "business_id", "text"])
    REVIEW_SUMMARY_BUSINESS_ID = (["business_id"], ["business_id", "latitude", "longitude"])
    ILLEGAL = []


QUERY_NON_STEMMING_FIELDS = [
    QueryType.BUSINESS.value[0][0],
]

FACETS_QUERY_TYPES = [
    QueryType.REVIEW_SUMMARY_ALL_USERS,
]


def display_config():
    print("================= Search Engine Configuration ==================")
    print(f"USE_SKIP_PREPROCESSING: {USE_SKIP_PREPROCESSING}")
    print(f"USE_SKIP_INDEX_BUILDING: {USE_SKIP_INDEX_BUILDING}")
    print(f"USE_QUERY_STEMMING: {USE_QUERY_STEMMING}")
    print(f"USE_QUERY_TERM: {USE_QUERY_TERM}")
    print(f"USE_QUERY_FUZZY: {USE_QUERY_FUZZY}")
    print(f"USE_QUERY_PHRASE: {USE_QUERY_PHRASE}")
    print(f"USE_REVIEW_SUMMARY_RANDOM_USER: {USE_REVIEW_SUMMARY_RANDOM_USER}")
    if USE_REVIEW_SUMMARY_RANDOM_USER:
        print("REVIEW_SUMMARY_REVIEW_COUNT_THRESHOLD: ", REVIEW_SUMMARY_RANDOM_REVIEW_COUNT_THRESHOLD)
    if not USE_REVIEW_SUMMARY_RANDOM_USER:
        print(f"REVIEW_SUMMARY_USER_ID: {REVIEW_SUMMARY_USER_ID}")
