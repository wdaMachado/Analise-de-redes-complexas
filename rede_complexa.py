import pandas as pd
from grafo1 import *

grafo = Grafo_ponderado()


df = pd.read_csv("data.csv")
with open("diretor-ator.txt", "w", encoding='utf-8') as arq:
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

grafo.show_grafo("JAMES FRANCO")
# (grupo, dfs1) = dfs(grafo.grafo())
# print(f"DFS: {grupo}")
# gerar_dot(grafo.grafo())


####### Testes de centralidade
# centralidade_grau = centralidade_grau(grafo.grafo(), "LAWRENCE KOH")
# print(f"Centralidade de grau: {centralidade_grau}")

# centr_proximidade = centralidade_proximidade(grafo.grafo(), "ABHISHEK BANERJEE")
# print(f"Centralidade de proximidade: {centr_proximidade}")

# centralidades = centralidade_intermediacao(grafo.grafo(), "ABHISHEK BANERJEE")
# print(f"Centralidade de intermediação de ABHISHEK BANERJEE: {centralidades:.20f}")

centralidades = centralidade_intermediacao(grafo.grafo())

top10 = sorted(centralidades.items(), key=lambda x: x[1], reverse=True)[:10] ## Já retorna os 10 diretores com maior centralidade
for v, c in top10:
    print(f"{v}: {c:.10f}")


