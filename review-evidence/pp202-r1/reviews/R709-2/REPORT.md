[R709] NEGATIVE - exact head ebb1f0010bde76c38cc5270a6366ee9e3157ec54

# R709-2: independent review of PR #204 (issue #202) at exact head

- **Head:** `ebb1f0010bde76c38cc5270a6366ee9e3157ec54`, tree `ce4931d11f3730d05e6ff8934ec96ddc2366578f`. Eight commits on `ed211803`. This round's delta is the four commits `a8aa626e..ebb1f001` (17 files, +475/−101).
- **Verdict:** NEGATIVE. Two MINOR findings are open, F1 and F2. There are also two RESIDUE items and three SUGGESTIONs.
- **Prior public findings:** R709-1 had F-1, F-2, F-3, RESIDUE-1 and S-1 to S-5. R710-1 had F01, F02 and R01. All three MAJOR/MINOR findings from each review are resolved at this head. R709-1 S-1 is superseded by F1, because the delta made its applicant window reachable. The full table is below.
- **Independent verdict first:** I wrote `independent-verdict.txt` (sha256 `d88837ae…`) before reading any prior finding. This report keeps its verdict and findings, and adds F2 and the resolution table. I found F2 after that point, while checking the author's parent receipts.

## How the review was done

- **Reconstruction:**
  - The repository has no AGENTS.md or CONTRIBUTING.md. I used README.md and docs/README.md (conventions, single-source rules, `make check`).
  - Issue #202: the body and its nine comments (the assignment, the STOP, the option-A owner decision, the round-3 hand-over and the REVIEW READY notices).
  - The PR #204 body.
  - The interface and requirement authorities the diff touches: 00 REQ-ACMP-010/GAP-04, 02 §4.2/F02.10, 05 F05.12 and `sec-05-sidmove`, 06 §6.2, 08 F08.1, 09 §8.13, 10 §6.1/F10.4, and the integrator guide.
  - Then `git diff ed211803..ebb1f001` and the history. Because this is a later round, I judged the delta `a8aa626e..ebb1f001` at its cause. Code the delta does not touch keeps its R709-1 lens verdict unless the delta changes what it depends on.
- **Public evidence:**
  - kebag-logic/milan-fpga `015d2d6a`, `review-evidence/pp202-r1`. All 1,191 `author-r3/` files match `MANIFEST.json`: 0 mismatches and 0 unlisted files (`receipts/evidence-verification.txt`).
  - `gate-status.json`: every accepted receipt has rc 0, with 1,030,552 processor checks.
  - Issue and PR evidence comments: at this head there is only the review-start notice.
- **Execution:**
  - Every build ran in a disposable copy under `scratch/`, using the pinned simulator. It identifies as 5.050; the wrapper digest is in `receipts/env.txt`.
  - Independent jobs ran concurrently.
  - Afterwards I verified the review clone byte-exact (`receipts/source-integrity.txt`):
    - write-tree is `ce4931d1`;
    - status, including ignored files, is empty;
    - the index (mode, blob, path) digest equals the tree's;
    - all 705 work-tree blobs and modes match;
    - there are 0 gitlinks, so there are no submodules to check.

## What I executed at this head

| Run | Result | Receipt |
|---|---|---|
| `tb/acmp_talker` | 1,520 checks: 1,520 PASS, rc 0 | `talker-head.log` |
| The head bench on the `a8aa626e` talker RTL | 1,502 PASS, 18 FAIL (J7, J7b, K8, S1 disable, S7 ×4, S8 ×4, S9, S10 ×5), as the PR states | `talker-head-bench-on-a8aa626-rtl.log` |
| STREAM_ID group of `tb/pp_top/acmp_mutants.py` (22 names, 25 arms, `--jobs 8`) | **25 of 25 KILLED** by their named checks. Goldens PASS: `acmp_talker`, and `pp_top --maap-internal-only` (MP8, including the new JoinMt check). This covers the new arms `pcp_after_withdrawal_skips_the_gap`, `pcp_pending_not_held`, `disable_keeps_declared_id`, `reopen_sends_new` and `publish_upper_from_slot0` | `streamid-mutants.log`, `streamid-mutants-results.json` |
| Talker `make lint` (zero-warning gate) | rc 0 | `talker-lint.log` |
| `make check` (in a disposable git clone at head) | rc 0 | `make-check.log` |
| Reviewer probe LV (SRP talker FSM) | see F1 | `lv-probe.log` |
| Reviewer probe WINDOW (talker, S10 block-allocator leg) | see F1 | `talker-window-probe.log` |

