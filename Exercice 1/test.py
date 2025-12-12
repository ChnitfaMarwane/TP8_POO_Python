from context_manager import TempFileWriter, temp_file_manager, gerer_multiples_fichiers
from pathlib import Path
from typing import List

def verifier_existence(paths: List[str]):
    exist_status = {p: Path(p).exists() for p in paths}
    print(f"Statut des fichiers : {exist_status}")

if __name__ == '__main__':
    
    file1 = "temp_flan.txt"
    paths1 = [file1]
    
    verifier_existence(paths1)
    with TempFileWriter(file1) as f:
        f.write("Contenu temporaire avec __enter__/__exit__.\n")
        verifier_existence(paths1)
    verifier_existence(paths1)
    
    file2 = "temp_fartlan.txt"
    paths2 = [file2]
    
    verifier_existence(paths2)
    with temp_file_manager(file2) as f:
        f.write("Contenu temporaire avec @contextmanager.\n")
        verifier_existence(paths2)
    verifier_existence(paths2)

    paths3 = ["a.txt", "b.txt", "c.txt"]
    
    verifier_existence(paths3)
    gerer_multiples_fichiers(paths3)
    verifier_existence(paths3)