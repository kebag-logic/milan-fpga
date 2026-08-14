# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for milan_base_formats.feature.
#
# THE ORACLE IS THE CLAUSE, so this file does NOT import the builder's
# base_format_cover(): the format strings below are transcribed from Milan
# v1.2 Table 6.2 "Summary of Base Audio Stream Formats" (printed p. 111) and
# the coverage arithmetic is written out from IEEE 1722-2016 Annex I.2.4.
# Grading a derivation with itself is how a wrong derivation passes.
#
# The configs are read through endstation_builder.load_config, which is where
# the completion happens, so what these scenarios see is what the descriptors
# will carry - not what the YAML says.

from behave import then, when

#: Milan v1.2 Table 6.2, the 48 kHz block: five Base formats, one per channel
#: count in 6.2's N in {1, 2, 4, 6, 8}. AAF PCM 32-bit, nsr 5, 6 samples/PDU.
BASE_48K = {1: 0x0205022000406000, 2: 0x0205022000806000,
            4: 0x0205022001006000, 6: 0x0205022001806000,
            8: 0x0205022002006000}
#: ...and the 96/192 kHz blocks, so a config that ever advertises them is
#: graded rather than silently skipped (nsr 7 / 9, 12 / 24 samples per PDU).
BASE_96K = {1: 0x020702200040C000, 2: 0x020702200080C000,
            4: 0x020702200100C000, 6: 0x020702200180C000,
            8: 0x020702200200C000}
BASE_192K = {1: 0x0209022000418000, 2: 0x0209022000818000,
             4: 0x0209022001018000, 6: 0x0209022001818000,
             8: 0x0209022002018000}
TABLE_6_2 = {48000: BASE_48K, 96000: BASE_96K, 192000: BASE_192K}
#: Milan v1.2 7.3.2 + Table 7.1 - the one CRF Media Clock Stream Format:
#: base frequency 48000 Hz, 1 timestamp per PDU, timestamp interval 96.
CRF_FORMAT = 0x041060010000BB80


def _cover(fmts):
    """{rate_hz: set(Base channel counts advertised)} for one formats list.

    IEEE 1722-2016 Annex I.2.4 on the ut bit: "When set to one (1) the stream
    source or sink is capable of using fewer channels than specified", so one
    ut entry advertises every Base count up to its own channels_per_frame -
    which Milan 6.5 makes the recommended spelling of the family and 5.3.3.4
    confirms reads that way ("a single entry in the formats list can describe
    a range of formats when using the "up to" bit").
    """
    cover = {}
    for f in fmts:
        n = int(str(f), 16)
        ut, ch = (n >> 52) & 1, (n >> 22) & 0x3FF
        stem = n & ~((1 << 52) | (0x3FF << 22))
        for rate, row in TABLE_6_2.items():
            if stem != row[8] & ~(0x3FF << 22):
                continue
            add = {c for c in row if c <= ch} if ut else {ch} & set(row)
            if add:
                cover.setdefault(rate, set()).update(add)
    return cover


def _missing(fmts):
    """{rate_hz: sorted missing Base channel counts} - empty when complete."""
    return {rate: sorted(set(TABLE_6_2[rate]) - got)
            for rate, got in _cover(fmts).items()
            if set(TABLE_6_2[rate]) - got}


@then("every Stream Input advertises all five 48 kHz Base channel counts")
def step_inputs_complete(context):
    bad = []
    for i, s in enumerate(context.cfg["listeners"]):
        for rate, miss in sorted(_missing(s["formats"]).items()):
            bad.append(f"STREAM_INPUT[{i}] ('{s['name']}') advertises "
                       f"{s['formats']} and is missing the {miss} channel "
                       f"{rate} Hz Base format(s)")
    assert not bad, (
        f"{context.cfg_name}: " + "; ".join(bad) + ". Milan v1.2 6.4: \"If "
        "the PAAD-AE Base Listener advertises support for a 48kHz (resp. "
        "96kHz, 192kHz) Base format in a Stream Input, then it shall also "
        "advertise support for all the other 48kHz (resp. 96kHz, 192kHz) "
        "Base formats in this Stream Input.\"")


@then("every Stream Input advertises the same Base sampling rates")
def step_inputs_same_rates(context):
    rates = {tuple(sorted(_cover(s["formats"])))
             for s in context.cfg["listeners"] if _cover(s["formats"])}
    assert len(rates) <= 1, (
        f"{context.cfg_name}: Stream Inputs advertise Base formats at "
        f"differing rate sets {sorted(rates)}. Milan v1.2 6.4: \"then it "
        "shall advertise support for a 48kHz (resp. 96kHz, 192kHz) Base "
        "format in all the Stream Input which advertise support for a Base "
        "format, in this Configuration.\"")


