FROM ubuntu:22.04

#setam directorul de lucru
WORKDIR /app

#copiem scriptul în container
COPY monitorizare.sh /app/monitorizare.sh

#facem scriptul executabil
RUN chmod +x /app/monitorizare.sh

#setam variabila de mediu pentru perioada (default 5s)
ENV PERIOD=5

#rulam scriptul
CMD ["/app/monitorizare.sh"]