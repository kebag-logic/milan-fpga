[R377] NEGATIVE - exact head cc7c911e933aed4bfc9324eb5da473ae73bef618

# R377-2: external independent re-review of processor PR #129 / issue #128

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `cc7c911e933aed4bfc9324eb5da473ae73bef618`, tree `3eff9b9f986b34ca2aec3e6c1b8387090978d88b` (verified in the detached review clone)
- Delta under review: `9476898b..cc7c911e` (one commit, "Close ACMP retry review gaps and document paced allocation semantics"). Cumulative diff from base `16be6768f710e79450aace277abacd6c2c3336e5` also read.
- Round-2 assignment: issue #128 comment 5861952375 (decision: keep the paced rounds, option a). Review start: PR #129 comment 5862479124.

## Verdict summary

Every round-1 finding from both reviewers is resolved at this head:

- The declaration-order defect is fixed.
- The paced-round semantics and the consumer-visible change are documented, and the PR body names both parent checks and what each must observe instead.
- The mutation runner no longer uses a host deadline.
- Every surviving mutant that either reviewer listed now fails a named assertion.
- The redundant `!en_q_r` term is removed, and the four remaining overlapping terms are stated as equivalent. A randomized lockstep comparison supports all four: no divergence in 48M cycles each, while a known non-equivalent control diverges in 12 of 16 seeds.

The RTL behaves correctly throughout. My probes pass at head, the parent first-probe harness passes, and the ports and parameters are unchanged.

**NEGATIVE because one MINOR finding is open (F1, Tests).** Round 2 took R377-1 S1 "as far as the terms are not redundant". S1 said that the 05 claim "commands and pending events alternate" was pinned only for retry events. Round 2 pinned the OFF and RELEASE terms of `txn_eligible_w`. The CONFLICT, PCP, TIMER and LISTENER terms are still unpinned, and they are not redundant: each one changes behaviour in lockstep (16/16 seeds). Removing any of them passes the committed suite (1172/1172). My probe P7 kills each one with a named assertion, and the head passes P7.

## Reconstruction (in order)

