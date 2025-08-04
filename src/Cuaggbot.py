from cuaggMods import *
from loginCuagg import *
import threading

soft_headers = {"User-Agent" : "CuaggBot (https://fr.wikipedia.org/wiki/Utilisateur:Cuaggbot)"}
botUN ='Cuaggbot'

S = requests.Session()

if __name__== "__main__":
    login(S)
    print("logged in")
    a = getExtLinks("nawaat.org", S)
    for page in a:
        p = inport(page, S)
        print(page)
        if ":" in page:
            continue
        else:
            outText = paramValChange(page, 
                                     "Lien web", 
                                     S,
                                     "site", 
                                     "nawaat.org", 
                                     "[[Nawaat]]")
            if outText != p:
                edit(page, outText, S, summary='Insertion IW Nawaat dans Lien web')
            else:continue
            
            
