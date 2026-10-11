#!/usr/bin/env python3
"""Reviewer-planted drifts against the AECP command gate.

Usage: python3 -I drifts.py HEAD_TREE WORK_DIR

HEAD_TREE is an export (git archive) of the reviewed head. Each drift is
applied to its own fresh copy under WORK_DIR; the gate
(scripts/check_aecp_commands.py) is run on that copy, and for the drifts marked
`make`, `make aecpcmd` too. Prints, per drift: name, gate rc, expected outcome,
and every gate output line. Exits 0 only when every drift behaves as expected.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

TABLE = "hdl/aecp/ucode/aecp_commands.json"
ENGINE = "hdl/aecp/KL_aecp_engine.sv"
DOC = "docs/architecture/06_aecp_engine.md"
GATE = "scripts/check_aecp_commands.py"


def edit_table(fn):
    def apply(root: Path):
        p = root / TABLE
        t = json.loads(p.read_text(encoding="utf-8"))
        fn(t)
        p.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return apply


def edit_text(path, old, new):
    def apply(root: Path):
        p = root / path
        s = p.read_text(encoding="utf-8")
        assert s.count(old) == 1, f"{old!r} occurs {s.count(old)} times in {path}"
        p.write_text(s.replace(old, new), encoding="utf-8")
    return apply


def write_doc(root: Path):
    """Regenerate F06.14 from the (drifted) table, as an author would."""
    r = subprocess.run([sys.executable, "-B", GATE, "--write"], cwd=root,
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def cmd(t, name):
    return next(c for c in t["commands"] if c["name"] == name)


def drop(t, name):
    t["commands"].remove(cmd(t, name))


def both(*fns):
    def apply(root):
        for f in fns:
            f(root)
    return apply


# (id, description, mutation, regenerate F06.14 first, expected rc, words that
#  must appear on one output line (None: expect a pass), also run make aecpcmd)
DRIFTS = [
    ("D1", "opcode renumbered in the table only: GET_COUNTERS 0x0029 -> 0x002A",
     edit_table(lambda t: cmd(t, "GET_COUNTERS").update(opcode="0x002A")), False, 1,
     ("engine: GET_COUNTERS: the table says opcode 0x002A", "OP_GET_COUNTERS_C = 0x0029"), True),
    ("D2", "size changed in the doc only: F06.14 row 0x0009 Resp. size 36 B (cdl 24) -> 40 B (cdl 28)",
     edit_text(DOC, "| 16 | 36 B (cdl 24) | SUCCESS, NO_SUCH_DESCRIPTOR, BAD_ARGUMENTS, NOT_SUPPORTED |",
               "| 16 | 40 B (cdl 28) | SUCCESS, NO_SUCH_DESCRIPTOR, BAD_ARGUMENTS, NOT_SUPPORTED |"),
     False, 1, ("F06.14: row 0x0009 GET_STREAM_FORMAT, column Resp. size", "40 B (cdl 28)"), False),
    ("D3", "OP_*_C changed in the RTL only: OP_SET_NAME_C 16'h0010 -> 16'h0012",
     edit_text(ENGINE, "OP_SET_NAME_C         = 16'h0010;", "OP_SET_NAME_C         = 16'h0012;"),
     False, 1, ("engine: SET_NAME: the table says opcode 0x0010", "OP_SET_NAME_C = 0x0012"), True),
    ("D4", "command missing from the table: IDENTIFY_NOTIFICATION row deleted, F06.14 regenerated",
     edit_table(lambda t: drop(t, "IDENTIFY_NOTIFICATION")), True, 1,
     ("OP_IDENTIFY_NOTIF_C = 0x0026 and the table has no command",), False),
    ("D5", "unrepresentable message type: SET_CONTROL message AEM -> AA",
     edit_table(lambda t: cmd(t, "SET_CONTROL").update(message="AA")), False, 1,
     ("schema: SET_CONTROL: message 'AA' is neither AEM nor MVU",), False),
    ("D5w", "unrepresentable message type refused by --write too (rc 1, no traceback)",
     edit_table(lambda t: cmd(t, "SET_CONTROL").update(message="AA")), "write-only", 1,
     ("schema: SET_CONTROL: message 'AA' is neither AEM nor MVU",), False),
    ("D6", "ROM-only drift: GET_SAMPLING_RATE status set loses NOT_SUPPORTED in the table",
     edit_table(lambda t: cmd(t, "GET_SAMPLING_RATE")["status"].remove("NOT_SUPPORTED")), True, 1,
     ("rom: GET_SAMPLING_RATE: status NOT_SUPPORTED is answered",), False),
    ("D7", "lock flag set on a read: GET_NAME lock false -> true, F06.14 regenerated",
     edit_table(lambda t: cmd(t, "GET_NAME").update(lock=True)), True, 1,
     ("GET_NAME", "lock true"), False),
    # probes of what the gate does NOT hold (expected to pass: these measure scope)
    ("P1", "PROBE echo response size changed in the table, F06.14 regenerated: SET_STREAM_INFO response cdl 96 -> 60",
     edit_table(lambda t: cmd(t, "SET_STREAM_INFO")["response"].update(cdl=60)), True, 1,
     ("rom: SET_STREAM_INFO: E_SIBAD answers BAD_ARGUMENTS at cdl 96",), False),
    ("P2", "PROBE echo response size changed in the table, F06.14 regenerated: ACQUIRE_ENTITY response cdl 28 -> 40",
     edit_table(lambda t: cmd(t, "ACQUIRE_ENTITY")["response"].update(cdl=40)), True, 0, None, False),
    ("P3", "PROBE command size changed in the table, F06.14 regenerated: SET_SAMPLING_RATE command cdl 20 -> 24",
     edit_table(lambda t: cmd(t, "SET_SAMPLING_RATE")["command"].update(cdl=24)), True, 0, None, False),
    ("P4", "PROBE status code with no RTL constant changed in the table: STREAM_IS_RUNNING 12 -> 13",
     edit_table(lambda t: t["status_codes"]["STREAM_IS_RUNNING"].update(code=13)), False, 0, None, False),
    ("P5", "PROBE documented row without its name field: refusal or traceback?",
     edit_table(lambda t: t["documented"][0].pop("name")), False, "nonzero", None, False),
]


def run(tree: Path, work: Path):
    work.mkdir(parents=True, exist_ok=True)
    bad = 0
    for did, what, fn, regen, want_rc, words, mk in DRIFTS:
        d = work / did
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(tree, d, symlinks=True)
        clean = subprocess.run([sys.executable, "-B", GATE], cwd=d, capture_output=True, text=True)
        fn(d)
        notes = []
        if regen == "write-only":
            rc, out = write_doc(d)
        else:
            if regen:
                wrc, wout = write_doc(d)
                notes.append(f"--write rc {wrc}: {wout.strip()}")
            r = subprocess.run([sys.executable, "-B", GATE], cwd=d, capture_output=True, text=True)
            rc, out = r.returncode, r.stdout + r.stderr
        ok = (rc != 0) if want_rc == "nonzero" else (rc == want_rc)
        if words is not None:
            ok = ok and any(all(w in line for w in words) for line in out.splitlines())
        verdict = "AS EXPECTED" if ok and clean.returncode == 0 else "UNEXPECTED"
        bad += verdict != "AS EXPECTED"
        print(f"=== {did}: {what}")
        print(f"unplanted copy gate rc {clean.returncode}; planted gate rc {rc}; "
              f"expected rc {want_rc}; words {words}; {verdict}")
        for n in notes:
            print(f"  {n}")
        for line in out.rstrip().splitlines():
            print(f"  | {line}")
        if mk:
            m = subprocess.run(["make", "aecpcmd"], cwd=d, capture_output=True, text=True)
            print(f"  make aecpcmd rc {m.returncode}")
            for line in (m.stdout + m.stderr).rstrip().splitlines()[-4:]:
                print(f"  make| {re.sub(str(d), '<copy>', line)}")
        shutil.rmtree(d)
    print(f"drifts: {len(DRIFTS)} run, {len(DRIFTS) - bad} as expected")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()))
