#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The builder-refusal arms of `yosys_sweep.py --selftest` (#652).

This is the half of the sweep's self-test that follows a configuration the
builder refuses through the sweep, kept beside it rather than inside it: the
outcome classifier, the builder's real refusal of a 235-name variant, the
shapes step's verdict through a stand-in builder, and a refused point through
run and summary. They share no fixture with the sweep's
rewrite, expansion, plan, guard and tree arms. Run them through the sweep,
which is the only supported entry point:

    python3 syn/resmap/yosys_sweep.py --selftest

Every arm takes the sweep module whose self-test is running and calls that
module's own functions, never a second import of its file, so a defect planted
in the running copy is the code the arm exercises.
"""

import contextlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType

#: A refusal line as the builder's CLI prints it.
REFUSAL = "CONFIG ERROR: this AEM model has 9 writable names and the saved-state backend holds 8 NAME records"

#: A stand-in for the builder's CLI in a synthetic tree, deciding by the configuration's name: a crash
#: exits with a traceback, a refusal prints REFUSAL, and anything else builds.
STAND_IN_BUILDER = f"""import sys
from pathlib import Path
name = Path(sys.argv[-1]).stem
if "crash" in name:
    sys.exit("Traceback (most recent call last):")
if "refused" in name:
    print({REFUSAL!r})
    sys.exit(1)
"""


def _outcome(sweep: ModuleType) -> list[str]:
    """A refusal is read with its line; a crash, a second refusal line or another exit is never a refusal;
    and the builder's own refusal of a 235-name variant reads as one, with nothing written."""
    problems = []
    for label, rc, text, want in (
            ("a build", 0, "[endstation_builder] built\n", ("built", "")),
            ("a refusal", 1, REFUSAL + "\n", ("refused", REFUSAL)),
            ("a traceback", 1, "Traceback (most recent call last):\n" + REFUSAL + "\n", "failed"),
            ("an exit with no refusal line", 1, "Killed\n", "failed"),
            ("two refusal lines", 1, REFUSAL + "\n" + REFUSAL + "\n", "failed"),
            ("a usage error", 2, REFUSAL + "\n", "failed")):
        got = sweep.builder_outcome(rc, text)
        if (got[0] if want == "failed" else got) != want:
            problems.append(f"outcome: {label} read as {got}")
    plan = sweep.load_plan(sweep.PLAN)
    base = (sweep.REPO / "configs" / f"{sweep.BASE_CONFIG}.yaml").read_text()
    with tempfile.TemporaryDirectory(prefix="resmap-outcome-") as tmp:
        config = Path(tmp) / "endstation_rm_selftest.yaml"
        config.write_text(sweep.variant_text(base, plan["variants"]["rm_ax7101_8x8_tdm8"]))
        run = subprocess.run([sys.executable, str(sweep.REPO / "sw/builder/endstation_builder.py"), "-o",
                              str(Path(tmp) / "out"), str(config)], cwd=sweep.REPO, capture_output=True,
                             text=True, check=False)
        outcome, line = sweep.builder_outcome(run.returncode, run.stdout + run.stderr)
        if outcome != "refused" or "writable names" not in line or (Path(tmp) / "out").exists():
            problems.append(f"outcome: the builder's refusal of the 8x8 TDM8 variant read as {outcome} {line!a}")
    return problems


