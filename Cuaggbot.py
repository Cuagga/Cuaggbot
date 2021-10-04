import requests, time
from cuaggMods import *

soft_headers = {"User-Agent" : "CuaggBot (https://fr.wikipedia.org/wiki/Utilisateur:Cuaggbot)"}
botUN ='Cuaggbot'
botPW = 'X9LnvynUASfFDCR'

url = 'https://fr.wikipedia.org/w/api.php'

S = requests.Session()

a = countMods('Age en jours')
npar = []

for k in a[1:]:
    page = inport(a)
    start = fetch(page,'{{Age en jours|')
    end = fetch(page[start+15], '}}')
    print(page[start:end])
    mod = page[start:end].split('|')
    npar.append(len(mod))

print(npar)
