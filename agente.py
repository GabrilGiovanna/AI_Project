"""
agente.py

criar aqui as funções que respondem às perguntas
e quaisquer outras que achem necessário criar

colocar aqui os nomes e número de aluno:
41235, Gabriel Ribeiro
42293, Pedro Mourato

"""

# imports
import time
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import networkx as nx
import math

people = []  # lista global para guardar as pessoas femininas que o agente vai vendo

G = nx.Graph()  # Criação do Grafo
pontosMedios = [(82.5, 290.5), (210.5, 215.5), (212.5, 382), (363, 300), (605.5, 220, 5), (605.5, 382), (82.5, 90), (232.5, 90),
                (382.5, 90), (532.5, 90), (700, 90), (700, 505), (532.5, 505), (382.5, 505), (232.5, 505), (82.5, 505)]  # para usar nos Nodos

zonas = []
for i in range(16):
    c = i
    zonas.append([])
    # nodos do Grafo
    G.add_node("Zona %d" % (c+1), pos=(pontosMedios[i][0], pontosMedios[i][1]))


def distancia(x, y):  # função para calcular distancia
    return math.sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))


# Como sabemos à priori todas as conexões, adicionamos todos as arestas no inicio do programa
G.add_edge("Zona 1", "Zona 7", distance=distancia(
    pontosMedios[0], pontosMedios[6]))
G.add_edge("Zona 1", "Zona 2", distance=distancia(
    pontosMedios[0], pontosMedios[1]))
G.add_edge("Zona 1", "Zona 3", distance=distancia(
    pontosMedios[0], pontosMedios[2]))
G.add_edge("Zona 1", "Zona 16", distance=distancia(
    pontosMedios[0], pontosMedios[15]))
G.add_edge("Zona 2", "Zona 8", distance=distancia(
    pontosMedios[1], pontosMedios[7]))
G.add_edge("Zona 2", "Zona 4", distance=distancia(
    pontosMedios[1], pontosMedios[3]))
G.add_edge("Zona 3", "Zona 4", distance=distancia(
    pontosMedios[2], pontosMedios[3]))
G.add_edge("Zona 3", "Zona 15", distance=distancia(
    pontosMedios[2], pontosMedios[14]))
G.add_edge("Zona 4", "Zona 9", distance=distancia(
    pontosMedios[3], pontosMedios[8]))
G.add_edge("Zona 4", "Zona 14", distance=distancia(
    pontosMedios[3], pontosMedios[13]))
G.add_edge("Zona 4", "Zona 5", distance=distancia(
    pontosMedios[3], pontosMedios[4]))
G.add_edge("Zona 4", "Zona 6", distance=distancia(
    pontosMedios[3], pontosMedios[5]))
G.add_edge("Zona 5", "Zona 10", distance=distancia(
    pontosMedios[4], pontosMedios[9]))
G.add_edge("Zona 5", "Zona 11", distance=distancia(
    pontosMedios[4], pontosMedios[10]))
G.add_edge("Zona 6", "Zona 13", distance=distancia(
    pontosMedios[5], pontosMedios[12]))
G.add_edge("Zona 6", "Zona 12", distance=distancia(
    pontosMedios[5], pontosMedios[11]))


def mostraGrafo(grafo):
    plt.gca().invert_yaxis()
    pos = nx.get_node_attributes(grafo, 'pos')
    nx.draw(grafo, pos, with_labels=True)
    plt.savefig("graph.png")
    plt.show()


# usados para a pergunta 6
dadosBateria = []  # para guardar o progresso da bateria ao longo da execução do programa
dadosTempo = []  # para guardar os tempos
dadosVelocidade = []  # para guardar a velocidade
tempoInicial = time.time()
objetosVistos = []  # Keep track of Objetos

posicaonova = [0, 0]  # Para verificar se posição mudou (usar na Questão 5)

tempoRecente = time.time()


def work(posicao, bateria, objetos):
    # esta função é invocada em cada ciclo de clock
    # e pode servir para armazenar informação recolhida pelo agente
    # recebe:
    # posicao = a posição atual do agente, uma lista [X,Y]
    # bateria = valor de energia na bateria, um número inteiro >= 0
    # objetos = o nome do(s) objeto(s) próximos do agente, uma string

    # podem achar o tempo atual usando, p.ex.
    # time.time()
    global listaposicao, tempoRecente, posicaonova  # acesso às variáveis

    listaposicao = list(posicao)
    if posicaonova[0] != listaposicao[0] or posicaonova[1] != listaposicao[1]:
        d = distancia(posicaonova, listaposicao)
        t = time.time() - tempoRecente
        v = d / t  # fórmula velocidade
        dadosVelocidade.append(v)
        tempoRecente = time.time()
        posicaonova = listaposicao.copy()

    for i in objetos:  # a cada ciclo de clock
        # se o objeto for uma pessoa, não tiver sido a ultima pessoa a ser vista, e for um nome feminino
        if (("adulto" in i or "criança" in i or "funcionário" in i) and (checkPrevious(i)) and checkFemale(i)):
            people.append(i)  # guardar na lista global de pessoas o objeto

    if objetos:
        # Sempre que se vir um novo objeto, guarda o objeto na zona respectiva
        adicionarObjeto(objetos)

    dadosBateria.append(bateria)
    dadosTempo.append(time.time() - tempoInicial)


