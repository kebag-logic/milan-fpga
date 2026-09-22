<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# nvm_port — KL_pp_nvm_port class-F suite

Proves the class-F NVM port (`hdl/packet_engine/KL_pp_nvm_port.sv`,
[02 §8](../../docs/architecture/02_interfaces.md) F02.8 +
[07 §5](../../docs/architecture/07_memory_maps.md) F07.8): `make` = build + run,
exit 0 = PASS, 122 checks. `-GMAX_PAYLOAD_P=1024` pins the geometry the C++
constants mirror.

The harness plays BOTH neighbors, independently of the RTL: a **manager BFM**
that frames records per 07 §5.2 (magic 0x1722, layout_version, record_id,
payload_length, crc16 — 16-bit fields big-endian on the stream; crc computed by
the harness, opaque to the DUT) and streams them with configurable stalls, and
a **device model** implementing the region port (req/gnt with delay, op
READ/WRITE/ERASE_REGION, region + offset + len, stalling byte phases,
busy/done/err with completion delays, error injection at any command index or
data byte, a seeded byte store, and a log of every accepted command (`ops`), and a log of every byte the port
put on the device write bus (`sent`), which is what the rule below points a
check at when the assertion must not read the array). It can also misbehave on
the HANDSHAKE, which is the half the five array-flavoured variants never
reached: it will pulse a `done` that belongs to no command at all, it will
answer an ERASE on the grant cycle, and it will answer any command on the same
edge that moves that command's final byte. See "Completion ownership" below.

Covered: the commit envelope ERASE_REGION → WRITE(0, 8+plen) with the device
store byte-exact against the manager's framed record and the erase visible past
it; the restore envelope READ(0,8) → READ(8,plen) with the returned stream
byte-exact; zero-payload records both ways (restore then issues only the header
probe); stall torture on all four byte interfaces at once (gnt and done
delayed); back-to-back ops with req re-asserted the cycle after the pulse;
req-while-busy ignored (single outstanding, F02.8); busy/done/err sequencing —
busy high mid-op, LOW at the pulse, done and err mutually exclusive and exactly
once per op; a device error during ERASE surfacing as exactly one manager-face
err with the WRITE never issued, plus recovery on retry; errors mid WRITE-data
and mid READ-payload; refusals per 07 §5.2 with zero (further) device traffic —
bad magic on commit, oversize payload_length on commit, bad magic and oversize
length in the stored record on restore (nothing forwarded to the manager); the
port serviceable again after every refusal; and completion ownership — a `done`
that belongs to no command ignored in every state that owns none, on both the
commit and the restore path, and the two completions the port must take: one
riding its own grant, one riding a command's final byte.

Known limits (honest): the CRC16 is carried, never checked — that is the
manager's job per 07 §5.3, so a corrupt-crc record passes this port by design
and must be caught by the NVM-manager suite (P4). The byte order of the 16-bit
header fields on the stream is a design decision of the port (network order),
not pinned by the doc.

