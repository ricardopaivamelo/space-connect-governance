# Correções aplicadas em 09/06/2026 (equipe de integração GBA)

1. **docker/docker-compose.yml — caminhos relativos corrigidos.** O arquivo
   referenciava `./docker/grafana/...`, `./docker/mosquitto/config` e
   `./nodered-flows`, caminhos que não existem relativos à pasta `docker/`
   onde o compose está. Com isso, o Grafana subia **sem** datasource e sem
   dashboard provisionados. Corrigido para `./grafana/...`,
   `./mosquitto/config` e `../nodered-flows`; a pasta duplicada
   `docker/docker/` foi removida. Validação: `docker compose config` OK e
   todos os arquivos referenciados existem.

2. **Observação não corrigida (decisão do autor):** o firmware usa o broker
   `host.docker.internal:1884` (src/main.cpp), enquanto o README cita
   `broker.hivemq.com`. `host.docker.internal` não resolve em Linux nem no
   Wokwi online sem gateway configurado — para demonstrar, usar o IP da
   máquina na rede local ou o gateway IoT do Wokwi.

3. **Observação:** as credenciais no docker-compose (InfluxDB/Grafana) são de
   stack local de desenvolvimento, sem acesso externo; recomenda-se movê-las
   para um arquivo `.env` (o `.gitignore` do projeto já o prevê).

4. **Pendência da disciplina:** o enunciado exige vídeo pitch de até 5 min
   mostrando as medições atualizando na plataforma — não incluído no pacote.
