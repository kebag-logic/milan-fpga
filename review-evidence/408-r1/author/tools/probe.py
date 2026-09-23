#!/usr/bin/env python3
"""Run gate 1b from a (textually patched) copy of test_builder.py, in memory.

Evidence driver for the #408/#409 lane. Nothing is written into the tree:
the source is read, patched as a string, compiled under the lane's real path
(so HERE/ROOT resolve to the lane) and executed as a fresh module. The
compiler is either the pinned SDK mapped onto the gate's absolute selector
(the same argv[0] substitution sw/builder/test_firmware_compiler.py makes) or
absent (every cross candidate raises FileNotFoundError).

Hooks, all optional:
  --collect         replace the mutation loop with one that records every
                    mutation's outcome instead of stopping at the first
  --labels FILE     only run mutations whose label is listed (one per line)
  --dump-cases      record the head's retired_rule_cases texts to --out
  --grade-cases F   grade each {label: firmware} in JSON F right after the
                    baseline, record the outcome, and stop
  --patch F         JSON list of [old, new] replacements applied first
"""

import argparse
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import time
import types
from pathlib import Path
from unittest.mock import patch

LANE = Path("$LANES/408-409-boot-gate-retire")
sys.path.insert(0, str(LANE / "scripts"))
sys.path.insert(0, str(LANE / "sw/builder"))
import ci_rv32_sdk as sdk  # noqa: E402

SDK = Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install")
SELECTOR = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
CROSS = {SELECTOR, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}
LOOP = "    for mutation in mutations:\n        assert_rejected(*mutation)\n"
BASELINE = ("    baseline_census_verdict = assert_boot_contract(\n"
            "        firmware_source, docs_source, csr_source)\n")
CASES_AT = "    accepted_cases.update(retired_rule_cases)\n"


class Done(Exception):
    """Raised by a hook once it has what it came for."""


def compiler_run(mode):
    real = subprocess.run

    def run(argv, **kwargs):
        first = str(argv[0])
        if first in CROSS:
            if mode == "absent" or first != SELECTOR:
                raise FileNotFoundError("deliberately absent RV32 candidate")
            argv = [str(SDK / sdk.COMPILER)] + [str(a) for a in argv[1:]]
        return real(argv, **kwargs)
    return run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path,
                    default=LANE / "sw/builder/test_builder.py")
    ap.add_argument("--mode", choices=("sdk", "absent"), required=True)
    ap.add_argument("--patch", type=Path)
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--labels", type=Path)
    ap.add_argument("--dump-cases", action="store_true")
    ap.add_argument("--grade-cases", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    text = args.source.read_text()
    if args.patch:
        for old, new in json.loads(args.patch.read_text()):
            assert text.count(old) == 1, f"patch anchor not unique: {old[:70]!r}"
            text = text.replace(old, new, 1)
    result = {"source": str(args.source), "mode": args.mode,
              "patched": bool(args.patch)}
    if args.collect or args.labels:
        assert text.count(LOOP) == 1
        text = text.replace(LOOP, "    _probe_mutations(mutations, assert_rejected)\n")
    if args.dump_cases:
        assert text.count(CASES_AT) == 1
        text = text.replace(CASES_AT, CASES_AT + "    _probe_dump(retired_rule_cases)\n")
    if args.grade_cases:
        assert text.count(BASELINE) == 1
        text = text.replace(BASELINE, BASELINE +
                            "    _probe_grade(assert_boot_contract, docs_source, csr_source)\n")

    wanted = set(args.labels.read_text().splitlines()) if args.labels else None

    def probe_mutations(mutations, assert_rejected):
        outcomes = []
        for mutation in mutations:
            if wanted is not None and mutation[0] not in wanted:
                continue
            try:
                assert_rejected(*mutation)
            except AssertionError as exc:
                outcomes.append({"label": mutation[0], "ok": False,
                                 "because": mutation[4], "said": str(exc)[:1500]})
            else:
                outcomes.append({"label": mutation[0], "ok": True,
                                 "because": mutation[4]})
        result["mutations"] = outcomes
        raise Done()

    def probe_dump(cases):
        result["cases"] = dict(cases)
        raise Done()

    def probe_grade(assert_boot_contract, docs, csr):
        graded = {}
        for label, firmware in json.loads(args.grade_cases.read_text()).items():
            listing = None
            if isinstance(firmware, dict):
                listing = tuple(firmware["listing"])
                firmware = firmware["firmware"]
            try:
                assert_boot_contract(firmware, docs, csr, None, listing)
            except (AssertionError, ValueError) as exc:
                graded[label] = {"verdict": "RED", "said": str(exc)[:1500]}
            else:
                graded[label] = {"verdict": "GREEN"}
        result["graded"] = graded
        raise Done()

    module = types.ModuleType("test_builder")
    module.__file__ = str(LANE / "sw/builder/test_builder.py")
    module._probe_mutations = probe_mutations
    module._probe_dump = probe_dump
    module._probe_grade = probe_grade
    code = compile(text, module.__file__, "exec")
    sys.modules["test_builder"] = module
    start = time.time()
    log = io.StringIO()
    with tempfile.TemporaryDirectory(prefix="a209-probe-") as tmp, \
            patch.object(subprocess, "run", side_effect=compiler_run(args.mode)), \
            patch.object(sys, "argv", [module.__file__]), \
            contextlib.redirect_stdout(log):
        exec(code, module.__dict__)
        module.OUT = Path(tmp)
        module.SKIPPED = []
        try:
            module.test_baremetal_profile_contract()
            result["finished"] = "gate returned"
        except Done:
            result["finished"] = "probe hook"
        except AssertionError as exc:
            result["finished"] = "gate raised"
            result["raised"] = str(exc)[:4000]
        result["skipped"] = [why[:300] for _gate, why, _kind in module.SKIPPED]
    result["seconds"] = round(time.time() - start, 1)
    result["stdout_tail"] = log.getvalue()[-3000:]
    args.out.write_text(json.dumps(result, indent=1))
    bad = [m["label"] for m in result.get("mutations", []) if not m["ok"]]
    print(json.dumps({"finished": result["finished"], "seconds": result["seconds"],
                      "mutations": len(result.get("mutations", [])),
                      "not_ok": bad, "raised": result.get("raised", "")[:600],
                      "graded": {k: v["verdict"] for k, v in
                                 result.get("graded", {}).items()}}, indent=1))


if __name__ == "__main__":
    main()
