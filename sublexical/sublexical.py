def main(target, response):
    """ Scores"""
    target = target.lower()
    response = response.lower()
    if "don't know" in response: return 0
    if "not sure" in response: return 0
    if ';' in response:
        '''If multiple responses entered, take the last one afer semicolon as the whole response.
        '''
        response = response.split(';')[-1]
    if len(response) > 1:
        while response[0] == " ": response = response[1:]
        while response[-1] == " ": response = response[:-1]
    if response == target: return 9
    if response == "" or response == "-" or response == "–": return 0  
    errors = 0
    if addition(target, response, errors): return 7
    overlap = overlapWord(target, response)
    if not overlap and len(response) == len(target): return 2
    elif not overlap: return 1
    if deletion(target, response, errors): return 4
    if transposition(target, response, errors): return 6
    if substitution(target, response, errors): return 5
    else: 
        if errors < 2: print("Not multiple errors?")
        return 3

def overlapWord(target, response):
    """ Determines overlap"""
    len_t = len(target)
    letters = 0
    overlap = 0
    copyr = response
    for i in range(len(target)):
        if target[i] in copyr:
            letters += 1
            copyr = remove(copyr, target[i])
    overlap = float(letters)/float(len_t)
    return overlap >=0.5

def addition(target, response, errors):
    """ Checks for additions"""
    lengthDiff = len(response) - len(target)
    if lengthDiff > 0:
        errors += lengthDiff
        for t in target:
            if t not in response: return False
    return lengthDiff == 1
   

def transposition(target, response, errors):
        """ Checks for transposition"""
        transpositions = 0
        if len(target) == len(response):
            for i in response:
                if i not in target:
                    transpositions +=1
            errors += transpositions
            return transpositions == 1
        return False
   
def substitution(target, response, errors):
    """ Checks for substitutions """
    if len(response) == len(target):
        i = 0
        subs = 0
        for i in range(0,len(response)):
            if response[i] !=target[i]:
                subs +=1
        errors += subs
        return subs == 1
    return False

def deletion(target, response, errors):
    """ Checks for deletion"""
    lengthDiff = len(target) - len(response)
    if lengthDiff > 0:
        for r in response:
            if r not in target: return False 
        errors += lengthDiff
        return lengthDiff == 1
 