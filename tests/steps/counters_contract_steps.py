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

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, then, when

if TYPE_CHECKING:
    # ANNOTATION-ONLY. `from __future__ import annotations` leaves every
    # signature below an unevaluated string, so this module imports at run time
    # exactly what it imported before the annotations existed - behave's own
    # internals are never reached for a type name.
    from behave.runner import Context

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tb" / "tools"))

import torture_campaign as tc  # noqa: E402

REGMAP = ROOT / "docs" / "reference" / "REGISTER_MAP.md"


def _regmap_text():
    """The register map's text, read and closed."""
    return REGMAP.read_text()


@given("the counters contract is importable")
def step_cc_import(context: Context) -> None:
    """Every table, mask and invariant below resolves out of the module the
    on-bench runner decodes real responses with, so the two cannot drift.
    """
    assert hasattr(tc, "MILAN_TABLE_56"), "torture_campaign tables missing"
    context.cc = tc
    context.cc_decoded = {}
    context.cc_payload = None


# ------------------------------------------------------------------- tables --
@then("the Milan Stream Input counter set has {n:d} members")
def step_cc_t56_len(context: Context, n: int) -> None:
    """Table 5.6 is a CLOSED set: a member gained or lost silently changes the
    mandatory mask every other step here is measured against.
    """
    assert len(tc.MILAN_TABLE_56) == n, tc.MILAN_TABLE_56


@then("the Milan Stream Input counter set is")
def step_cc_t56_names(context: Context) -> None:
    """The set in ORDER, because the order is 1722.1 block order: a name's
    position in this list is the block offset a decoder will read it from.
    """
    want = [r["counter"] for r in context.table]
    assert list(tc.MILAN_TABLE_56) == want, \
        f"{tc.MILAN_TABLE_56} != {want}"


@then("the Milan Stream Input mandatory wire mask is {mask}")
def step_cc_t56_mask(context: Context, mask: str) -> None:
    """The mask is DERIVED from the named set against the IEEE block and must
    equal the recorded constant - a hand-typed mask that drifts from its own
    table is exactly the defect.
    """
    m = tc.counters_valid_mask(tc.MILAN_TABLE_56, tc.IEEE_STREAM_INPUT_BLOCK)
    assert m == int(mask, 0) == tc.MILAN_INPUT_MANDATORY_MASK, \
        f"{m:#05x} != {mask}"


@then("the Milan Stream Output counter set has {n:d} members")
def step_cc_t54_len(context: Context, n: int) -> None:
    """Table 5.4's five, against 1722.1 Table 7-159's eight - the count is the
    first thing that tells the two Stream Output layouts apart.
    """
    assert len(tc.MILAN_TABLE_54) == n, tc.MILAN_TABLE_54


@then("the Milan Stream Output wire mask is {mask}")
def step_cc_t54_mask(context: Context, mask: str) -> None:
    """Table 5.4 packs its five densely, so the Milan output mask is its own
    layout's FULL mask - resolved against itself, not against the IEEE block.
    """
    assert tc.MILAN_OUTPUT_MASK == int(mask, 0)
    assert tc.counters_valid_mask(tc.MILAN_TABLE_54,
                                 tc.MILAN_TABLE_54) == int(mask, 0)


@then("the Milan Stream Output counter set is")
def step_cc_t54_names(context: Context) -> None:
    """The five in Milan layout order, which is the order trap 2 is about."""
    want = [r["counter"] for r in context.table]
    assert list(tc.MILAN_TABLE_54) == want, f"{tc.MILAN_TABLE_54} != {want}"


@then("the IEEE Stream Input block has {n:d} members")
def step_cc_ieee_len(context: Context, n: int) -> None:
    """Twelve, not ten: the IEEE block adds the two tv tallies Milan's Table
    5.16 mask deliberately skips.
    """
    assert len(tc.IEEE_STREAM_INPUT_BLOCK) == n


@then("the IEEE Stream Input full wire mask is {mask}")
def step_cc_ieee_mask(context: Context, mask: str) -> None:
    """The full block's mask, so the two bits between it and the Milan
    mandatory mask are the tv pair and nothing else.
    """
    assert tc.MILAN_INPUT_FULL_MASK == int(mask, 0)
    assert tc.counters_valid_mask(tc.IEEE_STREAM_INPUT_BLOCK,
                                 tc.IEEE_STREAM_INPUT_BLOCK) == int(mask, 0)


