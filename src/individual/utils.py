import re
from datetime import datetime
from decimal import Decimal
from typing import Optional

def parse_bool(v: Optional[str]) -> Optional[bool]:
    if v is None:
        return None
    s = str(v).strip().lower()
    if s in {"sim", "s", "true", "1", "yes"}:
        return True
    if s in {"nao", "não", "n", "false", "0", "no"}:
        return False
    return None

def parse_int_from_any(v: Optional[str]) -> Optional[int]:
    if v is None or str(v).strip() == "":
        return None
    # Tenta inteiro direto
    try:
        return int(str(v))
    except:
        pass
    # Extrai primeiro número inteiro encontrado
    m = re.search(r"(\d+)", str(v))
    return int(m.group(1)) if m else None

def parse_decimal_currency_br(v: Optional[str]) -> Optional[Decimal]:
    if v is None or str(v).strip() == "":
        return None
    s = str(v).strip()
    # remove "R$" e espaços
    s = s.replace("R$", "").replace(" ", "")
    # converte milhar ponto e decimal vírgula
    s = s.replace(".", "").replace(",", ".")
    try:
        return Decimal(s)
    except:
        return None

def parse_date_br(v: Optional[str]) -> Optional[datetime]:
    if v is None or str(v).strip() == "":
        return None
    try:
        return datetime.strptime(v.strip(), "%d/%m/%Y")
    except:
        return None