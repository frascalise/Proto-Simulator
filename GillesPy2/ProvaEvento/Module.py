import gillespy2


def protoZero(species, frequences, reactions):
    
    # Inizializzo il modello
    model = gillespy2.Model()

    with open('chimica3.txt', 'r') as file:
        lines = file.readlines()
    
    readSpecies = True  # Quanto incontrerò la riga che separa le specie dalle reazioni diventerà False
    reactionCounter = 0 # Conto le reazioni che vengono inserite dal file chimica.txt

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

            # Riempio le varie liste con i dati della chimica
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
            # IDEA: Aggiungere 'reactants' e 'products' con un for unendolo ai due for sotto.
            #       Se i 'reactants' sono vuoti allora inizializzo la reazione con il products e poi faccio 
            #       'add_product()' e 'add_reactant()'

            if reactants:
                reaction = gillespy2.Reaction(  name = 'r' + str(reactionCounter), 
                                                reactants = {reactants[0]:1}, 
                                                products = {}, 
                                                propensity_function = str(frequences[reactionCounter].name))
                reactants.pop(0)
            elif products:
                reaction = gillespy2.Reaction(  name = 'r' + str(reactionCounter), 
                                                reactants = {}, 
                                                products = {products[0]:1}, 
                                                propensity_function = str(frequences[reactionCounter].name))
                products.pop(0)
                
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

    trig = gillespy2.EventTrigger(expression = "A > 100")       # L'evento si attiva quando l'espressione diventa FALSO (da VERO) o VERO (da Falso)
    evento1 = gillespy2.EventAssignment(variable = "A", expression = "A/2")
    e_div = gillespy2.Event(name = "e_div", assignments = [evento1] , trigger = trig)

    model.add_event([e_div])

    # Set the timespan for the simulation.
    tspan = gillespy2.TimeSpan.linspace(t = 30, num_points = 31)
    model.timespan(tspan)
    return model
