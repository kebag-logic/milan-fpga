#!/usr/bin/env python3
"""Reviewer mutation probes for the selected-placement code at the head under review.

Usage: probe_mutants.py <repo> <scratch> <jobs>
Each mutant replaces one exact snippet (which must occur exactly once) in a copy of
syn/ooc/, then runs both self-tests that import the changed module. A mutant is
DETECTED when the self-test that owns the module exits non-zero. Prints one TSV row
per mutant and a summary; exits 0 when the probe ran, whatever the verdicts.
"""

import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys

GATE, BASE, PLACE = "pp_resource_gate.py", "pp_baseline.py", "pp_placement.py"
MUTANTS = [
    # new gate branches outside the author's 180-mutant table
    ("G1 ooc split refusal removed", GATE,
     '        if placement != "all-fabric" and kind != "route":\n', '        if False:\n'),
    ("G2 M9 re-record refusal removed", GATE,
     '        if args.placement != "all-fabric" and (args.write or args.command == "check-baseline"):\n',
     '        if False:\n'),
    ("G3 M9 refusal ignores check-baseline", GATE,
     '(args.write or args.command == "check-baseline")', '(args.write)'),
    ("G4 placement omitted from input digest", GATE,
     '        digest.update(f"placement\\0{placement}\\0".encode())\n', '        pass\n'),
    ("G5 split scopes rooted at wrapper", GATE,
     'root = ROOTS[kind] if placement == "all-fabric" else "alinx_ax7101"', 'root = ROOTS[kind]'),
    ("G6 split scope names not image-prefixed", GATE,
     '            if placement != "all-fabric":\n                relative = "image"',
     '            if False:\n                relative = "image"'),
    ("G7 cross-root scope deltas claimed", GATE,
     '    if ("image" in before) != ("image" in after):\n', '    if False:\n'),
    ("G8 datapath provenance accepted for all-fabric", GATE,
     '    if not repository and placement != "all-fabric":\n', '    if not repository:\n'),
    ("G9 datapath provenance removed", GATE,
     '    if not repository and placement != "all-fabric":\n', '    if False:\n'),
    ("G10 fuzz split refusal removed", GATE,
     '        if args.placement != "all-fabric":\n            parser.error("--fuzz',
     '        if False:\n            parser.error("--fuzz'),
    ("G11 CLI placement not passed to record", GATE,
     'record(directory, kind_of(directory), args.placement)', 'record(directory, kind_of(directory))'),
    ("G12 census validation not called", GATE,
     '        pp_placement.validate(directory, script, placement)\n', '        pass\n'),
    ("G13 placement selftest hook disabled", GATE,
     '        if result == 0:\n            from pp_placement_selftest import gate_selftest\n',
     '        if False:\n            from pp_placement_selftest import gate_selftest\n'),
    # placement module
    ("L1 all-fabric expects mailbox and processor MAAP", PLACE,
     '        count = 0 if role in ("mailbox", "processor-maap") else 1\n', '        count = 1\n'),
    ("L2 f0-f4 wrapper required", PLACE, '            return 0, 1  # AECP', '            return 1, 1  # AECP'),
    ("L3 f0-f4 wrapper may duplicate", PLACE, '            return 0, 1  # AECP', '            return 0, 2  # AECP'),
    ("L4 f0-f4 AECP optional", PLACE,
     '        if role in ("aecp", "notify"):\n            return 1, 1\n',
     '        if role in ("aecp", "notify"):\n            return 0, 1\n'),
    ("L5 mailbox and gPTP optional", PLACE,
     '    if role in ("mailbox", "gptp"):\n        return 1, 1\n', '    if role in ("mailbox", "gptp"):\n        return 0, 1\n'),
    ("L6 census matches ORIG_REF_NAME only", PLACE,
     '{{ORIG_REF_NAME == {module} || REF_NAME == {module}}}', '{{ORIG_REF_NAME == {module}}}'),
    ("L7 Tcl census lower bound dropped", PLACE,
     'f"if {{$placement_count < {low} || $placement_count > {high}}} {{"',
     'f"if {{$placement_count > {high}}} {{"'),
    ("L8 Tcl census row not written", PLACE,
     "            lines.append(f'puts $placement_file \"{placement}\\t{role}\\t$placement_count\"')\n",
     "            pass\n"),
    ("L9 processor MAAP role dropped", PLACE, '    "processor-maap": "KL_pp_maap",\n', ''),
    ("L10 census header check dropped", PLACE,
     '    if not lines or lines[0] != HEADER:\n', '    if False:\n'),
    ("L11 all-fabric request ignores split marker", PLACE,
     '    if not markers and requested == "all-fabric":\n', '    if requested == "all-fabric":\n'),
    ("L12 image timing path check dropped", PLACE,
     'if {[llength $worst] != 1} { error "No internal timing path for selected image" }\n', ''),
    # recipe module
    ("B1 split synthesis-command count unchecked", BASE,
     '    if len(commands) != 1:\n        raise ValueError("selected placement requires',
     '    if False:\n        raise ValueError("selected placement requires'),
    ("B2 split endpoint option refusal dropped", BASE,
     '        if args.integrated_log or args.attribution_only or output != gateware:\n', '        if False:\n'),
    ("B3 full-split may drop gPTP ROM", BASE,
     '(placement == "full-split" and parameter.startswith("PP_"))', '(placement == "full-split")'),
    ("B4 present removed-protocol ROM unchecked", BASE,
     '        if removed and not matches:\n', '        if removed:\n'),
    ("B5 split marker omitted", BASE,
     'script = pp_placement.MARKER + placement + "\\n" + prefix', 'script = prefix'),
    ("B6 split synthesis-only endpoint swapped", BASE,
     '    marker = "# Add pre-optimize commands" if synthesis_only else "# Bitstream generation"\n    endpoint, _ = split_once(rest, marker)\n    script = pp_placement',
     '    marker = "# Bitstream generation"\n    endpoint, _ = split_once(rest, marker)\n    script = pp_placement'),
    ("B7 split image timing omitted", BASE,
     '    script += pp_placement.scope_timing_tcl() + "\\nquit\\n"\n', '    script += "\\nquit\\n"\n'),
    ("B8 split image manifest not written", BASE,
     '    (gateware / "baseline_images.json").write_text(json.dumps(images, indent=2) + "\\n")\n    target = gateware / "baseline_integrated.tcl"\n    target.write_text(script)',
     '    target = gateware / "baseline_integrated.tcl"\n    target.write_text(script)'),
    ("B9 recipe placement selftest hook disabled", BASE,
     '        recipe_selftest(gateware, standalone, log, source, verilog)\n', '        pass\n'),
]


