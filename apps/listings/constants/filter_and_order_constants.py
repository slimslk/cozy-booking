# filter
PRICE_MIN = 'price_min'
PRICE_MAX = 'price_max'
LOCATION = 'location'
ROOMS = 'rooms'
APARTMENT_TYPE = 'apartment_type'
SEARCH = 'search'

# order
ORDER_PARAMETER = 'order'
PRICE_ASC_RANK = ('price_asc', 'price')
PRICE_DESC_RANK = ('price_desc', '-price')
CREATED_AT_ASC_RANK = ('created_at_asc', 'created_at')
CREATED_AT_DESC_RANK = ('created_at_desc', '-created_at')
VIEWS_ACS_RANK = ('views_asc', 'listing_views')
VIEWS_DESC_RANK = ('views_desc', '-listing_views')
RATING_ACS_RANK = ('rating_asc', 'rating')
RATING_DESC_RANK = ('rating_desc', '-rating')

# pagination
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
PAGE = 'page'
PAGE_SIZE = 'page_size'

FILTER_LIST_AND_PAGINATION = [
    PRICE_MIN,
    PRICE_MAX,
    LOCATION,
    ROOMS,
    APARTMENT_TYPE,
    SEARCH,
    PAGE,
    PAGE_SIZE
]
ORDER_LIST = [
    PRICE_ASC_RANK,
    PRICE_DESC_RANK,
    CREATED_AT_ASC_RANK,
    CREATED_AT_DESC_RANK,
    VIEWS_ACS_RANK,
    VIEWS_DESC_RANK,

]
FOREIGN_ORDER_LIST = [
    VIEWS_ACS_RANK[1],
    VIEWS_DESC_RANK[1],
    RATING_ACS_RANK[1],
    RATING_DESC_RANK[1],
]
VALUE_AS_NUMBER_LIST = [PRICE_MIN, PRICE_MAX, ROOMS, PAGE, PAGE_SIZE]

