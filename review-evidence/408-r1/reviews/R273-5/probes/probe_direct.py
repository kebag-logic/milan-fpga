#!/usr/bin/env python3
"""(R273-4 copy with R273_DIRECT=1: compile the unselected file directly.)

Grade firmware variants through gate 1b's own assert_boot_contract().

Evidence driver for the A219 correction round of PR #535 (#408, #409).
Adapted from the R272-1 probe driver (in-memory hook) so that NOTHING is
written into the lane: the gate source is read, optionally taken from a git
revision instead of the working tree, count-checked string patches are
applied (to DISCONNECT one fix), one hook is inserted, and the result runs
as a fresh module whose ROOT is the lane.

  --rev REV      read test_builder.py and docs/integration/BAREMETAL_FIRMWARE.md
                 from git revision REV (the base 759da623) instead of the tree;
                 the docs text is substituted in memory
  --sdk DIR      the pinned SDK mapped onto the settled selector (the same
                 argv[0] substitution sw/builder/test_firmware_compiler.py makes)
  --absent       every cross candidate hidden
  --cases F      JSON list of {label, firmware[, listing][, because]}
  --anchor A     baseline (default: grade right after the baseline verdict) or
                 mutations (grade every mutation-table entry, collecting)
  --labels F     with --anchor mutations: only these labels (one per line)
  --patch F      JSON list of [old, new], each old occurring exactly once
"""

import argparse
import json
import subprocess
import sys
import tempfile
import time
import types
from pathlib import Path
from unittest.mock import patch

