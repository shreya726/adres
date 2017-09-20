#!/usr/bin/python
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


import adres.scores.lexical as lex
import adres.scores.sublexical as sublex
import adres.scores.semantic_lexical as semantic_lex
import adres.scores.handle_csv as handle_csv

from adres.forms import UploadFileForm


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def upload(request):
    return render(request, 'upload.html')


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def index(request):
    # Dictionary with variable names from html.
    variable_names = {}

    # which scoring system?
    semantic = False
    if 'scoringsystem' in request.session:
        semantic = request.session['scoringsystem'] == 'ADRES Semantic'
    for i in range(1, 11):
        target_var = 'target' + str(i)
        response_var = 'response' + str(i)
        sub_lex_var = 'sublex' + str(i)
        lex_var = 'lex' + str(i)
        if target_var in request.session:
            variable_names[target_var] = request.session[target_var]
        if response_var in request.session:
            variable_names[response_var] = request.session[response_var]
        if sub_lex_var in request.session:
            variable_names[sub_lex_var] = request.session[sub_lex_var]
        if lex_var in request.session:
            variable_names[lex_var] = request.session[lex_var]
    request.session.clear()  # not sure if this works
    variable_names['scoringsystem'] = semantic
    return render(request, 'adres.html', variable_names)

#
# For 10 inputs on /adres page
#

def score(request):
    targets = []
    last3 = []
    semantic = False
    
    # For ADRES Semantic system.
    if request.POST.get('scoringsystem', '') == 'ADRES Semantic':
        semantic = True

    # Going through each input - storing each score as variable
    
    for i in range(1, 11):

        # initializing variable names
        target_var = 'target' + str(i)
        response_var = 'response' + str(i)
        sub_lex_var = 'sublex' + str(i)
        lex_var = 'lex' + str(i)

        # getting variables 
        target = request.POST.get(target_var, '')
        targets += [target]
        response = request.POST.get(response_var, '')

        # saving variables in session
        request.session[target_var] = target
        request.session[response_var] = response

        # scoring
        sublex_score = sublex.SublexicalScore(target=target, response=response).score()
        if semantic:
            lex_score = semantic_lex.SemanticLexicalScore(target=target, response=response, last3=last3,
                                                          targets=targets).score()

        else:
            lex_score = lex.LexicalScore(target=target, response=response, last3=last3, targets=targets).score()
        
        # updating last3 responses for perseveration
        if len(last3) > 2 and response != '':
            last3 = last3[1:]
            last3 += [response]

        # if no input 
        if target == '' and response == '':
            continue

        # saving results to session
        request.session[sub_lex_var] = 'Sublexical: ' + str(sublex_score)
        request.session[lex_var] = 'Lexical: ' + str(lex_score)

    return redirect('/adres')

#
# Download csv of scores
#

def script(request):
    csv = UploadFileForm(request.POST, request.FILES)

    if csv is not None:
        csv_input = request.FILES['csv'].read()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ADRES-scores.csv"'
        semantic = request.POST.get('scoringsystem', '') == 'ADRES Semantic'
        c = Context({
            'data': handle_csv.parse_csv(csv_input, semantic),
        })
        t = loader.get_template('clean_csv.txt')
        request.session['csv'] = 'csv_loaded'
        response.write(t.render(c))
        return response
    return redirect('/upload')
