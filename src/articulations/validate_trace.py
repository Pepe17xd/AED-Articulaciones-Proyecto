"""Reproduce y valida el estado de una traza sin volver a ejecutar Tarjan."""

from __future__ import annotations

from .graph import Graph
from .trace import Trace


class TraceValidationError(ValueError):
    """La secuencia de eventos no coincide con el estado que declara."""


def validate_trace(graph: Graph, trace: Trace) -> None:
    """Valida orden, padres, valores locales, aristas y decisiones registradas."""
    def require(condition: bool, message: str) -> None:
        if not condition:
            raise TraceValidationError(message)

    require(trace.vertices == graph.vertices, "los vértices de la traza no coinciden con el grafo")
    discovered: dict[str, int] = {}
    lows: dict[str, int] = {}
    tree_parent: dict[str, str | None] = {}
    finished: set[str] = set()
    found_articulations: set[str] = set()

    for expected_seq, event in enumerate(trace.events):
        require(event.seq == expected_seq, f"secuencia inválida en evento {expected_seq}")
        if event.type == "discover_vertex":
            require(event.vertex in graph.vertices, "descubrimiento de vértice inexistente")
            require(event.vertex not in discovered, "vértice descubierto más de una vez")
            require(event.tin_value == len(discovered), "tiempo de descubrimiento no consecutivo")
            require(event.low_value == event.tin_value, "low inicial debe ser igual a tin")
            require(event.parent == tree_parent.get(event.vertex), f"padre incorrecto al descubrir {event.vertex}")
            discovered[event.vertex] = event.tin_value
            lows[event.vertex] = event.low_value
        else:
            require(event.vertex in discovered, f"evento previo al descubrimiento de {event.vertex}")
            require(event.tin_value == discovered[event.vertex], f"tin inconsistente en evento {event.seq}")
            require(event.parent == tree_parent.get(event.vertex), f"padre inconsistente en evento {event.seq}")
            if event.type == "update_low":
                require(event.candidate is not None, "update_low requiere candidato")
                require(event.reason in {"child", "back_edge"}, "causa de update_low desconocida")
                require(event.candidate < lows[event.vertex], "update_low debe reducir el valor low")
                require(event.low_value == event.candidate, "low actualizado no coincide con candidato")
                if event.reason == "child":
                    require(event.neighbor in discovered, "hijo no descubierto al actualizar low")
                    require(event.candidate == lows[event.neighbor], "candidato child distinto de low[hijo]")
                else:
                    require(event.neighbor is not None, "arista de retroceso sin vecino")
                    require(event.candidate == discovered[event.neighbor], "candidato back_edge distinto de tin[vecino]")
                lows[event.vertex] = event.candidate
            else:
                require(event.low_value == lows[event.vertex], f"low inconsistente en evento {event.seq}")

        if event.neighbor is not None:
            require(event.neighbor in graph.neighbors(event.vertex), f"arista inexistente en evento {event.seq}")
            require(event.edge == tuple(sorted((event.vertex, event.neighbor))), "identificador de arista inválido")
            expected_neighbor_tin = discovered.get(event.neighbor)
            require(event.neighbor_tin == expected_neighbor_tin, f"tin del vecino incorrecto en evento {event.seq}")
        else:
            require(event.edge is None, "evento sin vecino no debe declarar arista")
            require(event.neighbor_tin is None, "evento sin vecino no debe declarar tin del vecino")

        if event.type == "traverse_tree_edge":
            require(event.neighbor not in discovered, "arista de árbol hacia vértice ya descubierto")
            tree_parent[event.neighbor] = event.vertex
        elif event.type == "observe_back_edge":
            require(event.neighbor in discovered, "arista de retroceso hacia vértice no descubierto")
            require(discovered[event.neighbor] < discovered[event.vertex], "arista observada no va a ancestro")
        elif event.type == "skip_parent_edge":
            require(event.neighbor == tree_parent.get(event.vertex), "arista omitida no es la parental")
        elif event.type == "finish_vertex":
            require(event.vertex not in finished, "vértice finalizado más de una vez")
            finished.add(event.vertex)
        elif event.type == "identify_articulation":
            if event.reason == "low_child_ge_tin_vertex":
                require(event.neighbor is not None, "articulación no raíz sin hijo")
                require(event.candidate is not None, "articulación no raíz sin low del hijo")
                require(event.candidate >= discovered[event.vertex], "condición low[hijo] >= tin[vértice] falsa")
                require(tree_parent.get(event.vertex) is not None, "condición no raíz aplicada a raíz")
            elif event.reason == "root_has_multiple_dfs_children":
                require(tree_parent.get(event.vertex) is None, "condición de raíz aplicada a no raíz")
                require(event.candidate is not None and event.candidate > 1, "raíz no tiene más de un hijo")
            else:
                raise TraceValidationError(f"causa de articulación desconocida: {event.reason}")
            found_articulations.add(event.vertex)

    require(finished == set(graph.vertices), "la traza no finaliza todos los vértices")
    require(tuple((v, discovered[v]) for v in graph.vertices) == trace.tin, "tin final no coincide con la traza")
    require(tuple((v, lows[v]) for v in graph.vertices) == trace.low, "low final no coincide con la traza")
    require(found_articulations == set(trace.articulations), "articulaciones/eventos no coinciden")
    require(tuple(tree_parent.get(v) for v in graph.vertices) == tuple(p for _, p in trace.parent), "padres finales no coinciden")
    require(tuple(sorted(found_articulations)) == trace.articulations, "articulaciones finales no ordenadas")
