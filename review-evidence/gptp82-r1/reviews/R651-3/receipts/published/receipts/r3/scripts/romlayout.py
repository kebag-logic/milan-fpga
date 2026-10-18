#!/usr/bin/env python3
"""Print fixed-program sizes, leg sizes and free words of one generator.
Revision-aware: a generator without the thisClock data words (before #82)
has no data rows, and the free-word summary still completes.
Usage: romlayout.py GENERATOR [SEQ_SEED [SYNC_SEQ_SEED]]"""
import importlib.util, sys
gen = sys.argv[1]
args = sys.argv[2:]
spec = importlib.util.spec_from_file_location("g", gen)
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
seq = int(args[0], 0) if args else 0
sseq = int(args[1], 0) if len(args) > 1 else 0
g.RUNTIME["cease_ms"] = 3000
g.set_servo_gains(2_000_000)
rom, used = g.build(0x02A1B2C3D4E5, seq, sseq)
fixed = [(16, g.prog_rx_sync), (64, g.prog_rx_followup), (128, g.prog_rx_announce),
         (192, g.prog_rx_pdreq), (256, g.prog_rx_pdresp), (320, g.prog_rx_pdrfu),
         (384, g.prog_rx_signal), (448, g.prog_tx_ts),
         (512, lambda b: g.prog_tmr(b, 0x02A1B2C3D4E5, seq, sseq)), (704, g.prog_tb_battery)]
occ = [None]*1024
for b, fn in fixed:
    n = len(fn(b).words()); print(f"fixed {b:4d}: {n:3d}")
    for i in range(n): occ[b+i] = f"F{b}"
for name, fn in g.LEG_FNS:
    n = len(fn(g.LB[name]).words()); print(f"leg {name:8s} @{g.LB[name]:4d}: {n:3d}")
    for i in range(n): occ[g.LB[name]+i] = name
data = [getattr(g, n) for n in ("ROM_CID_HI_C", "ROM_CID_LO_C") if hasattr(g, n)]
for a in data:
    occ[a] = "CID"
    print(f"data word {a}: {rom[a]:012X}")
if not data:
    print("data words: none in this generator")
free = [i for i in range(1024) if occ[i] is None]
print("used", used, "free", len(free), free)
