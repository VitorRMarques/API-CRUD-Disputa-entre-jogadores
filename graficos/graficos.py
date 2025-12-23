import matplotlib.pyplot as plt
import requests
from funcoes.gerais import titulo
from rich.console import Console

console = Console()

url = "http://localhost:3000"

def jogadores_saldo():
    titulo("Grafico - Saldo dos Jogadores")

    try:
        response = requests.get("http://localhost:3000/jogadores?status=a")

        if response.status_code != 200:
            print("Erro ao buscar jogadores")
            return
        
        jogadores = response.json()

        nomes = []
        saldos = []

        for jogador in jogadores:
            nomes.append(jogador.get("nome"))
            saldos.append(float(jogador.get("saldo", 0)))

        plt.figure(figsize=(10,6))
        plt.bar(nomes, saldos)
        plt.title("Saldo dos Jogadores", fontsize=16, weight='bold')
        plt.xlabel("Jogadores", fontsize=12)
        plt.ylabel("Saldo (R$)", fontsize=12)
        plt.xticks(rotation=40, ha="right")
        plt.tight_layout()
        for i, v in enumerate(saldos):
            plt.text(i, v, f"R${v:,.2f}", ha='center', va='bottom', fontsize=10)
        plt.show()
    
    except Exception as e:
        print(f"Erro ao gerar grafico: {e}")

    input("Pressione Enter para continuar...")

def jogadores_idade():
    titulo("Grafico - Idade dos Jogadores")

    try:
        response = requests.get("http://localhost:3000/jogadores?status=a")

        if response.status_code != 200:
            print("Erro ao buscar Jogadores")
            return
        
        jogadores = response.json()

        nomes = []
        idades = []

        for jogador in jogadores:
            nomes.append(jogador.get("nome"))
            idades.append(int(jogador.get("idade", 0)))

        plt.figure(figsize=(10,6))
        plt.bar(nomes, idades)
        plt.title("Idade dos Jogadores", fontsize=16, weight='bold')
        plt.xlabel("Jogadores", fontsize=12)
        plt.ylabel("Idade", fontsize=12)
        plt.xticks(rotation=40, ha="right")
        plt.tight_layout()
        for i, v in enumerate(idades):
            plt.text(i, v, f"{v} anos", ha='center', va='bottom', fontsize=10)
        plt.show()

    except Exception as e:
        print(f"Erro ao gerar grafico: {e}")

    input("Pressione Enter para continuar...")

def jogos_apostas():
    titulo("Grafico - Valor das Apostas dos Jogos")

    try:
        response = requests.get("http://localhost:3000/jogos")

        if response.status_code != 200:
            print("Erro ao buscar Jogos")
            return
        
        jogos = response.json()

        jogos_ids = []
        valores = []

        for j in jogos:
            jogos_ids.append(f"Jogo {j.get('id')}")
            valores.append(float(j.get("valor_aposta", 0)))

        plt.bar(jogos_ids, valores)
        plt.title("Valor das Apostas por Jogo", fontsize=16, weight='bold')
        plt.xlabel("Jogos", fontsize=12)
        plt.ylabel("Valor Apostado (R$)", fontsize=12)
        plt.xticks(rotation=40, ha='right')
        plt.tight_layout()

        for i, v in enumerate(valores):
            plt.text(i, v, f"R${v:,.2f}", ha='center', va='bottom', fontsize=10)

        plt.show()

    except Exception as e:
        print(f"Erro ao gerar grafico: {e}")

    input("Pressione Enter para continuar...")

def grafico_apostas_por_jogador():
    titulo("Gráfico - Apostas Individuais por Jogador")

    try:
        resp_jogos = requests.get(f"{url}/jogos")
        resp_jogadores = requests.get(f"{url}/jogadores")

        if resp_jogos.status_code != 200 or resp_jogadores.status_code != 200:
            console.print("Erro ao buscar dados", style="bold red")
            return

        jogos = resp_jogos.json()
        jogadores = resp_jogadores.json()

        mapa_jogadores = {j["id"]: j["nome"] for j in jogadores}

        labels = []
        valores = []

        for jogo in jogos:
            id_jogo = jogo.get("id")

            j1 = jogo.get("jogador1")
            j2 = jogo.get("jogador2")

            aposta_j1 = float(jogo.get("aposta_j1", 0))
            aposta_j2 = float(jogo.get("aposta_j2", 0))

            if j1:
                nome = mapa_jogadores.get(j1, f"ID {j1}")
                labels.append(f"{nome} (Jogo {id_jogo})")
                valores.append(aposta_j1)

            if j2:
                nome = mapa_jogadores.get(j2, f"ID {j2}")
                labels.append(f"{nome} (Jogo {id_jogo})")
                valores.append(aposta_j2)

        import matplotlib.pyplot as plt

        plt.figure(figsize=(14,7))
        plt.bar(labels, valores)
        plt.title("Apostas Individuais realizadas por Jogador", fontsize=15, weight="bold")
        plt.xlabel("Jogador / Jogo")
        plt.ylabel("Valor Apostado (R$)")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        plt.tight_layout()

        for i, v in enumerate(valores):
            plt.text(i, v, f"R$ {v:,.2f}", ha='center', va='bottom', fontsize=9)

        plt.show()

    except Exception as e:
        console.print(f"Erro ao gerar gráfico: {e}", style="bold red")

    input("Pressione Enter para continuar...")




