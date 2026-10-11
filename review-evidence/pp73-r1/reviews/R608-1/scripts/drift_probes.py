#!/usr/bin/env python3
"""Independent planted-drift probes against scripts/check_aecp_commands.py.

usage: python3 -I drift_probes.py <clean-head-export> <scratch-dir> <receipt-dir>

Each probe copies the clean export to <scratch-dir>/<probe>, applies ONE exact
string edit (refusing if the anchor is not unique), runs the gate there and
records rc and output in <receipt-dir>/<probe>.txt. The clean export itself is
never edited. A probe's expectation is printed beside its result; the reviewer
judges, the script only records.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

SRC, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:4])
TABLE = "hdl/aecp/ucode/aecp_commands.json"
ENGINE = "hdl/aecp/KL_aecp_engine.sv"
DOC = "docs/architecture/06_aecp_engine.md"
GEN = "hdl/aecp/ucode/gen_ucode.py"


def edit(root, path, old, new):
    p = root / path
    t = p.read_text(encoding="utf-8")
    if t.count(old) != 1:
        raise SystemExit(f"anchor not unique in {path}: {old!r} x{t.count(old)}")
    p.write_text(t.replace(old, new), encoding="utf-8")


def table_edit(root, fn):
    p = root / TABLE
    t = json.loads(p.read_text(encoding="utf-8"))
    fn(t)
    p.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd(t, name):
    return next(c for c in t["commands"] if c["name"] == name)


PROBES = [
    # (name, expectation, mutation, extra command or None)
    ("p0_clean", "rc 0", lambda r: None, None),
    ("p1_table_opcode_SET_NAME", "rc 1, names SET_NAME and OP_SET_NAME_C",
     lambda r: table_edit(r, lambda t: cmd(t, "SET_NAME").update(opcode="0x0012")), None),
    ("p2_doc_size_GET_COUNTERS", "rc 1, names row 0x0029 GET_COUNTERS column Resp. size",
     lambda r: edit(r, DOC, "| 160 B (cdl 148) |", "| 164 B (cdl 152) |"), None),
    ("p3_rtl_OP_GET_COUNTERS", "rc 1, names GET_COUNTERS and OP_GET_COUNTERS_C = 0x002A",
     lambda r: edit(r, ENGINE, "OP_GET_COUNTERS_C    = 16'h0029;",
                    "OP_GET_COUNTERS_C    = 16'h002A;"), None),
    ("p4_missing_START_STREAMING", "rc 1, names OP_START_STRM_C and no command",
     lambda r: table_edit(r, lambda t: t["commands"].remove(cmd(t, "START_STREAMING"))), None),
    ("p5_message_type_ADDRESS_ACCESS", "rc 1, schema finding names GET_MILAN_INFO message",
     lambda r: table_edit(r, lambda t: cmd(t, "GET_MILAN_INFO").update(message="AA")), None),
    ("p5b_message_type_write", "--write refuses (rc 1, schema line), F06.14 untouched",
     lambda r: table_edit(r, lambda t: cmd(t, "GET_MILAN_INFO").update(message="AA")),
     ["python3", "-B", "scripts/check_aecp_commands.py", "--write"]),
    ("p6_make_aecpcmd_table_opcode", "make aecpcmd rc 2 (selftest passes, gate rc 1)",
     lambda r: table_edit(r, lambda t: cmd(t, "SET_NAME").update(opcode="0x0012")),
     ["make", "aecpcmd"]),
    ("p7_generator_status_source", "rc 1, rom finding for SET_CONFIGURATION status",
     lambda r: edit(r, GEN, "ST_STRMRUN = _ST['STREAM_IS_RUNNING']",
                    "ST_STRMRUN = _ST['NO_RESOURCES']"), None),
    # coverage probes: the engine's per-command dispatch arm and opcode decode
    ("q1_dispatch_arm_SET_CLOCK_SOURCE_to_GCLKS",
     "a lock-protected command dispatched to an unlocked program: does the gate see it?",
     lambda r: edit(r, ENGINE, "else                                    upc_r <= UPC_SCLKS_C;",
                    "else                                    upc_r <= UPC_GCLKS_C;"), None),
    ("q2_decode_sclks_on_GET_opcode",
     "SET_CLOCK_SOURCE's decode keyed on another OP_*_C: does the gate see it?",
     lambda r: edit(r, ENGINE, "&& (txn_w.opcode == OP_SET_CLOCK_SRC_C);",
                    "&& (txn_w.opcode == OP_GET_CLOCK_SRC_C);"), None),
    ("q3_write_idempotent", "--write on the clean tree reports current, no byte change",
     lambda r: None, ["python3", "-B", "scripts/check_aecp_commands.py", "--write"]),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []
    for name, expect, fn, extra in PROBES:
        d = SCRATCH / name
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(SRC, d, symlinks=True)
        fn(d)
        doc_before = (d / DOC).read_bytes()
        argv = extra or ["python3", "-B", "scripts/check_aecp_commands.py"]
        r = subprocess.run(argv, cwd=d, capture_output=True, text=True)
        doc_same = (d / DOC).read_bytes() == doc_before
        body = (f"probe: {name}\nexpect: {expect}\ncommand: {' '.join(argv)}\n"
                f"rc: {r.returncode}\nF06.14 doc bytes unchanged by the run: {doc_same}\n"
                f"--- stdout\n{r.stdout}--- stderr\n{r.stderr}")
        (OUT / f"{name}.txt").write_text(body, encoding="utf-8")
        summary.append(f"{name}\trc={r.returncode}\tdoc_unchanged={doc_same}")
    (OUT / "SUMMARY.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))


main()
