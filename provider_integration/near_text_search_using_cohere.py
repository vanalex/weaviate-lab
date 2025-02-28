import weaviate
from settings.settings import Settings
from weaviate.classes.config import Configure
import weaviate.classes.config as wc

settings = Settings()

# Recommended: save sensitive data as environment variables
headers = {
    "X-Cohere-Api-Key": settings.cohere_api_key,
}

client = weaviate.connect_to_local(headers=headers)
#client.collections.delete("DemoCollection")
if not client.collections.exists("DemoCollection"):
    client.collections.create(
        "DemoCollection",
        generative_config=Configure.Generative.cohere(
            model="command-r-plus"
        ),
        vectorizer_config=[
            Configure.NamedVectors.text2vec_cohere(
                name="title_vector",
                source_properties=["title"],
                model="embed-multilingual-light-v3.0"
            )
        ],
        properties = [
            wc.Property(name="title", data_type=wc.DataType.TEXT)
        ],
    )

collection = client.collections.get("DemoCollection")

source_objects = [
    {"title": "The Shawshank Redemption", "description": "A wrongfully imprisoned man forms an inspiring friendship while finding hope and redemption in the darkest of places."},
    {"title": "The Godfather", "description": "A powerful mafia family struggles to balance loyalty, power, and betrayal in this iconic crime saga."},
    {"title": "The Dark Knight", "description": "Batman faces his greatest challenge as he battles the chaos unleashed by the Joker in Gotham City."},
    {"title": "Jingle All the Way", "description": "A desperate father goes to hilarious lengths to secure the season's hottest toy for his son on Christmas Eve."},
    {"title": "A Christmas Carol", "description": "A miserly old man is transformed after being visited by three ghosts on Christmas Eve in this timeless tale of redemption."}
]

if len(collection) == 0:
    with collection.batch.dynamic() as batch:
        for src_obj in source_objects:
            # The model provider integration will automatically vectorize the object
            batch.add_object(
                properties={
                    "title": src_obj["title"],
                    "description": src_obj["description"],
                },
                # vector=vector  # Optionally provide a pre-obtained vector
            )
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break

    failed_objects = collection.batch.failed_objects
    if failed_objects:
        print(f"Number of failed imports: {len(failed_objects)}")
        print(f"First failed object: {failed_objects[0]}")


response = collection.generate.near_text(
    query="A holiday film",  # The model provider integration will automatically vectorize the query
    single_prompt="Translate this into French: {title}",
    limit=2
)

for obj in response.objects:
    print(obj.properties["title"])
    print(f"Generated output: {obj.generated}")  # Note that the generated output is per object

client.close()