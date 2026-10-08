[R554] POSITIVE - exact head bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d

# R554-3 independent review: issue #167 / PR #169, round 3 (delta)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #169 (closes #167). Review start: PR #169 comment 6059879565. Manager correction notice: PR #169 comment 6059876262.
- Exact head `bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d`, tree `9a5bb28e18469943b28e1ece0194dc9693e0d5b7`. Source base (processor main) `ed340b9b85258194247334b85e62cf9c23d4d051`. Previous reviewed head `1411117e646023cb236de02e3acaf9bdfcef49e3`, tree `4b2b3045188f7c1403a5bafb56f7e9edc059a6dd`.
- Delta under review: `1411117e..bcbf382e`, one manager docs commit, read against the whole `ed340b9b..bcbf382e` diff. R555-2 (POSITIVE at 1411117e) and R554-2 are the baseline for the unchanged RTL, tests and records.
- Role: internal independent reviewer, cleared context, own detached clone.
- Reconstruction order:
  1. The repository has no AGENTS.md or CONTRIBUTING.md. I read README.md and docs/README.md (section 1 reading order: 09 is the document that shows how compliance is demonstrated).
  2. The issue #167 body (acceptance 1 to 3) and its five comments: assignment 6050430051, TAKEN, REVIEW READY f3fef224, round-2 assignment 6052908672, REVIEW READY 1411117e.
  3. The PR body, and the manager comments on the PR: four review-start notices, the correction notice 6059876262 and this round's start notice.
  4. docs/architecture/06_aecp_engine.md:880-929, 09_verification.md section 3 (categories) and section 8.4, and tb/aecp_notify/README.md (sections CX and SC).
  5. The RTL of `KL_aecp_notify` (cancel pick, `g_ca_turns`, `g_ca_own`), the full diff and history.
  6. The public evidence at kebag-logic/milan-fpga@5a59492617aa18d116fe881ceffe24b17aa4f9ba `review-evidence/pp167-r1/`, the `author-r2/round2/` area, suite and scope summaries.
- Prior public review reports (R554-1, R555-1, R554-2, R555-2) were read only after this review's independent pass, probes, verdict and ledger had been written to this file. They are reconciled below.

## Verdict

POSITIVE. All five lenses are CLEAN. There are no open BLOCKER, MAJOR or MINOR findings, and no RESIDUE. One new SUGGESTION is recorded (S1), and one prior SUGGESTION is carried (R554-2-S1). Neither affects the verdict.

The delta is one docs commit with two changes in `docs/architecture/09_verification.md`:
- `:301` changes "six" to "seven".
- `:321` adds the row `TIM | tb/aecp_notify SC (#167)`.

Every other tracked blob and mode is byte-identical to 1411117e, so no RTL, test, Makefile, README record or mutant driver changed.

The row is accurate against the suite, its README and 06. This review ran SC1 and SC2 at the exact head and confirmed with a probe that the failure falls in the deferred cancellation's clock. The count of seven equals the table's `tb/aecp_notify` rows. `make check` is rc 0. R554-2-F1 is therefore resolved.

## Delta verification

1. **Only the docs file changed** (`receipts/byte_identity.txt`).
   - `git diff --name-status 1411117e..bcbf382e` lists only `M docs/architecture/09_verification.md`.
   - `git ls-tree -r` at both commits, with that path excluded, is IDENTICAL: same blob and mode for all 580 other entries.
   - bcbf382e has the single parent 1411117e.
2. **The count.** Section 8.4 `:299-302` says "plus one section of the originator's unit suite and seven of the notification block's".
   - The table's `tb/aecp_notify` rows are FT, IX, TS, TW, DR, CX and SC: seven. At 1411117e there were six (no SC).
   - The originator row (`tb/originator` R) is one.
   - PT, CK, PD and CA are in the separate two-interface table (`:432-435`), as before.
