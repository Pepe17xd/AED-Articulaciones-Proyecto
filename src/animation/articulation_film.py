"""Película educativa completa: las secuencias algorítmicas vienen de Tarjan."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import (
    BLUE_C,
    GOLD,
    GREEN_C,
    GREY_B,
    ORANGE,
    RED_C,
    WHITE,
    Circle,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    Flash,
    Line,
    MathTex,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    DOWN,
    LEFT,
    RIGHT,
    UP,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from articulations import Graph, run_tarjan, validate_trace  # noqa: E402
from animation.intro_graph import INTRO_NAMES, INTRO_POSITIONS, intro_graph  # noqa: E402

BG = "#10131B"
MAIN_EDGES = [
    ("A", "B"),
    ("A", "G"),
    ("B", "C"),
    ("C", "D"),
    ("D", "B"),
    ("D", "E"),
    ("E", "F"),
]
MAIN_POSITIONS = {
    "A": (-4.4, 0.65, 0),
    "B": (-2.7, 0.65, 0),
    "C": (-1.0, 1.75, 0),
    "D": (0.7, 0.65, 0),
    "E": (2.4, 0.65, 0),
    "F": (4.1, 0.65, 0),
    "G": (-4.4, -1.5, 0),
}


def main_graph() -> Graph:
    return Graph.from_edges(MAIN_EDGES)


def graph_view(
    scene: Scene,
    graph: Graph,
    positions: dict[str, tuple[float, float, float]],
    *,
    radius: float = 0.31,
    value_labels: bool = False,
    node_labels: dict[str, str] | None = None,
) -> tuple[
    VGroup,
    dict[tuple[str, str], Line],
    dict[str, Circle],
    dict[str, Text],
    dict[str, Text],
]:
    """Build and animate a graph illustration; no algorithmic state is stored."""
    edges: dict[tuple[str, str], Line] = {}
    nodes: dict[str, Circle] = {}
    labels: dict[str, Text] = {}
    values: dict[str, Text] = {}
    edge_group = VGroup()
    for left, right in graph.edges:
        line = Line(positions[left], positions[right], color=GREY_B, stroke_width=3)
        edges[(left, right)] = line
        edge_group.add(line)

    node_group = VGroup()
    label_group = VGroup()
    value_group = VGroup()
    for vertex in graph.vertices:
        node = Circle(radius=radius, color=BLUE_C, stroke_width=2.5, fill_opacity=0.08)
        node.move_to(positions[vertex])
        label_text = (node_labels or {}).get(vertex, vertex)
        label = Text(label_text, font_size=19 if len(label_text) > 1 else 23, color=WHITE).move_to(node)
        nodes[vertex] = node
        labels[vertex] = label
        node_group.add(node)
        label_group.add(label)
        if value_labels:
            value = Text("tin —   low —", font_size=14, color=GREY_B)
            value.next_to(node, DOWN, buff=0.17)
            values[vertex] = value
            value_group.add(value)

    scene.play(Create(edge_group), run_time=0.65)
    scene.play(FadeIn(node_group), FadeIn(label_group), run_time=0.45)
    if value_group:
        scene.add(value_group)
    return VGroup(edge_group, node_group, label_group, value_group), edges, nodes, values, labels


class ArticulationFilm(Scene):
    """Siete capítulos, con la ejecución principal impulsada por eventos reales."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.scene_one_motivation()
        self.scene_two_definition()
        self.scene_three_idea()
        self.scene_four_real_execution()
        self.scene_five_root_case()
        self.scene_six_complexity()
        self.scene_seven_conclusion()

    def header(self, title: str, subtitle: str | None = None) -> VGroup:
        title_mob = Text(title, font_size=30, color=WHITE).to_edge(UP, buff=0.28)
        group = VGroup(title_mob)
        if subtitle:
            sub = Text(subtitle, font_size=19, color=GREY_B).next_to(title_mob, DOWN, buff=0.12)
            group.add(sub)
        self.play(FadeIn(group, shift=0.12 * DOWN), run_time=0.7)
        return group

    def caption(self, content: str, *, color=WHITE, size: int = 21, y: float = -3.15) -> Text:
        mob = Text(content, font_size=size, color=color)
        mob.move_to((0, y, 0))
        self.add(mob)
        return mob

    def change_caption(self, current: Text, content: str, *, color=WHITE, size: int = 21) -> Text:
        replacement = Text(content, font_size=size, color=color).move_to(current)
        current.become(replacement)
        return current

    def clear_chapter(self) -> None:
        if self.mobjects:
            self.play(*(FadeOut(mob) for mob in tuple(self.mobjects)), run_time=0.55)

    def scene_one_motivation(self) -> None:
        title = self.header("Cuando una estación falla, ¿qué pasa con la red?")
        caption = self.caption("Una red de transporte depende de conexiones entre estaciones.")
        graph = intro_graph()
        _, edges, nodes, _, labels = graph_view(
            self, graph, INTRO_POSITIONS, radius=0.4, node_labels=INTRO_NAMES
        )
        for station, label in labels.items():
            label.scale(0.78).next_to(nodes[station], DOWN, buff=0.42)
        self.play(*(edge.animate.set_color(BLUE_C).set_stroke(width=5) for edge in edges.values()), run_time=0.7)
        self.wait(3.5)
        caption = self.change_caption(caption, "Las líneas representan rutas disponibles entre estaciones.", size=20)
        self.wait(3.0)
        caption = self.change_caption(caption, "Si Centro queda fuera de servicio, la red puede separarse.")
        self.play(nodes["C"].animate.set_fill(RED_C, opacity=0.55), Flash(nodes["C"], color=RED_C), run_time=0.8)
        self.play(FadeOut(nodes["C"]), FadeOut(labels["C"]), run_time=0.45)
        # Remove the incident tracks and reveal the two disconnected sides.
        for edge in edges.values():
            if edge in (edges[("C", "E")], edges[("C", "O")], edges[("C", "S")]):
                edge.set_color(RED_C)
        self.play(*(FadeOut(edges[key]) for key in [("C", "O"), ("C", "E"), ("C", "S")]), run_time=0.5)
        self.play(nodes["O"].animate.set_fill(GREEN_C, opacity=0.3), nodes["S"].animate.set_fill(GREEN_C, opacity=0.3), run_time=0.35)
        self.play(nodes["E"].animate.set_fill(GOLD, opacity=0.3), nodes["N"].animate.set_fill(GOLD, opacity=0.3), run_time=0.35)
        caption = self.change_caption(caption, "¿Cómo encontramos, sin probar cada falla, los nodos críticos?", size=22)
        self.wait(8.0)
        self.clear_chapter()

    def scene_two_definition(self) -> None:
        self.header("La idea: medir qué vértices sostienen la conectividad")
        definition = Text(
            "Un vértice es de articulación si al retirarlo aumenta\nel número de componentes conexas.",
            font_size=25,
            line_spacing=0.9,
            color=WHITE,
        ).move_to((0, 1.95, 0))
        self.play(FadeIn(definition, shift=0.2 * UP), run_time=0.8)
        self.wait(5.0)
        left_title = Text("Ciclo: hay otra ruta", font_size=20, color=GREEN_C).move_to((-3.1, 0.65, 0))
        right_title = Text("Puente: la red se divide", font_size=20, color=ORANGE).move_to((3.1, 0.65, 0))
        self.play(FadeIn(left_title), FadeIn(right_title), run_time=0.45)

        cycle = Graph.from_edges([("A", "B"), ("B", "C"), ("C", "A")])
        cycle_pos = {"A": (-4.1, -0.55, 0), "B": (-2.6, -0.55, 0), "C": (-3.35, -1.85, 0)}
        cycle_group, cycle_edges, cycle_nodes, _, cycle_labels = graph_view(self, cycle, cycle_pos, radius=0.28)
        path = Graph.from_edges([("P", "Q"), ("Q", "R")])
        path_pos = {"P": (2.0, -0.55, 0), "Q": (3.5, -0.55, 0), "R": (5.0, -0.55, 0)}
        path_group, path_edges, path_nodes, _, path_labels = graph_view(self, path, path_pos, radius=0.28)
        self.wait(4.0)

        self.play(cycle_nodes["B"].animate.set_fill(RED_C, opacity=0.4), run_time=0.35)
        self.play(FadeOut(cycle_nodes["B"]), FadeOut(cycle_labels["B"]), FadeOut(cycle_edges[("A", "B")]), FadeOut(cycle_edges[("B", "C")]), run_time=0.5)
        self.play(cycle_edges[("A", "C")].animate.set_color(GREEN_C).set_stroke(width=5), run_time=0.55)
        self.wait(3.0)
        self.play(path_nodes["Q"].animate.set_fill(ORANGE, opacity=0.5), run_time=0.35)
        self.play(FadeOut(path_nodes["Q"]), FadeOut(path_labels["Q"]), FadeOut(path_edges[("P", "Q")]), FadeOut(path_edges[("Q", "R")]), run_time=0.5)
        self.play(path_nodes["P"].animate.set_fill(RED_C, opacity=0.35), path_nodes["R"].animate.set_fill(GOLD, opacity=0.35), run_time=0.45)
        footer = self.caption("Quitar B no desconecta el ciclo; quitar Q separa P de R.", size=19, y=-3.1)
        self.wait(8.0)
        self.clear_chapter()

    def scene_three_idea(self) -> None:
        self.header("DFS descubre rutas alternativas al retroceder")
        graph = main_graph()
        concept_positions = {
            vertex: (x * 0.82, y * 0.82 + 0.55, 0)
            for vertex, (x, y, _) in MAIN_POSITIONS.items()
        }
        _, edges, nodes, values, _ = graph_view(self, graph, concept_positions, value_labels=True)
        trace = run_tarjan(graph)
        validate_trace(graph, trace)
        caption = self.caption("DFS explora tan lejos como puede y luego vuelve por el árbol.", size=20)
        self.wait(6.0)
        discovered: dict[str, int] = {}
        lows: dict[str, int] = {}

        # This short intuition pass uses the execution's actual events and values.
        for event in trace.events:
            if event.type == "discover_vertex":
                discovered[event.vertex] = event.tin_value
                lows[event.vertex] = event.low_value
                replacement = Text(f"tin {event.tin_value}   low {event.low_value}", font_size=14, color=WHITE).move_to(values[event.vertex])
                self.play(nodes[event.vertex].animate.set_fill(BLUE_C, opacity=0.3), Transform(values[event.vertex], replacement), run_time=0.35)
                values[event.vertex] = replacement
            elif event.type == "traverse_tree_edge" and event.edge:
                self.play(edges[event.edge].animate.set_color(BLUE_C).set_stroke(width=4), run_time=0.22)
            elif event.type == "observe_back_edge" and event.vertex == "D":
                self.play(edges[event.edge].animate.set_color(GOLD).set_stroke(width=5), run_time=0.45)
                caption = self.change_caption(caption, "D encuentra una arista de retorno hacia el ancestro B.")
                self.wait(4.0)
            elif event.type == "update_low" and event.vertex == "D":
                lows[event.vertex] = event.low_value
                replacement = Text(f"tin {discovered[event.vertex]}   low {event.low_value}", font_size=14, color=GOLD).move_to(values[event.vertex])
                self.play(Transform(values[event.vertex], replacement), run_time=0.4)
                values[event.vertex] = replacement
                caption = self.change_caption(caption, "low[D] retrocede hasta tin[B] gracias a esa alternativa.")
                self.wait(5.0)

        formula = MathTex(
            r"low[u]=\min\bigl(tin[u],\ tin[ancestros],\ low[hijos]\bigr)",
            color=WHITE,
            font_size=38,
        ).move_to((0, -2.25, 0))
        self.play(FadeIn(formula, shift=0.15 * UP), run_time=0.65)
        caption = self.change_caption(caption, "low[u] resume el ancestro más antiguo que alcanza su subárbol.", size=19)
        self.wait(6.0)
        equality = MathTex(r"low[C]=1\quad =\quad tin[B]", color=GOLD, font_size=34).move_to((0, -1.15, 0))
        self.play(FadeIn(equality, shift=0.12 * UP), run_time=0.5)
        caption = self.change_caption(caption, "La igualdad también cuenta: B no tiene una salida desde el subárbol de C.", size=18)
        self.wait(6.0)
        self.clear_chapter()

    def scene_four_real_execution(self) -> None:
        self.header("Una ejecución real: cada paso sale de la traza")
        graph = main_graph()
        trace = run_tarjan(graph)
        validate_trace(graph, trace)
        _, edges, nodes, values, _ = graph_view(self, graph, MAIN_POSITIONS, value_labels=True)
        caption = self.caption("Orden determinista: vecinos en orden alfabético.", size=19)
        self.wait(7.5)
        current: str | None = None
        discovered: dict[str, int] = {}
        lows: dict[str, int] = {}
        important = {
            "discover_vertex",
            "traverse_tree_edge",
            "observe_back_edge",
            "update_low",
            "identify_articulation",
        }
        for event in trace.events:
            if event.type not in important:
                continue
            if event.type == "discover_vertex":
                current = event.vertex
                discovered[event.vertex] = event.tin_value
                lows[event.vertex] = event.low_value
                new_value = Text(f"tin {event.tin_value}   low {event.low_value}", font_size=14, color=WHITE).move_to(values[event.vertex])
                self.play(
                    nodes[event.vertex].animate.set_fill(BLUE_C, opacity=0.35),
                    Transform(values[event.vertex], new_value),
                    run_time=0.45,
                )
                values[event.vertex] = new_value
                caption = self.change_caption(caption, f"Descubrimos {event.vertex}: tin = low = {event.tin_value}", size=20)
                self.wait(1.3)
            elif event.type == "traverse_tree_edge":
                current = event.neighbor
                self.play(edges[event.edge].animate.set_color(BLUE_C).set_stroke(width=4.5), run_time=0.3)
                caption = self.change_caption(caption, f"Seguimos la arista de árbol {event.vertex} → {event.neighbor}.", size=20)
                self.wait(1.2)
            elif event.type == "observe_back_edge":
                self.play(edges[event.edge].animate.set_color(GOLD).set_stroke(width=5.5), run_time=0.4)
                caption = self.change_caption(
                    caption,
                    f"Retorno {event.vertex} → {event.neighbor}: llega al tiempo {event.neighbor_tin}.",
                    size=20,
                )
                self.wait(3.0)
            elif event.type == "update_low":
                lows[event.vertex] = event.low_value
                new_value = Text(
                    f"tin {discovered[event.vertex]}   low {event.low_value}",
                    font_size=14,
                    color=GOLD,
                ).move_to(values[event.vertex])
                self.play(Transform(values[event.vertex], new_value), run_time=0.42)
                values[event.vertex] = new_value
                caption = self.change_caption(caption, f"Al volver, low[{event.vertex}] = {event.candidate}.", size=20)
                self.wait(2.8)
            else:
                nodes[event.vertex].set_fill(ORANGE, opacity=0.52)
                condition = (
                    f"low[hijo] = {event.candidate} ≥ tin[{event.vertex}]"
                    if event.reason == "low_child_ge_tin_vertex"
                    else f"raíz con {event.candidate} hijos DFS"
                )
                ring = Circle(radius=0.43, color=GOLD, stroke_width=3).move_to(nodes[event.vertex])
                self.play(Create(ring), run_time=0.35)
                caption = self.change_caption(caption, f"Articulación {event.vertex}: {condition}.", color=GOLD, size=20)
                self.wait(3.0)
                self.play(FadeOut(ring), run_time=0.18)

        caption = self.change_caption(
            caption,
            "La ejecución termina: A, B, D y E cumplen la condición de articulación.",
            color=GOLD,
            size=20,
        )
        self.wait(8.0)
        self.clear_chapter()

    def scene_five_root_case(self) -> None:
        self.header("La raíz de DFS tiene una regla especial")
        left_heading = Text("Un hijo DFS", font_size=22, color=GREEN_C).move_to((-3.2, 1.75, 0))
        right_heading = Text("Dos hijos DFS", font_size=22, color=GOLD).move_to((3.0, 1.75, 0))
        self.play(FadeIn(left_heading), FadeIn(right_heading), run_time=0.5)

        one_graph = Graph.from_edges([("A", "B"), ("B", "C")])
        one_positions = {"A": (-4.4, 0.15, 0), "B": (-2.9, 0.15, 0), "C": (-1.4, 0.15, 0)}
        _, one_edges, one_nodes, _, _ = graph_view(self, one_graph, one_positions, radius=0.29)
        one_trace = run_tarjan(one_graph)
        validate_trace(one_graph, one_trace)
        one_root_children = sum(e.type == "traverse_tree_edge" and e.vertex == "A" for e in one_trace.events)
        note1 = Text(f"hijos = {one_root_children} → A no es articulación", font_size=19, color=GREEN_C).move_to((-2.9, -1.0, 0))
        self.play(one_nodes["A"].animate.set_fill(GREEN_C, opacity=0.25), FadeIn(note1), run_time=0.6)
        self.wait(5.0)

        two_graph = Graph.from_edges([("R", "S"), ("R", "T")])
        two_positions = {"R": (1.4, 0.15, 0), "S": (3.0, 0.95, 0), "T": (3.0, -0.65, 0)}
        _, two_edges, two_nodes, _, _ = graph_view(self, two_graph, two_positions, radius=0.29)
        two_trace = run_tarjan(two_graph)
        validate_trace(two_graph, two_trace)
        root_event = next(e for e in two_trace.events if e.type == "identify_articulation" and e.vertex == "R" and e.reason == "root_has_multiple_dfs_children")
        root_children = sum(e.type == "traverse_tree_edge" and e.vertex == "R" for e in two_trace.events)
        if dict(two_trace.parent)["R"] is not None or root_children <= 1 or root_event.candidate != root_children:
            raise ValueError("El ejemplo requiere una raíz DFS con varios hijos")
        note2 = Text(f"hijos = {root_children} → R sí es articulación", font_size=19, color=GOLD).move_to((3.15, -1.55, 0))
        self.play(two_nodes["R"].animate.set_fill(GOLD, opacity=0.45), FadeIn(note2), run_time=0.6)
        self.wait(6.0)
        caption = self.caption("La raíz se evalúa por número de hijos del árbol DFS; los demás usan low ≥ tin.", size=18)
        self.wait(8.0)
        self.clear_chapter()

    def scene_six_complexity(self) -> None:
        self.header("Una sola búsqueda basta")
        graph = main_graph()
        compact_positions = {v: (x * 0.6 - 1.5, y * 0.6 + 0.25, 0) for v, (x, y, _) in MAIN_POSITIONS.items()}
        _, edges, nodes, _, _ = graph_view(self, graph, compact_positions, radius=0.22)
        trace = run_tarjan(graph)
        validate_trace(graph, trace)
        vertex_count = len(graph.vertices)
        edge_count = len(graph.edges)
        stats = VGroup(
            Text(f"V = {vertex_count} vértices", font_size=25, color=WHITE),
            Text(f"E = {edge_count} aristas", font_size=25, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to((3.25, 1.05, 0))
        self.play(FadeIn(stats, shift=0.2 * LEFT), run_time=0.6)
        caption = self.caption("DFS descubre cada vértice una vez y examina cada arista desde ambos extremos.", size=19)
        self.wait(4.5)
        for vertex in graph.vertices:
            self.play(nodes[vertex].animate.set_fill(BLUE_C, opacity=0.32), run_time=0.11)
        for edge in graph.edges:
            self.play(edges[edge].animate.set_color(GOLD), run_time=0.1)
        time_formula = MathTex(r"T(V,E)=O(V+E)", color=GOLD, font_size=46).move_to((2.6, -0.75, 0))
        space_formula = MathTex(r"S_{aux}=O(V)\quad;\quad G=O(V+E)", color=WHITE, font_size=32).move_to((2.9, -1.65, 0))
        self.play(FadeIn(time_formula, shift=0.15 * UP), run_time=0.65)
        self.play(FadeIn(space_formula, shift=0.15 * UP), run_time=0.65)
        caption = self.change_caption(caption, "Las listas de adyacencia permiten recorrer el grafo en tiempo lineal.", size=19)
        self.wait(9.0)
        self.clear_chapter()

    def scene_seven_conclusion(self) -> None:
        self.header("Encontrar puntos críticos antes de que falle la red")
        graph = main_graph()
        compact_positions = {v: (x * 0.85, y * 0.72 + 0.5, 0) for v, (x, y, _) in MAIN_POSITIONS.items()}
        _, edges, nodes, _, _ = graph_view(self, graph, compact_positions)
        trace = run_tarjan(graph)
        validate_trace(graph, trace)
        for edge in graph.edges:
            self.play(edges[edge].animate.set_color(BLUE_C), run_time=0.08)
        self.wait(3.0)
        for vertex in trace.articulations:
            nodes[vertex].set_fill(ORANGE, opacity=0.52)
            ring = Circle(radius=0.42, color=GOLD, stroke_width=3).move_to(nodes[vertex])
            self.play(Create(ring), run_time=0.22)
        articulation_names = " · ".join(trace.articulations) or "ninguna"
        result = Text(f"Articulaciones: {articulation_names}", font_size=27, color=GOLD).move_to((0, -2.35, 0))
        self.play(FadeIn(result, shift=0.15 * UP), run_time=0.65)
        takeaway = Text("DFS + tin + low detectan dónde se rompe la conectividad.", font_size=21, color=WHITE).move_to((0, -2.95, 0))
        self.play(FadeIn(takeaway), run_time=0.5)
        self.wait(4.5)
        credits = VGroup(
            Text("Proyecto AED · Articulaciones en grafos", font_size=19, color=GREY_B),
            Text("Antony Yonel Rosales Esteban", font_size=19, color=WHITE),
            Text("Jeseph Imanol Burgos Ochoa", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.2).move_to((0, -1.55, 0))
        self.play(FadeOut(result), FadeOut(takeaway), FadeIn(credits, shift=0.15 * UP), run_time=0.75)
        self.wait(6.0)