@then("{name} is at block offset {off:d}")
def step_cc_offset(context: Context, name: str, off: int) -> None:
    """A counter's slot times four IS its counters_block byte offset; a reader
    off by one slot reports the neighbouring counter's value under this name.
    """
    got = tc.IEEE_STREAM_INPUT_BLOCK.index(name) * 4
    assert got == off, f"{name} is at offset {got}, expected {off}"


# --------------------------------------------------------- trap 1: numbering --
@then("the IEEE table bit number for block offset {off:d} is {bit:d}")
def step_cc_bitnum(context: Context, off: int, bit: int) -> None:
    """Trap 1: Table 7-156's bit number is 31 - offset/4, MSB-first, while the
    wire mask is 1 << offset/4. Reading the table literally inverts every mask.
    """
    got = tc.counters_valid_bit_ieee(off)
    assert got == bit, f"offset {off} -> table bit {got}, expected {bit}"


@then("a block offset that is not quadlet aligned is refused")
def step_cc_bitnum_refuse(context: Context) -> None:
    """The counters_block is quadlets, so an unaligned offset is a caller bug
    and must raise rather than floor quietly into the slot below it.
    """
    try:
        tc.counters_valid_bit_ieee(3)
    except ValueError:
        return
    raise AssertionError("an unaligned offset was accepted")


@then("the table bit number {bit:d} corresponds to wire mask {mask}")
def step_cc_bit_to_mask(context: Context, bit: int, mask: str) -> None:
    """The table-bit/wire-mask correspondence, closed as a ROUND TRIP through
    the production conversion so an inverted mapping cannot pass.
    """
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
def step_cc_milan_slot(context: Context, name: str, n: int) -> None:
    """Half of trap 2: where Milan Table 5.4 puts the name."""
    assert tc.MILAN_TABLE_54.index(name) == n


@then("in the IEEE layout {name} is at slot {n:d}")
def step_cc_ieee_slot(context: Context, name: str, n: int) -> None:
    """The other half: where 1722.1 Table 7-159 puts the SAME name. The two
    slots differing is what makes a wrong-layout decode silently plausible.
    """
    assert tc.IEEE_STREAM_OUTPUT_BLOCK.index(name) == n


@then("decoding a Milan Stream Output block with the IEEE layout mislabels "
      "FRAMES_TX")
def step_cc_mislabel(context: Context) -> None:
    """Picking the wrong Stream Output layout does not fail, it LIES: this
    device's FRAMES_TX arrives at the controller as TIMESTAMP_UNCERTAIN.
    """
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
def step_cc_payload(context: Context, dt: int, di: int, mask: str) -> None:
    """A well-formed response body. Every one of the 32 slots carries its own
    index plus one, so a value read from the wrong slot names the slot it came
    from instead of looking like a plausible count.
    """
    pay = bytearray(8 + 128)
    pay[0:2] = dt.to_bytes(2, "big")
    pay[2:4] = di.to_bytes(2, "big")
    pay[4:8] = int(mask, 0).to_bytes(4, "big")
    for i in range(32):
        pay[8 + 4 * i:12 + 4 * i] = (i + 1).to_bytes(4, "big")
    context.cc_payload = bytes(pay)


@given("a GET_COUNTERS payload truncated to {n:d} octets")
def step_cc_payload_short(context: Context, n: int) -> None:
    """Short of the 8-octet header plus the 128-octet block, which is the shape
    a cut-off or misparsed AECPDU hands the decoder.
    """
    context.cc_payload = b"\x00" * n


@then("decoding it raises")
def step_cc_decode_raises(context: Context) -> None:
    """A truncated payload must raise rather than half-decode: counters read
    past the end of a short buffer are worse than no counters at all.
    """
    try:
        tc.decode_counters_payload(context.cc_payload,
                                   tc.IEEE_STREAM_INPUT_BLOCK)
    except ValueError:
        return
    raise AssertionError("a truncated payload decoded without complaint")


@when("the contract decodes it as a Stream Input block")
def step_cc_decode_then(context: Context) -> None:
    """Runs the production decode - the same call the bench runner makes on a
    real GET_COUNTERS response.
    """
    context.cc_decoded = tc.decode_counters_payload(
        context.cc_payload, tc.IEEE_STREAM_INPUT_BLOCK)


