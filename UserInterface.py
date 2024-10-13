import InferenceEngine as IE
from prettytable import PrettyTable
import traceback

def valid_genotype(gene_rep, genotype, phenotype):

    if len(genotype) != 2:
        return False
    
    allele_1, allele_2 = genotype

    if (allele_1 not in IE.trait_to_gene[gene_rep-1][phenotype]) or (allele_2 not in IE.trait_to_gene[gene_rep-1][phenotype]):
        return False
    
    else:
        if phenotype == "Sex":
            if genotype == ("Y", "Y"):
                return False
        return True
    

def valid_trait(trait, genes):

    if trait != IE.gene_to_trait[0][genes[0]] and trait != IE.gene_to_trait[0][genes[1]] and trait != "X":
        return False
    
    else:
        return True
    

def valid_parents(p1_dna, p2_dna):

    p1_sex = set(p1_dna["Sex"])
    p2_sex = set(p2_dna["Sex"])

    if(p1_sex == p2_sex):
        return False
    
    else:
        return True


def get_dna(gene_rep):

    dna = {}

    for phenotype in IE.trait_to_gene[0]:
        while True:

            genotype = tuple(input(f"Enter {phenotype} genotype:  ".ljust(30)).split(' '))

            if valid_genotype(gene_rep, genotype, phenotype):
                break

            else:
                print("    \x1B[3mERROR:  Invalid input. Try again.\x1B[0m")

        dna[phenotype] = genotype

    return dna


def get_traits():

    traits = {}
    count = 0

    for phenotype, genes in IE.trait_to_gene[0].items():
        while True:
            
            trait = input(f"Enter {phenotype} ({IE.gene_to_trait[0][genes[0]]}/{IE.gene_to_trait[0][genes[1]]}):  ".ljust(38)).upper()
            
            if valid_trait(trait, genes):
                break
            
            else:
                print("    \x1B[3mERROR:  Invalid input. Try again.\x1B[0m")

        if trait == "X":
            traits[phenotype] = None
            count += 1

        else:
            traits[phenotype] = trait

        if count == len(IE.trait_to_gene[0]):
            print()
            print("\x1B[3mERROR:  Atleast 1 trait should be specced. Try again.\x1B[0m\n")
            traits = get_traits()

    return traits


def genotype_to_phenotype(gene_rep, dna):

    traits = IE.genotype_to_phenotype(gene_rep, dna)
    table = PrettyTable(["Phenotype", "Trait"])

    for phenotype, trait in traits.items():
        table.add_row([phenotype, trait])

    return table


def change_genotype_rep(gene_rep, genotype):

    if gene_rep == 1:

        genotype_1 = genotype
        alleles_1 = list(IE.gene_to_trait[0].keys())
        alleles_2 = list(IE.gene_to_trait[1].keys())
        genotype_2 = (alleles_2[alleles_1.index(genotype_1[0])], alleles_2[alleles_1.index(genotype_1[1])])

        return genotype_2
    
    if gene_rep == 2:

        genotype_2 = genotype

        alleles_1 = list(IE.gene_to_trait[0].keys())
        alleles_2 = list(IE.gene_to_trait[1].keys())
        genotype_1 = (alleles_1[alleles_2.index(genotype_2[0])], alleles_1[alleles_2.index(genotype_2[1])])

        return genotype_1


def print_dna(gene_rep, dna):

    table = PrettyTable(["Phenotype", "Gene Sequence", "Gene Description"])

    for phenotype in IE.trait_to_gene[0]:

        if (phenotype not in dna or dna[phenotype] == None) and phenotype != "Sex":
            genotype_1 = "ANY"
            genotype_2 = "ANY"

        elif gene_rep == 1:
            genotype_1 = ' '.join(dna[phenotype])
            genotype_2 = ' '.join(change_genotype_rep(gene_rep, dna[phenotype]))
        
        elif gene_rep == 2:
            genotype_2 = ' '.join(dna[phenotype])
            genotype_1 = ' '.join(change_genotype_rep(gene_rep, dna[phenotype]))

        table.add_row([phenotype, genotype_1, genotype_2])

    return table


def print_gamete(gene_rep, gamete):
    
    table = PrettyTable(["Phenotype", "Gene Sequence", "Gene Description"])

    for phenotype, allele in gamete.items():

        if gene_rep == 1:
            allele1 = allele
            alleles_1 = list(IE.gene_to_trait[0].keys())
            alleles_2 = list(IE.gene_to_trait[1].keys())
            allele2 = alleles_2[alleles_1.index(allele1)]

        if gene_rep == 2:
            allele2 = allele
            alleles_1 = list(IE.gene_to_trait[0].keys())
            alleles_2 = list(IE.gene_to_trait[1].keys())
            allele1 = alleles_1[alleles_2.index(allele2)]

        table.add_row([phenotype, allele1, allele2])

    return table


