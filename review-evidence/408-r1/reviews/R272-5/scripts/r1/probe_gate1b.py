#!/usr/bin/env python3
"""Grade firmware variants through gate 1b's own assert_boot_contract().

The gate source at <tree>/sw/builder/test_builder.py is executed IN MEMORY
with one hook inserted immediately before the accepted-case loop (or,
with --anchor mutations, before the mutation-table loop), so every
rule, instrument and closure the gate defines is the tree's own. Optional
--patch files apply exact, count-checked string replacements to that
in-memory source first (used to DISCONNECT one instrument). No file in
<tree> is written. The compiler environment is the one
sw/builder/test_firmware_compiler.py builds: the pinned SDK mapped onto the
absolute selector (--sdk), or every cross candidate hidden (--absent).

Usage:
  probe_gate1b.py --tree <repo> (--sdk <sdk-dir> | --absent) \
      --cases <cases.py> --out <results.json> [--patch <patch.json> ...]

<cases.py> defines cases(ns) -> iterable of dicts with keys `label`,
`firmware` and optionally `listing`, `makefile`, `datapath` (passed to
assert_boot_contract) and `because` (a str or list of str: the reasons the
refusal must ALL carry, reported as pin_ok). ns is the gate function's
locals() at the hook. A patch file is a JSON list of [old, new] pairs, each
old string required to occur exactly once.
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from unittest.mock import patch

ANCHORS = {
    "accepted": "    for label, accepted in accepted_cases.items():\n",
    "mutations": "    for mutation in mutations:\n        assert_rejected(*mutation)\n",
}
HOOK = ("    if _R272_PROBE is not None:\n"
        "        return _R272_PROBE(locals())\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--sdk", type=Path)
    mode.add_argument("--absent", action="store_true")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--patch", type=Path, action="append", default=[])
    parser.add_argument("--anchor", choices=sorted(ANCHORS), default="accepted")
    args = parser.parse_args()

    tree = args.tree.resolve()
    builder_path = tree / "sw/builder/test_builder.py"
    source = builder_path.read_text(encoding="utf-8")
    applied = []
    for patch_file in args.patch:
        for old, new in json.loads(patch_file.read_text(encoding="utf-8")):
            assert source.count(old) == 1, \
                f"{patch_file}: patch anchor occurs {source.count(old)} times"
            source = source.replace(old, new, 1)
            applied.append(str(patch_file))
    anchor = ANCHORS[args.anchor]
    assert source.count(anchor) == 1, "hook anchor not found exactly once"
    source = source.replace(anchor, HOOK + anchor, 1)
    sys.path.insert(0, str(tree / "scripts"))
    sys.path.insert(0, str(tree / "sw/builder"))

    spec = importlib.util.spec_from_file_location("r272_cases", args.cases)
    cases_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cases_module)

    results = []

    def hook(ns):
        for case in cases_module.cases(ns):
            record = {"label": case["label"]}
            because = case.get("because")
            if isinstance(because, str):
                because = [because]
            try:
                ns["assert_boot_contract"](
                    case["firmware"], ns["docs_source"], ns["csr_source"],
                    case.get("makefile"), case.get("listing"),
                    case.get("datapath"))
            except (AssertionError, ValueError) as exc:
                record.update(verdict="REFUSED", reason=str(exc)[:2000])
                if because is not None:
                    record["pin_ok"] = all(r in str(exc) for r in because)
            else:
                record.update(verdict="ACCEPTED")
                if because is not None:
                    record["pin_ok"] = False
            if because is not None:
                record["because"] = because
            results.append(record)
            pin = "" if because is None else \
                f" pin_ok={record['pin_ok']}"
            print(f"{record['verdict']}{pin}: {case['label']}", flush=True)
            if record["verdict"] == "REFUSED":
                print("    " + record["reason"][:300].replace("\n", " "),
                      flush=True)
        return None

    module = types.ModuleType("test_builder")
    module.__file__ = str(builder_path)
    module._R272_PROBE = hook
    sys.modules["test_builder"] = module
    exec(compile(source, str(builder_path), "exec"), module.__dict__)
    import test_firmware_compiler as tfc  # binds the in-memory module above

    destination = None if args.absent else args.sdk.resolve()
    if destination is not None:
        tfc.sdk.verify(destination)
    with tempfile.TemporaryDirectory(prefix="r272-probe-") as tmp:
        with (Path(tmp) / "audit.jsonl").open("w") as stream:
            audit = tfc.CompilerAudit(stream, destination)
            argv = [str(builder_path)] + (
                ["--require-rv32"] if destination is not None else [])
            with patch.object(subprocess, "run", side_effect=audit.invoke), \
                    patch.object(sys, "argv", argv), \
                    patch.object(module, "OUT", Path(tmp)), \
                    patch.object(module, "SKIPPED", []):
                module.test_baremetal_profile_contract()
            compiles = audit.compiles
    args.out.write_text(json.dumps({
        "tree": str(tree),
        "mode": "absent" if destination is None else "sdk",
        "patches": applied,
        "anchor": args.anchor,
        "compiles": compiles,
        "results": results}, indent=1) + "\n", encoding="utf-8")
    print(f"PROBE DONE: {len(results)} case(s), {compiles} firmware compiles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
