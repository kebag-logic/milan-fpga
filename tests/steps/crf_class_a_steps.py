# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for crf_sr_class_a.feature - the CRF Media Clock Output as an SR
# class A stream (Milan v1.2 7.3.3).
#
# WHAT THIS LAYER CAN AND CANNOT PROVE.  These steps read the ACTUAL RTL
# sources: the frame the CRF emitter builds, and the lane that frame leaves
# on.  There is deliberately NO duplicated table of expected bytes here -
# every number is either read out of the source or derived from a clause.
# What it CANNOT prove is that a bridge accepted the reservation; that is the
# silicon acceptance procedure, and the wire-level byte check lives in
# tb/verilator (crf_tx, milan_dp NxN).
#
# WHAT IS NO LONGER HERE.  The SR class constants the MSRP applicant declares,
# the TSpec the datapath provisions, the Σ-slope gate and the
# tag-follows-declaration interlock were all resolved out of
# hdl/ieee8021q/srp/**.  That RTL has been deleted - the protocol-processor
# submodule is the SRP declarer now - so those steps went with it instead of
# being repointed at something that cannot answer them.
#
# Clauses used:
#   IEEE 802.1Q 9.5     - C-VLAN tag, TPID 0x8100 immediately after SA
#   IEEE 802.1Q 9.6     - TCI = {PCP[15:13], DEI[12], VID[11:0]}
#   IEEE 1722-2016 cl.10- CRF AVTPDU
#   Milan v1.2 7.3.3    - the media clock stream is carried under an SRP
#                         reservation of the specified class (A)

import os
import re

from behave import given, then

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

CRF_TX_SV = os.path.join(ROOT, "hdl", "ieee1722", "crf", "KL_crf_tx.sv")
DATAPATH  = os.path.join(ROOT, "hdl", "milan", "milan_datapath.sv")


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


@given('the CRF talker RTL')
def step_crf_rtl(context):
    context.crf_src = _read(CRF_TX_SV)
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
