#!/usr/bin/env python3
"""#762's three [762-DP] stopped_i wiring mutants on obj_dynmap, at a merged head.

usage: wiring_mutants.py <clone> <outdir>

Each mutant replaces the one `.stopped_i` line of the KL_avtp_rx_monitor_ctx
instance in a copy of hdl/milan/milan_datapath.sv (the pattern must match
exactly once), builds the dynmap leg through the suite's own recipe
(`dynmap-build` with DP_SRC and DYNMAP_MDIR overridden, the generated ROM
images kept), and runs it from the suite directory. A mutant is caught when
the leg exits non-zero and its [FAIL] lines are EXACTLY the named checks:
nothing else in the leg, [MAPREC] included, may move. The clean leg is built
and run the same way first, alone. At most two builds at once.
"""
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
SUITE = CLONE / "tb/verilator/milan_dp"
DP = CLONE / "hdl/milan/milan_datapath.sv"
V = "<tools>/pinned-verilator-5.050/verilator"
LINE = "    .stopped_i      (acmpl_stopped_v_w[N_STREAMS-1:0]),\n"
GAP_SIL = ("[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0",
           "[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0")
MUTANTS = [
    ("clean", None, ()),
    ("port tied to '0", "    .stopped_i      ('0),\n", GAP_SIL),
    ("wrong vector: sink 1's level (acmpl_stopped_v_w[N_STREAMS:1])",
     "    .stopped_i      (acmpl_stopped_v_w[N_STREAMS:1]),\n", GAP_SIL),
    ("wrong vector: the bound level (acmpl_bound_v_w[N_STREAMS-1:0])",
     "    .stopped_i      (acmpl_bound_v_w[N_STREAMS-1:0]),\n",
     ("[762-DP] 4 started gap: STREAM_INTERRUPTED +1",)),
]
SLOTS = threading.Semaphore(2)


def one(i: int, name: str, repl: str | None, named: tuple) -> str:
    tag = f"m{i}"
    work = OUT / tag
    work.mkdir(parents=True, exist_ok=True)
    src = DP
    if repl is not None:
        text = DP.read_text()
        n = text.count(LINE)
        if n != 1:
            return f"[FAIL] {tag} {name}: the stopped_i line appears {n} time(s), expected 1"
        src = work / "milan_datapath.sv"
        src.write_text(text.replace(LINE, repl))
    mdir = work / "obj"
    cmd = ["make", "-s", "-C", str(SUITE), "-o", "ltn_rom.hex", "-o", "ucode.hex",
           "dynmap-build", f"DP_SRC={src}", f"DYNMAP_MDIR={mdir}", f"VERILATOR={V}",
           "VERILATOR_JOBS=2"]
    with SLOTS:
        b = subprocess.run(cmd, capture_output=True, text=True, check=False)
    (work / "build.log").write_text(" ".join(cmd) + "\n" + b.stdout + b.stderr
                                    + f"\nBUILD rc={b.returncode}\n")
    exe = mdir / "Vmilan_dp_dynmap"
    if b.returncode != 0 or not exe.is_file():
        return f"[FAIL] {tag} {name}: did not build (rc {b.returncode})"
    r = subprocess.run([str(exe)], cwd=str(SUITE), capture_output=True, text=True, check=False)
    log = r.stdout + r.stderr
    (work / "run.log").write_text(log + f"\nRUN rc={r.returncode}\n")
    fails = [ln.strip() for ln in log.splitlines() if ln.strip().startswith("[FAIL]")]
    tally = re.search(r"^checks: (\d+)\s+failures: (\d+)", log, re.M)
    t = f"{tally.group(1)} checks, {tally.group(2)} failures" if tally else "no tally"
    if repl is None:
        ok = r.returncode == 0 and not fails and tally is not None
        return f"[{'PASS' if ok else 'FAIL'}] {tag} clean leg: rc {r.returncode}, {t}"
    want = set(named)
    matched = all(any(f.startswith("[FAIL]") and n in f for f in fails) for n in named)
    extra = [f for f in fails if not any(n in f for n in named)]
    ok = r.returncode != 0 and matched and not extra and len(fails) == len(want)
    detail = "; ".join(fails) if fails else "no failure"
    return (f"[{'PASS' if ok else 'FAIL'}] {tag} {name}: rc {r.returncode}, {t}; "
            f"failed: {detail}" + (f"; NOT NAMED: {extra}" if extra else ""))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    # the clean leg alone first: it makes the shared generated inputs once
    res = [one(0, *MUTANTS[0])]
    with ThreadPoolExecutor(max_workers=2) as ex:
        res += list(ex.map(lambda a: one(a[0], *a[1]), list(enumerate(MUTANTS))[1:]))
    for line in res:
        print(line)
    bad = sum(not r.startswith("[PASS]") for r in res)
    print(f"{len(res)} checks: {len(res) - bad} PASS, {bad} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
