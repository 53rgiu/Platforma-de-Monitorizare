#maginea de baza Python 3
FROM python:3.11-slim

#setam directorul de lucru in container
WORKDIR /app

#copiem scriptul în container
COPY backup_log.py /app/backup_log.py

#cream directorul de backup (implicit)
ENV BACKUP_DIR=/app/backup
ENV BACKUP_INTERVAL=5

RUN mkdir -p $BACKUP_DIR

#setăm scriptul ca entrypoint
ENTRYPOINT ["python3", "/app/backup_log.py"]