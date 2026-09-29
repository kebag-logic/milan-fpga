#!/usr/bin/env python3
"""Planted-defect probe: each mutation is applied to a disposable copy of the packet
(or of a page) and rederive.py must report at least one FAIL for it.

usage: mutate.py <packet author dir> <606 page> <608 page> <scratch dir>
"""
import json, shutil, subprocess, sys
from pathlib import Path

A, P6, P8, S = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
RD = Path(__file__).resolve().parent / "rederive.py"


def edit_tsv(p, fn):
    lines = p.read_text().splitlines(keepends=True)
    p.write_text("".join(fn(lines)))


def m1(a, p6, p8):  # bridge re-declaration planted between cycle 22's own LeaveAll and its Lv
    def f(lines):
        k = next(i for i, l in enumerate(lines) if "\tbridge\tListener\tLv\t0200000000010001" in l)
        return lines[:k] + ["3.060000000\tbridge\tListener\tJoinIn\t0200000000010001\t2\n"] + lines[k:]
    edit_tsv(a / "cycles/cycle-022/msrp.tsv", f)


def m2(a, p6, p8):  # an IN cycle that kept streaming after its Lv
    j = a / "cycles/cycle-005/analysis.json"; x = json.loads(j.read_text())
    x["pdus_after_lv_plus_period"] = 3; x["last_pdu_after_lv_s"] = 0.006
    j.write_text(json.dumps(x))


def m3(a, p6, p8):  # page restart cell altered
    p8.write_text(p8.read_text().replace("| 0.012280 | PASS | PASS |", "| 0.012281 | PASS | PASS |", 1))


def m4(a, p6, p8):  # cycle 22's own LeaveAll removed from the record
    edit_tsv(a / "cycles/cycle-022/msrp.tsv", lambda ls: [l for l in ls if not (l.startswith("3.059247408\tDUT") and "LeaveAll" in l)])


def m5(a, p6, p8):  # STREAM_STOP not counted in one cycle
    j = a / "cycles/cycle-050/snapshot-after.jsonl"
    rows = [json.loads(l) for l in j.read_text().splitlines()]
    for r in rows:
        if r.get("role") == "dut" and r.get("what") == "counter-6-1":
            b = bytearray.fromhex(r["response"]["payload"]); v = int.from_bytes(b[12:16], "big") - 1
            b[12:16] = v.to_bytes(4, "big"); r["response"]["payload"] = b.hex()
    j.write_text("".join(json.dumps(r) + "\n" for r in rows))


def m6(a, p6, p8):  # a pre-bind TA declaration planted in bind 3's window (not fresh)
    def f(lines):
        return lines[:3] + ["1.000000000\tDUT\tTalkerAdvertise\tJoinIn\t0200000000010001\tNone\n"] + lines[3:]
    edit_tsv(a / "bind/bind-3/msrp.tsv", f)


def m7(a, p6, p8):  # 606 page first-bind latency altered
    p6.write_text(p6.read_text().replace("| 0.126451 | PASS |", "| 0.126452 | PASS |", 1))


def m8(a, p6, p8):  # block-table median altered
    p8.write_text(p8.read_text().replace("| 41-50 | 10 | 0.013580 |", "| 41-50 | 10 | 0.013581 |", 1))


def m9(a, p6, p8):  # near-LeaveAll table class altered
    p8.write_text(p8.read_text().replace("| 35 | -0.099666 | IN (observed) |", "| 35 | -0.099666 | LV |", 1))


def m10(a, p6, p8):  # growth interval altered to exclude zero
    p8.write_text(p8.read_text().replace("+0.000069285]", "-0.000001000]", 1))


out = []
for name, fn in [("M1 re-declaration before cycle-22 Lv", m1), ("M2 IN cycle keeps streaming", m2), ("M3 page restart cell", m3),
                 ("M4 cycle-22 own LeaveAll removed", m4), ("M5 STREAM_STOP uncounted", m5), ("M6 pre-bind TA declaration", m6),
                 ("M7 606 page latency cell", m7), ("M8 block median cell", m8), ("M9 near-table class", m9),
                 ("M10 growth interval", m10)]:
    d = S / "mut"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(A, d / "author"); shutil.copy(P6, d / "606.md"); shutil.copy(P8, d / "608.md")
    fn(d / "author", d / "606.md", d / "608.md")
    r = subprocess.run([sys.executable, "-B", str(RD), str(d / "author"), str(d / "606.md"), str(d / "608.md")], capture_output=True, text=True, timeout=600)
    fl = [l for l in r.stdout.splitlines() if l.startswith("FAIL ")]
    crashed = r.returncode != 0
    detected = bool(fl) or crashed
    out.append(detected)
    print(f"{name}: {'DETECTED' if detected else 'MISSED'} ({len(fl)} FAIL lines{', crashed' if crashed else ''})")
    for l in fl[:3]:
        print("    ", l)
    if crashed:
        print("    ", (r.stderr.strip().splitlines() or [''])[-1])
shutil.rmtree(S / "mut")
print(f"\n{sum(out)} of {len(out)} planted defects detected")
