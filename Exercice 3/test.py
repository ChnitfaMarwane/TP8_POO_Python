from batch_processor import BatchProcessor
import os
import csv
from typing import List

CSV_FILE = "operations_flan.csv"
LOG_FILE = "journal_flan.log"

def creer_csv(data: List[List[str]]):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def simuler_traitement(operations: list, provoquer_erreur: bool = False):
    print(f"\n--- Démarrage du Traitement sur {len(operations)} Lignes ---")
    for i, row in enumerate(operations):
        print(f"Traitement Ligne {i+1}: {row}")
        # Simuler une erreur lors de la 4ème ligne
        if provoquer_erreur and i == 3:
            raise RuntimeError(f"Erreur de données à la ligne {i+1}")
    print("Traitement terminé.")

if __name__ == '__main__':
    # Préparation du CSV
    operations_data = [
        ["Op1", "flan", "100"],
        ["Op2", "fartlan", "200"],
        ["Op3", "blanlan", "300"],
        ["Op4", "error_trigger", "400"],
        ["Op5", "never_reached", "500"]
    ]
    creer_csv(operations_data)

    # Nettoyage initial du log
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # --- 1. Test de Succès ---
    print("\n[SCÉNARIO 1] Traitement réussi.")
    try:
        with BatchProcessor(CSV_FILE, LOG_FILE) as ops:
            simuler_traitement(ops, provoquer_erreur=False)
    except Exception as e:
        print(f"Erreur inattendue dans le scénario de succès : {e}")

    # --- 2. Test d'Échec ---
    print("\n[SCÉNARIO 2] Traitement échoué (RuntimeError).")
    try:
        with BatchProcessor(CSV_FILE, LOG_FILE) as ops:
            simuler_traitement(ops, provoquer_erreur=True)
    except RuntimeError as e:
        print(f"Erreur capturée : {e}")

    # --- 3. Test de Fichier Introuvable ---
    print("\n[SCÉNARIO 3] Fichier introuvable.")
    try:
        with BatchProcessor("fichier_absent_flan.csv", LOG_FILE) as ops:
            pass
    except FileNotFoundError as e:
        print(f"Erreur capturée : {e.__class__.__name__}")
        
    # --- 4. Vérification Finale du Log ---
    print(f"\n[VÉRIFICATION] Contenu de {LOG_FILE} :")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            print(f.read())
    else:
        print("Le fichier log n'existe pas.")