1. **Rules.** The processor has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` and `docs/README.md` (single-source rules: timing values only in F08.1). I also read the parent's `AGENTS.md` (reviewer procedure, lenses, severity) and `CONTRIBUTING.md` (verification bar, the `xvlog` use-before-declaration rule and the `xelab` initialiser caveat, wording rules) at `b367df5d` (`receipts/01-inputs.txt`).
2. **Issue #128.** I read the body, assignment 5861093499 and the round-2 assignment 5861952375. Frozen scope:
   - bounded, fair reattempts with honest failure;
   - no retry storm and no command starvation;
   - no change to conflict or PCP backoff;
   - no interface change;
   - every new check pinned by a killed mutant.

   Round-2 items 1 to 4, plus taken suggestion R377-1 S1 for the non-redundant terms.
3. **Authorities.** Processor 02 §4.2, 05 §6bis (F05.12), 08 F08.1. Parent `hdl/milan/KL_pp_maap_shim.sv`, `tb/verilator/pp_shadow/sim_main.cpp` `[H]`/`[I]` and `scripts/measure_test_evidence.py`, all at `931f396e` (hashes in `receipts/01-inputs.txt`).
4. **Diff and history.**
   - `git diff 16be6768..cc7c911e`: 12 files, +1098/-80, and the only RTL file is `hdl/acmp/KL_acmp_talker.sv`.
   - Round-2 delta: 9 files, +464/-63.
5. **Public evidence.**
   - `kebag-logic/milan-fpga@b367df5d:review-evidence/pp128-r1`. Its HANDOFF names head `9476898b`, so it is round-1 author material; no round-2 author packet is public.
   - Manager comment 5862432079 (parent consumer gates at `cc7c911e`: 9 of 11 pass; the two remaining are the decided parent-lane `[H]`/`[I]` and the reader disposition).
   - Hosted check runs at the exact head.
6. **Prior public findings.** I wrote my independent notes (`receipts/02-independent-notes-before-prior-reviews.txt`) before I read R377-1 (5861647041) and R376-1 (5861948499). Each prior finding is resolved or retained below.

## Findings

### F1 - MINOR - Tests - four `txn_eligible_w` terms of the command/event alternation are still unpinned

```text
[R377] MINOR Tests - hdl/acmp/KL_acmp_talker.sv:594-597 - CONFLICT/PCP/TIMER/LISTENER eligibility terms survive every committed check
```

- **Where.**
  - `hdl/acmp/KL_acmp_talker.sv:594-597`: the `|pe_conflict_r`, `|pe_pcp_r`, `|pe_tmr_r` and `|pe_lsn_r` terms of `txn_eligible_w`.
  - `tb/acmp_talker/retry_cases.hpp:298-316` (R11): pins only disable/withdraw and release.
  - `tb/acmp_talker/retry_mutants.py:13-212`: the table has `elig_drop_off` and `elig_drop_rel`, but no mutant for these four terms.
- **Authority.**
  - Issue #128 comment 5861952375: "Taken suggestion: R377-1 S1, as far as the terms are not redundant."
  - R377-1 S1: "The 05 claim that commands alternate with *all* pending events is pinned only for retry events."
  - `docs/architecture/05_acmp_engine.md:423`: "Commands and pending events alternate when both are present."
  - Parent AGENTS Tests lens: each test can fail for the defect it claims to detect.
- **Evidence** (pinned simulator 5.050):
  - `receipts/20-reviewer-suite/`: `elig_drop_conflict`, `elig_drop_pcp`, `elig_drop_tmr` and `elig_drop_lsn` each pass the committed suite, 1172/1172.
  - `receipts/30-lockstep/`: each diverges observably from the head in 16/16 seeds, so none is equivalent. For comparison, the four stated equivalents and the removed `!en_q_r` term show 0/16.
  - `receipts/40-probe-p7/`: reviewer probe P7 (`probes/r377_event_classes.hpp`) holds a GET_TX_STATE continuously valid, raises one event of each class, and samples the gate level *before* releasing the command stream.
    - The head passes: 1193/1193.
    - Each mutant fails exactly one named assertion. Example: `P7 conflict event served under continuous commands (gates 0x02 want 0x00)`, and likewise for pcp, freshness and listener.
- **Impact.** At this head the RTL is correct. But a later edit could drop any of these terms and every suite would stay green. That edit would bring back the pre-#128 starvation of that event class under sustained command traffic:
  - a MAAP conflict on a declaring source would never withdraw, so the stream stays declared on a conflicted DA;
  - a PCP change would never back off;
  - a freshness lapse would never withdraw;
  - a Listener registration would never open or close the gate.
- **Required outcome.**
  - Add a committed regression that, like P7, shows each of these four event classes served while commands are held continuously.
  - Add the four mutants to `retry_mutants.py` so that each fails a named assertion. Alternatively, argue a term redundant and state it as an equivalent control; the lockstep evidence says none is.
- **Verification.**
  - `retry_mutants.py` (full run) kills the four new rows with named assertions, witnesses every new assertion site, and keeps baseline and restore at rc 0.
  - `acmp_talker` and `pp_top` stay green.

### Suggestions (do not affect the verdict)

- **S1 (RTL, Tests): two further redundant terms are neither removed nor stated.**
  - **(a)** The EVC_INIT `else ev_initset_w = 1'b1; // maap busy` branch (`hdl/acmp/KL_acmp_talker.sv:870-872`) is unreachable at this head.
    - EVC_INIT is now dispatched only when `maap_avail_w` is true (`:631`), and `maap_avail_w` cannot fall before `S_EV_ACT`. Busy is set only by an accept in `S_EV_MAAP`, a grant needs a live response while busy, and stale credits change only on a timeout while busy.
    - The EVC_REL comment at `:856-858` still contrasts itself with that branch.
  - **(b)** The `pe_off_r[maap_src_r]` term of `maap_kill_w` (`:480`) is observationally redundant with the `!cfg_src_en_i` term plus the sticky latch and the accept-side expression.
  - Both show 0/16 lockstep divergence and survive the suite (`receipts/30-lockstep/`, `receipts/20-reviewer-suite/`: `init_busy_else_removed`, `kill_w_no_off`).
  - The accept-side single terms (`accept_kill_no_pending_conflict`, `accept_kill_no_live_conflict`, also 0/16) are already covered by the stated `accept_kill_zero` control.
  - **Suggestion:** remove (a) or record it in `REMOVED_EQUIVALENTS`, and state (b) as an equivalent control.
