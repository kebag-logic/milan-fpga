#!/usr/bin/env python3
"""Cross-check the capture figures published in the docs against the receipt.

Reads tb/verilator/nvm_capture_cpu/measurements.json and asserts that every
figure section 17/18/20 of SAVED_STATE_SNAPSHOT_OWNERSHIP.md and the harness
README quote is present verbatim, recomputed from the receipt's rows.
Usage: check_capture_figures.py <repo>
"""
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
rec = json.loads((repo / "tb/verilator/nvm_capture_cpu/measurements.json").read_text())
own = (repo / "docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md").read_text()
readme = (repo / "tb/verilator/nvm_capture_cpu/README.md").read_text()
fails = 0


def need(text, needle, what):
    global fails
    ok = needle in text
    fails += not ok
    print(f"{'OK  ' if ok else 'MISS'} {what}: {needle!r}")


tag = {"endstation_ax7101_1x1_tdm8": "1x1", "endstation_ax7101_8x8": "8x8"}
for arm in rec["measurements"]:
    ms = [r["sys_cycles"] / arm["sys_hz"] * 1000 for r in arm["rows"]]
    lo, hi = min(ms), max(ms)
    assert abs(lo - arm["minimum_ms"]) < 1e-9 and abs(hi - arm["maximum_ms"]) < 1e-9
    ratio = 49 / hi
    basis = "contract" if arm["cpu_hz"] == 50_000_000 else "non-contract"
    row = (f"| {tag[arm['shape']]} | {arm['cpu_hz'] // 1_000_000} / 100, {basis} | "
           f"{arm['traffic'].upper()} | {lo:.5f} to {hi:.5f} | {ratio:.4f}x |")
    need(own, row, "section 18 table row")
m8 = next(m for m in rec["maxima"] if m["shape"].endswith("8x8") and m["cpu_hz"] == 50_000_000)
m1 = next(m for m in rec["maxima"] if m["shape"].endswith("tdm8"))
m100 = next(m for m in rec["maxima"] if m["cpu_hz"] == 100_000_000)
need(own, f"**The worst 8x8 measurement is {m8['maximum_ms']:.5f} ms.**", "8x8 maximum")
need(own, f"Its floor ratio is {49 / m8['maximum_ms']:.4f}x.", "8x8 floor ratio")
need(own, f"The margin to 24.5 ms is {24.5 - m8['maximum_ms']:.5f} ms.", "8x8 margin")
need(own, f"The 1x1 maximum is {m1['maximum_ms']:.5f} ms ({49 / m1['maximum_ms']:.4f}x floor ratio).",
     "1x1 maximum")
need(own, f"non-contract: {m100['maximum_ms']:.5f} ms maximum", "100 MHz point (section 20)")
for shape, t in tag.items():
    c = rec["measured_for"][shape]
    need(readme, f"covers {c['raw_bytes']:,} bytes and {c['records']} records", f"README census {t}")
    need(own, f"{c['raw_bytes']:,} bytes / {c['records']} records" if t == "1x1"
         else f"it is {c['raw_bytes']:,} bytes / {c['records']} records", f"section 18 census {t}")
need(own, f"Measured commit: `{rec['base']}`.", "measured commit")
need(own, f"Measured tree: `{rec['tree']}`.", "measured tree")
need(own, f"Firmware SHA-256: `{rec['product_firmware_sha256']}`.", "firmware digest")
print("RESULT:", "PASS" if not fails else f"FAIL ({fails})")
sys.exit(1 if fails else 0)
