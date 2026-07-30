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

import os
import re

from behave import given, when, then

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
_SRP = os.path.join(_ROOT, "hdl", "ieee8021q", "srp")

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


def _read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


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
@given("the lwSRP RTL sources")
def step_srp_sources(context):
    for name in ("KL_lwsrp_registrar.sv", "KL_lwsrp_bw_gate.sv",
                 "KL_lwsrp_tx.sv"):
        path = os.path.join(_SRP, name)
        assert os.path.isfile(path), "missing %s" % path
    context.srp_dir = _SRP


# ---------------------------------------------------------------------------
# Clause scenarios - resolved from the RTL expressions
# ---------------------------------------------------------------------------
@when("I read the listener_ready_o expression from KL_lwsrp_registrar")
def step_read_listener_ready(context):
    context.expr = _assign(
        _read(os.path.join(_SRP, "KL_lwsrp_registrar.sv")), "listener_ready_o")


@then("it requires the Listener attribute to be registered")
def step_requires_registered(context):
    assert "listener_reg_o" in context.expr, context.expr
    assert "&&" in context.expr or "&" in context.expr, context.expr


@then('it accepts the declaration {name}')
def step_accepts_decl(context, name):
    token = {"Ready": "LSTN_DECL_READY_C",
             "ReadyFailed": "LSTN_DECL_READY_FAIL_C"}[name]
    assert token in context.expr, \
        "Milan 5.3.7.3 names %s as licensing streaming; %s" % (name, context.expr)


@then('it rejects the declaration {name}')
def step_rejects_decl(context, name):
    token = {"AskingFailed": "LSTN_DECL_ASKING_FAIL_C",
             "Ignore": "LSTN_DECL_IGNORE_C"}[name]
    assert token not in context.expr, \
        "%s does not license streaming under 5.3.7.3; %s" % (name, context.expr)


@when("I read the req_w expression from KL_lwsrp_bw_gate")
def step_read_reqw(context):
    context.expr = _assign(
        _read(os.path.join(_SRP, "KL_lwsrp_bw_gate.sv")), "req_w")


@then("the request requires {signal}")
def step_request_requires(context, signal):
    assert signal in context.expr, \
        "%s is not a term of the bw-gate request: %s" % (signal, context.expr)


@when("I read the TalkerAdvertise inclusion term from KL_lwsrp_tx")
def step_read_talker_incl(context):
    body = _strip_comments(_read(os.path.join(_SRP, "KL_lwsrp_tx.sv")))
    terms = re.findall(r"talker_incl_r\s*<=\s*(.*?);", body, flags=re.S)
    assert terms, "no talker_incl_r assignment found"
    context.terms = [" ".join(t.split()) for t in terms]


@then("the Talker attribute does not depend on any Listener registration")
def step_talker_unconditional(context):
    for term in context.terms:
        for forbidden in ("lstn_ready_i", "listener_ready", "lstn_declare_i",
                          "ta_registered"):
            assert forbidden not in term, (
                "Milan 5.3.7.2: the Talker attribute is declared as soon as the "
                "SRP parameters are valid, unconditionally. Found %r in %r"
                % (forbidden, term))
    joined = " ".join(context.terms)
    assert "talker_en_i" in joined, context.terms


# ---------------------------------------------------------------------------
# Structure scenario - the admission composition and its one escape hatch
# ---------------------------------------------------------------------------
@when("I read the aaf_gate expression from milan_datapath")
def step_read_aaf_gate(context):
    path = os.path.join(_ROOT, "hdl", "milan", "milan_datapath.sv")
    context.expr = _assign(_read(path), "aaf_gate")


@then("the gate has exactly one escape hatch and it is named cfg_aaf_bypass")
def step_one_escape_hatch(context):
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
def step_gate_requires_lwsrp(context):
    assert "lwsrp_stream_gate" in context.expr, context.expr
    assert "cfg_lwsrp_enable" in context.expr, context.expr
    assert "acmp_talker_active" in context.expr, context.expr


@when("I read the per-talker lwSRP provisioning want from milan_datapath")
def step_read_srp_want(context):
    path = os.path.join(_ROOT, "hdl", "milan", "milan_datapath.sv")
    context.dp_src = _strip_comments(_read(path))
    # the AAF slot arm of the per-slot want vector (the generate branch that
    # covers talkers 1..N-1; the top slot is the CRF Media Clock Output)
    # the AAF slot arm is the FIRST srp_fab_want_v_w[gw] assign inside the
    # `g_slot_aaf branch (slot 0 is a constant 0, the CRF slot uses
    # crf_srp_want_w). Anchor on the branch label so a comment mentioning the
    # signal cannot be mistaken for the arm.
    aaf = re.search(r"g_slot_aaf(.*?)g_slot_crf",
                    context.dp_src, flags=re.S)
    assert aaf, "no g_slot_aaf branch in milan_datapath"
    m = re.search(r"assign\s+srp_fab_want_v_w\[gw\]\s*=\s*(.*?);",
                  aaf.group(1), flags=re.S)
    assert m, "no per-AAF-talker srp_fab_want_v_w arm in milan_datapath"
    context.expr = " ".join(m.group(1).split())


