# OpenF1 API — Documentação Resumida

> **Base URL:** `https://api.openf1.org/v1`
> **Autenticação:** Gratuita, sem API key (dados de 2023 em diante)
> **Formato padrão:** JSON (adicione `?csv=true` para CSV)

---

## Parâmetros Globais

| Parâmetro | Descrição |
|---|---|
| `session_key` | Identifica a sessão (ex: `9161`). Use `latest` para a mais recente |
| `meeting_key` | Identifica o fim de semana de corrida |
| `driver_number` | Número do piloto (ex: `44` = Hamilton) |
| `csv=true` | Retorna dados em CSV em vez de JSON |

### Operadores de Filtro

```
=    Igual          ?driver_number=1
>=   Maior ou igual ?speed>=300
<=   Menor ou igual ?lap_number<=20
>    Maior que      ?speed>315
<    Menor que      ?lap_number<5
```

Filtros por data usam ISO 8601: `?date>=2024-03-02T13:00:00`

---

## Endpoints

### 1. Meetings — `/meetings`

Informações sobre fins de semana de corrida (GPs).

**Campos:** `meeting_key`, `meeting_name`, `location`, `country`, `circuit_short_name`, `year`

```bash
curl "https://api.openf1.org/v1/meetings?year=2024"
```

---

### 2. Sessions — `/sessions`

Sessões dentro de um meeting (Treino, Classificação, Sprint, Corrida).

**Campos:** `session_key`, `session_name`, `session_type`, `date_start`, `date_end`, `meeting_key`, `year`

```bash
curl "https://api.openf1.org/v1/sessions?meeting_key=1229&session_name=Race"
```

---

### 3. Drivers — `/drivers`

Pilotos participantes de uma sessão.

**Campos:** `driver_number`, `full_name`, `name_acronym`, `team_name`, `team_colour`, `session_key`

```bash
curl "https://api.openf1.org/v1/drivers?session_key=latest"
```

---

### 4. Laps — `/laps`

Dados volta a volta: tempos, setores e velocidades.

**Campos:** `driver_number`, `lap_number`, `lap_duration`, `duration_sector_1`, `duration_sector_2`, `duration_sector_3`, `st_speed` (speed trap), `is_pit_out_lap`, `session_key`

```bash
curl "https://api.openf1.org/v1/laps?session_key=9161&driver_number=63&lap_number=8"
```

---

### 5. Car Data — `/car_data`

Telemetria de alta frequência (~3.7 Hz): velocidade, RPM, marcha, acelerador, freio, DRS.

**Campos:** `date`, `driver_number`, `speed`, `throttle`, `brake`, `n_gear`, `rpm`, `drs`, `session_key`

```bash
curl "https://api.openf1.org/v1/car_data?session_key=9159&driver_number=55&speed>=315"
```

> ⚠️ **Volume alto de dados** — sempre filtre por `driver_number` e intervalo de `date`.

---

### 6. Location — `/location`

Coordenadas cartesianas (X, Y, Z) dos carros na pista (~3.7 Hz).

**Campos:** `date`, `driver_number`, `x`, `y`, `z`, `session_key`

```bash
curl "https://api.openf1.org/v1/location?session_key=9159&driver_number=1"
```

---

### 7. Intervals — `/intervals`

Gap entre pilotos durante a sessão (intervalo para o líder e para o carro à frente).

**Campos:** `date`, `driver_number`, `gap_to_leader`, `interval`, `session_key`

```bash
curl "https://api.openf1.org/v1/intervals?session_key=9159&driver_number=1"
```

---

### 8. Position — `/position`

Posição dos pilotos na classificação ao longo da sessão.

**Campos:** `date`, `driver_number`, `position`, `session_key`

```bash
curl "https://api.openf1.org/v1/position?session_key=9159&driver_number=1"
```

---

### 9. Stints — `/stints`

Stints de pneus: composto usado, volta de início/fim e idade do pneu.

**Campos:** `session_key`, `driver_number`, `stint_number`, `compound` (`SOFT`, `MEDIUM`, `HARD`, `INTERMEDIATE`, `WET`), `lap_start`, `lap_end`, `tyre_age_at_start`

