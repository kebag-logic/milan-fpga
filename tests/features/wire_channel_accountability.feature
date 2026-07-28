# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: the ADVERTISED stream format must be one the fabric EMITS.
# Spec refs: IEEE 1722-2016 §7.3.3 (AAF channels_per_frame), §7.3.4 (bit_depth),
#            §7.3.5 (interleaved payload); IEEE 1722.1-2021 §7.2.6 (STREAM
#            descriptor current_format / formats); Milan v1.2 §5.5.1.2 (the
#            talker/listener format compatibility check ACMP runs).
#
# WHY THIS FEATURE EXISTS.  On 2026-07-27 every gate in this repo was green -
# 57/57 Verilator suites, yosys 48/48, behave 113/113, lint at ratchet - and the
# AX7101's eight talkers advertised 0x0205022002006000 (AAF PCM32 48 kHz, EIGHT
# channels) while the framer emitted STEREO.  Every one of those gates compares
# a declaration against ANOTHER declaration.  A Milan-validated PEER bound to
# talker 0, PASSED the Milan 5.5.1.2 format check, returned ACMP SUCCESS with a
# correct MAAP dmac and a 137042 ns MSRP latency - and then counted
# UNSUPPORTED_FORMAT on 296,294 of 296,294 frames.  Into a 2-channel sink the
# same talker counted ZERO over 1,491,239 frames, so the framer's width was
# proven in BOTH directions.
#
# These scenarios are the CONFORMANCE-SUITE half of that accounting: they run
# the same derivation scripts/check_wire_accountability.py runs, over the real
# shipping configs, and they include the negative controls that prove the
# derivation can say "no".  The RUNTIME half is hive_compliance.py check C6,
# which binds a real listener and reads its UNSUPPORTED_FORMAT counter.
#
# LEVEL / ORACLE (docs/testing/methodology.md):
#   LEVEL 3 - conformance to the standard.  ORACLE: THE CLAUSE.  IEEE 1722-2016
#   7.3.3 says channels_per_frame is what the frame carries; the entity's
#   advertised format states what a listener will be handed.  What is compared
#   here is a DECLARATION against a CAPABILITY DERIVED FROM RTL (which capture
#   front-end is elaborated and how many pair slots it drives), not against
#   another declaration - that distinction is the whole of item 00.
#   The last scenario is LEVEL 1: it asserts the ENFORCEMENT exists in the
#   fabric, so the constant cannot be raised past what the front-end feeds.
#   Two NEGATIVE CONTROLS are mandatory here and both are present: a config
#   that must come out clean (arty_current, which streams to the PEER with
#   zero unsupported-format frames) and a fabric state that must come out
#   dirty (the TDM bus unbacked, which is the 2026-07-27 gateware).

@item00 @wire_accountability @spec:1722-7.3.3
Feature: Advertised channels_per_frame is a width the fabric can emit

  Background:
    Given the end-station builder is importable

  Scenario: the shipping stereo config is self-consistent (negative control)
    # endstation_arty_current streams to the PEER with ZERO unsupported-format
    # frames. A check that only ever fails proves as little as one that only
    # ever passes, so this config MUST come out clean.
    Given the end-station config "endstation_arty_current"
    Then every AAF talker format's channels_per_frame equals the emitted width

  Scenario: the 8x8 config advertises 8 channels and the fabric emits 8
    Given the end-station config "endstation_ax7101_8x8"
    Then the declared talker width is 8 channels
    And every AAF talker format's channels_per_frame equals the emitted width

  Scenario: the 4x4 config advertises 4 channels and the fabric emits 4
    Given the end-station config "endstation_arty_4x4"
    Then the declared talker width is 4 channels
    And every AAF talker format's channels_per_frame equals the emitted width

  Scenario Outline: the generated wire constant matches the derivation
    # TALKER_WIRE_CHANS_C is what milan_datapath elaborates and what
    # KL_aaf_packetizer resets every talker's chans field from - so a stale
    # value here IS a wrong channels_per_frame on the wire.
    Given the end-station config "<config>"
    Then the generated TALKER_WIRE_CHANS_C equals the emitted width

    Examples:
      | config                  |
      | endstation_arty_current |
      | endstation_arty_4x4     |
      | endstation_ax7101_8x8   |

  Scenario: an unbacked audio interface does not silently change the gateware
    # USER 2026-07-27, "the tdm can be a placeholder": declaring the interface
    # the product will have is legitimate. What is not legitimate is letting
    # the declaration elaborate a front-end on a bus nothing drives - those
    # talkers emit NO FRAME AT ALL. With the TDM bus unbacked the build must
    # fall back to the front-end the board really has.
    Given the end-station config "endstation_ax7101_8x8"
    When the TDM bus is not backed by the fabric
    Then the audio interface is reported as a placeholder
    And the emitted width falls back to 2 channels

  Scenario: with the TDM master present the interface is backed
    # KL_tdm_capture_master GENERATES bclk/fsync, so it needs nobody to drive
    # it - that is what turns the declaration into a fabric fact.
    Given the end-station config "endstation_ax7101_8x8"
    When the TDM bus is backed by the fabric
    Then the audio interface is not a placeholder
    And the soc argv carries "--audio-interface"
    And the soc argv carries "--audio-interface-master"

  Scenario: the derivation REFUSES to over-declare (negative control)
    # The failure mode the master introduced: the supply jumped from 1 pair to
    # 16, and an uncapped derivation would have made a 4-channel config EMIT 8.
    # That is the same defect mirrored, and just as invisible to a listener
    # until it counted its discards.
    Given the end-station config "endstation_arty_4x4"
    When the TDM bus is backed by the fabric
    Then the front-end supplies at least 4 pair slots
    And the emitted width is still 4 channels

  Scenario: the derivation REFUSES to under-declare silently (negative control)
    # And the original defect, reproduced on demand: an 8-channel declaration
    # on a one-pair front-end must be REPORTED as a mismatch, not rounded away.
    Given the end-station config "endstation_ax7101_8x8"
    When the TDM bus is not backed by the fabric
    Then at least one AAF talker format's channels_per_frame differs from the emitted width

  Scenario: the elaboration guard is the enforcement, not a comment
    # TALKER_WIRE_CHANS_P must not be raisable past what the capture front-end
    # feeds - otherwise it becomes one more declaration agreeing with the other
    # declarations, which is exactly the state that shipped.
    Then milan_datapath refuses a wire width its capture front-end cannot feed
    And milan_datapath refuses a TDM master clock that is not an exact multiple
    And KL_aaf_packetizer resets every talker's chans field from the constant
