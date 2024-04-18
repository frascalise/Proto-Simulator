import argparse
import numpy as np
from datetime import datetime

from chemicalio import importParameters, printInfo, printFinalInfo
from odetools import simulation
from errorsCheck import resetInfo

"""
parameters = allParameters[0]
#parameters = [chi, delta, ro, Da, div]
chi, delta, ro, Da, div = parameters

environment = allParameters [1]
# environment = [nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp]; 
# nIterates, t_end, max_step, toll_min, toll_max, nFlux, gen_exp, calving, genExp_time, thresholdToll, thresholdZero, thresholdEffects = environment
"""

def main(verbose, reset, file, importView, ecomode):

    if reset: 
        resetInfo()

    parameters, environment, chemicalSpecies, reactions = importParameters (verbose, file)

    if importView: 
        printInfo(parameters, environment, chemicalSpecies, reactions)
        quit()

    if verbose:
        printInfo(parameters, environment, chemicalSpecies, reactions)

    currentTime = datetime.now().strftime("%H.%M")
    (timeSimulation, matrixSimulation) = simulation (verbose, ecomode, currentTime, environment, parameters, chemicalSpecies, reactions)

    printFinalInfo (currentTime, parameters, environment, chemicalSpecies, reactions, matrixSimulation)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="ProtoGen Simulator v.1 - 284660")
    parser.add_argument("-v", "--verbose", action="store_true", help="additional prints")
    parser.add_argument("-e", "--eco", action="store_true", help="eco mode - save RAM memory")
    parser.add_argument("-r", "--reset", action="store_true", help="reset directory out/")
    parser.add_argument("-f", "--file", action="store_true", help="specify input file for parameters and reactions")
    parser.add_argument("-i", "--importV", action="store_true", help="view data imported")

    args = parser.parse_args()

    main(args.verbose, args.reset, args.file, args.importV, args.eco)

