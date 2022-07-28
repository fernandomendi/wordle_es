import numpy as np
from data import getDistLengthN, getProbFromWord
from theory import possibleSecrets, bestQuadGuess

def quordle():
    dist = getDistLengthN(5)
    possibilities = [np.array(dist["word"]), np.array(dist["word"]), np.array(dist["word"]), np.array(dist["word"])]
    mostEntropic = "careo"
    i = 1
    while len(possibilities[0]) > 1 or len(possibilities[1]) > 1 or len(possibilities[2]) > 1 or len(possibilities[3]) > 1:
        print("-----------------------")
        print(f"Intento número {i}: ")
        print(f"La mejor palabra es {mostEntropic}")
        guess = input("Palabra elegida (pulsa ENTER para elegir la palabra sugerida): ")
        if guess == "":
            guess = mostEntropic
        for j in range(4):
            answer = input(f"Respuesta obtenida con este intento en la palabra {j+1}: ")
            if answer != "":
                poss = possibleSecrets(guess, answer, possibilities[j])
                print("Palabras posibles: ")
                for word in poss:
                    print(f"{word}: {round(getProbFromWord(dist, word), 4)}")
                if len(poss) == 0:
                    print("No hay palabras posibles, asegurate de introducir correctamente la respuesta. ")
                    exit()
                else:
                    print(f"Hay {len(poss)} palabras posibles")
                possibilities[j] = poss
        mostEntropic = bestQuadGuess(possibilities, dist)
        i += 1

# ----------------------------------------------------------------------

quordle()
