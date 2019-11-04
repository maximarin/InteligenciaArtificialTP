from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, \
    uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer

posicionMapa=(2,0)
posicionSalida=(5,5)

def manhatan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class entrega1(SearchProblem):

    def actions(self, state):
        franceses, piratas = state
        actions = []
        posicion=0

        for pirata in piratas:
            x,y = pirata[0]

            # derecha
            if (y < 5):
                actions.append([(0, 1),posicion])
            # izquierda
            if (y > 0):
                actions.append([( 0, -1),posicion])
            # arriba
            if (x > 0):
                actions.append([( -1, 0),posicion])
            # abajo
            if (x < 5):
                actions.append([(1,0),posicion])

            posicion=posicion+1
        return actions

    def result(self, state, action):
        franceses, piratas = state
        posicionMover,nroBarco = action


        lista_Estado = [list(franceses), list(piratas)]
        nuevapos = (lista_Estado[1][nroBarco][0][0] + posicionMover[0], lista_Estado[1][nroBarco][0][1] +posicionMover[1])

        #Si esta en la misma posicion que el mapa
        if nuevapos == posicionMapa:
            lista_Estado[1][nroBarco] = (nuevapos, 1)
        elif nuevapos in lista_Estado[0]:
            lista_Estado[0].remove(nuevapos)
            lista_Estado[1].pop(nroBarco)
        else:
             lista_Estado[1][nroBarco] = (nuevapos,piratas[nroBarco][1])

        franceses =tuple(lista_Estado[0])
        piratas =tuple(lista_Estado[1])

        return (franceses, piratas)

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        franceses, piratas = state

        for p in piratas:
            if p[0]==posicionSalida and p[1]==1:
                return True
        return False

    def heuristic(self, state):
        franceses, piratas =state
        listaCosto = []
        menor = 0

        for pirata in piratas:
            posicion, mapa = pirata
            posx,posy = posicion
            menor = 0
            if mapa == 1:
                #Solo se debe tener en cuenta la distancia a llegada(5,5) porque ya tiene el mapa
                costo = abs(posx - posicionSalida[0]) + abs(posy - posicionSalida[1])
                if(menor == 0):
                    menor = costo
                else:
                    if(costo < menor):
                        menor = costo
            else:
                #distancia hasta el mapa + la distancia del mapa a la llegada
                costo = (abs(posx - posicionMapa[0]) + abs(posy-posicionMapa[1])) + (abs(posicionMapa[0] - posicionSalida[0]) + abs(posicionMapa[1] - posicionSalida[1]))
                if(menor == 0):
                    menor = costo
                else:
                    if(costo < menor):
                         menor = costo

        return menor


def resolver(metodo_busqueda, franceses, piratas):
    viewer = BaseViewer()
    barcos_piratas = []

    for pirata in piratas:
        barcos_piratas.append((pirata, 0))

    initial = (tuple(franceses), tuple(barcos_piratas))

    problem = entrega1(initial)

    if metodo_busqueda == "breadth_first":
        resultado = breadth_first(problem, graph_search=True, viewer=viewer)
    elif metodo_busqueda == "greedy":
        resultado = greedy(problem, graph_search=True, viewer = viewer)
    elif metodo_busqueda == "depth_first":
        resultado = depth_first(problem, graph_search=True, viewer = viewer)
    elif metodo_busqueda == "astar":
        resultado = astar(problem, graph_search=True, viewer = viewer)
    elif metodo_busqueda == "uniform_cost":
        resultado = uniform_cost(problem, graph_search=True, viewer = viewer)

    return resultado

""""
if __name__ == '__main__':

    #metodo = "greedy"
    metodo = "breadth_first"
    #metodo = "astar"
    #metodo = "uniform_cost"
    #metodo = "depth_first"

    franceses = [(0,2), (0,3), (1,2), (1,3), (2,1), (2,2), (2,3), (3,0), (3,1), (3,2), (4,0), (4,1), (5,0)]
    piratas = [(4,4), (4,5), (5,4)]

    result = resolver(metodo, franceses, piratas)
   
"""



