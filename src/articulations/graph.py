"""Representación inmutable de un grafo simple, no dirigido y determinista."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Graph:
    """Grafo simple con vértices etiquetados por cadenas.

    Los vecinos se exponen en orden lexicográfico para que DFS y sus trazas sean
    reproducibles. Las aristas paralelas y los lazos se rechazan explícitamente.
    """

    vertices: tuple[str, ...]
    adjacency: Mapping[str, tuple[str, ...]]

    @classmethod
    def from_edges(
        cls,
        edges: Iterable[tuple[str, str]],
        *,
        vertices: Iterable[str] = (),
    ) -> Graph:
        vertex_set = set(vertices)
        normalized_edges: set[tuple[str, str]] = set()

        for edge in edges:
            try:
                left, right = edge
            except (TypeError, ValueError) as exc:
                raise ValueError("cada arista debe tener exactamente dos extremos") from exc
            if not isinstance(left, str) or not isinstance(right, str):
                raise TypeError("las etiquetas de vértice deben ser cadenas")
            if left == right:
                raise ValueError("los lazos no están admitidos en grafos simples")
            vertex_set.update((left, right))
            normalized = tuple(sorted((left, right)))
            if normalized in normalized_edges:
                raise ValueError(f"arista paralela duplicada: {normalized}")
            normalized_edges.add(normalized)

        if any(not isinstance(vertex, str) for vertex in vertex_set):
            raise TypeError("las etiquetas de vértice deben ser cadenas")

        ordered_vertices = tuple(sorted(vertex_set))
        neighbors = {vertex: set() for vertex in ordered_vertices}
        for left, right in normalized_edges:
            neighbors[left].add(right)
            neighbors[right].add(left)
        adjacency = MappingProxyType(
            {vertex: tuple(sorted(neighbors[vertex])) for vertex in ordered_vertices}
        )
        return cls(ordered_vertices, adjacency)

    def neighbors(self, vertex: str) -> tuple[str, ...]:
        """Devuelve los vecinos ordenados o genera KeyError si no existe el vértice."""
        return self.adjacency[vertex]

    @property
    def edges(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            (vertex, neighbor)
            for vertex in self.vertices
            for neighbor in self.neighbors(vertex)
            if vertex < neighbor
        )
