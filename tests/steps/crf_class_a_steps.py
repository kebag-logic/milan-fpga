# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for crf_sr_class_a.feature - the CRF Media Clock Output as an SR
# class A stream (Milan v1.2 7.3.3).
#
# WHAT THIS LAYER CAN AND CANNOT PROVE.  These steps read the ACTUAL RTL
# sources and cross-check the separately-authored artifacts that have to
# agree for the stream to be class A on the wire: the frame the emitter
# builds, the SR class constants the MSRP applicant declares, and the TSpec
# the datapath provisions.  There is deliberately NO duplicated table of
# expected bytes here - every number is either read out of the source or
# derived from a clause.  What it CANNOT prove is that a bridge accepted the
# reservation; that is the silicon acceptance procedure, and the wire-level
# byte check lives in tb/verilator (crf_tx, milan_dp NxN).
#
# Clauses used:
#   IEEE 802.1Q 9.5     - C-VLAN tag, TPID 0x8100 immediately after SA
#   IEEE 802.1Q 9.6     - TCI = {PCP[15:13], DEI[12], VID[11:0]}
#   IEEE 802.1Q 34.5 / Table 34-1 - SR class A default priority 3, SR VID 2
#   IEEE 802.1Q 35.1.2  - a declaration is what makes a bridge prune a
#                         stream toward registered Listeners
#   IEEE 802.1Q 35.2.2.4- MSRP attribute FirstValue layout (TalkerAdvertise
#                         = StreamID, DataFrameParameters, TSpec,
#                         PriorityAndRank, AccumulatedLatency)
#   IEEE 1722-2016 cl.10- CRF AVTPDU
#   Milan v1.2 4.2.7.2.1- MSRP Domain = {class A, priority 3, VID 2}
#   Milan v1.2 7.3.3    - the media clock stream is carried under an SRP
#                         reservation of the specified class (A)
#   Milan v1.2 5.3.7.3  - a Stream Output shall not be stopped

import os
import re

from behave import given, then

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

CRF_TX_SV = os.path.join(ROOT, "hdl", "ieee1722", "crf", "KL_crf_tx.sv")
LWSRP_PKG = os.path.join(ROOT, "hdl", "ieee8021q", "srp", "lwsrp_pkg.sv")
DATAPATH  = os.path.join(ROOT, "hdl", "milan", "milan_datapath.sv")
BUILDER   = os.path.join(ROOT, "sw", "builder", "endstation_builder.py")

#! 802.1Q idleSlope per-frame overhead, the identity this repo already uses:
#! preamble 8 + eth hdr 14 + VLAN tag 4 + FCS 4 + IPG 12
SRP_FRAME_OVERHEAD_B = 42
#! class A classMeasurementInterval 125 us
CLASS_A_INTERVALS_PS = 8000


def _read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


#! sized Verilog literal: [width]'[s][base]digits
_LIT = re.compile(r"(?:(\d+)\s*)?'([sS])?([bBoOdDhH])\s*([0-9A-Fa-f_xXzZ]+)")
_BASE = {"b": 2, "o": 8, "d": 10, "h": 16}


def _lit_sub(m):
    return str(int(m.group(4).replace("_", ""), _BASE[m.group(3).lower()]))


def _localparam_int(src, name, _depth=0):
    """Integer value of `localparam ... NAME = <expr>;`.

    Resolves sized literals and references to other localparams in the same
    file, so the check reads the RTL's real arithmetic instead of a number
    someone re-typed here. Deliberately arithmetic only - anything cleverer
    than +-*/ and parentheses should not be hiding in a frame-size constant.
    """
    assert _depth < 8, "localparam %s: reference loop" % name
    m = re.search(r"localparam\b[^;]*?\b" + re.escape(name) +
                  r"\s*=\s*([^;]+);", src)
    assert m, "no localparam %s found" % name
    expr = re.sub(r"//.*", "", m.group(1))
    expr = re.sub(r"\b\d+\s*'\s*\(", "(", expr)     # SV size cast 16'(...)
    expr = _LIT.sub(_lit_sub, expr)
    for ident in sorted(set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)),
                        key=len, reverse=True):
        expr = re.sub(r"\b" + ident + r"\b",
                      str(_localparam_int(src, ident, _depth + 1)), expr)
    assert re.fullmatch(r"[\s0-9+\-*/()]+", expr), \
        "localparam %s is not plain arithmetic: %r" % (name, expr)
    return int(eval(expr))     # noqa: S307 - guarded to digits and + - * / ( )


