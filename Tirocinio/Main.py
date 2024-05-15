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
    TRAJECTORIES = readTrajectories()
    COEFF = readCoeff()
    GENERATIONS = readGenerations()

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


    # Aggiungi la colonna TIME al foglio di lavoro
    ws.cell(row=1, column=1, value="TIME")
    
    rowIndex = 1
    columnIndex = 2

    for j in range(0, TRAJECTORIES):
        for i in species:
            cell = ws.cell(row=rowIndex, column=columnIndex, value=i.name)
            redBG = PatternFill(start_color="E97451", end_color="E97451", fill_type="solid")
            cell.fill = redBG

            columnIndex += 1

    rowIndex = 2
    for genCounter in range(0, GENERATIONS):
        species = [] 
        frequences = []
        reactions = []
        catalysis = {}

        model = protoZero(INPUT_FILE, TIME, POINTS, COEFF, species, frequences, reactions, catalysis)
        results = model.run(number_of_trajectories = TRAJECTORIES)

        columnIndex = 2

        for index in range(0, TRAJECTORIES):
            trajectory = results[index]
            
            for i in range(1, len(results['time'])):
                ws.cell(row=i+1, column=1, value=results['time'][i])

            for i in species:
                #plt.plot(trajectory['time'], trajectory[i.name], label = i.name)

                for yIndex in range(1, len(trajectory[i.name])):
                    ws.cell(row=rowIndex, column=columnIndex, value=int(trajectory[i.name][yIndex]))
                    rowIndex += 1
                
                columnIndex += 1
                rowIndex = 2

        #plt.legend()
        #plt.title("Esempio GillesPy") 
        #plt.show()

    # Salva il workbook su file
    wb.save(OUTPUT_FILE)


if __name__ == "__main__":
    main()
