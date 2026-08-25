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
  * 2026-08-22 (#157): build.sh's Linux recipes passed NO `--xlen` AT ALL,
    and milan_soc.py defaults it to 64 where the builder defaults it to 32,
    so `build.sh cfg_ax8x8` and `cfg_arty` elaborated an RV64 core under
    configs, a sweep table and a boot chain that are all RV32 single-hart.

Same shape both times: a build knob that lives in the declarative end-station
config, is NOT carried by the script that builds, and silently defaults.  This
gate makes the divergence a HARD FAILURE instead.

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

# build.sh's named recipes are the OTHER path to a flashed bitstream, so they
# get the same treatment: cfg function -> the end-station config it claims to
# build. The deployed 8x8 image came from the x32f1_eto sweep; cfg_ax8x8 has
# never produced a bitstream. This gate keeps that alternate recipe aligned
# with the same graded config before anybody uses it.
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

# PINNED DIVERGENCES - live disagreements that are DELIBERATE (or at least
# known and evidenced) and must not move silently. The gate fails if the pinned
# pair stops holding, which is the point: the exception is visible and dated
# instead of being an untracked gap.
#   (source, board/cfg, key): (source_value, config_value, reason)
PINNED = {
    # The ax8x8 l2_bytes divergence was RESOLVED 2026-07-26 by
    # correcting configs/endstation_ax7101_8x8.yaml from 32768 to 16384.
    # The USER 32K authorisation belongs to the 1x1 bench shape
    # (build.sh cfg_ax7101, --rx-queues 2); cfg_ax8x8 is --l2-bytes 16384
    # and its own comment records the measured close: WNS +0.080,
    # LUT 85.15%, TNS 0, all seeds. The deployed 8x8 bitstream was built
    # at 16384. Keep this dict as the place to record a DELIBERATE, dated
    # divergence rather than letting one go untracked.
}

# CPU WIDTH AND HART COUNT (2026-08-22, #157). The two entry points default
# this one decision opposite ways: milan_soc.py --xlen defaults to 64, and
# only its baremetal profile refuses anything else, while the builder's
# SOC_DEFAULTS says 32 and one hart. A build.sh recipe that omitted --xlen
# therefore elaborated an RV64 core under an RV32 config and an RV32 boot
# chain, and the symptom of that is a board that prints a BIOS banner and
# hangs at Liftoff with nothing naming the cause (8b5d0255, 2026-08-05). So
# for these two flags an ABSENT flag is drift, not a default: the recipe must
# state the value and it must equal what emit_soc_argv derives for the
# config. The full flag-for-flag comparison below now subsumes these two flags;
# this named set drives their dedicated absent-and-swapped negative controls.
CPU_FLAGS = {"--xlen": "xlen", "--cpu-count": "cpu_count"}


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
    """Require a recipe to use the generated artifacts for its graded config."""
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
               f"gateware and generated artifacts would be different shapes")
    if msg is None:
        return []
    print("SHAPE DRIFT: " + msg, file=sys.stderr)
    return [msg]