3. **The SC row against its authorities.** Each clause is checked below.
   - "at one interface": the SC1 and SC2 setup is the default build (`N_IF_P` = 1). README section SC: "at one AVB interface". 06:919: "At one interface".
   - "a TIME_LIMITED drain and another controller's command in the same clock". In `tb/aecp_notify/sim_main.cpp:336-341` (SC1) and `:406-411` (SC2), the command of the other row (`eids[1 - expired]`) is presented in the clock where the face shows the expired row's cancel. That clock is the drain's cancel clock (README: "On its drain's cancel cycle, the other controller sends a command for exactly one clock").
   - "send both availability cancellations exactly once, in either row order": `cancels[0] == 1 && cancels[1] == 1`, looped over `expired` = 0 and 1 (`:302`, `:355-356`; SC2 `:369`, `:434-435`). This review's run gives `{1,1}` in both orders for SC1 and SC2 (`receipts/aecp_notify_check.log`).
   - "a failure for the commanding owner presented in the deferred cancellation's clock". SC2 presents `ca_fail_owner_i = 1 - expired` at `met_at + 1` (`:413-418`). Probe Q1 logged the clock of every cancel: the deferred cancel of the commanding owner is at met+1, the same clock in which the failure is presented, in both row orders (`receipts/probe_q1_sc2_clock.log`). This matches 06:923-925 ("including the cycle that emits that deferred cancel"), and the RTL, where `cx_wait_r` holds the bit through the emitting clock (`hdl/aecp/KL_aecp_notify.sv:785-803`).
   - "leaves that controller registered and sends no DEREGISTER": `dbg_reg_cnt_o == 1` and `dereg_live == 0`. Every unsolicited frame must also be the expired controller's targeted DEREGISTER (`:423-429`, `:434-435`), so the one remaining entry is the commanding controller. The expired controller's own DEREGISTER is still required (see S1 for the wording).
   - Category TIM: 09 section 3 defines TIM as compressed-timer runs covering "controller monitors" and "TIME_LIMITED expiry". SC exercises both. This is consistent with the CX row, which the correction mirrors, and with R554-2-F1's "DIR or TIM".
4. **Gates at the exact head** (`scripts/run_gates.sh`). The suite uses the pinned Verilator 5.050 wrapper; its identity was checked (`receipts/verilator_version.txt`: "Verilator 5.050 2026-07-01 rev v5.050"). The host default is 5.052 and was not used.
   - `make check` in the review clone: rc 0, all targets OK (`receipts/make_check.log`, `.rc`).
   - `tb/aecp_notify` `make check` in a git-archive copy of the exact head: rc 0, `67 checks: 67 PASS, 0 FAIL`. That is 42 + 4 + 19 + 1 (SC1) + 1 (SC2), matching the README's accounting and the author's round-2 count (`receipts/aecp_notify_check.log`, `.rc`).
5. **SC controls still plant** (`scripts/run_probes.sh`, `receipts/probe_q2_sc_mutants*.{log,json,rc}`). `tb/pp_top/notify_mutants.py --only cancel_collision_drops_command cancel_pending_accepts_failure --jobs 4` ran from the exact-head copy, with disposable trees under scratch.
   - Both goldens PASS.
   - `cancel_collision_drops_command` is KILLED by SC1. `cancel_pending_accepts_failure` is KILLED by SC2. No named check is missing.

## Findings

### S1 - SUGGESTION - Docs

- **Location.** `docs/architecture/09_verification.md:321`, the final clause "... leaves that controller registered and sends no DEREGISTER".
- **Evidence.** SC2 also requires the expired controller's targeted DEREGISTER in the same watch (`tb/aecp_notify/sim_main.cpp:425-429`; README section SC: "The expired controller must still receive its own DEREGISTER"). The row's subject is the failure, and the failure causes no DEREGISTER, so the clause is accurate. A reader could still take "sends no DEREGISTER" as "no DEREGISTER at all".
- **Impact.** None on any measurement, test or claim.
- **Suggested outcome.** "... leaves that controller registered and sends it no DEREGISTER", mirroring README section SC ("no DEREGISTER may target that live controller").
- **Verification.** Read the row. `make check` rc 0.

## Reconciliation of prior public findings at this head

