import numpy as np
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

    with open(nome_arquivo, "w") as f:
        f.write(f"{tipo} G {{\n")
        for origem, destinos in grafo.items():
            for destino, peso in destinos.items():
                f.write(f'    "{origem}" {ligacao} "{destino}" [label="{peso}"];\n')
        f.write("}\n")

def dfs(grafo, source_node):
    stack = []
    visiting = set()
    finished = set()
    visited_finished = {}  # {'nó': {'start': tempo_inicio, 'end': tempo_fim}}

    time = 1
    stack.append((source_node, False))  # (nó, expandido?)
    while len(grafo) > len(finished):
        if len(stack) == 0:
            for node in grafo:
                if node not in visited_finished and node not in visiting and node not in finished:
                    stack.append((node, False))
                if len(stack) > 0:
                    break 
        while stack:
            current_node, expanded = stack.pop()

            if not expanded:
                if current_node not in visited_finished:
                    visiting.add(current_node)
                    visited_finished[current_node] = {'start': time, 'end': None}
                    time += 1

                    # Reempilha o nó para ser finalizado depois
                    stack.append((current_node, True))

                    # 🔧 MELHORIA 1: empilha apenas nós ainda não visitados
                    if grafo[current_node]:
                        for adj in sorted(grafo[current_node], reverse=True):
                            if adj not in visited_finished and adj not in visiting and adj not in finished:
                                stack.append((adj, False))

            else:
                visiting.remove(current_node)
                finished.add(current_node)
                visited_finished[current_node]['end'] = time
                time += 1

    return visited_finished

def transpose(grafo): #inverte cada uma das conexoes do grafo
        transposto = {}
        for ator, diretores in grafo.items(): 
            for diretor in diretores:
                if diretor not in transposto:
                    transposto[diretor] = {}
                transposto[diretor][ator] = grafo[ator][diretor]
                
        return transposto
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

gerar_dot(teste.grafo())
dfs1 = dfs(teste.grafo(), "C")
dfs1 = {Vertice: time for Vertice, time in sorted(dfs1.items(), key=lambda item: item[1]['end'], reverse=True)}
transposto = transpose(teste.grafo())
gerar_dot(transposto)
dfs2 = dfs(transposto, list(dfs1.keys())[0])
print(dfs1)
print(dfs2)

