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


# ------------------------------------ advertised-is-measured (AVTP-5t) ------
CRF_RX = os.path.join(ROOT, "hdl", "ieee1722", "crf", "KL_crf_rx.sv")

@then("a counter is either claimed in the mask and measured, or claimed by "
      "neither")
def step_cc_advertised_is_measured(context):
    # the rule itself, stated against the contract module so a future mask
    # edit cannot quietly re-open the defect on some other descriptor
    assert tc.MILAN_INPUT_MANDATORY_MASK == 0xF3F
    assert len(tc.MILAN_TABLE_56) == 10
    # the mask and the named set must BE the same set - the rule in one line
    assert tc.counters_valid_mask(tc.MILAN_TABLE_56,
                                  tc.IEEE_STREAM_INPUT_BLOCK) \
        == tc.MILAN_INPUT_MANDATORY_MASK
    context.cc_rule = "advertised-is-measured"


@then("the CRF Media Clock Input counters advertised as valid are all backed "
      "by a tally")
def step_cc_crf_no_constants(context):
    # WHERE THIS USED TO READ, and why it moved. The subject was the AECP
    # response builder's load_crf_input_counters_consts task: it advertised a
    # valid mask and, for five of the bits, wrote nothing into the payload -
    # a SERVED CONSTANT ZERO (traceability AVTP-5t). hdl/ieee17221/aecp/** is
    # deleted, so there is no loader left to catch. What the defect was really
    # about survives untouched: whether the ENGINE keeps a tally at all. A
    # counter with no register behind it is a constant zero however it is
    # served, so the rule is now resolved out of KL_crf_rx directly.
    src = open(CRF_RX).read()
    unbacked = []
    for name in tc.MILAN_TABLE_56:
        reg = CRF_COUNTER_REG[name]
        if not re.search(r"\b%s\s*<=\s*%s\s*\+" % (re.escape(reg),
                                                    re.escape(reg)), src):
            unbacked.append(f"{name}: KL_crf_rx never increments {reg}, so the "
                            f"Milan mandatory mask claims a counter that can "
                            f"only ever read zero")
    assert not unbacked, (
        "the CRF Media Clock Input advertises counters it does not measure "
        "(traceability AVTP-5t) - a claimed constant is worse than an "
        "unclaimed bit:\n  " + "\n  ".join(unbacked))


@then("the CRF Media Clock Input applies the {law} law to {counter}")
def step_cc_crf_law(context, law, counter):
    """The law is per counter, not per descriptor: KL_crf_rx must commit the
    per-interval ones on its Table 5.6 tick and the per-event ones at the PDU.
    """
    src = open(CRF_RX).read()
    sig = {
        "MEDIA_RESET":         ("iv_mr_r", "mr_cnt_o"),
        "TIMESTAMP_UNCERTAIN": ("iv_tu_r", "tu_cnt_o"),
        "LATE_TIMESTAMP":      ("iv_lt_r", "late_cnt_o"),
        "EARLY_TIMESTAMP":     ("iv_et_r", "early_cnt_o"),
        "STREAM_INTERRUPTED":  (None,      "cnt_intr_o"),
    }[counter]
    flag, cnt = sig
    assert f"{cnt}" in src, f"KL_crf_rx keeps no {counter} tally ({cnt})"
    # the interval commit block is the one guarded by the registered tick
    tick = src[src.index("if (iv_tick_r) begin"):]
    tick = tick[:tick.index("end else begin")]
    if law == "per-interval":
        assert flag and re.search(r"if \(%s\s*\|\|" % flag, tick), (
            f"{counter} is not committed on the observation-interval tick; "
            f"Milan v1.2 Table 5.6 says 'at the end of every observation "
            f"interval during which ...'")
        assert cnt in tick
    else:
        assert cnt not in tick, (
            f"{counter} is folded into the observation-interval commit; "
            f"Table 5.6 says 'incremented each time ...', which is per event")
        # the per-event increment may share its guard with the Table 5.22
        # dirty pulse (gh #60 F2), so a begin block is as lawful as the
        # bare statement - the LAW is the guard, not the block style
        assert re.search(r"if \(w_ev_si_w\)(?:\s*begin)?\s*%s\s*<=" % cnt,
                         src), (
            f"{counter} has no per-event increment in KL_crf_rx")


