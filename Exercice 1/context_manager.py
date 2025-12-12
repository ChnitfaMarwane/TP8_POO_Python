from pathlib import Path
from contextlib import contextmanager, ExitStack
from typing import List

class TempFileWriter:
    def __init__(self, nom_fichier="temp_flan.txt"):
        self.filepath = Path(nom_fichier)
        self.f = None

    def __enter__(self):
        self.f = self.filepath.open("w")
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.f:
            self.f.close()
        
        self.filepath.unlink(missing_ok=True)

@contextmanager
def temp_file_manager(nom_fichier="temp_fartlan.txt"):
    path = Path(nom_fichier)
    f = path.open("w")
    try:
        yield f 
    finally:
        f.close()
        path.unlink(missing_ok=True)


def gerer_multiples_fichiers(paths: List[str]):
    with ExitStack() as stack:
        files = [stack.enter_context(open(p, "w")) for p in paths]
        for f in files:
            f.write("Test de sortie ExitStack.\n")