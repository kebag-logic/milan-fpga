#!/usr/bin/env python3
"""R602-6 independent probe of #671 round 6 (PR #715 at c7d0ad63).

Run from a checkout of the head under review:
    python3 probe_terms.py <repo> <workdir> [--jobs N] [--part terms|controls|all]

part "terms": compiles the shipped firmware with one print added at the end of
nvm_read_slot (each read's verdict, byte count, prefix CRC and trailer), runs
the faulty boot (or writer restart) of every comparison-term class case on the
first shape and both product shapes, and requires the faulted slot's judgement
to be exactly: two refusals that differ in the case's own term and agree in the
other three, then a VD_OK read.

part "controls": grades every term-class case in full (the gate's own
grade_fault_case: read count, hold, window, changed and other records) on the
shipped firmware and on each mutant below, on all three shapes, and counts the
findings each class raises and whether they carry the class's own words.
Mutants: the four named r_omit_ controls, plus reviewer-written variants that
break a term in its computation rather than in the comparison.
Exit 0 when every expectation holds, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("work", type=Path)
ap.add_argument("--jobs", type=int, default=8)
ap.add_argument("--part", default="all")
a = ap.parse_args()
sys.path.insert(0, str(a.repo / "sw/firmware/nvm_hosttest"))
sys.argv = [sys.argv[0]]
import test_nvm_firmware as T  # noqa: E402
import read_fault_cases as R   # noqa: E402

SHAPES = ("endstation_arty_4x4", "endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8")
FW = (a.repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
END_OF_READ = ("\t\trd.tail = nvm_rd32(NVM_STG + rd.bytes - KLJ2_TRAILER);\n\t}\n\treturn rd;\n}\n")
assert FW.count(END_OF_READ) == 1
PROBE_FW = FW.replace(END_OF_READ, END_OF_READ.replace(
    "\treturn rd;\n",
    '\tprintf("PROBE slot=%lx vd=%u bytes=%lx digest=%08lx tail=%08lx\\n", (unsigned long)slot, '
    'rd.vd, (unsigned long)rd.bytes, (unsigned long)rd.digest, (unsigned long)rd.tail);\n\treturn rd;\n'))
PROBE_RE = re.compile(r"^PROBE slot=(\w+) vd=(\d+) bytes=(\w+) digest=(\w+) tail=(\w+)$", re.M)
FIELD = {"verdict": 1, "byte count": 2, "prefix CRC": 3, "trailer": 4}

# reviewer-written mutants: (label, [(old, new)], class whose words must catch it)
EXTRA = [
    ("x_tail_from_prefix", [("rd.tail = nvm_rd32(NVM_STG + rd.bytes - KLJ2_TRAILER);",
                             "rd.tail = nvm_rd32(NVM_STG + rd.bytes - 2u * KLJ2_TRAILER);")], "trailer"),
    ("x_digest_short", [("rd.digest = nvm_crc32(NVM_STG, rd.bytes - KLJ2_TRAILER);",
                         "rd.digest = nvm_crc32(NVM_STG, rd.bytes - 2u * KLJ2_TRAILER);")], "prefix CRC"),
    ("x_digest_header_only", [("rd.digest = nvm_crc32(NVM_STG, rd.bytes - KLJ2_TRAILER);",
                               "rd.digest = nvm_crc32(NVM_STG, KLJ2_HDR);")], "prefix CRC"),
    ("x_verdict_class_only", [("return a.vd == b.vd && ",
                               "return (a.vd == VD_BLANK) == (b.vd == VD_BLANK) && ")], "verdict"),
    ("x_bytes_from_header_const", [("return a.vd == b.vd && a.bytes == b.bytes && ",
                                    "return a.vd == b.vd && (a.bytes > 0u) == (b.bytes > 0u) && ")],
     "byte count"),
]


def cfg(stem: str) -> Path:
    return a.repo / "configs" / f"{stem}.yaml"


def term_cases(bench) -> list:
    body = T.KLJ2_HDR + (bench.img_len - T.KLJ2_HDR - T.KLJ2_TRAILER) // 2
    return [c for c in R.fault_cases(body) if R.term_of(c)]


def faulty_boot_text(bench, fr, case, w: Path) -> str:
    newer = fr.containers[(case.seq, False)]
    other = fr.containers[(case.seq, True)] if case.older else b"\xff" * T.SLOT
    slots = {case.valid.upper(): newer, case.other.upper(): other}
    (w / "a.bin").write_bytes(slots["A"])
    (w / "b.bin").write_bytes(slots["B"])
    base = ("--slot-a", str(w / "a.bin"), "--slot-b", str(w / "b.bin"))
    if case.restart:
        out, _, _ = T.run(bench, *base, "--boot", "--idle-ms", "100", *case.fault, "--restart")
        return out.split("HOST restarting\n", 1)[1].split("HOST restarted\n", 1)[0]
    out, _, _ = T.run(bench, *base, *case.fault, "--boot")
    return out


def judgement(text: str, slot_off: int) -> list[tuple]:
    reads = [m.groups() for m in PROBE_RE.finditer(text)]
    run, started = [], False
    for r in reads:
        if int(r[0], 16) == slot_off:
            run.append(r)
            started = True
            if r[1] == "0":
                break          # a judgement ends at its first VD_OK read; a re-stage may follow it
        elif started:
            break
    return run


def part_terms(out: dict) -> list[str]:
    f = []
    for stem in SHAPES:
        w = a.work / "terms" / stem
        w.mkdir(parents=True, exist_ok=True)
        bench = T.make_bench(cfg(stem), w, PROBE_FW)
        fr = T.fault_run(bench)
        cases = term_cases(bench)
        journal = T.JOURNAL

        def one(i: int):
            c = cases[i]
            d = w / f"c{i}"
            d.mkdir(exist_ok=True)
            slot_off = journal + (0x10000 if c.fault[1][0] == "b" else 0)
            j = judgement(faulty_boot_text(bench, fr, c, d), slot_off)
            term = R.term_of(c)
            bad = []
            if len(j) != 3 or j[2][1] != "0" or j[0][1] == "0" or j[1][1] == "0":
                bad.append(f"{stem}: {c.name}: judgement is not refusal, refusal, VD_OK: {j}")
            else:
                diff = [t for t, k in FIELD.items() if j[0][k] != j[1][k]]
                if diff != [term]:
                    bad.append(f"{stem}: {c.name}: the two refusals differ in {diff}, want only [{term!r}]: {j}")
            return term, c.restart, bad, j

        with ThreadPoolExecutor(a.jobs) as pool:
            res = list(pool.map(one, range(len(cases))))
        per = {}
        for term, restart, bad, j in res:
            per.setdefault(term, [0, 0])[int(restart)] += 1
            f += bad
        out.setdefault("terms", {})[stem] = {"cases": len(cases), "per_term_cold_restart": per,
                                             "bad": sum(len(b) for _, _, b, _ in res),
                                             "sample": {t: next(jj for tt, _, _, jj in res if tt == t)
                                                        for t in FIELD}}
        print(f"terms {stem}: {len(cases)} class cases, per term [cold, restart] {per}, "
              f"bad {out['terms'][stem]['bad']}", flush=True)
        for t in FIELD:
            if per.get(t, [0, 0]) != [16, 16]:
                f.append(f"{stem}: class {t} has {per.get(t)} cases, want 16 cold and 16 restart")
    return f


def mutants() -> list[tuple[str, list, str]]:
    m = [(R.control_of(term), list(R.READ_FAULT_MUTATIONS[R.control_of(term)][0]), term)
         for term, _, _ in R.COMPARISON]
    return [("shipped", [], "")] + m + EXTRA


def part_controls(out: dict) -> list[str]:
    f = []
    for stem in SHAPES:
        w0 = a.work / "controls" / stem
        w0.mkdir(parents=True, exist_ok=True)
        base = T.make_bench(cfg(stem), w0 / "base", FW)
        fr = T.fault_run(base)
        cases = term_cases(base)
        for label, pairs, want_term in mutants():
            text = FW
            for old, new in pairs:
                assert text.count(old) == 1, (label, old)
                text = text.replace(old, new)
            bench = base if label == "shipped" else T.replant(base, w0 / label, text)

            def one(i: int):
                d = (w0 / label / f"c{i}") if label != "shipped" else (w0 / "base" / f"c{i}")
                d.mkdir(parents=True, exist_ok=True)
                return R.term_of(cases[i]), T.grade_fault_case(bench, fr, cases[i], d, None)

            with ThreadPoolExecutor(a.jobs) as pool:
                res = list(pool.map(one, range(len(cases))))
            count = {t: [0, 0] for t in FIELD}   # [cases with any finding, cases with own-words finding]
            for term, got in res:
                count[term][0] += bool(got)
                count[term][1] += any(R.alone_in(term) in g for g in got)
            out.setdefault("controls", {}).setdefault(stem, {})[label] = count
            print(f"controls {stem} {label}: {count}", flush=True)
            for t in FIELD:
                want = [32, 32] if t == want_term else [0, 0]
                if label in [x[0] for x in EXTRA]:
                    # a reviewer variant must at least be named by its own class
                    ok = count[t][1] > 0 if t == want_term else True
                else:
                    ok = count[t] == want
                if not ok:
                    f.append(f"{stem}: {label}: class {t} gave {count[t]} (cases with findings, named), "
                             f"want {want if label not in [x[0] for x in EXTRA] else 'named > 0'}")
    return f


out: dict = {}
findings = []
if a.part in ("terms", "all"):
    findings += part_terms(out)
if a.part in ("controls", "all"):
    findings += part_controls(out)
(a.work / f"probe_{a.part}.json").write_text(json.dumps(out, indent=1, default=str))
for x in findings:
    print("FINDING:", x)
print(f"probe {a.part}: {'OK' if not findings else f'{len(findings)} finding(s)'}")
sys.exit(1 if findings else 0)
