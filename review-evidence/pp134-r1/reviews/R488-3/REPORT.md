[R488] POSITIVE - exact head ffc3a8e5733202384e55ea9094569cca86b78261

# R488-3: internal independent review of issue #134 / PR #160

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #160 (`pp134-lv-leave` into `main`).
- Exact head `ffc3a8e5733202384e55ea9094569cca86b78261`, tree `a7c1bce09cefceda944558258f6b38cfba7ac7ed`. Source base `ead8036035affd53ef4b29979190f2f4f67084c0`.
- Review start: PR #160 comment 6008707162. This was a cleared-context pass in a detached clone of its own. Every build and probe ran on `git archive` exports or local clones under the packet's `scratch/`. The review clone was never built in or patched (see Integrity).
- Simulator: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…e92f`, `receipts/tool-identity.txt`).

## Verdict summary

The round-3 widening does what rulings 5990549074, 5994864535 and 5995957938 ask:

- **RTL.** Both registrar planes now test leavetimer! before rLv! in the same `if / else if` chain (`hdl/srp/KL_srp_talker_fsm.sv:732-734`, `hdl/srp/KL_srp_listener_fsm.sv:769-772`). An expiry is never lost to a same-clock received event. For every event that can share the clock, the final registrar state equals "expiry first, then the event" under 802.1Q-2014 Table 10-4. No port, register, parameter or timer-service handshake changed.
- **Tests.**
  - SC1 composes all eight same-clock events on both planes (128 cases).
  - SC2 sweeps a real decoded `Lv` over k = 0..400 across the expiry clock: own and peer LeaveAll, talker and listener planes, 6416 cases, all CLOSED.
  - SC3 proves that each sweep hits the expiry clock exactly once.
  - The original-order mutant fails, and so does each plane's reversal planted alone.
- **D3 diagnostics.** The `printf` fix supplies the missing `D3_RECORDS` argument. Base builds with exactly two `-Wformat` warnings at those lines, and head builds with none. Every checked-in mutation arm still plants.
- **Merges.** Both merges reproduce their automatic merge trees exactly.
- **Docs.** 10 §6.5, both suite READMEs and the harness comments state the same-clock rule consistently.

R488-1 F1 (MAJOR) and F2 (MINOR) are resolved, and so are R488-2 F1 and F2. One RESIDUE (wording only) is recorded below. It does not affect the verdict.

## Reconstruction (order followed)

1. **Contributor guides.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head. I read the conventions from `README.md` and `docs/README.md`. The ones that matter here:
   - the §2 single-source rules (timing values only in F08.1);
   - the §4 citation style;
   - `make check` as the documentation gate.
2. **Issue #134.** The frozen acceptance:
   - the arm passes, both mutants turn red, and both are recorded in the suite README;
   - 10_srp_engine.md states the LV case with the clause;
   - donor and consumer gates pass.

   The scope decisions, all public on #134:
   - lane comment 5988316116;
   - ruling 5990549074, route (b): fix the RTL on both planes, apply the same-clock rule, run the k-sweep on own/peer LeaveAll and on the talker/listener planes, add an original-order mutant, update the docs and fix F2;
   - ruling 5994864535: the D3 `printf` fix, its planting check, record equality and a `--no-ff` merge of `21c6f709`;
   - ruling 5995957938: the fifth parent adoption patch;
   - ruling 6001384633 (round 4): R488-2 F1/F2.
3. **Authorities.**
   - 802.1Q-2014 Table 10-4, the registrar table:
     - rNew!: LV gives New, Stop leavetimer, IN; MT gives New, IN.
     - rJoinIn!/rJoinMt!: LV gives Stop leavetimer, IN; MT gives Join, IN.
     - rLv!/rLA!/txLA!/Re-declare!: IN gives Start leavetimer, LV; LV and MT give `-x-`.
     - leavetimer!: LV gives Lv, MT.
   - Milan v1.2 §4.2.7.2.2 (Δ13, F01.4), which replaces only IN / rLv!.
   - Milan v1.2 Table 4.3 LeaveTime, carried as F08.1 T-MRP-LEAVE.
   - The specification PDFs are not distributed. These readings rest on the repository's quotations and the reviewer's reading of the table.
4. **Diff and history.**
   - `git diff ead8036..ffc3a8e` touches 64 files. The lane's own changes are `git diff e6a759d..ffc3a8e`: 24 files. Under `hdl/`, only the two registrar planes changed (+13/-7). Under `tb/pp_top/`, only `d3_phases.hpp:2964,2994` changed. The rest is SRP tests, mutation patches and docs.
   - First-parent history: 68b0e61, 5ab43bd, ab3c168, ed727d4, 9d26598, merge 9050c4b (main 21c6f709), a596c76, merge ffc3a8e (main e6a759de).
5. **Public evidence.**
   - The milan-fpga `7aecfd0b…/review-evidence/pp134-r1` tree holds only round-1 material: a HANDOFF bound to head `5ab43bd9`, the round-1 PR-BODY, and four adoption patches. It carries no receipt bound to `ffc3a8e5`. This review therefore rests on its own executions (see Real limits).
   - The issue and the PR carry no manager evidence comments beyond the rulings and the review-start notes.
6. **Prior public review findings.** I read them only after my independent pass. A draft verdict and ledger were written first (`receipts/draft-verdict-before-prior-findings.md`). The resolution table is below.

## Executed evidence (reviewer runs; scripts in `scripts/`, raw logs in `receipts/`)

| # | What | Result | Receipt |
|---|---|---|---|
| E1 | Complete default `tb/srp_top`, head | rc 0. `8656 checks: 8656 PASS, 0 FAIL`; storage arms 4 × `15 PASS`; `TOTAL_CLOCKS 210547557`; 6416 `LV_COLLISION … CLOSED`, 0 STUCK; 8 `LV_LEAVE` lines: own 14200 → 19200 ms, peer 705 → 5705 ms, leave 5000 ms, 1 STREAM_STOP, 0 STREAM_START each | `head-srp_top.log/.rc` |
| E2 | Same suite at main `e6a759de`, normalised diff vs E1 | Base `2200 PASS`. Every pre-existing record line is identical. Head adds only the `--savable` build flag, the `LV_LEAVE`/`LV_COLLISION` lines, `TOTAL_CLOCKS` and the tally | `base-srp_top.log/.rc` |
| E3 | `tb/srp_stream_fsms`, head vs `e6a759de` | Head `1347 PASS`, base `1219 PASS` (+128 = SC1). The normalised diff is the tally line only | `head-/base-srp_stream_fsms.log/.rc` |
| E4 | `mutants.py --only` the six #134 arms, `--jobs 8` | 3 controls PASS. `lv-second-lv-ends` S1,S2 (16); `lv-never-ends` S2,S3 (16); `lv-expiry-masked` SC2 (16) and SC1 (16); `lv-expiry-last` SC1 (48); `lv-expiry-dropped` 86 = SC1 80 + 6 older (K 3, L 1, T 2); `lv-sweep-misses-collision` SC3 (16) with SC2 green. `10 checks: 10 PASS` | `camp134.log/.rc`, `camp134/` |
| E5 | The original two arms through the complete default suite | `lv-second-lv-ends`: 8640/16, S1 8 + S2 8. `lv-never-ends`: 5624/3032, S2 8 + S3 8 + SC2 3016. Storage 4 × 15 pass under both. This equals the README `:539-548` and the PR body | `full-lv-*.log/.rc` |
| E6 | Reviewer mutant: **talker plane alone** back to the original order (`lvcoll`) | 6424/8. All 8 failures are `plane=talker` (own/peer × fp × target, one per combination), all at k = 19 | `rm-talker-orig-lvcoll.log` |
| E7 | Reviewer mutant: **listener plane alone** back to the original order (`lvcoll`) | 6424/8. All 8 failures are `plane=listener`, one per combination, at k = 35 or k = 44 | `rm-listener-orig-lvcoll.log` |
| E8 | Reviewer mutants on SC1 (`srp_stream_fsms`) | No cancel on a same-clock renewal (talker): 24 SC1 (`timer=0`). Expiry outranks renewal (listener): 24 SC1 (`reg=0 want=1`). A same-clock LeaveAll in LV re-arms (talker): 16 SC1 (events 6/7). No other check fails under any of them | `rm-*-fsms.log` |
| E9 | Older `talker-strict-lv` / `talker-no-expiry` through `lvleave` | 16 each: S1,S2 closing at 14 ms (own) or 5 ms (peer); S2,S3 never closing. This matches README `:550-553` | `rm-talker-*-lvleave.log` |
| E10 | Planting audit (`scripts/plant_audit.py`): every `tb/**/*.patch` (`git apply --check`) and every exact-text `Mutant.edits` arm | Head: 482 arms, 482 plant. Base `e6a759de`: 476, all plant. The only difference is the six new SRP patches. No patch or exact-text table carries the two `d3_phases.hpp` lines (`git grep`) | `plant-audit-{head,base}.log` |
| E11 | `pp_top` `gsi-build` with `-Wall -Wextra`, base vs head | Base: exactly two `format '%d' expects a matching 'int' argument` warnings, at `d3_phases.hpp:2963` and `:2993`. Head: 0 warnings | `base-/head-pp_top-build.log` |
| E12 | `d3_mutants.py --only clks_restore_count_narrowed clks_restore_index_narrowed` at head | Golden `pp_top --d3-only` PASS, and both arms KILLED. The fixed diagnostics now print a defined count: `blank 58 of 59` (D3C3 and D3C4, both arms) | `d3-arms-a.log`, `d3a-*.log`, `d3a-results.json` |
| E13 | Merge reproduction (`git merge-tree --write-tree`) | 9050c4b (parents 9d26598, 21c6f709) → `3bcc8532…`, equal to the commit tree. ffc3a8e (parents a596c76, e6a759de) → `a7c1bce0…`, equal to the commit tree. Neither merge has a file changed on both sides | inspection |
| E14 | `make check` in a local clone at head | rc 0: matrix, parameters, IDs (537 files), figures and links all OK | `head-make-check.log` |
| E15 | Lint `--lint-only -Wall` (the repository's flags), tops `KL_srp_talker_fsm`, `KL_srp_listener_fsm`, `KL_srp_top` | rc 0 and no warning for all three | `head-lint-srp.log` |
| E16 | Indicative area: sv2v + Yosys `synth_xilinx` of the two FSMs, base vs head | FF unchanged at 1x1 (455/389) and at N = 8 (1630/2334), so no register was added. 1x1 LUT 3842 → 3712. Generic synthesis only; this is not the Vivado OOC figure | `yosys-fsm-area{,-1x1}.log` |
| E17 | Hosted checks at the exact head (read-only snapshot) | `docs-gates` and `portability` succeeded in runs 37408875830 and 37408871633. `suites` was **in progress** in both, combined status `pending` | `hosted-check-runs.txt` |

## Same-clock pairs against Table 10-4 (registrar in LV, leavetimer! on the event's clock)

| Event on the expiry clock | Table 10-4, expiry first | Head result (both planes) | Graded by |
|---|---|---|---|
| rLv! | LV → MT (Lv), then MT `-x-` → **MT** | MT, one close (ACTIVE edge / TK_UNREGISTERED) | SC1 ev 5; SC2 (6416); E6/E7 |
| rLA! (registrar's lane) | → MT, then `-x-` → **MT** | MT, no replacement ARM | SC1 ev 6; E8 re-arm mutant |
| txLA! (own LeaveAll) | → MT, then `-x-` → **MT** | MT, no replacement ARM | SC1 ev 7 |
| rIn! / rMt! | → MT; no registrar effect → **MT** | MT | SC1 ev 2/4 |
| rNew! | → MT (Lv), then New, **IN** | IN with the received value; the obsolete timer is cancelled; no intermediate withdrawal published | SC1 ev 0; E8 |
| rJoinIn! / rJoinMt! | → MT (Lv), then Join, **IN** | as rNew! | SC1 ev 1/3; E8 |

The final state equals expiry-first in every row. For renewals, the head publishes the composed result and not the transient Lv/Join indication pair. This choice is stated and justified in 10 §6.5 `:566-577` and in README `:593-598`, and its separate REGISTERED/UNREGISTERED ordering hazard is explained. R488-2-S1 already records it as a suggestion; it stays non-blocking. A cancel for an already-expired slot is idempotent in `KL_pp_timer_service.sv:202-204` (`armed_r <= !arm_cancel_i`).

## Findings

### R488-3-R1: RESIDUE. The group-selector sentence omits `lvcoll`

- **Lenses:** Docs.
- **Where:** `tb/srp_top/README.md:246-247`: "`RUN_ARGS=phases`, …, `join` or `lvleave` selects one group for a focused run".
- **Evidence:** `tb/srp_top/sim_main.cpp:621` and `:2949` also accept `lvcoll`, and README `:557` documents it separately.
- **Impact:** Wording only. It changes no measurement, figure, test, code or clause claim.
- **Exact fix:** change it to "`join`, `lvleave` or `lvcoll` selects one group for a focused run".
- **Verification:** read-through, and `make check` stays green.

No BLOCKER, MAJOR or MINOR is open.

### Suggestions (non-blocking)

- **R488-3-S1 (Tests).** SC2 covers the integrated collision for `Lv` only. Renewals and LeaveAll on the expiry clock are graded at FSM level (SC1). That is what ruling 5990549074 item 3 asks for, but an integrated JoinIn sweep (expect IN, no STREAM_STOP) would close the remaining gap cheaply.

## Prior public review findings at this head

| Finding | Prior severity | State at ffc3a8e5 | Evidence |
|---|---|---|---|
| R488-1-F1: a same-clock rLv masks leavetimer!, so the 10 §6.5 statement is false at a reachable timing | MAJOR | **RESOLVED** (route (b)). The expiry is tested before rLv! on both planes (talker `:732-734`, listener `:769-772`). The listener's `ind_unreg_w` (`:449-454`) agrees with `reg_r`. 10 §6.5 `:566-577`, README `:497-600` and `sim_main.cpp:778-789` state the same-clock rule | E1 (6416/6416 CLOSED), E4, E6, E7 |
| R488-1-F2: stale run-length figure at `sim_main.cpp:364-365` | MINOR | **RESOLVED.** `:368` states 210,547,557, which equals the measured `TOTAL_CLOCKS` | E1 |
| R488-2-F1: README mutation record false for `lv-never-ends` | MINOR | **RESOLVED.** README `:539-548` states 16 (S1,S2) and 16 + 3016 SC2 (3032), from complete default runs | E5 |
| R488-2-F2: PR-body bank totals did not reconcile | MINOR | **RESOLVED.** The PR body names exact trees `579e3c59…` / `3c8b892c…` and has a 33-row per-suite table. Its columns sum to 1,021,640 and 1,028,224, and every row delta checks, for +6,584. I independently confirmed the two changing rows (srp_top 2200 → 8656, srp_stream_fsms 1219 → 1347). The banks at ffc3a8e5 are manager-owned | E2, E3 |
| R488-1-S-1 / R489-1-S3: T-MRP-LEAVE value restated in 10 §6.5 | SUGGESTION | Adopted. `:558` cites T-MRP-LEAVE, F08.1 and Table 4.3 with no value | inspection |
| R488-1-S-2: the peer `aged` premise accepts any decoded LeaveAll lane | SUGGESTION | Retained, non-blocking. `lv1_reg == 2` still pins LV entry | inspection |
| R488-2-S1: name the composed same-clock renewal in F01.4 terms | SUGGESTION | Retained, non-blocking. F01.4 is unchanged; 10 §6.5 states the choice | inspection |
| R489-1-S1 / R489-1-S2 | SUGGESTION | Retained, non-blocking. Unchanged since R489-2 | inspection |

The other independent reviewer's prior reports carry no BLOCKER, MAJOR, MINOR or RESIDUE.

## Lens ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table 10-4 rows rNew!, rJoinIn!/rJoinMt!, rLv!/rLA!/txLA!, leavetimer! against the talker registrar `:720-750` and the listener registrar `:747-799`; Δ13 scope; F08.1 / Table 4.3 (5000 ms, E1); the pair table above; E1, E4, E6-E8 | R488-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| RTL | CLEAN | Lane diff under `hdl/` (+13/-7, two files); branch priority and nonblocking reads; the pending-ARM guard; `ind_unreg_w` consistency; timer-service cancel idempotence; lint (E15); no port/parameter/register change; indicative area with FF unchanged (E16); merge reproduction (E13) | R488-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| Robustness | CLEAN | Same-clock sweep on both planes, own and peer (E1, E6, E7); renewal-on-expiry cancel path (E8); 300 M cycle budget vs 210.5 M run; snapshot file under `TMPDIR`, removed after each sweep; `--savable` leaves pre-existing records unchanged (E2) | R488-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| Tests | CLEAN | `srp_stream_fsms/sim_main.cpp:1069-1107` (SC1); `srp_top/sim_main.cpp:778-976` (S, SC2, SC3); `mutants.py` rows and coverage term; six checked-in and five reviewer mutants (E4-E9); planting audit (E10); D3 fix and its diagnostics (E11, E12); record equality vs base (E2, E3) | R488-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |
| Docs | CLEAN (R488-3-R1 is RESIDUE) | `10_srp_engine.md:548-577`; `tb/srp_top/README.md:11-14, 242-248, 497-600`; `tb/srp_stream_fsms/README.md:8, 218-232`; RTL and harness comments; measured values vs E1/E5/E9; PR body tables; `make check` (E14) | R488-3 | ffc3a8e5733202384e55ea9094569cca86b78261 |

## Integrity

`receipts/clone-integrity.txt`, after all probes:

- HEAD is `ffc3a8e5…` and the tree is `a7c1bce0…`.
- `git status --porcelain --ignored` is empty, and the worktree and index diffs are empty.
- Index (mode, blob, path) equals `ls-tree` (`ec7996f6…`).
- All 562 worktree files hash to their tree blobs, and their exec bits match the tree modes.
- There are 0 gitlinks: this repository has no submodules, so no gitlink check applies.

## Real limits

- **Area.** The Vivado OOC delta (−16 LUT, −3 FF, gate 40/40) was not reproduced: this review has no Vivado, and another Vivado job was running on the host. E16 is generic synthesis and only indicates that no register was added. The OOC figure is retained round-3b author evidence.
- **Public evidence.** The public tree (`pp134-r1`) binds only to round-1 head `5ab43bd9`. No published receipt binds the manager's source/static/builder and native banks to `ffc3a8e5`. I did not inspect them beyond the hosted snapshot (E17).
- **Not run, per the review rules:**
  - the processor-wide `scripts/run_suites.sh` bank, the full SRP and pp_top campaigns, and the Yosys bank (E10-E12 and E4 are focused subsets);
  - the parent consumer set at dev `28f9666f` with the #148 bench patch;
  - the builder/static banks.
- **Hosted `suites`.** The jobs had not concluded at snapshot time.
- **Specifications.** I did not read the specification PDFs. The clause readings rest on the repository's quotations and the reviewer's reading of the tables.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof, and nothing here is hardware evidence.
- **Current-dev candidate.** The final candidate (source base `ead8036…`, live dev `28f9666f…`) is distinct from this source validation and was not built.

## Pending manager duties

- Hosted/act acceptance at `ffc3a8e5`, including the in-progress `suites` jobs.
- The parent consumer run at dev `28f9666f` with only the #148 bench patch, and the merge-turn current-dev candidate build.
- Publish or bind the source/static/builder and native bank receipts for `ffc3a8e5`.
- Carry R488-3-R1 to the residue checklist, and the suggestions at the manager's discretion.
- Apply the merge bar of two independent positive reviews and the full completion bar.

R488-3 FINISHED
