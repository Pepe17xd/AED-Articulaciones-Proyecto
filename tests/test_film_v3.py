from __future__ import annotations
import json, re, sys, unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class FilmV3Tests(unittest.TestCase):
 def test_editorial_script_keeps_all_math_and_fits_word_target(self):
  cues=json.loads((ROOT/'narration/cues.json').read_text(encoding='utf-8'))
  script=' '.join(item['text'] for item in cues)
  words=len(script.split())
  self.assertGreaterEqual(words, 650)
  self.assertLessEqual(words, 720)
  for phrase in ['tin', 'low', 'arista de retorno', 'low[F] = 5', 'tin[E] = 4', 'hijo DFS', 'O(V + E)']:
   self.assertIn(phrase, script)
 def test_v3_scene_has_all_cues_once(self):
  cues=json.loads((ROOT/'narration/cues.json').read_text(encoding='utf-8'))
  source=(ROOT/'src/animation/film_v3.py').read_text(encoding='utf-8')
  used=re.findall(r'self\.narrate\("([^\"]+)"\)',source)
  expected=[x['id'] for x in cues]
  self.assertEqual(Counter(used), Counter(expected))
  self.assertEqual(used, expected, 'La narración debe seguir el orden del guion y sus escenas.')
 def test_narration_is_runtime_switch_not_generated_copy(self):
  source=(ROOT/'src/animation/film_v3.py').read_text(encoding='utf-8')
  self.assertIn('narration_enabled()',source)
  self.assertTrue((ROOT/'src/animation/narrated_film_v3.py').exists())
  self.assertFalse((ROOT/'scripts/prepare_narrated_v3.py').exists())
  self.assertIn('from animation.film_v3 import ArticulationFilmV3', (ROOT/'src/animation/narrated_film_v3.py').read_text(encoding='utf-8'))
 def test_event_driven_disconnect_comparisons_and_tree_back_edges(self):
  source=(ROOT/'src/animation/film_v3.py').read_text(encoding='utf-8')
  for token in ['low[{event.neighbor}] = {event.candidate}', 'low_child_ge_tin_vertex', 'observe_back_edge', 'set_opacity(0.08)']:
   self.assertIn(token,source)
 def test_root_explanation_compares_graph_neighbors_with_dfs_children(self):
  source=(ROOT/'src/animation/film_v3.py').read_text(encoding='utf-8')
  self.assertIn('one_neighbors = len(one_graph.adjacency["A"])', source)
  self.assertIn('vecinos = {one_neighbors} · hijos DFS = {one_root_children}', source)
  self.assertIn('vecinos = 2 · hijos DFS = {root_children}', source)
  self.assertIn('two_edges[event.edge].animate.set_color(BLUE_C)', source)
if __name__=='__main__': unittest.main()
