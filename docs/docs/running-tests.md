# Como Rodar Testes e Qualidade

O projeto utiliza o **taskipy** para simplificar comandos frequentes de testes, lint, formatação e build de documentação.

## Comandos Rápidos (`poetry run task`)

| Comando | Descrição |
| --- | --- |
| `poetry run task test` | Executa os testes unitários via Pytest com verificação de cobertura (mínimo 50%). |
| `poetry run task lint` | Checa padrões de código com Ruff (linter e formatação). |
| `poetry run task format` | Formata automaticamente o código e corrige problemas de import com Ruff. |
| `poetry run task docs` | Realiza o build de validação da documentação MkDocs com `--strict`. |
| `poetry run task docs-serve` | Inicia o servidor local de documentação com recarregamento em tempo real. |

---

## Testes Unitários e Cobertura

Os testes estão localizados em `tests/unit/` e rodam com isolamento total (sem I/O ou chamadas de rede externas):

```bash
poetry run task test
```

### Relatório HTML de Cobertura
Para gerar um relatório visual navegável da cobertura:

```bash
poetry run pytest tests/unit/ --cov-report=html
```
O relatório será gerado na pasta `htmlcov/index.html`.

