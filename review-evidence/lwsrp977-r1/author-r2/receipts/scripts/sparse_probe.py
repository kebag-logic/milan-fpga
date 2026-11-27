"""sparse_probe.py <checkout> <work> <old-rev> <new-rev>: the scan-ending defect (type |= 31u -> type = 255u)
against the MAD trace driver of each revision, with LWSRP_LEAN_TX alone and with the end-station set, both profiles.
Each mutant build's traces are compared with the base revision's (main d1bb4f4e) over 200 seeds, 3000 steps.
The one-port seeds are compared as tests/check_differential.py compares them. Prints SURVIVED or KILLED at a seed."""
import hashlib
import subprocess
import sys
from pathlib import Path

checkout, work, old_rev, new_rev = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
BASE = "d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b"
sys.path.insert(0, str(checkout / "tests"))
import check_differential as cd  # the checkout's own comparison rules  # noqa: E402

work.mkdir(parents=True)
SOURCES = ["core/mrp_mad.c", "core/mrp_pdu.c", "ports/timer.c", "modules/msrp.c", "modules/mvrp.c", "modules/mmrp.c"]


def export(rev, into, paths):
    into.mkdir(parents=True)
    archive = into / "x.tar"
    subprocess.run(["git", "-C", str(checkout), "archive", "-o", str(archive), rev, *paths], check=True)
    subprocess.run(["tar", "-xf", str(archive), "-C", str(into)], check=True)


def build(src, driver, extra, milan, exe):
    keyed = "attr_key" in (src / "include/shish_lan/mrp.h").read_text()
    cmd = ["cc", *cd.FLAGS, *extra, *(["-DTRACE_ATTR_KEY"] if keyed else []), f"-DLWSRP_MILAN={milan}",
           f"-I{src}", f"-I{src / 'include'}", "-o", str(exe), str(driver), *[str(src / s) for s in SOURCES]]
    subprocess.run(cmd, check=True, capture_output=True)
    return exe


export(BASE, work / "base", ["src"])
for label, rev in (("old", old_rev), ("new", new_rev)):
    export(rev, work / label, ["src", "tests/differential/mad_trace.c"])
    mutant = work / f"{label}-mutant"
    export(rev, mutant, ["src"])
    target = mutant / "src/core/mrp_mad.c"
    text = target.read_text()
    old, new = "            type |= 31u;\n            continue;", "            type = 255u;\n            continue;"
    assert text.count(old) == 1
    target.write_text(text.replace(old, new))
    driver = work / label / "tests/differential/mad_trace.c"
    for milan in (0, 1):
        reference = build(work / "base/src", driver, [], milan, work / f"{label}-base-{milan}")
        expected = {}
        for seed in range(1, 201):
            out = subprocess.run([str(reference), str(seed), "3000"], capture_output=True, timeout=60).stdout
            expected[seed] = (cd.compared("mad", [], out), cd.compared("mad", cd.ONE_PORT, out))
        for config, extra in (("lean-tx", cd.LEAN_TX), ("end-station", cd.END_STATION)):
            exe = build(mutant / "src", driver, extra, milan, work / f"{label}-{config}-{milan}")
            seen = None
            for seed in range(1, 201):
                r = subprocess.run([str(exe), str(seed), "3000"], capture_output=True, timeout=60)
                if r.returncode or cd.compared("mad", extra, r.stdout) != expected[seed][cd.one_port_build(extra)]:
                    seen = seed
                    break
            print(f"driver {label} ({rev[:8]}) milan {milan} {config}: "
                  f"{'KILLED at seed %d' % seen if seen else 'SURVIVED 200 seeds'}", flush=True)