def _shapes(sweep: ModuleType) -> list[str]:
    """The shapes step through a stand-in builder, with no export: it passes when every outcome is the
    one the plan expects, and fails on an unexpected refusal, an expected refusal that builds, and a
    crash."""
    problems = []
    refused = {"expect": "refused"}
    for label, variants, want in (
            ("every outcome the expected one", {"v_built": {}, "v_refused_names": refused}, 0),
            ("an unexpected refusal", {"v_built": {}, "v_refused_names": {}}, 1),
            ("an expected refusal that builds", {"v_built": refused, "v_refused_names": refused}, 1),
            ("a crash", {"v_built": {}, "v_crash": {}}, 1)):
        with tempfile.TemporaryDirectory(prefix="resmap-shapes-") as tmp:
            work, tree = Path(tmp), Path(tmp) / "tree"
            (tree / "configs").mkdir(parents=True)
            (tree / "configs" / f"{sweep.BASE_CONFIG}.yaml").write_text(sweep.LISTENER + sweep.TALKER)
            (tree / "sw" / "builder").mkdir(parents=True)
            (tree / "sw" / "builder" / "endstation_builder.py").write_text(STAND_IN_BUILDER)
            plan = {"variants": {name: {"streams": 1, "channels": 8, **spec} for name, spec in variants.items()}}
            with contextlib.redirect_stdout(io.StringIO()):
                rc = sweep.generate_shapes(work, plan, tree)
            outcomes = json.loads((work / "shapes" / "outcomes.json").read_text())
            if rc != want:
                problems.append(f"shapes: {label} exited {rc}, not {want}: {outcomes}")
            if want == 0 and {name: (o["outcome"], o["refusal"]) for name, o in outcomes.items()} != {
                    "v_built": ("built", ""), "v_refused_names": ("refused", REFUSAL)}:
                problems.append(f"shapes: {label} recorded {outcomes}")
    return problems


def _refused_points(sweep: ModuleType) -> list[str]:
    """A point whose shape the builder refused is reported and not priced by run, recorded with its line by
    summary, and fails summary when it carries a priced receipt; a variant with no outcome is refused."""
    problems = []
    plan = {"tops": {"milan_datapath": {"shape": "endstation_base", "params": {}}},
            "variants": {"v_refused": {}, "v_built": {}, "v_unrun": {}},
            "points": [{"name": "p", "top": "milan_datapath", "shape": "v_refused"}]}
    outcomes = {"v_refused": {"outcome": "refused", "refusal": REFUSAL},
                "v_built": {"outcome": "built", "refusal": ""}}
    with tempfile.TemporaryDirectory(prefix="resmap-refused-") as tmp:
        work = Path(tmp)
        (work / "shapes").mkdir()
        (work / "shapes" / "outcomes.json").write_text(json.dumps(outcomes))
        lines = {shape: sweep.builder_refusal(work, plan, {"name": shape, "top": "milan_datapath", "shape": shape})
                 for shape in ("v_refused", "v_built", "endstation_base")}
        if lines != {"v_refused": REFUSAL, "v_built": "", "endstation_base": ""}:
            problems.append(f"refused: the outcomes read as {lines}")
        try:
            sweep.builder_refusal(work, plan, {"name": "q", "top": "milan_datapath", "shape": "v_unrun"})
            problems.append("refused: a variant with no builder outcome was taken as built")
        except sweep.PlanError:
            pass
        with contextlib.redirect_stdout(io.StringIO()):
            ran = sweep.command_run(work, plan, [], 1)
            summarized = sweep.command_summary(work, plan, 1)
        summary = json.loads((work / "summary.json").read_text())
        if ran or (work / "points").exists():
            problems.append(f"refused: run exited {ran} or priced the refused point")
        if summarized or summary != {"p": {"builder": {"refusal": REFUSAL}}}:
            problems.append(f"refused: summary exited {summarized} with {summary}")
        (work / "points" / "p").mkdir(parents=True, exist_ok=True)
        (work / "points" / "p" / "receipt.json").write_text("{}\n")
        with contextlib.redirect_stdout(io.StringIO()):
            if not sweep.command_summary(work, plan, 1):
                problems.append("refused: a priced receipt for a refused point was summarized")
    return problems


def run_arms(sweep: ModuleType) -> list[str]:
    """Every builder-refusal arm against the running sweep module; the problems they found."""
    return _outcome(sweep) + _shapes(sweep) + _refused_points(sweep)
