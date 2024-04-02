import gillespy2

def ToggleSwitch(parameter_values=None):
    # Initialize the model.
    gillespy2.Model(name="toggle_switch")

    # Define parameters.
    model = None

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
    cu = gillespy2.Reaction(name="r1", reactants={}, products={U:1},
                  propensity_function="alpha1/(1+pow(V,beta))")
    cv = gillespy2.Reaction(name="r2", reactants={}, products={V:1},
                  propensity_function="alpha2/(1+pow(U,gamma))")
    du = gillespy2.Reaction(name="r3", reactants={U:1}, products={},
                  rate=mu)
    dv = gillespy2.Reaction(name="r4", reactants={V:1}, products={},
                  rate=mu)
    model.add_reaction([cu, cv, du, dv])

    tspan = gillespy2.TimeSpan.linspace(0, 100, 101)
    model.timespan(tspan)
    return model

modello = ToggleSwitch()

s_results = modello.run()                 # Senza valori, di default si usa l'algoritmo SSA
d_results = modello.run(algorithm="ODE")  # Specificandolo, si puo usare l'algoritmo ODE

s_results.plot(title="Stochastic Switch")
d_results.plot(title="Deterministic Switch")

s_results.show()
d_results.show()