def _instance(src, module):
    """Text of the `<module> <inst> ( ... );` instantiation.

    Scoping matters: KL_aaf_packetizer has a `.vlan_vid_i` too, and a check
    that accidentally reads the AAF talker's VID would pass while the CRF
    stream carried a different VLAN from its own declaration.
    """
    #! by MODULE name (`<module> [#(params)] <inst> (`, parameters optional)
    #! or, failing that, by INSTANCE name (`... <inst> (`)
    m = re.search(r"\b" + re.escape(module) +
                  r"\s+(?:#\s*\([^;]*?\)\s*)?\w+\s*\(", src) \
        or re.search(r"\b" + re.escape(module) + r"\s*\(", src)
    assert m, "no %s instantiation found" % module
    i, depth = m.end() - 1, 0
    for j in range(i, len(src)):
        if src[j] == "(":
            depth += 1
        elif src[j] == ")":
            depth -= 1
            if depth == 0:
                return src[i:j + 1]
    raise AssertionError("unterminated %s instantiation" % module)


def _port(src, module, port):
    m = re.search(r"\." + re.escape(port) + r"\s*\(([^)]*)\)",
                  _instance(src, module))
    assert m, "%s.%s is not connected" % (module, port)
    return m.group(1).strip()


def _expr(src, name):
    """Right-hand side text of the first `... NAME = <expr>;`."""
    m = re.search(r"\b" + re.escape(name) + r"\s*=\s*(.*?);", src, re.S)
    assert m, "no assignment to %s found" % name
    return m.group(1)


@given('the CRF talker RTL')
def step_crf_rtl(context):
    context.crf_src = _read(CRF_TX_SV)
    context.srp_src = _read(LWSRP_PKG)
    context.dp_src = _read(DATAPATH)


# ---------------------------------------------------------------- the tag
@then('the CRF emitter builds an 802.1Q C-TAG with TPID 0x8100 at octet 12')
def step_tpid(context):
    # 802.1Q 9.5: the TPID sits immediately after the source address, i.e.
    # frame octets 12..13, and is 0x8100 for a C-TAG.
    assert re.search(r"fb\[12\]\s*=\s*8'h81;\s*fb\[13\]\s*=\s*8'h00;",
                     context.crf_src), \
        "no TPID 0x8100 at octets 12..13 in the tagged shape"


@then('the TCI is {{PCP, DEI, VID}} with DEI 0')
def step_tci(context):
    # 802.1Q 9.6: TCI = PCP[15:13] | DEI[12] | VID[11:0]. An SR class A
    # stream is never drop-eligible, so DEI must be a hard 0.
    assert re.search(
        r"fb\[14\]\s*=\s*\{vpcp_r,\s*1'b0,\s*vvid_r\[11:8\]\};"
        r"\s*fb\[15\]\s*=\s*vvid_r\[7:0\];", context.crf_src), \
        "TCI is not {PCP, DEI=0, VID[11:8]} / VID[7:0]"


@then('the EtherType moves to octet 16 in the tagged shape')
def step_ethertype(context):
    assert re.search(r"fb\[16\]\s*=\s*8'h22;\s*fb\[17\]\s*=\s*8'hF0;",
                     context.crf_src), \
        "AVTP EtherType 0x22F0 is not at octets 16..17 when tagged"


@then('the PCP and VID are wires, not literals')
def step_pcp_vid_wires(context):
    # A hardcoded PCP/VID would silently ignore the SR class the bridge
    # actually advertises in its MSRP Domain.
    for port in ("vlan_pcp_i", "vlan_vid_i", "vlan_en_i"):
        assert re.search(r"input\s+wire[^;]*\b" + port + r"\b",
                         context.crf_src), "%s is not a module input" % port


@then('both frame shapes are the same {n:d}-octet frame')
def step_frame_len(context, n):
    # The tag REPLACES pad. If it grew the frame instead, the reservation's
    # MaxFrameSize (below) and the emitted frame would disagree.
    assert _localparam_int(context.crf_src, "FRAME_BYTES") == n, \
        "FRAME_BYTES is not %d" % n


# ------------------------------------------------------- SR class A values
@then('the SR class A priority is {p:d}')
def step_sr_prio(context, p):
    # 802.1Q 34.5 / Table 34-1 default; Milan v1.2 4.2.7.2.1 pins the MSRP
    # Domain triple to {class A, priority 3, VID 2}.
    assert _localparam_int(context.srp_src, "SR_CLASS_A_PRIO_C") == p, \
        "SR_CLASS_A_PRIO_C is not %d" % p


