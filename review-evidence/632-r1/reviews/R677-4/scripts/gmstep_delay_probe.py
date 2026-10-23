#!/usr/bin/env python3
"""Falsification probe for the gmstep control "the grandmaster change stops the
talker for good": plant it alone through the campaign's own plant and build,
then run the clean and the planted leg at a non-default feed delay, so the
control is shown not to depend on the default boot timing.

Usage: gmstep_delay_probe.py <tree> <out dir> <feed delay> [control name]
Writes clean.log, planted.log and verdict.txt into <out dir>.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path


def main() -> int:
    tree, out, delay = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    name = sys.argv[4] if len(sys.argv) > 4 else "the grandmaster change stops the talker for good"
    out.mkdir(parents=True, exist_ok=True)
    path = tree / "tb/verilator/milan_dp_gm_steps/gmstep_mutants.py"
    spec = importlib.util.spec_from_file_location("gmstep_mutants", path)
    gm = importlib.util.module_from_spec(spec)
    sys.modules["gmstep_mutants"] = gm
    spec.loader.exec_module(gm)
    control = next(c for c in gm.CONTROLS if c.name == name)
    leg = gm.LEGS[control.leg]
    work = out / "work"
    work.mkdir(exist_ok=True)
    sources = {k: p.resolve() for k, p in gm.SOURCES.items()}
    lines = []

    def run(exe: Path, tag: str) -> tuple[int, str]:
        cmd = [str(exe), str(exe.parent / "aemi.bin"), delay]
        r = subprocess.run(cmd, cwd=str(gm.DP), capture_output=True, text=True, check=False)
        text = r.stdout + r.stderr
        (out / f"{tag}.log").write_text(text)
        return r.returncode, text

    clean = gm.build(leg, sources, work / "obj_clean")
    if clean is None:
        lines.append("clean build FAILED")
    else:
        rc, text = run(clean, "clean")
        lines.append(f"clean feed-delay {delay}: rc {rc}, verdict {gm.verdict(rc, text, None)}, "
                     f"failed {gm.failed_checks(text)}")
        lines += [l for l in text.splitlines() if l.startswith("GMDET:") or "boot grandmaster" in l]
    base = gm.SOURCES[control.source].resolve()
    text = base.read_text()
    lines.append(f"anchor count {text.count(control.anchor)}")
    planted = work / f"planted_{base.name}"
    planted.write_text(text.replace(control.anchor, control.replacement))
    psources = dict(sources)
    psources[control.source] = planted
    exe = gm.build(leg, psources, work / "obj_planted")
    if exe is None:
        lines.append("planted build FAILED")
    else:
        rc, ptext = run(exe, "planted")
        lines.append(f"planted feed-delay {delay}: rc {rc}, verdict {gm.verdict(rc, ptext, control.breaks)}")
        lines.append(f"named check {control.breaks!r}")
        lines.append(f"failed checks: {gm.failed_checks(ptext)}")
        lines += [l for l in ptext.splitlines() if l.startswith("GMDET:") or "baseline: the talker streams" in l]
    (out / "verdict.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
