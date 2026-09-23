#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Which programs differ in CONTENT between two generator versions.

Loads generator A and generator B as separate modules, builds B's image to
fix every leg address, then emits each of A's programs at B's addresses (so
branch targets agree) and compares it word for word with B's program. A
program that differs only because a leg moved is reported equal; a program
whose words differ at the same address is reported changed.

usage: rom_program_diff.py <genA.py> <genB.py> [generator args...]
Read-only: nothing is written.
"""
from __future__ import annotations

import importlib.util
import sys


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def configure(mod, argv: list[str]) -> tuple[int, int, int]:
    clk, cease, seq, sseq = 100_000_000, 300_000, 0, 0
    it = iter(argv)
    for a in it:
        if a == "--clk-hz":
            clk = int(next(it), 0)
        elif a == "--cease-ms":
            cease = int(next(it), 0)
        elif a == "--seq-seed":
            seq = int(next(it), 0)
        elif a == "--sync-seq-seed":
            sseq = int(next(it), 0)
    mod.RUNTIME["cease_ms"] = cease
    mod.RUNTIME["p1"] = 248
    mod.set_servo_gains(clk)
    return 0x02A1B2C3D4E5, seq, sseq


def programs(mod, mac: int, seq: int, sseq: int):
    fixed = [
        ("RX_SYNC@16", 16, mod.prog_rx_sync),
        ("RX_FU@64", 64, mod.prog_rx_followup),
        ("RX_ANN@128", 128, mod.prog_rx_announce),
        ("RX_PDREQ@192", 192, mod.prog_rx_pdreq),
        ("RX_PDRESP@256", 256, mod.prog_rx_pdresp),
        ("RX_PDRFU@320", 320, mod.prog_rx_pdrfu),
        ("RX_SIGNAL@384", 384, mod.prog_rx_signal),
        ("TX_TS@448", 448, mod.prog_tx_ts),
        ("TMR@512", 512, lambda b: mod.prog_tmr(b, mac, seq, sseq)),
        ("TB@704", 704, mod.prog_tb_battery),
    ]
    return fixed


def main() -> int:
    gen_a, gen_b, *args = sys.argv[1:]
    a = load(gen_a, "gen_a")
    b = load(gen_b, "gen_b")
    mac, seq, sseq = configure(b, args)
    configure(a, args)
    b.build(mac, seq, sseq)            # fixes b.LB
    for k, v in b.LB.items():          # a's branches resolve to b's layout
        a.LB[k] = v
    changed = []
    rows = []
    fa = dict((n, (base, fn)) for n, base, fn in programs(a, mac, seq, sseq))
    for name, base, fn in programs(b, mac, seq, sseq):
        wb = fn(base).words()
        wa = fa[name][1](base).words()
        same = wa == wb
        rows.append((name, len(wa), len(wb), same))
        if not same:
            changed.append(name)
    for name, fnb in b.LEG_FNS:
        base = b.LB[name]
        wb = fnb(base).words()
        fna = dict(a.LEG_FNS)[name]
        wa = fna(base).words()
        same = wa == wb
        rows.append((f"{name}@{base}", len(wa), len(wb), same))
        if not same:
            changed.append(name)
    for name, la, lb, same in rows:
        print(f"{'same   ' if same else 'CHANGED'} {name:16s} {la:4d} -> {lb:4d}")
    print("changed:", " ".join(n.split('@')[0] for n in changed) or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
