import weaviate.classes.config as wc
from datetime import datetime, timezone
import weaviate
import pandas as pd
import requests
import json
from tqdm import tqdm
from weaviate.util import generate_uuid5

from settings.settings import Settings

settings = Settings()

client = weaviate.connect_to_local(headers={"X-OpenAI-Api-Key": settings.openai_api_key})
try:
    assert client.is_live()
    metainfo = client.get_meta()
    print(json.dumps(metainfo, indent=2))

    if not (client.collections.exists("Movie")):
        client.collections.create(
            name="Movie",
            properties=[
                wc.Property(name="title", data_type=wc.DataType.TEXT),
                wc.Property(name="overview", data_type=wc.DataType.TEXT),
                wc.Property(name="vote_average", data_type=wc.DataType.NUMBER),
                wc.Property(name="genre_ids", data_type=wc.DataType.INT_ARRAY),
                wc.Property(name="release_date", data_type=wc.DataType.DATE),
                wc.Property(name="tmdb_id", data_type=wc.DataType.INT),
            ],
            # Define the vectorizer module
            vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
            # Define the generative module
            generative_config=wc.Configure.Generative.openai()
    )

    data_url = "https://raw.githubusercontent.com/weaviate-tutorials/edu-datasets/main/movies_data_1990_2024.json"
    resp = requests.get(data_url)
    df = pd.DataFrame(resp.json())

    # Get the collection
    movies = client.collections.get("Movie")

    # Enter context manager
    with movies.batch.dynamic() as batch:
        # Loop through the data
        for i, movie in tqdm(df.iterrows()):
            # Convert data types
            # Convert a JSON date to `datetime` and add time zone information
            release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d").replace(
                tzinfo=timezone.utc            )
            # Convert a JSON array to a list of integers
            genre_ids = json.loads(movie["genre_ids"])

            # Build the object payload
            movie_obj = {
                "title": movie["title"],
                "overview": movie["overview"],
                "vote_average": movie["vote_average"],
                "genre_ids": genre_ids,
                "release_date": release_date,
                "tmdb_id": movie["id"],
            }

            # Add object to batch queue
            batch.add_object(
                properties=movie_obj,
                uuid=generate_uuid5(movie["id"])
                # references=reference_obj  # You can add references here
            )
            # Batcher automatically sends batches

    # Check for failed objects
    if len(movies.batch.failed_objects) > 0:
        print(f"Failed to import {len(movies.batch.failed_objects)} objects")

finally:
    client.close()