@then("the decode reports claimed-but-unnamed slot {slot:d}")
def step_cc_unnamed(context: Context, slot: int) -> None:
    """A slot the mask claims but the layout cannot name is REPORTED, not
    dropped: an entity-specific claim is evidence about the device, not noise.
    """
    d = context.cc_decoded
    assert slot in d["claimed_but_unnamed_slots"], d


@then("the decode names only {name}")
def step_cc_only(context: Context, name: str) -> None:
    """Methodology R5: an unclaimed counter is ABSENT from the decode. A
    structural zero is indistinguishable from a healthy idle measurement.
    """
    d = context.cc_decoded
    assert list(d["decoded"]) == [name], d["decoded"]


# ------------------------------------------------------------- the invariants --
@given("MEDIA_LOCKED {a:d} and MEDIA_UNLOCKED {b:d}")
def step_cc_lock(context: Context, a: int, b: int) -> None:
    """Grades one MEDIA_LOCKED/MEDIA_UNLOCKED pair; Table 5.6 admits exactly
    two relations between them and nothing else.
    """
    context.cc_lock = tc.check_lock_invariant(
        {"MEDIA_LOCKED": a, "MEDIA_UNLOCKED": b})


@then("the lock invariant verdict is {want}")
def step_cc_lock_verdict(context: Context, want: str) -> None:
    """PASS for the two legal states, FAIL for any other difference."""
    assert context.cc_lock[0] == want, context.cc_lock


@then("the lock invariant reports the stream synchronized")
def step_cc_lock_sync(context: Context) -> None:
    """locked == unlocked + 1 is a lock STATE readout, not merely a consistency
    check, so a runner can use the pair instead of inventing a lock flag.
    """
    assert context.cc_lock[1]["synchronized"] is True, context.cc_lock


@then("the lock invariant reports the stream not synchronized")
def step_cc_lock_nosync(context: Context) -> None:
    """The other legal state, equal counts - the sink is not on the media
    clock, and that is a reading rather than a failure.
    """
    assert context.cc_lock[1]["synchronized"] is False, context.cc_lock


@given("STREAM_START {a:d} and STREAM_STOP {b:d}")
def step_cc_talker(context: Context, a: int, b: int) -> None:
    """Table 5.4's talker pair, which admits the same two relations: streaming
    now, or stopped.
    """
    context.cc_talker = tc.check_talker_invariant(
        {"STREAM_START": a, "STREAM_STOP": b})


@then("the talker invariant verdict is {want}")
def step_cc_talker_verdict(context: Context, want: str) -> None:
    """A start count behind its stop count, or ahead by more than one, is a
    talker that lost an event.
    """
    assert context.cc_talker[0] == want, context.cc_talker


@given("TIMESTAMP_VALID {tv:d} TIMESTAMP_NOT_VALID {tnv:d} FRAMES_RX {frx:d}")
def step_cc_tvtnv(context: Context, tv: int, tnv: int, frx: int) -> None:
    """The trap-3 triple: TV + TNV == FRAMES_RX is a 1722.1 identity, so the
    model must infer WHICH reading is in force before it grades anything.
    """
    context.cc_tv = tc.check_tv_tnv({"TIMESTAMP_VALID": tv,
                                     "TIMESTAMP_NOT_VALID": tnv,
                                     "FRAMES_RX": frx})


@then("the tv-tnv verdict is {want}")
def step_cc_tv_verdict(context: Context, want: str) -> None:
    """PASS under the per-frame identity, INFO under the Milan interval
    reading, FAIL only where neither reading can hold.
    """
    assert context.cc_tv[0] == want, context.cc_tv


@then('the reading in force is "{reading}"')
def step_cc_tv_reading(context: Context, reading: str) -> None:
    """The check must NAME the reading it concluded: asserting the 1722.1
    identity against a Milan interval counter files conformance as an 8000x
    defect.
    """
    assert context.cc_tv[1]["reading"] == reading, context.cc_tv


@then("the tv-tnv skip says the block was reset at the bind")
def step_cc_tv_vacuous(context: Context) -> None:
    """All three at zero is the state 5.3.8.10 guarantees straight after a
    bind, and it was the only state this check was ever called in - so the skip
    has to cite the clause rather than announce a reading from zero samples.
    """
    why = context.cc_tv[1].get("why", "")
    assert "5.3.8.10" in why and "vacuous" in why, why


