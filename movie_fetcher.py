from datetime import datetime
from typing import TypedDict

import weaviate

from settings.settings import Settings


class Movie(TypedDict):
    title: str
    overview: str
    release_date: datetime
    tmdb_id: int
    vote_average: float
    genre_ids: list[int]


settings = Settings()
# Get the collection
client = weaviate.connect_to_local(headers={"X-OpenAI-Api-Key": settings.openai_api_key})
movies = client.collections.get("Movie")

response = movies.query.fetch_objects(limit=2,
                                      return_properties=Movie)
client.close()
print(response)