- **S2 (Docs, advisory for the parent lane): widen the `[I]` reconciliation text.** The PR body's `[I]` text correctly asks the parent to key each response by its accepted request's source index. The parent check (`tb/verilator/pp_shadow/sim_main.cpp` @931f396e, `grade_maap_grants_and_opens_the_da_gate`) also snapshots `mo` only after it *observes* ANNOUNCE, and it polls every 2000 cycles. With automatic rounds, the first round after the block becomes valid can fall inside that polling window. The grant would then precede the snapshot, and "the shim GRANTED an address" would see zero new grants. It passes today, but it depends on timing. Suggest also counting per-source grants since MAAP enable. The comment there about grading "the third probe" also becomes stale.

## Resolution of prior public findings at this head

| Prior finding | Disposition at cc7c911e | Evidence |
|---|---|---|
| R377-1 F1 / R376-1 F1: `set_conflict_w` used before its declaration | **RESOLVED** | `KL_acmp_talker.sv:878-883` declarations now precede `retry_round` (`:885`). Scan: 0 forward references at head, 1 at `9476898b`, 0 at base (`receipts/60-forward-ref.txt`). The moved lines are bare `logic` declarations with no initialiser, so the `xelab` VRFC 10-9171 class does not apply (checked by hand). Manager `xvlog_gate` passes at this head (5862432079). |
| R377-1 F2 / R376-1 F3: host deadline and DUT reader in `retry_mutants.py` | **RESOLVED (processor side)** | No `timeout=` at `:237-238`. The parent's own `uses_wall_clock` is False at head and True at `9476898b` (`receipts/61-parent-evidence-classifier.txt`). The reader-disposition line is supplied in the PR body in the parent table's format; it is not yet in the parent table (pending manager). |
| R377-1 F3: five non-equivalent survivors | **RESOLVED** | All killed by named assertions in the committed suite: `init_elig_no_avail` (R9), `no_conflict_wait_clear` (R10), `no_probe_initset` / `no_lsn_initset` / `no_backoff_exit_initset` (R12). My round-1 probes P1-P6 pass at head: 1219/1219, 47 probe checks (`receipts/51-r1-probes-rerun/`). My round-1 mutant set, rerun: every non-equivalent mutant is killed. The only survivors are the three now stated as equivalent, and the two anchors that contained the removed `!en_q_r` term no longer exist (`receipts/50-r1-mutants-rerun/summary-acmp_talker.txt`). |
| R377-1 F4 / R376-1 F2: undeclared consumer-visible change, parent `[H]`/`[I]` | **RESOLVED (processor side)** | 05 §6bis `:452-458` "Consumer-visible timing change"; 02 §4.2 `:268-271`; F05.12 arc `:389`; 08 F08.1 row `:34`. The PR body names `[H]` and `[I]`, why they change and what each must observe, and this matches the parent source (sha256 `c9062587…`). The round-2 handoff is not public (limit). The parent test edits are the manager's lane. See S2. |
| R376-1 F4: m01, m02, m07, m17, m19-m22 | **RESOLVED** | Killed by named assertions: `no_conflict_wait_clear` / `no_enable_wait_clear` (R10), `elig_drop_rel` / `eligible_only_init` (R11), `init_elig_no_avail` (R9), `no_*_initset` (R12). The response-budget starvation mutant (`init_elig_no_avail`, and `busy_tracker_blocks_commands`) and the three demand-path mutants are all in the table (`receipts/10-author-campaign/`). |
| R377-1 S1 (taken for non-redundant terms) | **PARTIALLY RESOLVED; remainder retained as F1** | Listed terms: `grant_kill_reg_only`, `kill_no_live_conflict`, `kill_no_disable`, `init_ignores_off_conflict`, `elig_drop_rel` and `elig_drop_off` are killed. `no_sticky_gp_window`, `accept_kill_zero` and `kill_no_pending_conflict` (plus `accept_kill_no_disable`) are stated equivalent and confirmed 0/16 in lockstep. `!en_q_r` is removed and confirmed equivalent (0/16). The "alternation with all pending events" remainder is F1. |
| R377-1 S2 / R376-1 S1: publish the #606 wiring runner | not taken by the manager; unchanged | no verdict effect |
| R377-1 S3 / R376-1 S2: stale banner and comments; operator row | **RESOLVED** | `KL_acmp_talker.sv:174-179`; `tb/acmp_talker/sim_main.cpp:957-958`; `docs/guides/operator.md:282` |
| R376-1 S3: "100 ms" repeated beside the ID; no F05.12 arc | **RESOLVED** | no literal "100 ms" in 05, 02 or the guides; F05.12 `:389` |
| R376-1 S4: stalled `now_ms_i` dependency | **RESOLVED** | `docs/guides/integrator.md:44-47` |

