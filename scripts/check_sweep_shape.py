#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
check_sweep_shape.py - the sweep-vs-config shape gate.

WHY THIS EXISTS.  `sw/litex/sweep.sh` composes the milan_soc.py command line
that actually produces the flashed bitstream.  Every knob it gets wrong is
invisible until silicon. For example, in 2026-07-26 sweep.sh passed NO
`--num-streams` AT ALL, so
    `sweep.sh ax7101` built the DEFAULT 1x1 datapath while the config, the docs
    and the build directories all called it 8x8.
In 2026-08-22 (#157), two named recipes passed no `--xlen`, so the script
    and declarative configuration could select different CPU widths.
In 2026-09-06 (#362), build.sh launched without the PYTHONHASHSEED=0
    that sweep.sh pins, so the same recipe regenerated a differently
    named CPU core depending on which launcher ran it.
Until 2026-09-09 (#402), build.sh's three named recipes restated the whole
    design argv as shell literals, and this gate kept the copies equal:
    #155 repaired ten divergences at once, #157 and #362 two more. The
    recipes now read the argv out of the builder's artefact, and this gate
    checks the launch line they print instead of the literals they no
    longer carry.

Same shape both times: a build knob that lives in the declarative end-station
config, is NOT carried by the script that builds, and silently defaults.  This
gate makes the divergence a HARD FAILURE instead.

Two modes:

  runtime  (what sweep.sh calls, just before it launches Vivado)
      check_sweep_shape.py --board ax7101 --config configs/endstation_ax7101_8x8.yaml \
                           --num-streams 8 --l2-bytes 16384

  static   (CI / review: no Vivado - parse sweep.sh itself, and read every
            build.sh recipe's launch line out of its own --dry-run)
      check_sweep_shape.py                    # every board in sweep.sh's tables
      check_sweep_shape.py --self-test        # + prove a mismatch is rejected

Exit 0 = agree, 1 = drift (with the offending values printed), 2 = usage/setup.
Needs pyyaml (same dependency as sw/builder/test_builder.py).
"""

import argparse
import collections
import json
import os
import re
import subprocess
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SWEEP = ROOT / "sw/litex/sweep.sh"
BUILD = ROOT / "sw/litex/build.sh"

# build.sh's named recipes are the OTHER path to a flashed bitstream, so they
# get the same treatment: cfg function -> the end-station config it claims to
# build. This is the gate's oracle for build.sh's own recipe_config binding:
# the launch line's --entity-gen-dir and the artefact it was read from must
# both name this config. The deployed 8x8 image came from the x32f1_eto
# sweep; cfg_ax8x8 has never produced a bitstream.
BUILD_CFGS = {
    "ax7101": "configs/endstation_ax7101_1x1_tdm8.yaml",
    "ax8x8": "configs/endstation_ax7101_8x8.yaml",
    "arty":  "configs/endstation_arty_current.yaml",
}

# FLOW flags, not DESIGN flags: launch directives and per-run paths that
# emit_soc_argv deliberately does not own. The config comparison ignores only
# this explicit set; --entity-gen-dir is checked separately because it must
# name the same config as BUILD_CFGS.
FLOW_FLAGS = {
    "--synth-directive", "--opt-directive", "--place-directive",
    "--vivado-max-threads", "--output-dir", "--build",
}

#: What one `build.sh <name> --dry-run` said: the milan_soc.py argv on the
#: launch line launch_jobs prints, the artefact design_argv read it from and
#: the config it regenerated (both off the provenance line expand_jobs
#: prints), or `failure` naming why none of that could be read.
DryRun = collections.namedtuple("DryRun",
                                ("argv", "artefact", "config", "failure"))

#: expand_jobs' provenance line, the one place build.sh names the artefact.
PROVENANCE_RE = re.compile(
    r"^\[(\w+)\] design argv from (\S+) \(regenerated from (\S+)\)")

# Negative controls for the named-build branch, planted in build.sh's TEXT
# and executed in place (see dry_run): each is a way the launch line can
# stop being the config's emission now that no recipe restates it. A
# hand-appended literal wins in argparse (last occurrence), which is why the
# first two plants are the #157 CPU keys; the rebind is #155's "another
# config's artefacts"; the reader plant is the absent-flag class; the last
# one is the sourcing itself reverted. Every plant must apply exactly once.
#   (why, old fragment, new fragment, the drifts it must report)
BUILD_PLANTS = [
    ("cfg_ax8x8 hand-appends an RV64 --xlen after the sourced argv",
     '--place-directive AltSpreadLogic_high"',
     '--place-directive AltSpreadLogic_high --xlen 64"',
     ("cfg_ax8x8: design flag --xlen:",)),
    ("cfg_arty hand-appends a second hart",
     'echo ""', 'echo "--cpu-count 2"',
     ("cfg_arty: design flag --cpu-count:",)),
    ("cfg_ax8x8 is rebound to the 1x1 config",
     'ax8x8)  echo "configs/endstation_ax7101_8x8.yaml";;',
     'ax8x8)  echo "configs/endstation_ax7101_1x1_tdm8.yaml";;',
     ("cfg_ax8x8: --entity-gen-dir names",
      "cfg_ax8x8: design flag --num-streams:",
      "cfg_ax8x8: build.sh regenerated")),
    ("the reader drops the first design flag pair",
     'print(" ".join(argv))', 'print(" ".join(argv[2:]))',
     ("cfg_ax7101: design flag --board:", "cfg_arty: design flag --board:")),
    ("the launch line drops the sourced argv",
     "exec python3 milan_soc.py $args ", "exec python3 milan_soc.py ",
     ("cfg_ax7101: no --entity-gen-dir", "cfg_ax8x8: no --entity-gen-dir",
      "cfg_arty: no --entity-gen-dir")),
]

# Ways build.sh's regeneration can FAIL, planted in its text and executed in
# place. design_argv runs inside a command substitution, where bash drops
# errexit, so each of these once returned 0 with the PREVIOUS artefact on the
# launch line under a provenance line that said it had been regenerated: the
# #157 divergence class on the failure path. Deleting the regeneration line
# proves nothing about a regeneration that RAN and failed, so every plant
# keeps the line and breaks the run instead.
#   (why, old fragment, new fragment, what the refusal must name)
REGENERATION_PLANTS = [
    ("the builder run fails",
     '"$REPO_ROOT/sw/builder/endstation_builder.py" "$REPO_ROOT/$cfg" > /dev/null',
     '"$REPO_ROOT/sw/builder/endstation_builder.py" "$REPO_ROOT/$cfg"'
     ' --selftest-no-such-flag > /dev/null',
     "endstation_builder.py exited"),
    ("the artefact cannot be read",
     "json.loads(artefact.read_text())",
     'json.loads(artefact.read_text() + "!")',
     "cannot be read"),
    ("the artefact carries no design argv",
     'argv = params.get("argv")', 'argv = params.get("argv_absent")',
     "carries no design argv"),
    ("the artefact is another config's emission",
     'echo "$REPO_ROOT/sw/builder/out/$(basename "$1" .yaml)/soc_params.json"',
     'echo "$REPO_ROOT/sw/builder/out/endstation_ax7101_8x8/soc_params.json"',
     "was generated from"),
]

# BUILD_CFG values that must be REFUSED by name, before any builder run: the
# stem of that path picks BOTH the artefact design_argv reads and the
# configs/generated include --entity-gen-dir names, so a same-stem config
# anywhere else pairs one config's argv with another config's shape include.
# Whether the file exists is not the point; where it is, is.
#   (why, the BUILD_CFG value)
#: The phrase build.sh's own refusal carries. A control that accepted any
#: non-zero exit would be satisfied by "no such config", which is a
#: DIFFERENT refusal and would let the rule itself be deleted.
BUILD_CFG_RULE = "DIRECTLY under configs/"
BUILD_CFG_REJECTS = [
    ("a file that is not under configs/", "README.md"),
    ("a config one level below configs/", "configs/generated/probe.yaml"),
    ("an absolute path to a real config",
     str(ROOT / "configs/endstation_arty_current.yaml")),
    ("a .yml spelling, whose artefact path the launcher would miss",
     "configs/endstation_arty_current.yml"),
]


def _yaml():
    try:
        import yaml
    except ImportError:
        sys.exit("check_sweep_shape: pyyaml required (pip install pyyaml)")
    return yaml


def config_shape(path: str | Path) -> tuple[str, int, int, bool]:
    """(board, num_streams, l2_bytes, render_lpf) implied by a config.

    num_streams == milan_datapath N_STREAMS == the WIDER of the two stream
    directions, exactly as sw/builder/endstation_builder.emit_soc_argv computes
    it - kept as one line here on purpose so the two can be eyeballed together.
    """
    yaml = _yaml()
    cfg_file = Path(path)
    if not cfg_file.is_absolute():
        cfg_file = ROOT / cfg_file
    if not cfg_file.exists():
        sys.exit(f"check_sweep_shape: no such config {cfg_file}")
    with cfg_file.open() as handle:
        cfg = yaml.safe_load(handle)
    s = cfg.get("streams") or {}
    n_streams = max(len(s.get("listeners") or []), len(s.get("talkers") or []))
    board_cfg = cfg.get("board") or {}
    c = board_cfg.get("constraints") or {}
    features = board_cfg.get("features") or {}
    # render_lpf is the milan_datapath LPF_P area lever
    # (docs/design/AREA_BUDGET.md). Absent = filter PRESENT, which is
    # what every config said before 2026-07-27, so the default keeps old
    # configs byte-identical. It is gated here for the same reason
    # --eth-port is: it changes the BITSTREAM, one board at
    # a time, and a silent divergence between build.sh and sweep.sh is how
    # this project has lost builds twice.
    return (board_cfg["target"], n_streams, int(c["l2_bytes"]),
            bool(features.get("render_lpf", True)))


def parse_sweep(path: str | Path = SWEEP) -> dict[str, dict[str, str | int]]:
    """sweep.sh's per-board default tables -> {board: {opts,l2,ns,cfg}}.

    Deliberately the SAME parse shape test_builder.sweep_inline() uses for
    OPTS/L2, extended with the NS/CFG line - if either table is reformatted
    so this regex misses, the gate fails loudly rather than passing vacuously.
    """
    txt = Path(path).read_text()
    boards = {}
    for m in re.finditer(r'^\s*(\w+)\)\s+OPTS="([^"]+)"; L2=(\d+);',
                         txt, re.M):
        boards[m.group(1)] = dict(opts=m.group(2), l2=int(m.group(3)))
    if not boards:
        sys.exit(f"check_sweep_shape: no OPTS/L2 table found in {path}")
    # The surrounding quotes on the CFG assignment are OPTIONAL to this parse.
    # They were added by Rule 13's unquoted-expansion repair (SC2086), which is
    # correct shell - a config path with a space must survive the assignment -
    # and this regex rejected the whole table the moment they appeared, so the
    # gate exited "sweep.sh has no NS/CFG line for arty, ax7101" on a sweep.sh
    # that had simply been quoted. A shape gate must read the shape, not one
    # spelling of it.
    for m in re.finditer(r'^\s*(\w+)\)\s+NS=(\d+); CFG="?\$\{SWEEP_CFG:-([^}]+)\}"?',
                         txt, re.M):
        if m.group(1) in boards:
            boards[m.group(1)]["ns"] = int(m.group(2))
            boards[m.group(1)]["cfg"] = m.group(3)
    missing = [b for b, v in boards.items() if "ns" not in v]
    if missing:
        sys.exit("check_sweep_shape: sweep.sh has no NS/CFG line for "
                 + ", ".join(sorted(missing)))
    return boards


def design_opts_expected(cfg_path: str | Path) -> list[str]:
    """The complete SoC flag list this config implies, from the builder's
    own emission (sw/builder/endstation_builder.emit_soc_argv).

    Imported, not re-derived: interface_is_placeholder / framer_wire_channels
    / the tier-1 prune resolution are real logic, and a second copy here is
    exactly the kind that drifts. The import is in-repo and costs pyyaml,
    which this script already requires."""
    sys.path.insert(0, str(ROOT / "sw/builder"))
    import endstation_builder as eb
    p = Path(cfg_path)
    return eb.emit_soc_argv(eb.load_config(p if p.is_absolute() else ROOT / p))


def parse_flags(tokens: list[str]) -> dict[str, str | bool]:
    """['--a', '1', '--b'] -> {'--a': '1', '--b': True}. Values never start
    with '--', so a missing value cannot swallow the next flag."""
    d = {}
    for i, t in enumerate(tokens):
        if t.startswith("--"):
            nxt = tokens[i + 1] if i + 1 < len(tokens) else None
            d[t] = nxt if (nxt and not nxt.startswith("--")) else True
    return d


def compare(board: str, cfg_path: str | Path, ns: int, l2: int, where: str,
            opts: str = "") -> list[str]:
    """One board's effective shape vs its config. Returns a list of problems.

    `cfg_path` is echoed back VERBATIM in the drift header, because it is the
    spelling sweep.sh's table (or the command line) used and that is what a
    reader has to go and edit.
    """
    c_board, c_ns, c_l2, c_lpf = config_shape(cfg_path)
    bad = []
    if c_board != board:
        bad.append(f"config board {c_board!r} != sweep board {board!r}")
    if c_ns != ns:
        bad.append(f"--num-streams {ns} != config streams {c_ns} "
                   f"(max(listeners, talkers)) - the bitstream would be "
                   f"{ns}x{ns}, the config says {c_ns}x{c_ns}")
    if c_l2 != l2:
        bad.append(f"--l2-bytes {l2} != config l2_bytes {c_l2}")
    lpf = "--no-render-lpf" not in opts
    if c_lpf != lpf:
        bad.append(f"--no-render-lpf {'absent' if lpf else 'present'} != "
                   f"config render_lpf {c_lpf} - the LPF_P area lever must be "
                   "spent (or not) in exactly one place per board")
    # FULL design-flag equality (2026-07-28). The per-key checks above catch
    # the knobs that have burned this project by name; this catches the ones
    # that have not burned it YET. Both members of this gate's header class
    # recurred in one day - the tier-1 prunes and then the whole
    # audio-interface/wire-chans group reached the build plan but not the
    # fragment, so three seeds fitted a default-I2S 2-channel datapath that
    # every artifact called tdm32 8-channel - because the fragment carried a
    # hand-picked SUBSET of the design flags and this gate compared the same
    # subset. Now: effective OPTS must equal the builder's emit_soc_argv
    # flag-for-flag (parsed, so ordering cannot hide a value swap; the
    # --num-streams sweep.sh may append is part of the expectation already).
    if opts:
        got = parse_flags(opts.split())
        want = parse_flags(design_opts_expected(cfg_path))
        for k in sorted(set(got) | set(want)):
            if got.get(k) != want.get(k):
                bad.append(
                    f"design flag {k}: effective "
                    f"{got.get(k, '(absent)')} != config-implied "
                    f"{want.get(k, '(absent)')} (emit_soc_argv of "
                    f"{Path(cfg_path).name})")
    if bad:
        print(f"SHAPE DRIFT [{where}] {board} vs {cfg_path}:", file=sys.stderr)
        for b in bad:
            print(f"  - {b}", file=sys.stderr)
    else:
        print(f"  [sweep-shape] {board}: num-streams {ns}, "
              f"l2 {l2}, render-lpf {lpf} == {Path(cfg_path).name}")
    return bad


def check_fragment(board: str) -> int | None:
    """The generated fragment may pin NS too (it is sourced AFTER the defaults).
    When it does, it is authoritative and must agree; when it does not, say so -
    silence is what let the 8x8 build ship as 1x1."""
    p = ROOT / "configs/generated" / f"sweep_opts_{board}.sh"
    if not p.exists():
        return None
    txt = p.read_text()
    m = re.search(r"^NS=(\d+)\s*$", txt, re.M)
    if m:
        return int(m.group(1))
    m = re.search(r"--num-streams[= ]+(\d+)", txt)
    return int(m.group(1)) if m else None


def recipe_names(text: str) -> list[str]:
    """Every `cfg_<name>()` recipe build.sh declares, in file order."""
    names = re.findall(r"^cfg_(\w+)\(\)", text, re.M)
    if not names:
        sys.exit("check_sweep_shape: no cfg_* recipes found in build.sh")
    return names


def run_build_sh(text: str, args: list[str], build_cfg: str | None = None
                 ) -> subprocess.CompletedProcess:
    """`build.sh <args>`, executed from `text`.

    `bash -c` with $0 set to the real build.sh path, so SOC_DIR and
    REPO_ROOT resolve as they do for the tracked file while the self-test
    runs a mutated copy without writing one into sw/litex. BUILD_CFG is
    stripped: the gate grades the recipes' own bindings, never a caller's
    override. A control that is ABOUT BUILD_CFG passes one.
    """
    env = {k: v for k, v in os.environ.items() if k != "BUILD_CFG"}
    if build_cfg is not None:
        env["BUILD_CFG"] = build_cfg
    return subprocess.run(["bash", "-c", text, str(BUILD)] + args,
                          cwd=BUILD.parent, capture_output=True, text=True,
                          env=env)


def dry_run(text: str, name: str) -> DryRun:
    """`build.sh <name> --dry-run`, executed from `text`, read back."""
    proc = run_build_sh(text, [name, "--dry-run"])
    argv = artefact = config = None
    for line in proc.stdout.splitlines():
        m = PROVENANCE_RE.match(line)
        if m and m.group(1) == name:
            artefact, config = m.group(2), m.group(3)
        tokens = line.split()
        if LAUNCH_ENTRY in tokens:
            argv = tokens[tokens.index(LAUNCH_ENTRY) + 1:]
    failure = None
    if proc.returncode != 0:
        said = proc.stderr.strip().splitlines() or [proc.stdout[-300:]]
        failure = (f"build.sh {name} --dry-run exited {proc.returncode}: "
                   f"{said[-1]}")
    elif argv is None:
        failure = f"build.sh {name} --dry-run printed no {LAUNCH_ENTRY} launch line"
    elif artefact is None:
        failure = (f"build.sh {name} --dry-run named no artefact for its "
                   "design argv (no provenance line)")
    return DryRun(argv, artefact, config, failure)


def design_flags(flags: dict[str, str | bool]) -> dict[str, str | bool]:
    """Drop launcher-only flags and compare the Scala profile as one value."""
    design, scala = {}, []
    for key, value in flags.items():
        if key in FLOW_FLAGS:
            continue
        if key.startswith("--scala-args="):
            scala.append(key[len("--scala-args="):])
            continue
        design[key] = value
    if scala:
        design["--scala-args"] = " ".join(sorted(scala))
    return design


def _entity_gen_dir_agrees(name, cfg_path, flags):
    """Require a recipe to use the generated artifacts for its graded config.
    Returns the drift as a one-element list; the caller prints it."""
    want = Path(cfg_path).stem
    got = flags.get("--entity-gen-dir")
    msg = None
    if got is True or not got:
        msg = (f"cfg_{name}: no --entity-gen-dir. milan_soc.py refuses to "
               f"launch without it, so this recipe cannot be run at all; it "
               f"must name configs/generated/{want}")
    elif Path(str(got).rstrip("/")).name != want:
        msg = (f"cfg_{name}: --entity-gen-dir names "
               f"{Path(str(got).rstrip('/')).name!r} but this recipe "
               f"is graded against {Path(cfg_path).name} - the "
               f"gateware and generated artifacts would be different shapes")
    return [] if msg is None else [msg]


def artefact_drift(name: str, cfg_path: str, run: DryRun) -> list[str]:
    """The artefact the recipe read is the graded config's CURRENT emission.

    Freshness by construction is what build.sh promises (it regenerates in
    the same shell); this proves the promise: the artefact exists, names the
    config as its source, was regenerated FROM that config, and its argv is
    emit_soc_argv of it right now.
    """
    bad = []
    if run.config != cfg_path:
        bad.append(f"cfg_{name}: build.sh regenerated {run.config} for a "
                   f"recipe graded against {cfg_path}")
    artefact = Path(run.artefact)
    if not artefact.is_file():
        return bad + [f"cfg_{name}: the launch line was read from "
                      f"{artefact}, which does not exist"]
    data = json.loads(artefact.read_text())
    if data.get("_source_config") != cfg_path:
        bad.append(f"cfg_{name}: {artefact.name} was generated from "
                   f"{data.get('_source_config')!r}, not {cfg_path!r}")
    if data.get("argv") != design_opts_expected(cfg_path):
        bad.append(f"cfg_{name}: {artefact} is stale: its argv is not "
                   f"emit_soc_argv of {Path(cfg_path).name} - regenerate it")
    return bad


def check_recipe(name: str, cfg_path: str, run: DryRun,
                 quiet: bool = False) -> list[str]:
    """One recipe's dry-run launch line against its config, flag for flag.

    The launch line is graded as argparse reads it (last occurrence wins),
    so a literal hand-appended after the sourced argv is a value drift, not
    a duplicate nobody sees.
    """
    if run.failure:
        msg = f"cfg_{name}: {run.failure}"
        print("SHAPE DRIFT: " + msg, file=sys.stderr)
        return [msg]
    flags = parse_flags(run.argv)
    bad = _entity_gen_dir_agrees(name, cfg_path, flags)
    got = design_flags(flags)
    got.pop("--entity-gen-dir", None)  # checked above, by config basename
    want = design_flags(parse_flags(design_opts_expected(cfg_path)))
    n_ok = 0
    for k in sorted(set(got) | set(want)):
        g, w = got.get(k, "(absent)"), want.get(k, "(absent)")
        if g != w:
            bad.append(f"cfg_{name}: design flag {k}: launch line {g!r} != "
                       f"config-implied {w!r} (emit_soc_argv of "
                       f"{Path(cfg_path).name})")
        else:
            n_ok += 1
    bad += artefact_drift(name, cfg_path, run)
    for msg in bad:
        print("SHAPE DRIFT: " + msg, file=sys.stderr)
    if not bad and not quiet:
        artefact = Path(run.artefact)
        shown = (artefact.relative_to(ROOT) if artefact.is_relative_to(ROOT)
                 else artefact)
        print(f"  [sweep-shape] build.sh cfg_{name}: {n_ok} design flags on "
              f"the dry-run launch line agree with {Path(cfg_path).name} "
              f"flag for flag, --entity-gen-dir names it, and {shown} is "
              "its current emission")
    return bad


def check_build_sh(text: str | None = None,
                   quiet: bool = False) -> list[str]:
    """Every build.sh recipe's launch line against emit_soc_argv, flag for
    flag, read out of build.sh's own --dry-run rather than its text.

    Since #402 the recipes carry no design literal to parse: what they
    launch is the builder's artefact plus flow flags, so the only honest
    comparison is the line they print. `text` is build.sh's source (the
    tracked file by default; a mutated copy under --self-test); `quiet`
    suppresses the agreement summaries while negative controls run.
    """
    if text is None:
        text = BUILD.read_text()
    names = recipe_names(text)
    bad = []
    for name in sorted(set(names) - set(BUILD_CFGS)):
        msg = (f"build.sh cfg_{name} has no config binding in BUILD_CFGS; "
               "an ungraded recipe could silently build a different shape")
        print("SHAPE DRIFT: " + msg, file=sys.stderr)
        bad.append(msg)
    for name, cfg_path in sorted(BUILD_CFGS.items()):
        if name not in names:
            msg = f"build.sh has no cfg_{name}"
            print("SHAPE DRIFT: " + msg, file=sys.stderr)
            bad.append(msg)
            continue
        bad += check_recipe(name, cfg_path, dry_run(text, name), quiet)
    return bad


def run_static(sweep_path: str | Path = SWEEP,
               quiet: bool = False) -> list[str]:
    """Every board in sweep.sh against its config, plus the generated fragment.

    The fragment is checked as well as the default table because it is
    sourced AFTER the defaults: a fragment pinning a different NS wins, and
    winning silently is exactly how the 8x8 build shipped as 1x1.
    """
    boards = parse_sweep(sweep_path)
    bad = []
    for board, v in sorted(boards.items()):
        bad += compare(board, v["cfg"], v["ns"], v["l2"],
                       Path(sweep_path).name, opts=v["opts"])
        frag_ns = check_fragment(board)
        if frag_ns is not None and frag_ns != v["ns"]:
            msg = (f"{board}: generated fragment pins NS={frag_ns} but "
                   f"sweep.sh's default is {v['ns']} - the fragment is sourced "
                   "AFTER the defaults, so the fragment would win silently")
            print("SHAPE DRIFT: " + msg, file=sys.stderr)
            bad.append(msg)
        elif frag_ns is None and not quiet:
            print(f"  [sweep-shape] {board}: generated fragment carries no NS "
                  f"- sweep.sh's default ({v['ns']}) stands")
    return bad


#: The environment line both launchers must place BEFORE milan_soc.py runs.
#: LiteX spells the CPU ISA argument from a Python set, the pinned core's
#: netlist cache hashes that spelling, and an unpinned seed spells it
#: differently in every process: the cache misses, the core regenerates, and
#: the regenerated core placed anywhere between 12122 and 12661 LUTs across
#: six otherwise-identical builds (sweep.sh, 2026-08-02). build.sh shipped
#: without it until #362 (2026-09-06), so the two launchers had drifted.
LAUNCH_SEED = "export PYTHONHASHSEED=0"
LAUNCH_ENTRY = "milan_soc.py"
#: The first FLOW flag design_argv appends: everything before it on the launch
#: line is the design argv the artefact supplied, verbatim.
LAUNCH_GEN_DIR = "--entity-gen-dir"


def launch_seed_position(text: str) -> tuple[int | None, int | None]:
    """(line of the seed export, line of the first milan_soc.py launch).

    The seed export is recognised as a whole shell line or as a `&&` member
    of a composed command string; the launch is the first line that names
    the SoC script. Either is None when absent, so the caller can name what
    is missing instead of guessing.
    """
    seed = launch = None
    seed_re = re.compile(rf"(^|[\s\"'])+{re.escape(LAUNCH_SEED)}(\s|&&|\"|$)")
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if seed is None and seed_re.search(line):
            seed = number
        if launch is None and LAUNCH_ENTRY in line:
            launch = number
    return seed, launch


def check_launch_seed(build_path: str | Path = BUILD,
                      sweep_path: str | Path = SWEEP,
                      quiet: bool = False) -> list[str]:
    """Both launchers export the hash seed before the SoC script runs (#362).

    The two entry points to a flashed bitstream must agree on this or the
    same recipe builds a differently named, freshly regenerated core
    depending on which script launched it. Missing or late is drift.
    """
    bad = []
    for path in (Path(build_path), Path(sweep_path)):
        seed, launch = launch_seed_position(path.read_text())
        if launch is None:
            msg = f"{path.name}: no line launches {LAUNCH_ENTRY}"
        elif seed is None:
            msg = (f"{path.name}: launches {LAUNCH_ENTRY} without "
                   f"`{LAUNCH_SEED}`; the CPU netlist name would depend on "
                   "the process")
        elif seed > launch:
            msg = (f"{path.name}: `{LAUNCH_SEED}` on line {seed} comes after "
                   f"the {LAUNCH_ENTRY} launch on line {launch}")
        else:
            if not quiet:
                print(f"  [sweep-shape] {path.name}: `{LAUNCH_SEED}` on line "
                      f"{seed} precedes the {LAUNCH_ENTRY} launch on line "
                      f"{launch}")
            continue
        print("SHAPE DRIFT: " + msg, file=sys.stderr)
        bad.append(msg)
    return bad


def _temp_sh(text: str) -> Path:
    """`text` written to a throwaway .sh; the caller unlinks the path."""
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
        f.write(text)
        return Path(f.name)


def _self_test_sweep_ns(sweep_path):
    """Negative control: every board's NS bumped by one in a COPY of sweep.sh
    must be REJECTED. Without it the gate could be vacuously green (e.g. a
    regex that stopped matching). 0 = rejected as required, 2 = it was not."""
    txt = Path(sweep_path).read_text()
    mut = re.sub(r'^(\s*\w+\)\s+NS=)(\d+)',
                 lambda m: m.group(1) + str(int(m.group(2)) + 1),
                 txt, flags=re.M)
    if mut == txt:
        print("self-test: could not mutate NS in sweep.sh", file=sys.stderr)
        return 2
    tmp = _temp_sh(mut)
    try:
        print("  [self-test] mutated NS (+1 per board) - expecting REJECT:")
        bad_mut = run_static(tmp, quiet=True)
    finally:
        tmp.unlink()
    if not bad_mut:
        print("self-test FAILED: a wrong NS was accepted", file=sys.stderr)
        return 2
    print(f"  [self-test] OK: {len(bad_mut)} drift(s) reported for the "
          "mutated sweep.sh")
    return 0


def _self_test_build_plants(build_text):
    """Negative controls for the named-build branch: every BUILD_PLANTS
    mutation, run through build.sh's own dry-run, must be REJECTED naming
    each expected drift. 0 = all were, 2 = one was not (or a plant no
    longer matches the text it is planted in)."""
    for why, old, new, expected in BUILD_PLANTS:
        if build_text.count(old) != 1:
            print(f"self-test: {old!r} matched {build_text.count(old)} "
                  f"times in build.sh, want 1 ({why})", file=sys.stderr)
            return 2
        print(f"  [self-test] {why} - expecting REJECT:")
        bad_mut = check_build_sh(build_text.replace(old, new), quiet=True)
        missing = [e for e in expected
                   if not any(e in drift for drift in bad_mut)]
        if missing:
            print(f"self-test FAILED: {why} did not report {missing!r}",
                  file=sys.stderr)
            return 2
        print(f"  [self-test] OK: {len(bad_mut)} drift(s) reported")
    return 0


def _self_test_regeneration(build_text):
    """The regeneration is JUDGED, not merely run.

    Every plant keeps the regeneration line and breaks the run itself,
    which is the case a deleted-line control cannot reach. Each must end
    `build.sh` non-zero with NO launch line and NO provenance line, in a
    dry run as in a launch, and say what failed. 0 = every one refused,
    2 = one went through.
    """
    for why, old, new, named in REGENERATION_PLANTS:
        if build_text.count(old) != 1:
            print(f"self-test: {old!r} matched {build_text.count(old)} times "
                  f"in build.sh, want 1 ({why})", file=sys.stderr)
            return 2
        mutated = build_text.replace(old, new)
        print(f"  [self-test] {why} - expecting REFUSAL:")
        proc = run_build_sh(mutated, ["arty", "--dry-run"])
        if proc.returncode == 0 or LAUNCH_ENTRY in proc.stdout or any(
                PROVENANCE_RE.match(line)
                for line in proc.stdout.splitlines()):
            print(f"self-test FAILED: {why} and build.sh exited "
                  f"{proc.returncode}, printing:\n{proc.stdout[-400:]}",
                  file=sys.stderr)
            return 2
        if named not in proc.stderr:
            print(f"self-test FAILED: {why} and the refusal did not name "
                  f"{named!r}: {proc.stderr.strip()[-300:]}", file=sys.stderr)
            return 2
        print(f"  [self-test] OK: build.sh exited {proc.returncode}, no "
              f"launch line, no provenance line, refusal names {named!r}")
    # The gate must REPORT that refusal rather than read a stale line as a
    # pass: with the exit status ignored, a launcher that refused would be
    # graded on whatever its output happened to contain.
    why, old, new, _ = REGENERATION_PLANTS[0]
    bad_mut = check_build_sh(build_text.replace(old, new), quiet=True)
    if not any("--dry-run exited" in drift for drift in bad_mut):
        print(f"self-test FAILED: the gate did not report {why} as a "
              f"non-zero exit of build.sh ({bad_mut})", file=sys.stderr)
        return 2
    print(f"  [self-test] OK: the gate reports it as a non-zero exit "
          f"({len(bad_mut)} drift(s))")
    return 0


def _self_test_provenance_agrees(build_text):
    """The passing case, asserted rather than assumed.

    For every recipe: the provenance line names the config the recipe is
    bound to, the artefact it names exists, that artefact says the same
    config wrote it, and the design part of the launch line is that
    artefact's argv VERBATIM. Without it the negative controls above would
    all pass on a launcher that refused everything.
    """
    for name, cfg_path in sorted(BUILD_CFGS.items()):
        run = dry_run(build_text, name)
        if run.failure:
            print(f"self-test FAILED: {run.failure}", file=sys.stderr)
            return 2
        artefact = Path(run.artefact)
        if run.config != cfg_path or not artefact.is_file():
            print(f"self-test FAILED: cfg_{name}'s provenance line names "
                  f"{run.config} and {artefact}", file=sys.stderr)
            return 2
        params = json.loads(artefact.read_text())
        if params.get("_source_config") != cfg_path:
            print(f"self-test FAILED: {artefact} says "
                  f"{params.get('_source_config')!r} wrote it, and the "
                  f"provenance line says {cfg_path}", file=sys.stderr)
            return 2
        if LAUNCH_GEN_DIR not in run.argv:
            print(f"self-test FAILED: cfg_{name}'s launch line has no "
                  f"{LAUNCH_GEN_DIR} to end its design part at",
                  file=sys.stderr)
            return 2
        design = run.argv[:run.argv.index(LAUNCH_GEN_DIR)]
        if design != params.get("argv"):
            print(f"self-test FAILED: cfg_{name}'s launch line is not the "
                  f"argv of the artefact its provenance line names:\n"
                  f" line     {design}\n artefact {params.get('argv')}",
                  file=sys.stderr)
            return 2
        print(f"  [self-test] OK: cfg_{name} launched the {len(design)} "
              f"design tokens of the artefact it says it regenerated from "
              f"{cfg_path}")
    return 0


def _self_test_artefact_arms():
    """Each arm of `artefact_drift`, against a planted temporary artefact.

    The comparisons the freshness claim rests on - the config the launcher
    regenerated, the config the artefact names as its source, and the argv
    being emit_soc_argv right now - are graded one at a time, so none can
    be deleted or inverted while every other control stays green. The rows
    are synthetic: nothing in the tree is written.
    """
    name, cfg_path = "arty", BUILD_CFGS["arty"]
    argv = design_opts_expected(cfg_path)
    stale = list(argv)
    stale[stale.index("--xlen") + 1] = "64"
    rows = [
        ("an artefact another config wrote", cfg_path,
         {"_source_config": "configs/endstation_ax7101_8x8.yaml",
          "argv": argv}, "was generated from"),
        ("an artefact whose argv is not that config's current emission",
         cfg_path, {"_source_config": cfg_path, "argv": stale}, "is stale"),
        ("a launcher that regenerated another config",
         "configs/endstation_ax7101_8x8.yaml",
         {"_source_config": cfg_path, "argv": argv}, "build.sh regenerated"),
    ]
    tmp = Path(tempfile.mkdtemp()) / "soc_params.json"
    try:
        for why, regenerated, params, expected in rows:
            tmp.write_text(json.dumps(params))
            print(f"  [self-test] {why} - expecting REJECT:")
            bad = artefact_drift(name, cfg_path,
                                 DryRun(argv, str(tmp), regenerated, None))
            if not any(expected in drift for drift in bad):
                print(f"self-test FAILED: {why} did not report "
                      f"{expected!r} ({bad})", file=sys.stderr)
                return 2
            print(f"  [self-test] OK: {len(bad)} drift(s) reported")
        tmp.write_text(json.dumps({"_source_config": cfg_path, "argv": argv}))
        bad = artefact_drift(name, cfg_path, DryRun(argv, str(tmp),
                                                    cfg_path, None))
        if bad:
            print(f"self-test FAILED: a current artefact was reported as "
                  f"drifted ({bad})", file=sys.stderr)
            return 2
        tmp.unlink()
        bad = artefact_drift(name, cfg_path, DryRun(argv, str(tmp),
                                                    cfg_path, None))
        if not any("does not exist" in drift for drift in bad):
            print(f"self-test FAILED: a missing artefact was accepted "
                  f"({bad})", file=sys.stderr)
            return 2
    finally:
        shutil.rmtree(tmp.parent, ignore_errors=True)
    print("  [self-test] OK: a current artefact reports nothing, a missing "
          "one is rejected")
    return 0


def _self_test_build_cfg_scope(build_text):
    """BUILD_CFG is limited to configs/, and the refusal comes first.

    Every value in BUILD_CFG_REJECTS must be refused BY THE RULE with no
    launch line, and a config that IS under configs/ must still rebind the
    recipe - otherwise the rule could be kept by refusing everything.
    """
    for why, value in BUILD_CFG_REJECTS:
        print(f"  [self-test] BUILD_CFG is {why} - expecting REFUSAL:")
        proc = run_build_sh(build_text, ["arty", "--dry-run"], build_cfg=value)
        if proc.returncode == 0 or LAUNCH_ENTRY in proc.stdout:
            print(f"self-test FAILED: BUILD_CFG={value} was accepted "
                  f"(exit {proc.returncode})", file=sys.stderr)
            return 2
        if BUILD_CFG_RULE not in proc.stderr:
            print(f"self-test FAILED: BUILD_CFG={value} was refused without "
                  f"naming the rule ({BUILD_CFG_RULE!r}): "
                  f"{proc.stderr.strip()[-300:]}", file=sys.stderr)
            return 2
        print(f"  [self-test] OK: build.sh exited {proc.returncode} naming "
              f"the rule ({BUILD_CFG_RULE!r})")
    rebind = BUILD_CFGS["ax8x8"]
    print(f"  [self-test] BUILD_CFG={rebind} on cfg_arty - expecting ACCEPT:")
    proc = run_build_sh(build_text, ["arty", "--dry-run"], build_cfg=rebind)
    if proc.returncode != 0 or LAUNCH_ENTRY not in proc.stdout:
        print(f"self-test FAILED: a config under configs/ was refused "
              f"(exit {proc.returncode}): {proc.stderr.strip()[-300:]}",
              file=sys.stderr)
        return 2
    if f"(regenerated from {rebind})" not in proc.stdout:
        print(f"self-test FAILED: BUILD_CFG={rebind} did not rebind cfg_arty",
              file=sys.stderr)
        return 2
    print("  [self-test] OK: the recipe was rebound to a config under configs/")
    return 0


def _self_test_unbound_recipe(build_text):
    """A newly added cfg_* function must not escape grading merely because
    BUILD_CFGS was not extended with its declarative config. 0 = the unbound
    recipe was rejected, 2 = it was accepted (or the anchor moved)."""
    unbound_recipe = (
        "cfg_unbound_selftest() {\n"
        "    echo \"--board arty --cpu vexiiriscv --cpu-count 1 "
        "--xlen 32\"\n"
        "}\n\n")
    mutated, count = re.subn(r"^(SWEEP_DIRECTIVES=)",
                             unbound_recipe + r"\1", build_text,
                             count=1, flags=re.M)
    if count != 1:
        print("self-test: SWEEP_DIRECTIVES anchor not found in build.sh",
              file=sys.stderr)
        return 2
    print("  [self-test] unbound cfg_* recipe - expecting REJECT:")
    bad_mut = check_build_sh(mutated, quiet=True)
    if not any("cfg_unbound_selftest has no config binding" in drift
               for drift in bad_mut):
        print("self-test FAILED: unbound cfg_* recipe was accepted",
              file=sys.stderr)
        return 2
    print("  [self-test] OK: unbound cfg_* recipe rejected")
    return 0


def _self_test_launch_seed(build_text: str, sweep_path: str | Path) -> int:
    """Negative controls for the seed export (#362): each launcher with its
    `export PYTHONHASHSEED=0` removed, then build.sh with the export moved
    after the exec line, must be REJECTED naming that launcher. 0 = all
    were, 2 = one was not (or a plant no longer matches)."""
    sweep_text = Path(sweep_path).read_text()
    seed_line = f"cmd+=\"{LAUNCH_SEED} && \"\n"
    unseeded = build_text.replace(f"        {seed_line}", "")
    plants = [
        ("build.sh without the seed export", "build.sh", "without",
         unseeded, sweep_text),
        ("sweep.sh without the seed export", "sweep.sh", "without",
         build_text,
         re.sub(rf"^\s*{re.escape(LAUNCH_SEED)}\s*\n", "", sweep_text,
                flags=re.M)),
        ("build.sh exporting the seed after exec", "build.sh", "comes after",
         unseeded + f"\n{LAUNCH_SEED}\n", sweep_text),
    ]
    for why, culprit, expected, build_mut, sweep_mut in plants:
        if build_mut == build_text and sweep_mut == sweep_text:
            print(f"self-test: could not plant '{why}'", file=sys.stderr)
            return 2
        tmp_build, tmp_sweep = _temp_sh(build_mut), _temp_sh(sweep_mut)
        try:
            print(f"  [self-test] {why} - expecting REJECT:")
            bad_mut = check_launch_seed(tmp_build, tmp_sweep, quiet=True)
        finally:
            tmp_build.unlink()
            tmp_sweep.unlink()
        # The temp copies carry random names, so the culprit is matched by
        # its position: build.sh is reported first, sweep.sh second.
        want = 0 if culprit == "build.sh" else 1
        names = [tmp_build.name, tmp_sweep.name]
        if not any(drift.startswith(names[want]) and expected in drift
                   for drift in bad_mut):
            print(f"self-test FAILED: {why} did not report {culprit} "
                  f"{expected!r}", file=sys.stderr)
            return 2
        print(f"  [self-test] OK: {len(bad_mut)} drift(s) reported")
    return 0


def _run_self_test(sweep_path):
    """Every negative control, in order; the first failure's exit status."""
    status = _self_test_sweep_ns(sweep_path)
    if status:
        return status
    build_text = BUILD.read_text()
    status = _self_test_build_plants(build_text)
    if status:
        return status
    status = _self_test_regeneration(build_text)
    if status:
        return status
    status = _self_test_provenance_agrees(build_text)
    if status:
        return status
    status = _self_test_artefact_arms()
    if status:
        return status
    status = _self_test_build_cfg_scope(build_text)
    if status:
        return status
    status = _self_test_unbound_recipe(build_text)
    if status:
        return status
    return _self_test_launch_seed(build_text, sweep_path)


def main() -> int:
    """Pick the runtime or the static branch, and refuse a build that drifted.

    The runtime branch is the one sweep.sh calls seconds before Vivado, so
    its refusal message names the consequence - the bitstream would not be
    the shape the end-station config declares - rather than the flag.
    """
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--board")
    ap.add_argument("--config")
    ap.add_argument("--num-streams", type=int)
    ap.add_argument("--l2-bytes", type=int)
    # The EFFECTIVE option string, after sweep.sh has sourced the generated
    # fragment. Without it the runtime branch compared the render-LPF lever
    # against an empty string, concluded the filter was always PRESENT, and
    # refused every ax7101 build the moment the config declared it pruned -
    # while --self-test passed, because the self-test DID pass opts. A gate
    # that is green in its own test and wrong in production is the worst kind.
    ap.add_argument("--opts", default="",
                    help="effective milan_soc.py options (runtime mode)")
    ap.add_argument("--sweep", default=SWEEP, help="sweep.sh to parse (static mode)")
    ap.add_argument("--self-test", action="store_true",
                    help="also prove a deliberately mutated sweep.sh is REJECTED")
    a = ap.parse_args()

    runtime = [a.board, a.config, a.num_streams, a.l2_bytes]
    if any(x is not None for x in runtime):
        if any(x is None for x in runtime):
            ap.error("runtime mode needs --board --config --num-streams "
                     "--l2-bytes together")
        bad = compare(a.board, a.config, a.num_streams,
                      a.l2_bytes, "sweep.sh runtime", opts=a.opts)
        if bad:
            print("REFUSING TO BUILD: sweep.sh would produce a bitstream that "
                  "is not the shape the end-station config declares.",
                  file=sys.stderr)
            return 1
        return 0

    bad = run_static(a.sweep) + check_build_sh() + check_launch_seed(
        sweep_path=a.sweep)
    if bad:
        return 1
    print("sweep shape gate: OK")

    if a.self_test:
        return _run_self_test(a.sweep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
