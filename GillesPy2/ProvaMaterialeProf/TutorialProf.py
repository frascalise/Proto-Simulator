import gillespy2
import matplotlib.pyplot as plt

    
def protoZero(parameter_values=None):
    
    # Inizializzo il modello
    model = gillespy2.Model()

    # Definizione dei parametri della frequenza delle reazioni
    k_c = gillespy2.Parameter(name='k_c', expression=2.0)
    k_x = gillespy2.Parameter(name='k_x', expression=2.0)
    k_chi = gillespy2.Parameter(name='k_chi', expression=0.01)
    k_cost = gillespy2.Parameter(name='k_cost', expression=0.01)
    k_add = gillespy2.Parameter(name='k_add', expression=1.0)
    k_remove = gillespy2.Parameter(name='k_remove', expression=0.05)

    model.add_parameter([k_c, k_x, k_chi, k_cost, k_add, k_remove])

    # Definizione delle specie e della loro quantità
    c = gillespy2.Species(name='C', initial_value=20)
    x = gillespy2.Species(name='X', initial_value=30)
    model.add_species([c, x])

    # The list of reactants and products for a Reaction object are
    # each a Python dictionary in which the dictionary keys are
    # Species objects and the values are stoichiometries of the
    # species in the reaction.

    #REAZIONI PRESENTI: X->X+C (X catalizza la creazione di lipide); X->X+X (X catalizza la propria creazione)
    r_c = gillespy2.Reaction(name="C_creation", reactants={x:1}, products={x:1,c:1},propensity_function="k_c/pow(C+k_cost,1.5)")#propensità variabile
    r_x = gillespy2.Reaction(name="X_creation", reactants={x:1}, products={x:2},propensity_function="k_x/pow(C+k_cost,1.5)")#propensità variabile

    r_Cadd = gillespy2.Reaction(name="r_Cadd", reactants={}, products={c:1},rate="k_add")
    r_Xadd = gillespy2.Reaction(name="r_Xadd", reactants={}, products={x:1},rate="k_add")

    #r_Cremove = gillespy2.Reaction(name="r_Cremove", reactants={c:1}, products={},rate="k_remove")
    #r_Xremove = gillespy2.Reaction(name="r_Xremove", reactants={x:1}, products={},rate="k_remove")
    model.add_reaction([r_c, r_x, r_Cadd, r_Xadd])

    # MV definizione dell'evento di divisione
    trig = gillespy2.EventTrigger(expression="C < 25") # qui ho utilizzato una funzione lambda (da vedere se si riesce ad inserire qualcosa di più complesso)
    evAss1=gillespy2.EventAssignment(variable="C", expression="C/2")# divisione dei lipidi
    evAss2=gillespy2.EventAssignment(variable="X", expression="X*0.35")# divisione del materiale interno (con perdita)
    evento=gillespy2.Event(name="div",assignments=[evAss1,evAss2],trigger=trig)# definizione dell'evento
    model.add_event([evento])# Inserimento dell'evento

    # Set the timespan for the simulation.
    tspan = gillespy2.TimeSpan.linspace(t=200, num_points=201)
    model.timespan(tspan)
    return model

n_lanci=1 # Numero lanci da fare
model = protoZero()
results = model.run(number_of_trajectories=n_lanci)

for index in range(0, n_lanci):
    trajectory = results[index]
    plt.plot(trajectory['time'], trajectory['C'], 'red')
    plt.plot(trajectory['time'], trajectory['X'],   'green')

plt.title("Esempio GillesPy") 
plt.show()
