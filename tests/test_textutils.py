import pytest

from app.cli import main
from app.textutils import count_words, is_palindrome, slugify, top_words


def test_slugify_remove_acentos_e_pontuacao():
    assert slugify("Olá, Mundo! Ação 2026") == "ola-mundo-acao-2026"


def test_slugify_vazio():
    assert slugify("") == ""


def test_count_words():
    assert count_words("um dois  três, quatro.") == 4
    assert count_words("") == 0


def test_is_palindrome_verdadeiro():
    assert is_palindrome("Socorram-me, subi no ônibus em Marrocos")
    assert is_palindrome("Ovo")


def test_is_palindrome_falso_e_vazio():
    assert not is_palindrome("pipeline")
    assert not is_palindrome("")


def test_top_words_ordenacao():
    assert top_words("a b a c b a", n=2) == [("a", 3), ("b", 2)]


def test_top_words_n_invalido():
    with pytest.raises(ValueError):
        top_words("abc", n=0)


def test_cli_sem_argumentos(capsys):
    assert main([]) == 1
    assert "Uso:" in capsys.readouterr().out


def test_cli_com_texto(capsys):
    assert main(["Ovo"]) == 0
    saida = capsys.readouterr().out
    assert "ovo" in saida
    assert "sim" in saida
