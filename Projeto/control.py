# _*_ encoding:utf-8 _*_


import connectdb
from datetime import datetime
import menu
from time import sleep
from uuid import uuid4  # Importa a biblioteca para gerar um id único para o utilizador
import bcrypt  # Importa a biblioteca para comprarar o hash da senha
from random import randint
from random import choice
import validador
import re
import string

dataAtual = datetime.now()

'''CONECTA À BASE DE DADOS E É RESPONSAVEL POR ITERAR AS LINHAS E COLUNAS DA BASE DE DADOS'''
minhaBaseDados = connectdb.conectar
meuCursor = minhaBaseDados.cursor()

lista_nivelAcesso = []
ad = 0
ut = 1

# variavél que contém o formato do email válido
expressao = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# Mostra os produtos da base de dados
def listar_produtos(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 198)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 198)

    print('\033[1;32mLISTAR PRODUTOS\033[m\n\n')
    print('{:^352s}\n'.format(IDENTIFICACAO))
    print('{:^370}\n\n'.format('[7].TERMINAR SESSÃO'))

    print('-' * 196)
    print(
        '\033[1m|{:^17s}|{:^17s}|{:^26s}|{:^65s}|{:^21s}|     |{:^17s}|{:^19s}|\033[m'.format('REFERENCIA', 'CÓDIGO PRODUTO', 'NOME DO PRODUTO', 'DESCRIÇÃO',
                                                                                              'PREÇO VENDA', 'STOCK', 'STOCK MINIMO',
                                                                                              'CATEGORIA'))
    print('-' * 196)
    sql = '''SELECT * FROM produtos;'''
    cursor.execute(sql)

    for linha in cursor.fetchall():
        print('|{:^17s}|{:^17s}|{:^26s}|{:^65s}|{:^20s}€|     |{:^17s}|{:^19s}|'.format(str(linha[0]), str(linha[1]),
                                                                                        str(linha[2]), str(linha[3]),
                                                                                        str(linha[4]), str(linha[5]), str(linha[6]),
                                                                                        str(linha[7])))  # :20s limita o numero de caracteres do campo  numa string
    print('-' * 196)
    opcao_saida_para_menu_Princial()


