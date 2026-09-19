<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Saved-state snapshot ownership and acknowledgement identity

> **Status: PROPOSED CONTRACT.** This page is the design phase of issue #419.
> No product RTL or firmware change is made by this page: it states the
> contract an implementation lane would build, and nothing on the
> [saved-state page](SAVED_STATE_FASTCONNECT.md) moves until that lane lands.
> Implementing it is a separate lane under issue #70, with the two
> donor-interface scopes D1 and D2 of section 13. The contract is accepted only
> on two POSITIVE independent reviews of the pull request that adds this page.
>
> Two product decisions are recorded, and the contract is built on both:
>
> - **Separate pending bit** (owner decision, 2026-09-18,
>   [issue comment 5730427393](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5730427393)):
>   accepted producer work not yet represented in a verified slot is reported
>   on its own pending bit, not folded into a composite durable bit (section
>   6.1; the composite bit is rejected in section 15).
> - **One summary bit** (manager decision, 2026-09-19, which the owner may
>   overrule,
>   [issue comment 5739523021](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5739523021)):
>   the controller-visible status carries the pending bit as one bit, and the
>   per-record list of open records stays on the backend's own register face
>   and the console (section 16).

Source examined: dev `36ee8a37` (protocol-processor `8f2f58fb`, gptp-processor
`c1b61743`, third_party/verilog-axis `48ff7a7e`). Where this page says the
current source, it means that commit. A claim marked EXECUTED comes from the
run script at that source, graded in its results files; a claim marked DERIVED
does not. Case and check names are the ones the run script grades.

This page lands on dev `e578abad`, whose three submodule pins are the ones
above. Between `36ee8a37` and `e578abad`, the work of issues #398 and #401
changed seven of the files the evidence examined: the firmware writer's five
waits became generated constants with their values unchanged; the other edits
generate the CRF boot word and the fabric boot constants from one derivation,
drop the ADP capabilities write, and touch two register-map rows and the
configuration schema version. The evidence was not re-run at `e578abad`.

The executable evidence is kept out of this tree, on a branch that is never
merged. Every evidence citation on this page names the branch, the commit and a
path in it:

- the proposal as delivered:
  `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/PROPOSAL.md`;
- the command record, with every command, exit code and digest:
  `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/COMMAND_RESULTS.md`;
- the run script:
  `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/proposal-evidence/run.py`;
- its graded results:
  `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/proposal-evidence/results.txt`
  and
  `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/proposal-evidence/results.json`.

On that branch the checkout root, two forge account names and two agent-system
names are replaced by placeholders. Ten source copies under
`proposal-evidence/sources/` therefore differ from the digests the command
record lists, and the three files it lists under
`proposal-evidence/prior-session/` are left out as history; every other listed
digest matches.

Two repository gates refuse words the evidence uses: the documentation wording
gate refuses one stem in any committed Markdown (`DENY_CI` in
`scripts/docs_check.py`), and the tree-wide identity scrub refuses the
evidence's four-letter strobe name as a whole word (`IDENTITY_RULES`, same
file). This page therefore calls the capture proof an attestation: its strobe
is ATTEST, its state ATTESTED and its status flag attested. Evidence
identifiers are respelled the same way, one to one, so
M08_attestation_ignores_grant is the evidence's mutant M08, and
unattested_capture_never_flashed is found in the results by its unchanged
suffix. Phase labels such as @cert are quoted unchanged.

A section number that is a link points into the
[saved-state page](SAVED_STATE_FASTCONNECT.md); a plain section number is this
page's.

## Contents

