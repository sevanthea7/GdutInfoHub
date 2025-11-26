from volcenginesdkarkruntime import Ark
from src.crawler.LLM_api.api_keys import get_api_key
API_KEY = get_api_key()
client = Ark(
    api_key=API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)