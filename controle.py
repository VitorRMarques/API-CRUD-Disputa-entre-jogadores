from rich.console import Console
console = Console()

from funcoes.gerais import titulo
from jogadores.cadastros import incluir_jogador, listar_jogadores, alterar_jogador, excluir_jogador
from jogos.jogos import incluir_jogo, alterar_jogo, excluir_jogo, listar_jogo
from pesquisas.pesquisas import pesq_jogadores, pesq_jogos_aposta, pesq_idades
from graficos.graficos import jogadores_saldo, jogadores_idade, jogos_apostas, grafico_apostas_por_jogador
from utilitarios.backup import backup_dados
while True:
    print("1. Cadastro de Jogadores")
    print("2. Cadastro de Jogos")
    print("3. Pesquisas")
    print("4. Graficos")
    print("5. Utilitarios")
    print("6. Finalizar")
    opcao = int(input("Opcao: "))
    if opcao == 1:
        print("Cadastro de jogadores")
        print("1. Incluir")
        print("2. Alterar")
        print("3. Excluir")
        print("4. Listar")
        print("5. Retornar")

        sub_opcao = int(input("Opcao: "))
        if sub_opcao == 1:
            incluir_jogador()
        elif sub_opcao == 2:
            alterar_jogador()
        elif sub_opcao == 3:
            excluir_jogador()
        elif sub_opcao == 4:
            listar_jogadores()
    elif opcao == 2:
        print("Cadastro de Jogos")
        print("1. Incluir")
        print("2. Alterar")
        print("3. Excluir")
        print("4. Listar")
        print("5. Retornar")
        sub_opcao = int(input("Opcao: "))
        if sub_opcao == 1:
            incluir_jogo()
        elif sub_opcao == 2:
            alterar_jogo()
        elif sub_opcao == 3:
            excluir_jogo()
        elif sub_opcao == 4:
            listar_jogo()
    elif opcao == 3:
        print("Pesquisa Avancadas")
        print("1. Pesquisa de saldo de jogadores por intervalo")
        print("2. Pesquisa de valores por intervalo de apostas")
        print("3. Pesquisa por intervalo de idades")
        print("4. Retornar")
        sub_opcao = int(input("Opcao: "))
        if sub_opcao == 1:
            pesq_jogadores()
        elif sub_opcao == 2:
            pesq_jogos_aposta()
        elif sub_opcao == 3:
            pesq_idades()
    elif opcao == 4:
        print("Graficos do Sistema")
        print("1. Jogadores por Saldo")
        print("2. Jogadores por Idade")
        print("3. Jogos por Total de Apostas")
        print("4. Total apostado por Jogador")
        print("5. Retornar")
        sub_opcao = int(input("Opcao: "))
        if sub_opcao == 1:
            jogadores_saldo()
        elif sub_opcao == 2:
            jogadores_idade()
        elif sub_opcao == 3:
            jogos_apostas()
        elif sub_opcao == 4:
            grafico_apostas_por_jogador()
    elif opcao == 5:
        print("Utilitarios do Sistema")
        print("1. Backup dos Dados")
        print("2. Retornar")
        sub_opcao = int(input("Opcao: "))
        if sub_opcao == 1:
            backup_dados()
    else:
        break
        