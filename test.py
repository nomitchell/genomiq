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

#model.run_scratch("generate a DNA string that makes my yeast glow")

path = "input/plasmid/plasmid.dna"

plas = Plasmid(path)

gene = {
    "name": "test",
    "seq": "ATATATATATATATATATATATATAT"
}

plas.insert(gene)

sequence = "ATGATGATGATGATGTAGATGTAGATG"
model.verify_structure(sequence)

