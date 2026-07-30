# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for counters_contract_milan.feature.
#
# The counter tables, the mask arithmetic and the invariants all come from
# tb/tools/torture_campaign.py - the SAME module the on-bench runner decodes
# real GET_COUNTERS responses with. If this feature and the bench disagree about
# what MEDIA_LOCKED means, that is a bug in one file and not a difference of
# opinion between two.
#
# The two L1 scenarios read RTL and documentation source instead: they assert
# the fabric is bound to the contract (the masks it emits, the offsets the
# register map publishes), which is the tier docs/testing/methodology.md names
# as the one this repo was missing.

import os
import re
import sys

from behave import given, then, when

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tb", "tools"))

import torture_campaign as tc  # noqa: E402

BUILDER = os.path.join(ROOT, "hdl", "ieee17221", "aecp",
                       "KL_aecp_response_builder.sv")
REGMAP = os.path.join(ROOT, "docs", "reference", "REGISTER_MAP.md")


@given("the counters contract is importable")
def step_cc_import(context):
    assert hasattr(tc, "MILAN_TABLE_56"), "torture_campaign tables missing"
    context.cc = tc
    context.cc_decoded = {}
    context.cc_payload = None


# ------------------------------------------------------------------- tables --
@then("the Milan Stream Input counter set has {n:d} members")
def step_cc_t56_len(context, n):
    assert len(tc.MILAN_TABLE_56) == n, tc.MILAN_TABLE_56


@then("the Milan Stream Input counter set is")
def step_cc_t56_names(context):
    want = [r["counter"] for r in context.table]
    assert list(tc.MILAN_TABLE_56) == want, \
        f"{tc.MILAN_TABLE_56} != {want}"


@then("the Milan Stream Input mandatory wire mask is {mask}")
def step_cc_t56_mask(context, mask):
    m = tc.counters_valid_mask(tc.MILAN_TABLE_56, tc.IEEE_STREAM_INPUT_BLOCK)
    assert m == int(mask, 0) == tc.MILAN_INPUT_MANDATORY_MASK, \
        f"{m:#05x} != {mask}"


@then("the Milan Stream Output counter set has {n:d} members")
def step_cc_t54_len(context, n):
    assert len(tc.MILAN_TABLE_54) == n, tc.MILAN_TABLE_54


@then("the Milan Stream Output wire mask is {mask}")
def step_cc_t54_mask(context, mask):
    assert tc.MILAN_OUTPUT_MASK == int(mask, 0)
    assert tc.counters_valid_mask(tc.MILAN_TABLE_54,
                                 tc.MILAN_TABLE_54) == int(mask, 0)


@then("the Milan Stream Output counter set is")
def step_cc_t54_names(context):
    want = [r["counter"] for r in context.table]
    assert list(tc.MILAN_TABLE_54) == want, f"{tc.MILAN_TABLE_54} != {want}"


@then("the IEEE Stream Input block has {n:d} members")
def step_cc_ieee_len(context, n):
    assert len(tc.IEEE_STREAM_INPUT_BLOCK) == n


@then("the IEEE Stream Input full wire mask is {mask}")
def step_cc_ieee_mask(context, mask):
    assert tc.MILAN_INPUT_FULL_MASK == int(mask, 0)
    assert tc.counters_valid_mask(tc.IEEE_STREAM_INPUT_BLOCK,
                                 tc.IEEE_STREAM_INPUT_BLOCK) == int(mask, 0)


@then("{name} is at block offset {off:d}")
def step_cc_offset(context, name, off):
    got = tc.IEEE_STREAM_INPUT_BLOCK.index(name) * 4
    assert got == off, f"{name} is at offset {got}, expected {off}"


# --------------------------------------------------------- trap 1: numbering --
@then("the IEEE table bit number for block offset {off:d} is {bit:d}")
def step_cc_bitnum(context, off, bit):
    got = tc.counters_valid_bit_ieee(off)
    assert got == bit, f"offset {off} -> table bit {got}, expected {bit}"


@then("a block offset that is not quadlet aligned is refused")
def step_cc_bitnum_refuse(context):
    try:
        tc.counters_valid_bit_ieee(3)
    except ValueError:
        return
    raise AssertionError("an unaligned offset was accepted")


