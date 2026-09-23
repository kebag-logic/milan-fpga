#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R259-3 ROM check for FPGA-gPTP PR #74 at the reviewed head.

1. Each tracked image equals its generator's output at the head (with the
   arguments its consumer uses), and its SHA-256 is printed.
2. Per program, the base generator's and the cbccf22 generator's code,
   emitted at the head's own addresses with the head's leg table, is compared
   word for word with the head's image, at five clocks. Programs whose content
   differs, and legs whose placement moved, are listed.

Trees are read with `git archive` from the clone into a scratch directory;
nothing in the clone is written.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
import sys
import tarfile
import io
from pathlib import Path

CLONE = Path(os.environ["CLONE"])        # set by scripts/env.sh
SCRATCH = Path(os.environ["SCRATCH"])
REVS = {
    "base": "c1b617435824929a790739ea8585c3fe1a328cc0",
    "prev": "cbccf226068c107fb30764891c98b8d70c54d775",
    "head": "ba9268100ebe92dfc61aed30e2910245fc8c97cf",
}
GEN = "hdl/ucode/gen_gptp_ucode.py"
TRACKED = [
    ("tb/verilator/engine/gptp_ucode.hex", ["--clk-hz", "2000000", "--cease-ms", "3000"]),
    ("tb/tsngen/gptp_ucode.hex", ["--clk-hz", "2000000"]),
    ("tb/verilator/ucpu/gptp_ucode.hex", []),
    ("syn/ooc/work/gptp_ucode.hex", []),
]
CLOCKS = [2_000_000, 25_000_000, 50_000_000, 100_000_000, 125_000_000]
FAILS = 0


def fail(msg: str) -> None:
    global FAILS
    FAILS += 1
    print(f"FAIL {msg}")


