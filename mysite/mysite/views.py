#!/usr/bin/python
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
exec(open('lexical.py').read())
exec(open('sublexical.py').read())
from adres.models import Document
from adres.forms import DocumentForm
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
	if 'csv' in request.session:
		variables['csv'] = 'test'
	return render(request, 'adres.html',variables)