#!/usr/bin/env python3
"""Refresh SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 18 and section 20 item 6 from the new capture receipt.

usage: python3 -B refresh_section18.py REPO NEW_RECEIPT OLD_RECEIPT

Every edit replaces a text that must occur exactly once, so a page that moved
is refused rather than half-edited. Figures come from the receipts only.
"""
import json
import sys
from pathlib import Path

repo, new_path, old_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
new, old = json.loads(new_path.read_text()), json.loads(old_path.read_text())
page = repo / "docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md"
s = page.read_text()

ARMS = [("endstation_ax7101_1x1_tdm8", 50_000_000, "on", "1x1", "50 / 100, contract", "ON"),
        ("endstation_ax7101_1x1_tdm8", 50_000_000, "off", "1x1", "50 / 100, contract", "OFF"),
        ("endstation_ax7101_8x8", 50_000_000, "on", "8x8", "50 / 100, contract", "ON"),
        ("endstation_ax7101_8x8", 50_000_000, "off", "8x8", "50 / 100, contract", "OFF"),
        ("endstation_ax7101_8x8", 100_000_000, "on", "8x8", "100 / 100, non-contract", "ON"),
        ("endstation_ax7101_8x8", 100_000_000, "off", "8x8", "100 / 100, non-contract", "OFF")]


def arm(receipt, shape, hz, traffic):
    return next(m for m in receipt["measurements"]
                if (m["shape"], m["cpu_hz"], m["traffic"]) == (shape, hz, traffic))


def maximum(receipt, shape, hz):
    return next(m for m in receipt["maxima"] if (m["shape"], m["cpu_hz"]) == (shape, hz))


def row(receipt, a):
    m = arm(receipt, *a[:3])
    return (f"| {a[3]} | {a[4]} | {a[5]} | {m['minimum_ms']:.5f} to {m['maximum_ms']:.5f} | "
            f"{m['margin']:.4f}x |")


def sub(old_text, new_text):
    global s
    n = s.count(old_text)
    if n != 1:
        sys.exit(f"REFUSED: {n} matches for {old_text[:90]!r}")
    s = s.replace(old_text, new_text)


m88o, m88n = maximum(old, "endstation_ax7101_8x8", 50_000_000), maximum(new, "endstation_ax7101_8x8", 50_000_000)
m11o, m11n = maximum(old, "endstation_ax7101_1x1_tdm8", 50_000_000), maximum(new, "endstation_ax7101_1x1_tdm8", 50_000_000)
m81o, m81n = maximum(old, "endstation_ax7101_8x8", 100_000_000), maximum(new, "endstation_ax7101_8x8", 100_000_000)
limit = new["hold_floor_ms"] / 2
same = sum(a["sys_cycles"] == b["sys_cycles"]
           for x in ARMS for a, b in zip(arm(new, *x[:3])["rows"], arm(old, *x[:3])["rows"]))
pins = new["processor_pins"]

sub(f"Timing. MEASURED on {old['date']} in the", f"Timing. MEASURED on {new['date']} in the")
sub("The [#671 round-8 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895) requires this remeasurement, at the merge of dev `fa820988` into #671.\n"
    "That merge brings dev's MAAP and stream frame-counter RTL into the capture SoC.\n"
    "The firmware, capture harness, processor pins, clocks and census are unchanged.\n",
    f"The [#70 assignment of 2026-10-30]({new['remeasurement_assignment']}) requires this remeasurement, at `{new['base'][:8]}` on dev `1e80128f`.\n"
    "Its firmware reports the entity enable as a request and the held enable at the restore wait's timeout.\n"
    "It also polls the PHY on every boot path past the CSR identity check.\n"
    "The capture harness, clocks and census are unchanged; the processor pins are dev's.\n"
    "The [#671 round-8 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895) required the previous one, at the merge of dev `fa820988` into #671.\n"
    "That merge brought dev's MAAP and stream frame-counter RTL into the capture SoC.\n"
    "Its firmware, capture harness, processor pins, clocks and census were unchanged.\n")
