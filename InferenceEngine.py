import LearningModule as LM
import pickle


trait_to_gene = (
    {
        "Sex": ("GAT", "TCG"),
        "Eye Colour": ("ACG", "CGT"),
        "Hair Colour": ("GTA", "TAC"),
        "Skin Colour": ("TGC", "GCA"),
        "Height": ("CAT", "ATG"),
        "Intelligence": ("AGC", "CTG")
    },

    {
        "Sex": ("X", "Y"),
        "Eye Colour": ("B", "b"),
        "Hair Colour": ("H", "h"),
        "Skin Colour": ("D", "d"),
        "Height": ("T", "t"),
        "Intelligence": ("I", "i")
    }
)

gene_to_trait = (
    {
        "GAT": "FEMALE", "TCG": "MALE",
        "ACG": "BROWN", "CGT": "BLUE",
        "GTA": "BRUNETTE", "TAC": "BLONDE",
        "TGC": "DARK", "GCA": "LIGHT",
        "CAT": "TALL", "ATG": "SHORT",
        "AGC": "LOW", "CTG": "HIGH"
    },

    {
        "X": "FEMALE", "Y": "MALE",
        "B": "BROWN", "b": "BLUE",
        "H": "BRUNETTE", "h": "BLONDE",
        "D": "DARK", "d": "LIGHT",
        "T": "TALL", "t": "SHORT",
        "I": "LOW", "i": "HIGH"
    }
)


def get_KB():

    try:
        with open("KnowledgeBase.pkl", "rb") as file:
            KB = pickle.load(file)

    except pickle.UnpicklingError as e:
        print(str(e))

    return KB


def genotype_to_phenotype(gene_rep, dna):

    KB = get_KB()

    traits = {}

    for phenotype in trait_to_gene[0]:
        
        if phenotype not in dna or dna[phenotype] == None:
            trait = "ANY"

        else:
            genotype = dna[phenotype]
            trait = KB[gene_rep - 1][genotype]

        traits[phenotype] = trait

    return traits


def goal_test_1(c_dna, c_traits):

    for phenotype in c_traits:
        if phenotype not in c_dna:
            return False
        
    return True


def heuristic_func_1(gene_rep, c_genotype, p1_genotype, p2_genotype, c_phenotype):

    KB = get_KB()

    derivable = False
    trait_count = 0

    for allele1 in p1_genotype:
        for allele2 in p2_genotype:

            expressed_trait = KB[gene_rep - 1][(allele1, allele2)]

            if c_genotype == (allele1, allele2):
                derivable = True

                if expressed_trait == c_phenotype:
                    trait_count += 1

    prob = trait_count / (len(p1_genotype)*len(p2_genotype))
    
    return derivable, prob


