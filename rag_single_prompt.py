import os
import weaviate

from settings.settings import Settings

settings = Settings()
# Get the collection
client = weaviate.connect_to_local(headers={"X-OpenAI-Api-Key": settings.openai_api_key})


# Get the collection
movies = client.collections.get("Movie")

# Perform query
response = movies.generate.near_text(
    query="dystopian future",
    limit=5,
    single_prompt="Translate this into French: {title}"
)

# Inspect the response
for o in response.objects:
    print(o.properties["title"])  # Print the title
    print(o.generated)  # Print the generated text (the title, in French)

client.close()