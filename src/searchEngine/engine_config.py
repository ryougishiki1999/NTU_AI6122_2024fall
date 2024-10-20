import os

search_engine_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(search_engine_dir))
INDEX_DIR = os.path.join(PROJECT_ROOT, 'out', 'indexdir')
DATA_DIR = os.path.join(PROJECT_ROOT, 'resource', 'data')
DATA_CA_DIR = os.path.join(DATA_DIR, 'CA')
DATA_PREPROCESS_DIR = os.path.join(DATA_DIR, 'preprocess')
OUT_DIR = os.path.join(PROJECT_ROOT, 'out')
TMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')

ORIGIN_REVIEW_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_review.json')
ORIGIN_BUSINESS_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_business.json')
ORIGIN_USER_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_user.json')

CA_REVIEW_DATA_PATH = os.path.join(DATA_CA_DIR, 'CA_review.json')
CA_BUSINESS_DATA_PATH = os.path.join(DATA_CA_DIR, 'CA_business.json')
CA_USER_DATA_PATH = os.path.join(DATA_CA_DIR, 'CA_user.json')

REVIEW_DATA_PATH = os.path.join(DATA_PREPROCESS_DIR, 'review.json')
BUSINESS_DATA_PATH = os.path.join(DATA_PREPROCESS_DIR, 'business.json')
USER_DATA_PATH = os.path.join(DATA_PREPROCESS_DIR, 'user.json')


INDEX_BUFFER_SIZE = 5000
INDEX_BUFFER_PERIOD = 1 # not use right now
REVIEW_DOC_NUM = 348855
BUSINESS_DOC_NUM = 5202