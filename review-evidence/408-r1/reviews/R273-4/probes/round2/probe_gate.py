#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: grade firmware texts with gate 1b's own boot-contract check.

A disposable copy of sw/builder/test_builder.py is written under --work with
one hook inserted right after the gate grades the shipping firmware: every
case in --cases is handed to the SAME nested assert_boot_contract(), and every
spelling in --spellings to the SAME lexer_keeps() the lexer corpus uses. The
results go to --out and the gate stops there (no mutation table is run).

The repository is never edited. Compiler selection mirrors
sw/builder/test_firmware_compiler.py: with --sdk the absolute selector's argv[0]
is mapped to the verified SDK and every other cross candidate is hidden; with
--absent every cross candidate is hidden.
"""

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

ANCHOR = ("    baseline_census_verdict = assert_boot_contract(\n"
          "        firmware_source, docs_source, csr_source)\n")
HOOK = '''
    if os.environ.get("R273_PROBE_OUT"):
        _r273 = {"lexer": {}, "cases": []}
        for _spell in json.loads(Path(os.environ["R273_PROBE_SPELLINGS"]).read_text()):
            _got = lexer_keeps(_spell["text"])
            _r273["lexer"][_spell["label"]] = list(_got) if _got is not None else None
        for _case in json.loads(Path(os.environ["R273_PROBE_CASES"]).read_text()):
            try:
                _v = assert_boot_contract(_case["firmware"], docs_source, csr_source)
                _r273["cases"].append({"label": _case["label"], "verdict": "ACCEPTED",
                                       "census_ran": bool(_v.get("ran"))})
            except (AssertionError, ValueError) as _exc:
                _r273["cases"].append({"label": _case["label"], "verdict": "REFUSED",
                                       "reason": str(_exc)[:900]})
        _r273["baseline_census_ran"] = bool(baseline_census_verdict.get("ran"))
        _r273["lexer_note"] = lexer_note
        Path(os.environ["R273_PROBE_OUT"]).write_text(json.dumps(_r273, indent=1))
        raise SystemExit(97)
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--sdk", type=Path)
    mode.add_argument("--absent", action="store_true")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--spellings", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    source = (repo / "sw/builder/test_builder.py").read_text()
    assert source.count(ANCHOR) == 1, "hook anchor not unique"
    here_line = "HERE = Path(__file__).resolve().parent\n"
    assert source.count(here_line) == 1, "HERE anchor not unique"
    probe = source.replace(ANCHOR, ANCHOR + HOOK).replace(
        here_line, f"HERE = Path({str(repo / 'sw/builder')!r})\n")
    args.work.mkdir(parents=True, exist_ok=True)
    probe_path = args.work / "test_builder_r273_probe.py"
    probe_path.write_text(probe)

    import os
    os.environ["R273_PROBE_OUT"] = str(args.out.resolve())
    os.environ["R273_PROBE_CASES"] = str(args.cases.resolve())
    os.environ["R273_PROBE_SPELLINGS"] = str(args.spellings.resolve())

    spec = importlib.util.spec_from_file_location("test_builder_r273_probe", probe_path)
    builder = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = builder
    spec.loader.exec_module(builder)

    selector = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
    cross = {selector, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
    native = {"cc", "gcc"}
    real_run = subprocess.run
    compiles = {"n": 0}

    def invoke(argv, **kwargs):
        requested = [str(a) for a in argv]
        if requested[0] not in cross | native:
            return real_run(argv, **kwargs)
        if requested[0] in cross and (args.absent or requested[0] != selector):
            raise FileNotFoundError("hidden cross candidate")
        actual = requested.copy()
        if requested[0] == selector:
            actual[0] = str(args.sdk.resolve() / "bin/riscv32-linux-gcc")
            compiles["n"] += 1
        elif requested[1:] != ["--version"] and not any(
                Path(a).name == "probe.c" for a in requested[1:]):
            raise AssertionError("host compiler attempted firmware compilation")
        return real_run(actual, **kwargs)

    argv = ["probe_gate.py"] + (["--require-rv32"] if args.sdk else [])
    with tempfile.TemporaryDirectory(prefix="r273-probe-") as tmp, \
            patch.object(subprocess, "run", side_effect=invoke), \
            patch.object(sys, "argv", argv), \
            patch.object(builder, "OUT", Path(tmp)), \
            patch.object(builder, "SKIPPED", []):
        try:
            builder.test_baremetal_profile_contract()
        except SystemExit as done:
            if done.code != 97:
                raise
        else:
            raise AssertionError("probe hook never ran")
    result = json.loads(args.out.read_text())
    result["mode"] = "sdk" if args.sdk else "absent"
    result["compiler_invocations"] = compiles["n"]
    args.out.write_text(json.dumps(result, indent=1))
    for label, kept in result["lexer"].items():
        print(f"LEXER {label}: {kept}")
    for case in result["cases"]:
        print(f"{case['verdict']:8s} {case['label']}"
              + (f" :: {case['reason'][:220]}" if case["verdict"] == "REFUSED" else ""))
    print(f"mode={result['mode']} baseline_census_ran={result['baseline_census_ran']} "
          f"compiles={compiles['n']} lexer_note={result['lexer_note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
