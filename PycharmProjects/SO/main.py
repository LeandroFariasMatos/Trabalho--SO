import time

from transformar.transformarbinario import decimal_para_binario_com_20_bits
from tabelaPagina.tabelapagina import criar_tabela

tamanho_pagina = 1024
tamanho_quadro = 1024
tamanho_memoria_fisica = 4194304
tamanho_memoria_secundaria = 67108864
tabelas_paginas = []
tabela_secundaria = []
tabela_fisica = []
quantidade_quadros_secundaria = int(tamanho_memoria_secundaria/tamanho_quadro)
quantidade_quadros_fisica = int(tamanho_memoria_fisica/tamanho_quadro)

import tkinter as tk
from tkinter import messagebox
def adicionar_memoria_secundaria(processo, index):
    # Obtém o texto digitado no Entry e adiciona à Listbox
    if index is None:
        GUI_memoria_secundaria.insert(tk.END, processo)
    else:
        GUI_memoria_secundaria.insert(index, processo)

def remover_memoria_secundaria(processo):
    # Remove o item selecionado na Listbox
    for i in range(len(GUI_memoria_secundaria)):
        if GUI_memoria_secundaria[i] == processo:
            GUI_memoria_secundaria[i] = "-"

def adicionar_memoria_principal(processo, index):
    # Obtém o texto digitado no Entry e adiciona à Listbox
    if index is None:
        GUI_memoria_principal.insert(tk.END, processo)
    else:
        GUI_memoria_principal.insert(index, processo)

def remover_memoria_principal(processo):
    # Remove o item selecionado na Listbox
    for i in range(len(GUI_memoria_principal)):
        if GUI_memoria_principal[i] == processo:
            GUI_memoria_principal[i] = "-"

def adicionar_tabelas_paginas(processo, index, page, quadro):
    # Obtém o texto digitado no Entry e adiciona à Listbox
    if index is None:
        GUI_tabelas_paginas.insert(tk.END, processo)
    #Estou comecando a fazer as tabelas de paginas
    # else:
    #     pagina_antiga = GUI_tabelas_paginas.get(index)
    #     pagina_antiga[page][0] = 1
    #     pagina_antiga[page][2] = quadro


def remover_tabelas_paginas(processo):
    # Remove o item selecionado na Listbox
    for i in range(GUI_tabelas_paginas.size()):
        if GUI_tabelas_paginas.index(i) == processo:
            GUI_tabelas_paginas.insert(i,"-")

def atualizar_janela():
    janela.update()

# Criar janela principal
janela = tk.Tk()
janela.title("Exemplo de Lista")

labelMemoriaSecundaria = tk.Label(janela, text="Memoria Secundaria:")
labelMemoriaSecundaria.pack()

labelTamanhoSecundaria = tk.Label(janela, text=tamanho_memoria_secundaria)
labelTamanhoSecundaria.pack()

# Criar Listbox
GUI_memoria_secundaria = tk.Listbox(janela, selectmode=tk.SINGLE)
GUI_memoria_secundaria.pack(pady=10)

labelMemoriaPrincipal = tk.Label(janela, text="Memoria Principal:")
labelMemoriaPrincipal.pack()

labelTamanhoPrincipal = tk.Label(janela, text=tamanho_memoria_fisica)
labelTamanhoPrincipal.pack()
# Criar Listbox
GUI_memoria_principal = tk.Listbox(janela, selectmode=tk.SINGLE)
GUI_memoria_principal.pack(pady=10)

labelTabelasPaginas = tk.Label(janela, text="Tabelas Paginas:")
labelTabelasPaginas.pack()

# Criar Listbox
GUI_tabelas_paginas = tk.Listbox(janela, selectmode=tk.SINGLE)
GUI_tabelas_paginas.pack(pady=10)

for i in range(quantidade_quadros_secundaria):
    tabela_secundaria.append("-")
    adicionar_memoria_secundaria("-", None)

for i in range(quantidade_quadros_fisica):
    tabela_fisica.append("-")
    adicionar_memoria_principal("-", None)

