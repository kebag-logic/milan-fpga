# SPDX-License-Identifier: MIT
# usage: add_plants.py MUTATIONS_JSON  (round 4: registers the new owed-bound plants after owed-held-flag-kept)
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
ms = json.loads(p.read_text())
O = 'AcmpOwed.'
def plant(name, path, old, new, kills):
    return {'name': name, 'path': path, 'old': old, 'new': new,
            'kills': [{'test': O + t, 'needle': n} for t, n in kills],
            'original_tests': [O + t for t, _ in kills]}
PROBES = '\tbool probes = kind == ACMP_TIMER_DELAY || (kind == ACMP_TIMER_NO_RESP && s->state == ACMP_PRB_W_RESP);'
SCAN = '\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k) {\n\t\tif (a->sinks[k].probe_held) {'
ROOM = '\t\tif (listener && !room(a, cmd.msg == ACMP_MSG_BIND_RX_COMMAND ? OWED_BY_BIND : 1u)) {'
new = [
    plant('owed-bind-wait-cleared-by-refused-poll', 'src/acmp.c',
          '\tif (a->owed_count != 0u) {\n\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];',
          '\ta->bind_waiting = false;\n\tif (a->owed_count != 0u) {\n\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];',
          [('RefusedPollLeavesTheBindWaitingAndItsHold', 'a refused acmp_poll frees nothing and leaves bind_waiting set'),
           ('RefusedPollLeavesTheBindWaitingAndItsHold', 'no probe leaves ahead of the BIND_RX answer after a refused poll')]),
    plant('owed-bind-wait-set-at-full', 'src/acmp.c',
          '\t\t\tif (cmd.msg == ACMP_MSG_BIND_RX_COMMAND && a->owed_count < ACMP_OWED_MAX) {',
          '\t\t\tif (cmd.msg == ACMP_MSG_BIND_RX_COMMAND) {',
          [('BindDeclinedBehindTheFullSetHoldsNoProbe', 'a BIND_RX declined with no slot free does not set bind_waiting'),
           ('BindDeclinedBehindTheFullSetHoldsNoProbe', 'is lost and counted, and its timeout runs')]),
    plant('owed-hold-widened-to-second-no-resp', 'src/acmp.c', PROBES,
          '\tbool probes = kind == ACMP_TIMER_DELAY || kind == ACMP_TIMER_NO_RESP;',
          [('OnlyTimerProbesAreHeldBesideTheWaitingBind', 'the TMR_NO_RESP that ends PRB_W_RESP2 is not held beside a waiting BIND_RX'),
           ('OnlyTimerProbesAreHeldBesideTheWaitingBind', 'no expiry that sends no probe is held or counted in probes_held')]),
    plant('owed-hold-widened-to-every-timer', 'src/acmp.c', PROBES,
          '\tbool probes = kind != ACMP_TIMER_NONE;',
          [('OnlyTimerProbesAreHeldBesideTheWaitingBind', 'the TMR_NO_RESP that ends PRB_W_RESP2 is not held beside a waiting BIND_RX'),
           ('OnlyTimerProbesAreHeldBesideTheWaitingBind', 'a TMR_RETRY expiry is not held beside a waiting BIND_RX'),
           ('OnlyTimerProbesAreHeldBesideTheWaitingBind', 'a TMR_NO_TK expiry is not held beside a waiting BIND_RX')]),
    plant('owed-rebind-keeps-the-hold', 'src/acmp.c',
          '\tdisc_stop(s);\n\tsm_stop(s);\n\ts->bound = true;',
          '\tdisc_stop(s);\n\tbool kept_hold = s->probe_held;\n\tsm_stop(s);\n\ts->probe_held = kept_hold;\n\ts->bound = true;',
          [('BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces', 'a BIND_RX to another talker ends the hold of the probe it replaces'),
           ('BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces', 'the next retry that finds every slot owed is lost')]),
    plant('owed-probe-held-never-set', 'src/acmp.c',
          '\t\ts->probe_held = true;\n', '\t\ts->probe_held = false;\n',
          [('ProbesFallingDueInTheDrainWaitForTheDeferredBind', 'no probe held for the deferred BIND_RX is lost'),
           ('HoldEndsWithTheLastHeldProbe', 'the retry falling due beside the deferred BIND_RX is held, not owed')]),
    plant('owed-hold-scan-skips-the-last-sink', 'src/acmp.c', SCAN,
          '\tfor (unsigned k = 0; k + 1u < a->cfg.n_sinks; ++k) {\n\t\tif (a->sinks[k].probe_held) {',
          [('ProbesFallingDueInTheDrainWaitForTheDeferredBind', 'no probe held for the deferred BIND_RX is lost')]),
    plant('owed-hold-whenever-full', 'src/acmp.c',
          SCAN + '\n\t\t\treturn true;\n\t\t}\n\t}\n\treturn false;\n}', '\treturn true;\n}',
          [('HoldEndsWithTheLastHeldProbe', 'a retry that finds every slot owed is lost and counted'),
           ('BindDeclinedBehindTheFullSetHoldsNoProbe', 'is lost and counted, and its timeout runs'),
           ('BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces', 'the next retry that finds every slot owed is lost')]),
    plant('owed-hold-at-seven', 'src/acmp.c',
          '\tif (a->owed_count < ACMP_OWED_MAX) {\n\t\treturn false;',
          '\tif (a->owed_count + 1u < ACMP_OWED_MAX) {\n\t\treturn false;',
          [('ProbesFallingDueInTheDrainWaitForTheDeferredBind', 'one pass per probe before it')]),
    plant('owed-answered-bind-takes-one-slot', 'src/acmp.c', ROOM,
          '\t\tif (listener && !room(a, cmd.msg == ACMP_MSG_BIND_RX_COMMAND && cmd.listener_uid < a->cfg.n_sinks ? OWED_BY_BIND : 1u)) {',
          [('AnsweredOnlyBindAlsoWaitsForTwoSlots', 'a BIND_RX that is only answered also waits for two free owed slots')]),
    plant('owed-entry-widened', 'include/acmp.h',
          '\tuint8_t probe_of;\n\tuint32_t release;', '\tuint8_t probe_of;\n\tuint64_t release;',
          [('OwedSetIsEightFramesOfEightyBytes', 'the owed set holds eight frames of 80 bytes, 640 bytes')]),
    plant('owed-deferred-answer-error-status', 'src/acmp.c',
          '\tstruct pdu r = echo(cmd, ACMP_STATUS_SUCCESS);\n\tr.talker = s->binding.talker_entity_id;',
          '\tstruct pdu r = echo(cmd, a->busy_declined != 0u ? ACMP_STATUS_NOT_SUPPORTED : ACMP_STATUS_SUCCESS);\n\tr.talker = s->binding.talker_entity_id;',
          [('HeldEgressDefersTheCommandBehindTheOwedSet', 'its answer is the Milan Table 5.34 response, not an error status')]),
]
names = {m['name'] for m in ms}
assert not names & {m['name'] for m in new}
at = [m['name'] for m in ms].index('owed-held-flag-kept') + 1
ms[at:at] = new
for m in ms:
    for k in m['kills']:
        if k['needle'] == 'each pass that holds a probe counts once':
            k['needle'] = 'each held probe counts once for each pass it is held'
    if m['name'] == 'acmp-probe-before-response':
        m['kills'].append({'test': O + 'DeferredBindWaitsForTwoSlotsAndLosesNoProbe',
                           'needle': 'the first probe leaves at once, in the pass after the BIND_RX answer'})
        m['original_tests'].append(O + 'DeferredBindWaitsForTwoSlotsAndLosesNoProbe')
p.write_text(json.dumps(ms, indent=2) + '\n')
print(len(ms))
