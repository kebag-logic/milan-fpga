#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
check_sweep_shape.py - the sweep-vs-config shape gate.

WHY THIS EXISTS.  `sw/litex/sweep.sh` composes the milan_soc.py command line
that actually produces the flashed bitstream.  Every knob it gets wrong is
invisible until silicon:

  * 2026-07-24 (5ce9a13): sweep.sh passed `--rx-queues 1` for BOTH boards while
    the deployed arty gateware carried two RX queues.  A 2-queue build shifts
    every DMA window by 0x74 under an unchanged DTB.
  * 2026-07-26 (this gate): sweep.sh passed NO `--num-streams` AT ALL, so
    `sweep.sh ax7101` built the DEFAULT 1x1 datapath while the config, the docs
    and the build directories all called it 8x8.
  * 2026-08-20 (#116): the fabric gPTP plane became the product default, every
    Linux config gained an explicit `--no-fabric-gptp`, `sweep.sh` was updated
    and `build.sh` was not.  `build.sh cfg_ax8x8` and `cfg_arty` then died at
    `ap.error` BEFORE elaboration, and this gate did not see it: the build.sh
    branch compared four hand-picked keys while the sweep.sh branch had
    already been widened to flag-for-flag equality.  Both branches compare
    every design flag now.

Same shape all three times: a build knob that lives in the declarative
end-station config, is NOT carried by the script that builds, and silently
defaults.  This gate makes the divergence a HARD FAILURE instead.

Two modes:

  runtime  (what sweep.sh calls, just before it launches Vivado)
      check_sweep_shape.py --board ax7101 --config configs/endstation_ax7101_8x8.yaml \
                           --num-streams 8 --rx-queues 1 --l2-bytes 32768

  static   (CI / review: no shell, no Vivado - parse sweep.sh itself)
      check_sweep_shape.py                    # every board in sweep.sh's tables
      check_sweep_shape.py --self-test        # + prove a mismatch is rejected

Exit 0 = agree, 1 = drift (with the offending values printed), 2 = usage/setup.
Needs pyyaml (same dependency as sw/builder/test_builder.py).
"""

import argparse
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWEEP = os.path.join(ROOT, "sw/litex/sweep.sh")
BUILD = os.path.join(ROOT, "sw/litex/build.sh")

# build.sh's named recipes are the OTHER path to a flashed bitstream (the
# deployed ax8x8 gateware came from `build.sh ax8x8`), so they get the same
# treatment: cfg function -> the end-station config it claims to build.
BUILD_CFGS = {
    "ax7101": "configs/endstation_ax7101_1x1_tdm8.yaml",
    "ax8x8": "configs/endstation_ax7101_8x8.yaml",
    "arty":  "configs/endstation_arty_current.yaml",
}

# FLOW flags, not SHAPE flags: the tail a launcher appends after the shape
# flags. Vivado directives and per-run paths that emit_soc_argv deliberately
# does not emit (its own docstring says so, and the sweep multiplies the place
# directive by three). They are the launcher's business alone, so the
# flag-for-flag comparison below ignores them.
#
# THIS SET IS ALSO THE BLIND SPOT IT CREATES, so it has a second consumer.
# What a gate excludes from a comparison is exactly what separates a
# reconstructed argv from the line that really runs, and `sweep.sh:127-131`
# and `build.sh:303` both carry `--vivado-max-threads 32 --build`. A late
# `gptp_plane = args.fabric_gptp and not args.build` in milan_soc.py was
# therefore invisible to an argv built from emit_soc_argv alone (measured
# 2026-08-20). sw/builder/test_builder.py gate 1e now RUNS every member of
# this set, and asserts its own tail equals it, so adding a flag here without
# exercising it there fails.
#
# --entity-gen-dir is NOT in here: it names a config, and which config a
# recipe builds is exactly the fact this gate exists to pin (see
# _entity_gen_dir_agrees). --load is not either: no recipe or build-launcher
# line parsed by this script carries it. deploy.sh deliberately has a separate
# JTAG-load entry point, but a set that gate 1e must run has no
# business naming a flag that programs a board.
FLOW_FLAGS = {
    "--synth-directive", "--opt-directive", "--place-directive",
    "--vivado-max-threads", "--output-dir", "--build",
}

# PINNED DIVERGENCES - live disagreements that are DELIBERATE (or at least
# known and evidenced) and must not move silently. The gate fails if the pinned
# pair stops holding, which is the point: the exception is visible and dated
# instead of being an untracked gap.
#   (source, board/cfg, key): (source_value, config_value, reason)
PINNED = {
    # ---- build.sh <-> config, PRE-EXISTING at dev 10c7bf6c (measured
    #      2026-08-20 by running this widened gate against a dev worktree:
    #      the same ten pairs, flag for flag). The build.sh branch of this
    #      gate compared four keys until 2026-08-20; widening it to the
    #      flag-for-flag equality the sweep.sh branch already used surfaced
    #      these. NONE of them is resolved and none is claimed to be
    #      deliberate - they are pinned to their EXACT pair so the widening
    #      cannot be read as a blessing and so no side may move without this
    #      gate reporting it. Resolving them is issue #155; delete the entry
    #      as each closes.
    #
    #      THE --xlen AND --cpu-count PAIRS ARE NOT IN THAT CLASS and carry
    #      their own ticket, #157. Both recipes could not RUN at dev (no
    #      --entity-gen-dir, #156), so the CPU they select goes live with the
    #      #116 merge rather than having shipped for months. #116 made the
    #      recipes STATE the RV64 the absent flag already selected, which
    #      moves no elaborated SoC, and left the choice of winner to #157
    #      because it costs a CPU change on an arm that cannot be measured
    #      today.
    ("build.sh", "arty", "--xlen"): (
        "64", "32",
        "#157: recipe states the RV64 its absent --xlen already selected; "
        "endstation_arty_current.yaml and sweep.sh's arty leg both say 32"),
    ("build.sh", "arty", "--cpu-count"): (
        "2", "1",
        "#157: recipe builds two harts; the config and sweep.sh's arty leg "
        "both say one"),
    ("build.sh", "arty", "--cbs-queues-mask"): (
        "(absent)", "0x10",
        "#155: recipe leaves every queue with a CBS instance; the config "
        "derives the class-A-only mask"),
    ("build.sh", "arty", "--scala-args"): (
        "--l2-down-pending=8 --l2-general-slots=16 "
        "--lsu-hardware-prefetch=rpt --lsu-l1-refill-count=8",
        "--l2-down-pending=4 --l2-general-slots=8 --lsu-l1-refill-count=2",
        "#155: two different CPU cache profiles"),
    ("build.sh", "ax8x8", "--xlen"): (
        "64", "32",
        "#157: recipe states the RV64 its absent --xlen already selected; "
        "endstation_ax7101_8x8.yaml declares 32. This recipe agrees with its "
        "config on --cpu-count, which reads as an omission rather than a "
        "decision"),
    ("build.sh", "ax8x8", "--cbs-queues-mask"): (
        "0x18", "0x10",
        "#155: recipe shapes class A AND class B; the config derives class "
        "A alone (the 2026-07-31 area lever)"),
    ("build.sh", "ax8x8", "--eth-port"): (
        "(absent)", "e1",
        "#155: recipe relies on the argparse default, which is e1 today; "
        "the config states it"),
    ("build.sh", "ax8x8", "--no-datapath-probes"): (
        "(absent)", True,
        "#155: an AREA_BUDGET tier-1 prune the config declares and the "
        "recipe does not spend"),
    ("build.sh", "ax8x8", "--aaf-playback-streams"): (
        "(absent)", "1",
        "#155: recipe relies on the argparse default, which is 1 today; the "
        "config states it"),
    ("build.sh", "ax8x8", "--scala-args"): (
        "--lsu-hardware-prefetch=rpt --lsu-l1-refill-count=8",
        "--l2-down-pending=4 --l2-general-slots=8 --lsu-l1-refill-count=2",
        "#155: two different CPU cache profiles"),
    # (empty) - the ax8x8 l2_bytes divergence was RESOLVED 2026-07-26 by
    # correcting configs/endstation_ax7101_8x8.yaml from 32768 to 16384.
    # The USER 32K authorisation belongs to the 1x1 bench shape
    # (build.sh cfg_ax7101, --rx-queues 2); cfg_ax8x8 is --l2-bytes 16384
    # and its own comment records the measured close: WNS +0.080,
    # LUT 85.15%, TNS 0, all seeds. The deployed 8x8 bitstream was built
    # at 16384. Keep this dict as the place to record a DELIBERATE, dated
    # divergence rather than letting one go untracked.
}


def _yaml():
    try:
        import yaml
    except ImportError:
        sys.exit("check_sweep_shape: pyyaml required (pip install pyyaml)")
    return yaml


def config_shape(path):
    """(board, num_streams, rx_queues, l2_bytes, render_lpf) implied by a config.

    num_streams == milan_datapath N_STREAMS == the WIDER of the two stream
    directions, exactly as sw/builder/endstation_builder.emit_soc_argv computes
    it - kept as one line here on purpose so the two can be eyeballed together.
    """
    yaml = _yaml()
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    if not os.path.exists(path):
        sys.exit(f"check_sweep_shape: no such config {path}")
    cfg = yaml.safe_load(open(path))
    s = cfg.get("streams") or {}
    n_streams = max(len(s.get("listeners") or []), len(s.get("talkers") or []))
    c = (cfg.get("board") or {}).get("constraints") or {}
    # render_lpf is the milan_datapath LPF_P area lever
    # (docs/design/AREA_BUDGET.md). Absent = filter PRESENT, which is
    # what every config said before 2026-07-27, so the default keeps old
    # configs byte-identical. It is gated here for the same reason
    # --eth-port and --rx-queues are: it changes the BITSTREAM, one board at
    # a time, and a silent divergence between build.sh and sweep.sh is how
    # this project has lost builds twice.
    return (cfg["board"]["target"], n_streams,
            int(c["rx_queues"]), int(c["l2_bytes"]),
            bool(c.get("render_lpf", True)))


def parse_sweep(path=SWEEP):
    """sweep.sh's per-board default tables -> {board: {opts,l2,rxq,ns,cfg}}.

    Deliberately the SAME parse shape test_builder.sweep_inline() uses for
    OPTS/L2/RXQ, extended with the NS/CFG line - if either table is reformatted
    so this regex misses, the gate fails loudly rather than passing vacuously.
    """
    txt = open(path).read()
    boards = {}
    for m in re.finditer(r'^\s*(\w+)\)\s+OPTS="([^"]+)"; L2=(\d+); RXQ=(\d+)',
                         txt, re.M):
        boards[m.group(1)] = dict(opts=m.group(2), l2=int(m.group(3)),
                                  rxq=int(m.group(4)))
    if not boards:
        sys.exit(f"check_sweep_shape: no OPTS/L2/RXQ table found in {path}")
    for m in re.finditer(r'^\s*(\w+)\)\s+NS=(\d+); CFG=\$\{SWEEP_CFG:-([^}]+)\}',
                         txt, re.M):
        if m.group(1) in boards:
            boards[m.group(1)]["ns"] = int(m.group(2))
            boards[m.group(1)]["cfg"] = m.group(3)
    missing = [b for b, v in boards.items() if "ns" not in v]
    if missing:
        sys.exit("check_sweep_shape: sweep.sh has no NS/CFG line for "
                 + ", ".join(sorted(missing)))
    return boards


def design_opts_expected(cfg_path):
    """The complete SoC flag list this config implies, from the builder's
    own emission (sw/builder/endstation_builder.emit_soc_argv).

    Imported, not re-derived: interface_is_placeholder / framer_wire_channels
    / the tier-1 prune resolution are real logic, and a second copy here is
    exactly the kind that drifts. The import is in-repo and costs pyyaml,
    which this script already requires."""
    sys.path.insert(0, os.path.join(ROOT, "sw/builder"))
    import endstation_builder as eb
    p = cfg_path if os.path.isabs(cfg_path) else os.path.join(ROOT, cfg_path)
    return eb.emit_soc_argv(eb.load_config(p))


def parse_flags(tokens):
    """['--a', '1', '--b'] -> {'--a': '1', '--b': True}. Values never start
    with '--', so a missing value cannot swallow the next flag."""
    d = {}
    for i, t in enumerate(tokens):
        if t.startswith("--"):
            nxt = tokens[i + 1] if i + 1 < len(tokens) else None
            d[t] = nxt if (nxt and not nxt.startswith("--")) else True
    return d


def compare(board, cfg_path, ns, rxq, l2, where, opts=""):
    """One board's effective shape vs its config. Returns a list of problems."""
    c_board, c_ns, c_rxq, c_l2, c_lpf = config_shape(cfg_path)
    bad = []
    if c_board != board:
        bad.append(f"config board {c_board!r} != sweep board {board!r}")
    if c_ns != ns:
        bad.append(f"--num-streams {ns} != config streams {c_ns} "
                   f"(max(listeners, talkers)) - the bitstream would be "
                   f"{ns}x{ns}, the config says {c_ns}x{c_ns}")
    if c_rxq != rxq:
        bad.append(f"--rx-queues {rxq} != config rx_queues {c_rxq} "
                   "(CSR-rot rule: shifts every DMA window under the DTB)")
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
                    f"{os.path.basename(cfg_path)})")
    if bad:
        print(f"SHAPE DRIFT [{where}] {board} vs {cfg_path}:", file=sys.stderr)
        for b in bad:
            print(f"  - {b}", file=sys.stderr)
    else:
        print(f"  [sweep-shape] {board}: num-streams {ns}, rx-queues {rxq}, "
              f"l2 {l2}, render-lpf {lpf} == {os.path.basename(cfg_path)}")
    return bad


