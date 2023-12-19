from manim import *
import os

# Generate example genes with different bases
def generateGene(labels):
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


class Evolution(Scene):
    def construct(self):
        # Set the background color
        #self.camera.background_color = WHITE

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

        self.genes()

    def genes(self):
        # New title slide
        title = Text("Biologie")
        title.center()
        self.play(GrowFromCenter(title))
        self.wait(3)
        self.play(Uncreate(title))
        gene = generateGene(["A", "C", "G", "T", "A"])

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
        phenotype = Text("Phänotyp").next_to(genotype, 10 * RIGHT)
        cat = createCat(WHITE, BLACK, RIGHT).shift(0.5 * UP + 2*LEFT)
        phenotype = Text("Phänotyp").next_to(genotype, 10 * RIGHT)
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
        self.wait(2)

        # Transition to new scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


    def evolve(self):
        title = Text("Evolution?")
        title.move_to(ORIGIN)
        self.play(GrowFromEdge(title, DOWN))
        self.wait(1)
        self.play(title.animate.shift(3 * UP))
        self.wait(1)

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
        self.wait(5)

        # Survival of the fittest
        self.play(FadeIn(second))
        # Not adapted cats won't survive
        self.play(cat_brown[4].animate.rotate(PI), cat_white[4].animate.rotate(PI))
        self.wait(2)

        # Move and disappear the white cat
        self.play(cat_white.animate.to_edge(RIGHT).shift(3 * UP))
        self.play(FadeOut(cat_white))

        # Move and disappear the brown cat
        self.play(cat_brown.animate.to_edge(RIGHT).shift(3 * UP))
        self.play(FadeOut(cat_brown))

        # Survivers reproduce
        self.play(FadeIn(third))
        cat_dark_1 = createCat(GRAY, YELLOW_A, DL)
        cat_dark_2 = createCat(GRAY_BROWN, GOLD_E, DL).next_to(cat_dark_1)
        cat_dark_3 = createCat(BLACK, YELLOW_E, DL).next_to(cat_dark)
        cat_dark_4 = createCat(DARKER_GRAY, YELLOW_C, DL).next_to(cat_dark_3)

        h1 = heart().next_to(cat_grey, UR )
        h1.shift(0.6*LEFT)
        self.play(FadeIn(h1))
        self.play(FadeIn(cat_dark_1, cat_dark_2))
        self.play(FadeOut(h1))

        h2 = heart().next_to(cat_dark_1, UR).shift(0.6*LEFT)
        self.play(FadeIn(h2))
        self.play(FadeIn(cat_dark_3, cat_dark_4))
        self.play(FadeOut(h2))
        self.wait(2)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.terminology()

    def terminology(self):
        # Show inital genes
        gene1 = generateGene(["A", "C", "G", "T", "A"]).shift(LEFT)
        gene2 = generateGene(["C", "G", "G", "T", "T"]).next_to(gene1).shift(2 * RIGHT)
        self.play(FadeIn(gene1, gene2))
        self.wait(3)

        # Mutation animation
        mutatedGene = generateGene(["C", "A", "G", "T", "T"]).next_to(gene1).shift(2 * RIGHT)
        mutatedGene[1][1].set_color(PURE_RED)
        self.play(ReplacementTransform(gene2, mutatedGene, run_time=3))
        self.wait(2)


if __name__ == "__main__":
    os.system("manim -pql evolutionary.py Evolution")





