from weaviate import WeaviateClient

from settings.settings import Settings
import weaviate

def get_weaviate_client() -> WeaviateClient:
    settings = Settings()
    return weaviate.connect_to_local(headers={"X-OpenAI-Api-Key": settings.openai_api_key})
