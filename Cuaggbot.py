import requests, time


#Connexion au compte du bot
S = requests.Session()


URL = "https://fr.wikipedia.org/w/api.php"

# Login token 
PARAMS_0 = {
    'action':"query",
    'meta':"tokens",
    'type':"login|csrf",
    'format':"json"
}

R = S.get(url=URL, params=PARAMS_0)
DATA = R.json()
loginToken = DATA['query']['tokens']['logintoken']



PARAMS_1 = {
    'action':"login",
    'lgname':"Cuaggbot",
    'lgpassword':"X9LnvynUASfFDCR",
    'lgtoken':loginToken,
    'format':"json"
}

R = S.post(URL, data=PARAMS_1)

PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_2)
DATA = R.json()

editToken = DATA['query']['tokens']['csrftoken']


def inport(page):
    """Permet d'importer une page donnée en paramètre"""
    URL = "https://fr.wikipedia.org/w/api.php"
    
    PARAMS = {
        "action": "parse",
        "page": page,
        "prop":"wikitext",
        "format": "json"
    }
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    
    return DATA["parse"]["wikitext"]["*"]
    
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
    r = S.post(url=URL, params=PARAMS)
    data = r.json()
    for k in data['query']['categorymembers']:
        scope.append(k['title'])
    suite = True
    while suite:
        try:
            cont = data['continue']['cmcontinue']
            print(data['continue']['cmcontinue'])
            PARAMS.__setitem__('plcontinue', cont)
            scope += browse(cat, cont)
            suite = False
        except:
            suite = False
    return scope


# Bout de code Evaluation
def éval(projet):
    scope = []
    #Remplissage du scope
    portail = browse('Catégorie:Portail:'+projet+'/Articles liés')
    for k in scope: #Traitement des articles présents dans le scope 
        time.sleep(20)
        page = inport('Discussion:' + k)
        test = fetch(page, '{{Wikiprojet')
        if test==-1:
            prep = "{{Wikiprojet|"+projet+"|importance=?|avancement=?}}"
            PARAMS = {
                'action':'edit',
                'title':'Discussion:'+k,
                'section':'0',
                'prepend':prep,
                'format':'json',
                'token':editToken
                }
            r = S.post(url = 'https://fr.wikipedia.org/w/api.php', params = PARAMS)
        else:
            pageA = page[:test+13]
            pageB = page[test:]
            pageB = pageB[:fetch(pageB, 'avancement')]
            pageB.split('|') #Séparation des paramètres du modèle
            projets = []
            for j in range(len(pageB//2)):
                projets.append(pageB[2*j+1]) #Récupération des projets évalués
            if projet not in projets:
                pageC = page[test+13:]
                supp = projet + '|?'
                page = pageA + supp + pageC
                PARAMS = {
                    'action':'edit',
                    'title':'Discussion:'+k,
                    'bot':'true',
                    'token':editToken,
                    'text':page,
                    'summary':'Apposition du modèle Wikiprojet pour le projet '+ projet
                    }
                r = S.post(url='https://fr.wikipedia.fr/w/api.php', params=PARAMS)

#Requête de test














