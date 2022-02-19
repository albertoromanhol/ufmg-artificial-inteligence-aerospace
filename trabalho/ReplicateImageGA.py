import matplotlib.pyplot
import numpy as np
import itertools
import functools
import operator
import imageio
import random
import cv2
import os

from skimage.metrics import structural_similarity as ssim

## 

def image_to_chromossome(image_array):
    return np.reshape(a = image_array, 
        newshape = (functools.reduce(operator.mul, image_array.shape)))

def chromossome_to_image(chromossome_array, image_shape):
    return np.reshape(a = chromossome_array, newshape = image_shape)

##

def generate_initial_population(image_shape, n_individuals):
    population = np.empty(
        shape=(n_individuals, functools.reduce(operator.mul, image_shape)),
        dtype=np.uint8)

    for i in range(n_individuals):
        population[i, :] = np.random.random(
            functools.reduce(operator.mul, image_shape))*256

    return population

##

def calculate_fitness(target_chromosome, solution):
    fitness = np.mean(np.abs(target_chromosome - solution))
    fitness = np.sum(target_chromosome) - fitness

    return fitness

def calculate_population_fitness(target_chromossome, population):
    qualities = np.zeros(population.shape[0])

    for i in range(population.shape[0]):
        qualities[i] = calculate_fitness(target_chromossome, population[i, :])

    return qualities

##

def select_mating_pool(population, qualities, num_parents):
    parents = np.empty((num_parents, population.shape[1]), dtype=np.uint8)

    for parent_num in range(num_parents):
        max_fitness_index = np.where(qualities == np.max(qualities))
        max_fitness_index = max_fitness_index[0][0]

        parents[parent_num, :] = population[max_fitness_index, :]

        qualities[max_fitness_index] = -1

    return parents

def crossover(parents, image_shape, n_individuals):
    population = np.empty(
        shape=(n_individuals, functools.reduce(operator.mul, image_shape)),
        dtype=np.uint8)

    population[0:parents.shape[0], :] = parents
    
    number_genereted_population = n_individuals - parents.shape[0]
    parents_permutation_possible = list(itertools.permutations(iterable = np.arange(0, parents.shape[0]), r = 2))
    selected_permutations = random.sample(range(len(parents_permutation_possible)), number_genereted_population)
    
    genes_index = parents.shape[0]
    
    for genes in range(len(selected_permutations)):
        selected_genes_index = selected_permutations[genes]
        selected_genes = parents_permutation_possible[selected_genes_index]

        half_size = population.shape[1]//2

        population[genes_index + genes, :half_size] = parents[selected_genes[0], :half_size]
        population[genes_index + genes, half_size:] = parents[selected_genes[1], half_size:]
  
    return population

def mutation(population, num_parents_mating, mutation_percent):
    for index in range(num_parents_mating, population.shape[0]):
        random_index = np.uint32(
            np.random.random(size = np.uint32(mutation_percent/100 * population.shape[1]))
                    * population.shape[1])
        
        new_values = np.uint8(np.random.random(size=random_index.shape[0])*256)
        
        population[index, random_index] = new_values
    
    return population

##

def print_and_save_image(current_iteration, target_image, qualities, new_population, image_shape, save_point, save_diretory):
    if current_iteration % 100 == 0:
        print("Generation: ", current_iteration, "\t Fitness: ", np.max(qualities))
        
        image =  chromossome_to_image(new_population[np.where(qualities == np.max(qualities))[0][0], :], target_image.shape)
        ssimResult = ssim(target_image, image, multichannel=True)
        print('SSIM Score: ' + str(ssimResult))

        print('\n')	

    
    if current_iteration % save_point == 0:
        matplotlib.pyplot.imsave(save_diretory+'/'+str(
            current_iteration)+'.png', 
            chromossome_to_image(new_population[np.where(qualities == np.max(qualities))[0][0], :], 
            image_shape))

##

def run(image, generation_size, population_size, mutation_percent, gaussian_filter = False):
    target_image = imageio.imread(image, pilmode="RGB")
    
    if gaussian_filter:
        target_image = cv2.GaussianBlur(target_image, (5,5), sigmaX = 0)

    target_chromosome = image_to_chromossome(target_image)
    image_shape = target_image.shape

    num_parents_mating = population_size//2

    population = generate_initial_population(image_shape, population_size)

    print('\n Target Fitnes', np.sum(target_chromosome), '\n')

    for iteration in range(generation_size + 1):
        qualities = calculate_population_fitness(target_chromosome, population)
        parents = select_mating_pool(population, qualities, num_parents_mating)
        population = crossover(parents, image_shape, population_size)
        population = mutation(population, num_parents_mating, mutation_percent)
        print_and_save_image(iteration, target_image, qualities, population, image_shape, 500, os.curdir+'//')

##
run('heart.png', 20000, 128, 0.05, True)