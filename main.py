import numpy as np
import sys

if len(sys.argv) < 2:
        print("Digite o nome do arquivo. Exemplo: python main.py casoa")
        exit()

nomeArquivo = sys.argv[1]

try:
    linhas_sistemas = {}
    dict_sistema = {}
    gauss = []

    with open(nomeArquivo+".txt", "r") as arquivo:
        for linha in arquivo:
            if linha.startswith("Entrada"):
                entrada, valor = linha.strip().split(" : ")
                if entrada not in linhas_sistemas:
                    linhas_sistemas[entrada] = {}
                linhas_sistemas[entrada]["valor"] = float(valor)
            elif "->" in linha:
                xn, valor, bn = linha.strip().split(" -> ")
                ordem = xn.strip()[-1]
                if bn.startswith("Entrada"):
                    entrada = bn
                else:
                    entrada = f"Entrada {bn[0]}"
                if entrada not in linhas_sistemas:
                    linhas_sistemas[entrada] = {}
                if xn == bn:
                    valor = float(valor) - 1
                linhas_sistemas[entrada][ordem] = float(valor)

    for entrada, valores in linhas_sistemas.items():
        nparray = np.zeros(len(valores))
        for letra, valor in valores.items():
            if letra == "valor":
                nparray[-1] = valor
            else:
                i = ord(letra) - ord('A')
                nparray[i] = valor
        dict_sistema[entrada] = nparray

    #Print das linhas_sistemas
    #for entrada in linhas_sistemas:
    #    print(f"{entrada} : {linhas_sistemas}")

    #print dos valores das linhas_sistemas, ja em ordem
    print("Print - Sistema Linear: \n")
    for entrada, nparray in dict_sistema.items():
        print(f"{entrada}: {nparray}")


    #Criar a matriz em np + print
    lista_sistema = [nparray for entrada, nparray in dict_sistema.items()]
    matriz_sistema = np.vstack(lista_sistema)
    #print(f"\n\nEm matriz: \n{a}")


    ######### Gauss #########

    n = len(linhas_sistemas)

    #Vetor da solução
    solucao = np.zeros(n)

    #Gauss Elimination
    for i in range(n):
        if matriz_sistema[i][i] == 0.0:
            print('Divide by zero detected!')
            break
            
        for j in range(i+1, n):
            ratio = matriz_sistema[j][i]/matriz_sistema[i][i]
            
            for k in range(n+1):
                matriz_sistema[j][k] = matriz_sistema[j][k] - ratio * matriz_sistema[i][k]

    #Back Substitution
    solucao[n-1] = matriz_sistema[n-1][n]/matriz_sistema[n-1][n-1]

    for i in range(n-2,-1,-1):
        solucao[i] = matriz_sistema[i][n]
        
        for j in range(i+1,n):
            solucao[i] = solucao[i] - matriz_sistema[i][j]*solucao[j]
        
        solucao[i] = solucao[i]/matriz_sistema[i][i]
        

    #Exibindo solução
    print(f'\nSolução do Sistema (abs):\n')
    for i in range(n):
        gauss.append(abs(solucao[i]))
        #print('X%d = %0.3f' %(i,x[i]), end = '\t')
        print(f"Planeta {chr(65+i)}: {abs(solucao[i])}")

    print(f"\n\nCom isso, concluímos que: \n [1] O número de habitantes esperados no planeta A é de {gauss[0]}. \n [2] O planeta {chr(65+gauss.index(max(gauss)))} é o com maior número de habitantes esperados, tendo o total de {max(gauss)} habitantes.")

except FileNotFoundError:
    print(f"Arquivo '{nomeArquivo}' não encontrado. Digite o nome do arquivo corretamente e sem '.txt' Exemplo: python main.py casoa ")