@then("the table bit number {bit:d} corresponds to wire mask {mask}")
def step_cc_bit_to_mask(context, bit, mask):
    # BOTH DIRECTIONS, and through the PRODUCTION function in both.  The first
    # version of this step computed `slot = 31 - bit` itself and asserted
    # `1 << slot == mask`: arithmetic the step did, checked against arithmetic
    # the step did, with tc.counters_valid_bit_ieee() never called at all.  It
    # could not have failed if the production conversion had been inverted,
    # which is the exact defect it was written to guard.
    slot = 31 - bit
    assert tc.counters_valid_bit_ieee(slot * 4) == bit, (
        f"counters_valid_bit_ieee({slot * 4}) = "
        f"{tc.counters_valid_bit_ieee(slot * 4)}, and IEEE 1722.1-2021 Table "
        f"7-156 calls that bit {bit}")
    assert (1 << slot) == int(mask, 0), \
        f"table bit {bit} -> slot {slot} -> {1 << slot:#010x}, want {mask}"
    # and the round trip closes: the mask's own slot maps back to this bit
    assert tc.counters_valid_bit_ieee(
        (int(mask, 0).bit_length() - 1) * 4) == bit, mask


# ----------------------------------------------------------- trap 2: layouts --
@then("in the Milan layout {name} is at slot {n:d}")
def step_cc_milan_slot(context, name, n):
    assert tc.MILAN_TABLE_54.index(name) == n


@then("in the IEEE layout {name} is at slot {n:d}")
def step_cc_ieee_slot(context, name, n):
    assert tc.IEEE_STREAM_OUTPUT_BLOCK.index(name) == n


@then("decoding a Milan Stream Output block with the IEEE layout mislabels "
      "FRAMES_TX")
def step_cc_mislabel(context):
    # build a Milan-layout block: FRAMES_TX at slot 4 with a recognisable value
    pay = bytearray(8 + 128)
    pay[4:8] = tc.MILAN_OUTPUT_MASK.to_bytes(4, "big")
    pay[8 + 4 * 4:12 + 4 * 4] = (123456).to_bytes(4, "big")
    right = tc.decode_counters_payload(bytes(pay), tc.MILAN_TABLE_54)
    wrong = tc.decode_counters_payload(bytes(pay), tc.IEEE_STREAM_OUTPUT_BLOCK)
    assert right["decoded"]["FRAMES_TX"] == 123456, right
    assert wrong["decoded"].get("FRAMES_TX", 0) != 123456, wrong
    assert wrong["decoded"]["TIMESTAMP_UNCERTAIN"] == 123456, (
        "the IEEE layout must put the Milan FRAMES_TX value under "
        "TIMESTAMP_UNCERTAIN - that is the whole point of the trap")


# --------------------------------------------------------------- the payload --
@given("a GET_COUNTERS payload for descriptor {dt:d} index {di:d} claiming "
       "mask {mask}")
def step_cc_payload(context, dt, di, mask):
    pay = bytearray(8 + 128)
    pay[0:2] = dt.to_bytes(2, "big")
    pay[2:4] = di.to_bytes(2, "big")
    pay[4:8] = int(mask, 0).to_bytes(4, "big")
    for i in range(32):
        pay[8 + 4 * i:12 + 4 * i] = (i + 1).to_bytes(4, "big")
    context.cc_payload = bytes(pay)


@given("a GET_COUNTERS payload truncated to {n:d} octets")
def step_cc_payload_short(context, n):
    context.cc_payload = b"\x00" * n


@then("decoding it raises")
def step_cc_decode_raises(context):
    try:
        tc.decode_counters_payload(context.cc_payload,
                                   tc.IEEE_STREAM_INPUT_BLOCK)
    except ValueError:
        return
    raise AssertionError("a truncated payload decoded without complaint")


@when("the contract decodes it as a Stream Input block")
def step_cc_decode_then(context):
    context.cc_decoded = tc.decode_counters_payload(
        context.cc_payload, tc.IEEE_STREAM_INPUT_BLOCK)


@then("the decode reports claimed-but-unnamed slot {slot:d}")
def step_cc_unnamed(context, slot):
    d = context.cc_decoded
    assert slot in d["claimed_but_unnamed_slots"], d


@then("the decode names only {name}")
def step_cc_only(context, name):
    d = context.cc_decoded
    assert list(d["decoded"]) == [name], d["decoded"]


