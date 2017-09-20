#!/usr/bin/python

import matplotlib.pyplot as plt
import StringIO

import adres.scores.lexical as lexical
import adres.scores.sublexical as sublexical
import adres.scores.semantic_lexical as semantic_lexical


def score(targets, responses, semantic=False):
    # Header row
    scores = [tuple(['Target', 'Response', 'Sublexical Score', 'Lexical Score'])]

    # Checks for perseveration
    last3 = []

    for target, response in zip(targets, responses):
        try:
            # Accounting for weird formats in csv files
            response.decode('ascii')
        except:
            pass

        else:
            # Sublexical score
            sublex_score = sublexical.SublexicalScore(target=target, response=response).score()

            # Lexical score based on choice of scoring system
            if semantic:
                lex_score = semantic_lexical.SemanticLexicalScore(target=target, response=response,
                                                                  last3=last3, targets=targets).score()
            else:
                lex_score = lexical.LexicalScore(target=target, response=response,
                                                 last3=last3, targets=targets).score()
            scores += [tuple([target, response, sublex_score, lex_score])]

            # Noting last 3 targets and responses to monitor perseveration.
            if len(last3) < 6 and lex_score != 0:
                last3 += [response]
                last3 += [target]
            else:
                if lex_score != 0:
                    last3 = last3[2:]
                    last3.append(response)
                    last3.append(target)
                else:
                    if len(last3) > 1: last3[1] = target

    return scores


def parse_csv(file, semantic):
    targets = []
    responses = []
    for row in file.split('\n'):
        if len(row) < 2: continue
        # Getting first two columns
        row = row.split(',')
        targets.append(row[0])
        responses.append(row[1])
    scores = score(targets=targets, responses=responses, semantic=semantic)
    return scores

def graph(scores):
    #you can pass a StringIO object to pyplot.savefig(), and get the PNG file content by StringIO.getvalue().
    #
    scores_xy = [(x,y) for (t,r,x,y) in scores[1:]]
    points_xy = list(set(scores_xy))
    frequency_xy = {}
    for point in points_xy:
        frequency_xy[point] = scores_xy.count(point)
    x, y = zip(*frequency_xy.keys())
    s = list(frequency_xy.values())
    plt.scatter(x,y,s=s)
    plt.xlabel('Sublexical', fontsize=16)
    plt.ylabel('Lexical', fontsize=16)

    buf = StringIO.StringIO()
    plt.savefig(buf)

    return buf
    #pass
