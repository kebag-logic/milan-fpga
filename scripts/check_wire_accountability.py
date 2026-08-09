#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
check_wire_accountability.py - the ADVERTISED-vs-EMITTED gate (roadmap item 00).

WHY THIS EXISTS.  Every other consistency gate in this repo compares a
declaration against ANOTHER declaration - config to generated svh to CSR to
descriptor counts, plus the milan_datapath elaboration guard - and not one of
them can see the wire.  So on 2026-07-27 the AX7101 8x8 talkers advertised
0x0205022002006000 (AAF 48 kHz, EIGHT channels) while the framer emitted
STEREO, and everything stayed green: 57/57 Verilator suites, 2,062,389 checks,
yosys 48/48, behave 113/113, lint at ratchet.

The only thing that noticed was a Milan-validated reference device.  It bound
to talker 0, passed the Milan 5.5.1.2 format check, returned ACMP SUCCESS with
a correct MAAP dmac and a 137042 ns MSRP latency - and then counted
UNSUPPORTED_FORMAT on 296,294 of 296,294 frames at 8000/s, because it was
promised 8-channel AAF and handed the stereo the framer actually produces.

The deviation WAS recorded.  As a prose comment in the config.  A comment does
not fail a build.  This gate is that comment turned into an exit code.

THIS GATE IS EXPECTED TO FAIL, and it names an owner on every finding instead
of just printing a number.  The entity's declared 8-channel format STAYS -
down-declaring the talkers to 2ch was tried on 2026-07-27 (dade536) and
reverted (e103d8e) because it "fixes" the mismatch by abandoning the
requirement and would ship an 8x8 board advertising itself as stereo forever.

