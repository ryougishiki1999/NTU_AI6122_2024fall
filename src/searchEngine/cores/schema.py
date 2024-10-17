from whoosh.fields import ID, TEXT, KEYWORD, DATETIME, NUMERIC
from whoosh.fields import SchemaClass

class ReviewSchema(SchemaClass):
    """
    Schema for the reviews index.
    """
    review_id = ID(stored=True, unique=True)
    user_id = ID(stored=True)
    business_id = ID(stored=True)
    stars = NUMERIC(stored=True, decimal_places=2)
    date = DATETIME(stored=True)
    text = TEXT(stored=True)
    useful = NUMERIC(stored=True,decimal_places=0)
    funny = NUMERIC(stored=True,decimal_places=0)
    cool = NUMERIC(stored=True,decimal_places=0)
    
class Bussiness(SchemaClass):
    """TODO:
    Schema for the business index.
    """
    pass