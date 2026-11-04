"""Tipos de datos de solo lectura para registrar ejecuciones de Tarjan."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

EventType = Literal[
    "discover_vertex",
    "examine_edge",
    "skip_parent_edge",
    "traverse_tree_edge",
    "observe_back_edge",
    "skip_seen_edge",
    "update_low",
    "finish_vertex",
    "return_to_parent",
    "identify_articulation",
]

@dataclass(frozen=True, slots=True)
class Event:
    """Un hecho algorítmico con datos suficientes para una representación visual."""

    seq: int
    type: EventType
    vertex: str
    neighbor: str | None
    edge: tuple[str, str] | None
    parent: str | None
    candidate: int | None
    reason: str | None
    tin_value: int
    low_value: int
    neighbor_tin: int | None


@dataclass(frozen=True, slots=True)
class Trace:
    """Resultado de una ejecución y todos sus eventos, en orden de emisión."""

    vertices: tuple[str, ...]
    events: tuple[Event, ...]
    tin: tuple[tuple[str, int], ...]
    low: tuple[tuple[str, int], ...]
    parent: tuple[tuple[str, str | None], ...]
    articulations: tuple[str, ...]
    components: tuple[tuple[str, ...], ...]