The author's sweep and campaigns were built at `9a6d1d08`. I checked that `9a6d1d0..ebb1f00` changes only `05_acmp_engine.md`, three READMEs and one comment in `tb/acmp_talker/sim_main.cpp`. No HDL, script, syn or Makefile changed. So the published receipts apply to the consumed inputs at this head:

- `run_suites-9a6d1d0`: 1,030,552 checks, 0 failing;
- req-tags: 241;
- the ACMP campaign: 90/90;
- the other campaigns.

## Focus: the delta against the issue's acceptance

**1. PCP change after a withdrawal (answers R710-1 F01).**
- `EVC_PCP` from `DA_OK` with `sid_used_r` set enters `BACKOFF` and draws `T-SRP-LEAVEALL2` (`hdl/acmp/KL_acmp_talker.sv:903-909`).
- `pcp_hold_w` (`:526-528`) holds every same-ID open while a PCP change is pending, including in the strobe's own cycle. That covers:
  - the probe path (`:778`);
  - the grant (`:843-844`);
  - the backoff exit (`:921`);
  - the Listener event (`:950-951`).
- A moving grant is exempt from the hold. That is correct: by the cursor property, its ID has never been on the wire.
- 05's claim that a declared source in `NO_DA` always has a move booked holds. Only three paths reach `NO_DA` with `sid_used_r` set:
  - `EVC_CONFLICT`, which books the move;
  - `EVC_OFF`, which books the move;
  - a backoff exit with an invalid DA, and only a conflict invalidates the DA there.
- S7, S8 and S9 grade R710-1's exact interleaving on the configured ID and on a moved ID. Both new mutants are killed.

**2. Disable of a declared source books a move (answers R709-1 F-1).**
- `EVC_OFF` sets `ev_sid_owe_w = sid_used_r` (`:874`).
- S10 covers a fresh DA, and a block allocator returning the same DA. `disable_keeps_declared_id` is killed.
- J7 and K8 follow the rule.

**3. Publish, Join! and comments (answers R709-1 F-2 and F-3, and R710-1 R01).**
- S4 binds every slot's whole published ID.
- 10 F10.4 now says the re-open is a Join!. MP8 reads the first AttributeEvent (JoinMt), and `reopen_sends_new` is killed.
- The source-comment labels R710-1 listed are gone. The delta adds no new lane, round or reviewer label to source comments.

**4. Conflict path and reporting.** The delta does not change these, so the R709-1 verdict holds:
- conflict to new declaration in 1,700 ms (S1) and 1,737 ms (MP8);
- `TALKER_DEST_MAC_FAILED` only before the grant.

## Findings

