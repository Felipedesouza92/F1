---
name: python-f1-dashboard
description: >-
  Regras, convenções, ferramentas e boas práticas para desenvolver, testar,
  documentar e manter o projeto F1 Dashboard em Python.
  Stack oficial: pyenv (versão do Python), Poetry (ambiente e dependências),
  layout src/ com camadas (ingestion, processing, domain, dashboard, utils),
  Ruff (lint, formatação e imports), Pytest + pytest-cov (cobertura unitária
  mínima de 50%) e MkDocs Material (documentação). Use ao iniciar o projeto,
  implementar ou alterar código, escrever testes, configurar CI, revisar
  pull requests ou atualizar documentação.
---

# Skill: Padronização de Projeto Python — F1 Dashboard

## 0. Como usar este documento

### 0.1 Níveis de exigência

| Termo | Significado | Consequência do descumprimento |
| --- | --- | --- |
| **MUST** / **MUST NOT** | Requisito obrigatório. | Bloqueia merge e entrega. |
| **SHOULD** / **SHOULD NOT** | Recomendação forte. Desvios exigem justificativa no PR ou em comentário no código. | Deve ser discutido na revisão. |
| **MAY** | Prática opcional, adotada conforme contexto. | Nenhuma. |

Cada regra tem um identificador (`DEP-01`, `TST-03` etc.) para ser citada em revisões, PRs e commits.

### 0.2 Instruções específicas para agentes de IA

