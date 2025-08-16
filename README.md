							

							                    Proiect DevOps

							                                                            Sergiu Gabriel Paulescu

    ## Scopul Proiectului


		Proiectul presupune dezvoltarea unei platforme DevOps pentru monitorizarea stării unui sistem informatic folosind bash, Python, Docker, Ansible, Jenkins, AWS si Terraform. Utilizatorii vor putea observa evolutia utilizarii următoarelor resurse: cpu, memorie, număr de procese active și utilizare disk. Platforma trebuie să pastreze istoricul stării sistemelor pentru a le permite administratorilor de sistem să ia decizii legate de scalare

	## Ghid complet pentru pregatirea proiectului


    	1. Actualizare sistem

    	Primul pas este sa te asiguri ca sistemul este actualizat

    		```bash
    		sudo apt update
			sudo apt upgrade -y
			```

    	2. Instalare Python si pip

		scripturile Python necesita Python 3 si pip

			```bash
			sudo apt install -y python3 python3-pip
			```
		Verificam instalarea:
			```bash
    		python3 --version
			pip3 --version
			```


		3. Instalare Git

    	Git este necesar pentru gestionarea codului sursa si urcarea pe GitHub

    		```bash
			sudo apt install -y git
			```


		Configuram identitatea
			```bash
			git config --global user.name "Numele Tau"
			git config --global user.email "email@exemplu.com"
			git --version
			```

		Acum putem clona, commit-ui si impinge proiecte pe GitHub.

		4. Instalare Docker

		Docker iti permite sa rulezi scripturile intr-un mediu izolat (containere), ceea ce este recomandat pentru monitorizare si backup:
			```bash
			sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
			curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
			echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
			sudo apt update
			sudo apt install -y docker-ce docker-ce-cli containerd.io
			```
		Verificare Docker:
			```bash
			docker --version
			sudo systemctl status docker
			```


		Pentru a rula Docker fara sudo
			```bash
			sudo usermod -aG docker $USER
			```
    		reautentifica-te pentru ca schimbarea sa aiba efect.

		5. Instalare Docker Compose

		Docker Compose gestioneaza mai multe containere simultan, util pentru proiecte cu monitorizare + backup.
			```bash
			sudo apt install -y docker-compose
			docker-compose --version
			```

		6. Instalarea Ansible pe Ubuntu

     	Instalare din repository-ul oficial Ubuntu
     		```bash
			sudo apt update
			sudo apt install ansible -y
			```

		Verificam versiunea instalata:
			```bash
			ansible --version
			```


    ## Script bash monitorizare.sh 

	PERIOD="${PERIOD:-5}"
		PERIOD este intervalul de timp intre fiecare rulare a scriptului (in secunde).
		sintaxa este ${VAR:-VAL} inseamna: „daca variabila VAR nu exista sau e goala se foloseste VAL”.
		Asadar, daca nu setezi PERIOD in mediul de executie, scriptul foloseste 5 secunde.

	LOG_FILE="system-state.log"
		Aceasta este numele fisierului în care se vor scrie log-urile si care va fi creat in fisierul curent

	Bucla While
		while true; do 
	    ...
		sleep "$PERIOD"
	done

	while true rulează codul din interior la nesfarsit. La finalul buclei, sleep "$PERIOD" face scriptul sa astepte 5 secunde (in cazul nostru) inainte de urmatoarea executie.

	Afisare Data is Ora
		echo "=== $(date) ===" > "$LOG_FILE"
		$(date) executa comanda date si pune rezultatul in fisier, in cazul nostru este in prima linie ca este prima comanda. 
		(>) suprascrie fisierul system-state.log la fiecare rulare a buclei.

	echo "CPU: $(top -bn1 | awk '/Cpu/ {print $2 + $4"%"}')" >> "$LOG_FILE"
		*"top" este un monitor interactiv de procese si resurse, cand rulezi doar top, deschide o interfata live in terminal si actualizeaza continuu informatiile
		*"-b" înseamnă batch mode, adica "top" trimite iesirea ca text simplu pentru a putea fi prelucrata de "awk"
		*"-n<num>" spune de cate ori sa colecteze date "top", in cazul nostru o singura data adica "-n1"
		*"awk" este un interpreter pentru procesarea liniilor de text, vede linia impartita automat in campuri separate de spatii
		apoi selecteaza toata coloana cu CPU si ne afiseaza suma proceselor selectate. $1 reprezinta prima linie din tabel care contine denumirea (cpu)
		*">>" adaugă rezultatul la finalul fișierului, fără a-l suprascrie

	free -h | awk 'NR<=2' >> "$LOG_FILE"
		free -h afiseaza memoria disponibila, folosita in format human-readable (GiB, MiB).
		awk 'NR<=2' pastreaza doar primele doua linii (linia de antet si linia Mem:).

	echo "Procese active: $(ps -e --no-headers | wc -l)" >> "$LOG_FILE"
		"ps -e" listeaza toate procesele active.
		"--no-headers" elimina linia de antet.
		"wc -l" numara cate linii sunt, adica numarul total de procese.

	df -h | awk '$1 == "/dev/sda3" {print "Disk: size " $2 ", used " $3 ", available " $4 ", used " $5 ", mounted on " $6 ""}' >> "$LOG_FILE"
		"df -h" afișează spațiul disk-ului în format ușor de citit.
    	"awk" '$1 == "/dev/sda3" { print .. }' filtrează doar linia unde primul câmp este /dev/sda3
    	"$2" = dimensiunea totala a partitiei
    	"$3" = spatiul folosit
    	"$4" = spatiul liber
    	"$5" = procentul folosit
    	"$6" = montat in 

	sleep "$PERIOD"
		Pune scriptul sa astepte PERIOD secunde inainte de urmatorul ciclu al buclei.

	## Script python backup_log.py
		Acest script Python este conceput pentru a monitoriza un fisier de log si a crea copii de siguranta doar atunci cand continutul sau se schimba, pentru a pastra un istoric al modificarilor si a evita pierderea datelor.

		import os
		import time
		import shutil
		from datetime import datetime
   		Se importa bibliotecile necesare:
			os pentru operatii cu fisiere si directoare,
			time pentru delay intre verificari,
			shutil pentru copierea fisierelor pastrand metadatele,
			datetime pentru generarea timestamp-urilor unice pentru fisierele de backup.

		FISIER_SURSA = "logs/system-state.log"
		BACKUP_DIR = os.environ.get("BACKUP_DIR", "backup")
		FISIER_TIMP = "ultimul_timp.txt"
		INTERVAL = int(os.environ.get("BACKUP_INTERVAL", 5))


		FISIER_SURSA este calea fisierului pe care il monitorizam.
		BACKUP_DIR este directorul unde se vor salva backup-urile; poate fi setat prin variabila de mediu BACKUP_DIR, altfel se foloseste backup.
		FISIER_TIMP retine ultima valoare citita din fisierul sursa, pentru a verifica daca s-a schimbat.
		INTERVAL stabileste perioada de asteptare intre verificari, setabila prin BACKUP_INTERVAL, cu valoare implicita 5 secunde.
		os.makedirs(BACKUP_DIR, exist_ok=True)

		Creaza directorul de backup daca acesta nu exista, evitand erorile la salvarea fisierelor.

		if os.path.exists(FISIER_TIMP):
    	with open(FISIER_TIMP, "r") as f:
        ultimul_timp = f.read().strip()
		else:
    	ultimul_timp = None

    	Se verifica daca fisierul ultimul_timp.txt exista:
		Daca exista, se citeste ultima valoare salvata, eliminand spatiile albe.
		Daca nu exista, ultimul_timp este initializat cu None, ceea ce va determina ca prima modificare sa genereze un backup.

		while True:
		Incepe un loop infinit care va rula continuu.
	    	if os.path.exists(FISIER_SURSA):
        		with open(FISIER_SURSA, "r") as f:
            	prima_line = f.readline().strip()

		Se verifica daca fisierul sursa exista.
		Se deschide fisierul si se citeste prima linie, care este apoi curatata de spatii albe.

        if ultimul_timp != prima_line:
            ultimul_timp = prima_line
            with open(FISIER_TIMP, "w") as f:
                f.write(ultimul_timp)
		Daca linia citita difera de ultima valoare salvata, se actualizeaza fisierul ultimul_timp.txt cu noua valoare.
		Astfel scriptul stie pentru urmatoarea iteratie daca fisierul a fost modificat.


            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"system-state_{timestamp}.log")
            shutil.copy2(FISIER_SURSA, backup_file)
            print(f"Backup creat: {backup_file}")
		Se genereaza un timestamp unic pentru a denumi fisierul de backup.
		Se construieste calea completa pentru backup.
		Se copiaza fisierul sursa in backup pastrand datele originale.
		Se afiseaza un mesaj pentru confirmarea crearii backup-ului.
    		else:
        		print(f"{FISIER_SURSA} nu exista momentan.")
		Daca fisierul sursa nu exista, se afiseaza un mesaj informativ si scriptul asteapta urmatorul interval.

    	time.sleep(INTERVAL)
		Se asteapta perioada specificata in INTERVAL inainte de a repeta verificarea.

	## Docker

	In folderul principal al proiectului cream un folder numit docker cu comanda "mkdir" si in interiorul acestuia mai cream un folder numit monitoring. 
	In folderul monitoring cream un Dockerfile si copiem scriptul monitorizare.sh cu "cp sursa destinatie"
	In folderul docker cream un folder numit backup unde se va face backup-ul
	In folderul docker cream un folder numit shared-logs unde va fi pus fisierul system-state.log si tot de aici va fi citit de pentru a face backup.

	```
	docker - backup      - dockerfile
	       - monitoring  - dockerfile
	       - shared-logs - system-state.log
	```       

    ## containerul de monitoriare
	docker build -t monitor_sistem .
	docker run --name monitor_container --rm   -e PERIOD=5   -v /home/sergiu/git-projects/Platforma-de-Monitorizare/docker/shared-logs:/app/logs   -d monitor_sistem

	## containerul de backup
	docker build -t backup_sistem .
	docker run --name backup_container --rm -d \
  -e BACKUP_INTERVAL=5 \
  -v /home/sergiu/git-projects/Platforma-de-Monitorizare/docker/shared-logs:/app/logs \
  -v /home/sergiu/git-projects/Platforma-de-Monitorizare/docker/backup/docker-backup:/app/backup \
  backup_sistem
 	## docker-compose
 	comenzi de instalare docker compose pe masina

 	sudo apt update
    sudo apt install docker-compose

    pornire 
    docker-compose up -d

    oprire 
    docker-compose down

    vezi loguri in timp real
    docker-compose logs -f


    
