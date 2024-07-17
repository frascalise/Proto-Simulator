import math
import os
import platform
import subprocess
from openpyxl import Workbook, load_workbook               # type: ignore
from openpyxl.styles import PatternFill     # type: ignore


DISTANZA_ANGOLARE = "output/DistanzaAngolare.xlsx"

def read_params(file_path):
    params = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            params[key] = value
    return params

def write_params(file_path, params):
    with open(file_path, 'w') as file:
        for key, value in params.items():
            file.write(f"{key}\t{value}\n")


def run_script(n, params_path):
    params = read_params(params_path)
    
    # Salvare i valori originali
    original_output_file = params['OUTPUT']
    original_synthesis_file = params['SYNTHESIS']
    
    base_output_file = original_output_file.replace('.xlsx', '')
    base_synthesis_file = original_synthesis_file.replace('.xlsx', '')

    synthesis_files = []
    
    for i in range(1, n + 1):
        output_file = f"{base_output_file}_Sim{i}.xlsx"
        params['OUTPUT'] = output_file
        synthesis_file = f"{base_synthesis_file}_Sim{i}.xlsx"
        params['SYNTHESIS'] = synthesis_file
        synthesis_files.append(f"output/{synthesis_file}")
        write_params(params_path, params)

        print(f"Simulazione {i} di {n} in corso...")
        subprocess.run(['python3', 'Main.py'], capture_output=True, text=True)
        print(f"Simulazione {i} di {n} completata")
        print("\n-------------------------------------------\n")
    
    # Ripristinare i valori originali
    params['OUTPUT'] = original_output_file
    params['SYNTHESIS'] = original_synthesis_file
    write_params(params_path, params)
    
    return synthesis_files


def angular_distance_data(synthesis_files):
    # Inizializza il nuovo workbook
    wb_new = Workbook()
    ws_new = wb_new.active
    ws_new.title = "Dati Simulazione"
    
    # Flag per indicare se la riga di intestazione è già stata copiata
    header_copied = False
    
    for file in synthesis_files:
        wb = load_workbook(file)
        ws = wb.active
        
        if not header_copied:
            # Copia la riga di intestazione
            header = [cell.value for cell in ws[1]]
            ws_new.append(header)
            header_copied = True
        
        # Prendi l'ultima riga del foglio
        last_row = [cell.value for cell in ws[ws.max_row]]
        ws_new.append(last_row)
    
    # Rimuovi le colonne specificate
    columns_to_remove = ["TIME", "ABSOLUTE TIME", "tempo"]
    columns_to_delete = []
    
    for col in ws_new.iter_cols(min_row=1, max_row=1, max_col=ws_new.max_column):
        if col[0].value in columns_to_remove:
            columns_to_delete.append(col[0].column)
    
    for col_num in reversed(columns_to_delete):  # Rimuovi le colonne dalla fine all'inizio
        ws_new.delete_cols(col_num)
    
    # Salva il nuovo file Excel
    wb_new.save(DISTANZA_ANGOLARE)


def addIndexSimulazione(ws):
    # Inserisce la nuova colonna "Index Simulazione"
    ws.insert_cols(1)
    ws.cell(row=1, column=1, value="Index Simulazione")
    
    # Popola la prima colonna con valori "Simulazione1", "Simulazione2", ecc.
    for i in range(2, ws.max_row + 1):
        ws.cell(row=i, column=1, value=f"Simulazione{i-1}")
    
    # Cambia il colore della prima riga
    bg_fill = PatternFill(start_color="4287f5", end_color="4287f5", fill_type="solid")
    for cell in ws[1]:
        cell.fill = bg_fill


def angular_distance_calc():
    wb = load_workbook(DISTANZA_ANGOLARE)
    ws = wb.active

    # Inserisce la nuova colonna "Index Simulazione"
    addIndexSimulazione(ws)

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
    
    # Calcolo della distanza angolare (coseno dell'angolo tra i vettori)
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
            
            # Calcolo il coseno dell'angolo (distanza angolare)
            if magnitude1 != 0 and magnitude2 != 0:
                cosine_angle = dot_product / (magnitude1 * magnitude2)
            else:
                cosine_angle = None  # Gestione del caso di divisione per zero
            
            ws_new.cell(row=i + 2, column=j + 2, value=cosine_angle)
            ws_new.cell(row=j + 2, column=i + 2, value=cosine_angle)
    
    # Salvo il file Excel
    wb.save(DISTANZA_ANGOLARE)
    

def play_beep():
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 500)  # Frequenza di 1000 Hz per 500 ms
    elif platform.system() == 'Darwin':  # macOS
        import subprocess
        subprocess.run(['afplay', '-t', '0.5', '/System/Library/Sounds/Hero.aiff'])
        subprocess.run(['afplay', '-t', '0.5', '/System/Library/Sounds/Submarine.aiff'])
        subprocess.run(['afplay', '-t', '0.5', '/System/Library/Sounds/Morse.aiff'])
        subprocess.run(['afplay', '-t', '0.5', '/System/Library/Sounds/Purr.aiff'])
    else:
        print("Sistema operativo non supportato per la riproduzione del suono.")


if __name__ == "__main__":
    # ** ESEGUO N VOLTE LA SIMULAZIONE **
    params_path = 'input/params.txt'
    n = int(input("Quante volte vuoi eseguire main.py? "))
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    synthesis_files = run_script(n, params_path)

    # ** CALCOLO LA DISTANZA ANGOLARE **
    angular_distance_data(synthesis_files)
    angular_distance_calc()
    print(f"Distanza angolare salvata in {DISTANZA_ANGOLARE}\n")

    play_beep()