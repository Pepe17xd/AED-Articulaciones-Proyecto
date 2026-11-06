"""Create a production scene from the existing event-driven film and cue map."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "src/animation/articulation_film.py").read_text(encoding="utf-8")
source = source.replace("class ArticulationFilm(Scene):", "class NarratedArticulationFilm(Scene):")
# Holds are driven by the measured narration rather than fixed legacy pauses.
source = re.sub(r"self\.wait\([0-9.]+\)", "self.wait(0.3)", source)
marker = "    def header(self, title: str, subtitle: str | None = None) -> VGroup:"
method = '''    def narrate(self, cue: str) -> None:
        import av
        path = ROOT / "assets" / "audio" / "narration" / (cue + ".mp3")
        with av.open(str(path)) as audio:
            duration = audio.duration / 1_000_000
        self.add_sound(str(path))
        self.wait(duration + 0.3)

'''
source = source.replace(marker, method + marker)

def after(needle: str, cue: str, occurrence: int = 1) -> None:
    global source
    matches = list(re.finditer(re.escape(needle), source))
    if len(matches) < occurrence:
        raise RuntimeError(f"No se encontró la señal {cue}: {needle}")
    match = matches[occurrence - 1]
    line_start = source.rfind("\n", 0, match.end()) + 1
    indent = re.match(r"[ \t]*", source[line_start:match.end()]).group()
    end = match.end()
    source = source[:end] + f'\n{indent}self.narrate("{cue}")' + source[end:]

after('self.play(*(edge.animate.set_color(BLUE_C).set_stroke(width=5) for edge in edges.values()), run_time=0.7)', '01_red')
after('self.play(nodes["E"].animate.set_fill(GOLD, opacity=0.3), nodes["N"].animate.set_fill(GOLD, opacity=0.3), run_time=0.35)', '02_falla')
after('self.play(FadeIn(definition, shift=0.2 * UP), run_time=0.8)', '03_definicion')
after('self.play(cycle_edges[("A", "C")].animate.set_color(GREEN_C).set_stroke(width=5), run_time=0.55)', '04_ciclo')
after('footer = self.caption("Quitar B no desconecta el ciclo; quitar Q separa P de R.", size=19, y=-3.1)', '05_camino')
after('caption = self.caption("DFS explora tan lejos como puede y luego vuelve por el árbol.", size=20)', '06_dfs')
after('caption = self.change_caption(caption, "D encuentra una arista de retorno hacia el ancestro B.")', '07_retorno')
after('caption = self.change_caption(caption, "low[D] retrocede hasta tin[B] gracias a esa alternativa.")', '08_low')
after('caption = self.change_caption(caption, "La igualdad también cuenta: B no tiene una salida desde el subárbol de C.", size=18)', '09_igualdad')
after('caption = self.caption("Orden determinista: vecinos en orden alfabético.", size=19)', '10_recorrido')
after('caption = self.change_caption(caption, f"Descubrimos {event.vertex}: tin = low = {event.tin_value}", size=20)', '10a_descubre')
# Only the first discovery is A; later events must not replay this cue.
source = source.replace('                self.narrate("10a_descubre")', '                if event.vertex == "A":\n                    self.narrate("10a_descubre")')
needle = '                self.wait(0.3)\n            elif event.type == "update_low":'
if source.count(needle) != 1:
    raise RuntimeError("No se encontró el retorno de la ejecución")
source = source.replace(needle, '                if event.vertex == "D":\n                    self.narrate("10b_retorno")\n' + needle)
needle = '                self.play(FadeOut(ring), run_time=0.18)'
if source.count(needle) != 1:
    raise RuntimeError("No se encontró la articulación de la ejecución")
source = source.replace(needle, '                if event.vertex == "E":\n                    self.narrate("10c_articulacion")\n                elif event.vertex == "A":\n                    self.narrate("10d_raiz")\n' + needle)
needle = '            "La ejecución termina: A, B, D y E cumplen la condición de articulación.",\n            color=GOLD,\n            size=20,\n        )'
after(needle, '11_resultado')
after('self.play(one_nodes["A"].animate.set_fill(GREEN_C, opacity=0.25), FadeIn(note1), run_time=0.6)', '12_raiz_uno')
after('self.play(two_nodes["R"].animate.set_fill(GOLD, opacity=0.45), FadeIn(note2), run_time=0.6)', '13_raiz_dos')
after('caption = self.change_caption(caption, "Las listas de adyacencia permiten recorrer el grafo en tiempo lineal.", size=19)', '14_complejidad')
after('self.play(FadeIn(takeaway), run_time=0.5)', '15_conclusion')
(ROOT / "src/animation/narrated_articulation_film.py").write_text(source, encoding="utf-8")
