import weaviate
import weaviate.classes.query as wq
from settings.settings import Settings


settings = Settings()
# Get the collection
client = weaviate.connect_to_local(headers={"X-OpenAI-Api-Key": settings.openai_api_key})
movies = client.collections.get("Movie")

# Perform query
response = movies.query.near_text(
    query="dystopian future",
    limit=20,
    distance=0.6,
    return_metadata=wq.MetadataQuery(distance=True)
)
print(len(response.objects))
# Inspect the response
for o in response.objects:
    print(
        o.properties["title"], o.properties["release_date"].year
    )  # Print the title and release year (note the release date is a datetime object)
    print(
        f"Distance to query: {o.metadata.distance:.3f}\n"
    )  # Print the distance of the object from the query