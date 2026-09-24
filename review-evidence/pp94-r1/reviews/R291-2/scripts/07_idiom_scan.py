#!/usr/bin/env python3
"""Scan only this PR's new/changed bench files with the parent's Rule 11/12 scanners.

The scanners are the parent dev 9d328810 copies (scripts/check_cpp_idiom.py and
scripts/check_py_idiom.py), imported as modules; only their per-file scan()
functions and cflags_missing() are used, so no parent tree or ratchet is read.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

PKT = Path("$REVIEWS/pp94-r291-2-packet")
SRC = Path("$REVIEWS/r291-2-pp94")
BASE, HEAD = "008edbbf486598ae237414273d75e385cf0e1a56", "cc077a6ffe20585d20b116f008e07189ba1bb7f8"


def load(name: str):
    """Import one parent checker by file path (its sibling helper module on sys.path)."""
    sys.path.insert(0, str(PKT / "scratch/parent"))
    spec = importlib.util.spec_from_file_location(name, PKT / "scratch/parent" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blob(rev: str, rel: str) -> str | None:
    """File text at a revision, or None when absent."""
    res = subprocess.run(["git", "-C", str(SRC), "show", f"{rev}:{rel}"], capture_output=True, text=True)
    return res.stdout if res.returncode == 0 else None


def main() -> int:
    """Print base/head non-zero counts per file; return 1 if head adds any finding."""
    cpp, py = load("check_cpp_idiom"), load("check_py_idiom")
    worse = 0
    for rel in ("tb/desc_mem_guard/sim_main.cpp", "tb/pp_top/sim_main.cpp"):
        for rev in (BASE, HEAD):
            text = blob(rev, rel)
            counts = cpp.scan(text, rel) if text is not None else None
            nz = {k: v for k, v in (counts or {}).items() if v}
            print(f"{rel} @{rev[:8]}: {'absent' if counts is None else nz or 'zero findings'}")
        b, h = blob(BASE, rel), blob(HEAD, rel)
        bc = cpp.scan(b, rel) if b else {}
        hc = cpp.scan(h, rel)
        for key, val in hc.items():
            if val > bc.get(key, 0):
                worse += 1
                print(f"  ROSE {key}: {bc.get(key, 0)} -> {val}")
                for line, snip in cpp.sites(h, key, rel):
                    print(f"    {rel}:{line}: {snip}")
    mk = blob(HEAD, "tb/desc_mem_guard/Makefile")
    print(f"tb/desc_mem_guard/Makefile cflags_missing: {cpp.cflags_missing(mk)}")
    text = blob(HEAD, "tb/desc_mem_guard/mutate.py")
    counts, sites = py.scan(text, "tb/desc_mem_guard/mutate.py")
    nz = {k: v for k, v in counts.items() if v}
    print(f"tb/desc_mem_guard/mutate.py @{HEAD[:8]}: {nz or 'zero findings'}")
    worse += sum(nz.values())
    # Positive control: the round-1a bench (4f525eb) must reproduce the reported debt.
    r1a = "4f525eb55b310d6b9bc2f1a000254cb2dd483665"
    ctl = {k: v for k, v in cpp.scan(blob(r1a, "tb/desc_mem_guard/sim_main.cpp"), "tb/desc_mem_guard/sim_main.cpp").items() if v}
    pyc, _ = py.scan(blob(r1a, "tb/desc_mem_guard/mutate.py"), "tb/desc_mem_guard/mutate.py")
    print(f"CONTROL round-1a bench @{r1a[:8]}: cpp {ctl}; py { {k: v for k, v in pyc.items() if v} }")
    print(f"added findings: {worse}")
    return 1 if worse else 0


if __name__ == "__main__":
    sys.exit(main())