import os
DIRECT = os.environ.get("R273_DIRECT") == "1"
DIRECT_KEYS = ("id = ", "aem_loaded = 1", "0x90000600u", "MILAN_ADP_CTRL", "0x600u", "r273")
LANE = Path(os.environ["R273_LANE"])  # reviewer copy: the lane path is an argument, not a constant
ANCHORS = {
    "baseline": ("    baseline_census_verdict = assert_boot_contract(\n"
                 "        firmware_source, docs_source, csr_source)\n"),
    "mutations": ("    for mutation in mutations:\n"
                  "        assert_rejected(*mutation)\n"),
}
DOCS_READ = '    docs_source = docs_path.read_text(encoding="utf-8")\n'
HOOK = {
    "baseline": "    return _A219_PROBE(locals())\n",
    "mutations": "    return _A219_MUTATIONS(locals())\n",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--sdk", type=Path)
    mode.add_argument("--absent", action="store_true")
    ap.add_argument("--cases", type=Path)
    ap.add_argument("--anchor", choices=sorted(ANCHORS), default="baseline")
    ap.add_argument("--labels", type=Path)
    ap.add_argument("--patch", type=Path, action="append", default=[])
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    builder_path = LANE / "sw/builder/test_builder.py"
    if args.rev:
        source = subprocess.run(
            ["git", "-C", str(LANE), "show",
             f"{args.rev}:sw/builder/test_builder.py"],
            check=True, capture_output=True, text=True).stdout
        docs = subprocess.run(
            ["git", "-C", str(LANE), "show",
             f"{args.rev}:docs/integration/BAREMETAL_FIRMWARE.md"],
            check=True, capture_output=True, text=True).stdout
        assert source.count(DOCS_READ) == 1, "docs read anchor"
        source = source.replace(
            DOCS_READ, "    docs_source = _A219_DOCS\n", 1)
    else:
        source = builder_path.read_text(encoding="utf-8")
        docs = None
    applied = []
    for patch_file in args.patch:
        for old, new in json.loads(patch_file.read_text(encoding="utf-8")):
            assert source.count(old) == 1, \
                f"{patch_file}: anchor occurs {source.count(old)} times: " \
                f"{old[:80]!r}"
            source = source.replace(old, new, 1)
        applied.append(str(patch_file))
    anchor = ANCHORS[args.anchor]
    assert source.count(anchor) == 1, "hook anchor not found exactly once"
    source = source.replace(anchor, anchor + HOOK[args.anchor], 1) \
        if args.anchor == "baseline" else \
        source.replace(anchor, HOOK[args.anchor] + anchor, 1)
    sys.path.insert(0, str(LANE / "scripts"))
    sys.path.insert(0, str(LANE / "sw/builder"))

    cases = json.loads(args.cases.read_text(encoding="utf-8")) \
        if args.cases else []
    wanted = set(args.labels.read_text().splitlines()) if args.labels else None
    results = []

    def grade(ns):
        for case in cases:
            record = {"label": case["label"]}
            because = case.get("because")
            if isinstance(because, str):
                because = [because]
            listing = case.get("listing")
            if listing is not None:
                # a LINK is a head concept; base plants the bare name
                planted = ns.get("PlantedLink") or \
                    module.__dict__.get("PlantedLink") or (lambda n: n)
                listing = tuple(planted(n[5:]) if n.startswith("LINK:")
                                else n for n in listing)
            try:
                if DIRECT:
                    # R273-4: hand the UNSELECTED file to the compiler, as the
                    # product does: -E over the census headers, then the census
                    with tempfile.TemporaryDirectory(prefix="r273-direct-") as d:
                        root = Path(d)
                        ns["census_headers"](root)
                        (root / "milan_baremetal.c").write_text(case["firmware"])
                        cc = ns["census_compiler"]()
                        pre = subprocess.run(
                            [cc, "-std=gnu99", "-E", f"-I{root}",
                             str(root / "milan_baremetal.c")],
                            capture_output=True, text=True)
                    own = ns["preprocessed_own_text"](pre.stdout)
                    record["E_rc"] = pre.returncode
                    record["E_hits"] = [line.strip() for line in own.split("\n")
                                        if any(k in line for k in DIRECT_KEYS)]
                    print("    -E: " + " | ".join(record["E_hits"]), flush=True)
                    verdict = ns["assert_compiled_census_is_clean"](
                        case["firmware"])
                else:
                    verdict = ns["assert_boot_contract"](
                    case["firmware"], ns["docs_source"], ns["csr_source"],
                    None, listing)
            except (AssertionError, ValueError) as exc:
                record.update(verdict="REFUSED", reason=str(exc))
                if because is not None:
                    record["pin_ok"] = all(r in str(exc) for r in because)
            else:
                record.update(verdict="ACCEPTED",
                              census_ran=bool(verdict.get("ran")))
                if because is not None:
                    record["pin_ok"] = False
            if because is not None:
                record["because"] = because
            results.append(record)
            pin = "" if because is None else f" pin_ok={record['pin_ok']}"
            print(f"{record['verdict']}{pin}: {case['label']}", flush=True)
            if record["verdict"] == "REFUSED":
                print("    " + record["reason"][:400].replace("\n", " "),
                      flush=True)

    def mutations(ns):
        for mutation in ns["mutations"]:
            label, firmware, docs_text, csr, because = mutation[:5]
            if wanted is not None and label not in wanted:
                continue
            reasons = (because,) if isinstance(because, str) else \
                tuple(because)
            record = {"label": label, "pin": list(reasons)}
            try:
                ns["assert_rejected"](*mutation)
            except AssertionError as exc:
                record.update(ok=False, said=str(exc))
            else:
                record.update(ok=True)
            results.append(record)
            print(f"{'ok ' if record['ok'] else 'BAD'}: {label}", flush=True)
            if not record["ok"]:
                print("    " + record["said"][:400].replace("\n", " "),
                      flush=True)

    module = types.ModuleType("test_builder")
    module.__file__ = str(builder_path)
    module._A219_PROBE = grade
    module._A219_MUTATIONS = mutations
    module._A219_DOCS = docs
    sys.modules["test_builder"] = module
    exec(compile(source, str(builder_path), "exec"), module.__dict__)
    import test_firmware_compiler as tfc  # binds the in-memory module above

    destination = None if args.absent else args.sdk.resolve()
    if destination is not None:
        tfc.sdk.verify(destination)
    start = time.time()
    with tempfile.TemporaryDirectory(prefix="a219-probe-") as tmp:
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
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({
        "rev": args.rev or "working tree",
        "mode": "absent" if destination is None else "sdk",
        "patches": applied, "anchor": args.anchor, "compiles": compiles,
        "seconds": round(time.time() - start, 1),
        "results": results}, indent=1) + "\n", encoding="utf-8")
    print(f"PROBE DONE: {len(results)} result(s), {compiles} compiles, "
          f"{round(time.time() - start, 1)} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
