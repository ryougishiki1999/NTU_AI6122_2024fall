import os

search_engine_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(search_engine_dir))
INDEX_DIR = os.path.join(PROJECT_ROOT, 'out', 'indexdir')
DATA_DIR = os.path.join(PROJECT_ROOT, 'resource', 'data')

ORIGIN_REVIEW_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_review.json')
ORIGIN_BUSSIENESS_DATA_PATH = os.path.join(DATA_DIR, 'yelp_academic_dataset_business.json')

REVIEW_DATA_PATH = os.path.join(DATA_DIR, 'review.json')
BUSSIENESS_DATA_PATH = os.path.join(DATA_DIR, 'business.json')

