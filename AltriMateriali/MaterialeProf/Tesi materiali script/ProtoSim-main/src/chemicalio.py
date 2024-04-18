import numpy as np
import subprocess
import os
import xlsxwriter
from datetime import datetime

from errorsCheck import checkProtoSim
from reactions import identifyType, ReactionType

"""
parameters = allParameters[0]
# parameters = [chi, delta, ro, Da, div]
# chi, delta, ro, Da, div = parameters

environment = allParameters [1]
# environment = [nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp, calving, genExp_time, thresholdToll, thresholdZero, thresholdEffects]; 
# nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp, calving, genExp_time, thresholdToll, thresholdZero, thresholdEffects = environment
"""

def getOrdinal (number):
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return f"{number}{suffix}"

def getConcentration(x, C, ro, delta):
    return x / getVolume(C, ro, delta)

def getVolume(C, ro, delta):
    radius = delta * (pow(C / (ro * np.pi * delta * delta * delta) - 1/3, 0.5) - 1) / 2
    return 4 * np.pi * radius * radius * radius / 3

def importParameters (verbose, file): 

    parametersFile = "../input/"
    reactionsFile = "../input/"

    if file: 
        parametersUser = input("Type the name of text file with parameters> ")
        reactionsUser = input("Type the name of text file with reaction> ")
        parametersFile = parametersFile + parametersUser
        reactionsFile = reactionsFile + reactionsUser
    else: 
        parametersFile = parametersFile + "parameters.txt"
        reactionsFile = reactionsFile + "chimica.txt"

    fi=open(parametersFile,'r')   

    delta = eval(fi.readline().split()[0])
    ro = eval(fi.readline().split()[0])
    Da = eval (fi.readline().split()[0])
    div = eval(fi.readline().split()[0]) 
    nIterates = eval(fi.readline().split()[0])
    t_end = eval(fi.readline().split()[0])
    max_step = eval(fi.readline().split()[0])  
    toll_min = eval(fi.readline().split()[0])
    toll_max = eval(fi.readline().split()[0])
    nFlux = eval(fi.readline().split()[0]) 
    gen_exp = [int(x) for x in fi.readline().split() if x.isdigit()]
    genExp_timing = eval(fi.readline().split()[0]) 
    thresholdToll = eval(fi.readline().split()[0]) 
    thresholdZero = eval(fi.readline().split()[0]) 
    thresholdEffects = eval(fi.readline().split()[0]) 

    fi.close()

    checkProtoSim(7, [gen_exp, nIterates, genExp_timing])
    gen_exp = [value - 1 for value in gen_exp]

    calving = 0.353553
    chi = 1/(6*pow(np.pi*pow(delta,3)*pow(ro,3),0.5))

    # List of parameters to resolve ODE
    parameters = [chi, delta, ro, Da, div]

    # List of environment sets
    environment = [nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp, calving, genExp_timing, thresholdToll, thresholdZero, thresholdEffects]; 
    
    chemicalSpecies = {}
    reactions = []

    fi=open(reactionsFile,'r')
    specify = fi.readlines()
    fi.close()

    for line in specify: 
        
        line = line.strip()
        
        if line: 
            #parts = line.split ("\t")
            
            parts = line.split()
            
            if len(parts) == 3: # if  parts.strip (): if ';' in parts: 
                species, quantity, coefficient = parts

                if  verbose:
                    print (f"Loaded chemical species: {species}\t{quantity} Kg\t{coefficient}")

                chemicalSpecies[species] = (float(quantity), float(coefficient))
            
            else:  
                
                if verbose:
                    print ("start import", end = "|\t") 
                
                reactionsParts = line.strip().split(";")
                
                if len (reactionsParts) == 2: 
                    
                    reactionType = ReactionType.ND

                    reaction_str = reactionsParts[0].strip()
                    coefficient = float(reactionsParts[1].strip())
                    reagents, products = reaction_str.split('>')
                    reagents = [reagent.strip() for reagent in reagents.split('+')]
                    products = [product.strip() for product in products.split('+')]
                    
                    reactionType = identifyType(line, verbose)

                    reaction_data = {
                        "in": reagents,
                        "out": products,
                        "k": coefficient,
                        "type": reactionType
                    }
                
                    if verbose: 
                        print ("reactants: ", reagents, "|products: ", products, "|type: ", reactionType.value, "|Coefficient: ", coefficient, end=" \t|")
                        print ("end import")
                    
                    reactions.append(reaction_data)
                
                else: 
                    checkProtoSim (1, line)
    
    loadedSpecies = list(chemicalSpecies.keys())
     
    # Check of chemical species in the reactions
    checkProtoSim(3, [loadedSpecies, reactions])

    # Check acceptability of number of fluxes and number of reactions
    checkProtoSim (8, [len(reactions), nFlux])
    
    return [parameters, environment, chemicalSpecies, reactions]

