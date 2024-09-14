from snapgene_reader import snapgene_file_to_dict, snapgene_file_to_seqrecord

file_path = './snap_gene_file.dna'
dictionary = snapgene_file_to_dict(file_path)
seqrecord = snapgene_file_to_seqrecord(file_path)