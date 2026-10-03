#!/usr/bin/env python3
"""Scratch (never committed): print Markdown tables from the gate's own records."""
import json
import sys
from pathlib import Path

S = Path("$VALIDATION_STORAGE/234-a516")
DEVICE = {"LUT": 63400, "FF": 126800, "SLICE": 15850, "BRAM_TILE": 135, "DSP": 240}


def load(combo: str, endpoint: str) -> dict | None:
    path = S / combo / "work" / f"record-{endpoint}.json"
    return json.loads(path.read_text()) if path.exists() else None


def n(value) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"{value:+.3f}" if abs(value) < 10 else f"{value:,}"
    return f"{int(value):,}"


def totals(endpoint: str, figures: tuple[str, ...]) -> None:
    print(f"\n### {endpoint}")
    print("| Combination | " + " | ".join(figures) + " |")
    print("|---|" + "---:|" * len(figures))
    recs = {c: load(c, endpoint) for c in "AB"}
    for combo, rec in recs.items():
        if rec:
            print(f"| {combo} | " + " | ".join(n(rec["figures"][f]) for f in figures) + " |")
    if all(recs.values()):
        delta = []
        for f in figures:
            d = recs["B"]["figures"][f] - recs["A"]["figures"][f]
            delta.append(f"{d:+.3f}" if isinstance(d, float) and not float(d).is_integer() else f"{int(d):+,}")
        print("| B minus A | " + " | ".join(delta) + " |")


def scopes(endpoint: str, keys: list[str]) -> None:
    recs = {c: load(c, endpoint) for c in "AB"}
    print(f"\n### {endpoint} sub-blocks")
    print("| Instance | LUT A | LUT B | FF A | FF B | RAMB36 | RAMB18 | DSP | CARRY4 A |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k in keys:
        a = recs["A"]["scopes"].get(k) if recs["A"] else None
        b = recs["B"]["scopes"].get(k) if recs["B"] else None
        if not a:
            continue
        bl = n(b["LUT"]) if b else "-"
        bf = n(b["FF"]) if b else "-"
        print(f"| `{k}` | {n(a['LUT'])} | {bl} | {n(a['FF'])} | {bf} | {a['RAMB36']} | {a['RAMB18']} | {a['DSP']} | {n(a['CARRY4'])} |")


if __name__ == "__main__":
    totals("route-1x1", ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "BRAM_TILE", "DSP", "CARRY4", "WNS_ns", "WHS_ns"))
    for e in ("ooc-1x1", "ooc-8x8"):
        totals(e, ("LUT", "FF", "RAMB36", "RAMB18", "BRAM_TILE", "DSP", "CARRY4"))
    keys = sys.argv[1:] or ["wrapper", "u_pp", "u_nvm", "ctl_fifo", "u_pp/u_srp", "u_pp/u_adp", "u_pp/u_talker",
                            "u_pp/u_listener", "u_pp/u_aecp", "u_pp/u_aecp/u_ucpu", "u_pp/u_notify",
                            "u_pp/u_nvm_port", "u_pp/u_nvm_arb", "u_pp/u_nvm_shadow", "u_pp/u_aecp/u_d3"]
    for e in ("ooc-1x1", "ooc-8x8"):
        scopes(e, keys)


GROUPS = [
    ("SRP", ["u_pp/u_srp"]),
    ("ADP", ["u_pp/u_adp"]),
    ("ACMP talker", ["u_pp/u_talker"]),
    ("ACMP listener", ["u_pp/u_listener", "u_pp/u_lsn_admit"]),
    ("AECP engine, total", ["u_pp/u_aecp"]),
    ("AECP microcontroller", ["u_pp/u_aecp/u_ucpu"]),
    ("AECP saved-state writer (NVM manager)", ["u_pp/u_aecp/u_d3"]),
    ("Notification", ["u_pp/u_notify"]),
    ("NVM port", ["u_pp/u_nvm_port"]),
    ("NVM manager arbiter", ["u_pp/u_nvm_arb"]),
    ("ACMP binding store (NVM manager)", ["u_pp/u_nvm_shadow"]),
    ("NVM backend (wrapper)", ["u_nvm"]),
    ("Packet storage: RX pools", ["u_pp/g_rx_pool[0].u_rx_slots", "u_pp/g_rx_pool[1].u_rx_slots",
                                  "u_pp/g_rx_pool[2].u_rx_slots", "u_pp/g_rx_pool[3].u_rx_slots",
                                  "u_pp/g_rx_pool[4].u_rx_slots", "u_pp/g_rx_pool[5].u_rx_slots"]),
    ("Packet storage: TX slots", ["u_pp/u_tx_slots"]),
    ("Packet storage: trace ring", ["u_pp/u_trace"]),
    ("Packet storage: control frame FIFO (wrapper)", ["ctl_fifo"]),
    ("Wrapper total", ["wrapper"]),
]


def grouped(endpoint: str) -> None:
    recs = {c: load(c, endpoint) for c in "AB"}
    print(f"\n### {endpoint} grouped")
    print("| Sub-block | Instances | LUT A / B | FF A / B | RAMB36 A / B | RAMB18 A / B | DSP A / B | CARRY4 A / B |")
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    for label, keys in GROUPS:
        cells = []
        for f in ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4"):
            vals = []
            for c in "AB":
                r = recs[c]
                if not r:
                    vals.append("-")
                    continue
                present = [r["scopes"][k][f] for k in keys if k in r["scopes"]]
                vals.append(f"{sum(present):,}" if present else "-")
            cells.append(" / ".join(vals))
        inst = ", ".join(f"`{k}`" for k in keys if any(k in (recs[c] or {}).get("scopes", {}) for c in "AB"))
        if len(keys) > 2:
            inst = "`u_pp/g_rx_pool[*].u_rx_slots`"
        print(f"| {label} | {inst} | " + " | ".join(cells) + " |")


grouped("ooc-1x1")
grouped("ooc-8x8")
