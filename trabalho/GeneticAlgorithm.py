import GeneticFunctions as gf
import numpy as np
import imageio
import os

def run(image, generation_size, population_size, mutation_percent):
    target_image = imageio.imread(image)
    target_image = np.asarray(target_image/255, dtype = np.float64)
    image_shape = target_image.shape
    
    target_chromosome = gf.image_to_chromossome(target_image)

    num_parents_mating = population_size//2

    new_population = gf.initial_population(target_image.shape, population_size)

    print('\n Target Fitnes', np.sum(target_chromosome), '\n')

    for iteration in range(generation_size + 1):
        qualities = gf.calculate_population_fitness(target_chromosome, new_population)
        parents = gf.select_mating_pool(new_population, qualities, num_parents_mating)
        population = gf.crossover(parents, image_shape, population_size)
        population = gf.mutation(new_population, num_parents_mating, mutation_percent)
        gf.save_image(iteration, qualities, population, image_shape, 500, os.curdir+'//')