WHAT MOVED, 2026-07-28.  W1 is CLOSED on every shipped config: the TDM MASTER
front-end landed (hdl/ieee1722/aaf/KL_tdm_capture_master.sv, instantiated by
milan_datapath when AUDIO_IF_MASTER_P != 0), the fabric now GENERATES bclk and
fsync off its own MMCM output instead of waiting for a codec that was never
wired, and the capture supply went from ONE pair (KL_aaf_capture_i2s, which
hardwires pair_slot_o = 4'd0) to 16 pairs on the AX7101's TDM32 bus and 5 on
the Arty's TDM8+I2S blend (HANDOVER 8.3b).  Declared == emitted now reads
8 == 8 and 4 == 4 where it read 8 == 2 and 4 == 2.

AND W3 IS CLOSED TOO (2026-07-28 evening), the other way round from W1: not by
raising the supply but by making the FABRIC hold Milan v1.2 5.3.7.3 - "As long
as a PAAD is declaring a Talker Advertise attribute and receiving a Listener
Ready or Listener Ready Failed attribute for a Stream Output, it shall be
streaming AVTP packets."  KL_pair_zero_fill strobes every pair slot the
packetizer consumes at the true media rate (clk_audio/512, never the milan-clk
approximation), silence where no physical source feeds it, so a BOUND talker
always frames - real audio where fed, legal PCM where not, which is what any
shipping product does with an unpatched input.  What W3 reports now is SOURCE
COVERAGE - which slots carry a real capture channel - as INFORMATION: a
product truth worth printing, not a compliance failure any clause names.  W5
is the new failing check: the fill structure itself must exist, because a
deleted filler would silently reopen the clause violation.

WHAT IT CHECKS, per configs/endstation_*.yaml:

  W1  declared == emitted   every AAF talker format's channels_per_frame
                            (IEEE 1722-2016 7.3.3) equals the channels the
                            framer puts in that talker's PDU.  Owner: item 5.
  W2  placeholder rule      an audio_interface kind only counts if the SoC
                            actually drives that front-end's inputs.  Read out
                            of sw/litex/milan_soc.py rather than believed: the
                            TDM bus is tied to zero there.  This is NOT a
                            finding - USER 2026-07-27, "the tdm can be a
                            placeholder": declaring the interface the product
                            will have is legitimate.  What was dangerous is a
                            placeholder that SILENTLY changed the gateware, so
                            the builder withholds --audio-interface for one and
                            the build elaborates the I2S front-end the board
                            really has.  W2 reports that the withholding is in
                            effect.  Owner: item 4 (TDM header + SoC wiring).
  W3  source coverage       INFORMATIONAL since the 5.3.7.3 silence fill: a
                            talker beyond the physical supply frames SILENCE
                            (KL_pair_zero_fill), so it streams when bound.
                            Which slots carry a real capture channel is a
                            product fact this gate keeps visible - it is how
                            a bench operator knows talker 5 plays zeros
                            because nothing is plugged in, not because the
                            fabric is broken.
  W5  the fill is real      milan_datapath instantiates KL_pair_zero_fill
                            over N_STREAMS x WIRE_CHANS/2 slots, paces it
                            from the AUDIO clock (/512 = 48.000 kHz exactly),
                            and the packetizer's bypass leg consumes the
                            FILLED stream.  Deleting any of those silently
                            reopens the 5.3.7.3 violation, so each is a
                            failing check.
  W4  the constant is real  TALKER_WIRE_CHANS_C in the generated shape include
                            equals what the framer derivation computes, and
                            the RTL both DECLARES the parameter and USES it to
                            reset the packetizer's chans field.  A constant
                            nothing consumes is a decoration, and decorative
                            registers are what this whole item is about.

THE LISTENER HALF IS CLOSED, and not by this file.  Item 00's scope included
"a SET_STREAM_FORMAT we ACCEPT must be a format we can EMIT".  MEASURED on
silicon 2026-07-28: SET_STREAM_FORMAT on our STREAM_OUTPUT returns status 7
NOT_SUPPORTED and the readback is unchanged - we accept no such thing.  That
refusal is CORRECT: FR-STR-03 (docs/reference/FR_NFR.md, Milan v1.2 5.4)
requires format-adaptivity of the LISTENER - "STREAM_INPUT ... MUST NOT be
fixed" - and imposes nothing equivalent on a talker.  USER 2026-07-28: "only
the input stream can adapt".  So there is no accept-vs-emit defect on the
talker side; the fault is wholly the framer's, which is what W1 measures.

NEGATIVE CONTROL.  endstation_arty_current MUST pass.  It ships `clusters: 8`
with a 2-channel format and streams to the same reference device with zero
unsupported-format frames.  A check that only ever fails proves as little as
one that only ever passes - and gating on `clusters` was the FIRST wrong
attempt on 2026-07-27, refused exactly this config, and was reverted.

Usage:
    check_wire_accountability.py                 # every configs/endstation_*.yaml
    check_wire_accountability.py --self-test     # + prove it bites both ways
    check_wire_accountability.py --config <path> # one config

Exit 0 = the fabric backs every advertised width, 1 = it does not (findings
printed with their owner), 2 = usage/setup.  Needs pyyaml.
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT, "configs")
SOC = os.path.join(ROOT, "sw/litex/milan_soc.py")
DATAPATH = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
PACKETIZER = os.path.join(ROOT, "hdl/ieee1722/aaf/KL_aaf_packetizer.sv")

sys.path.insert(0, os.path.join(ROOT, "sw/builder"))

findings = []
checks = 0
quiet = False          #! set while a self-test mutation is being run


def ok(what, detail=""):
    global checks
    checks += 1
    if not quiet:
        print(f"  [ok]   {what}{(' = ' + detail) if detail else ''}")


def bad(what, owner, detail):
    global checks
    checks += 1
    findings.append((what, owner, detail))
    if not quiet:
        print(f"  [FAIL] {what}\n         {detail}\n         OWNER: {owner}")


def note(what, detail=""):
    """A fact worth printing that is NOT a finding - W3 source coverage.

    Counted as a check (it ran, it can be seen), never as a failure: since the
    5.3.7.3 silence fill, an unfed talker streams zeros, and no clause turns
    an unpatched input into a defect."""
    global checks
    checks += 1
    if not quiet:
        print(f"  [note] {what}{(' - ' + detail) if detail else ''}")


# ------------------------------------------------------------- SoC reading --
#  tdm_bus_wired() lives in endstation_builder.py: the builder needs the same
#  answer to decide whether --audio-interface is emitted, and two copies of a
#  fact about the fabric is how the fact stops being one fact.


