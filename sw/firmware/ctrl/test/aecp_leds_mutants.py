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
    ('leds-output-observation-brief', 'plat/ctrl_plat_leds_ports.h',
     'return adapter->environment->stream(owner, interface, type, index, out);',
     'out->brief = true; return adapter->environment->stream(owner, interface, type, index, out);',
     ('App.LedsReadTheAcmpBindingWithoutTheStreamWindow', 'LED output keeps the full observation')),
    ('leds-binding-accepts-past-the-end', 'plat/ctrl_plat_leds_ports.h',
     'index >= acmp->cfg.n_sinks', 'index > acmp->cfg.n_sinks',
     ('App.LedsReadTheAcmpBindingWithoutTheStreamWindow', 'LED input index follows ACMP')),
    ('leds-bound-through-unused-stream-window', 'plat/ctrl_plat_leds_ports.h',
     'if (type == CTRL_PLAT_LEDS_STREAM_INPUT) {', 'if (false) {',
     ('App.LedsReadTheAcmpBindingWithoutTheStreamWindow', 'called more times than expected')),
    ('leds-binding-reads-next-sink', 'plat/ctrl_plat_leds_ports.h',
     'out->bound = acmp->sinks[index].bound;', 'out->bound = acmp->sinks[index + 1u].bound;',
     ('App.LedsReadTheAcmpBindingWithoutTheStreamWindow', "LED bound bit is the ACMP owner's state")),

    ('leds-internal-reads-unused-lock', LEDS,
     'kind != CTRL_PLAT_LEDS_INTERNAL &&', 'true &&',
     (INTERNAL, 'called more times than expected')),
    ('leds-counter-pair-omits-validity', LEDS,
     'const uint32_t words[] = {0u, 1u, 32u};',
     'const uint32_t words[] = {0u, 1u, 2u};',
     ('Face.LedsReadOnlyTheLockPairAndValidity', 'LOCKED, UNLOCKED and validity selectors')),
    ('leds-counter-pair-reads-unused-words', LEDS,
     'for (unsigned n = 0u; n < 3u; ++n) {',
     'for (unsigned unused = 2u; unused < 32u; ++unused) {\n'
     '        uint64_t ignored = 0u; request[1] = unused;\n'
     '        (void)mbx_win_read(interface, MBX_WIN_CTR, request, &ignored);\n'
     '    }\n\tfor (unsigned n = 0u; n < 3u; ++n) {',
     ('Face.LedsReadOnlyTheLockPairAndValidity', 'LED observation reads exactly three counter words')),
    ('leds-counter-pair-wrong-unlock', LEDS,
     'const uint32_t words[] = {0u, 1u, 32u};',
     'const uint32_t words[] = {0u, 0u, 32u};',
     ('Face.LedsReadOnlyTheLockPairAndValidity', 'LED counter request preserves interface, descriptor and word')),
    ('leds-counter-pair-ignores-timeout', LEDS,
     'if (mbx_win_read(interface, MBX_WIN_CTR, request, &value) != MBX_STATUS_OK) return false;',
     '(void)mbx_win_read(interface, MBX_WIN_CTR, request, &value);',
     ('Face.LedsRefuseEveryUnansweredCounterWord', 'no read follows a failed LED word')),
    ('leds-counter-pair-ignores-validity', LEDS,
     ' || (c.valid & 3u) != 3u', '',
     ('Leds.BothLockCountersMustBeValid', 'both lock counters must be valid')),

    ('leds-external-without-domain-lock', LEDS,
     'kind == CTRL_PLAT_LEDS_EXTERNAL && domain_locked',
     'kind == CTRL_PLAT_LEDS_EXTERNAL',
     ('Leds.ExternalSourceRequiresDomainLock', 'external unlocked: LD3 off')),
    ('leds-internal-source-dark', LEDS,
     '\tif (kind == CTRL_PLAT_LEDS_INTERNAL) {\n\t\tword |= CTRL_PLAT_LEDS_CLOCK;',
     '\tif (kind == CTRL_PLAT_LEDS_INTERNAL) {\n\t\tword |= 0u;',
     (INTERNAL, 'internal: LD3 on')),
    ('leds-stream-source-without-the-domain-lock', LEDS,
     'ctrl_plat_leds_receiving(a, counters, stream, index) && domain_locked) {',
     'ctrl_plat_leds_receiving(a, counters, stream, index)) {',
     (FLOWING, 'the media clock not recovered: LD3 off')),
    ('leds-stream-source-not-the-named-input', LEDS,
     'ctrl_plat_leds_receiving(a, counters, stream, index) && domain_locked) {',
     'ctrl_plat_leds_receiving(a, counters, stream, (uint16_t)(index + 1u)) && domain_locked) {',
     (FLOWING, 'following a flowing stream, recovered: LD3 on')),
    ('leds-lock-read-as-a-comparison', LEDS,
     'return ((c.value[0] - c.value[1]) & 1u) != 0u;',
     'return c.value[0] > c.value[1];',
     (FLOWING, 'LOCKED - UNLOCKED odd across the wrap: locked')),
    ('leds-receiving-without-the-media-lock', LEDS,
     '\treturn ctrl_plat_leds_locked(a, counters, CTRL_PLAT_LEDS_STREAM_INPUT, index);',
     '\t(void)counters; return true;',
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
     '\t\tif (ctrl_plat_leds_receiving(a, counters, stream, i)) {\n\t\t\tword |= CTRL_PLAT_LEDS_STREAM;',
     '\t\tif (ctrl_plat_leds_receiving(a, counters, stream, i)) {\n\t\t\tword |= 0u;',
     (LD2, 'bound and receiving: LD2 on')),
)
