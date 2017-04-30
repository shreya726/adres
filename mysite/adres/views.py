#!/usr/bin/python
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import Context, loader
from django.http import HttpResponse

import mysite.scores.lexical as lex
import mysite.scores.sublexical as sublex
import mysite.scores.semantic_lexical as semantic_lex
import mysite.scores.handle_csv as handle_csv

from adres.models import Document
from adres.forms import UploadFileForm

def index(request):
	# Dictionary with variable names from html.
	variable_names = {}
	semantic = False
	if 'scoringsystem' in request.session:
		if request.session['scoringsystem'] == 'ADRES Semantic':
			semantic = True
	for i in range(1,11):
		target_var = 'target'+str(i)
		response_var = 'response'+str(i)
		sub_lex_var = 'sublex'+str(i)
		lex_var = 'lex'+str(i)
		if target_var in request.session:
			variable_names[target_var] = request.session[target_var]
		if response_var in request.session:
			variable_names[response_var] = request.session[response_var]
		if sub_lex_var in request.session:
			variable_names[sub_lex_var] = request.session[sub_lex_var]
		if lex_var in request.session:
			variable_names[lex_var] = request.session[lex_var]
	if 'csv' in request.session:
		variable_names['csv'] = 'test'
	variable_names['scoringsystem'] = semantic
	return render(request, 'adres.html',variable_names)

def score(request):
	targets = []
	last3 = []
	semantic = False
	#For ADRES Semantic system.
	if request.POST.get('scoringsystem','') == 'ADRES Semantic':
		semantic = True
	for i in range(1,11):
		target_var = 'target'+str(i)
		response_var = 'response'+str(i)
		sub_lex_var = 'sublex'+str(i)
		lex_var = 'lex'+str(i)
		target = request.POST.get(target_var,'')
		targets += [target]
		response = request.POST.get(response_var,'')
		request.session[target_var] = target
		request.session[response_var] = response

		sublex_score = sublex.SublexicalScore(target=target, response=response).score()
		if semantic:
			lex_score = semantic_lex.SemanticLexicalScore(target=target, response=response, last3=last3, targets=targets).score()

		else:
			lex_score = lex.LexicalScore(target=target, response=response, last3=last3, targets=targets).score()
		if len(last3) > 2 and response!= '':
			last3 = last3[1:]
			last3 += [response]

		if target == '' and response == '':
			continue
		request.session[sub_lex_var] = sublex_score
		request.session[lex_var] = lex_score
	
	return redirect('/adres')

def script(request):
	csv = UploadFileForm(request.POST, request.FILES)

	if csv is not None:
		csv_input = request.FILES['csv'].read()
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="ADRES-scores.csv"'
		semantic =  request.POST.get('scoringsystem', '') == 'ADRES Semantic'
		c = Context({
			'data': handle_csv.parse_csv(csv_input, semantic),
		})
		t = loader.get_template('clean_csv.txt')
		response.write(t.render(c))
		return response
	return redirect('/upload')
