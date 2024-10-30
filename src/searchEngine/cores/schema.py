from whoosh.analysis import StemmingAnalyzer, LowercaseFilter
from whoosh.fields import ID, TEXT, NUMERIC, STORED
from whoosh.fields import SchemaClass


class ReviewSchema(SchemaClass):
    """
    Schema for the reviews index.
    """
    review_id  = STORED()
    user_id = ID(stored=True)
    business_id = STORED()
    stars = STORED()
    date = STORED()
    text = TEXT(stored=True, phrase=True, analyzer=StemmingAnalyzer()|LowercaseFilter())
    useful = STORED()
    funny = STORED()
    cool = STORED()


class BusinessSchema(SchemaClass):
    """Schema for the business index."""
    
    business_id = ID(stored=True)
    name = TEXT(stored=True, phrase=True)
    address = STORED()
    city = STORED()
    state = STORED()
    postal_code = STORED()
    latitude = NUMERIC(stored=True, decimal_places=4)
    longitude = NUMERIC(stored=True, decimal_places=4)
    stars = STORED()
    review_count = STORED()
    is_open = STORED()
    attributes = STORED()
    categories = TEXT(stored=True, phrase=True, analyzer=StemmingAnalyzer()|LowercaseFilter())
    hours = STORED()

class UserSchema(SchemaClass):
    """Schema for the user index."""
    user_id = ID(stored=True)
    name = TEXT(stored=True, phrase=True)
    review_count = STORED()
    yelping_since = STORED()
    friends = STORED()
    useful = STORED()
    funny = STORED()
    cool = STORED()
    fans = STORED()
    elite = STORED()
    average_stars = STORED()
    compliment_hot = STORED()
    compliment_more = STORED()
    compliment_profile = STORED()
    compliment_cute = STORED()
    compliment_list = STORED()
    compliment_note = STORED()
    compliment_plain = STORED()
    compliment_cool = STORED()
    compliment_funny = STORED()
    compliment_writer = STORED()
    compliment_photos = STORED()