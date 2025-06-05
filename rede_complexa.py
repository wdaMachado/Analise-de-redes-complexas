import pandas as pd
from grafo1 import Grafo_ponderado, gerar_dot

grafo = Grafo_ponderado()


df = pd.read_csv("shortened_data.csv")
with open("diretor-ator.txt", "w") as arq:
    for index, linha in df.iterrows():
        diretores   = linha['director']
        atores      = linha['cast']
        # Verifica se diretores e atores não são nulos
        if pd.notna(diretores) and pd.notna(atores):
            # Transforma strings separadas por vírgula em listas, removendo espaços extras
            lista_diretores = [diretor.strip().upper() for diretor in diretores.split(',')]
            lista_atores = [ator.strip().upper() for ator in atores.split(',')]     
            #comeca a iteracao dos diretores e dos atores, para preencher o grafo tambem escrevendo no arquivo (remover isso) 
            for diretor in lista_diretores:
                grafo.add_vertice(diretor)

                arq.writelines(f"Diretor: {diretor} ; Atores: ")

                for ator in lista_atores:
                    grafo.add_vertice(ator)
                    grafo.add_conexao(ator, diretor)

                    arq.write(f"{ator}, ")
                arq.write(f"\n")            

n_vertices  = grafo.quant_vertices()
n_arestas   = grafo.quant_arestas()

print(f"Nodes: {n_vertices}\nArestas: {n_arestas} \n---------------------")
grafo.show_grafo("ABHISHEK BANERJEE")
print(f"DFS:      {grafo.dfs('ABHISHEK BANERJEE')}")

gerar_dot(grafo.conexoes)
