#!/bin/bash

#variabila de mediu cu valoarea de 5 secunde
PERIOD="${PERIOD:-5}"
# directorul unde se scriu logurile (volum montat din host)
LOG_DIR="/app/logs"
#fisierul in care se salveaza logurile, acesta este creat in directorul curent
LOG_FILE="$LOG_DIR/system-state.log"

while true; do
    # afiseaza data in partea superiora a fisierului.
    echo "===== $(date) =====" > "$LOG_FILE"
    # comanda "top -bn1" scoate informatiile o singura data si le trimite ca un fisier simpul text catre "awk" pentru a selecta
    # doar informatia despre cpu si din acea informatie afiseaza suma valorilor liniilor 2 si 4 si adauga rezultatul la finalul fisierului
    echo "CPU: $(top -bn1 | awk '/Cpu/ {print $2 + $4"%"}')" >> "$LOG_FILE"
    #free -h afiseaza memoria disponibila, folosita in format human-readable (GiB, MiB).
    #awk 'NR<=2' pastreaza doar primele doua linii (linia de antet si linia Mem:).
    free -h | awk 'NR<=2' >> "$LOG_FILE"
    
    echo "Procese active: $(ps -e --no-headers | wc -l)" >> "$LOG_FILE"
    
    df -h | awk '$1 == "/dev/sda3" {print "Disk:           size " $2 ", used " $3 ", available " $4 ", used " $5 ", mounted on " $6 ""}' >> "$LOG_FILE"
    
    sleep "$PERIOD"
done