def check_build_sh(path=BUILD, quiet=False):
    """Compare every build.sh design flag with emit_soc_argv, flag for flag.

    Divergences listed in PINNED are accepted and re-verified against their
    exact pair. Everything else is drift. This deliberately replaces the old
    four-key subset, which could not see the #155 cache, CBS, port, playback,
    or optional-block disagreements.
    `quiet` suppresses successful agreement summaries while negative controls
    exercise mutated copies.
    """
    recipes = parse_build_sh(path)
    bad = []
    unbound = sorted(set(recipes) - set(BUILD_CFGS))
    for name in unbound:
        msg = (f"build.sh cfg_{name} has no config binding in BUILD_CFGS; "
               "an ungraded recipe could silently build a different shape")
        print("SHAPE DRIFT: " + msg, file=sys.stderr)
        bad.append(msg)

    visited_pins = set()
    for name, cfg_path in sorted(BUILD_CFGS.items()):
        if name not in recipes:
            msg = f"build.sh has no cfg_{name}"
            print("SHAPE DRIFT: " + msg, file=sys.stderr)
            bad.append(msg)
            continue
        f = recipes[name]
        local = _entity_gen_dir_agrees(name, cfg_path, f)
        got = design_flags(f)
        want = design_flags(parse_flags(design_opts_expected(cfg_path)))
        got.pop("--entity-gen-dir", None)  # checked above, by config basename
        n_ok = n_pin = 0
        for k in sorted(set(got) | set(want)):
            pin_key = ("build.sh", name, k)
            pin = PINNED.get(pin_key)
            g = got.get(k, "(absent)")
            w = want.get(k, "(absent)")
            if pin is not None:
                visited_pins.add(pin_key)
                n_pin += 1
                if (g, w) != tuple(pin[:2]):
                    msg = (f"cfg_{name}: PINNED divergence on {k} no longer "
                           f"holds (build.sh {g!r} / config {w!r}, pinned "
                           f"{pin[0]!r} / {pin[1]!r}) - revisit the pin")
                    print("SHAPE DRIFT: " + msg, file=sys.stderr)
                    local.append(msg)
                elif not quiet:
                    print(f"  [sweep-shape] build.sh cfg_{name}: {k} "
                          f"{g!r} != config {w!r} - PINNED, known: {pin[2]}")
            elif g != w:
                msg = (f"cfg_{name}: design flag {k}: build.sh {g!r} != "
                       f"config-implied {w!r} (emit_soc_argv of "
                       f"{os.path.basename(cfg_path)})")
                print("SHAPE DRIFT: " + msg, file=sys.stderr)
                local.append(msg)
            else:
                n_ok += 1
        if not local and not quiet:
            print(f"  [sweep-shape] build.sh cfg_{name}: {n_ok} design flags "
                  f"agree with {os.path.basename(cfg_path)} flag for flag "
                  f"({n_pin} PINNED), and --entity-gen-dir names it")
        bad += local

    for pin_key in sorted(set(PINNED) - visited_pins):
        msg = (f"PINNED divergence {pin_key!r} was never visited; remove the "
               "stale exception or restore the recipe/config binding")
        print("SHAPE DRIFT: " + msg, file=sys.stderr)
        bad.append(msg)
    return bad


def self_test_build_sh(path=BUILD):
    """Negative controls for the build.sh CPU keys (#157).

    Two mutated copies of build.sh: the REAL defect replayed - every
    `--xlen N` and `--cpu-count N` stripped, so each recipe would inherit
    milan_soc.py's defaults - and its value-swapped cousin (xlen flipped
    between 32 and 64, one more hart). Each must be rejected on BOTH CPU flags
    of all three recipes, or a check is vacuous. Returns the
    (mutation, cfg, flag) triples the gate FAILED to reject; empty means every
    flag bit."""
    txt = open(path).read()
    mutations = {
        "absent": re.sub(r"--(?:xlen|cpu-count) \d+ ?", "", txt),
        "swapped": re.sub(
            r"--cpu-count (\d+)",
            lambda m: f"--cpu-count {int(m.group(1)) + 1}",
            re.sub(r"--xlen (\d+)",
                   lambda m: f"--xlen {32 if m.group(1) == '64' else 64}",
                   txt)),
    }
    missed = []
    for label, mut in mutations.items():
        if mut == txt:
            sys.exit("self-test: could not mutate the CPU flags in build.sh "
                     f"({label})")
        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
            f.write(mut)
            tmp = f.name
        try:
            print(f"  [self-test] build.sh --xlen/--cpu-count {label} - "
                  "expecting REJECT on both keys of every recipe:")
            bad = check_build_sh(tmp, quiet=True)
        finally:
            os.unlink(tmp)
        for name in BUILD_CFGS:
            for flag in CPU_FLAGS:
                drift = f"cfg_{name}: design flag {flag}:"
                pinned = f"cfg_{name}: PINNED divergence on {flag} "
                if not any(b.startswith(drift) or b.startswith(pinned)
                           for b in bad):
                    missed.append((label, name, flag))
    return missed


