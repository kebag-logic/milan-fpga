#!/usr/bin/env python3
"""Negative controls for the PR's scripts/check_source_evidence.py.

Loads the checker from an exported head tree and feeds it altered inputs in a
temporary copy; nothing in the export is modified. Each control must report
at least one finding; the unaltered head must report none.

Usage: python3 checker_controls.py <exported head> <clone>
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = "e5dcea6e351abff18a27a00f8e345f3251bdbd8f"


def load(tree):
    spec = importlib.util.spec_from_file_location(
        "cse", tree / "scripts/check_source_evidence.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    tree, clone = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
    ledger = (tree / "docs/SOURCE_EVIDENCE.md").read_text()
    base_ledger = subprocess.run(
        ["git", "-C", str(clone), "show", f"{BASE}:docs/SOURCE_EVIDENCE.md"],
        check=True, capture_output=True, text=True).stdout
    fails = 0
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "t"
        for d in ("docs", "hdl"):
            shutil.copytree(tree / d, root / d)
        cse = load(tree)
        eng = root / "hdl/top/KL_gptp_engine.sv"
        eng_text = eng.read_text()

        def run(label, text=ledger, expect_findings=True):
            nonlocal fails
            findings, exact = cse.check(root, text)
            ok = bool(findings) == expect_findings
            fails += not ok
            print(f"[{'OK' if ok else 'BAD'}] {label}: {len(exact)} exact, "
                  f"{len(findings)} findings")
            for f in findings[:12]:
                print(f"      {f}")

        run("unaltered head ledger", expect_findings=False)
        run("base e5dcea6 ledger against head sources", base_ledger)
        run("slew port anchor shifted +1",
            ledger.replace("KL_gptp_engine.sv#L109", "KL_gptp_engine.sv#L110"))
        run("word 2 and word 3 anchors swapped",
            ledger.replace("#L929", "#LXXX").replace("#L934", "#L929")
                  .replace("#LXXX", "#L934"))
        run("policy anchor removed",
            ledger.replace("[policy](../hdl/ucode/gen_gptp_ucode.py#L837)",
                           "[policy](../hdl/ucode/gen_gptp_ucode.py)"))
        run("slew row deleted",
            "\n".join(r for r in ledger.splitlines()
                      if not r.startswith("| Registered policy slew level")))
        eng.write_text("\n" + eng_text)
        run("one line inserted at the top of the engine source")
        eng.write_text(eng_text)
        run("engine source restored", expect_findings=False)
    print(f"checker controls: {'PASS' if not fails else 'FAIL'} ({fails} bad)")
    return int(bool(fails))


if __name__ == "__main__":
    sys.exit(main())