def check_fragment(board):
    """The generated fragment may pin NS too (it is sourced AFTER the defaults).
    When it does, it is authoritative and must agree; when it does not, say so -
    silence is what let the 8x8 build ship as 1x1."""
    p = os.path.join(ROOT, "configs/generated", f"sweep_opts_{board}.sh")
    if not os.path.exists(p):
        return None
    txt = open(p).read()
    m = re.search(r"^NS=(\d+)\s*$", txt, re.M)
    if m:
        return int(m.group(1))
    m = re.search(r"--num-streams[= ]+(\d+)", txt)
    return int(m.group(1)) if m else None


def parse_build_sh(path=BUILD):
    """build.sh's `cfg_<name>() { ... echo "<flags>" ... }` recipes -> flag dicts."""
    txt = open(path).read()
    out = {}
    for m in re.finditer(r'^cfg_(\w+)\(\)\s*\{(.*?)^\}', txt, re.M | re.S):
        body = m.group(2)
        e = re.search(r'echo\s+"(.*?)"', body, re.S)
        if not e:
            continue
        flags = e.group(1).replace("\\\n", " ").split()
        d = {}
        for i, t in enumerate(flags):
            if t.startswith("--"):
                nxt = flags[i + 1] if i + 1 < len(flags) else None
                d[t] = nxt if (nxt and not nxt.startswith("--")) else True
        out[m.group(1)] = d
    if not out:
        sys.exit(f"check_sweep_shape: no cfg_* recipes found in {path}")
    return out


