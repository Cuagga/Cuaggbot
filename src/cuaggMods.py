# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 16:03:31 2021

@author: Cuagga
"""
import requests
import time
from loginCuagg import login
import pandas as pd
import numpy
import re

soft_headers = {"User-Agent" : "CuaggBot (https://fr.wikipedia.org/wiki/Utilisateur:Cuaggbot)"}
botUN ='Cuaggbot'


url = 'https://fr.wikipedia.org/w/api.php'





def getEditToken(page, S):
    params_0 = {
		"action":"query",
		"meta":"tokens",
		"type":"csrf",
		"format":"json",
		"titles": page,
		}
    
    r = S.get(url=url, params= params_0, headers=soft_headers)
    data = r.json()
    edit_token = data["query"]["tokens"]["csrftoken"]
    #page_id = data["query"]["pageids"][0] #retrieve the page_title id, needed for the next line.
    
    
    return edit_token

def inport(page, S, maxAtt = 5):
    URL = "https://fr.wikipedia.org/w/api.php"
    time.sleep(1)
    PARAMS = {
        "action": "parse",
        "page": page,
        "prop":"wikitext",
        "format": "json",
        "utf8":1
    }
    réussite = False
    attempts = 0
    while réussite == False and attempts < maxAtt:
        try:
            r = S.post(url=URL, params=PARAMS, timeout=5)
            return r.json()["parse"]["wikitext"]["*"]
        except:
            attempts += 1
            time.sleep(10)
            print('Réessai')
            continue
    
def fetch(page, chaine, start=0):
    try:
        return page.index(chaine, start)
    except ValueError:
        return -1

def browse(cat, S, cmcont=''):
    scope = []
    URL = 'https://fr.wikipedia.org/w/api.php'
    PARAMS = {
        'action':'query',
        'prop':'links',
        'list':'categorymembers',
        'format':'json',
        'cmtitle':cat,
        'cmlimit':'500',
        'cmcontinue':cmcont
        }
    
    r = S.post(url=URL, params=PARAMS)
    data = r.json()
    for k in data['query']['categorymembers']:
        scope.append(k['title'])
    suite = True
    while suite:
        try:
            cont = data['continue']['cmcontinue']
            PARAMS.__setitem__('plcontinue', cont)
            scope += browse(cat, S, cont)
            suite = False
        except:
            suite = False
    return scope

def edit(page, text, S, summary = '', minor=1, isBot=1, maxTries=5):
    wait = 10
    retry = True
    tries = 0
    while retry == True and tries <= maxTries:
        
        try:
            editToken = getEditToken(page, S)
        except:
            tries += 1
            time.sleep(2)
            continue
        params0 = {
			"action":"edit",
			"format":"json",
			"title": page,
			"text": text,
			"summary": summary,
			"minor": minor,
			"bot": isBot,
			"assert":"user",
			"maxlag": 5,
            "token": editToken,
			}
        req = S.post(url, data=params0)
        data = req.json()
        try:
            
            result = data['edit']['result']
            if result=='Success':
                retry = False
            else:
                print('Réessai sur la page' + page)
                print(result)
                time.sleep(wait)
        except:
            print('Erreur')
            if data['error']['code'] == 'assertuserfailed':
                login(S)
            else:
                print('Non fait')
                print(data['error']['code'])
                print(f"Skipping {page}")
                return 0
            time.sleep(1)
        finally:
            tries += 1

def éval(projet, start='', end = -1, alias=''):
    #Remplissage du scope
    if alias == '':
        alias = projet    
    scope = browse('Catégorie:Portail:'+projet+'/Articles liés')
    print('browsed')
    while scope[0] < start:
        scope = scope[1:]
    count = 0
    print(scope[0])
    while count != end:
        for k in scope: #Traitement des articles présents dans le scope 
            page = inport('Discussion:' + k)
            if page == -1:
                page = ''
            test = fetch(page, '{{Wikiprojet')
            if test == -1:
                test = fetch(page, '{{wikiprojet')
            if test == -1:
                prep = "{{Wikiprojet|"+projet+"|?|avancement=?}}\n\n"
                page = prep + page
                print(k + ':Created')
                edit('Discussion:'+k, page, summary='Apposition du modèle Wikiprojet|'+projet)
                count += 1
            else:
                pageA = page[:test+13]
                pageB = page[test:fetch(page, 'avancement')]
                pageB = pageB.split('|') #Séparation des paramètres du modèle
                for j in range(len(pageB)):
                    pageB[j] = pageB[j].lower().strip()
                if alias.lower() not in pageB and projet.lower() not in pageB:
                    pageC = page[test+13:]
                    if pageA[-1] == '|':
                        supp = projet + '|?|\n'
                    else:
                        supp = '|' + projet + '|?\n'
                    page = pageA + supp + pageC
                    print(k + ':Editing')
                    edit('Discussion:'+k, page, summary='Apposition du modèle Wikiprojet|'+projet)
                    count += 1
                else:
                    print(k + ':Done')

def desEval(projet, alias=''):
    scope = browse(f'Catégorie:Portail:{projet}/Articles liés')
    print('browsed')
    for k in scope: #Traitement des articles présents dans le scope 
        page = inport(f'Discussion:{k}')
        if page == -1:
            page = ''
        test = fetch(page, '{{Wikiprojet')
        if test == -1:
            test = fetch(page, '{{wikiprojet')
        if test != -1:
            pageA = page[:test+13]
            pageB = page[test+13:fetch(page, 'avancement')]
            pageB = pageB.split('|') #Séparation des paramètres du modèle
            pageBis = pageB.copy()
            for j in range(len(pageB)):
                pageBis[j] = pageB[j].lower().strip()
            if projet.lower() in pageBis:
                pageC = page[fetch(page, 'avancement'):]
                ind = pageBis.index(projet.lower())
                if alias.lower() not in pageBis:
                    pageB[ind] = alias
                else:
                    pageB.pop(ind)
                    pageB.pop(ind)
                buff = ''
                for l in pageB:
                    buff += l + '|'
                page = pageA + buff[:-1] + pageC
                print(k+':En cours')
                edit('Discussion:'+k, page, summary = 'Retrait du projet '+projet+' (inexistant)')
                


def depCat(cat):
    scope = browse(cat)
    for k in scope:
        page = inport(k)
        if page == -1:
            page = ""
        test = fetch(page, cat.capitalize())
        if test == -1:
            test = fetch(page, cat.lower())
        if test != -1:
            pageA = page[:test]
            pageB = page[test+len(cat):]
            page = pageA+pageB
            edit(k, page, summary='Retrait de la catégorie '+cat)
            


def countMods(modèle, S, cont='', tinamespace = 0):
    #TODO: débuguer en profondeur
    scope = []
    URL = 'https://fr.wikipedia.org/w/api.php'
    ID = getID(f'Modèle:{modèle}')
    print(ID)
    PARAMS = {'action':'query',
              'format':'json',
              'prop':'transcludedin',
              'pages':f'Modèle:{modèle}',
              'tinamespace':tinamespace,
              'titles':'Modèle:'+modèle.capitalize(),
              
              'tilimit':'500'
              }
    r = S.get(url=URL, params=PARAMS)
    data = r.json()
    ID = str(list(ID)[0])
    print(data)
    for k in data['query']['pages'][ID]['transcludedin']:
        scope.append(k['title'])
    suite = True
    while suite:
        try:
            cont = data['continue']['ticontinue']
            scope += countMods(modèle, S, cont)
            suite = False
        except:
            suite = False
    return scope

def getID(page, S):
    URL = 'https://fr.wikipedia.org/w/api.php'
    PARAMS = {'action':'query',
              'format':'json',
              'prop':'pageprops',
              'titles':page
              }
    r = S.get(url=URL, params=PARAMS)
    data = r.json()
    print(data)
    return data['query']['pages'].keys()

def getHisto(page, S, start=None, stop=None):
    #TODO : reprendre du début 
    url = 'https://fr.wikipedia.org/w/api.php'
    params = {'action':'query',
              'list':'allrevisions',
              'format':'json',
              'titles':page,
              'arvprop':['ids', 'timestamp', 'flags', 'comment', 'user', 'size'],
              'arvlimit':500,
              'arvdir':'newer'
        }
    r = S.get(url=url, params=params)
    data = r.json()
    print(data)
    return dict(data['query']['allrevisions'].values())['revisions']


def browseDeep(cat, level=-1):
    scope = browse(cat)
    underCats = []
    for k in scope:
        if 'Catégorie:' in k:
            underCats.append(k[10:])
    while level != 0:
        underBis = underCats.copy()
        underCats = []
        for cat2 in underBis:
                a = browseDeep(cat2, level=level-1)
                scope += a[0]
                underCats.append(a[1])
    return scope, underCats

def getExtLinks(domain, S, cont='', flg=False):
    url = "https://fr.wikipedia.org/w/api.php?"
    print(domain, cont, f"flag: {flg}")
    params = {"action":"query",
              "list":"exturlusage",
              "euprop":"title",
              "euquery":domain, 
              "eulimit":"max",
              "eucontinue":cont,
              "format":"json"              
        }
    r = S.get(url=url, params=params)
    data = r.json()
    try:
        a = data["continue"]
    except Exception:
        data = pd.DataFrame.from_records(data["query"]["exturlusage"])
        if flg:
            return data
        else:
            return data.title.unique()
    else:
        time.sleep(1)
        data = numpy.concatenate([pd.DataFrame.from_records(data["query"]["exturlusage"]),getExtLinks(domain, S, data["continue"]["eucontinue"], flg=True)])
        return data
    
def paramValChange(page: str, template: str, changes: dict, S:requests.Session=requests.Session()):
    #TODO : coder
    
    """
    page est le nom (préfixé de l'espace de noms) de la page à laquelle accéder
    template est le nom du modèle dont on veut remplacer un paramètre
    S est la session qu'on veut maintenir
    changes est le dictionnaire des changements à effectuer. 
        Chaque clé est un paramètre utilisé par le modèle
        Chaque valeur est un dictionnaire comprenant :
            comme clés les valeurs à remplacer
            comme valeurs leur remplacement
            
    """
    try:
        assert type(changes) == dict
        for k in changes.values():
            assert type(k) == dict
            for val in k.values():
                assert type(val) == str
        
    except AssertionError:
        raise ValueError("changes a un format invalide")
    flg = False
    
    a = inport(page, S)
    groups = re.findall(f"({{{{{template}.+?}}}})", a)
    b = a
    for g in groups:
        try:
            dc = dictifyer(g)
        except Exception:
            continue
        
        for key in dc.keys():
            if key in changes.keys():
                if dc[key] in changes[key].keys():
                    dc[key] = changes[key][dc[key]]
                    new = undictify(template, dc)
                    b = f"{b[:fetch(b, g)]}{new}{b[fetch(b, g)+len(g):]}"
                    flg = True
    return b, flg, page
    
    

def dictifyer(model):
    inner = model[2:-2]
    splittedInnard = inner.split("|")
    dico = {i.split("=")[0]: i.split("=", maxsplit=1)[1] for i in splittedInnard[1:]}
    #print(dico)
    return dico

def undictify(model, dico):
    lst = []
    for k in dico.items():
        lst.append('='.join(k))
    out = '|'.join(lst)
    return f"{{{{{model}|{out}}}}}"
