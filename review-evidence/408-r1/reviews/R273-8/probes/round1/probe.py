#!/usr/bin/env python3
"""Reviewer probe: grade firmware edits through gate 1b's whole boot contract.

Portable, disposable, and never run against the review clone itself: it reads
<checkout>/sw/builder/test_builder.py, writes a sibling copy
test_builder_r273probe.py carrying one hook, and imports that copy, so ROOT is
still <checkout>. The hook runs right before gate 1b's baseline and, for every
case in a JSON list, calls assert_boot_contract() on the edited firmware and
records ACCEPTED or REFUSED with the full reason. Then the gate returns early.

Compiler environments reuse the checkout's own test_firmware_compiler.py
CompilerAudit: --sdk maps the settled selector argv[0] onto a verified SDK,
--absent hides every cross candidate (host firmware compilation refused).

--disconnect NAME rebinds one closure in the gate before the cases run:
  sel  arm_selections()                 -> None (no per-selection grading)
  E    assert_preprocessed_boot_path()  -> no-op
  H    assert_include_resolution_is_pinned() -> no-op
  R    assert_resolved_boot_flow()      -> no-op
  C    assert_compiled_census_is_clean() -> returns the taken verdict unjudged

Usage:
  probe.py --checkout DIR (--sdk DIR | --absent) --cases cases.json --out out.json
           [--disconnect NAME ...]
"""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

ANCHOR = ("    baseline_census_verdict = assert_boot_contract(\n"
          "        firmware_source, docs_source, csr_source)\n")

HOOK = '''    if os.environ.get("R273_EARLY_DISCONNECT") == "R":
        assert_resolved_boot_flow = lambda *_a, **_k: {"residual": [], "calls": 0}
    if os.environ.get("R273_PROBE_CASES"):
        _r273_disc = set(filter(None, os.environ.get("R273_DISCONNECT", "").split(",")))
        if "sel" in _r273_disc:
            arm_selections = lambda _source: None
        if "E" in _r273_disc:
            assert_preprocessed_boot_path = lambda *_a, **_k: None
        if "H" in _r273_disc:
            assert_include_resolution_is_pinned = lambda *_a, **_k: None
        if "R" in _r273_disc:
            assert_resolved_boot_flow = lambda *_a, **_k: {"residual": [], "calls": 0}
        if "C" in _r273_disc:
            assert_compiled_census_is_clean = (
                lambda _fw, _label="firmware", selection=None, taken=None:
                {"ran": bool(taken and taken.get("ran")),
                 "compiler": taken.get("compiler") if taken else None})
        _r273_results = []
        for _r273_case in json.loads(Path(os.environ["R273_PROBE_CASES"]).read_text()):
            _r273_listing = _r273_case.get("listing")
            if _r273_listing is not None:
                _r273_listing = tuple(
                    globals()["PlantedLink"](_n[5:]) if _n.startswith("LINK:")
                    else _n for _n in _r273_listing)
            try:
                _r273_v = assert_boot_contract(
                    _r273_case["firmware"], docs_source, csr_source, None,
                    _r273_listing)
                _r273_results.append({"label": _r273_case["label"],
                                      "verdict": "ACCEPTED",
                                      "census_ran": bool(_r273_v.get("ran"))})
            except (AssertionError, ValueError) as _r273_exc:
                _r273_results.append({"label": _r273_case["label"],
                                      "verdict": "REFUSED",
                                      "reason": str(_r273_exc)})
        Path(os.environ["R273_PROBE_OUT"]).write_text(
            json.dumps(_r273_results, indent=1) + "\\n")
        return
'''


#: Second hook, at the gate's own mutation loop: with R273_MUTATION_AUDIT set,
#: every entry of the gate's mutation table is graded (after the disconnects
#: above, which are re-applied here), recording ACCEPTED, or REFUSED with
#: whether the entry's own reason pin was carried. Everything the gate runs
#: before its mutation loop runs connected and must still pass.
LOOP_ANCHOR = ("    for mutation in mutations:\n"
               "        assert_rejected(*mutation)\n")

LOOP_HOOK = '''    if os.environ.get("R273_MUTATION_AUDIT"):
        _r273_disc = set(filter(None, os.environ.get("R273_DISCONNECT", "").split(",")))
        if "sel" in _r273_disc:
            arm_selections = lambda _source: None
        if "E" in _r273_disc:
            assert_preprocessed_boot_path = lambda *_a, **_k: None
        if "H" in _r273_disc:
            assert_include_resolution_is_pinned = lambda *_a, **_k: None
        if "R" in _r273_disc:
            assert_resolved_boot_flow = lambda *_a, **_k: {"residual": [], "calls": 0}
        if "C" in _r273_disc:
            assert_compiled_census_is_clean = (
                lambda _fw, _label="firmware", selection=None, taken=None:
                {"ran": bool(taken and taken.get("ran")),
                 "compiler": taken.get("compiler") if taken else None})
        _r273_results = []
        for _r273_m in mutations:
            _r273_label, _r273_fw, _r273_docs, _r273_csr, _r273_because = _r273_m[:5]
            _r273_files = _r273_m[5] if len(_r273_m) > 5 else MutantFiles()
            _r273_reasons = ((_r273_because,) if isinstance(_r273_because, str)
                             else tuple(_r273_because))
            try:
                assert_boot_contract(_r273_fw, _r273_docs, _r273_csr,
                                     _r273_files.makefile, _r273_files.listing,
                                     _r273_files.datapath)
                _r273_results.append({"label": _r273_label, "verdict": "ACCEPTED",
                                      "pin": list(_r273_reasons)})
            except (AssertionError, ValueError) as _r273_exc:
                _r273_results.append({
                    "label": _r273_label, "verdict": "REFUSED",
                    "pin": list(_r273_reasons),
                    "pin_ok": all(_r in str(_r273_exc) for _r in _r273_reasons),
                    "reason": str(_r273_exc)[:3000]})
        Path(os.environ["R273_PROBE_OUT"]).write_text(
            json.dumps(_r273_results, indent=1) + "\\n")
        return
'''