def design_flags(flags):
    """A parsed flag dict with the FLOW flags dropped and --scala-args joined.

    The scala arguments arrive as `--scala-args=<one>` tokens, so a plain
    parse spells each of them as its own flag and one differing cache knob
    reads as four unrelated divergences. Joined into a single sorted string
    they read as what they are: one CPU cache profile, compared whole.
    """
    d, scala = {}, []
    for k, v in flags.items():
        if k in FLOW_FLAGS:
            continue
        if k.startswith("--scala-args="):
            scala.append(k[len("--scala-args="):])
            continue
        d[k] = v
    if scala:
        d["--scala-args"] = " ".join(sorted(scala))
    return d


def _entity_gen_dir_agrees(name, cfg_path, flags):
    """build.sh must hand milan_soc.py the generated dir of the SAME config
    this gate compares the recipe against.

    Not decoration: --entity-gen-dir supplies the descriptor image, the
    platform shape (the reserved `ppmem` window compiled into the gateware)
    and, on a fabric build, the gPTP microcode ROM. A recipe that omits it
    cannot launch at all - measured 2026-08-20, `build.sh ax8x8` and
    `build.sh arty` both died at `this build needs its end-station config`
    before elaboration - and a recipe that names ANOTHER config builds one
    shape's gateware around another shape's descriptors. The literal is a
    path, so it cannot be derived from BUILD_CFGS in shell; it is pinned here
    instead.
    """
    want = os.path.splitext(os.path.basename(cfg_path))[0]
    got = flags.get("--entity-gen-dir")
    msg = None
    if got is True or not got:
        msg = (f"cfg_{name}: no --entity-gen-dir. milan_soc.py refuses to "
               f"launch without it, so this recipe cannot be run at all; it "
               f"must name configs/generated/{want}")
    elif os.path.basename(str(got).rstrip("/")) != want:
        msg = (f"cfg_{name}: --entity-gen-dir names "
               f"{os.path.basename(str(got).rstrip('/'))!r} but this recipe "
               f"is graded against {os.path.basename(cfg_path)} - the "
               f"gateware and the descriptors would be different shapes")
    if msg is None:
        return []
    print("SHAPE DRIFT: " + msg, file=sys.stderr)
    return [msg]


