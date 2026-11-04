"""Datos visuales compartidos por la introduccion original y su prototipo narrado."""

from articulations import Graph

INTRO_EDGES = (
    ("O", "C"),
    ("C", "E"),
    ("C", "S"),
    ("E", "N"),
)

INTRO_POSITIONS = {
    "O": (-3.6, 0.25, 0),
    "C": (-1.2, 0.25, 0),
    "E": (1.2, 0.25, 0),
    "N": (3.6, 0.25, 0),
    "S": (-1.2, -1.8, 0),
}

INTRO_NAMES = {
    "O": "Oeste",
    "C": "Centro",
    "E": "Este",
    "N": "Norte",
    "S": "Sur",
}


def intro_graph() -> Graph:
    """Return the same undirected station network used by the silent introduction."""
    return Graph.from_edges(INTRO_EDGES)
