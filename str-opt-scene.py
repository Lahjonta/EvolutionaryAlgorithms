from manim import *

class Example1(Scene):
    def construct(self):

        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        header = Text("String Optimization", font_size=48)
        target_text = Text("Target: Integrationsseminar", font_size=36)
        # LaTeX text with line breaks for valid_genes
        valid_genes = VGroup(
            Text("abcdefghijklmnopqrstuvwxyz", font_size=36),
            Text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", font_size=36),
            Text('1234567890, .-;:_!"#%&/()=?@${[]}', font_size=36)
        ).arrange(DOWN, center=True)
        brace_genes = Brace(mobject=valid_genes[2], direction=DOWN, buff=0.2)
        brace_genes_text = brace_genes.get_text("Valid Genes")

        self.add(header)
        # Set the target properties for the header
        header.target = header.copy()
        header.target.scale(0.50)  # Scale down the header
        header.target.to_edge(UL)  # Move to upper left
        # Animate the header transformation
        self.play(ScaleInPlace(header, 0.50), MoveToTarget(header))
        self.wait(1)
        # Position target_text three rows above center
        target_text.move_to(2 * UP)
        self.play(Create(target_text))
        self.wait(1)
        # Center valid_genes 
        valid_genes.move_to(ORIGIN)
        self.play(Create(valid_genes))
        self.play(GrowFromCenter(brace_genes), FadeIn(brace_genes_text), run_time=2)


if __name__ == "__main__":
    scene = Example1()
    scene.render()





