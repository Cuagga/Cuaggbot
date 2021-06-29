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
    """Permet d'importer une page donéée en paramètre"""
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
    page = inport(page)
    try:
        return page.index(chaine)
    except ValueError:
        return -1

def browse(cat):
    scope = []
    URL = 'https://fr.wikipedia.org/w/api.php'
    PARAMS = {
        'action':'query',
        'prop':'links|categories',
        'list':'categorymembers',
        'format':'json',
        'cmtitle':cat,
        'cmlimit':'5000'
        }
    r = S.post(url=URL, params=PARAMS)
    data = r.json()
    for k in data['query']['categorymembers']:
        scope.append(k['title'])
    return scope


# Bout de code Evaluation
def éval(projet):
    scope = []
    #Je voudrais bien utiliser Portail-éval, le gadget d'Orlodrim, pour remplir le scope
    #Les catégories ne sont pas exhaustives
    for k in scope:
        date = time.asctime()[:10]
        #Manque ici une prise en compte du cas où l'article est évalué par un autre portail
        #Et on pourrait vérifier aussi que l'évaluation manque réellement pour notre projet, au cas où
        prep = "{{évaluation|titre=''"+str(k)+"''|diff=|date=''"+ date +"''|importance=''[[Projet:Évaluation/Importance|à évaluer]]''|avancement=''[[Projet:Évaluation/Avancement|à évaluer]]''}}"
        PARAMS = {
            'action':'edit',
            'title':'Discussion:'+k,
            'section':'0',
            'prepend':prep,
            'format':'json',
            'token':editToken
            }
        r = S.post(url = 'https://fr.wikipedia.org/w/api.php', params = PARAMS)

#Requête de test
éval("Abbeville")













