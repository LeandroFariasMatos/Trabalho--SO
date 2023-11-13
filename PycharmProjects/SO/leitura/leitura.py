from tabelaPagina.tabelapagina import criar_tabela
def lendo_linha(tamanho_memoria_principal, tabelas_paginas, arquivo, linha):
    with open(arquivo) as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        count += 1
        if linha == count:
            partes = line.split(" ")
            if partes[1] == 'C':
                tabelas_paginas.append(criar_tabela(partes[0], partes[2], 1024))
                return tamanho_memoria_principal - int(partes[2]), tabelas_paginas