def print_gene_edit(gene_rep, gene_edit):

    table = PrettyTable(["Phenotype", "Before Edit", "After Edit"])
    exists = False

    for phenotype, genotypes in gene_edit.items():

        if genotypes == None:
            continue

        exists = True
        
        before_edit = genotypes[0]
        after_edit = genotypes[1]

        if gene_rep == 1:
            before_edit1 = ' '.join(before_edit)
            before_edit2 = ' '.join(change_genotype_rep(gene_rep, before_edit))
            after_edit1 = ' '.join(after_edit)
            after_edit2 = ' '.join(change_genotype_rep(gene_rep, after_edit))

        if gene_rep == 2:
            before_edit2 = ' '.join(before_edit)
            before_edit1 = ' '.join(change_genotype_rep(gene_rep, before_edit))
            after_edit2 = ' '.join(after_edit)
            after_edit1 = ' '.join(change_genotype_rep(gene_rep, after_edit))
        
        table.add_row([phenotype, before_edit1, after_edit1])
        table.add_row(['', before_edit2, after_edit2])

    if exists:
        return table
    
    else:
        return None


def best_child(gene_rep):

    while True:

        print(f"\033[1mPARENT 1 DNA:\033[0m")
        print("(alleles seperated by whitespace)")
        p1_dna = get_dna(gene_rep)
        print()

        print(f"\033[1mPARENT 2 DNA:\033[0m")
        print("(alleles seperated by whitespace)")
        p2_dna = get_dna(gene_rep)
        print()

        if valid_parents(p1_dna, p2_dna):
            break

        else:
            print("\x1B[3mERROR: Both parents cannot have same gender. Try again.\x1b[0m\n")

    p1_table = genotype_to_phenotype(gene_rep, p1_dna)
    p2_table = genotype_to_phenotype(gene_rep, p2_dna)

    p_table = PrettyTable(["Phenotype", "1st Traits", "2nd Traits"])
    for row1, row2 in zip(p1_table.rows, p2_table.rows):
        p_table.add_row([row1[0], row1[1], row2[1]])

    print("\033[1mPARENTS TRAITS:\033[0m")
    print(p_table)
    print()

    print(f"\033[1mDESIRED FEATURES IN CHILD:\033[0m")
    print("(input x if no preference)")
    c_traits = get_traits()
    print()

    c_dna, p1_gamete, p2_gamete, gene_edit = IE.inference_1(gene_rep, p1_dna, p2_dna, c_traits)

    c_dna_table = print_dna(gene_rep, c_dna)
    print("\033[1mOFFSPRING DNA:\033[0m")
    print(c_dna_table)
    print()

    p1_gamete_table = print_gamete(gene_rep, p1_gamete)
    print("\033[1mPARENT 1 GAMETE DNA:\033[0m")
    print(p1_gamete_table)
    print()

    p2_gamete_table = print_gamete(gene_rep, p2_gamete)
    print("\033[1mPARENT 2 GAMETE DNA:\033[0m")
    print(p2_gamete_table)
    print()

    
    gene_edit_table = print_gene_edit(gene_rep, gene_edit)
    if gene_edit_table:
        print("\033[1mOFFSPRING GENES TAGGED FOR CRISPR EDITING:\033[0m")
        print(gene_edit_table)
        print()


def best_mate(gene_rep):

    print(f"\033[1mPRIMARY PARENT DNA:\033[0m")
    print("(alleles seperated by whitespace)")
    p1_dna = get_dna(gene_rep)
    print()

    p1_table = genotype_to_phenotype(gene_rep, p1_dna)
    print("\033[1mPRIMARY PARENT TRAITS:\033[0m")
    print(p1_table)
    print()

    print(f"\033[1mDESIRED FEATURES IN CHILD:\033[0m")
    print("(input x if no preference)")
    c_traits = get_traits()
    print()
    
    p2_dna, gene_edit = IE.inference_2(gene_rep, p1_dna, c_traits)

    p2_dna_table = print_dna(gene_rep, p2_dna)
    p2_trait_table = genotype_to_phenotype(gene_rep, p2_dna)

    print("\033[1mSECONDARY PARENT DNA:\033[0m")
    print(p2_dna_table)
    print()

    print("\033[1mSECONDARY PARENT TRAITS:\033[0m")
    print(p2_trait_table)
    print()

    gene_edit_table = print_gene_edit(gene_rep, gene_edit)
    if gene_edit_table:
        print("\033[1mOFFSPRING GENES TAGGED FOR CRISPR EDITING:\033[0m")
        print(gene_edit_table)
        print()


while True:
    
    try:
        print("\033[1mSYSTEM FUNCTIONALITY SCHEME\033[0m")
        print("0:  EXIT")
        print("1:  DESIRED CHILD")
        print("2:  BEST PARTNER\n")
        choice = int(input("Enter choice:  "))

        if choice == 0:
            print("\x1B[3m\033[1mSystem going offline...\033[0m\x1B[0m\n")
            break

        elif choice < 0 or choice > 2:
            raise Exception()

        print()
        while True:

            try:
                print("\033[1mDNA INPUT SCHEME\033[0m")
                print("1:  AS GENE SEQUENCES")
                print("2:  AS GENE DESCRIPTIONS\n")
                gene_rep = int(input("Enter choice:  "))

                if gene_rep == 1 or gene_rep == 2:
                    print()
                    break

                else:
                    raise Exception()  
                   
            except:
                print("\x1B[3mERROR:  Invalid input. Try again.\x1B[0m\n")

        if choice == 1:
            best_child(gene_rep)

        if choice == 2:
            best_mate(gene_rep)

    except Exception as e:
        print(e)
        traceback.print_exc()
        print("\x1B[3mERROR:  Invalid input. Try again.\x1B[0m\n")