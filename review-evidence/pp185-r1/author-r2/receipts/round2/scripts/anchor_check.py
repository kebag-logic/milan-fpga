"""Check every campaign's planted edits against a tree: patches with git apply
--check, and (path, old, new) string tuples in the Python drivers by count."""
import importlib.util, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
bad = 0
for d in ("tb/pp_top/mutations", "tb/pp_top/aecp_dispatch_mutations", "tb/pp_top/ctr_mutations"):
    for p in sorted((root / d).glob("*.patch")):
        r = subprocess.run(["git", "-C", str(root), "apply", "--check", str(p)],
                           capture_output=True, text=True)
        if r.returncode:
            bad += 1
            print("PATCH FAIL", p.relative_to(root), r.stderr.strip().splitlines()[:2])

drivers = ["tb/pp_top/notify_mutants.py", "tb/pp_top/acmp_mutants.py", "tb/pp_top/d3_mutants.py",
           "tb/pp_top/gsi_mutants.py", "tb/pp_top/name_wr_mutant.py", "tb/pp_top/ctr_mutants.py",
           "tb/pp_top/aecp_mutants.py", "tb/pp_top/aecp_dispatch_mutants.py",
           "tb/aecp_cmds/mutants.py", "tb/elab_guards/mutants.py", "tb/name_state/mutants.py",
           "tb/adp_engine/mutants.py", "tb/maap/mutants.py", "tb/srp_top/mutants.py",
           "tb/srp_admission/mutants.py", "tb/acmp_talker/retry_mutants.py"]
seen = 0
def walk(obj, depth=0):
    global seen, bad
    if depth > 8:
        return
    if isinstance(obj, tuple) and len(obj) >= 3 and all(isinstance(x, str) for x in obj[:3]):
        path, old = obj[0], obj[1]
        f = root / path
        if "/" in path and f.is_file() and old:
            seen += 1
            n = f.read_text(encoding="utf-8", errors="replace").count(old)
            if n != 1:
                bad += 1
                print(f"EDIT count {n}: {path}: {old.strip().splitlines()[0][:90]!r}")
            return
    if isinstance(obj, (list, tuple, set)):
        for x in obj:
            walk(x, depth + 1)
    elif isinstance(obj, dict):
        for x in obj.values():
            walk(x, depth + 1)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        for x in obj:
            walk(x, depth + 1)

for drv in drivers:
    p = root / drv
    if not p.exists():
        continue
    sys.path[:0] = [str(p.parent), str(root / "tb" / "common")]
    spec = importlib.util.spec_from_file_location("m_" + p.stem, p)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    except Exception as e:
        print("IMPORT", drv, type(e).__name__, e)
        continue
    for k, v in vars(m).items():
        if not k.startswith("__"):
            walk(v)
print(f"edits checked: {seen}; failures: {bad}")
