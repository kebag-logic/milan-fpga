#!/usr/bin/env python3
"""Dump gate 1b's accepted cases and mutation rows, then stop (R317-1).

Run from the root of a milan-fpga tree (the head checkout, or an extracted
base tree). The tree's own sw/builder/test_builder.py is executed with a hook
at its accepted-case loop and at its mutation loop; each row is recorded as
(label, sha256 of every str field, reason pin) and the gate returns before
grading the mutations. The head run's grading is measured separately by the
full gate 1b run; this compares row identity only.

    python3 -B PACKET/dump_rows.py --mode sdk --sdk SDK --out FILE.json
    python3 -B PACKET/dump_rows.py --mode absent --out FILE.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=("sdk", "absent"), required=True)
parser.add_argument("--sdk")
parser.add_argument("--out", required=True)
parser.add_argument("--gate-source",
                    help="execute this test_builder.py text (e.g. the base "
                         "revision's) against the tree in the cwd")
args = parser.parse_args()
root = Path.cwd()
sys.path.insert(0, str(root / "sw/builder"))
import test_firmware_compiler as tfc  # noqa: E402

sdk_dir = Path(args.sdk) if args.mode == "sdk" else None
if sdk_dir:
    tfc.sdk.verify(sdk_dir)
path = root / "sw/builder/test_builder.py"
gate = Path(args.gate_source) if args.gate_source else path
source = gate.read_text()
acc = "    for label, accepted in accepted_cases.items():\n"
mut = "    for mutation in mutations:\n        assert_rejected(*mutation)\n"
assert source.count(acc) == 1 and source.count(mut) == 1
source = source.replace(acc, "    dump_accepted(accepted_cases)\n" + acc)
source = source.replace(mut, "    dump_mutations(mutations)\n    return\n" + mut)
out = {"gate_source_sha256": hashlib.sha256(gate.read_bytes()).hexdigest()}


def digest(value):
    if isinstance(value, str):
        return hashlib.sha256(value.encode("utf-8", "surrogatepass")).hexdigest()[:16]
    return repr(value)


def dump_accepted(cases):
    out["accepted"] = [[label, digest(text)] for label, text in cases.items()]


def dump_mutations(rows):
    out["mutations"] = [[row[0]] + [digest(v) for v in row[1:]] for row in rows]


with open(Path(args.out).with_suffix(".argv.jsonl"), "w") as stream:
    audit = tfc.CompilerAudit(stream, sdk_dir)
    argv = [str(path)] + (["--require-rv32"] if sdk_dir else [])
    with patch.object(subprocess, "run", side_effect=audit.invoke), \
            patch.object(sys, "argv", argv):
        module = types.ModuleType("test_builder_dump")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        module.dump_accepted = dump_accepted
        module.dump_mutations = dump_mutations
        exec(compile(source, str(path), "exec"), module.__dict__)
        with tempfile.TemporaryDirectory(prefix="r317-dump-") as tmp:
            module.OUT = Path(tmp)
            module.SKIPPED = []
            module.test_baremetal_profile_contract()
Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
print(args.out, len(out.get("accepted", [])), "accepted,",
      len(out.get("mutations", [])), "mutations")
