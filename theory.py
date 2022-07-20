from itertools import product
from math import log2
import time
import numpy as np
import pandas as pd
from data import getDistLengthN

class Word:
    def __init__(self, word):
        self.word = word
        self.N = len(word)

    def guess(self, guess):
        answer = "2" * self.N
        counted = {}
        for i, letter in enumerate(guess):
            if letter not in counted:
                counted[letter] = 0
            if letter == self.word[i]:
                answer = replaceLetterAtIndex(answer, "0", i)
                counted[letter] += 1
        for i, letter in enumerate(guess):
            if letter in self.word:
                cntWord = self.word.count(letter)
                if cntWord > counted[letter] and answer[i] == "2":
                    answer = replaceLetterAtIndex(answer, "1", i)
                    counted[letter] += 1
        return answer


def replaceLetterAtIndex(word, letter, i):
    return word[:i] + letter + word[i+1:]

def guessProbabilities(word: Word, words):
    freqs = {}
    vars = product("012", repeat = word.N)
    for var in vars:
        freqs["".join(var)] = 0
    for guess in words:
        freqs[word.guess(guess)] += 1
    probs = {}
    total = len(words)
    if total != 0:
        for comb, freq in freqs.items():
            probs[comb] = freq/total
    return probs

def entropy(word, words):
    probs = guessProbabilities(word, words)
    sum = 0
    for comb, prob in probs.items():
        if prob != 0:
            sum -= prob * log2(prob)
    return sum

def entropyLst(possibilities, words, toPrint=True):
    entropies = {}
    total = len(words)
    t0 = time.time()
    for i, word in enumerate(words):
        entropies[word] = entropy(Word(word), possibilities)
        if toPrint:
            print(f"{word}: {entropies[word]}")
            print(f"completed {i+1}/{total} - {round(time.time() - t0, 8)}s")
    return entropies

def possibleSecrets(guess, answer, words):
    possibilities = []
    for word in words:
        if Word(word).guess(guess) == answer:
            possibilities.append(word)
    return possibilities

def bestGuess(possibilities, dist, toPrint=False):
    entropies = entropyLst(possibilities, np.array(dist["word"]), toPrint)
    entropiesDF = pd.DataFrame(entropies.items(), columns=["word", "entropy"])
    mergeDF = pd.concat([dist, entropiesDF["entropy"]], axis=1)
    mergeDF["prob*entr"] = mergeDF["prob"] * mergeDF["entropy"]
    mostProbable = mergeDF.iloc[mergeDF["prob"].idxmax()]["word"]
    mostEntropic = mergeDF.iloc[mergeDF["entropy"].idxmax()]["word"]
    bestOverall = mergeDF.iloc[mergeDF["prob*entr"].idxmax()]["word"]
    return mostEntropic

def bestPair(word, words, toPrint=False):
    t0 = time.time()
    pairs = []
    possibleAnswers = list(map(lambda x: "".join(x), product("012", repeat=5)))
    for i, answer in enumerate(possibleAnswers):
        if toPrint:
            print(f"{i+1} / {3**5}")
        entropies = entropyLst(possibleSecrets(word, answer, words), words, False)
        word2 = max(entropies, key=entropies.get)
        pairs.append(((word, word2), entropies[word]+entropies[word2]))
    pairs.sort(key=lambda x: x[1], reverse=True)
    print(time.time() - t0)
    return pairs[0][0][1], pairs[0][1]


def bestThird(word1, word2, words, toPrint=False):
    t0 = time.time()
    thirds = []
    possibleAnswers = list(map(lambda x: "".join(x), product("012", repeat=5)))
    for i, answer1 in enumerate(possibleAnswers):
        possibilities = possibleSecrets(word1, answer1, words)
        for j, answer2 in enumerate(possibleAnswers):
            if toPrint:
                print(f"{j+i*(3**5)+1} / {(3**5)**2}")
            possibilities = possibleSecrets(word2, answer2, possibilities)
            entropies = entropyLst(possibilities, words, False)
            word3 = max(entropies, key=entropies.get)
            thirds.append(((word1, word2, word3), entropies[word1]+entropies[word2]+entropies[word3]))
    thirds.sort(key=lambda x: x[1], reverse=True)
    print(time.time() - t0)
    return thirds[0][0][2], thirds[0][1]


"""
Para comprobar cuales son las mejores 2 palabras:
    - Obtenemos: entropies = entropyLst(words, words, toPrint)
    - Nos quedamos solo con las palabras que tengan entropia >= 6: top_entropies = dict(filter(lambda elem: elem[1] >= 6, entropies.items()))
    - Doble bucle: {entropyLst(words, top_words) y escoger el máximo de esto}
        - El externo es top_entropies y el interno entropies
        - Calcular la entropia resultante de usar esas dos palabras seguidas
    - Elegir la pareja de entropia maxima
"""

# CAREO, TRIAS

dist = getDistLengthN(5)
words = np.array(dist["word"])

# entropies = entropyLst(words, words, True)
# entropies_over6 = dict(filter(lambda elem: elem[1] >= 6, entropies.items()))

# pairs = []
# for i, word1 in enumerate(entropies_over6):
    # for j, answer in enumerate(possibleAnswers):
    #     print(f"{i*243+j} / {116*243}")
    #     entropies2 = entropyLst(possibleSecrets(word1, answer, words), words, False)
    #     word2 = max(entropies2, key=entropies2.get)
    #     pairs.append(((word1, word2), entropies[word1]+entropies2[word2]))

# print(pairs)
# print("----------------------")
# print(max(pairs, key=lambda x: x[1]))
