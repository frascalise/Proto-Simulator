import math
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

DISTANZA_ANGOLARE = "output/DistanzaAngolare.xlsx"
ANGULAR_PARAMS = "input/AngularParams.txt"

def read_params(file_path):
    params = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            if key == "SPECIES":
                params["SPECIES"] = value.split(',')
            elif key == "GENERATIONS":
                params["GENERATIONS"] = int(value)
    return params

def angular_distance_calc():
    params = read_params(ANGULAR_PARAMS)
    species = params.get("SPECIES", [])
    required_generations = params.get("GENERATIONS", 0)

    if not species:
        print("Nessuna specie trovata nel file di parametri.")
        return

    try:
        wb = load_workbook(DISTANZA_ANGOLARE)
        ws = wb.active
    except Exception as e:
        print(f"Errore durante il caricamento del file: {e}")
        return

    # Ottieni gli indici delle colonne per le specie specificate
    species_indices = {}
    for i, cell in enumerate(ws[1], start=1):
        if cell.value in species:
            species_indices[cell.value] = i

    if not species_indices:
        print("Nessuna delle specie specificate è presente nel file.")
        return

    # Salvo i dati delle specie specificate di ogni simulazione in un dizionario
    simulation_data = {}
    generations_data = {}
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        sim_index = ws.cell(row=row[0].row, column=1).value
        generations = ws.cell(row=row[0].row, column=2).value  # Supponendo che il numero di generazioni sia nella seconda colonna
        data = []
        for species_name, col_index in species_indices.items():
            data.append(ws.cell(row=row[0].row, column=col_index).value)
        simulation_data[sim_index] = data
        generations_data[sim_index] = generations

    # Creo un nuovo foglio per la distanza angolare
    ws_new = wb.create_sheet("Distanza Angolare")

    # Ottieni l'elenco delle simulazioni
    simulations = list(simulation_data.keys())

    # Inserisco l'intestazione della matrice
    ws_new.cell(row=1, column=1, value="Index")
    for i in range(2, len(simulations) + 2):
        ws_new.cell(row=1, column=i, value=simulations[i-2])
        ws_new.cell(row=i, column=1, value=simulations[i-2])

    # Cambio colore della prima riga e della prima colonna
    bg_fill = PatternFill(start_color="4287f5", end_color="4287f5", fill_type="solid")
    for cell in ws_new[1]:
        cell.fill = bg_fill
    for row in ws_new.iter_rows(min_col=1, max_col=1):
        for cell in row:
            cell.fill = bg_fill

    # Calcolo della distanza angolare (angolo normale tra i vettori)
    for i in range(len(simulations)):
        sim1 = simulations[i]
        vector1 = simulation_data[sim1]
        ws_new.cell(row=i + 2, column=i + 2, value=0)  # Diagonale principale = 0 (distanza con se stesso)

        for j in range(i + 1, len(simulations)):
            sim2 = simulations[j]
            vector2 = simulation_data[sim2]

            # Controlla se entrambe le simulazioni hanno completato il numero richiesto di generazioni
            if generations_data[sim1] < required_generations or generations_data[sim2] < required_generations:
                angle = "Non Valida"
            else:
                # Calcolo il coseno dell'angolo tra i vettori
                dot_product = sum(a * b for a, b in zip(vector1, vector2))
                magnitude1 = math.sqrt(sum(a**2 for a in vector1))
                magnitude2 = math.sqrt(sum(b**2 for b in vector2))

                # Calcolo l'angolo (distanza angolare) in gradi
                if magnitude1 != 0 and magnitude2 != 0:
                    cosine_angle = dot_product / (magnitude1 * magnitude2)
                    angle = math.degrees(math.acos(cosine_angle))
                else:
                    angle = "Non Valida"  # Gestione del caso di divisione per zero

            ws_new.cell(row=i + 2, column=j + 2, value=angle)
            ws_new.cell(row=j + 2, column=i + 2, value=angle)

    # Salvo il file Excel
    try:
        wb.save(DISTANZA_ANGOLARE)
        print(f"Distanza angolare calcolata e salvata in {DISTANZA_ANGOLARE}")
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")

if __name__ == "__main__":
    angular_distance_calc()