def export(rev: str, name: str) -> Path:
    out = SCRATCH / f"rom-{name}"
    if not out.exists():
        data = subprocess.run(["git", "-C", str(CLONE), "archive", rev],
                              check=True, capture_output=True).stdout
        out.mkdir(parents=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as t:
            t.extractall(out, filter="data")
    return out


def load(tree: Path, tag: str):
    spec = importlib.util.spec_from_file_location(f"gen_{tag}", tree / GEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tracked_images(head: Path) -> None:
    print("== 1. tracked images equal the head generator's output")
    for rel, args in TRACKED:
        out = SCRATCH / "rom-regen" / rel.replace("/", "_")
        out.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run([sys.executable, str(head / GEN), *args, "-o", str(out)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"{rel}: generator exit {r.returncode}: {r.stderr.strip()}")
            continue
        same = out.read_bytes() == (head / rel).read_bytes()
        print(f"{rel} args={' '.join(args) or '(defaults)'}")
        print(f"  tracked sha256 {sha(head / rel)}")
        print(f"  regen   sha256 {sha(out)}  {'EQUAL' if same else 'DIFFERENT'}")
        print(f"  {r.stdout.strip().splitlines()[0].split(': ', 1)[1]}")
        if not same:
            fail(f"{rel} differs from its regeneration")
    for extra, args in [("engine --seq-seed 0x200000",
                         ["--clk-hz", "2000000", "--cease-ms", "3000", "--seq-seed", "0x200000"]),
                        ("engine --sync-seq-seed 0x10000",
                         ["--clk-hz", "2000000", "--cease-ms", "3000", "--sync-seq-seed", "0x10000"])] + \
                       [(f"--clk-hz {c}", ["--clk-hz", str(c)]) for c in CLOCKS]:
        out = SCRATCH / "rom-regen" / ("x_" + extra.replace(" ", "_").replace("-", ""))
        r = subprocess.run([sys.executable, str(head / GEN), *args, "-o", str(out)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"{extra}: generator exit {r.returncode}")
            continue
        print(f"image {extra}: sha256 {sha(out)}")


def programs(mod, clk: int):
    """(name, base, fn) for every program of mod's build at clk, after build."""
    mod.RUNTIME["cease_ms"] = 300_000
    mod.RUNTIME["p1"] = 248
    mod.set_servo_gains(clk)
    rom, used = mod.build(0x02A1B2C3D4E5)
    fixed = [(16, "RX_SYNC", mod.prog_rx_sync), (64, "RX_FU", mod.prog_rx_followup),
             (128, "RX_ANN", mod.prog_rx_announce), (192, "RX_PDREQ", mod.prog_rx_pdreq),
             (256, "RX_PDRESP", mod.prog_rx_pdresp), (320, "RX_PDRFU", mod.prog_rx_pdrfu),
             (384, "RX_SIGNAL", mod.prog_rx_signal), (448, "TX_TS", mod.prog_tx_ts),
             (512, "TMR", lambda b: mod.prog_tmr(b, 0x02A1B2C3D4E5)),
             (704, "TB", mod.prog_tb_battery)]
    progs = [(n, b, f) for b, n, f in fixed]
    progs += [(n, mod.LB[n], f) for n, f in mod.LEG_FNS]
    return rom, used, progs


def compare(old, head, oldname: str, clk: int) -> None:
    hrom, hused, hprogs = programs(head, clk)
    lb_head = dict(head.LB)
    # the old generator's own placement, for the relocation list
    orom, oused, oprogs = programs(old, clk)
    lb_old = dict(old.LB)
    moved = [f"{n} {lb_old[n]}->{lb_head[n]}" for n in lb_head
             if n in lb_old and lb_old[n] != lb_head[n]]
    # now emit the old code at the head's addresses
    old.LB.clear()
    old.LB.update(lb_head)
    old.RUNTIME["cease_ms"] = 300_000
    old.set_servo_gains(clk)
    oldfns = {n: f for n, _, f in programs_fns(old)}
    changed = []
    for name, base, fn in hprogs:
        hw = hrom[base:base + len(fn(base).words())]
        if name not in oldfns:
            changed.append(f"{name}(new)")
            continue
        ow = oldfns[name](base).words()
        if ow != hw:
            changed.append(f"{name}({len(ow)}->{len(hw)} words)")
    print(f"  {clk:>9} Hz vs {oldname}: real words {oused}->{hused}; "
          f"content differs: {', '.join(changed) or 'none'}; "
          f"moved: {', '.join(moved) or 'none'}")
    return changed, moved


def programs_fns(mod):
    fixed = [(16, "RX_SYNC", mod.prog_rx_sync), (64, "RX_FU", mod.prog_rx_followup),
             (128, "RX_ANN", mod.prog_rx_announce), (192, "RX_PDREQ", mod.prog_rx_pdreq),
             (256, "RX_PDRESP", mod.prog_rx_pdresp), (320, "RX_PDRFU", mod.prog_rx_pdrfu),
             (384, "RX_SIGNAL", mod.prog_rx_signal), (448, "TX_TS", mod.prog_tx_ts),
             (512, "TMR", lambda b: mod.prog_tmr(b, 0x02A1B2C3D4E5)),
             (704, "TB", mod.prog_tb_battery)]
    return [(n, b, f) for b, n, f in fixed] + [(n, 0, f) for n, f in mod.LEG_FNS]


def main() -> int:
    trees = {k: export(v, k) for k, v in REVS.items()}
    tracked_images(trees["head"])
    print("== 2. per-program content at the head's addresses")
    for oldname in ("base", "prev"):
        for clk in CLOCKS:
            head = load(trees["head"], f"head{clk}")
            old = load(trees[oldname], f"{oldname}{clk}")
            changed, moved = compare(old, head, oldname, clk)
            if oldname == "base":
                if sorted(c.split("(")[0] for c in changed) != ["PDPAIR", "SERVO"]:
                    fail(f"{clk} vs base: content change outside SERVO/PDPAIR: {changed}")
            else:
                if sorted(c.split("(")[0] for c in changed) != ["BECOME", "SRTO"]:
                    fail(f"{clk} vs prev: content change outside SRTO/BECOME: {changed}")
    print(f"\n{FAILS} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