def run(repo: Path, scratch: Path, name: str, target: str | None, old: str, new: str) -> str:
    """Apply one mutant in a private copy and return its TSV row."""
    folder = scratch / name.split()[0]
    shutil.rmtree(folder, ignore_errors=True)
    ooc = folder / "syn/ooc"
    shutil.copytree(repo / "syn/ooc", ooc, ignore=shutil.ignore_patterns("__pycache__"))
    (folder / "docs/design").mkdir(parents=True)
    shutil.copy2(repo / "docs/design/AREA_BUDGET.md", folder / "docs/design/AREA_BUDGET.md")
    if target is not None:
        source = (ooc / target).read_text()
        if source.count(old) != 1:
            return f"{name}\t{target}\tSNIPPET-COUNT-{source.count(old)}\t-\t-\tINVALID"
        (ooc / target).write_text(source.replace(old, new))
    rcs = {}
    for label, script in (("gate", GATE), ("recipe", BASE)):
        result = subprocess.run([sys.executable, "-B", str(ooc / script), "--selftest"], cwd=folder,
                                capture_output=True, text=True, timeout=300)
        rcs[label] = result.returncode
        (folder / f"{label}.log").write_text(result.stdout + result.stderr)
    owner = {GATE: "gate", BASE: "recipe", PLACE: None, None: None}[target]
    if target is None:
        verdict = "CONTROL-PASS" if not any(rcs.values()) else "CONTROL-FAIL"
    elif owner is None:
        verdict = "DETECTED" if any(rcs.values()) else "SURVIVED"
    else:
        verdict = "DETECTED" if rcs[owner] else "SURVIVED"
    return f"{name}\t{target}\tok\t{rcs['gate']}\t{rcs['recipe']}\t{verdict}"


def main() -> None:
    repo, scratch, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    work = [("C0 control", None, "", "")] + MUTANTS
    print("mutant\tfile\tsnippet\tgate_rc\trecipe_rc\tverdict")
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        rows = list(pool.map(lambda item: run(repo, scratch, *item), work))
    for row in rows:
        print(row)
    survived = [row.split("\t")[0] for row in rows if row.endswith("SURVIVED") or row.endswith("INVALID")]
    print(f"summary: {len(MUTANTS)} mutants, {len(MUTANTS) - len(survived)} detected, survived/invalid: {survived}")


if __name__ == "__main__":
    main()
