# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 16:03:31 2021

@author: Cuagga
"""
import requests
import time

soft_headers = {"User-Agent" : "CuaggBot (https://fr.wikipedia.org/wiki/Utilisateur:Cuaggbot)"}
botUN ='Cuaggbot'
botPW = '6iJCA3KJe8NykeH'

url = 'https://fr.wikipedia.org/w/api.php'

S = requests.Session()

def login():
    #get login token
    params_0 = {
    		"action":"query",
    		"meta":"tokens",
    		"type":"login",
    		"format":"json"
    		}
    current_request = S.get(url = url, params = params_0, headers = soft_headers)
    current_data = current_request.json()
    login_token = current_data["query"]["tokens"]["logintoken"]
    
    #try to login
    params_1 = {
    "action":"login",
    "lgname": botUN,
    "lgpassword": botPW,
    "lgtoken": login_token,
    "format":"json"
    		}
    		
    current_request = S.post(url, data = params_1, headers=soft_headers)
    current_data = current_request.json()
    login_result = current_data["login"]["result"]
    if login_result == "Success":
        print('Connecté')
        return True
    else:
        return False


def getEditToken(page):
    params_0 = {
		"action":"query",
		"meta":"tokens|userinfo",
		"type":"csrf",
		"format":"json",
		"curtimestamp":"1",
		"prop":"revisions",
		"rvprop":"timestamp",
		"rvslots":"*",
		"uiprop":"hasmsg",
		"titles": page,
		"indexpageids":"1"
		}
    current_request = S.get(url=url, params= params_0, headers=soft_headers)
    current_data = current_request.json()
    edit_token = current_data["query"]["tokens"]["csrftoken"]
    page_id = current_data["query"]["pageids"][0] #retrieve the page_title id, needed for the next line.
    try:
        last_revision_time = current_data["query"]["pages"][page_id]["revisions"][0]["timestamp"]
    except :
        last_revision_time = None
    current_time = current_data["curtimestamp"]
    return edit_token, last_revision_time, current_time

def inport(page):
    URL = "https://fr.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "parse",
        "page": page,
        "prop":"wikitext",
        "format": "json"
    }
    réussite = False
    while réussite == False:
        try:
            R = requests.post(url=URL, params=PARAMS)
            DATA = R.json()
            réussite = True
            time.sleep(.5)
        except:
            print('Réessai')
            time.sleep(10)
            continue
    try:
        return DATA['parse']['wikitext']['*']
    except:
        return -1
    
def fetch(page, chaine, start=0):
    try:
        return page.index(chaine, start)
    except ValueError:
        return -1

def browse(cat, cmcont=''):
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
    r = requests.post(url=URL, params=PARAMS)
    data = r.json()
    for k in data['query']['categorymembers']:
        scope.append(k['title'])
    suite = True
    while suite:
        try:
            cont = data['continue']['cmcontinue']
            PARAMS.__setitem__('plcontinue', cont)
            scope += browse(cat, cont)
            suite = False
        except:
            suite = False
    return scope

def edit(page, text, summary = '', minor=1, isBot=1):
    wait = 5
    slp = 6
    retry = True
    while retry == True:
        tupel = getEditToken(page)
        try:
            editToken, lastRevTime, curTimeStamp = tupel
        except:
            continue
        params0 = {
			"action":"edit",
			"format":"json",
			"title": page,
			"text": text,
			"summary": summary,
			"minor": minor,
			"bot": isBot,
			"token": editToken,
			"basetimestamp": lastRevTime,
			"starttimestamp": curTimeStamp,
			"assert":"user",
			"maxlag": 5
			}
        req = S.post(url, data=params0)
        data = req.json()
        print(data)
        try:
            time.sleep(5)
            result = data['edit']['result']
            if result=='Success':
                retry = False
                time.sleep(slp)
            else:
                print('Réessai sur la page' + page)
                time.sleep(wait)
        except:
            print('Erreur')
            if data['error']['code'] == 'assertuserfailed':
                login()
            else:
                print('Non fait')
                return
            time.sleep(1)

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
    scope = browse('Catégorie:Portail:'+projet+'/Articles liés')
    print('browsed')
    for k in scope: #Traitement des articles présents dans le scope 
        page = inport('Discussion:' + k)
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

def countMods(modèle, cont='', tinamespace = 0):
    scope = []
    URL = 'https://fr.wikipedia.org/w/api.php'
    ID = getID('Modèle:'+modèle)
    PARAMS = {'action':'query',
              'format':'json',
              'prop':'transcludedin',
              'tinamespace':tinamespace,
              'titles':'Modèle:'+modèle.capitalize(),
              'ticontinue':cont,
              'tilimit':'500'
              }
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    ID = str(list(ID)[0])
    for k in data['query']['pages'][ID]['transcludedin']:
        scope.append(k['title'])
    suite = True
    while suite:
        try:
            cont = data['continue']['ticontinue']
            scope += countMods(modèle, cont)
            suite = False
        except:
            suite = False
    return scope

def getID(page):
    URL = 'https://fr.wikipedia.org/w/api.php'
    PARAMS = {'action':'query',
              'format':'json',
              'prop':'pageprops',
              'titles':page.capitalize()
              }
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    return data['query']['pages'].keys()

def getHisto(page, start=None, stop=None):
    url = 'https://fr.wikipedia.org/w/api.php'
    params = {'action':'query',
              'format':'json',
              'titles':page,
              'rvprop':['ids', 'timestamp', 'flags', 'comment', 'user', 'size'],
              'rvlimit':500,
              'rvdir':'newer'
        }
    r = requests.get(url, params)
    data = r.json()
    return dict(data['query']['pages'].values())['revisions']


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

