## Assignment verification items

1. **Declaration order.** Fixed; see the table. Parent `xvlog` passes at this head according to the manager receipt (5862432079). I did not run `xvlog`.
2. **Round semantics documented.** Yes: 05 §6bis `:412-458` and 02 §4.2 `:264-271`. The PR body names `[H]` and `[I]` and exactly what each must observe instead, and this is accurate against the parent source.
3. **No wall-clock deadline; disposition supplied.** Yes, confirmed with the parent's own classifier.
4. **Reviewer probes committed; listed survivors killed.**
   - Committed regressions R9-R15 cover R377-1 P1, P2 and P4-P6 and R376-1 P1-P5.
   - Every surviving mutant either reviewer listed fails a named assertion, including the response-budget starvation mutant and the three demand-path mutants.
   - I reproduced the campaign: 56 killed, 4 equivalence controls, 50/50 assertion sites witnessed, baseline and restore rc 0 (`receipts/10-author-campaign.stdout`).
   - The README's 60-row table matches my rerun row for row: failure counts and named assertions (`receipts/12-readme-table-vs-rerun.txt`).
   - The one gap against the taken S1 is F1.
5. **Redundant terms removed or stated.** `!en_q_r` is removed; four terms are stated equivalent, and lockstep supports every statement. Two more redundant terms are unstated (S1, suggestion only).

No interface change: the talker's parameter and port header is identical to the base with comments stripped. `protocol_processor_top.sv`, `KL_pp_maap.sv` and `pp_pkg.sv` blobs are unchanged, and only the talker changed under `hdl/` (`receipts/72-interface.txt`).

## Reviewer-owned independent evidence (pinned simulator 5.050)

