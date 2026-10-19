#!/usr/bin/env python3
"""Check the merged mutant lists of a processor checkout against both merge parents.

Usage: check_mutant_union.py REPO MERGE PARENT1 PARENT2 BASE

A parent arm absent from the merge is accepted only when it is the merge base's
unchanged arm and the other parent changed that arm (a one-sided edit).

For tb/pp_top/acmp_mutants.py: every (name, suite) of either parent is in the
merge, and every planted edit's old text occurs exactly once in the merge's
source. For tb/srp_top/mutants.py: every arm of either parent is in the merge,
and every arm's patch file applies (`git apply --check`) to the merge's tree.
Reads git objects only; writes nothing in REPO.
"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def load(src, name):
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / f"{name}.py"
        f.write_text(src)
        spec = importlib.util.spec_from_file_location(name, f)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod


def main():
    repo, merge, p1, p2, base = sys.argv[1:6]
    bad = 0
    # ---- acmp_mutants.py
    mods = {r: load(show(repo, r, "tb/pp_top/acmp_mutants.py"), f"am_{i}")
            for i, r in enumerate((merge, p1, p2, base))}
    key = lambda m: (m.name, m.suite.directory, m.suite.run, m.edits, m.checks)
    merged = {key(m) for m in mods[merge].MUTANTS}
    for r in (p1, p2):
        for m in mods[r].MUTANTS:
            ok = key(m) in merged
            if not ok:
                other = p2 if r == p1 else p1
                ident = (m.name, m.suite.directory, m.suite.run)
                base_same = key(m) in {key(b) for b in mods[base].MUTANTS}
                other_v = [key(o) for o in mods[other].MUTANTS if key(o)[:3] == ident]
                if base_same and other_v and all(v in merged for v in other_v):
                    ok = True
                    print(f"acmp_mutants: {m.name}@{m.suite.directory}: {r[:8]} keeps the base arm, "
                          f"{other[:8]} edits it; the merge carries the edit (one-sided change)")
                else:
                    print(f"acmp_mutants: {m.name}@{m.suite.directory} of {r[:8]} MISSING or changed in merge")
            bad += not ok
    print(f"acmp_mutants: merge {len(mods[merge].MUTANTS)} arms; parents "
          f"{len(mods[p1].MUTANTS)} and {len(mods[p2].MUTANTS)}")
    extra = merged - {key(m) for r in (p1, p2) for m in mods[r].MUTANTS}
    print(f"acmp_mutants: arms in merge but in neither parent: {len(extra)}")
    bad += len(extra)
    for m in mods[merge].MUTANTS:
        for rel, old, _new in m.edits:
            n = show(repo, merge, rel).count(old)
            status = "OK" if n == 1 else "BAD"
            bad += n != 1
            print(f"anchor {status} {m.name}@{Path(m.suite.directory).name} {rel} count={n}")
    # ---- srp_top/mutants.py
    smods = {r: load(show(repo, r, "tb/srp_top/mutants.py").replace(
        "from mutant_pool import", "mutant_pool = None  # stub\n#"), f"sm_{i}")
        for i, r in enumerate((merge, p1, p2))}
    smerged = {tuple(m) for m in smods[merge].MUTANTS}
    for r in (p1, p2):
        for m in smods[r].MUTANTS:
            ok = tuple(m) in smerged
            bad += not ok
            if not ok:
                print(f"srp_top: {m[0]} of {r[:8]} MISSING or changed in merge")
    sextra = smerged - {tuple(m) for r in (p1, p2) for m in smods[r].MUTANTS}
    print(f"srp_top: merge {len(smods[merge].MUTANTS)} arms; parents "
          f"{len(smods[p1].MUTANTS)} and {len(smods[p2].MUTANTS)}; in neither parent: {len(sextra)}")
    bad += len(sextra)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(f"git -C {repo} archive {merge} | tar -x -C {tmp}", shell=True, check=True)
        subprocess.run(["git", "init", "-q", tmp], check=True)
        for m in smods[merge].MUTANTS:
            patch = Path(tmp) / "tb/srp_top/mutations" / f"{m[0]}.patch"
            rc = subprocess.run(["git", "apply", "--check", str(patch)], cwd=tmp,
                                capture_output=True).returncode if patch.exists() else -1
            bad += rc != 0
            print(f"patch {'OK' if rc == 0 else 'BAD'} {m[0]} rc={rc}")
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'} ({bad} problems)")
    return int(bad != 0)


if __name__ == "__main__":
    raise SystemExit(main())
