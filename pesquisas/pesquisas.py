import requests
from rich.console import Console
from rich.table import Table 
from rich.prompt import Prompt
from funcoes.gerais import titulo
from datetime import datetime

console = Console()
url = "http://localhost:3000"

def pesq_jogadores():
    titulo("Pesquisa de Jogadores por Intervalo de Saldo")

    saldo_min = Prompt.ask("Valor minimo", default="0")
    saldo_max = Prompt.ask("Valor maximo", default="0")

    try:
        saldo_min = float(saldo_min)
        saldo_max = float(saldo_max)

        response = requests.get(f"{url}/jogadores?status=a")

        if response.status_code != 200:
            console.print("Erro ao buscar jogadores.", style="bold red")
            return
        
        jogadores = response.json()

        jogadores_filtrados = [
            j for j in jogadores
            if saldo_min <= float(j.get("saldo", 0)) <= saldo_max
        ]

        if not jogadores_filtrados:
            console.print("Nenhum jogador encontrado nesse intervalo de saldo.")
            input("Pressione Enter para continuar...")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Nome")
        table.add_column("Idade")
        table.add_column("Saldo", justify="right")
        table.add_column("Detalhes")

        for j in jogadores_filtrados:
            saldo_f = f"{float(j.get('saldo', 0)):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            table.add_row(
                str(j.get("id")),
                j.get("nome", ""),
                j.get("idade", ""),
                f"R$ {saldo_f}",
                j.get("detalhes", "")
            )

            console.print(table)

    except ValueError:
        console.print("Informe valores numericos validos", style="bold red")
    except Exception as e:
        console.print(f"Erro na pesquisa: {e}", style="bold red")

    input("Pressione Enter para continuar...")

def pesq_jogos_aposta():
    titulo("Pesquisa de Jogos por Valor de Apostas")

    valor_min = Prompt.ask("Valor minimo R$", default="0")
    valor_max = Prompt.ask("Valor maximo R$", default="0")

    try:
        valor_min = float(valor_min)
        valor_max = float(valor_max)

        response = requests.get(f"{url}/jogos")

        if response.status_code != 200:
            console.print("Erro ao buscar jogos.", style="bold red")
            return
        
        jogos = response.json()

        jogos_filtrados = [
            j for j in jogos
            if valor_min <= float(j.get("valor_aposta", 0)) <= valor_max
        ]

        if not jogos_filtrados:
            console.print("Nenhum jogo encontrado nesse intervalo de apostas.")
            input("Pressione Enter para continuar...")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID Jogo", style="dim")
        table.add_column("Jogador 1")
        table.add_column("Jogador 2")
        table.add_column("Valor Aposta", justify="right")

        for jogo in jogos_filtrados:
            valor_f = f"{float(jogo.get('valor_aposta', 0)):,.2f}".replace(",","X").replace(".",",").replace("X", ".")

            table.add_row(
                str(jogo.get("id")),
                str(jogo.get("jogador1")),
                str(jogo.get("jogador2")),
                f"R$ {valor_f}"
            )
        console.print(table)

    except ValueError:
        console.print("Informe valores numericos validos!", style="bold red")
    except Exception as e:
        console.print(f"Erro na pesquisa: {e}", style="bold red")

    input("Pressione Enter para continuar...")

def pesq_idades():
    titulo("Pesquisa de Jogadores por Intervalo de Idade")

    idade_min = Prompt.ask("Idade mínima", default="0")
    idade_max = Prompt.ask("Idade máxima", default="0")

    try:
        idade_min = int(idade_min)
        idade_max = int(idade_max)

        response = requests.get(f"{url}/jogadores?status=a")

        if response.status_code != 200:
            console.print("Erro ao buscar jogadores", style="bold red")
            return
        
        jogadores = response.json()

        jogadores_filtrados = [
            j for j in jogadores
            if idade_min <= int(j.get("idade", 0)) <= idade_max
        ]

        if not jogadores_filtrados:
            console.print("Nenhum jogador encontrado nesse intervalo de idade.")
            input("Pressione Enter para continuar...")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Nome")
        table.add_column("Idade")
        table.add_column("Saldo", justify="right")
        table.add_column("Detalhes")

        for j in jogadores_filtrados:
            saldo_f = f"{float(j.get('saldo', 0)):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            table.add_row(
                str(j.get("id")),
                j.get("nome", ""),
                str(j.get("idade", "")),
                f"R$ {saldo_f}",
                j.get("detalhes", "")
            )

        console.print(table)

    except ValueError:
        console.print("Informe valores numéricos válidos", style="bold red")
    except Exception as e:
        console.print(f"Erro na pesquisa: {e}", style="bold red")

    input("Pressione Enter para continuar...")

        
    