from whoosh.fields import ID, TEXT, KEYWORD, DATETIME, NUMERIC, BOOLEAN, NGRAM
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
    useful = NUMERIC(stored=True, decimal_places=0)
    funny = NUMERIC(stored=True, decimal_places=0)
    cool = NUMERIC(stored=True, decimal_places=0)

class BusinessSchema(SchemaClass):
    """Schema for the business index."""

    business_id = ID(stored=True, unique=True)  # Unique identifier
    # Business name
    name = TEXT(stored=True)  # Name of the business
    address = TEXT(stored=True)  # Address of the business
    city = TEXT(stored=True)  # City where the business is located
    state = NGRAM(stored=True)  # 2 character state code
    postal_code = TEXT(stored=True)  # Postal code of the business
    latitude = NUMERIC(stored=True)  # Latitude coordinate
    longitude = NUMERIC(stored=True)  # Longitude coordinate

    # Star rating (rounded to half-stars)
    stars = NUMERIC(stored=True)  # Star rating of the business
    review_count = NUMERIC(stored=True, decimal_places=0)  # Count of reviews for the business
    is_open = BOOLEAN(stored=True)  # 0 or 1 indicating closed or open
    attributes = TEXT(stored=True)  # Attributes of the business stored as JSON string
    categories = KEYWORD(stored=True, commas=True)  # Categories as a comma-separated string
    # Business hours
    hours = DATETIME(stored=True)  # Operating hours stored as JSON string
