# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for tests/features/milan_streaming_licence.feature.
#
# These steps RESOLVE THE RTL'S OWN TEXT rather than restating a table: the
# clause is checked against the expression that implements it, so a change to
# the expression is what breaks the test. The wire scenarios decode a byte-exact
# MSRPDU captured from the certified bench bridge (ProfiShark inline tap on the
# ALINX <-> bridge link, 2026-07-28) - FCS stripped, nothing else touched.

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, when, then

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent.parent
_DATAPATH = _ROOT / "hdl" / "milan" / "milan_datapath.sv"
_PACKETIZER = _ROOT / "hdl" / "ieee1722" / "aaf" / "KL_aaf_packetizer.sv"
_MILAN_AUDIT = _ROOT / "docs" / "testing" / "MILAN_V12_AUDIT_2026-08-16.md"

# ---------------------------------------------------------------------------
# The capture. MSRP payload only: ProtocolVersion .. message-list EndMark.
# Four messages in one PDU, ordered TalkerAdvertise(1), Listener(3), Domain(4),
# TalkerFailed(2) - NOT ascending type - with LeaveAllEvent set in every one of
# the four vector headers, and the SR domains packed B-first as NumberOfValues
# = 2 from FirstValue {5, 2, VID} so that SR class A is the +1 value.
# ---------------------------------------------------------------------------
BRIDGE_LEAVEALL_PDU = bytes.fromhex(
    "00"
    "0119001e2001" "0200000000020000" "91e0f00008e0" "0002" "00e0" "0001" "70"
    "00021752" "6c" "0000"
    "0308000e2001" "0200000000010000" "6c" "80" "0000"
    "04040009" "2002" "05020002" "7e" "0000"
    "02220026" "2000" + "00" * 34 + "0000"
    "0000"
)

