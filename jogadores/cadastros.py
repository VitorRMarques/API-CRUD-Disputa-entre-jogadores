import requests
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from funcoes.gerais import titulo

url = "http://localhost:3000/jogadores"

console = Console()

def incluir_jogador():
    titulo("Inclusao de Jogador")

    nome = input("Nome do Jogador: ")
    idade = input("Idade do Jogador: ")
    saldo = float(input("Saldo do Jogador R$: "))
    detalhes = input("Detalhes do Jogador: ")
    

    try:
        response = requests.post(url, json={
            "nome": nome,
            "idade": idade,
            "saldo": saldo,
            "detalhes": detalhes,
            "status": "a"
        })
        if response.status_code == 201:
            jogador = response.json()
            print(f"Ok! Jogador cadastrado com Sucesso! Codigo: {jogador['id']}")
        else:
            print("Erro na inclusao")
    except:
        print("Erro....")
    
    print(listar_jogadores())
    input("Pressione Enter para continuar...")

def listar_jogadores():
    titulo("Listagem de Jogadores")

    try:
        response = requests.get(f"{url}") #?status=a
        if response.status_code != 200:
            print("Erro ao obter lista de jogadores")
            return
        
        jogadores = response.json()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Cod.", style="dim")
        table.add_column("nome")
        table.add_column("idade")
        table.add_column("saldo", justify="right")
        table.add_column("detalhes")
        table.add_column("status")

        for jogador in jogadores:

            saldo_f = f"{jogador.get('saldo', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            table.add_row(
                str(jogador.get("id")),
                jogador.get("nome", ""),
                jogador.get("idade", ""),
                f"R$ {saldo_f}",
                jogador.get("detalhes", ""),
                jogador.get("status", "")
            )
        
        console.print(table)

    except Exception as e:
        print(f"Erro de conexao: {e}")

    input("Pressione Enter para continuar...")

def alterar_jogador():
    titulo("Alteracao de jogador")
    print(listar_jogadores())

    try:
        id_jogador = Prompt.ask("Digite o ID do jogador para alterar")
        response = requests.get(f"{url}/{id_jogador}")

        if response.status_code != 200:
            console.print("Jogador nao encontrado.")
            input("Pressione Enter para continuar...")
            return
        
        jogador = response.json()

        nome = Prompt.ask("Nome do Jogador", default=jogador.get("nome", ""))
        idade = Prompt.ask("Idade", default=jogador.get("idade", ""))
        saldo = float(Prompt.ask("Saldo R$", default=str(jogador.get("saldo", "0"))))
        detalhes = Prompt.ask("Detalhes do Jogador", default=jogador.get("detalhes", ""))
        status =  Prompt.ask("Status do Jogador", default=jogador.get("status", ""))

        response = requests.put(f"{url}/{id_jogador}", json={
            "nome": nome,
            "idade": idade,
            "saldo": saldo,
            "detalhes": detalhes,
            "status": status
        })

        if response.status_code == 200:
            console.print("Jogador alterado com sucesso!", style="bold green")
        else:
            console.print("Erro na alteracao.", style="bold red")
        
    except Exception as e:
        console.print(f"Erro: {e}", style="bold red")

    input("Pressione Enter para continuar...")

def excluir_jogador():
    titulo("Exclusao de jogador")
    print(listar_jogadores())

    try:
        id_jogador = Prompt.ask("Digite o ID do jogador que deseja desativar cadastro")
        confirm = Confirm.ask("Confirmar?")

        if not confirm:
            console.print("Inativacao cancelada.", style="bold yellow")
            input("Pressione Enter para continuar...")
            return
        
        response = requests.patch(f"{url}/{id_jogador}", json={
            "status": "i"
        })

        if response.status_code == 200:
            console.print("Constando inatividade!", style="bold green")
        else:
            console.print("Erro na inativacao.", style="bold red")
        
    except Exception as e:
        console.print(f"Erro: {e}", style="bold red")

    input("Pressione Enter para continuar...")
        






        
        
