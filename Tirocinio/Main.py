import os
import matplotlib.pyplot as plt             # type: ignore
from openpyxl.styles import PatternFill     # type: ignore
from openpyxl import Workbook               # type: ignore

from Module import *
from ReadParams import *


def outputData(species, reactions, catalysis, events, frequences, genCounter):
    print("********** GENERAZIONE ", genCounter + 1, "********** \n")
    print("\n########## SPECIE ##########\n")
    for i in species:
        print(i)
    print("\n=================================")
    print("\n########## REAZIONI ##########\n")
    for i in reactions:
        print(i)
    print("\n=================================")
    print("\n########## FREQUENZE ##########\n")
    for i in frequences:
        print(i)
    print("\n=================================")
    print("\n########## CATALISI ##########\n")
    for i in catalysis:
        print(i, ":", catalysis[i])
    print("\n=================================")
    print("\n########## EVENTI ##########\n")
    for i in events:
        print(i)
    print("\n=================================")
    print("\n")


def initialize(species, frequences, reactions, catalysis, events):
    species.clear()
    frequences.clear()
    reactions.clear()
    catalysis.clear()
    events.clear()


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

    species = [] 
    frequences = []
    reactions = []
    catalysis = {}
    events = []  

    # Inizializzo le liste e dizionari che conterranno tutte le informazioni lette da chimica.txt
    initialize(species, frequences, reactions, catalysis, events)
    model = protoZero(INPUT_FILE, TIME, POINTS, COEFF, species, frequences, reactions, catalysis, events)

    # Creo il foglio dove scrivere i dati
    wb = Workbook()
    ws = wb.active

    speciesColumn = {}  # Dizionario che mappa la colonna con il nome della specie

    # Aggiungi la colonna TIME al foglio di lavoro
    ws.cell(row=1, column=1, value="TIME")
    speciesColumn[0] = "TIME"


    orderedSpecies = []
    for k in species:
        orderedSpecies.append(k.name)
    
    orderedSpecies.sort()
    orderedSpeciesColumn = {}
    
    rowIndex = 1
    columnIndex = 2
    for j in range(0, TRAJECTORIES):
        for i in orderedSpecies:
            cell = ws.cell(row=rowIndex, column=columnIndex, value=i)
            orderedSpeciesColumn[columnIndex-1] = i
            redBG = PatternFill(start_color="E97451", end_color="E97451", fill_type="solid")
            cell.fill = redBG

            columnIndex += 1

    speciesColumn.update(orderedSpeciesColumn)
    #print(speciesColumn)

    continueRow = 2 # Indice della riga da cui continuare a scrivere i dati
    continueTime = 0
    stopSimulation = False
    
    for genCounter in range(0, GENERATIONS):
        initialize(species, frequences, reactions, catalysis, events)
        stopGeneration = False
        dummyValues = {} # Dizionario temporanea per salvare i valori delle specie

        model = protoZero(INPUT_FILE, TIME, POINTS, COEFF, species, frequences, reactions, catalysis, events)
        os.system('cls' if os.name == 'nt' else 'clear')
        outputData(species, reactions, catalysis, events, frequences, genCounter)

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
                            #print("continueTime + trajectory[j][i] =",continueTime, "+", trajectory[j][i])
                            continueTime += trajectory[j][i]
                            stopGeneration = True
                            stopSimulation = False     
                    else:
                        ws.cell(row=i+continueRow, column=j+1, value=int(trajectory[j][i]))
                
                if stopGeneration:
                    continueRow += i

                    # Salva i valori delle specie in dummyValues
                    for j in range(1, len(trajectory)-1):
                        dummyValues[speciesColumn[j]] = int(trajectory[j][i])
                    
                    #print("DummyValues: ", dummyValues)

                    # Cancella il file "input/dummyChimica.txt" se esiste
                    if os.path.exists("input/KBVNRDL1Qp_Chimica.txt"):
                        os.remove("input/KBVNRDL1Qp_Chimica.txt")

                    # Crea un nuovo file di testo chiamato KBVNRDL1Qp_Chimica nella cartella input in scrittura, conterra' le nuove quantita' delle specie
                    # e le reazioni chimiche originali
                    with open("input/KBVNRDL1Qp_Chimica.txt", "w") as file:
                        INPUT_FILE = "input/KBVNRDL1Qp_Chimica.txt"
                        #print(catalysis)                        
                        
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


    os.system('cls' if os.name == 'nt' else 'clear')
    
    wb.save(OUTPUT_FILE) # Salva il file excel
    
    # Cancella il file "input/dummyChimica.txt" se esiste
    if os.path.exists("input/KBVNRDL1Qp_Chimica.txt"):
        os.remove("input/KBVNRDL1Qp_Chimica.txt")

    # Aggiungi una colonna tra la 1 e la 2 al file excel
    ws.insert_cols(2)

    # Aggiorna l'header della colonna aggiunta
    ws.cell(row=1, column=2, value="ABSOLUTE TIME")
    # Inizializza la colonna "ABSOLUTE TIME" a 0
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=2, max_col=2):
        for cell in row:
            cell.value = 0
    
    # Aggiorna il valore della prima cella di "ABSOLUTE TIME" con il valore della prima cella della prima colonna
    ws.cell(row=2, column=2, value=ws.cell(row=2, column=1).value)

    # Aggiorna i valori della colonna "ABSOLUTE TIME"
    for row in range(3, ws.max_row + 1):
        if ws.cell(row=row - 1, column=2).value < ws.cell(row=row, column=1).value:
            ws.cell(row=row, column=2).value = ws.cell(row=row, column=1).value
        else:
            ws.cell(row=row, column=2).value = ws.cell(row=row - 1, column=2).value + ws.cell(row=row, column=1).value
   

    # Salva il file excel
    wb.save(OUTPUT_FILE)

    print("\n########## SIMULAZIONE TERMINATA ##########\n")
    quotes()
    

if __name__ == "__main__":
    main()
