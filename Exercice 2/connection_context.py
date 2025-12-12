from datetime import datetime
from contextlib import ExitStack
import os
from typing import Type, Any

class ConnectionManager:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.log_prefix = f"[{datetime.now().isoformat(timespec='seconds')}]"

    def __enter__(self) -> 'ConnectionManager':
        print(f"{self.log_prefix} Connexion à {self.service_name} établie.")
        return self

    def __exit__(self, exc_type: Type[BaseException] | None, exc_value: Any, traceback: Any) -> bool | None:
        self.log_prefix = f"[{datetime.now().isoformat(timespec='seconds')}]"
        print(f"{self.log_prefix} Déconnexion de {self.service_name}.")
        
        if exc_type:
            print(f"Erreur détectée et gérée lors de la déconnexion : {exc_type.__name__} — {exc_value}")
        
        return None