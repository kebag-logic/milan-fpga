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

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, then, when

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context

ROOT = Path(__file__).resolve().parents[2]
#: `sys.path` takes strings, and `endstation_builder.load_config` declares
#: `path: str`. Those two are the only places a path leaves this module as a
#: string; everything here is a `Path`.
sys.path.insert(0, str(ROOT / "sw" / "builder"))

DATAPATH = ROOT / "hdl" / "milan" / "milan_datapath.sv"
PACKETIZER = ROOT / "hdl" / "ieee1722" / "aaf" / "KL_aaf_packetizer.sv"


def _source(path: Path) -> str:
    """One RTL or generated source's text, read and closed."""
    return path.read_text()


@given("the end-station builder is importable")
def step_builder(context: Context) -> None:
    """Bind the real builder module, so a scenario cannot judge a re-derivation.

    Leaves `context.wired` at None, which means "read the fabric" - the answer
    the build itself gets. A scenario that wants the other answer says so.
    """
    import endstation_builder
    context.builder = endstation_builder
    #: None = read the fabric (the answer that matters); a scenario may pin it
    context.wired = None


@given('the end-station config "{name}"')
def step_config(context: Context, name: str) -> None:
    """Load configs/<name>.yaml through the builder's own loader."""
    path = ROOT / "configs" / f"{name}.yaml"
    assert path.exists(), f"missing config {path}"
    context.cfg_name = name
    context.cfg = context.builder.load_config(str(path))


@when("the TDM bus is not backed by the fabric")
def step_unbacked(context: Context) -> None:
    """Pin the fabric answer to "no TDM bus", without editing the SoC."""
    context.wired = False


@when("the TDM bus is backed by the fabric")
def step_backed(context: Context) -> None:
    """Pin the fabric answer to "the TDM bus is there", without editing the SoC."""
    context.wired = True


def _emits(context):
    return context.builder.framer_wire_channels(context.cfg, context.wired)


@then("the declared talker width is {n:d} channels")
def step_declared(context: Context, n: int) -> None:
    """Check what the talkers ADVERTISE, before anything is compared to it."""
    got = context.builder.framer_declared_channels(context.cfg)
    assert got == n, (f"{context.cfg_name} talkers advertise {got}-channel AAF, "
                      f"expected {n} (IEEE 1722-2016 7.3.3 channels_per_frame)")


@then("every AAF talker format's channels_per_frame equals the emitted width")
def step_match(context: Context) -> None:
    """The advertised-vs-emitted agreement this whole feature exists to hold."""
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
def step_mismatch(context: Context) -> None:
    """The negative arm: a config that IS wrong must still be reported wrong."""
    emits = _emits(context)
    found = any(context.builder.fmt_channels(f) not in (None, emits)
                for t in context.cfg["talkers"] for f in t["formats"])
    assert found, (f"{context.cfg_name}: expected a REPORTED mismatch against "
                   f"an emitted width of {emits}ch, and found none - the "
                   f"derivation has stopped being able to say no")


@then("the generated TALKER_WIRE_CHANS_C equals the emitted width")
def step_generated(context: Context) -> None:
    """Catch a stale generated header: the constant the RTL uses must agree."""
    svh = (ROOT / "configs" / "generated" / context.cfg_name / "gen"
           / "adp_shape_defaults.svh")
    assert svh.exists(), f"{svh} missing - regenerate with the builder"
    m = re.search(r"localparam int TALKER_WIRE_CHANS_C\s*=\s*(\d+)\s*;",
                  _source(svh))
    assert m, f"{svh} carries no TALKER_WIRE_CHANS_C"
    emits = _emits(context)
    assert int(m.group(1)) == emits, (
        f"{context.cfg_name}: generated TALKER_WIRE_CHANS_C = {m.group(1)}, "
        f"the framer derivation says {emits}. This constant resets every "
        f"talker's chans field, so a stale value IS a wrong "
        f"channels_per_frame on the wire.")


@then("the audio interface is reported as a placeholder")
def step_placeholder(context: Context) -> None:
    """The audio interface must admit it is a stand-in, not real capture."""
    assert context.builder.interface_is_placeholder(context.cfg, context.wired)


@then("the audio interface is not a placeholder")
def step_not_placeholder(context: Context) -> None:
    """A backed TDM bus must stop the builder calling the interface a stand-in."""
    assert not context.builder.interface_is_placeholder(context.cfg,
                                                        context.wired)


@then("the emitted width falls back to {n:d} channels")
@then("the emitted width is still {n:d} channels")
def step_emits(context: Context, n: int) -> None:
    """Pin the width the fabric actually puts on the wire for this config."""
    assert _emits(context) == n, (f"{context.cfg_name}: emitted width is "
                                  f"{_emits(context)}ch, expected {n}ch")


@then("the front-end supplies at least {n:d} pair slots")
def step_supply(context: Context, n: int) -> None:
    """The capture front-end must have the pair slots the width needs."""
    got = context.builder.framer_pair_supply(context.cfg, context.wired)
    assert got >= n, f"{context.cfg_name}: front-end supplies {got} pair slots"


@then('the soc argv carries "{flag}"')
def step_argv(context: Context, flag: str) -> None:
    """The derived width must reach the SoC build, not stop at the builder."""
    argv = context.builder.emit_soc_argv(context.cfg)
    assert flag in argv, (f"{context.cfg_name}: {flag} absent from soc argv "
                          f"{argv}")


@then("milan_datapath refuses a wire width its capture front-end cannot feed")
def step_guard_width(context: Context) -> None:
    """The RTL must refuse the mismatch itself, not rely on this gate."""
    src = _source(DATAPATH)
    assert re.search(r"WIRE_PAIRS_NEEDED_C\s*>\s*AIF_PAIRS_C", src), (
        "milan_datapath has no elaboration guard for the wire width - "
        "TALKER_WIRE_CHANS_P could be raised to silence every gate without "
        "the framer being able to back it")


@then("milan_datapath refuses a TDM master clock that is not an exact multiple")
def step_guard_clock(context: Context) -> None:
    """A TDM master off a non-multiple clock frames at the wrong rate, silently."""
    src = _source(DATAPATH)
    assert re.search(r"AUDIO_IF_CLK_HZ_P\s*!=\s*2\s*\*\s*AIF_BCLK_HALF_C\s*\*"
                     r"\s*AIF_BCLK_HZ_C", src), (
        "milan_datapath does not check that clk_tdm_i is an exact even "
        "multiple of SLOTS*32*fs - a TDM master off the wrong clock frames at "
        "the wrong rate, silently")


@then("KL_aaf_packetizer resets every talker's chans field from the constant")
def step_pkt(context: Context) -> None:
    """Without this write, the constant every gate compares against decorates."""
    src = _source(PACKETIZER)
    assert re.search(r"chans_r\[t\]\s*<=\s*WIRE_CHANS_C\s*;", src), (
        "the channels_per_frame on the wire does not come from the constant "
        "every gate compares against - the constant would be a decoration")
