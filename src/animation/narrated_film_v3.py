"""Entry point for the shared narrated/silent v3 film."""
from animation.film_v3 import ArticulationFilmV3

class NarratedFilm(ArticulationFilmV3):
    """Same scenes as the silent render; AED_NARRATION selects audio cues."""
    pass