```bash
curl "https://api.openf1.org/v1/stints?session_key=9159&driver_number=44"
```

---

### 10. Pit — `/pit`

Eventos de pit stop: duração e volta.

**Campos:** `session_key`, `driver_number`, `pit_duration`, `lap_number`, `date`

```bash
curl "https://api.openf1.org/v1/pit?session_key=9159&lap_number=15"
```

---

### 11. Weather — `/weather`

Condições meteorológicas no circuito (atualizado ~1x por minuto).

**Campos:** `session_key`, `date`, `air_temperature`, `track_temperature`, `humidity`, `pressure`, `wind_speed`, `wind_direction`, `rainfall` (0 ou 1)

```bash
curl "https://api.openf1.org/v1/weather?session_key=9159"
```

---

### 12. Race Control — `/race_control`

Mensagens oficiais da direção de prova: bandeiras, safety car, penalidades.

**Campos:** `session_key`, `date`, `category`, `message`, `flag`, `scope`, `lap_number`

```bash
curl "https://api.openf1.org/v1/race_control?session_key=9159&category=SafetyCar"
```

---

### 13. Team Radio — `/team_radio`

Comunicações de rádio entre pilotos e boxes (links para áudio).

**Campos:** `session_key`, `driver_number`, `date`, `recording_url`

```bash
curl "https://api.openf1.org/v1/team_radio?session_key=9159&driver_number=16"
```

---

## Exemplos Rápidos em Python

### Buscar todos os pilotos da sessão mais recente

```python
import requests

url = "https://api.openf1.org/v1/drivers?session_key=latest"
drivers = requests.get(url).json()
for d in drivers:
    print(f"#{d['driver_number']} {d['full_name']} — {d['team_name']}")
```

### Telemetria de velocidade de um piloto

```python
import requests

url = "https://api.openf1.org/v1/car_data"
params = {
    "session_key": 9161,
    "driver_number": 1,
    "speed>=": 300
}
data = requests.get(url, params=params).json()
print(f"{len(data)} amostras com velocidade >= 300 km/h")
```

### Estratégia de pneus de um piloto

```python
import requests

url = "https://api.openf1.org/v1/stints"
params = {"session_key": 9161, "driver_number": 44}
stints = requests.get(url, params=params).json()
for s in stints:
    print(f"Stint {s['stint_number']}: {s['compound']} (voltas {s['lap_start']}-{s['lap_end']})")
```

---

## Dicas de Uso

- Use `session_key=latest` para acessar dados em tempo real durante sessões ao vivo
- Combine filtros para reduzir o volume de dados (especialmente em `/car_data` e `/location`)
- Dados disponíveis a partir da temporada **2023**
- Rate limits aplicados no tier gratuito — evite requisições em loop sem intervalo
- Todos os timestamps são em **UTC**


---

### 3. Drivers — `/drivers`

Pilotos participantes de uma sessão.

**Campos:** `driver_number`, `full_name`, `name_acronym`, `team_name`, `team_colour`, `session_key`

```bash
curl "https://api.openf1.org/v1/drivers?session_key=latest"
```

---

### 4. Laps — `/laps`

Dados volta a volta: tempos, setores e velocidades.

**Campos:** `driver_number`, `lap_number`, `lap_duration`, `duration_sector_1`, `duration_sector_2`, `duration_sector_3`, `st_speed` (speed trap), `is_pit_out_lap`, `session_key`

```bash
curl "https://api.openf1.org/v1/laps?session_key=9161&driver_number=63&lap_number=8"
```

---

### 5. Car Data — `/car_data`

Telemetria de alta frequência (~3.7 Hz): velocidade, RPM, marcha, acelerador, freio, DRS.

**Campos:** `date`, `driver_number`, `speed`, `throttle`, `brake`, `n_gear`, `rpm`, `drs`, `session_key`

```bash
curl "https://api.openf1.org/v1/car_data?session_key=9159&driver_number=55&speed>=315"
```

> ⚠️ **Volume alto de dados** — sempre filtre por `driver_number` e intervalo de `date`.

