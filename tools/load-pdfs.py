import os

os.environ["OPENAI_API_KEY"] = "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"
     
from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)
     
query_engine = index.as_query_engine()
print(query_engine.query("Could you summarize the given context? Return your response which covers the key points of the text and does not miss anything important, please."))
     
# Persist index to disk
index.storage_context.persist("data\pdfs_index")

from llama_index import StorageContext, load_index_from_storage

# Rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="data\pdfs_index")

# Load index from the storage context
new_index = load_index_from_storage(storage_context)

new_query_engine = new_index.as_query_engine()
response = new_query_engine.query("who is this text about?")
print(response)