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

THIS GATE IS EXPECTED TO FAIL TODAY.  That is the point, and it is why it
names an owner on every finding instead of just printing a number.  Roadmap
item 5 (NxN AAF Milan streams) owns raising the framer; the entity's declared
8-channel format STAYS - down-declaring the talkers to 2ch was tried on
2026-07-27 (dade536) and reverted (e103d8e) because it "fixes" the mismatch by
abandoning the requirement and would ship an 8x8 board advertising itself as
stereo forever.

WHAT IT CHECKS, per configs/endstation_*.yaml:

  W1  declared == emitted   every AAF talker format's channels_per_frame
                            (IEEE 1722-2016 7.3.3) equals the channels the
                            framer puts in that talker's PDU.  Owner: item 5.
  W2  interface is backed   an audio_interface kind only counts if the SoC
                            actually drives that front-end's inputs.  Read out
                            of sw/litex/milan_soc.py rather than believed:
                            the TDM bus is tied to zero there, so a `tdm16`
                            config elaborates KL_tdm_capture on a dead bus and
                            its talkers emit NO FRAME AT ALL.  Owner: item 4
                            (audio-interface subtask) / the platform.
  W3  source coverage       a talker with no pair slot behind it can never
                            emit.  Advertising it is an advertised capability
                            the fabric cannot back - the same defect class as
                            W1, which is why item 00's scope says "any".
  W4  the constant is real  TALKER_WIRE_CHANS_C in the generated shape include
                            equals what the framer derivation computes, and
                            the RTL both DECLARES the parameter and USES it to
                            reset the packetizer's chans field.  A constant
                            nothing consumes is a decoration, and decorative
                            registers are what this whole item is about.

WHAT IT DOES NOT CHECK, said out loud rather than left implied.  The listener
side.  Item 00's scope includes "a SET_STREAM_FORMAT we ACCEPT must be a
format we can EMIT", and that is unverified here: the render path follows the
wire's channels_per_frame by the 1-to-1 wire-truth rule, so accepting an 8ch
sink format and rendering its first pair is deliberate, not a defect.  Closing
that half needs a runtime probe (offer a format, then read what comes back on
the wire), not a static read of the config.

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


# ------------------------------------------------------------- SoC reading --
def tdm_bus_wired(soc_text):
    """Does any SoC in this tree DRIVE the TDM capture bus?

    milan_datapath's TDM front-end is only as real as its bclk/fsync/data.
    Today add_milan_datapath ties all three to 0 and nothing overrides them
    via extra_ports, so KL_tdm_capture's fsync never toggles and it yields no
    pairs at all.  Read rather than assumed, so that wiring a TDM header
    changes this answer without an edit here."""
    # Collect every assignment and ask whether ANY is non-zero. Deliberately
    # not a negative lookahead after `\s*=\s*`: that backtracks the whitespace
    # to width zero and then happily matches the space in front of the `0`,
    # so `i_tdm_fsync_i = 0` reads as "wired" and the check inverts itself.
    vals = re.findall(r"i_tdm_fsync_i\s*=\s*([^\s,)]+)", soc_text)
    return bool(vals) and any(v != "0" for v in vals)


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

    wired = tdm_bus_wired(soc_text)
    kind = cfg["interface"]["kind"]
    slots = builder.audio_if_slots(cfg)
    pairs = builder.framer_pair_supply(cfg, wired)
    emits = builder.framer_wire_channels(cfg, wired)
    talkers = cfg["talkers"]

    # -- W2: is the declared audio interface backed by anything? -------------
    if slots and not wired:
        bad(f"{name}: audio_interface '{kind}' is not backed by the fabric",
            "roadmap item 4 (audio-interface subtask) / platform",
            f"the config elaborates KL_tdm_capture with AUDIO_IF_SLOTS_P="
            f"{slots}, but sw/litex/milan_soc.py ties i_tdm_bclk_i / "
            f"i_tdm_fsync_i / i_tdm_data_i to 0 and no platform provides TDM "
            f"pads, so fsync never toggles and the front-end yields NO pairs: "
            f"every talker of this build would emit no frame at all. The "
            f"shipping bitstream avoids this only by having been built "
            f"WITHOUT --audio-interface, i.e. as something other than what "
            f"this config declares.")
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

    # -- W3: does every advertised talker have a pair slot behind it? --------
    # The packetizer partitions pair slots by a prefix sum of chans/2, so
    # talkers beyond the supply own slots nothing ever drives; they never fill
    # nsamp_r, never set pend_r, and emit nothing. Silent, not mis-framed -
    # a different failure from W1, and the reason this is its own finding.
    backed = pairs // max(1, emits // 2)
    if backed >= len(talkers):
        ok(f"{name}: all {len(talkers)} advertised talker(s) have a source")
    else:
        bad(f"{name}: {len(talkers) - backed} of {len(talkers)} advertised "
            f"talkers have no pair source",
            "roadmap item 5 (NxN AAF Milan streams)",
            f"the front-end supplies {pairs} pair slot(s) and each "
            f"{emits}-channel talker consumes {max(1, emits // 2)}, so "
            + (f"only talker(s) 0..{backed - 1} can ever emit a frame"
               if backed else "NO talker can ever emit a frame")
            + ". The rest are advertised, bindable, and structurally silent "
              "- ACMP will return SUCCESS for them.")

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


def check_rtl_consumption():
    """W4b: the constant DRIVES the wire instead of describing it.

    A build parameter that nothing consumes is a decoration, and this repo has
    already shipped two of those (the RX address-filter fields, the PTP
    latency registers: exported by milan_csr and read by nothing in fabric).
    So: milan_datapath must declare TALKER_WIRE_CHANS_P, hand it to the
    packetizer, and the packetizer must reset its per-talker chans field from
    it - that reset IS the channels_per_frame the wire carries."""
    print("\n== the constant reaches the wire ==")
    dp = open(DATAPATH).read()
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

    # NEGATIVE CONTROL: the config that demonstrably works on the wire.
    probe("arty_current (streams clean to the reference device)", cur,
          soc_text, expect_fail=False)
    # POSITIVE CONTROL: the config measured at 100 % UNSUPPORTED_FORMAT.
    probe("ax7101_8x8 (100 % UNSUPPORTED_FORMAT on silicon)", ax,
          soc_text, expect_fail=True)
    # A TDM header appearing must CHANGE the verdict, or W2 is a constant.
    probe("ax7101_8x8 with the TDM bus wired", ax,
          soc_text.replace("i_tdm_bclk_i = 0, i_tdm_fsync_i = 0, "
                           "i_tdm_data_i = 0",
                           "i_tdm_bclk_i = pads.bclk, i_tdm_fsync_i = "
                           "pads.fsync, i_tdm_data_i = pads.data"),
          expect_fail=True)   # still fails W1: 8ch needs 4 pairs/talker x 8

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
        print("This gate is EXPECTED to fail until the framer is raised. It "
              "exists to keep\nthat deviation a build failure instead of a "
              "prose comment - see roadmap item 00\nin docs/MILAN_COMPLIANCE_"
              "GAPS.md. Do NOT silence it by lowering a declared\nformat: "
              "that was tried (dade536) and reverted (e103d8e).")
    print(f"RESULT: {'PASS' if not findings and st_ok else 'FAIL'}")
    return 0 if (not findings and st_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
