import os
import matplotlib.pyplot as plt             # type: ignore
from openpyxl.styles import PatternFill     # type: ignore
from openpyxl import Workbook               # type: ignore

from Module import *
from ReadParams import *


def main():

    # Inizializzo i parametri che verranno poi letti in params.txt
    INPUT_FILE = readInput()
    OUTPUT_FILE = readOutput()
    TIME = readTime()
    POINTS = readPoints()
#    TRAJECTORIES = readTrajectories()
    TRAJECTORIES = 1
    COEFF = readCoeff()
    GENERATIONS = readGenerations()
    
    oldFile = INPUT_FILE    # Salva il file di input originale

    print("INPUT: ", INPUT_FILE)
    print("OUTPUT: ", OUTPUT_FILE)
    print("TIME: ", TIME)
    print("POINTS: ", POINTS)
    print("TRAJECTORIES: ", TRAJECTORIES)
    print("COEFF: ", COEFF)
    print("GENERATIONS: ", GENERATIONS)
    print("\n")

    # Inizializzo le liste e dizionari che conterranno tutte le informazioni lette da chimica.txt
    species = [] 
    frequences = []
    reactions = []
    catalysis = {}
    model = protoZero(INPUT_FILE, TIME, POINTS, COEFF, species, frequences, reactions, catalysis)

    # Creo il foglio dove scrivere i dati
    wb = Workbook()
    ws = wb.active

    speciesColumn = {}  # Dizionario che mappa la colonna con il nome della specie

    # Aggiungi la colonna TIME al foglio di lavoro
    ws.cell(row=1, column=1, value="TIME")
    speciesColumn[0] = "TIME"

    rowIndex = 1
    columnIndex = 2

    orderedSpecies = []
    for k in species:
        orderedSpecies.append(k.name)
    
    orderedSpecies.sort()

    orderedSpeciesColumn = {}
    for j in range(0, TRAJECTORIES):
        for i in orderedSpecies:
            cell = ws.cell(row=rowIndex, column=columnIndex, value=i)
            orderedSpeciesColumn[columnIndex-1] = i
            redBG = PatternFill(start_color="E97451", end_color="E97451", fill_type="solid")
            cell.fill = redBG

            columnIndex += 1

    speciesColumn.update(orderedSpeciesColumn)
    print(speciesColumn)

    continueRow = 2 # Indice della riga da cui continuare a scrivere i dati
    continueTime = 0
    stopSimulation = False
    
    for genCounter in range(0, GENERATIONS):
        species = [] 
        frequences = []
        reactions = []
        catalysis = {}
        stopGeneration = False
        dummyValues = {} # Dizionario temporanea per salvare i valori delle specie

        model = protoZero(INPUT_FILE, TIME, POINTS, COEFF, species, frequences, reactions, catalysis)
        print("********** GENERAZIONE ", genCounter + 1, "********** ")
        results = model.run(number_of_trajectories = TRAJECTORIES)
        
        for index in range(0, TRAJECTORIES):
            trajectory = results[index]
            #print("Trajectory: ", trajectory)

            for i in range(0, len(trajectory["time"])): # Scorro per tutta la lunghezza dei dati
                for j in range(0, len(trajectory)):     # Scorro per ogni specie, quindi inserimento per riga 

                    if speciesColumn[j] == "tempo":
                        ws.cell(row=i+continueRow, column=j+1, value=int(trajectory[j][i]+continueTime))
                        # Se il tempo cambia, vuol dire che la protocellula si e' divisa e la generazione finisce
                        if trajectory[j][i] != trajectory[j][i-1] and i != 0:       
                            #print("STOP GENERATION: ", stopGeneration, "\n")
                            #print("STOP SIMULATION: ", stopSimulation, "\n")
                            continueTime += trajectory[j][i]
                            print("continueTime + trajectory[j][i] =",continueTime, "+", trajectory[j][i])
                            stopGeneration = True
                            stopSimulation = False
                    else:
                        ws.cell(row=i+continueRow, column=j+1, value=int(trajectory[j][i]))
                      
                
                if stopGeneration:
                    continueRow += i

                    for j in range(1, len(trajectory)-1):
                        dummyValues[speciesColumn[j]] = int(trajectory[j][i])   # Primo e ultimo valore di questa lista sono da scartare
                    
                    #print("DummyValues: ", dummyValues)

                    # Cancella il file "input/dummyChimica.txt" se esiste
                    if os.path.exists("input/KBVNRDL1Qp_Chimica.txt"):
                        os.remove("input/KBVNRDL1Qp_Chimica.txt")

                    # Crea un nuovo file di testo chiamato dummyChimica nella cartella input in scrittura, conterra' le nuove quantita' delle specie
                    with open("input/KBVNRDL1Qp_Chimica.txt", "w") as file:
                        INPUT_FILE = "input/KBVNRDL1Qp_Chimica.txt"
                        print(catalysis)                        
                        
                        #   Scrive le nuove quantita' delle specie nel file dummyChimica.txt
                        for k in range(0, len(dummyValues)):
                            speciesFile = list(catalysis.keys())[k] + "\t" + str(dummyValues[list(catalysis.keys())[k]]) + "\t" + catalysis[list(catalysis.keys())[k]] + "\n"
                            file.write(speciesFile)
                        
                        file.write("\n")

                        # Apro in lettura la chimica originale per salvarmi le reazioni chimiche
                        with open(str(oldFile), "r") as of:
                            content = of.read()
                            empty_line_index = content.index("\n\n")

                            # scrivo tutto quello che trova dopo la riga vuota in una stringa
                            new_content = content[empty_line_index+2:]

                        # Scrivo le reazioni chimiche nel file dummyChimica.txt
                        file.write(new_content)
                    break
                else:
                    stopSimulation = True
        
        if stopSimulation:
            break


    # Salva il workbook su file
    wb.save(OUTPUT_FILE)
    
    # Cancella il file "input/dummyChimica.txt" se esiste
    if os.path.exists("input/KBVNRDL1Qp_Chimica.txt"):
        os.remove("input/KBVNRDL1Qp_Chimica.txt")


if __name__ == "__main__":
    main()
