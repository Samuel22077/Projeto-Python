# FEItv - CCP110

# variaveis usadas no codigo:
# f = arquivo aberto de forma normal
# fc = arquivo do catalogo (usado so pra verificar se existe o filmr)
# arq_favs = arquivo de favoritos do usuario
# arq_usuarios = arquivo com os usuarios cadastrados
# lins = lista com todas as linhas do arquivo pra reescrever
# lin = linha atual sendo lida no loop
# d = dados da linha depois do split por ;
# cred = credenciais do usuario depois do split por ,
# achou = True/False se achou o filme na pesquisa
# logado = True/False se o login foi aceito
# existe = True/False se o filme existe no catalogo
# achada = linha da lista de favoritos que foi encontrada
# op = opcao do menu de filme (curtir/descurtir/voltar)
# opm = opcao do menu principal
# opf = opcao do menu de favoritos
# conf = confirmacao do usuario (sim ou nao)
# nm = nome do filme digitado nos favoritos
# novo = novo nome digitado pra renomear lista

def listar_filmes(caminho_filmes):
    print("\n=== Catalogo de Filmes ===\n")
    try:
        f = open(caminho_filmes, "r", encoding="utf-8")
    except FileNotFoundError:
        print("filmes.txt nao achado")
        return
    for lin in f:
        d = lin.strip().split(";")
        print("Filme: " + d[0])
        print("Genero: " + d[1])
        print("Sinopse: " + d[2])
        print("Curtidas: " + d[3])
        print("----------------------------\n")
    f.close()

# nao precisa digita o nome completo, tipo "inter" ja acha interstellar
def pesquisar_filme(caminho_filmes):
    busca = input("Digite o nome do filme: ")
    if busca == "":
        print("Nao digitou nada!")
        return
    achou = False
    f = open(caminho_filmes, "r", encoding="utf-8")
    for lin in f:
        d = lin.strip().split(";")
        if busca.lower() in d[0].lower():
            achou = True
            print("\nFilme: " + d[0])
            print("Genero: " + d[1])
            print("Sinopse: " + d[2])
            print("Curtidas: " + d[3])
            print("\n1 - Curtir")
            print("2 - Descurtir")
            print("3 - Voltar")
            op = input("")
            if op == "1":
                curtir(caminho_filmes, d[0])
            elif op == "2":
                descurtir(caminho_filmes, d[0])
            # 3 ou qualquer coisa volta pro menu
    f.close()
    if not achou:
        print("Nenhum filme com esse nome foi encontrado.")

# add +1 na curtida e salva no arquivo
def curtir(caminho_filmes, titulo):
    lins = []
    f = open(caminho_filmes, "r", encoding="utf-8")
    for lin in f:
        d = lin.strip().split(";")
        if d[0] == titulo:
            d[3] = str(int(d[3]) + 1)
            print("Voce curtiu " + titulo + "!")
            lins.append(d[0] + ";" + d[1] + ";" + d[2] + ";" + d[3] + "\n")
        else:
            lins.append(lin)
    f.close()
    # tem q reescrever o arquivo todo pra atualizar
    f = open(caminho_filmes, "w", encoding="utf-8")
    f.writelines(lins)
    f.close()

# mesma coisa que curtir mas tira 1
def descurtir(caminho_filmes, titulo):
    lins = []
    f = open(caminho_filmes, "r", encoding="utf-8")
    for lin in f:
        d = lin.strip().split(";")
        if d[0] == titulo:
            d[3] = str(int(d[3]) - 1)
            print("Voce descurtiu " + titulo + ".")
            lins.append(d[0] + ";" + d[1] + ";" + d[2] + ";" + d[3] + "\n")
        else:
            lins.append(lin)
    f.close()
    f = open(caminho_filmes, "w", encoding="utf-8")
    f.writelines(lins)
    f.close()


# ---- favoritos ----

def criar_lista(nome_usuario, titulo_lista):
    if titulo_lista == "":
        print("nome vazio!")
        return
    f = open("favoritos_" + nome_usuario + ".txt", "a", encoding="utf-8")
    f.write("LISTA:" + titulo_lista + "\n")
    f.close()
    print("lista '" + titulo_lista + "' criada!")

