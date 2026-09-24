<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Saved-state snapshot ownership and acknowledgement identity

> **Status: ACCEPTED, AND IMPLEMENTED.** This page was the design phase of
> issue #419; the implementation lane is issue #484, under issue #70, and it
> landed the contract in the product RTL and firmware:
> `hdl/milan/KL_nvm_backend.sv`, `hdl/milan/KL_pp_shadow.sv`,
> `hdl/common/csr/milan_csr.sv` and
> `sw/firmware/milan_baremetal/milan_baremetal.c`, with the
> [saved-state page](SAVED_STATE_FASTCONNECT.md) sections 9.1, 9.2 and 9.3
> carrying what it changed. The suite that grades it against the SHIPPING pair
> -- not against the prototype this page was designed on -- is
> `tb/verilator/nvm_cosim`.
>
> **Four corrections the acceptance reviews asked for** are applied to this
> page's tables and to that suite's checks, and are marked **(#484)** where
> they land: the terminal row's two halves are re-split, because `[23]` and
> `[22]` are decided by the ordering and not by the state (section 5.3); the
> reset row states `[2]` and the term that refuses an ARM there (section 5.4);
> case W4's check grades its own premise; and the accepted-load unit case U11
> runs at 8x8 as well (section 9).
>
> **The two donor interface dependencies LANDED at the pinned revision**
> (`protocol-processor-control-plane-avb-milan` issue 90): scope D1 exports
> the binding manager's unflushed sinks and scope D2 the AECP commit marks,
> both of section 13, and `KL_pp_shadow.sv` binds all three ports at the one
> place that was reserved for them. A binding accepted inside the manager's
> debounce now reads PENDING (case E3, an ordinary passing case since), and a
> channel map or user name change is reported instead of reading durable.
> What is still a KNOWN LIMITATION of the shipping build, and a scope rather
> than a defect of this contract, is MATERIALIZATION: no record writer exists
> for the non-binding groups, which is scope D3 and UNRESOLVED 1.
>
> Two product decisions are recorded, and the contract is built on both:
>
> - **Separate pending bit** (owner decision, 2026-09-18,
>   [issue comment 5730427393](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5730427393)):
>   accepted producer work not yet represented in a verified slot is reported
>   on its own pending bit, not folded into a composite durable bit (section
>   6.1; the composite bit is rejected in section 15).
> - **One summary bit** (manager decision, 2026-09-19,
>   [issue comment 5739523021](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5739523021);
>   kept by the owner the same day,
>   [issue comment 5740180418](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5740180418)):
>   the controller-visible status carries the pending bit as one bit, and the
>   per-record list of open records stays on the backend's own register face
>   and the console (section 16).
>
> **Revision b** answers the contract review of this page at `b6ae45a5` (one
> NEGATIVE, one POSITIVE; the public summary and the manager's direction are
> [issue comment 5743971020](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5743971020)).
> RELOAD is now checked by the backend and accepted once per reset (section
> 5.3); a mutating request on the arm's own edge is deferred (section 4); the
> reset row and the identity across a reset are defined (section 5.4);
> PP_NVM_STAT[22] is the pending bit itself (section 5.1). The evidence was
> re-run in full for it. Section 21 maps every review finding to its answer.
>
> **Revision c** answers the re-review at `53b2026e` (one NEGATIVE, one
> POSITIVE; the public summary and the manager's direction are
> [issue comment 5744994840](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5744994840)).
> The boot window load now closes when the window GOES LIVE as well as on an
> accepted RELOAD, so no sequence of boot outcomes and writer restarts lets an
> accepted RELOAD retire work no slot holds (section 5.3, rule 8); the
> four-refusal terminal row is stated in full and the writer that reaches it
> retires, so nvm_backed reads 0; the hold's bound holds across chained
> captures by refusing an ARM while a deferred request waits (section 5.2);
> the restart, reset and one-writer premises are stated as contract
> obligations O1 to O4 (section 7) with what cannot be guaranteed carried as
> UNRESOLVED 8 to 10; the derived copy time is re-derived at the shipping
> 50 MHz CPU clock (section 18). Four cases and five mutants are added and the
> evidence was re-run in full from a clean state. Section 21 maps every
> re-review finding to its answer.
>
> **Revision d** answers the re-review at `e2d98d88` (one POSITIVE, one
> NEGATIVE; the public summary and the manager's direction are
> [issue comment 5746130783](https://github.com/kebag-logic/milan-fpga/issues/419#issuecomment-5746130783)).
> It SHRINKS THE STATE SPACE rather than closing one more ordering: **no
> capture without an accepted load.** The backend keeps one registered flag,
> set by an accepted RELOAD and cleared only by reset, and the arm condition
> gains one term reading it, so a boot whose window load was never accepted
> opens no capture, writes no slot and retires nothing, and its status can
> never read durable (section 5.3, rule 9). A writer restarted in that state
> does not re-attach and stays retired, and the writer stops re-basing and
> refilling the window once it has gone live. The terminal row is restated as
> the bits the state fixes and the bits the ordering decides, with its reading
> after a restart. Five cases and three mutants are added, two earlier cases
> are re-graded, and the evidence was re-run in full from a clean state.
> Section 21 maps every re-review finding to its answer.

Source examined: dev `36ee8a37` (protocol-processor `8f2f58fb`, gptp-processor
`c1b61743`, third_party/verilog-axis `48ff7a7e`). Where this page says the
current source, it means that commit. The evidence ran there, and its run
script refuses any other checkout. A claim marked EXECUTED comes from the run
script at that source, graded in its results files; a claim marked DERIVED
does not. Case and check names are the ones the run script grades.

<!-- milan-feature-value:gateware_version:historic -->
This page lands on dev `f56fa168`. Its protocol-processor pin is `6a9a1241`,
not the examined `8f2f58fb`; the gptp-processor and verilog-axis pins are the
examined ones. Between `36ee8a37` and `f56fa168` (#398, #401, #466, #438, #452,
#473), nine of the root files the evidence examined changed. The tracked
writer, which the model compiles, only turned its five waits into generated
constants with the same values (250, 1000, 3500, 50 and 3000 ms;
`sw/firmware/milan_baremetal/milan_baremetal.c`, `scripts/nvm_shape.py`, one
line of `sw/firmware/nvm_hosttest/test_nvm_firmware.py`) and dropped the ADP
capabilities write. `sw/litex/milan_soc.py` now generates the CRF boot word and
the fabric boot constants, both shape configurations moved to schema 1.2.0,
and [`REQUIREMENTS.md`](../../REQUIREMENTS.md), `hdl/common/csr/milan_csr.sv` and
[`docs/reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) step VERSION to 0x0002_005A (the register map
also rewords two rows). Between the two donor pins, the only examined donor
file that differs is its docs/architecture/02_interfaces.md, by one line; the
four donor sources the model compiles and `protocol_processor_top.sv` are
identical, so the line numbers section 13 cites hold at `6a9a1241`. The
evidence was not re-run at `f56fa168`.

The executable evidence is kept out of this tree, on a branch that is never
merged. Every evidence citation on this page names the branch, the commit and a
path in it:

- the proposal as delivered, with a revision-b, a revision-c and a revision-d
  note at its top:
  `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/PROPOSAL.md`;
- the command record, with every command, exit code and digest:
  `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/COMMAND_RESULTS.md`;
- the run script:
  `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/proposal-evidence/run.py`;
- its graded results:
  `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/proposal-evidence/results.txt`
  and
  `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/proposal-evidence/results.json`.

On that branch the checkout root, two forge account names and two agent-system
names are replaced by placeholders. The command record lists 88 digests of the
evidence itself, 65 sources and 23 outputs (and, separately, 31 digests of
production files, which are repository files and not part of the evidence
tree). Of those 88, 15 source copies under `proposal-evidence/sources/` differ
from their digests because of the placeholders, and the 11 files under
`proposal-evidence/prior-session/` (round-3 history, including earlier
sessions' console logs) are left out; the other 62 match. The evidence as
first reviewed is commit `08f019ff3f3c51d365ce49f0cca53341c9a49c2a` on the
same branch, revision b `739b9099c5521a2cf79cc2b7ad1c593b2869e5cc` is its
child, revision c `47ec64d48d58fd69ce4f2490f4dc0989cbe3e8f8` the child of
that, and revision d the child of revision c.

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
- **[3. Decision](#3-decision)** -- Eight rules: open bit, capture, identity, pending bit, load.
- **[4. Record ownership: the open vector](#4-record-ownership-the-open-vector)** -- Grant opens, WRITE closes.
- **[5. The capture handshake and state machine](#5-the-capture-handshake-and-state-machine)** -- Strobes, status, the checked load, reset, identity.
- **[6. Next-state functions, and the separate pending bit](#6-next-state-functions-and-the-separate-pending-bit)** -- Priorities explicit.
- **[7. The writer sequence](#7-the-writer-sequence)** -- Boot, service, capture, seal, program, acknowledge.
- **[8. The round-2 concern, answered](#8-the-round-2-concern-answered)** -- Three concerns, executed refutations.
- **[9. Ordering coverage](#9-ordering-coverage)** -- Every ordering with its case and checks.
- **[10. The four outcomes of a record operation](#10-the-four-outcomes-of-a-record-operation)** -- Kept distinct.
- **[11. Persistent-field materialization](#11-persistent-field-materialization)** -- Which field groups have a record writer.
- **[12. The section 9.2 revocation discrepancy](#12-the-section-92-revocation-discrepancy)** -- RTL follows prose.
- **[13. Donor dependencies, each its own scope](#13-donor-dependencies-each-its-own-scope)** -- D1, D2, D3.
- **[14. Old writer on new gateware, and the reverse](#14-old-writer-on-new-gateware-and-the-reverse)** -- Refused.
- **[15. Alternatives rejected](#15-alternatives-rejected)** -- Thirteen alternatives, including the composite durable bit.
- **[16. Per-record reporting versus one summary bit](#16-per-record-reporting-versus-one-summary-bit)** -- Decided: one bit.
- **[17. Consequences](#17-consequences)** -- What the contract changes and costs.
- **[18. Cost](#18-cost)** -- Measured area and firmware size, derived timing.
- **[19. The executable model and its omissions](#19-the-executable-model-and-its-omissions)** -- Scope and totals.
- **[20. UNRESOLVED](#20-unresolved)** -- Seven items this contract does not settle.
- **[21. Traceability](#21-traceability)** -- Acceptance bullets, obligations and review findings mapped to sections.

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
   it, apart from the boot load of rule 8. ERASE completion, err without done,
   a partial WRITE, an abandoned stream, permanent silence and withheld
   readiness all leave it set. Device-idle and erased bytes are never a
   record boundary: the boot load closes records only when the backend has
   seen that nothing but the writer's own load wrote the window.
2. The writer captures the record area into a PRIVATE stage it alone writes,
   prefilled with the last verified slot, and copies only records whose open
   bit is clear. An open record keeps its last verified bytes.
3. The capture is bounded: from the ARM's own edge on, mutating requests are
   deferred (never refused) for at most T_HOLD_MS_P = 50 ms; reads are never
   deferred. One request is deferred by AT MOST ONE capture: an ARM is
   refused while a request this backend already deferred still waits, so
   chained captures cannot hand a waiting request from one hold to the next
   and the bound is per request, not per capture (revision c). The backend
   ATTESTS the copy in hardware, and the attestation is false if any
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
8. The window load is checked by the backend the way the capture is. A
   re-base arms a load flag only while no mutating operation is in flight,
   and any mutating grant clears it; RELOAD is accepted only with the flag
   set, and only while the boot load is still open. A refused RELOAD changes
   nothing but its refusal bit, and the writer re-bases and loads again
   inside that boot. The boot load closes on the accepted RELOAD **and** the
   first time the window GOES LIVE -- a device-face operation the load
   sequence did not bracket is granted on a configured image, which is the
   restore walk's first read or an enabled producer (revision c). So no
   sequence of boot outcomes and writer restarts lets an accepted RELOAD
   close records or clear a dirty half once the producer has been able to
   write the window since reset. A writer restart without a fabric reset
   therefore never reloads: it re-attaches if the backend accepted this
   boot's load (rule 9); it stays RETIRED if none was accepted; and if it
   finds the boot load still open with the restore walk already sequenced, it
   stays disabled (section 5.3).
9. **No capture without an accepted load** (revision d). The backend keeps
   one registered flag, set by an ACCEPTED RELOAD and cleared only by reset,
   and no capture is armed while it is 0. A boot whose window load was never
   accepted -- because every attempt was refused, or because the window went
   live first -- therefore opens no capture at all: the capture identity
   never advances, no acknowledgement can quote a capture, no slot is
   written, no flash erase is issued, the committable bit never falls and the
   status can never read durable. The saved state stays at the last verified
   slot, the pending bit reads 1, nvm_backed reads 0, and only a reset leaves
   the state. Rule 8 keeps a later RELOAD from retiring work; this rule keeps
   the boot that validated nothing from retiring any. A writer restarted in
   that state does not re-attach: it reads the flag and stays retired, and
   this rule is what makes a writer that ignores that harmless (section 5.3).

## 4. Record ownership: the open vector

One bit per ALLOCATED record id of
[section 4.2](SAVED_STATE_FASTCONNECT.md#42-the-allocation----decided-the-donors-f078-rule-unchanged)
at the shape; an unallocated
id is a constant 0. Read by the writer as words 8 to 15 of the backend face
(word 8 + k holds ids 32k to 32k + 31).

| Event on the device face or control face | Effect on open[r] | Priority |
|---|---|---|
| reset | every allocated record OPEN (unknown until the first accepted RELOAD) | 1 |
| image re-based: a write to word 0 or 1, or to a channel-map table | every record OPEN | 1 |
| GRANT of a WRITE or ERASE on r, image configured, span in bounds, effective length nonzero | open[r] set (applied one cycle after the grant) | 2 |
| RELOAD strobe, ACCEPTED (section 5.3: load flag set and load pending) | every record CLOSED; an accepted RELOAD cannot meet a mutating operation in flight | 3 |
| RELOAD strobe, REFUSED | no change | - |
| whole-record WRITE on r (offset 0, length equal to the record length) ends with done and no error | open[r] cleared; the same completion sets dirty_live | 4 |
| ERASE on r ends with done | no change: open[r] stays set | - |
| WRITE or ERASE on r ends with err and no done | no change | - |
| partial WRITE on r ends with done | no change | - |
| stream abandoned, accepted write silent, readiness withheld | no change (the operation never ends) | - |
| any READ | no change | - |

A grant on the same edge as a close or an accepted reload wins, because its
operation is still to come. The set lands one cycle after its grant, and the
vector is still exact from the first cycle after an ARM, because the hold
starts on the arm's own edge: a mutating request in the ARM's cycle is
deferred like any later one. The last grant an ARM can follow is therefore on
the edge before it, and that grant's set lands on the arm edge. No writer
ordering is relied on.

EXECUTED: U4_grant_request_on_arm_edge requests an ERASE of the CLOSED record
0x20 in the ARM's own cycle (the reviewers' ordering). arm_edge_request_deferred:0x20
reads "ERASE requested in the arm's cycle, granted 303 cycles after it,
attestation at 301"; ownership_exact_after_arm@arm:0x20, in the first cycle
after the arm edge, reads "dev_busy 0, record 0x20 open 0"; the capture is
attested over the intact record. Mutant M19_arm_edge_grant_not_deferred, the
reviewed behaviour, grants that request on the arm edge ("granted 1 cycles
after it"), so an ERASE runs inside a capture whose vector read the record
closed; it is killed by U4 : arm_edge_request_deferred:0x20 and also fails
the other two checks. A11 now lets its WRITE be granted before the arm
(write_in_flight_at_arm: "WRITE granted -6 relative to the arm"), and C1a's
WRITE, requested on the arm's own edge, is granted 23 cycles later, at the
attestation.

Deferring was chosen over voiding: a capture voided on its own arm edge is a
guaranteed wasted attempt, while a deferred request waits at most until the
attestation or the hold's bound.

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
| [6] | RELOAD | the writer's boot load is complete; the backend accepts or refuses it (section 5.3) |

New read words: word 5, the capture identity (CAP_ID_W_P bits, 16 by
default, and an implementation must REFUSE a width outside 2..16 at
elaboration: the identity rides the acknowledgement word's upper half, and
one bit cannot distinguish the capture being acknowledged from the one
before it); words 8 to 15, the open vector.

PP_NVM_STAT read layout (tracked bits unchanged in place):

| Bits | Field |
|---|---|
| [31:24] | contract tag, value 0xC3 (0 on older gateware) |
| [23] | unres: at least one record is open (diagnostic) |
| [22] | nvm_pend: the pending bit of section 6.1, pend OR any record open; the same wire as the backend's nvm_pend output |
| [21] | arm refused: the last ARM was not accepted. Its causes are a capture already open, an unconfigured or unvalidated image, a mutating request this backend already deferred still waiting, and, from revision d, no RELOAD accepted since reset ([2] = 0) |
| [20] | ack refused (the last ACK was not accepted) |
| [19] | attested |
| [18] | valid (no mutating grant since the arm) |
| [17] | hold |
| [16] | open |
| [15:12] | verdict (unchanged) |
| [11] | reload refused: the last RELOAD strobe was refused (reserved zero in the tracked layout) |
| [10] | commit_busy (unchanged) |
| [9] | nvm_stale (unchanged) |
| [8] | nvm_dirty = dirty_live OR dirty_cap, committable image work |
| [7] | img_valid, [6] nvm_backed, [5] img_cfg, [4] dev_busy (unchanged) |
| [3] | load pending: a boot window load may STILL BE ACCEPTED (reserved zero in the tracked layout). Read it as that, not as "no RELOAD has been accepted": it falls both on an accepted RELOAD and the first time the window goes live, and the two are told apart by [2] |
| [2] | load accepted: a RELOAD HAS been accepted since reset (revision d; reserved zero in the tracked layout). While it is 0 the backend arms no capture, so nothing in that boot can be captured, committed or retired |

The pair ([3], [2]) is the boot's whole load history, and only three of its
four values occur: (1, 0) the boot load is still open, (0, 1) a load was
accepted and the window is the backend's, (0, 0) the boot load is over and
none was accepted, which is the terminal state of section 5.3. (1, 1) cannot
occur, because accepting a RELOAD clears [3] in the same cycle it sets [2].

In revision b, bit [22] carries nvm_pend itself. At the reviewed head the
prototype drove it from the producer half alone, and its console printed
pend=0 beside unres=1 for an open record. Every run now grades
pending_bit_is_status_bit_22, which requires [22] to equal the nvm_pend
output at every observation of a build that carries the contract; it passes
on every run of the prototype at both shapes.

### 5.2 The capture state machine

One capture at a time. Its identity advances only on an accepted ARM, so it
names captures, not attempts.

| From | Event | Condition | To | Effect |
|---|---|---|---|---|
| any | reset | - | IDLE | the reset row of section 5.4 |
| IDLE | ARM | a RELOAD has been accepted since reset, image configured and validated, no accepted reload or re-base on the edge, and no mutating request this backend already deferred still waiting | HELD | identity + 1; dirty_cap = dirty_live; dirty_live = 0 unless a completion lands on the same edge; hold timer = T_HOLD_MS_P; valid = 1; attested = 0; a mutating request on this edge is deferred |
| open | ARM | - | unchanged | arm refused = 1; identity unchanged |
| IDLE | ARM | a mutating request this backend already deferred is still waiting | unchanged | arm refused = 1; identity unchanged; that request takes this cycle's grant |
| IDLE | ARM | no RELOAD accepted since reset ([2] = 0) | unchanged | arm refused = 1; identity unchanged; nothing else changes (revision d) |
| HELD | hold timer reaches its bound | - | UNHELD | hold = 0; deferred requests are granted |
| HELD or UNHELD | mutating grant | reachable only when hold = 0 | same | valid = 0 (the copy is void) |
| HELD or UNHELD | ATTEST | valid, and no mutating grant on the same edge | ATTESTED | hold = 0; attested = 1 |
| HELD or UNHELD | ATTEST | not valid, or a grant on the same edge | UNHELD | hold = 0; attested stays 0 |
| ATTESTED | ACK quoting this identity | valid | IDLE | dirty_cap = 0 (retired); commit bracket closed |
| open, not attested | ACK quoting this identity | - | IDLE | refused; dirty_cap handed back to dirty_live |
| any | ACK quoting another identity, or no capture open | - | unchanged | ack refused = 1; nothing else changes |
| open | RELEASE | - | IDLE | dirty_cap handed back to dirty_live; commit bracket closed |
| open | accepted RELOAD or re-base | - | IDLE | capture ended; an accepted RELOAD clears both halves (the window now equals a verified slot and nothing else wrote it: section 5.3); re-base hands dirty_cap back |
| any | refused RELOAD | - | unchanged | reload refused = 1; nothing else changes |

The identity across wrap and reset is section 5.4.

A lapsed commit deadline does NOT end a capture: a late but valid completion
is accepted as data and does not by itself resurrect nvm_backed (EXECUTED:
C7_late_ack_after_commit_deadline).

The grant rule on the device face: while hold = 1, and on the edge of an
accepted ARM, a WRITE or ERASE request is not granted and the port holds its
request, as KL_pp_nvm_port's interface
already requires (dev_req_o held until dev_gnt_i); a READ is granted. No
refusal and no err is ever issued for a deferral.

**The bound, per request** (revision c). A request is deferred by at most ONE
capture: the backend registers "a mutating request I am holding back", and
while that bit is set an ARM is refused, so the request takes the cycle the
hold drops instead of being handed to the next capture. Without it the bound
was per capture and rested on a property of the writer's timing the page did
not state: a capture ended while HELD with an ARM in the adjacent cycle leaves
no cycle in which the waiting request can be granted, and a chain of such
captures extends one request's wait without bound. EXECUTED:
U10_arm_refused_while_request_deferred releases 20 ms into a hold and arms
again on the very next edge. arm_refused_while_request_deferred@arm2 reads
"arm refused 1, capture open 0" and hold_bounded_across_captures:0x21 reads
"2 arms, the second 20002 cycles after the first; request granted 20002 cycles
after it was raised (bound 51000)".
M20_arm_accepted_while_request_deferred deletes the refusal and is killed by
that check: "request granted 69733 cycles after it was raised". The writer
loses nothing by the refusal: it reads arm refused, strobes RELEASE and arms
afresh at its next service call, which is the path it already takes for every
refused arm (nvm_capture reports no capture; the identity it carries beside
that answer is never the answer, because section 5.4's wrap gives one capture
in every 2**CAP_ID_W_P the identity 0).

### 5.3 The window load: RELOAD checked by the backend

RELOAD is the writer's claim that the window holds exactly the container it
has just loaded from a verified slot, or the blank image. An accepted RELOAD
closes every record and clears both dirty halves. That is true only if
nothing else wrote the window between the start of the load and the strobe.
At the reviewed head the backend took the claim on trust. A RELOAD after an
ERASE that ended in err without done therefore closed the erased record on
device idle, and the next commit published it under a durable reading (the
reviewers' ordering).

The rule, in the backend (revision b, with the two bounds revision c adds):

- **Load flag.** 0 at reset. Every re-base (a write to word 0 or 1, or to a
  channel-map table) sets it to 1 if no mutating operation is in flight on
  that edge, and to 0 if one is. Every mutating grant clears it, and a grant
  wins over a re-base on the same edge.
- **Load pending**, PP_NVM_STAT[3]. 1 at reset. It falls on an accepted
  RELOAD, and (revision c) the first time the WINDOW GOES LIVE: a device-face
  operation that the load sequence did not bracket is granted on a configured
  image. Read it as "a boot window load may still be accepted", not as "no
  RELOAD has been accepted". The two differ in exactly one state, the one the
  re-review found: a boot whose loads were all refused, after which the
  restore walk reads the window and the producer writes it.
- **RELOAD is accepted** only when the load flag and load pending are both 1.
  An accepted RELOAD closes every record, clears both dirty halves, ends any
  capture, closes the commit bracket and clears reload refused.
- **A refused RELOAD** changes nothing but reload refused, PP_NVM_STAT[11].
  Every record stays as the last re-base left it, which is open, so nvm_pend
  reads 1, no durable reading is possible and nothing is retired.
- **Load accepted**, PP_NVM_STAT[2] (revision d). 0 at reset. An accepted
  RELOAD sets it. NOTHING clears it but a reset. **No capture is armed while
  it is 0**: the arm condition of section 5.2 reads it directly. So a boot
  whose window load was never accepted opens no capture at all, and rule 9
  below is what that buys.

The window-live term is what makes the promise universal. **What "the load
sequence brackets a grant" means, exactly** (revision d states it, because
revision c's wording implied more): the bracket holds for the FIRST mutating
grant after a re-base, and for no other. That grant clears the load flag, so
any further grant before the next re-base meets a clear flag on a configured
image, which is the window going live. A load the writer REPEATS therefore
survives exactly ONE unbracketed grant per attempt; a second grant in the
same attempt closes the boot load for the whole reset, and every remaining
attempt is refused. An ordinary complete record update is two grants, ERASE
then WRITE, so **the terminal state below is reachable from a single
disturbed attempt**, not only from four. **The invariant it buys**: no
sequence of boot outcomes and writer restarts can let an accepted RELOAD close
records or clear a dirty half once the producer has been able to write the
configured window since reset, because from that grant on no RELOAD is ever
accepted. Where a load IS accepted, the restore walk follows it in the same
boot (section 7 step 1.6), so the entity's state is re-derived from what was
loaded.

**Rule 9, the accepted-load term** (revision d), is what makes the promise
hold without a per-record repair. The window-live term stops a later RELOAD
from retiring work; it does not stop the OTHER half of the ownership rule
from being wrong in such a boot. A record's close rule is "a whole-record
WRITE that ended with done", and it assumes nothing else wrote the record's
bytes while that WRITE streamed. A REFUSED load has still WRITTEN the whole
window: for attempts 1 to 3 the next re-base re-opens every record, so
nothing survives, but after the last attempt nothing re-opens them, and a
record closed across that last fill reads CLOSED over bytes the fill wrote.
The re-review promoted exactly that record with a restarted writer. Rule 9
removes the promotion instead of repairing the record: **in a boot in which
no RELOAD was accepted, no capture opens**, so the capture identity never
advances, no acknowledgement can quote a capture, no slot is written, no
flash erase is issued, the committable bit never falls, and the status can
never read durable. The record still reads closed; it is REPORTED, never
retired, and a producer rewrite or a reset resolves it, which is the same
convergence every record the refused loads left open already had.

Each term and the mutant that deletes it:

| Term | Why | Mutant | Named killer | Killer detail under the mutant |
|---|---|---|---|---|
| a mutating grant after the re-base refuses (the since-re-base guard) | the granted operation may write the window after the load | R02_reload_ignores_grant_since_rebase | R1 : last_verified_kept@end:0x20 | "record 0x20 at end: ERASED"; R1 also fails every_verified_slot_keeps, no_durable_reading_over_erased_live and converged |
| a mutating operation in flight at the re-base refuses | it keeps writing its record after the load and may end (err without done) before the strobe with no grant after the re-base; this is the reviewed RELOAD's in-flight exception turned into a refusal, so an accepted RELOAD never meets an operation in flight and no record needs excepting | R01_reload_ignores_inflight | U5 : reload_refused_inflight_at_rebase@after:0x20 | "reload refused 0, record 0x20 open 0", with the record's bytes torn |
| the boot load is open once per reset | after the boot load the window is the producer's live image; a later re-base, load and RELOAD would overwrite and clear work the backend still owns | R03_reload_not_once_per_reset | U6 : held_work_survives_post_boot_reload@reload | "committable work 0, pending 0, reload refused 0" |
| a GRANT WINS over a re-base on the same edge (revision c executes the priority) | nothing is in flight on that edge, so only the priority keeps the flag clear; without it an operation granted on the last re-base write's edge blanks the loaded record and the RELOAD closes it | R04_rebase_wins_over_same_edge_grant | U8 : grant_wins_over_rebase_edge@after:0x20 | "grant registered at 14, decided on the re-base write's own edge 13 (True), reload refused 0, record 0x20 open 0", and closed_record_equals_load fails with the record closed over erased bytes |
| the boot load also closes when the WINDOW GOES LIVE (revision c) | otherwise a boot whose loads were all refused leaves load pending 1 over a window the producer then writes, and a restarted writer's RELOAD is accepted over it | R05_boot_load_stays_pending_when_live | U9 : boot_load_closed_when_live@boot | "load pending 1, reload refused 1"; the terminal row fails with it |
| NO CAPTURE until a RELOAD has been ACCEPTED since reset (revision d, rule 9) | img_valid is the writer's claim about the window; without the backend's own record of having validated one, a boot that accepted no load can still capture, commit and retire on that claim alone, over records a refused load's fill closed | R07_arm_without_accepted_load | U11 : arm_refused_without_accepted_load@stray | "load accepted 0, img valid 1, arm refused 0, capture open 1, capture identity 1": the capture opens, and U11's second check then reads "capture identity 1, attested 0, committable work 0", so the acknowledgement retired work no slot holds |

**The cold-boot sequence** (section 7 step 1) is re-base, load, RELOAD, then
read [11]. On a refusal the writer waits, bounded, for the device face to go
idle and repeats from the re-base, at most four attempts in all: an operation
that is merely slow would otherwise be in flight at every re-base and refuse
every attempt for a reason the next attempt cannot improve. On acceptance it
publishes the sequence and the verdict with the validity bit, then starts the
restore walk. At a cold boot no producer is enabled before the restore walk
(the entity enable follows it), so the first attempt is accepted, as in every
writer case of the evidence. Before the first configuration after a reset the
backend presents no memory write at all, because a mutating grant needs a
configured image, and for the same reason the window cannot GO LIVE before the
writer's first re-base. The writer still re-bases before it loads, so the
order does not depend on that.

A refusal means something outside that sequence wrote the window. **After a
refusal the writer reads PP_NVM_STAT[3]** (revision d). If it still reads 1
the boot load is open, the repeat's re-base re-arms the flag and its load
rewrites the window, so the repeat is accepted and the entity restores the
verified bytes. If it reads 0 the window has GONE LIVE, no later RELOAD can
be accepted, and the writer STOPS: it does not spend the remaining attempts
re-basing and refilling a window the producer now owns. Revision c performed
those three further attempts, which bought nothing and wrote the window three
more times; revision d makes them one refusal and a stop. EXECUTED:
U12_window_live_stops_the_repeat gives the first attempt the ordinary
two-grant disturbance (an ERASE then a whole-record WRITE of 0x21) and grades
window_live_stops_the_repeat@boot, "window went live True, RELOAD strobes 1
(want 1), load pending 0, load accepted 0". F12_repeat_ignores_window_live
deletes the read and is killed by it: "window went live False, RELOAD strobes
4 (want 1)". The end state is the terminal row below, reached in one attempt.
EXECUTED:
R1_reload_after_failed_erase runs on the slots of an A1 run, where slot A
holds X in record 0x20. An ERASE of 0x20 blanks the whole span and ends in err
without done between the window load and the strobe, and a later change
commits. reload_refused_then_reloaded@boot reads "one refusal then acceptance
reported True, load pending 0", and every_verified_slot_keeps@end:0x20 reads
"verified slots ['A: expected X', 'B: expected X']". The later record persists,
no observation reads durable over an erased live record, and converged@end
passes: the durable reading returns only when the slots hold every record,
so no bit is held asserted to pass a check. The same case passes at 8x8.
F07_reload_refusal_ignored, a writer that takes a refused load as accepted,
leaves every record open, so the pending bit stays 1 and it never converges;
it is killed by R1 : converged@end.

One ordering inside the repeat is worth stating, because it is sound for a
reason outside the load rule. A whole-record WRITE that COMPLETES with done
between the load and the strobe closes its record and is then overwritten by
the repeat's load, and the accepted RELOAD retires its dirty half with no
flash erase. Nothing is lost, and the reason is not the load rule: it is that
**the restore walk follows the accepted load in the same boot**, so the entity
is re-derived from exactly the container that was loaded. That is an
obligation on scope D3 (section 13): no device-face initiator may be enabled
before the restore walk. It is true of a LONE such WRITE: the WRITE is the
one grant the bracket survives, so the attempt that follows it is accepted.
Two grants in one attempt end in the terminal state instead, and that is the
paragraph above, not this one.

**What this paragraph does NOT say** (revision d withdraws the claim
revision c made here). It does not say that a record closed across a REFUSED
load's fill is sound. It is not: the fill wrote the record's bytes while the
WRITE streamed, so the record reads closed over bytes the producer did not
write, and after the LAST attempt no re-base re-opens it. Revision c argued
that the load rule alone was safe without obligation O3. That was false for
this one class of records, and the re-review promoted one. Rule 9 is what is
safe without O3 now, and it is safe by removing the capture rather than by
repairing the record: the record still reads closed, nothing can retire it,
and section 7 obligation O3 is restated accordingly.

**When no attempt is accepted** the writer leaves the window unvalidated and
RETIRES for this reset: it never commits, and it stops answering the liveness
deadline, so nvm_backed is revoked and the state reads as a port with no
writer rather than as a commit in flight. The restore walk still runs and
reads blank, so the entity comes up on defaults although a verified slot
exists. This is the TERMINAL STATE, and it is reached by four refusals or by
one disturbed attempt whose window then went live.

The table has two halves, because **not every bit of the row is fixed by the
state**: some are decided by the ordering that reached it, and a lane that
built its test from a single row would fail a conforming implementation.
Fixed by the state:

| What a controller reads | Value | Meaning |
|---|---|---|
| PP_NVM_STAT[3] load pending | 0 | the boot load is OVER: the window went live, so no later RELOAD is accepted |
| PP_NVM_STAT[2] load accepted | 0 | none was ever accepted, so **nothing in this boot can be captured, committed or retired** (rule 9) |
| PP_NVM_STAT[11] reload refused | 1 | the last window load was refused |
| PP_STAT restore done / fail / blank | 1 / 1 / 1 | the walk ran, failed and read the window blank |
| PP_NVM_STAT[5] img_cfg | 1 | the image IS configured, which is why producer writes still land in a window whose reads come back blank |
| PP_NVM_STAT[7] img_valid | 0 | the window was never validated: THE SAVED STATE WAS NOT RESTORED IN THIS BOOT, although a verified slot exists |
| PP_NVM_STAT[19] attested, [18] valid, [17] hold, [16] open, [10] commit busy | 0 | no capture was ever opened, so there is nothing to hold and nothing to attest |
| flash erases | 0 | no slot is touched: the last verified slot is intact |
| the capture identity, PP_NVM_SEL word 5 | 0 | it advances only on an accepted ARM, and rule 9 accepts none |

Decided by the ordering, with its cause:

| Bit | Reading | When |
|---|---|---|
| PP_NVM_STAT[23] unres, [22] nvm_pend (#484) | 1, 1 at the boot | every record the fills left open is open: nothing is represented in a slot. **These are NOT fixed by the state**, which is the first correction: they FALL to 0, 0 once nothing is left open, which W4 reaches by rewriting every allocated record whole on the device face. What refuses the durable reading there is the committable bit, which stays 1 because nothing was ever committed, and nvm_backed, which is 0 because the writer retired |
| PP_NVM_STAT[11] reload refused (#484) | 1 after a refused RELOAD, 0 if none was strobed | decided by whether THE WRITER STROBED, not by the state. A writer that reaches the state through the window going live before it ever loaded strobes none |
| PP_NVM_STAT[21] arm refused, [20] ack refused (#484) | 0 in every ordering a conforming writer produces | same reason: a conforming writer retires in step 1.3 or 1.6 and never arms, so neither bit is ever set. A writer that ignores the rule and arms anyway reads [21] 1, and the state is unchanged, because rule 9 refuses that ARM |
| nvm_backed | 0 throughout | the writer retired before it ever heartbeated. A boot with no flash write heartbeats at the restore walk, and this writer retires before it |
| nvm_backed | 1, then 0 no later than T-NVM-WRITER-ALIVE after the boot | the refusing operation was SLOW, so the bounded wait of the repeat ran, and that wait heartbeats |
| nvm_stale | 0 | nvm_backed never set: losing a writer that was never live is not a loss |
| nvm_stale | 1, from the same deadline | nvm_backed had set: losing a writer that WAS live is a loss, by the saved-state page's section 9.2 |
| PP_NVM_STAT[8] committable (nvm_dirty) | 0 at the boot, 1 after a later change | the disturbance was on the device face alone |
| PP_NVM_STAT[8] committable | 1 already at the boot | the disturbance was a paced WRITE the writer was still waiting on |

Both readings are honest and **neither is ever durable**: the first because
nvm_backed is 0, the second because the committable bit is 1 and then
nvm_backed falls too. EXECUTED, both:

- U9_four_window_loads_refused, a failed ERASE of record 0x20 before each of
  four RELOAD strobes on the slots of an A1 run. four_refusal_terminal_row@boot
  grades the fixed bits and (0, 0, 0) for the three above: "mismatches none,
  status 0xc3c00820, the writer reported it True"; `0xc3c00920` after the
  change. The writer's line is "the backend refused 4 window loads; the window
  is not validated and the writer is disabled until the next reset."
- U13_four_refusals_with_the_device_busy, the same state reached with a paced
  whole-record WRITE still streaming at every strobe, which is exactly the
  case the bounded wait was added for. terminal_row_writer_was_live@boot reads
  "mismatches none, status 0xc3c00960" (backed 1, committable 1, stale 0) and
  terminal_row_after_the_loss@end, 3 s later, reads "mismatches none, status
  0xc3c00b20" (backed 0, stale 1). Both at 1x1 and at 8x8.

**Decision on nvm_backed**: it must end at 0. nvm_backed is evidence that a
writer is keeping the state, and a writer that will never commit again is, to
a controller, absent; leaving it at 1 would be true about a program that is
running and false about the only thing the bit is read for.
F10_retired_writer_keeps_heartbeating restores the heartbeat and is killed by
U9 : writer_absent_when_retired@end ("backed 1, pending 1, flash erases 0").
A writer disabled for a shape or tag mismatch (section 14) predates this
contract; UNRESOLVED 8 carries that, and it is the TAG mismatch alone, since
on a shape mismatch the writer returns before it installs its service hook
and nothing heartbeats.

**The row after a writer restart is the same row** (revision d). Under
revision c a restarted writer re-attached here and published img_valid 1 and
nvm_backed 1, so the two bits that named the state stopped naming it. Under
rule 9 and the writer rule below it does not re-attach: img_valid stays 0,
nvm_backed stays 0, the capture identity stays 0 and no bit of either table
moves. That is the whole difference a controller sees, and it is why the
state now reads one of exactly two rows rather than four.

**A writer restart without a fabric reset** is a CPU-only reset: the fabric
keeps its ownership state, and what the writer does depends on the two bits
the backend publishes, never on an assumption about the previous boot.

- **Load pending 0 with load accepted 1** (the ordinary case: the boot load
  was accepted and the backend has kept ownership since): the writer
  RE-ATTACHES. It does not re-base, load or RELOAD, and the backend would
  refuse a RELOAD anyway. It strobes RELEASE, which ends any capture the
  previous run left open and hands that capture's work back to dirty_live; it
  re-derives the authoritative slot and the sequence from the media,
  publishes them and resumes service. It does not re-run a restore walk the
  fabric has already sequenced.
- **Load pending 0 with load accepted 0** (revision d; the terminal state
  above): the writer does NOT re-attach. No window load was accepted in this
  boot, so nothing in it may be captured or committed, and a re-attach could
  only publish a validity bit over a window no accepted load vouches for. It
  stays RETIRED until the next reset: it never commits and stops answering
  the liveness deadline, exactly as the writer that reached the state did.
  This is the WRITER RULE; **rule 9 is what makes a writer that ignores it
  harmless**, because the backend refuses every ARM in that boot whatever the
  writer claims. The two are not redundant: the rule keeps a conforming
  writer from publishing a false validity bit, and the term keeps any writer
  from capturing.
- **Load pending 1 with the restore walk already sequenced**: not a cold boot
  either. The producer has been able to write the window since the fabric's
  reset and nothing would re-derive the entity's state from a load, so the
  writer stays disabled until the next reset rather than reload over it. This
  is the writer rule that goes with the backend's window-live term; under the
  term it is unreachable in this model, and it is stated so that an
  implementation that weakens one of the two still holds the invariant.
- **Load pending 1 with no walk sequenced**: the cold boot above.

EXECUTED: W1_writer_restart_reattaches models the restart on the host by
returning every file-scope variable of the writer to its initial value and
running its boot again. At the restart, X2 is in the window and not yet
committed. restart_reattaches@restarted reads "re-attach reported True, reload
refused 0, committable work kept 1"; there is no durable claim at the restart,
and converged@end holds with X2 in the slot. F08_restart_reloads_window, a
restart that takes the cold-boot path, is refused at every attempt, never
claims durability and never converges; it is killed by W1 : converged@end.

EXECUTED, the composition the first re-review found:
W2_restart_after_refused_loads is the four-refusal boot above, a controller
change Z2 accepted on the live entity, and then the restart. **Its expected
outcome CHANGES in revision d**, and the change is the point of the revision,
so it is stated rather than quietly re-graded. Under revision c the
re-attached writer committed what the window held, and Z2 ended in a verified
slot. Under revision d it does not re-attach: restart_stays_retired_without_load@restarted
reads "stayed retired True, re-attached False, load accepted 0, capture
identity 0, capture open 0, status claims durable False", and the run ends
with Z2 still REPORTED beside the intact slot A, not committed into a slot:
change_landed_or_reported@end:0x21 "record 0x21 in the newest verified slot
False, still reported True, status claims durable False", and
last_verified_kept@end:0x20 "record 0x20 at end: expected X". Availability is
what is traded: an accepted change now waits for a reset instead of landing
after a restart. It is the right trade here, because the boot that reaches
this state never validated the window, so "what the window holds" is exactly
what no accepted load vouches for.

F11_restart_reattaches_without_load restores revision c's re-attach and is
killed by W2 : restart_stays_retired_without_load@restarted ("stayed retired
False, re-attached True, load accepted 0"), and W2 also fails
writer_absent_when_retired@end under it ("backed 1"). R06_revision_b_load_rule
restores revision b's rule in BOTH places it lives (the backend's window-live
term and the writer's rule) and still reproduces the first re-review's finding
whole; its named killer is re-aimed in revision d at the check that names the
invariant rather than at the one that named where the change landed, because
where it lands is what changed: killed by W2 : change_landed_or_reported@end:0x21,
reading "record 0x21 in the newest verified slot False, still reported False,
status claims durable True".

EXECUTED, the composition the second re-review found (its probes H1 and H2):

- W3_write_across_refused_fill_then_restart places a whole-record WRITE of
  0x21 carrying Z2 across the LAST refused load's fill, so the record ends
  CLOSED over bytes the fill wrote. The premise is graded, not assumed:
  write_spans_refused_fill@live:0x21 reads "WRITE granted 448, last RELOAD
  strobe 461, ended 8582 (done), record 0x21 open 0". Then the writer
  restarts. It stays retired, the last verified slot is intact, the work is
  still reported and nothing reads durable.
- W4_all_records_rewritten_after_refused_fill is W3 and then every OTHER
  allocated record rewritten whole on the device face, which is what removed
  the last thing still reporting under revision c. **Its check grades its own
  premise** (#484): the reading it is about is the one in which NOTHING IS
  OPEN, so "records open 0 and pending 0" is REQUIRED, not merely printed --
  a run that left a record open would reach the same verdict for a reason the
  check is not about and would pass vacuously. It no longer helps:
  no_durable_reading_when_nothing_open@end2 reads "records open 0, pending 0,
  backed 0, committable 1, status claims durable False, flash erases 0". Note
  which bits carry it. The pending bit DOES fall to 0 once no record is open,
  because the disturbance was on the device face and no producer work is
  outstanding; what refuses the durable reading is the committable bit, which
  stays 1 because nothing was ever committed, and nvm_backed, which is 0
  because the writer retired. Under revision c the re-attached writer
  committed, the committable bit fell and nvm_backed stayed 1, and the same
  reading came out durable.

The reviewers' other RELOAD orderings are now refused (U6_reload_refused_after_boot):
the ERASE-to-WRITE gap, then a RELOAD with no re-base, reads "reload refused 1,
record 0x21 open 1"; a RELOAD with a whole-record WRITE in flight reads the
same; a re-base, a load and a RELOAD after the boot, over held work, read
"committable work 1, pending 1, reload refused 1".

### 5.4 Reset, and the identity across a reset

The reset row, EXECUTED by U7_reset_row_and_pre_reset_ack : reset_row@reset,
graded bit by bit ("mismatches none; every allocated record open True (53 of
53)", and 156 of 156 at 8x8):

| State | After reset |
|---|---|
| capture | closed: open 0, hold 0, valid 0, attested 0; arm refused 0, ack refused 0 |
| identity | 0; the first accepted ARM names capture 1 |
| dirty_live, dirty_cap | 0 and 0, so nvm_dirty is 0 |
| open vector | every allocated record open, so nvm_pend (PP_NVM_STAT[22]) reads 1 until the first accepted RELOAD |
| load | load flag 0, load pending PP_NVM_STAT[3] 1, **load accepted PP_NVM_STAT[2] 0** (#484), reload refused 0; a RELOAD before a re-base is refused (the flag is not readable, so U7 does not grade that clause bit by bit; the same term is executed by U5 and by U8) |
| image | length 0 (not configured) and img_valid 0 |
| an ARM here (#484) | REFUSED, and it stays refused after a writer configures and validates the image: load accepted is 0, and the arm condition reads it directly (rule 9). An implementation that refused only on the unconfigured image would pass a reset-row test and still open a capture in a boot that accepted no load |
| status | nvm_backed 0 and nvm_stale 0, because no writer has been live |

Identity wrap within one reset: the identity advances once per accepted ARM,
at most once per commit attempt, so a 16-bit identity repeats only after
65,536 captures, and an ACK aliases only if a stale one from exactly that many
captures earlier arrives while the current capture is attested. EXECUTED
control: A8 passes with 16 bits and FAILS on the 2-bit build (proto-w2-1x1),
as the run script requires.

The identity is a plain counter and its VALUE carries nothing else -- in
particular not "no capture", because the wrap gives one capture in every
2**CAP_ID_W_P the identity 0. A writer that spelled a refusal in that value
domain would read that capture, attested and holding real work, as a refusal:
it would defer the commit, print a refusal that did not happen, count it, and
issue none of the RELEASE step 3.5 defines for the opposite case. So the
writer reports the capture in a word BESIDE the identity, never in it
(#484 round 2, found by both reviewers of the implementation). EXECUTED:
`make -C tb/verilator/nvm_cosim wrap` runs five committing cases at 2
identity bits, the contract's minimum, where the identity is 0 on the fourth
accepted arm rather than the 65,536th, and requires each to report what it
reports at 16 -- the same acknowledgements, the same deferrals and the same
`captures refused` -- with at least one acknowledgement quoting the identity
0. Five pairs, five acknowledgements quoting 0. Cases that commit fewer than
four times carry a commit tail (`--commits`) applied identically at both
widths, so the identity width stays the only thing that moves between the two
runs of a pair. **No narrower build is run**, and none can be: 2 is the
minimum `CAP_ID_W_P` section 5.1 requires an implementation to admit, and the
suite passes `-Werror-USERERROR` on every Verilator invocation, so a build
outside 2..16 is refused at elaboration instead of being graded (#484 round
3, found by review of round 2's test arm).

Across a reset the alias distance is zero, not 65,536: the identity restarts
at 0, so the first capture after every reset is 1, like the first one before
it. A late ACK from before a reset can alias only if it is written after the
first post-reset ARM. Two facts exclude that ordering, and neither is the
identity's width. **Both are CONTRACT OBLIGATIONS, not observations about
today's product**: an implementation and every later lane must keep them, or
re-open the alias and answer it another way (section 17, obligations O1 and
O2). Fact 1 as written is true of the product examined here; fact 2 is a
property of the writer sequence this contract defines, and section 7 states
it as a rule.

1. In the product the backend's reset is the datapath's
   (`i_axis_resetn = ~ResetSignal(milan_cd)` in `sw/litex/milan_soc.py`). The
   Milan clock domain and the CPU's system domain come from one PLL whose
   reset is the board reset, so no writer instance from before a fabric reset
   runs after it. A CPU-only reset does not reset the backend, whose identity
   keeps counting (W1).
2. By construction in the backend, no ARM is accepted after a reset until a
   writer has configured and validated the image (the reset row). The one
   writer is sequential: a writer that survived a fabric-only reset writes
   its pending ACK before it can observe the reset and run its boot. That ACK
   meets no open capture and is refused, whether it arrives before the
   post-reset boot load (U7 : pre_reset_ack_refused@early_ack, "ack refused 1,
   capture open 0, id 0") or after it and before the first post-reset ARM
   (U7 and U1 : post_reset_ack_retires_nothing@after, "committable work 1";
   the tracked module fails both with "committable work 0").

The remaining ordering, a pre-reset ACK written after a post-reset capture is
attested, needs a second writer instance running beside the first. A review
probe builds it and the backend accepts it. The contract has ONE SEQUENTIAL
WRITER by obligation O1 (section 7, section 17); the ordering is excluded by
that, not by the hardware. This is carried as an open item, not closed: the
alias is excluded by an obligation an implementation must keep, and UNRESOLVED
9 records what must be shown or changed if a lane ever breaks either
obligation.

## 6. Next-state functions, and the separate pending bit

Stated like
[section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven),
priorities written out:

```
close        = done AND no error AND the operation was a whole-record WRITE
reload_ok    = RELOAD AND load_flag AND load_pending
arm_ok       = ARM AND image configured AND img_valid AND NOT open AND NOT (reload_ok OR re-base)
                   AND NOT deferred_wait AND load_accepted
grant        = request AND device idle AND NOT ((hold OR arm_ok) AND the request is a WRITE or ERASE)
mut_wait     = a WRITE or ERASE request AND device idle AND NOT grant
deferred_wait' = mut_wait                            (one cycle: the request this capture holds back)
window_live  = grant AND image configured AND NOT load_flag
void_grant   = mutating grant AND open AND NOT attested
attest_ok    = ATTEST AND open AND NOT attested AND valid AND NOT void_grant AND NOT (reload_ok OR re-base)
ack_ok       = ACK AND open AND attested AND valid AND id = cap_id AND NOT (reload_ok OR re-base)
end_cap      = open AND ((ACK AND id = cap_id) OR RELEASE OR reload_ok OR re-base)
drop         = end_cap AND NOT ack_ok

load_flag'   = mutating grant ? 0 : re-base ? NOT (a mutating operation in flight) : load_flag
load_pending' = (reload_ok OR window_live) ? 0 : load_pending
load_accepted' = reload_ok ? 1 : load_accepted       (revision d; only reset clears it)
reload_ref'  = RELOAD ? NOT reload_ok : reload_ref
open[r]'     = re-base OR (grant set on r) OR (NOT reload_ok AND open[r] AND NOT close on r)

dirty_live'  = close ? 1 : reload_ok ? 0 : arm_ok ? 0 : drop ? (dirty_live OR dirty_cap) : dirty_live
dirty_cap'   = reload_ok ? 0 : arm_ok ? dirty_live : (ack_ok OR drop) ? 0 : dirty_cap
nvm_dirty    = dirty_live OR dirty_cap

pend'        = pend_i
nvm_pend     = pend OR (any record open)             (also PP_NVM_STAT[22])

loss_event   = ALIVE expired OR COMMIT expired OR reported ERASE/PROGRAM/VERIFY failure OR alarm
loss         = loss_event AND a writer had been live since reset
backed'      = loss_event ? 0 : heartbeat ? 1 : backed
stale'       = loss ? 1 : (backed' AND NOT nvm_dirty') ? 0 : stale
```

Same-edge rules, each EXECUTED: a completion on the ACK edge stays in
dirty_live because the ACK reaches only dirty_cap (A3_write_done_on_ack_edge);
a completion on the ARM edge stays live, costing one extra commit
(U2_close_on_arm_edge); a mutating request on the ARM edge is deferred
(U4_grant_request_on_arm_edge); a grant on the ATTEST edge voids the
attestation (U3_grant_on_attest_edge); a grant on a re-base edge leaves the
load flag clear (U8_grant_on_rebase_edge, with R04 as its mutant: revision b
listed this one as executed and no case executed it). The (backed 1, dirty 0,
stale 1) row stays unreachable in the state (unreachable_row_never_held,
graded on every run).

### 6.1 The pending bit (owner decision)

nvm_pend is published at PP_NVM_STAT[22] on the backend face and, for the
reader of
[section 9.3](SAVED_STATE_FASTCONNECT.md#93-reading-the-three-bits-together),
at PP_STAT[11] (free today: [8] dirty, [9] stale, [10]
img_valid and [15:12] verdict are taken). Proposed status dictionary row for
[section 9.1](SAVED_STATE_FASTCONNECT.md#91-the-bits):

| bit | name | meaning |
|---|---|---|
| [11] | nvm_pend | accepted work that no verified slot holds and nvm_dirty does not report: a change the producer still holds, a record whose logical write has not completed, or -- from reset until the boot window load is accepted -- every record, because none is known yet |

SETS, one cycle after its cause, whenever:

- pend_i is 1. pend_i is a LEVEL wired in KL_pp_shadow: the dynamic-state
  store's sticky persisted-field level (aecp_dyn_dirty_o, today reduced to its
  rising edge), OR, once donor scope D1 lands, any sink the binding manager
  has accepted and not yet flushed; or
- any record is open (section 4). Between reset and the first accepted window
  load that is EVERY allocated record, so a reader of PP_STAT[11] sees 1
  through the whole boot interval, and a build with no writer at all reads 1
  for ever where saved-state section 9.3 documents (0,0,0). That is the truth
  told conservatively -- nothing is known durable yet -- and it is why the
  three bits are read together.

CLEARS only when pend_i is 0 AND no record is open. pend_i falls when the
manager has flushed every sink (its dirty bit clears on done, or is dropped on
retry exhaustion, which raises the alarm and revokes nvm_backed) and the
dynamic-state level is 0, which today happens only at reset because nothing
writes those fields (section 11). An open record closes at its whole-record
WRITE completion, or at the accepted boot RELOAD (section 5.3), which the
backend accepts only when no mutating operation was granted since the last
re-base and none was in flight at it. It never closes on device idle.

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
`branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/proposal-evidence/prototype/milan_baremetal.proto.c`
implements it:

1. Boot, in this order (nvm_boot):
   1. Validate both slots from the media and choose the newer accepted one,
      or the blank image when neither is accepted.
   2. Read PP_NVM_STAT. If [31:24] is not 0xC3, load the window, configure
      the backend and publish the verdict for the restore walk, then disable
      the writer (the runtime cross-check of section 14).
   3. If [3], load pending, is 0, the boot load is over, and [2], load
      accepted, says what that means (revision d).
      - **[2] = 1**: a writer restart on a live backend the fabric owns by a
        load it accepted. Re-attach as section 5.3 says (RELEASE, publish,
        ready) and skip to step 1.6.
      - **[2] = 0**: no window load was ever accepted in this boot, so
        nothing in it may be captured or committed (rule 9). Do NOT
        re-attach and do not publish a validity bit. Retire the writer for
        this reset, as step 1.6 does, and report it.
   4. Otherwise, if the fabric has ALREADY sequenced a restore walk since its
      reset, the window is live and unvalidated: do not load it. Retire the
      writer for this reset (no heartbeat) and report it. Step 1.6 is skipped
      because the writer is retired, and the walk in step 1.7 is skipped
      because the fabric has already sequenced it. This is the writer rule
      that goes with the backend's window-live term; under that term the
      backend has already closed the boot load, so this branch is unreachable
      in the model and is stated for an implementation that weakens one of
      the two.
   5. Otherwise re-base the backend (image base, length and channel-map
      tables), copy the chosen slot or the blank image into the live window,
      fence, strobe RELOAD and read [11]. If it is refused, read [3]
      (revision d): if it is 0 the window has gone live, no later RELOAD can
      be accepted, and the writer stops repeating. Otherwise wait (bounded)
      for the device face to go idle and repeat this step from the re-base,
      at most four attempts in all (section 5.3).
   6. Once a RELOAD is accepted, publish the sequence and the verdict with
      the validity bit, and the writer is ready. If none is accepted, leave
      the window unvalidated and RETIRE the writer: it never commits and
      stops answering the liveness deadline, so nvm_backed is revoked
      (section 5.3, the terminal row).
   7. Run the donor restore walk unless the fabric has already sequenced it
      since its reset; the entity is enabled only after this.
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
   2. ARM, then read the status. Not open, or arm refused ([21]): RELEASE and
      retry at the next service call. **The writer's behaviour on a refusal
      is unchanged by revision d, and needs no new bit.** A refused ARM is
      reported on [21] whatever refused it, and the writer treats every cause
      the same way: it gives the capture up and tries again later, never
      repeating the arm in the same service call. A conforming writer never
      meets the rule-9 cause at all, because it has retired in step 1.3 or
      1.6 before it ever reaches a capture; a writer that reaches one anyway
      is refused, and [2] tells it and a controller which cause it was.
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

The writer never strobes RELOAD outside step 1.5, and the backend accepts one
RELOAD per reset at most (section 5.3). A later contract that wanted a
run-time reload would have to change that rule, not merely call it.

**The obligations this sequence puts on an implementation**, stated as rules
the contract requires and not as observations about today's product. Each is
an acceptance item of the implementation lane; UNRESOLVED 9 and 10 carry what
cannot be guaranteed from this page.

- **O1. One sequential writer.** Exactly one control-face master runs this
  sequence, and it issues its control writes in order: no second instance, no
  debug bridge and no second initiator writes the strobe word, the image base
  or length, or the channel-map tables. The reset-crossing ACK argument of
  section 5.4 rests on this, and so does the reading of the open vector, which
  is exact only between a capture's arm and its attestation.
- **O2. One reset domain for the CPU and the fabric.** Every reset of the
  backend also resets the CPU that runs the writer. The product examined here
  satisfies it (one PLL, the board reset), and a later lane that adds a
  datapath soft reset, or a reset controller that can reset the fabric alone,
  breaks the argument in section 5.4 and must re-answer the alias.
- **O3. No device-face initiator before the restore walk.** The entity enable
  and every other device-face initiator (donor scope D3) come up only after
  step 1.7. What is safe without this, and what is not, is stated exactly
  (revision d corrects revision c, which claimed more). SAFE without it: no
  accepted RELOAD can retire work no slot holds, because a live window
  refuses the load; and nothing in a boot that accepted no load can be
  captured, committed or retired, because rule 9 arms no capture there. NOT
  safe without it: the RESTORE, which is what makes an accepted load
  re-derive the entity's state; and the per-record ownership reading, since a
  record closed across a refused load's fill reads closed over bytes the
  producer did not write. That record is reported and never retired, and only
  a producer rewrite or a reset resolves it.
- **O4. The live window and the fabric's view of it survive a writer
  restart.** The re-attach branch of step 1.3 assumes that the memory holding
  the window still holds what the backend believes it holds. A CPU-only
  restart whose path re-initialises that memory breaks the assumption without
  contradicting any other rule here; UNRESOLVED 10 states the two honest ways
  out and neither is decided on this page. Revision d narrows what rests on
  it: the branch is now taken only when [2] says the backend itself accepted
  the load, so the obligation covers a window the backend vouches for rather
  than any window a previous run left behind.

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

The construction above protects the capture, where the writer reads the
window. The load, where the writer writes the window and strobes RELOAD, had
no such protection at the reviewed head; revision b gives it the same shape in
the backend (section 5.3).

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
| WRITE granted before the arm and still in flight at it | A11 | real + BFM | write_in_flight_at_arm:0x21, inflight_record_excluded@first:0x21 | n/a |
| Last byte accepted before the arm, done after it | A12 | real + BFM | converged@end | n/a |
| ARM on the WRITE's request edge, ERASE done; the WRITE is deferred to the attestation | C1a | real | arm_inside_erase_write_gap:0x21, never_torn_or_erased@after:0x21 | n/a |
| Mutating request on the ARM's own edge, CLOSED record | U4 | unit | arm_edge_request_deferred:0x20, ownership_exact_after_arm@arm:0x20, attested_over_intact_record@attest:0x20 | n/a |
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
| Change inside the manager's debounce | E3 | real | no_durable_claim@in_debounce | FAILS; passes in the tree since donor scope D1 landed |
| Flash absent | F3 | real | producer_wait_bounded_by_hold, work_still_owned@end | passes |
| ACK from before a reset | U1 | unit | post_reset_ack_retires_nothing@after | FAILS |
| Completion on the ARM edge | U2 | unit | close_on_arm_edge_stays_live@acked | FAILS |
| Grant on the ATTEST edge | U3 | unit | grant_on_attest_edge_voids@cert | n/a |
| Reset row; a pre-reset ACK before and after the post-reset boot load | U7 | unit | reset_row@reset, pre_reset_ack_refused@early_ack, post_reset_ack_retires_nothing@after | FAILS (the ACK) |
| ERASE ending in err without done between the window load and RELOAD, then a later commit (the reviewers' ordering) | R1 | real + BFM, slots of an A1 run | reload_refused_then_reloaded@boot, last_verified_kept@end:0x20, every_verified_slot_keeps@end:0x20, no_durable_reading_over_erased_live, converged@end | n/a |
| Mutating operation in flight at a re-base, ending in err before RELOAD | U5 | unit | reload_refused_inflight_at_rebase@after:0x20, closed_record_equals_load@after:0x20 | n/a |
| RELOAD after the boot: in the ERASE-to-WRITE gap, with a WRITE in flight, over held work after a re-base | U6 | unit | gap_record_stays_open@gap:0x21, inflight_record_stays_open@inflight:0x21, held_work_survives_post_boot_reload@reload | n/a |
| Writer restart without a fabric reset | W1 | real, host restart model | restart_reattaches@restarted, no_durable_claim@restarted, converged@end | n/a |
| Mutating grant on the LAST re-base write's own edge, then RELOAD | U8 | unit | grant_wins_over_rebase_edge@after:0x20, closed_record_equals_load@after:0x20 | n/a |
| A capture ended while HELD, an ARM in the adjacent cycle, a request waiting | U10 | unit | hold_bounded_across_captures:0x21, arm_refused_while_request_deferred@arm2 | n/a |
| All four window loads refused: the terminal row, and a change after it | U9 | real + BFM, slots of an A1 run | four_refusal_terminal_row@boot, boot_load_closed_when_live@boot, writer_absent_when_retired@end, last_verified_kept@end:0x20, every_verified_slot_keeps@end:0x20, change_landed_or_reported@end:0x21 | n/a |
| A writer restart from the four-refusal state, with a change accepted after it | W2 | real + BFM, restart model, slots of an A1 run | restart_never_reloads_live_window@restarted, restart_stays_retired_without_load@restarted, writer_absent_when_retired@end, last_verified_kept@end:0x20, every_verified_slot_keeps@end:0x20, change_landed_or_reported@end:0x21 | n/a |
| An ARM on a window the control face validated exactly as a writer does, in a boot that accepted no load | U11 | unit | arm_refused_without_accepted_load@stray, no_capture_without_accepted_load@end | n/a |
| One disturbed attempt of two grants (ERASE then WRITE): the window goes live and the writer stops repeating | U12 | real + BFM, slots of an A1 run | window_live_stops_the_repeat@boot, writer_absent_when_retired@end, last_verified_kept@end:0x20, every_verified_slot_keeps@end:0x20, change_landed_or_reported@end:0x21 | n/a |
| The terminal state reached with the device BUSY at every strobe, so the bounded wait heartbeats: the row's second reading | U13 | real + BFM, slots of an A1 run | terminal_row_writer_was_live@boot, terminal_row_after_the_loss@end, last_verified_kept@end:0x20, every_verified_slot_keeps@end:0x20, change_landed_or_reported@end:0x21 | n/a |
| A whole-record WRITE across the LAST refused load's fill, then a writer restart (the re-review's probe H1) | W3 | real + BFM, restart model, slots of an A1 run | write_spans_refused_fill@live:0x21, restart_stays_retired_without_load@restarted, writer_absent_when_retired@end, last_verified_kept@end:0x20, every_verified_slot_keeps@end:0x20, change_landed_or_reported@end:0x21 | n/a |
| W3, and then every other allocated record rewritten whole, so nothing is left open by accident (probe H2) | W4 | real + BFM, restart model, slots of an A1 run | write_spans_refused_fill@live:0x21, restart_stays_retired_without_load@restarted, no_durable_reading_when_nothing_open@rewritten and @end2, last_verified_kept@end2:0x20, every_verified_slot_keeps@end2:0x20 | n/a |

Every run grades unreachable_row_never_held, and every run of a build that
carries the contract also grades pending_bit_is_status_bit_22 (a tracked or
firmware-mutant build where a hook never fires grades neither). No check of
any case may grade n/a on a prototype build. The 8x8 prototype passes the
core set, which includes A1, R1 and U4 to U7, together with U9, U12, U13,
W2, W3 and W4, which follow A1 on every build that runs it, **and U11, which
issue #484 adds there because the accepted-load term is shape-independent and
an acceptance review asked for it to be shown so**: 27 case runs, 150 checks,
all passing. U8 and U10 are unit cases and run at 1x1.

**In the tree, at the shipping source**, all of this is `tb/verilator/nvm_cosim`
(issue #484), which runs the same cases against `hdl/milan/KL_nvm_backend.sv`
and `sw/firmware/milan_baremetal/milan_baremetal.c` rather than against the
prototype: 465 checks over 89 case runs at the two shapes, with NO labelled
expected failure left, every mutant below killed by its named check, and the
three defects of section 2 reproduced RED against a pre-contract backend and
writer. It was 469 over 90 while donor scope D1 was modelled rather than
exported: E3 ran twice, at `d1=0` and `d1=1`, and the `d1=0` run was the one
labelled failure. With the export bound (issue 90) the modelled variant has
no subject, so E3 runs once and passes, and the four checks of the retired
variant are the whole difference in both counts.

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
| 0x20 to 0x2F | binding, parameters and started state | KL_acmp_nvm_shadow | the manager's per-sink dirty on nvm_unflushed_o (donor scope D1, landed), then the record's own grant and completion in the backend | KL_acmp_nvm_shadow through KL_pp_nvm_port, the ONLY record writer | the whole contract, pending from the accept inside the manager's debounce |
| 0x30 to 0x3F | stream format in | KL_aecp_dyn_state, selector 3 | the dynamic-state level | NONE | nvm_pend 1 until reset (E1: two accepted format changes; the tracked and composite builds commit record 0x30 erased, and the prototype commits no slot at all, "record 0x30 in slot None") |
| 0x40 to 0x4F | stream format out | KL_aecp_dyn_state, selector 4 | the dynamic-state level | NONE | nvm_pend 1 until reset |
| 0x50 to 0x5F | presentation time offset | KL_aecp_dyn_state, selector 5 | the dynamic-state level | NONE | nvm_pend 1 until reset |
| 0x60 to 0x7F | channel maps in and out | the AECP engine's mapping state | its commit mark, class 6, on aecp_nvm_stb_o / aecp_nvm_mark_o (donor scope D2, landed) | NONE | nvm_pend 1 from the first marked change until reset; never durable, and never written (UNRESOLVED 1) |
| 0x80 to 0xFF | user names | KL_aecp_desc_store (SET_NAME) | commit mark class 7, on the same pair | NONE | as the maps row: reported from the mark, never written (UNRESOLVED 1) |

Acknowledgement identity repairs none of the NONE rows; what this contract
guarantees for them is only that the status never claims durability over a
change it can see (E1 on the prototype: no_durable_claim_unmaterialized@first
and @end pass, and the tracked build fails both). Materialization itself is
UNRESOLVED 1. The channel-map and name rows are now REPORTED, because donor
scope D2 landed and the glue makes either mark sticky; what they still lack
is a writer, which is the same UNRESOLVED 1.

A writer for every NONE row is proposed on its own page,
[Saved-state materialization](SAVED_STATE_MATERIALIZATION.md) (issue #500,
PROPOSED): one processor-side record writer behind the same port, so this
contract applies to its records unchanged.

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
reading of a lost change. It stays so even after the same sink is rewritten
and committed later: a permanent false negative, never a false durable claim.
Whether and when the alarm may be forgiven is UNRESOLVED 7. The JEDEC cause has no reporter at the current
source (the writer performs no identity check): UNRESOLVED 5. EXECUTED
controls: M12_alarm_not_revoking is killed by B1 : alarm_revokes@end and
M13_report_not_revoking by F2 : failure_revokes.

## 13. Donor dependencies, each its own scope

None of these touches donor PR 26 or donor issues 14, 15 and 20, which stay in
their own lanes.

**D1, export the binding manager's unflushed state. LANDED** at the pinned
revision 424c688f (issue 90, merged): one new output port, no behaviour change.

- Port: protocol_processor_top carries
  `output logic [N_STREAM_IN_P-1:0] nvm_unflushed_o`, driven by
  `u_nvm_shadow.dbg_dirty_o`, which used to end on `nvm_dbg_dirty_nc_w`.
  It is a combinational read of the manager's `dirty_r` register, clk_i.
- Meaning, read off the manager rather than off the request: bit k is 1 from
  the cycle the manager ACCEPTS a change on sink k until it flushes it with
  done, or gives up after RETRY_MAX_P retries, which is the same cycle it
  raises alarm_o. Two refinements the export's own suite grades and this page
  had not stated: the accept is two clk_i cycles after the listener's record
  write, because the capture is pipelined one stage and the accept is the
  compare against the shadow, so a write-back that moves no persisted field
  never raises the bit at all; and a capture that lands mid-flush HOLDS it
  (the burst re-serializes), so the bit spans the whole unflushed interval
  and not just the first attempt. Neither weakens the parent use: both make
  the vector report exactly the changes the manager still owes.
- Parent use: KL_pp_shadow drives the backend's
  `pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_o) | <the D2 sticky bit>`.
- EXECUTED: E3_binding_inside_manager_debounce is an ordinary PASSING case of
  `tb/verilator/nvm_cosim` with the export bound. It was the suite's one
  labelled expected failure while the term was tied to zero, and the label is
  retired with the tie. On the donor side the export is graded at its source
  (`protocol-processor/tb/acmp_nvm` group X: raised on the accepted change, held to the commit's
  done, and dropped on the give-up cycle only with alarm_o) and at the pin
  (`protocol-processor/tb/pp_top` S9).

**D2, export the AECP commit marks. LANDED** at the pinned revision
424c688f (issue 90, merged): two new output ports, no behaviour change.

- Ports: `output logic aecp_nvm_stb_o` and
  `output logic [7:0] aecp_nvm_mark_o`, driven by KL_aecp_engine's
  `eff_nvm_stb_o` and `eff_nvm_mark_o`, which used to end on
  `aecp_eff_nvm_stb_nc_w` and `aecp_eff_nvm_mark_nc_w`. Both are
  combinational reads of the uCPU's E-stage registers (KL_aecp_ucpu
  `effects`), clk_i, one cycle per advanced OP_NVM_MARK, and the mark is the
  micro-op immediate, meaningful only while the strobe is 1.
- Mark encoding, from the microprograms that carry the op: **1** a
  dynamic-state field (SET_SAMPLING_RATE, SET_CLOCK_SOURCE,
  SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO), **6** channel maps
  (ADD/REMOVE_AUDIO_MAPPINGS), **7** user names (SET_NAME).
- Parent use: a mark of class 6 or class 7 sets a sticky pend_i source until
  the record that materializes it is written, or until reset while no writer
  exists -- and none does (section 11 is NONE for both), so at this revision
  it clears only at reset. Class 1 is deliberately not taken: the processor
  already publishes that group as the aecp_dyn_dirty_o level.
- EXECUTED at the pin: `protocol-processor/tb/pp_top` R21 grades a committed
  ADD_AUDIO_MAPPINGS raising one strobe carrying 6, a committed SET_NAME one
  carrying 7, and a GET raising none; tying `aecp_nvm_stb_o` to zero fails
  R21 and R21c by name. The program inventory stays
  [section 12.1](SAVED_STATE_FASTCONNECT.md#121-the-inventory-derived-from-the-donor)
  of the saved-state page.

**D3, materialization of the non-binding fields. STILL OPEN** -- the only
donor dependency of this contract that is. Not settled here and not
only an interface: a record writer must exist for every NONE row of section
11 before those fields can reach a slot at all. Whether it is a donor-side
manager per group or a parent-side writer behind a second device-face
initiator is its own scope: UNRESOLVED 1. Its proposal, one donor-side
writer for every group behind the one port, is
[Saved-state materialization, section 3](SAVED_STATE_MATERIALIZATION.md#3-decision).

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
  over its commits; it never strobes RELOAD either, so every record stays
  open and nvm_pend stays 1 (DERIVED).

## 15. Alternatives rejected

| Alternative | Rejected because | Evidence |
|---|---|---|
| A composite durable bit: pending work folded into nvm_dirty | Owner decision for the separate bit. Consequences found: the writer commits on nvm_dirty, so a field nothing materializes (every dynamic-state field today) triggers a full A/B commit every debounce window until reset, one sector erase each time; [section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven)'s recovery clears stale only when nvm_dirty is 0, so after any outage the status would read (1,1,1) "recovering" until reset; and the in-flight row of [section 9.3](SAVED_STATE_FASTCONNECT.md#93-reading-the-three-bits-together) would be shown permanently, which is dirty held asserted rather than a missed case repaired | EXECUTED as the alternative build mut-A01_composite_durable_bit (the prototype with the pending work folded into nvm_dirty, its status bit and the stale recovery): it passes every ordering check but FAILS E1 : pending_drives_no_commit@end with 5 full A/B commits (5 sector erases) in 6.03 s of model time for zero committable work, where the separate bit does 0 |
| The tracked rule (an ACK pulse clears dirty; the live image is the copy) | The issue #418 race and the round-1 counterexample | EXECUTED: A2 and B1 fail on the tracked build (section 2) |
| Round 2 as written (an attestation the flash write does not depend on) | A stale mask attests an erased span | EXECUTED: M08 and F01 are killed by C2 and fail C2e |
| A content rule (an erased span means "in progress") | Contradicts the ratified KLJ2 [6.1](SAVED_STATE_FASTCONNECT.md#61-the-container) erased-record rule: first-boot erased records are legitimate, and an erased span validates | EXECUTED: B7 passes only because erased records are accepted; C2e under M08 promotes an erased span that validates |
| Device idle as the record boundary; the tracked device-busy gate | Device idle occurs inside a logical record, and a gate on it lets one wedged record stop every other record | EXECUTED: C1g (idle between ERASE done and WRITE grant); F05 is killed by B9 |
| A completion counter, generation or sticky identity alone, without a per-record open bit | A counter of completions cannot see a record that is not completing, which is exactly the ERASE-error counterexample; the per-record open bit is the smallest sticky identity that names the record | EXECUTED proxies: M01 (open at completion) killed by B1, M02 (close on any completion) killed by C1g |
| Freezing the producer for the whole flash transaction | [Section 9.4](SAVED_STATE_FASTCONNECT.md#94-the-deadlines)'s worst case is 3.07 s at 1x1 and 3.26 s at 8x8, one erase dominating; the control plane would stall for seconds | EXECUTED: M07 (hold never expires) killed by C2 : hold_bounded; F3 keeps the producer's longest request-to-grant wait at 1 cycle with no flash at all; A9 keeps nvm_backed and a 250 ms heartbeat gap through a 3 s erase |
| An edge-detected producer change (the tracked parent glue) | A second change while the level is high is lost | EXECUTED: G01 killed by E1 |
| An acknowledgement without identity | A stale or duplicate ACK retires a newer capture; with the identity checked but not sent, nothing converges | EXECUTED: M04 killed by A6; F04 killed by A1 : stable_no_churn |
| Dirty from accepted bytes instead of a record close | A record whose bytes all moved before the arm but whose completion lands after it is retired unwritten | EXECUTED: M11 killed by A12 |
| RELOAD as an unchecked strobe, safe only by a writer obligation (the reviewed rule) | The backend cannot refuse a RELOAD that follows a failed operation, and a writer's promise of producer quiescence cannot be checked by anything | EXECUTED: R02, the since-re-base guard deleted, promotes record 0x20 erased in R1 under a durable reading |
| Narrowing RELOAD per record (a touched-since-load vector) instead of refusing it | A second per-record vector (53 flip-flops at 1x1, 156 at 8x8) for an event the cold-boot sequence never produces; refusing costs three flip-flops and the writer's repeat converges | DERIVED |
| A grant on the arm edge voiding the capture instead of being deferred | A capture voided on its own arm edge is a certain wasted attempt; deferring costs one term in the grant | EXECUTED: M19, the request granted on the arm edge, killed by U4 |
| Leaving the 50 ms bound per CAPTURE and stating the writer premise that makes it per request (that a capture's end and the next ARM are never adjacent) | The premise is a property of the writer's timing and of the bus between it and the control face, and nothing on either side is obliged to keep it; one flip-flop and one term make the bound hold whatever writes the strobe word | EXECUTED: M20, the arm accepted while a deferred request waits, killed by U10 ("granted 69733 cycles after it was raised") |
| Closing the F6 restart hole by the writer rule alone (load pending 1 with the walk sequenced means stay disabled), with no backend term | The same objection the reviewed RELOAD met: a writer's promise cannot be checked by anything, and the state it must avoid is exactly the one where the previous writer did not behave as promised. The backend term costs no flip-flop (it retimes an existing one) | EXECUTED: R06, both halves reverted to revision b, reproduces the finding ("record 0x21 in the newest verified slot False, still reported False, status claims durable True") and is killed by W2 |
| **Repairing the closed record instead of removing the capture** (revision d): a refused RELOAD re-opens every record as a re-base does, and an operation in flight at a re-base or at a refused RELOAD does not close its record when it completes (the re-review's sketch RS1, one flip-flop and two terms) | It repairs one symptom of a boot that validated nothing, per record and with new per-record behaviour on a path that already has four cases. Rule 9 removes the promotion itself, for every record and every ordering, with one flip-flop, one term and NO per-record state, and it is the stronger statement: not "this record is not promoted" but "this boot captures nothing". The sketch is a correct repair and is not needed once rule 9 holds; nothing else in revision d needs it, and the page does not adopt it | EXECUTED: R07, rule 9's term deleted, opens the capture and retires the work (U11, section 5.3 term table); W3 and W4 end with the record still closed, still reported and never durable |
| **Reporting a rule-9 refusal on a NEW status bit** instead of the existing [21] | A refused ARM is a refused ARM: the writer's response is the same for every cause, and [2] already distinguishes the cause for a controller and for a diagnostic read. A second refusal bit would add a controller-visible field that no rule in this contract reads | DERIVED; the writer's behaviour on [21] is step 3.2 of section 7 and is unchanged by revision d |

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
  (MILAN_NVM_STAGE_BASE): 3264 bytes at 1x1 and 12680 at 8x8,
  derived in [section 4.2](SAVED_STATE_FASTCONNECT.md#42-the-allocation----decided-the-donors-f078-rule-unchanged).
- A mutating producer request may be deferred up to 50 ms by ONE capture, and
  never by a second: an ARM is refused while a deferred request waits, so the
  bound is per request. Reads are never deferred. The deferral is a withheld
  grant on an interface that already holds its request; nothing is refused and
  no err is issued. The cost falls on the writer, which sees a refused arm and
  retries at its next service call.
- A record stuck open keeps its last verified bytes in every later slot
  while nvm_pend stays 1 and every other record keeps being saved.
- A completion that lands on the arm edge costs one extra commit. A mutating
  request that lands on the arm edge waits for the attestation or the hold's
  bound, like any request inside the hold.
- RELOAD is the boot load and is accepted at most once per reset, and never
  after the window has gone live. A writer restart without a fabric reset
  re-attaches instead of reloading, and a run-time reload would need a later
  contract to change the backend's rule. A boot repeats a refused load at
  most four times, waiting for the device face between attempts, and stops
  earlier if the window has gone live.
- **A boot in which no window load was accepted can write nothing.** No
  capture is armed there, so no slot is written, no flash erase is issued and
  no acknowledgement retires anything; the writer RETIRES for that reset; the
  entity runs on defaults; nvm_pend reads 1 and nvm_backed 0 until the next
  reset. The saved state is not lost (no slot is touched); it is not restored
  either, and the status says so through img_valid 0 and the restore-fail
  bit. **Only a reset leaves that state**, and a writer restart does not: it
  reads the load-accepted bit and stays retired. The trade is availability,
  and it is deliberate: a change accepted in such a boot waits for a reset
  instead of being committed out of a window that no accepted load vouches
  for.
- A record closed by a whole-record WRITE that streamed across a refused
  load's fill reads CLOSED over bytes the fill wrote. Nothing promotes it,
  because that boot captures nothing, and it is reported until a producer
  rewrites it or the fabric is reset (UNRESOLVED 11).
- An implementation inherits the four obligations O1 to O4 of section 7. They
  are not properties this page can prove of a later system; each is an
  acceptance item of the implementation lane.
- A verified slot is promoted even when its acknowledgement is refused; the
  refused work is simply captured again.
- nvm_backed now falls at a reported transaction failure and while the
  manager alarm is raised; the alarm holds it at 0 until reset.
- nvm_dirty keeps its [section 9.1](SAVED_STATE_FASTCONNECT.md#91-the-bits)
  meaning; the durable reading gains pend 0.
- The KLJ2 format, the erased-record rule and the A/B rule of
  [section 7](SAVED_STATE_FASTCONNECT.md#7-durability-the-ab-contract) are
  unchanged.
- Until D3 lands, channel-map and name changes are reported pending but are
  never made durable (section 11): this proposal does not hide that.

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
| 1x1 | 782 | 1051 | +269 | 377 | 476 | +99 | 6 and 6 |
| 1x1, no DSP | 846 | 1129 | +283 | 377 | 476 | +99 | 0 |
| 8x8 | 915 (787 + 128) | 1476 (1348 + 128) | +561 | 313 | 515 | +202 | 6 and 6 |
| 8x8, no DSP | 993 (865 + 128) | 1553 (1425 + 128) | +560 | 313 | 515 | +202 | 0 |

Revision b against the reviewed prototype, by the same method: +34, +26, -22
and +39 LUT in the four rows, and +3 flip-flops in each (the load flag, load
pending and reload refused). The reviewed RELOAD's per-record in-flight term
is gone; the arm-edge deferral adds one term to the grant. **Revision c
against revision b**: -20, +3, -3 and -61 LUT, and +1 flip-flop in each row
(the deferred-request bit; the window-live term is a wire). **Revision d
against revision c**: -21, -18, +13 and +4 LUT, and +1 flip-flop in each row,
which is `load_accepted` itself; rule 9 adds one term to an assignment that
already had six. The new terms of all three revisions are one gate each on
paths the synthesiser was already mapping, so the LUT figures move by less
than the tool's own noise between otherwise identical runs and the sign is
not meaningful; what is measured is that no bound and no rule here costs area
worth naming, and that revision d costs exactly the one flip-flop the
direction budgeted.

DERIVED breakdown: the open vector is one flip-flop per allocated record, 53
at 1x1 and 156 at 8x8 by the record table of the run, and its per-record
compare against the operation's region drives most of the LUT delta at 8x8;
the rest is the capture state, a 16-bit identity, the hold counter, the two
dirty halves, the four load bits and the deferred-request bit (about 46
flip-flops). Against the XC7A100T's 63,400 LUT the 8x8 delta is 0.9 percent
(0.9 without DSP). Post-place figures are owed by a bitstream build.

MEASURED firmware, RV32I at -Os against the same target stubs: text 9790 to
12550 bytes at 1x1 (+2760) and 9906 to 12710 at 8x8 (+2804); bss +12 bytes;
data unchanged. Revision b's window load, re-attach path and messages account
for 640 and 676 of those bytes, revision c's retirement, its bounded wait for
the device face, its restart rule and their messages for 360 more in each
(bss +4: one flag), and revision d's two-bit restart split, its stop on a
live window and their messages for 300 more in each, with no new static.

Memory shape: the stage holds one container.
[Section 4.2](SAVED_STATE_FASTCONNECT.md#42-the-allocation----decided-the-donors-f078-rule-unchanged)
derives 3264 bytes at 1x1 and 12680 at 8x8.

Timing. The prototype's RV32I -Os build measured per-byte instruction counts.
The following times are DERIVED, without hardware measurements.
The hold covers copying closed records after ARM.
Flash prefill happens before ARM, outside the hold.
The model uses six instructions and two DDR accesses per byte.
Walking each record adds about 50 instructions.
Each instruction costs 10 cycles; each DDR access costs 30.
The pessimistic case doubles both cycle costs.

The current gate supplies section 4.2's raw areas and counts.
These exclude container headers, alignment padding, and trailers.
For raw area `A` and record count `N`:

```text
instructions = 6 * A + 50 * N
DDR accesses = 2 * A
cycles = 10 * instructions + 30 * DDR accesses
time_ms = cycles * 1000 / 50000000
hold_margin = 50 / time_ms
```

| Quantity | 1x1 | 8x8 |
|---|---|---|
| Raw bytes / records | 3,218 / 53 | 12,634 / 156 |
| Instructions | 21,958 | 83,604 |
| DDR accesses | 6,436 | 25,268 |
| Nominal cycles | 412,660 | 1,594,080 |
| Nominal copy / 50 ms hold margin | 8.3 ms / 6.06x | 31.9 ms / 1.57x |
| Twice both costs / hold margin | 16.5 ms / 3.03x | 63.8 ms / 0.78x |

The shipping CPU clock is 50 MHz.
`sw/litex/milan_soc.py` selects it from the Milan domain.
The [clock-domain page](../litex/CLOCK_DOMAINS.md) records this shipping choice.
The CPU memory master also crosses into the system domain.
Hold sizing must use the writer's actual clock and measured latency.

**The grown 8x8 copy exceeds 50 ms under doubled costs.**
A grant after hold expiry voids capture; release and retry preserve safety.
Sustained producer activity risks liveness through repeated void-and-retry cycles.
The shipping 1x1 shape and its margins are unchanged.

[The #501 decision](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5823589125)
retains the hold without an RTL change here.
Today only BINDING is materialized; maps are not copied yet.
No materialized map copy can overrun the hold today.
Donor writer adoption through processor #61/#83 must measure the copy.
It must size the hold with a stated margin.
Alternatively, measurements must prove the existing 50 ms adequate.
The [donor acceptance obligation](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/61#issuecomment-5823590638)
requires recording those measurements in UNRESOLVED 6.

The hold remains below the 500 ms heartbeat period.
It also remains below the 8000 ms commit deadline.
The parameter refuses a hold at or above that deadline.
Hardware timing and memory ordering remain UNRESOLVED 6.

## 19. The executable model and its omissions

- ONE process per build: the real donor KL_acmp_nvm_shadow, KL_pp_nvm_port
  and KL_aecp_dyn_state at 8f2f58fb, the backend (tracked file or the
  prototype copy
  `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/proposal-evidence/prototype/KL_nvm_backend.proto.sv`),
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
- The writer restart of W1, W2, W3 and W4 is modelled on the host by a
  function the run script appends to the host build of the prototype writer
  only. It
  returns every file-scope variable of the writer to its initial value and
  runs the writer's boot again; the run script refuses to build it unless it
  names every such variable. **Nothing else of a CPU reset is modelled**, and
  the omissions matter to the reading of those four cases: the boot code's own memory
  initialisation is not modelled, nor is any test or re-initialisation of the
  memory that holds the live window, nor the bus fabric's state. The model
  therefore ASSUMES obligation O4 of section 7 (the window and the fabric's
  view of it survive the restart); it cannot test it. UNRESOLVED 10.
- One physical premise both checked copies rest on, which the model cannot
  show: that a backend write reported done is visible to the CPU's memory
  port, which is a different port of the same controller. The capture (the
  CPU reads what the backend wrote) and the load (the backend's flag vouches
  that nothing else wrote) both assume it. The model has one memory and no
  port ordering. It belongs with the hardware measurement, UNRESOLVED 6.
- Totals, revision d, from a clean state: 2637 graded runs over 45 builds: 3
  prototype builds (1x1, 8x8, and a 2-bit identity build for the wrap
  control), 2 tracked builds, 1 mixed build (the new writer on tracked
  gateware), 38 mutants and 1 executed alternative; 13,371 graded checks
  (12,608 pass, 418 fail, 345 not expressible). The 1x1 prototype passes 318
  checks with 1 listed expected failure (E3 without D1); the 8x8 prototype
  passes 146 of 146; every one of the 39 mutants is killed by its named
  check; the tracked build still fails the three checks of section 2 at both
  shapes. Revision c had 2250 runs over 42 builds, 282 plus 1 and 114 of 114;
  revision b had 1824 runs over 37 builds, 258 plus 1 and 98 of 98; the
  reviewed record had 1326 runs over 31 builds, 180 plus 1 and 55 of 55. See
  `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/COMMAND_RESULTS.md`.

## 20. UNRESOLVED

1. Materialization. Nothing writes a record for configuration index,
   sampling rate, clock source, stream formats, presentation time offset,
   channel maps or names at the current source; only bindings have a writer.
   The pending bit reports the dynamic-state fields truthfully (1 until
   reset); making them durable needs scope D3, which is proposed in
   [Saved-state materialization](SAVED_STATE_MATERIALIZATION.md) (issue #500).
2. CLOSED for reporting by donor scope D2 (issue 90): the channel-map and
   name commit marks reach the parent on `aecp_nvm_stb_o` /
   `aecp_nvm_mark_o`, and either sets a sticky pending source, so the status
   no longer reads durable over them. Making them durable still needs D3,
   which is item 1.
3. CLOSED by donor scope D1 (issue 90): `nvm_unflushed_o` is bound in
   `KL_pp_shadow`, a binding inside the manager's debounce reads pending from
   the accept, and E3 passes as an ordinary case.
4. Whether the shipping memory bridge can withhold a write completion forever
   is not established. The contract relies on neither answer, but a silent
   write wedges the single-outstanding device face, so no later record
   operation of any record is granted until reset; a device-face timeout that
   ends such an operation with err is a possible follow-up, not proposed here.
5. The JEDEC identity-mismatch revocation cause of
   [section 9.2](SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven)
   has no reporter at the current source.
6. Physical timing remains unmeasured: capture hold, debounce, and memory ordering.
   Section 18 derives the current full-copy budget at 50 MHz.
   At 8x8, 12,634 bytes over 156 records take 31.9 ms nominally.
   Doubled cycle costs give 63.8 ms against the 50 ms hold.
   The corresponding margins are 1.57x and 0.78x.
   Void and retry preserve safety; sustained activity risks liveness.
   Shipping 1x1 stays unchanged: 8.3/16.5 ms, margins 6.06x/3.03x.
   Only BINDING is materialized today; maps are not copied yet.
   Processor #61/#83 adoption must measure the actual 8x8 copy.
   Size the hold with a stated margin from that measurement.
   Alternatively, prove the existing 50 ms sufficient with measurements.
   Record the result here, as the
   [donor obligation](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/61#issuecomment-5823590638)
   requires. The section 19 memory-port ordering also needs measurement.
   The debounce measurement remains open under
   [section 14](SAVED_STATE_FASTCONNECT.md#14-what-this-page-does-not-decide).
7. Alarm forgiveness. The donor alarm is sticky until reset, so one retry
   exhaustion holds nvm_backed at 0 and nvm_stale at 1 until reset, even
   after the same sink is later rewritten and committed (section 12). That
   is a permanent false negative, never a false durable claim. A donor-side
   alarm clear, or a backend rule that forgives the alarm after a later
   verified commit of the record, is not defined here.
8. A writer disabled for a SHAPE or TAG mismatch (section 14) keeps
   heartbeating, so it reads as a live writer that never commits: (backed 1,
   dirty 0 or 1, stale 0) with pend 1. It is the TAG mismatch alone: on a
   SHAPE mismatch the writer returns before it installs its service hook, so
   nothing heartbeats. That predates this contract and this page does not
   change it; revisions c and d retire the writer only in the state they
   introduce, the terminal row of section 5.3. Making every disabled writer
   stop heartbeating would be a one-line change with a wider blast radius
   (the mixed-build case reads backed 1 today) and belongs to the
   implementation lane, with the saved-state section 9.3 rows re-read.
9. Obligations O1 (one sequential writer) and O2 (one reset domain) of
   section 7 are what exclude the pre-reset acknowledgement alias of section
   5.4. O2 holds for the product examined here (one PLL, the board reset) and
   the reverse -- a CPU-only reset -- is real; a fabric-only reset is not
   excluded by hardware, only by the absence of a reset controller that could
   request one. Neither obligation is enforced by anything in the backend. The
   honest alternatives, neither chosen here: make the identity not repeat
   across a reset (a reset-surviving identity or a boot nonce), or have the
   backend refuse an acknowledgement until the writer has re-armed after the
   reset it did not see. Until one is taken, a later lane that adds a second
   control-face master or a datapath soft reset re-opens the alias.
10. Obligation O4: whether the live window and the fabric's view of it
    survive the product's CPU-only restart is NOT established. The re-attach
    branch needs the memory holding the window to still hold what the backend
    believes it holds; a restart path that re-initialises that memory would
    leave records reading closed over bytes nobody wrote, and the once-per-
    reset rule refuses the only action that would repair them. What stands
    between that and a slot is the stage validation, which a corrupted frame
    fails; a span that reads all 0xFF is a valid erased record under the
    ratified KLJ2 rule and would be promoted. The two honest ways out: show
    that the window survives the product's CPU-only restart, or make every
    CPU reset a fabric reset, in which case load pending reads 1 with no walk
    sequenced and the cold-boot path runs. Whichever is chosen belongs in the
    implementation lane's acceptance. Not reachable in the cold-boot contract
    and not a defect of the backend rules; W1 to W4 cannot see it
    (section 19). Revision d narrows the exposure but does not close the item:
    the re-attach branch is now taken only when PP_NVM_STAT[2] says the
    backend accepted the load, so a boot that validated nothing no longer
    re-attaches at all; a boot that DID accept its load still re-attaches over
    a window this page cannot prove survived the restart.

11. **A record closed across a refused load's fill stays closed until a
    producer rewrites it or the fabric is reset** (revision d, from the second
    re-review). A refused RELOAD does not un-write the window: the fill wrote
    the whole window, so a whole-record WRITE streaming across the last
    attempt's fill ends with done over bytes the fill wrote, and its record
    reads CLOSED although the producer did not write those bytes. Rule 9 makes
    this safe rather than absent: nothing in that boot can capture, commit or
    retire, so the record is REPORTED and never promoted, the last verified
    slot is untouched and no reading is durable (W3, W4). What is not resolved
    is convergence WITHIN that reset: the record's bytes are wrong until
    something rewrites it, and only a producer rewrite or a reset does. The
    honest alternative, not taken here, is the re-review's RS1 (a refused
    RELOAD re-opens every record, and an operation in flight at a re-base or a
    refused RELOAD does not close its record); section 15 says why rule 9 was
    preferred. An implementation lane may adopt RS1 in addition, and nothing
    in this contract forbids it.

## 21. Traceability

Issue body, acceptance for this design phase:

| Bullet | Where | Executed by |
|---|---|---|
| Exact handshakes and ownership: already-granted writes, deferred requests, concurrent captures | 4, 5, 7 | A11, A12, C1g, C1, C1r, C5, U4 (a request on the arm's own edge) |
| ACK cannot clear newer work before, on or after its edge; no-change converges; dirty not held to pass | 5, 6 | A2, A3, A4, A1; convergence requires the durable reading (M18); U11 (no capture opens in a boot that accepted no load, so no ACK there can retire anything) |
| No transient erased record promoted; first-boot erased records kept; last verified slot kept on failure | 3, 4, 7, 8 | B1 to B5, C1g, C2, C2e, B7, B8, F2, R_power_cycle; W3 and W4 (a record closed across a refused load's fill is reported, never promoted) |
| Control plane responsive; producer pause quantified with a timeout | 3, 5, 18 | C1 and C1r (deferral ends at the attestation, 23 cycles after the arm), C2 and C2e (bounded at 50 ms, then the capture is void), U10 (the bound across chained captures), A9, F3 |
| Reset and re-arm, abandoned and duplicate ACKs, counter wrap, CRC and sequence promotion, liveness and stale | 5, 5.3, 5.4, 6, 7 | U1, U7 (reset row), A5, A6, A8, C7, C8, D1, F2; R1, U5, U6, U8 (the window load), U9, U12, U13 (a boot that accepts no load: the terminal row in both its readings), U11 (no capture there), W1, W2, W3, W4 (writer restarts) |
| Bounded executable model on production interfaces, missing orderings, meaningful mutations, omitted timing stated | 9, 15, 19 | 2637 runs; 38 mutants each killed by a named check, and one executed alternative |
| ADR, source hashes, command results; review ledger before product edits | this page; `branch 419-design-evidence, commit bf523a78402ebf4ab0a1c8977bd0288a4e61ef2f, path design-evidence/419-snapshot-ownership/COMMAND_RESULTS.md` | the review ledger belongs to the independent reviewers |

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

The contract review at `b6ae45a5`, revision b (the NEGATIVE review's findings
are N1 to N5, the POSITIVE review's P1 to P5 and its suggestions PS1 to PS4):

| Finding | Answer | Where | Executed by |
|---|---|---|---|
| RELOAD closes a record on device idle and can promote a failed erased record (N1, MAJOR; P2) | The backend checks RELOAD: a load flag armed by a re-base with nothing in flight, cleared by any mutating grant, accepted once per reset; a refusal changes nothing; the writer repeats the load; a restart re-attaches | 3 (rule 8), 4, 5.3, 6, 7 | R1 (the review's ordering), U5, U6, W1; R01, R02, R03, F07, F08 killed |
| A mutating grant on the arm edge is neither deferred nor voiding (N2; P1) | Deferred: the hold starts on the arm's own edge, and the vector is exact from the first cycle after it | 3 (rule 3), 4, 5.2, 6 | U4; M19 killed |
| Reset of the capture machine undefined; the identity restarts at reset (P3) | The reset row; the identity across a reset, argued from the shared reset and the one sequential writer, with the reachable orderings executed | 5.4 | U7, U1 |
| PP_NVM_STAT[22] (N5; P4) | [22] is nvm_pend, the same wire as the port | 5.1, 6 | pending_bit_is_status_bit_22 on every run |
| The landing base is stale (N3; P5) | The base, its pin and the nine changed files are stated | the preamble | - |
| The boot order of section 7 step 1 (N4) | The executed order, step by step | 7 | R1, W1 |
| The owner's confirmation is not cited (PS3) | Cited | the status block | - |
| "far below 50 ms" carries no number (PS2) | The measured instruction count and a derived time | 18, 20 (item 6) | - |
| Alarm forgiveness (PS1, and a suggestion of the NEGATIVE review) | UNRESOLVED 7 | 12, 20 | - |
| "record 0x30 erased in every slot" (PS4) | Stated per build | 11 | E1 |

The re-review at `53b2026e`, revision b (the NEGATIVE review's findings are
M1 to M3 and its suggestions MS1 and MS2 here; the POSITIVE review's are G1
to G6 and S5 to S7):

| Finding | Answer | Where | Executed by |
|---|---|---|---|
| A restart from the four-refusal state takes the cold-boot path over a live producer, and the accepted RELOAD retires work no slot holds (M1, MAJOR) | The boot load also closes when the WINDOW GOES LIVE, so no RELOAD is accepted once the producer could write; the writer rule (load pending 1 with the walk sequenced means stay disabled) is stated beside it; rule 8 and the two universal sentences of 5.3 are corrected | 3 (rule 8), 5.3, 6, 7 (step 1.4 and O1 to O4) | U9, W2; R05 and R06 killed |
| The hold's bound is no longer by construction across chained captures (M2, MINOR; G2) | An ARM is refused while a request this backend deferred still waits; the bound is per request | 3 (rule 3), 5.2, 17 | U10; M20 killed |
| The one-writer exclusion and the shared reset are argued, not stated as obligations (M3, MINOR; G5) | Stated as obligations O1 and O2, with UNRESOLVED 9 for what is not enforced; W1's modelling limit moved into section 19 as well | 5.4, 7, 19, 20 (items 9 and 10) | - |
| "a grant on a re-base edge leaves the load flag clear" is labelled EXECUTED and no case executes it (G1, MINOR) | Executed, with the priority's own mutant | 5.3 (the term table), 6, 9 | U8; R04 killed |
| The four-refusal terminal state has no status row, and nvm_backed stays 1 in it (G3, MINOR) | The row is stated in full and graded bit by bit; the retired writer stops heartbeating, so nvm_backed reads 0 | 5.3, 7 (step 1.6), 17 | U9; F10 killed |
| The re-attach rule rests on an unstated precondition, and the restart path may re-initialise the window's memory (G4, MINOR) | Stated as obligation O4 and carried as UNRESOLVED 10 with the two honest ways out; section 19 states what the restart model omits | 7, 19, 20 (item 10) | - |
| The derived copy time assumes 100 MHz; the shipping core runs at 50 MHz (G6, MINOR) | Re-derived at 50 MHz: about 22 ms and 44 ms at 8x8, a margin of 1.1 to 2.3 | 18, 20 (item 6) | - |
| The repeat does not wait for the device face (S5) | The repeat waits, bounded, for the device face to go idle | 5.3, 7 (step 1.5) | R1, U9 |
| Two gaps around the reset row (S6) | The unreadable clause is named as such, and the pending bit's boot-interval cause is in the dictionary row | 5.4, 6.1 | - |
| Memory-port ordering between the two checked copies (S7) | Named in section 19 and folded into UNRESOLVED 6 | 19, 20 (item 6) | - |
| A completed WRITE between the load and the RELOAD is sound only because the restore walk follows (MS1) | Said, and made an obligation on scope D3 (O3) | 5.3, 7 | R1 |
| "77 evidence sources" and "every run also grades" (MS2) | Counted and qualified | the preamble, 9 | - |

The re-review at `e2d98d88`, revision c (the NEGATIVE review's findings are
K1 to K3 and its suggestion S8 here; the POSITIVE review's are F9 to F11 and
four suggestions). Both reviewers found the same two MINOR defects
independently, so the rows below carry both labels:

| Finding | Answer | Where | Executed by |
|---|---|---|---|
| A record closed across a refused load's fill is promoted by a re-attached writer, its work is retired by an accepted acknowledgement, and the status can read durable over it (K1, MAJOR) | Rule 9: no capture is armed until a RELOAD has been ACCEPTED since reset (one registered flag, one term). A boot that accepted no load opens no capture, so nothing in it can be captured, committed or retired; the record stays closed and REPORTED. The restarted writer does not re-attach in that state. The two sentences that claimed more (O3's second, and 5.3's "commits what the window holds") are corrected, and the residual is carried as UNRESOLVED 11 | 5.1, 5.2, 5.3 (rule 9 and the term table), 6, 7 (step 1.3, step 3.2, O3, O4), 15, 20 (item 11) | U11, W3, W4 (the reviewer's probes H1 and H2), W2 re-graded; R07 and F11 killed |
| Once the window has gone live the writer still re-bases and refills it three more times, and a two-grant disturbance is terminal although the page describes the repeat as converging (K2, MINOR; F9, MINOR) | What "bracket" means is stated exactly (the FIRST mutating grant after a re-base, and no other), the page says the terminal state is reachable from one disturbed attempt, and the writer reads [3] after a refusal and stops repeating once it reads 0 | 5.3, 7 (step 1.5), 9 | U12; F12 killed |
| The terminal row is the row of ONE ordering, and it has no reading after a restart (K3, MINOR; F10, MINOR) | The row is split into the bits the STATE fixes and the bits the ORDERING decides, each with its cause; the second reading is executed; and the row after a restart is the same row, because the writer no longer re-attaches | 5.3, 9 | U9 (the cold row), U13 (the row after a heartbeating wait), W2, W3, W4 |
| Bit [3]'s dictionary row still reads "no RELOAD accepted since reset", the reading 5.3 tells a reader not to use, and the prototype's two comments carry it too (F11, MINOR; S8) | The dictionary row carries the reading 5.3 uses, the new bit [2] is what distinguishes the two, and both prototype comments are corrected | 5.1, the prototype backend and writer at the cited commit | - |
| The terminal row could name [5] img_cfg 1 beside img_valid 0 (S8) | Named, with the reason: it is why producer writes land in a window whose reads come back blank | 5.3 | U9, U13 |
| UNRESOLVED 8 overstates: a writer disabled for a SHAPE mismatch does not heartbeat (suggestion) | Corrected; it is the tag mismatch alone | 20 (item 8) | - |
| "step 1.6 is skipped too, since the walk in step 1.7 runs only if the fabric has not" justifies skipping 1.7, not 1.6 (suggestion) | Reworded: 1.6 is skipped because the writer is retired | 7 (step 1.4) | - |
| c_hold_bounded_chained has no contract guard and grades vacuously on the tracked build (suggestion) | NOT adopted in revision d. The check's vacuous pass is disclosed and is not what makes it non-vacuous where it matters, which is M20; adding a guard changes run.py's grading surface for no finding, and this revision was directed to add no mechanism beyond the one term. Carried for the implementation lane | 19 | M20 |
| Section 20 items 8 to 10 and O1 to O4 should be copied verbatim into the implementation Issue's acceptance criteria, and the re-attach branch should not ship before item 10 is decided (suggestion) | Accepted as an instruction to the lane that opens that Issue; this page cannot open it. UNRESOLVED 11 joins the list | 7, 20 | - |
