#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
check_entity_shape.py - the advertised-shape gate.

WHY THIS EXISTS.  An end station tells every controller on the segment how many
streams it has in exactly three places, and all three have to be the same
number:

  1. the ADPDU it broadcasts - talker_stream_sources / listener_stream_sinks,
     served by milan_csr at 0x618 / 0x61C;
  2. its AEM descriptor set - the STREAM_OUTPUT / STREAM_INPUT descriptors a
     controller can actually READ_DESCRIPTOR and bind;
  3. the gateware that was built - the ACMP source/sink contexts that answer
     CONNECT_TX / BIND_RX, sized by N_STREAMS at elaboration.

On 2026-07-27 they were three different numbers.  0x618 and 0x61C were plain
RW registers resetting to ZERO, so the advertised counts came from two
hand-typed lines in a boot script:

    w 0x618 0x48010001   # 1 implemented stream (honest count, Milan strict)
    w 0x61C 0x48010002   # 2 STREAM_INPUTs (media + CRF desc)

That comment was true at 1x1 and became false the day the board went 8x8.  The
flashed AX7101 - built N_STREAMS = 8 - advertised 1 talker source and 2
listener sinks next to a reference device advertising 4/10 and a peer host
advertising 8/8, so every controller on the segment could see and bind ONE of
its eight streams.  The register faithfully held what was written, so nothing
looked broken anywhere.

The CRF Media Clock Output is the sharpest case: it is a bindable ACMP talker
source at talker_unique_id = N_STREAMS, its PDUs were on the wire every 2 ms,
and it was invisible to ATDECC because uid 8 sat outside an advertised range
of 1.  (That is NOT the same gap as M-CLK-2, which is about the CRF stream not
holding an SRP class-A reservation.  This gate is only about discoverability.)

WHAT IT CHECKS, per end-station config:

  A  RTL shape        milan_datapath's own ACMP_SRC_C / ACMP_SINKS_C
                      localparam expressions, evaluated at this config's
                      N_STREAMS (the expressions are PARSED out of the RTL, so
                      the gate cannot drift away from the design)
  B  wiring           milan_datapath passes them to milan_csr's
                      N_TALKER_SRC_P / N_LISTENER_SINK_P
  C  read-only        milan_csr builds 0x618/0x61C from those parameters, has
                      a defaults arm for both, and has NO write arm and NO
                      is_plain_rw entry for either
  D  AEM model        the AEM overlay this config produces declares exactly
                      the same STREAM_OUTPUT / STREAM_INPUT counts, and its
                      entity_counts agree with its descriptor_counts
  E  tracked ROM      the tracked hdl/ieee17221/aecp/gen/aecp_aem_rom.svh
                      matches the config that OWNS the tracked RTL tables
                      (srp.rtl_table), descriptor for descriptor

Usage:
    check_entity_shape.py                 # every configs/endstation_*.yaml
    check_entity_shape.py --self-test     # + prove disagreeing shapes FAIL

