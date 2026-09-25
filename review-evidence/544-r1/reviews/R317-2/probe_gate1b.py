#!/usr/bin/env python3
"""Grade firmware variants through gate 1b's own assert_boot_contract().

Portable reviewer probe (R317-1, issue #544 / PR #558). Run from the root of a
milan-fpga checkout:

    python3 -B PACKET/probe_gate1b.py --mode sdk --sdk SDK_DIR --rev head --tag T
    python3 -B PACKET/probe_gate1b.py --mode absent --rev base --tag T
    ... [--disconnect]  replace the #544 check of that mode with a no-op

--rev head reads the checkout's sw/builder/test_builder.py; --rev base reads
it from BASE (git show). The SDK is mapped onto the gate's absolute selector
argv[0] only, through the checkout's own CompilerAudit; --mode absent hides
every cross candidate and asserts no firmware compile happened. A hook is
inserted before `subset_note = assert_subset_refuses()`, grades every case in
cases_544.py and returns, so the full gate bank is NOT run. Output: one JSON
line per case to stdout and OUTDIR/<tag>.json.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch

BASE = "ffcbd33de70278ae34b533dcbadde0b36c8cba13"
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=("sdk", "absent"), required=True)
parser.add_argument("--sdk")
parser.add_argument("--rev", choices=("head", "base"), required=True)
parser.add_argument("--disconnect", action="store_true")
parser.add_argument("--only", default="")
parser.add_argument("--tag", required=True)
parser.add_argument("--outdir", required=True)
args = parser.parse_args()
root = Path.cwd()
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
sys.path.insert(0, str(root / "sw/builder"))
import cases_544  # noqa: E402
import test_firmware_compiler as tfc  # noqa: E402

sdk_dir = Path(args.sdk) if args.mode == "sdk" else None
if sdk_dir:
    tfc.sdk.verify(sdk_dir)
path = root / "sw/builder/test_builder.py"
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                      text=True, check=True).stdout.strip()
if args.rev == "base":
    source = subprocess.run(["git", "show", f"{BASE}:sw/builder/test_builder.py"],
                            capture_output=True, text=True, check=True).stdout
else:
    source = path.read_text()
marker = "    subset_note = assert_subset_refuses()"
assert source.count(marker) == 1
source = source.replace(marker, "    probe_hook(locals())\n    return\n" + marker)
results = []
audit_log = Path(args.outdir) / f"{args.tag}-argv.jsonl"


def probe_hook(ns):
    contract = ns["assert_boot_contract"]
    if args.disconnect:
        name = ("assert_identity_macro_free" if args.mode == "absent"
                else "assert_preprocessed_identity_sample")
        cells = dict(zip(contract.__code__.co_freevars, contract.__closure__))
        assert name in cells, (name, sorted(cells))
        cells[name].cell_contents = lambda *a, **k: None
    fw = ns["firmware_source"]
    for label, firmware in cases_544.build(fw):
        if args.only and args.only not in label:
            continue
        assert firmware != fw or label.startswith("CTRL unchanged"), label
        try:
            contract(firmware, ns["docs_source"], ns["csr_source"])
        except (AssertionError, ValueError) as exc:
            row = dict(label=label, verdict="REFUSED",
                       reason=str(exc).splitlines()[0][:400])
        else:
            row = dict(label=label, verdict="ACCEPTED")
        results.append(row)
        print(json.dumps(row), flush=True)


with audit_log.open("w") as stream:
    audit = tfc.CompilerAudit(stream, sdk_dir)
    argv = [str(path)] + (["--require-rv32"] if sdk_dir else [])
    with patch.object(subprocess, "run", side_effect=audit.invoke), \
            patch.object(sys, "argv", argv):
        module = types.ModuleType("test_builder_probe")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        module.probe_hook = probe_hook
        exec(compile(source, str(path), "exec"), module.__dict__)
        with tempfile.TemporaryDirectory(prefix="r317-probe-") as tmp:
            module.OUT = Path(tmp)
            module.SKIPPED = []
            module.test_baremetal_profile_contract()
    summary = dict(head=head, rev=args.rev, mode=args.mode,
                   disconnect=args.disconnect, compiles=audit.compiles,
                   hidden=sorted(audit.hidden))
    if sdk_dir is None:
        assert audit.compiles == 0, "absent mode compiled firmware"
    else:
        assert audit.compiles > 0, "SDK mode compiled nothing"
print("SUMMARY " + json.dumps(summary), flush=True)
(Path(args.outdir) / f"{args.tag}.json").write_text(
    json.dumps(dict(summary=summary, rows=results), indent=2) + "\n")