def i2s_capture_pads(soc_text):
    """Boards whose I2S capture front-end has real pads behind sdout.

    The AX7101 has `_connectors = []`, so there is no pmoda, so `i2s_pads`
    stays None and `i_i2s_sdout_i = 0`: the front-end still produces one pair
    per sample period, of digital SILENCE.  That distinction matters for W3
    (a pair slot IS fed, so the talker does emit) and is why this returns a
    flag rather than reducing the pair count."""
    return bool(re.search(r"i_i2s_sdout_i\s*=\s*self\.i2s_pads\[3\]", soc_text))


# --------------------------------------------------------------- the checks --
def check_config(builder, path, soc_text):
    name = os.path.basename(path)[:-5]
    cfg = builder.load_config(path)
    if not quiet:
        print(f"\n== {name} ==")

    wired = builder.tdm_bus_wired(soc_text)
    kind = cfg["interface"]["kind"]
    declared = builder.AUDIO_IF_SLOTS.get(kind, 0)   # what the CONFIG asks for
    slots = builder.audio_if_slots(cfg, wired)       # what the BUILD elaborates
    pairs = builder.framer_pair_supply(cfg, wired)
    emits = builder.framer_wire_channels(cfg, wired)
    talkers = cfg["talkers"]

    # -- W2: is the declared audio interface backed by anything? -------------
    # NOT a finding when unbacked - USER 2026-07-27: "the tdm can be a
    # placeholder". Declaring the interface the product will have is
    # legitimate; the danger was only ever that the placeholder SILENTLY
    # changed the gateware, and the builder now withholds --audio-interface
    # so it cannot. What this reports is that the withholding is in effect.
    if declared and not wired:
        ok(f"{name}: audio_interface '{kind}' is a PLACEHOLDER (declared, "
           f"fabric does not drive it)",
           f"--audio-interface withheld; build elaborates the I2S front-end "
           f"({pairs} pair slot(s))")
    else:
        ok(f"{name}: audio_interface '{kind}' is backed",
           f"{pairs} pair slot(s) supplied")

    # -- W1: declared channels_per_frame == what the framer emits ------------
    # THE measured defect. Compared per format, because a talker may declare
    # several and every one of them is bindable.
    for i, t in enumerate(talkers):
        for fmt in t["formats"]:
            declared = builder.fmt_channels(fmt)
            if declared is None:
                continue                       # CRF carries no channel count
            what = (f"{name}: talker {i} format {fmt} declares "
                    f"{declared}ch, fabric emits {emits}ch")
            if declared == emits:
                ok(what)
            else:
                bad(what, "roadmap item 5 (NxN AAF Milan streams) - RAISE THE "
                          "FRAMER, do not lower the declaration",
                    f"a listener binding this stream is promised {declared} "
                    f"channels and handed {emits}. Measured on silicon "
                    f"2026-07-27: ACMP SUCCESS, Milan 5.5.1.2 format check "
                    f"passed, then UNSUPPORTED_FORMAT on 100 % of 296,294 "
                    f"frames. The framer's width is milan_datapath "
                    f"TALKER_WIRE_CHANS_P and it cannot be raised past what "
                    f"the capture front-end feeds (elaboration guard).")

    # -- W3: source coverage, INFORMATIONAL since the 5.3.7.3 silence fill ---
    # The packetizer partitions pair slots by a prefix sum of chans/2.
    # Talkers beyond the physical supply frame SILENCE (KL_pair_zero_fill
    # strobes their slots at the media rate), so a bound one streams as the
    # clause requires; what remains worth PRINTING is which talkers carry a
    # real capture channel - the difference between "plays zeros because
    # nothing is plugged in" and "broken".
    backed = pairs // max(1, emits // 2)
    if backed >= len(talkers):
        ok(f"{name}: all {len(talkers)} advertised talker(s) have a "
           f"physical source")
    else:
        note(f"{name}: source coverage {backed} of {len(talkers)} talkers",
             f"the front-end supplies {pairs} physical pair slot(s), each "
             f"{emits}-channel talker consumes {max(1, emits // 2)}; "
             f"talker(s) {backed}..{len(talkers) - 1} frame SILENCE via "
             f"KL_pair_zero_fill when bound (Milan v1.2 5.3.7.3). Physical "
             f"backing for them is roadmap item 5.")

    # -- W4: the constant is generated AND consumed --------------------------
    svh = os.path.join(CONFIG_DIR, "generated", name, "gen",
                       "adp_shape_defaults.svh")
    if not os.path.exists(svh):
        bad(f"{name}: no generated shape include", "run endstation_builder.py",
            f"{svh} is missing - the wire constant has nowhere to live")
        return
    m = re.search(r"localparam int TALKER_WIRE_CHANS_C\s*=\s*(\d+)\s*;",
                  open(svh).read())
    if not m:
        bad(f"{name}: generated shape include carries no TALKER_WIRE_CHANS_C",
            "sw/builder/endstation_builder.py emit_adp_shape_svh",
            "the framer's width is not expressed anywhere a gate can read - "
            "which is the state that let the 8ch/2ch gap ship")
    elif int(m.group(1)) != emits:
        bad(f"{name}: generated TALKER_WIRE_CHANS_C is stale",
            "regenerate with endstation_builder.py",
            f"include says {m.group(1)}, the framer derivation says {emits}")
    else:
        ok(f"{name}: generated TALKER_WIRE_CHANS_C matches the framer",
           str(emits))


