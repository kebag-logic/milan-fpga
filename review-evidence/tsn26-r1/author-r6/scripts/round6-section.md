## Round 6

Two new commits on top of 715d208. Nothing was rebased or amended. No core
source changes: `src/`, `include/` and `examples/` are as at round 3, so the
behaviour, memory, instruction counts and bare-metal image are unchanged. This
round follows the round 6 ruling (items 1 to 4). It removes the upper limit
that the port contract gave for a held probe's wait, and it states instead
what holds by construction. Four rounds in a row found a gap in that limit,
while the core behaved correctly each time. No Milan deadline depends on it,
because a held probe's own TMR_NO_RESP runs from when it leaves.

1. **The held probe's wait has no upper limit** (ruling item 1; finding F5 of
   the external review).
   - `docs/PORTING.md` "ACMP owed bound" no longer has the "waits at most"
     sentence, its count of one probe per other sink, its TMR_NO_RESP (200 ms)
     condition or the list of what can be owed past that. The sentence
     "These counts assume passes at least 1 ms apart" went with them, because
     no count is left for it to qualify. The 1 ms condition is still stated
     where the hold is defined.
   - In their place PORTING now says: a held probe is never dropped for want
     of a slot, and it takes a freed slot only at timer service with no
     BIND_RX waiting, after every command the core takes first, whether kept
     or offered for the first time, so no command answer waits for it. Its
     wait has no upper limit while commands keep taking the freed slots; its
     own TMR_NO_RESP runs from when it leaves.
   - The command bound (n + 1 + f + r) and the egress-hold budget are
     unchanged.
   - The three probing-restart paths that qualified the removed count now
     qualify the gated-port sentence, the only count still to use "probing
     restarts". Its wording is otherwise unchanged.
   - This body: the Round 3 item 1 delay sentence, Round 4 item 3 and Round 5
     item 3 now say the same. So do the Round 3 sentence on freed slots, the
     How to validate entry for the round 3 test, and the Round 5 probe table
     row that cited the removed clause.
