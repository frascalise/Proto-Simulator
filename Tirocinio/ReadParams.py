def readInput():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "INPUT":
                    return "input/" + parameter_value
                
def readOutput():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "OUTPUT":
                    return "output/" + parameter_value
                
def readTime():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "TIME":
                    return int(parameter_value)
                
def readPoints():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "POINTS":
                    return int(parameter_value)
                
def readTrajectories():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "TRAJECTORIES":
                    return int(parameter_value)

def readCoeff():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "COEFF":
                    return float(parameter_value)