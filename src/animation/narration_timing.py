"""Cálculo puro de la espera entre señales consecutivas de narración."""

def remaining_voice_time(now: float, voice_end: float) -> float:
    """Evita solapar señales sin detener animaciones mientras suena una voz."""
    return max(0.0, voice_end - now)


def narration_enabled() -> bool:
    """Read the render mode at runtime so one scene serves narrated and silent exports."""
    import os
    return os.environ.get("AED_NARRATION", "1") != "0"
