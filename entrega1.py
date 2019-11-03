from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer, ConsoleViewer

franceses = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (5, 0)]
piratas = [(4, 4), (4, 5), (5, 4)]
MovimientosPosibles = ((0,1),(0,2),(0,3),(0,4),(0,5),
                       (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),
                       (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),
                       (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),
                       (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),
                       (5,0),(5,1),(5,2),(5,3),(5,4),(5,5))
mapa = (2, 0)
llegada = (5, 5)

Initial =()


def resolver (metodo_busqueda,franceses, piratas):
    franc = tuple(franceses)
    pirat = tuple(piratas)
    mapasEncontrados = []


    for pirata in range(len(pirat)):
        mapasEncontrados.append(0)

    indice = 0
    initial = (franc,pirat,tuple(mapasEncontrados))
    metodo = str(metodo_busqueda).lower()

    if metodo == "breadth_first":
        resultado = breadth_first(Entrega1(initial))

    if metodo == "depth_first":
        resultado = depth_first(Entrega1(initial))

    if metodo == "uniform_cost":
        resultado= uniform_cost(Entrega1(initial))

    if metodo == "greedy":
        resultado = greedy(Entrega1(initial))

    if metodo == 'astar':
        resultado = astar(Entrega1(initial), viewer=BaseViewer())

    return resultado

def convertir_lista(listaDetuplas):
    listaRetornar = [list(elem) for elem in listaDetuplas]
    return listaRetornar

def convertir_tupla(listaDeListas):
    listaRetornar = tuple([tuple(elem) for elem in listaDeListas])

    return listaRetornar

class Entrega1(SearchProblem):

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        franceses,piratas,mapasEncontrados = state

        if 1 in mapasEncontrados:
            for pirata in piratas:
                indice = piratas.index(pirata)
                if mapasEncontrados[indice] == 1 and pirata[1] == 5 and pirata[0] == 5:
                    return True
        return False

    def actions(self, state):
        franceses, piratas, mapasEncontrados = state
        acciones = []  #se devolver una lista de la siguiente manera  [(posx,posy),nroBarco]

        #movimientos
        for pirata in piratas:
            x,y = pirata
            nroBarco = piratas.index(pirata)

            #Pregunto si el barco tiene el mapa
            if mapasEncontrados[nroBarco] != 1:
                #Si no tiene el mapa puedo moverme por cualquier posicion
                if (x+1,y) < 5:
                    acciones.append([(x+1,y),piratas.index(pirata)])

                if (x-1,y) > 0:
                    acciones.append([(x-1,y),piratas.index(pirata)])

                if (x,y+1) < 5:
                    acciones.append([(x,y+1),piratas.index(pirata)])

                if(x,y-1) > 0:
                    acciones.append([(x, y -1), piratas.index(pirata)])

            else:
                # Si tiene el mapa solo muevo por posiciones donde no hay franceses
                if (x+1,y) < 5 and (x+1,y) not in franceses:
                    acciones.append([(x+1,y),piratas.index(pirata)])

                if (x-1,y) > 0 and (x-1,y) not in franceses:
                    acciones.append([(x-1,y),piratas.index(pirata)])

                if (x,y+1) < 5 and (x,y+1) not in franceses:
                    acciones.append([(x,y+1),piratas.index(pirata)])

                if (x,y-1) > 0 and (x,y-1) not in franceses:
                    acciones.append([(x,y-1),piratas.index(pirata)])

        return acciones


    def result(self, state, action):
        franceses, piratas, mapasEncontrados = state
        pos, nroBarco = action
        posAccionX,postAccionY= pos
        #si la pos de la accion lleva al mapa, actualizo la tupla de mapas encontrados
        if pos == mapa:
            mapasEncontradosLista = convertir_lista(mapasEncontrados)
            mapasEncontradosLista[nroBarco] = 1
            mapasEncontradosTupla = convertir_tupla(mapasEncontradosLista)
            mapasEncontrados = mapasEncontradosTupla

        #SI hay franceses en la posicion a la cual lleva al accion, elimino el barco frances y el pirata
        if pos in franceses:
            francesesLista = convertir_lista(franceses)
            posicionEliminar = [pos[0],pos[1]]
            francesesLista.remove(posicionEliminar)
            francesesTupla = convertir_tupla(francesesLista)
            franceses = francesesTupla

            piratasLista = convertir_lista(piratas)
            pirtataAEliminar = piratasLista[nroBarco]
            piratasLista.remove(pirtataAEliminar)
            piratasTupla = convertir_tupla(piratasLista)
            piratas = piratasTupla
        else:
            #El barco pirata se mueve a una posición donde no hay franceses.
            piratasLista = convertir_lista(piratas)
            piratasLista[nroBarco][0] = posAccionX
            piratasLista[nroBarco][1] = postAccionY
            piratasTupla = convertir_tupla(piratasLista)
            piratas = piratasTupla

        return franceses,piratas,mapasEncontrados


    def heuristic(self, state):
        franceses, piratas,mapasEncontrados = state
        listaCostos = []
        #Se corrobora cuanto falta para llegar a la meta

        for pirata in piratas:
            indice = piratas.index(pirata)
            barcoX,barcoY = pirata

            #si ya tiene el mapa se calcula la distancia a (5,5)
            if mapasEncontrados[indice] == 1:
                llegadaX,llegadaY = llegada
                costo = abs(barcoX - llegadaX) + abs(barcoY-llegadaY)

            else:
                #si no tiene el mapa se calcula la distancia para llegar al mapa y luego volver a (5,5)
                mapaX,mapaY = mapa
                llegadaX, llegadaY = llegada

                costo = abs(barcoX - mapaX) + abs(barcoY-mapaY) + abs(mapaX - llegadaX) + abs(mapaY - llegadaY)

            listaCostos.append(costo)
            minimo = min (listaCostos)

        return min(listaCostos)


if __name__ == '__main__':

    print(' ')
    visor = BaseViewer()

    result = resolver("astar",franceses,piratas)

    print('-----------------<Result Path>-----------------')

    for action, state in result.path():
        print('Action:', action)
        print(state)

    print('------------------------------------------------')
    print('Result State: ', result.state)
    print(visor.stats)



