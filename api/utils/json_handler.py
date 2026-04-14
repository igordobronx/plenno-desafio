#criando o json para os alertas
import json
from pathlib import Path
from typing import List, Dict
from datetime import date, datetime

JSON_PATH = Path(__file__).parent.parent / "data" / "alertas.json"


def carregar_alertas() -> List[Dict]:
    if not JSON_PATH.exists():
        return []

    with open(JSON_PATH, "r", encoding="utf-8") as f:
      return json.load(f)


def salvar_alerta(alerta_dict: Dict) -> None:
    alertas = carregar_alertas()
    alertas.append(alerta_dict)

    JSON_PATH.parent.mkdir(exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
      json.dump(alertas, f, indent=2, ensure_ascii=False)


def listar_todos_alertas() -> List[Dict]:
    return carregar_alertas()
