# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Executable channel-IDENTITY contract for the chmap64 CAPTURE mux
# (docs/CHANNEL_MAP_64.md Section 4/Section 5; RTL: hdl/ieee1722/aaf/KL_chan_map_capture.sv).
#
# WHY THIS LAYER EXISTS.  Every audio result this project has produced so far
# is PRESENCE-shaped: a counter moved, a frame arrived, audio was heard.  None
# of them can tell a correct channel map from one that swapped L and R,
# duplicated one channel over its neighbour, or dropped a channel silently -
# because the only multi-channel source the boards had emitted the SAME sample
# on every channel (the pilot tone is literally {tone, tone}) and the AX7101
# has no audio input at all.  The rx -> talker loopback is the first source
# that can carry per-channel-DISTINCT content, so it is the first time the
# identity property is testable - and this file states the property in terms
# of the STANDARD rather than of the RTL, so a model/RTL divergence shows up
# as a disagreement instead of as two copies of the same mistake.
#
# CLAUSES PINNED HERE
#   IEEE 1722-2016 7.3.3  channels_per_frame - the number of channels in the
#                         AAF-PCM payload, carried ON THE WIRE.  The
#                         de-interleave follows THIS, never the AEM store
#                         (the 1-to-1 wire-truth rule).
#   IEEE 1722-2016 7.3.5  the payload is a chronological sequence of sample
#                         events, each event carrying one sample per channel
#                         in channel order.  So payload sample k belongs to
#                         wire channel k mod channels_per_frame - THE one
#                         statement every identity check below rests on.
#   IEEE 1722.1-2021 7.2.19  AUDIO_MAP mapping entries are port-relative:
#                         (stream_index, stream_channel) -> (cluster_offset,
#                         cluster_channel).  The capture map is the egress
#                         mirror of that, at pair granularity (Section 4.2).
#   Milan v1.2 Section 5.4.2.27  dynamic audio maps are the canonical programmer of
#                         both map RAMs; the CSR 0x900 window is the debug
#                         override (Section 6/Section 7).

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from behave import given, when, then     # noqa: F401  (behave step decorators)

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context


# --- the Section 5 capture map word -------------------------------------------------
SRC_ZERO, SRC_I2S, SRC_TDM, SRC_RING, SRC_TONE, SRC_LOOP = range(6)


def csr_word(en: int, src: int, idx_hi: int, idx_lo: int) -> int:
    """The Section 5 CHMAP_WORD as typed at the bench:
    {EN[15], SRC[14:12], rsvd[11:8], IDX_HI[7:4], IDX_LO[3:0]}."""
    return (((en & 1) << 15) | ((src & 7) << 12)
            | ((idx_hi & 0xF) << 4) | (idx_lo & 0xF))


def cmap_entry(word: int) -> int:
    """What the CMAP RAM receives from that word:
    {idxh[11:8], en[7], src[6:4], idx[3:0]} - bits [7:0] are bit-for-bit the
    pre-loopback byte, so a word written before the loopback existed keeps its
    exact meaning and reads back with idxh = 0."""
    return ((((word >> 4) & 0xF) << 8)
            | (((word >> 15) & 1) << 7)
            | (((word >> 12) & 7) << 4)
            | (word & 0xF))


