#!/usr/bin/env python3
"""Round 7b probe: the gmstep control 'the grandmaster change stops the talker
for good' failed at d835ba12 'but not the named check'. Plant that one
control exactly as gmstep_mutants.run_control does (a disposable source copy,
the driver's own build and run), then print the leg's verdict, every check it
printed as failed, and every licence / talker line, so the STOP names what the
mutant breaks. Run with the repository's tb/verilator/milan_dp_gm_steps as cwd.
usage: gm_stop_probe.py <out dir> [control name]
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
import gmstep_mutants as g  # noqa: E402

out_dir = Path(sys.argv[1]); out_dir.mkdir(parents=True, exist_ok=True)
name = sys.argv[2] if len(sys.argv) > 2 else "the grandmaster change stops the talker for good"
control = next(c for c in g.CONTROLS if c.name == name)
base = g.SOURCES[control.source].resolve()
text = base.read_text()
print("anchor count", text.count(control.anchor))
with tempfile.TemporaryDirectory(prefix="gmstop-probe-") as td:
    work = Path(td)
    planted = work / f"c_{base.name}"
    planted.write_text(text.replace(control.anchor, control.replacement))
    sources = {key: path.resolve() for key, path in g.SOURCES.items()}
    sources[control.source] = planted
    leg = g.LEGS[control.leg]
    exe = g.build(leg, sources, work / "obj_c")
    print("built", exe is not None)
    rc, out = g.run_leg(leg, exe, False)
(out_dir / "leg.log").write_text(out)
print("rc", rc)
print("verdict", g.verdict(rc, out, control.breaks))
print("named check", repr(control.breaks))
broke = g.failed_checks(out)
print(f"failed checks ({len(broke)}):")
for b in broke:
    print("   ", b)
print("lines naming the licence or the talker's pauses:")
for line in out.splitlines():
    if "licence" in line or "pause" in line:
        print("   ", line.strip()[:300])
