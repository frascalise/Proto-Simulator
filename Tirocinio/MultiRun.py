import os
import subprocess


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
    
    for i in range(1, n + 1):
        output_file = f"{base_output_file}_Sim{i}.xlsx"
        params['OUTPUT'] = output_file
        synthesis_file = f"{base_synthesis_file}_Sim{i}.xlsx"
        params['SYNTHESIS'] = synthesis_file
        write_params(params_path, params)

        print(f"Simulazione {i} di {n} in corso...")
        subprocess.run(['python3', 'Main.py'], capture_output=True, text=True)
        print(f"Simulazione {i} di {n} completata")
        print("\n-------------------------------------------\n")
    
    # Ripristinare i valori originali
    params['OUTPUT'] = original_output_file
    params['SYNTHESIS'] = original_synthesis_file
    write_params(params_path, params)

if __name__ == "__main__":
    params_path = 'input/params.txt'
    n = int(input("Quante volte vuoi eseguire main.py? "))
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    run_script(n, params_path)