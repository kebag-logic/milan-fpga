#!/usr/bin/env python3
"""Compare the ACMP and MAAP plant tables of dev and the head: same names, and every field equal except a path
that moves from the ctrl tree's core copy to the stack's (ctrl_build.LEGACY's mapping).
usage: tables_compare.py <dev tree> <head tree>"""
import importlib, sys
from pathlib import Path
from collections import namedtuple

LEG = {"adp/adp.c": "tsn-c-stack/src/adp.c", "acmp/acmp.c": "tsn-c-stack/src/acmp.c",
       "maap/maap.c": "tsn-c-stack/src/maap.c", "adp/adp.h": "tsn-c-stack/include/adp.h",
       "acmp/acmp.h": "tsn-c-stack/include/acmp.h", "maap/maap.h": "tsn-c-stack/include/maap.h",
       "wire/wire.h": "tsn-c-stack/include/wire.h"}

def load(tree, name):
    t = Path(tree) / "sw/firmware/ctrl/test"
    sys.path[:0] = [str(t), str(Path(tree) / "sw/firmware/gtest")]
    for m in [m for m in list(sys.modules) if m.startswith(("ctrl_", "fw_", "acmp_", "maap_"))]:
        del sys.modules[m]
    mod = importlib.import_module(name)
    sys.path[:] = [p for p in sys.path if not p.startswith(str(tree))]
    if hasattr(mod, "MUTANTS"):
        return mod.MUTANTS
    Kind = namedtuple("Kind", "name path old new arm test needle also", defaults=((),))
    def kind(*a, **k):
        return (a, tuple(sorted(k.items())))
    return mod.mutants(kind)

def key(m):
    if isinstance(m, tuple):
        return m[0][0], m
    return m.name, m

def norm(m, head):
    if isinstance(m, tuple):
        args = tuple(LEG.get(x, x) if isinstance(x, str) and not head else x for x in m[0])
        return (args, m[1])
    d = dict(m.__dict__)
    if not head:
        d["path"] = LEG.get(d["path"], d["path"])
    return d

bad = 0
for table in ("ctrl_mutants", "acmp_mutants", "acmp_review_mutants", "maap_mutants"):
    dv = dict(key(m) for m in load(sys.argv[1], table))
    hd = dict(key(m) for m in load(sys.argv[2], table))
    missing = sorted(set(dv) - set(hd)); extra = sorted(set(hd) - set(dv))
    changed = sorted(n for n in set(dv) & set(hd) if norm(dv[n], False) != norm(hd[n], True))
    print(f"{table}: dev {len(dv)} head {len(hd)} missing {missing} extra {extra} changed-beyond-path {changed}")
    bad += len(missing) + len(changed)
sys.exit(1 if bad else 0)
