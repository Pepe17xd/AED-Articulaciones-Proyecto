"""DFS de Tarjan para hallar puntos de articulación con una traza real."""

from __future__ import annotations

from .events import EventRecorder
from .graph import Graph
from .trace import Trace


def run_tarjan(graph: Graph) -> Trace:
    """Ejecuta DFS en todos los componentes y devuelve resultado más eventos.

    Para un vértice no raíz, la condición de articulación es
    ``low[child] >= tin[vertex]``. La raíz se evalúa por separado y requiere
    más de un hijo DFS. La arista al padre se omite; al ser un grafo simple,
    basta comparar la etiqueta del vértice padre.
    """
    tin: dict[str, int] = {}
    low: dict[str, int] = {}
    parent: dict[str, str | None] = {vertex: None for vertex in graph.vertices}
    child_count = {vertex: 0 for vertex in graph.vertices}
    articulation: set[str] = set()
    components: list[tuple[str, ...]] = []
    recorder = EventRecorder(graph.vertices)
    timer = 0
    active_component: list[str] = []

    def emit(
        event_type: str,
        vertex: str,
        neighbor: str | None = None,
        *,
        candidate: int | None = None,
        reason: str | None = None,
    ) -> None:
        recorder.record(
            event_type,
            vertex,
            neighbor,
            parent=parent[vertex],
            tin=tin,
            low=low,
            candidate=candidate,
            reason=reason,
        )

    def dfs(vertex: str) -> None:
        nonlocal timer
        tin[vertex] = low[vertex] = timer
        timer += 1
        active_component.append(vertex)
        emit("discover_vertex", vertex)

        for neighbor in graph.neighbors(vertex):
            emit("examine_edge", vertex, neighbor)
            if neighbor == parent[vertex]:
                emit("skip_parent_edge", vertex, neighbor, reason="parent")
                continue
            if neighbor not in tin:
                parent[neighbor] = vertex
                child_count[vertex] += 1
                emit("traverse_tree_edge", vertex, neighbor)
                dfs(neighbor)

                candidate = low[neighbor]
                if candidate < low[vertex]:
                    low[vertex] = candidate
                    emit("update_low", vertex, neighbor, candidate=candidate, reason="child")
                else:
                    emit("return_to_parent", vertex, neighbor, candidate=candidate, reason="child")

                if parent[vertex] is not None and low[neighbor] >= tin[vertex]:
                    articulation.add(vertex)
                    emit(
                        "identify_articulation",
                        vertex,
                        neighbor,
                        candidate=low[neighbor],
                        reason="low_child_ge_tin_vertex",
                    )
            elif tin[neighbor] < tin[vertex]:
                emit("observe_back_edge", vertex, neighbor)
                candidate = tin[neighbor]
                if candidate < low[vertex]:
                    low[vertex] = candidate
                    emit("update_low", vertex, neighbor, candidate=candidate, reason="back_edge")
                else:
                    emit("return_to_parent", vertex, neighbor, candidate=candidate, reason="back_edge")
            else:
                # Arista ya procesada al descubrir a este descendiente.
                emit("skip_seen_edge", vertex, neighbor, reason="already_processed")

        emit("finish_vertex", vertex)
        if parent[vertex] is None and child_count[vertex] > 1:
            articulation.add(vertex)
            emit(
                "identify_articulation",
                vertex,
                candidate=child_count[vertex],
                reason="root_has_multiple_dfs_children",
            )

    for root in graph.vertices:
        if root not in tin:
            active_component = []
            dfs(root)
            components.append(tuple(active_component))

    return Trace(
        vertices=graph.vertices,
        events=recorder.events,
        tin=tuple((vertex, tin[vertex]) for vertex in graph.vertices),
        low=tuple((vertex, low[vertex]) for vertex in graph.vertices),
        parent=tuple((vertex, parent[vertex]) for vertex in graph.vertices),
        articulations=tuple(sorted(articulation)),
        components=tuple(components),
    )
