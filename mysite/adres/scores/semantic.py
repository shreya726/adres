from nltk.corpus import wordnet as w
from pattern.en import pluralize, comparative, superlative, lemma
from PyDictionary import PyDictionary
pyDict = PyDictionary()
import enchant
usDict = enchant.Dict('en_US')
ukDict = enchant.Dict('en_UK')

def related(response, target):
    if not is_word(response):
        # Check if word for the call from related_description()
        return False
    if response in target: return True
    if compound(response, target): return True

    # #Checks synonyms
    try:
        target_synset = w.synsets(target)[0]
        response_synset = w.synsets(response)[0]
        if target_synset.path_similarity(response_synset) > 0.1:
            return True
        #print('here')
        if response in pyDict.synonym(target): return True
        if target in pyDict.synonym(response): return True
    except:
        # Not a word
        return False
    return False

def is_word(response):
    # add all targets
    if len(response) < 2:
        # Single letters are not counted as words.
        return False
    try:
        return usDict.check(response) or ukDict.check(response)
    except:
        return False

def description(response, target):
    if response[0] == '[' and response[-1] == ']':
        # Format for gestural descriptions
        return True
    if ' ' in response:
        total = 0
        areWords = 0
        for i in response.split():
            total += 1
            if is_word(i):
                areWords += 1
        # The number of non-words in the response must be
        # less than 50% to count as a description.
        if float(areWords) / float(total) >= 0.5:
            return True
    return False


def morphological_error(target, response):
    if response == pluralize(target):
        # Checks for the plural form of the target.
        return True
    if response == comparative(target):
        # Checks for the comparative form of the target.
        return True
    if response == superlative(target):
        # Checks for the superlative form of the target.
        return True
    if lemma(target) == lemma(response):
        # Check to see if the target and response share a lemma.
        return True
    return False


def related_description(target, response):
    if description(response, target):
        if response[0] == '[' and response[-1] == ']':
            # Case of gestural descriptions
            words = response[1:-1].split()
        else:
            words = response.split()
        if target in words: return True

        for i in words:
            if target == i: return True
            # Check if any of the words in the description are related.
            if related(i, target):
                return True
            if morphological_error(target, i):
                # Check if the lemmas of the words correlate.
                return True
    return False


# To prevent recursion with the compound word check in isWord()
# check if this is still needed since changes to compound()
global flag
flag = False


def compound(response, target):
    global flag
    flag = True

    if is_word(response + target):
        return True
    elif is_word(target + response):
        return True
    elif is_word(target + "-" + response):
        return True
    elif is_word(response + "-" + target):
        return True

    # Checks for hyphenated words where the target is in the response.
    if "-" in response:
        response = response.split('-')
        if len(response) > 2: return False
        if target in response: return True
        if is_word(response[0]) and is_word(response[1]): return True
    return False