#! The KL_crf_rx register that carries each Table 5.6 symbol. The era wipe is
#! judged against THIS set, not against whatever the block happens to clear:
#! a counter missing from the wipe is a counter that survives its own era.
CRF_COUNTER_REG = {
    "MEDIA_LOCKED":        "cnt_locked_o",
    "MEDIA_UNLOCKED":      "cnt_unlocked_o",
    "STREAM_INTERRUPTED":  "cnt_intr_o",
    "SEQ_NUM_MISMATCH":    "seq_err_o",
    "MEDIA_RESET":         "mr_cnt_o",
    "TIMESTAMP_UNCERTAIN": "tu_cnt_o",
    "UNSUPPORTED_FORMAT":  "fmt_err_o",
    "LATE_TIMESTAMP":      "late_cnt_o",
    "EARLY_TIMESTAMP":     "early_cnt_o",
    "FRAMES_RX":           "pdu_count_o",
}


def _crf_bind_block():
    """The body of KL_crf_rx's `if (w_bind_rise_w)` arm - the era wipe."""
    src = open(CRF_RX).read()
    key = "if (w_bind_rise_w) begin"
    assert key in src, (
        "KL_crf_rx has no bind-edge arm at all; Milan v1.2 5.3.8.10 requires "
        "one to reset the Table 5.6 counters on not-bound -> bound")
    body = src[src.index(key) + len(key):]
    # no nested begin/end in this arm, so the first dedented `end` closes it
    return src, body[:body.index("\n      end")]


@then("the CRF Media Clock Input zeroes all ten counters on the bind edge")
def step_cc_crf_era_wipe(context):
    src, body = _crf_bind_block()
    survivors = []
    for name in tc.MILAN_TABLE_56:
        reg = CRF_COUNTER_REG[name]
        if not re.search(r"\b%s\s*<=\s*'0\s*;" % re.escape(reg), body):
            survivors.append(f"{name} ({reg})")
    assert not survivors, (
        "these Table 5.6 counters survive a bind edge in KL_crf_rx, so a new "
        "binding inherits a dead era's totals (Milan v1.2 5.3.8.10 'shall "
        "reset all of these counters to zero'):\n  " + "\n  ".join(survivors))
    # the observation-interval SEEN flags belong to the dead era too: one left
    # standing commits +1 into a just-zeroed counter at the very next tick
    stale = [f for f in ("iv_frx_r", "iv_uf_r", "iv_sm_r", "iv_mr_r",
                         "iv_tu_r", "iv_lt_r", "iv_et_r")
             if not re.search(r"\b%s\s*<=\s*1'b0\s*;" % f, body)]
    assert not stale, (
        "interval seen flags left standing across the era wipe, each good for "
        "one phantom event in the new binding: " + ", ".join(stale))


@then("the CRF Media Clock Input era wipe fires on the bind edge only")
def step_cc_crf_era_edge(context):
    src, _ = _crf_bind_block()
    m = re.search(r"wire\s+w_bind_rise_w\s*=\s*([^;]+);", src)
    assert m, "KL_crf_rx no longer derives the bind edge"
    expr = " ".join(m.group(1).split())
    assert expr == "en_i && !en_q", (
        f"the era wipe triggers on `{expr}`. Milan v1.2 5.3.8.10 wipes on the "
        f"RISING edge only - 'the PAAD-AE does not reset these counters when "
        f"the Stream Input changes its state from bound to not bound', so an "
        f"`!en_i` or `en_i != en_q` term destroys the evidence of whatever "
        f"fault caused the unbind")


@then("the CRF Media Clock Input bind edge drops media lock without scoring "
      "an unlock")
def step_cc_crf_era_lock(context):
    src, body = _crf_bind_block()
    assert re.search(r"\blocked_o\s*<=\s*1'b0\s*;", body), (
        "the bind edge zeroes MEDIA_LOCKED/MEDIA_UNLOCKED but leaves locked_o "
        "set: Table 5.6 reads the zeroed pair as 'not synchronized on the "
        "media clock', which contradicts a sink that still claims lock")
    # and the drop must not walk +1 into the zeroed MEDIA_UNLOCKED
    assert not re.search(r"cnt_unlocked_o\s*<=\s*cnt_unlocked_o", body), (
        "the bind edge increments MEDIA_UNLOCKED, stranding the sink at "
        "MEDIA_UNLOCKED = MEDIA_LOCKED + 1 - neither of the two states Table "
        "5.6 allows")
    # the wipe must be the LAST writer of locked_o in the engine block, so a
    # timeout unlock landing in the same cycle cannot outrank it
    tail = src[src.index("if (w_bind_rise_w) begin"):]
    assert "locked_o" not in tail[tail.index("\n      end"):], (
        "something writes locked_o after the era wipe in KL_crf_rx; the wipe "
        "has to be the last writer or a same-cycle timeout unlock outranks it")


