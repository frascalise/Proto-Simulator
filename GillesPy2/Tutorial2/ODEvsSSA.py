import gillespy2
import matplotlib.pyplot as plt

def ToggleSwitch(parameter_values=None):
    # Initialize the model.
    gillespy2.Model(name="toggle_switch")

    # Inizializza il modello
    model = gillespy2.Model()

    # Define parameters.

    alpha1 = gillespy2.Parameter(name='alpha1', expression=1)
    alpha2 = gillespy2.Parameter(name='alpha2', expression=1)
    beta = gillespy2.Parameter(name='beta', expression=2.0)
    gamma = gillespy2.Parameter(name='gamma', expression=2.0)
    mu = gillespy2.Parameter(name='mu', expression=1.0)
    model.add_parameter([alpha1, alpha2, beta, gamma, mu])

    # Define molecular species.
    U = gillespy2.Species(name='U', initial_value=10)
    V = gillespy2.Species(name='V', initial_value=10)
    model.add_species([U, V]) 

    # Define reactions.
    cu = gillespy2.Reaction(name="r1", reactants={}, products={U:1}, propensity_function="alpha1/(1+pow(V,beta))")
    cv = gillespy2.Reaction(name="r2", reactants={}, products={V:1}, propensity_function="alpha2/(1+pow(U,gamma))")
    du = gillespy2.Reaction(name="r3", reactants={U:1}, products={}, rate=mu)
    dv = gillespy2.Reaction(name="r4", reactants={V:1}, products={}, rate=mu)
    model.add_reaction([cu, cv, du, dv])

    tspan = gillespy2.TimeSpan.linspace(100, 101)
    model.timespan(tspan)
    return model

model = ToggleSwitch()

trajectoriesNumber = int(input("Numero di traiettorie: "))

s_results = model.run(number_of_trajectories = trajectoriesNumber)                    # Senza valori, di default si usa l'algoritmo SSA
d_results = model.run(number_of_trajectories = trajectoriesNumber, algorithm="ODE")   # Specificandolo, si puo usare l'algoritmo ODE

for index in range(0, trajectoriesNumber):
    trajectory = s_results[index]
    plt.plot(trajectory['time'], trajectory['U'], 'red')
    plt.plot(trajectory['time'], trajectory['V'], 'green')

plt.title("Stochastic Switch")
plt.show()

for index in range(0, trajectoriesNumber):
    trajectory = d_results[index]
    plt.plot(trajectory['time'], trajectory['U'], 'red')
    plt.plot(trajectory['time'], trajectory['V'], 'green')

plt.title("Deterministic Switch")
plt.show()