sub(f"Measured commit: `{old['base']}`.\n", f"Measured commit: `{new['base']}`.\n")
sub(f"Measured tree: `{old['tree']}`.\n", f"Measured tree: `{new['tree']}`.\n")
sub(f"Firmware SHA-256: `{old['product_firmware_sha256']}`.\n", f"Firmware SHA-256: `{new['product_firmware_sha256']}`.\n")
sub(f"Protocol-processor pin: `{old['processor_pins']['protocol-processor']}`.\n",
    f"Protocol-processor pin: `{pins['protocol-processor']}`.\n")
sub(f"gPTP-processor pin: `{old['processor_pins']['gptp-processor']}`.\n",
    f"gPTP-processor pin: `{pins['gptp-processor']}`.\n")
sub(f"\n**The worst 8x8 measurement is {m88o['maximum_ms']:.5f} ms.**\n"
    f"Its floor ratio is {m88o['margin']:.4f}x.\n"
    f"The margin to 24.5 ms is {limit - m88o['maximum_ms']:.5f} ms.\n"
    "The previous #671 receipt measured 13.86328 ms, and so did the one before it, at the same census.\n"
    "All 96 captures repeat the previous #671 receipt's system-cycle counts.\n",
    f"\n**The worst 8x8 measurement is {m88n['maximum_ms']:.5f} ms.**\n"
    f"Its floor ratio is {m88n['margin']:.4f}x.\n"
    f"The margin to 24.5 ms is {limit - m88n['maximum_ms']:.5f} ms.\n"
    f"The previous receipt, #671's round 8, measured {m88o['maximum_ms']:.5f} ms at the same census, and so did the two before it.\n"
    + ("All 96 captures repeat its system-cycle counts.\n" if same == 96
       else f"{same} of 96 captures repeat its system-cycle counts; the firmware's code layout moved.\n"))
sub("The firmware changed in its boot path and its console report of the writer's hold only; `nvm_capture()`, the backend's capture hold and the census are unchanged.\n",
    "The firmware changed in its boot and restore-wait reports and its PHY poll only; `nvm_capture()`, the backend's capture hold and the census are unchanged.\n")
sub(f"\nThe 1x1 maximum is {m11o['maximum_ms']:.5f} ms ({m11o['margin']:.4f}x floor ratio).\n",
    f"\nThe 1x1 maximum is {m11n['maximum_ms']:.5f} ms ({m11n['margin']:.4f}x floor ratio).\n")
for a in ARMS:
    sub("\n" + row(old, a) + "\n", "\n" + row(new, a) + "\n")
# section 20 item 6
sub(f"   The worst 8x8 copy is {m88o['maximum_ms']:.5f} ms across both arms.\n",
    f"   The worst 8x8 copy is {m88n['maximum_ms']:.5f} ms across both arms.\n")
sub(f"   Its ratio to the guaranteed 49 ms floor is {m88o['margin']:.4f}x.\n",
    f"   Its ratio to the guaranteed 49 ms floor is {m88n['margin']:.4f}x.\n")
sub(f"   The 24.5 ms margin is {limit - m88o['maximum_ms']:.5f} ms.\n",
    f"   The 24.5 ms margin is {limit - m88n['maximum_ms']:.5f} ms.\n")
sub("   The previous #671 receipt measured 13.86328 ms, with a 10.63672 ms margin.\n",
    f"   The previous receipt, #671's round 8, measured {m88o['maximum_ms']:.5f} ms, with a {limit - m88o['maximum_ms']:.5f} ms margin.\n")
sub(f"   The 1x1 maximum is {m11o['maximum_ms']:.5f} ms ({m11o['margin']:.4f}x floor ratio).\n",
    f"   The 1x1 maximum is {m11n['maximum_ms']:.5f} ms ({m11n['margin']:.4f}x floor ratio).\n")
sub(f"   The 100 MHz 8x8 comparison is non-contract: {m81o['maximum_ms']:.5f} ms maximum.\n",
    f"   The 100 MHz 8x8 comparison is non-contract: {m81n['maximum_ms']:.5f} ms maximum.\n")
page.write_text(s)
print(f"refreshed: 8x8 {m88n['maximum_ms']:.5f} ms ({m88n['margin']:.4f}x, margin {limit - m88n['maximum_ms']:.5f} ms); "
      f"1x1 {m11n['maximum_ms']:.5f} ms; 8x8/100 {m81n['maximum_ms']:.5f} ms; {same} of 96 captures repeat")
