#!/usr/bin/env python3

import os#                      -pentru operațiuni legate de fișiere și directoare.
import time#                    -pentru funcții legate de timp    
import shutil#                  -pentru operațiuni de copiere a fișierelor.
from datetime import datetime#  -pentru a obține data și ora curentă, folosită la timestamp.

FISIER_SURSA = "logs/system-state.log"#               -variabila cu calea fisierului de log care trebuie monitorizat pentru backup
BACKUP_DIR = os.environ.get("BACKUP_DIR", "backup")#  -obtine din mediul de executie directorul unde se fac backup-urile.
FISIER_TIMP = "ultimul_timp.txt"  #                   -unde stocam ultima linie citita din log, pentru ca scriptul sa stie sa faca log
INTERVAL = int(os.environ.get("BACKUP_INTERVAL", 5))# -Intervalul de timp (in secunde) intre verificările fisierului sursa

os.makedirs(BACKUP_DIR, exist_ok=True)#      creeaza directorul pentru backup daca nu exista deja si nu da eroare daca directorul exista

if os.path.exists(FISIER_TIMP):#             citim ultima valoare salvată, dacă exista
    with open(FISIER_TIMP, "r") as f:#       daca exista, citeste valoarea si o pune în ultimul_timp
        ultimul_timp = f.read().strip()
else:
    ultimul_timp = None#     Daca nu exista, ultimul_timp este None

while True:
    if os.path.exists(FISIER_SURSA):#           verifica daca fisierul de log exista.
        with open(FISIER_SURSA, "r") as f:
            prima_line = f.readline().strip()#  daca exista, citeste prima linie (cea mai recentă stare) si elimina spatiile albe cu strip() 

        if ultimul_timp != prima_line:#          compara linia curenta cu ultima valoare salvata.
            ultimul_timp = prima_line#           actualizăm fișierul cu ultima valoare
            with open(FISIER_TIMP, "w") as f:#   daca e diferita, actualizeaza ultimul_timp si il scrie in ultimul_timp.txt
                f.write(ultimul_timp)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")#                     creeaza un timestamp de forma YYYYMMDDHHMMSS
            backup_file = os.path.join(BACKUP_DIR, f"system-state_{timestamp}.log")# construieste calea completa a fisierului de backup
            shutil.copy2(FISIER_SURSA, backup_file)#                                 copiaza fisierul sursa in folderul de backup, pastrand  (shutil.copy2)
            print(f"Backup creat: {backup_file}")#                                   afiseaza mesaj ca backup-ul a fost creat.
    else:
        print(f"{FISIER_SURSA} nu există momentan.")# daca fisierul sursa nu exista, afiseaza un mesaj de avertizare.

    time.sleep(INTERVAL)#      asteapta  INTERVAL secunde inainte de urmatoarea verificare.