@given("{counter} reads {before:d} then {after:d}")
def step_cc_growth(context: Context, counter: str, before: int,
                   after: int) -> None:
    """One error counter sampled twice across a 4 s window - the shape the
    bench runner produces from two GET_COUNTERS reads.
    """
    context.cc_growth = tc.check_no_growth({counter: before},
                                           {counter: after}, (counter,),
                                           window_s=4.0)


@given("{counter} is not claimed by the mask")
def step_cc_growth_unclaimed(context: Context, counter: str) -> None:
    """A counter absent from both snapshots was never measured, so no window
    over it can be a clean pass.
    """
    context.cc_growth = tc.check_no_growth({}, {}, (counter,), window_s=4.0)


@then("the growth verdict is {want}")
def step_cc_growth_verdict(context: Context, want: str) -> None:
    """These are VERDICTS. Emitted as INFO they contributed nothing to the exit
    code, and a board discarding 296 294 of 296 294 frames passed green.
    """
    assert context.cc_growth[0] == want, context.cc_growth


@given("a measured frames rate of {rate:f} per second")
def step_cc_rate(context: Context, rate: float) -> None:
    """Classifies a measured FRAMES_RX rate into a reading band, keeping the
    band's own explanation for the steps below.
    """
    context.cc_reading = tc.frames_rate_reading(rate)
    context.cc_rate = context.cc_reading["band"]


@then("the rate is consistent with the {reading} reading")
def step_cc_rate_band(context: Context, reading: str) -> None:
    """The clause bounds the interval from ABOVE only, so 200/s is a lawful
    5 ms interval; an earlier table called it the defect and a unit test
    cemented that.
    """
    assert context.cc_rate == reading, \
        f"classified as {context.cc_rate}, expected {reading} " \
        f"({context.cc_reading['why']})"


@then("the implied observation interval is {secs:f} seconds")
def step_cc_rate_interval(context: Context, secs: float) -> None:
    """The interval a rate implies is reported as a number, so a reader can
    hold it against the one-second ceiling instead of trusting the band.
    """
    got = context.cc_reading["implied_interval_s"]
    assert got is not None and abs(got - secs) < 1e-9, \
        f"implied interval {got}, expected {secs}"


@then("the reading refusal cites the 1 second ceiling")
def step_cc_rate_ceiling(context: Context) -> None:
    """An interval over one second is the ONLY non-conformant interval, so the
    refusal must name that ceiling rather than merely landing on "neither".
    """
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
def step_cc_plan_inputs(context: Context) -> None:
    """EVERY index, not index 0: the 0x800 window makes index 0 a hard alias of
    the flat registers, so an index-0 pass exercises the alias path only.
    """
    _plan(context)
    assert context.cc_cov["dut_listener"] == tc.ARTY.listener_indices(), \
        context.cc_cov


@then("the campaign plan asks for counters on every Stream Output index")
def step_cc_plan_outputs(context: Context) -> None:
    """The talker direction of the same coverage rule."""
    _plan(context)
    assert context.cc_cov["dut_talker"] == tc.ARTY.talker_indices(), \
        context.cc_cov


@then("the campaign plan includes the CRF Media Clock indices")
def step_cc_plan_crf(context: Context) -> None:
    """The CRF pair are Stream descriptors like any other and owe GET_COUNTERS
    like any other; they are the two most often left out of a sweep.
    """
    _plan(context)
    assert tc.ARTY.crf_out in context.cc_cov["dut_talker"]
    assert tc.ARTY.crf_in in context.cc_cov["dut_listener"]


@then("the CRF Media Clock Input index is in the plan's listener coverage")
def step_cc_plan_crf_in(context: Context) -> None:
    """Named on its own because the CRF sink is the descriptor the rest of this
    feature's L1 steps hold KL_crf_rx to.
    """
    _plan(context)
    assert tc.ARTY.crf_in in context.cc_cov["dut_listener"], context.cc_cov


@then("the mandatory mask required of it is {mask}")
def step_cc_crf_mask(context: Context, mask: str) -> None:
    """The CRF Media Clock Input is a Stream Input, so Table 5.16's mandatory
    mask applies to it unchanged - no reduced set for a clock-only sink.
    """
    assert tc.MILAN_INPUT_MANDATORY_MASK == int(mask, 0)