# ------------------------------------------------------------- the invariants --
@given("MEDIA_LOCKED {a:d} and MEDIA_UNLOCKED {b:d}")
def step_cc_lock(context, a, b):
    context.cc_lock = tc.check_lock_invariant(
        {"MEDIA_LOCKED": a, "MEDIA_UNLOCKED": b})


@then("the lock invariant verdict is {want}")
def step_cc_lock_verdict(context, want):
    assert context.cc_lock[0] == want, context.cc_lock


@then("the lock invariant reports the stream synchronized")
def step_cc_lock_sync(context):
    assert context.cc_lock[1]["synchronized"] is True, context.cc_lock


@then("the lock invariant reports the stream not synchronized")
def step_cc_lock_nosync(context):
    assert context.cc_lock[1]["synchronized"] is False, context.cc_lock


@given("STREAM_START {a:d} and STREAM_STOP {b:d}")
def step_cc_talker(context, a, b):
    context.cc_talker = tc.check_talker_invariant(
        {"STREAM_START": a, "STREAM_STOP": b})


@then("the talker invariant verdict is {want}")
def step_cc_talker_verdict(context, want):
    assert context.cc_talker[0] == want, context.cc_talker


@given("TIMESTAMP_VALID {tv:d} TIMESTAMP_NOT_VALID {tnv:d} FRAMES_RX {frx:d}")
def step_cc_tvtnv(context, tv, tnv, frx):
    context.cc_tv = tc.check_tv_tnv({"TIMESTAMP_VALID": tv,
                                     "TIMESTAMP_NOT_VALID": tnv,
                                     "FRAMES_RX": frx})


@then("the tv-tnv verdict is {want}")
def step_cc_tv_verdict(context, want):
    assert context.cc_tv[0] == want, context.cc_tv


@then('the reading in force is "{reading}"')
def step_cc_tv_reading(context, reading):
    assert context.cc_tv[1]["reading"] == reading, context.cc_tv


@then("the tv-tnv skip says the block was reset at the bind")
def step_cc_tv_vacuous(context):
    why = context.cc_tv[1].get("why", "")
    assert "5.3.8.10" in why and "vacuous" in why, why


@given("{counter} reads {before:d} then {after:d}")
def step_cc_growth(context, counter, before, after):
    context.cc_growth = tc.check_no_growth({counter: before},
                                           {counter: after}, (counter,),
                                           window_s=4.0)


@given("{counter} is not claimed by the mask")
def step_cc_growth_unclaimed(context, counter):
    context.cc_growth = tc.check_no_growth({}, {}, (counter,), window_s=4.0)


@then("the growth verdict is {want}")
def step_cc_growth_verdict(context, want):
    assert context.cc_growth[0] == want, context.cc_growth


@given("a measured frames rate of {rate:f} per second")
def step_cc_rate(context, rate):
    context.cc_reading = tc.frames_rate_reading(rate)
    context.cc_rate = context.cc_reading["band"]


@then("the rate is consistent with the {reading} reading")
def step_cc_rate_band(context, reading):
    assert context.cc_rate == reading, \
        f"classified as {context.cc_rate}, expected {reading} " \
        f"({context.cc_reading['why']})"


@then("the implied observation interval is {secs:f} seconds")
def step_cc_rate_interval(context, secs):
    got = context.cc_reading["implied_interval_s"]
    assert got is not None and abs(got - secs) < 1e-9, \
        f"implied interval {got}, expected {secs}"


@then("the reading refusal cites the 1 second ceiling")
def step_cc_rate_ceiling(context):
    why = context.cc_reading["why"]
    assert "less than or equal to 1 s" in why, why
    assert context.cc_reading["band"] == "neither", context.cc_reading


# ------------------------------------------------------------ plan coverage --
def _plan(context):
    if getattr(context, "cc_plan", None) is None:
        context.cc_plan = tc.build_plan(["matrix"])
        context.cc_cov = tc.plan_covers_every_index(context.cc_plan)
    return context.cc_plan


@then("the campaign plan asks for counters on every Stream Input index")
def step_cc_plan_inputs(context):
    _plan(context)
    assert context.cc_cov["dut_listener"] == tc.ARTY.listener_indices(), \
        context.cc_cov


