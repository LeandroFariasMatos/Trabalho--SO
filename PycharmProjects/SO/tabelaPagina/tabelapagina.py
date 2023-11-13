def criar_tabela(processo, tamanho_processo, tamanho_pagina):
    quantidade_paginas = int(int(tamanho_processo)*1024/int(tamanho_pagina))
    tabela = [processo]
    for i in range(quantidade_paginas):
        parte = [0, 0, "-"]
        tabela.append(parte)
    return tabela
