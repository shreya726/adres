#!/usr/bin/python
from nltk.corpus import wordnet
from nltk.corpus import wordnet as w
import pattern
from pattern.en import pluralize, comparative, superlative, lemma
from PyDictionary import PyDictionary
import enchant
usDict = enchant.Dict('en_US') 
ukDict = enchant.Dict('en_UK') 
pyDict = PyDictionary()

from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.http import HttpResponse

def index(request):
	sublexical = ''
	lexical = ''
	target = ''
	response = ''
	if 'target' in request.session:
		target = request.session['target']
	if 'response' in request.session:
		response = request.session['response']
	if 'sublexical' in request.session:
		sublexical = request.session['sublexical']
	if 'lexical' in request.session:
		lexical = request.session['lexical']
	# 	score = request.session['score']
	return render(request, 'adres.html',{'subLex':sublexical, 'lex':lexical, 'target':target, 'response':response})

def score(request):
	target = request.POST.get('target','')
	response = request.POST.get('response','')
	request.session['target'] = target
	request.session['response'] = response
	subLex = subLexScoring(target, response)
	#lex = lexical.scoring(target, response, [])[0]
	lex = lexScoring(target, response, [], [])[0]
	request.session['sublexical'] = subLex
	request.session['lexical'] = lex
	return redirect('/adres')

def subLexScoring(target, response):
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
    if response == "" or response == "-": return 0  
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

def lexScoring(target, response, last3,targets):
	target = target.lower() #Makes target lower case
	if len(response) > 1:
		#Makes all of the response other than the first letter lower-case.
		response = response[0] + response[1:].lower() 
	if "don't know" in response: return (0,response)
	if "not sure" in response: return (0, response)
	if ';' in response:
		#If multiple responses entered, take the last one afer 
		#semicolon as the whole response.
		response = response.split(';')[-1]
	
	if len(response) > 1:
		#Taking out spaces at the beginning and end of string
		while response[0] == " ": response = response[1:]
		while response[-1] == " ": response = response[:-1]

	if response.lower() == target:
		#Target
		return (9,response.lower())

	if response == '' or response == ' ':
		#No response
		return (0,response)
	
	elif not isWord(response,target,targets):

		if target in response.split():
			#If target is in the description,
			#treat as accurate response of 9.
			return (9,response)

		elif related_description(target, response):
			#Related description
			return (5,response)

		elif description(response,target): 
			#Unrelated description
			return (2,response)
		else: 
			#Non-word
			return (3,response)

	elif morphological_error(target, response):
		#Morphological errors
		return (8,response)
	else:
	#elif not related(response, target) and isWord(response,target):
		#Unrelated word 
		return (6,response)
	
def perseveration(response, last3):
	if response in last3: return True
	else: return False
	
def perseverationNonWord(response, last3,target):
	#In progress
	return False

def overlap(response, last3):
	for word in last3:
		if overlapWord(word, response): 
			return True
	return False

def overlapWord(wordInLast3, response):
	#Sets the longer word to wordInLast3
	if len(wordInLast3)!=len(response):
		longer = max(wordInLast3,response)
		response = min(wordInLast3, response)
		wordInLast3 = longer
	total = 0
	for i in response:
		#Checks the 50% overlap overall
		if i in wordInLast3:
			total+=1
	if float(total)/float(len(wordInLast3)) <= 0.5: return False
	#Overlap must be in order, 
	#but can have extraneous letters in between.

	for j in range(0,len(wordInLast3)):
		for i in range(0,len(response)):
			letters = 0
			if j > len(wordInLast3) -1: break
			if response[i] == wordInLast3[j]:
				letters +=1
				i+=1
				j+=1
				while i<len(response) and j<len(wordInLast3):
					if response[i] == wordInLast3[j]:
						letters +=1
						i+=1
					j+=1
				if float(letters)/float(len(wordInLast3)) >=0.5:
					return True
	return False 

def isWord(response,target,targets = []):
	#add all targets
	if response in targets: return True
	if len(response) < 2: 
		#Single letters are not counted as words.
		return False
	try:
		
		return usDict.check(response) or ukDict.check(response)

	except: 
		return False
	if not flag:
		if compound(response, target):
			#Checks for combinations of response and target, 
			#as well as hyphenated words where the target is in the word.
			return True
	return False

def related(response, target):
	if not isWord(response,target): 
		#Check if word for the call from related_description()
		return False 
	if response in target: return True
	if compound(response, target): return True
	
	return False
	
	# #Checks synonyms
	try:
		print('here')
		if response in pyDict.synonym(target): return True
		if target in pyDict.synonym(response): return True
	except:
		#Not a word
		return False

def description(response,target):
	if response[0] == '[' and response[-1] == ']':
		#Format for gestural descriptions
		return True
	if ' ' in response:
		total = 0
		areWords = 0
		for i in response.split():
			total +=1 
			if isWord(i,target): 
				areWords +=1
		#The number of non-words in the response must be
		#less than 50% to count as a description.	
		if float(areWords)/float(total) >= 0.5:
			return True
	return False

def morphological_error(target, response):
	if response == pluralize(target): 
		#Checks for the plural form of the target.
		return True
	if response == comparative(target) :
		#Checks for the comparative form of the target. 
		return True
	if response == superlative(target): 
		#Checks for the superlative form of the target.
		return True
	if lemma(target) == lemma(response): 
		#Check to see if the target and response share a lemma.
		return True
	return False

def related_description(target, response):
	if description(response,target):
		if response[0] == '[' and response[-1]==']':
			#Case of gestural descriptions
			words = response[1:-1].split()
		else: words = response.split()
		if target in words: return True
		
		for i in words:
			if target == i: return True
			#Check if any of the words in the description are related.
			if related(i, target):
				return True
			if morphological_error(target,i): 
				#Check if the lemmas of the words correlate.
				return True
	return False

#To prevent recursion with the compound word check in isWord()
#check if this is still needed since changes to compound()
global flag
flag = False

def compound(response, target):
	global flag
	flag = True

	if isWord(response+target,target): return True
	elif isWord(target+response,target): return True
	elif isWord(target+"-"+response,target): return True
	elif isWord(response+"-"+target,target): return True
	
	#Checks for hyphenated words where the target is in the response.
	if "-" in response:
		response = response.split('-')
		if len(response) >2: return False
		if target in response: return True
		if isWord(response[0],target) and isWord(response[1],target): return True
	return False