#!/usr/bin/env python3
"""For every served command, move its response cdl (then its command cdl) by +4
in the table, regenerate F06.14, and record whether the AECP command gate fails.
Usage: python3 -I size_sweep.py HEAD_TREE WORK_DIR. Prints one line per probe;
a probe the gate PASSES is a size the gate holds to nothing but the table."""
import json, shutil, subprocess, sys
from pathlib import Path
TABLE = "hdl/aecp/ucode/aecp_commands.json"
GATE = "scripts/check_aecp_commands.py"
tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
names = [c["name"] for c in json.loads((tree / TABLE).read_text())["commands"]]
held = {"response": [], "command": []}
free = {"response": [], "command": []}
for side in ("response", "command"):
    for n in names:
        d = work / f"{side}-{n}"
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(tree, d)
        t = json.loads((d / TABLE).read_text())
        c = next(c for c in t["commands"] if c["name"] == n)
        c[side]["cdl"] += 4
        (d / TABLE).write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
        w = subprocess.run([sys.executable, "-B", GATE, "--write"], cwd=d, capture_output=True, text=True)
        r = subprocess.run([sys.executable, "-B", GATE], cwd=d, capture_output=True, text=True)
        first = next((l.strip() for l in r.stdout.splitlines() if l.startswith("  ")), "")
        echo = " echo" if c["response"].get("echo") else ""
        print(f"{side:8} {n:38} write rc {w.returncode} gate rc {r.returncode}{echo:5} {first[:150]}")
        (held if r.returncode else free)[side].append(n)
        shutil.rmtree(d)
for side in ("response", "command"):
    print(f"{side}: {len(held[side])} held by a consumer, {len(free[side])} held to the table alone: {free[side]}")
