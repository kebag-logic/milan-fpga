#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""check_deploy_shape.py - the deploy-vs-generated-shape gate.

WHY THIS EXISTS.  `sw/litex/deploy.sh` is the THIRD path to a flashed
bitstream, beside `sweep.sh` and `build.sh`, and until #453 it was the only
one that spelled the design shape as a hand-kept literal instead of reading
the generated emission of an end-station config.  A hand-kept copy drifts in
silence: this one had lost `--audio-interface-render 8`, `--num-streams 1`
and `--uart-baudrate 115200`, so a deploy-built bitstream elaborated
`AUDIO_IF_RENDER_SLOTS_P = 0`, took `milan_datapath`'s `g_tdm_render_parked`
arm and held J11.5 low while every sweep-built image rendered.  Two entry
points, one commit, two shipping shapes - the divergence class
`check_sweep_shape.py` already holds `sweep.sh` and `build.sh` to.

WHAT IT CHECKS, against the launch line `deploy.sh build --dry-run` prints
(the line is READ, not parsed out of the script's text, so what is graded is
what argparse would receive):

  1. the shape is DERIVED, not restated: deploy.sh names the generated
     fragment and composes its options from the `OPTS` it defines;
  2. the design part of the launch line - every token before
     `--entity-gen-dir` - equals that fragment's `OPTS` token for token, so
     deploy.sh and sweep.sh elaborate the identical option string;
  3. every design flag equals the config's own emission
     (`sw/builder/endstation_builder.emit_soc_argv`), flag for flag;
  4. `--entity-gen-dir` names the config being deployed;
  5. a config that declares a TDM render lane does not launch with the lane
     absent or zero, which is the consequence rule: `milan_soc.py` passes
     `p_AUDIO_IF_RENDER_SLOTS_P` only above zero and the RTL default is 0;
  6. what deploy.sh appends AFTER the shared shape is a flow flag, the
     entity directory, or a repeat of a value the shape already carries -
     never a design flag of its own (argparse takes the last occurrence, so
     an appended literal is a value drift, not a duplicate nobody sees).

Usage:

    python3 scripts/check_deploy_shape.py             # the gate
    python3 scripts/check_deploy_shape.py --selftest  # + the planted drifts

