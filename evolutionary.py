from manim import *
import os
import numpy as np
import random
import cv2


# Generate example genes with different bases
def generateGene(labels, col):
    gene = VGroup()

    for label in labels:
        rect = Rectangle(width=1, height=1)
        text_label = Text(label)
        text_label.move_to(rect.get_center())

        # Group each rectangle ("gene") and label
        rect_and_label = VGroup(rect, text_label)
        gene.add(rect_and_label)

    # Positioning rectangles and labels
    for i, rect_and_label in enumerate(gene):
        rect_and_label.next_to(ORIGIN, UP, buff=i)
        rect_and_label.shift(2 * DOWN, 2 * LEFT)

    # Decide color of gene
    for rect in gene:
        rect[0].set_fill(color=col, opacity=0.8)

    return gene

# Create cat population to show evolution
def createCat(color, eye_color, position):
    head = Arc(radius=0.9, angle=TAU, fill_opacity=1, color=color)
    left_ear = Triangle(fill_opacity=1, color=color).scale(0.5).rotate(PI / 4).shift(0.45 * UP + 0.7 * LEFT)
    right_ear = Triangle(fill_opacity=1, color=color).scale(0.5).rotate(-PI / 4).shift(0.45 * UP + 0.7 * RIGHT)
    ears = VGroup(left_ear, right_ear)
    left_eye = Dot(radius=0.12, color=eye_color).shift(0.2 * UP + 0.3 * LEFT)
    right_eye = Dot(radius=0.12, color=eye_color).shift(0.2 * UP + 0.3 * RIGHT)
    eyes = VGroup(left_eye, right_eye)
    nose = Triangle(fill_opacity=1, color=PINK).scale(0.15).next_to(head, ORIGIN).rotate(60 * DEGREES).shift(
        0.15 * DOWN)
    mouth_left = ArcBetweenPoints(0.3 * LEFT, ORIGIN, color=PINK).next_to(nose, DOWN).shift(0.22 * UP + 0.15 * LEFT)
    mouth_right = ArcBetweenPoints(0.3 * RIGHT, ORIGIN, color=PINK, angle=-TAU / 4).next_to(nose, DOWN).shift(
        0.22 * UP + 0.15 * RIGHT)
    mouth = VGroup(mouth_left, mouth_right)
    cat = VGroup(head, ears, eyes, nose, mouth).to_edge(position)

    return cat

# Create heart shapes with function
def heart():
    x = 1
    y = 1
    el1 = CubicBezier([x, y, 0], [x, y - .3, 0], [x - .5, y - .3, 0], [x - 0.5, y, 0])
    el2 = CubicBezier([x - .5, y, 0], [x - .5, y + .3, 0], [x, y + 0.35, 0], [x, y + 0.6, 0])
    el3 = CubicBezier([x, y + .6, 0], [x, y + .35, 0], [x + .5, y + .3, 0], [x + .5, y, 0])
    el4 = CubicBezier([x + .5, y, 0], [x + .5, y - .3, 0], [x, y - .3, 0], [x, y, 0])
    heart = VGroup(el1, el2, el3, el4).set_color(RED).rotate(180 * DEGREES)

    return heart

# Generate a random RGB color for start population
def get_random_color():
    return np.random.rand(3)

# Calculate the fitness -> Fitness is the inverse of the mean absolute difference between the color and BACKGROUND_COLOR.
def fitness(individual_color):
    # RGB values are normalized in manim therefore 1 not 255 #mean to average across all three channels
    return 1 - np.abs(individual_color - BACKGROUND_COLOR).mean()

# Mutate a color by randomly altering its RGB values based on MUTATION_RATE.
def mutate(individual_color):
    mutation_mask = np.random.rand(GENOME_LENGTH) < MUTATION_RATE
    individual_color[mutation_mask] = np.random.rand(mutation_mask.sum())
    return individual_color

# Crossover between two colors where the values of 1 RGB component are switched
def crossover(parent1, parent2):
    # Each parent consists of a numpy array representing RGB values
    component = random.randint(0, 2)  # Choose one of R, G, B -> very simplified crossover
    parent1[component], parent2[component] = parent2[component], parent1[component]
    return parent1, parent2

# Functions to convert ManimColor Codes and RGB Color Codes
def manim_color_to_array(manim_color):
    # Extract the RGB components from the Manim Color object
    rgb = manim_color.to_rgb()
    # Convert to a NumPy array
    return np.array(rgb)

