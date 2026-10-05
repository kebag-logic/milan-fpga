[R489] POSITIVE - exact head 5ab43bd98209ef3cde206b325c06f0e7405e1e86

# R489-1: external independent review of processor issue #134 / PR #160

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #160 (`pp134-lv-leave` into `main`)
- Exact head `5ab43bd98209ef3cde206b325c06f0e7405e1e86`, tree `fbe1f7b8e626e707333bd5f2f00b4fed02bd0ce0`; PR base `ead8036035affd53ef4b29979190f2f4f67084c0` (ancestor of the head, two commits: `68b0e615`, `5ab43bd9`)
- Reviewed in an isolated detached clone at the exact head. All runs used disposable trees under the packet's `scratch/`.
- Verilator: the scoped pinned launcher, identity `Verilator 5.050 2026-07-01 rev v5.050`. It was called through `scripts/vl-wrap.sh`, which only caps the build's `-j 0` at 3 threads.

## Verdict

POSITIVE. The new `srp_top` group `lvleave` (checks S1-S3, 8 cases) does what issue #134 asks:
- Both an own and a peer LeaveAll move the Listener registrar to LV before the peer's `Lv` arrives. This is shown in the registrar trace, not just in the timing.
- Both `Lv`s meet LV and change nothing.
- The registration and ACTIVE stay until the leave timer expires, 5000 ms after the LeaveAll. They then close with exactly one ACTIVE fall (STREAM_STOP) and one `LISTENER_REG_CHANGE`.

Both new mutants fail the group for the right check, the control passes, and neither mutant fails any base check. The diff contains no RTL change. The docs paragraph states the behaviour with the clause. The README counts are the base counts plus exactly the new group. No BLOCKER, MAJOR, MINOR or RESIDUE is open. Three SUGGESTIONs follow.

## Reconstruction (order followed)

1. Contributor docs. The repository has no `AGENTS.md` or `CONTRIBUTING.md` at any depth (searched). I read the root `README.md` and `docs/README.md`, the author conventions: single-source timing rule §2, citation rules §4.
2. Scope.
   - Issue #134 body (frozen acceptance 1-3).
   - Manager lane comment 5988316116: arm for both an own and a peer LeaveAll; cite Table 10-4 rLv! in LV; record the leave time against Milan Table 4.3; two mutants recorded in the README; docs with the clause; no RTL change (STOP if the RTL is wrong).
   - TAKEN 5988324405 and REVIEW READY 5990196588.
3. Authorities in the repo.
   - F08.1 `docs/architecture/08_timing.md:40`: T-MRP-LEAVE 5000 ms (4500-7500), Milan Table 4.3.
   - REQ-SRP-001 `docs/00_MILAN_COMPLIANCE_REVIEW.md:498`: Table 4.3 LeaveTime 5000 ms (4500-7500).
   - F01.4 Δ13 `docs/architecture/01_overview.md:143`: Milan §4.2.7.2.2, `IN / rLv!` goes to MT with no leavetimer.
   - 02 §4.6 and the §6 `streaming[src]` row: the integrator owns STREAM_START/STREAM_STOP.
   - Integrator guide: `srp_active_o` (`docs/guides/integrator.md:533`).