Exit 0 = agree, 1 = drift (offending values printed), 2 = usage/setup.
Needs pyyaml (same dependency as sw/builder/test_builder.py).
"""

import argparse
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATAPATH = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
CSR = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")
AEM_ROM = os.path.join(ROOT, "hdl/ieee17221/aecp/gen/aecp_aem_rom.svh")
CONFIG_DIR = os.path.join(ROOT, "configs")

# IEEE 1722.1-2021 Table 7.1 descriptor types
STREAM_INPUT, STREAM_OUTPUT = 0x0005, 0x0006

fails = []
checks = 0
quiet = False          #! set while a self-test mutation is being run


def ck(what, got, exp):
    global checks
    checks += 1
    if got != exp:
        fails.append(f"{what}: got {got!r}, expected {exp!r}")
        if not quiet:
            print(f"  [FAIL] {what}: got {got!r}, expected {exp!r}")
    elif not quiet:
        print(f"  [ok]   {what} = {got!r}")


# ------------------------------------------------------- RTL shape parsing --
def sv_localparam_expr(text, name):
    """Pull `localparam int <name> = <expr>;` out of SystemVerilog source."""
    m = re.search(r"localparam\s+int\s+" + re.escape(name) + r"\s*=\s*([^;]+);",
                  text)
    if not m:
        raise SystemExit(f"SETUP: no `localparam int {name}` in the RTL")
    return " ".join(m.group(1).split())


def eval_sv_ternary(expr, n_streams):
    """Evaluate a simple SV integer expression in N_STREAMS.

    Only the vocabulary these two localparams actually use is accepted -
    N_STREAMS, integer literals, ?:, comparisons and + - * ( ). Anything else
    is a hard error rather than a guess, because a silently mis-evaluated
    shape is the whole class of defect this gate exists to catch."""
    if not re.fullmatch(r"[N_STREAMS0-9\s()?:+\-*<>=]+", expr):
        raise SystemExit(f"SETUP: refusing to evaluate {expr!r} - the gate "
                         "only understands N_STREAMS arithmetic. Update "
                         "check_entity_shape.py deliberately.")
    py = expr.replace("N_STREAMS", str(n_streams))
    # SV `c ? a : b` -> Python `a if c else b`
    m = re.fullmatch(r"\s*\((.+?)\)\s*\?\s*(.+?)\s*:\s*(.+?)\s*", py)
    if m:
        py = f"({m.group(2)}) if ({m.group(1)}) else ({m.group(3)})"
    return int(eval(py, {"__builtins__": {}}, {}))   # noqa: S307 - vetted above


def rtl_shape(n_streams):
    """(talker_sources, listener_sinks) the built gateware will advertise."""
    text = open(DATAPATH).read()
    return (eval_sv_ternary(sv_localparam_expr(text, "ACMP_SRC_C"), n_streams),
            eval_sv_ternary(sv_localparam_expr(text, "ACMP_SINKS_C"),
                            n_streams))


def check_rtl_wiring():
    """B + C: the advertised count IS the addressable count, and it is RO."""
    print("== RTL: the shape is elaborated, not provisioned ==")
    dp = open(DATAPATH).read()
    inst = re.search(r"milan_csr\s*#\((.*?)\)\s*csr\s*\(", dp, re.S)
    if not inst:
        raise SystemExit("SETUP: no milan_csr instantiation in milan_datapath")
    params = inst.group(1)
    ck("milan_csr .N_TALKER_SRC_P <- ACMP_SRC_C",
       bool(re.search(r"\.N_TALKER_SRC_P\s*\(\s*ACMP_SRC_C\s*\)", params)), True)
    ck("milan_csr .N_LISTENER_SINK_P <- ACMP_SINKS_C",
       bool(re.search(r"\.N_LISTENER_SINK_P\s*\(\s*ACMP_SINKS_C\s*\)",
                      params)), True)

    csr = open(CSR).read()
    ck("milan_csr declares N_TALKER_SRC_P",
       bool(re.search(r"parameter\s+int\s+N_TALKER_SRC_P", csr)), True)
    ck("milan_csr declares N_LISTENER_SINK_P",
       bool(re.search(r"parameter\s+int\s+N_LISTENER_SINK_P", csr)), True)
    ck("0x618 word is built from N_TALKER_SRC_P",
       bool(re.search(r"ADP_TALK_C\s*=\s*\{[^}]*N_TALKER_SRC_P", csr, re.S)),
       True)
    ck("0x61C word is built from N_LISTENER_SINK_P",
       bool(re.search(r"ADP_LIST_C\s*=\s*\{[^}]*N_LISTENER_SINK_P", csr, re.S)),
       True)
    ck("0x618 has a defaults-ROM arm",
       bool(re.search(r"A_ADP_TALK\[10:0\]:\s*csr_default\s*=\s*ADP_TALK_C",
                      csr)), True)
    ck("0x61C has a defaults-ROM arm",
       bool(re.search(r"A_ADP_LIST\[10:0\]:\s*csr_default\s*=\s*ADP_LIST_C",
                      csr)), True)
    # RO means: no write arm and no shadow-write entry. Either one coming back
    # restores the exact defect - a register that faithfully holds a lie.
    ck("0x618 has NO write arm",
       bool(re.search(r"A_ADP_TALK:\s*\w+\s*<=", csr)), False)
    ck("0x61C has NO write arm",
       bool(re.search(r"A_ADP_LIST:\s*\w+\s*<=", csr)), False)
    rw = re.search(r"function automatic logic is_plain_rw.*?endfunction", csr,
                   re.S)
    if not rw:
        raise SystemExit("SETUP: no is_plain_rw function in milan_csr")
    body = re.sub(r"//[^\n]*", "", rw.group(0))     # comments name them
    ck("0x618 is NOT plain-RW", "A_ADP_TALK" in body, False)
    ck("0x61C is NOT plain-RW", "A_ADP_LIST" in body, False)


# ------------------------------------------------------------ AEM ROM read --
def rom_descriptor_counts(path):
    """Count descriptors by type in a generated aecp_aem_rom.svh directory."""
    text = open(path).read()
    body = re.search(r"AEM_DIR_C\s*\[[^\]]*\]\s*=\s*'\{(.*?)\};", text, re.S)
    if not body:
        raise SystemExit(f"SETUP: no AEM_DIR_C directory in {path}")
    counts = {}
    for row in re.findall(r"64'h([0-9A-Fa-f_]{4})_", body.group(1)):
        t = int(row.replace("_", ""), 16)
        counts[t] = counts.get(t, 0) + 1
    return counts


# -------------------------------------------------------------- the checks --
def check_config(builder, path, tracked_rom_counts):
    cfg = builder.load_config(path)
    name = cfg["name"]
    L, T = len(cfg["listeners"]), len(cfg["talkers"])
    n_streams = max(L, T)                    # emit_soc_argv's --num-streams
    print(f"\n== {name}  ({L}x{T}, N_STREAMS={n_streams}) ==")

    src, sink = rtl_shape(n_streams)
    ovl = builder.emit_aem_overlay(cfg)
    dc, ec = ovl["descriptor_counts"], ovl["entity_counts"]

    # D: the AEM model is self-consistent (the ADPDU counts ARE the descriptor
    # counts - 1722.1-2021 6.2.1.9 / 6.2.1.11)
    ck(f"{name}: entity_counts.talker == STREAM_OUTPUT descriptors",
       ec["talker_stream_sources"], dc["STREAM_OUTPUT"])
    ck(f"{name}: entity_counts.listener == STREAM_INPUT descriptors",
       ec["listener_stream_sinks"], dc["STREAM_INPUT"])

    # A + D: the gateware's addressable range IS the model's descriptor set.
    # This is the arm that catches a CRF output the talker count does not
    # cover: crf_output moves STREAM_OUTPUT to T+1 while ACMP_SRC_C is
    # N_STREAMS+1 only when N_STREAMS > 1.
    ck(f"{name}: advertised talker sources == STREAM_OUTPUT count",
       src, dc["STREAM_OUTPUT"])
    ck(f"{name}: advertised listener sinks == STREAM_INPUT count",
       sink, dc["STREAM_INPUT"])

    # the CRF sources/sinks are the reason the counts are N+1: say so, so a
    # future reader sees which uid the extra slot belongs to
    if cfg["clocking"]["crf_output"]:
        ck(f"{name}: CRF talker uid {n_streams} is inside the advertised range",
           src > n_streams, True)
    if cfg["clocking"]["crf_sink"]:
        ck(f"{name}: CRF sink uid {n_streams} is inside the advertised range",
           sink > n_streams, True)

    # E: the tracked AEM ROM belongs to exactly one config - the one that owns
    # the tracked RTL tables. Everything else builds against a ROM it did not
    # generate, which is a build-flow fact worth stating rather than assuming.
    if cfg["srp"]["rtl_table"]:
        ck(f"{name} owns the tracked AEM ROM: STREAM_OUTPUT",
           tracked_rom_counts.get(STREAM_OUTPUT, 0), dc["STREAM_OUTPUT"])
        ck(f"{name} owns the tracked AEM ROM: STREAM_INPUT",
           tracked_rom_counts.get(STREAM_INPUT, 0), dc["STREAM_INPUT"])
        ck(f"{name} owns the tracked AEM ROM: matches the RTL shape",
           (tracked_rom_counts.get(STREAM_OUTPUT, 0),
            tracked_rom_counts.get(STREAM_INPUT, 0)), (src, sink))


def load_builder():
    sys.path.insert(0, os.path.join(ROOT, "sw/builder"))
    try:
        import endstation_builder as b
    except ImportError as e:                          # pragma: no cover
        raise SystemExit(f"SETUP: cannot import endstation_builder ({e})")
    return b


def run(configs=None):
    builder = load_builder()
    rom = rom_descriptor_counts(AEM_ROM)
    print(f"tracked AEM ROM {os.path.relpath(AEM_ROM, ROOT)}: "
          f"{rom.get(STREAM_OUTPUT, 0)} STREAM_OUTPUT, "
          f"{rom.get(STREAM_INPUT, 0)} STREAM_INPUT")
    check_rtl_wiring()
    for p in configs or sorted(
            os.path.join(CONFIG_DIR, f) for f in os.listdir(CONFIG_DIR)
            if f.startswith("endstation_") and f.endswith(".yaml")):
        check_config(builder, p, rom)


# ---------------------------------------------------------------- self-test --
def mutate(text, old, new):
    if old not in text:
        raise SystemExit(f"SELF-TEST SETUP: {old!r} not in the source")
    return text.replace(old, new, 1)


def expect_fail(label, fn):
    """Run a mutated world and require the pipeline to REJECT it.

    A rejection counts whether it comes from this gate's own comparisons or
    from the builder refusing to load the config - both stop the build."""
    global fails, checks, quiet
    saved_f, saved_c, saved_q = fails, checks, quiet
    fails, checks, quiet = [], 0, True
    try:
        fn()
    except Exception as e:                            # noqa: BLE001
        fails.append(f"{type(e).__name__}: {e}")
    caught, why = bool(fails), (fails[0] if fails else "")
    fails, checks, quiet = saved_f, saved_c, saved_q
    ck(f"MUTATION rejected: {label}", caught, True)
    if caught:
        print(f"         (rejected by: {why})")


def with_rtl(dp_text=None, csr_text=None):
    """Context-manager-ish helper: swap in mutated RTL for one call."""
    global DATAPATH, CSR
    keep = (DATAPATH, CSR)
    td = tempfile.mkdtemp()
    if dp_text is not None:
        DATAPATH = os.path.join(td, "milan_datapath.sv")
        open(DATAPATH, "w").write(dp_text)
    if csr_text is not None:
        CSR = os.path.join(td, "milan_csr.sv")
        open(CSR, "w").write(csr_text)

    def restore():
        global DATAPATH, CSR
        DATAPATH, CSR = keep
        shutil.rmtree(td, ignore_errors=True)
    return restore


def self_test():
    """Mutation proof: five ways the shape can disagree, each must FAIL."""
    print("\n== self-test: a disagreeing shape must be REJECTED ==")
    builder = load_builder()
    rom = rom_descriptor_counts(AEM_ROM)
    src_cfg = os.path.join(CONFIG_DIR, "endstation_ax7101_8x8.yaml")
    base_cfg = open(src_cfg).read()
    base_dp = open(DATAPATH).read()
    base_csr = open(CSR).read()

    # 1. THE CRF CASE the bench found. The gateware keeps a CRF Media Clock
    #    Output at talker_unique_id = N_STREAMS but the advertised source
    #    count drops back to N_STREAMS, so uid 8 sits outside the range and
    #    no controller can see or bind it - CRF on the wire, invisible to
    #    ATDECC. This is the mutation that reproduces the 2026-07-27 report.
    restore = with_rtl(dp_text=mutate(
        base_dp,
        "localparam int ACMP_SRC_C = (N_STREAMS > 1) ? N_STREAMS + 1 : 1;",
        "localparam int ACMP_SRC_C = N_STREAMS;"))
    try:
        expect_fail("advertised talker count excludes the CRF uid",
                    lambda: check_config(builder, src_cfg, rom))
    finally:
        restore()

    # 2. the pre-fix sink formula max(N, 2): at N = 8 that is 8 sinks against
    #    a 9-STREAM_INPUT model - the CRF sink un-addressable the same way
    restore = with_rtl(dp_text=mutate(
        base_dp,
        "localparam int ACMP_SINKS_C = (N_STREAMS > 1) ? N_STREAMS + 1 : 2;",
        "localparam int ACMP_SINKS_C = (N_STREAMS > 2) ? N_STREAMS : 2;"))
    try:
        expect_fail("RTL sink count regressed to max(N_STREAMS, 2)",
                    lambda: check_config(builder, src_cfg, rom))
    finally:
        restore()

    # 3. the register going back to RW: a write arm restored in milan_csr
    restore = with_rtl(csr_text=mutate(
        base_csr,
        "          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;",
        "          A_ADP_TALK:   adp_ccaps <= s_axi_wdata;\n"
        "          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;"))
    try:
        expect_fail("milan_csr regained a write arm for 0x618",
                    check_rtl_wiring)
    finally:
        restore()

    # 4. and the other half of RW: the shadow write-back entry restored, which
    #    is what actually makes a written value stick on readback
    restore = with_rtl(csr_text=mutate(
        base_csr, "      A_ADP_ECAPS, A_ADP_CCAPS, A_ADP_GMLO,",
        "      A_ADP_ECAPS, A_ADP_TALK, A_ADP_LIST, A_ADP_CCAPS, A_ADP_GMLO,"))
    try:
        expect_fail("milan_csr regained the is_plain_rw entries",
                    check_rtl_wiring)
    finally:
        restore()

    # 5. a config whose model loses one STREAM_INPUT while N_STREAMS (set by
    #    the wider direction, 8 talkers) does not move
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "short_listener.yaml")
        open(p, "w").write(mutate(
            base_cfg,
            '    - { name: "Stream In 7", channels: 8, formats: '
            '["0x0205022002006000", "0x0215022002006000"] }\n', ""))
        expect_fail("8x8 config missing one STREAM_INPUT",
                    lambda: check_config(builder, p, rom))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--self-test", action="store_true",
                    help="additionally prove that disagreeing shapes FAIL")
    args = ap.parse_args()
    run()
    if args.self_test:
        self_test()
    print("-" * 70)
    print(f"checks: {checks}   failures: {len(fails)}")
    for f in fails:
        print(f"  {f}")
    print(f"RESULT: {'FAIL' if fails else 'PASS'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