@then("the want does NOT require the per-context runtime enable")
def step_want_not_tctx_en(context):
    # Milan 5.3.7.2 makes the declaration unconditional for a DECLARED Stream
    # Output; gating it on the per-context runtime enable (tctx_en_r, reset 0,
    # A_STRMW_CTRL[0]) is a runtime poke the shape-static directive forbids and
    # left a fresh boot silent for t>0.
    assert "tctx_en_r" not in context.expr, context.expr


@then("the want requires the lwSRP engine and its talker declaration")
def step_want_engine(context):
    assert "cfg_lwsrp_enable" in context.expr, context.expr
    assert "cfg_lwsrp_talker_en" in context.expr, context.expr


@then("the want does NOT depend on the lwSRP stream gate")
def step_want_not_circular(context):
    # THE CIRCULAR-DEPENDENCY TRAP. lwsrp_stream_gate[] is an OUTPUT of this
    # engine - it needs the row provisioned AND a Listener Ready - so a want
    # built on it (or on the composed aaf_stream_en_w, which contains it)
    # can never be satisfied: no row because no stream, no stream because no
    # row. Only UPSTREAM terms may appear here.
    for bad in ("lwsrp_stream_gate", "aaf_stream_en_w", "lwsrp_res_active"):
        assert bad not in context.expr, (
            "%s is an engine OUTPUT - wanting on it deadlocks provisioning: %s"
            % (bad, context.expr))


@then("the want does NOT depend on ACMP talker_active, per 5.5.2.7")
def step_want_not_acmp(context):
    # Milan 5.5.2.7: "Talkers rely only on SRP (not ACMP) to determine when to
    # transmit", so a registered Listener Ready starts the stream with no ACMP
    # involvement at all - the advertisement has to exist BEFORE a controller
    # binds, or fast-connect (5.5.3.5.3) finds no reservation to register
    # against.
    assert "acmp_talker_active" not in context.expr, (
        "an SRP-only listener could never be served: %s" % context.expr)


@then("the fabric yields the provisioning port to a CSR write, never to its poll")
def step_arbiter_yields_write_only(context):
    gnt = _assign(context.dp_src, "srp_fab_gnt_w")
    assert "csr_srp_ctx_we" in gnt, gnt
    # gating on the REQUEST is the recorded starvation bug: milan_csr's window
    # master polls level-high for as long as a non-zero row is selected, which
    # every boot script and TB leave in place, so the fabric would never be
    # granted at all.
    assert "csr_srp_ctx_req" not in gnt, (
        "yielding to the CSR POLL pins the fabric requesters off forever: %s"
        % gnt)
    # and the beat that writes must be KL_lwsrp_ctx's own service expression
    svc = _assign(context.dp_src, "srp_fab_svc_w")
    assert "srp_fab_gnt_w" in svc and "srp_ctx_gnt_w" in svc, svc


@then("the escape hatch is recorded as a Milan 5.3.7.3 conformance defect")
def step_escape_hatch_recorded(context):
    gaps = _read(os.path.join(_ROOT, "docs", "MILAN_COMPLIANCE_GAPS.md"))
    assert "AAF_CTRL[1]" in gaps and "5.3.7.3" in gaps, (
        "the bypass must stay named in MILAN_COMPLIANCE_GAPS.md with its clause "
        "for as long as it can be set")


# ---------------------------------------------------------------------------
# Wire scenarios - the byte-exact capture
# ---------------------------------------------------------------------------
@given("the MSRPDU captured from the bench bridge on 2026-07-28")
def step_capture(context):
    context.pdu = BRIDGE_LEAVEALL_PDU
    context.msgs = _decode(context.pdu)
    assert context.msgs, "capture did not decode"


@then("it is a well-formed MRPDU whose every AttributeLength matches 802.1Q "
      "Table 35-1")
def step_wellformed(context):
    assert context.pdu[0] == 0, "ProtocolVersion must be 0"
    seen = [m[0] for m in context.msgs]
    assert seen == [1, 3, 4, 2], (
        "the capture's message order is load-bearing evidence: %s" % seen)
    for at, alen, _all, _nv, lva, _fv, _e, _d in context.msgs:
        assert Q_TABLE_35_1[at] == alen, (at, alen)
        assert lva == 1, "every vector header in this PDU carries LeaveAll"