def printInfo (parameters, environment, chemicalSpecies, reactions): 

    sDelta = "\u03b4"
    sRo = "\u03c1"
    sChi = "\u03c7"

    chi, delta, ro, Da, div = parameters
    nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp, calving, genExp_time, thresholdToll, thresholdZero, thresholdEffects = environment

    print("\nRecognized Parameters:")
    print("]", sDelta, ":\t", delta)
    print("]", sRo, ":\t", ro)
    print ("]", sChi, ":\t", chi)
    print("]", "Da:\t", Da)
    print("]", "Duplication threshold:\t", div)

    print("\nExecution Parameters:")
    print("]", "flux:\t",nFlux)
    print("]", "iterations:\t", nIterates)
    print("]", "calving:\t", calving)
    print("]", "end time:\t",t_end)
    print("]", "max  step:\t",max_step)       
    print("]", "min toll. :",toll_min, "\t]", "max toll. :",toll_max)
    print("]", "toll. threshold:\t", thresholdToll)
    print("]", "zero threshold:\t", thresholdZero)       
    print("]", "effect threshold:\t", thresholdEffects)
    
    (gen_exp := [value + 1 for value in gen_exp])
    gen_exp_str = ', '.join(map(str, gen_exp))
    print("]", "generation to expand: ", gen_exp_str, end = '\t') if gen_exp else print("]", "generation to expand: nd\t", end = '')
    print ("]", "export time: ", genExp_time) if genExp_time != -1 else print ("]", "export time: nd")

    print("\nChemical Species imported:")
    i = 0
    for species, (quantity, coefficient) in chemicalSpecies.items():
        i+=1
        print (f"{i}] {species} \t {quantity} kg\tCoefficient: ", coefficient)

    print("\nReactions imported:")
    i = 0
    for i, reaction in enumerate (reactions): 
        reagents_str = " + ".join(reaction["in"])
        products_str = " + ".join(reaction["out"])

        if reaction["type"] is not ReactionType.FLOWIN and reaction["type"] is not ReactionType.FLOWOUT:
            print (f"{i+1}] {reagents_str} -> {products_str}\nKinetic Coefficient: ", reaction["k"], "\tType: ", reaction["type"].value, "\n")

        else: 
            arrow =" \u2192 "
            if reaction["type"] is ReactionType.FLOWIN: 
                print (f"{i+1}] {products_str} {arrow} [CSTR] \nSubstance Fraction: ", reaction["k"], "\tType: ", reaction["type"].value, "\n")
            else: 
                print (f"{i+1}] [CSTR] {arrow} {reagents_str}\nSubstance Fraction: ", reaction["k"], "\tType: ", reaction["type"].value, "\n")

def map_single_species (species, loadedSpecies): 
    
    if species in loadedSpecies:
        return loadedSpecies.index(species)
    else:
        checkProtoSim(10, species)

def map_species_to_indices(reactions, loadedSpecies):
    index_based_reactions = []

    for reaction in reactions:
        indexed_reagents = []
        indexed_products = []

        if reaction["type"] == ReactionType.FLOWIN or reaction["type"] == ReactionType.FLOWOUT: 

            if reaction["type"] == ReactionType.FLOWIN: 
                indexed_reagents.append(None)
                indexed_products.append(loadedSpecies.index(reaction["out"][0]))

            if reaction["type"] == ReactionType.FLOWOUT: 
                indexed_products.append(None)
                indexed_reagents.append(loadedSpecies.index(reaction["in"][0]))

        else: 
            for reagent in reaction["in"]:
                if reaction["type"] == ReactionType.DIFFUSION:
                    indexed_reagents.append(float(reaction["in"][0]))
                elif reagent in loadedSpecies:
                    indexed_reagents.append(loadedSpecies.index(reagent))

            for product in reaction["out"]:
                if product in loadedSpecies:
                    indexed_products.append(loadedSpecies.index(product))
                else:
                    checkProtoSim (6, product)

        indexed_reaction = {
            "in": indexed_reagents,
            "out": indexed_products,
            "k": reaction["k"],
            "type": reaction["type"]
        }

        index_based_reactions.append(indexed_reaction)
    
    return index_based_reactions

