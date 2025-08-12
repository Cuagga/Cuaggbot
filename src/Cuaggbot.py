import numpy as np
import cuaggMods
import threading
import time
import sys
import queue
from loginCuagg import *


soft_headers = {"User-Agent" : "CuaggBot (https://fr.wikipedia.org/wiki/Utilisateur:Cuaggbot)"}
botUN ='Cuaggbot'

S = requests.Session()


if __name__== "__main__":
    
    login(S) #défini dans loginCuagg
    print("logged in")
    lt1 = cuaggMods.getExtLinks("rfi.fr", S)
    lt2 = cuaggMods.getExtLinks("kapitalis.com", S)
    lt3 = cuaggMods.getExtLinks("mosaiquefm.net", S)
    lt4 = cuaggMods.getExtLinks("shemsfm.net", S)
    lt5 = cuaggMods.getExtLinks("leaders.com.tn", S)
    a = set(np.concatenate([lt1, lt2, lt3, lt4], axis=None)) #Réunion, aplatissement
                                                               #et retrait des pages en double 
    """
    editcount = 0
    for page in a:
        if not isinstance(page, str):
            continue
        if ":" in page:
            continue
        else:
            
            outText, flag = cuaggMods.paramValChange(page, 
                           "Lien web", 
                           {"site": 
                            {"rfi.fr":"[[Radio France internationale|RFI]]", 
                             "kapitalis.com":"[[Kapitalis]]", 
                             "mosaiquefm.net" : "[[Mosaïque FM (Tunisie)|Mosaïque FM]]"}
                            }, S = S)
                
            if flag:
                print(f"Editing {page}")
                cuaggMods.edit(page, outText, S, summary='Insertion IW Leaders, HuffPost Maghreb et Tuniscope dans Lien web')
                editcount += 1
            else:continue"""

    qPage = queue.Queue()
    qClock = queue.Queue()
    
    # Thread 1 : producer
    def createWikicode(pages, q=queue.Queue()):
        for page in pages:
            if not isinstance(page, str):
                continue
            if ":" in page:
                continue
            out = cuaggMods.paramValChange(page, 
                       "Lien web", 
                       {"site": 
                        {"rfi.fr":"[[Radio France internationale|RFI]]", 
                         "kapitalis.com":"[[Kapitalis]]", 
                         "mosaiquefm.net" : "[[Mosaïque FM (Tunisie)|Mosaïque FM]]",
                         "shemsfm.net" : "[[Shems FM]]",
                         "[[Leaders (Tunisie)]]" : "[[Leaders (Tunisie)|Leaders]]"
                         }
                        }, S = S)
            if out[1]:
                q.put(out)
                print(f"{out[2]} traité")
            time.sleep(1)
    
    def clock(qIn, qOut):
        while True:
            try:
                a = qIn.get_nowait()
                print(a[2])
                qIn.task_done()
                qOut.put(a)
                print("put in clock-output")
                time.sleep(10)
            except queue.Empty:
                print("Queue In vide")
                time.sleep(10)
        
        
    def edit(q):
        "Utilise la qOut de clock en tant que queue d'entrée"
        while True:
            item = q.get()
            if item[1]:
                print(f"Editing {item[2]}")
                cuaggMods.edit(item[2], item[0], S, summary="Insertion LI dans le champ 'site' de Lien web (Kapitalis, RFI, Mosaïque FM, Shems FM)")
            q.task_done()
            
    
    threadWork = threading.Thread(target=createWikicode, args=(a, qPage), daemon=True)
    threadClock = threading.Thread(target=clock, args=(qPage, qClock))
    threadEdit = threading.Thread(target=edit, args=(qClock, ), daemon=True)
    
    threadWork.start()
    threadClock.start()
    threadEdit.start()
    while True:
        pass
    