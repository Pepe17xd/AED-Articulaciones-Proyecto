"""Prototipo de escena controlado por eventos reales de run_tarjan."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import (
    BLUE_C,
    GOLD,
    GREY_B,
    ORANGE,
    WHITE,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    Text,
    Transform,
    DOWN,
    UP,
    config,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from articulations import Graph, run_tarjan, validate_trace  # noqa: E402


class TracePreview(Scene):
    """Muestra un ciclo y sus articulaciones reproduciendo la traza de Tarjan."""

    def construct(self) -> None:
        self.camera.background_color = "#10131B"
        graph = Graph.from_edges(
            [
                ("A", "B"),
                ("A", "G"),
                ("B", "C"),
                ("C", "D"),
                ("D", "B"),
                ("D", "E"),
                ("E", "F"),
            ]
        )
        trace = run_tarjan(graph)
        validate_trace(graph, trace)

        title = Text("Puntos de articulación · DFS en vivo", font_size=31, color=WHITE)
        title.to_edge(UP, buff=0.32)
        self.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.55)

        positions = {
            "A": (-4.4, 0.65, 0),
            "B": (-2.7, 0.65, 0),
            "C": (-1.0, 1.75, 0),
            "D": (0.7, 0.65, 0),
            "E": (2.4, 0.65, 0),
            "F": (4.1, 0.65, 0),
            "G": (-4.4, -1.5, 0),
        }
        edge_objects: dict[tuple[str, str], Line] = {}
        for left, right in graph.edges:
            edge = Line(positions[left], positions[right], color=GREY_B, stroke_width=3)
            edge_objects[(left, right)] = edge
        self.play(*(Create(edge) for edge in edge_objects.values()), run_time=0.65)

        nodes: dict[str, Circle] = {}
        values: dict[str, Text] = {}
        for vertex in graph.vertices:
            node = Circle(radius=0.32, color=BLUE_C, stroke_width=2.5, fill_opacity=0.08)
            node.move_to(positions[vertex])
            label = Text(vertex, font_size=23, color=WHITE).move_to(node)
            value = Text("tin —  low —", font_size=15, color=GREY_B)
            value.next_to(node, DOWN, buff=0.18)
            nodes[vertex] = node
            values[vertex] = value
            self.add(node, label, value)

        caption = Text("La escena sigue los eventos producidos por la DFS.", font_size=20, color=WHITE)
        caption.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(caption), run_time=0.35)

        tin_values: dict[str, int] = {}
        low_values: dict[str, int] = {}
        significant = {
            "discover_vertex",
            "traverse_tree_edge",
            "observe_back_edge",
            "update_low",
            "identify_articulation",
        }
        for event in trace.events:
            if event.type not in significant:
                continue

            if event.type == "discover_vertex":
                tin_values[event.vertex] = event.tin_value
                low_values[event.vertex] = event.low_value
                new_value = Text(
                    f"tin {event.tin_value}   low {event.low_value}",
                    font_size=15,
                    color=WHITE,
                ).move_to(values[event.vertex])
                self.play(
                    nodes[event.vertex].animate.set_fill(BLUE_C, opacity=0.35),
                    Transform(values[event.vertex], new_value),
                    run_time=0.3,
                )
                values[event.vertex] = new_value
                caption_text = f"Descubrimos {event.vertex}: tin = low = {event.tin_value}"
            elif event.type == "traverse_tree_edge":
                edge = edge_objects[event.edge]
                self.play(edge.animate.set_color(BLUE_C).set_stroke(width=5), run_time=0.18)
                caption_text = f"Arista de árbol: {event.vertex} → {event.neighbor}"
            elif event.type == "observe_back_edge":
                edge = edge_objects[event.edge]
                self.play(edge.animate.set_color(GOLD).set_stroke(width=5), run_time=0.2)
                caption_text = (
                    f"Retorno {event.vertex} → {event.neighbor}: "
                    f"tin[{event.neighbor}] = {event.neighbor_tin}"
                )
            elif event.type == "update_low":
                low_values[event.vertex] = event.low_value
                new_value = Text(
                    f"tin {tin_values[event.vertex]}   low {event.low_value}",
                    font_size=15,
                    color=GOLD,
                ).move_to(values[event.vertex])
                self.play(Transform(values[event.vertex], new_value), run_time=0.2)
                values[event.vertex] = new_value
                caption_text = f"Actualizamos low[{event.vertex}] = {event.candidate}"
            else:
                nodes[event.vertex].set_fill(ORANGE, opacity=0.52)
                caption_text = (
                    f"{event.vertex} es articulación · "
                    + (
                        f"low[hijo] = {event.candidate} ≥ tin[{event.vertex}]"
                        if event.reason == "low_child_ge_tin_vertex"
                        else f"raíz con {event.candidate} hijos DFS"
                    )
                )

            new_caption = Text(caption_text, font_size=20, color=WHITE).move_to(caption)
            caption.become(new_caption)

        final = Text(
            "Articulaciones: " + " · ".join(trace.articulations),
            font_size=26,
            color=GOLD,
        ).move_to(caption)
        caption.become(final)
        self.wait(1.0)


if __name__ == "__main__":
    config.pixel_width = 1280
    config.pixel_height = 720
