import requests
import json
from datetime import datetime
from funcoes.gerais import titulo
from rich.console import Console

console = Console()

# URL base do json-server (sem / no final)
BASE_URL = "http://localhost:3000"

# Recursos que provavelmente existem — adicione outros se seu db.json tiver nomes diferentes
KNOWN_RESOURCES = ["jogadores", "jogos", "users", "products", "sales"]

def backup_dados():
    titulo("Backup dos Dados do Sistema")
    try:
        # 1) Tentar obter /db (algumas instalações expõem isso)
        try:
            console.print("Tentando obter todo o DB via /db ...")
            r = requests.get(f"{BASE_URL}/db", timeout=8)
            if r.status_code == 200:
                try:
                    dados = r.json()
                    console.print("OK: obtido /db diretamente.")
                except Exception as ex_json:
                    console.print(f"A resposta de /db não é JSON válido: {ex_json}", style="bold red")
                    dados = None
            else:
                console.print(f"/db retornou status {r.status_code}. Vou tentar detectar recursos.", style="yellow")
                dados = None
        except requests.RequestException as ex:
            console.print(f"Falha ao acessar /db: {ex}", style="yellow")
            dados = None

        # 2) Se /db não funcionou, buscar recursos conhecidos (somente os que existirem)
        if dados is None:
            dados = {}
            console.print("Detectando recursos conhecidos (jogadores, jogos, ...)")
            for res in KNOWN_RESOURCES:
                try:
                    r2 = requests.get(f"{BASE_URL}/{res}", timeout=6)
                    if r2.status_code == 200:
                        try:
                            dados_res = r2.json()
                        except Exception:
                            dados_res = None
                        # só adicionar se for JSON válido
                        if dados_res is not None:
                            dados[res] = dados_res
                            console.print(f" - recurso encontrado: /{res} (itens: {len(dados_res)})")
                    else:
                        # recurso não existe — ignora
                        pass
                except requests.RequestException:
                    # falha ao contactar esse recurso — ignora e continua
                    pass

            if not dados:
                console.print("Nenhum recurso detectado. Verifique se o json-server está rodando e se os nomes das coleções estão corretos.", style="bold red")
                return

        # 3) Gravar em arquivo
        nome_arquivo = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            console.print(f"✅ Backup criado com sucesso: {nome_arquivo}", style="green")
        except Exception as ex_file:
            console.print(f"Erro ao gravar arquivo de backup: {ex_file}", style="bold red")
            return

    except Exception as e:
        console.print(f"Erro inesperado durante backup: {e}", style="bold red")

    input("Pressione Enter para continuar...")
