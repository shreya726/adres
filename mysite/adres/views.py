#!/usr/bin/python
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
exec(open('lexical.py').read())
exec(open('sublexical.py').read())

def index(request):
	sublexical = ''
	lexical = ''
	target = ''
	response = ''
	variables = {}
	for i in range(1,11):
		targetVar = 'target'+str(i)
		responseVar = 'response'+str(i)
		subLexVar = 'sublex'+str(i)
		lexVar = 'lex'+str(i)
		if targetVar in request.session:
			variables[targetVar] = request.session[targetVar]
		if responseVar in request.session:
			variables[responseVar] = request.session[responseVar]
		if subLexVar in request.session:
			variables[subLexVar] = request.session[subLexVar]
		if lexVar in request.session:
			variables[lexVar] = request.session[lexVar]
	return render(request, 'adres.html',variables)

def score(request):
	targets = []
	last3 = []
	for i in range(1,11):
		targetVar = 'target'+str(i)
		responseVar = 'response'+str(i)
		subLexVar = 'sublex'+str(i)
		lexVar = 'lex'+str(i)
		target = request.POST.get(targetVar,'')
		targets += [target]
		response = request.POST.get(responseVar,'')
		if len(last3) > 2:
			last3 = last3[1:]
		last3 += [response]
		if target == '' and response == '':
			continue
		request.session[targetVar] = target
		request.session[responseVar] = response
		subLex = subLexScoring(target, response)
		lex = lexScoring(target, response, last3, targets)[0]
		request.session[subLexVar] = subLex
		request.session[lexVar] = lex
	return redirect('/adres')