### F1 MINOR: after a disable and return inside one `T-MRP-JOIN`, the moved ID's declaration replaces the withdrawn ID's owed Leave, so that Leave is never sent

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/acmp/KL_acmp_talker.sv:851-875`: the delta's `EVC_OFF` move booking. The grant then opens at once under the moved ID (`:835-847`).
  - `hdl/srp/KL_srp_talker_fsm.sv`:
    - `:473`: the open is a Join!;
    - `:236`: LA + Join! → AA;
    - `:512`, `:588-591`: the open overwrites the source's single `{stream_id, DA, VLAN}` record.
  - `docs/architecture/05_acmp_engine.md:498-504` and `docs/architecture/10_srp_engine.md:433-434`.
  - The PR body, "Notes for review".
- **Authority:**
  - IEEE 802.1Q-2018 §10.7: the Applicant state machine and its Table 10-3 run per attribute. The 10 text itself says "a new StreamID is a new attribute value". The withdrawn ID's WITHDRAW (Lv!) leaves that attribute's applicant in LA, owing its Leave at the next tx!. A Join! for a different attribute value does not cancel that Leave.
  - Issue #202, Required: "the talker withdraws as now".
  - The processor's own listener FSM already parks a changed stream_id so that the owed Lv goes out (`hdl/srp/KL_srp_listener_fsm.sv:70-74`, `:106-107`, `:812`).
- **Evidence:**
  - `receipts/lv-probe.log`, from the SRP talker FSM unit (`scripts/run_lv_probe.sh`):
    - Probe arm: declare `…0003`, withdraw it, re-open the same source under `…0008` before the next tx!, then tick twice. The only push is `event=3` (JoinMt) for `…0008`. No Lv for `…0003` is ever sent.
    - Control arm: with one tx! between the close and the open, the FSM sends `event=5` (Lv) for `…0003`, then the JoinMt for `…0008`.
  - `receipts/talker-window-probe.log` (`scripts/run_talker_window_probe.sh`; S10's block-allocator leg unchanged, 1,520/1,520 PASS). src5's close (`…0005`) and its open under `…0009` both happen at 1500 ms, so the interval is 0 ms.
  - Reachability:
    - The in-scope MAAP engine answers ALLOC_DA in the next cycle while in DEFEND, and RELEASE_DA is a no-op (`hdl/maap/KL_pp_maap.sv:100-106`). So a disable and return of a declared source is granted at once.
    - The gate re-opens at that grant whenever the Listener registrar still holds the old registration. The registrar is cleared only at a re-open, not at a close (`KL_srp_talker_fsm.sv:745-749`). It also re-opens on any probe.
    - The author's own text (05:503-504) says that "a disable and return answered within one `T-MRP-JOIN` can" reach this window.
  - R709-1 S-1 judged this window unreachable at `a8aa626e`. There, a return re-declared the same ID, and LA + Join! → AA was the correct cancel within one attribute. This round's disable move turns it into a replacement across two attributes.
- **Impact:**
  - The withdrawn Stream ID is never withdrawn on the wire. Its Talker Advertise stays registered at the bridge until LeaveAll aging (one LeaveAll period plus LeaveTime).
  - Any Listener Ready still declared for the withdrawn ID keeps its reservation in place beside the new ID's. On a loaded link, the new reservation can fail admission for that period.
  - A listener still bound to the withdrawn ID sees a live Talker Advertise for a stream that no frame carries.
  - §35.2.2.8 itself is not violated: nothing is re-declared under the withdrawn ID.
- **Required outcome**, one of:
  - **(a) RTL.** Do not let a moved ID's open reach the SRP applicant while the withdrawn ID's Leave is still owed. Either:
    - hold a moving open until a tx! has passed since the close, or until the applicant reports that the Leave was sent; or
    - park the withdrawn ID in `KL_srp_talker_fsm` and send its owed Lv before latching the new ID, as the listener FSM does.

    Then add an SRP-level or wire-level check that a disable and return with an immediate grant puts the withdrawn ID's Lv on the wire, and add a named STREAM_ID mutant that removes the hold.
  - **(b) Owner ruling.** The owner accepts the lost Leave as a documented deviation. Then:
    - correct 05:498-504 and 10:433-434 so they no longer cite Table 10-3 for a transition across two attribute values;
    - state the deviation, its window, and its impact (a stale registration and reservation for up to one LeaveAll period plus LeaveTime);
    - record the probe shape as a committed check.
- **Verification:**
  - For (a): the PROBE arm of `scripts/run_lv_probe.sh`, adapted to the new interface, shows the Lv for the withdrawn ID, and every suite stays green.
  - For (b): the ruling and the corrected text are present.

### F2 MINOR: the PR body's 8x8 parent timing has no published receipt; the receipt says 1,816 ms

- **Lenses:** Tests, Docs.
- **Where:**
  - The PR #204 body, "Parent integration and consumer gate": "declares a new ID in under 2 s (1,735 ms and 1,778 ms)".
  - `review-evidence/pp202-r1/author-r3/HANDOFF.md:175` ("1,778 ms on 8x8").
- **Evidence:** `receipts/evidence-verification.txt`.
  - The published `author-r3/receipts/parent/sidmove8-8x8-head.txt` (rc 0, 52 checks, 0 failures) records `conflict to the new ID's declaration under 2 s (1816 ms)` for both graded talkers.
  - The round-2 precedence control also records 1816 ms.
  - No `author-r3` file contains "1778 ms".
  - The AX 1x1 figure (1,735 ms) matches its receipt.
- **Impact:** a stated measurement that the published evidence does not support. Both values are under 2 s, so the acceptance verdict is unaffected. It is a figure, so it is not RESIDUE.
- **Required outcome:** either state 1,816 ms in the PR body and the hand-over, or publish the receipt that measured 1,778 ms and name its pin.
- **Verification:** the PR body's figure matches a listed receipt.

### RESIDUE-1: two port comments omit the disable move

- **Where:**
  - `hdl/top/protocol_processor_top.sv:680-682`: "moved after a MAAP conflict (issue #202, 05 F05.12)";
  - `hdl/acmp/KL_acmp_talker.sv:308-310`: "moved at the first grant after a MAAP conflict once the ID has been declared".