@then("the campaign plan asks for counters on every Stream Output index")
def step_cc_plan_outputs(context):
    _plan(context)
    assert context.cc_cov["dut_talker"] == tc.ARTY.talker_indices(), \
        context.cc_cov


@then("the campaign plan includes the CRF Media Clock indices")
def step_cc_plan_crf(context):
    _plan(context)
    assert tc.ARTY.crf_out in context.cc_cov["dut_talker"]
    assert tc.ARTY.crf_in in context.cc_cov["dut_listener"]


@then("the CRF Media Clock Input index is in the plan's listener coverage")
def step_cc_plan_crf_in(context):
    _plan(context)
    assert tc.ARTY.crf_in in context.cc_cov["dut_listener"], context.cc_cov


@then("the mandatory mask required of it is {mask}")
def step_cc_crf_mask(context, mask):
    assert tc.MILAN_INPUT_MANDATORY_MASK == int(mask, 0)


# ------------------------------------------------------- L1 fabric bindings --
def _get_counters_block(src: str) -> str:
    """The CMD_GET_COUNTERS arm of the response builder, and nothing else.

    Every const_q[3] assignment in this file used to be a candidate for every
    descriptor's mask check, because the regex was DESCRIPTOR-CONTEXT-FREE: it
    searched the whole 2500-line source for `const_q[3] <= 8'h1F;` and would have
    matched an unrelated command's payload byte just as happily.  Two of the
    three masks in this contract (0x23 for AVB_INTERFACE) literally appear twice
    in the file, so the check was passing on a line it was not aiming at.
    """
    # `CMD_GET_COUNTERS:` appears in more than one case statement (the batch
    # length function has its own), so take the arm that actually decodes the
    # descriptor - anything else is not the responder.
    #! anchor on the CASE ARM (`CMD_GET_COUNTERS: begin`), not on any mention.
    #! An earlier mention (the batch-length table, the multi-command `||` test)
    #! has no `begin`, so its "next CMD_/default" boundary lands hundreds of
    #! lines later and the slice swallows unrelated commands - including the
    #! SET/GET_STREAM_FORMAT arms whose `w_gs_index < 16'd2` literal then gets
    #! blamed on the counters path. That mis-slice produced a false "counters
    #! answers only sinks 0-1" finding that a wire capture refuted (2026-07-30).
    for m in re.finditer(r"CMD_GET_COUNTERS[ \t]*:[ \t]*begin", src):
        i = m.start()
        nxt = re.search(r"\n[ \t]+(?:CMD_[A-Z0-9_]+|default)[ \t]*:",
                        src[i + 18:])
        blk = src[i:i + 18 + nxt.start()] if nxt else src[i:]
        if "w_gs_type" in blk:
            return blk
    raise AssertionError("no CMD_GET_COUNTERS arm in the response builder "
                         "decodes w_gs_type - the responder is gone")


def _get_counters_arm(src: str, descriptor: str) -> str:
    """The one `if (w_gs_type == DESC_<descriptor> ...)` arm INSIDE
    CMD_GET_COUNTERS, so a mask assertion is anchored to its own descriptor."""
    blk = _get_counters_block(src)
    arms = re.split(r"\n[ \t]*(?:end\s*)?else if \(|\n[ \t]*if \(", blk)[1:]
    want = f"DESC_{descriptor.upper()}"
    for a in arms:
        if want in a.split("begin")[0]:
            return a
    raise AssertionError(
        f"CMD_GET_COUNTERS has no arm for {want}; the descriptors it names are "
        f"{sorted(set(re.findall(r'DESC_[A-Z_]+', blk)))}")


def _assert_arm_mask(descriptor, mask):
    src = open(BUILDER).read()
    arm = _get_counters_arm(src, descriptor)
    n = int(mask, 0)
    assert re.search(rf"const_q\[3\]\s*<=\s*8'h{n:02X}\s*;", arm, re.I), (
        f"the CMD_GET_COUNTERS arm for DESC_{descriptor.upper()} does not emit "
        f"mask {mask}.  The arm is:\n{arm[:600]}")
    return arm


@then("KL_aecp_response_builder serves Stream Output mask {mask}")
def step_cc_rtl_out_mask(context, mask):
    _assert_arm_mask("stream_output", mask)
    assert tc.MILAN_OUTPUT_MASK == int(mask, 0), (
        f"the RTL emits {mask} but Milan Table 5.4 wants "
        f"{tc.MILAN_OUTPUT_MASK:#04x}; if the RTL changed, this contract and "
        f"the table have to be revisited together")


