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
    
    R = requests.get(url=URL, params=PARAMS)
    DATA = R.json()
    try:
        return DATA["parse"]["wikitext"]["*"]
    except:
        return -1
    
def fetch(page, chaine):
    try:
        return page.index(chaine)
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
    slp = 10
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
        try:
            result = data['edit']['result']
            if result=='Success':
                retry = False
                time.sleep(slp)
            else:
                print('Réessai sur la page' + page)
                time.sleep(wait)
        except:
            print('Erreur')
            time.sleep(wait)

def éval(projet):
    #Remplissage du scope
    scope = browse('Catégorie:Portail:'+projet+'/Articles liés')
    print('browsed')
    for k in scope: #Traitement des articles présents dans le scope 
        page = inport('Discussion:' + k)
        if page == -1:
            page = ''
        test = fetch(page, '{{Wikiprojet')
        if test == -1:
            test = fetch(page, '{{wikiprojet')
            
        if test == -1:
            prep = "{{Wikiprojet|"+projet+"|importance=?|avancement=?}}"
            page = prep + page
            edit('Discussion:'+k, page, summary='Apposition du modèle Wikiprojet|'+projet)
            print(k + ':Done')

        else:
            pageA = page[:test+13]
            pageB = page[test:]
            pageB = pageB[:fetch(pageB, 'avancement')]
            pageB = pageB.split('|') #Séparation des paramètres du modèle
            if projet not in pageB:
                pageC = page[test+13:]
                supp = '|' + projet + '|?'
                page = pageA + supp + pageC
                edit('Discussion:'+k, page, summary='Apposition du modèle Wikiprojet|'+projet)
                print(k + ':Edited')
            else:
                print(k + ':Done')


def depCat(cat):
    scope = browse(cat)
    for k in scope:
        page=inport(k)
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