@then('the TalkerAdvertise PriorityAndRank octet is 0x{v:x}')
def step_prio_rank(context, v):
    # 802.1Q 35.2.2.4 FirstValue: PriorityAndRank = priority[7:5], rank[4].
    expr = _expr(context.srp_src, "SR_PRIO_RANK_C")
    assert "SR_CLASS_A_PRIO_C[2:0]" in expr and "SR_RANK_C" in expr, \
        "SR_PRIO_RANK_C is not built from the class A priority and rank"
    prio = _localparam_int(context.srp_src, "SR_CLASS_A_PRIO_C")
    rank = _localparam_int(context.srp_src, "SR_RANK_C")
    assert ((prio & 0x7) << 5) | ((rank & 1) << 4) == v, \
        "PriorityAndRank does not encode to 0x%02x" % v


@then('the frame PCP and the declared priority are one constant')
def step_pcp_is_declared_prio(context):
    # If the tag's PCP and the TalkerAdvertise's priority were two literals
    # they could drift; the bridge would then police the stream against a
    # class it was never declared in.
    expr = _expr(context.dp_src, "crft_pcp_w")
    assert "SR_CLASS_A_PRIO_C" in expr, \
        "the CRF tag PCP is not the lwsrp_pkg SR class A priority"


@then('the frame VID and the declared VID are one wire')
def step_vid_is_declared_vid(context):
    # DataFrameParameters carries the VID (802.1Q 35.2.2.4); the applicant
    # takes it from LWSRP_VID, so the frames must take it from there too.
    assert "cfg_lwsrp_vid" in _port(context.dp_src, "KL_crf_tx", "vlan_vid_i"), \
        "the CRF tag VID is not LWSRP_VID (the declaration's VID)"



def _milan_wire_slot(max_frame, interval_frames=1):
    """Milan v1.2 4.3.3.2 steps 1-3, including the minimum-frame clamp."""
    f = max_frame + 22                  # eth hdr incl VLAN tag, plus FCS
    if f < 68:                          # a tagged minimum-size frame
        f = 68
    return f + 20                       # preamble 8 + inter-packet gap 12


# ------------------------------------------------------------- the TSpec
@then('the declared MaxFrameSize is Table 4.4\'s, and its reservation still '
      'covers the emitted frame')
def step_maxframe(context):
    # MILAN v1.2 4.3.3.2 Table 4.4, row "CRF, 1 ts/pdu": MaxFrameSize =
    # 28 + 1, and the clause makes the table a "shall use". This check used
    # to demand the PADDED MSDU (frame - tagged header = 42) instead, on the
    # reasoning that a reservation must not be smaller than the bytes on the
    # wire. That reasoning is right and is KEPT below - but the clause's own
    # remedy for it is step 2 of the bandwidth recipe, the 68-octet
    # minimum-frame clamp, which KL_lwsrp_bw_gate was missing. With the
    # clamp, the clause's 29 reserves MORE wire than the padded 42 did
    # (88 octets against 84), so following the table is now both conformant
    # AND the safer of the two. Declaring 42 with no clamp reserved
    # 5376 kbps where Table 4.4 mandates 5632.
    frame = _localparam_int(context.crf_src, "FRAME_BYTES")
    eth = _localparam_int(context.dp_src, "CRF_L2_BYTES_C")
    hdr = _localparam_int(context.dp_src, "CRF_TAGGED_HDR_C")
    pdu = _localparam_int(context.dp_src, "CRF_PDU_OCTETS_C")
    maxf = _localparam_int(context.dp_src, "CRF_SRP_MAXF_C")
    assert eth == frame, \
        "milan_datapath CRF_L2_BYTES_C (%d) != KL_crf_tx FRAME_BYTES (%d)" \
        % (eth, frame)
    assert hdr == 14 + 4, "the tagged Ethernet header is not 14 + 4"
    assert maxf == pdu + 1, \
        "CRF_SRP_MAXF_C (%d) is not Table 4.4's 28 + 1" % maxf
    # ...and the property the old assertion existed to protect: the octets
    # the reservation buys must still be at least the octets we emit.
    reserved = _milan_wire_slot(maxf)
    emitted = frame + 4 + 20            # + FCS, + preamble and IPG
    assert reserved >= emitted, \
        "reservation %d octets < emitted %d - the clamp is missing" \
        % (reserved, emitted)
    context.crf_maxf = maxf


