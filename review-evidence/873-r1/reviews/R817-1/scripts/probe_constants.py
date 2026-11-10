#!/usr/bin/env python3
"""Compare every upper-case module-level constant shared by the base and head runners.

Usage: python3 -I probe_constants.py <base act_ci.py> <head act_ci.py>

Prints shared constants whose values differ (none expected), the constants
only the base has (the replaced ones) and those only the head has (the new
geometry names), then PROBE: PASS when no shared constant differs.
"""
from __future__ import annotations

import importlib.util
import sys


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


base = load("act_ci_base", sys.argv[1])
head = load("act_ci_head", sys.argv[2])


def constants(module) -> dict[str, object]:
    return {name: getattr(module, name) for name in dir(module)
            if name.isupper() and not callable(getattr(module, name)) and not name.startswith("_")}


def comparable(name: str, value: object, module) -> object:
    """A context variable compares by its name and default; ROOT by its path relative to the clone."""
    import contextvars
    import pathlib
    if isinstance(value, contextvars.ContextVar):
        return ("ContextVar", value.name, repr(value.get()))
    if name == "ROOT" and isinstance(value, pathlib.Path):
        return ("ROOT", pathlib.Path(module.__file__).resolve().relative_to(value))
    return repr(value)


a, b = constants(base), constants(head)
differ = sorted(name for name in a.keys() & b.keys()
                if comparable(name, a[name], base) != comparable(name, b[name], head))
for name in differ:
    print(f"DIFFER {name}: base {a[name]!r} head {b[name]!r}")
print("only base:", {name: a[name] for name in sorted(a.keys() - b.keys())})
print("only head:", {name: b[name] for name in sorted(b.keys() - a.keys())})
print(f"shared constants compared: {len(a.keys() & b.keys())}")
print("PROBE: " + ("PASS" if not differ else f"FAIL ({len(differ)})"))
raise SystemExit(1 if differ else 0)
