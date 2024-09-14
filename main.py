from plasmid import Plasmid
from model import Model
import os

documents = []
filenames = []

dataset = "dataset/curated"

for filename in os.listdir(dataset):
    with open(os.path.join(dataset, filename), 'r') as f:
        documents.append(f.read())
        filenames.append(filename)

model = Model()

model.add_documents(documents, filenames)

results = collection.query(
    query_texts=["This is a query document about resistance"],
    n_results=1
)
print(results)

path = "input/plasmid.dna"

plas = Plasmid(path)

gene = {
    "name": "test",
    "seq": "ATATATATATATATATATATATATAT"
}

plas.insert(gene)