@then('the declared MaxIntervalFrames is {n:d}')
def step_interval(context, n):
    # class A classMeasurementInterval is 125 us and CRF sends one PDU every
    # 2 ms, so a TSpec - which counts whole frames per interval - can only
    # express 1. The over-provision is structural, not an error.
    assert _localparam_int(context.dp_src, "CRF_SRP_INTV_C") == n, \
        "CRF_SRP_INTV_C is not %d" % n
    context.crf_intv = n


@then('the reservation fits the 75 percent class A budget on a {rate:d} Mb link')
def step_budget(context, rate):
    slope = context.crf_intv * \
        (context.crf_maxf + SRP_FRAME_OVERHEAD_B) * 8 * CLASS_A_INTERVALS_PS
    ceiling = int(rate * 1e6 * 0.75)        # Milan 5.6 / 802.1Q 34.3.1
    assert slope <= ceiling, \
        "CRF idleSlope %d bps exceeds the %d bps class A ceiling" \
        % (slope, ceiling)
    context.crf_slope = slope


@then('the reservation is over-provisioned by at least {factor:d}x the real rate')
def step_overprovision(context, factor):
    # The honest statement of the cost: 500 PDU/s of an 84-octet wire slot.
    # It is recorded so nobody "optimises" it by weakening the SR class.
    real = 500 * (context.crf_maxf + SRP_FRAME_OVERHEAD_B) * 8
    assert context.crf_slope >= factor * real, \
        "over-provision is %.1fx, expected at least %dx" \
        % (context.crf_slope / float(real), factor)


# ---------------------------------------------------- the prune interlock
@then('the tag is derived from the provisioned reservation, not from a bare bit')
def step_interlock(context):
    # 802.1Q 35.1.2: pruning toward registered Listeners is what a
    # declaration buys. A tag with no declaration puts the stream in the
    # reserved SR VLAN while holding no reservation - unshaped traffic in a
    # shaped tree. The tag must therefore be a FUNCTION of the declaration.
    driver = _port(context.dp_src, "KL_crf_tx", "vlan_en_i")
    assert driver == "crft_class_a_w", \
        "vlan_en_i is driven by %r, not the class A interlock" % driver
    expr = _expr(context.dp_src, "crft_class_a_w")
    assert "crf_srp_val_r" in expr, \
        "the tag does not depend on the provisioned lwSRP row"
    assert "cfg_lwsrp_enable" in expr and "cfg_lwsrp_talker_en" in expr, \
        "the tag does not depend on a running MSRP applicant"


@then('a bare CSR request cannot tag the stream on its own')
def step_csr_cannot_tag(context):
    # NEGATIVE: CRFT_CTRL[1] must not appear in the tag expression. It asks
    # for class A; only the granted row grants it.
    expr = _expr(context.dp_src, "crft_class_a_w")
    assert "cfg_crft_class_a" not in expr, \
        "CRFT_CTRL[1] reaches the tag directly - the interlock is bypassable"


@then('the reservation row is provisioned by the fabric, not by software')
def step_fabric_provisions(context):
    # The CRF stream_id and DMAC are DERIVED (they follow the ACMP answer
    # for talker_unique_id = N_STREAMS); software could only restate them.
    #
    # 2026-07-30: the CRF row became ONE SLOT of a rotating fabric arbiter
    # (every AAF talker row joined it), so the port is presented the slot's
    # record rather than the CRF wires directly; 2026-08-02: that record is
    # presented THROUGH the timing-closure launch stage's capture register.
    # The property is unchanged and now needs THREE links: the port takes
    # the captured fabric record under the fabric's port select, the capture
    # latches the fabric record mux, and the record mux resolves to the
    # derived CRF identity on the CRF slot.
    for port, q, rec, sig in (
            ("ctx_sid_i", "srp_fab_qsid_r", "srp_fab_sid_w",
             "eff_crft_sid_w"),
            ("ctx_dmac_i", "srp_fab_qdmac_r", "srp_fab_dmac_w",
             "eff_crft_dmac_w")):
        assert re.search(r"\." + port + r"\s*\(srp_fab_qsel_w\s*\?\s*" + q,
                         context.dp_src), \
            "%s is not the captured fabric record's own port arm" % port
        assert re.search(q + r"\s*<=\s*" + rec, context.dp_src), \
            "%s does not capture the fabric record mux" % q
        assert re.search(r"wire.*" + rec +
                         r"\s*=\s*srp_fab_is_crf_w\s*\r?\n?\s*\?\s*" + sig,
                         context.dp_src), \
            "%s is not what the fabric presents for the CRF slot" % sig