def resp1():
    if len(people) > 1:
        print(people[-2])
    else:
        print("Ainda não vi pelo menos duas pessoas do sexo feminino")


def resp2():
    zona_atual = verificaCorredorZona()
    coisas_zona_atual = zonas[zona_atual - 1]
    
    for coisa in coisas_zona_atual:
        if "zona_" in coisa:
            print(f"Estamos numa zona de {coisa.split('_')[1]}")
            return

    print("Não sei em que zona é que estou")


def resp3():
    papelaria()


def resp4():
    talho()


def resp5():
    saida()


def resp6():
    funcaoBateria()
    pass


def resp7():
	total_pessoas=0
	numero_criancas =0
	for zona in zonas:
		for nome in zona:
			if "criança" in nome:
				numero_criancas= numero_criancas + 1
			total_pessoas=total_pessoas+1
	if total_pessoas == 0:
		print ("não é possivel responder à pergunta")
		return
	else:
		print (f"A probabilidade de ser crianca é {numero_criancas/total_pessoas} ")


def resp8():
    # What is the probability a randomly selected person is male, given that they own a pet?
    # 8. Qual é a probabilidade de encontrar um adulto numa zona se estiver lá uma
    # criança mas não estiver lá um carrinho

    # P(A | (C^!R))
    # ver salas onde há adultos, criancas mas que não há carrinhos
    # a divdir pelo numero de salas que há adultos

    # P(A ^ (C^!R))
    # /
    # P(A)

	PACNR = n_quartos_com_adultos_criancas_mas_nao_carro()
	PA = n_quartos_com_adultos() / len(zonas)
	if PA == 0:
		print("Ainda não foi vista nenhuma pessoa")
		return

	print(f"A probabilidade é de {PACNR / PA}")


def n_quartos_com_adultos():
    a = 0
    for zona in zonas:
        if any("adulto" in s for s in zona):
            a = a + 1
    return a



def n_quartos_com_adultos_criancas_mas_nao_carro():
    resultado = 0

    for zona in zonas:
        n_adultos = 0
        n_crincas = 0
        n_carros = 0
        for objeto in zona:
            if any("criança" in s for s in objeto):
                n_crincas = n_crincas + 1
            elif any("adulto" in s for s in objeto):
                n_adultos = n_adultos + 1
            elif any("carrinho" in s for s in objeto):
                n_carros = n_carros + 1

        if n_adultos > 0 and n_crincas > 0 and n_carros == 0:
            resultado = resultado + 1

    return resultado


def checkPrevious(x):  # para a questão nº1, verifica se a pessoa vista é a mesma que o agente viu anteriormente
    if people:
        if people[-1] == x:
            return False
    return True


def checkFemale(x):  # para a questão nº1, verifica se a pessoa é do sexo feminino com um ficheiro de texto com os Nomes femininos legais em Portugal
    y = x.partition("_")[2]  # só nos interessa o nome e não o "tipo"
    # abre o ficheiro e verifica se o nome existe no ficheiro
    if y not in open('ficheiro nomes masculinos.txt', encoding="utf8").read():
        return True
    return False


def verificaCorredorZona():  # função para verificar em que zona(numerica) estamos
    x = listaposicao[0]

    y = listaposicao[1]

    if((30 <= x <= 135) and (30 <= y <= 150)):
        return 7

    if((180 <= x <= 285) and (30 <= y <= 150)):
        return 8

    if((330 <= x <= 435) and (30 <= y <= 150)):
        return 9

    if((480 <= x <= 585) and (30 <= y <= 150)):
        return 10

    if((630 <= x <= 770) and (30 <= y <= 150)):
        return 11

    if((30 <= x <= 135) and (440 <= y <= 570)):
        return 16

    if((180 <= x <= 285) and (440 <= y <= 570)):
        return 15

    if((330 <= x <= 435) and (440 <= y <= 570)):
        return 14

    if((480 <= x <= 585) and (440 <= y <= 570)):
        return 13

    if((630 <= x <= 770) and (440 <= y <= 570)):
        return 12

    if((30 <= x <= 135) and (151 <= y <= 430)):
        return 1

    if((136 <= x <= 285) and (151 <= y <= 280)):
        return 2

    if((140 <= x <= 285) and (325 <= y <= 439)):
        return 3

    if((286 <= x <= 440) and (165 <= y <= 435)):
        return 4

    if((441 <= x <= 770) and (151 <= y <= 290)):
        return 5

    if((441 <= x <= 770) and (325 <= y <= 439)):
        return 6

    return 0


