import time

from leitura.leitura import printar
from transformar.transformarbinario import decimal_para_binario_com_20_bits
from tabelaPagina.tabelapagina import criar_tabela

tamanho_pagina = 1024
tamanho_quadro = 1024
tamanho_memoria_fisica = 2048
tamanho_memoria_secundaria = 67108864
tabelas_paginas = []
tabela_secundaria = []
tabela_fisica = []
ultimos_acessos = []
quantidade_quadros_secundaria = int(tamanho_memoria_secundaria/tamanho_quadro)
quantidade_quadros_fisica = int(tamanho_memoria_fisica/tamanho_quadro)

for i in range(quantidade_quadros_secundaria):
    tabela_secundaria.append("-")

for i in range(quantidade_quadros_fisica):
    tabela_fisica.append("-")
    ultimos_acessos.append("-")

arq = open("/home/leandro/PycharmProjects/SO/teste.txt")
linhas = arq.readlines()
contador = 0
for linha in linhas:
    contador +=1
    time.sleep(2)
    printar(tabela_fisica)
    printar(tabela_secundaria)
    printar(tabelas_paginas)
    partes = linha.split(" ")
    if partes[1] == 'C': # Caso crie um Processo
        quantidade_quadros_processo = int(partes[2]) # Pega a quantidade de quadros do processo
        valor_pagina = 0 # Valor pagina atual
        for i in range(quantidade_quadros_secundaria): # Aloca os quadros do processo na memoria secundaria
            if (tabela_secundaria[i] == "-") & (quantidade_quadros_processo > 0):
                tabela_secundaria[i] = partes[0] + " - pagina " + str(valor_pagina)
                quantidade_quadros_processo -= 1
                valor_pagina += 1
        tabelas_paginas.append(criar_tabela(partes[0], partes[2], 1024)) # Cria a tabela de pagina do processo
        tamanho_memoria_secundaria -= int(partes[2]) # Diminui o espaço liberado da memoria secundaria
    else:
        if partes[1][0] == 'T': # Caso encerre o processo
            print("Encerrando o processo "+partes[0])
            for g in range(len(tabelas_paginas)): #Percorre a tabela de paginas
                if partes[0] == tabelas_paginas[g][0]: # Acha a tabela de pagina do processo
                    paginas = tabelas_paginas[g]
                    for q in range(len(paginas)):
                        if q!= 0:
                            if paginas[q][1] == 1: # Verifica se o bit de modificaçao da pagina eh 1
                                print("Preciso atualizar na memoria secundaria") #Caso seja atualiza ele na memoria secundaria
                                quadro_atualizado = tabela_fisica[paginas[q][2]]
                                for u in range(len(tabela_secundaria)):
                                    quadro_desatualizado = tabela_secundaria[u]
                                    if quadro_desatualizado == quadro_atualizado:
                                        tabela_secundaria[u] = quadro_atualizado
                            if paginas[q][2] != "-": #Caso nao seja,apenas exclui o quadro da tabela principal
                                tabela_fisica[int(paginas[q][2])] = "-"
                                ultimos_acessos[int(paginas[q][2])] = "-"
                    del tabelas_paginas[g] # Exclui a tabela de pagina daquele processo
                    break
        else:
            endereco = partes[2][1:-3]
            endereco_logico = decimal_para_binario_com_20_bits(int(endereco))  # Transforma o endereco para binario
            numero_pagina = endereco_logico[0:10]  # Separa o numero da pagina
            offset = endereco_logico[10::]  # Separa o offset
            for p in range(len(tabelas_paginas)):  # Procura a tabela de processo na tabela de todos os processos
                if tabelas_paginas[p][0] == partes[0]:
                    pagina = tabelas_paginas[p][
                        int(numero_pagina, 2) + 1]# Pega a pagina do processo na tabela no processo
                    if pagina[2] == "-":  # Se o quadro estiver vazio da pagina, a pagina nao esta na memoria principal
                        quadro_tabela_fisica = -1
                        for k in range(len(tabela_secundaria)):  # Procura na memoria secundaria a pagina
                            quadro_secundaria = tabela_secundaria[k].split(" ")
                            if quadro_secundaria[0] != '-':
                                if (quadro_secundaria[0] == partes[0]) & (int(quadro_secundaria[3]) == int(numero_pagina, 2)):
                                    for x in range(len(tabela_fisica)):  # Coloca na memoria principal se tiver espaço
                                        if tabela_fisica[x] == "-":
                                            tabela_fisica[x] = tabela_secundaria[k]
                                            ultimos_acessos[x] = contador
                                            quadro_tabela_fisica = x
                                            print("Pegamos a pagina na memoria secundaria")
                                            break
                                        if x == len(tabela_fisica)-1: # Caso a memoria principal esteja cheia
                                            print("Memoria principal esta cheia")
                                            menor = 1000000000000000000000000
                                            ind = -1
                                            for t in range(len(ultimos_acessos)): #Percorre a lista dos ultimos acessos dos quadros da tabela principal e acha o mais antigo
                                                if (menor > ultimos_acessos[t]):
                                                    menor = ultimos_acessos[t]
                                                    ind = t
                                            quadro_substituido = tabela_fisica[ind]
                                            for g in range(len(tabelas_paginas)): # Percorre a tabela de paginas
                                                if tabelas_paginas[g][0] == quadro_substituido[0:2]: #Encontra a tabela de pagina daquele processo
                                                    for z in range(len(tabelas_paginas[g])):
                                                        if z != 0:
                                                            if tabelas_paginas[g][z][2] == ind:
                                                                if tabelas_paginas[g][z][1] == 1: # Se for igual a 1 o bit de modificacao ,precisamos atualizar na memoria secundaria
                                                                    for h in range(len(tabela_secundaria)):
                                                                        if tabela_secundaria[h] == quadro_substituido:
                                                                            tabela_secundaria[h] = quadro_substituido
                                                                tabelas_paginas[g][z][0] = 0 # Atualizamos os valores na tabela de pagina
                                                                tabelas_paginas[g][z][1] = 0
                                                                tabelas_paginas[g][z][2] = "-"
                                            tabela_fisica[ind] = tabela_secundaria[k] # Substituimos o novo quadro na tabela principal
                                            ultimos_acessos[ind] = contador # Atualizamos o valor no ultimo acesso
                                            quadro_tabela_fisica = ind

                        tabelas_paginas[p][int(numero_pagina, 2) + 1][0] = 1 # Atualizamos o valor na tabela de pagina
                        tabelas_paginas[p][int(numero_pagina, 2) + 1][2] = quadro_tabela_fisica
                    if (pagina[0] == 1) & (pagina[1] == 0):  # A pagina esta na memoria principal
                        print("Esta na memoria principal")
                        ultimos_acessos[int(pagina[2])] = contador
                    if (pagina[0] == 1) & (pagina[1] == 1):  # A pagina na memoria secundaria precisa ser atualizada
                        print("A pagina precisa ser atualizada na memoria secundaria")
                        ultimos_acessos[int(pagina[2])] = contador
                        for y in range(len(tabela_secundaria)): # Atualizamos na memoria secundaria
                            if tabela_secundaria[y] == tabela_fisica[pagina[2]]:
                                tabela_secundaria[y] = tabela_fisica[pagina[2]]
                        pagina[1] = 0
                    if partes[1] == 'P':  # Caso a instruçao a ser executada
                        print("Executando a instruçao " + partes[0] + " no endereco logico(" + endereco + ")2")
                        break
                    if partes[1] == 'R':  # Caso seja uma instruçao de leitura
                        print("Lendo a instruçao " + partes[0] + " no endereco logico(" + endereco + ")2")
                        break
                    if partes[1] == 'W': # Caso seja uma instruçao de escrita
                        print("Escrevendo a instrucao " + partes[0]+" no endereco logico("+endereco+")2")
                        if tabelas_paginas[p][int(numero_pagina, 2) + 1][0] == 1:
                            tabelas_paginas[p][int(numero_pagina, 2) + 1][1] = 1
                        break
                    if partes[1] == 'I':
                        print("Executando a instruçao de I/O " + partes[0] + " no endereco logico(" + endereco + ")2")
                        print("Ocorre um swapper ")
                        for j in range(len(tabela_fisica)): #Percorremos a memoria fisica
                            if partes[0] == tabela_fisica[j][0:2]: # Achamos o processo
                                for d in range(len(tabelas_paginas)):
                                    if tabelas_paginas[d][0] == partes[0]:
                                        pag = tabelas_paginas[d][int(tabela_fisica[j][-1])+1]
                                        if pag[1] == 0:
                                            tabela_fisica[j] = "-"
                                            ultimos_acessos[j] = "-"
                                            pag[0] = 0
                                            pag[1] = 0
                                            pag[2] = "-"
                                        else:
                                            for u in range(len(tabela_secundaria)):
                                                if tabela_secundaria[u] == tabela_fisica[j]:
                                                    tabela_secundaria[u] = tabela_fisica[j]
                                            pag[0] = 0
                                            pag[1] = 0
                                            pag[2] = "-"
                        break

