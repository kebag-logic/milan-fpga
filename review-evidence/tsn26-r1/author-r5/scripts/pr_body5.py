# SPDX-License-Identifier: MIT
# usage: pr_body5.py CURRENT_BODY ROUND5_SECTION OUT
# Applies the round 5 corrections to the earlier sections of the PR body and appends the round 5 section.
import sys
from pathlib import Path
body = Path(sys.argv[1]).read_text().rstrip('\n') + '\n'
section = Path(sys.argv[2]).read_text()


def rep(a, b):
    global body
    assert body.count(a) == 1, (a[:80], body.count(a))
    body = body.replace(a, b)


rep('[A750e] Decline, never drop, an ACMP command at the owed bound',
    '[A750f] Decline, never drop, an ACMP command at the owed bound')
rep("""- Port contract (`docs/PORTING.md`, "ACMP owed bound"): keep a declined frame
  and deliver it again right after each `acmp_poll` that accepts an owed frame,
  before servicing `acmp_timer_expired`. Deliver no later ACMP frame before it.""",
    """- Port contract (`docs/PORTING.md`, "ACMP owed bound"): keep a declined frame
  and deliver it again right after each `acmp_poll` that accepts an owed frame,
  before servicing `acmp_timer_expired`. Deliver no later ACMP frame before it.
  After each such poll, offer the waiting ACMP frames in arrival order, the
  kept one first, until `acmp_rx` declines one or none is left, and only then
  service the timers (round 5); the bound below assumes this.""")
rep("""- The port contract derives when every kept command leaves: in pass
  `ACMP_OWED_MAX` + 1 + f + r after the egress returns, where f counts the
  frames owed by the kept commands ahead of it and r the refused polls. It
  gives the egress-hold budget for the deepest backlog a port keeps (round 4).""",
    """- The port contract derives when every kept command leaves: in pass
  n + 1 + f + r after the egress returns, where n is the number of frames owed
  then (`ACMP_OWED_MAX`, or one less when the first kept frame is a BIND_RX
  declined with one slot free), f counts the frames owed by the kept commands
  ahead of it and r the refused polls. It gives the egress-hold budget for the
  deepest backlog a port keeps (round 4; n since round 5).""")
rep("""egress after 60 ms. The test port model polls once per 1 ms pass and delivers
kept frames in the same pass.""",
    """egress after 60 ms. The test port model polls once per 1 ms pass, then offers
every waiting frame in arrival order until `acmp_rx` declines one or none is
left, then services its timers.""")
rep("""  follow the last kept frame one per pass, in sink order, none lost.
""",
    """  follow the last kept frame one per pass, in sink order, none lost.
- `AcmpOwed.KeptCommandsBehindSevenOwedLeaveOnePassSooner` (round 5): the
  egress returns with seven frames owed, behind a BIND_RX declined with one slot
  free, a GET_RX_STATE and a second new binding. A retry falling due in the
  hold is held. The answers leave in passes 8, 10 and 11, each
  `ACMP_OWED_MAX` + f, and the held retry follows in pass 13, none lost.
- `AcmpOwed.AnsweredProbeEndsTheHoldOfItsRetry` (round 5): the answer to the
  probe a held retry repeats waits behind the kept BIND_RX; once taken it ends
  the hold, with a failure status in PRB_W_RETRY and with SUCCESS in
  SETTLED_NO_RSV, and the retry is never sent.
""")
rep("""  - 51 `owed-*` plants, all caught, and nine ACMP plants""",
    """  - 53 `owed-*` plants, all caught, and nine ACMP plants""")
rep("""  - Run against the full ACMP test binary (123 tests at this head: 122 ACMP
    tests and main's Wire test), every one of these 60 plants fails at least
    one test and passes once its failing tests are excluded. Seven of the 15
    round 4 plants pass the whole round 3 suite.
  - The campaign counts 437 core plants (435 from this branch and main's two
    `wire-put-be-*` plants) and 4 generated configuration plants.""",
    """  - Run against the full ACMP test binary (125 tests at this head: 124 ACMP
    tests and main's Wire test), every one of these 62 plants fails at least
    one test and passes once its failing tests are excluded. Seven of the 15
    round 4 plants pass the whole round 3 suite, and both round 5 plants pass
    every test but the round 5 test that kills each.
  - The campaign counts 439 core plants (437 from this branch and main's two
    `wire-put-be-*` plants) and 4 generated configuration plants.""")