| Receipt | Result |
|---|---|
| `receipts/00-tool-identity.txt` | The requested wrapper path is absent. I used a byte-identical copy of the sibling pinned wrapper (sha256 `905795b9…`), which reports `Verilator 5.050 2026-07-01 rev v5.050`. |
| `receipts/71-suites-head.txt` | `acmp_talker` 1172/1172 and `pp_top` 7751/7751 (the only two suites that instantiate the talker) |
| `receipts/70-gates.txt` | talker `make lint` rc 0; `make check` rc 0 (41 mermaid, 18 wavedrom, 921 links, matrix, 24 parameters); `gen_matrix --check` 92 rows, 0 untested |
| `receipts/10-author-campaign*` | committed campaign reproduced (see item 4) |
| `receipts/20-reviewer-suite/` | 24 reviewer single edits against the committed suite |
| `receipts/30-lockstep/` | Observational lockstep, 16 seeds x 3M cycles per edit: every output of the head and the edited copy compared every cycle, under contract-conforming random stimulus with focused churn. Identity-control totals over 48M cycles: 50,513 accepts, 7,703 grants, 38,331 refusals, 37,278 conflicts, 1,351,195 command responses, 5,720 declare edges and 167 resets. The known-killed control diverges 12/16. |
| `receipts/40-probe-p7/` | F1 probe: head passes, four mutants killed with named assertions |
| `receipts/50-r1-mutants-rerun/`, `receipts/51-r1-probes-rerun/` | my round-1 mutants and probes at this head |
| `receipts/73-parent-first-probe-cc7c911e.txt` | Reconstructed parent first-probe harness (real parent shim `965fbee0…`, published oracle `9a195388…`). Result: first probe status 0, DA `91e0f0006818`, no probe-triggered ALLOC_DA, harness rc 0. This is the #128 acceptance. |
| `receipts/80-hosted-checks.txt` | Six hosted jobs at the exact head (`suites`, `portability` and `docs-gates`, in two workflow runs) all executed and succeeded; none was skipped. The legacy combined status has 0 contexts. |
| `receipts/90-clone-integrity.txt` | Review clone detached at the exact head and tree; index tree equals HEAD tree; 251 tracked blobs re-hash equal in bytes and mode; 0 untracked or ignored files; 0 assume-unchanged or skip-worktree flags. This repository has no gitlinks. |

**Survivors judged benign (no finding).** These edits diverge in lockstep but stay inside documented bounds:

- `turn_not_on_grant`: a grant does not restore the command turn, which adds at most one 3-cycle grant event inside the `P-MAAP-ACCEPT-CYC + 64` bound.
- `tick_sets_all` and `init_ready_no_en`: pending-INIT bits of disabled sources cause a one-cycle-earlier dispatch or a wasted walker visit, with no request.
- `t0_reset_zero`: one extra round boundary after reset, which 05 allows ("two adjacent attempts are possible").

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #128 scope and round-2 decision 5861952375. First-probe success after the bound: R1 and the reconstructed parent harness (`receipts/73`). Honest status 3 and bounded failures for absent, refusing and out-of-block allocators (R2, R3, R7). Backoff unchanged (R6). Port and parameter identity (`receipts/72`). Parent `[H]`/`[I]` text against parent source `c9062587…`. Manager consumer receipt 5862432079. | R377-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| RTL | CLEAN | Full read of `hdl/acmp/KL_acmp_talker.sv` at head: retry round, rotating picker, `txn_eligible_w`/`txn_ready_o`, kill tracker, EVC_INIT guards, reset of every new register. Declaration order (`receipts/60`), with no initialiser split in the moved lines. Wrap-safe 32-bit compares. Lint rc 0 (`receipts/70`). Lockstep equivalence of the stated terms (`receipts/30`). S1 is a suggestion only. | R377-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| Robustness | CLEAN | Every event class served under continuous commands at head (P7, `receipts/40`). Silent-accept command bound (R9, P1). Stale-credit saturation (R5). Obsolete-grant cancellation swept over edges (R13, R14). Wrap (R5, R8). Disable/re-enable and conflict restarts (R10). Release fairness (R11, R15). 167 random mid-activity resets in lockstep. | R377-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| Tests | UNCLEAN (F1) | `retry_cases.hpp` R1-R15; `retry_mutants.py` (rerun 56/4/50, README table 60/60); `sim_main.cpp` edits; `pp_top` MP3/S10 (7751 pass); 24 reviewer single edits; lockstep; P7; round-1 probes and mutants rerun | R377-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |
| Docs | CLEAN | 05 §6bis `:412-458`, 02 §4.2 `:258-285`, 08 F08.1 `:34`, integrator `:44-47`, operator `:282`, `tb/acmp_talker/README.md` (R9-R15 table, campaign table checked against the rerun), `tb/pp_top/README.md`, talker banner, PR body `[H]`/`[I]`/disposition text; `make check` rc 0. S2 is a suggestion only. | R377-2 | cc7c911e933aed4bfc9324eb5da473ae73bef618 |

