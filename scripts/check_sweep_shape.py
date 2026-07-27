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

# build.sh's named recipes are the OTHER path to a flashed bitstream (the
# deployed ax8x8 gateware came from `build.sh ax8x8`), so they get the same
# treatment: cfg function -> the end-station config it claims to build.
# cfg_ax7101 has no counterpart (there is no 1x1 ax7101 config) and is skipped.
BUILD_CFGS = {
    "ax8x8": "configs/endstation_ax7101_8x8.yaml",
    "arty":  "configs/endstation_arty_current.yaml",
}

# PINNED DIVERGENCES - live disagreements that are DELIBERATE (or at least
# known and evidenced) and must not move silently. The gate fails if the pinned
# pair stops holding, which is the point: the exception is visible and dated
# instead of being an untracked gap.
#   (source, board/cfg, key): (source_value, config_value, reason)
PINNED = {
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
    # (docs/NXN_ARCHITECTURE.md 6.2/6.3). Absent = filter PRESENT, which is
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


def check_build_sh(path=BUILD):
    """build.sh recipe vs the end-station config it builds. Divergences listed
    in PINNED are accepted (and re-verified); anything else is drift."""
    recipes = parse_build_sh(path)
    bad = []
    for name, cfg_path in sorted(BUILD_CFGS.items()):
        if name not in recipes:
            bad.append(f"build.sh has no cfg_{name}")
            continue
        f = recipes[name]
        _b, c_ns, c_rxq, c_l2, c_lpf = config_shape(cfg_path)
        got = {"num_streams": int(f.get("--num-streams", 1)),
               "rx_queues":   int(f["--rx-queues"]),
               "l2_bytes":    int(f["--l2-bytes"]),
               "render_lpf":  "--no-render-lpf" not in f}
        want = {"num_streams": c_ns, "rx_queues": c_rxq, "l2_bytes": c_l2,
                "render_lpf": c_lpf}
        for k in sorted(got):
            pin = PINNED.get(("build.sh", name, k))
            if pin is not None:
                if (got[k], want[k]) != pin[:2]:
                    msg = (f"cfg_{name}: PINNED divergence on {k} no longer "
                           f"holds (build.sh {got[k]} / config {want[k]}, "
                           f"pinned {pin[0]} / {pin[1]}) - revisit the pin")
                    print("SHAPE DRIFT: " + msg, file=sys.stderr)
                    bad.append(msg)
                else:
                    print(f"  [sweep-shape] build.sh cfg_{name}: {k} "
                          f"{got[k]} != config {want[k]} - PINNED, known")
            elif got[k] != want[k]:
                msg = (f"cfg_{name}: {k} {got[k]} != "
                       f"{os.path.basename(cfg_path)} {want[k]}")
                print("SHAPE DRIFT: " + msg, file=sys.stderr)
                bad.append(msg)
            else:
                print(f"  [sweep-shape] build.sh cfg_{name}: {k} {got[k]} "
                      f"== {os.path.basename(cfg_path)}")
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
                      a.l2_bytes, "sweep.sh runtime")
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