def load_probe_module(checkout: Path):
    """The checkout's gate with the hooks, imported as `test_builder`."""
    builder_dir = checkout / "sw/builder"
    text = (builder_dir / "test_builder.py").read_text(encoding="utf-8")
    assert text.count(ANCHOR) == 1, "baseline anchor not found exactly once"
    assert text.count(LOOP_ANCHOR) == 1, "mutation loop anchor not found once"
    probe = builder_dir / f"test_builder_r273probe_{os.getpid()}.py"
    probe.write_text(text.replace(ANCHOR, HOOK + ANCHOR)
                     .replace(LOOP_ANCHOR, LOOP_HOOK + LOOP_ANCHOR),
                     encoding="utf-8")
    sys.path.insert(0, str(checkout / "scripts"))
    sys.path.insert(0, str(builder_dir))
    spec = importlib.util.spec_from_file_location("test_builder", probe)
    module = importlib.util.module_from_spec(spec)
    sys.modules["test_builder"] = module
    spec.loader.exec_module(module)
    return module, probe


def full_run(tfc, builder, probe, args) -> None:
    """The whole gate, with only the early disconnect applied."""
    destination = None if args.absent else args.sdk
    if destination is not None:
        tfc.sdk.verify(destination)
    with args.out.open("w") as stream, \
            tempfile.TemporaryDirectory(prefix="r273-full-") as tmp:
        audit = tfc.CompilerAudit(stream, destination)
        argv = [str(probe)] + (["--require-rv32"] if destination else [])
        with patch.object(subprocess, "run", side_effect=audit.invoke), \
                patch.object(sys, "argv", argv), \
                patch.object(builder, "OUT", Path(tmp)), \
                patch.object(builder, "SKIPPED", []):
            builder.test_baremetal_profile_contract()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--checkout", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--sdk", type=Path)
    mode.add_argument("--absent", action="store_true")
    what = parser.add_mutually_exclusive_group(required=True)
    what.add_argument("--cases", type=Path)
    what.add_argument("--mutation-audit", action="store_true")
    what.add_argument("--full-with-resolver-off", action="store_true",
                      help="run the whole gate with the resolver disconnected "
                           "BEFORE the baseline; the gate must fail closed")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--disconnect", action="append", default=[])
    args = parser.parse_args()
    checkout = args.checkout.resolve()
    builder, probe = load_probe_module(checkout)
    try:
        import test_firmware_compiler as tfc  # the checkout's own audit shim
        if args.mutation_audit:
            os.environ["R273_MUTATION_AUDIT"] = "1"
        elif args.full_with_resolver_off:
            os.environ["R273_EARLY_DISCONNECT"] = "R"
            try:
                full_run(tfc, builder, probe, args)
            except AssertionError as exc:
                print(f"GATE FAILED CLOSED: {str(exc)[:600]}")
                return
            print("GATE PASSED WITH THE RESOLVER DISCONNECTED")
            return
        else:
            os.environ["R273_PROBE_CASES"] = str(args.cases.resolve())
        os.environ["R273_PROBE_OUT"] = str(args.out.resolve())
        os.environ["R273_DISCONNECT"] = ",".join(args.disconnect)
        destination = None if args.absent else args.sdk
        if destination is not None:
            tfc.sdk.verify(destination)
        audit_path = args.out.with_suffix(".audit.jsonl")
        with audit_path.open("w") as stream, \
                tempfile.TemporaryDirectory(prefix="r273-probe-") as tmp:
            audit = tfc.CompilerAudit(stream, destination)
            argv = [str(probe)] + (["--require-rv32"] if destination else [])
            with patch.object(subprocess, "run", side_effect=audit.invoke), \
                    patch.object(sys, "argv", argv), \
                    patch.object(builder, "OUT", Path(tmp)), \
                    patch.object(builder, "SKIPPED", []):
                builder.test_baremetal_profile_contract()
            if destination is None:
                assert audit.compiles == 0, "absent mode compiled firmware"
        results = json.loads(args.out.read_text())
        for entry in results:
            reason = entry.get("reason", "")
            pin = ("" if "pin_ok" not in entry else
                   " [pin ok]" if entry["pin_ok"] else " [PIN MISSED]")
            print(f"{entry['verdict']:8}{pin} {entry['label']}"
                  + (f"\n         -> {reason[:300]}" if reason and
                     not args.mutation_audit else ""))
        print(f"mode={'absent' if args.absent else 'sdk'} "
              f"disconnect={args.disconnect} compiles={audit.compiles} "
              f"cases={len(results)}")
    finally:
        probe.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
