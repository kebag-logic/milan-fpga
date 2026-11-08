# SPDX-License-Identifier: MIT
# usage: make_step.py FINAL_DIR TREE STEP   (writes the round 4 step 1, 2 or 3 versions of the changed files into TREE)
import json, re, sys
from pathlib import Path
final, tree, step = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
files = {str(p.relative_to(final)): p.read_text() for p in final.rglob('*') if p.is_file()}
def rep(name, a, b):
    t = files[name]
    assert t.count(a) == 1, (name, a[:60], t.count(a))
    files[name] = t.replace(a, b)
NEW_TESTS = ['OwedSetIsEightFramesOfEightyBytes', 'AnsweredOnlyBindAlsoWaitsForTwoSlots',
             'BindDeclinedBehindTheFullSetHoldsNoProbe', 'OnlyTimerProbesAreHeldBesideTheWaitingBind',
             'RefusedPollLeavesTheBindWaitingAndItsHold', 'BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces',
             'SameTalkerRebindKeepsTheHeldProbe', 'GatedPortBudgetsOnePassPerProbeOwedAhead']
STEP2_NEEDLES = {'while bind_waiting is set at most one owed slot is free',
                 'the first probe leaves at once, in the pass after the BIND_RX answer',
                 'each command kept behind the BIND_RX is answered after its frames and before any held probe',
                 'each held probe was sent, and its timeout runs from when it left',
                 'held probes follow the frames of the last kept command, one per pass in sink order'}
NEW_PLANTS = ['owed-bind-wait-cleared-by-refused-poll', 'owed-bind-wait-set-at-full', 'owed-hold-widened-to-second-no-resp',
              'owed-hold-widened-to-every-timer', 'owed-rebind-keeps-the-hold', 'owed-probe-held-never-set',
              'owed-hold-scan-skips-the-last-sink', 'owed-hold-whenever-full', 'owed-hold-at-seven',
              'owed-answered-bind-takes-one-slot', 'owed-entry-widened', 'owed-deferred-answer-error-status',
              'owed-same-talker-rebind-cancels-the-hold', 'owed-refused-poll-drops-the-frame', 'owed-ninth-frame-taken']
P, C = 'docs/PORTING.md', 'scripts/check_port_contracts.py'
if step <= 2:   # undo the residue wording (step 3)
    rep(C, ",\n                        \"its sink's probing does not advance until the probe is owed\"),", "),")
    rep(P, " while no sink's discovery restarts. These counts", ". These counts")
    rep(P, "at most one per sink while no sink's discovery restarts.\n", "at most one per sink.\n")
    rep(P, "While the port keeps commands or no owed frame is accepted, a held probe keeps waiting: its timer is re-armed every 1 ms and its sink's probing does not advance until the probe is owed.\n", "")
    rep(P, 'so it is retried at the first timer service 1 ms or more later, which is the next pass for a port whose passes are at least 1 ms apart',
        'so a port that services its timers once per pass retries it in the next pass')
    rep(P, 'after the commands still kept.\nEach held probe increments `probes_held` once for each pass it is held.\n'
           'A held probe is never dropped for want of a slot; it is cancelled only when its sink stops probing, as when its talker departs or a BIND_RX binds the sink to another talker.\n',
        'after the commands still kept. Each pass that holds a probe increments `probes_held`.\n')
    rep(P, 'A held probe therefore waits at most from', 'A held probe therefore waits from')
    rep(P, ' These counts assume passes at least 1 ms apart.', '')
    rep(P, '| `probes_held` | Holds of a timer probe for a waiting BIND_RX or behind another held probe: one for each held probe in each pass it is held. A held probe is never dropped for want of a slot; it is cancelled only when its sink stops probing. |',
        '| `probes_held` | Passes that held a timer probe for a waiting BIND_RX or behind another held probe. A held probe is never dropped. |')
    rep(C, "'retried at the first timer service 1 ms or more later'", "'retries it in the next pass'")
    rep(C, ", 'once for each pass it is held',\n                        'cancelled only when its sink stops probing', 'Held probes follow the frames of the last kept command',\n                        'These counts assume passes at least 1 ms apart'),",
        ",\n                        'Held probes follow the frames of the last kept command'),")
    rep('tests/test_acmp.cpp', '"each held probe counts once for each pass it is held"', '"each pass that holds a probe counts once"')
    rep('tests/mutations.json', '"each held probe counts once for each pass it is held"', '"each pass that holds a probe counts once"')
    rep('CHANGELOG.md', 're-armed 1 ms on instead of owed', 're-armed for the next pass instead of owed')
if step <= 1:   # undo the pins (step 2)
    rep(P, 'A refused `acmp_poll` leaves it set, and a BIND_RX declined with no slot free does not set it.', 'A refused `acmp_poll` leaves it set.')
    t = files[P]
    m = re.search(r'\nNo other expiry is held: [^\n]*\n', t); assert m
    files[P] = t[:m.start()] + '\n' + t[m.end():]
    rep(P, ', such as one for an unknown sink or a rebind to the same talker,', ', such as one for an unknown sink,')
    rep(P, 'and its timeout recovers it; so is one that falls due while a BIND_RX is declined behind the full set.', 'and its timeout recovers it.')
    rep(C, ", 'A refused `acmp_poll` leaves it set',\n                         'a BIND_RX declined with no slot free does not set it', 'No other expiry is held'),",
        ", 'A refused `acmp_poll` leaves it set'),")
    for name in ('docs/REQUIREMENTS.md', 'docs/requirements.json'):
        rep(name, 'waits for the next accepted owed frame, hold each timer probe, and no other expiry, instead of owing it',
            'waits, hold each timer probe instead of owing it')
    rep('docs/REQUIREMENTS.md', 'so they cannot delay it; no other expiry is held.', 'so they cannot delay it.')
    rep('docs/VERIFICATION.md', 'All 437 core plants', 'All 422 core plants')
    T = 'tests/test_acmp.cpp'
    rep(T, '        unsigned waiting_with_room = 0;\n', '')
    rep(T, '            waiting_with_room += a.bind_waiting && a.owed_count + 1u < ACMP_OWED_MAX ? 1u : 0u;\n', '')
    rep(T, '        EXPECT_EQ(waiting_with_room, 0u) << "while bind_waiting is set at most one owed slot is free";\n', '')
    t = files[T]
    a = t.index('// REQ: ACMP-12\nTEST_F(AcmpOwed, ' + NEW_TESTS[0])
    b = t.index('// REQ: ACMP-12, ACMP-09\nTEST_F(AcmpOwed, KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem')
    for n in NEW_TESTS:
        assert t[a:b].count('TEST_F(AcmpOwed, ' + n + ')') == 1, n
    files[T] = t[:a] + t[b:]
    ms = [m for m in json.loads(files['tests/mutations.json']) if m['name'] not in NEW_PLANTS]
    for m in ms:
        keep = [k for k in m['kills'] if k['test'].split('.')[-1] not in NEW_TESTS and k['needle'] not in STEP2_NEEDLES]
        if keep != m['kills']:
            m['kills'] = keep
            m['original_tests'] = [k['test'] for k in keep]
    files['tests/mutations.json'] = json.dumps(ms, indent=2) + '\n'
for name, text in files.items():
    if name in ('docs/TESTS.md', 'docs/TRACEABILITY.md'):
        continue
    (tree / name).write_text(text)
print('step', step, 'written')
