import random as rnd

def genotype_numbers():
    return [round(rnd.uniform(-5.12, 5.12), 5) for _ in range(n_solution)]

def child_fitness_gen(number):
    total_sum = 0
    n = len(number)

    for i in range(n):
        for _ in range(n_solution): 
            total_sum += number[i]**2

    fit = 1/(1 + abs(total_sum))
        
    return fit

def child_fitness(number):
    total_sum = 0

    for _ in range(n_solution): 
        total_sum += number**2

    fit = 1/(1 + abs(total_sum))

    return fit

def selected_tournment(population):
    n = len(population)
    return bigger_fitness_genotype(population[rnd.randint(0, n-1):n])

def roulette_wheel(population):
    probabilities = [probability(n) for n in population]

    total = sum(probabilities)
    pick = rnd.uniform(0, total)
    current = 0

    for i in range(len(probabilities)):
        current += probabilities[i]
        if current > pick:
            return i

def probability(chromosome):
    return child_fitness(chromosome)

def pick_parent(population):
    selected_tournment_probability = 0.02

    if (selected_tournment_probability > rnd.random()):
        parent = selected_tournment(population)
    else:
        parent = population[roulette_wheel(population)]

    return parent

def crossover(x, y):
    # n = len(x)
    # c = rnd.randint(0, n - 1)
    #return x[0:c] + y[c:n], y[0:c] + x[c:n]
    return (x+y)*x, (x+y)*y

def mutate(child):
    mutation_probability = 0.05

    if (mutation_probability > rnd.random()):
        # n = len(child)
        # position = rnd.randrange(0, n)
        # child[position] = round(rnd.uniform(-5.12, 5.12), 5)
        # n = len(child)
        # position = rnd.randrange(0, n)
        child = round(rnd.uniform(-5.12, 5.12), 5)

    return child

def pick_children(parent1, parent2):
    child1, child2 = crossover(parent1, parent2)
    child1 = mutate(child1)
    child2 = mutate(child2)

    child = bigger_fitness_genotype([child1, child2])

    return child

def new_generation(population):
    new_population = []
    for chrom in population:
        new_chrom = []
        for _ in range(len(chrom)):
            parent1 = pick_parent(chrom)
            parent2 = pick_parent(chrom)
            child = pick_children(parent1, parent2)
            show_children(child)
            new_chrom.append(child)

        new_population.append(new_chrom)

        # if child_fitness(child) == perfect_solution: break

    return new_population

def show_children(child):
    print('number = {}, fitness = {}'
        .format(str(child), child_fitness(child)))

def find_best_population(population):
    generation = 0
    max_generation = 1024
    
    while generation < max_generation and not is_perfect_solution(population):
        generation += 1
        population = new_generation(population)
        print('generation = {}, best fitness = {}'.format(generation, (max([child_fitness_gen(n) for n in population]))))

    print('found a generation', generation)
    return population

def is_perfect_solution(population):
    for chrom in population:
        for number in chrom:
            fit = child_fitness(number)
            if (fit > (perfect_solution - limit_solution) and fit < (perfect_solution + limit_solution)):
                return True
    return False

def bigger_fitness_genotype(population):
    best_fitness = 0

    for chrom in population:
        if child_fitness(chrom) > best_fitness:
            best_fitness = child_fitness(chrom)
            c = chrom
    
    return c

def bigger_fitness_number(population):
    best_fitness = 0

    for chrom in population:
        for number in chrom:
            fit = child_fitness(number)
            if (fit > best_fitness):
                best_fitness = child_fitness(number)
                c = number
        
    return c

print('-----------------------------------')
n_solution = 10
perfect_solution = 1/(1+0)
print('max fitness:', perfect_solution)

limit_solution = 1e-4

n_population = 10
print('n_population:', n_population)
print('-----------------------------------')

population = [ genotype_numbers() for _ in range(n_population) ]

best_pouplation = find_best_population(population)
bigger_fitness = bigger_fitness_number(best_pouplation)


print('-----------------------------------')
print('n queen problem - genetic algorithm')
print('n_solution:', n_solution)
print('n_population:', n_population)
print('max fitness:', perfect_solution)
print('-----------------------------------')
fit = child_fitness(bigger_fitness)
if (fit > (perfect_solution - limit_solution) and fit < (perfect_solution + limit_solution)):
    print('found a solution by fitness')
else:
    print('no solution, stopped by generation limit')
print('found fitness:', child_fitness(bigger_fitness))
print('best_number:', bigger_fitness)
print('-----------------------------------')