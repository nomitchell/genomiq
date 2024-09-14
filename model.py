import chromadb
import cohere
import os
import re

class Model():
    def __init__(self):
        chroma_client = chromadb.Client()
        self.collection = chroma_client.create_collection(name="main")
        self.co = cohere.Client(os.environ["COHERE_API_KEY"])

        with open("prompts/generate.txt", 'r') as f:
            self.generate_prompt = f.read()

    def add_documents(self, documents, filenames):
        self.collection.add(
            documents=documents,
            ids=filenames
        )

    def run_retrieval(self, query):
        # save money
        # retrieval doesn't need cohere generation
        # extract sequence
        
        result = self.collection.query(
            query_texts=[query],
            n_results=1
        )
        vector_choice = result["documents"][0][0]

        pattern = r'```(.*?)```'
        extracted = re.findall(pattern, vector_choice, re.DOTALL)

        return extracted

    def run_scratch(self, query):
        # TODO simple fine tune

        prompt = self.generate_prompt + "\n" + query

        print(prompt)

        response = self.co.chat(
            message=prompt
        )
        
        print(response)
        



