
import numpy as np

import utils


def ga_algorithm(setup):

    # Setup config
    n_iter = setup['N_ITER']
    n_pop = setup['N_POP']
    n_cities = setup['N_CITIES']
    origin = setup['ORIGIN'] 
    type_selection = setup['TYPE_SELECTION']
    type_crossover = setup['TYPE_CROSSOVER']
    grafo = setup['GRAFO']
    probability_mutation = setup['PROBABILITY_MUTATION']
    
    if grafo == None:
        grafo = []
    else:
        pass 


    # Creating variables in the iterations procedure
    X = np.zeros((n_pop, n_cities))
    OF = np.zeros((n_pop, 1))
    FIT = np.zeros((n_pop, 1))

    # Initial population
    X = utils.initial_population_tsp(n_pop, n_cities, X)

    for i in range(n_pop):
        OF[i, 0] = utils.objective_function(X[i], origin, grafo['Grafo'])
        FIT[i, 0] = utils.fit_value(OF[i, 0])
        

    # Iteration procedure
    for iter in range(n_iter):
        new_population = np.zeros((n_pop, n_cities))
        for individual in range(n_pop):
            # Selection procedure
            if type_selection == 'ROULETTE WHEEL':
                # Roulette wheel
                parent_1_position, parent_2_position = utils.roulette_wheel_selection(FIT, n_pop)
            elif type_selection == 'TOURNAMENT':
                # Tournament
                parent_1_position, parent_2_position = utils.tournament_selection(FIT, n_pop)
            
            if type_crossover == 'TSP CROSSOVER':
                child_1, _ = utils.crossover(X[parent_1_position], X[parent_2_position])
            
            new_population[individual] = child_1


        new_of, new_fit = utils.update_fit(new_population, origin, grafo, n_pop)
        new_population = utils.mutation(new_population, new_of, probability_mutation, grafo['Grafo'])
        
        X = np.concatenate((X, new_population))
        OF = np.concatenate((OF, new_of))
        FIT = np.concatenate((FIT, new_fit))
        
        X, OF, FIT = utils.update_population(X, OF, FIT, n_pop, n_cities)                                     
      
    
    return X, OF, FIT
