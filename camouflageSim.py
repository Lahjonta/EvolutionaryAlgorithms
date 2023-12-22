import numpy as np
import pygame
import sys

# Constants
POPULATION_SIZE = 100
GRID_SIZE = 10  # Number of organisms in each row and column
GENOME_LENGTH = 3  # RGB channels only
MUTATION_RATE = 0.01
GENERATIONS = 100
BACKGROUND_COLOR = (0, 0, 0)  # RGB for black
RECTANGLE_SIZE = 30  # Size of each organism rectangle
GRID_SPACING = 2  # Spacing between grid cells

# Pygame initialization
pygame.init()
screen_size = (400, 400)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Genetic Algorithm Color Evolution")

# Function to generate an initial population with more randomness
def generate_population(size):
    return np.random.randint(0, 255, size=(size, GENOME_LENGTH))

# Function to calculate fitness
def fitness(individual_color):
    return 255 - np.abs(individual_color - BACKGROUND_COLOR).mean()

# Function for mutation
def mutate(individual):
    mutation_mask = np.random.rand(GENOME_LENGTH) < MUTATION_RATE
    individual[mutation_mask] = np.random.randint(0, 255, mutation_mask.sum())
    return individual

# Main genetic algorithm loop
population = generate_population(POPULATION_SIZE)
fitness_history = []

for generation in range(GENERATIONS):
    # Handle events, such as closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Evaluate fitness
    scores = np.array([fitness(ind) for ind in population])
    fitness_history.append(scores.max())

    # Selection: Keep the top 50% of the population
    selected_indices = np.argsort(scores)[-POPULATION_SIZE // 2:]
    population = population[selected_indices]

    # Reproduction: Mutation
    mutated_population = np.array([mutate(ind) for ind in population])

    # Create the next generation by combining the original and mutated populations
    population = np.vstack((population, mutated_population))

    # Visualize the population in a grid
    screen.fill((0, 0, 0))  # Clear the screen

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            if index < len(population):
                color_tuple = tuple(population[index].astype(int))
                rect = pygame.Rect(j * (RECTANGLE_SIZE + GRID_SPACING),
                                   i * (RECTANGLE_SIZE + GRID_SPACING),
                                   RECTANGLE_SIZE, RECTANGLE_SIZE)
                pygame.draw.rect(screen, color_tuple, rect)

    pygame.display.flip()
    pygame.time.delay(50)  # Delay in milliseconds (adjust as needed)

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
