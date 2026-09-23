#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Which ROM programs changed CONTENT between two generator revisions?

Loads the base and head generators as modules, places every program of the
BASE generator at the HEAD image's addresses (so relocated branch targets
agree), and compares each program's words with the head image word for word.
A program whose words match is only relocated; a program that differs
changed content. Unowned words (the address-seeded filler) are compared too.

Usage: rom_leg_differential.py <base_gen.py> <head_gen.py> <clk_hz> [gen args]
Generator args accepted: --cease-ms N, --seq-seed N, --sync-seq-seed N.
"""

import importlib.util
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def configure(mod, clk, cease):
    mod.RUNTIME["cease_ms"] = cease
    mod.set_servo_gains(clk)


def programs(mod, mac, seq_seed, sync_seed):
    """(name, base, fn) for every program, fixed and packed, at mod.LB."""
    fixed = [
        ("RX_SYNC", 16, mod.prog_rx_sync), ("RX_FU", 64, mod.prog_rx_followup),
        ("RX_ANN", 128, mod.prog_rx_announce), ("RX_PDREQ", 192, mod.prog_rx_pdreq),
        ("RX_PDRESP", 256, mod.prog_rx_pdresp), ("RX_PDRFU", 320, mod.prog_rx_pdrfu),
        ("RX_SIG", 384, mod.prog_rx_signal), ("TX_TS", 448, mod.prog_tx_ts),
        ("TMR", 512, lambda b: mod.prog_tmr(b, mac, seq_seed, sync_seed)),
        ("TB", 704, mod.prog_tb_battery),
    ]
    legs = [(n, mod.LB[n], fn) for n, fn in mod.LEG_FNS]
    return fixed + legs


def main():
    base_path, head_path, clk = sys.argv[1], sys.argv[2], int(sys.argv[3])
    rest = sys.argv[4:]
    opts = {"--cease-ms": 300_000, "--seq-seed": 0, "--sync-seq-seed": 0}
    for i in range(0, len(rest), 2):
        opts[rest[i]] = int(rest[i + 1], 0)
    mac = 0x02A1B2C3D4E5
    base = load(base_path, "gen_base")
    head = load(head_path, "gen_head")
    for mod in (base, head):
        configure(mod, clk, opts["--cease-ms"])
    rom, used = head.build(mac, opts["--seq-seed"], opts["--sync-seq-seed"])
    print(f"clk {clk}: head image {used} real words; head legs "
          + " ".join(f"{n}@{head.LB[n]}" for n, _ in head.LEG_FNS))
    # the base generator's programs at the head's addresses
    base.LB.clear()
    base.LB.update(head.LB)
    owned = [False] * head.DEPTH
    changed = []
    for name, addr, fn in programs(base, mac, opts["--seq-seed"],
                                   opts["--sync-seq-seed"]):
        words = fn(addr).words()
        hsz = len(fn_head_words(head, name, addr, mac, opts))
        same = (len(words) == hsz and
                all(rom[addr + i] == w for i, w in enumerate(words)))
        for i in range(max(len(words), hsz)):
            if addr + i < head.DEPTH:
                owned[addr + i] = True
        tag = "relocated/identical" if same else "CONTENT CHANGED"
        if not same:
            changed.append(name)
        print(f"  {name:9s} @{addr:4d} base {len(words):3d} words, "
              f"head {hsz:3d} words: {tag}")
    filler_bad = [i for i in range(head.DEPTH)
                  if not owned[i] and rom[i] != head.splitmix48(i)]
    print(f"unowned words that are not the address filler: {len(filler_bad)}")
    print(f"programs whose content changed: {', '.join(changed) or 'none'}")


def fn_head_words(head, name, addr, mac, opts):
    table = {n: fn for n, _, fn in programs(head, mac, opts["--seq-seed"],
                                           opts["--sync-seq-seed"])}
    return table[name](addr).words()


if __name__ == "__main__":
    main()