# ------------------------------------ advertised-is-measured (AVTP-5t) ------
CRF_RX = ROOT / "hdl" / "ieee1722" / "crf" / "KL_crf_rx.sv"


def _crf_rx_source():
    """KL_crf_rx.sv's text, read and closed."""
    return CRF_RX.read_text()


@then("a counter is either claimed in the mask and measured, or claimed by "
      "neither")
def step_cc_advertised_is_measured(context: Context) -> None:
    """The rule in one line: the mandatory mask and the named set must BE the
    same set, stated against the contract module so no later mask edit can
    re-open the defect on a different descriptor.
    """
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
def step_cc_crf_no_constants(context: Context) -> None:
    """AVTP-5t: a counter with no register incrementing behind it is a served
    constant zero however it reaches the wire, so the tally is looked for in
    KL_crf_rx rather than in whatever serves the response.
    """
    # WHERE THIS USED TO READ, and why it moved. The subject was the AECP
    # response builder's load_crf_input_counters_consts task: it advertised a
    # valid mask and, for five of the bits, wrote nothing into the payload -
    # a SERVED CONSTANT ZERO (traceability AVTP-5t). hdl/ieee17221/aecp/** is
    # deleted, so there is no loader left to catch. What the defect was really
    # about survives untouched: whether the ENGINE keeps a tally at all. A
    # counter with no register behind it is a constant zero however it is
    # served, so the rule is now resolved out of KL_crf_rx directly.
    src = _crf_rx_source()
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
def step_cc_crf_law(context: Context, law: str, counter: str) -> None:
    """The law is per counter, not per descriptor: KL_crf_rx must commit the
    per-interval ones on its Table 5.6 tick and the per-event ones at the PDU.
    """
    src = _crf_rx_source()
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
    src = _crf_rx_source()
    key = "if (w_bind_rise_w) begin"
    assert key in src, (
        "KL_crf_rx has no bind-edge arm at all; Milan v1.2 5.3.8.10 requires "
        "one to reset the Table 5.6 counters on not-bound -> bound")
    body = src[src.index(key) + len(key):]
    # no nested begin/end in this arm, so the first dedented `end` closes it
    return src, body[:body.index("\n      end")]


@then("the CRF Media Clock Input zeroes all ten counters on the bind edge")
def step_cc_crf_era_wipe(context: Context) -> None:
    """5.3.8.10's era wipe, judged against all ten registers AND the interval
    seen flags: a flag left standing across the wipe is worth one phantom event
    in the new binding at the very next tick.
    """
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
def step_cc_crf_era_edge(context: Context) -> None:
    """The wipe triggers on the RISING edge alone. An `!en_i` or `en_i != en_q`
    term would destroy the evidence of whatever fault caused the unbind.
    """
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
def step_cc_crf_era_lock(context: Context) -> None:
    """The wipe must also drop locked_o, must not walk +1 into the zeroed
    MEDIA_UNLOCKED, and must be the LAST writer of locked_o - otherwise a
    same-cycle timeout unlock outranks it and the new era starts already lying.
    """
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
# The repository-local response builder was deleted, but the protocol processor
# now serves GET_COUNTERS through KL_pp_shadow's root gather face. Wire-format
# and descriptor-index checks live in the pp_shadow and milan_dp harnesses. The
# step below independently pins the documented fabric register path to the same
# ten Stream Input values.
@then("the register map documents A_STRMW_CNT0..9 as the ten Table 5.6 counters")
def step_cc_regmap_counters(context: Context) -> None:
    """The documented 0x830 window and the contract must name the SAME ten
    counters, so a bench read of the register path lands where the clause says.
    """
    doc = _regmap_text()
    assert "A_STRMW_CNT0..9" in doc, "the 0x830 window row is gone"
    row = doc[doc.index("A_STRMW_CNT0..9"):][:2000]
    for name in tc.MILAN_TABLE_56:
        assert name in row, f"{name} missing from the A_STRMW_CNT row"


@then("the register map warns that the flat views saturate")
def step_cc_regmap_saturate(context: Context) -> None:
    """The narrow AVTPRX views saturate, and the map has to say so: 0xFF means
    "at least 255", which is how a frozen-looking error counter hid 5.1 M LATE
    and 4.8 M EARLY timestamps.
    """
    doc = _regmap_text()
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
def step_cc_law_total(context: Context) -> None:
    """No counter may be silent about when it moves - the law table has to
    cover the block exactly, with no spare entries and no gaps.
    """
    missing = [n for n in tc.IEEE_STREAM_INPUT_BLOCK
               if tc.counter_law(n) is None]
    assert not missing, f"no update law stated for {missing}"
    assert len(tc.STREAM_INPUT_COUNTER_LAW) == len(tc.IEEE_STREAM_INPUT_BLOCK)


