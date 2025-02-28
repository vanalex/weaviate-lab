from datetime import datetime
from typing import TypedDict

import weaviate

from settings.settings import Settings
from utils.weaviate import get_weaviate_client


class Movie(TypedDict):
    title: str
    overview: str
    #release_date: datetime
    tmdb_id: int
    vote_average: float
    genre_ids: list[int]



client = get_weaviate_client()
movies = client.collections.get("Movie")

response = movies.query.fetch_objects(limit=2,return_properties=Movie)
client.close()
print(response)