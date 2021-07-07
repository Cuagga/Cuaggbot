import requests, time
from cuaggMods import *

soft_headers = {"User-Agent" : "CuaggBot (https://fr.wikipedia.org/wiki/Utilisateur:Cuaggbot)"}
botUN ='Cuaggbot'
botPW = 'X9LnvynUASfFDCR'

url = 'https://fr.wikipedia.org/w/api.php'

S = requests.Session()


login()
éval('Armes')