4. Diff `ead8036..5ab43bd9` (6 files, +235/-4) and history. Then the public evidence at milan-fpga `7aecfd0b/review-evidence/pp134-r1`: `MANIFEST.json`, plus `author/HANDOFF.md` (sha256 `fb077d45…`, matches the manifest's published hash). I also read the PR body and PR comments. At reading time the PR had only the two review-start notices. It had no review findings and no PR review objects, so there are no prior public findings to resolve or retain at this head.

## Lens results

### Conformance: CLEAN
- **802.1Q-2014 Table 10-4 reading.**
  - The row `rLv! | rLA! | txLA! | Re-declare!` reads: IN → "Start leavetimer", LV; LV → `-x-`.
  - `leavetimer!` in LV → Lv, MT.
  - rNew!/rJoinIn!/rJoinMt! in LV → Stop leavetimer, IN.

  The arm comment (`tb/srp_top/sim_main.cpp:773-783`), the README (`tb/srp_top/README.md:497-506`) and 10 §6.5 (`docs/architecture/10_srp_engine.md:548-565`) all state this reading. They are consistent with Δ13, which replaces only the IN/rLv! cell. The RTL matches: `hdl/srp/KL_srp_talker_fsm.sv:729-740` (rLv! in LV has no branch; the expiry in LV → MT). So does the listener-side registrar that 10 §6.5 also names: `hdl/srp/KL_srp_listener_fsm.sv:766-779`. Its Lv-in-LV behaviour is already graded by the existing `listener-strict-lv`/K11 row.
- **Leave time.**
  - `LEAVE_MS_P` = 5000 (`hdl/srp/KL_srp_top.sv:106`). The suite wrapper does not override it (`tb/srp_top/srp_top_wrap.sv`). The processor top does not override it either (`hdl/top/protocol_processor_top.sv:2494-2506` passes no `LEAVE_MS_P`).
  - The trace shows the arm deadline is the LeaveAll ms + 5000 (`REGTRACE ... arm slot=16 cancel=0 deadline=19200` for a LeaveAll at 14200; `deadline=5705` for 705).
  - Measured close: 5000 ms after the LeaveAll in all 8 cases. That is Milan v1.2 Table 4.3's LeaveTime default, inside 4500-7500 ms (the range recorded in REQ-SRP-001 and F08.1).
  - I had no copy of the specifications to consult. The clause reading is checked against the standard's published table structure and the repository's own recorded quotes.
- No conformance claim in the diff contradicts the RTL or the measured trace.

### RTL: CLEAN
- `git diff --name-status ead8036..5ab43bd9` lists only `docs/architecture/10_srp_engine.md`, `tb/srp_top/{README.md,mutants.py,sim_main.cpp}` and two new files under `tb/srp_top/mutations/`. `git diff --stat ... -- hdl syn scripts .github Makefile` is empty. No RTL, port, parameter, synthesis or CI change.
- The issue's STOP condition was not triggered: the probe trace shows the unchanged RTL behaving as Table 10-4 requires.
- The two mutant patches touch only scratch copies, through the campaign driver (`git apply --check`, then `git apply`, in a temp copy).

### Robustness: CLEAN (one SUGGESTION)
- **The arm reaches LV before the `Lv`, from the registrar state.**
  - The harness reads `dbg_t_reg_o` (registrar {0 MT, 1 IN, 2 LV}) into `lv1_reg` before it feeds the first `Lv` (`sim_main.cpp:823`, `:836`) and into `lv2_reg` before the second. S1 requires both to equal 2.
  - Independently, my trace probe (`receipts/probe-diffs/trace.diff`, display-only, 24/24 PASS) logs the registrar state at the clock each Listener `Lv` reaches the target's registrar. In all 16 deliveries it reads `reg_at_rx=2` (LV).
    - Own: IN→LV at 14200, `Lv` at 14214 and 16700, expiry at 19200, LV→MT.
    - Peer: IN→LV at 705, `Lv` at 710 and 3205, expiry at 5705.
  - The other registrations go back to IN on the bridge's re-joins, and their slots are cancelled (`cancel=1`). So only the target ages. (`receipts/probe-trace.log`)
- **Timing tolerance.** S2 accepts a close 5000-5001 ms after the LeaveAll. Probes show the window is tight: `leave-5002` fails S2 in all 8 cases; `leave-4998` fails S1 and S2 in all 8.
- **The precondition is graded per cause.**
  - `own-la-no-age` (own LeaveAll stops aging the registrar) fails S1 and S2 for the 4 own cases only.
  - `peer-la-no-age` fails S1 and S2 for the 4 peer cases only.
- **Plausible wrong readings are caught.**
  - `lv-restarts-timer` (an `Lv` in LV restarts the timer) fails S2 and S3 in 8 of 8.
  - `lv-in-lv-ends-now` fails S1 and S2 in 8 of 8, closing 14 ms / 5 ms after the LeaveAll.
- Determinism: the control, the head suite, the trace probe and the published handoff all give identical `LV_LEAVE` lines.
- See R489-1-S1 below. Taken alone, the arm cannot tell an `Lv` that was ignored from one that was never delivered.

### Tests: CLEAN
- **Focused group, control** (`receipts/mutants-head/control-srp_top-lvleave.log`): `24 checks: 24 PASS, 0 FAIL`. The 8 `LV_LEAVE` lines match the README and the PR body: own 14200 / 14216,16700 / 19200; peer 705 / 711,3205 / 5705; leave_time 5000; stop 1, start 0.
- **Campaign driver** (`receipts/mutants-head.log`; `mutants.py --only lv-second-lv-ends,lv-never-ends --jobs 3`, run from a scratch copy of the head):
  - `control srp_top lvleave: rc=0 PASS`
  - `lv-second-lv-ends: rc=2 failures=16 KILLED tags=S1,S2`, closing at 2500 ms, the second `Lv`, in all 8 cases. Its required assertion is `S1:`, the right check: the registration must survive the second `Lv`.
  - `lv-never-ends: rc=2 failures=16 KILLED tags=S2,S3`, never closing. Its required assertion is `S2:`, the right check: the close at expiry.
  - `3 checks: 3 PASS, 0 FAIL`
- **Only the new group kills them.** The complete default base suite (`ead8036`) with each mutant planted gives `2200 checks: 2200 PASS, 0 FAIL` plus the 4×15 storage arms, rc 0, for both mutants (`receipts/srp_top-full-base-planted-*.log`).
- **README cross-check of the older patches.** Run through `lvleave`, `talker-strict-lv` fails 16 checks (S1, S2; closes at 14 / 5 ms) and `talker-no-expiry` fails 16 checks (S2, S3; never closes) (`receipts/old-*-lvleave.log`). Both match the README's claim.
- **Coverage gate.** `mutants.py:248` adds `("S", 3)`. S1, S2 and S3 are each killed by at least one row (S1 by the first arm, S2 by both, S3 by the second).
- **Head versus base, full default `make -C tb/srp_top`.**
  - Head: rc 0, storage 4×`15 checks: 15 PASS`, `2224 checks: 2224 PASS, 0 FAIL`.
  - Base: rc 0, the same storage lines, `2200 checks: 2200 PASS, 0 FAIL`.
  - The normalised logs differ in exactly the 8 `LV_LEAVE` lines and the tally line (`receipts/srp_top-full-base-vs-head.diff`).

### Docs: CLEAN (two SUGGESTIONs)
- **10 §6.5 (`docs/architecture/10_srp_engine.md:548-565`, anchor `sec-10-lv-withdrawal`)** states the LV-case behaviour with the clause:
  - Table 10-4, rLv! in LV is `-x-`, and leavetimer! in LV is Lv, MT.
  - Δ13 covers only the IN cell.
  - The close is at T-MRP-LEAVE (F08.1), Milan Table 4.3 LeaveTime.
  - One `LISTENER_REG_CHANGE` and one ACTIVE fall.
  - A re-declaration before expiry returns the registrar to IN.
  - It links the suite.

  This meets acceptance item 2.
- **Suite README counts.**
  - Line 14: `2224 checks`, which is 2200 + the group's 24, measured.
  - Line 247: the group list adds `lvleave`.
  - The new section (`:497-549`) records the group, the cases, S1-S3, the leave-timer value against Table 4.3, the measured values, both mutants (16 failures each, tags S1,S2 / S2,S3) and the older-patch cross-check. All match my receipts.
  - The campaign totals (128 → 131 = + control + 2 arms; coverage 80 → 83 = + S1-S3) appear only in the PR body. They are consistent with the `mutants.py` diff: 2 rows and one new group pair (one control), plus 3 coverage tags.
- `make check` on a scratch copy of the head: rc 0. Lint: 41 mermaid + 18 wavedrom blocks; links 1140; matrix 115 REQ rows, 94 rows, 0 untested; parameters 28 (`receipts/make-check-head.log`).

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R489-1-S1 | SUGGESTION | Tests, Robustness | `tb/srp_top/sim_main.cpp:819-848` | Probe `harness-no-lv` (removes both `Lv`s from the stimulus) still passes 24/24 (`receipts/probe-harness-no-lv.log`) | S1's "both Lvs meet LV" is not observed by the plain suite alone. That the `Lv`s are delivered is shown at this head by the trace probe and by both campaign arms. If delivery broke, the campaign would report the arms UNPROVEN, so the gate set still catches it | Optional: add an observation in the group that the target's Listener `Lv` was decoded (for example a decoded-event strobe or count already on a debug face), so the plain suite fails if the `Lv` never arrives | Re-run `harness-no-lv`; it should then fail S1 |
| R489-1-S2 | SUGGESTION | Docs | `tb/srp_top/README.md:519-521`; `sim_main.cpp:354-357` | 02 §6 `streaming[src]` row: the integrator's STREAM_START/STREAM_STOP count edges of its own `streaming` level. The harness counts `srp_active_o` edges | The proxy is sound for an integrator that gates its talker on ACTIVE (integrator guide `:533`). The wording "as the integrator's ... counters do" could be read as the processor counting STREAM_STOP itself | Optional wording: "counts every edge of ACTIVE, the licence the integrator's `streaming` level follows; its STREAM_START / STREAM_STOP counters count that level's edges (02 §4.6)" | Read-through |
| R489-1-S3 | SUGGESTION | Docs | `docs/architecture/10_srp_engine.md:558-559` | `docs/README.md` §2 single-source rule: timing values live in F08.1. The paragraph cites T-MRP-LEAVE and F08.1, then restates "5000 ms" and "(4500–7500 ms)". There is precedent in the same section (`:708`, `:723`), and `make check` passes | No wrong value. Only a second copy of the F08.1 value | Optional: keep only "T-MRP-LEAVE after the LeaveAll ([F08.1]), Milan v1.2 Table 4.3 LeaveTime" and leave the figures to F08.1 and the suite README | `make check` |

No BLOCKER, MAJOR, MINOR or RESIDUE.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 802.1Q-2014 Table 10-4 reading in `sim_main.cpp:773-783`, `README.md:497-506`, `10_srp_engine.md:548-565`; Δ13 (F01.4); F08.1 / REQ-SRP-001 (Table 4.3 LeaveTime); talker and listener registrar RTL; trace deadline and close times | R489-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| RTL | CLEAN | `git diff --name-status`/`--stat` base..head (no `hdl/`, `syn/`, `scripts/`, CI change); `LEAVE_MS_P` plumbing (`KL_srp_top.sv:106`, wrapper, `protocol_processor_top.sv:2494`) | R489-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| Robustness | CLEAN | registrar trace probe (16 of 16 `Lv`s at LV); timing-window probes 5002 / 4998; per-cause aging probes; wrong-reading probes (restart, end-now); harness-no-lv limit probe | R489-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| Tests | CLEAN | control 24/24; campaign 3/3 (both arms KILLED for S1: / S2:); base suite with each mutant planted 2200/2200; older patches 16 failures each; full head 2224/2224 vs base 2200/2200, diff = 8 `LV_LEAVE` lines + tally | R489-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| Docs | CLEAN | 10 §6.5 paragraph; suite README count line, group list, new section; PR body campaign counts; `make check` rc 0 | R489-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |

## Commands run (all in the foreground or polled from the foreground; logs in `receipts/`)

- `scripts/prep_trees.sh`: `git archive` of the head and base, the base with each new mutant planted, the head with each older patch planted, and the probe trees (`scripts/make_probes.py`; exact-anchor edits, diffs in `receipts/probe-diffs/`).
- `scripts/run_all.sh <packet> 1`:
  - `make -C tb/srp_top` at head and base;
  - `python3 tb/srp_top/mutants.py --only lv-second-lv-ends,lv-never-ends --jobs 3` with `TMPDIR` under `scratch/`;
  - 8 probes, `make -C tb/srp_top RUN_ARGS=lvleave`, two at a time.
- `scripts/run_all.sh <packet> 2`: the base full suite with each new mutant planted.
- The older patches on `lvleave`: `make -C tb/srp_top RUN_ARGS=lvleave` in `scratch/old-*`.
- `make check` in a separate scratch copy of the head.
- `scripts/verify_clone.py <clone> <head> <tree>`, run after every probe.
- Peak concurrency: 7 Verilator builds at 3 threads each. No Vivado run and no shared install.

Every rc file is in `receipts/`.
- rc 0: `srp_top-full-head`, `srp_top-full-base`, `srp_top-full-base-planted-*`, `mutants-head`, `probe-trace`, `probe-harness-no-lv`, `make-check-head`.
- rc 2: the six fault probes and the two older-patch runs. Each is a red group, as expected.
- In the published logs, the pinned tool's install root is replaced by `<PINNED_VERILATOR_ROOT>`.

## Restoration

I never edited the review clone; every probe ran in `scratch/`. After the probes, `receipts/clone-integrity.txt` shows:
- HEAD `5ab43bd9…`; tree, and index tree from `git write-tree`, `fbe1f7b8…`;
- `git status --porcelain --ignored --untracked-files=all` empty;
- the index (mode, blob, path) equal to HEAD's tree;
- all 560 working files byte-identical (`git hash-object --no-filters`), with matching executable bits;
- 0 gitlinks. The tree has no submodules, so there are no gitlinks to verify.

## Real limits

- No specification PDFs were available to me. Table 10-4 and Table 4.3 are checked against the standard's table structure as cited and the repository's recorded quotes (REQ-SRP-001, F08.1, F01.4).
- Not run by me, as scoped:
  - `scripts/run_suites.sh` (all suites), `scripts/lint_hdl.sh`, Yosys, `gen_matrix.py --check` (its matrix part is covered by `make check`);
  - the full `tb/srp_top/mutants.py` campaign (131 rows) and `tb/srp_admission/mutants.py`;
  - the 17 parent consumer gates with the gitlink staged.

  These are the author's, per the published HANDOFF, and the manager's to accept.
- The public evidence directory at milan-fpga `7aecfd0b` holds the author's HANDOFF, PR body and four adoption patches. I found no manager bank receipts there. The statement that the manager's source banks passed at this head is the manager's, and I did not verify it.
- **Hosted, exact head** (`receipts/hosted-check-runs.txt`, snapshot 07:52Z): `docs-gates` success ×2, `portability` success ×2 (executed jobs); `suites` in progress ×2 at the snapshot, so not evidence. No skipped context was observed.
- Physical calibration NOT RUN. No hardware was used, and simulation is not hardware proof. The bench case (milan-fpga #608) is cited, not reproduced.
- The STREAM_STOP count is the processor-side ACTIVE edge count (R489-1-S2). The integrator's counter itself is outside this repository.

## Pending manager duties

- The final current-dev candidate at the merge turn (source base `ead8036`, live dev `fa450d30`), and its banks.
- Hosted/act acceptance, including the `suites` job still in progress at this head.
- Acceptance item 3: the donor gates and the parent consumer gates with the gitlink staged.
- The second independent review (R488) and the completion bar; carrying the three SUGGESTIONs at the manager's discretion (no RESIDUE to carry).

R489-1 FINISHED