# ------------------------------------------------------- L1 fabric bindings --
# The KL_aecp_response_builder mask-serving steps that lived here are gone with
# hdl/ieee17221/aecp/**: this device answers no AECP command, so there is no
# GET_COUNTERS arm to anchor a mask assertion on. The documented register
# window below is the surviving fabric path to the same ten values.
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


# --------------------------------------------------- the per-counter law --
# The update law is the answer to "WHEN does this counter move?", and Milan
# Table 5.6 answers it in two grammars while IEEE 1722.1-2021 Table 7-157 uses
# a third.  These steps hold the RTL's behaviour and the bench grader to ONE
# table, in tb/tools/torture_campaign.py, so the feature file and the on-bench
# runner cannot drift apart about what a counter means.
@then("every Stream Input counter has an update law")
def step_cc_law_total(context):
    missing = [n for n in tc.IEEE_STREAM_INPUT_BLOCK
               if tc.counter_law(n) is None]
    assert not missing, f"no update law stated for {missing}"
    assert len(tc.STREAM_INPUT_COUNTER_LAW) == len(tc.IEEE_STREAM_INPUT_BLOCK)


@then('the update laws in use are "{laws}"')
def step_cc_law_kinds(context, laws):
    want = sorted(s.strip() for s in laws.split(","))
    got = sorted({v[0] for v in tc.STREAM_INPUT_COUNTER_LAW.values()})
    assert got == want, f"{got} != {want}"


@then("the update law of {counter} is {law} per {clause}")
def step_cc_law_one(context, counter, law, clause):
    got = tc.counter_law(counter)
    assert got is not None, f"{counter} has no stated update law"
    assert got[0] == law, f"{counter}: law is {got[0]}, not {law}"
    assert got[1] == clause, f"{counter}: clause is {got[1]!r}, not {clause!r}"


@then('the trigger for {counter} mentions "{phrase}"')
def step_cc_law_trigger(context, counter, phrase):
    got = tc.counter_law(counter)
    assert got is not None, f"{counter} has no stated update law"
    assert phrase in got[2], (
        f"{counter} trigger is {got[2]!r}, which does not mention {phrase!r} - "
        f"a counter can have the right update law and still watch the wrong "
        f"signal")


# ------------------------------------------- the interval-ceiling contract --
def _cc_window(context):
    if not hasattr(context, "cc_before"):
        context.cc_before, context.cc_after = {}, {}
    return context.cc_before, context.cc_after


@given("a stream input window where {counter} advanced by {delta:d}")
def step_cc_window_open(context, counter, delta):
    context.cc_before, context.cc_after = {}, {}
    context.cc_before[counter] = 0
    context.cc_after[counter] = delta
    context.cc_window_s = 30.0


@given("{counter} advanced by {delta:d} in that window")
def step_cc_window_add(context, counter, delta):
    before, after = _cc_window(context)
    before[counter] = 0
    after[counter] = delta


@then("the interval-ceiling verdict is {verdict}")
def step_cc_ceiling(context, verdict):
    got, detail = tc.check_interval_ceiling(
        context.cc_before, context.cc_after,
        window_s=getattr(context, "cc_window_s", 30.0))
    context.cc_ceiling_detail = detail
    assert got == verdict, f"{got} != {verdict}: {detail}"


@then("the interval-ceiling offender is {counter}")
def step_cc_ceiling_offender(context, counter):
    names = [o["counter"] for o in context.cc_ceiling_detail.get("offenders", [])]
    assert names == [counter], f"{names} != [{counter}]"


@given("{counter} advanced by {delta:d} over {window:d} seconds with the "
       "stream flowing")
def step_cc_sem_given(context, counter, delta, window):
    context.cc_sem = tc.grade_counter_semantics(
        counter, delta, float(window), stream_flowing=True)


@then("the semantics verdict is {verdict} and the reading is {reading}")
def step_cc_sem_then(context, verdict, reading):
    got, detail = context.cc_sem
    assert got == verdict, f"{got} != {verdict}: {detail}"
    assert detail.get("reading") == reading, \
        f"reading {detail.get('reading')!r} != {reading!r}: {detail}"
    assert detail.get("clause"), "a semantics grade must name its clause"
