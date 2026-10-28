# Como Executar Localmente

Siga o passo a passo abaixo para rodar o projeto em seu ambiente local.

## Pré-requisitos

1. **Python 3.12.10** (gerenciado preferencialmente com `pyenv` ou instalado no sistema).
2. **Poetry ≥ 2.0**.

---

## 1. Instalação das Dependências

Clone o repositório e navegue até a pasta:

```bash
cd F1
```

Instale as dependências com o Poetry (incluindo grupos de desenvolvimento e documentação):

```bash
poetry install --with docs
```

---

## 2. Configuração de Variáveis de Ambiente

Crie o arquivo `.env` a partir do modelo disponível:

```bash
cp .env.example .env
```

Conteúdo padrão do `.env`:
```ini
OPENF1_BASE_URL=https://api.openf1.org/v1
OPENF1_TIMEOUT=10
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## 3. Executando o Dashboard Streamlit

Para iniciar o painel interativo:

```bash
poetry run streamlit run src/f1/dashboard/app.py
```

Acesse no seu navegador: `http://localhost:8501`.