Exit 0 = deploy.sh builds the shape the config declares, 1 = drift (with the
offending values printed), 2 = usage/setup or a self-test that did not catch
its own plant.  Needs pyyaml, like every gate that reads the builder.
"""

import argparse
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# The shared shape vocabulary lives in the sweep gate; a second copy of
# design_flags()/parse_flags() here is the very drift these gates exist to
# stop.  scripts/ is already sys.path[0] when this file is run directly; the
# insert is for the self-test and for anything that imports it.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_sweep_shape import (  # noqa: E402  (path set above)
    FLOW_FLAGS, design_flags, design_opts_expected, parse_flags)

DEPLOY = ROOT / "sw/litex/deploy.sh"
#: The end-station config deploy.sh is bound to, exactly as
#: check_sweep_shape.BUILD_CFGS binds each build.sh recipe to one.
DEPLOY_CFG = "configs/endstation_ax7101_1x1_tdm8.yaml"
DEPLOY_BOARD = "ax7101"
#: The generated fragment sweep.sh sources and deploy.sh now reads: the ONE
#: place the AX7101 shape is written down.
FRAGMENT = ROOT / "configs/generated" / f"sweep_opts_{DEPLOY_BOARD}.sh"
LAUNCH_ENTRY = "milan_soc.py"
#: The first flag deploy.sh appends: everything before it is the shared shape.
GEN_DIR_FLAG = "--entity-gen-dir"
RENDER_FLAG = "--audio-interface-render"
#: What run_milan_soc prints in a dry run, and the %q-quoted argv beneath it.
DRY_MARK = "DRY ["

#: Negative controls, planted in deploy.sh's TEXT and executed in place: each
#: is a way the deploy shape can stop being the config's emission again.  The
#: first is #453 itself, restored verbatim; the second keeps the derivation
#: and strips one flag out of it, so the flag comparison - not the text rule -
#: has to be what catches it; the last two are the fragment's per-board
#: ownership, which is why deploy.sh checks its provenance before sourcing it.
#: Every replacement must apply exactly once.
#:   (why, [(old, new), ...], the drifts it must report)
HAND_KEPT_OPTS = (
    "--board ax7101 --cpu vexiiriscv --cpu-count 1 --xlen 32 "
    "--software-profile baremetal --full --milan-clk-freq 50e6 "
    "--with-spiflash --flashboot baremetal --gtx-tx-invert --timing-opt "
    "--floorplan --eth-port e1 --no-i2s-playback --no-render-lpf "
    "--audio-interface tdm8 --audio-interface-master --talker-wire-chans 8 "
    "--loopback-lane --fabric-gptp --l2-bytes 0")
DEPLOY_PLANTS = [
    ("the hand-kept option string of #453 is restored",
     [('MILAN_OPTS="$OPTS ', f'MILAN_OPTS="{HAND_KEPT_OPTS} ')],
     ("is not derived from", RENDER_FLAG, "AUDIO_IF_RENDER_SLOTS_P",
      "--num-streams")),
    ("the derived string is filtered on its way to the launcher",
     [('MILAN_OPTS="$OPTS ',
       'MILAN_OPTS="${OPTS/ --audio-interface-render 8/} ')],
     (RENDER_FLAG, "AUDIO_IF_RENDER_SLOTS_P", "is not the fragment")),
    ("a design flag is hand-appended after the shared shape",
     [('--entity-gen-dir $GEN_DIR"', '--entity-gen-dir $GEN_DIR --xlen 64"')],
     ("appends --xlen 64", "design flag --xlen")),
    ("another board's fragment is sourced",
     [("sweep_opts_ax7101.sh", "sweep_opts_arty.sh")],
     ("does not name",)),
    ("another board's fragment is sourced with the provenance check neutered",
     [("sweep_opts_ax7101.sh", "sweep_opts_arty.sh"),
      ('grep -q "$(basename "$DEPLOY_CFG")" "$SHAPE_FRAGMENT" || {',
       'true || {')],
     ("--board",)),
    ("the sourced fragment defines no shape",
     [('. "$SHAPE_FRAGMENT"', 'OPTS=""')],
     ("defines no OPTS",)),
]


def _short(value: str) -> str:
    """A path inside the tree as a repository-relative one.

    deploy.sh composes absolute paths from its own location, so a verdict
    that echoed them back would print the operator's home directory into
    every CI log and every piece of evidence pasted from one."""
    path = Path(value)
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else value


def fragment_opts(path: Path = FRAGMENT) -> str | None:
    """The `OPTS=` line of the generated per-board fragment, or None.

    None is not "no constraint": every caller reports it, because a missing
    fragment is exactly how a launcher falls back to a shape nobody chose."""
    if not path.is_file():
        return None
    match = re.search(r'^OPTS="([^"]*)"', path.read_text(), re.M)
    return match.group(1) if match else None


def run_deploy_sh(text: str, args: list[str]) -> subprocess.CompletedProcess:
    """`deploy.sh <args>`, executed from `text`.

    `bash -c` with $0 set to the real deploy.sh path, so HERE and the repo
    root resolve as they do for the tracked file while the self-test runs a
    mutated copy without writing one into sw/litex.  BAUD is stripped: the
    gate grades the recipe's own binding, never a caller's console override.
    """
    env = {k: v for k, v in os.environ.items() if k != "BAUD"}
    return subprocess.run(["bash", "-c", text, str(DEPLOY)] + args,
                          cwd=DEPLOY.parent, capture_output=True, text=True,
                          env=env)


def deploy_launch_argv(text: str) -> tuple[list[str] | None, str | None]:
    """(the milan_soc.py argv of `deploy.sh build --dry-run`, or a failure).

    The dry run prints the argv `%q`-quoted on the line after its `DRY [...]`
    header, which is the same argv an execution passes, so reading it back
    grades what argparse receives rather than what the script's text looks
    like.  A refusal is a failure, never an empty shape: with the exit status
    ignored, a deploy.sh that refused would be graded on whatever its output
    happened to contain.
    """
    proc = run_deploy_sh(text, ["build", "--dry-run"])
    argv = None
    lines = proc.stdout.splitlines()
    for number, line in enumerate(lines):
        if line.startswith(DRY_MARK) and number + 1 < len(lines):
            tokens = shlex.split(lines[number + 1])
            entry = [i for i, t in enumerate(tokens)
                     if t.endswith(LAUNCH_ENTRY)]
            if entry:
                argv = tokens[entry[0] + 1:]
    if proc.returncode != 0:
        return None, (f"deploy.sh build --dry-run exited {proc.returncode}; "
                      f"it said: {proc.stderr.strip()[-400:]}")
    if argv is None:
        return None, ("deploy.sh build --dry-run printed no "
                      f"{LAUNCH_ENTRY} launch line")
    return argv, None


def derivation_drift(text: str) -> list[str]:
    """deploy.sh READS the shared shape rather than restating it.

    The flag comparisons below would pass a hand-kept copy on the day it was
    written; what they cannot say is that it will still be the config's
    emission tomorrow.  This arm is the property that makes them stay true:
    one source, expanded into the launcher's options.
    """
    bad = []
    if FRAGMENT.name not in text:
        bad.append(f"deploy.sh does not name {FRAGMENT.name}, the generated "
                   "fragment sweep.sh builds from; a shape it spells itself "
                   "is a second shipping shape")
    matches = re.findall(r'^MILAN_OPTS="([^"\n]*)"$', text, re.M)
    if len(matches) != 1:
        bad.append(f"deploy.sh has {len(matches)} MILAN_OPTS assignments, "
                   "want exactly one composed from the fragment")
    elif "$OPTS" not in matches[0] and "${OPTS" not in matches[0]:
        bad.append("deploy.sh's MILAN_OPTS is not derived from the "
                   f"fragment's OPTS: {matches[0][:80]}...")
    return bad


def fragment_parity_drift(argv: list[str]) -> list[str]:
    """The design part of the launch line IS the fragment's OPTS, verbatim.

    Token for token, not flag for flag: this is the acceptance the issue
    states - deploy.sh and sweep.sh elaborate the IDENTICAL option string -
    and an exact comparison is the only one that keeps saying so.  Deploy-only
    additions are therefore appended from `--entity-gen-dir` onward, where
    `appended_drift` grades them one at a time and this report prints them.
    """
    opts = fragment_opts()
    if opts is None:
        return [f"no {FRAGMENT.relative_to(ROOT)}: the deploy shape has no "
                "generated source to be equal to. Regenerate it with "
                f"endstation_builder.py {DEPLOY_CFG} --write-fragment"]
    if GEN_DIR_FLAG not in argv:
        return [f"deploy.sh's launch line has no {GEN_DIR_FLAG} to end its "
                "shared-shape part at"]
    design = argv[:argv.index(GEN_DIR_FLAG)]
    if design == opts.split():
        return []
    return [f"deploy.sh's design argv is not the fragment's OPTS:\n"
            f"      launch line {' '.join(design)}\n"
            f"      fragment    {opts}"]


def config_drift(argv: list[str]) -> list[str]:
    """Every design flag on the launch line against the config's emission.

    The same oracle and the same flag-for-flag comparison
    `check_sweep_shape.check_recipe` applies to build.sh's recipes: an
    absent flag is a milan_soc.py default, not a builder default, which is
    how a launch silently becomes a shape nobody chose (#157).
    """
    flags = parse_flags(argv)
    bad = []
    want_dir = Path(DEPLOY_CFG).stem
    got_dir = flags.get(GEN_DIR_FLAG)
    if got_dir is True or not got_dir:
        bad.append(f"deploy.sh: no {GEN_DIR_FLAG}. milan_soc.py refuses to "
                   f"launch without it; it must name configs/generated/"
                   f"{want_dir}")
    elif Path(str(got_dir).rstrip("/")).name != want_dir:
        bad.append(f"deploy.sh: {GEN_DIR_FLAG} names "
                   f"{Path(str(got_dir).rstrip('/')).name!r} but deploy.sh is "
                   f"graded against {Path(DEPLOY_CFG).name} - the gateware "
                   "and the generated artifacts would be different shapes")
    got = design_flags(flags)
    got.pop(GEN_DIR_FLAG, None)  # checked above, by config basename
    want = design_flags(parse_flags(design_opts_expected(DEPLOY_CFG)))
    for key in sorted(set(got) | set(want)):
        if got.get(key, "(absent)") != want.get(key, "(absent)"):
            bad.append(f"deploy.sh: design flag {key}: launch line "
                       f"{got.get(key, '(absent)')!r} != config-implied "
                       f"{want.get(key, '(absent)')!r} (emit_soc_argv of "
                       f"{Path(DEPLOY_CFG).name})")
    return bad


def render_lane_drift(argv: list[str]) -> list[str]:
    """A declared TDM render lane that would elaborate to nothing (#453).

    Named apart from the flag comparison because the CONSEQUENCE is the
    point and it is invisible in a flag list: milan_soc.py passes
    `p_AUDIO_IF_RENDER_SLOTS_P` only when the flag is above zero, the
    milan_datapath parameter defaults to 0, and 0 takes the
    `g_tdm_render_parked` arm that assigns `tdm_dout_o = 1'b0`.  An option
    string that merely LOSES this one flag builds a board whose render pin
    is dead while every other flag agrees.
    """
    want = parse_flags(design_opts_expected(DEPLOY_CFG)).get(RENDER_FLAG)
    if want is None or want is True or int(want) <= 0:
        return []
    got = parse_flags(argv).get(RENDER_FLAG)
    if got is not True and got is not None and int(got) == int(want):
        return []
    return [f"deploy.sh would build {Path(DEPLOY_CFG).name} with "
            f"{RENDER_FLAG} {'(absent)' if got is None else got} where the "
            f"config declares {want} render slots: milan_datapath would "
            "elaborate AUDIO_IF_RENDER_SLOTS_P = 0, take the "
            "g_tdm_render_parked arm and tie tdm_dout_o (J11.5) to 1'b0, so "
            "the board would render silence"]


def appended_drift(argv: list[str]) -> tuple[list[str], list[str]]:
    """(drifts, the deploy-only flags kept) for the tail after the shape.

    A flow flag, the entity directory, or a repeat of a value the shared
    shape already carries is a deploy-only addition and is REPORTED so it
    stays visible.  Anything else is a design flag this launcher decided by
    itself: argparse takes the last occurrence, so it wins over the shape.
    """
    if GEN_DIR_FLAG not in argv:
        return [], []
    tail = parse_flags(argv[argv.index(GEN_DIR_FLAG):])
    shared = parse_flags((fragment_opts() or "").split())
    bad, kept = [], []
    for key, value in tail.items():
        shown = key if value is True else f"{key} {_short(str(value))}"
        if key == GEN_DIR_FLAG or key in FLOW_FLAGS:
            kept.append(shown)
        elif key in shared and shared[key] == value:
            kept.append(f"{shown} (repeats the shared shape)")
        else:
            bad.append(f"deploy.sh appends {shown} after the shared shape: "
                       "argparse takes the last occurrence, so this is a "
                       "design decision deploy.sh makes alone")
    return bad, kept


def check_deploy(text: str | None = None, quiet: bool = False) -> list[str]:
    """Every arm against one deploy.sh source; the problems, printed."""
    if text is None:
        text = DEPLOY.read_text()
    bad = derivation_drift(text)
    argv, failure = deploy_launch_argv(text)
    if failure:
        bad.append(failure)
    else:
        bad += fragment_parity_drift(argv)
        bad += config_drift(argv)
        bad += render_lane_drift(argv)
        appended, kept = appended_drift(argv)
        bad += appended
    for msg in bad:
        print("DEPLOY SHAPE DRIFT: " + msg, file=sys.stderr)
    if not bad and not quiet:
        print(f"  [deploy-shape] deploy.sh builds {Path(DEPLOY_CFG).name} "
              f"from {FRAGMENT.relative_to(ROOT)}: its design argv is that "
              f"fragment's OPTS token for token, every design flag is "
              f"emit_soc_argv of the config, and {RENDER_FLAG} "
              f"{parse_flags(argv)[RENDER_FLAG]} keeps tdm_dout_o alive")
        print(f"  [deploy-shape] deploy-only additions: {', '.join(kept)}")
    return bad


def _selftest_agrees() -> int:
    """The passing case, asserted rather than assumed.

    Without it every negative control below would pass on a deploy.sh that
    refused everything, and the parity claim would rest on the absence of a
    complaint.  0 = the tracked tree agrees, 2 = it does not."""
    argv, failure = deploy_launch_argv(DEPLOY.read_text())
    if failure:
        print(f"selftest FAILED: {failure}", file=sys.stderr)
        return 2
    opts = fragment_opts()
    design = argv[:argv.index(GEN_DIR_FLAG)] if GEN_DIR_FLAG in argv else argv
    if opts is None or design != opts.split():
        print("selftest FAILED: deploy.sh's design argv is not the "
              f"fragment's OPTS:\n line     {design}\n fragment {opts}",
              file=sys.stderr)
        return 2
    if parse_flags(argv).get(RENDER_FLAG) != "8":
        print("selftest FAILED: the tracked deploy.sh does not launch "
              f"{RENDER_FLAG} 8", file=sys.stderr)
        return 2
    print(f"  [selftest] OK: deploy.sh launches the {len(design)} tokens of "
          f"{FRAGMENT.name} verbatim, {RENDER_FLAG} 8 among them")
    return 0


def _selftest_plants(text: str) -> int:
    """Every DEPLOY_PLANTS mutation, run through deploy.sh's own dry run,
    must be REJECTED naming each expected drift.  0 = all were, 2 = one was
    not (or a plant no longer matches the text it is planted in)."""
    for why, edits, expected in DEPLOY_PLANTS:
        mutated = text
        for old, new in edits:
            if mutated.count(old) != 1:
                print(f"selftest: {old!r} matched {mutated.count(old)} times "
                      f"in deploy.sh, want 1 ({why})", file=sys.stderr)
                return 2
            mutated = mutated.replace(old, new)
        print(f"  [selftest] {why} - expecting REJECT:")
        bad = check_deploy(mutated, quiet=True)
        missing = [e for e in expected if not any(e in drift for drift in bad)]
        if missing:
            print(f"selftest FAILED: {why} did not report {missing!r}",
                  file=sys.stderr)
            return 2
        print(f"  [selftest] OK: {len(bad)} drift(s) reported")
    return 0


def main() -> int:
    """Grade the tracked deploy.sh, then optionally its planted drifts."""
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", "--self-test", action="store_true",
                    help="also prove a deliberately drifted deploy.sh is "
                         "REJECTED")
    args = ap.parse_args()
    if check_deploy():
        print("REFUSING TO DEPLOY: deploy.sh would build a bitstream that is "
              "not the shape the end-station config declares.", file=sys.stderr)
        return 1
    print("deploy shape gate: OK")
    if args.selftest:
        status = _selftest_agrees()
        return status or _selftest_plants(DEPLOY.read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
