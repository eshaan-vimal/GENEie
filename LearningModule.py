import pickle


def set_KB(KB):

    try:
        with open("KnowledgeBase.pkl", "wb") as file:
            pickle.dump(KB, file, pickle.HIGHEST_PROTOCOL)

    except pickle.PicklingError as e:
        print(str(e))


def tell_1(KB, p1_genotype, p2_genotype, c_phenotype, c_genotype, p1_gamete, p2_gamete, gene_edit):
        
    key = (p1_genotype, p2_genotype, c_phenotype)
    value = {"c_genotype": c_genotype, "p1_gamete": p1_gamete, "p2_gamete": p2_gamete, "gene_edit": gene_edit}
    
    KB[2][key] = value

    set_KB(KB)


def tell_2(KB, p1_genotype, c_phenotype, p2_genotype, gene_edit):

    key = (p1_genotype, c_phenotype)
    value = {"p2_genotype": p2_genotype, "gene_edit": gene_edit}
        
    KB[3][key] = value

    set_KB(KB)