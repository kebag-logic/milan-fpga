#!/usr/bin/env python3
"""R532-7 reviewer matrix: head probes, the lane's twelve new plants and reviewer plants.

usage: r532_7_matrix.py REPO PACKET LWSRP JOBS
Exports REPO HEAD (plus the processor submodules) to PACKET/scratch/root-head,
creates one planted copy per defect, runs every (root, test, filter, IF) job
through scripts/r532_probe.py with JOBS workers, and writes
PACKET/receipts/matrix/<job>.{log,rc} plus PACKET/receipts/matrix.tsv.
A plant job is CAUGHT only when rc==1, the named test fails and the needle
appears in that failure block (the lane's own srp_mutants.caught rule).
"""
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
from pathlib import Path

repo, packet, lwsrp, jobs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
scratch, scripts = packet / "scratch", packet / "scripts"
out = packet / "receipts/matrix"
out.mkdir(parents=True, exist_ok=True)
head = scratch / "root-head"
if head.exists():
    shutil.rmtree(head)
head.mkdir(parents=True)
subprocess.run(f"git -C {repo} archive HEAD | tar -x -C {head}", shell=True, check=True)
for sm in ("protocol-processor", "gptp-processor"):
    subprocess.run(f"git -C {repo}/{sm} archive HEAD | tar -x -C {head}/{sm}", shell=True, check=True)

sys.path[:0] = [str(head / "sw/firmware/ctrl/test"), str(head / "sw/firmware/gtest")]
import srp_mutants  # the head's own plant list and catch rule
from ctrl_build import Outcome

SRC = "sw/firmware/ctrl/srp/srp_mbx.c"
lane = [d for d in srp_mutants.DEFECTS if d.suite == "srp_rx_retry.cpp" and d.name.startswith("receive-") and
        ("retention" in d.name or "discard" in d.name or "deadline" in d.name or "expir" in d.name or
         "flood" in d.name)]
assert len(lane) == 12, [d.name for d in lane]
reviewer = {
    # Poll retry no longer checks the bound; only first refusal/recreation do.
    "rv-poll-no-expire": ("            } else {\n                expire_receive(m);\n            }", "            }"),
    # The deadline is renewed at every failed retry: a moving window.
    "rv-retry-renews-deadline": ("            } else {\n                expire_receive(m);",
                                 "            } else {\n                m->pending_rx.arrival_ms = mbx_now_ms();\n"
                                 "                expire_receive(m);"),
    # Discard is counted but the record stays.
    "rv-expire-keeps-record": ("        m->pending_rx.len = 0;\n        ++m->rx_discarded;", "        ++m->rx_discarded;"),
    # Discard is counted as an ordinary refusal instead of the distinct counter.
    "rv-discard-as-refused": ("        ++m->rx_discarded;", "        ++m->refused;"),
    # Bound set to LeaveTime instead of one periodic interval.
    "rv-bound-leavetime": ("#define SRP_RX_RETRY_MS 1000u", "#define SRP_RX_RETRY_MS 5000u"),
}
plants = {d.name: (d.old, d.new) for d in lane} | reviewer
for name, (old, new) in plants.items():
    root = scratch / f"root-{name}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(head, root, symlinks=True)
    f = root / SRC
    text = f.read_text()
    assert text.count(old) == 1, f"{name}: {text.count(old)} sites"
    f.write_text(text.replace(old, new))

retry = "sw/firmware/ctrl/test/srp_rx_retry.cpp"
work = []  # (job, root, test, filter, ifs, plant-test, needle)
probes = [scripts / p for p in ("r533_5_independent.cpp", "r532_retry_probes.cpp", "r532_hol_probe.cpp",
                                "r532_flood_probe.cpp", "r532_7_bound_probe.cpp")]
for n in (1, 2):
    work.append((f"head-srp_rx_retry-if{n}", head, head / retry, "*", n, None, None))
    for p in probes:
        work.append((f"head-{p.stem}-if{n}", head, p, "*", n, None, None))
    for d in lane:
        work.append((f"{d.name}-named-if{n}", scratch / f"root-{d.name}", scratch / f"root-{d.name}" / retry,
                     d.test, n, d.test, d.needle))
    for name in reviewer:
        r = scratch / f"root-{name}"
        work.append((f"{name}-srp_rx_retry-if{n}", r, r / retry, "*", n, None, None))
        work.append((f"{name}-r532_7_bound_probe-if{n}", r, scripts / "r532_7_bound_probe.cpp", "*", n, None, None))

env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch / "tmp"))


def one(item):
    job, root, test, flt, n, named, needle = item
    o = scratch / "matrix" / job
    if o.exists():
        shutil.rmtree(o)
    r = subprocess.run([sys.executable, "-B", str(scripts / "r532_probe.py"), str(root), str(lwsrp), str(o), str(n),
                        str(test), flt], env=env, capture_output=True, text=True)
    full = (o / "probe.log").read_text() if (o / "probe.log").exists() else ""
    (out / f"{job}.log").write_text(r.stdout + r.stderr + "\n--- full log ---\n" + full)
    (out / f"{job}.rc").write_text(f"{r.returncode}\n")
    verdict = ""
    if named:
        ok = srp_mutants.caught(named, needle, Outcome("srp", r.returncode, full))
        verdict = "CAUGHT" if ok else "ESCAPED"
    return job, r.returncode, verdict


with cf.ThreadPoolExecutor(jobs) as pool:
    rows = list(pool.map(one, work))
(packet / "receipts/matrix.tsv").write_text("".join(f"{j}\t{rc}\t{v}\n" for j, rc, v in sorted(rows)))
for j, rc, v in sorted(rows):
    print(j, rc, v)
