import GeneticFunctions as gf
import numpy as np
import imageio
import os
import cv2

def run(image, generation_size, population_size, mutation_percent, flag_filter):
    target_image = imageio.imread(image, pilmode="RGB")
    
    if flag_filter == 1:
        target_image = cv2.GaussianBlur(target_image, (5,5), sigmaX = 0)

    target_chromosome = gf.image_to_chromossome(target_image)
    image_shape = target_image.shape

    num_parents_mating = population_size//2

    population = gf.generate_initial_population(image_shape, population_size)

    print('\n Target Fitnes', np.sum(target_chromosome), '\n')

    for iteration in range(generation_size + 1):
        qualities = gf.calculate_population_fitness(target_chromosome, population)
        parents = gf.select_mating_pool(population, qualities, num_parents_mating)
        population = gf.crossover(parents, image_shape, population_size)
        population = gf.mutation(population, num_parents_mating, mutation_percent)
        gf.print_and_save_image(iteration, target_image, qualities, population, image_shape, 500, os.curdir+'//')

run('apple_low_res.jpg', 10000, 64, 0.05, 1)