# 802.1Q-2018 Table 35-1: attribute type -> FirstValue length
Q_TABLE_35_1 = {1: 25, 2: 34, 3: 8, 4: 4}
DECL_NAMES = {0: "Ignore", 1: "AskingFailed", 2: "Ready", 3: "ReadyFailed"}
EVT_NAMES = {0: "New", 1: "JoinIn", 2: "In", 3: "JoinMt", 4: "Mt", 5: "Lv"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_comments(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    return re.sub(r"//[^\n]*", " ", text)


def _assign(text, lhs):
    """Return the right-hand side of `assign <lhs> = ...;` or `wire ... <lhs> = ...;`."""
    body = _strip_comments(text)
    m = re.search(r"\b" + re.escape(lhs) + r"\s*=\s*(.*?);", body, flags=re.S)
    assert m, "no assignment to %s found" % lhs
    return " ".join(m.group(1).split())


def _decode(pdu):
    """Minimal MRPDU walk. Returns [(type, alen, all_len, nv, lva, fv, evts, decls)]."""
    out, off = [], 1
    while off + 2 <= len(pdu) and pdu[off:off + 2] != b"\x00\x00":
        at, alen = pdu[off], pdu[off + 1]
        all_len = int.from_bytes(pdu[off + 2:off + 4], "big")
        p, end = off + 4, off + 4 + all_len
        while p + 2 <= min(end, len(pdu)) and pdu[p:p + 2] != b"\x00\x00":
            vh = int.from_bytes(pdu[p:p + 2], "big")
            lva, nv = vh >> 13, vh & 0x1FFF
            p += 2
            fv = pdu[p:p + alen]
            p += alen
            n3 = (nv + 2) // 3
            evts = []
            for o in pdu[p:p + n3]:
                evts += [(o // 36) % 6, (o // 6) % 6, o % 6]
            p += n3
            decls = []
            if at == 3:
                n4 = (nv + 3) // 4
                for o in pdu[p:p + n4]:
                    decls += [(o >> 6) & 3, (o >> 4) & 3, (o >> 2) & 3, o & 3]
                p += n4
            out.append((at, alen, all_len, nv, lva, fv, evts[:nv], decls[:nv]))
        off = end
    return out


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
@given("the Milan datapath and AAF talker RTL sources")
def step_rtl_sources(context: Context) -> None:
    """Refuse to grade a clause against a source that is not there: every
    later step resolves the RTL by regex, and a regex over a missing file
    would report the absence of the defect it was meant to find."""
    for path in (_DATAPATH, _PACKETIZER):
        assert path.is_file(), "missing %s" % path


# ---------------------------------------------------------------------------
# Structure scenario - the admission composition and its one escape hatch
# ---------------------------------------------------------------------------
@when("I read the aaf_gate expression from milan_datapath")
def step_read_aaf_gate(context: Context) -> None:
    """Resolve the aaf_gate right-hand side as it ships, so the scenario
    grades the expression that admits the talker and not a copy of it."""
    context.expr = _assign(_read(_DATAPATH), "aaf_gate")


@then("the gate has exactly one escape hatch and it is named cfg_aaf_bypass")
def step_one_escape_hatch(context: Context) -> None:
    """Pin the whole identifier set of the admission composition: exactly one
    bypass, spelled cfg_aaf_bypass, sitting on the left of the escape OR."""
    # The whole point of this scenario is that a SECOND silent bypass must not
    # appear. So pin the identifier set, not the shape: any new signal in the
    # admission composition has to be argued for here first.
    expected = {
        "cfg_aaf_enable",        # AAF_CTRL[0], the talker enable
        "cfg_maap_enable",       # MAAP_CTRL[0] ...
        "maap_addr_valid",       # ... and its claim, per Milan 4.3.5.1
        "cfg_aaf_bypass",        # AAF_CTRL[1], THE escape hatch
        "acmp_talker_active",    # the 1722.1 talker SM
        "cfg_lwsrp_enable",      # LWSRP_CTRL[0] ...
        "lwsrp_stream_gate",     # ... and the Milan 5.3.7.3 licence
    }
    found = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", context.expr))
    assert found == expected, (
        "the AAF admission composition changed - unexpected %s, missing %s; "
        "expression is %s"
        % (sorted(found - expected), sorted(expected - found), context.expr))
    assert context.expr.count("cfg_aaf_bypass") == 1, context.expr
    assert "(cfg_aaf_bypass |" in context.expr, (
        "cfg_aaf_bypass must be the left operand of the escape-hatch OR, so "
        "that clearing it leaves the qualified admission alone: %s"
        % context.expr)


@then("with the escape hatch clear the gate requires the lwSRP stream gate")
def step_gate_requires_lwsrp(context: Context) -> None:
    """With the hatch clear, admission still depends on the Milan 5.3.7.3
    licence terms - the engine enable, its stream gate and the talker SM."""
    assert "lwsrp_stream_gate" in context.expr, context.expr
    assert "cfg_lwsrp_enable" in context.expr, context.expr
    assert "acmp_talker_active" in context.expr, context.expr


@then("the escape hatch is recorded as a Milan 5.3.7.3 conformance defect")
def step_escape_hatch_recorded(context: Context) -> None:
    """A bypass that can still be set has to stay named, with its clause, in
    the current Milan audit; an undocumented escape hatch is the defect."""
    gaps = _read(_MILAN_AUDIT)
    assert "AAF_CTRL[1]" in gaps and "5.3.7.3" in gaps, (
        "the bypass must stay named in the current Milan audit with its clause "
        "for as long as it can be set")


# ---------------------------------------------------------------------------
# Wire scenarios - the byte-exact capture
# ---------------------------------------------------------------------------
@given("the MSRPDU captured from the bench bridge on 2026-07-28")
def step_capture(context: Context) -> None:
    """Decode the bench capture once for the scenario, and fail here rather
    than let an empty walk make every later wire assertion vacuously true."""
    context.pdu = BRIDGE_LEAVEALL_PDU
    context.msgs = _decode(context.pdu)
    assert context.msgs, "capture did not decode"


@then("it is a well-formed MRPDU whose every AttributeLength matches 802.1Q "
      "Table 35-1")
def step_wellformed(context: Context) -> None:
    """Grade the PDU as a whole: ProtocolVersion, the message ORDER (which is
    evidence that the bridge does not sort by type), the Table 35-1 length of
    every attribute, and LeaveAll in every vector header."""
    assert context.pdu[0] == 0, "ProtocolVersion must be 0"
    seen = [m[0] for m in context.msgs]
    assert seen == [1, 3, 4, 2], (
        "the capture's message order is load-bearing evidence: %s" % seen)
    for at, alen, _all, _nv, lva, _fv, _e, _d in context.msgs:
        assert Q_TABLE_35_1[at] == alen, (at, alen)
        assert lva == 1, "every vector header in this PDU carries LeaveAll"


@then("it declares a Listener attribute for StreamID {sid}")
def step_listener_sid(context: Context, sid: str) -> None:
    """Select, by byte-exact StreamID, the Listener attribute the remaining
    steps grade - and bind it so they all speak about the same one."""
    lis = [m for m in context.msgs if m[0] == 3 and m[3] > 0]
    assert lis, "no Listener attribute with NumberOfValues > 0"
    context.listener = lis[0]
    assert context.listener[5].hex() == sid, context.listener[5].hex()


@then("that Listener declaration is {want}")
def step_listener_decl(context: Context, want: str) -> None:
    """Name the Listener's four-packed declaration type: Ready and
    ReadyFailed license a talker, AskingFailed and Ignore do not."""
    decls = context.listener[7]
    assert decls and DECL_NAMES[decls[0]] == want, decls


@then("the SR class A domain is present as the +1 value of a B-first packed pair")
def step_domain_plus_one(context: Context) -> None:
    """SR class A is present ONLY as the incremented second value of a
    B-first packed pair, so a decoder that reads FirstValue alone concludes
    the bridge never offered class A."""
    dom = [m for m in context.msgs if m[0] == 4]
    assert dom, "no Domain message"
    at, alen, _all, nv, _lva, fv, evts, _d = dom[0]
    assert nv == 2, "expected the B-first packed pair, NumberOfValues=%d" % nv
    assert (fv[0], fv[1]) == (5, 2), "FirstValue is not SR class B: %s" % fv.hex()
    # 802.1Q-2018 10.8.1.4: value k is the FirstValue incremented k times
    assert (fv[0] + 1, fv[1] + 1) == (6, 3), "the +1 value is not SR class A"
    assert int.from_bytes(fv[2:4], "big") == 2, "SRclassVID"
    assert evts[1] not in (4, 5), (
        "the class-A value's event must be a registering one, got %s"
        % EVT_NAMES[evts[1]])


@when("the Listener three-packed event is changed to Lv")
def step_mutate_to_lv(context: Context) -> None:
    """Rewrite one event byte of the real capture to Lv - the negative
    control that proves these wire assertions can fail (methodology R2)."""
    # message @35, +4 header, +2 vector header, +8 FirstValue = payload offset 49
    body = bytearray(context.pdu)
    assert body[49] == 3 * 36, "mutation targets the wrong byte: 0x%02x" % body[49]
    body[49] = 5 * 36
    context.pdu = bytes(body)
    context.msgs = _decode(context.pdu)


@then("the Listener declaration is a withdrawal and licenses nothing")
def step_withdrawal(context: Context) -> None:
    """The mutated attribute decodes as a Leave, which withdraws the
    registration and therefore licenses nothing."""
    lis = [m for m in context.msgs if m[0] == 3 and m[3] > 0][0]
    assert EVT_NAMES[lis[6][0]] == "Lv", lis[6]


# ---------------------------------------------------------------------------
# 0x001F - the t>0 admission and the t>0 wire identity
# ---------------------------------------------------------------------------
@when("I read the t>0 AAF admission expression from milan_datapath")
def step_read_tgt0_admission(context: Context) -> None:
    """Resolve the per-stream admission arm out of the g_aaf_stream_en
    generate block - the t>0 twin of the flat t0 aaf_gate."""
    src = _strip_comments(_read(_DATAPATH))
    m = re.search(r"g_aaf_stream_en(.*?)endgenerate", src, flags=re.S)
    assert m, "no g_aaf_stream_en branch in milan_datapath"
    a = re.search(r"assign\s+aaf_stream_en_raw_w\[gs\]\s*=\s*(.*?);",
                  m.group(1), flags=re.S)
    assert a, "no aaf_stream_en_raw_w[gs] arm in g_aaf_stream_en"
    context.expr = " ".join(a.group(1).split())


@then("the t>0 admission does NOT require a per-context runtime enable")
def step_tgt0_no_ctx_enable(context: Context) -> None:
    """The deleted per-context runtime enable has not come back under either
    polarity, and the one enable t>0 may use is the same AAF_CTRL[0] t0
    already answers to."""
    # The deleted term. Named both ways it has existed so a revival under
    # either polarity is caught.
    for forbidden in ("tctx_en_r", "tctx_dis_r"):
        assert forbidden not in context.expr, context.expr
    # ...and the one enable that IS allowed is the flat AAF_CTRL[0] that t0
    # already used, so the two talker classes share one switch.
    assert "cfg_aaf_enable" in context.expr, context.expr


@then("the t>0 admission requires the lwSRP stream gate unconditionally")
def step_tgt0_gate_unconditional(context: Context) -> None:
    """t>0 admits nothing without the lwSRP stream gate and gets no
    engine-off escape, because LWSRP_CTRL resets to engine-OFF."""
    assert "lwsrp_stream_gate" in context.expr, context.expr
    # no engine-off escape for t>0: LWSRP_CTRL resets to engine-OFF, so an
    # escape here would admit unpaced streams out of reset.
    assert "cfg_lwsrp_enable" not in context.expr, (
        "t>0 must not mirror t0's ~cfg_lwsrp_enable escape: %s" % context.expr)


@then("the effective t>0 admission is masked by output mapping reservations")
def step_tgt0_mapping_reservation(context: Context) -> None:
    """The raw t>0 admission reaches the fabric masked by the output-mapping
    reservation, and by nothing else - the term is pinned verbatim."""
    effective = _assign(_read(_DATAPATH), "aaf_stream_en_w")
    assert effective == "aaf_stream_en_raw_w & ~amap_edit_out_resv_r", effective


@when("I read the t>0 wire identity from KL_aaf_packetizer")
def step_read_tgt0_identity(context: Context) -> None:
    """Resolve the three effective identity wires - destination MAC, VID and
    unique_id - that a t>0 stream actually puts on the wire."""
    src = _strip_comments(_read(_PACKETIZER))
    context.ident = {}
    for name in ("eff_dmac_w", "eff_vid_w", "eff_uid_w"):
        m = re.search(r"wire\s*\[[^\]]*\]\s*%s\s*=\s*(.*?);" % name,
                      src, flags=re.S)
        assert m, "no %s in KL_aaf_packetizer" % name
        context.ident[name] = " ".join(m.group(1).split())


@then("the t>0 identity is derived from the same roots the declaration uses")
def step_tgt0_identity_derived(context: Context) -> None:
    """Each identity field is derived from the root the SRP declaration and
    the ACMP answer already use, so the three cannot describe different
    streams."""
    # dmac = the MAAP block base + t, vid = the engine VID, unique_id = t -
    # literally the wires acmp_src_dmac_w and srp_fab_sid_w/dmac_w carry, so
    # advertisement, ACMP answer and wire cannot disagree.
    dmac = context.ident["eff_dmac_w"]
    assert "dest_mac_i" in dmac and "et_r" in dmac, dmac
    assert "vlan_vid_i" in context.ident["eff_vid_w"], context.ident
    uid = context.ident["eff_uid_w"]
    assert "et_r" in uid, uid


@then("software may still name each identity field explicitly")
def step_tgt0_identity_override(context: Context) -> None:
    """A non-zero staged register still wins per field, so an identity a
    controller named explicitly is never overwritten by the derivation."""
    # the CRFT_SID precedent, per field: a NON-ZERO staged value wins over
    # the derived one, so a controller-named identity is never overwritten.
    for name, reg in (("eff_dmac_w", "edmac_r"), ("eff_vid_w", "evid_r"),
                      ("eff_uid_w", "euid_r")):
        expr = context.ident[name]
        assert ("|%s" % reg) in expr.replace(" ", ""), (name, expr)
