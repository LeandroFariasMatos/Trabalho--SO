def decimal_para_binario_com_20_bits(decimal):
    binario = bin(decimal)[2:]
    binario_com_20_bits = binario.zfill(20)

    return binario_com_20_bits
