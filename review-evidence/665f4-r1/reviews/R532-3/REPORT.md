[R532] NEGATIVE - exact head c1049de1970e93d2c36ace62891ee9d947cd3191

# R532-3: internal cleared-context review of PR #690 (issue #665, lane F4), round 3

- **Head and pins:** head `c1049de1970e93d2c36ace62891ee9d947cd3191`, tree `168564db27f588e2eaf34d2fa3ff54947eecd00d`, lwSRP gitlink `23d9a8173b07503a0ee6e8528f922fceab4e67f0`.
- **Delta under review:** `42a0371a..c1049de1`, one commit. I also read `db9aa8c9..c1049de1` (the FC r2 source base) for context. Against live dev `d51b373a`, the PR changes no file under `hdl/`, `tb/`, `syn/`, `constraints/` or `sw/mailbox/`.
- **Reading order:**
  1. AGENTS.md, CONTRIBUTING.md (sections 2-3 and 6), docs/README.md.
  2. The #665 body; the F4 assignment 6030279477; acceptance additions 6009661573 and 6030870481; assignments 6033558691 and 6035166787; STOP 6036003609 and ruling 6036016117.
  3. docs/design/MAILBOX_SPLIT.md (event coalescing) and `sw/mailbox/mailbox.yaml` (LINK register and record).
  4. The diff and history.
  5. The author packet `review-evidence/665f4-r1/author-r3/` at evidence tip `cd267b52`, and the exact-head hosted check runs.
- **Independence:** the verdict, findings and ledger below were fixed before any prior review report was opened (`VERDICT-BEFORE-PRIORS.md`, sha256 `a4c68f01...`; see `receipts/environment.txt`). The prior-finding dispositions come after the ledger. I did not read the other current-round report.

## Findings

### R532-3-F1 MINOR: Tests. The round-3 shared-Applicant inheritance is not discriminated by any lane test

- **Where:** `sw/firmware/ctrl/srp/srp_mbx.c:313-325`. This is the block added by round 3 so a replacement or new binding carries the shared Applicant and committed VID. `declared` is inherited at `:318-320`, keyed by StreamID, from every bound slot.
- **Authority:** the R533-2-F1 acceptance (assignment 6035166787 item 3) says "no stale Listener Ready may remain after a shared rebind ... Add regressions and planted defects". AGENTS.md section 6, Tests, says "Each new test can fail for the defect it claims to detect" and asks for "Positive, negative, and boundary behavior". srp/README.md:58-64 states the shared-declaration rule.
- **Evidence:** I ran reviewer plants against the WHOLE `srp_mbx.cpp` suite (50 cases) at IF=1 and IF=2 (`probe_srp.py --reviewer`, `receipts/reviewer-plants.json`). Two plants at the root of this block survive every case:
  - **RP3:** `replacement.declared |= r->declared;` becomes `if (r == s) { ... }`, so a slot inherits only from itself. This is round 2's behaviour for a binding that joins an already-declared StreamID from another slot.
  - **RP10:** inheritance is not keyed by StreamID (`if (true)`).
- **Both plants are observable wire defects.** The reviewer probes `srp_probe.cpp` (`probe_scenarios.py`) pass at the head at IF=1 and IF=2 and fail exactly on their plants (`receipts/scenario-probes.json`, `receipts/logs/scenario-*.log`):
  - Under RP3, `ProbeJoiningSharedBindingCarriesApplicantWhenOriginalLeaves` fails. The sequence: a Ready binding, then an ineligible binding joins the same StreamID in the other slot, then the Ready binding leaves. The wire shows Listener Ready renewed (event 3) with no Lv. This is the stale-Ready outcome R533-2-F1 forbids, reached through a binding that joins rather than a replacement in place.
  - Under RP10, `ProbeRebindToRegisteredStreamDeclaresReadyBesideAnotherReadyStream` fails. A StreamID whose Talker is still registered is rebound while another StreamID is Ready, and no Ready is ever declared for it.
