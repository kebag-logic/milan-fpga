[R377] POSITIVE - exact head 66451539ee49262d97403bc6b010202bb773d272

# R377-3: external independent re-review of processor PR #129 / issue #128

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `66451539ee49262d97403bc6b010202bb773d272`, tree `8007bb9891167941cf8db57da813e86dfb1f2f56`. I verified both in the detached review clone.
- Delta under review:
  - round-3 commit `8eefb7b9` ("Pin ACMP event fairness and absent-allocator retry pacing") on `cc7c911e`;
  - manager merge `66451539` of processor main `97bd3786` (PR #130, SRP LeaveAll fix).
  - I also read the cumulative diff `97bd3786..66451539`: 12 files, +1264/-83. The only RTL file is `hdl/acmp/KL_acmp_talker.sv`.
- Round-3 assignment: issue #128 comment 5862928771. Review start: PR #129 comment 5864924170.

## Verdict summary

**POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open. Two suggestions are recorded; they do not affect the verdict.

Every round-3 item is met at this head:

1. **R377-2 F1 is resolved.**
   - New regression R16 (`tb/acmp_talker/retry_cases.hpp:394-432`) holds a GET_TX_STATE for another source continuously valid. It raises one conflict, PCP, freshness or listener event, and samples `declaring_o` (a flop mirror written only by walker actions) before the command stream stops.
   - The four `txn_eligible_w` mutants are in the campaign table (`retry_mutants.py:218-233`). Each fails exactly one named R16 assertion, for example `R16 conflict event served under continuous commands (gates 0x02 want 0x00)`.
   - My own probe P7 also kills all four at this head.
   - The full campaign kills 62 mutants, keeps 7 equivalence controls and 1 performance control, and witnesses 59/59 assertion sites. Baseline and restore both pass 1342/1342 at rc 0.
2. **R376-2 S1 is resolved.** R17 (`retry_cases.hpp:434-451`) counts allocation *offers* with ready tied low. `wait_only_on_accept` is in the table and fails `R17 absent same-round probes cannot re-offer`.
3. **R376-2 S2 and R377-2 S1 are resolved.** Each of the four is recorded in the campaign table, and my lockstep agrees with every classification:

   | Term | Recorded as | Lockstep, 64 seeds x 3M cycles |
   |---|---|---|
   | m29 `sticky_kill_ignores_accept` | equivalent | 0/64 |
   | EVC_INIT maap-busy else branch (`init_busy_else_removed`) | equivalent | 0/64 |
   | `pe_off_r` term of `maap_kill_w` (`kill_w_no_off`) | equivalent | 0/64 |
   | m28 `init_ready_no_en` | performance-only, explicitly not an equivalence claim | diverges 16/16, as a cycle-level change must |

   - The known-defect control diverges in 49 of 64 seeds.
   - The EVC_REL comment is updated (`KL_acmp_talker.sv:856-858`).
   - The round-3 RTL edit is comment-only. With comments stripped, the talker hashes the same at `cc7c911e`, `8eefb7b9` and the head. I also derived each equivalence by hand (see the lenses below).
4. **R376-2 S3 is resolved.** 05 §6bis `:416-418` states the conflict lifetime restart, and it matches the RTL.
5. **No interface change.**
   - The talker's comment-stripped parameter/port header is identical to base `97bd3786`.
   - The `protocol_processor_top.sv`, `pp_pkg.sv`, `srp_pkg.sv` and `KL_pp_maap.sv` blobs are unchanged.
6. **The composition with main `97bd3786` is sound.**
   - The merge is textually clean. `diff(16be6768, 8eefb7b9)` equals `diff(97bd3786, 66451539)` byte for byte, and the main side likewise; the two sides share no file.
   - All ACMP, SRP and MAAP suites and `pp_top` pass at the merge head.
   - Both mutation campaigns pass at rc 0: `retry_mutants.py` as above, and `make -C tb/srp_top mutants` 64/64 with 49/49 assertion coverage.
   - The #128 acceptance holds at this head. The parent first-probe harness, with the real parent shim, returns status 0 with DA `91e0f0006818` and no probe-triggered ALLOC.

## Reconstruction (in order)

1. **Rules.**
   - The processor has no `AGENTS.md` or `CONTRIBUTING.md`.
   - I read `README.md` and `docs/README.md`. Single-source rules: timing only in F08.1, IDs cited rather than values.
2. **Issue #128.** I read the body and the comments 5861093499 (scope decisions), 5861952375 (round 2, option a: paced rounds) and 5862928771 (round-3 assignment). Frozen scope:
   - bounded, fair reattempts with honest failure;
   - no retry storm and no command starvation;
   - conflict/PCP backoff unchanged;
   - no interface change;
   - every new check pinned by a killed mutant.
3. **Authorities.**
   - Processor 05 §6bis (F05.12 and the allocation-recovery text), 02 §4.2 and 08 F08.1 `T-ACMP-DA-RETRY`.
   - Parent `hdl/milan/KL_pp_maap_shim.sv`: fetched at `931f396e`, and byte-identical at live dev `54ce8773`.
   - Parent `scripts/measure_test_evidence.py` at `54ce8773`.
   - Hashes are in `receipts/01-inputs.txt`.
4. **Diff and history.** Cumulative diff and round-3 delta, as above. The graph is `9476898b` → `cc7c911e` → `8eefb7b9`, then the merge with `97bd3786`.
5. **Public evidence.**
   - `kebag-logic/milan-fpga@b367df5d:review-evidence/pp128-r1` is the round-1 author packet (head `9476898b`). The `pp128-review-evidence` branch tip `3b613880` has no round-3 author packet.
   - Manager comment 5865084506 (banks at `66451539`):
     - donor bank 9/9;
     - parent consumer gates 9/11, where the only failures are the declared `[H]`/`[I]` and the pending reader-disposition row.
   - Hosted check runs at the exact head.
6. **Prior public findings.**
   - I wrote `receipts/02-independent-notes-before-prior-reviews.txt` after my own pass over the diff. Only then did I read the R377-2 text (my own packet, read-only) and R376-2's suggestions.
   - The R376-3 report was not posted when I checked, and I did not read it.

## Findings

No MINOR, MAJOR or BLOCKER finding.

### Suggestions (do not affect the verdict)

- **S1 (Tests): the retry campaign is not in hosted CI.**
  - **Where:** `.github/workflows/hdl.yml:55-58`.
  - **Observation:** The merge from main brought in a CI step that runs the SRP LeaveAll campaign (`make -C tb/srp_top mutants`). `tb/acmp_talker/retry_mutants.py` runs only by hand, and a later RTL edit could let a killed row survive without any gate noticing.
  - **Status:** #128 does not require CI exposure, and the campaign passes today (`receipts/20-*`).
  - **Suggestion:** add a CI step or a make target for it, or state why it stays manual.
- **S2 (Tests, Docs): two comments are slightly stale.**
  - The `EQUIVALENT_MUTATIONS` header at `retry_mutants.py:259-261` still says the controls are "single terms [that] overlap by construction", with whole-cause mutants tested separately. It now also lists an unreachable branch (`init_busy_else_removed`) and a term that is false on the accept edge (`sticky_kill_ignores_accept`).
  - The EVC_INIT branch comment `KL_acmp_talker.sv:871` ("maap busy: keep the request pending") does not say that the branch is unreachable. The EVC_REL comment at `:857-858` does.
  - **Suggestion:** reword both the next time the file is touched.

## Resolution of prior public findings at this head

| Prior item | Disposition at 66451539 | Evidence |
|---|---|---|
| R377-2 F1 (MINOR, Tests): CONFLICT/PCP/TIMER/LISTENER `txn_eligible_w` terms unpinned | **RESOLVED** | R16 `retry_cases.hpp:394-432`; mutants `retry_mutants.py:218-233`. Committed campaign: each killed, 1 named R16 failure (`receipts/20-retry-campaign/elig_drop_*.txt`). Reviewer suite: same (`receipts/40-reviewer-suite`). P7: head 1363/1363, each mutant 2 failures (R16 + P7) (`receipts/43-probe-p7`). Every new site witnessed (`coverage.txt`: `:401-449`, 59/59); baseline/restored rc 0. |
| R377-2 S1 (a) EVC_INIT busy else; (b) `pe_off_r` in `maap_kill_w` | **RESOLVED (stated)** | `init_busy_else_removed` and `kill_w_no_off` in `EQUIVALENT_MUTATIONS`; EVC_REL comment `:856-858` updated. Lockstep 0/64 each (`receipts/42-lockstep-64`). |
| R377-2 S2 (parent `[I]` wording) | **Out of scope here** per 5862928771; retained for the parent pin-adoption lane | Pending manager duty below |
| R376-2 S1: absent-allocator demand pacing | **RESOLVED** | R17 `:434-451`; `wait_only_on_accept` killed by `R17 absent same-round probes cannot re-offer` (4 failures); reviewer lockstep diverges 16/16 |
| R376-2 S2: m29, m28 | **RESOLVED (stated)** | m29 = `sticky_kill_ignores_accept`, equivalent, 0/64. m28 = `init_ready_no_en`, `PERFORMANCE_MUTATIONS`, explicitly "not an equivalence claim"; it must still pass the suite (rc 0 in my rerun), and it diverges in lockstep 16/16 as stated. |
| R376-2 S3: conflict lifetime restart | **RESOLVED** | 05 §6bis `:416-418`. It is accurate: `set_conflict_w` clears the pacing bit (`KL_acmp_talker.sv:898`); only the `DA_OK` arm of EVC_CONFLICT sets INIT (`:783-784`); an obsolete grant is released, never installed (`:733-736`). |
| Round-1 findings (R377-1 F1-F4, R376-1 F1-F4), resolved in round 2 | **Remain resolved** | Declaration order: 0 forward references (`receipts/32`). Wall clock: parent `uses_wall_clock` False on all three changed test files (`receipts/33`). Round-1 probes P1-P6: 1389/1389 (`receipts/44`). Parent first probe: status 0 (`receipts/50`). |

## Five lenses

- **Conformance.**
  - #128's acceptance is reproduced at this head with the real parent shim and the published oracle (`receipts/50`).
  - Honest status 3 and bounded offers with an absent allocator: R17, R2 and R3.
  - Backoff is unchanged: R6, with `half_backoff` and `backoff_bypass` killed.
  - No interface change (`receipts/30`).
  - The manager's consumer receipt 5865084506 shows only the declared parent-lane items failing.
- **RTL.** The round-3 edit is comment-only (`receipts/30`). My own equivalence arguments:
  - **EVC_INIT busy fallback.** It is dispatched only with `maap_avail_w`. Before `S_EV_ACT`:
    - busy can rise only on an accept, which happens only in `S_EV_MAAP`;
    - `gp_valid` can rise only on a live response, which needs busy;
    - stale credit can rise only on a response timeout, which needs busy.
    So availability cannot fall, and the branch is unreachable.
  - **`pe_off_r` in `maap_kill_w`.** It is set only on the cycle after `!cfg_src_en_i`. That cycle's `!en` term is caught by one of three paths:
    - the sticky latch, if busy or a grant is held;
    - the accept expression, if the accept falls on that cycle;
    - otherwise the later accept expression, which also reads `pe_off_r`. EVC_OFF cannot dispatch while the walker is in `S_EV_MAAP`.
  - **m29.** Every path into `S_EV_MAAP` requires availability, so busy and `gp_valid` are both 0 on the accept edge.

  Lockstep agrees (0/64 each). Talker lint rc 0; no forward references.
- **Robustness.** Checked under sustained command traffic:
  - every event class is served (R16, P7);
  - absent-allocator offers stay paced under repeated probes (R17);
  - my full reviewer set of 26 single edits was run against the suite and in lockstep: 16 seeds x 3M cycles with random resets, wrap, disable pulses and allocator stalls (`receipts/40`, `receipts/41`).

  The edits that survive the suite fall into two groups:
  - the stated equivalents, plus the accept-side single terms already covered by `accept_kill_zero`;
  - edits I judged benign in round 2 (`turn_not_on_grant`, `tick_sets_all`, `turn_clear_on_dispatch`, `t0_reset_zero`) and the stated performance control.

  Round-1 probes pass.
- **Tests.**
  - The committed campaign reproduces exactly: 62/7/1, 59/59 sites, rc 0.
  - The README's 70-row table matches my rerun row for row, in failure count and in the named assertion (`receipts/22`).
  - The README's check counts are right: 1342 in total, 503 in section R.
  - The SRP campaign passes: 64/64, 49/49.
  - S1 and S2 are suggestions only.
- **Docs.**
  - The 05 §6bis sentence is accurate.
  - The talker README's R16/R17 rows, campaign table and equivalence/performance text are accurate.
  - The PR body's round-3 section matches this head. Its "Validation at `8eefb7b9`" counts are the author's pre-merge figures; the merge head is covered by the manager's receipt.
  - `make check` rc 0 (41 mermaid, 18 wavedrom, 925 links, matrix, 24 parameters); `gen_matrix --check` 92 rows, 0 untested.

## Reviewer-owned evidence (pinned simulator 5.050)

| Receipt | Result |
|---|---|
| `receipts/00-tool-identity.txt` | The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` is ABSENT. I used a byte-identical copy of `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` (sha256 `905795b9…`). It reports `Verilator 5.050 2026-07-01 rev v5.050`, and its underlying binaries are identical to the ones I used in R377-2. |
| `receipts/10-suites-head/` | At the merge head: `acmp_talker` 1342, `acmp_listener` 2544, `acmp_nvm` 349, `srp_admission` 991231, `srp_decoder` 190, `srp_encoder` 562, `srp_stream_fsms` 1215, `srp_top` 1987, `maap` 75 and `pp_top` 7751. All pass with rc 0. |
| `receipts/20-retry-campaign*`, `receipts/22-*` | Committed `retry_mutants.py`: 62 killed, 7 equivalent, 1 performance, 59/59 sites, baseline/restored 1342 at rc 0. The README table matches 70/70 rows. |
| `receipts/21-srp-campaign*` | `make -C tb/srp_top mutants`: 7 controls pass, 56 arms killed by their named assertions, coverage 49/49 (7 + 56 + 1 coverage check = `64 checks: 64 PASS`), rc 0 |
| `receipts/30-rtl-identity-interface.txt` | comment-only RTL delta; header and interface blobs identical to base |
| `receipts/31-lint-docs.txt`, `receipts/32-forward-ref.txt` | talker lint rc 0; `make check` rc 0; matrix rc 0; 0 forward references |
| `receipts/33-parent-evidence-classifier.txt` | Parent classifier at `54ce8773`: no wall-clock use in `retry_mutants.py`, `retry_cases.hpp` or `sim_main.cpp`. The reader-disposition row is not yet in the parent table (parent lane). |
| `receipts/40-reviewer-suite/`, `receipts/41-lockstep/`, `receipts/42-lockstep-64/` | 26 reviewer single edits against the suite; lockstep at 16 seeds for all of them, and at 64 seeds for the three new equivalents, the identity and the control |
| `receipts/43-probe-p7/`, `receipts/44-r1-probes/` | My round-2 probe P7 and my round-1 probes P1-P6 at this head |
| `receipts/50-parent-first-probe-66451539.txt` | Real parent shim `965fbee0…` and published oracle `9a195388…`. First probe status 0, DA `91e0f0006818`, no probe-triggered ALLOC; harness rc 0. |
| `receipts/80-hosted-checks.txt` | Six hosted jobs at the exact head (push and pull_request runs of `hdl`): `docs-gates`, `suites` and `portability`, each twice, all completed with success. The only skipped step is the cached Verilator build; the SRP campaign step executed. The legacy combined status has 0 contexts. |
| `receipts/90-clone-integrity.txt` | Detached at the exact head and tree; index tree equals the HEAD tree; 309 tracked blobs re-hash equal in bytes and mode; 0 untracked or ignored files; 0 assume-unchanged or skip-worktree flags. The repository has no gitlinks and no `.gitmodules`. |

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #128 body, 5861093499, 5861952375, 5862928771; parent first-probe harness at head (`receipts/50`); R1/R2/R3/R6/R17 honest-failure and backoff checks; interface identity (`receipts/30`); manager consumer receipt 5865084506 | R377-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| RTL | CLEAN | `hdl/acmp/KL_acmp_talker.sv` at head: comment-only round-3 delta, hand-derived equivalence of the EVC_INIT fallback, the `pe_off_r` kill term and m29, lockstep 0/64, lint rc 0, 0 forward references, composition with the SRP RTL from main (`pp_top`) | R377-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| Robustness | CLEAN | R16/P7 event classes under continuous commands; R17 absent-allocator pacing; 26 reviewer edits in suite and lockstep (random resets, wrap, disable pulses, allocator stalls); round-1 probes; SRP LeaveAll composition through `pp_top` and the SRP campaign | R377-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| Tests | CLEAN | `retry_cases.hpp` R16/R17; `retry_mutants.py` (rerun 62/7/1, 59/59, rc 0; README 70/70); `tb/srp_top/mutants.py` (64/64, 49/49); ACMP/SRP/MAAP/`pp_top` suites; parent classifier; S1 and S2 are suggestions only | R377-3 | 66451539ee49262d97403bc6b010202bb773d272 |
| Docs | CLEAN | 05 §6bis `:412-458` (including the new `:416-418`), talker README (R16/R17, campaign table, equivalence/performance text), EVC_REL comment, PR body round-3 section; `make check` and matrix rc 0; S2 is a suggestion only | R377-3 | 66451539ee49262d97403bc6b010202bb773d272 |

## Real limits

- **Simulator.** The assigned simulator path does not exist. I used the byte-identical sibling pinned wrapper, as in R377-2 (`receipts/00`). CPU use was capped at 8 cores and at most 8 parallel jobs.
- **Bank scope.** I ran only the ACMP, SRP and MAAP suites, `pp_top`, talker lint, `make check`, the matrix check and both campaigns. I did not run the 33-suite bank, full HDL lint, Yosys/portability, or any parent/gPTP/builder bank.
  - Hosted `suites` (every suite, full lint, SRP campaign) and `portability` executed and succeeded at the exact head.
  - The manager reports the donor bank at 9/9 (5865084506). No public bank artifact for this head exists: the evidence branch has no round-3 packet.
- **Parent gates.** I did not run `xvlog_gate`, `pp_shadow` or `measure_test_evidence --check`. My checks of those mechanisms are the declaration scan, the parent classifier's own functions, and the reconstructed first-probe harness, which is my round-1 reconstruction and not the original #606 runner.
- **Lockstep.** It is randomized simulation, not a formal equivalence proof. The equivalence verdicts rest on it together with the hand derivations above.
- **Author material.** The author's round-3 lockstep receipts are not public. I reproduced the README's claims (0/16 each, control 12/16) with my own harness.
- **Timing of the long runs.** The two campaigns exceeded the tool's 10-minute foreground limit. I polled them to completion in the foreground before reading any results; both receipts end with rc 0.
- **Writes.** Nothing was written outside this packet. The clone was read through `git archive`/`git show`. `git write-tree` yielded the existing HEAD tree id.
- **Hardware.** Physical calibration NOT RUN. No bench, hardware or field result exists for this head, and field skips are not hardware proof.

## Pending manager duties

- **Parent pin-adoption lane:**
  - update `pp_shadow` `[H]` (base, vid73 and crf builds) and `[I]` (crf), as the PR body states, including R377-2 S2 (count grants per source from MAAP enable; replace the stale third-probe wording);
  - add the `retry_mutants.py` row to `DUT_READER_DISPOSITIONS`;
  - add the real-shim first-probe MAAP regression;
  - rerun the consumer gates on the pin-adopting candidate and publish the receipts.
- **Final candidate.** Build the final current-dev candidate at the merge turn (source base `97bd3786a56020adec99068369642d2025b801e4`, live dev `54ce877371ee6e8878cf67294e86c2a8481b62f6`). This is distinct from source validation.
- **Acceptance.** Own hosted and act acceptance.
- **Hardware.** Physical calibration and a bench re-measure of the first bind after pin adoption (NOT RUN).
- **Merge.** Merge still needs two independent positive reviews at the same exact head.

## Packet

- `probes/run_r377_3.sh` reproduces every run. Its inputs are a clone, a revision, a simulator, a scratch directory, an output directory and, optionally, the parent inputs.
- `probes/r377_mutants.py` has suite and lockstep modes and runs at most 8 jobs. It never counts a missing tally as a kill. The round-3 rows are `eq_sticky_kill_ignores_accept` and `wait_only_on_accept`.
- The other scripts:
  - `probes/lockstep/` holds the lockstep wrapper and its driver;
  - `probes/r377_event_classes.hpp` is P7;
  - `probes/r1/` holds the round-1 probes, the declaration scan and the first-probe harness;
  - `probes/compare_readme.py` checks the README table against a campaign rerun;
  - `probes/strip_sv_comments.py` strips comments for the RTL identity check.
- Receipts are under `receipts/`. Host paths are redacted to `<PACKET>`, `<SCRATCH>`, `<CLONE>`, `$VALIDATION_STORAGE` and `$HOME`. Every published file is listed in `MANIFEST.sha256`.

R377-3 FINISHED
