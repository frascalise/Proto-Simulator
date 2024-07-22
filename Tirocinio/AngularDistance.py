import math
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

DISTANZA_ANGOLARE = "output/DistanzaAngolare.xlsx"

def angular_distance_calc():
    wb = load_workbook(DISTANZA_ANGOLARE)
    ws = wb.active

    # Salvo i dati di ogni simulazione in un dizionario
    simulation_data = {}
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=2, max_col=ws.max_column):
        sim_index = ws.cell(row=row[0].row, column=1).value
        simulation_data[sim_index] = [cell.value for cell in row]
    
    # Creo il nuovo foglio "Distanza Angolare"
    ws_new = wb.create_sheet("Distanza Angolare")
    
    # Ottengo l'elenco delle simulazioni
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
    
    # Calcolo dell'angolo in gradi tra i vettori
    for i in range(len(simulations)):
        sim1 = simulations[i]
        vector1 = simulation_data[sim1]
        ws_new.cell(row=i + 2, column=i + 2, value=0)  # Diagonale principale = 0 (distanza con se stesso)
        
        for j in range(i + 1, len(simulations)):
            sim2 = simulations[j]
            vector2 = simulation_data[sim2]
            
            # Calcolo il coseno dell'angolo tra i vettori
            dot_product = sum(a * b for a, b in zip(vector1, vector2))
            magnitude1 = math.sqrt(sum(a**2 for a in vector1))
            magnitude2 = math.sqrt(sum(b**2 for b in vector2))
            
            if magnitude1 != 0 and magnitude2 != 0:
                cosine_angle = dot_product / (magnitude1 * magnitude2)
                # Calcolo l'angolo in radianti e poi lo converto in gradi
                angle_radians = math.acos(cosine_angle)
                angle_degrees = math.degrees(angle_radians)
            else:
                angle_degrees = None  # Gestione del caso di divisione per zero
            
            ws_new.cell(row=i + 2, column=j + 2, value=angle_degrees)
            ws_new.cell(row=j + 2, column=i + 2, value=angle_degrees)
    
    # Salvo il file Excel
    wb.save(DISTANZA_ANGOLARE)

if __name__ == "__main__":
    angular_distance_calc()
    print(f"Distanza angolare calcolata e salvata in {DISTANZA_ANGOLARE}\n")