class CaptureMuxModel:
    """The capture mux as the STANDARD describes it, not as the RTL codes it.

    holds[(stream, pair)] = (L, R) is the latest-sample wire-truth latch of
    wire channels (2*pair, 2*pair+1) of that received stream - Section 9 latest-sample
    slip policy: a starved pair repeats, a fast one drops, nothing queues.
    """

    def __init__(self, slots=32, streams=8, channels=8):
        self.slots = slots
        self.streams = streams          # RX streams kept
        self.channels = channels        # wire channels kept per stream
        self.pairs_per_stream = channels // 2
        self.cmap = {}                  # slot -> 12-bit entry
        self.chan = {}                  # (stream, wire channel) -> sample
        # what the AEM store BELIEVES each stream's channel count is. Never
        # consulted by the de-interleave - it exists so a scenario can prove
        # that it is not consulted (the 1-to-1 wire-truth rule).
        self.aem_channels = {}

    # -- map programming (CSR 0x900 window / AEM projector) ------------------
    def write_word(self, slot: int, word: int) -> None:
        """Program one slot from a CSR 0x900 word, storing what the CMAP RAM
        would hold and not the word, so the packing is exercised every time."""
        self.cmap[slot] = cmap_entry(word)

    def entry(self, slot: int) -> int:
        """The 12-bit entry a slot holds. An unwritten slot reads 0, which is
        EN clear - a fresh fabric emits nothing rather than silence."""
        return self.cmap.get(slot, 0)

    # -- the received payload (depacketizer clone) ---------------------------
    def deliver_pdu(self, stream: int, wire_channels: int, samples: list[int]) -> int:
        """One AAF-PCM PDU of `stream`.  `samples` is the payload in wire
        order.  7.3.5: sample k is channel k mod channels_per_frame; 7.3.3:
        channels_per_frame is the WIRE's, and the pre-first-accept value 0
        means 'not yet known' which the fabric reads as 2."""
        chans = wire_channels if wire_channels != 0 else 2
        for k, smp in enumerate(samples):
            c = k % chans
            if c < self.channels:       # channels beyond the kept width are
                self.chan[(stream, c)] = smp   # virtual: counted, not stored
        return chans

    # -- one media tick: walk the slots low to high -------------------------
    def emit(self) -> dict[int, tuple[int, int] | None]:
        """slot -> (L, R) for every ENABLED slot.  A disabled slot is ABSENT
        from the result (it emits no pulse at all, Section 4: that is what stops a
        dead slot from skewing its stream's other channels); an enabled slot
        whose entry cannot be resolved emits SILENCE (0, 0)."""
        out = {}
        for slot in range(self.slots):
            e = self.cmap.get(slot, 0)
            if not (e >> 7) & 1:
                continue                       # en = 0 -> absence, not silence
            src = (e >> 4) & 7
            idx = e & 0xF
            idxh = (e >> 8) & 0xF
            if src != SRC_LOOP:
                out[slot] = None               # other buckets: not modelled
                continue
            if idxh >= self.streams or idx >= self.pairs_per_stream:
                out[slot] = (0, 0)             # illegal encoding -> silence
                continue
            left = self.chan.get((idxh, 2 * idx), 0)
            right = self.chan.get((idxh, 2 * idx + 1), 0)
            out[slot] = (left, right)
        return out


# --- helpers ----------------------------------------------------------------
def _sig(stream, channel, event):
    """A value that is DISTINCT for every (stream, channel, sample event).
    A test that drives the same value on two channels cannot detect a swap -
    which is precisely the hole this feature exists to close."""
    return 0x400000 | ((stream & 7) << 12) | ((channel & 0xF) << 4) | (event & 0xF)


def _pdu(stream, chans, events, e0):
    """A chronological, channel-interleaved payload (7.3.5)."""
    return [_sig(stream, c, e0 + e) for e in range(events) for c in range(chans)]


# --- steps ------------------------------------------------------------------
@given('a fabric capture mux with {slots:d} pair slots over {streams:d}'
       ' RX streams of {channels:d} channels')
def step_capture_mux(context: Context, slots: int, streams: int,
                     channels: int) -> None:
    """Build the fabric under test and drop anything an earlier step captured."""
    context.cap = CaptureMuxModel(slots=slots, streams=streams,
                                  channels=channels)
    context.captures = {}


@given('the AEM store believes RX stream {s:d} carries {n:d} channels')
def step_aem_belief(context: Context, s: int, n: int) -> None:
    """Record what the AEM store believes, so a scenario can prove it is never
    consulted: 7.3.3 gives the de-interleave the WIRE's count, not this one."""
    context.cap.aem_channels[s] = n


@when('RX stream {s:d} delivers a {chans:d}-channel PDU of {events:d}'
      ' sample events from event {e0:d}')
def step_deliver(context: Context, s: int, chans: int, events: int, e0: int) -> None:
    """Deliver one PDU in which every (stream, channel, event) carries a
    DISTINCT value, and keep its shape so a Then step knows which event is
    latest - a test driving one value everywhere cannot detect a swap."""
    context.cap.deliver_pdu(s, chans, _pdu(s, chans, events, e0))
    context.last_pdu = (s, chans, events, e0)


