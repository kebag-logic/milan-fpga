#!/usr/bin/env python3
"""Independent command-model mutation, generation, and incremental-build probes."""
import argparse
import copy
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--packet", type=Path, required=True)
    a = ap.parse_args()
    a.root, a.packet = a.root.resolve(), a.packet.resolve()
    scratch = a.packet / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    (a.packet / "receipts").mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(scratch)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(a.root / "scripts"))
    from aecp_gate.inputs import load, ucode_of, DOC, TABLE, ENGINE
    from aecp_gate.gate import check
    from aecp_gate.doc import regenerated
    from aecp_gate.rom import check_rom
    from aecp_gate.plants import rom_op
    base = load(a.root)
    assert not check(base)
    ucode_of(base)
    records = []

    def record(name, findings, expected):
        ok = any(expected in f for f in findings)
        records.append({"probe": name, "detected": ok, "findings": findings})
        print(json.dumps(records[-1]), flush=True)
        assert ok, name

    for field in ("command", "response"):
        for j, original in enumerate(base.table["commands"]):
            inp = copy.deepcopy(base)
            inp.table["commands"][j][field]["cdl"] += 4
            inp.texts[DOC] = regenerated(inp.table, inp.texts[DOC])
            found = check(inp)
            # A regenerated doc cannot be the sole detection.
            assert all("F06.14" not in f for f in found)
            record(field + ":" + original["name"], found, original["name"])
    for entry in ("GAMAP", "GAVB", "GASP", "RDESC", "GSTRI", "GCTRS"):
        for op in ("BUILD_FLD", "APPEND"):
            inp = copy.deepcopy(base)
            try:
                at = rom_op(inp, entry, op)
            except Exception:
                continue
            inp.ucode.rom[at] = 0
            # Check the semantic walk itself, independent of the ROM digest.
            record(f"ROM:{entry}:{op}@{at}", check_rom(inp.table, inp.ucode), "rom:")
    for cdl in (20, 28):
        inp = copy.deepcopy(base)
        next(c for c in inp.table["commands"] if c["name"] == "GET_AUDIO_MAP")["response"]["cdl"] = cdl
        inp.texts[DOC] = regenerated(inp.table, inp.texts[DOC])
        record(f"GET_AUDIO_MAP:{cdl}", check(inp), "rom: GET_AUDIO_MAP")

    tree = scratch / "file-probes"
    tree.mkdir()
    raw = subprocess.check_output(["git", "archive", "HEAD"], cwd=a.root)
    with tarfile.open(fileobj=io.BytesIO(raw)) as tf:
        tf.extractall(tree, filter="data")
    def gate():
        p = subprocess.run([sys.executable, "-B", "scripts/check_aecp_commands.py"], cwd=tree,
                           text=True, capture_output=True)
        return p.returncode, p.stdout + p.stderr
    table_path = tree / TABLE
    table_bytes = table_path.read_bytes()
    engine_path = tree / ENGINE
    engine_bytes = engine_path.read_bytes()
    doc_path = tree / DOC
    doc_bytes = doc_path.read_bytes()
    for name in ("opcode", "doc-size", "rtl-opcode", "missing-command", "mvu-message", "unplaced-entry"):
        t = json.loads(table_bytes)
        by_name = {c["name"]: c for c in t["commands"]}
        expected = "GET_COUNTERS"
        if name == "opcode": by_name[expected]["opcode"] = "0x007E"
        elif name == "doc-size":
            doc_path.write_bytes(doc_bytes.replace(b"160 B (cdl 148)", b"164 B (cdl 152)"))
        elif name == "rtl-opcode":
            old = b"OP_GET_COUNTERS_C    = 16'h0029;"
            assert engine_bytes.count(old) == 1
            engine_path.write_bytes(engine_bytes.replace(old, b"OP_GET_COUNTERS_C    = 16'h007E;"))
        elif name == "missing-command": t["commands"].remove(by_name[expected])
        elif name == "mvu-message":
            expected = "GET_MILAN_INFO"
            by_name[expected]["message"] = "AAU"
        elif name == "unplaced-entry":
            expected = "GET_CLOCK_SOURCE"
            by_name[expected]["entries"].append("SCFGRUN2")
        table_path.write_text(json.dumps(t))
        rc, out = gate()
        print(f"FILE {name} rc={rc}\n{out}")
        assert rc == 1 and expected in out and "Traceback" not in out
        if name == "unplaced-entry":
            p = subprocess.run([sys.executable, "-O", "hdl/aecp/ucode/gen_ucode.py"], cwd=tree,
                               text=True, capture_output=True)
            print(f"OPTIMIZED GENERATOR rc={p.returncode}\n{p.stdout}{p.stderr}")
            assert p.returncode != 0 and expected in p.stdout + p.stderr
        table_path.write_bytes(table_bytes)
        engine_path.write_bytes(engine_bytes)
        doc_path.write_bytes(doc_bytes)

    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for suite in ("pp_top", "ucpu", "aecp_cmds"):
        cwd = tree / "tb" / suite
        subprocess.run(["make", "-j16", "ucode.hex"], cwd=cwd, env=env, check=True)
        before = hashlib.sha256((cwd / "ucode.hex").read_bytes()).hexdigest()
        t = json.loads(table_bytes)
        t["status_codes"]["STREAM_IS_RUNNING"]["code"] = 13
        table_path.write_text(json.dumps(t))
        # Explicit mtime advance makes the dependency test independent of filesystem granularity.
        stat = (cwd / "ucode.hex").stat()
        os.utime(table_path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000))
        q = subprocess.run(["make", "-q", "ucode.hex"], cwd=cwd, env=env)
        assert q.returncode == 1
        subprocess.run(["make", "-j16", "ucode.hex"], cwd=cwd, env=env, check=True)
        after = hashlib.sha256((cwd / "ucode.hex").read_bytes()).hexdigest()
        print(f"PREREQUISITE {suite}: query={q.returncode}, before={before}, after={after}")
        assert before != after
        table_path.write_bytes(table_bytes)
    print("PROBE CONTRACT PASS: 62 size drifts, variable/fixed ROM controls, four acceptance file drifts, two generator input refusals, optimized-interpreter refusal, three incremental rules")
    (a.packet / "receipts/contract-results.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