def ver_lista(nome_usuario, titulo_lista):
    achada = None
    try:
        f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8")
    except FileNotFoundError:
        # isso acontece se o usuario nao tiver nenhuma lista ainda
        print("arquivo de favoritos nao encontrado.")
        return
    for lin in f:
        if lin.startswith("LISTA:" + titulo_lista):
            achada = lin.strip()
            break  # ja achou, para de ler
    f.close()

    if achada == None:
        print("lista nao encontrada.")
        return

    print("\n" + achada)
    print("\n1 - Renomear lista")
    print("2 - Adicionar filme")
    print("3 - Remover filme")
    print("4 - Excluir lista\n")
    op = input("")

    if op == "1":
        novo = input("novo nome: ")
        if novo == "":
            print("nome invalido.")
            return
        renomear_lista(nome_usuario, titulo_lista, novo)

    elif op == "2":
        nm = input("nome exato do filme (igual ao catalogo): ")
        # tenho q verificar se o filme existe antes de adiciona
        existe = False
        fc = open("filmes.txt", "r", encoding="utf-8")
        for lin in fc:
            if nm == lin.split(";")[0]:
                existe = True
                break
        fc.close()
        if existe:
            adicionar_filme(nome_usuario, titulo_lista, nm)
        else:
            print("esse filme nao ta no catalogo.")

    elif op == "3":
        nm = input("filme que quer remover: ")
        if ";" + nm in achada:
            remover_filme(nome_usuario, titulo_lista, nm)
        else:
            print("esse filme nao ta nessa lista.")

    elif op == "4":
        conf = input("tem certeza? escreva sim pra confirmar: ")
        if conf == "sim":
            excluir_lista(nome_usuario, titulo_lista)
        else:
            print("Ok, lista mantida.")

def renomear_lista(nome_usuario, titulo_antigo, titulo_novo):
    lins = []
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8")
    for lin in f:
        if lin.startswith("LISTA:" + titulo_antigo):
            # troca o nome antigo pelo novo
            lin = lin.replace("LISTA:" + titulo_antigo, "LISTA:" + titulo_novo)
        lins.append(lin)
    f.close()
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8")
    f.writelines(lins)
    f.close()
    print("renomeada pra '" + titulo_novo + "'!")

# adiciona o filme na linha da lista la no txt
def adicionar_filme(nome_usuario, titulo_lista, titulo_filme):
    lins = []
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8")
    for lin in f:
        if lin.startswith("LISTA:" + titulo_lista):
            lin = lin.strip() + ";" + titulo_filme + "\n"
        lins.append(lin)
    f.close()
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8")
    f.writelines(lins)
    f.close()
    print(titulo_filme + " adicionado!")

def remover_filme(nome_usuario, titulo_lista, titulo_filme):
    lins = []
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8")
    for lin in f:
        if lin.startswith("LISTA:" + titulo_lista):
            # so tira o filme da linha, o resto fica
            lin = lin.replace(";" + titulo_filme, "")
        lins.append(lin)
    f.close()
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8")
    f.writelines(lins)
    f.close()
    print(titulo_filme + " removido.")

def excluir_lista(nome_usuario, titulo_lista):
    lins = []
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8")
    for lin in f:
        # pega tudo menos a lista q quer deletar
        if not lin.startswith("LISTA:" + titulo_lista):
            lins.append(lin)
    f.close()
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8")
    f.writelines(lins)
    f.close()
    print("lista deletada.")


# ---- main ----

rodando = True

while rodando:
    print("\n=== FEI TV ===")
    print("1 - Criar conta")
    print("2 - Entrar")
    print("0 - Sair")
    inicio = input("")

    if inicio == "0":
        print("Ate logo!")
        rodando = False

    # cadastro
    elif inicio == "1":
        nome_novo = input("Escolha um nome de usuario: ")
        senha_nova = input("Crie sua senha: ")

        if nome_novo == "" or senha_nova == "":
            print("usuario e senha nao podem tar vazios.")
            continue

        f = open("usuarios.txt", "a", encoding="utf-8")
        f.write(nome_novo + "," + senha_nova + "\n")
        f.close()

        # cria o arquivo de favorito vazio pro usuario novo
        f = open("favoritos_" + nome_novo + ".txt", "w", encoding="utf-8")
        f.close()

        print("Conta criada! Ja pode entrar.")
        inicio = "2"

    # login
    if inicio == "2":
        nome_login = input("Usuario: ")
        senha_login = input("Senha: ")

        logado = False
        try:
            f = open("usuarios.txt", "r", encoding="utf-8")
        except FileNotFoundError:
            # se nao tem nenhum usuario cadastrado ainda
            print("Nenhum usuario cadastrado ainda.")
            continue
        for lin in f:
            cred = lin.strip().split(",")
            if len(cred) == 2:
                if cred[0] == nome_login and cred[1] == senha_login:
                    logado = True
                    break
        f.close()

        if not logado:
            print("usuario ou senha errados, tenta de novo.")

        else:
            print("\nBem vindo, " + nome_login + "!\n")
            no_app = True

            while no_app:
                print("\n1 - Ver catalogo")
                print("2 - Buscar filme")
                print("3 - Favoritos")
                print("0 - Sair da conta\n")
                opm = input("")

                if opm == "0":
                    no_app = False
                    print("Saindo...")

                elif opm == "1":
                    listar_filmes("filmes.txt")

                elif opm == "2":
                    pesquisar_filme("filmes.txt")

                elif opm == "3":
                    print("\n1 - Criar lista")
                    print("2 - Ver lista\n")
                    opf = input("")

                    if opf == "1":
                        nm = input("Nome da nova lista: ")
                        criar_lista(nome_login, nm)
                    elif opf == "2":
                        nm = input("Nome da lista: ")
                        ver_lista(nome_login, nm)
                    else:
                        print("opcao nao existe.")

                else:
                    print("opcao invalida.")