2. **Commands offered for the first time also come first** (ruling item 2;
   the external review's wording).
   - The held-probe sentence now ends "held probes take freed slots one per
     pass, after the commands the port still keeps or offers before its timer
     service".
   - The waiting sentence now begins "While the port keeps or offers commands
     that take the freed slots, or no owed frame is accepted, a held probe
     keeps waiting".
3. **Pins, test and plant** (ruling item 3).
   - `scripts/check_port_contracts.py` drops the six pins of removed or
     changed clauses: "after the commands still kept", "through the pass that
     takes the BIND_RX", "These counts assume passes at least 1 ms apart", "at
     most one per other sink while no sink's probing restarts", "the held probe
     has waited less than TMR_NO_RESP (200 ms)" and "past that, another sink's
     TMR_NO_RESP retry can also be owed before it".
   - It pins eight phrases of the new text. The two restart-path phrases moved
     to the `acmp_rx_ready` pins, with the gated-port sentence they now
     qualify, and that sentence's "at most one per sink while no sink's probing
     restarts" is pinned too. The self-test refuses 77 meaning-removal
     controls, up from 74.
   - New test `CommandOfferedAfterTheTakenBindDelaysTheHeldRetry`:
     - A retry is held beside a kept BIND_RX, which is taken in pass 2.
     - Then none, one or three GET_RX_STATE commands are offered for the first
       time, one after each accepting poll, and each is taken at once.
     - Its named assertion is "after the BIND_RX is taken, a GET_RX_STATE
       offered after the next accepting poll delays the held retry one pass".
       The retry is owed in passes 3, 4 and 6.
     - Every answer leaves before the retry ("no command answer waits for the
       held retry"). Nothing is lost, and the retry's TMR_NO_RESP runs from
       when it leaves.
   - New plant `owed-held-probe-owed-at-the-poll`:
     - At an accepting `acmp_poll` with no BIND_RX waiting, it owes a held
       probe at once, so the probe takes the slot ahead of a command offered
       after that poll.
     - It does this only when no command was declined since the previous
       accepting poll, so commands kept from before still go first. That is
       the difference between a command offered for the first time and a kept
       one, and the core sees it only through `busy_declined`, as in the round
       5 plant.
     - It is registered with both needles above. The new test kills it, and
       without that test it passes all 125 other tests.
   - No test or plant was removed. No test asserts the removed limit.
     `ProbesFallingDueInTheDrainWaitForTheDeferredBind` asserts the exact pass
     of each held probe when no command follows the BIND_RX ("one pass per
     probe before it"). The retained sentence "Held probes follow the frames of
     the last kept command, one per pass" and the new sentences still state
     that. Its two plants, `owed-hold-rearmed-late` and `owed-hold-at-seven`,
     stay registered.
4. **Residue** (ruling item 4).
   - RES9 of the external review: Round 5 item 4 now says "a probe that falls
     due then, with no probe held, is lost".
   - RES8 of both reviews went with the removed clause.
   - Not taken, as outside the ruling: the internal review's RES9 (add "while
     no sink's probing restarts" to the integration note's gated-port sentence)
     and the optional RV32 smoke step (S7 of the internal review, S8 of the
     external review).

### Every stated behaviour, again

The sentence map was rebuilt for the new text. It has 65 sentences and
clauses, 50 of them core. Each core sentence has a named assertion and a
registered plant that it kills and the campaign catches. The new held-probe
sentences are pinned by the new test and its plant, and by the round 3 test's
exact passes and its timeout assertion.

### Both reviews' probes at this head

All the probes of both reviews' rounds 4 and 5 ran unchanged on a clean clone
of this head. The internal review's runners export the commit, and the
external review's runner copies an archive of it. Every PROBE line is
identical to the reviews' own receipts, because the core is unchanged, and
each run ends with rc 0.

| Probe | Output | Sentence it meets |
|---|---|---|
| `probe_owed7` (external, round 5), commands offered for the first time or declined and kept after the BIND_RX is taken | The held retry is owed in pass 3 with none, then 4, 6 and 13 with 1, 3 and 10 such commands; `probes_lost` 0. The probe's own "stated" column prints the removed round 5 limit | It takes a freed slot only at timer service, after every command the core takes first, whether kept or offered for the first time; its wait has no upper limit while commands keep taking the freed slots |
| `probe_r5` (internal, round 5), a GET every pass for 5600 passes | Sink 3's retry is held through pass 5602 and leaves in pass 5611, after sink 2's two probes; `probes_lost` 0 | Its wait has no upper limit while commands keep taking the freed slots; it is never dropped for want of a slot |
| `probe_r5b` (internal, round 5), the same with one gap of two command-free passes | The two lowest held retries leave in the gap. Sink 2 then owes a third probe in pass 6409, before sink 3's held retry in pass 6410; `probes_lost` 0 | The same two sentences. The removed list named only the retry past 200 ms |
| `probe_r4c`, sustained | Sink 2's probes leave in passes 11 and 250, sink 3's held retry in pass 251 | The same two sentences |
| `probe_r4c`, failure response | `probe_held` 1 → 0; PRB_W_RETRY, probing ACTIVE, TMR_RETRY | Cancelled when a held retry's earlier probe is answered |
| `probe_r4` and `probe_r4b`, ports "all" and "one" | As at round 5: the formula passes for "all", one pass late for "one" (201 ms at 189 ms) | n + 1 + f + r and the budget; the redelivery rule excludes "one" |
| `probe_owed6`, eight and seven owed | 9, 11 and 12; 8, 10 and 11 | n = 8 and n = 7 |
| `probe_r3`, `probe_intermittent` and `probe_timer_ahead` (internal, rerun in round 5) | 14 and 5 lines, as at round 5 | The command bound, the budget and the gated port, all unchanged |

The external review's `escape_check5.py` also ran unchanged. With 126 tests,
both round 5 plants and its two reviewer plants fail the full binary, and
every registered needle is SEEN. The internal review's `plant_escape.sh`, run
unchanged on the round 6 plant, gives: the full suite fails only the new test,
and without it 125 of 125 pass.

### Gates at this head

On a clean clone of this head, `python3 scripts/validate.py --work <w> --jobs 16 --graphs`
returns 0 for all 28 gates. That includes the full mutation campaign
(444 caught, 0 escaped, 0 errors), privacy, coverage (`src/acmp.c` 813/813 lines and 424/424 branches,
unchanged), both sanitizer arms, static analysis and graphs.
`python3 scripts/baremetal.py --work <w> --jobs 8` returns 0 in Debug and
Release. Each of the two commits passed the same gates on its own tree before
it was committed.

The core is unchanged, so memory and instruction counts are as in the Round 3
tables. The Release RV32 image is byte-identical to round 5's: 50504 bytes,
`.text` 38668, `acmp.c` object text 19365. The Debug image is 150332 bytes for
both heads, built from exported trees at paths of equal length.

Issue #26 stays open: the parent firmware's harness row still needs the parent
to adopt this head (see the integration note). Round 6 changes no source, so
no parent fragment moves.
