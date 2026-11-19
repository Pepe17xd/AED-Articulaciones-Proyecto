from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class NarratedFilmTests(unittest.TestCase):
    def test_cue_wait_is_only_the_unplayed_voice_tail(self):
        import sys
        sys.path.insert(0, str(ROOT / 'src'))
        from animation.narration_timing import remaining_voice_time
        self.assertEqual(remaining_voice_time(4.0, 6.5), 2.5)
        self.assertEqual(remaining_voice_time(7.0, 6.5), 0.0)

    def test_low_propagates_from_d_to_c(self):
        import sys
        sys.path.insert(0, str(ROOT / 'src'))
        from articulations import Graph, run_tarjan, validate_trace
        graph = Graph.from_edges([('A','B'), ('A','G'), ('B','C'), ('C','D'), ('D','B'), ('D','E'), ('E','F')])
        trace = run_tarjan(graph)
        validate_trace(graph, trace)
        self.assertTrue(any(e.type == 'update_low' and e.vertex == 'C' and e.neighbor == 'D' and e.low_value == 1 for e in trace.events))
        self.assertEqual(dict(trace.low)['C'], dict(trace.tin)['B'])

    def test_triangle_root_has_two_neighbors_but_one_dfs_child(self):
        import sys
        sys.path.insert(0, str(ROOT / 'src'))
        from articulations import Graph, run_tarjan, validate_trace
        graph = Graph.from_edges([('A','B'), ('B','C'), ('A','C')])
        trace = run_tarjan(graph)
        validate_trace(graph, trace)
        self.assertEqual(len(graph.neighbors('A')), 2)
        self.assertEqual(sum(e.type == 'traverse_tree_edge' and e.vertex == 'A' for e in trace.events), 1)
        self.assertNotIn('A', trace.articulations)

if __name__ == '__main__':
    unittest.main()
