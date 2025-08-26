from src.individual.enums import SexoType, EstadoCivilType, SituacaoCadastralType
from typing import Optional

def map_sexo(v: Optional[str]) -> Optional[SexoType]:
    if not v:
        return None
    s = v.strip().lower()
    if s.startswith("masc"):
        return SexoType.MASCULINO
    if s.startswith("fem"):
        return SexoType.FEMININO
    return None

def map_estado_civil(v: Optional[str]) -> Optional[EstadoCivilType]:
    if not v:
        return None
    s = v.strip().upper()
    # ajuste conforme teus valores de enum
    if "SOLTE" in s:   return EstadoCivilType.SOLTEIRO
    if "CASAD" in s:   return EstadoCivilType.CASADO
    if "SEPARA" in s:  return EstadoCivilType.SEPARADO
    if "DIVORC" in s:  return EstadoCivilType.DIVORCIADO
    if "VIUV" in s or "VIÚV" in s: return EstadoCivilType.VIUVO
    return None

def map_situacao_cadastral(v: Optional[str]) -> Optional[SituacaoCadastralType]:
    if not v:
        return None
    s = v.strip().upper()
    # ajuste conforme teu enum
    if "REGULAR" in s:     return SituacaoCadastralType.REGULAR
    if "PENDENTE" in s:    return SituacaoCadastralType.PENDENTE
    if "CANCEL" in s:      return SituacaoCadastralType.CANCELADA
    if "SUSPEN" in s:      return SituacaoCadastralType.SUSPENSA
    if "NULA" in s:        return SituacaoCadastralType.NULA
    return None