Power-cut coverage (issue #70, added 2026-08-20). A commit is ERASE(region)
then WRITE(0, 8+plen). The destructive window is the WHOLE commit, not just the
WRITE: a cut at `S_WWREQ` errs with zero bytes on the bus and `erase_count`
already advanced, so **`err` never means "the saved set is unchanged"**. A cut
inside the WRITE leaves the region erased plus a
partial record: the record being written is gone, and on the backends that
erase in place **so is whatever it replaced**. That is a property of writing a
slot in place. The flash map's A/B slots are related but do NOT cover it: they
are per record SET, whole-image with read-back-then-promote, and this port has
no slot notion at all. What covers a torn SINGLE record is the crc16, and it IS
implemented — in the manager, not here: `hdl/acmp/KL_acmp_nvm_shadow.sv`
serialises it (`:402-403`), accumulates it (`:627`) and gates the record on it
(`:316`), with the per-record vendor-default policy at `:54-55`. It is
instantiated at `hdl/top/protocol_processor_top.sv:2238` and pinned by
`tb/acmp_nvm`. An earlier revision of this file said nothing implemented it,
which was wrong and is the third time this file has asserted an absence without
checking for the presence. It is NOT
universal: measured with the RTL byte-identical, a backend that both answers
ERASE lazily and buffers writes to the page leaves the old record intact. So
the suite pins what the port DOES guarantee, and where a claim about the array
follows a device `err` it is either moved onto the bus or conditioned on what
the array actually holds. Claims that follow a `done` are asserted directly and
need no condition, which is most of them. Counted in the unit the claim is
about, CHECK sites whose condition depends on the array: **16 sites, of which 2
condition on it and 14 do not**. Counting this needs care and got it wrong once:
`T16 no other region's bytes moved` reaches the array through `other_moved`, a
local hoisted 35 lines above its CHECK, so every text sweep for `store` missed
it -- and that site is the #70 isolation claim itself, the most important member
of the set. See "Where a check may read from" for the rule and its one known exception,
`T1 erase visible past the record`, which asserts on the array after a device
`done` and reddens under a lazy-erase backend:

- **T15** a torn commit reports `err` and never `done`, with busy low at the
  pulse; the cut is proven real on the BUS (ERASE then a WRITE that stopped 12
  bytes in, checked against the write-handshake log) rather than by reading the
  array, which is the backend's business; unless the old record survived the
  tear, it never restores as a VALID record — either the port refuses it at the
  header or the bytes it forwards fail the manager's CRC,
  which the suite computes itself; and the port is serviceable afterwards.
- **T16** the property #70 actually needs: a torn commit of one record leaves
  **every other record** untouched. All 8 regions are snapshotted in FULL
  (every one of `REG_BYTES`, not just the record-sized prefix) before the cut
  and compared after, so a clobber landing two regions over, or past the end of
  a record, is caught rather than only the byte range the test happens to use;
  the neighbour still restores byte-exactly afterwards. The isolation claim is
  guarded against vacuity by first pinning that the torn commit really did
  reach the device — otherwise "nothing else moved" would also hold for a port
  that never issued anything. Getting that guard right took three attempts and
  the first two were themselves vacuous, which is worth recording: "the
  region's bytes changed" is satisfied by the ERASE alone, and "some byte is
  not 0xFF" is satisfied by whatever an earlier phase left behind — region 1
  still holds T5b's record (the `f5b` commit in T5) eleven phases later, so that
  spelling passed even under a mutant where the port wedged and issued no
  device traffic at all. What actually defends the claim is the pair of checks
  that READ THE DUT: the op log must show ERASE then the WRITE for this record,
  and the region's erase count must have moved. Both are driven by `dev_req_o`,
  and a port issuing nothing can fake neither. The byte comparison beside them
  reads the write-handshake log `sent`, NOT the region, so it pins what the
  port put on the bus and carries no model dependency. An earlier spelling
  compared the region's bytes and was doubly wrong: `torn[0..4]` is
  byte-identical to the T5b residue prefix, so its separating power sat
  entirely in `store[1][5] == 0xFF`, and it reddened under a half-page model
  with the RTL untouched.
- **T17** the cut a NOR device actually produces. T15 and T16 cut while bytes
  are still moving, but a real program failure is not reported then: the device
  latches the bytes, starts the program cycle, and raises its error when that
  cycle ends — after the last byte, busy still high. That is the port's
  `S_WWAIT` arm, the widest window in a commit, and nothing else in the suite
  enters it. The phase pins what the port owes there — `err` and never `done`,
  busy released and the port idle afterwards, and the port usable for the next
  commit. It also exercises the READ side, because whether the port still
  serves a region after taking `S_WWAIT`'s error exit is its own property and
  T17 otherwise covered only the write side. It does NOT restore the torn
  region, because what that region holds is the backend's choice: it commits
  a good record
  first, which ends in `done` so every model agrees what the array now holds,
  and only then reads it back, pinning the device ops the way T2 does so a
  fabricated restore cannot pass. Two earlier spellings compared against the
  record being written and against the array, and both pinned the model.
- **T18** the same argument on the RESTORE side. A NOR read fails the way a
  program does: an ECC or timeout error surfaces when the read cycle ENDS, not
  mid-stream. `S_RPWAIT` is the exact mirror of the arm T17 closed, `S_RHWAIT`
  is that window on the header probe, and `S_RHCOLL` is an error during the
  header collect — which sits on the boot restore walk, the one path where a
  torn image is actually consumed. All three survived the suite before T18.

### Completion ownership (issue #14)

`done_seen_r` is sticky because a device `done` may land on the same edge a pump
moves its last byte; the wait states consume it a cycle later. The set used to
sit OUTSIDE the state case, so the flag was armed in EVERY state — including the
states where this port has no device command outstanding at all. A `done`
arriving while a commit's header was still being collected was then consumed by
`S_WEWAIT` as the ERASE's, and the WRITE went out into a region the backend was
still erasing, reported to the manager as `done` rather than `err`.

Nothing here could see it, and the reason belongs beside the model rules below:
**a harness whose device model is well behaved cannot exercise the port's
tolerance of one that is not.** This model only ever completed a command it had
accepted, so "sticky per command" and "sticky globally" were the same port to
it. The array-flavoured variants vary a different axis and none of them reaches
this.

What the port owes is now stated in its own header as refusal (c) and gated on
it (`dev_cmd_owned_w`, `KL_pp_nvm_port.sv:151-162`): a completion is this port's
from the cycle its grant is observed — that cycle may carry the completion —
until the wait state consumes it, and ownership retires at the terminal state,
at the next accept, and at reset. `S_WHDR`, an ungranted `*REQ`, `S_RHFWD`,
`S_FIN` and `S_IDLE` own nothing. Note where that contract comes from:
[02 §8](../../docs/architecture/02_interfaces.md) leaves the device face free,
so nothing above this module says whether a grant may carry its own completion.
The port's header is the decision and T21 is the measurement of it, not a
licence the architecture handed down.

`arm_unsolicited_done(after_ops, in_req)` is the device the harness could not
play before: it pulses one `done` for no command at all, in a window named by
what the BUS shows — how many commands the backend has accepted, and whether a
request is up that it has not granted — so no check reads DUT state, and an
arming that never found its window reports zero pulses rather than passing
quietly.

| phase | the stray `done` lands in | reached by the withdrawn `S_WHDR` clear | the counter that fails when ownership admits that state |
|---|---|---|---|
| T19a | `S_WHDR`: collecting the header, nothing issued | yes | `req_while_owed` |
| T19b | `S_WEREQ`: ERASE requested, ungranted | no | `req_while_owed` |
| T19c | `S_WWREQ`: WRITE requested, ungranted | no | `pulse_while_owed` |
| T20a | `S_RHREQ`: header READ requested, ungranted | no | `fwd_while_owed` |
| T20b | `S_RHFWD`: after the header read, before the payload read | no | `pulse_while_owed` |
| T20c | `S_RPREQ`: payload READ requested, ungranted | no | `pulse_while_owed` |

The last column is measured the same way as everything else here: ownership was
widened by exactly one state term, one build each, and the counter named is the
one that goes non-zero. It is in the table because a phase that names a state
and cannot fail for it is the defect this suite has now made twice -- and the
`S_RHREQ` row was that defect until the third counter landed.

T21 and T22 are the other edge of the same window, and between them they are why
it opens at the grant and stays open through the pumps. T21: a backend without
erase semantics -- the one the port's own header names -- answering ERASE with
`done` on the grant cycle. That completion IS the port's, and a fix narrowed to
"strictly after the grant" wedges the commit in `S_WEWAIT` against a device
doing nothing wrong. T22: a backend answering on the same edge that moves a
command's final byte, which is the coincidence the sticky flag was written for.
A cycle later the wait state reads `done_seen_r` rather than `dev_done_i`, so a
window narrowed to the grant handshake alone drops that completion and waits
forever for one the backend already sent. T22 runs it on the WRITE's payload
pump, on a header-only WRITE whose last byte moves in `S_WHPUMP`, and on both
reads of a restore, which is the four states of the window that can move a final
byte.

**Why the checks are on the bus.** A stray `done` consumed as somebody else's
does not corrupt the stream: the bytes still move, the record still lands, the
restore still comes back byte-exact. What changes is WHEN — and against a model
that will not grant a second command while one is in flight, the damage shows as
a port running one command ahead of its backend. So the three discriminating
counters count exactly that: cycles where the port requested a new device command
while the backend still owed a completion, cycles where it answered the manager
inside the same window, and cycles where it handed the manager a byte out of its
own header buffer inside it. None reads the array, so all three hold under
every model here. Against a backend that grants while busy — which this model
deliberately is not — the same one-command-ahead port is the WRITE landing in a
still-erasing region, which is the failure the ticket describes.

The third counter is not decoration, and the reason is the interesting part of
this suite's history. The first two are read a long way downstream of the
defect: a completion taken in an ungranted `S_RHREQ` is consumed by `S_RHWAIT`
the moment the eighth header byte lands, but the next REQUEST and the manager's
PULSE come a whole header forward later, so whether the backend is still owing a
completion by then is a property of its own delay rather than of the port. At
the delay T20 runs, both were back to zero and T20a passed under a mutant that
did exactly what the row says it must not: measured before this counter existed,
admitting an ungranted `S_RHREQ` into the window left the whole suite green,
T20a included. The forward counter fires
two cycles after the flag is consumed instead, and it is causal rather than
tuned -- the port may hand up a buffered header only once the read that filled
the buffer has completed, on any backend, at any delay.

The sticky latch is no longer invisible on the pristine model either: deleting the set
line now reddens 9 of 122 here, in T21, all three T22 arms and the end-of-run
idle check, because a commit that never gets its completion never releases
busy, and under a coincident-completion model the same
mutations fail 91 of 122.
Narrowing ownership the other way, by dropping the grant term, reddens exactly
the same nine: T21 is the first phase that needs a completion the wait state
cannot read live, so the port wedges there and T22 dies with it.

**Both halves of the window are pinned now, and one half was not.**
`dev_cmd_owned_w` is the grant handshake plus eight state terms. The grant term
was defended from the start, by T21. The eight state terms were not defended by
anything: every backend the suite ran completed some cycles after the last byte,
a completion that lands with the port already in a wait state is read live from
`dev_done_i`, and the sticky flag is then never consulted at all, so the whole
state half could be deleted with the suite green. The coincident-completion
model in this file already reddened that mutation heavily, which says the terms
are load-bearing rather than dead; what was missing was a standing phase pairing
them with the completion semantics the port's own header allows. T22 is that
phase, and these are the measurements:

- ownership narrowed to the grant handshake alone **fails 6 of 122**. The port
  wedges on T22a and every later phase dies with it.
- dropping the single `S_RHCOLL` term **fails 3 of 122**: the restore whose
  header read is answered on its own eighth byte loses that completion, wedges
  in `S_RHWAIT`, and never issues the payload read, so T22c's own witness
  reports one coincidence where it requires two.
- dropping the single `S_WWAIT` term **fails 0 of 122**, and that is not an
  oversight; see the list below.
- admitting an ungranted `S_RHREQ` into the window **fails 1 of 122**, on
  T20a's forward counter. Before that counter existed this mutant was green.

**What this does NOT establish.** Nothing here says the defect was reachable on
any bitstream. What answers this port's device face lives in the integrating
parent, which this repository does not contain and this suite does not model;
what is proved is the port's contract. Beyond that, here is exactly which part
of the fix each check reaches and which parts nothing here reaches, enumerated
rather than summarised because "one line of the fix" was the previous summary
and it was too small:

- **the four wait-state terms** of `dev_cmd_owned_w`: `S_WEWAIT`, `S_WWAIT`,
  `S_RHWAIT`, `S_RPWAIT`. Each was dropped on its own and the suite stayed
  green, and that is a property of the FSM rather than of this suite: a wait
  state consumes `dev_done_i` on the cycle it arrives, so the sticky set beside
  it can never be read. They are kept because the window is stated as a
  property of the whole outstanding command, and a later wait state that can
  stall would need them. The `S_WWAIT` row above is that equivalence, measured:
  if a check ever does reach it, the row goes red and this paragraph is wrong.
- **the four pump and collect terms** are the opposite case and are pinned:
  `S_WHPUMP` and `S_WDPUMP` by T22a and T22b, `S_RHCOLL` and `S_RPPUMP` by
  T22c.
- **both retirement clears.** Clearing `done_seen_r` in `S_FIN` retires
  ownership at the terminal boundary, and the accept path in `S_IDLE` clears it
  again before the next op can read it. Removing either leaves the suite green,
  and so does removing BOTH, under every device model here: no observer can
  separate a flag cleared twice from a flag cleared once. They are kept because
  the invariant they state, that the flag is never set outside the window, is
  what the ticket asks for, and a reader should not have to reconstruct it from
  two distant clears.
- **the grant-carried completion is proven for ERASE only.** T21 measures it on
  the ERASE a backend without erase semantics answers at once, which is the
  case the port's header names. The banner states the freedom for every
  command, and for a READ the grant cycle carrying a completion is a zero-byte
  short read: `S_RHCOLL`'s defence tests the live `dev_done_i` and not the
  latched flag, so that completion is remembered and the port waits in
  `S_RHCOLL` for bytes that never come. That is unchanged by this work (the
  pre-fix latch set the flag on that cycle too), and it is the wedge class of
  issue #15, which this suite does not model.

Mutation-proven (backup → sed → run → restore → green). **These figures are
against the 122-check suite; earlier revisions of this file carried 55-era
numbers for M1 to M3 long after the suite grew.**
- **M1** commit skips the ERASE: the transition INTO `S_WEREQ` (`:201`)
  rewritten to `S_WWREQ`, so no ERASE is ever issued. **Fails 24 of 122**
  (op-log shape, erase pulse/visibility, erase-error path).
  The description used to read "`S_WEREQ` target rewritten", which is ambiguous
  and the two readings differ enormously: rewriting what `S_WEREQ` itself
  transitions to (`:215`), so the ERASE is REQUESTED but never awaited, **fails
  only 5 of 122**. That sibling is a real coverage gap and is recorded as one
  rather than hidden by the ambiguity.
- **M2** magic gate dropped from `hdr_ok_w`: **fails 5 of 122** (both bad-magic
  refusals and the nothing-forwarded check). Note this drops BOTH magic bytes;
  the low byte alone is uncovered, see the gap list below.
- **M3** payload pump off-by-one (`bcnt_r == plen_r` for `plen_r - 1`, both
  directions): **fails 91 of 122** (every data-phase op times out or mismatches).
- **M4** (2026-08-20) the write phase swallows the device error (`S_WDPUMP`'s
  `if (dev_err_i)` forced false): **fails 52 of 122**. A torn commit then looks
  clean, which is exactly the false success #70 exists to remove. Six checks
  survive in the phases the mutation reaches, enumerated by RUNNING the
  mutation rather than reasoning about it,
  because earlier versions of this file twice published a survivor list written
  from what M4 ought to do: `T15 seed record committed` (it precedes the cut);
  `T15 busy raised then low at the err pulse` and `T17 busy raised then low at
  the err pulse` (a wedged port holds busy high and never pulses, so neither
  pair is contradicted); `T15 the cut was real: ERASE then a WRITE stopped 12
  bytes in`; and T16's two isolation checks, `erased no other region` and `no
  other region's bytes moved`, which pass VACUOUSLY because a wedged port
  issues no further device traffic and so nothing else can move. That vacuity
  is what the T16 guard exists to answer. The completion-ownership phases add
  nine survivors of the same dull kind, one per arm of T19, T20, T21, T22a and
  T22c: their bus counters cannot fire on a port that has stopped issuing
  anything at all, which is what the completion check beside each of them is
  for.
- **M5** (2026-08-20) the completion window swallows the device error
  (`S_WWAIT`'s `if (dev_err_i)` forced false): **fails 39 of 122**, and survives
  the whole suite without T17. The port waits for a `done` a failed device will
  never send, so the commit never answers at all: `run_op` returns -1 after
  100,000 cycles. `busy_seen && busy_ok` does NOT catch this, and the comment
  at that check says so: a wedged port holds busy high, so `busy_seen` is true
  and no pulse arrives to contradict `busy_ok`. Everything after T17 dies with
  it, which is why the count is so much larger than the mechanism.
- **M6** (2026-09-07) the completion latch armed in every state: the ownership
  gate removed from the set, putting the flag back the way issue #14 found it.
  **fails 6 of 122**, one per arm of the unsolicited-completion table above and
  nothing else in the suite — before those phases the same mutation was green.
  The same edit plus the withdrawn one-line clear in `S_WHDR`, the fix the
  ticket proposed first and then retracted, **fails 5 of 122**: it closes the
  header-collection arm alone, `S_WEREQ` stays exposed on the commit side, and
  a restore never enters `S_WHDR` at all. It is measured rather than argued
  because "that would not have been enough" is exactly the shape of claim this
  file has had to retract before.
- **Probes** (mutations of the TEST, not the RTL). Arming T16's tear as
  `arm_err(1, -1)`, so the WRITE fails before its first byte moves, fails 1 of
  122. Replacing the torn commit with a bare `rc = 1` and no device traffic at
  all — the port the T16 prose names as the threat — fails 3 of 122. Under the
  previous guard that second probe failed only ONE check, the erase count,
  while the payload guard passed on residue from an earlier phase.
- **Model probe**: changing only the DEVICE MODEL to roll the last 4 bytes back
  to 0xFF on a completion-window failure — the half-programmed page a real NOR
  may leave — must not redden a check about the PORT. The T17 restore check
  did exactly that, and so did the T16 byte comparison. Neither does now, by
  two different routes: T16's moved onto the bus, T17's moved to assert after
  a `done` where the array is known. The half-page model is 122 PASS, 0 FAIL.
  See the matrix below for every pre-fix form against every model.

### Device-error arm coverage

`KL_pp_nvm_port.sv` has twelve `if (dev_err_i)` arms. Each was forced to
`1'b0` in turn and the suite re-run, so this table is measured, not argued —
and it is now **checked by a script rather than by hand**: `measure_figures.py`
re-runs every arm, cross-checks the arm COUNT against the RTL, and re-measures
**every figure in this file**: eighteen mutations and probes, seven device-model
result rows, and all thirty cells of the pre-fix matrix. CI runs it.

The covered set is DERIVED, not asserted. Every `N of M` and `N PASS, N FAIL`
here is a claim by default, satisfied only by a measurement or by an explicit
waiver whose reason and absorbed count the script prints on a clean run. A new
figure is a hard error until it is measured, so it cannot be added silently --
and it cannot be deleted to silence the gate either, because deleting it makes
the measurement that owns it fail instead.

**What that does NOT establish, stated plainly because an earlier version of
this paragraph claimed otherwise.** The default is inverted over the SHAPE of a
figure, and shapes are recognised, not resolved. An earlier version argued the
vocabulary could not grow behind the gate because English number words are a
closed class. The argument is true and beside the point: the closed class is
number words, the open class is ways of writing a ratio, and closing one axis
leaves the other. Ten of thirteen phrasings still evaded, two of them using
digits only -- `fails 22 of the 122 checks` and `fails 22 out of 122`. Both are
caught now, and `| Mx | 22 |`, `reddens 22 checks`, `a fifth of the suite`,
`68/90ths` and `24%` are not. A real closure would mean treating every bare
integer as a claim: measured, 292 numbers in this file fall outside every claim
and waiver, so the waiver list would be larger than what it protects. This is a
strong default that catches every phrasing anyone has written here. It is not a
proof that none can be written, and the difference is the whole subject of this
section.

It took four rounds to get the gate itself honest, and the failures belong in
the record because they are the same failure four times. Version one checked
only denominators and result-row sums, so seven of eight falsifications walked
past it -- including reverting a numerator to the exact stale value the gate had
been written after finding. Version two added a table of named mutations and
still missed M3, the very numerator that had gone stale, because nothing
required the table to cover this file's own claims. Version three coupled the
two but matched ONE PHRASE, `fails N of M`, so three figures already present
were invisible to it. Version three also declared the thirty matrix cells
unmeasurable because their check forms no longer exist in the tree -- a cost
choice dressed as an impossibility, contradicted by this file's own sentence
that re-deriving the matrix is re-running it. Each version closed a narrower
class than it claimed. Inverting the default is what ended that, and it paid for
itself on its first run by finding that the coincident-completion figure could
not be re-derived at all: its recipe had never been committed. The number was
sound; it was unverifiable rather than wrong, so the recipe was committed rather
than the figure retracted.

Run `make -C tb/nvm_port figures` after any change to this suite. About four
minutes on two cores; it prints its own derived build count. That is the price of figures that four
review rounds found stale. Two of those rounds found the arm TABLE stale; the
other two found stale numerators elsewhere in the file, which is why the gate
covers every figure rather than the table alone.
The arm table specifically has been stale twice. Splitting one T17 check moved every row reaching T17;
later, replacing an array-negative check with a bus check moved every row whose
mutant WEDGES BEFORE T15, because the old check survived those mutants and the
new one does not. The second time a spot-check missed it: M4 and M5 were
re-measured and both were genuinely unchanged, since under those the bytes were
really sent before the swallowed error. **Checking only the figures you changed
is the wrong sample.** Any change to the suite invalidates every number here and
the whole table has to be re-swept.

| line | state | checks failed |
|---|---|---|
| 211 | `S_WEREQ`  | **0 — uncovered** |
| 220 | `S_WEWAIT` | 69 |
| 230 | `S_WWREQ`  | **0 — uncovered** |
| 240 | `S_WHPUMP` | 64 |
| 253 | `S_WDPUMP` | 52 |
| 263 | `S_WWAIT`  | 39 |
| 274 | `S_RHREQ`  | **0 — uncovered** |
| 284 | `S_RHCOLL` | 32 |
| 302 | `S_RHWAIT` | 29 |
| 329 | `S_RPREQ`  | **0 — uncovered** |
| 339 | `S_RPPUMP` | 63 |
| 349 | `S_RPWAIT` | 26 |

**Eight of twelve are covered; four are not.** The survivors are the four
`*REQ` arms, where the device asserts an error before its request is granted.
Reaching them needs an `err_at_req` mode the device model does not have. That
is written down here rather than left to be rediscovered, because a phase list
that reads as complete is worse than one that names its gaps. The other
outstanding item is the same: `09_verification.md:56` sets the bar as "cut at
randomized commit points ... every record type cut >= once", and this suite
uses fixed cut points on both sides, so the randomized half is still owed.

### Reachability pins, and why they exist

T17 and T18 name the windows they cover, and until a review probed them nothing
CHECKED that they reached those windows. Both were measured green under probes
that removed the thing being tested:

- moving T17's cut off the completion window, so `S_WWAIT` is never entered:
  **122/122 green** before, now fails on `T17 the cut was in the completion
  window: every byte sent first`.
- replacing T18's three device errors with a bad stored magic, so ZERO device
  errors occur anywhere: **122/122 green** before. The op log alone could not tell
  them apart, because the port issues the header READ BEFORE validating it, so
  a refusal and a device error produce the same two ops. Distinguishing them
  needed a count of DEVICE-raised errors, separate from the port's own `err`
  pulses; `dev_errs` is that counter and each arm now pins it.
- replacing a T18 arm with a bare `r = 1`, port never touched: now fails 3.

The general shape: a phase that names a window is not the same as a phase that
proves it entered one, and the evidence for the difference lived only in the
"Device-error arm coverage" table, which this file says has gone stale twice.
That table, and every other figure here, is now re-measured by
`make -C tb/nvm_port figures` and gated in CI.

### On checks that cannot fail alone

TWO added checks are implied by a neighbour:

- `T16 the neighbour's stored bytes are untouched` is subsumed by `no other
  region's bytes moved`, now that the latter compares all of `REG_BYTES`.
- `T17 the port is idle after the late failure` is structurally implied by
  `rc == 1` plus the next commit succeeding. It is kept because it states
  F02.8's busy envelope -- busy low once the terminating pulse has passed --
  on the signal that carries it, so it sits on the specification side of the
  rule below rather than restating the implementation.

Both are kept deliberately, because a weak specification claim beside a strong
implementation pin records WHAT is required separately from HOW the port
happens to satisfy it today, and the two drift apart.

The rule this suite follows, stated once: a check may restate a stronger
neighbour when it states the SPECIFICATION, but a check that only restates the
same implementation fact in other words is removed. That is why `rc != -1` was
dropped from T17 while the two above were kept.

**A third check was listed here and the claim was FALSE**, so it is recorded
rather than quietly deleted. `T15 unless the old record survived, a torn image
never restores as valid` was called weaker than the header-agreement check
beside it, on the evidence of twelve arms and four models showing no
divergence. Measured directly by moving T15's tear into the completion window:
that check FAILS while the header check PASSES, 2 of 122. It can fail alone, so
it is not a member of this section at all. The error is the same shape as the
corollary retracted below -- a general claim generalised from the states that
happened to be tried -- and this file has now made it twice, because "no
divergence across the cases I ran" is not "cannot diverge".


### Where a check may read from

FIVE checks in this file were written against what the flash ARRAY held and
had to be rewritten, because what the array holds is the device MODEL's choice,
not the port's behaviour. FIVE device models and one combination were run, RTL
byte-identical. Four vary what the array RETAINS; the fifth, coincident
completion, varies the HANDSHAKE instead -- the device raises `dev_done_i` on
the same edge that moves a pump's final byte, which `KL_pp_nvm_port.sv:175-179`
says the sticky `done_seen_r` latch exists for. It is a contract freedom rather
than a broken peer, and the port handles it. Its whole interest was that
deleting that latch was INVISIBLE without it, which stopped being true when
T21 and T22 landed -- it still catches far more of that deletion than the
pristine model does, and it is the only model here that varies the handshake
for EVERY phase rather than at one armed moment. It is not a separate
implementation any more either: the behaviour is the harness's own armed
backend (`present_coincident_completion`), which T22 arms for one commit and
one restore, and this model is the same arming left on for the whole run. That
matters for what the model can be trusted to say -- a model spliced in from the
gate is a second implementation of the thing under test, and this one is not. The four array-flavoured models:
this one, which keeps every accepted byte; a half-page model, which drops the
last four on a failure; a page-buffered NOR, which keeps none until the program
cycle ends with `done`; and a lazy-erase backend, which answers ERASE with
`done` without rewriting the array at all. None is invented. The port's own
header names the last one ("backends without erase semantics answer ERASE with
done at once"). `02 SS8` does list host filesystem via `mgmt` among the
permitted backings in general, but NOT for these records: the parent's
`sw/litex/milan_soc.py` places the binding records in a journal slot that is
deliberately RAW, no filesystem,
for exactly this reason. The lazy-erase freedom is real and is what the models
below exercise; the host-filesystem framing was too wide and is withdrawn.

The rule:

> **After a device `done`, assert on the array only for what the port itself
> put there. After a device `err`, assert on what the port SENT or REQUESTED,
> never on what the array retained.**

The `done` clause carries that qualifier because a device SIDE EFFECT is not
the port's behaviour either: `T1 erase visible past the record` asserts after a
`done` and still reddens under lazy erase, since whether an ERASE rewrites the
array is the backend's business. T1 is pre-existing and left as it is, named
here as the one known remaining member rather than quietly fixed. It is the
exception the power-cut preamble points at.

**A negative claim about the array is NOT automatically safe.** An earlier
version of this section said it was, and that was false: under lazy erase
COMBINED WITH page buffering the old record survives a torn commit intact, so
`the torn image is neither the old record nor the new one` reddens for a device
doing exactly what #70 asks. The two freedoms are needed TOGETHER, measured by
printing `old_intact` after T15's tear with the RTL byte-identical:

| model | old record intact |
|---|---|
| pristine | 0 |
| lazy erase alone | 0 |
| lazy erase + page buffering | **1** |

Under lazy erase alone the write still lands and the old record dies with it.
A check that goes red when the device gets the requirement RIGHT is the wrong
check. Where the property genuinely is about the array, CONDITION it on what
the array holds rather than asserting it, the way T15's header check does.

But a condition must be LIVE, or it hides a check as effectively as it rescues
one: a guard always true under the model CI runs silently disables everything
behind it. Check both arms independently. Fix B's disjunction was verified that
way -- under the pristine model `old_intact` fails alone while
`refused || crc_rejects` passes alone, and under lazy erase PLUS page buffering
the reverse -- lazy erase alone gives the same result as pristine -- so it
is conditioned AND still doing work in CI.

Applied here:

- **T16** reads `sent`, the write-bus handshake log, instead of the region's
  bytes. Identical discriminating power, zero model dependency.
- **T17** commits a good record first, so the array is known under every model
  because that commit ended in `done`, and only then exercises the read side,
  pinning the device ops the way T2 does so a fabricated restore cannot pass.
- **T15** had THREE members. Its branch pin surfaced under the page-buffered
  model; the other two needed lazy erase AND page buffering together:
  - its branch pin no longer records WHICH branch fired, because which one
    fires legitimately differs by device -- this model keeps the bytes so the
    CRC rejects, a page-buffered NOR discards them so the port rightly refuses
    at the header. It pins that the branch the port took AGREES with what the
    array holds, which is the port's behaviour under any model.
  - "the cut was real" is stated on the bus: ERASE then a WRITE that stopped
    12 bytes in, checked against `sent`.
  - the #70 property is CONDITIONED rather than asserted -- unless the old
    record survived, a torn image never restores as valid.

| model | result |
|---|---|
| pristine | **122 PASS, 0 FAIL** |
| half-page | **122 PASS, 0 FAIL** |
| page-buffered NOR | **122 PASS, 0 FAIL** |
| lazy erase | 121 PASS, 1 FAIL, only the pre-existing `T1` |
| lazy erase + page-buffered | 121 PASS, 1 FAIL, only `T1` |
| coincident completion | **122 PASS, 0 FAIL** |

A device model variant is the cheapest way to find a check that tests the
harness rather than the DUT, and it belongs in the standing mutation set. Each
addition found members the previous ones could not. Rather than say which,
here is the measurement: every pre-fix form re-injected, every model run, RTL
byte-identical throughout. An attribution sentence drifts from the runs; this
cannot, because re-deriving it is re-running it.

Re-running is not enough on its own, though, and the reason is worth stating.
Two people reconstructing these forms from the old commits share whatever
transcription error both make, and all thirty cells agree either way. That is
not hypothetical: one reconstruction merged two T17 checks into one conjunction
and moved the array capture from after the restore to before it, and every cell
still agreed. So each row's predicates are additionally pinned VERBATIM against
the revision they were recovered from -- git is the third party, and it costs no
builds. Every row carries at least one pin, which the gate enforces: the first
version of that pin had five predicates and all five were T17, the one row where
a defect had already been found, leaving the other four rows unpinned.

Two further rules close what those two share. **Every condition line of every
injected CHECK must be pinned**, not merely one line per row: T16's form spans
two lines, and deleting the second left the row nominally compliant while
re-opening the exact escape the pin existed to close. The rule is read off the
artifact rather than set as a threshold, because the forms carry one, three and
three checks and any count would be arbitrary. And **no injected line may appear
more times than in its source revision**, which catches a structural change that
moves no cell: prepend a second restore and the predicates stay verbatim while
every cell stays byte-identical, so neither of the other two mechanisms sees it,
but the duplicate IS the structure. An earlier draft of this paragraph called
that case unclosable. It is not, and the version that was tried first --
diffing the injected span against the git hunk -- fails for a different reason
worth recording: T17's form merges removals from two revisions and T15's from
three, so it false-positives unless given a splice budget of three or more.

**What still gets through**, narrowed to two nameable cases rather than left as
a general excuse: an invented line that happens to exist elsewhere in the
pre-fix file, and an ANCHOR change that moves no cell. The anchor half is the
hard one; moving an anchor after the good commit flips ten cells, so the cell
comparison is a real backstop there, but it is a backstop rather than a pin.
The merged T17 form that started all this was caught only because it also
altered predicate text, which was luck rather than coverage.

| pre-fix form | pristine | half-page | page-buf | lazy | lazy+pb |
|---|---|---|---|---|---|
| T16 byte comparison | pass | **FAIL** | FAIL | FAIL | FAIL |
| T17 restore vs the record | pass | **FAIL** | FAIL | pass | FAIL |
| T17 restore vs the array | pass | pass | **FAIL** | pass | pass |
| T15 branch pin | pass | pass | **FAIL** | pass | FAIL |
| T15 cut was real | pass | pass | pass | pass | **FAIL** |
| T15 #70 property, unconditioned | pass | pass | pass | pass | **FAIL** |

Bold marks first discovery, reading left to right. By MEMBER that partitions as
**half-page 2, page-buffered 1, the combination 2 = the five** named above; the
six rows exceed the five members because T17's restore appears twice, which is
the most instructive line in the table:

- **T17's restore was found twice, by two different models.** Half-page killed
  the record-relative spelling. The array-relative fix written in response
  SURVIVES half-page -- the very model that prompted it -- and page-buffered
  killed it anyway. Passing the model that found the bug is not evidence the
  fix is model-independent.

Every row passes under pristine, which is why all six survived until a model
beyond the shipping one was tried. Trying one model is how a family of five
looked like a family of one; trying one freedom at a time is how the last two
stayed hidden after three models had been run.


### What this suite does NOT establish

Recorded so the phase list does not read as closing #70:

- **#70's desk-proof sentence is "leave the PREVIOUS SAVED SET intact", and this
  layer cannot meet it.** T16 pins "every OTHER record", which is honest and is
  what the port can guarantee, but it is weaker precisely on the record being
  rewritten. Covering that is the crc16's job, and the crc16 exists — in
  `KL_acmp_nvm_shadow`, on the synthesized path. What does not exist is A/B
  promotion. So the gap is narrower than "nothing covers it": the manager can
  reject a torn record, it just cannot recover the one it replaced.
- **A restore failure is one signal for three situations**: a refused region, a
  torn header, and a tear after a complete header has already been forwarded.
  T18 pins that each reports `err`; it does not distinguish them, and the
  specification requires the manager to. Tracked as issue #20; issue #16 stated
  this as a port-face defect and was closed, because the manager already makes
  the distinction — what survives is narrower and is #20.
- **NONE of the twelve `dev_err_i` arms can fire on any bitstream that exists.**
  The parent answers this port's device face with a blank-flash responder that
  ties `nvm_dev_err_i` to `1'b0` (`milan-fpga hdl/milan/KL_pp_shadow.sv:1010`).
  That is the largest limitation here and it was omitted from this list: the
  whole error-handling half of the port, and every row of the "Device-error arm
  coverage" table, is unreachable until a real backend lands. Note the responder is not inert - it
  drives `nvm_dev_done_i` and answers every command - so what makes issues #14
  and #15 unfirable is that it is WELL BEHAVED, not that error is tied off. The
  port's own `nvm_err_o` is live and fires on every restore on the shipping
  build. **That paragraph describes the parent at the revision it was written
  against, and this repository cannot re-derive it**: the device face is
  answered outside this tree, the responder there has since been reported
  changed, and nothing here re-checks it. Read it as a statement about a parent
  revision, not as a live reachability result either way — the phases below
  prove a contract, not a bitstream.
- **The device model was well-behaved by construction**, and the half of the
  contract that lives in the HANDSHAKE went untested for exactly that reason.
  The five variants in "Where a check may read
  from" -- pristine, half-page, page-buffered NOR, lazy erase, and lazy erase
  plus page buffering -- all vary what the array RETAINS. Three armings vary the
  handshake now, all of them in "Completion ownership": the `done` that belongs
  to no command, which is what closed issue #14; the completion that rides its
  own grant; and the completion that rides a command's final byte, whose arming
  the coincident-completion model leaves on for a whole run rather than for one
  phase. **#15 is still open
  and this suite is still blind to it**: the port has no timeout, so a backend
  that simply never answers holds it busy forever, and no phase here bounds
  that wait or asserts anything about it.
- **No phase asserts `rst_n` after init.** "Power cut" means "the device raised
  `err`" throughout this file. A real reset mid-commit is the path a power cut
  actually takes, and it is not modelled: after one, the port forwards a 32-byte
  torn image with 23 bytes erased as a well-formed record. That is #70's
  "half-record that restores as garbage", reached the way it actually happens.
  Tracked as issue #18.
- **Three of the four RTL mechanisms issue #19 lists still have zero coverage**:
  the low magic byte (`hdr_r[1]`, since both magic tests corrupt only
  the high byte), the payload bound's upper edge (`<=` to `<` is green, so the
  largest legal record can be silently refused), and the short-read defence at
  `:294`, whose failure
  mode is a hang on the boot restore walk and which no `dev_err_i` mutation can
  reach because it guards `dev_done_i`. The fourth was the sticky `done_seen_r`
  latch, and it is covered now — see "Completion ownership" for what closed it
  and by how much.
- **The `err` clause of the rule has THREE known exceptions**, and T1 is not
  among them: T1 asserts after a `done` and reddens only under lazy erase, so
  it is a `done`-clause exception. The three are T16's isolation checks, and a coarse-erase
  model where a sector spans regions reddens all three with the RTL untouched.
  The erase-count check does not redden, which is the asymmetry the rule exists
  to describe.
