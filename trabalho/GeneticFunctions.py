import numpy as np
import functools
import operator
import matplotlib.pyplot
import random
import itertools

## 

def image_to_chromossome(image_array):
    return np.reshape(a = image_array, newshape = (functools.reduce(operator.mul, image_array.shape)))

def chromossome_to_image(chromossome_array, image_shape):
    return np.reshape(a = chromossome_array, newshape = image_shape)

##

def initial_population(image_shape, n_individuals):
    population = np.empty(
        shape=(n_individuals, functools.reduce(operator.mul, image_shape)),
        dtype=np.uint8)

    for i in range(n_individuals):
        population[i, :] = np.random.random(
            functools.reduce(operator.mul, image_shape))*256

    return population

##

def fitness(target_chromosome, solution):
    fitness = np.mean(np.abs(target_chromosome - solution))
    fitness = np.sum(target_chromosome) - fitness

    return fitness

def calculate_population_fitness(target_chromossome, population):
    qualities = np.zeros(population.shape[0])

    for i in range(population.shape[0]):
        qualities[i] = fitness(target_chromossome, population[i, :])

    return qualities

##

def select_mating_pool(population, qualities, num_parents):
    parents = np.empty((num_parents, population.shape[1]), dtype=np.uint8)

    for parent_num in range(num_parents):
        max_fitness_idx = np.where(qualities == np.max(qualities))
        max_fitness_idx = max_fitness_idx[0][0]

        parents[parent_num, :] = population[max_fitness_idx, :]

        qualities[max_fitness_idx] = -1

    return parents

def crossover(parents, image_shape, n_individuals):
    children = np.empty(
        shape=(n_individuals, functools.reduce(operator.mul, image_shape)),
        dtype=np.uint8)

    children[0:parents.shape[0], :] = parents
    
    num_newly_genereted_children = n_individuals - parents.shape[0]
    parents_permutation = list(itertools.permutations(iterable = np.arange(0, parents.shape[0]), r = 2))
    selected_permutations = random.sample(range(len(parents_permutation)), num_newly_genereted_children)
    
    comb_index = parents.shape[0]
    
    for comb in range(len(selected_permutations)):
        selected_comb_index = selected_permutations[comb]
        selected_comb = parents_permutation[selected_comb_index]

        half_size = children.shape[1]//2

        children[comb_index + comb, :half_size] = parents[selected_comb[0], :half_size]
        children[comb_index + comb, half_size:] = parents[selected_comb[1], half_size:]
  
    return children

def mutation(population, num_parents_mating, mutation_percent):
    for index in range(num_parents_mating, population.shape[0]):
        random_index = np.uint32(
            np.random.random(size = np.uint32(mutation_percent/100 * population.shape[1]))
                    * population.shape[1])
        
        new_values = np.uint8(np.random.random(size=random_index.shape[0])*256)
        
        population[index, random_index] = new_values
    
    return population

##

def save_image(current_iteration, qualities, new_population, image_shape, save_point, save_diretory):
    if current_iteration % 100 == 0:
        print("Generation: ", current_iteration, "\t Fitness: ", np.max(qualities))
    
    if current_iteration % save_point == 0:
        matplotlib.pyplot.imsave(save_diretory+'/'+str(
            current_iteration)+'.png', 
            chromossome_to_image(new_population[np.where(qualities == np.max(qualities))[0][0], :], 
            image_shape))

##
