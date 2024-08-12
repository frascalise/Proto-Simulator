import gillespy2    #  type: ignore


def outputData(species, catalysis):
    print("\n")
    for i in species:
        print("Nome: ", i.name, "\tQuantità: ", i.initial_value)
    print("\n")
    print("CATALISI: ", catalysis)
    print("\n")


#   Scorrere il dizionario catalysis e aggiungere a reactions le reazioni di catalisi.
#   Per ogni specie che ha un valore diverso da 0 nel dizionario catalysis, aggiungere una reazione.
#   Esempio reazione:
#       A	>	A	+	Lipid	;	valore_catalisi_nel_dizionario
#   species_name:   è il nome della specie nelle prime righe della chimica
#   catalysis_value:    è il valore di catalisi associato alla specie
def addCatalysisReactions(model, catalysis, frequences, reactionCounter, reactions):
    for species_name, catalysis_value in catalysis.items():
        if float(catalysis_value) > 0:
            frequences.append(gillespy2.Parameter(name = 'k' + str(reactionCounter), expression = 1))
            reaction = gillespy2.Reaction(  name = 'catalysis_' + species_name,
                                            reactants = {species_name: 1},
                                            products = {species_name: 1, list(catalysis.keys())[0]: 1},
                                            propensity_function = str(float(catalysis_value)) + "*" + species_name + "*" + str(frequences[reactionCounter].name))
            reactionCounter = reactionCounter + 1
            #print(reaction)
            model.add_reaction(reaction)
            reactions.append(reaction)


def protoZero(INPUT_FILE, TIME, POINTS, COEFF, MAX_LIPID, DIVISION, LIPID_EXP, species, frequences, reactions, catalysis, events):
    # Inizializzo il modello
    model = gillespy2.Model()

    with open(INPUT_FILE, 'r') as file:
        lines = file.readlines()
    
    readSpecies = True  # Quanto incontrerò la riga che separa le specie dalle reazioni diventerà False
    reactionCounter = 0 # Conto le reazioni che vengono inserite dal file chimica.txt

    counterSpecies = 0
    for line in lines: 
        columns = line.split('\t')                  # Divido la riga in colonne usando tab come separatore 
        columns = [col.strip() for col in columns]  # Rimuovo i caratteri di inizio/fine riga

        ### Se la riga è vuota allora la skippo ###
        if len(columns) < 2:
            readSpecies = False
            continue

        ### Leggo specie dell'ambiente dal file e le salvo in 'species[]' ###
        if readSpecies:  
            species.append(gillespy2.Species(name = columns[0], initial_value = int(columns[1])))
            catalysis[columns[0]] = columns[2]      # Salvo le catalisi in un dizionario

            # La prima specie che leggo è SEMPRE il lipide
            if counterSpecies == 0:                 
                lipidName = columns[0]

            counterSpecies = counterSpecies + 1

        ### Poi leggo le reazioni e le loro frequenze ###                
        else:
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
            #   AGGIORNAMENTO 05-05-2024: Al posto di vol inserisco COEFF*lipidName
            #   AGGIORNAMENTO 12-08-2024: Al posto di COEFF*lipidName inserisco COEFF*(lipidName^1.5)

            reactantsNumber = len(reactants)    
            propensityFunction = str(frequences[reactionCounter].name)

            if reactantsNumber != 0:
                
                for i in reactants:
                    propensityFunction += "*" + str(i)

                if reactantsNumber > 1:
                    propensityFunction += "/(" + "(" + str(COEFF) + "*(" + str(lipidName) + "^" + str(LIPID_EXP) + "))"

                    for i in range(1, (reactantsNumber - 1)):
                        propensityFunction += "*" + "(" + str(COEFF) + "*(" + str(lipidName) + "^" + str(LIPID_EXP) + "))"

                    propensityFunction += ")"

            # Costruisco la reazione, con GillesPy2 non si può creare una reazione senza almeno un reagente o un prodotto
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

            #print(reaction)
            reactions.append(reaction)
            reactionCounter = reactionCounter + 1

    species.append(gillespy2.Species(name = "tempo", initial_value = 0))    # Aggiungo la specie tempo all'ambiente
    
    model.add_species(species)
    model.add_reaction(reactions)
    
    addCatalysisReactions(model, catalysis, frequences, reactionCounter, reactions)    # Aggiungo le reazioni di catalisi
    model.add_parameter(frequences)

    ### EVENTI ###
    #   Aggiungo il trigger per l'evento di divisione
    trig = gillespy2.EventTrigger(expression = "L > " + str(MAX_LIPID))       # L'evento si attiva quando l'espressione diventa FALSO (da VERO) o VERO (da Falso)
    
    #  Aggiungo gli eventi di divisione
    #print("EVENTI: ")
    
    #  Evento di divisione del lipide
    evento = gillespy2.EventAssignment(variable = list(catalysis.keys())[0], expression = f"{list(catalysis.keys())[0]}/2")
    events.append(evento)
    #print(evento)

    # Con questo ciclo for simulo l'avvenimento di una divisione dividendo tutte le specie per DIVISION
    for species_name in list(catalysis.keys())[1:]:
        evento = gillespy2.EventAssignment(variable = species_name, expression = f"{species_name}*"+ str(DIVISION))
        events.append(evento)
        #print(evento)
    
    # Con questo ciclo for imposto tutti i k delle reazioni (le loro frequenze) a 0 in modo tale che non avvengano piu' reazioni
    for parametro in frequences:    
        evento = gillespy2.EventAssignment(variable = parametro.name, expression = "0.0")
        events.append(evento)
        #print(evento)

    # Creo l'evento che assegnerà il tempo esatto della divisione della protocellula alla specie tempo
    evento = gillespy2.EventAssignment(variable = "tempo", expression = "t")
    events.append(evento)
    #print(evento)

    e_div = gillespy2.Event(name = "e_div", assignments = events , trigger = trig)

    model.add_event([e_div])

    # Set the timespan for the simulation.
    tspan = gillespy2.TimeSpan.linspace(t = TIME, num_points = POINTS)
    model.timespan(tspan)

    #outputData(species, catalysis)

    return model