- **[1. Context](#1-context)** -- Three reproduced defects and the round-2 concern.
- **[2. What reproduces at the current source](#2-what-reproduces-at-the-current-source)** -- Three defects fail.
- **[3. Decision](#3-decision)** -- Seven rules: open bit, capture, identity, pending bit.
- **[4. Record ownership: the open vector](#4-record-ownership-the-open-vector)** -- Grant opens, WRITE closes.
- **[5. The capture handshake and state machine](#5-the-capture-handshake-and-state-machine)** -- Strobes, status, identity.
- **[6. Next-state functions, and the separate pending bit](#6-next-state-functions-and-the-separate-pending-bit)** -- Priorities explicit.
- **[7. The writer sequence](#7-the-writer-sequence)** -- Boot, service, capture, seal, program, acknowledge.
- **[8. The round-2 concern, answered](#8-the-round-2-concern-answered)** -- Three concerns, executed refutations.
- **[9. Ordering coverage](#9-ordering-coverage)** -- Every ordering with its case and checks.
- **[10. The four outcomes of a record operation](#10-the-four-outcomes-of-a-record-operation)** -- Kept distinct.
- **[11. Persistent-field materialization](#11-persistent-field-materialization)** -- Which field groups have a record writer.
- **[12. The section 9.2 revocation discrepancy](#12-the-section-92-revocation-discrepancy)** -- RTL follows prose.
- **[13. Donor dependencies, each its own scope](#13-donor-dependencies-each-its-own-scope)** -- D1, D2, D3.
- **[14. Old writer on new gateware, and the reverse](#14-old-writer-on-new-gateware-and-the-reverse)** -- Refused.
- **[15. Alternatives rejected](#15-alternatives-rejected)** -- Ten alternatives, including the composite durable bit.
- **[16. Per-record reporting versus one summary bit](#16-per-record-reporting-versus-one-summary-bit)** -- Decided: one bit.
- **[17. Consequences](#17-consequences)** -- What the contract changes and costs.
- **[18. Cost](#18-cost)** -- Measured area and firmware size, derived timing.
- **[19. The executable model and its omissions](#19-the-executable-model-and-its-omissions)** -- Scope and totals.
- **[20. UNRESOLVED](#20-unresolved)** -- Six items this contract does not settle.
- **[21. Traceability](#21-traceability)** -- Acceptance bullets and obligations mapped to sections.

## 1. Context

- Issue #418 reproduced the acknowledgement race: a WRITE completes after the
  writer's copy and before its acknowledgement, and the acknowledgement clears
  nvm_dirty, so a change no slot holds reads as durable.
- Round 1 was answered by the manager counterexample: an ERASE that ends in
  error emits err without done, the tracked backend then admits the erased or
  partly erased record into the next slot with nvm_dirty 0, and the
  acknowledgement is accepted.
- Issue #420 established the one-pulse re-arm failure: the parent derives the
  backend's change_i from the rising edge of the dynamic-state store's sticky
  level, so a second change while the level stays high is never reported, and
  the dynamic-state fields it reports have no record writer at all.
- Round 2 (never reviewed) carried a manager source-only concern: capture
  validity and the producer hold were not re-checked before the flash write;
  the sequence and the authoritative slot advanced before the acknowledgement
  reference was checked; an expired hold could admit a new ERASE while an old
  ownership mask was in use.

Authority: [`REQUIREMENTS.md`](../../REQUIREMENTS.md) (required Milan state
survives power loss); the [saved-state page](SAVED_STATE_FASTCONNECT.md)
sections [6](SAVED_STATE_FASTCONNECT.md#6-the-record-image-format-klj2),
[7](SAVED_STATE_FASTCONNECT.md#7-durability-the-ab-contract),
[9](SAVED_STATE_FASTCONNECT.md#9-what-the-fabric-may-claim-the-durability-and-liveness-contract)
and [14](SAVED_STATE_FASTCONNECT.md#14-what-this-page-does-not-decide); the
ratified KLJ2 [section 6.1](SAVED_STATE_FASTCONNECT.md#61-the-container)
erased-record rule, which this proposal does not change.

## 2. What reproduces at the current source

EXECUTED at dev 36ee8a37 and donor 8f2f58fb. The tracked build is the
unmodified `hdl/milan/KL_nvm_backend.sv` and the unmodified
`sw/firmware/milan_baremetal/milan_baremetal.c`, co-simulated with the real
donor producer path. All three historical defects still reproduce, at both
shipped shapes:

| Defect | Case : check | Tracked 1x1 | Tracked 8x8 | Prototype |
|---|---|---|---|---|
| Issue #418 acknowledgement race | A2_write_between_verify_and_ack : ack_retires_only_slot@post_ack:0x20 | FAILS | FAILS | passes |
| Round-1 ERASE-error counterexample | B1_erase_error_full_span : last_verified_kept@end:0x20 | FAILS | FAILS | passes |
| Issue #420 one-pulse re-arm | E1_dyn_change_ack_then_second_change : no_durable_claim_unmaterialized@end | FAILS | FAILS | passes |

The run script refuses to report success unless the tracked build fails all
three (its PROD_MUST_FAIL list), so the checks are shown not to be vacuous.
Other tracked-build failures of note, 1x1: a duplicate acknowledgement
retires newer work (A5); the ERASE-to-WRITE gap is promoted (B5); a partial
WRITE blocks every later record (B10); an abandoned stream, a silent write or
withheld readiness blocks an unrelated record already waiting to be committed
(B9, D4c, D4d); two failed
records are both promoted as erased (B6b); a power cycle after B1, B2 or B4
restores the wrong bindings (R_power_cycle); a reported flash failure does
not revoke nvm_backed until the 8000 ms commit deadline (F2); the manager
alarm never revokes (B1 to B4); a concurrent update during a 3 s erase
revokes nvm_backed once (A9); an acknowledgement from before a reset retires
work after it (U1).

## 3. Decision

1. Every allocated record carries an OPEN bit in the backend. The GRANT of a
   mutating operation (WRITE or ERASE that will present memory writes) sets
   it; only a whole-record WRITE that completes with done and no error clears
   it. ERASE completion, err without done, a partial WRITE, an abandoned
   stream, permanent silence and withheld readiness all leave it set.
   Device-idle and erased bytes are never a record boundary.
2. The writer captures the record area into a PRIVATE stage it alone writes,
   prefilled with the last verified slot, and copies only records whose open
   bit is clear. An open record keeps its last verified bytes.
3. The capture is bounded: from the ARM, mutating grants are deferred (never
   refused) for at most T_HOLD_MS_P = 50 ms; reads are never deferred. The
   backend ATTESTS the copy in hardware, and the attestation is false if any
   mutating grant happened between the arm and the attest, which can only
   happen after the hold lapsed. Only an attested capture reaches flash.
4. nvm_dirty keeps its [section 9.1](SAVED_STATE_FASTCONNECT.md#91-the-bits)
   meaning and becomes two halves: dirty_live
   (record completions the current capture does not hold) and dirty_cap (what
   the open capture holds). The acknowledgement quotes the capture identity
   and can reach only dirty_cap, so work completing before, on or after its
   edge is never retired by it.
5. Accepted work that is in no verified slot and that nvm_dirty does not
   report, namely a producer-held change or an open record, is published on
   its own bit, nvm_pend (owner decision). No acknowledgement touches it.
6. A reported ERASE, PROGRAM or VERIFY failure and the manager alarm revoke
   nvm_backed, as
   [section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven)'s
   prose lists (section 12).
7. The generator that emits this contract withdraws the older writer's image
   constant, so an older writer does not compile against new gateware, and
   the new writer refuses an older generator (section 14).

## 4. Record ownership: the open vector

One bit per ALLOCATED record id of
[section 4.2](SAVED_STATE_FASTCONNECT.md#42-the-allocation----decided-the-donors-f078-rule-unchanged)
at the shape; an unallocated
id is a constant 0. Read by the writer as words 8 to 15 of the backend face
(word 8 + k holds ids 32k to 32k + 31).

| Event on the device face or control face | Effect on open[r] | Priority |
|---|---|---|
| reset | every allocated record OPEN (unknown until the writer reloads) | 1 |
| image re-based: a write to word 0 or 1, or to a channel-map table | every record OPEN | 1 |
| GRANT of a WRITE or ERASE on r, image configured, span in bounds, effective length nonzero | open[r] set (applied one cycle after the grant) | 2 |
| RELOAD strobe (writer validated the window from a verified slot) | every record CLOSED except the one an in-flight mutating operation owns | 3 |
| whole-record WRITE on r (offset 0, length equal to the record length) ends with done and no error | open[r] cleared; the same completion sets dirty_live | 4 |
| ERASE on r ends with done | no change: open[r] stays set | - |
| WRITE or ERASE on r ends with err and no done | no change | - |
| partial WRITE on r ends with done | no change | - |
| stream abandoned, accepted write silent, readiness withheld | no change (the operation never ends) | - |
| any READ | no change | - |

A grant on the same edge as a close or a reload wins, because its operation
is still to come. The one-cycle delay of the set is safe because the writer
reads the vector only after its arm and the hold defers every mutating grant
from the arm on; a grant that races the arm is one cycle before it and its
set lands on the arm edge (EXECUTED: C1a_real_port_arm_after_erase_done, the
WRITE requested on the arm's own edge).

Why the grant and not a completion: the grant is the only point at which the
backend knows an operation will mutate a record, and a whole-record WRITE
with done is the only point at which it knows the logical record is complete.
Mutant M01_open_at_erase_completion (killed by B1) and
M02_close_on_any_completion (killed by the real-port case
C1g_real_port_copy_inside_erase_write_gap) are the two cheaper rules.

## 5. The capture handshake and state machine

### 5.1 The control face

PP_NVM_SEL word 4, the strobe word (written through PP_NVM_STAT, write one to
pulse). Bits 0 to 2 are unchanged; 3 to 6 are new; the acknowledgement word
carries the capture identity.

| Bit | Strobe | Meaning |
|---|---|---|
| [0] | heartbeat | re-arms T-NVM-WRITER-ALIVE (unchanged) |
| [1] | ACK | commit acknowledged; [31:16] quote the capture identity |
| [2] | START | opens the commit bracket (unchanged) |
| [3] | ARM | opens a capture |
| [4] | ATTEST | asks for the attestation |
| [5] | RELEASE | closes the capture without retiring anything |
| [6] | RELOAD | the window now holds a validated container |

New read words: word 5, the capture identity (CAP_ID_W_P bits, 16 by
default); words 8 to 15, the open vector.

PP_NVM_STAT read layout (tracked bits unchanged in place):

| Bits | Field |
|---|---|
| [31:24] | contract tag, value 0xC3 (0 on older gateware) |
| [23] | unres: at least one record is open (diagnostic) |
| [22] | pend: the pending bit of section 6 |
| [21] | arm refused (the last ARM found a capture open or no valid image) |
| [20] | ack refused (the last ACK was not accepted) |
| [19] | attested |
| [18] | valid (no mutating grant since the arm) |
| [17] | hold |
| [16] | open |
| [15:12] | verdict (unchanged) |
| [10] | commit_busy (unchanged) |
| [9] | nvm_stale (unchanged) |
| [8] | nvm_dirty = dirty_live OR dirty_cap, committable image work |
| [7] | img_valid, [6] nvm_backed, [5] img_cfg, [4] dev_busy (unchanged) |

### 5.2 The capture state machine

One capture at a time. Its identity advances only on an accepted ARM, so it
names captures, not attempts.

| From | Event | Condition | To | Effect |
|---|---|---|---|---|
| IDLE | ARM | image configured and validated, no reload or re-base on the edge | HELD | identity + 1; dirty_cap = dirty_live; dirty_live = 0 unless a completion lands on the same edge; hold timer = T_HOLD_MS_P; valid = 1; attested = 0 |
| open | ARM | - | unchanged | arm refused = 1; identity unchanged |
| HELD | hold timer reaches its bound | - | UNHELD | hold = 0; deferred requests are granted |
| HELD or UNHELD | mutating grant | reachable only when hold = 0 | same | valid = 0 (the copy is void) |
| HELD or UNHELD | ATTEST | valid, and no mutating grant on the same edge | ATTESTED | hold = 0; attested = 1 |
| HELD or UNHELD | ATTEST | not valid, or a grant on the same edge | UNHELD | hold = 0; attested stays 0 |
| ATTESTED | ACK quoting this identity | valid | IDLE | dirty_cap = 0 (retired); commit bracket closed |
| open, not attested | ACK quoting this identity | - | IDLE | refused; dirty_cap handed back to dirty_live |
| any | ACK quoting another identity, or no capture open | - | unchanged | ack refused = 1; nothing else changes |
| open | RELEASE | - | IDLE | dirty_cap handed back to dirty_live; commit bracket closed |
| open | RELOAD or re-base | - | IDLE | capture ended; RELOAD clears both halves (the window now equals a verified slot); re-base hands dirty_cap back |

Identity wrap: the identity advances once per accepted ARM, at most once per
commit, so a 16-bit identity repeats only after 65,536 captures; an ACK can
alias only if a stale one from exactly that many captures earlier arrives
while the current capture is attested. EXECUTED control: A8 passes with 16
bits, and the same case FAILS on a build with a 2-bit identity, which aliases
after four captures (proto-w2-1x1; the run script requires that failure).

A lapsed commit deadline does NOT end a capture: a late but valid completion
is accepted as data and does not by itself resurrect nvm_backed (EXECUTED:
C7_late_ack_after_commit_deadline).

The grant rule on the device face: while hold = 1 a WRITE or ERASE request
is not granted and the port holds its request, as KL_pp_nvm_port's interface
already requires (dev_req_o held until dev_gnt_i); a READ is granted. No
refusal and no err is ever issued for a deferral.

## 6. Next-state functions, and the separate pending bit

Stated like
[section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven),
priorities written out:

```
close        = done AND no error AND the operation was a whole-record WRITE
arm_ok       = ARM AND image configured AND img_valid AND NOT open AND NOT (RELOAD OR re-base)
void_grant   = mutating grant AND open AND NOT attested
attest_ok    = ATTEST AND open AND NOT attested AND valid AND NOT void_grant AND NOT (RELOAD OR re-base)
ack_ok       = ACK AND open AND attested AND valid AND id = cap_id AND NOT (RELOAD OR re-base)
end_cap      = open AND ((ACK AND id = cap_id) OR RELEASE OR RELOAD OR re-base)
drop         = end_cap AND NOT ack_ok

dirty_live'  = close ? 1 : RELOAD ? 0 : arm_ok ? 0 : drop ? (dirty_live OR dirty_cap) : dirty_live
dirty_cap'   = RELOAD ? 0 : arm_ok ? dirty_live : (ack_ok OR drop) ? 0 : dirty_cap
nvm_dirty    = dirty_live OR dirty_cap

pend'        = pend_i
nvm_pend     = pend OR (any record open)

loss_event   = ALIVE expired OR COMMIT expired OR reported ERASE/PROGRAM/VERIFY failure OR alarm
loss         = loss_event AND a writer had been live since reset
backed'      = loss_event ? 0 : heartbeat ? 1 : backed
stale'       = loss ? 1 : (backed' AND NOT nvm_dirty') ? 0 : stale
```

Same-edge rules, each EXECUTED: a completion on the ACK edge stays in
dirty_live because the ACK reaches only dirty_cap (A3_write_done_on_ack_edge);
a completion on the ARM edge stays live, costing one extra commit
(U2_close_on_arm_edge); a grant on the ATTEST edge voids the attestation
(U3_grant_on_attest_edge). The (backed 1, dirty 0, stale 1) row stays
unreachable in the state (unreachable_row_never_held, graded on every run).

### 6.1 The pending bit (owner decision)

nvm_pend is published at PP_NVM_STAT[22] on the backend face and, for the
reader of
[section 9.3](SAVED_STATE_FASTCONNECT.md#93-reading-the-three-bits-together),
at PP_STAT[11] (free today: [8] dirty, [9] stale, [10]
img_valid and [15:12] verdict are taken). Proposed status dictionary row for
[section 9.1](SAVED_STATE_FASTCONNECT.md#91-the-bits):

| bit | name | meaning |
|---|---|---|
| [11] | nvm_pend | accepted work that no verified slot holds and nvm_dirty does not report: a change the producer still holds, or a record whose logical write has not completed |

SETS, one cycle after its cause, whenever:

- pend_i is 1. pend_i is a LEVEL wired in KL_pp_shadow: the dynamic-state
  store's sticky persisted-field level (aecp_dyn_dirty_o, today reduced to its
  rising edge), OR, once donor scope D1 lands, any sink the binding manager
  has accepted and not yet flushed; or
- any record is open (section 4).

CLEARS only when pend_i is 0 AND no record is open. pend_i falls when the
manager has flushed every sink (its dirty bit clears on done, or is dropped on
retry exhaustion, which raises the alarm and revokes nvm_backed) and the
dynamic-state level is 0, which today happens only at reset because nothing
writes those fields (section 11). An open record closes at its whole-record
WRITE completion, or at a RELOAD when no operation is in flight on it.

NOTHING ELSE affects it: no ACK, RELEASE, commit, deadline or heartbeat.
It does not drive a commit: the writer commits on nvm_dirty only, so a
pending bit held by an unmaterialized field costs no flash wear (EXECUTED:
pending_drives_no_commit@end on E1, zero erases).

[Section 9.3](SAVED_STATE_FASTCONNECT.md#93-reading-the-three-bits-together)'s
durable reading becomes (backed 1, dirty 0, stale 0) AND pend 0.
The stale recovery rule is unchanged and reads nvm_dirty only: work the
pending bit reports does not hold stale.

Why it is not vacuous: mutant M18_pending_bit_stuck, a pending bit held at 1,
passes every "no false durable claim" check and is killed by convergence
(A1_stable_no_change : converged@end, which now requires the durable reading).

## 7. The writer sequence

The ordinary firmware service, as the prototype translation unit
`branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/proposal-evidence/prototype/milan_baremetal.proto.c`
implements it:

1. Boot. The restore walk validates a slot into the live window. If
   PP_NVM_STAT[31:24] is not 0xC3 the writer disables itself (the runtime
   cross-check of section 14); otherwise it strobes RELOAD and is ready.
2. Service. Heartbeat at most every 500 ms. Commit when nvm_dirty has been 1
   for the debounce window and no commit bracket is open. dev_busy does NOT
   block a commit: an open record keeps its last verified bytes, so a wedged
   producer cannot stop every other record from being saved (mutant
   F05_device_busy_gate_kept, the tracked gate, is killed by B9).
3. Capture.
   1. Prefill the stage from the authoritative slot, or with the
      [section 6.1](SAVED_STATE_FASTCONNECT.md#61-the-container) blank image
      when no slot was ever accepted (F03_prefill_from_blank is
      killed by B1: a blank prefill writes erased records over verified ones).
   2. ARM, then read the status. Not open, or arm refused: RELEASE and retry
      at the next service call.
   3. Read the capture identity (word 5) and the open vector (words 8 to 15).
   4. Copy every CLOSED record from the live window into the stage; an open
      record keeps its prefilled bytes (F02_copies_open_records is killed by
      B1).
   5. Fence, ATTEST, read the status. Not attested: RELEASE, report the
      refusal, retry at the next service call (F01_attestation_not_checked is
      killed by C2).
4. Seal the stage under sequence + 1 and validate it; not VD_OK: RELEASE.
5. START, then erase, program and read back the non-authoritative slot FROM
   THE STAGE. On failure: publish the transaction verdict (which revokes
   nvm_backed), RELEASE, no ACK (F06_ack_after_failed_slot, an ACK after a
   failed slot, is killed by F2).
6. On a verified slot: advance the sequence and the authoritative slot,
   publish VD_OK, ACK quoting the identity, read ack refused. If refused, the
   verified slot stands (its content is an attested capture) and the captured
   work stays owned, so the next commit captures it again.

The backend never touches the stage. After the attestation nothing the
producer does can change what is sealed, programmed or compared: updates land
in the live window during the verify (A2) and during a 3 s erase (A9) and are
carried by the next capture.

## 8. The round-2 concern, answered

| Concern | Answer in this design | Refuting checks (EXECUTED) | Mutants killed |
|---|---|---|---|
| Capture validity and the producer hold are not re-checked before the flash write | The attestation is computed by the backend at ATTEST from the valid flag, which any mutating grant after the arm clears, and the writer does not open the flash transaction unless it reads attested. After the attestation the copy is in a private stage nothing else writes, so no later re-check is needed: fixed by construction | C2 : unattested_capture_never_flashed, last_verified_kept@after:0x21; C2e : never_torn_or_erased@after:0x21 | M08_attestation_ignores_grant (named killer C2, also fails C2e); F01_attestation_not_checked (named killer C2, also fails C2e) |
| The sequence and the authoritative slot advance before the acknowledgement reference is checked | Kept deliberately and made safe by construction: promotion depends on the attestation, which is checked BEFORE the flash write, so a verified slot only ever holds an attested capture of completed records. The ACK decides only whether dirty_cap is retired; a refused ACK retires nothing and the next capture re-covers the work | C8_ack_refused_after_verified_slot : attested_slot_promoted@pre_hb:0x20, refused_ack_retires_nothing@pre_hb, converged@end; A6 : stale_identity_refused@stray | M04_ack_ignores_identity (A6); F06_ack_after_failed_slot (F2) |
| An expired hold admits a new ERASE while an old ownership mask is in use | That ERASE can only be granted after the hold lapsed, and its grant voids the capture, so the stale mask can never be attested; RELEASE hands the captured work back; the next capture reads a fresh mask in which the record is open | C2 (BFM ERASE with no WRITE behind it), C2e (real manager, first WRITE byte slow, the record is one erased span), C2r (real manager, torn record): hold_bounded, unattested_capture_never_flashed, never_torn_or_erased, later_record_persists, converged | M07_hold_never_expires (C2 : hold_bounded:0x21); M10_release_forgets_work (C2 : later_record_persists@after:0x20); M17_hold_expiry_voids_capture (C3 : slow_copy_attests, the expiry alone must not void a copy no grant disturbed) |

Under M08 the torn record of C2r is refused by the stage's CRC validation,
while the erased span of C2e is a valid KLJ2 record and is promoted. A
content check therefore cannot replace the attestation, which is also why the
issue's "valid erased span can mean first boot" point holds.

## 9. Ordering coverage

Every row is EXECUTED on the 1x1 prototype (all pass) and on the tracked 1x1
build. "n/a" means the tracked build cannot express the ordering (it has no
arm, attestation or identity). Producer: "real" is the donor manager and port
at 8f2f58fb; "BFM" is the device-face bus-functional model; "stray" is a
strobe the harness writes on the control face.

| Ordering | Case | Producer | Named checks | Tracked |
|---|---|---|---|---|
| Stable, no change | A1 | real | converged@end, stable_no_churn | passes |
| WRITE completes between verify and ACK (issue #418) | A2 | real | ack_retires_only_slot@post_ack:0x20 | FAILS |
| WRITE done on the ACK edge | A3 | BFM | ack_retires_only_slot@post_ack:0x20 | passes |
| WRITE after the ACK | A4 | real | converged@end | passes |
| Duplicate ACK | A5 | real + stray | ack_retires_only_slot@after_stray:0x20 | FAILS |
| Late ACK while a newer capture is open | A6 | real + stray | stale_identity_refused@stray | FAILS |
| Identity wrap (16-bit holds; a 2-bit identity aliases) | A8 | real + stray | ack_retires_only_slot@end:0x20 | n/a |
| Updates during a 3 s erase | A9 | real | no_revocation_from_concurrent_update, heartbeat_gap<=500ms | FAILS |
| WRITE already granted and in flight at the arm | A11 | real + BFM | inflight_record_excluded@first:0x21 | n/a |
| Last byte accepted before the arm, done after it | A12 | real + BFM | converged@end | n/a |
| ARM on the WRITE's request edge, ERASE done | C1a | real | arm_inside_erase_write_gap:0x21, never_torn_or_erased@after:0x21 | n/a |
| Capture inside the ERASE-to-WRITE gap, ERASE granted before the arm | C1g | real | capture_inside_erase_write_gap:0x21, never_torn_or_erased@after:0x21 | n/a |
| Mutating request during the hold | C1, C1r | BFM, real | deferred_until_attestation:0x21 | n/a |
| Concurrent capture request | C5 | real + stray | concurrent_arm_refused@stray | n/a |
| ACK after the commit deadline | C7 | real | late_ack_accepted_not_resurrecting@pre_hb | passes |
| ACK refused after a verified slot | C8 | real + stray | refused_ack_retires_nothing@pre_hb | n/a |
| ERASE error, full, partial and no byte; WRITE error after ERASE | B1 to B4 | real | last_verified_kept, later_record_persists, no_durable_claim, alarm_revokes | FAILS |
| ERASE with no WRITE yet, gap held open | B5 | real + BFM | last_verified_kept@gap:0x20, no_durable_claim@gap | FAILS |
| Two failed records, then an operation on a third | B6, B6b | real + BFM | last_verified_kept (0x20, 0x30), later_record_persists@end:0x21, open_records_named@end | FAILS |
| First boot, erased records | B7 | real | first_boot_erased_image_accepted@blank_commit | passes |
| First boot, failed ERASE | B8 | real + BFM | never_written_record_stays_erased@end:0x20 | passes |
| Abandoned WRITE stream | B9 | real + BFM | later_record_persists@abandoned:0x20, stuck_record_reported | FAILS |
| Partial WRITE | B10 | real + BFM | later_record_persists@end:0x21 | FAILS |
| Power cycle after B1, B2, B4, B9 | R_power_cycle | slots of the run | restores_last_verified@restored | FAILS (B1, B2, B4) |
| Writer loss and recovery | D1 | real | status rows (0,0,1), (1,0,0), (0,1,1), (1,0,0) | passes |
| Change inside the manager's debounce | E3 | real | no_durable_claim@in_debounce | FAILS; prototype fails without D1 (expected) |
| Flash absent | F3 | real | producer_wait_bounded_by_hold, work_still_owned@end | passes |
| ACK from before a reset | U1 | unit | post_reset_ack_retires_nothing@after | FAILS |
| Completion on the ARM edge | U2 | unit | close_on_arm_edge_stays_live@acked | FAILS |
| Grant on the ATTEST edge | U3 | unit | grant_on_attest_edge_voids@cert | n/a |

The 8x8 prototype passes the eleven-case core set at 8x8 (55 checks).

## 10. The four outcomes of a record operation

Kept distinct, as the issue #420 obligations require. The model injects each at
the memory bridge; none is assumed to be what the shipping bridge does.

| Outcome | Injected as | Backend | open[r] | Published | Case |
|---|---|---|---|---|---|
| Ordinary completion | done, no err | operation ends; a whole-record WRITE closes the record | cleared | nvm_dirty 1 until a capture holding it is acknowledged | A-cases |
| Completion with error | done with err | operation ends with err and no done; device face idle | stays set | nvm_pend 1, unres 1, dev_busy 0; the manager retries; on exhaustion its alarm revokes nvm_backed | B1 to B4 |
| Accepted write, permanent silence | accepted, done never | operation never ends; dev_busy stays 1; the single-outstanding device face grants nothing else | stays set | nvm_pend 1, dev_busy 1; every other record keeps being committed from the stage | D4c, D4e (inside a capture) |
| Readiness withheld before acceptance | ready never rises | as silence, with no byte accepted | stays set | as silence | D4d |

Completion with error is told apart by dev_busy 0 with the record open;
silence and withheld readiness both hold dev_busy 1 and are not told apart by
the status, because the contract relies on neither ever ending.

## 11. Persistent-field materialization

Traced at dev 36ee8a37 and donor 8f2f58fb. The only device-face initiator in
the gateware is KL_pp_nvm_port, driven only by KL_acmp_nvm_shadow; the
firmware writes no record content (it copies whole containers). Record ids
are
[section 4.2](SAVED_STATE_FASTCONNECT.md#42-the-allocation----decided-the-donors-f078-rule-unchanged)'s.

| Ids | Group | Live value held by | Change indication reaching the parent | Record writer | What this contract publishes |
|---|---|---|---|---|---|
| 0x00 | configuration index | KL_aecp_dyn_state, selector 0 | aecp_dyn_dirty_o, a sticky level set on any persisted-field write, cleared only by reset | NONE | nvm_pend 1 from the first change until reset |
| 0x01 | system unique id | no AECP program writes it | none | NONE | nothing changes, nothing to report |
| 0x02 to 0x09 | sampling rate | KL_aecp_dyn_state, selector 1 | the dynamic-state level | NONE | nvm_pend 1 until reset |
| 0x0A to 0x11 | clock source | KL_aecp_dyn_state, selector 2 | the dynamic-state level | NONE | nvm_pend 1 until reset |
| 0x12 to 0x19 | media clock reference | no AECP program writes it | none | NONE | nothing changes, nothing to report |
| 0x20 to 0x2F | binding, parameters and started state | KL_acmp_nvm_shadow | the manager's per-sink dirty (dbg_dirty_o, unconnected today, donor scope D1), then the record's own grant and completion in the backend | KL_acmp_nvm_shadow through KL_pp_nvm_port, the ONLY record writer | the whole contract; pending inside the manager's debounce only with D1 |
| 0x30 to 0x3F | stream format in | KL_aecp_dyn_state, selector 3 | the dynamic-state level | NONE | nvm_pend 1 until reset (E1: two accepted format changes, record 0x30 erased in every slot) |
| 0x40 to 0x4F | stream format out | KL_aecp_dyn_state, selector 4 | the dynamic-state level | NONE | nvm_pend 1 until reset |
| 0x50 to 0x5F | presentation time offset | KL_aecp_dyn_state, selector 5 | the dynamic-state level | NONE | nvm_pend 1 until reset |
| 0x60 to 0x7F | channel maps in and out | the AECP engine's mapping state | NONE: its commit mark, class 6, ends on an unconnected wire in protocol_processor_top | NONE | nothing: a mapping change reads durable (UNRESOLVED 2) |
| 0x80 to 0xFF | user names | KL_aecp_desc_store (SET_NAME) | NONE: commit mark class 7, unconnected | NONE | nothing: a name change reads durable (UNRESOLVED 2) |

Acknowledgement identity repairs none of the NONE rows; what this contract
guarantees for them is only that the status never claims durability over a
change it can see (E1 on the prototype: no_durable_claim_unmaterialized@first
and @end pass, and the tracked build fails both). Materialization itself is
UNRESOLVED 1, and the channel-map and name rows cannot even be reported
until donor scope D2 lands.

## 12. The section 9.2 revocation discrepancy

The
[saved-state page](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven)'s
prose lists five causes that clear nvm_backed: T-NVM-WRITER-ALIVE
expiring, T-NVM-COMMIT-TIMEOUT expiring, a reported erase, program or
read-back-verify failure, a reported JEDEC identity mismatch, and the port's
nvm_alarm. Its next-state function, and the tracked RTL, evaluate only the
two deadlines; the backend has no alarm input and treats a reported verdict
as data. EXECUTED on the tracked build: after a reported failure the status
keeps nvm_stale 0 until the commit deadline (F2 : stale_until_good_commit@failed
fails), and after the manager's retry exhaustion the status reads durable
while the change it abandoned is in no slot (B1 to B4 : alarm_revokes fails).

RESOLUTION: the RTL follows the saved-state page's prose, and that page's
next-state function is corrected to list what is evaluated:

```
loss_event = ALIVE expired OR COMMIT expired
             OR a reported VD_ERASE, VD_PROGRAM or VD_VERIFY verdict
             OR alarm (a level)
```

Reasons, in order of weight:

1. The alarm is the only evidence of a producer change abandoned before any
   record was granted: on retry exhaustion KL_acmp_nvm_shadow drops its dirty
   bit and raises the sticky alarm, so neither nvm_dirty nor the pending bit
   can report the loss afterwards. Without the revocation the status reads
   durable over a lost controller change.
2. A reported transaction failure is known when it is reported; waiting for
   the 8000 ms commit deadline advertises durability for up to 8 s after a
   known failure.
3. No donor change is needed: the alarm is already exported (nvm_alarm_o,
   PP_STAT[4]); the change is one backend input and one connection in
   KL_pp_shadow.

Changing the saved-state page instead (dropping the alarm and the reported
failure from the prose) would ratify the false durable claim of reason 1.
Consequence: the
alarm is sticky in the donor until reset, so after a retry exhaustion the
entity reads nvm_backed 0 and nvm_stale 1 until reset, which is the honest
reading of a lost change. The JEDEC cause has no reporter at the current
source (the writer performs no identity check): UNRESOLVED 5. EXECUTED
controls: M12_alarm_not_revoking is killed by B1 : alarm_revokes@end and
M13_report_not_revoking by F2 : failure_revokes.

## 13. Donor dependencies, each its own scope

None of these touches donor PR 26 or donor issues 14, 15 and 20, which stay in
their own lanes.

**D1, export the binding manager's unflushed state.** Scope: protocol-processor
only, one new output port, no behaviour change.

- Port: protocol_processor_top gains
  `output logic [N_STREAM_IN_P-1:0] nvm_unflushed_o`, driven by
  `u_nvm_shadow.dbg_dirty_o`, which today ends on `nvm_dbg_dirty_nc_w`
  (protocol_processor_top.sv, the u_nvm_shadow instance, line 2365).
- Meaning: bit k is 1 from the cycle the manager takes a change on sink k
  until it flushes it with done, or gives up after RETRY_MAX_P retries (and
  raises alarm_o).
- Parent use: KL_pp_shadow drives the backend's
  `pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_o)`.
- EXECUTED: E3_binding_inside_manager_debounce passes with the export
  modelled (d1=1) and FAILS without it (d1=0, the one listed expected failure
  of the prototype): without D1 a binding inside the manager's debounce reads
  durable.

**D2, export the AECP commit marks.** Scope: protocol-processor only, two
new output ports, no behaviour change.

- Ports: `output logic aecp_nvm_stb_o` and
  `output logic [7:0] aecp_nvm_mark_o`, driven by KL_aecp_engine's
  `eff_nvm_stb_o` and `eff_nvm_mark_o`, which today end on
  `aecp_eff_nvm_stb_nc_w` and `aecp_eff_nvm_mark_nc_w` (declared at lines
  2884 and 2885, bound at 3164 and 3165).
- Parent use: a mark of class 6 (channel maps) or class 7 (names) sets a
  sticky pend_i source until the record that materializes it is written, or
  until reset while no writer exists.
- DERIVED only (the pinned donor does not export them;
  [section 12.1](SAVED_STATE_FASTCONNECT.md#121-the-inventory-derived-from-the-donor)
  of the saved-state page is the program inventory).

**D3, materialization of the non-binding fields.** Not settled here and not
only an interface: a record writer must exist for every NONE row of section
11 before those fields can reach a slot at all. Whether it is a donor-side
manager per group or a parent-side writer behind a second device-face
initiator is its own scope: UNRESOLVED 1.

**No donor dependency** for the hold (KL_pp_nvm_port holds dev_req_o until
dev_gnt_i by its own stated contract and has no grant timeout; EXECUTED with
the real port in C1r, C2r, C2e and C1g) or for the alarm (already exported).

## 14. Old writer on new gateware, and the reverse

- The generator: `sw/litex/milan_soc.py` publishes MILAN_NVM_IMAGE_BASE today.
  The contract-3 generator withdraws it and publishes MILAN_NVM_LIVE_BASE
  (the same window), MILAN_NVM_STAGE_BASE (the private stage) and
  MILAN_NVM_CONTRACT with the value 3.
- An older writer names MILAN_NVM_IMAGE_BASE, so it does not compile against
  the new output. The new writer carries a preprocessor error unless
  MILAN_NVM_CONTRACT is 3, so it does not compile against an older generator.
- EXECUTED, both ways, with the repository's warning flags:
  old_writer_new_generator exits 1 naming MILAN_NVM_IMAGE_BASE;
  new_writer_old_generator exits 1 naming contract 3.
- Runtime cross-check, EXECUTED (mix-newfw-oldgw-1x1): the new writer on the
  tracked backend reads tag 0 at PP_NVM_STAT[31:24], reports that the backend
  does not carry contract 3, disables itself and erases nothing; it therefore
  never converges, and its two failing checks are the expected result.
- An older writer on new gateware at runtime, only if the build refusal were
  bypassed: it never arms, so every ACK it writes names no open capture and is
  refused, nvm_dirty is never retired, and the status never reads durable
  over its commits (DERIVED).

## 15. Alternatives rejected

| Alternative | Rejected because | Evidence |
|---|---|---|
| A composite durable bit: pending work folded into nvm_dirty | Owner decision for the separate bit. Consequences found: the writer commits on nvm_dirty, so a field nothing materializes (every dynamic-state field today) triggers a full A/B commit every debounce window until reset, one sector erase each time; [section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven)'s recovery clears stale only when nvm_dirty is 0, so after any outage the status would read (1,1,1) "recovering" until reset; and the in-flight row of [section 9.3](SAVED_STATE_FASTCONNECT.md#93-reading-the-three-bits-together) would be shown permanently, which is dirty held asserted rather than a missed case repaired | EXECUTED as the alternative build mut-A01_composite_durable_bit (the prototype with the pending work folded into nvm_dirty, its status bit and the stale recovery): it passes every ordering check but FAILS E1 : pending_drives_no_commit@end with 5 full A/B commits (5 sector erases) in 6.03 s of model time for zero committable work, where the separate bit does 0 |
| The tracked rule (an ACK pulse clears dirty; the live image is the copy) | The issue #418 race and the round-1 counterexample | EXECUTED: A2 and B1 fail on the tracked build (section 2) |
| Round 2 as written (an attestation the flash write does not depend on) | A stale mask attests an erased span | EXECUTED: M08 and F01 are killed by C2 and fail C2e |
| A content rule (an erased span means "in progress") | Contradicts the ratified KLJ2 [6.1](SAVED_STATE_FASTCONNECT.md#61-the-container) erased-record rule: first-boot erased records are legitimate, and an erased span validates | EXECUTED: B7 passes only because erased records are accepted; C2e under M08 promotes an erased span that validates |
| Device idle as the record boundary; the tracked device-busy gate | Device idle occurs inside a logical record, and a gate on it lets one wedged record stop every other record | EXECUTED: C1g (idle between ERASE done and WRITE grant); F05 is killed by B9 |
| A completion counter, generation or sticky identity alone, without a per-record open bit | A counter of completions cannot see a record that is not completing, which is exactly the ERASE-error counterexample; the per-record open bit is the smallest sticky identity that names the record | EXECUTED proxies: M01 (open at completion) killed by B1, M02 (close on any completion) killed by C1g |
| Freezing the producer for the whole flash transaction | [Section 9.4](SAVED_STATE_FASTCONNECT.md#94-the-deadlines)'s worst case is 3.06 s at 1x1 and 3.18 s at 8x8, one erase dominating; the control plane would stall for seconds | EXECUTED: M07 (hold never expires) killed by C2 : hold_bounded; F3 keeps the producer's longest request-to-grant wait at 1 cycle with no flash at all; A9 keeps nvm_backed and a 250 ms heartbeat gap through a 3 s erase |
| An edge-detected producer change (the tracked parent glue) | A second change while the level is high is lost | EXECUTED: G01 killed by E1 |
| An acknowledgement without identity | A stale or duplicate ACK retires a newer capture; with the identity checked but not sent, nothing converges | EXECUTED: M04 killed by A6; F04 killed by A1 : stable_no_churn |
| Dirty from accepted bytes instead of a record close | A record whose bytes all moved before the arm but whose completion lands after it is retired unwritten | EXECUTED: M11 killed by A12 |

## 16. Per-record reporting versus one summary bit

> **DECIDED 2026-09-19: option A, one summary bit** (manager decision, which
> the owner may overrule;
> [issue comment 5739523021](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5739523021)).
> The options and the recommendation the decision followed are kept below.

The question: when records are unresolved (open), does the status the
controller-side reader sees name each record, or carry one summary bit?

| Option | What is published | Consequences against [`REQUIREMENTS.md`](../../REQUIREMENTS.md) and [section 9](SAVED_STATE_FASTCONNECT.md#9-what-the-fabric-may-claim-the-durability-and-liveness-contract) |
|---|---|---|
| A. One summary bit | PP_STAT[11] nvm_pend (section 6.1); the per-record vector stays on the backend face (PP_NVM words 8 to 15) and in the writer's console status | [Section 9.3](SAVED_STATE_FASTCONNECT.md#93-reading-the-three-bits-together) stays one reading per entity: durable is (1,0,0) with pend 0. [`REQUIREMENTS.md`](../../REQUIREMENTS.md) asks that required state survive power loss; the reader's decision (is the entity's state durable?) is binary and A answers it exactly. One PP_STAT bit; no new window. Diagnosis per record needs the backend face, which the writer already reads and prints (EXECUTED: open_records_named@end on B6 and B6b names 0x20 and 0x30) |
| B. Per-record reporting in the reader's status | the open vector (53 bits at 1x1, 156 at 8x8) or a count and first id beside PP_STAT | A new read window and a new status-dictionary family sized by the shape; no [section 9](SAVED_STATE_FASTCONNECT.md#9-what-the-fabric-may-claim-the-durability-and-liveness-contract) rule consumes it; the vector changes every grant, so a reader sampling it races the producer; and it still cannot name the fields that have no writer (section 11), so it is not more complete than A |
| C. Summary bit plus a count of open records | PP_STAT[11] plus a small count field | Cheaper than B, but a count says nothing A plus the backend face does not, and it invites a threshold policy [section 9](SAVED_STATE_FASTCONNECT.md#9-what-the-fabric-may-claim-the-durability-and-liveness-contract) does not define |

RECOMMENDATION: A, one summary bit, with the per-record vector kept on the
backend face and in the console status. Reason: the only decision
[section 9](SAVED_STATE_FASTCONNECT.md#9-what-the-fabric-may-claim-the-durability-and-liveness-contract)
asks of the reader is whether the entity's accepted state is durable, which
one bit answers; the per-record detail is a diagnostic the writer already
owns and prints, and publishing it to the reader adds a shape-sized interface
that no rule consumes and that races the producer by construction.

## 17. Consequences

- The writer needs a second image-sized buffer in DDR, the private stage
  (MILAN_NVM_STAGE_BASE): 3264 bytes at 1x1 and 8648 at 8x8.
- A mutating producer request may be deferred up to 50 ms once per commit;
  reads never are. The deferral is a withheld grant on an interface that
  already holds its request; nothing is refused and no err is issued.
- A record stuck open keeps its last verified bytes in every later slot
  while nvm_pend stays 1 and every other record keeps being saved.
- A completion that lands on the arm edge costs one extra commit.
- A verified slot is promoted even when its acknowledgement is refused; the
  refused work is simply captured again.
- nvm_backed now falls at a reported transaction failure and while the
  manager alarm is raised; the alarm holds it at 0 until reset.
- nvm_dirty keeps its [section 9.1](SAVED_STATE_FASTCONNECT.md#91-the-bits)
  meaning; the durable reading gains pend 0.
- The KLJ2 format, the erased-record rule and the A/B rule of
  [section 7](SAVED_STATE_FASTCONNECT.md#7-durability-the-ab-contract) are
  unchanged.
- Until D2 and D3 land, channel-map and name changes can read durable when
  they are not (section 11): this proposal does not hide that.

## 18. Cost

MEASURED, out-of-context synthesis of KL_nvm_backend alone (xc7 family, the
[section 8.3](SAVED_STATE_FASTCONNECT.md#83-the-area-measured) recipe
reimplemented standalone because the tracked script only
accepts its own tops). Calibration: the tracked module at the saved-state
page's name bound (N_NAME_P 30) returns 772 LUT and 377 FF, and 857 LUT
without DSP, exactly the
[section 8.3](SAVED_STATE_FASTCONNECT.md#83-the-area-measured) row.

| Shape | Tracked LUT (with LUTRAM) | Prototype LUT | Delta | Tracked FF | Prototype FF | Delta | DSP |
|---|---|---|---|---|---|---|---|
| 1x1 | 782 | 1058 | +276 | 377 | 471 | +94 | 6 and 6 |
| 1x1, no DSP | 846 | 1118 | +272 | 377 | 471 | +94 | 0 |
| 8x8 | 915 (787 + 128) | 1488 (1360 + 128) | +573 | 313 | 510 | +197 | 6 and 6 |
| 8x8, no DSP | 993 (865 + 128) | 1571 (1443 + 128) | +578 | 313 | 510 | +197 | 0 |

DERIVED breakdown: the open vector is one flip-flop per allocated record, 53
at 1x1 and 156 at 8x8 by the record table of the run, and its per-record
compare against the operation's region drives most of the LUT delta at 8x8;
the rest is the capture state, a 16-bit identity, the hold counter and the
two dirty halves (about 41 flip-flops). Against the XC7A100T's 63,400 LUT the
8x8 delta is 0.9 percent. Post-place figures are owed by a bitstream build.

MEASURED firmware, RV32I at -Os against the same target stubs: text 9790 to
11250 bytes at 1x1 (+1460) and 9906 to 11374 at 8x8 (+1468); bss +8 bytes;
data unchanged.

Memory shape: the stage is one container, 3264 bytes at 1x1 and 8648 at 8x8.

Timing assumptions (DERIVED, not measured on hardware): the hold must cover
the copy of the record area by the CPU, a few thousand byte moves at 1x1 and
under 9000 at 8x8, which is far below 50 ms at any plausible CPU clock; the
50 ms bound is well under the 500 ms heartbeat period and the 8000 ms commit
deadline, and the parameter refuses a hold at or above the commit deadline.

## 19. The executable model and its omissions

- ONE process per build: the real donor KL_acmp_nvm_shadow, KL_pp_nvm_port
  and KL_aecp_dyn_state at 8f2f58fb, the backend (tracked file or the
  prototype copy
  `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/proposal-evidence/prototype/KL_nvm_backend.proto.sv`),
  parent glue transcribed from KL_pp_shadow, and the ordinary firmware service
  compiled for the host (the tracked translation unit or the prototype copy),
  routed to the RTL through its two CSR primitives exactly as the
  repository's nvm_hosttest adapter does, all on one clock.
- Real producer versus BFM: every case names its producer (section 9 and
  results.json "producer"). The listener record-write port and the uCPU
  state-port write are BFMs in front of the real manager and dynamic-state
  store; the device-face BFM is used only for operations the manager does
  not produce on demand (an ERASE with no WRITE, an abandoned or partial
  stream). The gap, stale-mask and deferral orderings each have a real-port
  case (C1a, C1g, C1r, C2r, C2e).
- Transaction counts versus model time: the backend clock is 1 MHz of MODEL
  time (one cycle is 1 us); the hold, the deadlines and the heartbeat are
  counted in that time. Firmware execution between two CSR accesses takes
  zero model time; the harness advances time where the writer idles.
- Omitted physical timing, stated plainly: CPU instruction time, DDR and
  bus latency and arbitration, clock-domain crossings, the product's clock
  rate, and real flash timing (the flash is a host model with injectable
  failures and one 3 s erase in A9). No hardware was run.
- Totals: 1326 graded runs over 31 builds: 3 prototype builds (1x1, 8x8,
  and a 2-bit identity build for the wrap control), 2 tracked builds, 1 mixed
  build (the new writer on tracked gateware), 24 mutants and 1 executed
  alternative. The 1x1
  prototype passes 180 checks with 1 listed expected failure (E3 without
  D1); the 8x8 prototype passes 55 of 55; every mutant is killed by its named
  check. See
  `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/COMMAND_RESULTS.md`.

## 20. UNRESOLVED

1. Materialization. Nothing writes a record for configuration index,
   sampling rate, clock source, stream formats, presentation time offset,
   channel maps or names at the current source; only bindings have a writer.
   The pending bit reports the dynamic-state fields truthfully (1 until
   reset); making them durable needs scope D3.
2. Channel-map and name changes do not reach the parent at all (their commit
   marks end on unconnected wires), so the status can read durable over them.
   Reporting them needs D2; making them durable needs D3.
3. D1 is not landed: until it is, a binding inside the manager's debounce
   reads durable (E3 without D1 fails, as listed).
4. Whether the shipping memory bridge can withhold a write completion forever
   is not established. The contract relies on neither answer, but a silent
   write wedges the single-outstanding device face, so no later record
   operation of any record is granted until reset; a device-face timeout that
   ends such an operation with err is a possible follow-up, not proposed here.
5. The JEDEC identity-mismatch revocation cause of
   [section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven)
   has no reporter at the current source.
6. Physical timing: the 50 ms hold against the real copy time, and the
   debounce value
   ([section 14](SAVED_STATE_FASTCONNECT.md#14-what-this-page-does-not-decide)
   of the saved-state page, still open), are not measured on hardware.

## 21. Traceability

Issue body, acceptance for this design phase:

| Bullet | Where | Executed by |
|---|---|---|
| Exact handshakes and ownership: already-granted writes, deferred requests, concurrent captures | 4, 5, 7 | A11, A12, C1g, C1, C1r, C5 |
| ACK cannot clear newer work before, on or after its edge; no-change converges; dirty not held to pass | 5, 6 | A2, A3, A4, A1; convergence requires the durable reading (M18) |
| No transient erased record promoted; first-boot erased records kept; last verified slot kept on failure | 3, 4, 7, 8 | B1 to B5, C1g, C2, C2e, B7, B8, F2, R_power_cycle |
| Control plane responsive; producer pause quantified with a timeout | 3, 5, 18 | C1 and C1r (deferral ends at the attestation, 23 cycles after the arm), C2 and C2e (bounded at 50 ms, then the capture is void), A9, F3 |
| Reset and re-arm, abandoned and duplicate ACKs, counter wrap, CRC and sequence promotion, liveness and stale | 5, 6, 7 | U1, A5, A6, A8, C7, C8, D1, F2 |
| Bounded executable model on production interfaces, missing orderings, meaningful mutations, omitted timing stated | 9, 15, 19 | 1326 runs; 24 mutants each killed by a named check |
| ADR, source hashes, command results; review ledger before product edits | this page; `branch 419-design-evidence, commit 08f019ff3f3c51d365ce49f0cca53341c9a49c2a, path design-evidence/419-snapshot-ownership/COMMAND_RESULTS.md` | the review ledger belongs to the independent reviewers |

[Comment 5670792796](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5670792796),
obligations incorporated from issue #420:

| Obligation | Where | Executed by |
|---|---|---|
| Persistent-field materialization and producer ownership | 11, 13 (D3) | E1; UNRESOLVED 1 and 2 |
| Re-arm after ACK while a source level stays high | 6.1 | E1 (second change, level high); G01 and M14 killed |
| One logical record boundary across ERASE and WRITE; device idle and erased bytes are not one | 4 | B5, B6, B6b, B10, C1a, C1g; M01 and M02 killed |
| Capture, promotion and ACK are separate ownership steps; an earlier failed record never disappears | 5, 7, 8 | B6, B6b, C8, R_power_cycle, A1 |
| Four outcomes distinct; permanent silence only as an injected assumption; [section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven) discrepancy resolved | 10, 12 | D4c, D4d, D4e, B1 to B4, F2; UNRESOLVED 4 |

The eleven items of the round-3 author's brief map to sections as follows: 1
is sections 4, 5 and 7; 2 is sections 5 and 6; 3 is sections 3, 4 and 8; 4 is
sections 5 and 18; 5 is sections 6, 10 and 12; 6 is section 11; 7 is section
12; 8 is sections 13 and 14; 9 is sections 9 and 19; 10 is section 18; 11(a)
is section 6.1 (decided) and section 15, and 11(b) is section 16 (decided).