def mutate_build_recipe(text, name, old, new):
    """Change one flag fragment inside one named recipe for a negative test."""
    match = re.search(rf"^cfg_{re.escape(name)}\(\)\s*\{{.*?^\}}",
                      text, re.M | re.S)
    if not match:
        raise ValueError(f"cfg_{name} recipe not found")
    recipe = match.group(0)
    count = recipe.count(old)
    if count != 1:
        raise ValueError(
            f"{old!r} matched {count} times in cfg_{name}, want 1")
    mutated = recipe.replace(old, new)
    return text[:match.start()] + mutated + text[match.end():]


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
        missed = self_test_build_sh()
        if missed:
            print("self-test FAILED: build.sh CPU-flag mutations accepted on "
                  + ", ".join(f"{m}/cfg_{n}/{k}" for m, n, k in missed),
                  file=sys.stderr)
            return 2
        print("  [self-test] OK: --xlen and --cpu-count rejected on "
              f"{len(BUILD_CFGS)} build.sh recipes, absent and swapped")

        # Negative controls for the named-build branch. These span the seven
        # #155 repairs and the config-artifact binding. CPU absence/value
        # mutations are covered above. Each edit starts from the pristine
        # recipe so one mismatch cannot mask another.
        build_mutations = [
            ("cfg_ax8x8 loses its explicit Ethernet port",
             "ax8x8", "--eth-port e1", "", "design flag --eth-port:"),
            # #259 retired the playback rings and the cache scala words,
            # so the dropped-flag and added-word plants below ride tokens
            # the bare-metal recipes still carry.
            ("cfg_ax8x8 loses its wire-channel count",
             "ax8x8", "--talker-wire-chans 8", "",
             "design flag --talker-wire-chans:"),
            ("cfg_ax8x8 stops spending the datapath-probe prune",
             "ax8x8", "--no-datapath-probes", "",
             "design flag --no-datapath-probes:"),
            ("cfg_ax8x8 restores the class-B CBS instance",
             "ax8x8", "--cbs-queues-mask 0x10",
             "--cbs-queues-mask 0x18", "design flag --cbs-queues-mask:"),
            ("cfg_ax8x8 adds an RV64-era prefetch Scala word",
             "ax8x8", "--l2-bytes 0",
             "--l2-bytes 0 --scala-args=--lsu-hardware-prefetch=rpt",
             "design flag --scala-args:"),
            ("cfg_arty loses its class-A CBS mask",
             "arty", "--cbs-queues-mask 0x10", "",
             "design flag --cbs-queues-mask:"),
            ("cfg_arty restores an RV64-era Scala slot count",
             "arty", "--l2-bytes 0",
             "--l2-bytes 0 --scala-args=--l2-general-slots=16",
             "design flag --scala-args:"),
            ("cfg_arty loses its generated entity directory",
             "arty", "--entity-gen-dir "
             "$SOC_DIR/../../configs/generated/endstation_arty_current", "",
             "no --entity-gen-dir"),
            ("cfg_ax8x8 points at another config's generated artifacts",
             "ax8x8", "configs/generated/endstation_ax7101_8x8",
             "configs/generated/endstation_ax7101_1x1_tdm8",
             "--entity-gen-dir names"),
        ]
        btxt = open(BUILD).read()
        for why, name, old, new, expected in build_mutations:
            try:
                mutated = mutate_build_recipe(btxt, name, old, new)
            except ValueError as exc:
                print(f"self-test: {exc}", file=sys.stderr)
                return 2
            with tempfile.NamedTemporaryFile("w", suffix=".sh",
                                             delete=False) as f:
                f.write(mutated)
                tmp = f.name
            try:
                print(f"  [self-test] {why} - expecting REJECT:")
                bad_mut = check_build_sh(tmp, quiet=True)
            finally:
                os.unlink(tmp)
            if not any(expected in drift for drift in bad_mut):
                print(f"self-test FAILED: {why} did not report {expected!r}",
                      file=sys.stderr)
                return 2
            print(f"  [self-test] OK: {len(bad_mut)} drift(s) reported")

        # A newly added cfg_* function must not escape grading merely because
        # BUILD_CFGS was not extended with its declarative config.
        unbound_recipe = (
            "cfg_unbound_selftest() {\n"
            "    echo \"--board arty --cpu vexiiriscv --cpu-count 1 "
            "--xlen 32\"\n"
            "}\n\n")
        mutated, count = re.subn(r"^(SWEEP_DIRECTIVES=)",
                                  unbound_recipe + r"\1", btxt,
                                  count=1, flags=re.M)
        if count != 1:
            print("self-test: SWEEP_DIRECTIVES anchor not found in build.sh",
                  file=sys.stderr)
            return 2
        with tempfile.NamedTemporaryFile("w", suffix=".sh",
                                         delete=False) as f:
            f.write(mutated)
            tmp = f.name
        try:
            print("  [self-test] unbound cfg_* recipe - expecting REJECT:")
            bad_mut = check_build_sh(tmp, quiet=True)
        finally:
            os.unlink(tmp)
        if not any("cfg_unbound_selftest has no config binding" in drift
                   for drift in bad_mut):
            print("self-test FAILED: unbound cfg_* recipe was accepted",
                  file=sys.stderr)
            return 2
        print("  [self-test] OK: unbound cfg_* recipe rejected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