| Prior finding | Severity, lenses | Status at bcbf382e | Evidence |
|---|---|---|---|
| R554-1-F1: at count one, the deferred cancel let a failure one cycle after the coincidence remove the live controller and send it a targeted DEREGISTER | MAJOR; Conformance, RTL, Robustness, Tests | **RESOLVED** (resolved at 1411117e; still resolved) | The guard `&& !cx_wait_w[cf_ix_w]` at `hdl/aecp/KL_aecp_notify.sv:801-803` is byte-identical to 1411117e. SC2 passes in both orders with 1 entry and 0 live DEREGISTER. Its guard-removal control `cancel_pending_accepts_failure` is KILLED at this head. 06:923-928 states the rule. |
| R554-2-F1: 09 section 8.4 had no row for `tb/aecp_notify` SC, and the count read "six" | MINOR; Docs | **RESOLVED** | `09_verification.md:321` adds a TIM row in the CX row's style. It carries both required statements: both cancellations exactly once in either row order, and the commanding controller kept with no DEREGISTER after a failure in the deferred cancel's clock. `:301` reads "seven". `make check` rc 0. No RTL, test or record changed (Delta verification 1 to 5). |
| R554-2-S1: the `g_ca_own` comment at `hdl/aecp/KL_aecp_notify.sv:779-784` does not mention `cx_wait_r`'s second role, the failure guard at `:803` | SUGGESTION; RTL (comment only) | **CARRIED** as SUGGESTION. The RTL is unchanged, and the outcome is optional. | `:782-784` still describes only cancellation retention. 06:923-925 documents the guard. |
| R555-1 and R555-2 | none | nothing to resolve or retain | Both reports record no findings, RESIDUE or SUGGESTION items. |

## Lens evidence

- **Conformance - CLEAN.**
  - Issue #167 acceptance:
    - Acceptance 1: both cancels at count one.
    - Acceptance 2: a same-cycle check with a planted control that drops the second cancel.
    - Acceptance 3: OOC 1x1 within +20/+20, and every arm plants.
  - Acceptances 1 and 2 are re-verified at this head by SC1 and its control. The R554-1-F1 window remains closed (SC2 and its control).
  - Acceptance 3: RTL and synthesis inputs are byte-identical to 1411117e, so the author's round-2 receipt applies unchanged: `author-r2/round2/area-comparison.json`, LUT 23,160 to 23,171 (+11) and FF 19,787 to 19,807 (+20); BRAM and DSP unchanged; `within_limit` true. It was inspected and not reproduced.
  - The new 09 row makes no conformance claim beyond what the suite grades (Delta verification 3).
  - No port, parameter or register-map change, so no STOP condition applies.
- **RTL - CLEAN.**
  - `hdl/` is byte-identical to 1411117e. The whole-PR RTL diff was re-read:
    - `cx_wait_r` pending bits, with the emitted index cleared after the union.
    - The common pick term at `:619`.
    - `cx_wait_w = '0` in `g_ca_turns`, so the count-two path is untouched.
    - The failure guard at `:803`.
  - The behaviour matches 06:919-929.
- **Robustness - CLEAN.**
  - Probe Q1 placed the SC2 failure in the deferred cancellation's own clock in both row orders, and the guard held: 1 entry, 0 live DEREGISTER.
  - Reset and lifetime properties of the unchanged pending bits are carried from the R554-2/R555-2 baseline. No new behaviour exists to stress.
- **Tests - CLEAN.**
  - `tb/aecp_notify` passes 67/67 at the exact head, with five run tallies.
  - Both SC controls are KILLED by their named checks, and both goldens PASS.
  - Test sources, Makefile and the mutant driver are byte-identical to 1411117e.
- **Docs - CLEAN.**
  - The 09 section 8.4 row and the count are accurate against README section SC and 06:919-929.
  - `make check` rc 0 (lint, wavedrom-check, links, matrix, modmatrix, params, ids, figures, stale).
  - S1 is a SUGGESTION only.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #167 acceptance 1-3; assignments 6050430051 and 6052908672; 09_verification.md:297-324 SC row and count vs tb/aecp_notify/README.md section SC and 06_aecp_engine.md:919-929; author round-2 area receipt (inspected) | R554-3 | bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d |
