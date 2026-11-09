#!/usr/bin/env python3
"""Mutate the twin's MRP Applicant grade (twin_mrp.py) and judge each mutant with the twin's own captures.

usage: probe_mrp_mutants.py LEG_DIR OBJ_TWIN_DIR WORK_DIR

LEG_DIR is tb/verilator/milan_dp of a clean checkout, OBJ_TWIN_DIR the obj_twin directory make twin-plants
left (fabric.json, split.json, report.json and the planted captures). For each mutant the leg's Python is
copied to WORK_DIR/<mutant>, one edit applied (it must match exactly once), and the mutant is judged as
make twin and make twin-plants judge the head: CAUGHT when twin_compare.py exits non-zero on the unplanted
captures or any capture plant's control escapes, SURVIVED otherwise. The head itself is run first and must
be clean.
"""
import shutil
import subprocess
import sys
from pathlib import Path

LEG, OBJ, WORK = (Path(a).resolve() for a in sys.argv[1:4])
SPLIT_PLANTS = ["uncovered-field", "vanished-owed", "command-byte", "command-sequence", "response-sequence",
                "table-10-3", "received-join", "leave-all-declaration", "leave-all-omission", "mvrp-join-in", "mvrp-received-join"]
FABRIC_PLANTS = ["vanished-mvrp-leave-all", "vanished-available-index", "vanished-domain-new",
                 "domain-trace-moved", "vanished-vid2-join-in", "vid2-registrar-in"]
MUTANTS = {
    "head": None,
    "an-tx-sends-join": ('TX = (_row("[s] sJ sN sN sJ', 'TX = (_row("[s] sJ sN sJ sJ'),
    "vn-tx-sends-join": ('TX = (_row("[s] sJ sN sN sJ', 'TX = (_row("[s] sJ sJ sN sJ'),
    "an-note8-dropped": ('after = "QA" if registrar == "IN" else "AA"', 'after = "QA"'),
    "sj-ignores-registrar-mt": ('return "JoinIn" if registrar == "IN" else "JoinMt"', 'return "JoinMt"'),
    "sj-ignores-registrar-in": ('return "JoinIn" if registrar == "IN" else "JoinMt"', 'return "JoinIn"'),
    "msrp-milan-cell-dropped": ('REGISTRAR = {"MSRP": {**TABLE_10_4, "rLv!": {"IN": "MT"}}, "MVRP": TABLE_10_4}',
                                'REGISTRAR = {"MSRP": TABLE_10_4, "MVRP": TABLE_10_4}'),
    "mvrp-gets-milan-cell": ('"MVRP": TABLE_10_4}', '"MVRP": {**TABLE_10_4, "rLv!": {"IN": "MT"}}}'),
    "rjoinin-aa-stays": ('"rJoinIn!": _row("AO AP -  -  QA', '"rJoinIn!": _row("AO AP -  -  - '),
    "rnew-registrar-ignored": ('"rNew!": {"LV": "IN", "MT": "IN"},', '"rNew!": {},'),
    "rjoinin-registrar-ignored": ('"rJoinIn!": {"LV": "IN", "MT": "IN"},', '"rJoinIn!": {},'),
    "txla-qa-bracketed": ('TXLA = (_row("[s] s  sN sN sJ sJ', 'TXLA = (_row("[s] s  sN sN sJ [sJ]'),
    "txla-aa-sends-nothing": ('TXLA = (_row("[s] s  sN sN sJ sJ', 'TXLA = (_row("[s] s  sN sN [s] sJ'),
    "lv-row-dropped": ('"Lv!": _row("-  VO LA LA LA LA -  -  -  AO QO -"),', '"Lv!": _row("-  VO LA LA -  -  -  -  -  AO QO -"),'),
    "la-tx-sends-join": ('_row("[s] sJ sN sN sJ [sJ] sL', '_row("[s] sJ sN sN sJ [sJ] sJ'),
    "no-join-request": ('return ("Join!",)\n    return ()', 'return ()\n    return ()'),
    "split-p2p-false": ('OPER_P2P = {"all-fabric": True, "split": True}', 'OPER_P2P = {"all-fabric": True, "split": False}'),
    "periodic-dropped": ('"periodic!": _row("-  -  -  -  -  AA -  -  -  -  AP -"),', '"periodic!": _row("-  -  -  -  -  -  -  -  -  -  -  -"),'),
}


def run(tree: Path, *args: str) -> int:
    return subprocess.run([sys.executable, "-B", "twin_compare.py", *args], cwd=tree, capture_output=True,
                          text=True, check=False).returncode


def judge(tree: Path) -> list[str]:
    caught = []
    f, s, base = str(OBJ / "fabric.json"), str(OBJ / "split.json"), str(OBJ / "report.json")
    if run(tree, f, s) != 0:
        caught.append("make twin rc 1")
    for p in SPLIT_PLANTS:
        planted = str(OBJ / f"split-{p}.json")
        if run(tree, s, planted, "--plant", p, "--self") != 0:
            caught.append(f"{p} (self) escaped")
        if run(tree, f, planted, "--plant", p, "--baseline", base) != 0:
            caught.append(f"{p} escaped")
    for p in FABRIC_PLANTS:
        planted = str(OBJ / f"fabric-{p}.json")
        if run(tree, f, planted, "--plant", p, "--self") != 0:
            caught.append(f"{p} (self) escaped")
        if run(tree, planted, s, "--plant", p, "--baseline", base) != 0:
            caught.append(f"{p} escaped")
    return caught


def main() -> int:
    rc = 0
    for name, edit in MUTANTS.items():
        tree = WORK / name
        shutil.rmtree(tree, ignore_errors=True)
        tree.mkdir(parents=True)
        for py in LEG.glob("twin_*.py"):
            shutil.copy(py, tree / py.name)
        if edit:
            text = (tree / "twin_mrp.py").read_text()
            if text.count(edit[0]) != 1:
                print(f"{name}: edit does not match exactly once")
                rc = 2
                continue
            (tree / "twin_mrp.py").write_text(text.replace(edit[0], edit[1]))
        # twin_decode.py finds srp_wire_compare.py from its own path: point it at the checkout's
        dec = (tree / "twin_decode.py").read_text()
        dec = dec.replace('HERE.parents[2] / "sw/firmware/ctrl/test"', f'"{LEG.parents[2] / "sw/firmware/ctrl/test"}"')
        (tree / "twin_decode.py").write_text(dec)
        caught = judge(tree)
        if name == "head":
            print(f"head: {'CLEAN' if not caught else 'NOT CLEAN: ' + '; '.join(caught)}")
            rc = rc or (1 if caught else 0)
        else:
            print(f"{name}: {'CAUGHT by ' + '; '.join(caught[:4]) if caught else 'SURVIVED'}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
