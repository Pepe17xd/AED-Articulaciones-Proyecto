"""Registro incremental de eventos independiente del recorrido DFS."""

from __future__ import annotations

from .trace import Event


class EventRecorder:
    """Asigna secuencias y captura solo valores locales por evento.

    Los consumidores reconstruyen el estado aplicando los eventos en orden; así
    el tamaño de la traza permanece O(V + E), sin snapshots completos repetidos.
    """

    def __init__(self, vertices: tuple[str, ...]) -> None:
        self._vertices = vertices
        self._events: list[Event] = []

    def record(
        self,
        event_type: str,
        vertex: str,
        neighbor: str | None,
        *,
        parent: str | None,
        tin: dict[str, int],
        low: dict[str, int],
        candidate: int | None = None,
        reason: str | None = None,
    ) -> None:
        edge = tuple(sorted((vertex, neighbor))) if neighbor is not None else None
        self._events.append(
            Event(
                seq=len(self._events),
                type=event_type,  # type: ignore[arg-type]
                vertex=vertex,
                neighbor=neighbor,
                edge=edge,
                parent=parent,
                candidate=candidate,
                reason=reason,
                tin_value=tin[vertex],
                low_value=low[vertex],
                neighbor_tin=tin.get(neighbor) if neighbor is not None else None,
            )
        )

    @property
    def events(self) -> tuple[Event, ...]:
        return tuple(self._events)
