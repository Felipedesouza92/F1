# Arquitetura do Sistema

O projeto adota uma arquitetura em camadas bem definida, orientada a contratos e com inversão de controle / injeção de dependências.

```text
dashboard → domain.services → (domain.repositories, processing) → domain.models
                                        ↑
                                   ingestion (implementa os contratos)
```

## Camadas

### 1. `domain` (Núcleo)
- **Modelos (`models.py`)**: Entidades e projeções tipadas com validação Pydantic v2.
- **Repositórios (`repositories.py`)**: Interfaces abstratas (ABCs) para cada endpoint da OpenF1.
- **Serviços (`services.py`)**: Orquestrador de regras de negócio (`F1DashboardService`).
- **Regra de Ouro**: A camada de domínio **nunca** importa bibliotecas externas de I/O (`httpx`, `streamlit`) nem camadas superiores.

### 2. `processing` (Funções Puras)
- Transformações determinísticas sem efeitos colaterais ou chamadas de I/O:
  - `laps.py`: Filtragem de voltas válidas, cálculo de top N e ritmos.
  - `stints.py`: Agrupamento e projeção de stints e pit stops.
  - `results.py`: Classificação e estados de corrida.
  - `weather.py`: Resumo e agregação das medições meteorológicas.
  - `formatting.py`: Cores das equipes e conversão de tempos (`83.456` → `1:23.456`).

### 3. `ingestion` (Fontes e I/O Externo)
- **`http_client.py`**: Cliente HTTP resiliente com retries exponenciais, timeout e tratamento de 429/5xx.
- **`openf1_repositories.py`**: Implementações concretas das interfaces ABCs do domínio.

### 4. `dashboard` (Apresentação Streamlit)
- `app.py`: Ponto de entrada (composition root) da aplicação.
- `charts.py`: Criação das figuras interativas com Plotly em tema escuro.
- `components.py`: Componentes modulares de UI (cards, métricas, pódio).

### 5. `utils` (Transversal)
- `config.py`: Gerenciamento centralizado de configurações por ambiente (`Settings`).
- `logger.py`: Configuração padronizada do logger do sistema.