def array_to_manim_color(array):
    return ManimColor(tuple(array))

BACKGROUND_COLOR = np.array([0, 0, 0])  # Target color for the genetic algorithm
GENERATIONS = 30  # Number of generations to simulate
GENOME_LENGTH = 3  # Number of genes (RGB channels) in each individual
MUTATION_RATE = 0.05  # Probability of a gene mutating


########################################################################################################################
# Manim Video Code
class Evolution(MovingCameraScene):
    def construct(self):
        # Set Font
        Text.set_default(font="Monospace")

        # Create front page
        text_1 = Text('Darwins Erbe:', color=WHITE)
        text_2 = Text('Evolutionäre Algorithmen', color=WHITE)
        text = VGroup(text_1, text_2).arrange(DOWN, aligned_edge=LEFT)
        text.move_to(ORIGIN)
        self.add(text)
        box = SurroundingRectangle(text_2, corner_radius=0.2, color=RED)
        text_2.shift(0.1 * DOWN)
        self.play(Create(box))
        self.wait(2)
        self.play(box.animate.shift(3 * UP), text.animate.shift(3 * UP))

        # Add image of Darwin
        darwin = ImageMobject("darwin.png").to_edge(DL)
        self.play(FadeIn(darwin))
        self.wait(4)

        # Transition to the next scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        # Workaround to play a video in manim
        cap = cv2.VideoCapture(r"C:\Users\Janika\Documents\GitHub\EvolutionaryAlgorithms\EvoHuman.mp4")
        flag = True
        while flag:
            flag, frame = cap.read()
            if flag:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_img = ImageMobject(frame)
                self.add(frame_img)
                self.wait(0.08)
                self.remove(frame_img)
        cap.release()

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.genes()

    def genes(self):
        # New title slide
        title = Text("Biologie")
        title.center()
        self.play(GrowFromCenter(title))
        self.wait(2)
        self.play(FadeOut(title))
        gene = generateGene(["A", "C", "G", "T", "A"], BLACK)

        # Add rectangles and labels to the scene
        self.play(FadeIn(gene))

        # Wait for 2 seconds
        self.wait(2)

        # Add a surrounding rectangle
        box = SurroundingRectangle(gene, color=YELLOW)
        self.play(FadeIn(box))

        # Add an arrow and text
        arrow = Arrow(start=gene[2].get_left() + LEFT * 2, end=gene[2].get_left(), color=WHITE)
        text_gen = Text("Gen", color=WHITE).next_to(arrow, LEFT, buff=0.1)
        self.play(FadeIn(arrow, text_gen))

        genotype = Text("Genotyp").next_to(gene[0], 5 * DOWN, buff=0.2)
        self.play(FadeIn(genotype))
        self.wait(3)
        # Create phenotype to genes
        cat = createCat(WHITE, BLACK, RIGHT).shift(0.5 * UP + 2*LEFT)
        phenotype = Text("Phänotyp").next_to(genotype, 12 * RIGHT)
        # Add the components to the mobject
        self.play(FadeIn(cat))
        self.wait(2)
        self.play(FadeIn(phenotype))
        # Make cat blink
        self.wait(1)
        self.play(cat[2].animate.set_opacity(0))
        self.wait(0.1)
        self.play(cat[2].animate.set_opacity(1))
        self.wait(2)
        self.play(cat[2].animate.set_opacity(0))
        self.wait(0.1)
        self.play(cat[2].animate.set_opacity(1))

        # Transition to new scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.evolve()

    def evolve(self):
        title = Text("Evolution?")
        title.move_to(ORIGIN)
        self.play(GrowFromEdge(title, DOWN))
        self.wait(2)
        self.play(title.animate.shift(3 * UP))
        self.wait(2)

        first = Text("1. Genetische Variation").scale(0.5).to_edge(LEFT).shift(2 * UP)
        second = Text("2. Beschränktes Überleben").scale(0.5).next_to(first, DOWN, buff=0.5, aligned_edge=LEFT)
        third = Text("3. Vererbung").scale(0.5).next_to(second, DOWN, buff=0.5, aligned_edge=LEFT)

        # Create cat population
        self.play(FadeIn(first))
        cat_white = createCat(WHITE, BLACK, DL)
        cat_brown = createCat(LIGHT_BROWN, BLUE_E, DL).next_to(cat_white)
        cat_grey = createCat(DARK_GREY, YELLOW_D, DL).next_to(cat_brown)
        cat_dark = createCat(DARKER_GREY, YELLOW_D, DL).next_to(cat_grey)
        self.play(FadeIn(cat_white, cat_brown, cat_grey, cat_dark))
        self.wait(12)

        # Survival of the fittest
        self.play(FadeIn(second))
        # Not adapted cats won't survive
        self.play(cat_brown[4].animate.rotate(PI), cat_white[4].animate.rotate(PI))
        self.wait(2)

        # Move and disappear the white cat
        self.play(cat_white.animate.to_edge(RIGHT).shift(3 * UP))
        self.play(FadeOut(cat_white))
        self.wait(3)

        # Move and disappear the brown cat
        self.play(cat_brown.animate.to_edge(RIGHT).shift(3 * UP))
        self.play(FadeOut(cat_brown))
        self.wait(3)

        self.wait(3)

        # Survivers reproduce
        self.play(FadeIn(third))
        cat_dark_1 = createCat(GRAY, YELLOW_A, DL)
        cat_dark_2 = createCat(GRAY_BROWN, GOLD_E, DL).next_to(cat_dark_1)
        cat_dark_3 = createCat(BLACK, YELLOW_E, DL).next_to(cat_dark)
        cat_dark_4 = createCat(DARKER_GRAY, YELLOW_C, DL).next_to(cat_dark_3)

        h1 = heart().next_to(cat_grey, UR)
        h1.shift(0.6 * LEFT)
        self.play(FadeIn(h1))
        self.play(FadeIn(cat_dark_1, cat_dark_2))
        self.play(FadeOut(h1))
        self.wait(2)

        h2 = heart().next_to(cat_dark_1, UR).shift(0.6 * LEFT)
        self.play(FadeIn(h2))
        self.play(FadeIn(cat_dark_3, cat_dark_4))
        self.play(FadeOut(h2))
        self.wait(13)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.terminology()

    def terminology(self):
        self.wait(1)
        mutation = Text("Mutation", color=PURE_RED)
        mutation.shift(4 * RIGHT + 0.5 * UP)
        self.play(FadeIn(mutation))
        self.wait(1)

        # Show inital genes
        gene1 = generateGene(["A", "C", "G", "T", "A"], BLUE_E).shift(LEFT)
        gene2 = generateGene(["C", "G", "G", "T", "T"], MAROON_E).next_to(gene1).shift(2 * RIGHT)
        self.play(FadeIn(gene1, gene2))
        self.wait(3)

        # Mutation animation
        mutatedGene1 = generateGene(["A", "C", "G", "T", "C"], BLUE_E).shift(LEFT)
        mutatedGene2 = generateGene(["C", "A", "G", "T", "T"], MAROON_E).next_to(gene1).shift(2 * RIGHT)

        mutatedGene2[1][1].set_color(PURE_RED)
        mutatedGene1[4][1].set_color(PURE_RED)
        self.play(ReplacementTransform(gene2, mutatedGene2, run_time=4))
        self.wait(2)
        self.play(ReplacementTransform(gene1, mutatedGene1, run_time=4))
        self.wait(8)

        # Crossover
        cross = Text("Crossover", color=PURE_RED)
        cross.shift(4 * RIGHT + 0.5 * UP)

        self.play(ReplacementTransform(mutation, cross, run_time=3))
        self.wait(5)

        # Corresponding parts of genes break off and swap places
        gene1Part = VGroup(mutatedGene1[0], mutatedGene1[1])
        gene2Part = VGroup(mutatedGene2[0], mutatedGene2[1])
        self.play(
            gene1Part.animate.move_to(gene2.get_center()).shift(1.5 * DOWN),
            gene2Part.animate.move_to(gene1.get_center()).shift(1.5 * DOWN),
            run_time=5
        )

        self.wait(15)

        binaryGene1 = generateGene(["0", "1", "0", "1", "0"], BLUE_E).shift(LEFT)
        binaryGene2 = generateGene(["1", "0", "1", "1", "1"], MAROON_E).next_to(binaryGene1)
        binaryGene3 = generateGene(["1", "1", "0", "0", "0"], GREEN_E).next_to(binaryGene2)
        binaryGene4 = generateGene(["0", "0", "1", "0", "1"], GOLD_A).next_to(binaryGene3)
        pop = Text("Population").next_to(binaryGene4.get_center(), RIGHT)
        pop.shift(RIGHT)

        self.play(
            FadeOut(cross),
            ReplacementTransform(mutatedGene1, binaryGene1),
            ReplacementTransform(mutatedGene2, binaryGene2),
            FadeIn(pop, binaryGene3, binaryGene4),
            run_time=2
        )

        self.wait(25)

        # Move to evaluation 1
        evaluation = Text("Evaluation").next_to(binaryGene2, UR)
        evaluation.shift(5 * UP + 5 * RIGHT)
        arrow = Arrow(binaryGene4.get_top(), evaluation, buff=1)
        self.play(
            self.camera.frame.animate.move_to(evaluation),
            FadeIn(arrow),
            FadeIn(evaluation),
            run_time=4
        )

        # Move to selection 1
        selection = Text("Selektion").next_to(evaluation, RIGHT)
        selection.shift(1.7 * DOWN + 3 * RIGHT)
        binary1 = binaryGene1.copy().next_to(selection, UP)
        binary1.shift(0.3 * DOWN + 0.3 * LEFT)
        binary3 = binaryGene3.copy().next_to(binary1, RIGHT)
        arrow2 = Arrow(evaluation.get_right(), evaluation.get_right() + 4 * RIGHT, buff=1)
        selection.shift(0.5 * DOWN + 0.3 * RIGHT)

        self.play(
            self.camera.frame.animate.move_to(binary1[1].get_center()),
            FadeIn(arrow2),
            FadeIn(selection),
            FadeIn(binary1, binary3),
            run_time=4
        )

        # Move to mutation/crossover 1
        binary1copy = binaryGene1.copy().next_to(binary3, 20 * RIGHT)
        binary1copy.shift(0.5 * LEFT)
        binary3copy = binaryGene3.copy().next_to(binary1copy, RIGHT)
        mutCross = Text("Mutation/Crossover").next_to(binary1copy, DOWN)
        arrow3 = Arrow(binary3[1].get_right(), binary1copy[1].get_left(), buff=1)
        mutCross.shift(0.22 * DOWN + 0.3 * RIGHT)

        self.play(
            self.camera.frame.animate.move_to(binary1copy[1].get_center()),
            FadeIn(arrow3),
            FadeIn(mutCross),
            FadeIn(binary1copy, binary3copy),
            run_time=4
        )

        ## Mutation
        binary1mut = generateGene(["0", "1", "1", "1", "0"], BLUE_E).next_to(binary3, 20 * RIGHT)
        binary1mut.shift(0.5 * LEFT)
        binary3mut = generateGene(["1", "1", "0", "0", "1"], GREEN_E).next_to(binary1mut, RIGHT)
        binary1mut[2][1].set_color(PURE_RED)
        binary3mut[4][1].set_color(PURE_RED)
        self.play(
            ReplacementTransform(binary1copy, binary1mut, run_time=2),
            ReplacementTransform(binary3copy, binary3mut, run_time=2),
            run_time=0.5
        )

        ## Crossover
        binary1mutPart = VGroup(binary1mut[3], binary1mut[4])
        binary3mutPart = VGroup(binary3mut[1], binary3mut[2])
        self.play(
            binary1mutPart.animate.move_to(binary3mut.get_center()).shift(0.5 * DOWN),
            binary3mutPart.animate.move_to(binary1mut.get_center()).shift(1.5 * UP),
            run_time=0.5
        )

        self.wait(2)

        self.next_section(skip_animations=True)  # skip animations or the video will be too long
        # Move to evaluation 2
        evaluation2 = Text("Evaluation").next_to(binaryGene2, DR)
        evaluation2.shift(5 * DOWN + 5 * RIGHT)
        arrow4 = Arrow(binaryGene4.get_bottom(), evaluation2, buff=1)
        self.play(
            self.camera.frame.animate.move_to(evaluation2),
            FadeIn(arrow4),
            FadeIn(evaluation2),
            run_time=4
        )

        self.wait(3)

        # Move to selection 2
        selection2 = Text("Selektion").next_to(evaluation2, RIGHT)
        selection2.shift(2 * DOWN + 3 * RIGHT)
        binary1x = binaryGene1.copy().next_to(selection2, UP)
        binary1x.shift(0.5 * LEFT)
        binary4 = binaryGene4.copy().next_to(binary1x, RIGHT)
        arrow5 = Arrow(evaluation2.get_right(), evaluation2.get_right() + 4 * RIGHT, buff=1)
        selection2.shift(0.2 * DOWN + 0.3 * RIGHT)

        self.play(
            self.camera.frame.animate.move_to(binary1x[1].get_center()),
            FadeIn(arrow5),
            FadeIn(selection2),
            FadeIn(binary1x, binary4),
            run_time=4
        )

        self.wait(3)

        # Move to mutation/crossover 2
        binary1copyx = binaryGene1.copy().next_to(binary4, 20 * RIGHT)
        binary4copy = binaryGene4.copy().next_to(binary1copyx, RIGHT)
        mutCross2 = Text("Mutation/Crossover").next_to(binary1copyx, DOWN)
        arrow6 = Arrow(binary4[1].get_right(), binary1copyx[1].get_left(), buff=1)
        mutCross2.shift(0.21 * DOWN + 0.3 * RIGHT)

        self.play(
            self.camera.frame.animate.move_to(binary1copyx[1].get_center()),
            FadeIn(arrow6),
            FadeIn(mutCross2),
            FadeIn(binary1copyx, binary4copy),
            run_time=4
        )

        ## Mutation
        binary1mutx = generateGene(["0", "0", "0", "1", "0"], BLUE_E).next_to(binary4, 20 * RIGHT)
        binary4mut = generateGene(["1", "0", "1", "0", "1"], GOLD_A).next_to(binary1mutx, RIGHT)
        binary1mutx[1][1].set_color(PURE_RED)
        binary4mut[0][1].set_color(PURE_RED)
        self.play(
            ReplacementTransform(binary1copyx, binary1mutx, run_time=2),
            ReplacementTransform(binary4copy, binary4mut, run_time=2)
        )

        ## Crossover
        binary1mutPartx = VGroup(binary1mutx[0], binary1mutx[1])
        binary4mutPart = VGroup(binary4mut[0], binary4mut[1])
        self.play(
            binary1mutPartx.animate.move_to(binary4mut.get_center()).shift(1.5 * DOWN),
            binary4mutPart.animate.move_to(binary1mutx.get_center()).shift(1.5 * DOWN),
            run_time=1
        )

        self.wait(3)

        self.next_section()

        # New population
        newPop = Text("Neue Population").next_to(pop, 80 * RIGHT)
        arrow7 = Arrow(mutCross.get_right(), newPop.get_left(), buff=2)
        arrow8 = Arrow(binary4copy[4].get_right(), newPop.get_left(), buff=2)
        arrow9 = Arrow(newPop.get_left(), pop.get_right(), buff=1)

        self.play(
            self.camera.frame.animate.move_to(pop.get_right() * 2.5).scale(3)
        )

        self.wait(2)

        self.play(
            FadeIn(newPop, arrow7, arrow8, arrow9))

        self.wait(15)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.fitnessFunction()

    def fitnessFunction(self):
        # Reset camera
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set_height(config.frame_height)
        )

        # Define fitness function and representative cats
        fitness_function = Text("Fitness Funktion")
        fitness_function.move_to(ORIGIN)
        self.play(FadeIn(fitness_function))
        self.wait(2)
        self.play(fitness_function.animate.shift(3 * UP))

        cat_good = createCat(DARKER_GREY, YELLOW_E, ORIGIN).shift(2 * LEFT)
        cat_medium = createCat(GREY, YELLOW_D, ORIGIN).next_to(cat_good)
        cat_bad = createCat(WHITE, YELLOW_C, ORIGIN).next_to(cat_medium)

        self.play(FadeIn(cat_good, cat_medium, cat_bad))
        self.wait(5)

        good = Text("Gut", font_size=24).next_to(cat_good, 2 * DOWN)
        medium = Text("Medium", font_size=24).next_to(cat_medium, 2 * DOWN)
        bad = Text("Schlecht", font_size=24).next_to(cat_bad, 2 * DOWN)

        self.play(FadeIn(good, medium, bad))
        self.wait(6)

        self.play(FadeOut(good, medium, bad, cat_good, cat_medium, cat_bad))

        # Explain fitness  function and show change for color
        fitness = Text("Fitness = 255 - |Hintergrundfarbe - Individuenfarbe|", font_size=28).next_to(fitness_function,
                                                                                                     5 * DOWN)
        self.play(FadeIn(fitness))

        self.wait(15)

        black_cat = createCat(BLACK, YELLOW_E, ORIGIN).shift(DOWN)
        fit_score = Text("Fitness = 255 - |0 - 0|", font_size=24).next_to(black_cat,
                                                                          2 * DOWN)  # for every one of the RGB channels

        self.play(FadeIn(black_cat, fit_score))
        self.wait(5)

        fit_score_2 = Text(f"Fitness = {255 - abs(0 - 0)}", font_size=24).next_to(black_cat,
                                                                                  2 * DOWN)  # backgroundcolor = individual color -> very good

        self.play(Transform(fit_score, fit_score_2), run_time=3)

        self.wait(5)

        # Loop to gradually lighten the cat and update fitness score
        for i in range(0, 256, 10):
            new_color = interpolate_color(BLACK, WHITE, i / 255)
            new_cat = createCat(new_color, YELLOW_E, ORIGIN).shift(DOWN)
            # Calculate and create a new fitness score text
            new_fit_score = Text(f"Fitness = {255 - abs(i - 0)}", font_size=24).next_to(black_cat, 2 * DOWN)
            # Change cats color and transform the old fitness score to the new one
            self.play(Transform(black_cat, new_cat), Transform(fit_score, new_fit_score), run_time=0.1)
            self.wait(0.1)

        self.wait(5)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.camouflageSim()

    def camouflageSim(self):
        size = 12
        example1 = Text("Zeit für die Simulation!")
        example1.move_to(ORIGIN)
        self.play(FadeIn(example1))
        self.wait(2)
        self.play(example1.animate.shift(3 * UP + 4 * LEFT).scale(0.7))

        # Initialize the generation counter
        generation_counter = Text("Generation: 0", font_size=24)
        generation_counter.next_to(example1, DOWN)
        self.play(FadeIn(generation_counter))

        # Initialize the grid with random colors (random start population)
        colors = [get_random_color() for _ in range(size ** 2)]
        squares = VGroup(*[Square(side_length=0.5, fill_opacity=1, fill_color=color, color=BLACK) for color in colors])
        squares.arrange_in_grid(rows=size, cols=size, buff=0).shift(2 * RIGHT)
        self.add(squares)
        self.wait(10)

        for gen in range(GENERATIONS):
            # Update the counter
            new_counter = Text(f"Generation: {gen + 1}", font_size=24).next_to(example1, DOWN)
            self.play(Transform(generation_counter, new_counter))
            # Calculate fitness for each square based on color similarity to BACKGROUND_COLOR, only the top 50% adapted survive
            fitness_scores = [fitness(manim_color_to_array(square.get_fill_color())) for square in squares]
            sorted_squares = sorted(zip(squares, fitness_scores), key=lambda x: x[1], reverse=True)

            # Keep the top 50% of squares based on fitness
            top_half = [item[0] for item in sorted_squares[:len(sorted_squares) // 2]]

            # Perform crossover between two randomly selected squares from the top half -> parents reproducing
            idx1, idx2 = random.sample(range(len(top_half)), 2)  # Get two random indices
            color1 = manim_color_to_array(top_half[idx1].get_fill_color())
            color2 = manim_color_to_array(top_half[idx2].get_fill_color())

            # Swap one RGB component between the two colors
            new_color1, new_color2 = crossover(color1, color2)
            top_half[idx1].set_fill(array_to_manim_color(new_color1))
            top_half[idx2].set_fill(array_to_manim_color(new_color2))

            # Set the bottom half to black -> they dead
            bottom_half = [item[0] for item in sorted_squares[len(sorted_squares) // 2:]]
            for square in bottom_half:
                square.set_fill(color=BLACK)

            if gen < 2:
                self.wait(20)  # Wait for a second

            # Mutate the top colors and apply these mutations to the bottom half
            for i, top_square in enumerate(top_half):
                # Each bottom square gets a mutated version of the corresponding top square color
                color_array = manim_color_to_array(top_square.get_fill_color())
                mutated_color_array = mutate(color_array)
                mutated_manim_color = array_to_manim_color(mutated_color_array)
                bottom_half[i].set_fill(mutated_manim_color)
            if gen < 2:
                self.wait(15)
        self.wait(10)

if __name__ == "__main__":
    os.system("manim -pqh evolutionary.py Evolution")