# Adiciona um produto verificando se a referência já existe
def adicionar_produto(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mADICIONAR PRODUTOS\033[m\n\n')
    print('{:^302s}\n'.format(IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))

    identificacaoProduto = 0
    codigoProduto = gera_idVenda(identificacaoProduto)
    sql = '''INSERT INTO produtos(idProduto, codProduto, nomeProduto,descricao,precoProduto,quantProduto,minimaQuantidadeEstoque,catProduto) values (idProduto,%s,%s,%s,%s,%s,%s,%s)'''
    try:
        nome = input('Insira o nome do produto\n')[0:15]
        descricao = input('Insira a descrição do produto\n')[0:40]
        preco = float(input('Insira o preço unitário do produto\n')[0:9])
        quantidade = int(input('Insira a quantidade do produto\n')[0:8])
        quantidadeMinima = int(input('Insira a quantidade minima do produto\n')[0:8])
        categoria = input('Insira a categoria\n')[0:15]
        if nome == '' or descricao == '' or preco == '' or quantidade == '' or quantidadeMinima == '' or categoria == '':
            print('\033[1;41mOs campos não podem ser vazios!\033[m')
            sleep(1)
            atualizar_produto(cursor)
        else:
            valor = (codigoProduto, nome, descricao, preco, quantidade, quantidadeMinima, categoria)
            cursor.execute(sql, valor)
            minhaBaseDados.commit()
            print('\033[1;42mO produto foi adicionado com sucesso!\033[m')
            limpar_tela(1)
            menu.gestao_produtos()

    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        adicionar_produto(cursor)

    except Exception as ex:
        print('{:^145}'.format('\033[1;41mErro devido a {} \033[m'.format(str(ex))))
        limpar_tela(100)
        adicionar_produto(cursor)


# Atualiza um produto da base de dados
def atualizar_produto(cursor):
    limpar_tela(1)

    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_produtos(cursor)

    contador = 0
    try:
        print('\033[1;32mATUALIZAR PRODUTOS\033[m\n\n')
        codigo = str(input('Insira o código do produto que deseja atualizar\n'))
        if codigo == '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            atualizar_produto(cursor)
        else:
            procurar = 'SELECT count(*) FROM produtos WHERE codProduto=%s;'
            valor = (codigo,)
            cursor.execute(procurar, valor)

            for linha in cursor:
                contador = linha[0]
            if contador != 0:
                quantidade = int(input('Insira a quantidade do produto\n'))
                quantidadeMinima = int(input('Insira a quantidade Minima do produto\n'))
                if quantidade == '' or quantidadeMinima == '':
                    print('\033[1;41mOs campos não podem ser vazios!\033[m')
                    sleep(1)
                    atualizar_produto(cursor)
                else:
                    sql = '''UPDATE produtos SET quantProduto = quantProduto + %s, minimaQuantidadeEstoque = minimaQuantidadeEstoque + %s WHERE codProduto = %s'''
                    valor = (quantidade, quantidadeMinima, codigo)
                    cursor.execute(sql, valor)
                    minhaBaseDados.commit()
                    print(f'\033[1;42m Os Produtos foram atualizados com sucesso!\033[m')
                    limpar_tela(1)
                    atualizar_produto(cursor)
            else:
                print(f'\033[1;41m O código {codigo} do produto não existe!\033[m')
                limpar_tela(1)
                atualizar_produto(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)

        opcao_saida_para_menu_Princial()


# Elimina um produto da base de dados
def eliminar_Produto(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_produtos(cursor)
    contador = 0

    print('\033[1;32mELIMINAR PRODUTOS\033[m\n\n')
    try:
        codigo_verificar = str(input('Insira o código do produto que deseja eliminar\n'))
        codigo = verificar_campo(codigo_verificar)
        procurar = 'SELECT count(*) FROM produtos WHERE codProduto=%s;'
        valor = (codigo,)
        cursor.execute(procurar, valor)

        for linha in cursor:
            contador = linha[0]
        if contador != 0:
            sql = '''DELETE FROM produtos WHERE codProduto=%s;'''
            valor = (codigo,)
            cursor.execute(sql, valor)
            minhaBaseDados.commit()
            print(f'\033[1;42mO registro do produto com ID', meuCursor.rowcount, 'foi eliminado.\033[m')
            limpar_tela(1)
            eliminar_Produto(cursor)
        else:
            print(f'\033[1;41m O código {codigo} do produto não existe!\033[m')
            limpar_tela(1)
            eliminar_Produto(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        eliminar_Produto(cursor)


# Adiciona uma encomentda verificando se já existe alguma feita com o mesma referência
def adicionar_encomenda(cursor, data):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mADICIONAR ENCOMENDA DE PRODUTOS\033[m\n\n')
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))

    contador = 0
    nomeF = ''
    listar_produtos(cursor)

    try:
        codigoF = input('Insira o código do fornecedor já registado\n')
        if codigoF == '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            adicionar_encomenda(cursor, data)
        else:
            sql = '''SELECT count(*) from fornecedores WHERE idFornecedor=%s;'''
            valores = (codigoF,)
            cursor.execute(sql, valores)
            for linhas in cursor:
                contador = linhas[0]
            if contador != 0:
                sql = '''SELECT nomeFornecedor from fornecedores WHERE idFornecedor=%s;'''
                valor = (codigoF,)
                cursor.execute(sql, valor)
                for linhas in cursor:
                    print(f'\033[1;42m{linhas}\033[m')
                    nomeF = str(linhas[-1])

            else:
                print(f'\033[1;41mO código do fornecedor {codigoF} não se encontra registado!\033[m')
                venda_produtos(cursor, data)
    except ValueError:
        print('\033[1;41mO valor inserido não é válido!\033[m')
        venda_produtos(cursor, data)

    try:

        codigo = int(input('Insira o código do produto\n')[0:9])
        if codigo == '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            adicionar_encomenda(cursor, data)
        else:
            procurar = 'SELECT count(*) FROM encomendas WHERE codProduto=%s;'
            valor = (codigo,)
            cursor.execute(procurar, valor)

            for linha in cursor:
                contador = linha[0]
            if contador == 0:
                codigoEncomenda = gerar_codigo_encomenda()
                preco = float(input('Insira o preço por unidade do produto\n')[0:6])
                quantidade = int(input('Insira a quantidade do produto\n')[0:10])
                categoria = input('Insira a categoria do produto\n')[0:15]
                # vendaID = int(input('Insira um ID para a venda do Produto\n'))
                if preco == '' or quantidade == '' or categoria == '':
                    print('\033[1;41mOs campos não podem ser vazios!\033[m')
                    sleep(1)
                    adicionar_encomenda(cursor, data)
                else:
                    sql = '''INSERT INTO encomendas(idEncomenda, codEncomenda, codProduto, precoProduto, quantidade, fornecedor, categoria, data) values (idEncomenda, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)'''
                    valor = (codigoEncomenda, codigo, preco, quantidade, nomeF, categoria)
                    cursor.execute(sql, valor)
                    minhaBaseDados.commit()
                    sql = '''UPDATE produtos SET quantProduto=%s WHERE codProduto = %s'''
                    valor = (quantidade, codigo)
                    cursor.execute(sql, valor)
                    minhaBaseDados.commit()
                    print(f'\033[1;42m Encomenda adicionada com sucesso!\033[m')
                    opcao_saida_para_menu_Princial()
            else:
                print(f'\033[1;41m A referência {codigo} do produto já existe!\033[m')
                limpar_tela(1)
                adicionar_encomenda(cursor, data)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        adicionar_encomenda(cursor, data)


# except Exception as ex:
#    print('{:^145}'.format('\033[1;41mErro devido a {} \033[m'.format(str(ex))))
#   limpar_tela(10)
#  adicionar_encomenda(cursor, data)


# mostra as encomendas efetuadas da base de dados
def listar_encomendas(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mLISTAR ENCOMENDA DOS PRODUTOS\033[m\n\n')
    print('{:^302s}\n'.format(IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))

    print(' ' * 0, '-' * 175)
    print(' ' * 0,
          '\033[1m|{:^17s}|{:^26s}|{:^20s}|{:^21s}|{:^20s}|{:^20s}|     |{:^17s}|{:^19s}|\033[m'.format('Nº ENCOMENDA', 'CODIGO ENCOMENDA',
                                                                                                        'CÓDIGO PRODUTO',
                                                                                                        'PREÇO UNITÀRIO', 'QUANTIDADE',
                                                                                                        'FORNECEDOR',
                                                                                                        'CATEGORIA', 'DATA E HORA'))
    print(' ' * 0, '-' * 175)

    sql = '''SELECT * from encomendas'''
    cursor.execute(sql)

    for i in cursor:
        print(' ' * 0,
              '|{:^17s}|{:^26s}|{:^20s}|{:^20s}€|{:^20s}|{:^20s}|     |{:^17s}|{:^19s}|'.format(str(i[0]), str(i[1]), str(i[2]),
                                                                                                str(i[3]), str(i[4]), str(i[5]),
                                                                                                str(i[6]), str(i[7])))

    print(' ' * 0, '-' * 175)

    opcao_saida_para_menu_Princial()


# verifica se a referência do produto existe, no caso de existir da-se a quantia desejada e é calculado a total a pagar inserindo depois os dados na base de dados
def venda_produtos(cursor, data):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_produtos(cursor)
    quantidadeProduto = 0
    preco = 0
    contador = 0
    nomeC = ''

    print('\033[1;32mVENDA DE PRODUTOS\033[m\n\n')

    try:
        nif = input('Insira o número de contribuinte do cliente já registado\n')
        if nif == '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            venda_produtos(cursor, data)
        else:
            sql = '''SELECT count(*) from clientes WHERE nif=%s;'''
            valores = (nif,)
            cursor.execute(sql, valores)
            for linhas in cursor:
                contador = linhas[0]
            if contador != 0:
                sql = '''SELECT nomeCliente from clientes WHERE nif=%s;'''
                valor = (nif,)
                cursor.execute(sql, valor)
                for linhas in cursor:
                    print(f'\033[1;42m{linhas}\033[m')
                    nomeC = str(linhas[-1])
            else:
                print(f'\033[1;41mO número de identificação {nif} não se encontra registado!\033[m')
                venda_produtos(cursor, data)
    except ValueError:
        print('\033[1;41mO valor inserido não é válido!\033[m')
        venda_produtos(cursor, data)

    try:
        # id_venda = 0
        # id = gera_idVenda(id_venda)

        procurar = int(input('Insira o código do Produto\n'))
        if procurar == '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            venda_produtos(cursor, data)
        else:
            sql = '''SELECT count(*) from produtos WHERE codProduto=%s;'''
            valores = (procurar,)
            cursor.execute(sql, valores)

            for linhas in cursor:
                contador = linhas[0]
            if contador != 0:
                sql = '''SELECT * from produtos WHERE codProduto=%s;'''
                valor = (procurar,)
                cursor.execute(sql, valor)
                for linhas in cursor:
                    print(f'\033[1;42m{linhas}\033[m')
                    preco = float(linhas[4])
                    quantidadeProduto = int(linhas[5])

                quantidade = int(input('Insira a quantidade pretendida\n'))
                if procurar == '' or quantidade == '':
                    print('\033[1;41mOs campos não podem ser vazios!\033[m')
                    sleep(1)
                    venda_produtos(cursor,data)
                else:
                    if quantidade <= quantidadeProduto:
                        total = quantidade * preco
                        print(f'\033[1;42m O total a pagar é {total}€\033[m')
                        sql = '''INSERT INTO vendas values(idVenda,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)'''
                        valor = (nomeC, procurar, preco, quantidade, total)
                        cursor.execute(sql, valor)
                        sql = '''UPDATE produtos SET quantProduto=quantProduto-%s WHERE codProduto=%s'''
                        valor = (quantidade, procurar)
                        cursor.execute(sql, valor)
                        minhaBaseDados.commit()
                        sleep(2)
                        opcao_saida_para_menu_Princial()
                    else:
                        print('\033[1;41mO produto está esgotado!\033[m')
                        limpar_tela(1)
                        venda_produtos(cursor, data)
            else:
                print(f'\033[1;41mA referência {procurar} do produto nao está disponívél!\033[m')
                limpar_tela(1)
                venda_produtos(cursor, data)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        venda_produtos(cursor, data)


# Mostra os produtos que foram vendidos da base de dados
def listar_vendas_produtos(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mLISTAR VENDAS\033[m\n\n')
    print('{:^302s}\n'.format(IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))

    sql = '''SELECT * FROM vendas'''
    cursor.execute(sql)

    print(' ' * 9, '-' * 154)
    print(' ' * 9, '\033[1m|{:^17s}|{:^26s}|{:^20s}|{:^21s}|{:^18s}|{:^19s}|     |{:^19s}|\033[m'.format('Nº DE RECIBO', 'NOME CLIENTE', 'CÓDIGO PRODUTO',
                                                                                                                 'PREÇO UNIDADE',
                                                                                                                 'QUANTIDADE',
                                                                                                                 'TOTAL PAGO', 'DATA E HORA'))
    print(' ' * 9, '-' * 154)

    for x in cursor:
        print(' ' * 9,'|{:^17s}|{:^26s}|{:^20s}|{:^20s}€|{:^18s}|{:^18s}€|     |{:^17s}|'.format(str(x[0]), str(x[1]), str(x[2]), str(x[3]), str(x[4]), str(x[5]), str(x[6])))
    print(' ' * 9, '-' * 154)

    opcao_saida_para_menu_Princial()


# gera um id unico e encripta a password antes de inserir na base de dados
def adicionar_utilizador(cursor):
    contador = 0
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)
    print('\033[1;32mADICIONAR UTILIZADORES\033[m\n\n')
    try:
        identificacaoU = uuid4()
        nome = input('Insira o nome\n')
        if nome== '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            adicionar_utilizador(cursor)
        else:
            sql = '''SELECT count(*) from utilizadores WHERE nomeUtilizador=%s;'''
            valores = (nome,)
            cursor.execute(sql, valores)

            for linhas in cursor:
                contador = linhas[0]
            if contador == 0:
                password = input('Insira a password\n').encode('utf-8')  # normaliza codificando em utf-8
                # cria um salt aleatório para codificar a password
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                nivel = int(input('Insira o nivel de acesso \033[1;42mAdministrador[0]\033[m ou \033[1;42mUtilizador[1]\033[m\n'))
                # print(hash_password)
                if password == '':
                    print('\033[1;41mO campo não pode ser vazio!\033[m')
                    sleep(1)
                    adicionar_utilizador(cursor)
                else:
                    if nivel < 0 or nivel > 1:
                        print('\033[1;41m O nível de acesso deve ser 0 ou 1!\033[m')
                        limpar_tela(1)
                        adicionar_utilizador(cursor)
                    else:
                        sql = '''INSERT INTO utilizadores values(idUtilizador,%s,%s,%s,%s,CURRENT_TIMESTAMP)'''
                        valores = (str(identificacaoU), nome, hash_password, str(nivel))
                        cursor.execute(sql, valores)
                        minhaBaseDados.commit()
                        print(f'\033[1;42mFoi criado {meuCursor.rowcount} utilizador\033[m')
                        opcao_saida_para_menu_Princial()
            else:
                print(f'\033[1;41m O nome {nome} já se encontra registado!\033[m')
                limpar_tela(1)
                adicionar_utilizador(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        adicionar_utilizador(cursor)
    except Exception as ex:
        print('{:^145}'.format('\033[1;41mErro devido a {} \033[m'.format(str(ex))))
        limpar_tela(1)
        adicionar_utilizador(cursor)


# Mostra os utilizadores inseridos da base de dados
def listar_utilizadores(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mLISTAR UTILIZADORES\033[m\n\n')
    print('{:^302s}\n'.format(IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))

    sql = '''SELECT idUtilizador, nomeUtilizador, passwordUtilizador FROM utilizadores'''
    cursor.execute(sql)
    print(' ' * 17, '-' * 140)
    print(' ' * 17, '\033[1m|{:^36s}|{:^20s}|{:^80s}|\033[m'.format('ID', 'UTILIZADOR', 'PASSWORD'))
    print(' ' * 17, '-' * 140)
    for i in cursor:
        print(' ' * 17, '|{:^36s}|{:^20s}|{:^80}|'.format(str(i[0]), str(i[1]), str(i[2])))
    print(' ' * 17, '-' * 140)
    opcao_saida_para_menu_Princial()


# Atualiza um cliente da base de dados
def atualizar_utilizador(cursor):
    limpar_tela(1)

    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_utilizadores(cursor)

    contador = 0
    try:
        print('\033[1;32mATUALIZAR UTILIZADOR\033[m\n\n')
        nome = input('Insira o nome do utilizador para alterar a password\n')
        if nome=='':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            atualizar_utilizador(cursor)
        else:
            procurar = 'SELECT count(*) FROM utilizadores WHERE nomeUtilizador=%s;'
            valor = (nome,)
            cursor.execute(procurar, valor)

            for linha in cursor:
                contador = linha[0]
            if contador != 0:
                password = input('Insira a nova password\n').encode('utf-8')
                # cria um salt aleatório para codificar a password
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                if nome == '' or password == '':
                    print('\033[1;41mOs campos não podem ser vazios!\033[m')
                    sleep(1)
                    atualizar_utilizador(cursor)
                else:
                    sql = '''UPDATE utilizadores SET passwordUtilizador = %s WHERE nomeUtilizador=%s'''.format(str(hash_password))
                    valor = (hash_password, nome)
                    cursor.execute(sql, valor)
                    minhaBaseDados.commit()
                    print(f'\033[1;42m Os dados do utilizador foram atualizados com sucesso!\033[m')
                    limpar_tela(1)
                    atualizar_utilizador(cursor)
            else:
                print(f'\033[1;41m O nome {nome} do utilizador não existe!\033[m')
                limpar_tela(1)
                atualizar_utilizador(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)

    opcao_saida_para_menu_Princial()


# Elimina um cliente da base de dados
def eliminar_utilizador(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_utilizadores(cursor)
    contador = 0
    print('\033[1;32mELIMINAR UTILIZADORES\033[m\n\n')
    try:
        codigo_verificar = int(input('Insira o ID do utilizador que deseja eliminar\n'))
        codigo = verificar_campo(codigo_verificar)
        procurar = 'SELECT count(*) FROM utilizadores WHERE idUtilizador=%s;'
        valor = (codigo,)
        cursor.execute(procurar, valor)

        for linha in cursor:
            contador = linha[0]
        if contador != 0:
            sql = '''DELETE FROM utilizadores WHERE idUtilizador = %s;'''
            valor = (codigo,)
            cursor.execute(sql, valor)
            minhaBaseDados.commit()
            print(f'\033[1;42mA conta do utilizador com o ID', codigo, 'foi eliminada com sucesso.\033[m')
            limpar_tela(1)
            eliminar_utilizador(cursor)
        else:
            print(f'\033[1;41m O ID do utilizador {codigo}  não está registado!\033[m')
            limpar_tela(1)
            eliminar_utilizador(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        eliminar_utilizador(cursor)


def adicionar_cliente(cursor):
    limpar_tela(1)
    nif = ''
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mDADOS PARA REGISTRO DO NOVO CLIENTE\033[m\n\n')
    try:
        nome = input('Insira o nome do cliente\n').capitalize()
        nif_verificar = input('Insira o número fiscal do cliente\n').capitalize()
        if validador.controlNIF(nif_verificar) == True:
            nif = nif_verificar
        else:
            print(f'\033[1;41m O Número Fiscal {nif_verificar} é inválido!\033[m')
            adicionar_cliente(cursor)
        morada = input('Insira a morada do cliente\n').capitalize()
        localidade = input('Insira a localidade do cliente\n').capitalize()
        codigoPostal_validar = input('Insira o código postal do cliente\n').capitalize()
        codigoPostal = verificar_codigo_postal(codigoPostal_validar, cursor)
        telefone_validar = input('Insira o telefone do cliente\n').capitalize()
        telefone = verificar_numero_telefone_cliente(telefone_validar, cursor)
        if nome == '' or nif == '' or morada == '' or localidade == '' or codigoPostal_validar == '' or telefone_validar == '':
            print('\033[1;41mOs campos não podem ser vazios!\033[m')
            sleep(1)
            adicionar_cliente(cursor)
        else:
            sql = '''INSERT INTO clientes values(idCliente,%s,%s,%s,%s,%s,%s)'''
            valores = (nome, nif, morada, localidade, codigoPostal, telefone)
            cursor.execute(sql, valores)
            minhaBaseDados.commit()
            print(f'\033[1;42mFoi criado {meuCursor.rowcount} cliente\033[m')
            opcao_saida_para_menu_Princial()
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        adicionar_cliente(cursor)
    except Exception as ex:
        print('{:^145}'.format('\033[1;41mErro devido a {} \033[m'.format(str(ex))))
        limpar_tela(1)
        adicionar_cliente(cursor)


# Mostra os utilizadores inseridos da base de dados
def listar_clientes(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 190)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 190)

    print('\033[1;32mLISTAR CLIENTES\033[m\n\n')
    print('{:^302s}\n'.format(IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))

    sql = '''SELECT * FROM clientes'''
    cursor.execute(sql)
    print(' ' * 0, '-' * 188)
    print(' ' * 0, '\033[1m|{:^30s}|{:^20s}|{:^20s}|{:^40s}|{:^30s}|{:^20s}|{:^20s}|\033[m'.format('ID CLIENTE', 'NOME', 'NIF', 'MORADA', 'LOCALIDADE', 'CÓDIGO POSTAL', 'Nº TELEFONE'))
    print(' ' * 0, '-' * 188)
    for i in cursor:
        print(' ' * 0, '|{:^30s}|{:^20s}|{:^20s}|{:^40s}|{:^30s}|{:^20s}|{:^20s}|'.format(str(i[0]), str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6])))
    print(' ' * 0, '-' * 188)
    opcao_saida_para_menu_Princial()


# Atualiza um cliente da base de dados
def atualizar_clientes(cursor):
    limpar_tela(1)
    c=''
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_clientes(cursor)

    contador = 0
    print('\033[1;32mATUALIZAR CLIENTE\033[m\n\n')
    try:
        codigo = input('Insira o número de identificação fiscal do cliente que deseja atualizar\n')
        if codigo == '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            atualizar_clientes(cursor)
        else:
            if validador.controlNIF(codigo) == True:
                c = codigo
            else:
                print(f'\033[1;41m O Número Fiscal {codigo} é inválido!\033[m')
                adicionar_cliente(cursor)
            procurar = 'SELECT count(*) FROM clientes WHERE nif=%s;'
            valor = (c,)
            cursor.execute(procurar, valor)

            for linha in cursor:
                contador = linha[0]
            if contador != 0:
                morada = input('Insira a nova morada\n')

                localidade = input('Insira a nova localidade\n')

                codigoPostal_validar = input('Insira o novo código Postal\n')
                codigoPostal = verificar_codigo_postal_atualizar(codigoPostal_validar, cursor)

                telefone_validar = input('Insira o novo número de telefone\n')
                telefone = verificar_numero_telefone_cliente_atualizar(telefone_validar, cursor)
                if morada == '' or localidade == '' or codigoPostal_validar == '' or telefone_validar == '':
                    print('\033[1;41mOs campos não podem ser vazios!\033[m')
                    sleep(1)
                    adicionar_cliente(cursor)
                else:
                    sql = '''UPDATE clientes SET moradaCliente = %s, localidadeCliente = %s,  telefoneCliente = %s, codigoPostalCliente = %s WHERE nif=%s'''
                    valor = (morada, localidade, telefone, codigoPostal, codigo)
                    cursor.execute(sql, valor)
                    minhaBaseDados.commit()
                    print(f'\033[1;42m Os dados do cliente foram atualizados com sucesso!\033[m')
                    limpar_tela(1)
                    atualizar_clientes(cursor)
            else:
                print(f'\033[1;41m O número de identificação fiscal {codigo} do cliente não existe!\033[m')
                limpar_tela(1)
                atualizar_clientes(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)

    opcao_saida_para_menu_Princial()


# Elimina um cliente da base de dados
def eliminar_Cliente(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_clientes(cursor)
    contador = 0
    print('\033[1;32mELIMINAR CLIENTE\033[m\n\n')
    try:
        codigo_verificar = int(input('Insira o número de identificação fiscal do cliente que deseja eliminar\n'))
        codigo = verificar_campo(codigo_verificar)
        procurar = 'SELECT count(*) FROM clientes WHERE nif=%s;'
        valor = (codigo,)
        cursor.execute(procurar, valor)

        for linha in cursor:
            contador = linha[0]
        if contador != 0:
            sql = '''DELETE FROM clientes WHERE nif = %s;'''
            valor = (codigo,)
            cursor.execute(sql, valor)
            minhaBaseDados.commit()
            print(f'\033[1;42mO registro do cliente', meuCursor.rowcount, 'foi eliminado.\033[m')
            limpar_tela(1)
            eliminar_Cliente(cursor)
        else:
            print(f'\033[1;41m O número de identificação fiscal {codigo} do cliente não existe!\033[m')
            limpar_tela(1)
            eliminar_Cliente(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        eliminar_Cliente(cursor)


def adicionar_fornecedor(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mDADOS PARA REGISTRO DO NOVO FORNECEDOR\033[m\n\n')
    try:
        nome = input('Insira o nome do fornecedor\n').capitalize()
        telefone_verificar = input('Insira o número de telefone do fornecedor\n')
        telefone = verificar_numero_telefone_fornecedor(telefone_verificar, cursor)
        email_verificar = input('Insira o email do fornecedor\n')
        email = verificar_email_fornecedor(email_verificar, cursor)
        if nome == '' or telefone_verificar == '' or email_verificar == '':
            print('\033[1;41mOs campos não podem ser vazios!\033[m')
            sleep(1)
            adicionar_fornecedor(cursor)
        else:
            sql = '''INSERT INTO fornecedores values(idFornecedor,%s,%s,%s)'''
            valores = (nome, telefone, email)
            cursor.execute(sql, valores)
            minhaBaseDados.commit()
            print(f'\033[1;42mFoi criado {meuCursor.rowcount} fornecedor\033[m')
            opcao_saida_para_menu_Princial()
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        adicionar_fornecedor(cursor)
    except Exception as ex:
        print('{:^145}'.format('\033[1;41mErro devido a {} \033[m'.format(str(ex))))
        limpar_tela(1)
        adicionar_fornecedor(cursor)


# Mostra os utilizadores inseridos da base de dados
def listar_fornecedor(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    print('\033[1;32mLISTAR FORNECEDORES\033[m\n\n')
    print('{:^302s}\n'.format(IDENTIFICACAO))
    print('{:^330}\n\n'.format('[7].TERMINAR SESSÃO'))

    sql = '''SELECT * FROM fornecedores'''
    cursor.execute(sql)
    print(' ' * 23, '-' * 115)
    print(' ' * 23, '\033[1m|{:^30s}|{:^20s}|{:^20s}|{:^40s}|\033[m'.format('ID FORNECEDOR', 'NOME FORNECEDOR', 'TELEFONE', 'EMAIL'))
    print(' ' * 23, '-' * 115)
    for i in cursor:
        print(' ' * 23, '|{:^30s}|{:^20s}|{:^20s}|{:^40s}|'.format(str(i[0]), str(i[1]), str(i[2]), str(i[3])))
    print(' ' * 23, '-' * 115, '\n')
    opcao_saida_para_menu_Princial()


# Atualiza um cliente da base de dados
def atualizar_fornecedor(cursor):
    limpar_tela(1)

    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_fornecedor(cursor)

    contador = 0
    print('\033[1;32mATUALIZAR FORNECEDOR\033[m\n\n')
    try:
        nomeF = input('Insira o nome do fornecedor que deseja atualizar\n')
        if nomeF == '':
            print('\033[1;41mO campo não pode ser vazio!\033[m')
            sleep(1)
            atualizar_fornecedor(cursor)
        else:
            procurar = 'SELECT count(*) FROM fornecedores WHERE nomeFornecedor=%s;'
            valor = (nomeF,)
            cursor.execute(procurar, valor)

            for linha in cursor:
                contador = linha[0]
            if contador != 0:
                telefone_validar = input('Insira o novo número de telefone\n')
                telefone = verificar_numero_telefone_fornecedor(telefone_validar, cursor)
                email_validar = input('Insira o novo email\n')
                email = verificar_email_fornecedor(email_validar, cursor)
                if nomeF == '' or telefone_validar == '' or email_validar == '':
                    print('\033[1;41mOs campos não podem ser vazios!\033[m')
                    sleep(1)
                    atualizar_fornecedor(cursor)
                else:
                    sql = '''UPDATE fornecedores SET telefoneFornecedor = %s, emailFornecedor = %s WHERE nomeFornecedor=%s'''
                    valor = (telefone, email, nomeF)
                    cursor.execute(sql, valor)
                    minhaBaseDados.commit()

                    print(f'\033[1;42m Os dados do fornecedor foram atualizados com sucesso!\033[m')
                    limpar_tela(1)
                    atualizar_fornecedor(cursor)
            else:
                print(f'\033[1;41m O nome do fornecedor {nomeF} não se encontra registado!\033[m')
                limpar_tela(1)
                atualizar_fornecedor(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)

    opcao_saida_para_menu_Princial()


# Elimina um cliente da base de dados
def eliminar_fornecedor(cursor):
    limpar_tela(1)
    print('\033[1m*\033[m' * 178)
    print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
    print('\033[1m*\033[m' * 178)

    listar_fornecedor(cursor)
    contador = 0
    print('\033[1;32mELIMINAR FORNECEDOR\033[m\n\n')
    try:
        idF = input('Insira o ID do fornecedor que deseja eliminar\n')
        procurar = 'SELECT count(*) FROM fornecedores WHERE idFornecedor=%s;'
        valor = (idF,)
        cursor.execute(procurar, valor)

        for linha in cursor:
            contador = linha[0]
        if contador != 0:
            sql = '''DELETE FROM fornecedores WHERE idFornecedor=%s;'''
            valor = (idF,)
            cursor.execute(sql, valor)
            minhaBaseDados.commit()
            print(f'\033[1;42mO registro do fornecedor com o ID', idF, 'foi eliminado.\033[m')
            limpar_tela(1)
            eliminar_fornecedor(cursor)
        else:
            print(f'\033[1;41m O fornecedor com o ID {idF} não se encontra registado!\033[m')
            limpar_tela(1)
            eliminar_fornecedor(cursor)
    except ValueError:
        print(f'\033[1;41m O valor inserido não é válido!\033[m')
        limpar_tela(1)
        eliminar_fornecedor(cursor)


# faz o login do utilizador, no caso de o hash da password ser igual ele entra para o menu principal
def logar(cursor):
    contador = 0
    try:
        print(' ' * 75, '\033[1;32mUTILIZADOR\033[m')
        utilizador = input('{:^74s}->'.format(' '))[0:10]
        print(' ' * 75, ' \033[1;32mPASSWORD\033[m')
        password = input('{:^74s}->'.format(' ')).encode('utf-8')

        if utilizador == '' and password == '':
            print(' ' * 48, end='')
            print(' \033[1;41mVoçê deve preencher os campos!\033[m')
            sleep(1)
            menu.menuLogin()
        else:
            procurar = 'SELECT count(*) FROM utilizadores WHERE nomeUtilizador=%s;'
            valor = (utilizador,)
            cursor.execute(procurar, valor)

            for linha in cursor:
                contador = linha[0]
            if contador != 0:
                sql = '''SELECT passwordUtilizador FROM utilizadores WHERE nomeUtilizador=%s'''
                valores = (utilizador,)
                cursor.execute(sql, valores)
                dados = cursor.fetchone()
                hash_password = str(dados[0]).encode('utf-8')
                if bcrypt.hashpw(password,
                                 hash_password) == hash_password:  # verifica se o hash da base de dados é igual ao hash da password digitada

                    verifica_nivel_de_acesso(cursor, utilizador)
                else:
                    print('{:^172}'.format('\033[1;41mA Password é inválido/a!\033[m'))
                    limpar_tela(1)
                    menu.menuLogin()
            else:
                print('{:^172}'.format('\033[1;41mO Utilizador é inválido/a!\033[m'))
                limpar_tela(1)
                menu.menuLogin()
    except Exception as ex:
        print('{:^175}'.format('\033[1;41mErro devido a {} \033[m'.format(str(ex))))
        limpar_tela(10)
        menu.menuLogin()


# Faz um espaçamento para simular um clear
def limpar_tela(segundos):
    sleep(segundos)
    print('\n' * 100)


# permite escolher várias opções  para voltar para o menu principal
def opcao_saida_para_menu_Princial():
    sleep(1)
    opcao = input('VOLTAR AO MENU PRINCIPAL [S/N]\n').lower()
    if opcao == 's':
        limpar_tela(1)
        menu.menuPrincipal()
    elif opcao == 'n':
        print()
    else:
        opcao_saida_para_menu_Princial()


# def cabecalho_do_programa():
#   print('\033[1m*\033[m' * 178)
#  print('{:^170}'.format('\033[1mGESTOR DE STOCK DE PEÇAS INFORMÁTICAS\033[m'))
# print('\033[1m*\033[m' * 178)


def mostra_identificacao(cursor, nome):
    global IDENTIFICACAO
    mostra_ident = ''

    # print('Estou aqui',nome)
    sql = '''SELECT identificacao, nomeUtilizador FROM utilizadores WHERE nomeUtilizador=%s'''
    valores = (nome,)
    cursor.execute(sql, valores)
    dados = cursor.fetchone()

    if int(str(lista_nivelAcesso)[1:-1]) == 0:
        mostra_ident = str('{}'.format('\033[1;32mADMINISTRADOR\033[m'))
    elif int(str(lista_nivelAcesso)[1:-1]) == 1:
        mostra_ident = str('{}'.format('\033[1;32mUTILIZADOR\033[m'))
    IDENTIFICACAO = f'\033[1;32mID: \033[m' + f' \033[1;32m{mostra_ident}: \033[m'.join(dados)

    # print(IDENTIFICACAO)


# Gera um novo id sem repetir os números
def gera_idVenda(id):
    id_guardado = []
    while len(id_guardado) != 1:
        id_gerado = randint(0000000, 9999999)
        if id_gerado not in id_guardado:
            id_guardado.append(id_gerado)
    id = int(str(id_guardado)[
             1:-1])  # converte a lista em string depois em inteiro e remove os parentises na posição 1 e na final
    return id


# Verifica o nível de acesso do utilizador e retorna para o menu com a devida permissão
def verifica_nivel_de_acesso(cursor, utilizador):
    sql = '''SELECT nivelAcesso FROM utilizadores WHERE nomeUtilizador=%s'''
    valores = (utilizador,)
    cursor.execute(sql, valores)
    dados = cursor.fetchone()
    nivel = int(str(dados[0]))  # converte os dados do nivel de acesso na base de dados em inteiro
    lista_nivelAcesso.append(nivel)

    # print(nivel)
    print('{:^172}'.format('\033[1;42mO Login efetuado com sucesso!\033[m'))
    limpar_tela(1)

    mostra_identificacao(cursor, utilizador)
    menu.menuPrincipal()


def verificar_numero_telefone_cliente(numero, cursor):
    if len(numero) == 8 or len(numero) == 9:
        return numero
    else:
        print(f'\033[1;41m O número de telefone {numero} é inválido\033[m!')
        sleep(1)
        adicionar_cliente(cursor)

def verificar_numero_telefone_cliente_atualizar(numero, cursor):
    if len(numero) == 8 or len(numero) == 9:
        return numero
    else:
        print(f'\033[1;41m O número de telefone {numero} é inválido\033[m!')
        sleep(1)
        atualizar_clientes(cursor)


def verificar_numero_telefone_fornecedor(numero, cursor):
    if len(numero) == 8 or len(numero) == 9:
        return numero
    else:
        print(f'\033[1;41m O número de telefone {numero} é inválido\033[m!')
        sleep(1)
        adicionar_fornecedor(cursor)

def verificar_numero_telefone_fornecedor_atualizar(numero, cursor):
    if len(numero) == 8 or len(numero) == 9:
        return numero
    else:
        print(f'\033[1;41m O número de telefone {numero} é inválido\033[m!')
        sleep(1)
        atualizar_fornecedor(cursor)





def verificar_codigo_postal(numero, cursor):
    if len(numero) == 8 and numero[4] == '-':
        return numero
    else:
        print(f'\033[1;41m O código postal {numero} é inválido\033[m!')
        sleep(1)
        adicionar_cliente(cursor)


def verificar_codigo_postal_atualizar(numero, cursor):
    if len(numero) == 8 and numero[4] == '-':
        return numero
    else:
        print(f'\033[1;41m O código postal {numero} é inválido\033[m!')
        sleep(1)
        atualizar_clientes(cursor)


def verificar_email(email, cursor):
    if re.match(expressao, email):
        return email
    else:
        print(f'\033[1;41m O email {email} é inválido\033[m!')
        sleep(1)
        adicionar_cliente(cursor)


def verificar_email_fornecedor(email, cursor):
    if re.match(expressao, email):
        return email
    else:
        print(f'\033[1;41m O email {email} é inválido\033[m!')
        sleep(1)
        adicionar_fornecedor(cursor)


# gera o id de encomendas de 8 digitos
def gerar_codigo_encomenda():
    caracteres = string.ascii_uppercase + string.digits
    tamanho = 8
    return ''.join(choice(caracteres) for x in range(tamanho))


# funcão que verifica se os campos estão vazios
def verificar_campo(campo):
    if campo !='':
        return campo
    else:
        return


def mostra_cabecalho_opcoes_menu():
    return str('{}'.format('---------------------------------\n          \033[1;32mMENU OPÇÕES\033[m\n---------------------------------'))

# -------------------#----------------------------#
#             TESTES DE CONTROLO                 #
# -------------------#----------------------------#
# print(logar(meuCursor))
# print(gera_idVenda(id))
# print(mostra_identificacao(meuCursor,nome))#print(logar(meuCursor))
# print(listar_utilizadores(meuCursor))
# print(adicionar_utilizador(meuCursor))
# print(venda_produtos(meuCursor,dataAtual))
# print(listar_encomendas(meuCursor))
# print(adicionar_encomenda(meuCursor,dataAtual))
# print((eliminar_Produto(meuCursor)))
# print(atualizar_produto(meuCursor))
# print(adicionar_produto(meuCursor))
# print(listar_produtos(meuCursor))
# print(listar_vendas_produtos(meuCursor))
# print(listar_clientes(meuCursor))


# tipoPagamento = input('Qual das formas deseja pagar? MULTIBANCO[M] MB WAY[W] DINHEIRO[D]\n')
#                if tipoPagamento == 'M'.lower():
#                    tipo = 'MULTIBANCO'
#                    print(tipo)
#                    pagamento = float(input('Insira o montante a pagar pela venda\n'))
#                    if pagamento == total:
#                        print(f'\033[1;42mA venda de {total}€ foi efetuada com sucesso!\033[m')
#                        sleep(2)
#                    else:
#                        print(f'\033[1;41mA venda de {total}€ não pode ser concluída\033[m')
#                        venda_produtos(cursor, data)
#
#                elif tipoPagamento == 'W'.lower():
#                    tipo = 'MB WAY'
#                    print(tipo)
#                    pagamento = float(input('Insira o montante a pagar pela venda\n'))
#                    if pagamento == total:
#                        print(f'\033[1;42mA venda de {total}€ foi efetuada com sucesso!\033[m')
#                        sleep(2)
#                    else:
#                        print(f'\033[1;41mA venda de {total}€ não pode ser concluída\033[m')
#                        venda_produtos(cursor, data)
#
#                elif tipoPagamento == 'D'.lower():
#                    tipo = 'DINHEIRO'
#                    print(tipo)
#                    pagamento = float(input('Insira o montante a pagar pela venda\n'))
#                    if pagamento == total:
#                        print(f'\033[1;42mA venda de {total}€ foi efetuada com sucesso!\033[m')
#                        sleep(2)
#                    else:
#                        print(f'\033[1;41mA venda de {total}€ não pode ser concluída\033[m')
#                        venda_produtos(cursor, data)