## Real limits

- **Simulator.** The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a byte-identical copy of the sibling wrapper `372-manager-r2` (identical to the `cc7c911e` manager wrapper), with identity recorded in `receipts/00-tool-identity.txt`.
- **Parent gates.** I did not run the parent's `xvlog`, `pp_shadow` or evidence gates (not permitted). Those results are the manager's receipt 5862432079. My checks of the same mechanisms are the declaration scan, the parent's own classifier functions, and reading the parent test source.
- **Public evidence.** The public packet `pp128-r1` is round-1 material (`9476898b`). No round-2 author packet or handoff is public, so I verified the "handoff names the two parent checks" part of item 2 only against the PR body. The statement that the manager's source static/builder and native banks passed at this head rests on the assignment; 5862432079 covers the consumer gates only.
- **Suite coverage.** I ran only `acmp_talker` and `pp_top`, plus talker lint, `make check` and the matrix check. I did not run the 33-suite bank, Yosys or the portability bank locally; the hosted `portability` job succeeded at the exact head.
- **Lockstep limits.** The lockstep is randomized simulation, not a formal equivalence proof. The first-probe harness is my round-1 reconstruction, not the original #606 runner. I mapped R376-1's probes to committed regressions and killed mutants; I did not rerun R376-1's own probe scripts.
- **Writes.** Nothing outside this packet was written. The clone was read through `git archive` and `git show`; the index check used `git write-tree`, which yields the existing HEAD tree id.
- **Hardware.** Physical calibration NOT RUN. No bench, hardware or field result exists for this head. Field skips are not hardware proof.

## Pending manager duties

- Parent pin-adoption lane:
  - update `pp_shadow` `[H]` (base, vid73 and crf builds) and `[I]` (crf) as the PR body states, considering S2;
  - add the `retry_mutants.py` `DUT_READER_DISPOSITIONS` line;
  - add the real-shim first-probe MAAP regression;
  - re-run the consumer gates (`xvlog_gate`, `pp_shadow`, `measure_test_evidence`) on the pin-adopting candidate and publish the receipts.
- After F1 is fixed: rerun the consumer set at the new head.
- Build the final current-dev candidate at the merge turn (source base `16be6768f710e79450aace277abacd6c2c3336e5`, live dev `c07232228c12b72805dd20e6852bf93f25794da0`). This is distinct from source validation.
- Own hosted and act acceptance.
- Physical calibration and a bench re-measure of the first bind after pin adoption (NOT RUN).

## Packet

Portable scripts are under `probes/`:

- `run_r377_2.sh`: reproduces every run from a clone, a revision, a simulator, a scratch directory and an output directory.
- `r377_mutants.py`: suite and lockstep modes, at most 8 jobs; a missing tally is never counted as a kill.
- `lockstep/`: the lockstep wrapper and its randomized driver.
- `r377_event_classes.hpp` (P7) and `apply_probe.py`.
- `r1/`: my round-1 scripts, unchanged; `r377_1_adapter.hpp` runs their probes at this head.

Receipts are under `receipts/`, with host paths redacted to `<PACKET>`, `<CLONE>`, `$VALIDATION_STORAGE` and `$HOME`. Every published file is listed in `MANIFEST.sha256`.

R377-2 FINISHED
