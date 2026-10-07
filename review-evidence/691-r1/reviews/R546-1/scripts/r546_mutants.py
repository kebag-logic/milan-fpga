#!/usr/bin/env python3
"""Reviewer probe R546-1: build disposable receiver mutants.

usage: r546_mutants.py PATCHED_PKG_PARENT OUT_DIR
Copies PATCHED_PKG_PARENT/liteeth into OUT_DIR/<mutant>/liteeth and applies
one textual mutation to liteeth/phy/gmii.py. Every replacement must match
exactly once, or the script refuses (a mutant that did not apply proves
nothing).
"""
import shutil
import sys
from pathlib import Path

MUTANTS = {
    # the four controls named by the assignment
    "live-reset-valid": [("source.valid.eq(rx_dv & ~rx_reset)",
                          "source.valid.eq(rx_dv & ~ResetSignal())")],
    "last-forced-0": [("source.last.eq(~pads.rx_dv & source.valid)",
                       "source.last.eq(0)")],
    "data-bit7-lost": [("rx_data.eq(pads.rx_data),",
                        "rx_data.eq(pads.rx_data[:7]),")],
    # reviewer additions
    "live-reset-data": [("Mux(rx_reset, 0, rx_data)",
                         "Mux(ResetSignal(), 0, rx_data)")],
    "data-unmasked": [("Mux(rx_reset, 0, rx_data)", "rx_data")],
    "last-unmasked-dv": [("source.last.eq(~pads.rx_dv & source.valid)",
                          "source.last.eq(~pads.rx_dv & rx_dv)")],
    "reset-not-sampled": [("rx_reset.eq(ResetSignal()),", ""),
                          ("rx_reset = Signal(reset=1, reset_less=True)",
                           "rx_reset = ResetSignal()")],
    "extra-latency": [("rx_dv.eq(pads.rx_dv),",
                       "rx_dv.eq(rx_dv0), rx_dv0.eq(pads.rx_dv),"),
                      ("rx_dv = Signal(reset_less=True)",
                       "rx_dv = Signal(reset_less=True); rx_dv0 = Signal(reset_less=True)")],
}


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    for name, edits in MUTANTS.items():
        dst = out / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src / "liteeth", dst / "liteeth")
        f = dst / "liteeth" / "phy" / "gmii.py"
        text = f.read_text()
        for old, new in edits:
            if text.count(old) != 1:
                raise SystemExit(f"{name}: {old!r} matches {text.count(old)} times")
            text = text.replace(old, new)
        f.write_text(text)
        print(name)


if __name__ == "__main__":
    main()