def check_build_sh(path=BUILD):
    """build.sh recipe vs the end-station config it builds, FLAG FOR FLAG.

    Until 2026-08-20 this branch compared exactly four keys - num_streams,
    rx_queues, l2_bytes, render_lpf - while the sweep.sh branch above had
    already been widened to full equality against emit_soc_argv. That is the
    same "hand-picked SUBSET of the design flags" failure this file's header
    comment was written to end, and it let a real one through: #116 made
    `--fabric-gptp` the default, every Linux config gained an explicit
    `--no-fabric-gptp`, and cfg_ax8x8 / cfg_arty said nothing, so both aborted
    with `ap.error` before elaboration and no gate noticed.

    Divergences listed in PINNED are accepted AND RE-VERIFIED against their
    recorded pair; anything else is drift.
    """
    recipes = parse_build_sh(path)
    bad = []
    for name, cfg_path in sorted(BUILD_CFGS.items()):
        if name not in recipes:
            bad.append(f"build.sh has no cfg_{name}")
            continue
        f = recipes[name]
        local = _entity_gen_dir_agrees(name, cfg_path, f)
        got = design_flags(f)
        want = design_flags(parse_flags(design_opts_expected(cfg_path)))
        got.pop("--entity-gen-dir", None)      # checked above, by basename
        n_ok = n_pin = 0
        for k in sorted(set(got) | set(want)):
            pin = PINNED.get(("build.sh", name, k))
            g, w = got.get(k, "(absent)"), want.get(k, "(absent)")
            if pin is not None:
                n_pin += 1
                if (g, w) != tuple(pin[:2]):
                    msg = (f"cfg_{name}: PINNED divergence on {k} no longer "
                           f"holds (build.sh {g!r} / config {w!r}, pinned "
                           f"{pin[0]!r} / {pin[1]!r}) - revisit the pin")
                    print("SHAPE DRIFT: " + msg, file=sys.stderr)
                    local.append(msg)
                else:
                    print(f"  [sweep-shape] build.sh cfg_{name}: {k} "
                          f"{g!r} != config {w!r} - PINNED, known")
            elif g != w:
                msg = (f"cfg_{name}: design flag {k}: build.sh {g!r} != "
                       f"config-implied {w!r} (emit_soc_argv of "
                       f"{os.path.basename(cfg_path)})")
                print("SHAPE DRIFT: " + msg, file=sys.stderr)
                local.append(msg)
            else:
                n_ok += 1
        if not local:
            print(f"  [sweep-shape] build.sh cfg_{name}: {n_ok} design flags "
                  f"agree with {os.path.basename(cfg_path)} flag for flag "
                  f"({n_pin} PINNED), and --entity-gen-dir names it")
        bad += local
    return bad


