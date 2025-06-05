import numpy as np
#estrutura {"ator" : {'diretor1' : peso1, 'diretor2' : peso2}}
class Grafo_ponderado:
    def __init__(self):
        self.n_vertices = 0
        self.vertices = []
        self.conexoes = {}
    
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

    def dfs(self, source_node):
        visited = []
        stack   = []
        visited_finished = {} #Estrutura {'vertice' : {'visited' : {finalizado} }} Ainda em implementacao
        i = 1
        stack.append(source_node)
        while len(stack) > 0:
            current_node = stack.pop()

            if current_node not in visited:
                visited.append(current_node)
                visited_finished[current_node] = {}
                visited_finished[current_node][i] = np.inf
                
                for adj in sorted(self.conexoes[current_node], reverse=True):
                    if adj not in visited:
                        stack.append(adj)  
                adj

            i+=1 
        return visited

    def transpose(self): #inverte cada uma das conexoes do grafo
        transposto = {}
        for ator, diretores in self.conexoes.items(): 
            for diretor in diretores:
                if diretor not in transposto:
                    transposto[diretor] = {}
                transposto[diretor][ator] = self.conexoes[ator][diretor]
                
        return transposto
    

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

teste.show_grafo()
print(teste.dfs("C"))

gerar_dot(teste.conexoes)
transposto = teste.transpose()
gerar_dot(transposto, "grafo_transposto.dot")

