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

def listar_filmes(caminho_filmes): # recebe o caminho do arquivo de filmes
    print("\n=== Catalogo de Filmes ===\n") # cabecalho do catalogo
    try:
        f = open(caminho_filmes, "r", encoding="utf-8") # abre o arquivo pra leitura
    except FileNotFoundError: # se o arquivo nao existir
        print("filmes.txt nao achado") # avisa o usuario
        return # para a funcao
    for lin in f: # le linha por linha do arquivo
        d = lin.strip().split(";") # tira espacos e separa os dados pelo ;
        print("Filme: " + d[0]) # d[0] e o nome do filme
        print("Genero: " + d[1]) # d[1] e o genero
        print("Sinopse: " + d[2]) # d[2] e a sinopse
        print("Curtidas: " + d[3]) # d[3] e o numero de curtidas
        print("----------------------------\n") # separador entre filmes
    f.close() # fecha o arquivo

# nao precisa digita o nome completo, tipo "inter" ja acha interstellar
def pesquisar_filme(caminho_filmes): # recebe o caminho do arquivo de filmes
    busca = input("Digite o nome do filme: ") # pede o nome pro usuario
    if busca == "": # se nao digitou nada
        print("Nao digitou nada!") # avisa
        return # para a funcao
    achou = False # começa como falso, vira True se achar algum filme
    f = open(caminho_filmes, "r", encoding="utf-8") # abre o arquivo pra leitura
    for lin in f: # le cada linha do arquivo
        d = lin.strip().split(";") # separa os dados da linha
        if busca.lower() in d[0].lower(): # compara ignorando maiusculas
            achou = True # encontrou pelo menos um filme
            print("\nFilme: " + d[0]) # mostra o nome
            print("Genero: " + d[1]) # mostra o genero
            print("Sinopse: " + d[2]) # mostra a sinopse
            print("Curtidas: " + d[3]) # mostra as curtidas
            print("\n1 - Curtir") # opcao de curtir
            print("2 - Descurtir") # opcao de descurtir
            print("3 - Voltar") # opcao de voltar
            op = input("") # pega a opcao do usuario
            if op == "1": # se escolheu curtir
                curtir(caminho_filmes, d[0]) # chama a funcao curtir
            elif op == "2": # se escolheu descurtir
                descurtir(caminho_filmes, d[0]) # chama a funcao descurtir
            # 3 ou qualquer coisa volta pro menu
    f.close() # fecha o arquivo
    if not achou: # se nao achou nenhum filme
        print("Nenhum filme com esse nome foi encontrado.") # avisa o usuario

# add +1 na curtida e salva no arquivo
def curtir(caminho_filmes, titulo): # recebe o arquivo e o nome do filme
    lins = [] # lista vazia pra guardar as linhas atualizadas
    f = open(caminho_filmes, "r", encoding="utf-8") # abre pra leitura
    for lin in f: # le cada linha
        d = lin.strip().split(";") # separa os dados
        if d[0] == titulo: # se for o filme que quer curtir
            d[3] = str(int(d[3]) + 1) # converte pra int, soma 1, volta pra string
            print("Voce curtiu " + titulo + "!") # confirma pro usuario
            lins.append(d[0] + ";" + d[1] + ";" + d[2] + ";" + d[3] + "\n") # reconstroi a linha atualizada
        else:
            lins.append(lin) # se nao for o filme, mantem a linha igual
    f.close() # fecha o arquivo de leitura
    # tem q reescrever o arquivo todo pra atualizar
    f = open(caminho_filmes, "w", encoding="utf-8") # abre pra escrita, apaga o conteudo antigo
    f.writelines(lins) # escreve todas as linhas de volta
    f.close() # fecha o arquivo

# mesma coisa que curtir mas tira 1
def descurtir(caminho_filmes, titulo): # recebe o arquivo e o nome do filme
    lins = [] # lista vazia pra guardar as linhas
    f = open(caminho_filmes, "r", encoding="utf-8") # abre pra leitura
    for lin in f: # le cada linha
        d = lin.strip().split(";") # separa os dados
        if d[0] == titulo: # se for o filme que quer descurtir
            d[3] = str(int(d[3]) - 1) # converte pra int, subtrai 1, volta pra string
            print("Voce descurtiu " + titulo + ".") # confirma pro usuario
            lins.append(d[0] + ";" + d[1] + ";" + d[2] + ";" + d[3] + "\n") # reconstroi a linha
        else:
            lins.append(lin) # mantem a linha igual
    f.close() # fecha leitura
    f = open(caminho_filmes, "w", encoding="utf-8") # abre pra escrita
    f.writelines(lins) # reescreve tudo
    f.close() # fecha


# ---- favoritos ----

def criar_lista(nome_usuario, titulo_lista): # recebe o usuario e o nome da lista
    if titulo_lista == "": # se nao digitou nome
        print("nome vazio!") # avisa
        return # para a funcao
    f = open("favoritos_" + nome_usuario + ".txt", "a", encoding="utf-8") # abre no modo append, nao apaga o que ja tinha
    f.write("LISTA:" + titulo_lista + "\n") # escreve a linha da lista nova
    f.close() # fecha
    print("lista '" + titulo_lista + "' criada!") # confirma

