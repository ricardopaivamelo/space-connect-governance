# 🛰️ AgroSat Monitor

**Global Solution 2026.1 — FIAP | Tecnólogo em IA — 2TIAP**

> Sistema IoT de Monitoramento Agrícola Inteligente para a Nova Economia Espacial

---

## 📋 Sobre o Projeto

O **AgroSat Monitor** é uma solução IoT que integra dados de sensores locais (ESP32) com dados simulados de satélites, aplicando IA para apoiar decisões na **agricultura sustentável** — um dos pilares da nova economia espacial.

Satélites como os da constelação Copernicus (ESA) fornecem dados de NDVI (índice de vegetação), cobertura de nuvens e temperatura de superfície. O AgroSat complementa esses dados com sensores de solo, temperatura, umidade e luminosidade, gerando alertas e decisões automatizadas.

---

## 🏗️ Arquitetura

```
[ESP32 + Sensores]
       |
       | MQTT (WiFi)
       ↓
[Mosquitto Broker] ←→ [Node-RED] → [InfluxDB] → [Grafana]
                            |
                            ↓
                      [Telegram Bot]
                            ↑
                    [API Satélite (sim)]
```

### Componentes

| Serviço    | Função                          | Porta |
|------------|----------------------------------|-------|
| Mosquitto  | Broker MQTT                      | 1883  |
| Node-RED   | Orquestrador de fluxos           | 1880  |
| InfluxDB   | Banco de dados time-series       | 8086  |
| Grafana    | Dashboard de visualização        | 3000  |

---

## 🔌 Hardware (Wokwi Simulation)

### Sensores
| Sensor        | GPIO | Função                          |
|---------------|------|---------------------------------|
| DHT22         | D4   | Temperatura e Umidade do Ar     |
| LDR (analóg.) | VP(36)| Luminosidade (%)               |
| Potenciôm. 1  | D35  | Umidade do Solo (simulado)      |
| Potenciôm. 2  | D32  | Sensor de Chuva (simulado)      |

### Atuadores
| Atuador     | GPIO | Função                          |
|-------------|------|---------------------------------|
| LED Vermelho| D2   | Alerta crítico ativo            |
| LED Verde   | D15  | Sistema operando normalmente    |
| LED Azul    | D5   | Conectado ao broker MQTT        |
| Buzzer      | D18  | Alarme sonoro de alerta         |
| LCD I2C     | 21/22| Display local (4 telas rotativas)|

---

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados
- VS Code com extensão Wokwi (para simulação)
- PlatformIO instalado (ou use o Wokwi diretamente)

---

### 1. Subir a Stack Docker

```bash
# Na raiz do projeto
cd docker
docker compose up -d

# Verificar se os containers estão rodando
docker compose ps
```

Aguarde ~30 segundos para todos os serviços inicializarem.

---

### 2. Configurar o Node-RED

1. Acesse: http://localhost:1880
2. Menu hambúrguer → **Import** → **Clipboard**
3. Cole o conteúdo de `nodered-flows/agrosat-flow.json`
4. Clique em **Import** e depois **Deploy**

Instale os nodes necessários (Menu → Manage Palette):
- `node-red-contrib-influxdb`
- `node-red-node-mqtt` (geralmente já vem instalado)

---

### 3. Configurar Telegram Bot

1. Abra o Telegram e pesquise `@BotFather`
2. Envie `/newbot` e siga as instruções
3. Copie o **Token** gerado
4. Pesquise `@userinfobot` e envie qualquer mensagem para obter seu **Chat ID**

No Node-RED, abra o nó **"Enviar Telegram"** e configure:
```javascript
const BOT_TOKEN = 'SEU_TOKEN_AQUI';   // ← substitua
const CHAT_ID   = 'SEU_CHAT_ID_AQUI'; // ← substitua
```

Ou configure como variáveis de ambiente no `docker-compose.yml`:
```yaml
nodered:
  environment:
    - TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
    - TELEGRAM_CHAT_ID=-100123456789
```

---

### 4. Verificar o Grafana

1. Acesse: http://localhost:3000
2. Login: `admin` / `agrosat123`
3. O dashboard **AgroSat Monitor** já estará disponível automaticamente

---

### 5. Simular no Wokwi

