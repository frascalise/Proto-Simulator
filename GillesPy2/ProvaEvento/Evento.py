import gillespy2
import matplotlib.pyplot as plt

    
def protoZero(parameter_values = None):
    
    # Inizializzo il modello
    model = gillespy2.Model()

    with open('chimica.txt', 'r') as file:
        lines = file.readlines()
    
    # Inizializzo gli che conterranno tutte le informazioni lette da chimica.txt
    species = [] 
    frequences = []
    reactions = []

    readSpecies = True  # Quanto incontrerò la riga che separa le specie dalle reazioni diventerà False
    reactionCounter = 0 # Conto le reazioni che vengono inserite dal file chimica.txt

    dummy_species = gillespy2.Species(name = "dummy", initial_value = 10000000000)
    species.append(dummy_species)

    for line in lines: 
        columns = line.split('\t')                  # Divido la riga in colonne usando tab come separatore 
        columns = [col.strip() for col in columns]  # Rimuovo i caratteri di inizio/fine riga

        if len(columns) < 2:                        # Se la riga è vuota allora la skippo
            readSpecies = False
            continue
        
        if readSpecies:                             # Leggo specie dell'ambiente dal file e le salvo in 'species[]'
            species.append(gillespy2.Species(name = columns[0], initial_value = int(columns[1])))

        else:                                       # Poi leggo le reazioni e le loro frequenze
            reactants = []
            products = []

            arrowFound = False      # Se ho trovato il carattere '>'
            semicolonFound = False  # Se ho trovato il carattere ';'

            for i in columns:
                if i == '>':
                    arrowFound = True
                elif i == ';':
                    semicolonFound = True
                elif semicolonFound:
                    frequence = float(i)
                elif arrowFound and i != '+': 
                    products.append(i)
                elif not arrowFound and i != '' and i != '+':
                    reactants.append(i)

            frequences.append(gillespy2.Parameter(name = 'k' + str(reactionCounter), expression = frequence))

            # FIXME: Sostituire 'propensity_function' con 'rate' e cercare di eliminare 'dummy_species'
            # IDEA: Provare ad aggiungere alla fine della riga '.add_reactant()' 
            reaction = gillespy2.Reaction(name = 'r' + str(reactionCounter), reactants = {dummy_species:1}, products = {}, rate = frequences[reactionCounter])

            for i in reactants:
                reaction.add_reactant(species=i, stoichiometry=1)
            for i in products:
                reaction.add_product(species=i, stoichiometry=1)

            print(reaction)
            reactions.append(reaction)

            reactionCounter = reactionCounter + 1
    
    for i in species:
        print("Nome: ", i.name, "\tQuantità: ", i.initial_value)

    model.add_species(species)
    model.add_parameter(frequences)
    model.add_reaction(reactions)

    trig = gillespy2.EventTrigger(expression = "A > 500")       # L'evento si attiva quando l'espressione diventa FALSO (da VERO) o VERO (da Falso)
    evento1 = gillespy2.EventAssignment(variable = "A", expression = "A/2")
    e_div = gillespy2.Event(name = "e_div", assignments = [evento1] , trigger = trig)

    model.add_event([e_div])

    # Set the timespan for the simulation.
    tspan = gillespy2.TimeSpan.linspace(t = 2000, num_points = 2001)
    model.timespan(tspan)
    return model

n_lanci=1 # Numero lanci da fare
model = protoZero()
results = model.run(number_of_trajectories = n_lanci)

for index in range(0, n_lanci):
    trajectory = results[index]
    plt.plot(trajectory['time'], trajectory['A'], 'red', label = 'A')
    plt.plot(trajectory['time'], trajectory['B'], 'green', label = 'B')
    plt.plot(trajectory['time'], trajectory['C'], 'orange', label = 'C')
    plt.plot(trajectory['time'], trajectory['AB'], 'blue', label = 'AB')
    plt.plot(trajectory['time'], trajectory['AC'], 'yellow', label = 'AC')
    plt.plot(trajectory['time'], trajectory['BC'], 'purple', label = 'BC')

plt.legend()
plt.title("Esempio GillesPy") 
plt.show()
