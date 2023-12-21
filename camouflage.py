import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Constants
NUM_BOXES = 5
NUM_GENERATIONS = 100
POPULATION_SIZE = 50
MUTATION_RATE = 0.1
BACKGROUND_COLOR = (0, 0, 0)  # Black
PLOT_EVERY_N_GENERATIONS = 10  # Plot every 10 generations

# Helper Functions
def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def calculate_color_distance(color1, color2):
    return np.sqrt(sum((np.array(color1) - np.array(color2))**2))

# Genome Representation
class BoxColorGenome:
    def __init__(self):
        self.colors = [generate_random_color() for _ in range(NUM_BOXES)]
        self.fitness = 0

    def calculate_fitness(self):
        self.fitness = 0
        for box_color in self.colors:
            self.fitness += calculate_color_distance(box_color, BACKGROUND_COLOR)
        self.fitness = -self.fitness  # Minimize distance

# Genetic Operators
def crossover(parent1, parent2):
    child = BoxColorGenome()
    midpoint = random.randint(1, NUM_BOXES - 1)
    child.colors = parent1.colors[:midpoint] + parent2.colors[midpoint:]
    return child

def mutate(individual):
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, NUM_BOXES - 1)
        individual.colors[idx] = generate_random_color()

# Plotting Function
def plot_generation(genome, generation):
    fig, ax = plt.subplots()
    # Create a black background
    ax.set_facecolor(BACKGROUND_COLOR)
    plt.title(f'Generation {generation}')

    # Plot each box
    for i, color in enumerate(genome.colors):
        rect = patches.Rectangle((i * 1, 0), 1, 1, linewidth=1, edgecolor='none', facecolor=np.array(color)/255)
        ax.add_patch(rect)

    plt.xlim(0, NUM_BOXES)
    plt.ylim(0, 1)
    plt.xticks([])
    plt.yticks([])
    plt.show()

# Genetic Algorithm with Plotting
def genetic_algorithm():
    population = [BoxColorGenome() for _ in range(POPULATION_SIZE)]

    for generation in range(NUM_GENERATIONS):
        # Calculate fitness
        for individual in population:
            individual.calculate_fitness()

        # Sort by fitness
        population.sort(key=lambda x: x.fitness, reverse=True)

        # Plot if needed
        if generation % PLOT_EVERY_N_GENERATIONS == 0 or generation == NUM_GENERATIONS - 1:
            plot_generation(population[0], generation + 1)

        # Selection (top 50%)
        population = population[:POPULATION_SIZE // 2]

        # Crossover and mutation
        offspring = []
        while len(offspring) < POPULATION_SIZE // 2:
            parent1, parent2 = random.sample(population, 2)
            child = crossover(parent1, parent2)
            mutate(child)
            offspring.append(child)

        population += offspring

    return population[0]

# Run the algorithm
best_solution = genetic_algorithm()

