import requests
from getpass import getpass
from tabulate import tabulate

API_BASE = "https://suap.ifrn.edu.br/api/"

def fazer_login():
    usuario = input("Digite seu usuário SUAP: ")
    senha = getpass("Digite sua senha: ")

    corpo = {"username": usuario, "password": senha}
    resposta = requests.post(API_BASE + "v2/autenticacao/token/", json=corpo)

    if resposta.status_code == 200 and "access" in resposta.json():
        return resposta.json()["access"]
    else:
        print("\n[Erro] Falha ao autenticar. Verifique suas credenciais.")
        try:
            print(resposta.json())
        except:
            pass
        exit()

def buscar_boletim(token, ano):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://suap.ifrn.edu.br/api/edu/meu-boletim/{ano}/1/"

    resposta = requests.get(url, headers=headers)

    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"[Erro] Não foi possível acessar o boletim. Código: {resposta.status_code}")
        try:
            print(resposta.json())
        except:
            pass
        exit()

def mostrar_tabela(boletim, ano):
    

    cabecalho = ["Disciplina", "Etapa 1", "Etapa 2", "Etapa 3", "Etapa 4", "Média Final", "Situação", "Faltas"]
    linhas = []

    for materia in boletim:
        linha = [
            materia.get("disciplina", "—"),
            materia.get("nota_etapa_1", {}).get("nota", "—"),
            materia.get("nota_etapa_2", {}).get("nota", "—"),
            materia.get("nota_etapa_3", {}).get("nota", "—"),
            materia.get("nota_etapa_4", {}).get("nota", "—"),
            materia.get("media_final_disciplina", "—"),
            materia.get("situacao", "—"),
            materia.get("numero_faltas", "—")
        ]
        linhas.append(linha)

    print(tabulate(linhas, headers=cabecalho, tablefmt="rounded_grid"))

def main():
    token = fazer_login()
    ano = input("Digite o ano do boletim (ex: 2025): ")
    boletim = buscar_boletim(token, ano)
    mostrar_tabela(boletim, ano)

if __name__ == "__main__":
    main()
