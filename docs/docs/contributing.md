# Como Contribuir

Agradecemos o interesse em contribuir com o **F1 Dashboard**! Para garantir a qualidade e a padronização do código, siga as diretrizes abaixo.

## Padrões de Desenvolvimento

- **Type Hints**: Todas as funções, métodos e atributos de classes públicas devem conter anotações de tipos completas (PEP 484).
- **Docstrings**: Formato Google nas funções e classes públicas.
- **Logging**: Utilize sempre `get_logger(__name__)` em vez de `print()`.
- **Pureza Funcional**: Novas regras de negócio e agregações devem ser implementadas como funções puras na camada `src/f1/processing/`.

---

## Checklist de Validação Obrigatória

Antes de abrir um Pull Request, certifique-se de que todos os comandos abaixo foram executados e passaram com código de retorno 0:

```bash
# 1. Checar lint e formatação
poetry run task lint

# 2. Executar testes e atingir cobertura >= 50%
poetry run task test

# 3. Validar build da documentação sem links quebrados
poetry run task docs
```

Após todas as validações estarem 100% verdes, seu Pull Request estará pronto para revisão!