@when('RX stream {s:d} delivers a PDU carrying {chans:d} channels of samples'
      ' but declaring {wire:d} on the wire')
def step_deliver_mismatch(context: Context, s: int, chans: int, wire: int) -> None:
    """A payload that LOOKS `chans`-channel against a header declaring `wire`.
    7.3.3 gives the wire the last word, and this is where that is graded."""
    # the payload LOOKS 8-channel; 7.3.3 says the wire's count decides
    context.cap.deliver_pdu(s, wire, _pdu(s, chans, 2, 1))
    context.last_pdu = (s, chans, 2, 1)


@when('I map capture slot {slot:d} to RX stream {s:d} pair {p:d}')
def step_map_loop(context: Context, slot: int, s: int, p: int) -> None:
    """Point one enabled capture slot at an RX stream's channel pair."""
    context.cap.write_word(slot, csr_word(1, SRC_LOOP, s, p))


@when('I map capture slot {slot:d} to RX stream {s:d} pair {p:d} DISABLED')
def step_map_loop_dis(context: Context, slot: int, s: int, p: int) -> None:
    """The same mapping with EN clear - the slot that must emit no pulse at
    all, which is Section 4's other, and quieter, way to be silent."""
    context.cap.write_word(slot, csr_word(0, SRC_LOOP, s, p))


@when('I map capture slot {slot:d} to the pilot tone')
def step_map_tone(context: Context, slot: int) -> None:
    """Point a slot at the pilot tone: a source this loopback model does not
    resolve, so the slot reads as present-but-not-a-loopback-slot."""
    context.cap.write_word(slot, csr_word(1, SRC_TONE, 0, 0))


@when('the media tick walks the capture slots')
def step_tick(context: Context) -> None:
    """One media tick: walk the slots low to high and keep what each emitted."""
    context.emitted = context.cap.emit()


@then('capture slot {slot:d} carries RX stream {s:d} wire channels'
      ' {cl:d} and {cr:d}')
def step_slot_carries(context: Context, slot: int, s: int, cl: int, cr: int) -> None:
    """THE identity assertion: the slot carries the latest sample event of
    exactly those two wire channels of that stream. 7.3.5 is the whole of the
    expectation - payload sample k is wire channel k mod channels_per_frame -
    so a swapped, duplicated or dropped channel reads as a wrong value here."""
    got = context.emitted.get(slot)
    assert got is not None, f'slot {slot} emitted nothing'
    _, chans, events, e0 = context.last_pdu
    exp = (_sig(s, cl, e0 + events - 1), _sig(s, cr, e0 + events - 1))
    assert got == exp, (f'slot {slot}: got (0x{got[0]:06X}, 0x{got[1]:06X}), '
                        f'expected (0x{exp[0]:06X}, 0x{exp[1]:06X})')


@then('capture slot {slot:d} L and R are different')
def step_slot_distinct(context: Context, slot: int) -> None:
    """L and R differ, which is what separates a real stereo pair from one
    channel duplicated over its neighbour."""
    got = context.emitted.get(slot)
    assert got is not None, f'slot {slot} emitted nothing'
    assert got[0] != got[1], (f'slot {slot}: L == R == 0x{got[0]:06X} - a '
                              f'duplicated half is indistinguishable from a '
                              f'correct mono source, which is why every '
                              f'channel here carries a distinct value')


@then('capture slot {slot:d} is silent')
def step_slot_silent(context: Context, slot: int) -> None:
    """The slot pulses zeros: enabled, but its entry cannot be resolved."""
    got = context.emitted.get(slot)
    assert got is not None, f'slot {slot} emitted nothing (expected silence)'
    assert got == (0, 0), f'slot {slot}: expected silence, got {got}'


@then('capture slot {slot:d} emits nothing at all')
def step_slot_absent(context: Context, slot: int) -> None:
    """The slot does not pulse at all. That is what keeps a dead slot from
    skewing the rest of its stream, and it is not the same as silence."""
    assert slot not in context.emitted, (
        f'slot {slot} pulsed; a DISABLED slot must be absent from the walk, '
        f'not silent - Section 4 "two ways to be silent"')