def check_rtl_consumption(dp_text=None):
    """W4b: the constant DRIVES the wire instead of describing it.

    A build parameter that nothing consumes is a decoration, and this repo has
    already shipped two of those (the RX address-filter fields, the PTP
    latency registers: exported by milan_csr and read by nothing in fabric).
    So: milan_datapath must declare TALKER_WIRE_CHANS_P, hand it to the
    packetizer, and the packetizer must reset its per-talker chans field from
    it - that reset IS the channels_per_frame the wire carries.

    `dp_text` overrides the milan_datapath source so the self-test can prove
    the W5 checks bite (methodology R2)."""
    if not quiet:
        print("\n== the constant reaches the wire ==")
    dp = dp_text if dp_text is not None else open(DATAPATH).read()
    pk = open(PACKETIZER).read()

    if re.search(r"parameter int TALKER_WIRE_CHANS_P\s*=\s*2\s*,", dp):
        ok("milan_datapath declares TALKER_WIRE_CHANS_P (default 2)")
    else:
        bad("milan_datapath does not declare TALKER_WIRE_CHANS_P",
            "roadmap item 00", "the wire width has no build constant")

    if re.search(r"\.WIRE_CHANS_P\s*\(\s*TALKER_WIRE_CHANS_P\s*\)", dp):
        ok("milan_datapath passes it to KL_aaf_packetizer")
    else:
        bad("KL_aaf_packetizer is not given TALKER_WIRE_CHANS_P",
            "roadmap item 00",
            "the packetizer would keep its own literal and the constant "
            "would describe rather than drive")

    if re.search(r"\.CHANS_P\s*\(\s*TALKER_WIRE_CHANS_P\s*\)", dp):
        ok("milan_datapath passes it to KL_pcm_tx")
    else:
        bad("KL_pcm_tx is not given TALKER_WIRE_CHANS_P", "roadmap item 00",
            "the ALSA-playback pair source would de-interleave a different "
            "width from the one the framer stamps")

    if re.search(r"chans_r\[t\]\s*<=\s*WIRE_CHANS_C\s*;", pk):
        ok("KL_aaf_packetizer resets every talker's chans from the constant")
    else:
        bad("KL_aaf_packetizer does not reset chans from WIRE_CHANS_P",
            "roadmap item 00",
            "the channels_per_frame on the wire would not come from the "
            "constant the gate compares against")

    if re.search(r"WIRE_PAIRS_NEEDED_C\s*>\s*AIF_PAIRS_C", dp):
        ok("milan_datapath guards the constant against the front-end supply")
    else:
        bad("milan_datapath has no elaboration guard for the wire width",
            "roadmap item 00",
            "TALKER_WIRE_CHANS_P could be raised to silence this gate "
            "without the framer being able to back it - which would make it "
            "one more declaration agreeing with the other declarations")

    # -- W5: the 5.3.7.3 silence fill is structurally present ----------------
    # Each of these is a FAILING check: delete the filler (or its pacing, or
    # its consumer) and a bound-but-unfed talker goes back to emitting no
    # frame at all after answering ACMP SUCCESS - the exact state the clause
    # forbids and the reason W3 could become informational.
    if re.search(r"ZF_TOTAL_C\s*=\s*N_STREAMS\s*\*\s*"
                 r"\(\s*TALKER_WIRE_CHANS_P\s*/\s*2\s*\)", dp):
        ok("W5: fill covers N_STREAMS x WIRE_CHANS/2 pair slots (ZF_TOTAL_C)")
    else:
        bad("W5: ZF_TOTAL_C does not span every consumed pair slot",
            "Milan v1.2 5.3.7.3 (the silence fill)",
            "a fill that covers fewer slots than the packetizer consumes "
            "leaves the uncovered talkers bindable and mute")
    if re.search(r"KL_pair_zero_fill\s*#\(\s*\.TOTAL_P\s*\(\s*ZF_TOTAL_C", dp):
        ok("W5: KL_pair_zero_fill instantiated over that span")
    else:
        bad("W5: milan_datapath does not instantiate KL_pair_zero_fill",
            "Milan v1.2 5.3.7.3 (the silence fill)",
            "a bound talker with no physical source emits NO FRAME AT ALL - "
            "ACMP SUCCESS, then the state the clause's first sentence "
            "forbids")
    if re.search(r"zf_apulse_r\s*<=\s*\(\s*zf_adiv_r\s*==\s*9'd511\s*\)", dp) \
       and re.search(r"cdc_pulse\s+zf_tick_cdc", dp):
        ok("W5: the fill grid is the AUDIO clock /512 (48.000 kHz exactly), "
           "CDC'd")
    else:
        bad("W5: the fill grid is not derived from the audio clock",
            "Milan v1.2 5.3.7.3 (the silence fill)",
            "pacing fills from the milan-clk divider (48.03 kHz at 50 MHz) "
            "makes a silence stream drift +640 ppm against its declared "
            "rate and collect LATE_TIMESTAMP at the listener")
    # The selector was a bare cfg_chmap_enable until the crossbar became
    # in-circuit BY SHAPE (VERSION 0x002C): it is now cap_xbar_live_w =
    # odmap_dyn | cfg_chmap_enable, so a dynamic-map shape feeds the
    # packetizer from the crossbar without anyone arming a debug bit.  Match
    # the mux by its ARMS (the fill is the non-crossbar leg, which is what
    # this check is about) and prove the selector separately below.
    if re.search(r"pkt_pv_w\s*=\s*\w+\s*\?\s*cmap_pv_w\s*:\s*zf_pv_w", dp):
        ok("W5: the packetizer bypass leg consumes the FILLED stream")
    else:
        bad("W5: the packetizer does not consume the filled stream",
            "Milan v1.2 5.3.7.3 (the silence fill)",
            "a filler nothing downstream reads is a decoration - the "
            "packetizer would still starve on unfed slots")
    if re.search(r"KL_pair_blend\s*#\(\s*\.TDM_SLOTS_P\s*\("
                 r"\s*AUDIO_IF_SLOTS_P", dp):
        ok("W5: the 8.3b blend arm exists (KL_pair_blend, I2S = pair slot 0)")
    else:
        bad("W5: milan_datapath has no KL_pair_blend arm",
            "HANDOVER 8.3b (the Arty audio shape)",
            "the Arty build would lose the I2S pair the budget counts - "
            "supply 4, not 5, and the builder's arithmetic would disagree "
            "with the fabric")


