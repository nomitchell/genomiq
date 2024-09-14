from load_plasmid import p_utils
from insert_utils import in_utils

class Plasmid():
    def __init__(self, path):
        self.seq, self.feat, self.rs = p_utils.load_plasmid(path)

        self.rs = in_utils.restriction_ordering(self.rs, self.feat)

    def insert(self, gene):
        # test = in_utils.restriction_scoring(self.rs, self.feat)
        # at best restriction site, insert sequence
        # using sequence length, update all features past it to new location
        # using sequence lenght, update all restriction sites past it to new location
        # using new features, reorder rs list
        # gene is dict name=name seq=seq

        # TODO need to add promoter and terminator stuff

        gene_seq = gene["seq"][0][1:-2]
        gene_name = gene["name"]
        gene_len = len(gene_seq)

        best_rs_loc = self.rs[0]["location"]
        
        print(self.seq)
        print("\n")
        print("gene seq", gene_seq)

        self.seq = self.seq[:best_rs_loc] + gene_seq + self.seq[best_rs_loc:]

        for rsite in self.rs:
            if rsite["location"] > best_rs_loc:
                rsite["location"] += gene_len
        
        for f in self.feat:
            if f["start"] > best_rs_loc:
                f["start"] += gene_len
                f["end"] += gene_len
        
        self.feat.append(
            {
                "start": best_rs_loc,
                "end": best_rs_loc + gene_len,
                "name": gene_name
            }
        )