arq = open("/home/leandro/PycharmProjects/SO/teste.txt")
linhas = arq.readlines()
for linha in linhas:
    time.sleep(3)
    partes = linha.split(" ")
    if partes[1] == 'C': # Caso crie um Processo
        quantidade_quadros_processo = int(partes[2]) # Pega a quantidade de quadros do processo
        valor_pagina = 0 # Valor pagina atual
        for i in range(quantidade_quadros_secundaria): # Aloca os quadros do processo na memoria secundaria
            if (tabela_secundaria[i] == "-") & (quantidade_quadros_processo > 0):
                tabela_secundaria[i] = partes[0] + " - pagina " + str(valor_pagina)
                adicionar_memoria_secundaria(partes[0] + " - pagina " + str(valor_pagina), i)
                quantidade_quadros_processo -= 1
                valor_pagina += 1
        tabelas_paginas.append(criar_tabela(partes[0], partes[2], 1024)) # Cria a tabela de pagina do processo
        adicionar_tabelas_paginas(criar_tabela(partes[0], partes[2], 1024), None, None, None)
        tamanho_memoria_secundaria -= int(partes[2]) # Diminui o espaço liberado da memoria secundaria
        atualizar_janela()
    else:
        if partes[1][0] == 'T':
            print("Encerrando o processo "+partes[0])
            for g in range(len(tabelas_paginas)):
                if partes[0] == tabelas_paginas[g][0]:
                    paginas = tabelas_paginas[g]
                    for q in range(len(paginas)):
                        if q!= 0:
                            if paginas[q][1] == 1:
                                print("Preciso atualizar na memoria secundaria")
                                quadro_atualizado = tabela_fisica[paginas[q][2]]
                                for u in range(len(tabela_secundaria)):
                                    quadro_desatualizado = tabela_secundaria[u]
                                    if quadro_desatualizado == quadro_atualizado:
                                        tabela_secundaria[u] = quadro_atualizado
                                        print("Atualizando na memoria secundaria")
                            if paginas[q][2] != "-":
                                tabela_fisica[int(paginas[q][2])] = "-"
                    del tabelas_paginas[g]
                    break
        else:
            endereco = partes[2][1:-3]
            endereco_logico = decimal_para_binario_com_20_bits(int(endereco))  # Transforma o endereco para binario
            numero_pagina = endereco_logico[0:10]  # Separa o numero da pagina
            offset = endereco_logico[10::]  # Separa o offset
            for p in range(len(tabelas_paginas)):  # Procura a tabela de processo na tabela de todos os processos
                if tabelas_paginas[p][0] == partes[0]:
                    pagina = tabelas_paginas[p][
                        int(numero_pagina, 2) + 1]  # Pega a pagina do processo na tabela no processo
                    if pagina[2] == "-":  # Se o quadro estiver vazio da pagina, a pagina nao esta na memoria principal
                        quadro_tabela_fisica = -1
                        for k in range(len(tabela_secundaria)):  # Procura na memoria secundaria a pagina
                            quadro_secundaria = tabela_secundaria[k].split(" ")
                            if quadro_secundaria[0] != '-':
                                if (quadro_secundaria[0] == partes[0]) & (int(quadro_secundaria[3]) == int(numero_pagina, 2)):
                                    for x in range(len(tabela_fisica)):  # Coloca na memoria principal se tiver espaço
                                        if tabela_fisica[x] == "-":
                                            tabela_fisica[x] = tabela_secundaria[k]
                                            adicionar_memoria_principal(tabela_secundaria[k], x)
                                            quadro_tabela_fisica = x
                                            print("Pegamos a pagina na memoria secundaria")
                                            break
                                        if x == len(tabela_fisica):
                                            #TODO
                                            print("Memoria principal esta cheia")

                        tabelas_paginas[p][int(numero_pagina, 2) + 1][0] = 1
                        tabelas_paginas[p][int(numero_pagina, 2) + 1][2] = quadro_tabela_fisica
                        adicionar_tabelas_paginas(1, p, int(numero_pagina, 2) + 1, quadro_tabela_fisica)
                    if (pagina[0] == 1) & (pagina[1] == 0):  # A pagina esta na memoria principal
                        print("Esta na memoria principal")
                    if (pagina[0] == 1) & (pagina[1] == 1):  # A pagina na memoria secundaria precisa ser atualizada
                        print("A pagina precisa ser atualizada na memoria secundaria")
                        for y in range(len(tabela_secundaria)):
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
                        for j in range(len(tabela_fisica)):
                            if partes[0] == tabela_fisica[j][0:2]:
                                for d in range(len(tabelas_paginas)):
                                    if tabelas_paginas[d][0] == partes[0]:
                                        pag = tabelas_paginas[d][int(tabela_fisica[j][-1])+1]
                                        if pag[1] == 0:
                                            tabela_fisica[j] = "-"
                                            pag[0] = 0
                                            pag[1] = 0
                                            pag[2] = "-"
                                        else:
                                            print("Atualizando a pagina na memoria secundaria")
                                            for u in range(len(tabela_secundaria)):
                                                if tabela_secundaria[u] == tabela_fisica[j]:
                                                    tabela_secundaria[u] = tabela_fisica[j]
                                            pag[0] = 0
                                            pag[1] = 0
                                            pag[2] = "-"
                        break



print(tabelas_paginas)
# print(tabelas_paginas[1])
print(tabela_fisica)


janela.mainloop()