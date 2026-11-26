# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_leds_mutants.py - the AECP campaign's planted defects in the status LEDs the firmware owns (#1018,
plat/ctrl_plat_leds.h): LD3 on for an INTERNAL clock source; for an INPUT_STREAM source on only while the STREAM_INPUT
it names is bound with its media locked and the clock domain locked; a lock state the parity of its two counters; LD2
on for a bound and receiving STREAM_INPUT or a STREAM_OUTPUT with a Listener. aecp_mutants.py plants each row; every
named check must fail on its own words."""

INTERNAL = 'Leds.ClockSourceInternalLightsLd3'
FLOWING = 'Leds.FollowingAFlowingStreamLightsLd3'
STOPPED = 'Leds.FollowingAStoppedStreamDarkensLd3'
LD2 = 'Leds.Ld2IsABoundReceivingInputOrAListenedOutput'
LEDS = 'plat/ctrl_plat_leds.h'

ROWS = (
    ('leds-internal-source-dark', LEDS,
     '\tif (kind == CTRL_PLAT_LEDS_INTERNAL) {\n\t\tword |= CTRL_PLAT_LEDS_CLOCK;',
     '\tif (kind == CTRL_PLAT_LEDS_INTERNAL) {\n\t\tword |= 0u;',
     (INTERNAL, 'internal: LD3 on')),
    ('leds-stream-source-without-the-domain-lock', LEDS,
     'ctrl_plat_leds_receiving(a, index) && domain_locked) {',
     'ctrl_plat_leds_receiving(a, index)) {',
     (FLOWING, 'the media clock not recovered: LD3 off')),
    ('leds-stream-source-not-the-named-input', LEDS,
     'ctrl_plat_leds_receiving(a, index) && domain_locked) {',
     'ctrl_plat_leds_receiving(a, (uint16_t)(index + 1u)) && domain_locked) {',
     (FLOWING, 'following a flowing stream, recovered: LD3 on')),
    ('leds-lock-read-as-a-comparison', LEDS,
     'return ((c.value[0] - c.value[1]) & 1u) != 0u;',
     'return c.value[0] > c.value[1];',
     (FLOWING, 'LOCKED - UNLOCKED odd across the wrap: locked')),
    ('leds-receiving-without-the-media-lock', LEDS,
     '\treturn ctrl_plat_leds_locked(a, CTRL_PLAT_LEDS_STREAM_INPUT, index);',
     '\treturn true;',
     (STOPPED, 'following a stream that stopped: LD3 off'), (LD2, 'bound, not receiving: LD2 off')),
    ('leds-receiving-unbound', LEDS,
     ' || !s.bound) return false;',
     ') return false;',
     (STOPPED, 'following an unbound stream: LD3 off'), (LD2, 'receiving, unbound: LD2 off')),
    ('leds-ld2-ignores-the-outputs', LEDS,
     '(s.flags_ex & 1u) != 0u;',
     '(s.flags_ex & 1u) != 0u && false;',
     (LD2, 'with a Listener: LD2 on')),
    ('leds-ld2-ignores-the-inputs', LEDS,
     '\t\tif (ctrl_plat_leds_receiving(a, i)) {\n\t\t\tword |= CTRL_PLAT_LEDS_STREAM;',
     '\t\tif (ctrl_plat_leds_receiving(a, i)) {\n\t\t\tword |= 0u;',
     (LD2, 'bound and receiving: LD2 on')),
)
