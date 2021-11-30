import random
import numpy

def find_best_fitness(max_fitness, population):
    generation = 0
    
    max_generation = -13*len(population[0]) + 277
    print('max_generation = {}'.format(max_generation))
    
    while generation < max_generation and not max_fitness in [fitness(queens) for queens in population]:
        generation += 1
        population = new_generation(population, fitness)
        print('generation = {}, fitness = {}'.format(generation, (max([fitness(n) for n in population]))))

    print('found a generation', generation)
    return population

def fitness(chromosome):
    score = 0
    n = len(chromosome)
    chromosome = numpy.array(chromosome) - 1

    for col in range(n): 
        row = chromosome[col]  
        
        for other_col in range(n):
            if other_col == col: # MESMA COLUNA 
                continue
            if chromosome[other_col] == row: # MESMA LINHA
                continue
            if other_col + chromosome[other_col] == col + row: # DIAGONAL SUPERIOR
                continue
            if other_col - chromosome[other_col] == col - row: # DIAGONAL INFERIOR
                continue
            # se nao atacar, pode ter score + 1, nao vai capturar
            score += 1
    return score/2

def new_generation(population, fitness):
    new_population = []
    probabilities = [probability(n, fitness) for n in population]

    for _ in range(len(population)):
        parent1 = pick_parent(population, probabilities)
        parent2 = pick_parent(population, probabilities)
        child = pick_children(parent1, parent2)
        # escolhe a melhor dos dois filhosd = pick_childrens(parent1, parent2)
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
    return bigger_fitness(population[random.randint(0, n-1):n])
    
# VERIFICAR ISSO AQUI
def roulette_wheel(probabilities):
    total = sum(probabilities)
    pick = random.uniform(0, total)
    current = 0

    for i in range(len(probabilities)):
        current += probabilities[i]
        if current > pick:
            return i

# certo, faz chross over com os parntes e retorna 2 filhos
def pick_children(parent1, parent2):

    child1, child2 = crossover(parent1, parent2)
    child1 = mutate(child1)
    child2 = mutate(child2)

    # escolhe a melhor dos dois filhos
    child = bigger_fitness([child1, child2])

    return child

# certo, pega os pais em uma posição aleatoria de 0 a n, divide e junta com o outro pai
def crossover(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n], y[0:c] + x[c:n]

# certo, pega um chromossomo em posição aleatoria e define um valor aleatorio para ele 
def mutate(chromosome):
    mutation_probability = 0.05

    if (mutation_probability > random.random()):
        n = len(chromosome)
        position = random.randrange(0, n)
        chromosome[position] = random.randrange(1, n + 1)

    return chromosome

# certo, funcao para mostrar o chromossomo e o fitness desse
def show_children(child):
    print('chromosome = {}, fitness = {}'
        .format(str(child), fitness(child)))

# encontrando o best queen da populacao, maior fitness
def bigger_fitness(population):
    best_fitness = 0

    for chrom in population:
        if fitness(chrom) > best_fitness:
            best_fitness = fitness(chrom)
            c = chrom
    
    return c
    
# imprimir o board
def print_board(board_queens, n):
    board = []
    for _ in range(n):
        board.append(["x"] * n)
    for i in range(n):
        board[board_queens[i]-1][i]="Q"
    for row in board:
        print (" ".join(row))

# gerar genotipo aleatorio para primeira popoulação
def genotype_queens(n):
    return [ random.randint(1, n) for _ in range(n)]

# main, que trata do imput e chama as funcoes
n_queens = int(input("number of queens: "))
max_collisions = (n_queens*(n_queens-1))/2
print('max fitness:', max_collisions)

n_population = 2*(n_queens**2)
print('n_population:', n_population)

population = [genotype_queens(n_queens) for _ in range(n_population)]

best_pouplation = find_best_fitness(max_collisions, population)
bigger_fitness = bigger_fitness(best_pouplation)

print('-----------------------------------')
print('n queen problem - genetic algorithm')
print('n_queens:', n_queens)
print('n_population:', n_population)
print('max fitness:', max_collisions)
print('-----------------------------------')
if fitness(bigger_fitness) == max_collisions:
    print('found a solution by fitness')
else:
    print('no solution, stopped by generation limit')
print('found fitness:', fitness(bigger_fitness))
print('best_queen:',bigger_fitness)
print_board(bigger_fitness, n_queens)
print('-----------------------------------')