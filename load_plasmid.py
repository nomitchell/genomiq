from snapgene_reader import snapgene_file_to_dict, snapgene_file_to_seqrecord
from Bio.Seq import Seq
from Bio.Restriction import *

class p_utils():
    def load_plasmid(path):
        # given a .dna file, needs to return
        # - string of bases
        # - annotated segments with start and end
        # - restriction sites with index
        pdict = snapgene_file_to_dict(path)

        sequence = pdict['seq']
        features = p_utils._get_features(pdict)
        rsites = p_utils._get_restriction(sequence)
        
        return sequence, features, rsites

    def _get_features(dictionary):
        raw_list = dictionary["features"]
        final_list = []

        for i in raw_list:
            final_list.append(
                {
                    "start": i["start"],
                    "end": i["end"],
                    "name": i["name"]
                }
            )

        return final_list

    def _get_restriction(seq):
        seq = Seq(seq)
        a = Analysis(AllEnzymes, seq)
        
        return a.full()

p_utils.load_plasmid("input/plasmid.dna")