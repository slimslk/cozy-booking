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
ORDER_LIST = [PRICE_ASC_RANK, PRICE_DESC_RANK, CREATED_AT_ASC_RANK, CREATED_AT_DESC_RANK]
VALUE_AS_NUMBER_LIST = [PRICE_MIN, PRICE_MAX, ROOMS, PAGE, PAGE_SIZE]

