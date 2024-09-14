from plasmid import Plasmid

path = "input/plasmid.dna"

plas = Plasmid(path)

gene = "ATATATATATATATATATATATATAT"

plas.insert(gene)