# ------------------------------------------------------------------- driver --
def load_builder():
    try:
        import endstation_builder
    except ImportError as e:
        print(f"cannot import sw/builder/endstation_builder.py: {e}",
              file=sys.stderr)
        sys.exit(2)
    return endstation_builder


def all_configs():
    return sorted(os.path.join(CONFIG_DIR, f)
                  for f in os.listdir(CONFIG_DIR)
                  if f.startswith("endstation_") and f.endswith(".yaml"))


def run(paths=None):
    builder = load_builder()
    soc_text = open(SOC).read()
    for p in (paths or all_configs()):
        check_config(builder, p, soc_text)
    check_rtl_consumption()


# ---------------------------------------------------------------- self-test --
def self_test():
    """A gate that cannot fail is not a gate, and a gate that only fails is
    not one either.  Both directions, on real configs."""
    global quiet, findings, checks
    builder = load_builder()
    soc_text = open(SOC).read()
    print("\n== self-test: the gate bites in both directions ==")
    passed = True

    def probe(label, path, text, expect_fail):
        nonlocal passed
        global quiet, findings
        quiet, saved = True, list(findings)
        findings = []
        try:
            check_config(builder, path, text)
            got = bool(findings)
        finally:
            findings = saved
            quiet = False
        verdict = "as expected" if got == expect_fail else "WRONG"
        if got != expect_fail:
            passed = False
        print(f"  [{'ok' if got == expect_fail else 'FAIL'}]   {label}: "
              f"{'findings' if got else 'clean'} - {verdict}")

    cur = os.path.join(CONFIG_DIR, "endstation_arty_current.yaml")
    ax = os.path.join(CONFIG_DIR, "endstation_ax7101_8x8.yaml")

    # NEGATIVE CONTROLS: every shipped config is clean now - arty_current
    # streams to the reference device, and the 8x8 emits the 8 channels it
    # advertises with its unfed talkers framing 5.3.7.3 silence.
    probe("arty_current (streams clean to the reference device)", cur,
          soc_text, expect_fail=False)
    probe("ax7101_8x8 (W1 closed by the master, W3 closed by the fill)", ax,
          soc_text, expect_fail=False)
    # W2 MUST NOT BE A CONSTANT: strip the master out of the SoC and the same
    # config must fall back to the I2S front-end (1 pair) and report the
    # ORIGINAL W1 defect - 8 channels advertised, 2 emitted, which is what a
    # Milan-validated device measured at 296,294 of 296,294 frames. This probe
    # is the one that proves the 2026-07-28 change is what moved the verdict
    # and not a loosened rule.
    probe("ax7101_8x8 with the TDM master removed (the 07-27 fabric)", ax,
          soc_text.replace('dp_params["p_AUDIO_IF_MASTER_P"] = 1',
                           'pass  # master removed for the self-test'),
          expect_fail=True)

    # W5 MUST BITE (R2): delete the silence fill from the datapath text and
    # the RTL-consumption pass must fail - a deleted filler is exactly how
    # the 5.3.7.3 violation would silently come back.
    global quiet, findings
    quiet, saved = True, list(findings)
    findings = []
    try:
        check_rtl_consumption(
            open(DATAPATH).read().replace("KL_pair_zero_fill", "KL_deleted"))
        got = bool(findings)
    finally:
        findings = saved
        quiet = False
    if got:
        print("  [ok]   datapath with the silence fill deleted: findings - "
              "as expected")
    else:
        passed = False
        print("  [FAIL]   datapath with the silence fill deleted: clean - "
              "WRONG (W5 cannot bite)")

    print(f"  self-test: {'PASS' if passed else 'FAIL'}")
    return passed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--config", help="check one config")
    args = ap.parse_args()

    run([args.config] if args.config else None)
    st_ok = self_test() if args.self_test else True

    print("\n" + "-" * 70)
    print(f"checks: {checks}   findings: {len(findings)}")
    if findings:
        print("\nTHE FABRIC CANNOT BACK WHAT THE ENTITY ADVERTISES:\n")
        for what, owner, detail in findings:
            print(f"  * {what}")
            print(f"    {detail}")
            print(f"    OWNER: {owner}\n")
        print("Since 2026-07-28 this gate is EXPECTED TO PASS: the framer "
              "was raised to the\ndeclaration (TDM master, W1) and every "
              "bound talker frames (the 5.3.7.3\nsilence fill, W3->W5). A "
              "finding here is a REGRESSION of one of those, or a\nnew "
              "advertised width the fabric cannot back. Do NOT silence it by "
              "lowering a\ndeclared format: that was tried (dade536) and "
              "reverted (e103d8e).")
    print(f"RESULT: {'PASS' if not findings and st_ok else 'FAIL'}")
    return 0 if (not findings and st_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