- **Why the lane tests miss them:**
  - The lane plants `rebind-loses-shared-applicant` and `consecutive-rebind-loses-applicant` delete the whole line, and they are caught. But every lane case either replaces in the same slot or keeps a matching Talker, so the cross-slot join-then-leave order and the StreamID keying are never exercised.
  - The second half of `ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation` (`srp_mbx.cpp:775`) builds the join, but only in its desired-Ready branch, where a re-declare hides a lost cache.
- **Impact:** a regression to round-2 bookkeeping for a binding that joins, or a mis-keyed inheritance, would pass the complete gate and both campaigns. The production code at this head is correct; only the evidence is incomplete.
- **Required outcome:** named lane tests fail for both defect classes:
  - stale Ready after a joining ineligible binding outlives the eligible one, in both slot orders;
  - no inheritance across StreamIDs.
  Each needs a matching `srp_mutants.py` entry with its observable.
- **Verification:** plants RP3 and RP10 are caught by name at IF=2 in the lane campaign. The head passes at IF=1 and IF=2.

### R532-3-F2 MINOR: Tests, Docs. The Domain-VID guard on the final unbind is untested, and the README rule omits it

- **Where:** `sw/firmware/ctrl/srp/srp_mbx.c:334`, `if (old.vid != i->domain.vid && !has_sink(i,&old,false))`, and `sw/firmware/ctrl/srp/README.md:65`, "The final binding releases its VID regardless of prior eligibility."
- **Authority:**
  - Round 3 (R532-2-F3) removed the per-sink `vlan_requested` condition. The Domain comparison is now the only thing that keeps the last unbind on the Domain's VID from withdrawing the SR class VLAN.
  - Startup declares MVRP membership in VID 2 for the Domain and Talkers (srp/README.md:86; assignment 6030279477 Part B.4, "MVRP for the SR class VID (VID 2)"). Talker licences depend on that membership (Milan v1.2 4.3.2).
  - AGENTS.md section 6, Tests, asks for boundary behaviour; Docs says "Changed contracts are reflected in authoritative docs".
- **Evidence:**
  - Plant RP5 drops `old.vid != i->domain.vid &&`. It survives all 50 cases at IF=1 and IF=2 (`receipts/reviewer-plants.json`, `receipts/logs/plant-RP5-*.log`).
  - Probe `ProbeUnbindingTheLastDomainVidBindingKeepsSrClassVlan` binds one sink on VID 2, reaches Ready and unbinds it. It passes at the head and fails under RP5 at both interface counts: the wire carries an MVRP Lv for VID 2 (`receipts/logs/scenario-RP5-*.log`).
  - The README sentence states the release with no Domain-VID exception, so it describes the RP5 behaviour as the contract.
- **Impact:**
  - A regression that withdraws the SR class VLAN whenever a listener on VID 2 unbinds would pass the gate. The bridge would drop the port from VLAN 2 while the Talker licences stay granted.
  - An integrator (F3) reading the README is told the opposite of what the code does.
- **Required outcome:** a named lane test fails when the final unbind on the current Domain VID withdraws that VID, with its `srp_mutants.py` plant. srp/README.md:65 states the exception, for example "The final binding releases its VID, unless it is the current Domain VID, regardless of prior eligibility."
- **Verification:** RP5 is caught by name at IF=2. The README sentence matches `srp_mbx.c:334`.

### RESIDUE

- **R532-3-R1:** the PR #690 body Status and Round 3 sections are stale. They say "STOP: round-3 validation incomplete", "the compiler-absent entry remains incomplete" and "Full local or hosted docs-context success is not claimed". Ruling 6036016117 accepted the head as REVIEW READY, and the manager's run of that docs entry returned rc 0 (PR comment 6036186046, GATE 1b PASS). This is wording only; it changes no code, test or gate result. Exact fix:
  - Status: "REVIEW READY under ruling 6036016117. The compiler-absent docs entry passed in the manager's run (PR comment 6036186046); the builder bank remains with the candidate bank."
  - Round 3: replace "76 pass and the compiler-absent entry remains incomplete" with "76 pass in the lane; the compiler-absent entry passed in the manager's run (6036186046)".

