#!/usr/bin/env python3
"""[R383] Does a refused build leave a bitstream deploy.sh would pick by mtime?

Builds a disposable HERE with an older ACCEPTED build and a newer REFUSED build
(12-5201 in its log) and a newer build whose log is MISSING, runs the head's
real check_implementation_log on each, then evaluates deploy.sh's own BIT=/LAYOUT=
default lines (read from the file, not restated) and layout_from_soch's glob.
Usage: deploy_pick_probe.py <tree> <scratch dir>   (LiteX interpreter)"""
import os, re, shutil, subprocess, sys, time
from pathlib import Path
tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/litex"))
from clock_constraints import check_implementation_log
shutil.rmtree(work, ignore_errors=True)
def mk(name, log, layout):
    g = work / name / "gateware"; g.mkdir(parents=True)
    (g / "alinx_ax7101.bit").write_bytes(name.encode())
    if log is not None: (g / "vivado.log").write_text(log)
    if layout: (work / name / "flashboot_layout.json").write_text("{}")
    time.sleep(1.1)
    return g
results = {}
for name, log, layout in [("build_accepted_old", "INFO: ok\n", True),
                          ("build_refused_new", "CRITICAL WARNING: [Vivado 12-5201] planted\n", False),
                          ("build_nolog_newest", None, False)]:
    g = mk(name, log, layout)
    try:
        check_implementation_log(g / "vivado.log"); results[name] = "accepted"
    except (RuntimeError, OSError) as e:
        results[name] = f"refused ({type(e).__name__})"
    results[name] += f"; gateware now: {sorted(p.name for p in g.iterdir() if 'bit' in p.name)}"
for k, v in results.items(): print(f"{k}: {v}")
deploy = (tree / "sw/litex/deploy.sh").read_text().splitlines()
lines = [l for l in deploy if re.match(r'^(BIT|LAYOUT)="\$\{(BIT|LAYOUT):-\$\(ls -t', l)]
assert len(lines) == 2, lines
script = "set -e\nHERE=" + str(work) + "\nunset BIT LAYOUT\n" + "\n".join(lines) + '\necho "BIT=$BIT"\necho "LAYOUT=$LAYOUT"\n'
out = subprocess.run(["bash", "-c", script], capture_output=True, text=True, check=True).stdout
print("deploy.sh lines evaluated:"); [print("  " + l) for l in lines]
print(out.replace(str(work), "<HERE>"), end="")
for name in results:
    print(f"layout_from_soch glob {name}: {sorted(p.name for p in (work / name / 'gateware').glob('*.bit'))}")
assert "build_accepted_old" in out.split("BIT=")[1].splitlines()[0]
print("PASS: newest refused/unverifiable builds are not selected; the accepted build is")
shutil.rmtree(work)
