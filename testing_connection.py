import weaviate

client = weaviate.connect_to_local()

print(client.is_ready())
print(client.get_meta())
client.close()