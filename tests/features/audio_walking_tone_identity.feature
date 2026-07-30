# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@torture @audio @identity @level:L3 @matrix:M-AAF-CHMAP
Feature: AUDIO IS NEVER FORGOTTEN - channel identity and a THD+N gate that measures
  Every audio result this project has ever recorded was PRESENCE-shaped: a
  counter moved, or audio was heard. Presence cannot tell a correct channel map
  from one that swapped two channels, duplicated one over its neighbour, or
  dropped one silently, and it cannot tell a clean converter from a noisy one.
  These scenarios are the two properties presence cannot see - IDENTITY and
  DISTORTION - written so they can be re-run every round and extended in one
  place.

  LEVEL / ORACLE (docs/testing/methodology.md). LEVEL 3 - conformance to the
  standard. ORACLE for identity: IEEE 1722-2016 7.3.5, encoded as hand-built
  payloads. ORACLE for THD+N: the DEFINITION of total harmonic distortion plus
  noise, implemented independently in these steps as an exact coherent DFT, and
  compared against the harness implementation the bench will actually use. Two
  implementations of one definition is the point: one is derived from the maths
  here and the other is the production analyser, and they have to agree.
  Structurally blind to: whether the fabric drives the pattern at all (that is
  L5, a real capture off a tap).

  METHODOLOGY R4 IN ONE SENTENCE - the shape of the test must match the shape of
  the property. Every sample driven here is DISTINCT per channel, because a
  pattern that drove equal values on two channels could not fail on a swap.
  That is not a stylistic preference: the only multi-channel source the boards
  had for months emitted the SAME sample on every channel (the pilot tone is
  {tone, tone}), which is exactly why identity was never observable before.

  THE WINDOW TRAP, and why it gets its own negative controls. The pilot tone is
  exact-period - 48 samples = 1 kHz at 48 kHz - so a capture truncated to whole
  periods is coherently sampled and its FFT has no leakage to suppress. Applying
  a window to a coherent tone spreads the fundamental across neighbouring bins,
  which a residual that excludes only the fundamental BIN then counts as
  distortion: it does not clean up the measurement, it MANUFACTURES the number
  it is supposed to measure. The reference result on this bench is -147.99 dBFS.
  Both failure modes are demonstrated below on synthetic data, with numbers.

  Clauses and definitions under test:
    IEEE 1722-2016 7.3.5 - the AAF PCM payload is a chronological sequence of
      sample frames, each carrying one sample per channel IN CHANNEL ORDER, so
      payload sample k belongs to wire channel k mod channels_per_frame.
    IEEE 1722-2016 7.3.3 - channels_per_frame is what the frame carries.
    IEEE 1722.1-2021 7.2.19 - AUDIO_MAP entries are port-relative
      (stream_index, stream_channel) -> (cluster_offset, cluster_channel).
    Milan v1.2 5.3.10.1 - "A PAAD-AE shall support changing mappings from a
      Stream Input at any time (even when it is bound)", and the mapping list
      "shall be saved in a non-volatile memory and restored after a power
      cycle".
    USER acceptance: THD+N <= -120 dBFS end to end; the digital source alone
      measures -147.99 dBFS, so the wire and ring path must add nothing.

  Background:
    Given the audio identity model is importable

  # --------------------------------------------------------------- identity
  @class:identity @clause:1722-7.3.5
  Scenario: a walking tone lands on the channel it was written to
    Given a 4-channel AAF frame carrying a walking tone
    When the identity check runs for 4 channels
    Then every identity verdict is PASS

  @class:identity @negative-control @clause:1722-7.3.5
  Scenario: two swapped channels are reported as CROSSED, not as "audio present"
    Given a 4-channel AAF frame whose channels 1 and 2 are swapped
    When the identity check runs for 4 channels
    Then the identity check reports FAIL on "uncrossed"

  @class:identity @negative-control
  Scenario: one channel duplicated over its neighbour is its own failure
    # The signature of a capture mux stuck on one pair. A level meter cannot
    # see it at all: both channels are loud and correct-looking.
    Given a 4-channel AAF frame where channel 0 is duplicated onto channel 1
    When the identity check runs for 4 channels
    Then the identity check reports FAIL on "no-duplicate-neighbour"

  @class:identity @negative-control
  Scenario: a dropped channel is reported as silent, not averaged away
    Given a 4-channel AAF frame where channel 2 was dropped
    When the identity check runs for 4 channels
    Then the identity check reports FAIL on "no-silent-channel"

  @class:identity @negative-control @clause:1722-7.3.3
  Scenario: a frame carrying fewer channels than expected fails the count check
    Given a 2-channel AAF frame carrying a walking tone
    When the identity check runs for 4 channels
    Then the identity check reports FAIL on "channel-count"

  # ------------------------------------------------- the channel-preserving loop
  #
  # THE RETURN LEG GOES THROUGH THE REAL DECODE PATH. It used to be a SHALLOW
  # dict copy of the sent samples - the same list objects - so the bit-exactness
  # assertion below compared a list with itself and could not fail, and there was
  # no negative counterpart. Now the samples are packed into an AAF frame built
  # from IEEE 1722-2016 Figure 26, decoded back through the production decoder,
  # and de-interleaved by channel_identity(), so a single altered sample reddens
  # it - which the next-but-one scenario proves.
  @class:identity @clause:Milan-5.3.10.1
  Scenario: a channel-preserving loop through the reference device is an identity test
    # USER directive: stream to the reference device's ch 1/2 and it returns on
    # ch 1/2. Because the peer is Milan-validated and we do not control its
    # firmware, the loop's oracle is a FOREIGN implementation (methodology L4),
    # which is the only kind of oracle that can find our own bugs.
    Given a walking tone sent on channels 1 and 2
    When the peer returns the same channels unchanged
    Then the loop is channel-preserving
    And the returned samples are bit-exact with the sent samples

  @class:identity @negative-control @clause:1722-7.3.5
  Scenario: ONE altered sample in the return leg is not bit-exact
    # The smallest possible corruption of an otherwise perfect loop: one sample,
    # one channel, +1. An assertion that cannot see this cannot see anything.
    Given a walking tone sent on channels 1 and 2
    When the peer returns the same channels with sample 3 of channel 2 altered by 1
    Then the returned samples are NOT bit-exact with the sent samples

  @class:identity @negative-control
  Scenario: a loop that returns the channels swapped is NOT channel-preserving
    Given a walking tone sent on channels 1 and 2
    When the peer returns the channels swapped
    Then the loop is not channel-preserving
    And the crossed channel pair is reported

  @class:identity @negative-control
  Scenario: a loop that returns different channels entirely is NOT channel-preserving
    # The failure a counter-only check calls a pass: frames arrive, counters
    # tick, and the audio came back on the wrong pair.
    Given a walking tone sent on channels 1 and 2
    When the peer returns channels 3 and 4 instead
    Then the loop is not channel-preserving

  @class:identity @clause:1722-7.3.5
  Scenario: the payload decode follows the WIRE channel count, never the store
    # 1-to-1 wire truth: de-interleaving by the AEM descriptor's channel count
    # instead of the frame's is how an 8-channel declaration reads a 2-channel
    # frame as garbage while every declaration still agrees with every other.
    Given a 2-channel AAF frame carrying a walking tone
    Then de-interleaving by the wire count yields 2 channels
    And de-interleaving by a declared count of 8 is refused

  # ------------------------------------------------------------------ THD+N
  @class:thdn @clause:definition
  Scenario: the independent reference reads the numerical floor on a pure coherent tone
    Given a synthetic 1 kHz tone of 480 samples at 48 kHz
    When the reference THD+N is measured coherently without a window
    Then the reference THD+N is at most -200 dB

  @class:thdn @clause:definition @negative-control
  Scenario: the reference MEASURES distortion rather than always returning a tiny number
    # A measurement that only ever reports the floor is not a measurement. A
    # known third harmonic has to come back at its known level.
    Given a synthetic 1 kHz tone of 480 samples at 48 kHz with a -60 dB third harmonic
    When the reference THD+N is measured coherently without a window
    Then the reference THD+N is -60 dB within 1 dB

  @class:thdn @negative-control @regression
  Scenario: windowing a coherent tone MANUFACTURES distortion
    # Hann spreads the fundamental into the two neighbouring bins. A residual
    # that excludes only the fundamental bin counts that spread as distortion
    # and reports about -3 dB on a mathematically perfect sine.
    Given a synthetic 1 kHz tone of 480 samples at 48 kHz
    When the reference THD+N is measured with a Hann window excluding only the fundamental bin
    Then the reference THD+N is worse than -10 dB
    And the un-windowed measurement of the SAME samples is at most -200 dB

  @class:thdn @negative-control @regression
  Scenario: a capture not truncated to whole periods MANUFACTURES distortion too
    # 500 samples is 10.4 periods, so the tone is not bin-centred and leaks
    # across the whole spectrum. Truncating the SAME capture to 480 samples -
    # ten whole periods - reads the floor. This is why the analyser truncates
    # rather than trusting the caller.
    Given a synthetic 1 kHz tone of 500 samples at 48 kHz
    When the reference THD+N is measured without truncating to whole periods
    Then the reference THD+N is worse than -30 dB
    When the reference THD+N is measured coherently without a window
    Then the reference THD+N is at most -200 dB

  @class:thdn @clause:definition @honesty
  Scenario: the production analyser states the coherence preconditions it will not measure without
    # harness/milanharness/thdn.py raises rather than measuring when
    # rate % f0 != 0 or fewer than 8 whole periods are present: the un-windowed
    # method does not apply, and returning a number anyway would be the
    # manufactured measurement above with no warning.
    #
    # RECORDED, not glossed: both guards sit AFTER that function's numpy
    # import, so on a host without numpy they cannot fire - the caller gets an
    # ImportError instead of the precondition message, although the module's own
    # docstring says numpy is needed "here and NOWHERE else ... so a host
    # without it still runs every other phase". The assertions below are
    # therefore STRONGER where numpy exists and still honest where it does not,
    # and the ordering is handed back as a finding rather than fixed in passing
    # (methodology section 5: record it, do not detour).
    Then 44100 Hz with a 1000 Hz tone is not an integer number of samples per period
    And the production THD+N analyser carries both coherence guards in its source
    And the production THD+N analyser refuses an incoherent rate where numpy exists
    And the production THD+N analyser refuses a capture shorter than 8 periods where numpy exists

  # -------------------------------------------------------- the THD+N gate
  @class:thdn @clause:USER-acceptance
  Scenario Outline: the acceptance gate picks the WORST channel, and clipping invalidates
    Given a THD+N result set <results>
    Then the THD+N gate verdict is <verdict> because <why>

    Examples:
      | results       | verdict | why                                    |
      | -140 and -135 | PASS    | the worst channel is inside -120       |
      | -140 and -100 | FAIL    | one bad channel fails the set          |
      | -140 clipped  | FAIL    | a clipped capture is not a measurement |
      | empty         | FAIL    | nothing analysed is not a pass         |

  # ----------------------------------------------------- L1: the bindings
  @level:L1 @class:binding
  Scenario: the production analyser applies no window, and says why in its own source
    # An L1 check: it asks whether the production code is still bound to the
    # method these scenarios validate. A window silently reintroduced would
    # make every future THD+N number worse by construction and nothing else in
    # the tree would notice.
    Then the harness THD+N module states that it applies NO WINDOW
    And the harness THD+N module truncates to whole periods
    And the harness THD+N module excludes DC and the fundamental skirt
    And the harness THD+N module treats a clipped capture as invalid

  @level:L1 @class:binding
  Scenario: the campaign plan carries the audio steps, so a round cannot skip them
    Then the campaign audio area has an identity step
    And the campaign audio area has a per-channel-distinct pattern
    And the campaign audio area has a THD+N step that reuses the harness analyser
    And the campaign audio area has a channel-preserving loop through the peer

  @level:L1 @class:binding @rule:never-index-0-only
  Scenario: the audio area walks every index, and the audit is PER AREA so it can say no
    # The audio area was index-0-only (talker 0, peer listener 0, peer talker 0)
    # and the coverage audit reported success, because it was computed over the
    # WHOLE plan and the matrix area's full coverage masked it. Index 0 is the
    # LEAST representative index on this fabric: the 0x800 window makes it a hard
    # alias of the legacy flat registers, which is how four separate per-index
    # defects hid. A CRF Media Clock Stream carries timestamps and not audio
    # samples, so the audio expectation is every AAF index and the CRF index is
    # deliberately out of scope here - stated, not assumed.
    Then the campaign audio area walks every AAF talker index
    And the campaign audio area covers more than index 0
    And the per-area audit reddens on an index-0-only audio area
