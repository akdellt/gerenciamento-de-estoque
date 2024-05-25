import os
os.system("cls")

#AUTENTICAÇÃO DO SISTEMA COM SENHA

#ABRE ARQUIVO COM USUÁRIOS E SENHAS
userSenha = open("./usuarios.txt", "r")

#CRIA LISTAS COM USUÁRIOS E SENHAS
linhas = userSenha.readlines()

user = []
senhas = []
cont = 2

#SEPARA APENAS OS USUÁRIOS QUE CONSTAM NO ARQUIVO
for pos, usuarios in enumerate(linhas):
    if pos % 2 == 0:
        user.append(usuarios.strip())

#SEPARA APENAS AS SENHAS QUE CONSTAM NO ARQUIVO
for pos, senha in enumerate(linhas):
    if pos % 2 == 1:
        senhas.append(senha.strip())

#SOLICITA INFORMAÇÕES DE LOGIN
usuario = input("Usuário: ")
senha = input("Senha: ")

#CASO UM/DOIS ITENS ESTEJAM ERRADOS
while usuario not in user or senha not in senhas:
    if cont < 3:
        print("\nUsuário ou senha incorreta, tente novamente: " )
        print(">>> Você tem", cont, "tentativas restantes. \n")
        usuario = input("Nome do usuário: ")
        senha = input("Senha: ")

        cont -= 1

    #CASO OS DOIS ITENS ESTEJAM CERTOS NA ÚLTIMA TENTATIVA
    if usuario in user and senha in senhas and cont == 0:
        continue    

    #CASO OS DOIS ITENS ESTEJAM ERRADOS NA ÚLTIMA TENTATIVA
    if usuario not in user and senha not in senhas and cont == 0:
        print(">>> Limite excedido. Acesso negado. \n")
        exit()

#CASO OS DOIS ITENS ESTEJAM CERTOS
else:
    print(">>> Acesso permitido.")

userSenha.close()


#>>>>> MENU COM FUNCIONALIDADES

#DECLARAÇÃO DE VARIÁVEIS E DICIONÁRIOS
opcao = 0
produtos = {}
categorias = {}
ESTOQUE_MINIMO = {}


#MENU 
def menu():
    print(" ") 
    print("=" *30)
    print("[1] Inserir produtos \n[2] Editar produtos \n[3] Deletar produtos \n[4] Relatório de produtos \n[5] Total de estoque \n[6] Status por categoria \n[7] Verificar estoque mínimo \n[8] Sair")
    print("=" *30)


#INSERIR PRODUTO
def produto():
    global produtos, categorias, ESTOQUE_MIN

    #INSERE INFORMAÇÕES DOS PRODUTOS
    while True:
        nome = input("\nNome do produto: ")

        if nome == "sair":
            print(">>> Voltando ao menu.")
            break

        categoria = input("Categoria do produto: ")

        while True:
            try:
                quantidade = int(input("Quantidade do produto: "))
                break
            #FORÇA USUÁRIO A INSERIR NÚMEROS PARA O ITEM
            except ValueError:
                print(">>> A quantidade deve ser inserida em número. Tente novamente.\n")


        #SE A CATEGORIA AINDA NÃO EXISTIR ADICIONAR ESTOQUE
        if categoria not in categorias:
            categorias[categoria] = 0

            #DEFINE VALOR MÍNIMO DE ESTOQUE PARA CADA CATEGORIA INSERIDA
            while True:
                try:
                    ESTOQUE_MIN = int(input("\nQual é o estoque mínimo desta categoria? "))
                    break
                #FORÇA USUÁRIO A INSERIR NÚMEROS PARA O ITEM
                except ValueError:
                    print(">>> A quantidade deve ser inserida em número. Tente novamente.")
                
            ESTOQUE_MINIMO[categoria] = ESTOQUE_MIN

        #SE A CATEGORIA E/OU NOME JÁ EXISTIR ADICIONAR PRODUTO
        if categoria in categorias:
            if nome in produtos:
                produtos[nome] += quantidade
                categorias[categoria] += quantidade
            else:
                produtos[nome] = quantidade
                categorias[categoria] += quantidade


#CALCULAR QUANT TOTAL DOS PRODUTOS EM ESTOQUE
def estoque():
    global quantidade, produtos

    #SEPARA AS CATEGORIAS INSERIDAS E IMPRIME O RESULTADO
    print("\nA quantidade total de produtos no estoque é: ")
    for categoria, quantidade in categorias.items():
        print(f"\n{categoria}: {quantidade} unidades")


