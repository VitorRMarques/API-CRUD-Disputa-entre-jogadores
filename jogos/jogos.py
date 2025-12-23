import requests
from funcoes.gerais import titulo
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from datetime import datetime
from jogadores.cadastros import listar_jogadores

url = "http://localhost:3000"

console = Console()

def incluir_jogo():
    titulo("Inclusão de Jogo")
    print(listar_jogadores())

    try:
        jogador1 = str(input("ID do jogador 1: "))
        jogador2 = str(input("ID do jogador 2: "))


        aposta1 = float(input("Valor que o Jogador 1 vai apostar: R$ "))
        aposta2 = float(input("Valor que o Jogador 2 vai apostar: R$ "))

        # Buscar jogadores
        j1 = requests.get(f"http://localhost:3000/jogadores/{jogador1}").json()
        j2 = requests.get(f"http://localhost:3000/jogadores/{jogador2}").json()

        saldo1 = float(j1["saldo"])
        saldo2 = float(j2["saldo"])

        if j1["status"] != "a":
            console.print("O jogador 1 está inativo. É necessário ativar o status para 'a'", style="bold red")
            return
        
        if j2["status"] != "a":
            console.print("O jogador 2 está inativo. É necessário ativar o status para 'a'", style="bold red")
            return

        if aposta1 > saldo1 or aposta2 > saldo2:
            console.print("Saldo insuficiente para uma das apostas!", style="bold red")
            return

        # Atualizar saldo dos jogadores
        requests.put(f"http://localhost:3000/jogadores/{jogador1}", json={
            **j1,
            "saldo": saldo1 - aposta1
        })

        requests.put(f"http://localhost:3000/jogadores/{jogador2}", json={
            **j2,
            "saldo": saldo2 - aposta2
        })

        novo_jogo = {
            "jogador1": jogador1,
            "jogador2": jogador2,
            "aposta_j1": aposta1,
            "aposta_j2": aposta2,
            "valor_aposta": aposta1 + aposta2,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        response = requests.post("http://localhost:3000/jogos", json=novo_jogo)

        if response.status_code in [200, 201]:
            console.print("Jogo cadastrado com sucesso!", style="bold green")
        else:
            console.print("Erro ao cadastrar jogo", style="bold red")

    except ValueError as e:
        console.print(str(e), style="bold red")        

    except Exception as e:
        console.print(f"Erro: {e}", style="bold red")

    input("Pressione Enter para continuar...")
   

def alterar_jogo():
    titulo("Alterar Jogo (com atualização de saldo)")

    listar_jogo()

    try:
        id_jogo = input("ID do jogo a alterar: ")

        # Buscar jogo atual
        resp_jogo = requests.get(f"{url}/jogos/{id_jogo}")
        if resp_jogo.status_code != 200:
            console.print("Jogo não encontrado!", style="bold red")
            return

        jogo = resp_jogo.json()

        j1_id = jogo["jogador1"]
        j2_id = jogo["jogador2"]

        aposta_antiga_j1 = float(jogo.get("aposta_j1", 0))
        aposta_antiga_j2 = float(jogo.get("aposta_j2", 0))

        print(f"Apostas atuais -> J1: R$ {aposta_antiga_j1} | J2: R$ {aposta_antiga_j2}")

        nova_aposta_j1 = float(input("Novo valor da aposta do Jogador 1: R$ "))
        nova_aposta_j2 = float(input("Novo valor da aposta do Jogador 2: R$ "))

        # Buscar jogadores
        jogador1 = requests.get(f"{url}/jogadores/{j1_id}").json()
        jogador2 = requests.get(f"{url}/jogadores/{j2_id}").json()

        # Diferenças
        diff_j1 = nova_aposta_j1 - aposta_antiga_j1
        diff_j2 = nova_aposta_j2 - aposta_antiga_j2

        # Atualizar saldo
        jogador1["saldo"] = float(jogador1["saldo"]) - diff_j1
        jogador2["saldo"] = float(jogador2["saldo"]) - diff_j2

        # Atualizar jogadores no servidor
        requests.put(f"{url}/jogadores/{j1_id}", json=jogador1)
        requests.put(f"{url}/jogadores/{j2_id}", json=jogador2)

        # Atualizar jogo
        jogo_atualizado = {
            **jogo,
            "aposta_j1": nova_aposta_j1,
            "aposta_j2": nova_aposta_j2,
            "valor_aposta": nova_aposta_j1 + nova_aposta_j2
        }

        resp_update = requests.put(f"{url}/jogos/{id_jogo}", json=jogo_atualizado)

        if resp_update.status_code in [200, 201]:
            console.print("✅ Jogo e saldos atualizados com sucesso!", style="bold green")
        else:
            console.print("Erro ao atualizar jogo", style="bold red")

    except Exception as e:
        console.print(f"Erro: {e}", style="bold red")

    input("Pressione Enter para continuar...")


def excluir_jogo():
    titulo("Excluir Jogo")
    print(listar_jogo())

    try:
        id_jogo = str(input("ID do jogo a excluir: "))

        # Buscar jogo
        resp_jogo = requests.get(f"http://localhost:3000/jogos/{id_jogo}")
        if resp_jogo.status_code != 200:
            console.print("Jogo não encontrado!", style="bold red")
            return
        
        jogo = resp_jogo.json()

        jogador1 = jogo.get("jogador1")
        jogador2 = jogo.get("jogador2")
        aposta1 = float(jogo.get("aposta_j1", 0))
        aposta2 = float(jogo.get("aposta_j2", 0))

        # Buscar jogadores
        j1 = requests.get(f"http://localhost:3000/jogadores/{jogador1}").json()
        j2 = requests.get(f"http://localhost:3000/jogadores/{jogador2}").json()

        saldo1 = float(j1.get("saldo", 0))
        saldo2 = float(j2.get("saldo", 0))

        # Devolver valores ao saldo
        requests.put(f"http://localhost:3000/jogadores/{jogador1}", json={
            **j1,
            "saldo": saldo1 + aposta1
        })

        requests.put(f"http://localhost:3000/jogadores/{jogador2}", json={
            **j2,
            "saldo": saldo2 + aposta2
        })

        # Agora excluir o jogo
        response = requests.delete(f"http://localhost:3000/jogos/{id_jogo}")

        if response.status_code == 200:
            console.print("Jogo excluído e saldos devolvidos com sucesso!", style="bold green")
        else:
            console.print("Erro ao excluir jogo", style="bold red")
        
    except Exception as e:
        console.print(f"Erro: {e}", style="bold red")

    input("Pressione Enter para continuar...")


def listar_jogo():
    titulo("Lista de Jogos")

    try:
        response_jogos = requests.get("http://localhost:3000/jogos")
        response_jogadores = requests.get("http://localhost:3000/jogadores")

        jogos = response_jogos.json()
        jogadores = response_jogadores.json()

        mapa_jogadores = {j['id']: j['nome'] for j in jogadores}

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", justify="center")
        table.add_column("jogador 1")
        table.add_column("jogador 2")
        table.add_column("APOSTA TOTAL(R$)", justify="right")

        for jogo in jogos:
            j1 = mapa_jogadores.get(jogo["jogador1"], "N/A")
            j2 = mapa_jogadores.get(jogo["jogador2"], "N/A")
            valor = float(jogo.get("valor_aposta", 0))

            valor_f = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            table.add_row(
                str(jogo["id"]),
                j1,
                j2,
                f"R$ {valor_f}"
            )

        console.print(table)

    except Exception as e:
        console.print(f"Erro: {e}", style="bold red")

    input("Pressione Enter para continuar...")



    
    
