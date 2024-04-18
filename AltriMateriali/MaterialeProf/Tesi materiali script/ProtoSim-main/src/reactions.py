from enum import Enum

from errorsCheck import checkProtoSim

class ReactionType (Enum): 
    
    CONDENSATION_21 = "Condensation 2:1"
    CONDENSATION_22 = "Condensation 2:2"
    CONDENSATION_32 = "Condensation 3:2"

    CLEAVAGE_12 = "Cleavage 1:2"
    CLEAVAGE_23 = "Cleavage 2:2"
    
    DIFFUSION = "Diffusion"

    FLOWIN = "in-CSTR"
    FLOWOUT = "CSTR-out"

    ND = "Undefined Type"

def identifyType (reaction, verbose): 

    reactionsParts = reaction.strip().split(";")
    reaction_str = reactionsParts[0].strip()
    reagents, products = reaction_str.split('>')
    
    reagents = [reagent.strip() for reagent in reagents.split('+')]
    products = [product.strip() for product in products.split('+')]

    nReactans = len (reagents)
    nProducts = len (products)

    if verbose: 
        print(f"Identifying Reaction Type: {nReactans};{nProducts}")

    if nProducts == 1 and products[0] == '':
        return ReactionType.FLOWOUT

    if nReactans == 1: 
        if reagents[0] == '':
            return ReactionType.FLOWIN
        if nProducts == 1: 
            return ReactionType.DIFFUSION
        if nProducts == 2: 
            return ReactionType.CLEAVAGE_12

    if nReactans == 2: 
        if nProducts == 1: 
            return ReactionType.CONDENSATION_21
        if nProducts == 2: 
            return ReactionType.CONDENSATION_22
        if nProducts == 3: 
            return ReactionType.CLEAVAGE_23
        
    if nReactans == 3:
        if nProducts == 2:
            return ReactionType.CONDENSATION_32

    checkProtoSim(2, reaction)

def identifyCatalysts (reaction, verbose):
    
    reactionsParts = reaction.strip().split(";")
    reaction_str = reactionsParts[0].strip()
    reagents, products = reaction_str.split('>')
    
    reagents = [reagent.strip() for reagent in reagents.split('+')]
    products = [product.strip() for product in products.split('+')]

    catalysts = [species for species in reagents if species in products]
    catalysts = list(set(catalysts))

    cataList = []

    for species in catalysts:
            occurrences_in_reagents = reagents.count(species)
            occurrences_in_products = products.count(species)
            result = occurrences_in_products - occurrences_in_reagents

            if result == 0:

                if verbose: 
                    print (species, "-species only catalyzes reaction")

                cataList.append ((species, result))

            elif result > 0:
                
                if verbose: 
                    print (species, "-species catalyzes and is produced in reaction")
                
                cataList.append ((species, result))
            
            elif result < 0:
                
                if verbose: 
                    print (species, "-species catalyzes and reacts in reaction")
                
                cataList.append ((species, result))
    
    return cataList