@then("KL_aecp_response_builder serves AVB_INTERFACE mask {mask}")
def step_cc_rtl_iface_mask(context, mask):
    _assert_arm_mask("avb_interface", mask)
    assert tc.AVB_INTERFACE_EXPECT_MASK == int(mask, 0)


@then("KL_aecp_response_builder serves the Stream Input mandatory mask")
def step_cc_rtl_in_mask(context):
    src = open(BUILDER).read()
    arm = _get_counters_arm(src, "stream_input")
    m = re.search(r"load_input_counters_consts", arm)
    assert m, ("the CMD_GET_COUNTERS STREAM_INPUT arm does not call the "
               "per-sink counter loader")
    # The mask lives in the TASK the arm calls, so follow it there.  The mandatory
    # ten (0xF3F) or the full twelve (0xFFF) both satisfy Milan 5.3.8.10;
    # anything narrower drops the badge on that index.
    task = src[src.index("task automatic load_input_counters_consts"):]
    task = task[:task.index("endtask")]
    hit = re.search(r"const_q\[2\]\s*<=\s*8'h0(F|F)\s*;.*?"
                    r"const_q\[3\]\s*<=\s*8'h(3F|FF)\s*;", task,
                    re.I | re.S)
    assert hit, (
        "load_input_counters_consts no longer loads the Milan mandatory "
        "STREAM_INPUT mask (0xF3F) or the full 1722.1 twelve (0xFFF); Milan "
        f"v1.2 5.3.8.10 keeps all ten of Table 5.6 'for each Stream Input'. "
        f"The task body is:\n{task[:600]}")
    got = int(f"0{hit.group(1)}{hit.group(2)}", 16)
    assert got in (tc.MILAN_INPUT_MANDATORY_MASK, tc.MILAN_INPUT_FULL_MASK), (
        f"the loader emits mask {got:#05x}, which is neither the Milan "
        f"mandatory {tc.MILAN_INPUT_MANDATORY_MASK:#05x} nor the full "
        f"{tc.MILAN_INPUT_FULL_MASK:#05x}")
    # THE DEAD `or` THAT USED TO BE HERE.  The assertion read
    #     assert re.search(<mask regex>, src) or "load_input_counters_consts" in src
    # three lines after asserting that same substring was present, so the right
    # operand was unconditionally True and the mask regex was dead code: the
    # mask could have been edited to anything and this step would still pass.
    context.cc_in_mask = got


@then("the STREAM_INPUT GET_COUNTERS arm answers every Stream Input the entity "
      "declares")
def step_cc_rtl_in_every_index(context):
    """Milan v1.2 5.3.8.10: "For each Stream Input of the currently set
    Configuration, the PAAD-AE shall keep track of the counters in Table 5.6";
    5.4.2.25 makes GET_COUNTERS mandatory per descriptor. So the index bound must
    follow the DECLARED descriptor set, never a literal.

    SETTLED 2026-07-30 after a source-vs-silicon dispute, by decoding the AECP
    status byte off an inline tap: desc_type 5 idx 2 -> SUCCESS mask 0xFFF,
    idx 4 -> SUCCESS mask 0xF3F. The mechanism is `acc_found` (KL_aecp_accessor's
    descriptor-existence oracle) plus `w_gs_index < n_aaf_sinks_i` splitting the
    AAF sinks from the CRF Media Clock Input so each gets its own mask - there is
    no literal bound in this arm. An earlier round of this step matched a
    `w_gs_index < 16'd2` literal that lives in the SET/GET_STREAM_FORMAT path
    (the `fmt_in*_r` registers under `ifdef AEM_PER_STREAM_FMT), which is a REAL
    but SEPARATE gap tracked on its own.

    METHOD NOTE, because it cost real time: the peer-side controller tool emits
    NO status field, so a payload-only reading cannot distinguish SUCCESS from
    BAD_ARGUMENTS. Confirm any index-serving claim from the wire or a
    status-aware client, and never from a mask value alone.
    """
    src = open(BUILDER).read()
    arm = _get_counters_arm(src, "stream_input")
    literal = re.search(r"w_gs_index\s*<\s*16'd(\d+)", arm.split("begin")[0])
    assert not literal, (
        f"the CMD_GET_COUNTERS STREAM_INPUT arm is bounded by the LITERAL "
        f"{literal.group(0) if literal else ''} instead of the descriptor "
        f"oracle, so every sink at or above it answers BAD_ARGUMENTS - Milan "
        f"5.3.8.10 exempts no Stream Input, the CRF Media Clock Input included.")
    assert re.search(r"DESC_STREAM_INPUT\s*&&\s*acc_found", src), (
        "the STREAM_INPUT counters arms no longer gate on acc_found, the "
        "descriptor-existence oracle that makes the served set equal the "
        "DECLARED set. A narrower gate silently un-serves sinks.")


