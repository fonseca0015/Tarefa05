"""Funções utilitárias de texto usadas como base do projeto de pipeline."""

import re
import unicodedata


def slugify(text: str) -> str:
    """Converte um texto em slug (minúsculo, sem acentos, separado por hífen)."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower())
    return ascii_text.strip("-")


def count_words(text: str) -> int:
    """Conta as palavras de um texto."""
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


def is_palindrome(text: str) -> bool:
    """Verifica se o texto é um palíndromo, ignorando acentos, espaços e pontuação."""
    cleaned = slugify(text).replace("-", "")
    return cleaned != "" and cleaned == cleaned[::-1]


def top_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    """Retorna as n palavras mais frequentes (minúsculas), em ordem decrescente."""
    if n <= 0:
        raise ValueError("n deve ser maior que zero")
    counts: dict[str, int] = {}
    for word in re.findall(r"\w+", text.lower(), flags=re.UNICODE):
        counts[word] = counts.get(word, 0) + 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]
