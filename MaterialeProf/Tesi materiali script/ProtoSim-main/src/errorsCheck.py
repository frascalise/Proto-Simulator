import os
import subprocess

def checkProtoSim (arg, data):
    
    match arg: 

        case 0: 
            if (data != 'C'):
                print ("\nERROR 00 - loading parameters from file")
                quit()
        
        case 1: 
            print ("\nERROR 01 - information symbol: view chemistry file", data)
            quit ()
        
        case 2: 
            print (f"\nERROR 02 - \" {data} \" type of reaction unknown")
            quit()

        case 3: 
            
            from reactions import ReactionType
            from chemicalio import getOrdinal

            for i, reaction in enumerate (data[1]):
                
                reactants = reaction["in"]
                products = reaction["out"]

                for specie in reactants + products:
                    
                    if reaction["type"] == ReactionType.FLOWIN: 
                        if products[0] not in data [0]: 
                            print (f"\nERROR 03 - invalid {getOrdinal(i+1)} reaction: '{products[0]}' chemical species unknown ")
                            quit()
                        else: 
                            continue

                    if reaction["type"] == ReactionType.FLOWOUT: 
                        if reactants[0] not in data [0]: 
                            print (f"\nERROR 03 - invalid {getOrdinal(i+1)} reaction: '{reactants[0]}' chemical species unknown")
                            quit ()
                        else: 
                            continue

                    if reaction["type"] == ReactionType.DIFFUSION: 
                        
                        if products[0] not in data [0]: 
                            print (f"\nERROR 03 - invalid {getOrdinal(i+1)} reaction: '{products[0]}' chemical species unknown")
                            quit ()
                        else: 
                            continue

                    if specie not in data[0]: 
                            print (f"\nERROR 03 - invalid {getOrdinal(i+1)} reaction: '{specie}' chemical species unknown")
                            quit()

        case 4: 
            print ("\nERROR 04 - negative quantities detected\n")
            print ("Value: ", data[0], "\tIndex: ", data[1], "\n")
            quit()

        case 5: 
            print ("\nERROR 05 - ode_function, unknow variation rules for ", data["type"])
            quit()

        case 6: 
            print (f"\nERROR 06 - indexing reactions '{data}'")
            quit()

        case 7: 

            if data [1] < 1: 
                print ("ERROR 07 - invalid number of iterations [nIterates] detected")
                quit()

            if data [0] == -1 and data[2] == -1:
                return

            for element in data [0]: 
                if element == 0 or element > data [1]:
                    print (f"\nERROR 07 - loading generation indexes to expand\nIf you don't want to export any specific generation, type '-1' in the parameters file.")
                    quit()

            for element in data [0]: 
                element-=1

            if data [2] != -1:
                if data [2] <= 0:
                    print(f"ERROR 07 - unknown time of export generations of expansion\nIf you don't want to define the time, type '-1' in the parameters file.")
                    quit()

            if data [2] != -1 and data [0] == -1: 
                print(f"ERROR 07 - unknown time of export generations of expansion\nIf you don't want to export any specific generation, type '-1' in the parameters file.")
                quit()

            if not data[0] and data [2] != -1:
                print(f"ERROR 07 - unknown time of export generations of expansion\nIf you don't want to export any specific generation, type '-1' in the parameters file.")
                quit()

        
        case 8: 

            if data [0] <= 0:
                print (f"\nERROR 08 - zero reactions found\n")
                quit()

            if data [1] < 0 or not (isinstance(data [1], int)):

                print (f"\nERROR 08 - unknown flux number: please type '0' in parameters file to disable tracking\n")
                quit()

            if data [1] == 0:
                return

            if data [1] > 0: 
                if data [1] > data [0]: 
                    print (f"\nERROR 08 - too many fluxes recognized\nnumber of imported reactions: {data [0]} - number of flux imported: {data[1]}.")
                    quit()

        case 9: 
            print (f"\nERROR 09 - tollerance Test: empty protoX [{data}]\n")
            quit()

        case 10:
            print (f"\nERROR 10 - species '{data}' not found in loadedSpecies\n")
            quit()

        case _: 
            print ("\nUNKNOW ERROR XY")
            quit ()

def resetInfo (): 
    
    if os.path.exists("../out"):
        try:
            subprocess.run(["rm", "-fr", "../out"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in removing the existing directory: {e}")
    quit()