- **MUST** ler `pyproject.toml`, `README.md` e a documentação em `docs/` antes de alterar código.
- **MUST** executar o fluxo de validação da [seção 10](#10-fluxo-de-desenvolvimento-e-validação) antes de declarar uma tarefa concluída e relatar o resultado real de cada etapa, incluindo falhas.
- **MUST NOT** reduzir o limite de cobertura, adicionar `# noqa`, `# pragma: no cover`, `per-file-ignores` ou desativar etapas de CI com o objetivo de fazer a validação passar.
- **MUST NOT** editar `poetry.lock` manualmente nem usar `pip` para gerenciar dependências.
- **MUST NOT** adicionar dependências, frameworks ou camadas arquiteturais sem necessidade demonstrada pela tarefa. Ao adicionar uma dependência, justifique-a no resumo da entrega.
- **SHOULD** perguntar quando um requisito for ambíguo, em vez de presumir.
- **MUST NOT** inventar opções de configuração ou comandos. Em caso de dúvida, consulte `poetry run <ferramenta> --help`.

---

## 1. Gerenciamento do ambiente Python

### 1.1 Ferramentas obrigatórias

| Ferramenta | Responsabilidade |
| --- | --- |
| **pyenv** | Instalar e selecionar a versão do Python localmente. |
| **Poetry ≥ 2.0** | Gerenciar ambiente virtual, dependências, lock, build e execução de comandos. |

### 1.2 Regras

| ID | Nível | Regra |
| --- | --- | --- |
| DEP-01 | MUST NOT | Usar `pip install`, `pip uninstall`, `python -m pip`, `virtualenv`, `conda` ou equivalentes para gerenciar dependências do projeto. |
| DEP-02 | MUST | A versão do Python **MUST** ser definida no arquivo `.python-version`, gerenciado pelo pyenv. |
| DEP-03 | MUST | A versão no `.python-version` **MUST** ser compatível com `requires-python` do `pyproject.toml`. |
| DEP-04 | MUST | O ambiente virtual **MUST** ser gerenciado pelo Poetry, preferencialmente localizado dentro do projeto (`virtualenvs.in-project = true`). |
| DEP-05 | MUST NOT | Nenhuma dependência do projeto ou ferramenta de desenvolvimento pode ser instalada globalmente no Python do sistema. |
| DEP-06 | MUST | Todas as instalações usam Poetry: produção, desenvolvimento, lint, formatação, testes e documentação. |
| DEP-07 | MUST | Ferramentas Python **MUST** ser executadas com `poetry run` ou mecanismos equivalentes do Poetry. |
| DEP-08 | MUST | Versionar `poetry.lock` no Git. |
| DEP-09 | MUST NOT | Editar `poetry.lock` manualmente. |
| DEP-10 | MUST | Após alterar `pyproject.toml` em campos que afetem a resolução, executar `poetry lock` e versionar o lock atualizado. |
| DEP-11 | MUST | Separar dependências em grupos: produção (`[project] dependencies`), `dev` (lint, testes) e `docs` (MkDocs). |

**Exceção:** a instalação do **próprio Poetry** fica fora do projeto. Use o instalador oficial ou `pipx install poetry`.

### 1.3 Configuração do ambiente desde uma instalação limpa

```bash
# 1. Instalar pyenv (Windows: pyenv-win)
# https://github.com/pyenv-win/pyenv-win#installation

# 2. Instalar a versão do Python definida pelo projeto
pyenv install 3.12.10

# 3. Definir a versão local (gera/atualiza .python-version)
pyenv local 3.12.10

# 4. Verificar
python --version
# Python 3.12.10

# 5. Instalar Poetry (se ainda não tiver)
pipx install poetry

# 6. Configurar o Poetry para criar o venv dentro do projeto
poetry config virtualenvs.in-project true

# 7. Selecionar o interpretador
poetry env use python

# 8. Instalar todas as dependências (incluindo docs)
poetry install --with docs

# 9. Validar o ambiente
poetry env info
poetry run python --version
poetry check --lock
```

### 1.4 Comandos de gerenciamento de dependências

| Situação | Comando |
| --- | --- |
| Instalar o projeto e dependências não opcionais | `poetry install` |
| Instalar também o grupo de documentação | `poetry install --with docs` |
| Instalar apenas produção (deploy) | `poetry install --only main` |
| Adicionar dependência de produção | `poetry add httpx` |
| Adicionar dependência com restrição | `poetry add "httpx>=0.27,<1.0"` |
| Adicionar dependência de desenvolvimento | `poetry add --group dev pytest` |
| Adicionar dependência de documentação | `poetry add --group docs mkdocs-material` |
| Remover dependência | `poetry remove httpx` |
| Remover de grupo | `poetry remove --group dev pre-commit` |
| Atualizar dentro das restrições | `poetry update` ou `poetry update httpx` |
| Regenerar lock sem atualizar versões | `poetry lock` |
| Verificar consistência pyproject ↔ lock | `poetry check --lock` |
| Listar dependências desatualizadas | `poetry show --outdated` |
| Executar ferramenta | `poetry run ruff check .` |

> `poetry shell` foi removido do núcleo do Poetry 2.x. Prefira `poetry run`.

---

## 2. Estrutura do projeto

### 2.1 Estrutura de referência

```text
F1/
├── .python-version            # versão do Python (pyenv)
├── .gitignore                 # arquivos ignorados pelo Git
├── .env.example               # variáveis de ambiente esperadas (sem valores reais)
├── .pre-commit-config.yaml    # hooks de pre-commit
├── .secrets.baseline          # baseline do detect-secrets
├── .streamlit/
│   └── config.toml            # tema visual do Streamlit
├── pyproject.toml             # metadados, dependências e configuração de ferramentas
├── poetry.lock                # lock de dependências (versionado)
├── README.md                  # visão geral e guia rápido
├── SKILL.md                   # este documento
├── src/
│   └── f1/                    # pacote principal da aplicação
│       ├── __init__.py
│       ├── ingestion/         # fontes e destinos: HTTP clients, repositórios concretos
│       │   └── __init__.py
│       ├── processing/        # transformações puras, limpeza, agregações
│       │   └── __init__.py
│       ├── domain/            # modelos, ABCs de repositórios, serviços, regras de negócio
│       │   └── __init__.py
│       ├── dashboard/         # camada de apresentação Streamlit (composition root)
│       │   └── __init__.py
│       └── utils/             # config.py, logger.py, helpers transversais
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # fixtures compartilhadas
│   ├── fixtures/              # JSON sintéticos por endpoint
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       └── __init__.py
├── docs/
│   ├── mkdocs.yml             # configuração do MkDocs Material
│   └── docs/
│       ├── index.md
│       ├── architecture.md
│       ├── project-structure.md
│       ├── running-locally.md
│       ├── running-tests.md
│       └── contributing.md
└── .github/
    └── workflows/
        └── ci.yml             # CI: lint, testes, cobertura, docs
```

### 2.2 Responsabilidades dos diretórios e arquivos

| Diretório / Arquivo | Responsabilidade |
| --- | --- |
| `.python-version` | Define a versão do Python para o pyenv. |
| `pyproject.toml` | Centraliza metadados, dependências, config do Ruff, Pytest, Coverage e MkDocs. |
| `poetry.lock` | Garante reprodutibilidade das instalações. |
| `src/f1/` | Todo código de produção. Usa o padrão `src/` para isolar o pacote dos testes e configurações. |
| `src/f1/ingestion/` | Leitura e escrita de dados externos: HTTP clients, repositórios concretos da OpenF1. |
| `src/f1/processing/` | Transformações puras (sem I/O): filtros, agregações, formatação de dados. |
| `src/f1/domain/` | Modelos (Pydantic), ABCs de repositórios, serviços de orquestração, regras de negócio. |
| `src/f1/dashboard/` | Camada de apresentação Streamlit: `app.py` (composition root), gráficos Plotly, componentes UI. |
| `src/f1/utils/` | Código transversal sem regra de negócio: configuração, logging, helpers. |
| `tests/` | Testes unitários e de integração, separados do código de produção. |
| `tests/unit/` | Testes rápidos, determinísticos, sem rede nem serviços externos. |
| `tests/integration/` | Testes que acessam a API real (marcados com `@pytest.mark.integration`). |
| `docs/` | Documentação técnica com MkDocs Material. |

### 2.3 Regras de estrutura

| ID | Nível | Regra |
| --- | --- | --- |
| EST-01 | MUST | Todo código de produção fica em `src/f1/`, com `__init__.py`. |
| EST-02 | MUST | Testes em `tests/`, documentação em `docs/`, configuração de ferramentas em `pyproject.toml`. |
| EST-03 | MUST | Configurar o Poetry: `packages = [{ include = "f1", from = "src" }]` em `[tool.poetry]`. |
| EST-04 | MUST NOT | Criar subpacotes vazios apenas para seguir uma estrutura. |
| EST-05 | MUST | Organizar o código nas camadas `ingestion/`, `processing/`, `domain/`, `dashboard/` e `utils/`. |
| EST-06 | MUST NOT | Colocar lógica de negócio em scripts de execução, `__main__`, notebooks ou `conftest.py`. |
| EST-07 | MUST | Usar imports absolutos (`from f1.domain.models import Session`). Imports relativos são proibidos. |

### 2.4 Regra de dependência entre camadas

```text
dashboard → domain.services → (domain.repositories, processing) → domain.models
                                        ↑
                                   ingestion (implementa os contratos)
```

- `domain` **MUST NOT** importar `ingestion`, `httpx` nem `streamlit`.
- `ingestion` **MUST NOT** conter regra de negócio.
- `processing` é puro: sem I/O, sem estado.
- `utils` pode ser importado por todas as camadas e não importa nenhuma delas.

---

## 3. Gerenciamento de dependências com Poetry

### 3.1 Regras

| ID | Nível | Regra |
| --- | --- | --- |
| DEP-12 | MUST | `pyproject.toml` concentra todas as configurações: metadados, `requires-python`, dependências, Ruff, Pytest, Coverage e MkDocs. |
| DEP-13 | MUST | Adicionar dependências com `poetry add` e remover com `poetry remove`. |
| DEP-14 | SHOULD NOT | Editar à mão as seções de dependências do `pyproject.toml`. Use `poetry add`/`poetry remove`. |
| DEP-15 | MUST NOT | Misturar Poetry com pip, virtualenv, conda ou outros gerenciadores. |
| DEP-16 | SHOULD | Preferir a biblioteca padrão quando resolver o problema. Cada nova dependência **SHOULD** ter justificativa no PR. |
| DEP-17 | MUST | `version` do `pyproject.toml` segue SemVer (`MAJOR.MINOR.PATCH`). |

### 3.2 Configuração de referência do `pyproject.toml`

> Os metadados e versões são **ilustrativos**. As faixas de versão das dependências são geradas por `poetry add`.
> As seções `[tool.*]` são a **referência obrigatória**.

```toml
[project]
name = "f1"
version = "0.1.0"
description = "Dashboard interativo de Fórmula 1 com dados da OpenF1 API."
authors = [
    {name = "Felipe de Souza", email = "felipe.desouza1992@gmail.com"}
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = []  # gerenciado por `poetry add`

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"

# ---------------------------------------------------------------- Poetry
[tool.poetry]
packages = [{include = "f1", from = "src"}]

# Grupos gerados por `poetry add --group ...` (versões ilustrativas).
[tool.poetry.group.dev.dependencies]
ruff = "^0.9.0"
pytest = "^8.3.0"
pytest-cov = "^6.0.0"
pytest-mock = "^3.14.0"
pre-commit = "^4.0.0"
detect-secrets = "^1.5.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs-material = "^9.5.0"
mkdocstrings = { version = "^0.27.0", extras = ["python"] }

# ---------------------------------------------------------------- Ruff
[tool.ruff]
target-version = "py312"     # MUST corresponder ao limite inferior de requires-python
line-length = 88
src = ["src", "tests"]       # classificação first-party dos imports
extend-exclude = ["notebooks"]

[tool.ruff.lint]
select = [
    # Conjunto mínimo obrigatório
    "E",    # pycodestyle (erros)
    "W",    # pycodestyle (avisos)
    "F",    # pyflakes: nomes indefinidos, imports não utilizados
    "I",    # isort: ordenação de imports
    "N",    # pep8-naming
    "UP",   # pyupgrade: sintaxe moderna para o target-version
    "B",    # flake8-bugbear: bugs prováveis
    "C4",   # flake8-comprehensions
    # Regras adicionais
    "SIM",  # flake8-simplify
    "RET",  # flake8-return
    "PTH",  # flake8-use-pathlib
    "BLE",  # flake8-blind-except
    "T20",  # flake8-print: proíbe print()
    "S",    # flake8-bandit: segurança
    "PT",   # flake8-pytest-style
    "D",    # pydocstyle (PEP 257)
    "TID",  # flake8-tidy-imports: proíbe imports relativos
    "RUF",  # regras do Ruff
]
ignore = [
    "E501",  # comprimento de linha: gerenciado pelo formatador
    "D100",  # docstring de módulo: opcional
    "D104",  # docstring de pacote (__init__.py): opcional
    "D105",  # docstring de métodos mágicos: opcional
    "D107",  # docstring de __init__: documentar na classe
    "D206",  # conflita com o formatador
    "D300",  # conflita com o formatador
    "W191",  # conflita com o formatador
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",  # assert é o mecanismo do pytest
    "D",     # docstrings não exigidas em testes
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
known-first-party = ["f1"]

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

# ---------------------------------------------------------------- Pytest
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--import-mode=importlib",
    "--cov=src/f1",
    "--cov-report=term-missing",
    "--cov-fail-under=50",
]
markers = [
    "integration: testes que dependem de recursos externos (API real)",
]

# ---------------------------------------------------------------- Coverage
[tool.coverage.run]
branch = true

[tool.coverage.report]
fail_under = 50
show_missing = true
exclude_also = [
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
```

**Pontos de consistência que MUST ser mantidos:**

- `target-version` do Ruff = limite inferior de `requires-python` (`py312` ↔ `>=3.12`).
- `known-first-party` usa o **nome do pacote importável** (`f1`) e `--cov=` usa o **caminho** do pacote (`src/f1`).
- A cobertura fica em `addopts`, então `poetry run pytest tests/unit/` já aplica o limite de 50%.
- Testes de integração e execuções focadas **MUST** rodar com `--no-cov`.
- As regras do conjunto mínimo obrigatório do Ruff (`E`, `W`, `F`, `I`, `N`, `UP`, `B`, `C4`) **MUST NOT** ser removidas do `select`.

---

## 4. Qualidade e formatação com Ruff

### 4.1 Regras

| ID | Nível | Regra |
| --- | --- | --- |
| LNT-01 | MUST | Usar Ruff para lint, formatação e organização de imports, configurado em `[tool.ruff]` no `pyproject.toml`. |
| LNT-02 | MUST | `poetry run ruff check .` e `poetry run ruff format --check .` **MUST** passar sem erros antes de considerar uma tarefa concluída. |
| LNT-03 | MUST | Remover imports não utilizados (`F401`) e manter imports ordenados (`I`). |
| LNT-04 | MUST NOT | Usar Black, isort, flake8, pylint ou outras ferramentas para responsabilidades cobertas pelo Ruff. |
| LNT-05 | MUST | Justificar cada supressão com `# noqa: <CÓDIGO>` e motivo. `# noqa` sem código é proibido. |
| LNT-06 | MUST | Revisar o diff de `ruff check --fix`. `--unsafe-fixes` **MUST NOT** ser aplicado sem revisão. |

### 4.2 Comandos

```bash
# Verificar lint
poetry run ruff check .

# Lint com correções automáticas seguras (inclui imports)
poetry run ruff check . --fix

# Formatar o código
poetry run ruff format .

# Verificar formatação sem alterar (CI)
poetry run ruff format --check .

# Explicar uma regra
poetry run ruff rule BLE001
```

**Diferença entre os comandos:**

| Comando | O que faz |
| --- | --- |
| `ruff check .` | **Verifica** — analisa o código e reporta problemas de lint sem alterar nada. |
| `ruff check . --fix` | **Corrige** — aplica correções automáticas seguras (ex: remover imports, reordenar). |
| `ruff format .` | **Formata** — reformata o código (indentação, aspas, quebras de linha). |
| `ruff format --check .` | **Verifica formatação** — checa se o código já está formatado, sem alterar. |

**Ordem local recomendada:** `ruff check . --fix` → `ruff format .` → `ruff check .`

O código **MUST** passar por lint e formatação antes de ser considerado pronto para entrega.

---

## 5. Testes unitários com Pytest

### 5.1 Regras

| ID | Nível | Regra |
| --- | --- | --- |
| TST-01 | MUST | Usar Pytest, executado via `poetry run pytest`. Testes em `tests/unit/` e `tests/integration/`, cada pasta com `__init__.py`. |
| TST-02 | MUST | Nomear arquivos `test_*.py` e funções `test_*`. Nomes **SHOULD** descrever o comportamento. |
| TST-03 | MUST | Testes para funções, classes e módulos relevantes do projeto. |
| TST-04 | MUST | Testar sucesso, erros esperados (`pytest.raises`), limites (vazio, um elemento, valores extremos) e dados inválidos. |
| TST-05 | MUST | Nomes de testes descritivos e organização consistente. |
| TST-06 | MUST | Testes unitários isolados: sem rede, banco, serviços externos. Usar fixtures e mocks. |
| TST-07 | SHOULD | Usar `@pytest.mark.parametrize` para variações de entrada, com `pytest.param(..., id="...")`. |
| TST-08 | SHOULD | Usar `pytest-mock` (`mocker`) para simular dependências; para contratos `ABC`, preferir `mocker.create_autospec()`. |
| TST-09 | MUST NOT | Usar credenciais reais ou dados de produção em testes. |
| TST-10 | MUST | Marcar testes de integração com `@pytest.mark.integration` e mantê-los em `tests/integration/`. |
| TST-11 | MUST | Corrigir um bug sempre com um teste que o reproduz. |

### 5.2 Cobertura mínima: 50%

A cobertura de testes unitários **MUST** ser de no mínimo **50%** do código de produção em `src/f1/`.

Regras de cobertura:

| ID | Nível | Regra |
| --- | --- | --- |
| TST-12 | MUST | A cobertura é medida com `pytest-cov` sobre `src/f1/` (configurada em `addopts`). |
| TST-13 | MUST | A execução **MUST** falhar quando a cobertura ficar abaixo de 50% (`--cov-fail-under=50`). |
| TST-14 | MUST | Calcular a cobertura somente sobre o código de produção. Os próprios testes **MUST NOT** entrar no cálculo. |
| TST-15 | MUST NOT | Reduzir o limite mínimo de cobertura para fazer os testes passarem. |
| TST-16 | MUST | Exclusões de cobertura (`# pragma: no cover`) **MUST** ser explícitas e justificadas. |

> **Cobertura de linhas não garante qualidade.** 50% é um piso mínimo, não uma meta. Um teste sem asserção relevante aumenta a cobertura e não protege nada. O revisor **MUST** avaliar se os testes verificam comportamento (valores retornados, exceções, efeitos), não apenas se executam linhas.
>
> Com `branch = true`, o percentual combina linhas e ramificações, tornando o limite mais rigoroso.

### 5.3 Comandos

```bash
# Suíte unitária com cobertura (--cov vem de addopts)
poetry run pytest tests/unit/

# Com relatório completo
poetry run pytest --cov=f1 --cov-report=term-missing

# Com verificação de cobertura mínima explícita
poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50

# Relatório HTML (MAY)
poetry run pytest tests/unit/ --cov-report=html

# Testes de integração (sem cobertura)
poetry run pytest tests/integration/ -m integration --no-cov

# Execução focada durante o desenvolvimento (sem o limite de cobertura)
poetry run pytest tests/unit/test_processing_laps.py -k "top_n" -x --no-cov
```

> Rodar um único arquivo com o limite ativo pode falhar por cobertura baixa; por isso a execução focada usa `--no-cov`.

---

## 6. Documentação com MkDocs Material

### 6.1 Regras

| ID | Nível | Regra |
| --- | --- | --- |
| DOC-01 | MUST | Usar MkDocs com o tema Material, configurado em `docs/mkdocs.yml`, com conteúdo em `docs/docs/`. |
| DOC-02 | MUST | `poetry run mkdocs build -f docs/mkdocs.yml --strict` **MUST** passar localmente e na CI. |
| DOC-03 | MUST | Atualizar a documentação no mesmo PR que altera comportamento, arquitetura ou configuração. |
| DOC-04 | MUST | MkDocs e Material são instalados dentro do ambiente virtual gerenciado pelo Poetry. |

### 6.2 Conteúdo mínimo da documentação

| Página | Conteúdo esperado |
| --- | --- |
| `index.md` | Visão geral e objetivo do projeto. |
| `architecture.md` | Diagrama de camadas, fluxo de dados, injeção de dependências. |
| `project-structure.md` | Árvore de diretórios comentada. |
| `running-locally.md` | Requisitos e pré-requisitos. Instalação e configuração do ambiente. Instruções de execução. |
| `running-tests.md` | Como executar testes, verificar e formatar o código. Referência de configuração. |
| `contributing.md` | Guia de contribuição, fluxo de PR, checklist. |

### 6.3 `docs/mkdocs.yml` de referência

```yaml
site_name: F1 Dashboard
site_description: Dashboard interativo de Fórmula 1 com dados da OpenF1 API.
docs_dir: docs
site_dir: site

theme:
  name: material
  language: pt
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.highlight
    - content.code.copy

nav:
  - Início: index.md
  - Arquitetura: architecture.md
  - Estrutura do Projeto: project-structure.md
  - Como Rodar Local: running-locally.md
  - Como Rodar Testes: running-tests.md
  - Como Contribuir: contributing.md

plugins:
  - search

markdown_extensions:
  - admonition
  - attr_list
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.highlight
  - pymdownx.inlinehilite
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true

validation:
  omitted_files: warn
  absolute_links: warn
  unrecognized_links: warn
  anchors: warn
```

### 6.4 Comandos

```bash
# Instalar dependências de documentação
poetry add --group docs mkdocs-material "mkdocstrings[python]"
poetry install --with docs

# Servidor local com recarga automática
poetry run mkdocs serve -f docs/mkdocs.yml

# Build de validação (CI)
poetry run mkdocs build -f docs/mkdocs.yml --strict
```

---

## 7. Boas práticas e restrições

### 7.1 Código

| ID | Nível | Regra |
| --- | --- | --- |
| PY-01 | MUST | Código legível, modular e de fácil manutenção. |
| PY-02 | MUST | Type hints em todas as funções e métodos (PEP 484, sintaxe moderna: `list[str]`, `X \| None`). |
| PY-03 | MUST | Docstrings no estilo Google nas APIs públicas e componentes que precisem de explicação. |
| PY-04 | MUST | Tratamento explícito de exceções. Capturar exceções específicas. |
| PY-05 | MUST | Encadear exceções ao traduzi-las (`raise NovoErro(...) from exc`). |
| PY-06 | MUST | Usar context managers (`with`) para arquivos, conexões e recursos. |
| PY-07 | MUST | Usar `logging` para observabilidade. `print()` proibido em código de produção. |
| PY-08 | MUST | Nomes claros: `snake_case` para variáveis/funções, `PascalCase` para classes, `UPPER_SNAKE_CASE` para constantes. |
| PY-09 | SHOULD | Princípio de responsabilidade única e baixo acoplamento. |
| PY-10 | SHOULD | Preferir funções puras. Isolar efeitos colaterais nas bordas (I/O, rede). |
| PY-11 | SHOULD | Usar `pathlib.Path` em vez de `os.path`. |
| PY-12 | SHOULD | Usar `dataclasses` ou Pydantic para estruturas de dados. |

### 7.2 Segurança

| ID | Nível | Regra |
| --- | --- | --- |
| SEG-01 | MUST NOT | Segredos, tokens e credenciais no código, logs ou versionamento. |
| SEG-02 | MUST | Usar variáveis de ambiente para configurações sensíveis. |
| SEG-03 | MUST | Manter `.env` fora do versionamento (`.gitignore`). |
| SEG-04 | MUST | Fornecer `.env.example` com variáveis esperadas e valores fictícios. |
| SEG-05 | MUST | Centralizar configuração em `utils/config.py`, carregando uma vez no ponto de entrada. |

### 7.3 Restrições

| ID | Nível | Regra |
| --- | --- | --- |
| RES-01 | MUST NOT | Alterar configurações ou dependências sem necessidade. |
| RES-02 | MUST NOT | Reduzir o limite mínimo de cobertura para fazer os testes passarem. |
| RES-03 | MUST NOT | Ignorar erros de lint ou testes sem justificativa documentada. |
| RES-04 | MUST NOT | Incluir `.venv/`, `__pycache__/`, `.coverage`, `htmlcov/`, `docs/site/` ou caches no Git. |
| RES-05 | MUST NOT | Introduzir abstrações, dependências e complexidade desnecessárias. |
| RES-06 | MUST NOT | Usar estado global mutável ou argumentos default mutáveis. |

### 7.4 `.gitignore` mínimo

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
coverage.xml
htmlcov/
site/
docs/site/
dist/
.env
*.pem
*.key
*.secret
credentials.json
```

---

## 8. Logger padrão: `utils/logger.py`

```python
import logging
import sys

FORMATO = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
FORMATO_DATA = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """Retorna o logger do módulo `name`, sem configurar handlers."""
    return logging.getLogger(name)


def configurar_logging(nivel: str = "INFO") -> None:
    """Configura o handler único da aplicação. Chamar apenas no ponto de entrada."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=FORMATO, datefmt=FORMATO_DATA))
    raiz = logging.getLogger()
    raiz.handlers[:] = [handler]
    raiz.setLevel(nivel)
```

Uso: `logger = get_logger(__name__)` no topo de cada módulo; `configurar_logging(config.log_level)` apenas no ponto de entrada.

---

## 9. Pre-commit

### 9.1 `.pre-commit-config.yaml` de referência

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-merge-conflict
      - id: check-toml
      - id: check-yaml
      - id: check-added-large-files
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0  # MUST ser a versão do Ruff no poetry.lock
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]

  - repo: local
    hooks:
      - id: poetry-check-lock
        name: poetry check --lock
        entry: poetry check --lock
        language: system
        files: ^(pyproject\.toml|poetry\.lock)$
        pass_filenames: false
```

### 9.2 Comandos de configuração

```bash
poetry add --group dev pre-commit detect-secrets
poetry run detect-secrets scan > .secrets.baseline
poetry run pre-commit install
poetry run pre-commit run --all-files
```

---

## 10. Fluxo de desenvolvimento e validação

### 10.1 Fluxo mínimo (local = CI)

Antes de considerar uma implementação concluída, a IA **MUST**:

1. Entender a estrutura e as convenções existentes do projeto.
2. Confirmar a versão do Python e o ambiente gerenciado pelo Poetry.
3. Implementar a solução seguindo as convenções do código existente.
4. Criar ou atualizar testes unitários relevantes.
5. Executar o Ruff para verificar e corrigir problemas.
6. Executar o formatador Ruff.
7. Executar os testes e verificar a cobertura mínima de 50%.
8. Atualizar a documentação afetada.
9. Validar a compilação da documentação com MkDocs Material.
10. Resumir as alterações realizadas e informar os comandos executados e seus resultados.

| # | Etapa | Comando | Obrigatória |
| --- | --- | --- | --- |
| 1 | Consistência do lock | `poetry check --lock` | MUST |
| 2 | Instalação reprodutível | `poetry install --with docs` | MUST |
| 3 | Lint | `poetry run ruff check .` | MUST |
| 4 | Formatação | `poetry run ruff format --check .` | MUST |
| 5 | Testes unitários + cobertura ≥ 50% | `poetry run pytest tests/unit/` | MUST |
| 6 | Documentação | `poetry run mkdocs build -f docs/mkdocs.yml --strict` | MUST |

```bash
poetry check --lock
poetry install --with docs
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest tests/unit/
poetry run mkdocs build -f docs/mkdocs.yml --strict
```

A IA **MUST NOT** afirmar que testes, verificações ou builds passaram sem ter executado os respectivos comandos e verificado os resultados.

Caso algum comando falhe, a IA **MUST** informar o erro, investigar sua causa e tentar corrigi-lo quando estiver dentro do escopo da tarefa.

### 10.2 GitHub Actions (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validacao:
    runs-on: ubuntu-latest
    env:
      POETRY_VERSION: "2.1.3"
    steps:
      - uses: actions/checkout@v4

      - name: Instalar Poetry
        run: pipx install "poetry==${POETRY_VERSION}"

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: poetry

      - name: Selecionar interpretador
        run: poetry env use python

      - name: Verificar consistência do lock
        run: poetry check --lock

      - name: Instalar dependências
        run: poetry install --with docs

      - name: Lint
        run: poetry run ruff check . --output-format=github

      - name: Formatação
        run: poetry run ruff format --check .

      - name: Testes unitários e cobertura
        run: poetry run pytest tests/unit/

      - name: Documentação
        run: poetry run mkdocs build -f docs/mkdocs.yml --strict
```

### 10.3 Pull Requests

| ID | Nível | Regra |
| --- | --- | --- |
| PR-01 | MUST NOT | Fazer merge direto na branch principal. Todo código entra por Pull Request. |
| PR-02 | MUST NOT | Contornar checks de CI ou hooks (`--no-verify`). |
| PR-03 | MUST | Descrever o PR com: o que mudou, motivo, como validar e checklist de validação. |

---

## 11. Critérios de aceitação

Uma tarefa está **concluída** somente quando **todos** os itens abaixo são verdadeiros:

| # | Critério | Verificação |
| --- | --- | --- |
| 1 | O pyenv define a versão local do Python. | `.python-version` existe e é compatível com `requires-python`. |
| 2 | O Poetry gerencia o ambiente virtual e as dependências. | `poetry check --lock` retorna código 0. |
| 3 | Todas as ferramentas Python são instaladas no ambiente virtual. | `poetry install --with docs` retorna código 0. |
| 4 | O Ruff executa lint e formatação sem erros. | `poetry run ruff check .` e `poetry run ruff format --check .` retornam código 0. |
| 5 | O Pytest executa os testes unitários. | `poetry run pytest tests/unit/` retorna código 0. |
| 6 | A cobertura mínima de 50% é verificada para `src/f1/`. | `--cov-fail-under=50` em `addopts` passa. |
| 7 | A documentação usa MkDocs Material e compila. | `poetry run mkdocs build -f docs/mkdocs.yml --strict` retorna código 0. |
| 8 | Os comandos de configuração, validação e execução estão documentados. | Páginas em `docs/docs/` atualizadas. |
| 9 | O fluxo de trabalho da IA exige validação antes de declarar a tarefa concluída. | Seção 10 executada e resultados reportados. |
| 10 | Todo comportamento novo ou alterado tem teste. | Testes criados/atualizados no PR. |
| 11 | Nenhuma supressão ou dependência nova sem justificativa. | Revisão do PR. |

Para agentes de IA: ao entregar, informe o resultado de cada comando dos itens 2–7 (sucesso ou falha, com a saída relevante), liste as dependências adicionadas com justificativa e descreva as limitações conhecidas. **Não declare conclusão se qualquer item falhar.**

---

## 12. Solução de problemas comuns

| Sintoma | Causa provável | Solução |
| --- | --- | --- |
| `ModuleNotFoundError: f1` nos testes | Pacote não instalado ou `packages` ausente | Conferir `[tool.poetry] packages` (EST-03) e executar `poetry install`. |
| Poetry instala em outro ambiente | Variável `VIRTUAL_ENV` herdada | Remover `VIRTUAL_ENV` da sessão; conferir com `poetry env info`. |
| `pyproject.toml changed significantly since poetry.lock was last generated` | `pyproject.toml` editado sem atualizar o lock | `poetry lock` e versionar o lock (DEP-10). |
| Ruff classifica o pacote como third-party | `src` ou `known-first-party` incorretos | Conferir `[tool.ruff] src` e `known-first-party`. |
| Cobertura 0% ou "module was never imported" | `--cov` com nome/caminho errado | Usar `--cov=src/f1` em `addopts`. |
| `Required test coverage of 50% not reached` ao rodar um único arquivo | O limite vem de `addopts` | Rodar com `--no-cov`. |
| `Config file 'mkdocs.yml' does not exist` | MkDocs procura na raiz | Passar `-f docs/mkdocs.yml`. |
| `mkdocs` não encontrado | Grupo `docs` não instalado | `poetry install --with docs`. |
| Hooks do pre-commit falham com `poetry: command not found` | Poetry fora do `PATH` | Garantir Poetry no `PATH` (instalação via `pipx`). |
| Comando com `\` falha no PowerShell | Continuação de linha diferente | Usar crase (`` ` ``) ou a forma em uma linha. |

