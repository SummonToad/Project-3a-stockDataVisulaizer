import os

# Uses the ALPHAVANTAGE_API_KEY environment variable if set, otherwise the hardcoded key.
# "or" (instead of a default argument) also covers Docker passing in an empty value.
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY") or "4I9DKK4J58SKMY98"
BASE_URL = "https://www.alphavantage.co/query"
REQUEST_TIMEOUT = 30  # seconds