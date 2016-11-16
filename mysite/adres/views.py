#!/usr/bin/python
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
exec(open('lexical.py').read())
exec(open('semanticLexical.py').read())
exec(open('sublexical.py').read())
from adres.models import Document
from adres.forms import DocumentForm

def index(request):
	sublexical = ''
	lexical = ''
	target = ''
	response = ''
	variables = {}
	semantic = False
	if 'scoringsystem' in request.session:
		#print('here')
		if request.session['scoringsystem'] == 'ADRES Semantic':
			semantic = True
	for i in range(1,11):
		print(request.session)
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
	variables['scoringsystem'] = semantic
	return render(request, 'adres.html',variables)

def score(request):
	targets = []
	last3 = []
	semantic = False
	#For ADRES Semantic system.
	if request.POST.get('scoringsystem','') == 'ADRES Semantic':
		semantic = True
	for i in range(1,11):
		targetVar = 'target'+str(i)
		responseVar = 'response'+str(i)
		subLexVar = 'sublex'+str(i)
		lexVar = 'lex'+str(i)
		target = request.POST.get(targetVar,'')
		targets += [target]
		response = request.POST.get(responseVar,'')
		request.session[targetVar] = target
		request.session[responseVar] = response
		subLex = subLexScoring(target, response)
		print(semantic)
		if semantic:
			lex = semanticLexScoring(target, response, last3, targets)[0]
		else:
			lex = lexScoring(target, response, last3, targets)[0]
		if len(last3) > 2:
			last3 = last3[1:]
		if response!= '':
			last3 += [response]
		if target == '' and response == '':
			continue
		request.session[subLexVar] = subLex
		request.session[lexVar] = lex
	
	return redirect('/adres')

def script(request):
	#http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example
	# csv = request.POST.get('csvfile',None)
	# print(type(csv))
	# print(csv)
	# if csv!=None:
	# 	csv_input = csv.reader(open(csv, 'rU'), dialect=csv.excel_tab)
	# 	sublex_scores = []
	# 	lex_scores = []
	# 	for row in csv_input:
	# 		try:
	# 			words = [line.strip() for line in row[0].split(',')]
	# 		except:
	# 			print('Not comma separated')
	# 			pass
	# 		try:
	# 			sublex_scores += [subLexScoring(words[0],words[1])]
	# 			lex_scores += [lexScoring(words[0],words[1],[],[])[0]]
	# 		except:
	# 			print('ASCII error')
	# 			pass
	# 	request.session['csv'] = lex_Scores[0]
	# return redirect('/adres')
	# Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        #if form.is_valid():
        newdoc = Document(docfile = request.FILES['docfile'])
        newdoc.save()
        csv = newdoc
        print(type(csv))
        # Redirect to the document list after POST
    return redirect('/adres')
    # else:
    #     form = DocumentForm() # A empty, unbound form

    # # Load documents for the list page
    # documents = Document.objects.all()

    # # Render list page with the documents and the form
    # return render_to_response(
    #     'myapp/list.html',
    #     {'documents': documents, 'form': form},
    #     context_instance=RequestContext(request)
    # )