### Observations (not findings)

- **Equivalent plants:** RP6 (attach assumes up) and RP7 (a poll-observed edge does not set `link_seen`) survive. I judge both equivalent:
  - RP6 self-corrects at the first poll, before any transmission, because the poll's level reconcile precedes `mrp_transmit`.
  - RP7 changes only whether a later stale UP record causes one extra conservative reset. Participants created at the down-edge reset never transmit or register while down (`srp_mbx.c:361,659`).
- **Double reset:** when the level change is seen by poll before its delayed record, a second reset follows the record. This is the documented conservative "repeated UP recreates state" path (srp/README.md:112), and state converges at the next pass.

## Assigned focus items, verified at their root

| Item | Result at `c1049de1` | Evidence |
|---|---|---|
| R532-2-F1: link learned from the current level at (re)attach, no interface left dead | RESOLVED | `srp_mbx.c:684-686` samples `mbx_link_up` at attach. `:601-606` reconciles both edges from the level every pass with reset and receive fence. LINK is "Current link level per interface" (`mailbox.yaml:100-105`). Lane tests `ReattachLearnsAnAlreadyUpLinkWithoutAnotherRecord` (re-init with level up and no record) and `CancelledLinkRecordRecoversFromLevelAndFencesOldReceive` (held DOWN cancelled; old RX fenced; peer interface unaffected) pass at IF=1/2. Lane plants `attach-ignores-current-link` and `cancelled-link-never-recovers` are caught. My RP8 (up edge without reset) and RP12 (down edge not reconciled) are caught. srp/README.md:49-51,111 state the rule. |
| R532-2-F2: `third_party/lwSRP` documented where the docs gates require | RESOLVED | THIRD_PARTY.md row (Apache-2.0, LICENSE/NOTICE), SUBMODULES.md pin row, fetch, licence and evidence rows, regenerated submodule diagram, `check_submodule_docs.py` edge label. In a submodule-free clone at the head, all four "Verified submodule documentation gate" commands rc 0, as do `docs_check.py`, `check_doc_style.py`, `check_diagram_pngs.py`, `DOC_MAP.gen.py --check`, `check_solution_docs.py` and `gen_module_matrix.py --check` (`receipts/docs-gates.summary`). Pinned lwSRP has `LICENSE`, `NOTICE` and SPDX in 55/55 tracked files. The compiler-absent entry passed in the manager's run (6036186046). Hosted `docs-check` was still in progress when inspected (manager duty). |
| R533-2-F1: replacing a shared binding keeps the shared declaration, no stale Ready | RESOLVED in code. The test remainder is R532-3-F1. | `srp_mbx.c:305-337` builds the replacement with inherited `declared`/`vlan_*`, installs it, then judges withdrawal over the complete new set. The R533-2-F1 sequence (VID 2, destinations ...09/...0A, rebind sink 0 to ...0A) replayed as `ProbeR533OverlappingRebindWithdrawsSharedReady` passes at IF=1/2: Lv only, no renewal. Lane `SharedRebindKeepsOnlyTheRemainingEligibleRequest` (both slots, destination/VID change, retained and lost match) and `ConsecutiveSharedReplacementsKeepApplicantStateUntilReconciliation` pass. Their plants are caught, and so are my RP1/RP2 (VID-flag inheritance dropped), RP4 (judging without the replacement) and RP9 (cross-VID inheritance). |
| R532-2-F3: shared VID withdrawn when its last binding leaves, including a never-eligible last binding | RESOLVED. The Domain-VID boundary is R532-3-F2. | `srp_mbx.c:334` withdraws on the last binding regardless of `vlan_requested`. `LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder` asserts the never-requested setup (`ASSERT_FALSE(...vlan_requested)`) and both unbind orders on every interface. Its plant `last-ineligible-vid-leaks` and my RP11 (withdraw while still bound) are caught. |
| R532-2-F4: the three discriminable plants killed | RESOLVED | My L1, L3 and S2 shapes are now lane plants `reset-keeps-owed-domain`, `reset-keeps-sink-vlan` and `shared-ready-uses-first-vlan`. Each is caught by its named test (`RefusedPeerDomainDoesNotSurviveLinkRestart`, `SinkVlanRedeclaredBeforeReadyAfterLinkRestart`, `SharedReadyWaitsForTheMatchingBindingsOwnVlan`) in my replay (`receipts/author-plants-srp_mbx.json`). |
| R533-2-F2: note 4/5 lwSRP tests on the published `f4-applicant-notes` (495520f) | RESOLVED | `git ls-remote` shows `refs/heads/f4-applicant-notes` at `495520f5`, a child of the pin. `git diff 23d9a817 495520f5` touches only README.md, `tests/check_reversals.py` and `tests/unit/integration_test.c`, so production sources equal the pin. I built cgreen in scratch and ran `tests/check_reversals.py` at `495520f5`: 40 reversals, 0 failures. `point-to-point-condition` fails both `applicant_receive_conditions_follow_link_mode` and `pending_applicant_joinin_obeys_note_four`; `pending-point-to-point-condition` fails the latter; `shared-in-condition` fails the former. The unit binary gives 2675 passes, matching the topic README. behave: 3 scenarios, 10 steps pass. The pin moving later to lwSRP main is not a finding. |

