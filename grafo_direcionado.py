import numpy as np
import heapq
from collections import defaultdict

#estrutura {"ator" : {'diretor1' : peso1, 'diretor2' : peso2}}
class Grafo_ponderado:
    def __init__(self):
        self.n_vertices = 0
        self.vertices = []
        self.conexoes = {}
    
    def grafo(self):
        return self.conexoes

    def show_grafo(self, vertice = None):
        if vertice:
            return print(self.conexoes[vertice])
        return print(self.conexoes)
    
    def quant_vertices(self):
        return len(self.vertices)
    
    def quant_arestas(self):   
        soma = 0
        for ator,lista_diretores in self.conexoes.items(): # utiliza o dicionario que 'e o valor do dicionario inicial
            for chave in lista_diretores.items():          # para somar 1 cada conexao
                soma += 1
        return soma


    def add_vertice(self, vertice):  
        if vertice not in self.vertices: #checa se o vertice ja esta na lista de vertices, e adiciona na mesma.
            self.vertices.append(vertice)
            self.conexoes[vertice] = {}
        
    def add_conexao(self, vertice, adj):
        if vertice not in self.conexoes:    #checa se o vertice esta no dicionario de conexoes (basicamente o grafo)
            self.conexoes[vertice] = {}     #entao cria uma chave com o vertice, e um dicionario que ira receber os adjacentes
            self.conexoes[vertice][adj] = 1 #adiciona o peso inicial de uma conexao
        else:
            if adj not in self.conexoes[vertice]:
                self.conexoes[vertice][adj] = 1
            else:
                self.conexoes[vertice][adj] = self.conexoes[vertice][adj]+1

##Funcao para gerar uma imagem do grafo facilitando o entendimento
def gerar_dot(grafo, nome_arquivo="grafo.dot", direcionado=True):
    tipo = "digraph" if direcionado else "graph"
    ligacao = "->" if direcionado else "--"

    with open(nome_arquivo, "w", encoding='utf-8') as f:
        f.write(f"{tipo} G {{\n")
        for origem, destinos in grafo.items():
            for destino, peso in destinos.items():
                f.write(f'    "{origem}" {ligacao} "{destino}" [label="{peso}"];\n')
        f.write("}\n")

def dfs(grafo, source_node=None, ordem_personalizada=None):
    stack = []
    visiting = set()
    finished = set()

    visited_finished = {}  #{'nó': {'start': tempo_inicio, 'end': tempo_fim}}
    time = 1
    contador_grupos = {}
    i = 0

    # Define ordem de visita
    if source_node is not None:
        ordem = [source_node]
    elif ordem_personalizada is not None:
        ordem = ordem_personalizada
    else:
        ordem = list(grafo.keys())

    for node in ordem:
        if node in finished:
            continue
        stack.append((node, False))
        while stack:
            current_node, expanded = stack.pop()
            if not expanded:
                if current_node not in visited_finished:
                    visiting.add(current_node)
                    visited_finished[current_node] = {'start': time, 'end': None}
                    time += 1
                    stack.append((current_node, True))
                    for adj in sorted(grafo.get(current_node, {}), reverse=True):
                        if adj not in visited_finished and adj not in visiting and adj not in finished:
                            stack.append((adj, False))
            else:
                visiting.remove(current_node)
                finished.add(current_node)
                if i not in contador_grupos:
                    contador_grupos[i] = []
                contador_grupos[i].append(current_node)
                visited_finished[current_node]['end'] = time
                time += 1
        i += 1

    return contador_grupos, visited_finished

def dijkstra_distancias(grafo, origem):
    distancias = {v: float('inf') for v in grafo}
    distancias[origem] = 0
    visitados = set()

    while len(visitados) < len(grafo):
        # Seleciona o nó não visitado com menor distância atual
        atual = None
        menor_dist = float('inf')
        for v in grafo:
            if v not in visitados and distancias[v] < menor_dist:
                menor_dist = distancias[v]
                atual = v

        if atual is None:
            break  # Todos os nós restantes são inalcançáveis

        visitados.add(atual)

        for vizinho, peso in grafo[atual].items():
            if distancias[vizinho] > distancias[atual] + peso:
                distancias[vizinho] = distancias[atual] + peso


    return distancias

def transpose(grafo): #inverte cada uma das conexoes do grafo
        transposto = {}
        for ator, diretores in grafo.items(): 
            for diretor in diretores:
                if diretor not in transposto:
                    transposto[diretor] = {}
                transposto[diretor][ator] = grafo[ator][diretor]
                
        return transposto

