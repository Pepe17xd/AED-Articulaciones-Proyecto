"""Componentes reutilizables para representar grafos sin duplicar su estado."""
from manim import BLUE_C, GREY_B, WHITE, Circle, Create, FadeIn, Line, Scene, Text, VGroup, DOWN
from articulations import Graph

from animation.style import BACKGROUND

BG = BACKGROUND
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
            value = Text("tin —   low —", font_size=18, color=GREY_B)
            value.next_to(node, DOWN, buff=0.17)
            values[vertex] = value
            value_group.add(value)

    scene.play(Create(edge_group), run_time=0.65)
    scene.play(FadeIn(node_group), FadeIn(label_group), run_time=0.45)
    if value_group:
        scene.add(value_group)
    return VGroup(edge_group, node_group, label_group, value_group), edges, nodes, values, labels

