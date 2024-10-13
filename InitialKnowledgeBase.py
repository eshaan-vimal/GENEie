import pickle

KB = [
     {
     ("TCG", "GAT"): "MALE",
     ("GAT", "TCG"): "MALE",

     ("GAT", "GAT"): "FEMALE",    
     
     ("ACG", "ACG"): "BROWN",
     ("ACG", "CGT"): "BROWN",
     ("CGT", "ACG"): "BROWN",

     ("CGT", "CGT"): "BLUE",

     ("GTA", "GTA"): "BRUNETTE",
     ("GTA", "TAC"): "BRUNETTE",
     ("TAC", "GTA"): "BRUNETTE",
     ("TAC", "TAC"): "BLONDE",

     ("TGC", "TGC"): "DARK",
     ("TGC", "GCA"): "DARK",
     ("GCA", "TGC"): "DARK",

     ("GCA", "GCA"): "LIGHT",

     ("CAT", "ATG"): "TALL",
     ("ATG", "CAT"): "TALL",
     ("CAT", "CAT"): "TALL",

     ("ATG", "ATG"): "SHORT",

     ("AGC", "AGC"): "LOW",
     ("AGC", "CTG"): "LOW",
     ("CTG", "AGC"): "LOW",

     ("CTG", "CTG"): "HIGH"
     },


    {
     ("Y", "X"): "MALE",
     ("X", "Y"): "MALE",

     ("X", "X"): "FEMALE",

     ("B", "B"): "BROWN",
     ("B", "b"): "BROWN",
     ("b", "B"): "BROWN",

     ("b", "b"): "BLUE",

     ("H", "H"): "BRUNETTE",
     ("H", "h"): "BRUNETTE",
     ("h", "H"): "BRUNETTE",

     ("h", "h"): "BLONDE",

     ("D", "D"): "DARK",
     ("D", "d"): "DARK",
     ("d", "D"): "DARK",

     ("d", "d"): "LIGHT",

     ("T", "T"): "TALL",
     ("T", "t"): "TALL",
     ("t", "T"): "TALL",

     ("t", "t"): "SHORT",

     ("I", "I"): "LOW",
     ("I", "i"): "LOW",
     ("i", "I"): "LOW",

     ("i", "i"): "HIGH"
     },

     {},

     {}
]


try:
    with open("KnowledgeBase.pkl", "wb") as file:
        pickle.dump(KB, file, pickle.HIGHEST_PROTOCOL)
except pickle.PicklingError as e:
    print(str(e))