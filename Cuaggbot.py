import requests


#Connexion au compte du bot
S = requests.Session()

URL = "https://fr.wikipedia.org/w/api.php"
"""
# Retrieve login token first
PARAMS_0 = {
    'action':"query",
    'meta':"tokens",
    'type':"login|csrf",
    'format':"json"
}

R = S.get(url=URL, params=PARAMS_0)
DATA = R.json()
loginToken = DATA['query']['tokens']['logintoken']

print(loginToken)

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
print(editToken)"""

def inport(page):
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
    
def fetch(page, chaine, typ):
    page = inport(page)
    if typ == 'lien':
        




















