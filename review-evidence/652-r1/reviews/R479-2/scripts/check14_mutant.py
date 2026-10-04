#!/usr/bin/env python3
"""Run check 14's allocation-table negative controls with a defect planted IN
MEMORY in scripts/nvm_allocation_table.py (the tree is never written).

check_nvm_record_space.py --self-test re-runs itself as a subprocess per
control, so a parent-side preload would not reach them. This driver instead
runs each allocation control (and the unmutated real check) in its own child
process that loads the mutated module first, then calls the gate's main().
A control is red when it exits 1 with the gate's own required FINDING text and
no traceback, exactly the self-test's rule.

Usage: check14_mutant.py <tree> OLD NEW [OLD2 NEW2]
Exit 1 when any control fails to redden or the real check is not clean (the
self-test would be red), else 0."""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

CONTROLS = ("short_allocation_row", "long_allocation_row", "stale_allocation_table")


def child(tree: Path, pairs: list[tuple[str, str]], control: str) -> int:
    scripts = tree / "scripts"
    sys.path.insert(0, str(scripts))
    path = scripts / "nvm_allocation_table.py"
    source = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if source.count(old) != 1:
            sys.exit(f"anchor occurs {source.count(old)} times: {old!r}")
        source = source.replace(old, new)
    spec = importlib.util.spec_from_file_location("nvm_allocation_table", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["nvm_allocation_table"] = module
    exec(compile(source, str(path), "exec"), module.__dict__)
    import check_nvm_record_space as gate
    sys.argv = [str(scripts / "check_nvm_record_space.py"), "--quiet"] + (
        [f"--mutate={control}"] if control != "real" else [])
    return gate.main()


def parent(tree: Path, args: list[str]) -> int:
    sys.path.insert(0, str(tree / "scripts"))
    import check_nvm_record_space as gate  # unmutated, only to read the required texts
    red = True
    for control in (*CONTROLS, "real"):
        env = dict(os.environ, C14_CONTROL=control)
        r = subprocess.run([sys.executable, __file__, str(tree), *args], cwd=tree, env=env,
                           capture_output=True, text=True)
        text = r.stdout + r.stderr
        if "anchor occurs" in text:
            print(text)
            return 2
        crashed = "Traceback (most recent call last):" in text
        if control == "real":
            ok = r.returncode == 0 and not crashed
            print(f"real check: rc={r.returncode} traceback={crashed} -> {'clean' if ok else 'NOT CLEAN'}")
        else:
            required = gate.MUTATIONS[control][1]
            finding = next((ln for ln in r.stdout.splitlines()
                            if ln.startswith("FINDING:") and required in ln), None)
            ok = r.returncode == 1 and finding is not None and not crashed
            print(f"control {control}: rc={r.returncode} traceback={crashed} finding={finding!r} -> "
                  f"{'reddens' if ok else 'SELF-TEST FAILED (control did not redden as required)'}")
        if not ok:
            for line in text.splitlines()[-4:]:
                print(f"    | {line}")
        red = red and ok
    return 0 if red else 1


if __name__ == "__main__":
    tree = Path(sys.argv[1]).resolve()
    rest = sys.argv[2:]
    if os.environ.get("C14_CONTROL"):
        pairs = list(zip(rest[0::2], rest[1::2]))
        sys.exit(child(tree, pairs, os.environ["C14_CONTROL"]))
    sys.exit(parent(tree, rest))