## Gates and probes run by this reviewer at the exact head

| Command / probe | Result | Receipt |
|---|---|---|
| `srp_mbx.cpp` unmodified, IF=1 and IF=2 | 50 + 50 pass | `receipts/baseline-srp_mbx.json` |
| Lane SRP plants in `srp_mbx.cpp` (54), replayed with the lane's `caught()` predicate | 54/54 caught | `receipts/author-plants-srp_mbx.json` |
| Lane SRP plants in the debug, latency, walk and shape suites (13), through the lane's `campaign()` | 13/13 caught | `receipts/author-plants-other-suites.out` |
| Reviewer plants RP1-RP12 against the whole suite, IF=1/2 | 7 caught; RP3, RP5, RP10 escape (F1, F2); RP6, RP7 equivalent | `receipts/reviewer-plants.json`, `receipts/logs/plant-*.log` |
| Reviewer scenario probes (4), head and RP3/RP5/RP10, IF=1/2 | head 4/4 pass; each plant fails exactly its probe | `receipts/scenario-probes.json` |
| `test_ctrl_firmware.py --jobs 4` (host gate, no `--self-test`) | rc 0; 28 arms incl. RV32 freestanding, lwsrp, SRP adapter/debug/latency/walk at IF=1/2, 10 shape arms | `receipts/fw-host-gate.out` |
| `fw_coverage.py --check --jobs 4` | rc 0; 15 files 100 %; `srp_mbx.c` 441/441 lines, 410/410 branches | `receipts/fw-coverage-check.out` |
| `make -C tb/verilator/mbx -j16` with pinned Verilator 5.050 (identity in `receipts/environment.txt`) | rc 0; mbx mutants 5/5 caught | `receipts/mailbox-suite.out` |
| `gen_mailbox.py --check` | 0 findings, rc 0 | `receipts/gen-mailbox-check.out` |
| Docs gates in a submodule-free clone (11 commands) | 10 rc 0. `check_em_dash.py` could not judge locally (its pinned renderer dependency is absent: rc 2, not a verdict); the author receipt and a direct scan show no added U+2014 in `d51b373a..HEAD` | `receipts/docs-gates.summary`, `receipts/logs/doc_*.log` |
| lwSRP `check_reversals.py` at `495520f5` / unit / behave | 40/40 killed; 2675 passes; 3 scenarios pass | `receipts/lwsrp-*.out`, `receipts/logs/lwsrp-*.log` |
| Final integrity of this clone | parent 1169 blobs plus PP 558, gPTP 104, lwSRP 55 and verilog-axis 214 blobs; modes, stage-0 index, no hidden flags, gitlinks equal pins, no untracked or ignored files | `receipts/final-integrity.out` |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c:270-340,546-606,676-697` against srp/README.md:41-118, Milan v1.2 4.3.2 / 5.5.2.7 and IEEE 802.1Q-2018 35.1.2.2 as cited by the assignment; assignment 6035166787 items 1-6; lwSRP `495520f5` diff and reversal logs; reviewer probes (head passes all four, including the R533-2-F1 replay); the manager's compiler-absent result 6036186046 | R532-3 | `c1049de1970e93d2c36ace62891ee9d947cd3191` |
| RTL | CLEAN | No hdl/tb/syn/constraints/sw/mailbox change vs dev `d51b373a`. Firmware use of the contract: `mbx.c:281-285` (`mbx_link_up` reads LINK) against `mailbox.yaml:100-105` and MAILBOX_SPLIT.md:125-143 (coalesced records, level at posting); loop order `ctrl_loop.c:145-153` (events, then RX, then polls) and `rx_ready` (`srp_mbx.c:342-347`); `make -C tb/verilator/mbx` and `gen_mailbox.py --check` | R532-3 | `c1049de1970e93d2c36ace62891ee9d947cd3191` |
| Robustness | CLEAN | Re-init with level up, held-then-cancelled DOWN, stale DOWN/UP record after a level-observed edge, double reset, attach before open; bind with owed output, same-slot and cross-slot replacement, consecutive replacements before service, never-eligible last binding; plants RP1-RP12 and their dispositions (`receipts/reviewer-plants.json`) | R532-3 | `c1049de1970e93d2c36ace62891ee9d947cd3191` |
| Tests | UNCLEAN (R532-3-F1, R532-3-F2) | `srp_mbx.cpp:681-934` (9 new cases), `srp_mutants.py:460-501` (9 new and 4 retargeted plants), all 67 lane plants replayed, 12 reviewer plants, 4 reviewer probes, coverage ratchet, host firmware gate, lwSRP topic tests and reversals | R532-3 | `c1049de1970e93d2c36ace62891ee9d947cd3191` |
| Docs | UNCLEAN (R532-3-F2) | srp/README.md:41-66,103-118,163-174; ctrl/README.md:135-140; THIRD_PARTY.md; docs/reference/SUBMODULES.md; docs/diagrams/submodule_boundaries.{gen.py,svg,drawio,png} and PNG_MANIFEST.json; PR #690 body (R532-3-R1); author-r3 packet; docs gates rerun | R532-3 | `c1049de1970e93d2c36ace62891ee9d947cd3191` |

## Prior public review findings at this head

Read after the verdict and ledger above were fixed. Sources: R532-2 (PR comment 6035102894) and R533-2 (PR comment 6035155719). For R532-1 and R533-1, I rely on their dispositions in round 2 and recheck only the open SUGGESTION.

| Prior finding | Disposition at `c1049de1` | Evidence |
|---|---|---|
| R532-2-F1 MAJOR (link only from records) | RESOLVED | See focus table. My round-2 probes P1 and P2 correspond to the lane's `ReattachLearns...` and `CancelledLinkRecord...`, which pass. Their plants are caught. |
| R532-2-F2 MAJOR (lwSRP undocumented; docs-check red) | RESOLVED locally; hosted context pending | The four submodule commands rc 0 in a submodule-free clone, and the manager's compiler-absent run rc 0. Hosted `docs-check` was in progress at inspection. |
| R532-2-F3 MINOR (never-eligible last binding keeps VID) | RESOLVED | See focus table. The author notes that my round-2 P3 setup assertion (the newly bound flag stays false) conflicts with deliberate inheritance. I accept that: the lane test keeps a never-requested setup by binding the waiting sink first, and it checks the wire outcome I required, in both orders. The new boundary gap is R532-3-F2. |
| R532-2-F4 MINOR (L1, L3, S2 escapes) | RESOLVED | See focus table. |
| R532-2-R1 RESIDUE (ctrl README stale fetch text) | RESOLVED | ctrl/README.md:139-140 now says the pin is published on `mark2-port` (PR #12) and that a hosted checkout needs read access. Verified: `23d9a817` is an ancestor of remote `mark2-port`. |
| R532-2-R2 RESIDUE (PR body Status stale) | RETAINED in new form as R532-3-R1 | The round-3 body repeats the pattern ("STOP ... incomplete") after ruling 6036016117. |
| R532-2-S1 SUGGESTION (no parent test that MVRP keeps Table 10-4 under the Milan option) | RESOLVED | `MilanMsrpOptionLeavesMvrpOnTheOriginalLeaveDeadline` plus plant `milan-rapid-leave-leaks-to-mvrp`, caught. |
| R533-2-F1 MAJOR (shared rebind loses declaration; stale Ready) | RESOLVED (code and its reproduction). The residual test gap is R532-3-F1. | See focus table. |
| R533-2-F2 MINOR (note 4/5 topic not public) | RESOLVED | Topic published at `495520f5`. Tests named, production sources equal the pin, and the reversals were executed by this reviewer. |
| R532-1-S2 SUGGESTION (generic LV/rJoinIn extra indication) | RETAINED as SUGGESTION | A dependency matter for lwSRP PR #12, not re-examined. It does not dirty a lens. |

## Real limits

- **Not run, by assignment:** the full parent, processor, gPTP, Yosys and builder banks; `test_ctrl_firmware.py --self-test` (its 100 control plants were not replayed by me; the 67 SRP plants were); Docker/act; host `act_ci`; hardware. Physical calibration is NOT RUN, and field skips are not hardware proof.
- **Linked size:** the composition sizes (53,968 / 65,216 / 68,656 / 94,656 bytes) were not re-linked. The runtime archives are externally provisioned. Round 3 changes `srp_mbx.c` by +39/-14 lines, which is consistent with the reported +64 to +112 byte span changes from round 2.
- **Host model:** all probes run on the host mailbox model. "Cancelled level change" is modelled by changing the LINK level without posting a record, as the lane's tests do.
- **`check_em_dash.py`:** could not judge here because its pinned renderer dependency is absent. I replaced it with a direct scan for added U+2014 and found none.
- **Hosted contexts at `c1049de1`** (read-only inspection at 2026-10-07T10:52Z; `receipts/hosted-checkruns-c1049de1-refresh.json`):
  - Executed and failed: `firmware-unit` fails at its submodule fetch because the private lwSRP clone is refused ("could not read Username", `receipts/hosted-firmware-unit.log`), and `rtl-fast` fails as the aggregate.
  - Executed and passed: `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, Yosys shards 0-3 and Verilator shard 3.
  - In progress: `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4.
  - Skipped (not execution): `Physical gPTP (nightly and manual)`.
- **Source vs candidate:** this verdict is on source. The current-dev candidate (source base `db9aa8c9`, live dev `d51b373a`) is built by the manager at the merge turn.

## Pending manager duties

- Carry R532-3-F1 and R532-3-F2 to the executor. Carry R532-3-R1 to the residue checklist.
- Make lwSRP fetchable for hosted CI (it gates `firmware-unit`/`rtl-fast`), merge lwSRP PR #12 and the `f4-applicant-notes` follow-up, and move the pin in the later delta. Carry R532-1-S2 to PR #12.
- Record the final hosted `docs-check`, `elaborate` and Verilator shard results for this head, or the next one.
- Run the candidate builder bank (including `test_baremetal_profile_contract`), the full candidate gates on current dev, and post-merge containment. Merge requires explicit maintainer authorisation.

R532-3 FINISHED
