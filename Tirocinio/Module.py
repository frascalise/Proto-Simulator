import gillespy2


def protoZero(INPUT_FILE, TIME, POINTS, species, frequences, reactions):
    
    # Inizializzo il modello
    model = gillespy2.Model()

    with open(INPUT_FILE, 'r') as file:
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

            # Riempio le varie liste con i dati della chimica a seconda di cosa ho letto
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


            #    FORMULE PER PROPENSITY_FUNCTION
            #       >   A   ;   k1                                  |   propensity_function = "k1"
            #       A   >   ;   k1                                  |   propensity_function = "k1*A"
            #       A   +   B   >   AB   ;   k1                     |   propensity_function = "k1*A*B/vol"
            #       A   +   B   +   C   >   AB   ;   k1             |   propensity_function = "k1*A*B*C/(vol*vol)"
            #       A   +   B   +   C   +   D   >   AB   ;   k1     |   propensity_function = "k1*A*B*C*D/(vol*vol*vol)"

            #   reactantsNumber:    mi dice il numero di reagenti presenti nella reazione che ho appena letto
            #   propensityFunction: e' la stringa che contiene la formula da inserire in propensityFunction e viene costruita a seconda
            #                       della reazione che consideriamo (vedi formule sopra)
            reactantsNumber = len(reactants)    
            propensityFunction = str(frequences[reactionCounter].name)

            if reactantsNumber != 0:
                
                for i in reactants:
                    propensityFunction += "*" + str(i)

                if reactantsNumber > 1:
                    propensityFunction += "/(vol" 

                    for i in range(1, (reactantsNumber - 1)):
                        propensityFunction += "*vol"

                    propensityFunction += ")"

            if reactants:
                reaction = gillespy2.Reaction(  name = 'r' + str(reactionCounter), 
                                                reactants = {reactants[0]:1}, 
                                                products = {}, 
                                                propensity_function = propensityFunction)
                reactants.pop(0)
            elif products:
                reaction = gillespy2.Reaction(  name = 'r' + str(reactionCounter), 
                                                reactants = {}, 
                                                products = {products[0]:1}, 
                                                propensity_function = propensityFunction)
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
    tspan = gillespy2.TimeSpan.linspace(t = TIME, num_points = POINTS)
    model.timespan(tspan)
    return model