# funcao para ver se o objeto ja foi visto
def verificaSeObjetoJaFoiVisto(obj, lista):
    if lista:
        for x in lista:
            if x == obj:
                return True
    return False


def adicionarObjeto(objetos):
    for y in objetos:
        if verificaSeObjetoJaFoiVisto(y, objetosVistos) == False:
            objetosVistos.append(y)  # guardar nos objetos vistos
            for i in range(16):
                c = i
                if verificaCorredorZona() == c+1:  # se se encontra na zona 1
                    zonas[i].append(y)  # guardar na zona 1
        else:  # Se Objeto já foi visto, não adiciona em lado nenhum
            break


def funcaoBateria():  # Questão 6
    metadeBateria = (dadosBateria[-1] / 2)
    X = np.array(dadosBateria)
    y = np.array(dadosTempo)
    X = X.reshape(-1, 1)
    y = y.reshape(-1, 1)
    # Regressão Linear Polinomial com grau 2 ( para evitar overfit)
    poly_reg = PolynomialFeatures(degree=2)
    X_poly = poly_reg.fit_transform(X)
    pol_reg = LinearRegression()
    pol_reg.fit(X_poly, y)
    plt.scatter(X, y, color='red')  # Gráfico para ilustrar
    plt.plot(X, pol_reg.predict(poly_reg.fit_transform(X)), color='blue')
    plt.title('Grafo (Polynomial Regression)')
    plt.xlabel('Bateria')
    plt.ylabel('Tempo')
    #plt.show()
    r = pol_reg.predict(poly_reg.fit_transform(
        [[metadeBateria]]))  # Prevê o Y dado um valor X
    # Como o valor X é um tempo eventual, subtraímos esse tempo pelo tempo atual, e calculamos o tempo que resta para chegar ao tempo previsto
    resposta = r - dadosTempo[-1]
    resposta = resposta[0][0]  # Tirar os parenteses
    # Este valor não pode ser menor que 0, portanto se for menor que 0 é porque a previsão é incorreta.
    if (resposta < 0):
        print("Ainda não tenho dados suficientes, tentar mais tarde.")
    else:
        print("Faltam aproximadamente:", resposta, "segundos")
    return


def papelaria():  # função que calcula o caminho mais curto para a papelaria(Questão 3)
    for indice, zona in enumerate(zonas):
        c = indice
        if any("papelaria" in s for s in zona):
            Gaux = G.copy()
            # Adiciona Nodo onde o agente se encontra
            Gaux.add_node("Agente", pos=(listaposicao[0], listaposicao[1]))
            Gaux.add_edge("Agente", "Zona %d" % (verificaCorredorZona()), distance=distancia(
                listaposicao, pontosMedios[indice]))  # liga o nodo Agente ao ponto médio da zona onde se encontra
            Gaux = adicionarEdges("Zona %d" % (
                verificaCorredorZona()), "Agente", Gaux)
            mostraGrafo(Gaux)
            print(
                "O caminho mais curto até à papelaria do Agente até à papelaria é (--->):")
            print(nx.dijkstra_path(Gaux, "Agente", "Zona %d" %
                  (c+1), weight='distance'))

            #print(nx.dijkstra_path(Gaux, "Agente", "Zona %d" % (c+1), weight='distance'))
            return

    print("Não foi ainda encontrada a papelaria")


def saida():  # função que devolve a zona que é a saída, devolve 0 se ainda nao foi encontrada
    for indice, zona in enumerate(zonas):
        c = indice
        if any("caixa" in s for s in zona):
            Gaux = G.copy()
            # Adiciona Nodo onde o agente se encontra
            Gaux.add_node("Agente", pos=(listaposicao[0], listaposicao[1]))
            Gaux.add_edge("Agente", "Zona %d" % (verificaCorredorZona()), distance=distancia(
                listaposicao, pontosMedios[indice]))  # liga o nodo Agente ao ponto médio da zona onde se encontra
            Gaux = adicionarEdges("Zona %d" % (
                verificaCorredorZona()), "Agente", Gaux)
            mostraGrafo(Gaux)
            d = (nx.shortest_path_length(Gaux, "Agente",
                 "Zona %d" % (c+1), weight='distance'))
            mv = np.average(dadosVelocidade)  # média das velocidades guardadas
            tempo = d / mv
            print("O tempo previsto é de", tempo, "segundos")
            return
    print("Ainda não foi encontrada a saída")
    return


