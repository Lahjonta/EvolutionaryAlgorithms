from manim import *
import random

class EvolutionaryAlgorithm:
    def __init__(self, target, valid_genes, population_size=100, mutation_rate=0.01):
        self.target = target
        self.valid_genes = ''.join([text.text for text in valid_genes])  # Extract valid genes from Manim Text objects
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()
    
    def initialize_population(self):
        return [''.join(random.choice(self.valid_genes) for _ in range(len(self.target))) for _ in range(self.population_size)]
    
    def fitness(self, individual):
        return sum(individual[i] != self.target[i] for i in range(len(self.target)))
    
    def select_parent(self):
        weights = [1 / (self.fitness(individual) + 1) for individual in self.population]
        return random.choices(self.population, weights=weights, k=2)
    
    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(self.target))
        return parent1[:crossover_point] + parent2[crossover_point:]
    
    def mutate(self, individual):
        mutated = list(individual)
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = random.choice(self.valid_genes)
        return ''.join(mutated)
    
    def evolve(self):
        new_generation = []
        for _ in range(self.population_size):
            parent1, parent2 = self.select_parent()
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_generation.append(child)
        self.population = new_generation

class Example1(Scene):
    def construct(self):
        
        # set the default font
        Text.set_default(font="Monospace")

        # Set the header, target & valid genes
        header = Text("String Optimierung", font_size=48)
        target = "Integrationsseminar"

        # First string with its rectangle, centered horizontally
        first_string_text = Text("sjdzsknvz86hsnmpelr", font_size=26)
        first_string_box = SurroundingRectangle(first_string_text, color=RED, buff=0.5).set_fill(RED, opacity=0.2)
        # Use ORIGIN to center the first string, then move it slightly to the left to make room
        first_string_group = VGroup(first_string_text, first_string_box).move_to(ORIGIN + LEFT * 3.3)
        
        # Second string with its rectangle
        second_string_text = Text("Integrationsseminar", font_size=26)
        second_string_box = SurroundingRectangle(second_string_text, color=BLUE, buff=0.5).set_fill(BLUE, opacity=0.2)
        # Place the second string to the right of the first string
        second_string_group = VGroup(second_string_text, second_string_box).next_to(first_string_box, RIGHT, buff=2)

        # Create and display the new question text
        question_text = Text("Wie erreichen wir unser gewünschtes Ziel?", font_size=36).move_to(ORIGIN)
        
        valid_genes = VGroup(
            Text("abcdefghijklmnopqrstuvwxyz", font_size=36),
            Text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", font_size=36),
            Text('1234567890, .-;:_!"#%&/()=?@${[]}', font_size=36)
        ).arrange(DOWN, center=True)
        # Create a brace for describing the valid genes
        brace_genes = Brace(mobject=valid_genes[2], direction=DOWN, buff=0.2)
        brace_genes_text = brace_genes.get_text("Valide Gene")

        # Create Text objects for "Selection", "Mutation", and "Cross-over"
        selection_text = Text("Selektion", font_size=28)
        mutation_text = Text("Mutation", font_size=28)
        crossover_text = Text("Crossover", font_size=28)

        # Position these texts on the screen
        selection_text.move_to(LEFT * 3.5)
        mutation_text.move_to(ORIGIN)
        crossover_text.move_to(RIGHT * 3.5)

        # Surround each text with a yellow rectangle with low opacity
        selection_box = SurroundingRectangle(selection_text, color=YELLOW, buff=0.5).set_fill(YELLOW, opacity=0.2)
        mutation_box = SurroundingRectangle(mutation_text, color=YELLOW, buff=0.5).set_fill(YELLOW, opacity=0.2)
        crossover_box = SurroundingRectangle(crossover_text, color=YELLOW, buff=0.5).set_fill(YELLOW, opacity=0.2)

        # Group texts and boxes for animation
        selection_group = VGroup(selection_text, selection_box)
        mutation_group = VGroup(mutation_text, mutation_box)
        crossover_group = VGroup(crossover_text, crossover_box)

        # Target elements
        target_text = Text("Integrationsseminar", font_size=36).shift(LEFT * 2)
        target_box = SurroundingRectangle(target_text, color=BLUE, buff=0.5).set_fill(BLUE, opacity=0.2)

        # Initial generation count and best fitness value
        generation_count = 0
        best_fitness_value = float('inf')  # Start with the highest possible fitness value
        best_individual = None

        # Initialize display texts and add them to the scene
        best_string_text_display = Text("", font_size=36).move_to(ORIGIN).shift(LEFT * 2)

        # Combine generation and fitness texts into one, within a red rectangle
        combined_text = Text(f"Generation: {generation_count} - Fitness: 19", font_size=24).move_to(2 * LEFT)
        combined_text_box = SurroundingRectangle(combined_text, color=RED, buff=0.5).set_fill(RED, opacity=0.2)
        combined_text_group = VGroup(combined_text, combined_text_box).move_to(2 * LEFT)

        # Initialize the evolutionary algorithm
        ea = EvolutionaryAlgorithm(target, valid_genes)

        # Animate scene
        self.add(header)
        # Set the target properties for the header
        header.target = header.copy()
        header.target.scale(0.50)  # Scale down the header
        header.target.to_edge(UL)  # Move to upper left
        # Animate the header transformation
        self.play(ScaleInPlace(header, 0.50), MoveToTarget(header))
        self.wait(1)

        # Display the first and second strings with rectangles
        self.play(Create(first_string_group))
        # Animate an arrow pointing from the first rectangle to the second
        arrow = Arrow(first_string_box.get_right(), second_string_box.get_left(), buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow))
        self.play(Create(second_string_group))
        self.wait(5)
        # Fade out the two boxes and the arrow
        self.play(FadeOut(first_string_group), FadeOut(second_string_group), FadeOut(arrow))

        # Make Question appear
        self.play(Write(question_text))
        self.wait(2)
        self.play(FadeOut(question_text))

        # Show valid genes
        valid_genes.move_to(ORIGIN)
        self.play(Create(valid_genes))
        self.play(GrowFromCenter(brace_genes), FadeIn(brace_genes_text), run_time=2)
        self.wait(5)
        # Fade out the valid_genes and brace_genes with brace_genes_text
        self.play(FadeOut(valid_genes), FadeOut(brace_genes), FadeOut(brace_genes_text))
        self.wait(1)

        # Display the texts with rectangles
        self.play(Create(selection_group))
        self.play(Create(mutation_group))
        self.play(Create(crossover_group))
        self.wait(4)

        # Zoom in and out animation for 'Selection'
        self.play(ScaleInPlace(selection_group, 1.2), run_time=0.5)
        self.play(ScaleInPlace(selection_group, 1/1.2), run_time=0.5)
        self.wait(0.5)

        # Zoom in and out animation for 'Mutation'
        self.play(ScaleInPlace(mutation_group, 1.2), run_time=0.5)
        self.play(ScaleInPlace(mutation_group, 1/1.2), run_time=0.5)
        self.wait(0.5)

        # Zoom in and out animation for 'Cross-over'
        self.play(ScaleInPlace(crossover_group, 1.2), run_time=0.5)
        self.play(ScaleInPlace(crossover_group, 1/1.2), run_time=0.5)
        self.wait(0.5)

        # Calculate new positions on the right side of the screen, arranged vertically
        new_positions = [UP * 2, 0, DOWN * 2]

        # Animate movement to the new positions
        self.play(
            selection_group.animate.move_to(RIGHT * 4.5 + new_positions[0]),
            mutation_group.animate.move_to(RIGHT * 4.5 + new_positions[1]),
            crossover_group.animate.move_to(RIGHT * 4.5 + new_positions[2]),
            run_time=2
        )
        self.wait(2)

        # Position target_text and target_box, then shift both UP * 2
        self.play(Create(target_text), Create(target_box))
        # Use .animate syntax to move both at the same time
        self.play(target_text.animate.shift(UP * 2), target_box.animate.shift(UP * 2))
        self.wait(4)

        # Display the combined text and rectangle
        self.play(Create(combined_text_group))
        # Move the combined text
        self.play(combined_text_group.animate.shift(DOWN * 2))

        self.play(Create(best_string_text_display))
        self.wait(8)



        # Limit the number of generations for demonstration
        for _ in range(1750):  # Use a for loop or another breaking condition to avoid infinite loops
            ea.evolve()

            # Find the best individual in the current generation
            current_best_individual = min(ea.population, key=ea.fitness)
            current_best_fitness_value = ea.fitness(current_best_individual)

            if current_best_fitness_value < best_fitness_value:
                best_fitness_value = current_best_fitness_value
                best_individual = current_best_individual
            
            generation_count += 1

            # Break the loop if the best fitness value reaches 0
            if best_fitness_value == 0:
                
                # Update the combined text display
                new_combined_text_content = f"Generation: {generation_count} - Fitness: {best_fitness_value}"
                new_combined_text = Text(new_combined_text_content, font_size=24).move_to(LEFT * 2 + DOWN * 2)
                new_combined_text_box = SurroundingRectangle(new_combined_text, color=RED, buff=0.5).set_fill(RED, opacity=0.2)
                new_combined_text_group = VGroup(new_combined_text, new_combined_text_box).move_to(LEFT * 2 + DOWN * 2)
                new_best_string_text = Text(f"{best_individual}", font_size=36).shift(LEFT * 2)

                # Animate updates to the combined text display
                self.play(Transform(combined_text_group, new_combined_text_group),
                          Transform(best_string_text_display, new_best_string_text),
                           run_time=1)
                self.wait(1)
                break  # Exit the loop

            if generation_count % 50 == 0:  # Check if it's time to update the display
                # Update the combined text display
                new_combined_text_content = f"Generation: {generation_count} - Fitness: {best_fitness_value}"
                new_combined_text = Text(new_combined_text_content, font_size=24).move_to(LEFT * 2 + DOWN * 2)
                new_combined_text_box = SurroundingRectangle(new_combined_text, color=RED, buff=0.5).set_fill(RED, opacity=0.2)
                new_combined_text_group = VGroup(new_combined_text, new_combined_text_box).move_to(LEFT * 2 + DOWN * 2)
                new_best_string_text = Text(f"{best_individual}", font_size=36).shift(LEFT * 2)

                # Animate updates to the combined text display
                self.play(Transform(combined_text_group, new_combined_text_group),
                          Transform(best_string_text_display, new_best_string_text),
                           run_time=1)
                self.wait(1)


if __name__ == "__main__":
    scene = Example1()
    scene.render()