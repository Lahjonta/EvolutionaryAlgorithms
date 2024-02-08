import numpy as np 
from manim import *
import random 

  

class GeneticAlgorithm: 

    def __init__(self, maze, start, goal): 

        self.maze = maze 

        self.start = start 

        self.goal = goal 

        self.population_size = 100 

        self.gene_length = 300  # Maximum number of steps in a path 

        self.mutation_rate = 0.01 

        self.generations = 200 

        self.moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left 

        self.wall_penalty = 100  # Increased penalty for hitting a wall 

        self.out_of_bounds_penalty = 50  # Penalty for going out of bounds 

  

    def generate_individual(self): 

        return [random.randint(0, 3) for _ in range(self.gene_length)] 

  

    def compute_fitness(self, individual): 

        position = list(self.start) 

        fitness = 0 

        for move in individual: 

            next_position = [position[0] + self.moves[move][0], position[1] + self.moves[move][1]] 

            # Check if next position is out of bounds 

            if not (0 <= next_position[0] < self.maze.shape[1] and 0 <= next_position[1] < self.maze.shape[0]): 

                fitness -= self.out_of_bounds_penalty 

                continue  # Continue evaluating the path despite a penalty 

            # Check if next position is a wall 

            if self.maze[next_position[1]][next_position[0]] == 1: 

                fitness -= self.wall_penalty 

                continue  # Continue evaluating the path despite a penalty 

            position = next_position  # Update position for valid moves 

            fitness += 1  # Reward for a valid step 

            if position == list(self.goal): 

                fitness += 1000  # High reward for reaching the goal 

                break 

        return fitness 


  

    def crossover(self, parent1, parent2): 

        crossover_point = random.randint(0, self.gene_length) 

        child1 = parent1[:crossover_point] + parent2[crossover_point:] 

        child2 = parent2[:crossover_point] + parent1[crossover_point:] 

        return child1, child2 

  

    def mutate(self, individual): 

        for i in range(self.gene_length): 

            if random.random() < self.mutation_rate: 

                individual[i] = random.randint(0, 3) 

        return individual 

  

    def run(self): 

        population = [self.generate_individual() for _ in range(self.population_size)] 

        for generation in range(self.generations): 

            fitnesses = [self.compute_fitness(individual) for individual in population] 

            parents_indices = np.argsort(fitnesses)[-2:]  # Select two best individuals 

            new_population = [population[i] for i in parents_indices] 

            while len(new_population) < self.population_size: 

                parent1, parent2 = [population[i] for i in random.choices(parents_indices, k=2)] 

                child1, child2 = self.crossover(parent1, parent2) 

                new_population.extend([self.mutate(child1), self.mutate(child2)]) 

            population = new_population 

            if max(fitnesses) >= 1000: 

                print("Solution found!") 

                break 

        best_individual = population[np.argmax(fitnesses)] 

        return best_individual 

  

class MazeScene(Scene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previous_path_lines = [] # Initialize an empty list to keep track of path lines
        self.goal = (12,9)

    def construct(self): 

        self.maze = np.array([ 

            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 

            [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0], 

            [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0], 

            [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], 

            [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], 

            [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0], 

            [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 

            [0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0], 

            [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0], 

            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0] 

        ]) 

        self.rows, self.cols = self.maze.shape  # Define rows and cols here 

        ga = GeneticAlgorithm(self.maze, (0, 0), (12, 9)) 

        best_path = ga.run() 

  

        # Draw the maze 

        for i in range(self.rows): 

            for j in range(self.cols): 

                cell = Square(side_length=0.5) 

                cell.move_to(np.array([(j - self.cols / 2 + 0.5) * 0.5, (-i + self.rows / 2 - 0.5) * 0.5, 0])) 

                if self.maze[i, j] == 1:  # Use self.maze instead of maze 

                    cell.set_fill(WHITE, opacity=1) 

                self.add(cell) 
        # Draw the best path found by the GA 
        self.update_path(best_path)
        self.wait(1)
        self.update_path(best_path)

  

    def translate_path(self, best_path, start):
        path_coords = [start]
        for move in best_path:
            next_x = path_coords[-1][0] + (move == 1) - (move == 3)
            next_y = path_coords[-1][1] - (move == 0) + (move == 2)
            # Check if next move is within bounds and not through a wall
            if 0 <= next_x < self.cols and 0 <= next_y < self.rows and self.maze[next_y, next_x] == 0:
                path_coords.append((next_x, next_y))
            else:
                # If move is invalid, break or continue based on your handling of invalid moves
                continue  # or continue, depending on how you want to handle invalid paths
        # Convert coordinates to Manim's format
        return [(x * 0.5 - self.cols / 2 * 0.5 + 0.25, -y * 0.5 + self.rows / 2 * 0.5 - 0.25) for x, y in path_coords]


    def update_path(self, best_path):
        path = self.translate_path(best_path, (0,0))
        self.draw_path(path)
        if path[-1] == (self.goal[0], self.goal[1]):  # Check if the last position is the goal
            self.wait(1)  # Wait for a moment to visualize the final path
            self.clear()


    def draw_path(self, path_coords):
            
            if self.previous_path_lines: 
                for line in self.previous_path_lines:
                    self.play(FadeOut(line), run_time=0.2)
                self.previous_path_lines = []

            # Convert path coordinates to Manim VMobjects and animate them sequentially 

            for i in range(len(path_coords) - 1): 

                start_point = np.array([path_coords[i][0], path_coords[i][1], 0]) 

                end_point = np.array([path_coords[i + 1][0], path_coords[i + 1][1], 0]) 

                line = Line(start_point, end_point).set_stroke(RED, width=2) 

                self.play(Create(line), run_time=0.5)  # Adjust run_time for animation speed

                self.previous_path_lines.append(line)
    
if __name__ == "__main__":
    scene = MazeScene()
    scene.render()