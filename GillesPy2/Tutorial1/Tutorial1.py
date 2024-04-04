import gillespy2
import matplotlib.pyplot as plt

def Dimerization(parameter_values=None):
    # First call the gillespy2.Model initializer.
    model = gillespy2.Model()

    # Define parameters for the rates of creation and dissociation.
    k_c = gillespy2.Parameter(name='k_c', expression=0.05)
    k_d = gillespy2.Parameter(name='k_d', expression=0.08)
    k_p = gillespy2.Parameter(name='k_p', expression=0.002)
    k_e = gillespy2.Parameter(name='k_p', expression=0)
    model.add_parameter([k_c, k_d, k_p])

    # Define variables for the molecular species representing M & D.
    m = gillespy2.Species(name='monomer', initial_value=30)
    d = gillespy2.Species(name='dimer',   initial_value=20)
    p = gillespy2.Species(name='prova',   initial_value=15)
    model.add_species([m, d, p])

    # The list of reactants and products for a Reaction object are
    # each a Python dictionary in which the dictionary keys are
    # Species objects and the values are stoichiometries of the
    # species in the reaction.
    r_c = gillespy2.Reaction(name="r_creation", rate=k_c, reactants={m:2}, products={d:1})
    r_d = gillespy2.Reaction(name="r_dissociation", rate=k_d, reactants={d:1}, products={m:2})
    r_p = gillespy2.Reaction(name="r_prova", rate=k_p, reactants={d:1, m:1}, products={p:1})
    r_e = gillespy2.Reaction(name="r_esempio", rate=k_p, reactants={p:1}, products={})

    model.add_reaction([r_e])

    # Set the timespan for the simulation.
    # t -> tempo della simulazione | num_points -> numero di punti che voglio avere nel tempo t
    tspan = gillespy2.TimeSpan.linspace(t = 100, num_points = 101)
    model.timespan(tspan)
    return model

model = Dimerization()
results = model.run(number_of_trajectories=10)

for index in range(0, 10):
    trajectory = results[index]
    plt.plot(trajectory['time'], trajectory['monomer'], 'red')
    plt.plot(trajectory['time'], trajectory['prova'],   'green')
    plt.plot(trajectory['time'], trajectory['dimer'],   'blue')

plt.title("Esempio GillesPy")
plt.show()
