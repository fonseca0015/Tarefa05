"""Interface de linha de comando simples: python -m app.cli "seu texto"."""

import sys

from app.textutils import count_words, is_palindrome, slugify, top_words


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print('Uso: python -m app.cli "texto de exemplo"')
        return 1
    text = " ".join(args)
    palindromo = "sim" if is_palindrome(text) else "não"
    print(f"Slug:         {slugify(text)}")
    print(f"Palavras:     {count_words(text)}")
    print(f"Palíndromo:   {palindromo}")
    print(f"Top palavras: {top_words(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
