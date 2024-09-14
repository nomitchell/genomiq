from load_plasmid import p_utils
from insert_utils import in_utils

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation

# constants for general use, in actualy production would vary based on factors
PROMOTER = ('tef1 promoter', 'tatcacataggaagcaacaggcgcgttggacttttaattttcgaggaccgcgaatccttacatcacacccaatcccccacaagtgatcccccacacaccatagcttcaaaatgtttctactccttttttactcttccagattttctcggactccgcgcatcgccgtaccacttcaaaacacccaagcacagcatactaaatttcccctctttcttcctctagggtgtcgttaattacccgtactaaaggtttggaaaagaaaaaagagaccgcctcgtttctttttcttcgtcgaaaaaggcaataaaaatttttatcacgtttctttttcttgaaaatttttttttttgatttttttctctttcgatgacctcccattgatatttaagttaataaacggtcttcaatttctcaagtttcagtttcatttttcttgttctattacaactttttttacttcttgctcattagaaagaaagcatagcaatctaatctaagttttaattacaaa')
TERMINATOR = ('cyc1 terminator', 'tcatgtaattagttatgtcacgcttacattcacgccctccccccacatccgctctaaccgaaaaggaaggagttagacaacctgaagtctaggtccctatttatttttttatagttatgttagtattaagaacgttatttatatttcaaatttttcttttttttctgtacagacgcgtgtacgcatgtaacattatactgaaaaccttgcttgagaaggttttgggacgctcgaaggctttaatttgc')
ADDED_LEN = len(PROMOTER[1]) + len(TERMINATOR[1])


class Plasmid():
    def __init__(self, path):
        self.seq, self.feat, self.rs = p_utils.load_plasmid(path)

        #self.rs = in_utils.restriction_ordering(self.rs, self.feat)

    def insert(self, gene):
        # test = in_utils.restriction_scoring(self.rs, self.feat)
        # at best restriction site, insert sequence
        # using sequence length, update all features past it to new location
        # using sequence lenght, update all restriction sites past it to new location
        # using new features, reorder rs list
        # gene is dict name=name seq=seq

        # TODO need to add promoter and terminator stuff

        self.rs = in_utils.restriction_ordering(self.rs, self.feat)

        gene_seq = gene["seq"]
        gene_name = gene["name"]
        gene_len = len(gene_seq)

        best_rs_loc = self.rs[0]["location"]

        self.seq = self.seq[:best_rs_loc] + PROMOTER[1] + gene_seq + TERMINATOR[1] + self.seq[best_rs_loc:]

        for rsite in self.rs:
            if rsite["location"] > best_rs_loc:
                rsite["location"] += (gene_len + ADDED_LEN)
        
        for f in self.feat:
            if f["start"] > best_rs_loc:
                f["start"] += (gene_len + ADDED_LEN)
                f["end"] += (gene_len + ADDED_LEN)
        
        print("appending", gene)

        self.feat.append(
            {
                "start": best_rs_loc + len(PROMOTER[1]),
                "end": best_rs_loc + gene_len + len(PROMOTER[1]),
                "name": gene_name
            }
        )

        self.feat.append(
            {
                "start": best_rs_loc,
                "end": best_rs_loc + len(PROMOTER[1]),
                "name": PROMOTER[0]
            }
        )
        
        self.feat.append(
            {
                "start": best_rs_loc + len(PROMOTER[1]) + gene_len,
                "end": best_rs_loc + ADDED_LEN + gene_len,
                "name": TERMINATOR[0]
            }
        )

    def save(self):
        of = "download/out_plasmid.gb"
        
        sequence = Seq(self.seq)

        record = SeqRecord(
            sequence,
            id="1",
            name="plasmid",
            description="Plasmid made with GenomIQ"
        )

        record.annotations["molecule_type"] = "DNA"

        for f in self.feat:
            feature = SeqFeature(FeatureLocation(start=f["start"], end=f["end"]), type="gene", qualifiers={"gene": f["name"]})
            record.features.append(feature)

        with open(of, "w") as output_file:
            SeqIO.write(record, output_file, "genbank")

        print("GenBank file saved as 'out_plasmid.gb'")

        return of