| RTL | CLEAN | `hdl/aecp/KL_aecp_notify.sv` PR diff (`:461-464`, `:602-623`, `:695-806`); byte identity of all non-09 blobs to 1411117e | R554-3 | bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d |
| Robustness | CLEAN | probe Q1 (SC2 cancel-clock log, both row orders); SC2 outcome at head | R554-3 | bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d |
| Tests | CLEAN | `tb/aecp_notify/sim_main.cpp:296-442`, Makefile; suite 67/67 rc 0; `notify_mutants.py --only` the two SC arms: 2/2 KILLED, 2 goldens PASS | R554-3 | bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d |
| Docs | CLEAN (S1 SUGGESTION) | `docs/architecture/09_verification.md` delta and section 3; `make check` rc 0; README section SC; 06:919-929 | R554-3 | bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d |

## Real limits

- **Not run by this reviewer**, by the assignment's rules or for lack of tools:
  - the full processor suite bank, `scripts/lint_hdl.sh`, `gen_matrix.py` beyond `make check`'s `modmatrix`, and `syn/yosys/run.sh`;
  - the OOC 1x1 synthesis;
  - the other notify-campaign arms and the nine other campaigns;
  - the 17 parent consumer gates.

  Because this delta changes only one docs file, the author's round-2 receipts at 1411117e (`author-r2/round2/`: suite totals 1,028,291 to 1,028,293; area +11 LUT / +20 FF) apply to byte-identical RTL, test and record inputs. They are the only source-head execution evidence for those gates. They were inspected, not reproduced.
- **Unit level only.** Probe Q1 is unit-level (`KL_aecp_notify` alone). The originator-side premise of the guard is carried from the R554-2 baseline, not re-run.
- **Hosted CI at the exact head**, snapshot 2026-10-08T12:34:29Z (`receipts/hosted_check_runs_bcbf382e.tsv`): docs-gates and portability completed with success in both runs (37777167641, 37777163060). Both `suites` jobs were in progress. No hosted suite or campaign conclusion is claimed; the manager owns hosted/act acceptance.
- **No manager source bank** runs at this exact head, and none is claimed or inferred. Source validation at this head is distinct from the current-dev merge candidate, which the manager builds at the merge turn: source base ed340b9b85258194247334b85e62cf9c23d4d051 onto live dev 17f62ef64a66562384e8a93b1d6be6f86e51f95c.
- **Physical calibration** NOT RUN. Field skips are not hardware proof. The author records the external calibration-report arm as not run.
- **Toolchain and parallelism.** Pinned Verilator 5.050 wrapper, identity in `receipts/verilator_version.txt`. At most two concurrent builds; the campaign ran with `--jobs 4`. The two scripts now take the wrapper from `VERILATOR` (a portability edit made after the runs; the runs used the same wrapper).
- **Clone integrity** after all work (`receipts/clone_integrity.txt`):
  - HEAD and tree are exact, and the index tree equals the HEAD tree.
  - All 581 tracked files match their blobs byte for byte, with modes 564 × 100644 and 17 × 100755.
  - There are no gitlinks and no `.gitmodules`; the processor has no submodules.
  - `make check`'s wavedrom bootstrap created an ignored `.venv-wavedrom/`, absent at the start. It was removed, and the final `status --porcelain --ignored` is empty.
  - All builds, probes and plants ran in disposable trees under the unpublished `scratch/`.
- **Redaction.** Host path prefixes in two receipt logs were replaced with `<PACKET>`, `<PINNED_VERILATOR>` and `<TOOLROOT>` (`scripts/redact_receipts.py`). No result line was changed.

## Pending manager duties

- Hosted/act acceptance at the exact head, including the two in-progress `suites` jobs.
- The manager banks announced for this head in comment 6059876262, and the current-dev merge candidate (builder and native banks) at the merge turn, with receipts linked on the PR.
- Optionally carry S1 and R554-2-S1 to the author. Neither blocks.
- The second (external) independent review of this round, R555-3. Merge requires two positive reviews and the full completion bar.

## Packet

- Scripts:
  - `scripts/run_gates.sh`: `make check`, and the aecp_notify suite in a git-archive copy.
  - `scripts/run_probes.sh`: probe Q1, and the two SC arms.
  - `scripts/probe_sc2_clock.py`: the Q1 instrumentation patch.
  - `scripts/redact_receipts.py`.
- Receipts are under `receipts/`. Every published file is listed in `MANIFEST.sha256`.

R554-3 FINISHED
