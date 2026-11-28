#!/usr/bin/env python3
"""Independent re-derivation of the USB-network Arty held-egress ledger.

Usage: ledger_probe.py <repo root>

Reads the USB table from docs/design/USB_NET_PATH.md and the Arty table from
docs/design/SPLIT_CONTROL_MEMORY.md, applies #894's rule
  60 + 1.05 * (max(arty, injected) - 60), rounded up to 0.01 ms,
and checks: (1) every USB figure equals the rule; (2) the USB table's Arty
column equals the Arty table's measurement column; (3) the original Arty
figures are the rule of the Arty column alone; (4) the margins and the
one-80-MHz-cycle excess of the last AECP row.
"""
import re
import sys
from decimal import ROUND_CEILING, Decimal
from pathlib import Path


def rule(ms):
    return Decimal(60) + ((Decimal(ms) - 60) * Decimal("1.05")).quantize(Decimal("0.01"), ROUND_CEILING)


def main(root):
    usb = Path(root, "docs/design/USB_NET_PATH.md").read_text()
    split = Path(root, "docs/design/SPLIT_CONTROL_MEMORY.md").read_text()
    urows = re.findall(r"^\| `([^`]+)` \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|$",
                       usb.split("| USB-network Arty held-egress row |", 1)[1].split("\n\n", 1)[0], re.M)
    arows = re.findall(r"^\| `([^`]+)` \| ([\d.]+) \| ([\d.]+) \|$",
                       split.split("| Arty held-egress row |", 1)[1].split("\n\n", 1)[0], re.M)
    arty = {n: (m, f) for n, m, f in arows}
    bad = 0
    print(f"{'row':40s} {'arty':>9s} {'inj':>9s} {'max':>9s} {'rule':>6s} {'doc':>6s} {'arty fig':>8s} margin")
    for n, a, i, f in urows:
        mx = max(Decimal(a), Decimal(i))
        r = rule(mx)
        ok = r == Decimal(f) and arty[n][0] == a and rule(a) == Decimal(arty[n][1])
        bad += not ok
        print(f"{n:40s} {a:>9s} {i:>9s} {mx!s:>9s} {r!s:>6s} {f:>6s} {arty[n][1]:>8s} {Decimal(f) - mx}"
              f" {'OK' if ok else 'MISMATCH'}")
    print("rows:", len(urows), "arty rows:", len(arows))
    cyc = Decimal(1) / Decimal(80000)  # ms per 80 MHz cycle
    print("62.14 + one 80 MHz cycle =", Decimal("62.14") + cyc, "ms; at 5-place grade resolution",
          (Decimal("62.14") + cyc).quantize(Decimal("0.00001")))
    print("unrounded last AECP figure:", Decimal(60) + (Decimal("62.03635") - 60) * Decimal("1.05"))
    print("RESULT", "PASS" if bad == 0 and len(urows) == 7 else "FAIL")
    return 0 if bad == 0 and len(urows) == 7 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