@then("it declares a Listener attribute for StreamID {sid}")
def step_listener_sid(context, sid):
    lis = [m for m in context.msgs if m[0] == 3 and m[3] > 0]
    assert lis, "no Listener attribute with NumberOfValues > 0"
    context.listener = lis[0]
    assert context.listener[5].hex() == sid, context.listener[5].hex()


@then("that Listener declaration is {want}")
def step_listener_decl(context, want):
    decls = context.listener[7]
    assert decls and DECL_NAMES[decls[0]] == want, decls


@then("the SR class A domain is present as the +1 value of a B-first packed pair")
def step_domain_plus_one(context):
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
def step_mutate_to_lv(context):
    # message @35, +4 header, +2 vector header, +8 FirstValue = payload offset 49
    body = bytearray(context.pdu)
    assert body[49] == 3 * 36, "mutation targets the wrong byte: 0x%02x" % body[49]
    body[49] = 5 * 36
    context.pdu = bytes(body)
    context.msgs = _decode(context.pdu)


@then("the Listener declaration is a withdrawal and licenses nothing")
def step_withdrawal(context):
    lis = [m for m in context.msgs if m[0] == 3 and m[3] > 0][0]
    assert EVT_NAMES[lis[6][0]] == "Lv", lis[6]


# ---------------------------------------------------------------------------
# 0x001F - the t>0 admission and the t>0 wire identity
# ---------------------------------------------------------------------------
@when("I read the t>0 AAF admission expression from milan_datapath")
def step_read_tgt0_admission(context):
    path = os.path.join(_ROOT, "hdl", "milan", "milan_datapath.sv")
    src = _strip_comments(_read(path))
    m = re.search(r"g_aaf_stream_en(.*?)endgenerate", src, flags=re.S)
    assert m, "no g_aaf_stream_en branch in milan_datapath"
    a = re.search(r"assign\s+aaf_stream_en_w\[gs\]\s*=\s*(.*?);",
                  m.group(1), flags=re.S)
    assert a, "no aaf_stream_en_w[gs] arm in g_aaf_stream_en"
    context.expr = " ".join(a.group(1).split())


@then("the t>0 admission does NOT require a per-context runtime enable")
def step_tgt0_no_ctx_enable(context):
    # The deleted term. Named both ways it has existed so a revival under
    # either polarity is caught.
    for forbidden in ("tctx_en_r", "tctx_dis_r"):
        assert forbidden not in context.expr, context.expr
    # ...and the one enable that IS allowed is the flat AAF_CTRL[0] that t0
    # already used, so the two talker classes share one switch.
    assert "cfg_aaf_enable" in context.expr, context.expr


@then("the t>0 admission requires the lwSRP stream gate unconditionally")
def step_tgt0_gate_unconditional(context):
    assert "lwsrp_stream_gate" in context.expr, context.expr
    # no engine-off escape for t>0: LWSRP_CTRL resets to engine-OFF, so an
    # escape here would admit unpaced streams out of reset.
    assert "cfg_lwsrp_enable" not in context.expr, (
        "t>0 must not mirror t0's ~cfg_lwsrp_enable escape: %s" % context.expr)


@when("I read the t>0 wire identity from KL_aaf_packetizer")
def step_read_tgt0_identity(context):
    path = os.path.join(_ROOT, "hdl", "ieee1722", "aaf",
                        "KL_aaf_packetizer.sv")
    src = _strip_comments(_read(path))
    context.ident = {}
    for name in ("eff_dmac_w", "eff_vid_w", "eff_uid_w"):
        m = re.search(r"wire\s*\[[^\]]*\]\s*%s\s*=\s*(.*?);" % name,
                      src, flags=re.S)
        assert m, "no %s in KL_aaf_packetizer" % name
        context.ident[name] = " ".join(m.group(1).split())


@then("the t>0 identity is derived from the same roots the declaration uses")
def step_tgt0_identity_derived(context):
    # dmac = the MAAP block base + t, vid = the engine VID, unique_id = t -
    # literally the wires acmp_src_dmac_w and srp_fab_sid_w/dmac_w carry, so
    # advertisement, ACMP answer and wire cannot disagree.
    dmac = context.ident["eff_dmac_w"]
    assert "dest_mac_i" in dmac and "et_r" in dmac, dmac
    assert "vlan_vid_i" in context.ident["eff_vid_w"], context.ident
    uid = context.ident["eff_uid_w"]
    assert "et_r" in uid, uid


@then("software may still name each identity field explicitly")
def step_tgt0_identity_override(context):
    # the CRFT_SID precedent, per field: a NON-ZERO staged value wins over
    # the derived one, so a controller-named identity is never overwritten.
    for name, reg in (("eff_dmac_w", "edmac_r"), ("eff_vid_w", "evid_r"),
                      ("eff_uid_w", "euid_r")):
        expr = context.ident[name]
        assert ("|%s" % reg) in expr.replace(" ", ""), (name, expr)
