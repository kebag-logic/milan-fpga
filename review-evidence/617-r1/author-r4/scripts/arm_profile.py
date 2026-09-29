#!/usr/bin/env python3
"""Profile the committed capture_coherence mutation arm item by item: for every leg's
clean control and every mutant, the build's wall time and largest-process RSS
(GNU time around the suite's own make recipe) and the harness run's wall time, one
at a time, using the suite's own mutants.py (LEGS, MUTATIONS, mutate, verdict).

  python3 arm_profile.py <suite-dir> <workdir> <out.tsv>
"""
import importlib.util
import subprocess
import sys
import time
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
sys.argv = [str(suite / "mutants.py")]
spec.loader.exec_module(m)
work.mkdir(parents=True, exist_ok=True)


def build(leg, rtl_path, tag):
    s, target, src_var, mdir_var, _, exe_name, _ = m.LEGS[leg]
    mdir = work / f"obj_{tag}"
    tfile = work / f"time_{tag}.txt"
    t0 = time.monotonic()
    r = subprocess.run(["/usr/bin/time", "-f", "%e %M", "-o", str(tfile), "make", "-s", "-C", str(s), target,
                        f"{src_var}={rtl_path}", f"{mdir_var}={mdir}"], capture_output=True, text=True, check=False)
    wall = time.monotonic() - t0
    rss = tfile.read_text().split()[-1] if tfile.exists() else "?"
    exe = mdir / exe_name
    return (exe if r.returncode == 0 and exe.is_file() else None), wall, rss


rows = []
items = [("control", leg, None, None, None) for leg in m.LEGS]
items += [("mutant", leg, name, edits, breaks) for leg, name, edits, breaks in m.MUTATIONS]
with out.open("w") as f:
    f.write("kind\tleg\tname\tbuild_s\tbuild_maxrss_kb\trun_s\tverdict\n")
    for i, (kind, leg, name, edits, breaks) in enumerate(items):
        rtl = m.LEGS[leg][4]
        src = rtl.read_text()
        if kind == "mutant":
            src = m.mutate(src, edits)
        tag = f"{i:02d}_{kind}_{leg}"
        p = work / tag / rtl.name
        p.parent.mkdir()
        p.write_text(src)
        exe, bwall, rss = build(leg, p, tag)
        if exe is None:
            f.write(f"{kind}\t{leg}\t{name or ''}\t{bwall:.1f}\t{rss}\t-\tdid not compile\n")
            f.flush()
            continue
        t0 = time.monotonic()
        rc, text = m.run_harness(leg, exe)
        rwall = time.monotonic() - t0
        ans = m.verdict(rc, text, m.named_checks(breaks) if breaks else ())
        f.write(f"{kind}\t{leg}\t{name or ''}\t{bwall:.1f}\t{rss}\t{rwall:.1f}\t{ans}\n")
        f.flush()
print("done")