def ver_lista(nome_usuario, titulo_lista): # recebe o usuario e o nome da lista
    achada = None # começa como None, vai guardar a linha da lista se achar
    try:
        f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8") # tenta abrir o arquivo
    except FileNotFoundError: # isso acontece se o usuario nao tiver nenhuma lista ainda
        print("arquivo de favoritos nao encontrado.") # avisa
        return # para a funcao
    for lin in f: # le cada linha do arquivo
        if lin.startswith("LISTA:" + titulo_lista): # se a linha for da lista que quer ver
            achada = lin.strip() # guarda a linha sem o \n
            break  # ja achou, para de ler
    f.close() # fecha o arquivo

    if achada == None: # se nao encontrou a lista
        print("lista nao encontrada.") # avisa
        return # para a funcao

    print("\n" + achada) # mostra o conteudo atual da lista
    print("\n1 - Renomear lista") # opcao 1
    print("2 - Adicionar filme") # opcao 2
    print("3 - Remover filme") # opcao 3
    print("4 - Excluir lista\n") # opcao 4
    op = input("") # pega a escolha do usuario

    if op == "1": # se escolheu renomear
        novo = input("novo nome: ") # pede o novo nome
        if novo == "": # se nao digitou nada
            print("nome invalido.") # avisa
            return # para
        renomear_lista(nome_usuario, titulo_lista, novo) # chama a funcao de renomear

    elif op == "2": # se escolheu adicionar filme
        nm = input("nome exato do filme (igual ao catalogo): ") # pede o nome do filme
        # tenho q verificar se o filme existe antes de adiciona
        existe = False # começa como falso
        fc = open("filmes.txt", "r", encoding="utf-8") # abre o catalogo pra verificar
        for lin in fc: # le cada linha do catalogo
            if nm == lin.split(";")[0]: # compara com o nome do filme
                existe = True # achou o filme
                break # para de procurar
        fc.close() # fecha o catalogo
        if existe: # se o filme existe no catalogo
            adicionar_filme(nome_usuario, titulo_lista, nm) # adiciona na lista
        else:
            print("esse filme nao ta no catalogo.") # avisa se nao existir

    elif op == "3": # se escolheu remover filme
        nm = input("filme que quer remover: ") # pede o nome do filme
        if ";" + nm in achada: # verifica se o filme esta na lista
            remover_filme(nome_usuario, titulo_lista, nm) # remove o filme
        else:
            print("esse filme nao ta nessa lista.") # avisa se nao tiver

    elif op == "4": # se escolheu excluir a lista
        conf = input("tem certeza? escreva sim pra confirmar: ") # pede confirmacao
        if conf == "sim": # se confirmou
            excluir_lista(nome_usuario, titulo_lista) # exclui a lista
        else:
            print("Ok, lista mantida.") # se nao confirmou mantem

def renomear_lista(nome_usuario, titulo_antigo, titulo_novo): # recebe usuario, nome antigo e nome novo
    lins = [] # lista vazia pra guardar as linhas
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8") # abre pra leitura
    for lin in f: # le cada linha
        if lin.startswith("LISTA:" + titulo_antigo): # se for a linha da lista que quer renomear
            # troca o nome antigo pelo novo
            lin = lin.replace("LISTA:" + titulo_antigo, "LISTA:" + titulo_novo) # substitui o nome
        lins.append(lin) # adiciona a linha na lista
    f.close() # fecha leitura
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8") # abre pra escrita
    f.writelines(lins) # reescreve tudo com o nome novo
    f.close() # fecha
    print("renomeada pra '" + titulo_novo + "'!") # confirma

# adiciona o filme na linha da lista la no txt
def adicionar_filme(nome_usuario, titulo_lista, titulo_filme): # recebe usuario, lista e filme
    lins = [] # lista vazia
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8") # abre pra leitura
    for lin in f: # le cada linha
        if lin.startswith("LISTA:" + titulo_lista): # se for a linha da lista certa
            lin = lin.strip() + ";" + titulo_filme + "\n" # tira o \n, coloca ;filme e coloca o \n de volta
        lins.append(lin) # adiciona na lista
    f.close() # fecha leitura
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8") # abre pra escrita
    f.writelines(lins) # reescreve com o filme novo
    f.close() # fecha
    print(titulo_filme + " adicionado!") # confirma

def remover_filme(nome_usuario, titulo_lista, titulo_filme): # recebe usuario, lista e filme
    lins = [] # lista vazia
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8") # abre pra leitura
    for lin in f: # le cada linha
        if lin.startswith("LISTA:" + titulo_lista): # se for a linha da lista certa
            # so tira o filme da linha, o resto fica
            lin = lin.replace(";" + titulo_filme, "") # remove o ;filme da linha
        lins.append(lin) # adiciona na lista
    f.close() # fecha leitura
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8") # abre pra escrita
    f.writelines(lins) # reescreve sem o filme
    f.close() # fecha
    print(titulo_filme + " removido.") # confirma

