# Pipeline automatizada com GitHub Actions

Projeto em Python que serve de base para demonstrar uma pipeline de CI no GitHub Actions
usando **3 Actions do GitHub Marketplace**, cada uma aplicada em uma etapa adequada do processo.

## O projeto

Biblioteca pequena de utilitários de texto (`app/textutils.py`) com uma CLI (`app/cli.py`):

| Função | O que faz |
|---|---|
| `slugify(texto)` | Gera slug sem acentos (`"Olá, Mundo!"` → `ola-mundo`) |
| `count_words(texto)` | Conta palavras |
| `is_palindrome(texto)` | Detecta palíndromos ignorando acentos e pontuação |
| `top_words(texto, n)` | Palavras mais frequentes |

Uso local:

```bash
pip install -r requirements.txt
pytest --cov=app
python -m app.cli "Socorram-me, subi no ônibus em Marrocos"
```

## A pipeline (`.github/workflows/ci.yml`)

Disparada em `push` e `pull_request` na branch `main`, e manualmente (`workflow_dispatch`).

```
 push / PR
    │
    ▼
┌─────────────────────────────────────┐     ┌──────────────────────────────┐
│ Job "test" (Python 3.11 e 3.12)     │     │ Job "security"               │
│  1. checkout                        │     │  1. checkout                 │
│  2. actions/setup-python  ◄─ ACTION 1│ ──► │  2. codeql-action/init  ◄─ 3 │
│  3. instala dependências            │     │  3. codeql-action/analyze    │
│  4. pytest + cobertura (mín. 90%)   │     │     (só roda se "test" passar)│
│  5. actions/upload-artifact ◄─ ACTION 2│   └──────────────────────────────┘
└─────────────────────────────────────┘
```

## Actions utilizadas

| # | Action | Etapa | Função | Contribuição para a automação |
|---|---|---|---|---|
| 1 | [`actions/setup-python`](https://github.com/marketplace/actions/setup-python) | Preparação do ambiente (build) | Instala a versão do Python pedida na matriz (3.11 e 3.12) e faz cache do `pip` | Ambiente idêntico e reproduzível a cada execução, sem configuração manual; o cache reduz o tempo das execuções seguintes; a matriz testa duas versões em paralelo |
| 2 | [`actions/upload-artifact`](https://github.com/marketplace/actions/upload-artifact) | Pós-testes (relatórios) | Guarda `junit.xml`, `coverage.xml` e o relatório HTML (`htmlcov/`) como artefatos da execução | Os resultados ficam disponíveis para download mesmo quando os testes falham (`if: always()`), facilitando a auditoria e a análise de falhas |
| 3 | [`github/codeql-action`](https://github.com/marketplace/actions/codeql-action) (`init` + `analyze`) | Segurança | Analisa estaticamente o código Python em busca de vulnerabilidades e publica os alertas na aba **Security** | Verificação de segurança automática a cada alteração, sem ferramenta externa; só roda depois que os testes passam (`needs: test`) |

> `actions/checkout` também é usado, mas é apenas o pré-requisito para baixar o código, por isso não conta entre as 3 Actions principais.

Etapas adicionais sem Action de terceiros: instalação das dependências, execução do `pytest` com limite mínimo de cobertura (`--cov-fail-under=90`) e resumo de cobertura exibido na página da execução (`GITHUB_STEP_SUMMARY`).

## Como verificar o funcionamento de cada etapa

1. Abra a aba **Actions** do repositório e clique na execução **CI Pipeline**.
2. **setup-python**: no job *Testes e cobertura*, o passo "Configurar Python" deve ficar verde; na 2ª execução, procure a mensagem de *cache hit*.
3. **upload-artifact**: no fim da página da execução, a seção **Artifacts** deve listar `relatorios-py3.11` e `relatorios-py3.12`.
4. **CodeQL**: o job *Análise de segurança* deve ficar verde; resultados em **Security → Code scanning**.
5. O resumo de cobertura aparece na aba **Summary** da execução.

## Evidências da execução

> Cole aqui os prints depois de rodar a pipeline.

- [ ] Print da execução completa (todos os jobs verdes)
- [ ] Print da seção *Artifacts*
- [ ] Print da aba *Security → Code scanning*