def talho():  # função que calcula a distância até ao talho(Questão 3)
    for indice, zona in enumerate(zonas):
        c = indice
        if any("talho" in s for s in zona):
            Gaux = G.copy()
            # Adiciona Nodo onde o agente se encontra
            Gaux.add_node("Agente", pos=(listaposicao[0], listaposicao[1]))
            Gaux.add_edge("Agente", "Zona %d" % (verificaCorredorZona()), distance=distancia(
                listaposicao, pontosMedios[indice]))  # liga o nodo Agente ao ponto médio da zona onde se encontra
            Gaux = adicionarEdges("Zona %d" % (
                verificaCorredorZona()), "Agente", Gaux)
            mostraGrafo(Gaux)
            print("O talho encontra-se a cerca de %f unidades de medida" %
                  (nx.shortest_path_length(Gaux, "Agente", "Zona %d" % (c+1), weight='distance')))
            return

    print("Não foi ainda encontrado o talho")


# função para adicionar edges da zona onde o agente se encontra ao agente, de forma a tornar as distâncias mais realistas
def adicionarEdges(x, y, grafo):
    if x == "Zona 1":
        grafo.add_edge(y, "Zona 7", distance=distancia(
            listaposicao, pontosMedios[6]))
        grafo.add_edge(y, "Zona 2", distance=distancia(
            listaposicao, pontosMedios[1]))
        grafo.add_edge(y, "Zona 3", distance=distancia(
            listaposicao, pontosMedios[2]))
        grafo.add_edge(y, "Zona 16", distance=distancia(
            listaposicao, pontosMedios[15]))
    if x == "Zona 2":
        grafo.add_edge(y, "Zona 8", distance=distancia(
            listaposicao, pontosMedios[7]))
        grafo.add_edge(y, "Zona 4", distance=distancia(
            listaposicao, pontosMedios[3]))
    if x == "Zona 3":
        grafo.add_edge(y, "Zona 4", distance=distancia(
            listaposicao, pontosMedios[3]))
        grafo.add_edge(y, "Zona 15", distance=distancia(
            listaposicao, pontosMedios[14]))
    if x == "Zona 4":
        grafo.add_edge(y, "Zona 9", distance=distancia(
            listaposicao, pontosMedios[8]))
        grafo.add_edge(y, "Zona 14", distance=distancia(
            listaposicao, pontosMedios[13]))
        grafo.add_edge(y, "Zona 5", distance=distancia(
            listaposicao, pontosMedios[4]))
        grafo.add_edge(y, "Zona 6", distance=distancia(
            listaposicao, pontosMedios[5]))
    if x == "Zona 5":
        grafo.add_edge(y, "Zona 10", distance=distancia(
            listaposicao, pontosMedios[9]))
        grafo.add_edge(y, "Zona 11", distance=distancia(
            listaposicao, pontosMedios[10]))
    if x == "Zona 6":
        grafo.add_edge(y, "Zona 13", distance=distancia(
            listaposicao, pontosMedios[12]))
        grafo.add_edge(y, "Zona 12", distance=distancia(
            listaposicao, pontosMedios[11]))
    if x == "Zona 7":
        grafo.add_edge("Zona 1", y, distance=distancia(
            listaposicao, pontosMedios[0]))
    if x == "Zona 8":
        grafo.add_edge(y, "Zona 2", distance=distancia(
            listaposicao, pontosMedios[1]))
    if x == "Zona 9":
        grafo.add_edge(y, "Zona 4", distance=distancia(
            listaposicao, pontosMedios[3]))
    if x == "Zona 10":
        grafo.add_edge(y, "Zona 5", distance=distancia(
            listaposicao, pontosMedios[4]))
    if x == "Zona 11":
        grafo.add_edge(y, "Zona 5", distance=distancia(
            listaposicao, pontosMedios[4]))
    if x == "Zona 12":
        grafo.add_edge(y, "Zona 6", distance=distancia(
            listaposicao, pontosMedios[5]))
    if x == "Zona 13":
        grafo.add_edge(y, "Zona 6", distance=distancia(
            listaposicao, pontosMedios[5]))
    if x == "Zona 14":
        grafo.add_edge(y, "Zona 4", distance=distancia(
            listaposicao, pontosMedios[3]))
    if x == "Zona 15":
        grafo.add_edge(y, "Zona 3", distance=distancia(
            listaposicao, pontosMedios[2]))
    if x == "Zona 16":
        grafo.add_edge(y, "Zona 1", distance=distancia(
            listaposicao, pontosMedios[0]))
    return grafo