def centralidade_grau(grafo, vertice):
    centralidade = {}
    centralidade[vertice] = len(grafo[vertice])/ len(grafo)
    return centralidade

def centralidade_proximidade(grafo, vertice=None):
    def calcular_para(v):
        distancias = dijkstra_distancias(grafo, v)
        dist_validas = [d for u, d in distancias.items() if u != v and d != float('inf')]
        dist_certas = []
        if len(dist_validas) == 0:
            return 0
        for dist in dist_validas:
            dist_certas.append(1/dist)
        soma = sum(dist_certas)
        return soma/(len(grafo)-1) if soma > 0 else 0

    if vertice is not None:
        return {vertice: calcular_para(vertice)}
    else:
        return {v: calcular_para(v) for v in grafo}

def centralidade_intermediacao(grafo, vertice=None):
    centralidade = dict.fromkeys(grafo, 0.0)
    
    # Se nenhum vértice for passado, calcula para todos
    nos_origem = [vertice] if vertice else list(grafo)

    for s in nos_origem:
        pilha = []
        Anteriores = defaultdict(list)
        Caminhos_min = dict.fromkeys(grafo, 0.0)
        Distancia_min = dict.fromkeys(grafo, float('inf'))
        Caminhos_min[s] = 1.0
        Distancia_min[s] = 0.0

        fila = []
        heapq.heappush(fila, (0, s))

        while fila:
            dist_vertice, u = heapq.heappop(fila)
            if Distancia_min[u] < dist_vertice:
                continue
            pilha.append(u)
            for w in grafo[u]:
                peso = grafo[u][w]
                if Distancia_min[w] > Distancia_min[u] + peso:
                    Distancia_min[w] = Distancia_min[u] + peso
                    heapq.heappush(fila, (Distancia_min[w], w))
                    Caminhos_min[w] = 0.0
                    Anteriores[w] = []
                if Distancia_min[w] == Distancia_min[u] + peso:
                    Caminhos_min[w] += Caminhos_min[u]
                    Anteriores[w].append(u)

        delta = dict.fromkeys(grafo, 0.0)
        while pilha:
            w = pilha.pop()
            for v in Anteriores[w]:
                if Caminhos_min[w] > 0:
                    delta[v] += (Caminhos_min[v] / Caminhos_min[w]) * (1 + delta[w])
            if w != s:
                centralidade[w] += delta[w]

    # Normalização apenas se foi para todos
    if vertice is None:
        n = len(grafo)
        if n > 2:
            fator = (n - 1) * (n - 2)
            for v in centralidade:
                centralidade[v] /= fator
        return centralidade
    else:
        return centralidade[vertice]


teste = Grafo_ponderado()
teste.add_vertice("A")
teste.add_vertice("B")
teste.add_vertice("C")
teste.add_vertice("D")
teste.add_vertice("E")
teste.add_vertice("F")
teste.add_vertice("G")
teste.add_vertice("H")

teste.add_conexao("C", "D")
teste.add_conexao("C", "G")
teste.add_conexao("D", "H")
teste.add_conexao("D", "C")
teste.add_conexao("G", "H")
teste.add_conexao("G", "F")
teste.add_conexao("F", "G")
teste.add_conexao("E", "F")
teste.add_conexao("E", "A")
teste.add_conexao("A", "B")
teste.add_conexao("B", "F")
teste.add_conexao("B", "E")
teste.add_conexao("B", "C")

#teste.show_grafo()

# gerar_dot(teste.grafo())
# (grupos1, dfs1) = dfs(teste.grafo())
# dfs1 = {Vertice: time for Vertice, time in sorted(dfs1.items(), key=lambda item: item[1]['end'], reverse=True)}
# transposto = transpose(teste.grafo())
# gerar_dot(transposto, "grafo_transposto")
# (grupos2, dfs2) = dfs(transposto, ordem_personalizada=list(dfs1.keys()))
# print(grupos1)
# print(grupos2)

# centralidade_proximidade = centralidade_proximidade(teste.grafo(), "A")
# print(f"Centralidade de proximidade: {centralidade_proximidade}")

# centralidade_intermediacao = centralidade_intermediacao(teste.grafo(), "C")
# print(f"Centralidade de intermediacao: {centralidade_intermediacao}")