#APRESENTAR STATUS EM PORCENTAGEM POR CATEGORIA
def status():
    global categorias, quantidade, ESTOQUE_MINIMO

    #PARA CADA CATEGORIA DE PRODUTOS NO ESTOQUE É CALCULA A PORCENTAGEM EM RELAÇÃO AO VALOR MÍNIMO
    print("\nO status de estoque de cada categoria é: ")
    for categoria, quantidade in categorias.items():
        if categoria in ESTOQUE_MINIMO:
            ESTOQUE_MIN = ESTOQUE_MINIMO[categoria]
            porcentagem_total = (quantidade / ESTOQUE_MIN) * 100
            print(f"\n{categoria}: {porcentagem_total:.2f}% da capacidade mínima preenchida.")


#VERIFICAÇÃO DOS PRODUTOS CADASTRADOS ABAIXO DO ESTOQUE MINIMO
def verificar():
    global categorias, ESTOQUE_MINIMO
    estoque_cheio = True

    #INFORMA QUAIS CATEGORIAS ESTÃO COM DÉFICT DE PRODUTOS
    for categoria, ESTOQUE_MIN in ESTOQUE_MINIMO.items():
        if categoria in categorias and categorias[categoria] < ESTOQUE_MIN:
            print(f"\nCategoria {categoria} com produtos abaixo do nível mínimo de estoque. Necessário novo pedido. ")
            estoque_cheio = False
            
        #INFORMA QUE TODAS AS CATEGORIAS ESTÃO OU PASSARAM DO SEU MÍNIMO
    if estoque_cheio:
        print("\nNão há necessidade de realizar um novo pedido")


#LISTAR OS PRODUTOS INSERIDOS EXPORTANDO PARA UM ARQUIVO
def listar():
    #CRIAR ARQUIVO DE ESTOQUE
    estoque = open("estoque.txt", "wt+")
    estoque.write("PRODUTOS INSERIDOS \n \n")

    estoque = open("estoque.txt", "a")
    for nome, quantidade in produtos.items():
        estoque.write(f"{nome}: {quantidade} unidades \n")
    
    estoque.close() 

    print("\nArquivo [estoque.txt] criado!")  


#EDITAR OS PRODUTOS INSERIDOS
def editar():
    global categorias, produtos

    #EDITAR QUANTIDADE
    while True:
        editado = input("\nDigite o produto a ser editado: ")

        #FINALIZA FUNÇÃO SE QUISER SAIR
        if editado == "sair":
            print(">>> Voltando ao menu.")
            break

        if editado not in produtos:
            print(">>> Produto não existente. Tente novamente.")

        categoria = input("Categoria do produto a ser editado: ")

        if categoria not in categorias:
            print(">>> Categoria não existente. Tente novamente.")

        #ADICIONA QUANTIDADE NOVA
        while True:
            try:
                nova_quantidade = int(input("Nova quantidade do produto: "))
                break
            #FORÇA USUÁRIO A INSERIR NÚMEROS PARA O ITEM
            except ValueError:
                print(">>> A quantidade deve ser inserida em número. Tente novamente.\n")

        #SE NOME E CATEGORIA INSERIDAS EXISTIREM
        if editado and categoria in categorias:
            quantidade = produtos[editado]
            produtos[editado] = nova_quantidade
            categorias[categoria] += nova_quantidade - quantidade   


#DELETAR O RPODUTO SELECIONADO
def deletar():
    global categorias, produtos, deletado, quantidade

    #DELETAR PRODUTO
    while True:
        deletado  = input("\nDigite o produto a ser deletado: ")

        #FINALIZA FUNÇÃO SE QUISER SAIR
        if deletado == "sair":
            print(">>> Voltando ao menu.")
            break

        if deletado not in produtos:
            print(">>> Produto não existente. Tente novamente.")

        categoria = input("Categoria do produto a ser editado: ")

        if categoria not in categorias:
            print(">>> Categoria não existente. Tente novamente.")

        #SE NOME E CATEGORIA INSERIDAS EXISTIREM
        if deletado and categoria in categorias:
            quantidade = produtos.pop(deletado)
            categorias[categoria] -= quantidade


#FUNCIONAMENTO DO MENU COM ESTRUTURA MATCH CASE E WHILE
while opcao != 8:
    menu()
    opcao = int(input("\nSelecione uma opção: "))
    print(" ")
    print("=" *30)
    match opcao:
        case 1:
            print("Escreva 'sair' para voltar ao menu.")
            produto()
        case 2:
            print("Escreva 'sair' para voltar ao menu.")
            editar()
        case 3:
            print("Escreva 'sair' para voltar ao menu.")
            deletar()
        case 4:
            listar()
        case 5:
            estoque()
        case 6:
            status()
        case 7:
            verificar()
        case 8:
            print("\nSaindo...")
            exit()
        case _:
            print("\nOpção inválida, tente novamente.")

