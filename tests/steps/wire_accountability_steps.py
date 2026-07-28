# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for wire_channel_accountability.feature.
#
# These steps deliberately call the SAME functions the build and the
# scripts/check_wire_accountability.py gate call - endstation_builder's
# framer_pair_supply / framer_wire_channels / interface_is_placeholder /
# emit_soc_argv - rather than re-implementing the derivation. Two
# implementations of one fact is how the fact stops being one fact, and this
# whole item exists because four separate declarations agreed with each other
# while none of them could see the wire.
#
# `wired` is passed EXPLICITLY where a scenario needs it, using the builder's
# own override parameter: that is how a scenario can ask "what would this
# config do if the TDM bus were / were not backed" without editing the SoC.

import os
import re
import sys

from behave import given, then, when

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "sw", "builder"))

DATAPATH = os.path.join(ROOT, "hdl", "milan", "milan_datapath.sv")
PACKETIZER = os.path.join(ROOT, "hdl", "ieee1722", "aaf", "KL_aaf_packetizer.sv")


@given("the end-station builder is importable")
def step_builder(context):
    import endstation_builder
    context.builder = endstation_builder
    #: None = read the fabric (the answer that matters); a scenario may pin it
    context.wired = None


@given('the end-station config "{name}"')
def step_config(context, name):
    path = os.path.join(ROOT, "configs", f"{name}.yaml")
    assert os.path.exists(path), f"missing config {path}"
    context.cfg_name = name
    context.cfg = context.builder.load_config(path)


@when("the TDM bus is not backed by the fabric")
def step_unbacked(context):
    context.wired = False


@when("the TDM bus is backed by the fabric")
def step_backed(context):
    context.wired = True


def _emits(context):
    return context.builder.framer_wire_channels(context.cfg, context.wired)


@then("the declared talker width is {n:d} channels")
def step_declared(context, n):
    got = context.builder.framer_declared_channels(context.cfg)
    assert got == n, (f"{context.cfg_name} talkers advertise {got}-channel AAF, "
                      f"expected {n} (IEEE 1722-2016 7.3.3 channels_per_frame)")


@then("every AAF talker format's channels_per_frame equals the emitted width")
def step_match(context):
    emits = _emits(context)
    bad = []
    for i, t in enumerate(context.cfg["talkers"]):
        for fmt in t["formats"]:
            c = context.builder.fmt_channels(fmt)
            if c is not None and c != emits:
                bad.append(f"talker {i} format {fmt} declares {c}ch")
    assert not bad, (
        f"{context.cfg_name}: the fabric emits {emits}ch and " + "; ".join(bad)
        + ". A listener binding such a stream passes Milan 5.5.1.2, gets ACMP "
          "SUCCESS and then discards every frame as UNSUPPORTED_FORMAT "
          "(measured 2026-07-27: 296,294 of 296,294).")


@then("at least one AAF talker format's channels_per_frame differs from the "
      "emitted width")
def step_mismatch(context):
    emits = _emits(context)
    found = any(context.builder.fmt_channels(f) not in (None, emits)
                for t in context.cfg["talkers"] for f in t["formats"])
    assert found, (f"{context.cfg_name}: expected a REPORTED mismatch against "
                   f"an emitted width of {emits}ch, and found none - the "
                   f"derivation has stopped being able to say no")


@then("the generated TALKER_WIRE_CHANS_C equals the emitted width")
def step_generated(context):
    svh = os.path.join(ROOT, "configs", "generated", context.cfg_name, "gen",
                       "adp_shape_defaults.svh")
    assert os.path.exists(svh), f"{svh} missing - regenerate with the builder"
    m = re.search(r"localparam int TALKER_WIRE_CHANS_C\s*=\s*(\d+)\s*;",
                  open(svh).read())
    assert m, f"{svh} carries no TALKER_WIRE_CHANS_C"
    emits = _emits(context)
    assert int(m.group(1)) == emits, (
        f"{context.cfg_name}: generated TALKER_WIRE_CHANS_C = {m.group(1)}, "
        f"the framer derivation says {emits}. This constant resets every "
        f"talker's chans field, so a stale value IS a wrong "
        f"channels_per_frame on the wire.")


@then("the audio interface is reported as a placeholder")
def step_placeholder(context):
    assert context.builder.interface_is_placeholder(context.cfg, context.wired)


@then("the audio interface is not a placeholder")
def step_not_placeholder(context):
    assert not context.builder.interface_is_placeholder(context.cfg,
                                                        context.wired)


@then("the emitted width falls back to {n:d} channels")
@then("the emitted width is still {n:d} channels")
def step_emits(context, n):
    assert _emits(context) == n, (f"{context.cfg_name}: emitted width is "
                                  f"{_emits(context)}ch, expected {n}ch")


@then("the front-end supplies at least {n:d} pair slots")
def step_supply(context, n):
    got = context.builder.framer_pair_supply(context.cfg, context.wired)
    assert got >= n, f"{context.cfg_name}: front-end supplies {got} pair slots"


@then('the soc argv carries "{flag}"')
def step_argv(context, flag):
    argv = context.builder.emit_soc_argv(context.cfg)
    assert flag in argv, (f"{context.cfg_name}: {flag} absent from soc argv "
                          f"{argv}")


@then("milan_datapath refuses a wire width its capture front-end cannot feed")
def step_guard_width(context):
    src = open(DATAPATH).read()
    assert re.search(r"WIRE_PAIRS_NEEDED_C\s*>\s*AIF_PAIRS_C", src), (
        "milan_datapath has no elaboration guard for the wire width - "
        "TALKER_WIRE_CHANS_P could be raised to silence every gate without "
        "the framer being able to back it")


@then("milan_datapath refuses a TDM master clock that is not an exact multiple")
def step_guard_clock(context):
    src = open(DATAPATH).read()
    assert re.search(r"AUDIO_IF_CLK_HZ_P\s*!=\s*2\s*\*\s*AIF_BCLK_HALF_C\s*\*"
                     r"\s*AIF_BCLK_HZ_C", src), (
        "milan_datapath does not check that clk_tdm_i is an exact even "
        "multiple of SLOTS*32*fs - a TDM master off the wrong clock frames at "
        "the wrong rate, silently")


@then("KL_aaf_packetizer resets every talker's chans field from the constant")
def step_pkt(context):
    src = open(PACKETIZER).read()
    assert re.search(r"chans_r\[t\]\s*<=\s*WIRE_CHANS_C\s*;", src), (
        "the channels_per_frame on the wire does not come from the constant "
        "every gate compares against - the constant would be a decoration")