@then('the request retires only on the beat the engine sampled it')
def step_handshake(context):
    # The defect this pins: retiring on any ctx grant let a foreign grant
    # (the CSR window's continuous poll) mark the row provisioned while it
    # had never been written - tag on, no Talker Advertise. Since the
    # 2026-08-02 launch stage the sampling beat is the fabric's OWN capture
    # (srp_fab_launch_w, guaranteed delivery), still never anybody's grant.
    expr = _expr(context.dp_src, "crf_srp_ret_w")
    assert "srp_fab_launch_w" in expr and "srp_fab_is_crf_w" in expr, \
        "crf_srp_ret_w is not {our own capture} restricted to the CRF slot"
    launch = _expr(context.dp_src, "srp_fab_launch_w")
    assert "srp_ctx_gnt_w" not in launch, \
        "the launch depends on the port grant - a foreign grant can retire us"
    assert re.search(r"if\s*\(crf_srp_ret_w\)\s*begin", context.dp_src), \
        "the provisioning shadow does not retire on the capture beat"


# ------------------------------------------------------------- the lane
@then('the CRF AXIS is bound to the data lane, not the control merge')
def step_lane(context):
    # L1 BINDING (structural). The CRF PDU carries a gPTP timestamp a
    # listener steers its recovery clock against; on the control lane it sat
    # behind tx_ifg_gasket's 512-cycle per-frame spacing and behind whatever
    # ADP/AECP/ACMP/MAAP/lwSRP burst was in flight.
    #
    # ORACLE HONESTY: this observes the STRUCTURE, not the wire. The
    # wire-observable form of the property is CRF inter-arrival jitter under
    # a controller enumeration burst, which is an L5 measurement on the tap -
    # see the silicon acceptance procedure. Structure is what this offline
    # layer can see, and it is recorded as such.
    body = _instance(context.dp_src, "crf_dp_mux")
    assert "dpaaf_" in body, \
        "crf_dp_mux does not take the AAF/data lane as its other input"
    assert "crft_tx_" in body, "crf_dp_mux does not take the CRF AXIS"
    # ...and the control-lane gasket must NOT see the CRF stream any more
    gasket = _instance(context.dp_src, "ctl_ifg")
    assert "crft_tx_" not in gasket and "ctli_tx_" not in gasket, \
        "the CRF stream still passes through the control min-IFG gasket"


# --------------------------------------------- reservation observability
@then('the reservation state is readable, not inferable from silence')
def step_readable(context):
    # R5: a stream that vanished is not a measurement. Three DISTINCT bits
    # so "not declared", "declared but no Listener registered" (correctly
    # pruned by the bridge) and "reserved and flowing" are told apart from
    # software without a capture.
    stat = _expr(context.dp_src, "crft_stat_c[4]")
    assert "crf_srp_val_r" in stat, "0x750[4] is not the declaration state"
    assert "crft_class_a_w" in _expr(context.dp_src, "crft_stat_c[5]"), \
        "0x750[5] is not the tagged state"
    assert "crft_res_active_w" in _expr(context.dp_src, "crft_stat_c[6]"), \
        "0x750[6] is not the reservation-active state"
    act = _expr(context.dp_src, "crft_res_active_w")
    assert "lwsrp_stream_gate" in act, \
        "reservation-active does not come from the bw-gate"


# ------------------------------------------------------------- SR class B
@then('SR class B is still not reachable')
def step_class_b(context):
    # Do not let class B look covered: neither the engine nor the bench has
    # ever exercised it, and Milan 7.3.3 fixes the CRF stream at class A.
    src = _read(BUILDER)
    m = re.search(r"SRP_SR_CLASSES\s*=\s*(.*?)\n", src)
    assert m, "SRP_SR_CLASSES not found in the builder"
    assert '"B"' not in m.group(1) and "'B'" not in m.group(1), \
        "the builder now offers SR class B - it has never been exercised"
    assert "SR_CLASS_B" not in context.srp_src, \
        "lwsrp_pkg gained class B constants without a bench that exercises it"