#### Opção A — VS Code com PlatformIO
```bash
# Na raiz do projeto
pio run --target upload   # compila e envia para o Wokwi
```
Pressione F1 → `Wokwi: Start Simulator`

#### Opção B — Wokwi Online
1. Acesse https://wokwi.com
2. Crie novo projeto ESP32
3. Substitua o `diagram.json` pelo arquivo deste repositório
4. Cole o conteúdo de `src/main.cpp` no editor
5. Inicie a simulação

> ⚠️ **Para o Wokwi Online**: O broker padrão configurado é `broker.hivemq.com` (público).
> Para usar o broker local Docker, configure `wokwi.toml` com port forwarding e use `host.docker.internal` como endereço.

---

## 📊 Tópicos MQTT

| Tópico              | Direção     | Descrição                         |
|---------------------|-------------|-----------------------------------|
| `agrosat/telemetria`| ESP32 → NR  | Dados completos dos sensores      |
| `agrosat/alertas`   | ESP32 → NR  | Alertas gerados no dispositivo    |
| `agrosat/status`    | ESP32 → NR  | Status de conectividade           |
| `agrosat/comandos`  | NR → ESP32  | Comandos remotos (irrigar, etc.)  |
| `agrosat/satelite`  | NR → ESP32  | Dados simulados de satélite       |

### Exemplo de payload de telemetria
```json
{
  "device_id": "agrosat-esp32-001",
  "timestamp": 12345678,
  "status": "NORMAL",
  "sensores": {
    "temperatura": 27.5,
    "umidade_ar": 65.2,
    "umidade_solo": 42.0,
    "luminosidade": 78.3,
    "chuva": 12.1
  },
  "satelite": {
    "ndvi": 0.72,
    "temp_superficie": 28.5,
    "nuvens": "15%",
    "alerta": "Normal"
  },
  "analise": {
    "necessita_irrigacao": false,
    "risco_geada": false,
    "periodo_noturno": false,
    "alerta_ativo": false
  }
}
```

### Enviar comando remoto (via MQTT)
```json
// Publicar em: agrosat/comandos
{ "comando": "IRRIGAR_ON" }
{ "comando": "IRRIGAR_OFF" }
{ "comando": "STATUS" }
{ "comando": "RESET_ALERTAS" }
```

---

## 🚨 Limites de Alerta

| Parâmetro       | Mínimo | Máximo | Ação                  |
|-----------------|--------|--------|-----------------------|
| Temperatura     | 5°C    | 35°C   | Alerta + Telegram     |
| Umidade do Ar   | 20%    | —      | Alerta seco           |
| Umidade do Solo | 25%    | 85%    | Irrigar / Encharcado  |
| Chuva           | —      | 60%    | Info (não alerta)     |

---

## 🗂️ Estrutura do Projeto

```
agrosat-monitor/
├── src/
│   └── main.cpp              # Código ESP32 principal
├── docker/
│   ├── docker-compose.yml    # Stack IoT completa
│   ├── mosquitto/
│   │   └── config/
│   │       └── mosquitto.conf
│   └── grafana/
│       ├── provisioning/
│       │   ├── datasources/influxdb.yml
│       │   └── dashboards/dashboards.yml
│       └── dashboards/
│           └── agrosat.json  # Dashboard pré-configurado
├── nodered-flows/
│   └── agrosat-flow.json     # Fluxos Node-RED exportados
├── platformio.ini            # Config PlatformIO
├── wokwi.toml               # Config simulador Wokwi
├── diagram.json              # Diagrama de hardware Wokwi
└── README.md
```

---

## 🛰️ Inovação: Integração IoT + Satélite

O diferencial do AgroSat é a **fusão de dados terrestres e espaciais**:

1. **Sensores locais** (ESP32) coletam dados em tempo real do campo
2. **Dados de satélite** (NDVI, temperatura superficial, cobertura de nuvens) são recebidos via MQTT do Node-RED, que pode integrá-los com APIs como a do INPE, Copernicus ou NASA Earthdata
3. A **análise combinada** gera recomendações: ex., se NDVI cai (satélite) + umidade do solo está baixa (sensor) → alerta prioritário de irrigação

---

## 👥 Equipe

**FIAP — Tecnólogo em IA — 2TIAP — 2026**

---

## 📄 Licença

MIT License
