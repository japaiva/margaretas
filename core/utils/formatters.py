# =============================================================================
# ARQUIVO: core/utils/formatters.py (LIMPO)
# =============================================================================

from typing import Any, Dict, Union
from .decimal_helpers import safe_decimal, safe_float, safe_int

def formato_seguro(valor: Any, decimais: int = 2) -> float:
    """
    Formata um número com segurança, tratando possíveis erros
    
    Args:
        valor: Valor a ser formatado
        decimais: Número de casas decimais
        
    Returns:
        float: Valor formatado
    """
    try:
        numero = float(valor)
        return round(numero, decimais)
    except (ValueError, TypeError):
        return 0.0


def formato_negrito(texto: str) -> str:
    """
    Formata texto com negrito de maneira compatível com PDF e HTML
    
    Args:
        texto: Texto a ser formatado
        
    Returns:
        str: Texto formatado
    """
    return f"<strong>{texto}</strong>"


def formato_moeda_br(valor: Union[int, float, str], incluir_simbolo: bool = True) -> str:
    """
    Formata valores monetários no padrão brasileiro
    
    Args:
        valor: Valor a ser formatado
        incluir_simbolo: Se deve incluir o símbolo R$
        
    Returns:
        str: Valor formatado
    """
    try:
        if valor is None:
            return "R$ 0,00" if incluir_simbolo else "0,00"
        
        # Usar safe_float para conversão segura
        valor_float = safe_float(valor)
        
        # Formatar o número
        formatted = f"{valor_float:,.2f}"
        
        # Troca vírgula e ponto para padrão brasileiro
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        if incluir_simbolo:
            return f"R$ {formatted}"
        return formatted
        
    except Exception:
        return "R$ 0,00" if incluir_simbolo else "0,00"


def formato_numero_br(valor: Union[int, float, str]) -> str:
    """
    Formata números para o padrão brasileiro (vírgula para decimal, ponto para milhares)
    
    Args:
        valor: Valor a ser formatado
        
    Returns:
        str: Número formatado
    """
    try:
        if valor is None:
            return "0,00"
        
        valor_float = safe_float(valor)
        formatted = f"{valor_float:,.2f}"
        
        # Troca vírgula e ponto para padrão brasileiro
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        
        return formatted
        
    except Exception:
        return "0,00"


def formato_percentual_br(valor: Union[int, float, str]) -> str:
    """
    Formata percentuais no padrão brasileiro
    
    Args:
        valor: Valor a ser formatado
        
    Returns:
        str: Percentual formatado
    """
    try:
        if valor is None:
            return "0,0%"
        
        valor_float = safe_float(valor)
        formatted = f"{valor_float:.1f}".replace('.', ',')
        return f"{formatted}%"
        
    except Exception:
        return "0,0%"