def inference_1(gene_rep, p1_dna, p2_dna, c_traits):

    KB = get_KB()

    c_dna = {}
    p1_gamete = {}
    p2_gamete = {}
    gene_edit = {}

    for phenotype in trait_to_gene[0]:

        gene = trait_to_gene[gene_rep - 1][phenotype]

        c_phenotype = c_traits[phenotype]
        p1_genotype = p1_dna[phenotype]
        p2_genotype = p2_dna[phenotype]

        if phenotype == "Sex":

            if c_phenotype == "FEMALE":

                c_dna["Sex"] = (gene[0], gene[0])
                p1_gamete["Sex"] = gene[0]
                p2_gamete["Sex"] = gene[0]

            else:

                c_dna["Sex"] = (gene[0], gene[1])

                if gene[1] in p1_genotype:
                    p1_gamete["Sex"] = gene[1]
                    p2_gamete["Sex"] = gene[0]

                else:
                    p2_gamete["Sex"] = gene[1]
                    p1_gamete["Sex"] = gene[0]

        else:

            if (key := (p1_genotype, p2_genotype, c_phenotype)) in KB[2]:

                c_dna[phenotype] = KB[2][key]["c_genotype"]
                p1_gamete[phenotype] = KB[2][key]["p1_gamete"]
                p2_gamete[phenotype] = KB[2][key]["p2_gamete"]
                gene_edit[phenotype] = KB[2][key]["gene_edit"]
            
            else:

                if c_phenotype == None:

                    c_dna[phenotype] = (p1_dna[phenotype][0], p2_dna[phenotype][0])
                    p1_gamete[phenotype] = p1_genotype[0]
                    p2_gamete[phenotype] = p2_genotype[0]

                    continue

                frontier = set()

                for allele1 in gene:
                        for allele2 in gene:
                            frontier.add((allele1, allele2))

                max_prob = 0

                for c_genotype in frontier:

                    derivable, prob = heuristic_func_1(gene_rep, c_genotype, p1_genotype, p2_genotype, c_phenotype)

                    if KB[gene_rep - 1][c_genotype] == c_phenotype:
                        ideal_genotype = c_genotype

                    if derivable and prob >= max_prob:
                        best_genotype = c_genotype
                        max_prob = prob
                
                c_dna[phenotype] = best_genotype

                if max_prob == 0:
                    c_dna[phenotype] = ideal_genotype
                    gene_edit[phenotype] = [best_genotype, ideal_genotype]
                
                else:
                    gene_edit[phenotype] = None

                p1_gamete[phenotype] = best_genotype[0]
                p2_gamete[phenotype] = best_genotype[1]

                LM.tell_1(KB, p1_genotype, p2_genotype, c_phenotype, c_dna[phenotype], p1_gamete[phenotype], p2_gamete[phenotype], gene_edit[phenotype])

        if goal_test_1(c_dna, c_traits):
            return c_dna, p1_gamete, p2_gamete, gene_edit

    return None, None, None, None


def goal_test_2(p2_dna, c_traits):

    for phenotype, trait in c_traits.items():
        if trait != None and phenotype not in p2_dna:
            return False
        
    return True


def heuristic_func_2(gene_rep, p1_genotype, p2_genotype, c_phenotype):

    KB = get_KB()

    trait_count = 0

    for allele1 in p1_genotype:
        for allele2 in p2_genotype:

            expressed_trait = KB[gene_rep - 1][(allele1, allele2)]

            if expressed_trait == c_phenotype:
                trait_count += 1

    prob = trait_count / (len(p1_genotype)*len(p2_genotype))
    
    return prob


def inference_2(gene_rep, p1_dna, c_traits):

    KB = get_KB()

    p2_dna = {}
    gene_edit = {}

    for phenotype in trait_to_gene[0]:

        gene = trait_to_gene[gene_rep - 1][phenotype]

        c_phenotype = c_traits[phenotype]
        p1_genotype = p1_dna[phenotype]

        if phenotype == "Sex":

            if gene[1] in p1_genotype:
                p2_dna["Sex"] = (gene[0], gene[0])

            else:
                p2_dna["Sex"] = (gene[0], gene[1])

        else:

            if (key := (p1_genotype, c_phenotype)) in KB[3]:

                p2_dna[phenotype] = KB[3][key]["p2_genotype"]
                gene_edit[phenotype] = KB[3][key]["gene_edit"]

            else:

                if c_phenotype == None:
                    p2_dna[phenotype] = None
                    continue

                frontier = set()

                for allele1 in gene:
                    for allele2 in gene:
                        frontier.add(tuple(sorted([allele1, allele2])))
            
                max_prob = 0
                
                for p2_genotype in frontier:

                    prob = heuristic_func_2(gene_rep, p1_genotype, p2_genotype, c_phenotype)

                    if KB[gene_rep - 1][p2_genotype] == c_phenotype:
                        ideal_genotype = p2_genotype

                    if prob >= max_prob:
                        best_genotype = p2_genotype
                        max_prob = prob
                
                p2_dna[phenotype] = best_genotype
                
                if max_prob == 0:
                    p2_dna[phenotype] = ideal_genotype
                    gene_edit[phenotype] = [(p1_genotype[0], best_genotype[1]), ideal_genotype]
                
                else:
                    gene_edit[phenotype] = None

                LM.tell_2(KB, p1_genotype, c_phenotype, p2_dna[phenotype], gene_edit[phenotype])

        if goal_test_2(p2_dna, c_traits):
            return p2_dna, gene_edit

    return None, None