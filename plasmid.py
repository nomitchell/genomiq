from load_plasmid import p_utils
from insert_utils import in_utils

class Plasmid():
    def __init__(self, path):
        self.seq, self.feat, self.rs = p_utils.load_plasmid(path)

        self.rs = in_utils.restriction_ordering(self.rs, self.feat)

    def insert(gene):
        # test = in_utils.restriction_scoring(self.rs, self.feat)
        # at best restriction site, insert sequence
        # using sequence length, update all features past it to new location
        # using sequence lenght, update all restriction sites past it to new location
        # using new features, reorder rs list
        
        pass