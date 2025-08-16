#!/usr/bin/env python3
import os
import time
import shutil
from datetime import datetime

# Setări implicite și citirea variabilelor de mediu
SOURCE_FILE = "system-state.log"
BACKUP_DIR = os.environ.get("BACKUP_DIR", "backup")
INTERVAL = int(os.environ.get("BACKUP_INTERVAL", 5))  # în secunde

# Creează directorul de backup dacă nu există
os.makedirs(BACKUP_DIR, exist_ok=True)

# Citire inițială a conținutului (fără backup)
previous_content = None
if os.path.exists(SOURCE_FILE):
    with open(SOURCE_FILE, "r") as f:
        previous_content = f.read()

while True:
    if os.path.exists(SOURCE_FILE):
        # Citește conținutul fișierului
        with open(SOURCE_FILE, "r") as f:
            current_content = f.read()

        # Dacă fișierul s-a modificat față de ultima verificare
        if current_content != previous_content:
            previous_content = current_content
            # Creează numele fișierului de backup cu data și ora
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_file = os.path.join(BACKUP_DIR, f"system-state_{timestamp}.log")
            # Copiază fișierul
            shutil.copy2(SOURCE_FILE, backup_file)
            print(f"Backup creat: {backup_file}")
    else:
        print(f"{SOURCE_FILE} nu există momentan.")

    time.sleep(INTERVAL)
