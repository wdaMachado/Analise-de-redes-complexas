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
        
    def add_conexao(self, vertice, adj):
        if vertice not in self.conexoes:    #checa se o vertice esta no dicionario de conexoes (basicamente o grafo)
            self.conexoes[vertice] = {}     #entao cria uma chave com o vertice, e um dicionario que ira receber os adjacentes
            self.conexoes[vertice][adj] = 1 #adiciona o peso inicial de uma conexao
        else:
            if adj not in self.conexoes[vertice]:
                self.conexoes[vertice][adj] = 1
            else:
                self.conexoes[vertice][adj] = self.conexoes[vertice][adj]+1


# teste = Grafo_ponderado()
# teste.add_vertice("william")
# teste.add_vertice("Camila")
# teste.add_vertice("Sandra")
# teste.add_conexao("William", "Camila")
# teste.add_conexao("William", "Camila")
# teste.add_conexao("William", "Sandra")
# teste.add_conexao("Sandra", "Camila")

# teste.show_grafo()