def printMapReactions (mapReactions): 
    for reaction in mapReactions:
        print("Reagents (indices):", reaction["in"])
        print("Products (indices):", reaction["out"])
        print("Rate constant (k):", reaction["k"])
        print("Reaction type:", reaction["type"])
        print()

def excelInit (chemicalSpecies, allParameters, currentTime, refName): 

    chi, delta, ro, Da, div = allParameters[0]
    nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp, calving, genExp_time, thresholdToll, thresholdZero, thresholdEffects = allParameters[1]
    reactions = allParameters[2]

    #* path directory definition
    directory_name = "../out"

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating the directory: {e}")

    currentData = datetime.now().strftime("%d.%m")
    directory_name = f"../out/data {currentData}"

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating second directory: {e}")

    directory_name = f"../out/data {currentData}/simulation {currentTime}"

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating second directory: {e}")

    
    name = f"../out/{directory_name}/{refName[1]}.xlsx"
    workbook = xlsxwriter.Workbook (name)

    #* global settings of excel export
    we = workbook.add_worksheet("Environment")
    wk = workbook.add_worksheet("Chemical Species")
    wr = workbook.add_worksheet("Reactions")
    wq = workbook.add_worksheet("Quantity")
    wc = workbook.add_worksheet("Concentration")

    if nFlux > 0:
        wf = workbook.add_worksheet("Flux")

    wq.set_column('A:Z', 15)
    wc.set_column('A:Z', 15)
    we.set_column('A:Z', 18)
    wk.set_column('A:Z', 15)
    wr.set_column('A:Z', 15)
    wr.set_column('B:B', 5)
    
    if nFlux > 0:
        wf.set_column('A:Z', 15)

    even_format = workbook.add_format({'bg_color': '#DDEBF7', 'align': 'center', 'valign': 'vcenter'})
    odd_format = workbook.add_format({'bg_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter'})
    even_format.set_border(1)
    odd_format.set_border(1)
    
    header_format = workbook.add_format({'bg_color': '#008E3E', 'bold': True, 'align': 'center'})
    header_format.set_border(1)

    (gen_exp := [value + 1 for value in gen_exp])
    gen_exp_str = ', '.join(map(str, gen_exp)) if gen_exp else 'nd'
    timeExp = genExp_time if genExp_time != -1 else "nd"

    #* export parameters
    data = {
        "\u03b4": delta,
        "\u03c1": ro,
        "\u03c7": chi,
        "Da": Da,
        "Duplication Threshold": div,
        "flux": nFlux,
        "gen. to expand": gen_exp_str,
        "interval for expansion": timeExp,
        "iterations": nIterates,
        "calving": calving,
        "end time": t_end,
        "max step": max_step,
        "min toll.": toll_min,
        "max toll.": toll_max,
        "tollerance th.": thresholdToll,
        "zero th.": thresholdZero,
        "effects th.": thresholdEffects,
    }

    we.write(0, 0, "Parameter", header_format)
    we.write(0, 1, "Value", header_format)
    
    row = 1
    for key, value in data.items():
        
        cell_format = even_format if row % 2 == 0 else odd_format
        we.write(row, 0, key, cell_format)
        we.write(row, 1, value, cell_format)

        row += 1

    we.set_column('C:XFD', None, None, {'hidden': True})
    we.set_default_row(hide_unused_rows=True)
    
    #* export chemical species
    wk.write(0, 0, "Species", header_format)
    wk.write(0, 1, "Quantity [KG]", header_format)
    wk.write(0, 2, "Coefficient", header_format)

    row = 1
    for i, (species, (quantity, coefficient)) in enumerate(chemicalSpecies.items(), start=1):
        
        cell_format = even_format if row % 2 == 0 else odd_format
        wk.write(row, 0, species, cell_format)
        wk.write(row, 1, quantity, cell_format)
        wk.write(row, 2, coefficient, cell_format)

        row += 1

    wk.set_column('D:XFD', None, None, {'hidden': True})
    wk.set_default_row(hide_unused_rows=True)

    #* export reactions
    _header_format = workbook.add_format({'bg_color': '#FFFF00', 'bold': True, 'align': 'center'})
   
    wr.write(0, 0, "Reagents", header_format)
    wr.write(0, 1, ">", _header_format)
    wr.write(0, 2, "Products", header_format)
    wr.write(0, 3, "Kinetic Coefficient", header_format)
    wr.write(0, 4, "Type", header_format)

    row = 1
    for i, reaction in enumerate(reactions, start=1):
        
        cell_format = even_format if row % 2 == 0 else odd_format
        
        reagents_str = " + ".join(reaction["in"])
        products_str = " + ".join(reaction["out"])

        wr.write(row, 0, reagents_str, cell_format)
        wr.write(row, 1, ">", _header_format)
        wr.write(row, 2, products_str, cell_format)
        wr.write(row, 3, reaction['k'], cell_format)
        wr.write(row, 4, reaction['type'].value, cell_format)
        
        row += 1

    wr.set_column('F:XFD', None, None, {'hidden': True})
    wr.set_default_row(hide_unused_rows=True)

    #* Header writing export
    loadedSpecies = list(chemicalSpecies.keys())

    # Working on expansion generation file
    if refName[0] == 1:
        wq.write(0, 0, "Iteration", header_format)
        wc.write(0, 0, "Iteration", header_format)
    
    # Working on simulation summary
    else: 
        wq.write(0, 0, "Generation", header_format)
        wc.write(0, 0, "Generation", header_format)

    wq.write(0, 1, "Time", header_format)
    wc.write(0, 1, "Time", header_format)

    i = 2
    for species in loadedSpecies: 
        wq.write(0, i, species, header_format)
        wc.write(0, i, species, header_format)
        i+=1

    # wq.set_column(i, 16383, None, {'hidden': True})
    # wc.set_column(f'{i}:{16383}', None, None, {'hidden': True})

    #* Export of fluxes information
    if nFlux > 0: 

        if refName[0] == 1: 
            wf.write(0, 0, "Iteration", header_format)
        else: 
            wf.write(0, 0, "Generation", header_format)
        
        wf.write(0, 1, "Time", header_format)
        ic = 2

        for i, reaction in enumerate(reactions[:nFlux]):
        
            ind = ic
            url = f'internal:Reactions!{ind}:{ind}'
            tx = f"Flux {i+1}"
            
            wf.write_url(0, ic, url, string=tx, cell_format = header_format)

            reagents_str = " + ".join(reaction["in"])
            products_str = " + ".join(reaction["out"])
            
            if reaction["type"] is not ReactionType.FLOWIN and reaction["type"] is not ReactionType.FLOWOUT:
                wf.write_comment(0, i:=i+2, f'{reagents_str} -> {products_str}')
            
            else: 
                arrow =" \u2192 "
                if reaction["type"] is ReactionType.FLOWIN: 
                    wf.write_comment(0, i:=i+2, f'{products_str} {arrow} [CSTR]')
                else: 
                    wf.write_comment(0, i:=i+2, f'[CSTR] {arrow} {reagents_str}')
            
            ic+=1

    if nFlux == 0:
        return workbook, wc, wq
    
    if nFlux > 0:
        return workbook, wc, wq, wf