@then('the update laws in use are "{laws}"')
def step_cc_law_kinds(context: Context, laws: str) -> None:
    """There are exactly three grammars, and the grammar IS the requirement:
    "each time", "at the end of every observation interval", "on receipt of".
    """
    want = sorted(s.strip() for s in laws.split(","))
    got = sorted({v[0] for v in tc.STREAM_INPUT_COUNTER_LAW.values()})
    assert got == want, f"{got} != {want}"


@then("the update law of {counter} is {law} per {clause}")
def step_cc_law_one(context: Context, counter: str, law: str,
                    clause: str) -> None:
    """One counter's law AND the clause that fixes it, because the two tv
    tallies are governed by 1722.1 alone - Milan never defined them.
    """
    got = tc.counter_law(counter)
    assert got is not None, f"{counter} has no stated update law"
    assert got[0] == law, f"{counter}: law is {got[0]}, not {law}"
    assert got[1] == clause, f"{counter}: clause is {got[1]!r}, not {clause!r}"


@then('the trigger for {counter} mentions "{phrase}"')
def step_cc_law_trigger(context: Context, counter: str, phrase: str) -> None:
    """A counter can have the right update law and still watch the wrong
    signal: MEDIA_RESET counted a local I2S buffer rail no clause mentions.
    """
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
def step_cc_window_open(context: Context, counter: str, delta: int) -> None:
    """Opens a fresh 30 s window - discarding any previous one, so a scenario
    cannot inherit a counter it never mentioned.
    """
    context.cc_before, context.cc_after = {}, {}
    context.cc_before[counter] = 0
    context.cc_after[counter] = delta
    context.cc_window_s = 30.0


@given("{counter} advanced by {delta:d} in that window")
def step_cc_window_add(context: Context, counter: str, delta: int) -> None:
    """Adds another counter to the open window; the ceiling is a relation
    between counters, so it needs more than one to grade.
    """
    before, after = _cc_window(context)
    before[counter] = 0
    after[counter] = delta


@then("the interval-ceiling verdict is {verdict}")
def step_cc_ceiling(context: Context, verdict: str) -> None:
    """FRAMES_RX ticks in every interval any frame arrived in, so no
    per-interval counter can out-tick it - true whatever the implementation's
    interval is, which is what makes this checkable without a rate band.
    """
    got, detail = tc.check_interval_ceiling(
        context.cc_before, context.cc_after,
        window_s=getattr(context, "cc_window_s", 30.0))
    context.cc_ceiling_detail = detail
    assert got == verdict, f"{got} != {verdict}: {detail}"


@then("the interval-ceiling offender is {counter}")
def step_cc_ceiling_offender(context: Context, counter: str) -> None:
    """The failure has to NAME the counter still counting per frame, and name
    only that one - the exempt tv tallies must not be swept in with it.
    """
    names = [o["counter"] for o in context.cc_ceiling_detail.get("offenders", [])]
    assert names == [counter], f"{names} != [{counter}]"


@given("{counter} advanced by {delta:d} over {window:d} seconds with the "
       "stream flowing")
def step_cc_sem_given(context: Context, counter: str, delta: int,
                      window: int) -> None:
    """Grades one counter against ITS OWN law over a measured window, with the
    stream known to be flowing so a zero delta means something.
    """
    context.cc_sem = tc.grade_counter_semantics(
        counter, delta, float(window), stream_flowing=True)


@then("the semantics verdict is {verdict} and the reading is {reading}")
def step_cc_sem_then(context: Context, verdict: str, reading: str) -> None:
    """The verdict, the reading it concluded, and a named clause: a grade that
    cannot cite the sentence it applied is an opinion.
    """
    got, detail = context.cc_sem
    assert got == verdict, f"{got} != {verdict}: {detail}"
    assert detail.get("reading") == reading, \
        f"reading {detail.get('reading')!r} != {reading!r}: {detail}"
    assert detail.get("clause"), "a semantics grade must name its clause"
