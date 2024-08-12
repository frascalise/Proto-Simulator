import random

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
                
def readSynthesis():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "SYNTHESIS":
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
                
def readGenerations():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "GENERATIONS":
                    return int(parameter_value)

def readMaxLipid():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "MAX_LIPID":
                    return int(parameter_value)

def readTotalSim():
    with open("input/AngularParams.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "TOTAL_SIM":
                    return int(parameter_value)

def readDivision():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "DIVISION":
                    return float(parameter_value)

def readLipidExp():
    with open("input/params.txt", "r") as file:
        for line in file:
            columns = line.split('\t')
            columns = [col.strip() for col in columns]

            if len(columns) == 2:
                parameter_type, parameter_value = columns
                if parameter_type == "LIPID_EXP":
                    return float(parameter_value)


def quotes():
    quotes = [
        "Science is organised knowledge. Wisdom is organised life.",
        "Science may set limits to knowledge, but should not set limits to imagination.",
        "Research is what I’m doing when I don’t know what I’m doing.",
        "The most exciting phrase to hear in science, the one that heralds new discoveries, is not ‘Eureka!’ (I found it!) but ‘That’s funny …’",
        "Everything is theoretically impossible, until it is done.",
        "The reward of the young scientist is the emotional thrill of being the first person in the history of the world to see something or to understand something. Nothing can compare with that experience.",
        "What you learn from a life in science is the vastness of our ignorance.",
        'When do you think a person dies?\nWhen a bullet from a pistol pierces his heart? No.\nWhen he is attacked by an incurable disease? No.\nWhen he eats a soup of deadly poisonous mushrooms? No.\nA man dies when people forget him! - Dr. Hiriluk',
        "I'll Do What You Can't Do, And You Do What I Can't Do.",
        "The Flower Of Friendship Can Bloom Even In Hell.",
        "If You Ask This Old Man Anything… Then I Will Quit Being A Pirate! \nIf It’s A Boring Adventure, I Don’t Want It!",
        "If You Don’t Take Risks, You Can’t Create A Future",
        "Life would be tragic if it weren't funny.",
        "The past, like the future, is indefinite and exists only as a spectrum of possibilities."
        ]
    print(quotes[random.randint(0, len(quotes) - 1)], "\n\n")