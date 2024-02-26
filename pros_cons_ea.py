from manim import *
import os
import numpy as np
import random


# Manim Code
class Pros_Cons(MovingCameraScene):
    def construct(self):
        Text.set_default(font="Monospace")
        # Erste Seite
        text_1 = Text('Vor- und Nachteile', color=WHITE,t2c={'[:3]': 'GREEN', '[9:]': 'RED'})
        text_2 = Text('Genetischer Algorithmen', color=WHITE)
        text = VGroup(text_1, text_2).arrange(DOWN, aligned_edge=LEFT)
        text.move_to(ORIGIN)
        self.play(FadeIn(text))
        text_2.shift(0.1 * DOWN)
        self.wait(2)
        self.play(text.animate.shift(3 * UP), text.animate.shift(3 * UP))

        # Löscht alles von der Szene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Aufruf der nächsten Methode als nächste Folie
        self.pros()

    def pros(self):
        # Nächste Folie
        title = Text("Vorteile",color=GREEN)
        title.center()
        title.move_to(ORIGIN)
        self.play(GrowFromCenter(title))
        self.play(title.animate.shift(3 * UP), title.animate.shift(3 * UP))

        self.wait(2)
        
        # Erster Vorteil Text
        pro1 = Paragraph("1. Sie lassen sich auf eine Vielzahl von Problemstellungen anwenden,","   ohne dass ein spezielles Problem-Know-how notwendig ist.").scale(0.5).to_edge(LEFT).shift(2 * UP)
        pro1_title = Text("1. Flexibilität").scale(0.5).to_edge(LEFT).shift(2 * UP)
        
        # Zweiter Vorteil Text
        pro2 = Paragraph("2. Im Gegensatz zu vielen traditionellen Optimierungsverfahren,","   die in lokalen Optima stecken bleiben können,","   haben evolutionäre Algorithmen eine bessere Chance,","   globale Optima zu finden,","   insbesondere in komplexen und rauen Suchlandschaften.").scale(0.5).next_to(pro1_title, DOWN, buff=0.5, aligned_edge=LEFT)
        pro2_title = Text("2. Fähigkeit, globale Optima zu finden").scale(0.5).next_to(pro1_title, DOWN, buff=0.5, aligned_edge=LEFT)

        # Dritter Vorteil Text
        pro3 = Paragraph("3. Evolutionäre Algorithmen sind gut parallelisierbar,","   d.h. sie können moderne Multicore- und verteilte Computersysteme","   nutzen, um schneller zu einem Ziel zu konvergieren.").scale(0.5).next_to(pro2_title, DOWN, buff=0.5, aligned_edge=LEFT)
        pro3_title = Text("3. Parallelisierbarkeit").scale(0.5).next_to(pro2_title, DOWN, buff=0.5, aligned_edge=LEFT)
    
        # Vierter Vorteil Text
        pro4 = Paragraph("4. Sie sind oft robust gegenüber Veränderungen der Problemstellung","   oder der Einführung von Störungen, was sie für","   dynamische oder unsichere Umgebungen geeignet macht.").scale(0.5).next_to(pro3_title, DOWN, buff=0.5, aligned_edge=LEFT)
        pro4_title = Text("4. Robustheit").scale(0.5).next_to(pro3_title, DOWN, buff=0.5, aligned_edge=LEFT)
        
        # Fünfter Vorteil Text
        pro5 = Paragraph("5. Im Gegensatz zu Methoden wie dem Gradientenabstieg benötigen","   Evolutionäre Algorithmen keine Information über den Gradienten ","   der Zielfunktion, was sie für Probleme nützlich macht,","   bei denen diese Information schwer zu berechnen ist.").scale(0.5).next_to(pro4_title, DOWN, buff=0.5, aligned_edge=LEFT)
        pro5_title = Text("5. Keine Information über den Gradienten erforderlich").scale(0.5).next_to(pro4_title, DOWN, buff=0.5, aligned_edge=LEFT)

        # Animation für Pro1
        self.play(FadeIn(pro1))
        self.wait(10)
        self.play(ReplacementTransform(pro1, pro1_title))
        self.wait(2)
        
        # Animation für Pro2
        self.play(FadeIn(pro2))
        self.wait(15)
        self.play(ReplacementTransform(pro2, pro2_title))
        self.wait(2)
        
        # Animation für Pro3 # Nächste Folie
        self.play(FadeIn(pro3))
        self.wait(10)
        self.play(ReplacementTransform(pro3, pro3_title))
        self.wait(2)
        
        # Animation für Pro4
        self.play(FadeIn(pro4))
        self.wait(12)
        self.play(ReplacementTransform(pro4, pro4_title))
        self.wait(2)
        
        # Animation für Pro5
        self.play(FadeIn(pro5))
        self.wait(13)
        self.play(ReplacementTransform(pro5, pro5_title))
        self.wait(2)

        # Auflösung der Texte
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        # Aufruf der nächsten Methode als nächste Folie 
        self.cons()

    def cons(self):
        # Nächste Folie
        title = Text("Nachteile",color=RED)
        title.center()
        title.move_to(ORIGIN)
        self.play(GrowFromCenter(title))
        self.play(title.animate.shift(3 * UP), title.animate.shift(3 * UP))

        self.wait(2)
        
        # Erster Nachteil Text 
        cons1 = Paragraph("1. Sie können sehr rechenintensiv sein, insbesondere für Probleme","   mit hoher Dimensionalität oder wenn eine große Anzahl","   von Generationen erforderlich ist,","   um eine akzeptable Lösung zu finden.").scale(0.5).to_edge(LEFT).shift(2 * UP)
        cons1_title = Text("1. Rechenintensität").scale(0.5).to_edge(LEFT).shift(2 * UP)
        
        # Zweiter Nachteil Text
        cons2 = Paragraph("2. Die Leistungsfähigkeit evolutionärer Algorithmen hängt stark","   von der Wahl der Parameter (z.B. Populationsgröße, Mutationsrate)","   ab und die optimale Einstellung dieser Parameter","   ist oft problemabhängig und nicht trivial.").scale(0.5).next_to(cons1_title, DOWN, buff=0.5, aligned_edge=LEFT)
        cons2_title = Text("2. Parameterwahl").scale(0.5).next_to(cons1_title, DOWN, buff=0.5, aligned_edge=LEFT)

        # Dritter Nachteil Text
        cons3 = Paragraph("3. Für einige Probleme können Evolutionäre Algorithmen","   langsamer konvergieren als spezialisierte Optimierungsverfahren.").scale(0.5).next_to(cons2_title, DOWN, buff=0.5, aligned_edge=LEFT)
        cons3_title = Text("3. Geschwindigkeit der Konvergenz").scale(0.5).next_to(cons2_title, DOWN, buff=0.5, aligned_edge=LEFT)

        # Vierter Nachteil Text
        cons4 = Paragraph("4. Obwohl die Grundkonzepte von genetischen Algorithmen","   verständlich sind, kann die Implementierung einer","   effektiven und effizienten Lösung komplex sein,","   insbesondere was die Gestaltung der Zielfunktion und","   die Auswahl der richtigen Operatoren betrifft.").scale(0.5).next_to(cons3_title, DOWN, buff=0.5, aligned_edge=LEFT)
        cons4_title = Text("4. Aufstellung der Zielfunktion").scale(0.5).next_to(cons3_title, DOWN, buff=0.5, aligned_edge=LEFT)

        # Animation für cons1
        self.play(FadeIn(cons1))
        self.wait(15)
        self.play(ReplacementTransform(cons1, cons1_title))
        self.wait(2)

        # Animation für cons2
        self.play(FadeIn(cons2))
        self.wait(17)
        self.play(ReplacementTransform(cons2, cons2_title))
        self.wait(2)

        # Animation für cons3
        self.play(FadeIn(cons3))
        self.wait(15)
        self.play(ReplacementTransform(cons3, cons3_title))
        self.wait(2)

        # Animation für cons4
        self.play(FadeIn(cons4))
        self.wait(15)
        self.play(ReplacementTransform(cons4, cons4_title))

        # Warte 2 Sekunden
        self.wait(2)

        # Auflösung der Texte
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        

if __name__ == "__main__":
    os.system("manim -pql pros_cons_ea.py Pros_Cons")