rep("""   - Result: a deferred BIND_RX at the head of the kept frames is answered in
     pass `ACMP_OWED_MAX` + 1, whatever probes fall due; a command kept behind
     it follows one pass per frame owed ahead of it.""",
    """   - Result: a deferred BIND_RX at the head of the kept frames is answered in
     pass n + 1 (`ACMP_OWED_MAX` + 1 from a full set), whatever probes fall
     due; a command kept behind it follows one pass per frame owed ahead of it.""")
rep("""     kept behind the BIND_RX and for each other probe owed before it, at most
     one per other sink. Its TMR_NO_RESP runs from when it leaves, so its""",
    """     kept behind the BIND_RX and for each other probe owed before it, at most
     one per other sink under the conditions Round 5 states. Its TMR_NO_RESP
     runs from when it leaves, so its""")
rep("""     - So a kept command leaves in pass `ACMP_OWED_MAX` + 1 + f + r. Here f
       counts the frames owed by the kept commands ahead of it: two for a""",
    """     - So a kept command leaves in pass n + 1 + f + r. Here n, `ACMP_OWED_MAX`
       or one less, is the number of frames owed when the egress returns (one
       less only when the first kept frame is a BIND_RX declined with one slot
       free; round 5). f counts the frames owed by the kept commands ahead of
       it: two for a""")
rep("""       one kept command, 189 ms for two.
     - The redelivery rule the bound assumes is stated with a refused poll: it
       frees no slot and leaves `bind_waiting` set, so the port may wait for
       the next accepting poll or deliver the kept frame again, which is
       declined again.""",
    """       one kept command, 189 ms for two. The budget uses `ACMP_OWED_MAX` for
       n, so it holds from either start.
     - The redelivery rule the bound assumes is stated with a refused poll: it
       frees no slot and leaves `bind_waiting` set, so the port may wait for
       the next accepting poll or deliver the kept frame again, which is
       declined again.
     - The bound assumes that after each `acmp_poll` that accepts an owed
       frame the port offers its waiting ACMP frames in arrival order, the kept
       one first, until `acmp_rx` declines one or none is left, and only then
       services `acmp_timer_expired`. Since round 5 the redelivery rule says
       so; a port that offers fewer can leave a slot free for a timer probe
       ahead of a later kept command.""")
rep("""     head of the kept frames is answered in pass `ACMP_OWED_MAX` + 1, whatever
     probes fall due; a command kept behind it follows one pass per frame owed
     ahead of it.""",
    """     head of the kept frames is answered in pass n + 1 (`ACMP_OWED_MAX` + 1
     from a full set), whatever probes fall due; a command kept behind it
     follows one pass per frame owed ahead of it.""")
rep("""   the pass counts say so; a held probe is never dropped for want of a slot and
   is cancelled only when its sink stops probing. Two suggestions are taken: a
   held probe keeps waiting, its timer re-armed every 1 ms and its probing not
   advancing, while the port keeps commands or nothing is accepted; the
   one-per-sink counts hold while no sink's discovery restarts. This body: the
   Round 3 "Result" sentence and the `probes_held` wording.""",
    """   the pass counts say so; a held probe is never dropped for want of a slot and
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
   `probes_held` wording.""")
rep("""  is answered in passes 9, 11, 12, 14 and 15, each `ACMP_OWED_MAX` + 1 + f. A""",
    """  is answered in passes 9, 11, 12, 14 and 15, each `ACMP_OWED_MAX` + 1 + f
  from the full set. A""")
for word in ('/ho' + 'me/', '/da' + 'ta/', 'tsn' + '26-', 'milan-fpga-' + 'management'):
    assert word not in section, word
Path(sys.argv[3]).write_text(body + '\n' + section.rstrip('\n') + '\n')
print('ok')