@then("the per-input STREAM_FORMAT store covers every declared Stream Input")
def step_cc_rtl_per_stream_fmt(context):
    """The SECOND, separate finding in the same file - a real one, and it is not
    the counters arm.

    Milan v1.2 5.5.1.2 makes the Listener's current format the value a bind is
    checked against, and the standing USER directive is that a controller must
    ALWAYS SET_STREAM_FORMAT the listener to the talker's format rather than
    refuse the bind.  Per-input format storage therefore has to exist for every
    declared Stream Input.

    In this builder the per-stream format registers live behind
    ``ifdef AEM_PER_STREAM_FMT``, and the ``else`` arm keeps only inputs 0..1
    (`fmt_in0_r` / `fmt_in1_r`, guarded `w_gs_index < 16'd2`).  If no shipped
    config defines that macro then sinks >= 2 have nowhere to store a format.
    """
    src = open(BUILDER).read()
    if "AEM_PER_STREAM_FMT" not in src:
        return
    fmt_regs = sorted(set(re.findall(r"fmt_in(\d+)_r", src)))
    configs = os.path.join(ROOT, "configs")
    defined = []
    for dirpath, _dirs, files in os.walk(configs):
        for f in files:
            try:
                txt = open(os.path.join(dirpath, f), errors="ignore").read()
            except OSError:
                continue
            if "AEM_PER_STREAM_FMT" in txt:
                defined.append(os.path.relpath(os.path.join(dirpath, f), ROOT))
    assert defined, (
        f"the builder keeps per-input STREAM_FORMAT storage behind "
        f"`ifdef AEM_PER_STREAM_FMT and its else arm defines only "
        f"fmt_in{{{','.join(fmt_regs)}}}_r, yet no file under configs/ defines "
        f"AEM_PER_STREAM_FMT - so every Stream Input above index "
        f"{len(fmt_regs) - 1} has nowhere to store a format.  Milan v1.2 "
        f"5.5.1.2 makes the Listener's current format the value the bind is "
        f"checked against, and the standing directive is that a controller must "
        f"ALWAYS SET_STREAM_FORMAT the listener rather than refuse the bind.")


@then("the register map documents A_STRMW_CNT0..9 as the ten Table 5.6 counters")
def step_cc_regmap_counters(context):
    doc = open(REGMAP).read()
    assert "A_STRMW_CNT0..9" in doc, "the 0x830 window row is gone"
    row = doc[doc.index("A_STRMW_CNT0..9"):][:2000]
    for name in tc.MILAN_TABLE_56:
        assert name in row, f"{name} missing from the A_STRMW_CNT row"


@then("the register map warns that the flat views saturate")
def step_cc_regmap_saturate(context):
    doc = open(REGMAP).read()
    # ANCHORED on the rows it is actually about.  A bare `"saturating" in doc`
    # matched anywhere in a 900-line register map - including rows that have
    # nothing to do with the AVTP RX counters - so the warning could have been
    # deleted from the two rows that need it while an unrelated row kept the
    # step green.
    hits = [ln for ln in doc.splitlines()
            if "saturat" in ln.lower()
            and ("AVTPRX_STAT" in ln or "AVTPRX_ERR" in ln)]
    assert hits, (
        "no AVTPRX_STAT / AVTPRX_ERR row in the register map warns that those "
        "words are SATURATING narrow views of the 32-bit STREAM_INPUT counters "
        "- a bench read of them cannot see a counter past its ceiling, and 0xFF "
        "means 'at least 255', which is how a frozen-looking error counter hid "
        "5.1 M LATE and 4.8 M EARLY timestamps")
    context.cc_saturate_rows = len(hits)
