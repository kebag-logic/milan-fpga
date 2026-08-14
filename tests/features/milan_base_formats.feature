# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD feature: Milan v1.2 Section 6 "Base Stream Formats" against the shipping
# end-station configs.
# Spec refs: Milan v1.2 6.2 + Table 6.1 (Base Format Type: AAF PCM, 32-bit,
#            SR in {48, 96, 192} kHz, N in {1, 2, 4, 6, 8} channels, NS =
#            6/12/24 samples per PDU), Table 6.2 (the fifteen format strings),
#            6.3 (Talker requirements), 6.4 (Listener requirements), 6.5 (the
#            "up to" bit recommendation), 5.3.3.3 (AUDIO_UNIT sampling rates),
#            5.3.3.4 (STREAM_INPUT/OUTPUT, incl. CRF/AAF exclusivity);
#            IEEE 1722-2016 Annex I.2.4 (the AAF stream format and its ut bit).
#
# WHY THIS FEATURE EXISTS.  Milan 6.4 obliges a Stream Input that advertises
# ONE 48 kHz Base format to advertise them ALL, and 6.2 fixes what "all" means:
# channel counts 1, 2, 4, 6 and 8.  endstation_arty_4x4 spelled that family out
# by hand as an "up to" entry capped at FOUR channels, so its four Stream
# Inputs advertised counts 1, 2 and 4 and left the 6- and 8-channel 48 kHz Base
# formats unadvertised - in a file where the encoding sits one character away
# from the right one, and where nothing on the bench can see the difference
# until a controller refuses a connection.  The completion is derived now
# (endstation_builder.base_format_complete); these scenarios are the
# conformance-suite half of that, run over the real shipping configs.
#
# THE ASYMMETRY IS THE CLAUSE, not an oversight.  Milan 6.3 is the whole of
# what a Base Talker owes and it ends "A PAAD-AE Base Talker may advertise any
# Base Format that is reasonable for its functionality".  There is no
# all-channel-counts rule and no cross-Stream-Output rate rule anywhere in
# Section 6, and a talker could not honour a wider claim in any case: it emits
# one width and SET_STREAM_FORMAT on a STREAM_OUTPUT answers NOT_SUPPORTED
# (FR-STR-03 makes format adaptivity a LISTENER requirement).
#
# LEVEL / ORACLE (docs/testing/methodology.md):
#   LEVEL 3 - conformance to the standard.  ORACLE: THE CLAUSE.  The five
#   48 kHz format strings the steps compare against are transcribed from Milan
#   Table 6.2, not computed by the code under test.
#   A NEGATIVE CONTROL is mandatory and present: the last scenario takes a
#   Stream Input's family away and requires the check to say so.

@milan @base_formats @spec:milan-6.4
Feature: Every Stream Input advertises the whole Base format family

  Background:
    Given the end-station builder is importable

  Scenario Outline: <config> completes the 48 kHz Base family on every Stream Input
    Given the end-station config "<config>"
    Then every Stream Input advertises all five 48 kHz Base channel counts
    And every Stream Input advertises the same Base sampling rates
    And every advertised Base sampling rate is one the AUDIO_UNIT reports

    Examples:
      | config                        |
      | endstation_arty_current       |
      | endstation_arty_4x4           |
      | endstation_arty_8ch           |
      | endstation_ax7101_8x8         |
      | endstation_ax7101_1x1_tdm8    |

  Scenario Outline: <config> leaves its Stream Outputs at wire truth (Milan 6.3)
    # 6.3 asks for one Stream Output advertising a Base format and nothing
    # more; the width a Stream Output declares is what the framer emits.
    Given the end-station config "<config>"
    Then at least one Stream Output advertises a Base format
    And no Stream Output advertises more than one Base channel count

    Examples:
      | config                        |
      | endstation_arty_current       |
      | endstation_arty_4x4           |
      | endstation_ax7101_8x8         |
      | endstation_ax7101_1x1_tdm8    |

  Scenario Outline: <config> keeps the CRF media clock streams out of the family
    # Milan 5.3.3.4: a Stream Input/Output supporting the CRF Media Clock
    # Stream Format shall not support the AAF Audio Stream Format, and vice
    # versa - so 6.4's family rule, which is scoped to "all the Stream Input
    # which advertise support for a Base format", never reaches them.
    Given the end-station config "<config>"
    Then every CRF stream advertises exactly the CRF media clock format
    And no CRF stream advertises an AAF Base format

    Examples:
      | config                        |
      | endstation_arty_current       |
      | endstation_arty_4x4           |
      | endstation_ax7101_8x8         |
      | endstation_ax7101_1x1_tdm8    |

  Scenario: a Stream Input short of the family is REPORTED (negative control)
    # The 2026-08-14 defect verbatim: an "up to" entry capped at four channels
    # advertises Base counts 1, 2 and 4 only. A check that only ever passes
    # proves as little as one that only ever fails.
    Given the end-station config "endstation_arty_4x4"
    When a Stream Input's family is capped at 4 channels
    Then the Base family check REPORTS the missing 6- and 8-channel formats
