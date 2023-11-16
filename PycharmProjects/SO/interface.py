

    # def remover_memoria_secundaria(processo):
    #     # Remove o item selecionado na Listbox
    #     for i in range(len(GUI_memoria_secundaria)):
    #         if GUI_memoria_secundaria[i] == processo:
    #             GUI_memoria_secundaria[i] = "-"
    #
    # def adicionar_memoria_principal(processo, index):
    #     # Obtém o texto digitado no Entry e adiciona à Listbox
    #     if index is None:
    #         GUI_memoria_principal.insert(tk.END, processo)
    #     else:
    #         GUI_memoria_principal.insert(index, processo)
    #
    # def remover_memoria_principal(processo):
    #     # Remove o item selecionado na Listbox
    #     for i in range(len(GUI_memoria_principal)):
    #         if GUI_memoria_principal[i] == processo:
    #             GUI_memoria_principal[i] = "-"
    #
    # def adicionar_tabelas_paginas(processo, index, page, quadro):
    #     # Obtém o texto digitado no Entry e adiciona à Listbox
    #     if index is None:
    #         GUI_tabelas_paginas.insert(tk.END, processo)
    #     #Estou comecando a fazer as tabelas de paginas
    #     # else:
    #     #     pagina_antiga = GUI_tabelas_paginas.get(index)
    #     #     pagina_antiga[page][0] = 1
    #     #     pagina_antiga[page][2] = quadro
    #
    #
    # def remover_tabelas_paginas(processo):
    #     # Remove o item selecionado na Listbox
    #     for i in range(GUI_tabelas_paginas.size()):
    #         if GUI_tabelas_paginas.index(i) == processo:
    #             GUI_tabelas_paginas.insert(i,"-")

#
#
# def criar_interface():
#     def adicionar_memoria_secundaria(tabela_memoria_secundaria):
#         # Obtém o texto digitado no Entry e adiciona à Listbox
#         for item in tabela_memoria_secundaria:
#             GUI_memoria_secundaria.insert(tk.END, item)
#
#         # Criar janela principal
#
#     janela = tk.Tk()
#     janela.title("Exemplo de Lista")
#
#     labelMemoriaSecundaria = tk.Label(janela, text="Memoria Secundaria:")
#     labelMemoriaSecundaria.pack()
#
#     labelTamanhoSecundaria = tk.Label(janela, text=tamanho_memoria_secundaria)
#     labelTamanhoSecundaria.pack()
#
#     # Criar Listbox
#     GUI_memoria_secundaria = tk.Listbox(janela, selectmode=tk.SINGLE)
#     GUI_memoria_secundaria.pack(pady=10)
#
#     labelMemoriaPrincipal = tk.Label(janela, text="Memoria Principal:")
#     labelMemoriaPrincipal.pack()
#
#     labelTamanhoPrincipal = tk.Label(janela, text=tamanho_memoria_fisica)
#     labelTamanhoPrincipal.pack()
#     # Criar Listbox
#     GUI_memoria_principal = tk.Listbox(janela, selectmode=tk.SINGLE)
#     GUI_memoria_principal.pack(pady=10)
#
#     labelTabelasPaginas = tk.Label(janela, text="Tabelas Paginas:")
#     labelTabelasPaginas.pack()
#
#     # Criar Listbox
#     GUI_tabelas_paginas = tk.Listbox(janela, selectmode=tk.SINGLE)
#     GUI_tabelas_paginas.pack(pady=10)
#     janela.mainloop()
#
# # Criar uma thread para executar a interface gráfica
#
# thread_interface = Thread(target=criar_interface())
#
# # Iniciar a thread
# thread_interface.start()