def excluir_lista(nome_usuario, titulo_lista): # recebe usuario e nome da lista
    lins = [] # lista vazia
    f = open("favoritos_" + nome_usuario + ".txt", "r", encoding="utf-8") # abre pra leitura
    for lin in f: # le cada linha
        # pega tudo menos a lista q quer deletar
        if not lin.startswith("LISTA:" + titulo_lista): # se nao for a lista que quer deletar
            lins.append(lin) # adiciona na lista
    f.close() # fecha leitura
    f = open("favoritos_" + nome_usuario + ".txt", "w", encoding="utf-8") # abre pra escrita
    f.writelines(lins) # reescreve sem aquela lista
    f.close() # fecha
    print("lista deletada.") # confirma


# ---- main ----

rodando = True # controla o loop principal, vira False quando o usuario sair

while rodando: # fica rodando enquanto o usuario nao sair
    print("\n=== FEI TV ===") # cabecalho
    print("1 - Criar conta") # opcao de cadastro
    print("2 - Entrar") # opcao de login
    print("0 - Sair") # opcao de sair
    inicio = input("") # pega a opcao do usuario

    if inicio == "0": # se escolheu sair
        print("Ate logo!") # despedida
        rodando = False # para o loop

    # cadastro
    elif inicio == "1": # se escolheu criar conta
        nome_novo = input("Escolha um nome de usuario: ") # pede o nome
        senha_nova = input("Crie sua senha: ") # pede a senha

        if nome_novo == "" or senha_nova == "": # se deixou algum campo vazio
            print("usuario e senha nao podem tar vazios.") # avisa
            continue # volta pro inicio do loop

        f = open("usuarios.txt", "a", encoding="utf-8") # abre no modo append
        f.write(nome_novo + "," + senha_nova + "\n") # salva usuario e senha
        f.close() # fecha

        # cria o arquivo de favorito vazio pro usuario novo
        f = open("favoritos_" + nome_novo + ".txt", "w", encoding="utf-8") # cria o arquivo vazio
        f.close() # fecha

        print("Conta criada! Ja pode entrar.") # confirma o cadastro
        inicio = "2" # redireciona pro login automaticamente

    # login
    if inicio == "2": # se vai fazer login
        nome_login = input("Usuario: ") # pede o usuario
        senha_login = input("Senha: ") # pede a senha

        logado = False # começa como falso
        try:
            f = open("usuarios.txt", "r", encoding="utf-8") # tenta abrir o arquivo de usuarios
        except FileNotFoundError: # se nao tem nenhum usuario cadastrado ainda
            print("Nenhum usuario cadastrado ainda.") # avisa
            continue # volta pro menu
        for lin in f: # le cada linha do arquivo
            cred = lin.strip().split(",") # separa usuario e senha pela virgula
            if len(cred) == 2: # verifica se a linha tem usuario e senha
                if cred[0] == nome_login and cred[1] == senha_login: # compara com o que foi digitado
                    logado = True # login aceito
                    break # para de procurar
        f.close() # fecha o arquivo

        if not logado: # se nao achou o usuario ou senha errada
            print("usuario ou senha errados, tenta de novo.") # avisa

        else: # se o login foi aceito
            print("\nBem vindo, " + nome_login + "!\n") # mensagem de boas vindas
            no_app = True # controla o loop interno do app

            while no_app: # fica no app enquanto nao sair da conta
                print("\n1 - Ver catalogo") # opcao de listar filmes
                print("2 - Buscar filme") # opcao de pesquisar
                print("3 - Favoritos") # opcao de favoritos
                print("0 - Sair da conta\n") # opcao de logout
                opm = input("") # pega a opcao

                if opm == "0": # se escolheu sair da conta
                    no_app = False # para o loop interno
                    print("Saindo...") # confirma

                elif opm == "1": # se escolheu ver catalogo
                    listar_filmes("filmes.txt") # chama a funcao de listar

                elif opm == "2": # se escolheu buscar filme
                    pesquisar_filme("filmes.txt") # chama a funcao de pesquisa

                elif opm == "3": # se escolheu favoritos
                    print("\n1 - Criar lista") # opcao de criar
                    print("2 - Ver lista\n") # opcao de ver
                    opf = input("") # pega a opcao

                    if opf == "1": # se escolheu criar lista
                        nm = input("Nome da nova lista: ") # pede o nome da lista
                        criar_lista(nome_login, nm) # chama a funcao de criar
                    elif opf == "2": # se escolheu ver lista
                        nm = input("Nome da lista: ") # pede o nome da lista
                        ver_lista(nome_login, nm) # chama a funcao de ver
                    else:
                        print("opcao nao existe.") # opcao invalida no menu de favoritos

                else:
                    print("opcao invalida.") # opcao invalida no menu principal