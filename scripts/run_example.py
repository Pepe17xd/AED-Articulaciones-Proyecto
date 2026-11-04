"""Run Tarjan on the graph used to illustrate the project."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from articulations import Graph, run_tarjan  # noqa: E402


def main() -> None:
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
    print(f"Articulaciones: {trace.articulations}")
    print(f"tin: {dict(trace.tin)}")
    print(f"low: {dict(trace.low)}")


if __name__ == "__main__":
    main()
