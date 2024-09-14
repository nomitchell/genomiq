import chromadb
import cohere
import os

class Model():
    def __init__(self):
        chroma_client = chromadb.Client()
        self.collection = chroma_client.create_collection(name="main")
        self.co = cohere.Client(os.environ["COHERE_API_KEY"])

    def add_documents(self, documents):
        self.collection.add(
            documents=documents,
            ids=filenames
        )

    def run(self, query):
        response = co.chat(
            message="hello world!"
        )
        print(response)



