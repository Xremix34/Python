import time

import control  # importa a classe control.py


def menuPrincipal():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('LOJA')
    print('{:^302s}'.format(control.IDENTIFICACAO))
    print('{:^330}'.format('[7].TERMINAR SESSÃO'))
    print(control.mostra_cabecalho_opcoes_menu())
    print('1. GESTÃO DE PRODUTOS\n2. GESTÃO DE VENDAS\n3. GESTÃO DE ENCOMENDAS\n4. GESTÃO DE UTILIZADORES\n5. GESTÃO DE CLIENTES\n6. GESTÃO DE FORNECEDORES\n0. SAIR\n')

    opcao = str(input('ESCOLHA UMA OPÇÂO: '))
    print()
#condição que permite verificar se tem niveis de acesso para aceder À opção
    if opcao.isnumeric():
        if opcao == '1' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ad or opcao == '1' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ut:
            gestao_produtos()
        elif opcao == '2' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ut or opcao == '2' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ad:
            gerenciamento_de_compras()
        elif opcao == '3' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ad:
            gestao_de_encomendas()
        elif opcao == '4' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ad:
            gestao_de_utilizadores()
        elif opcao == '5' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ut or opcao == '5' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ad:
            gestao_de_clientes()
        elif opcao == '6' and int(str(control.lista_nivelAcesso)[1:-1]) == control.ad:
            gestao_de_fornecedores()
        elif opcao == '7':
            control.IDENTIFACAO = ''
            control.lista_nivelAcesso.clear()
            menuLogin()
        elif opcao == '0':
            exit(0)
        else:
            print('\033[1;41m Não tem as pemissões necessárias para aceder a esta opção!\033[m')
            time.sleep(1)
            menuPrincipal()
    else:
        print('\033[1;41m A opção escolhida não é válida!\033[m')
        time.sleep(1)
        menuPrincipal()

def menuLogin():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('LOGIN')

    print('{:^330}\n\n'.format(''))
    control.logar(control.meuCursor)


def gestao_produtos():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('GESTÃO DE PRODUTOS')
    print('{:^302s}\n'.format(control.IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))
    print(control.mostra_cabecalho_opcoes_menu())
    print('1. ADICIONAR NOVO PRODUTO\n2. LISTAR PRODUTOS\n3. ACTUALIZAR PRODUTOS\n4. ELIMINAR PRODUTOS\n5. VOLTAR\n0. SAIR\n')

    opcao = str(input('ESCOLHA UMA OPÇÂO: '))

    if opcao == '1':
        control.adicionar_produto(control.meuCursor)
    elif opcao == '2':
        control.listar_produtos(control.meuCursor)
    elif opcao == '3':
        control.atualizar_produto(control.meuCursor)
    elif opcao == '4':
        control.eliminar_Produto(control.meuCursor)
    elif opcao == '5':
        menuPrincipal()
    elif opcao == '0':
        exit(0)
    else:
        print('\033[1;41mA opção escolhida não é válida\033[m!')
        time.sleep(1)
        gestao_produtos()


def gerenciamento_de_compras():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('GESTÃO DE VENDAS')
    print('{:^302s}\n'.format(control.IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))
    print(control.mostra_cabecalho_opcoes_menu())
    print('1. VENDER PRODUTOS\n2. LISTAR VENDAS\n5. VOLTAR\n0. SAIR\n')

    opcao = str(input('ESCOLHA UMA OPÇÂO: '))

    if opcao == '1':
        control.venda_produtos(control.meuCursor, control.dataAtual)
    elif opcao == '2':
        control.listar_vendas_produtos(control.meuCursor)
    elif opcao == '5':
        menuPrincipal()
    elif opcao == '0':
        exit(0)
    else:
        print('\033[1;41mA opção escolhida não é válida\033[m!')
        time.sleep(1)
        gerenciamento_de_compras()