@then('every emitted capture channel is distinct')
def step_all_distinct(context: Context) -> None:
    """No sample value repeats anywhere in the walk, so no two capture
    channels are carrying the same source."""
    vals = []
    for slot, pair in sorted(context.emitted.items()):
        assert pair is not None, f'slot {slot} is not a loopback slot'
        vals.extend(pair)
    dups = len(vals) - len(set(vals))
    assert dups == 0, (f'{dups} duplicated sample(s) across '
                       f'{len(vals)} emitted channels: {[hex(v) for v in vals]}')


@then('no emitted capture channel is silent')
def step_none_silent(context: Context) -> None:
    """No emitted half is zero: a dropped channel is precisely the failure a
    presence-shaped test reports as a pass."""
    for slot, pair in sorted(context.emitted.items()):
        assert pair is not None and pair[0] != 0 and pair[1] != 0, (
            f'slot {slot} has a silent half: {pair} - a dropped channel is '
            f'the failure mode a presence-shaped test cannot see')


@then('the capture entry at slot {slot:d} reads 0x{val:x}')
def step_entry_reads(context: Context, slot: int, val: int) -> None:
    """The CMAP RAM entry, pinned by value, so the word-to-entry packing is
    graded on its own and bits [7:0] keep their pre-loopback meaning."""
    got = context.cap.entry(slot)
    assert got == val, f'slot {slot}: entry 0x{got:03X}, expected 0x{val:03X}'


@then('the CSR word for RX stream {s:d} pair {p:d} is 0x{val:x}')
def step_word_is(context: Context, s: int, p: int, val: int) -> None:
    """The Section 5 CSR word as typed at the bench, pinned by value: a
    re-packing of the register shows up here rather than at the mux."""
    got = csr_word(1, SRC_LOOP, s, p)
    assert got == val, f'0x{got:04X} != 0x{val:04X}'


# --- the binary walking tone -------------------------------------------------
@when('I run a binary walking-tone identification over {n:d} channels'
      ' of RX stream {s:d}')
def step_walking_tone(context: Context, n: int, s: int) -> None:
    """Channel N is driven ON in capture round b iff bit b of N is set, so
    ceil(log2(n)) captures identify all n channels instead of n sweeps.  The
    identity read back per channel is the bit pattern of ITS OWN index - any
    swap makes two channels report each other's pattern, any duplication makes
    two report the same one, and a dead channel reports 0 in every round."""
    rounds = max(1, (n - 1).bit_length())
    observed = {c: 0 for c in range(n)}
    for b in range(rounds):
        # drive: channel c gets a non-zero sample in this round iff bit b set
        samples = []
        for e in range(2):
            for c in range(n):
                samples.append(_sig(s, c, e + 1) if (c >> b) & 1 else 0)
        context.cap.deliver_pdu(s, n, samples)
        emitted = context.cap.emit()
        for slot, pair in sorted(emitted.items()):
            if pair is None:
                continue
            e = context.cap.entry(slot)
            base = 2 * (e & 0xF)          # the pair this slot was mapped to
            for half, val in enumerate(pair):
                ch = base + half
                if ch < n and val != 0:
                    observed[ch] |= (1 << b)
    context.walk_rounds = rounds
    context.walk_observed = observed


@then('every channel reports its own index')
def step_walk_identity(context: Context) -> None:
    """Every channel reported the bit pattern of its OWN index. A foreign one
    is a swap, a repeated one a duplication, and 0 a dead channel."""
    bad = {c: v for c, v in context.walk_observed.items() if v != c}
    assert not bad, (f'walking tone: channels reporting a foreign index '
                     f'{ {c: hex(v) for c, v in bad.items()} } - a swap, a '
                     f'duplication or a dead channel')


@then('it took {n:d} captures')
def step_walk_rounds(context: Context, n: int) -> None:
    """The identification cost: ceil(log2(n)) captures rather than n sweeps."""
    assert context.walk_rounds == n, (
        f'{context.walk_rounds} captures, expected {n}')
