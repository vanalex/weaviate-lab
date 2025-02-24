import weaviate
import weaviate.classes.query as wq
import os

from settings.settings import Settings

settings = Settings()
# Get the collection
client = weaviate.connect_to_local(headers={"X-OpenAI-Api-Key": settings.openai_api_key})
movies = client.collections.get("Movie")


# Get the collection
movies = client.collections.get("Movie")

# Perform query
response = movies.query.bm25(
    query="history", limit=5, return_metadata=wq.MetadataQuery(score=True)
)

# Inspect the response
for o in response.objects:
    print(
        o.properties["title"], o.properties["release_date"].year
    )  # Print the title and release year (note the release date is a datetime object)
    print(
        f"BM25 score: {o.metadata.score:.3f}\n"
    )  # Print the BM25 score of the object from the query

client.close()