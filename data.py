import numpy as np
import pandas as pd
from math import exp
import matplotlib.pyplot as plt


def removeAccents(word):
    return word.replace("á", "a").replace("à", "a").replace("é", "e").replace("è", "e").replace("í", "i").replace("ì", "i").replace("ó", "o").replace("ò", "o").replace("ú", "u").replace("ü", "u").replace("ù", "u")

def allWordsLengthN(N):
    words = []
    with open("possible_words.txt", "r") as f:
        for word in f:
            word = word.strip()
            word = removeAccents(word.strip())
            if len(word) == N and word not in words:
                words = np.append(word, words)
    return words

def getDistLengthN(N):
    words, probs = [], []
    with open(f"freq_sorted_{N}.txt", "r+") as f:
        for line in f:
            words.append(line.split()[1])
            probs.append(float(line.split()[2]))
    return pd.DataFrame({"word": words, "prob": probs})

def sigmoid(x):
    return 1/(1 + exp(-x))

def saveWordsProb():
    """
    To add a missing word, open "freq_sorted_5.txt" and find the approximate position for the word
    Add a line with a temporary index and probability
    Run this function and check the new position and probability
    """
    toWrite = []
    words = np.array(getDistLengthN(5)["word"])
    xVals = np.linspace(-10, 10, len(words)) # CORTE PARA SIGMOID ESTA EN 3500 +- la mitad asi que asi se queda
    for i, x in enumerate(xVals):
        toWrite.append(f"{len(words) - i-1} {words[len(words)-i-1]} {sigmoid(x)}\n")
    toWrite.reverse()
    with open("freq_sorted_5.txt", "w+") as f:
        for line in toWrite:
            f.write(line)

def getProbFromWord(dist, word):
    return dist.loc[dist["word"]==word]["prob"].to_numpy()[0]

saveWordsProb()

def compare_rae_frecs(): # ZIPF
    indeces = []
    frecs_rel = []
    with open("rae_frecuencias.txt", "r") as f:
        rl = f.readlines()
        n = len(rl)
        frec_total = int(rl[1].strip().split("\t")[2].strip().replace(',',''))
        for line in rl[1:]:
            sline = line.strip().split("\t")
            frecs_rel.append(int(sline[2].strip().replace(',',''))/frec_total)
    for i in range(1, n):
        indeces.append(1/i)
    plt.loglog(range(n-1), frecs_rel)
    plt.loglog(range(n-1), indeces)
    plt.show()

# def saveWords():
#     words = []
#     with open("freq_sorted_5.txt", "r") as f:
#         for line in f:
#             sline = line.strip().split(" ")
#             words.append(sline[1])
#     words.sort()
#     with open("words.txt", "w+") as f:
#         for word in words:
#             f.write(f"{word}\n")
