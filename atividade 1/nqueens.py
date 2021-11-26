import random

def find_best_fitness(max_fitness, population):
    generation = 0

    while generation < 500 and not max_fitness in [fitness(queens) for queens in population]:
        generation += 1
        population = new_generation(population, fitness)
        print('generation = {}, fitness = {}'.format(generation, (max([fitness(n) for n in population]))))

    print('found a generation', generation)
    return population

# VERIFICAR FUNCAO, MELHORAR, ALTERAR
def fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen)-1 for queen in chromosome])/2

    n = len(chromosome)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    
    return int(max_collisions - (horizontal_collisions + diagonal_collisions))

def new_generation(population, fitness):
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for _ in range(len(population)):
        parent1 = pick_parent(population, probabilities)
        parent2 = pick_parent(population, probabilities)
        child = pick_child(parent1, parent2)
        # show_children(child)
        new_population.append(child)

        if fitness(child) == max_collisions: break
    return new_population

def probability(chromosome, fitness):
    return fitness(chromosome) / max_collisions

def pick_parent(population, probabilities):
    selected_tournment_probability = 0.1

    if (selected_tournment_probability > random.random()):
        parent = selected_tournment(population)
    else:
        parent = population[roulette_wheel(probabilities)]

    return parent

# VERIFICAR SE PODE FAZER ISSO AQUI
def selected_tournment(population):
    n = len(population)
    return best_queen(population[random.randint(0, n-1):n])
    
# VERIFICAR ISSO AQUI
def roulette_wheel(probabilities):
    total = sum(probabilities)
    pick = random.uniform(0, total)
    current = 0
    for i in range(len(probabilities)):
        current += probabilities[i]
        if current > pick:
            return i

def pick_child(parent1, parent2):
    mutation_probability = 0.05

    child = crossover(parent1, parent2)

    if (mutation_probability > random.random()):
        child = mutate(child)

    return child

# VERIFICAR ISSO AQUI
def crossover(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

# VERIFICAR ISSO AQUI
def mutate(chromosome):
    n = len(chromosome)
    position = random.randrange(0, n)
    chromosome[position] = random.randrange(1, n + 1)
    return chromosome

def show_children(child):
    print('chromosome = {}, fitness = {}'
        .format(str(child), fitness(child)))

def best_queen(population):
    best_fitness = 0

    for chrom in population:
        if fitness(chrom) > best_fitness:
            best_fitness = fitness(chrom)
            c = chrom
    
    return c
    
def print_board(board_queens, n):
    board = []
    for _ in range(n):
        board.append(["x"] * n)
    for i in range(n):
        board[board_queens[i]-1][i]="Q"
    for row in board:
        print (" ".join(row))

def genotype_queens(n):
    return [ random.randint(1, n) for _ in range(n)]
    
if __name__ == "__main__":
    n_queens = int(input("number of queens: "))
    max_collisions = (n_queens*(n_queens-1))/2

    n_population = (2*n_queens)**2
    population = [genotype_queens(n_queens) for _ in range(n_population)]

    best_pouplation = find_best_fitness(max_collisions, population)
    best_queen = best_queen(best_pouplation)

    print('-----------------------------------')
    print('n queen problem - genetic algorithm')
    print('alberto romanhol moreira')
    print('n_queens:', n_queens)
    print('n_population:', n_population)
    print('max fitness:', max_collisions)
    print('-----------------------------------')
    if fitness(best_queen) == max_collisions:
        print('found a solution by fitness')
    else:
        print('no solution, stopped by generation limit')
    print('found fitness:', fitness(best_queen))
    print('best_queen:',best_queen)
    print_board(best_queen, n_queens)
    print('-----------------------------------')