def gestao_de_encomendas():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('GESTÂO DE ENCOMENDAS')
    print('{:^302s}\n'.format(control.IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))
    print(control.mostra_cabecalho_opcoes_menu())
    print('1. ADICIONAR ENCOMENDA\n2. LISTAR ENCOMENDAS\n5. VOLTAR\n0. SAIR\n')

    opcao = str(input('ESCOLHA UMA OPÇÂO: '))

    if opcao == '1':
        control.adicionar_encomenda(control.meuCursor, control.dataAtual)
    elif opcao == '2':
        control.listar_encomendas(control.meuCursor)
    elif opcao == '5':
        menuPrincipal()
    elif opcao == '0':
        exit(0)
    else:
        print('\033[1;41mA opção escolhida não é válida\033[m!')
        time.sleep(1)
        gestao_de_encomendas()


def gestao_de_utilizadores():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('GESTAO DE UTILIZADORES')
    print('{:^302s}\n'.format(control.IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))
    print(control.mostra_cabecalho_opcoes_menu())
    print('1. ADICIONAR UTILIZADOR\n2. LISTAR UTILIZADORES\n3. ATUALIZAR UTILIZADORES\n4. ELIMINAR UTILIZADORES\n5. VOLTAR\n0. SAIR\n')

    opcao = str(input('ESCOLHA UMA OPÇÂO: '))

    if opcao == '1':
        control.adicionar_utilizador(control.meuCursor)
    elif opcao == '2':
        control.listar_utilizadores(control.meuCursor)
    elif opcao == '3':
        control.atualizar_utilizador(control.meuCursor)
    elif opcao == '4':
        control.eliminar_utilizador(control.meuCursor)
    elif opcao == '5':
        menuPrincipal()
    elif opcao == '0':
        exit(0)
    else:
        print('\033[1;41mA opção escolhida não é válida\033[m!')
        time.sleep(1)
        gestao_de_utilizadores()


def gestao_de_clientes():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('GESTAO DE CLIENTES')
    print('{:^302s}\n'.format(control.IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))
    print(control.mostra_cabecalho_opcoes_menu())
    print('1. ADICIONAR NOVO CLIENTE\n2. LISTAR CLIENTES\n3. ATUALIZAR CLIENTE\n4. ELIMINAR CLIENTE\n5. VOLTAR\n0. SAIR\n')

    opcao = str(input('ESCOLHA UMA OPÇÂO: '))

    if opcao == '1':
        control.adicionar_cliente(control.meuCursor)
    elif opcao == '2':
        control.listar_clientes(control.meuCursor)
    elif opcao == '3':
        control.atualizar_clientes(control.meuCursor)
    elif opcao == '4':
        control.eliminar_Cliente(control.meuCursor)
    elif opcao == '5':
        menuPrincipal()
    elif opcao == '0':
        exit(0)
    else:
        print('\033[1;41mA opção escolhida não é válida\033[m!')
        time.sleep(1)
        gestao_de_clientes()


def gestao_de_fornecedores():
    control.limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('GESTAO DE FORNECEDORES')
    print('{:^302s}\n'.format(control.IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))
    print(control.mostra_cabecalho_opcoes_menu())
    print('1. ADICIONAR NOVO FORNECEDOR\n2. LISTAR FORNECEDOR\n3. ATUALIZAR FORNECEDOR\n4. ELIMINAR FORNECEDOR\n5. VOLTAR\n0. SAIR\n')

    opcao = str(input('ESCOLHA UMA OPÇÂO: '))

    if opcao == '1':
        control.adicionar_fornecedor(control.meuCursor)
    elif opcao == '2':
        control.listar_fornecedor(control.meuCursor)
    elif opcao == '3':
        control.atualizar_fornecedor(control.meuCursor)
    elif opcao == '4':
        control.eliminar_fornecedor(control.meuCursor)
    elif opcao == '5':
        menuPrincipal()
    elif opcao == '0':
        exit(0)
    else:
        print('\033[1;41mA opção escolhida não é válida\033[m!')
        time.sleep(1)
        gestao_de_fornecedores()


if __name__ == "__main__":
     menuLogin()



# -------------------#----------------------------#
#             TESTES DO MENU                      #
# -------------------#----------------------------#
    # menuPrincipal()
    # gestao_produtos()
    # gestao_de_encomendas()
    # gerenciamento_de_compras()
    # gestao_de_utilizadores()

