# Estrutura do Projeto

A organização de pastas segue rigorosamente as especificações do `SKILL.md`:

```text
F1/
├── .python-version            # Versão do interpretador Python (3.12.10)
├── .gitignore                 # Arquivos ignorados no versionamento
├── .env.example               # Exemplo de variáveis de ambiente
├── pyproject.toml             # Metadados, dependências e configurações de ferramentas
├── poetry.lock                # Lockfile de dependências determinístico
├── README.md                  # Apresentação rápida do repositório
├── src/
│   └── f1/                    # Pacote raiz da aplicação
│       ├── __init__.py
│       ├── domain/            # Modelos, contratos ABC e serviços
│       │   ├── models.py
│       │   ├── repositories.py
│       │   └── services.py
│       ├── ingestion/         # Clientes de rede e repositórios OpenF1 concretos
│       │   ├── http_client.py
│       │   └── openf1_repositories.py
│       ├── processing/        # Transformações puras, estatísticas e filtros
│       │   ├── formatting.py
│       │   ├── laps.py
│       │   ├── results.py
│       │   ├── stints.py
│       │   └── weather.py
│       ├── dashboard/         # Camada de apresentação Streamlit
│       │   ├── app.py
│       │   ├── charts.py
│       │   └── components.py
│       └── utils/             # Configuração e logging transversal
│           ├── config.py
│           └── logger.py
├── tests/
│   ├── conftest.py
│   ├── unit/                  # Testes unitários isolados
│   │   ├── test_charts.py
│   │   ├── test_config.py
│   │   ├── test_formatting.py
│   │   ├── test_http_client.py
│   │   ├── test_logger.py
│   │   ├── test_models.py
│   │   ├── test_processing_laps.py
│   │   └── test_processing_other.py
│   └── integration/           # Testes de integração com a API real
└── docs/                      # Documentação técnica com MkDocs Material
    ├── mkdocs.yml
    └── docs/
        ├── index.md
        ├── architecture.md
        ├── project-structure.md
        ├── running-locally.md
        ├── running-tests.md
        └── contributing.md
```

