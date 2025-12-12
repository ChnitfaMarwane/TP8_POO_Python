from connection_context import ConnectionManager
from contextlib import ExitStack
from datetime import datetime
import os

LOG_FILE = "log_flan.txt"

if __name__ == '__main__':
    # S'assurer que le fichier log.txt est vide pour un nouveau test
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        
    print("\n--- 1. Test de Succès avec Composition (Parties 2) ---")
    
    try:
        with ExitStack() as stack:
            # 1. Acquisition du fichier de log
            log = stack.enter_context(open(LOG_FILE, "a"))
            # 2. Acquisition de la connexion
            conn = stack.enter_context(ConnectionManager("Serveur Flan"))
            
            # Tâche principale
            current_time = datetime.now().isoformat(timespec='seconds')
            log_message = f"[{current_time}] Tâche effectuée sur {conn.service_name}\n"
            log.write(log_message)
            
            print(f"Log écrit dans {LOG_FILE} et tâche réussie.")
            
        # Les ressources sont libérées ici (Déconnexion et fermeture du fichier)
    except Exception as e:
        print(f"Erreur inattendue dans le test de succès: {e}")

    print("\n--- 2. Test d'Échec avec Composition (Partie 3) ---")
    
    try:
        with ExitStack() as stack:
            # 1. Acquisition du fichier de log
            log = stack.enter_context(open(LOG_FILE, "a"))
            # 2. Acquisition de la connexion
            conn = stack.enter_context(ConnectionManager("Base Fartlan"))
            
            # Tâche principale - Provoque une erreur
            log.write(f"[{datetime.now().isoformat(timespec='seconds')}] Tentative de tâche sur {conn.service_name}\n")
            raise RuntimeError("Erreur de traitement simulée par l'application.")
            
    except RuntimeError as e:
        # L'exception est levée après l'exécution des __exit__ par ExitStack
        print(f"L'exception a été capturée APRÈS le nettoyage : {e.__class__.__name__} - {e}")
    
    # Vérification du log
    print(f"\n--- Vérification du contenu du log ({LOG_FILE}) ---")
    with open(LOG_FILE, "r") as f:
        print(f.read())