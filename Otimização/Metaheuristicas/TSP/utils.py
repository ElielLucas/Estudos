import numpy as np
from random import randint, randrange


def initial_population_tsp(n_pop, n_cities, X):    
    for i in range(n_pop):      
        chromosome = np.random.choice(n_cities, n_cities, replace = False)
        X[i] = chromosome
        
    return X

def objective_function(X, origin, grafo):
    weight_matrix = grafo
    N = len(X)
    output = 0
    if (X[0] == origin):
        for I in range(N - 1):
            u = int(X[I])
            v = str(int(X[I + 1]))
            w = weight_matrix[u][v]
            if w == 0:
                return 999999
            output+= w
        u = int(X[I + 1])
        v = str(int(X[0]))
        w = weight_matrix[u][v]
        if w == 0:
            return 999999
        output+= w
    else:
        return 999999
    
    return output


def fit_value(of_value):
    if of_value >= 0:
        fit_value = 1 / (1 + of_value)
    elif of_value < 0:
        fit_value = 1 + abs(of_value)
    return fit_value



def update_population(X, OF, fit, n_pop, n_cities):
    sort_positions = np.argsort(OF.T)[0]
    
    new_x = np.zeros((n_pop, n_cities))
    new_of = np.zeros((n_pop, 1))
    new_fit = np.zeros((n_pop, 1))
    
    for i in range(n_pop):
        new_x[i] = X[sort_positions[i]]
        new_of[i] = OF[sort_positions[i]]
        new_fit[i] = fit[sort_positions[i]]
        
    return new_x, new_of, new_fit


def update_fit(X, origin, grafo, n_pop):
    new_of = np.zeros((n_pop, 1))
    new_fit = np.zeros((n_pop, 1))
    for i in range(n_pop):
        new_of[i, 0] = objective_function(X[i], origin, grafo['Grafo'])
        new_fit[i, 0] = fit_value(new_of[i, 0])
        
    return new_of, new_fit
    
def roulette_wheel_selection(fit, n_pop):
    IDS = np.linspace(0, n_pop, n_pop, endpoint = False)
    sum_fit = fit.sum()
    PROB = []
    for I_COUNT in range(n_pop):
        FIT_K = fit[I_COUNT][0]
        PROB_K = FIT_K / sum_fit
        PROB.append(PROB_K)

    IDS = np.random.choice(IDS, 2, replace = False, p = PROB)

    return (int(IDS[0]), int(IDS[1]))

def tournament_selection(fit, n_pop):
    selecionados = []
    for i in range(n_pop):
      cromossomo_1 = randint(0, n_pop-1)
      cromossomo_2 = randint(0, n_pop-1)

      if fit[cromossomo_1] > fit[cromossomo_2]:
          selecionados.append(cromossomo_1)
      else:
          selecionados.append(cromossomo_2)
    return (selecionados[0], selecionados[1])


def crossover(PARENT_1, PARENT_2):
    N = len(PARENT_1)
    crossover_point = randint(1, N - 1)
    
    piece_1 = PARENT_1[:crossover_point]
    piece_2 = PARENT_2[:crossover_point]
    
    for i in range(N):
        if PARENT_1[i] not in piece_2:
            piece_2 = np.append(piece_2, PARENT_1[i])
        if PARENT_2[i] not in piece_1:
            piece_1 = np.append(piece_1, PARENT_2[i])

    return (piece_1, piece_2)


def cost_change(matriz_custo, n1, n2, n3, n4):
    return matriz_custo[n1][str(n3)] + matriz_custo[n2][str(n4)] - matriz_custo[n1][str(n2)] - matriz_custo[n3][str(n4)]

def two_opt(route, cost_mat):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                if cost_change(cost_mat, int(best[i - 1]), int(best[i]), int(best[j - 1]), int(best[j])) < 0:
                    best[i:j] = best[j - 1:i - 1:-1]
                    improved = True
        route = best
            
    return best


def mutation(X, OF, probability_mutation, matriz_custo):
    sort_positions = np.argsort(OF.T)[0][::-1]
    N = int(len(X) * probability_mutation)
    
    for i in range(N):
        cromossomo = X[sort_positions[i]].tolist()
        cross_size = len(cromossomo)
        GENE_1 = 0
        GENE_2 = 0
        while GENE_1 == GENE_2:
            GENE_1 = randrange(cross_size)
            GENE_2 = randrange(GENE_1, cross_size)

        cromossomo[GENE_1], cromossomo[GENE_2] = cromossomo[GENE_2], cromossomo[GENE_1]
        cromossomo = two_opt(cromossomo, list(matriz_custo))
        X[sort_positions[i]] = cromossomo
    
    return X


    
def ONE_POINT_CROSSOVER(PARENT_1, PARENT_2):

    crossover_point = randint(1, len(PARENT_1) - 1)

    child_1 = PARENT_1[:crossover_point] + PARENT_2[crossover_point:]
    child_2 = PARENT_2[:crossover_point] + PARENT_1[crossover_point:]

    return (child_1, child_2)



def MULTI_POINT_CROSSOVER(PARENT_1, PARENT_2, N):
    
    crossover_point = sorted(set([randint(1, len(PARENT_1) - 1) for i in range(N)]))

    child_1 = PARENT_1[:crossover_point[0]] + PARENT_2[crossover_point[0]:crossover_point[1]] + PARENT_2[crossover_point[1]:]
    child_2 = PARENT_2[:crossover_point[0]] + PARENT_1[crossover_point[0]:crossover_point[1]] + PARENT_1[crossover_point[1]:]

    return (child_1, child_2)


def UNIFORM_CROSSOVER(PARENT_1, PARENT_2):

    child_1 = []
    child_2 = []
    for gene in range(len(PARENT_1)):
        chosen = randint(1, 2)

        if chosen == 1:
            child_1.append(PARENT_1[gene])
            child_2.append(PARENT_2[gene])
        else:
            child_1.append(PARENT_1[gene])
            child_2.append(PARENT_2[gene])

    return (child_1, child_2)