@then("every advertised Base sampling rate is one the AUDIO_UNIT reports")
def step_rates_match_audio_unit(context):
    unit = [int(r) for r in context.cfg["clocking"]["audio_unit_rates_hz"]]
    bad = []
    for label, key in (("STREAM_INPUT", "listeners"),
                       ("STREAM_OUTPUT", "talkers")):
        for i, s in enumerate(context.cfg[key]):
            for rate in sorted(_cover(s["formats"])):
                if rate not in unit:
                    bad.append(f"{label}[{i}] advertises a {rate} Hz Base "
                               f"format")
    assert not bad, (
        f"{context.cfg_name}: " + "; ".join(bad) + f" while the AUDIO_UNIT "
        f"reports sampling rates {unit}. Milan v1.2 5.3.3.3: \"The list of "
        "supported sampling rates of each AUDIO_UNIT descriptor shall "
        "correctly report the sampling rates supported by the Audio Unit\", "
        "and 5.3.3.4 says the same of the formats list - one of the two is "
        "lying.")


@then("at least one Stream Output advertises a Base format")
def step_output_has_base(context):
    assert any(_cover(s["formats"]) for s in context.cfg["talkers"]), (
        f"{context.cfg_name}: no Stream Output advertises a Milan 6.2 Base "
        "format. Milan v1.2 6.3: \"A PAAD-AE Base Talker shall have at least "
        "one Configuration that contains at least one Stream Output which "
        "advertises support for a Base format in its list of supported "
        "formats.\"")


@then("no Stream Output advertises more than one Base channel count")
def step_output_is_wire_truth(context):
    bad = []
    for i, s in enumerate(context.cfg["talkers"]):
        for rate, got in sorted(_cover(s["formats"]).items()):
            if len(got) != 1:
                bad.append(f"STREAM_OUTPUT[{i}] ('{s['name']}') advertises "
                           f"{rate} Hz Base channel counts {sorted(got)}")
    assert not bad, (
        f"{context.cfg_name}: " + "; ".join(bad) + ". Milan v1.2 6.3 asks a "
        "Base Talker for no family - \"A PAAD-AE Base Talker may advertise "
        "any Base Format that is reasonable for its functionality\" - and a "
        "talker cannot correct a wider claim: it emits ONE width and "
        "SET_STREAM_FORMAT on a STREAM_OUTPUT answers NOT_SUPPORTED, so a "
        "listener handed a width the framer cannot produce discards every "
        "frame (silicon 2026-07-27: 296,294 of 296,294).")


def _crf_streams(context):
    clk = context.cfg["clocking"]
    out = []
    if clk["crf_sink"]:
        out.append(("STREAM_INPUT", clk["crf_format"]))
    if clk["crf_output"]:
        out.append(("STREAM_OUTPUT", clk["crf_output_format"]))
    return out


@then("every CRF stream advertises exactly the CRF media clock format")
def step_crf_format(context):
    got = _crf_streams(context)
    assert got, f"{context.cfg_name}: no CRF stream to check"
    for label, fmt in got:
        assert int(str(fmt), 16) == CRF_FORMAT, (
            f"{context.cfg_name}: the CRF {label} advertises {fmt}; Milan "
            f"v1.2 7.3.2 / Table 7.1 define exactly one CRF Media Clock "
            f"Stream Format, 0x{CRF_FORMAT:016X} (base frequency 48000 Hz, "
            f"1 timestamp per PDU, timestamp interval 96)")


@then("no CRF stream advertises an AAF Base format")
def step_crf_has_no_aaf(context):
    for label, fmt in _crf_streams(context):
        assert not _cover([fmt]), (
            f"{context.cfg_name}: the CRF {label} advertises the AAF Base "
            f"format {fmt}. Milan v1.2 5.3.3.4: a Stream Input/Output that "
            f"supports the CRF Media Clock Stream Format \"shall not support "
            f"the [...] AAF Audio Stream Format, and vice versa\".")


@when("a Stream Input's family is capped at 4 channels")
def step_cap_family(context):
    #: The pre-2026-08-14 bytes, restored by hand: 0x0215022001006000 is the
    #: ut entry at FOUR channels endstation_arty_4x4 used to carry.
    context.cfg["listeners"][0]["formats"] = ["0x0205022001006000",
                                              "0x0215022001006000"]


@then("the Base family check REPORTS the missing 6- and 8-channel formats")
def step_family_check_bites(context):
    miss = _missing(context.cfg["listeners"][0]["formats"])
    assert miss == {48000: [6, 8]}, (
        f"a 4-channel ut family reported {miss}, expected the 6- and "
        f"8-channel 48 kHz Base formats missing - the check has stopped "
        f"being able to say no")
