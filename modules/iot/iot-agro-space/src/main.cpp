/**
 * ============================================================
 * AgroSat Monitor - Global Solution 2026.1
 * FIAP - Tecnólogo em IA - 2TIAP
 * ============================================================
 * 
 * Sistema de Monitoramento Agrícola Inteligente para a
 * Nova Economia Espacial
 * 
 * Sensores:
 *   - DHT22     → Temperatura e Umidade do Ar (GPIO 4)
 *   - LDR       → Luminosidade Analógica (GPIO 36/VP)
 *   - Potenc.1  → Umidade do Solo Simulada (GPIO 35)
 *   - Potenc.2  → Sensor de Chuva Simulado (GPIO 32)
 * 
 * Atuadores:
 *   - LED Vermelho  → Alerta crítico (GPIO 2)
 *   - LED Verde     → Sistema OK (GPIO 15)
 *   - LED Azul      → Conectado ao MQTT (GPIO 5)
 *   - Buzzer        → Alarme sonoro (GPIO 18)
 *   - LCD I2C       → Display local (SDA=21, SCL=22)
 * 
 * Protocolo: MQTT sobre WiFi → Node-RED → InfluxDB → Grafana
 * Alertas: Telegram via Node-RED
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ─────────────────────────────────────────
// CONFIGURAÇÕES DE REDE E MQTT
// ─────────────────────────────────────────
#define WIFI_SSID     "Wokwi-GUEST"
#define WIFI_PASSWORD ""

// Broker público para testes no Wokwi
// Em produção: substitua pelo IP do seu broker local (docker)
#define MQTT_BROKER   "host.docker.internal"
#define MQTT_PORT     1884
#define MQTT_CLIENT_ID "agrosat-esp32-001"

// Para broker local com autenticação:
// #define MQTT_USER   "agrosat"
// #define MQTT_PASS   "agrosat123"

// ─────────────────────────────────────────
// TÓPICOS MQTT
// ─────────────────────────────────────────
#define TOPIC_TELEMETRY   "agrosat/telemetria"
#define TOPIC_ALERT       "agrosat/alertas"
#define TOPIC_STATUS      "agrosat/status"
#define TOPIC_CMD         "agrosat/comandos"   // recebe comandos remotos
#define TOPIC_SATELLITE   "agrosat/satelite"   // dados simulados de satélite

// ─────────────────────────────────────────
// PINOS
// ─────────────────────────────────────────
#define PIN_DHT       4
#define PIN_LDR_AO    36   // VP - analógico LDR
#define PIN_SOLO      35   // potenciômetro umidade solo
#define PIN_CHUVA     32   // potenciômetro sensor chuva

#define PIN_LED_RED   2
#define PIN_LED_GREEN 15
#define PIN_LED_BLUE  5
#define PIN_BUZZER    18

#define DHT_TYPE      DHT22

// ─────────────────────────────────────────
// LIMITES DE ALERTAS
// ─────────────────────────────────────────
#define TEMP_MAX        35.0   // °C - temperatura crítica
#define TEMP_MIN        5.0    // °C - geada
#define UMID_AR_MIN     20.0   // % - muito seco
#define UMID_SOLO_MIN   25.0   // % - solo muito seco (irrigar)
#define UMID_SOLO_MAX   85.0   // % - solo encharcado
#define LDR_NOITE       15.0   // % - nível de luz noturno
#define CHUVA_THRESHOLD 60.0   // % - chuva detectada

// ─────────────────────────────────────────
// INTERVALOS
// ─────────────────────────────────────────
#define INTERVALO_LEITURA   5000    // ms entre leituras
#define INTERVALO_MQTT      10000   // ms entre publicações MQTT
#define INTERVALO_LCD       3000    // ms troca de tela LCD

// ─────────────────────────────────────────
// INSTÂNCIAS
// ─────────────────────────────────────────
DHT dht(PIN_DHT, DHT_TYPE);
WiFiClient espClient;
PubSubClient mqttClient(espClient);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ─────────────────────────────────────────
// VARIÁVEIS GLOBAIS
// ─────────────────────────────────────────
struct Telemetria {
  float temperatura;
  float umidadeAr;
  float umidadeSolo;
  float luminosidade;
  float chuva;
  bool  alertaAtivo;
  String statusSistema;
  unsigned long timestamp;
};

Telemetria dados;
unsigned long ultimaLeitura   = 0;
unsigned long ultimoMQTT      = 0;
unsigned long ultimoLCD       = 0;
int telaLCD = 0;
bool mqttConectado = false;

// Dados simulados de satélite (em produção viria de API)
struct DadosSatelite {
  float ndvi;          // Índice de vegetação
  float temperatura;   // Temperatura superfície
  String coberturaNuvem;
  String alertaClimatico;
};
DadosSatelite satelite = { 0.72, 28.5, "15%", "Normal" };

// ─────────────────────────────────────────
// PROTÓTIPOS
// ─────────────────────────────────────────
void conectarWiFi();
void conectarMQTT();
void callbackMQTT(char* topic, byte* payload, unsigned int length);
void lerSensores();
void analisarAlertas();
void publicarTelemetria();
void publicarAlerta(String mensagem, String nivel);
void atualizarAtuadores();
void atualizarLCD();
void bip(int frequencia, int duracao);
String gerarPayloadTelemetria();
float mapAnalogico(int valor, float minOut, float maxOut);

// ─────────────────────────────────────────
// SETUP
// ─────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Serial.println("\n╔══════════════════════════════╗");
  Serial.println("║  AgroSat Monitor v1.0        ║");
  Serial.println("║  FIAP GS 2026.1              ║");
  Serial.println("╚══════════════════════════════╝\n");

  // Pinos de saída
  pinMode(PIN_LED_RED,   OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_BLUE,  OUTPUT);
  pinMode(PIN_BUZZER,    OUTPUT);

  // Pinos de entrada analógica
  pinMode(PIN_LDR_AO, INPUT);
  pinMode(PIN_SOLO,   INPUT);
  pinMode(PIN_CHUVA,  INPUT);

  // Inicializar LCD
  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("AgroSat Monitor");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");

  // Inicializar DHT22
  dht.begin();

  // LEDs de boot
  digitalWrite(PIN_LED_RED,   HIGH);
  digitalWrite(PIN_LED_GREEN, HIGH);
  digitalWrite(PIN_LED_BLUE,  HIGH);
  delay(500);
  digitalWrite(PIN_LED_RED,   LOW);
  digitalWrite(PIN_LED_GREEN, LOW);
  digitalWrite(PIN_LED_BLUE,  LOW);

  // Conectar WiFi
  conectarWiFi();

  // Configurar MQTT
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(callbackMQTT);
  mqttClient.setKeepAlive(60);
  mqttClient.setBufferSize(512);

  // Conectar MQTT
  conectarMQTT();

  // Primeira leitura
  lerSensores();
  analisarAlertas();
  atualizarAtuadores();
  atualizarLCD();

  bip(1000, 200);
  Serial.println("[SISTEMA] Inicialização completa!\n");
}

// ─────────────────────────────────────────
// LOOP PRINCIPAL
// ─────────────────────────────────────────
void loop() {
  unsigned long agora = millis();

  // Manter conexão MQTT
  if (!mqttClient.connected()) {
    mqttConectado = false;
    digitalWrite(PIN_LED_BLUE, LOW);
    conectarMQTT();
  }
  mqttClient.loop();

  // Leitura periódica dos sensores
  if (agora - ultimaLeitura >= INTERVALO_LEITURA) {
    ultimaLeitura = agora;
    lerSensores();
    analisarAlertas();
    atualizarAtuadores();
  }

  // Publicação MQTT periódica
  if (agora - ultimoMQTT >= INTERVALO_MQTT) {
    ultimoMQTT = agora;
    publicarTelemetria();
  }

  // Atualizar LCD periodicamente
  if (agora - ultimoLCD >= INTERVALO_LCD) {
    ultimoLCD = agora;
    atualizarLCD();
  }
}

// ─────────────────────────────────────────
// CONEXÃO WiFi
// ─────────────────────────────────────────
void conectarWiFi() {
  Serial.print("[WiFi] Conectando a ");
  Serial.println(WIFI_SSID);
  lcd.setCursor(0, 1);
  lcd.print("Conectando WiFi ");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] Conectado!");
    Serial.print("[WiFi] IP: ");
    Serial.println(WiFi.localIP());
    lcd.setCursor(0, 1);
    lcd.print("WiFi OK!        ");
    digitalWrite(PIN_LED_GREEN, HIGH);
    delay(1000);
    digitalWrite(PIN_LED_GREEN, LOW);
  } else {
    Serial.println("\n[WiFi] FALHA na conexão!");
    lcd.setCursor(0, 1);
    lcd.print("WiFi ERRO!      ");
    // Modo offline: continua funcionando localmente
  }
}

// ─────────────────────────────────────────
// CONEXÃO MQTT
// ─────────────────────────────────────────
void conectarMQTT() {
  int tentativas = 0;
  while (!mqttClient.connected() && tentativas < 3) {
    Serial.print("[MQTT] Conectando ao broker...");

    bool conectado = mqttClient.connect(
      MQTT_CLIENT_ID
      // MQTT_USER, MQTT_PASS  // descomente para broker autenticado
    );

    if (conectado) {
      Serial.println(" OK!");
      mqttConectado = true;
      digitalWrite(PIN_LED_BLUE, HIGH);

      // Inscrever-se no tópico de comandos remotos
      mqttClient.subscribe(TOPIC_CMD);
      mqttClient.subscribe(TOPIC_SATELLITE);

      // Publicar status online
      JsonDocument statusDoc;
      statusDoc["device"]  = MQTT_CLIENT_ID;
      statusDoc["status"]  = "online";
      statusDoc["versao"]  = "1.0.0";
      char statusBuf[128];
      serializeJson(statusDoc, statusBuf);
      mqttClient.publish(TOPIC_STATUS, statusBuf, true); // retain=true

    } else {
      Serial.print(" Falha, rc=");
      Serial.println(mqttClient.state());
      tentativas++;
      delay(3000);
    }
  }
}

// ─────────────────────────────────────────
// CALLBACK MQTT (recebe comandos)
// ─────────────────────────────────────────
void callbackMQTT(char* topic, byte* payload, unsigned int length) {
  String topico = String(topic);
  String msg = "";
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  Serial.print("[MQTT] Mensagem recebida [");
  Serial.print(topico);
  Serial.print("]: ");
  Serial.println(msg);

  // Processar comandos remotos
  if (topico == TOPIC_CMD) {
    JsonDocument doc;
    DeserializationError err = deserializeJson(doc, msg);
    if (!err) {
      String cmd = doc["comando"] | "";

      if (cmd == "IRRIGAR_ON") {
        Serial.println("[CMD] Irrigação ativada remotamente!");
        bip(800, 300);
        lcd.setCursor(0, 1);
        lcd.print("IRRIGAR: ON     ");
      }
      else if (cmd == "IRRIGAR_OFF") {
        Serial.println("[CMD] Irrigação desativada remotamente!");
        lcd.setCursor(0, 1);
        lcd.print("IRRIGAR: OFF    ");
      }
      else if (cmd == "STATUS") {
        publicarTelemetria();
      }
      else if (cmd == "RESET_ALERTAS") {
        dados.alertaAtivo = false;
        digitalWrite(PIN_LED_RED, LOW);
        noTone(PIN_BUZZER);
        Serial.println("[CMD] Alertas resetados remotamente!");
      }
    }
  }

  // Dados de satélite recebidos via MQTT
  if (topico == TOPIC_SATELLITE) {
    JsonDocument doc;
    DeserializationError err = deserializeJson(doc, msg);
    if (!err) {
      satelite.ndvi            = doc["ndvi"]              | satelite.ndvi;
      satelite.temperatura     = doc["temp_superficie"]   | satelite.temperatura;
      satelite.coberturaNuvem  = doc["nuvens"].as<String>();
      satelite.alertaClimatico = doc["alerta"].as<String>();
      Serial.println("[SAT] Dados de satélite atualizados!");
    }
  }
}

// ─────────────────────────────────────────
// LEITURA DOS SENSORES
// ─────────────────────────────────────────
void lerSensores() {
  // DHT22 - Temperatura e Umidade do Ar
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (!isnan(t)) dados.temperatura = t;
  if (!isnan(h)) dados.umidadeAr   = h;

  // LDR - Luminosidade (0-4095 → 0-100%)
  int ldrRaw = analogRead(PIN_LDR_AO);
  dados.luminosidade = mapAnalogico(ldrRaw, 0, 100);

  // Potenciômetro 1 - Umidade do Solo (0-4095 → 0-100%)
  int soloRaw = analogRead(PIN_SOLO);
  dados.umidadeSolo = mapAnalogico(soloRaw, 0, 100);

  // Potenciômetro 2 - Sensor de Chuva (0-4095 → 0-100%)
  int chuvaRaw = analogRead(PIN_CHUVA);
  dados.chuva = mapAnalogico(chuvaRaw, 0, 100);

  dados.timestamp = millis();

  // Log serial
  Serial.println("┌─────────────────────────────┐");
  Serial.printf("│ Temp:       %.1f °C          \n", dados.temperatura);
  Serial.printf("│ Umid. Ar:   %.1f %%          \n", dados.umidadeAr);
  Serial.printf("│ Solo:       %.1f %%          \n", dados.umidadeSolo);
  Serial.printf("│ Luz:        %.1f %%          \n", dados.luminosidade);
  Serial.printf("│ Chuva:      %.1f %%          \n", dados.chuva);
  Serial.printf("│ NDVI Sat:   %.2f             \n", satelite.ndvi);
  Serial.println("└─────────────────────────────┘");
}

// ─────────────────────────────────────────
// ANÁLISE DE ALERTAS
// ─────────────────────────────────────────
void analisarAlertas() {
  String alertas = "";
  dados.alertaAtivo = false;

  if (dados.temperatura >= TEMP_MAX) {
    alertas += "CALOR_CRITICO;";
    dados.alertaAtivo = true;
  }
  if (dados.temperatura <= TEMP_MIN) {
    alertas += "GEADA_RISCO;";
    dados.alertaAtivo = true;
  }
  if (dados.umidadeAr <= UMID_AR_MIN) {
    alertas += "AR_MUITO_SECO;";
    dados.alertaAtivo = true;
  }
  if (dados.umidadeSolo <= UMID_SOLO_MIN) {
    alertas += "IRRIGAR_URGENTE;";
    dados.alertaAtivo = true;
  }
  if (dados.umidadeSolo >= UMID_SOLO_MAX) {
    alertas += "SOLO_ENCHARCADO;";
    dados.alertaAtivo = true;
  }
  if (dados.chuva >= CHUVA_THRESHOLD) {
    alertas += "CHUVA_DETECTADA;";
  }
  if (satelite.alertaClimatico != "Normal" && satelite.alertaClimatico != "") {
    alertas += "ALERTA_SAT:" + satelite.alertaClimatico + ";";
    dados.alertaAtivo = true;
  }

  // Determinar status geral
  if (dados.alertaAtivo) {
    dados.statusSistema = "ALERTA";
    publicarAlerta(alertas, "CRITICO");
  } else if (dados.chuva >= CHUVA_THRESHOLD) {
    dados.statusSistema = "CHUVA";
  } else if (dados.luminosidade <= LDR_NOITE) {
    dados.statusSistema = "NOITE";
  } else {
    dados.statusSistema = "NORMAL";
  }
}

// ─────────────────────────────────────────
// ATUALIZAR ATUADORES
// ─────────────────────────────────────────
void atualizarAtuadores() {
  if (dados.alertaAtivo) {
    digitalWrite(PIN_LED_RED,   HIGH);
    digitalWrite(PIN_LED_GREEN, LOW);
    // Buzzer pulsante para alertas críticos
    tone(PIN_BUZZER, 1000, 200);
  } else {
    digitalWrite(PIN_LED_RED,   LOW);
    digitalWrite(PIN_LED_GREEN, HIGH);
    noTone(PIN_BUZZER);
  }

  // LED Azul indica conexão MQTT
  digitalWrite(PIN_LED_BLUE, mqttConectado ? HIGH : LOW);
}

// ─────────────────────────────────────────
// PUBLICAR TELEMETRIA VIA MQTT
// ─────────────────────────────────────────
void publicarTelemetria() {
  if (!mqttClient.connected()) return;

  JsonDocument doc;

  // Dados do dispositivo
  doc["device_id"]    = MQTT_CLIENT_ID;
  doc["timestamp"]    = dados.timestamp;
  doc["status"]       = dados.statusSistema;

  // Sensores locais
  JsonObject sensores = doc.createNestedObject("sensores");
  sensores["temperatura"]  = round(dados.temperatura * 10) / 10.0;
  sensores["umidade_ar"]   = round(dados.umidadeAr   * 10) / 10.0;
  sensores["umidade_solo"] = round(dados.umidadeSolo * 10) / 10.0;
  sensores["luminosidade"] = round(dados.luminosidade * 10) / 10.0;
  sensores["chuva"]        = round(dados.chuva       * 10) / 10.0;

  // Dados de satélite integrados
  JsonObject sat = doc.createNestedObject("satelite");
  sat["ndvi"]            = satelite.ndvi;
  sat["temp_superficie"] = satelite.temperatura;
  sat["nuvens"]          = satelite.coberturaNuvem;
  sat["alerta"]          = satelite.alertaClimatico;

  // Análise integrada IoT + Satélite
  JsonObject analise = doc.createNestedObject("analise");
  analise["necessita_irrigacao"] = (dados.umidadeSolo < UMID_SOLO_MIN && dados.chuva < CHUVA_THRESHOLD);
  analise["risco_geada"]         = (dados.temperatura < TEMP_MIN);
  analise["periodo_noturno"]     = (dados.luminosidade < LDR_NOITE);
  analise["alerta_ativo"]        = dados.alertaAtivo;

  char payload[512];
  serializeJson(doc, payload);

  bool sucesso = mqttClient.publish(TOPIC_TELEMETRY, payload);
  if (sucesso) {
    Serial.println("[MQTT] Telemetria publicada com sucesso!");
  } else {
    Serial.println("[MQTT] ERRO ao publicar telemetria!");
  }
}

// ─────────────────────────────────────────
// PUBLICAR ALERTA
// ─────────────────────────────────────────
void publicarAlerta(String mensagem, String nivel) {
  if (!mqttClient.connected()) return;

  // Evitar spam de alertas (publicar só uma vez por leitura)
  static String ultimoAlerta = "";
  if (mensagem == ultimoAlerta) return;
  ultimoAlerta = mensagem;

  JsonDocument doc;
  doc["device_id"] = MQTT_CLIENT_ID;
  doc["nivel"]     = nivel;
  doc["alertas"]   = mensagem;
  doc["timestamp"] = dados.timestamp;

  char payload[256];
  serializeJson(doc, payload);

  mqttClient.publish(TOPIC_ALERT, payload);
  Serial.print("[ALERTA] Publicado: ");
  Serial.println(mensagem);
}

// ─────────────────────────────────────────
// ATUALIZAR LCD
// ─────────────────────────────────────────
void atualizarLCD() {
  lcd.clear();
  switch (telaLCD) {
    case 0: // Temperatura e Umidade Ar
      lcd.setCursor(0, 0);
      lcd.print("Temp: ");
      lcd.print(dados.temperatura, 1);
      lcd.print(" C");
      lcd.setCursor(0, 1);
      lcd.print("Umid: ");
      lcd.print(dados.umidadeAr, 1);
      lcd.print(" %");
      break;
    case 1: // Solo e Chuva
      lcd.setCursor(0, 0);
      lcd.print("Solo: ");
      lcd.print(dados.umidadeSolo, 1);
      lcd.print(" %");
      lcd.setCursor(0, 1);
      lcd.print("Chuva:");
      lcd.print(dados.chuva, 1);
      lcd.print(" %");
      break;
    case 2: // Luminosidade e Status
      lcd.setCursor(0, 0);
      lcd.print("Luz:  ");
      lcd.print(dados.luminosidade, 1);
      lcd.print(" %");
      lcd.setCursor(0, 1);
      lcd.print("Status:");
      lcd.print(dados.statusSistema);
      break;
    case 3: // Dados do Satélite
      lcd.setCursor(0, 0);
      lcd.print("NDVI:");
      lcd.print(satelite.ndvi, 2);
      lcd.print(" SAT");
      lcd.setCursor(0, 1);
      lcd.print("Nuvens:");
      lcd.print(satelite.coberturaNuvem);
      break;
  }
  telaLCD = (telaLCD + 1) % 4;
}

// ─────────────────────────────────────────
// UTILITÁRIOS
// ─────────────────────────────────────────
float mapAnalogico(int valor, float minOut, float maxOut) {
  return (valor / 4095.0) * (maxOut - minOut) + minOut;
}

void bip(int frequencia, int duracao) {
  tone(PIN_BUZZER, frequencia, duracao);
  delay(duracao + 50);
  noTone(PIN_BUZZER);
}
