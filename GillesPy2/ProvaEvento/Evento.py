#   SPECIE: [ A (20) | B (30) | C (40) ]
#      
#   FREQUENZE: [ k_add (1.00) | k_remove (0.05) | k_ab (0.01) | k_ac (0.01) | k_bc (0.01) | k_abc (1.00) | k_acb (1.00) | k_bca (1.00) ]      
#   
#   CSTR:
#       • > A   k_add
#       • > B   k_add
#       • > C   k_add
#       • A >   k_remove
#       • B >   k_remove
#       • C >   k_remove
#
#   CONDENSAZIONI:
#       • A + B > AB    k_ab
#       • A + C > AC    k_ac
#       • B + C > BC    k_bc
#
#   ROTTURE CATALIZZATE:
#       • AB + C > A + B + C    k_abc
#       • AC + B > A + C + B    k_acb
#       • BC + A > B + C + A    k_bca 
#

import gillespy2
import matplotlib.pyplot as plt

    
def protoZero(parameter_values = None):
    
    # Inizializzo il modello
    model = gillespy2.Model()

    # --------------- SPECIE ---------------
    a = gillespy2.Species(name = 'A', initial_value = 100)
    b = gillespy2.Species(name = 'B', initial_value = 100)
    c = gillespy2.Species(name = 'C', initial_value = 100)
    ab = gillespy2.Species(name = 'AB', initial_value = 0)
    ac = gillespy2.Species(name = 'AC', initial_value = 0)
    bc = gillespy2.Species(name = 'BC', initial_value = 0)

    model.add_species([a, b, c, ab, ac, bc])

    # ---------- FREQUENZA REAZIONI ----------
    k_add = gillespy2.Parameter(name = 'k_add', expression = 1.0)
    k_remove = gillespy2.Parameter(name = 'k_remove', expression = 0.05)
    k_ab = gillespy2.Parameter(name = 'k_ab', expression = 0.01)
    k_ac = gillespy2.Parameter(name = 'k_ac', expression = 0.01)
    k_bc = gillespy2.Parameter(name = 'k_bc', expression = 0.01)
    k_abc = gillespy2.Parameter(name = 'k_abc', expression = 1)
    k_acb = gillespy2.Parameter(name = 'k_acb', expression = 1)
    k_bca = gillespy2.Parameter(name = 'k_bca', expression = 1)

    model.add_parameter([k_add, k_remove, k_ab, k_ac, k_bc, k_abc, k_acb, k_bca])

    # --------------- REAZIONI ---------------
    #  CSTR 
    r_Aadd = gillespy2.Reaction(name = "r_Aadd", reactants = {}, products = {a:1}, rate = "k_add")
    r_Badd = gillespy2.Reaction(name = "r_Badd", reactants = {}, products = {b:1}, rate = "k_add")
    r_Cadd = gillespy2.Reaction(name = "r_Cadd", reactants = {}, products = {c:1}, rate = "k_add")
    r_Aremove = gillespy2.Reaction(name = "r_Aremove", reactants = {a:1}, products = {}, rate = "k_remove")
    r_Bremove = gillespy2.Reaction(name = "r_Bremove", reactants = {b:1}, products = {}, rate = "k_remove")
    r_Cremove = gillespy2.Reaction(name = "r_Cremove", reactants = {c:1}, products = {}, rate = "k_remove")

    #  CONDENSAZIONI 
    r_ab = gillespy2.Reaction(name = "r_ab", reactants = {a:1, b:1}, products = {ab:1}, rate = "k_ab")
    r_ac = gillespy2.Reaction(name = "r_ac", reactants = {a:1, c:1}, products = {ac:1}, rate = "k_ac")
    r_bc = gillespy2.Reaction(name = "r_bc", reactants = {b:1, c:1}, products = {bc:1}, rate = "k_bc")

    #  ROTTURE CATALIZZATE 
    r_abc = gillespy2.Reaction(name = "r_abc", reactants = {ab:1, c:1}, products = {a:1, b:1, c:1}, propensity_function = "k_abc")
    r_acb = gillespy2.Reaction(name = "r_acb", reactants = {ac:1, b:1}, products = {a:1, c:1, b:1}, propensity_function = "k_acb")
    r_bca = gillespy2.Reaction(name = "r_bca", reactants = {bc:1, a:1}, products = {b:1, c:1, a:1}, propensity_function = "k_bca")

    model.add_reaction([r_Aadd, r_Badd, r_Cadd, r_Aremove, r_Bremove, r_Cremove, r_ab, r_ac, r_bc, r_abc, r_acb, r_bca])

    # -------------- EVENTI --------------
    trig = gillespy2.EventTrigger(expression = "AB < 50")       # L'evento si attiva non appena questa espressione diventa FALSA (si triggera)
    evento1 = gillespy2.EventAssignment(variable = "AB", expression = "AB/2")
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
    plt.plot(trajectory['time'], trajectory['AB'], 'purple', label = 'AB')
    plt.plot(trajectory['time'], trajectory['AC'], 'blue', label = 'AC')
    plt.plot(trajectory['time'], trajectory['BC'], 'yellow', label = 'BC')

plt.legend()
plt.title("Esempio GillesPy") 
plt.show()