def run_static(sweep_path=SWEEP, quiet=False):
    boards = parse_sweep(sweep_path)
    bad = []
    for board, v in sorted(boards.items()):
        bad += compare(board, v["cfg"], v["ns"], v["rxq"], v["l2"],
                       os.path.basename(sweep_path), opts=v["opts"])
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--board")
    ap.add_argument("--config")
    ap.add_argument("--num-streams", type=int)
    ap.add_argument("--rx-queues", type=int)
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

    runtime = [a.board, a.config, a.num_streams, a.rx_queues, a.l2_bytes]
    if any(x is not None for x in runtime):
        if any(x is None for x in runtime):
            ap.error("runtime mode needs --board --config --num-streams "
                     "--rx-queues --l2-bytes together")
        bad = compare(a.board, a.config, a.num_streams, a.rx_queues,
                      a.l2_bytes, "sweep.sh runtime", opts=a.opts)
        if bad:
            print("REFUSING TO BUILD: sweep.sh would produce a bitstream that "
                  "is not the shape the end-station config declares.",
                  file=sys.stderr)
            return 1
        return 0

    bad = run_static(a.sweep) + check_build_sh()
    if bad:
        return 1
    print("sweep shape gate: OK")

    if a.self_test:
        # Negative control: bump every board's NS by one in a COPY of sweep.sh
        # and require the gate to reject it. Without this the gate could be
        # vacuously green (e.g. a regex that stopped matching).
        txt = open(a.sweep).read()
        mut = re.sub(r'^(\s*\w+\)\s+NS=)(\d+)',
                     lambda m: m.group(1) + str(int(m.group(2)) + 1),
                     txt, flags=re.M)
        if mut == txt:
            print("self-test: could not mutate NS in sweep.sh", file=sys.stderr)
            return 2
        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
            f.write(mut)
            tmp = f.name
        try:
            print("  [self-test] mutated NS (+1 per board) - expecting REJECT:")
            bad_mut = run_static(tmp, quiet=True)
        finally:
            os.unlink(tmp)
        if not bad_mut:
            print("self-test FAILED: a wrong NS was accepted", file=sys.stderr)
            return 2
        print(f"  [self-test] OK: {len(bad_mut)} drift(s) reported for the "
              "mutated sweep.sh")

        # Negative control for the OTHER branch, and for the exact escape
        # that widened it: build.sh had no gptp flag at all while every
        # Linux config emits `--no-fabric-gptp`, and the four-key comparison
        # could not see a flag it did not name. Each mutation deletes ONE
        # token from a COPY of build.sh and the gate must report it.
        build_mutations = [
            ("--loopback-lane deleted from cfg_ax7101",
             "--loopback-lane --fabric-gptp", "--fabric-gptp"),
            ("--no-fabric-gptp deleted from cfg_ax8x8 (the #116 escape)",
             "--aaf-playback --no-fabric-gptp", "--aaf-playback"),
            ("--entity-gen-dir deleted from cfg_arty (recipe cannot launch)",
             "--entity-gen-dir "
             "$SOC_DIR/../../configs/generated/endstation_arty_current", ""),
            ("cfg_ax8x8's --entity-gen-dir repointed at another config",
             "configs/generated/endstation_ax7101_8x8",
             "configs/generated/endstation_ax7101_1x1_tdm8"),
        ]
        btxt = open(BUILD).read()
        for why, old, new in build_mutations:
            if btxt.count(old) != 1:
                print(f"self-test: {old!r} matched {btxt.count(old)} times "
                      "in build.sh, want 1", file=sys.stderr)
                return 2
            with tempfile.NamedTemporaryFile("w", suffix=".sh",
                                             delete=False) as f:
                f.write(btxt.replace(old, new))
                tmp = f.name
            try:
                print(f"  [self-test] {why} - expecting REJECT:")
                bad_mut = check_build_sh(tmp)
            finally:
                os.unlink(tmp)
            if not bad_mut:
                print(f"self-test FAILED: {why} was accepted", file=sys.stderr)
                return 2
            print(f"  [self-test] OK: {len(bad_mut)} drift(s) reported")
    return 0


if __name__ == "__main__":
    sys.exit(main())
