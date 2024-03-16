import genetico
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math

def plot_route(individual, mapa, origin):
    m = Basemap(projection='lcc', resolution=None,
                width=5E6, height=5E6,
                lat_0=-15, lon_0=-56)
    
    plt.axis('off')
    plt.title("Rota mais curta")

    for i in range(0, len(individual)):
        x, y = m(float(mapa[int(individual[i])][1]), float(mapa[int(individual[i])][2]))

        if i == origin:
            plt.plot(x, y, 'ok', c='r', markersize=5)
        else:
            plt.plot(x, y, 'ok', c='b', markersize=5)
            
        if i == len(individual) - 1:
            x2, y2 = m(float(mapa[int(individual[0])][1]), float(mapa[int(individual[0])][2]))
        else:
            x2, y2 = m(float(mapa[int(individual[i+1])][1]), float(mapa[int(individual[i+1])][2]))

        plt.plot([x, x2], [y, y2], 'k-', c='g')
    plt.show()


def dist(V, u, v):
    return math.sqrt(pow((float(V[u][1]) - float(V[v][1])),2) + pow((float(V[u][2]) - float(V[v][2])),2))


##############################################################################################################

file1 = open('entrada.txt', 'r')
Lines = file1.readlines()

N = int(Lines[0].strip())

adjVec = [{} for i in range(N)]

mapa = []
for i in range(1, len(Lines)):
    mapa.append(Lines[i].strip().split(' '))

for i in range(N):
    for j in range(N):
        if i != j:
            adjVec[int(i)][str(j)] = int(dist(mapa, int(i), int(j)))


grafo = {'Grafo': adjVec}

SETUP = {
        'N_ITER': 50,
        'N_POP':  50,
        'N_CITIES':      N,
        'ORIGIN': 0,
        'TYPE_SELECTION': 'TOURNAMENT',
        'TYPE_CROSSOVER': 'TSP CROSSOVER',
        'PROBABILITY_MUTATION': 0.4,
        'GRAFO': grafo
}


X, OF, FIT = genetico.ga_algorithm(SETUP)


plot_route(X[0], mapa, 0)


