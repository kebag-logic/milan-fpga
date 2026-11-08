#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# usage: pr_body6.py CURRENT_BODY ROUND6_SECTION OUT
# Applies the round 6 in-place corrections to the current PR body and appends the Round 6 section.
# Every replaced text must occur exactly once.
import sys
from pathlib import Path

cur, sec, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
t = cur.read_text().rstrip('\n') + '\n'
R = [
    ('[A750f] Decline, never drop', '[A750g] Decline, never drop'),
    # Round 3 item 1
    ("""     - A held probe is never lost. While any probe is held, a probe that finds
       every slot owed is held with it. Held probes take freed slots one per
       pass, after the commands the port still keeps.""",
     """     - A held probe is never lost. While any probe is held, a probe that finds
       every slot owed is held with it. Held probes take freed slots one per
       pass, after the commands the port still keeps or offers before its timer
       service (round 6)."""),
    ("""   - The held probe's own delay, stated in `docs/PORTING.md` "ACMP owed bound"
     (Milan v1.2 5.5.3.5): it waits at most from the pass it falls due through the pass
     that takes the BIND_RX, plus one pass for each frame owed by a command
     kept behind the BIND_RX and for each other probe owed before it, at most
     one per other sink under the conditions Round 5 states. Its TMR_NO_RESP
     runs from when it leaves, so its response window is unchanged.""",
     """   - The held probe's own delay, stated in `docs/PORTING.md` "ACMP owed bound"
     (Milan v1.2 5.5.3.5): a held probe is never dropped for want of a slot. It
     takes a freed slot only at timer service with no BIND_RX waiting, after
     every command the core takes first, whether kept or offered for the first
     time, so no command answer waits for it. Its wait has no upper limit while
     commands keep taking the freed slots (round 6 removed the earlier limit).
     Its own TMR_NO_RESP runs from when it leaves, so its response window is
     unchanged."""),
    # How to validate
    ("""  `probes_lost` is 0. Its own probe leaves next, then the commands kept behind
  it, then every held probe in sink order. Each held probe is owed exactly in
  the pass the documented bound gives, its TMR_NO_RESP runs from when it left,""",
     """  `probes_lost` is 0. Its own probe leaves next, then the commands kept behind
  it, then every held probe in sink order. Each held probe is owed in the pass
  after the BIND_RX is taken, one pass later for each frame of the commands
  kept behind it and for each probe before it; its TMR_NO_RESP runs from when it left,"""),
    ("""  SETTLED_NO_RSV, and the retry is never sent.
""",
     """  SETTLED_NO_RSV, and the retry is never sent.
- `AcmpOwed.CommandOfferedAfterTheTakenBindDelaysTheHeldRetry` (round 6): a
  retry is held beside a kept BIND_RX, which is taken in pass 2. Then none, one
  or three GET_RX_STATE commands are offered for the first time, one after each
  accepting poll, and each is taken at once. The held retry is owed in pass
  2 + 1 + the number of those commands, so each one delays it one pass. Every
  answer leaves before the retry, nothing is lost, and the retry's TMR_NO_RESP
  runs from when it leaves.
"""),
    ("""  - 53 `owed-*` plants, all caught, and nine ACMP plants that the owed-bound""",
     """  - 54 `owed-*` plants, all caught, and nine ACMP plants that the owed-bound"""),
    ("""  - Run against the full ACMP test binary (125 tests at this head: 124 ACMP
    tests and main's Wire test), every one of these 62 plants fails at least
    one test and passes once its failing tests are excluded. Seven of the 15
    round 4 plants pass the whole round 3 suite, and both round 5 plants pass
    every test but the round 5 test that kills each.
  - The campaign counts 439 core plants (437 from this branch and main's two""",
     """  - Run against the full ACMP test binary (126 tests at this head: 125 ACMP
    tests and main's Wire test), every one of these 63 plants fails at least
    one test and passes once its failing tests are excluded. Seven of the 15
    round 4 plants pass the whole round 3 suite, both round 5 plants pass
    every test but the round 5 test that kills each, and the round 6 plant
    passes every test but the round 6 test.
  - The campaign counts 440 core plants (438 from this branch and main's two"""),
    # Round 4 item 3
    ("""3. **Residue and suggestions.** `probes_held` counts each held probe once per
   pass (PORTING and the counter row); a held probe waits "at most" its bound;
   the 1 ms re-arm is the next pass only for passes at least 1 ms apart, and
   the pass counts say so; a held probe is never dropped for want of a slot and
   is cancelled only when its sink stops probing or, for a retry, when the probe
   it repeats is answered (round 5). Two suggestions are taken: a held probe
   keeps waiting, its timer re-armed every 1 ms and its probing not advancing
   until it is owed or cancelled, while the port keeps commands or nothing is
   accepted; the one-per-sink counts hold while no sink's probing restarts (an
   ADP re-advertisement that does not raise the available index, a new
   discovery after its talker departs or its advertisement times out, or
   `acmp_tk_unregistered`) and, for a held probe, while it has waited less than
   TMR_NO_RESP (200 ms); past that, another sink's TMR_NO_RESP retry can also be
   owed before it (round 5). This body: the Round 3 "Result" sentence and the
   `probes_held` wording.""",
     """3. **Residue and suggestions.** `probes_held` counts each held probe once per
   pass (PORTING and the counter row); the 1 ms re-arm is the next pass only
   for passes at least 1 ms apart; a held probe is never dropped for want of a
   slot and is cancelled only when its sink stops probing or, for a retry, when
   the probe it repeats is answered (round 5). Two suggestions are taken: a
   held probe keeps waiting, its timer re-armed every 1 ms and its probing not
   advancing until it is owed or cancelled, while the port keeps or offers
   commands that take the freed slots, or nothing is accepted (round 6); the
   gated port's one-per-sink count holds while no sink's probing restarts (an
   ADP re-advertisement that does not raise the available index, a new
   discovery after its talker departs or its advertisement times out, or
   `acmp_tk_unregistered`) (round 5). A held probe's wait has no upper limit:
   it takes a freed slot only at timer service with no BIND_RX waiting, after
   every command the core takes first, whether kept or offered for the first
   time, so no command answer waits for it, and its own TMR_NO_RESP runs from
   when it leaves (round 6). This body: the Round 3 "Result" sentence and the
   `probes_held` wording."""),
    # Round 5 item 3
    ("""3. **The held probe's conditions** (finding F6 of the internal review, and
   suggestion S9 of the external review).
   - The count of one probe per other sink also needs the held probe's wait to
     stay under TMR_NO_RESP. Past 200 ms, a sink whose TMR_DELAY probe was owed
     before the held probe can owe its TMR_NO_RESP retry before it too. In the
     internal review's sustained probe, sink 3 left after both of sink 2's
     probes, with no restart.
   - PORTING now says "at most one per other sink while no sink's probing
     restarts (an ADP re-advertisement that does not raise the available index,
     a new discovery after its talker departs or its advertisement times out,
     or `acmp_tk_unregistered`) and the held probe has waited less than
     TMR_NO_RESP (200 ms); past that, another sink's TMR_NO_RESP retry can also
     be owed before it". The gated-port sentence uses the same "probing
     restarts".
   - S9 named two restart paths. The code has a third that lets a sink owe a
     second probe within 200 ms: its talker departs, by ENTITY_DEPARTING or by
     the end of the advertisement's valid time. When the talker is discovered
     again, a new TMR_DELAY is armed. The text names all three.""",
     """3. **The held probe's conditions** (finding F6 of the internal review, and
   suggestion S9 of the external review).
   - Round 5 bounded a held probe's wait with a count of one probe per other
     sink, valid while no sink's probing restarts and while the held probe had
     waited less than TMR_NO_RESP (200 ms), and listed what can be owed past
     that. Round 6 removes that limit, its per-sink counts and the list (Round 6
     item 1).
   - PORTING now states instead that a held probe is never dropped for want of
     a slot; that it takes a freed slot only at timer service with no BIND_RX
     waiting, after every command the core takes first, whether kept or offered
     for the first time; that no command answer waits for it; and that its wait
     has no upper limit while commands keep taking the freed slots, its own
     TMR_NO_RESP running from when it leaves.
   - S9 named two restart paths. The code has a third that lets a sink owe a
     second probe within 200 ms: its talker departs, by ENTITY_DEPARTING or by
     the end of the advertisement's valid time. When the talker is discovered
     again, a new TMR_DELAY is armed. The text names all three; since round 6
     they qualify the gated port's one-per-sink count."""),
    # Round 5 item 4 (RES9 of the external review)
    ("""     a BIND_RX waits. A BIND_RX declined with no slot free also waits, and a
     probe that falls due then is lost; `BindDeclinedBehindTheFullSetHoldsNoProbe`""",
     """     a BIND_RX waits. A BIND_RX declined with no slot free also waits, and a
     probe that falls due then, with no probe held, is lost; `BindDeclinedBehindTheFullSetHoldsNoProbe`"""),
    # Round 5 probe table
    ("""| `probe_r4c`, sustained | Sink 2's TMR_DELAY probe leaves in pass 11 and its TMR_NO_RESP retry in pass 250, both before sink 3's held retry (pass 251) | Past 200 ms, another sink's TMR_NO_RESP retry can also be owed before the held probe |""",
     """| `probe_r4c`, sustained | Sink 2's TMR_DELAY probe leaves in pass 11 and its TMR_NO_RESP retry in pass 250, both before sink 3's held retry (pass 251) | Past 200 ms, another sink's TMR_NO_RESP retry can also be owed before the held probe (a clause round 6 removes; since round 6: a held probe's wait has no upper limit while commands keep taking the freed slots) |"""),
]
for a, b in R:
    n = t.count(a)
    if n != 1:
        raise SystemExit(f'{n} matches for: {a[:70]!r}')
    t = t.replace(a, b)
t = t.rstrip('\n') + '\n\n' + sec.read_text().strip('\n') + '\n'
out.write_text(t)
print('written', out, len(t.splitlines()), 'lines')
