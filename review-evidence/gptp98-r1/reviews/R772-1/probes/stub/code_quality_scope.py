"""Stub of the parent's scope module: the probe passes paths explicitly."""
PROJECT_SUBMODULES: tuple[str, ...] = ()


def tracked(pattern: str) -> list[str]:
    """No enumeration here; the probe names every file."""
    return []
