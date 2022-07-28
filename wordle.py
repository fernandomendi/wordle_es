import numpy as np
from data import getDistLengthN, getProbFromWord
from theory import possibleSecrets, bestGuess

def wordle():
    # N = int(input("Longitud de las palabras: "))
    dist = getDistLengthN(5)
    possibilities = np.array(dist["word"])
    mostEntropic = "careo"
    i = 1
    while len(possibilities) > 1:
        print("-----------------------")
        print(f"Intento número {i}: ")
        print(f"La mejor palabra es {mostEntropic}")
        guess = input("Palabra elegida (pulsa ENTER para elegir la palabra sugerida): ")
        if guess == "":
            guess = mostEntropic
        answer = input("Respuesta obtenida con este intento: ")
        possibilities = possibleSecrets(guess, answer, possibilities)
        print("Palabras posibles: ")
        for word in possibilities:
            print(f"{word}: {round(getProbFromWord(dist, word), 4)}")
        if len(possibilities) == 0:
            print("No hay palabras posibles, asegurate de introducir correctamente la respuesta. ")
            break
        else:
            print(f"Hay {len(possibilities)} palabras posibles")
            mostEntropic = bestGuess(possibilities, dist)
            i += 1

# ----------------------------------------------------------------------

wordle()