- **Why it is residue:** the delta added the disable move, and 02 F02.10, 06 and the integrator guide already state it. These two comments are now incomplete. The fix is wording only.
- **Exact fix:**
  - top: "moved after a MAAP conflict, or at the return from a disable, once the ID has been declared (issue #202, 05 F05.12)";
  - talker: "moved at the first grant after a MAAP conflict, or after a disable, once the ID has been declared (issue #202)".

### RESIDUE-2: the PR body says the PR supersedes itself

- **Where:** the PR #204 body: "This PR supersedes #204 and answers its two reviews".
- **Exact fix:** "This round answers the two reviews of PR #204 (R710-1 and R709-1, both negative at `a8aa626e`)." Wording only.

### SUGGESTIONs (do not affect the verdict)

- **SUG-1 (Docs, 05:532-535).** The lap argument now counts "a disable and return of the source" as a move that is widely spaced in time. Unlike a MAAP claim, it has no protocol floor: S10 does one in a few hundred cycles. Each move still needs a declaration since the previous one, so a lap inside 20 s would need thousands of disable/probe cycles per second. Suggest stating the assumption (disables are quasi-static, at configuration-change rate) instead of "far beyond".
- **SUG-2 (Robustness, `KL_acmp_talker.sv:843-844`, `:893-898`).** Suppose a PCP change is pending when a moving grant declares the new ID. The PCP change is dispatched after the grant. It withdraws the just-declared new ID into a full `T-SRP-LEAVEALL2` backoff, although no earlier FirstValue was ever declared under that ID. This is conservative and conformant, but costs 20-30 s of availability in a rare interleaving. One option: clear the source's pending PCP bit when a moving grant declares.
- **SUG-3 (Docs, F05.12).** The `DA_OK --> DECLARING` arc could carry the PCP-hold guard ("no PCP change pending for a declared ID"), so that the figure matches the prose at 05:483-486.

## Prior public findings at this head

| Finding | State | Evidence |
|---|---|---|
| R709-1 F-1 MINOR: disable/re-enable re-declares the same ID with another DA | **RESOLVED** | `EVC_OFF` books the move (`KL_acmp_talker.sv:874`); covered by S10 and J7/K8; `disable_keeps_declared_id` is killed; S10 fails on the `a8aa626e` RTL. The fix makes the R709-1 S-1 window reachable (F1) |
| R709-1 F-2 MINOR: no check binds a slot's upper 48 bits | **RESOLVED** | S4 checks every slot's whole published ID; `publish_upper_from_slot0` is killed |
| R709-1 F-3 MINOR: 10 says New, the RTL issues Join! | **RESOLVED** | 10:428-435 now says Join!; MP8 checks that the first AttributeEvent is a JoinMt; `reopen_sends_new` is killed. The new Table 10-3 sentence at 10:433-434 falls under F1's docs outcome |
| R709-1 RESIDUE-1: "on the lane tree" | **RESOLVED** | no instance remains in the three READMEs |
| R709-1 S-1: fast-grant applicant window | **SUPERSEDED by F1** | now reachable through the disable move |
| R709-1 S-2: stable-since-reset assumption | addressed | 05:536-539 |
| R709-1 S-3: TCTX UID precedence in the parent patch | addressed | see R710-1 F02 |
| R709-1 S-4: GAP-04 wording | addressed | 00:141-142 presents the new Stream ID as this design's choice |
| R709-1 S-5: a parent conflict scenario | addressed | two parent legs with a real MAAP conflict, receipts rc 0; the no-wiring and round-2-precedence controls fail (6 and 2 checks) |
| R710-1 F01 MAJOR: a same-ID PCP change after a withdrawal bypasses the gap | **RESOLVED** | `KL_acmp_talker.sv:903-909` and `:526-528`; S7 to S9 grade R710-1's exact sequence on configured and moved IDs; I ran both new mutants and both are killed; S7 to S9 fail on the `a8aa626e` RTL |
| R710-1 F02 MAJOR: a parent TCTX UID overrides the published ID | **RESOLVED (by reading and published receipts)** | The handed-over patch (sha256 `c8a74c2a…`, verified against the manifest) stamps `stream_id_i[64*et_r +: 64]` whenever `SID_PP_P` = 1, which the datapath sets; only the standalone derivation reads a TCTX UID. The 8x8 leg names talker 1's TCTX UID explicitly and passes (52/0); the round-2-precedence control fails it (2). I did not re-run any parent leg |
| R710-1 R01 RESIDUE: bench labels in source comments | **RESOLVED** | every listed site has been rewritten (`sid_cases.hpp` headings; `sim_main.cpp:13` and `:213`; `acmp_mutants.py:419-422`; `pp_top_wrap.sv:268`; `pp_top/sim_main.cpp:9381`, `:9394` and `:9411`) |

## Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | 802.1Q-2018 §35.2.2.8 and §10.7/Table 10-3 (as quoted in the issue, the PR and 10) against the delta's `EVC_OFF`/`EVC_PCP`/`pcp_hold_w`/grant paths and the `KL_srp_talker_fsm` gate handling; REQ-ACMP-010, GAP-04 and the 08 row; the conflict path is unchanged since R709-1 | R709-2 | ebb1f0010bde76c38cc5270a6366ee9e3157ec54 |
| RTL | UNCLEAN (F1) | the whole `KL_acmp_talker.sv` delta (banner, `pcp_hold_w`, txn commit, `ev_eval`, `sid_state`); the `NO_DA` invariant traced; the SRP talker applicant open/close path; the MAAP face decisions; the LV and WINDOW probes | R709-2 | ebb1f0010bde76c38cc5270a6366ee9e3157ec54 |
| Robustness | UNCLEAN (F1) | disable and return with an immediate grant; a PCP change pending at a moving grant, inside a backoff, with a pending conflict, and while disabled; cursor-lap timing after the disable move (SUG-1, SUG-2) | R709-2 | ebb1f0010bde76c38cc5270a6366ee9e3157ec54 |
| Tests | UNCLEAN (F1, F2) | S7 to S10 in `sid_cases.hpp`, the J7/K8 edits and the MP8 JoinMt check; talker 1,520/1,520; the head bench on the `a8aa626e` RTL (18 FAIL); STREAM_ID 25/25 with goldens PASS; talker lint; the author's receipts (1,191 manifest-verified files: suites 1,030,552, campaigns, parent legs and controls) | R709-2 | ebb1f0010bde76c38cc5270a6366ee9e3157ec54 |
| Docs | UNCLEAN (F1, F2) | 00, 02, 05 (F05.12, `sec-05-sidmove`), 06, 08, 09 §8.13, 10 §6.1/F10.4, the integrator guide, the three test READMEs, the PR body and the HANDOFF; `make check` rc 0; a comment-rule scan of every added hdl/tb line (no new residue labels; RESIDUE-1 and RESIDUE-2 are wording) | R709-2 | ebb1f0010bde76c38cc5270a6366ee9e3157ec54 |

## Real limits

- **Not run by me:**
  - the full `tb/pp_top` suite (only its internal-MAAP golden ran, inside the campaign);
  - the full suite bank;
  - the campaigns other than STREAM_ID;
  - the portability elaboration;
  - any parent suite or leg.

  Those figures come from the author's manifest-verified receipts, at a pin whose consumed inputs I checked are identical to this head's.
- **F1's wire-level consequence:** shown at the SRP talker FSM unit and through the talker's strobe timing, not through `tb/pp_top`'s MAC stream.
- **Clause texts:** taken as quoted in the issue, the PR and the architecture documents. I did not retrieve the licensed standards independently.
- **Hosted checks at this head** (read at 15:56Z, inspection only):
  - docs-gates: success ×2;
  - portability: success ×2;
  - suites: in progress ×2. Nothing is inferred from these.
- **Manager source bank:** none exists at this head, and none is claimed.
- **Hardware:** physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Route F1: an RTL fix (a) or an owner ruling (b).
- Have F2 corrected in the PR text and the hand-over.
- Carry RESIDUE-1 and RESIDUE-2 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `ed211803`, live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`) with the builder and native banks, and link the receipts.
- Own hosted/act acceptance, including the `suites` contexts still running at 15:56Z.
- Land the parent wiring in the milan-fpga pin-adoption PR. The PR also records an out-of-scope maap-face index-width defect for power-of-two shapes above one.

## Packet

- **`scripts/`:**
  - `run_review.sh`: reproduces every execution above from an exact-head clone;
  - `run_lv_probe.sh` with `lv_probe_tail.cpp`: the SRP talker FSM probe for F1;
  - `run_talker_window_probe.sh`: the talker strobe-timing probe for F1;
  - `verify_evidence.py`: verifies the manifest and extracts the F2 figures.
- **`receipts/`:** run logs and rc files, the campaign `results.json`, the simulator identity, the evidence verification and the source-integrity record. Local paths are replaced by placeholders.
- **`independent-verdict.txt`.**
- **`MANIFEST.sha256`:** lists every published file.

R709-2 FINISHED
