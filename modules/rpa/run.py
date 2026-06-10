"""
run.py
======
Ponto de entrada do robô MissionOps RPA.

Uso:
    python run.py

Lê os arquivos da pasta inbox/, processa tudo e gera os artefatos na
pasta outputs/. Um resumo é impresso no final.
"""

from robo import executar


def main():
    relatorio = executar()
    est = relatorio["estatisticas"]

    print("\n" + "=" * 50)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 50)
    print(f"Arquivos reconhecidos : {est['total_arquivos']}")
    print(f"Processados com sucesso: {est['total_processados']}")
    print(f"Falhas (tratadas)     : {est['total_falhas']}")
    print(f"Telemetrias críticas  : {est['telemetria_criticas']}")
    print(f"Docs críticos/alerta  : {est['documentos_criticos']}")
    print(f"Imagens anômalas      : {est['imagens_anomalas']}")
    print(f"Duração               : {relatorio['duracao_segundos']}s")
    print("\nArtefatos gerados:")
    for nome, caminho in relatorio["artefatos"].items():
        print(f"  - {nome}: {caminho}")
    print("\nVeja o log completo em logs/execucao.log")


if __name__ == "__main__":
    main()
