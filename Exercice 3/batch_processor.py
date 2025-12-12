import csv
from datetime import datetime
from typing import Type, Any
import os

class BatchProcessor:
    def __init__(self, input_csv: str, log_file: str = "journal_flan.log"):
        self.input_csv = input_csv
        self.log_file = log_file
        self.f_csv = None
        self.f_log = None

    def __enter__(self) -> list:
        # Acquisition des ressources
        try:
            # 1. Ouverture du fichier CSV en lecture (r)
            self.f_csv = open(self.input_csv, 'r', newline='')
            csv_reader = csv.reader(self.f_csv)
            self.operations = list(csv_reader)
            
            # 2. Ouverture du fichier LOG en ajout (a)
            self.f_log = open(self.log_file, 'a')
            
            # Journalisation du début de traitement
            self.f_log.write(f"[{datetime.now().isoformat(timespec='seconds')}] DEBUT du traitement du lot '{self.input_csv}'.\n")
            
            return self.operations
        
        except FileNotFoundError:
            if self.f_csv: self.f_csv.close()
            # Journalisation de l'erreur dans la console si le log n'est pas encore ouvert
            print(f"[ERREUR CRITIQUE] Le fichier source '{self.input_csv}' est introuvable.")
            raise # Relance la FileNotFoundError
        
        except Exception as e:
            # Nettoyage en cas d'erreur d'ouverture inattendue
            if self.f_csv: self.f_csv.close()
            if self.f_log: self.f_log.close()
            raise # Relance toute autre exception

    def __exit__(self, exc_type: Type[BaseException] | None, exc_value: Any, traceback: Any) -> bool | None:
        
        # 1. Journalisation de la fin ou de l'erreur dans le log (si le log a été ouvert)
        if self.f_log:
            if exc_type is None:
                self.f_log.write(f"[{datetime.now().isoformat(timespec='seconds')}] FIN du traitement (Succès).\n")
            else:
                self.f_log.write(f"[{datetime.now().isoformat(timespec='seconds')}] FIN du traitement (ÉCHEC : {exc_type.__name__} - {exc_value}).\n")

        # 2. Fermeture garantie des deux fichiers
        if self.f_csv:
            self.f_csv.close()
        if self.f_log:
            self.f_log.close()
            
        # Ne pas masquer l'exception (retourne None/False)
        return None