def excelExport (matrixSimulation, timeSimulation, chemicalSpecies, allParameters, currentTime, refName, verbose): 

    # allParameters [0] -> parameters
    # allParameters [1] -> environment
    # allParameters [2] -> reaction
    # refName [0] -> type of export
    # refName [1] -> name of file

    nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp, calving, genExp_time, thresholdToll, thresholdZero, thresholdEffects = allParameters[1]

    if nFlux == 0:
        workbook, wc, wq = excelInit(chemicalSpecies, allParameters, currentTime, refName)

    if nFlux > 0:
        workbook, wc, wq, wf = excelInit(chemicalSpecies, allParameters, currentTime, refName)

    chemicalVariation = [row[:len(chemicalSpecies)] for row in matrixSimulation]
    if nFlux > 0: 
        fluxes = [row[-nFlux:] for row in matrixSimulation]
    
    # export generation data to be expanded at a defined interval 
    if refName [0] == 1 and genExp_time != -1:
        
        i = 1
        if nFlux == 0:
            for interval in np.arange(0, max(timeSimulation), genExp_time):
                index = np.argmin(np.abs(np.array(timeSimulation) - interval))
                
                wq.write(i, 0, index)
                wc.write(i, 0, index)

                wq.write(i, 1, timeSimulation[index])
                wc.write(i, 1, timeSimulation[index])

                column = 2
                for value in chemicalVariation[index]:
                    wq.write(i, column, value)
                    wc.write(i, column, getConcentration (value, chemicalVariation[index][0], allParameters[0][2], allParameters[0][1]))
                    column += 1
                i+=1
        
        i=1
        if nFlux > 0:
            for interval in np.arange(0, max(timeSimulation), genExp_time):
                index = np.argmin(np.abs(np.array(timeSimulation) - interval))
                
                wq.write(i, 0, index)
                wc.write(i, 0, index)

                wq.write(i, 1, timeSimulation[index])
                wc.write(i, 1, timeSimulation[index])

                column = 2
                for value in chemicalVariation[index]:
                    wq.write(i, column, value)
                    wc.write(i, column, getConcentration (value, chemicalVariation[index][0], allParameters[0][2], allParameters[0][1]))
                    column += 1
                i+=1
            
            i=1
            for interval in np.arange(0, max(timeSimulation), genExp_time):
                index = np.argmin(np.abs(np.array(timeSimulation) - interval))

                wf.write(i, 0, index)

                wf.write(i, 1, timeSimulation[index])

                column = 2
                for value in fluxes[index]:
                    wf.write(i, column, value)
                    column += 1
                i+=1

        i+=1
        wq.write(i, 0, len(chemicalVariation))
        wc.write(i, 0, len(chemicalVariation))

        wq.write(i, 1, timeSimulation[-1])
        wc.write(i, 1, timeSimulation[-1])

        column = 2
        for value in chemicalVariation[-1]:
            wq.write(i, column, value)
            wc.write(i, column, getConcentration (value, chemicalVariation[index][0], allParameters[0][2], allParameters[0][1]))
            column += 1
        
        cell_format = workbook.add_format({'bg_color': '#00FFFF'})
        wq.set_row(i, None, cell_format)
        wc.set_row(i, None, cell_format)

        if nFlux > 0: 
            wf.write(i, 0, len(chemicalVariation))
            wf.write(i, 1, timeSimulation[-1])

            column = 2
            for value in fluxes[-1]:
                wf.write(i, column, value)
                column += 1
        
            wf.set_row(i, None, cell_format)

    # export generation data standard
    else: 
        
        #* Index writing
        if nFlux == 0:
            for i in range(1, len(matrixSimulation) + 1):
                wq.write(i,0,i)
                wc.write(i,0,i)

        if nFlux > 0:
            for i in range(1, len(matrixSimulation) + 1):
                wq.write(i,0,i)
                wc.write(i,0,i)
                wf.write(i,0,i)

        #* Timing export
        row = 1 
        column = 1        
        
        if nFlux == 0:
            for value in np.array(timeSimulation):
                wq.write(row,column,value)
                wc.write(row,column,value)
                row+=1
       
        if nFlux > 0:
            for value in np.array(timeSimulation):
                wq.write(row,column,value)
                wc.write(row,column,value)
                wf.write(row,column,value)
                row+=1

        #* Data export [quantities and concentrations] + [any export fluxes]
        row=1
        for matLine in chemicalVariation:
            column=2
            for value in matLine:
                wq.write(row, column, value)
                wc.write(row, column, getConcentration (value, matLine[0], allParameters[0][2], allParameters[0][1]))
                column+=1
            row+=1

        if nFlux > 0:
            row=1
            for matLine in fluxes:
                column=2
                for value in matLine:
                    wf.write(row, column, value)
                    column+=1
                row+=1



    """
    wc.set_default_row(hide_unused_rows=True)
    wq.set_default_row(hide_unused_rows=True)
    
    if nFlux > 0: 
        wf.set_default_row(hide_unused_rows=True)
    """
        
    workbook.close()

def printFinalInfo (currentTime, parameters, environment, chemicalSpecies, reactions, matrixSimulation): 

    print ("\n->END SIMULATION<-")
    printInfo(parameters, environment, chemicalSpecies, reactions)

    print ("\n->About last generation<-")
    lastGen = matrixSimulation[-1]

    i=0
    for species in chemicalSpecies.items():
        print (f"{i+1}.", species[0], f"[{lastGen[i]} Kg]\n")
        i+=1
    
    nFlux = environment[5]
    
    if nFlux > 0: 
        print ("\n->About flux in last generation<-")
    
    for i in range (len(chemicalSpecies), len(lastGen)):
        print(f"{i+1-len(chemicalSpecies)}. Flux", f"[{lastGen[i]}]\n")
        i+=1

    print (f"All simulation data has been successfully exported to the directory /simulation {currentTime}.")