---

### 6. Location — `/location`

Coordenadas cartesianas (X, Y, Z) dos carros na pista (~3.7 Hz).

**Campos:** `date`, `driver_number`, `x`, `y`, `z`, `session_key`

```bash
curl "https://api.openf1.org/v1/location?session_key=9159&driver_number=1"
```

---

### 7. Intervals — `/intervals`

Gap entre pilotos durante a sessão (intervalo para o líder e para o carro à frente).

**Campos:** `date`, `driver_number`, `gap_to_leader`, `interval`, `session_key`

```bash
curl "https://api.openf1.org/v1/intervals?session_key=9159&driver_number=1"
```

---

### 8. Position — `/position`

Posição dos pilotos na classificação ao longo da sessão.

**Campos:** `date`, `driver_number`, `position`, `session_key`

```bash
curl "https://api.openf1.org/v1/position?session_key=9159&driver_number=1"
```

---

### 9. Stints — `/stints`

Stints de pneus: composto usado, volta de início/fim e idade do pneu.

**Campos:** `session_key`, `driver_number`, `stint_number`, `compound` (`SOFT`, `MEDIUM`, `HARD`, `INTERMEDIATE`, `WET`), `lap_start`, `lap_end`, `tyre_age_at_start`

```bash
curl "https://api.openf1.org/v1/stints?session_key=9159&driver_number=44"
```

---

### 10. Pit — `/pit`

Eventos de pit stop: duração e volta.

**Campos:** `session_key`, `driver_number`, `pit_duration`, `lap_number`, `date`

```bash
curl "https://api.openf1.org/v1/pit?session_key=9159&lap_number=15"
```

---

### 11. Weather — `/weather`

Condições meteorológicas no circuito (atualizado ~1x por minuto).

**Campos:** `session_key`, `date`, `air_temperature`, `track_temperature`, `humidity`, `pressure`, `wind_speed`, `wind_direction`, `rainfall` (0 ou 1)

```bash
curl "https://api.openf1.org/v1/weather?session_key=9159"
```

---

### 12. Race Control — `/race_control`

Mensagens oficiais da direção de prova: bandeiras, safety car, penalidades.

**Campos:** `session_key`, `date`, `category`, `message`, `flag`, `scope`, `lap_number`

```bash
curl "https://api.openf1.org/v1/race_control?session_key=9159&category=SafetyCar"
```

---

### 13. Team Radio — `/team_radio`

Comunicações de rádio entre pilotos e boxes (links para áudio).

**Campos:** `session_key`, `driver_number`, `date`, `recording_url`

```bash
curl "https://api.openf1.org/v1/team_radio?session_key=9159&driver_number=16"
```

---

## Exemplos Rápidos em Python

### Buscar todos os pilotos da sessão mais recente

```python
import requests

url = "https://api.openf1.org/v1/drivers?session_key=latest"
drivers = requests.get(url).json()
for d in drivers:
    print(f"#{d['driver_number']} {d['full_name']} — {d['team_name']}")
```

### Telemetria de velocidade de um piloto

```python
import requests

url = "https://api.openf1.org/v1/car_data"
params = {
    "session_key": 9161,
    "driver_number": 1,
    "speed>=": 300
}
data = requests.get(url, params=params).json()
print(f"{len(data)} amostras com velocidade >= 300 km/h")
```

### Estratégia de pneus de um piloto

```python
import requests

url = "https://api.openf1.org/v1/stints"
params = {"session_key": 9161, "driver_number": 44}
stints = requests.get(url, params=params).json()
for s in stints:
    print(f"Stint {s['stint_number']}: {s['compound']} (voltas {s['lap_start']}-{s['lap_end']})")
```

---

## Dicas de Uso

- Use `session_key=latest` para acessar dados em tempo real durante sessões ao vivo
- Combine filtros para reduzir o volume de dados (especialmente em `/car_data` e `/location`)
- Dados disponíveis a partir da temporada **2023**
- Rate limits aplicados no tier gratuito — evite requisições em loop sem intervalo
- Todos os timestamps são em **UTC**