import requests
from configuration.settings import settings
# from loguru import logger


def openai_embedding(input):
    api = 'https://api.openai.com/v1/embeddings'
    headers = {"Authorization": "Bearer " + settings.OPENAI_API_KEY,
               "Content-Type": "application/json"}
    payload = {
        "input": input,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    }
    embedding = requests.post(api, headers=headers, json=payload)
    return embedding
