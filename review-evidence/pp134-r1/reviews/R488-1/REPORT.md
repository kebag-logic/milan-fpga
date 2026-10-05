[R488] NEGATIVE - exact head 5ab43bd98209ef3cde206b325c06f0e7405e1e86

# R488-1 internal independent review: issue #134 / PR #160

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #160 (`pp134-lv-leave` into `main`).
- Exact head `5ab43bd98209ef3cde206b325c06f0e7405e1e86`, tree `fbe1f7b8e626e707333bd5f2f00b4fed02bd0ce0`. Base `ead8036035affd53ef4b29979190f2f4f67084c0`.
- Review start: PR #160 comment 5990217845. Cleared-context pass with a detached clone of its own. All probes ran on `git archive` extractions under the packet's `scratch/`. The clone was never modified (see Integrity).
- Simulator: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…e92f`, `receipts/verilator-identity.txt`).

## Verdict summary

The arm itself is good. It does what the issue scopes:
- The registrar trace shows LV before each `Lv`, in all eight cases.
- The close comes at leavetimer!, 5000 ms after the LeaveAll, with exactly one STREAM_STOP.
- Both mutants fail the arm for the right checks, and the control passes.
- The README counts are the base plus exactly the new group.
- No RTL changed.

The verdict is NEGATIVE for two reasons:

- **F1 (MAJOR).** The new 10 §6.5 paragraph (and the suite README) states without exception that an `Lv` in LV "changes nothing, however often it repeats" and that the registration ends at leavetimer!. That is false at one reachable timing. The RTL that this PR documents and grades (unchanged, pre-existing) drops the leave-timer expiry when the same registrar's `Lv` decodes on the expiry clock. The registration and ACTIVE then stay up indefinitely.
- **F2 (MINOR).** A present-tense measured figure in a hunk-adjacent comment of `tb/srp_top/sim_main.cpp` is stale at this head.

## Reconstruction

1. **Contributor guides.** The repository has no AGENTS.md or CONTRIBUTING.md at this head; `find` over the tree found neither. I read the conventions from `README.md` and `docs/README.md`. The ones that matter here:
   - the §2 single-source rules ("Timing values only in F08.1");
   - the §4 citation style;
   - `make check` as the documentation gate.
2. **Issue #134 (frozen acceptance).**
   - The arm passes, both mutants turn red, and they are recorded in the suite README.
   - 10_srp_engine.md states the LV-case behaviour with the clause.
   - Donor gates and parent consumer gates pass.

   The maintainer's lane comment adds four rules:
   - run both an own and a peer LeaveAll;
   - cite Table 10-4 (rLv! in LV);
   - record the leave-timer value against Milan Table 4.3;
   - "No RTL change. If the arm shows the RTL does not behave as the clause requires, STOP with the trace."
3. **Authorities.**
   - 802.1Q-2014 Table 10-4, the registrar state table. Row `rLv! || rLA! || txLA! || Re-declare!`: IN gives "Start leavetimer" and LV; LV gives `-x-`. Row `leavetimer!`: LV gives Lv and MT.
   - Milan v1.2 §4.2.7.2.2, Δ13 (`docs/architecture/01_overview.md:143`), which replaces only the IN / rLv! cell.
   - Milan v1.2 Table 4.3 LeaveTime: 5000 ms (4500–7500). The repository carries it as REQ-SRP-001 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:498`) and as F08.1 T-MRP-LEAVE (`docs/architecture/08_timing.md:40`).
   - The specification PDFs are not distributed. The clause readings above rest on the repository's own quotations and on the reviewer's reading of the standard's table. Nothing in the repository contradicts them.
4. **Diff `ead8036..5ab43bd9`.** Two commits, six files, +235/-4. `git diff --name-status` shows only:
   - `docs/architecture/10_srp_engine.md`
   - `tb/srp_top/README.md`
   - `tb/srp_top/mutants.py`
   - two new `tb/srp_top/mutations/*.patch`
   - `tb/srp_top/sim_main.cpp`

   The diff under `hdl/`, `syn/`, `scripts/` and `.github/` is 0 lines (`receipts/clone-integrity.txt`). **No RTL changed.**
5. **Public evidence.** milan-fpga `7aecfd0b…/review-evidence/pp134-r1`:
   - `MANIFEST.json` lists the author HANDOFF (path-redacted), PR-BODY and four parent adoption patches.
   - The published PR-BODY.md (sha256 `b0bf7061…`) is byte-identical to the live PR body, apart from trailing whitespace.
   - The HANDOFF's measured table (LeaveAll 14200/705 ms, close 19200/5705 ms, 5000 ms in all eight cases, 16/24 per mutant, campaign 131/131 with coverage 83/83) matches my own runs exactly.
   - The issue and the PR carry no manager evidence comments beyond the lane assignment and the two review-start notes.
   - Parent consumer and builder/static banks were not re-run (not allowed). They stay manager-owned (see Pending manager duties).
6. **Prior public review findings on PR #160: none.** The PR has 0 reviews, 0 review comments, and only the two review-start comments. There is nothing to resolve or retain.

## Executed evidence (reviewer runs, this head)

| # | What | Result | Receipt |
|---|---|---|---|
| E1 | Complete default `tb/srp_top` suite, base vs head | base rc 0, `2200 checks: 2200 PASS, 0 FAIL`; head rc 0, `2224 checks: 2224 PASS, 0 FAIL`; storage arms 4 × 15 at both. Normalised output differs only by the 8 `LV_LEAVE` lines and the tally (+24) | `receipts/srp_top-full-{base,head}.log/.rc` |
| E2 | `mutants.py --only lv-second-lv-ends,lv-never-ends --jobs 3` | control `srp_top lvleave` PASS; `lv-second-lv-ends` 16 failures, tags S1,S2, KILLED; `lv-never-ends` 16 failures, tags S2,S3, KILLED; `3 checks: 3 PASS` | `receipts/mutants-new-head.log`, `receipts/mutants-head/` |
| E3 | Full `tb/srp_top/mutants.py --jobs 6` at head | rc 0, `assertion coverage: 83/83`, `131 checks: 131 PASS, 0 FAIL` | `receipts/mutants-full-head.log`, `receipts/mutants-full-head/` |
| E4 | Each new mutant through the **complete** head suite | both `2224 checks: 2208 PASS, 16 FAIL`, and the failures are only S lines (8 × S1 + 8 × S2; 8 × S2 + 8 × S3). Storage arms 4 × 15 pass. No other check fails | `receipts/arm-full-*.log` |
| E5 | Older `talker-strict-lv` / `talker-no-expiry` through `lvleave` | 16/24 each: S1,S2 closing at 14 ms (own) or 5 ms (peer) after the LeaveAll; S2,S3 with no close. This matches the README's claim | `receipts/arm-lvleave-*.log` |
| E6 | Registrar trace (sim-only `$display` monitor; patch `scripts/probe-registrar-monitor.patch`), group `lvleave` | 24/24. In every case: `reg 1->2` on the sLA / received Listener-lane LeaveAll; leave slot armed with `deadline_ms = LeaveAll + 5000`; non-targets re-joined (`2->1`, cancel); **both `rLv reg_before=2`** (LV), the first 14 ms (own) or 5 ms (peer) after the LeaveAll and the second at +2500 ms; `leavetimer_expiry reg_before=2` and `reg 2->0` at exactly +5000 ms | `receipts/probe-trace-lvleave.log` |
| E7 | Same-clock probe `lvcoll` (scripts below): `Lv` start swept k = 0..400 clocks before the calibrated close, peer LeaveAll, fp Ready/ReadyFailed × source 0/7 | 400 of 401 offsets CLOSED. **k = 19 STUCK in all four**: `COLLIDE rLv_and_expiry_same_clock reg_before=2`, then reg 2 (LV), `lstn_reg_state` published, ACTIVE 1, 0 STREAM_STOP | `receipts/probe-lvcoll-fp{2,3}-src{0,7}.log` |
| E8 | k = 18..20 held 40 s after the expiry | k = 19 still LV / ACTIVE 1 / 0 STREAM_STOP at 45 705 ms, after three own LeaveAlls (15200, 26800, 38400 ms). k = 18 and k = 20 close normally | `receipts/probe-lvcoll-hold40s.log` |
| E9 | Complete-run DUT clocks, base vs head (counter print added in scratch) | base **185,012,669** (equal to the `sim_main.cpp:365` comment); head **189,637,549** | `receipts/clock-count-{base,head}.log` |
| E10 | `make -k check` on a head extraction | rc 0: 41 mermaid + 18 wavedrom, links 1140, 115 REQ, 94 rows / 0 untested, 28 parameters | `receipts/make-check-head.log` |
| E11 | Hosted checks at the exact head (read-only snapshot, 2026-10-05 ~09:55 CEST) | `docs-gates` and `portability` succeeded in both workflow runs (37279101523, 37279096094); `suites` was **in progress** in both, not concluded. Combined status `pending` | `receipts/hosted-check-runs.txt` |

Scripts (portable; they take the packet directory as an argument):
- `scripts/run_campaigns.sh` (E1, E2);
- `scripts/run_mutant_probes.sh` (E3–E5);
- `scripts/probe-registrar-monitor.patch` with `scripts/probe_lvcoll.py` (E6–E8);
- `scripts/clock_count.sh` (E9).

As run, `run_mutant_probes.sh` lost the E4/E5 rc files: its subshell inherited `set -e`. I read the verdicts from each log's tally and from make's `Error 1` lines, and fixed the script afterwards (commented in place). No other receipt is affected.

## Findings

### F1: MAJOR. A same-clock rLv masks leavetimer!, so the new section 6.5 statement is false at a reachable timing

- **Lenses:** Conformance, RTL, Robustness, Docs.
- **Where:**
  - `docs/architecture/10_srp_engine.md:554-560`: "An `Lv` that then arrives … changes nothing, however often it repeats … ACTIVE stays high until leavetimer! … The registration then ends".
  - `tb/srp_top/README.md:504-505`: "So the `Lv` changes nothing, and the registration and ACTIVE end when the leave timer expires".
  - The comment at `tb/srp_top/sim_main.cpp:779`.
  - The cause, pre-existing and unchanged: `hdl/srp/KL_srp_talker_fsm.sv:729-740`. The `rLv` branch (`:729`) precedes the expiry branch (`:737-739`) in one `if / else if` chain, and `exp_valid_i` is a single-clock strobe with no handshake (`:164`). The listener-side registrar has the same ordering (`hdl/srp/KL_srp_listener_fsm.sv:766-779`), found by inspection only, not probed. There, `ind_unreg_w` (`:449-454`) still fires on that clock and requests a withdrawal while `reg_r` stays LV.
- **Authority:** 802.1Q-2014 Table 10-4. rLv! in LV is `-x-`, and leavetimer! in LV is Lv and MT. Taken in either order, the two events end in MT. The RTL ends in LV, with no timer pending, which neither order produces. Δ13 (Milan §4.2.7.2.2) touches only IN / rLv!.
- **Evidence:** E7 and E8. In all four combinations, an `Lv` that decodes on the expiry clock (k = 19) leaves the Listener registration published and ACTIVE high, with 0 STREAM_STOP. That state was still there 40 s later, through three own LeaveAlls. A LeaveAll only ages IN registrars (`:735`), so nothing re-arms the timer. Only a registering event or a gate re-open clears it. The arm's own cases (E6) do not reach this timing, so S1–S3 pass.
- **Impact:** The documentation this PR adds certifies, as the clause's behaviour, something the landed RTL does not do at one reachable timing. The consequence is unbounded: a talker keeps its stream licence and keeps streaming with no listener, and the integrator's STREAM_STOP never counts. Per occurrence the probability is small (one clock per withdrawal that meets LV), but nothing ever recovers it. The lane rule ("if the RTL does not behave as the clause requires, STOP") was not triggered only because the arm never landed an `Lv` on the expiry clock.
- **Required outcome:** A maintainer ruling, then one of the following.
  - **(a)** Keep this PR test-and-docs only. Qualify the 10 §6.5 paragraph, the README section and the `sim_main.cpp:779` comment with the same-clock exception, and link a newly opened, tracked RTL issue covering both the talker and the listener registrar planes.
  - **(b)** Widen the scope to an RTL fix, so that an expiry for an LV registrar is never lost to a same-clock rLv, with a lane arm that lands the `Lv` on the expiry clock.

  Either way the documentation must not state the unconditional behaviour while the RTL does not provide it.
- **Verification:**
  - For (a): the qualified text and the issue link are present at the new head.
  - For (b): `scripts/probe_lvcoll.py` plus the monitor patch over k = 0..400 reports CLOSED at every k, including the COLLIDE clock, for the talker plane, and a listener-plane equivalent does the same.
  - In both cases, E1/E3 stay green.

### F2: MINOR. A stale present-tense run-length figure in the harness comment

- **Lenses:** Tests, Docs.
- **Where:** `tb/srp_top/sim_main.cpp:364-365`, in `H::step()` (the PR's hunk at `:351-362` sits directly above it): "The complete default run takes 185,012,669 (the P8 arm-delay sweep 53.3 M)."
- **Evidence:** E9. Base: exactly 185,012,669 clocks. Head: 189,637,549 (+4,624,880, the new group). The README's mention (`tb/srp_top/README.md:242-243`) is phrased historically and stays true.
- **Impact:** The comment justifies the 300,000,000-clock budget with a measured figure that is wrong at this head. The margin is still sufficient (63 %), so no check changes. Because a measured figure is involved, this is not RESIDUE.
- **Required outcome:** State the head's figure (189,637,549), or rephrase it as a dated historical measurement.
- **Verification:** `scripts/clock_count.sh` on the new head prints a `R488_TOTAL_CLOCKS` value that matches the comment.

### Suggestions (non-blocking)

- **S-1 (Docs).** `10_srp_engine.md:558-559` restates the T-MRP-LEAVE value ("5000 ms", "4500–7500 ms") beside the F08.1 link. `docs/README.md` §2 says "Timing values only in F08.1". The same file has precedent (§6.5 "10–15 s"), and `make check` does not enforce the rule, so this is not a finding. Consider citing `T-MRP-LEAVE` / F08.1 alone and leaving the Table 4.3 value to the suite README, where the issue asked for it.
- **S-2 (Tests).** In the peer case, S1's `aged` term accepts any received MSRP LeaveAll lane (`dbg_rx_la_o != 0`), but the README says "the peer's Listener lane". The `lv1_reg == 2` term does pin LV entry, which only the Listener lane or an own sLA can cause, so the check is sound. The wording could still say what is measured.

## Lens ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Table 10-4 rows rLv!/rLA!/txLA! and leavetimer! against `KL_srp_talker_fsm.sv:654-757` and `KL_srp_listener_fsm.sv:747-785`; Δ13 (`01_overview.md:143`); Table 4.3 LeaveTime vs `LEAVE_MS_P` 5000 and F08.1; E6 trace (LV before both `Lv`s, close at +5000 ms); E7/E8 | R488-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| RTL | UNCLEAN (F1) | 0-line diff under `hdl/` (`receipts/clone-integrity.txt`); registrar plane priority chains (talker, listener); timer-service strobe; both mutant patches against the RTL context (they apply cleanly via `git apply --check`, E2/E3) | R488-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| Robustness | UNCLEAN (F1) | same-clock rLv/expiry sweep (E7), 40 s persistence through three own LeaveAlls (E8); reset handling of the new edge counters (`sim_main.cpp:459`); cycle budget margin (E9) | R488-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| Tests | UNCLEAN (F2) | `check_withdrawal_meets_an_lv_registrar` (`sim_main.cpp:773-871`), the edge/LRC counters (`:354-393`), group dispatch (`:617`, `:2843`); `mutants.py` rows and the S coverage term; E1–E5 (control passes; `lv-second-lv-ends` fails S1,S2 by a close at +2500 ms; `lv-never-ends` fails S2,S3 with no close; no other check fails under either); stale run-length figure (`:365`) | R488-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |
| Docs | UNCLEAN (F1) | `10_srp_engine.md` §6.5 new paragraph (`:548-565`: Table 10-4, Δ13 scope, Table 4.3, anchor `sec-10-lv-withdrawal`); suite README §"A withdrawal that meets an LV registrar" (`:497-549`), the group list (`:247`) and the count (`:14`, 2200 → 2224 = base + the group's 24); measured values vs E1/E6; `make check` (E10); PR body vs published PR-BODY.md | R488-1 | 5ab43bd98209ef3cde206b325c06f0e7405e1e86 |

## Integrity

Read from `receipts/clone-integrity.txt`, checked after all probes:
- The clone is at HEAD `5ab43bd9…`, tree `fbe1f7b8…`.
- `git status --porcelain --ignored` is empty.
- The worktree and index equal HEAD.
- Index (mode, blob, path) equals `ls-tree`.
- Worktree `hash-object` equals the tree blobs for all 560 files, and the exec bits equal the tree modes.
- There are 0 gitlinks: this repository has no submodules, so no gitlink applies.

Every probe ran in scratch extractions. The clone was never built in or patched.

## Real limits

- I did not read the specification PDFs. The Table 10-4 and Table 4.3 readings rest on the repository's quotations (REQ-SRP-001, F08.1, F01.4) and the reviewer's reading of the standard.
- The listener-plane form of F1 comes from inspection only, not a probe.
- Not run, per the review rules: the processor-wide `scripts/run_suites.sh`, lint and Yosys banks, `tb/srp_admission/mutants.py`, and the parent consumer set of 17 and the builder/static banks. The published evidence reports them green at this head. I did not re-execute them.
- The hosted `suites` jobs had not concluded at snapshot time (E11).
- Physical calibration was NOT RUN. Field skips are not hardware proof, and none of this review is hardware evidence.
- The final current-dev candidate (source base `ead8036…`, live dev `fa450d30…`) has not been built. It is distinct from this source validation.

## Pending manager duties

- Rule on F1's route, (a) or (b), and on the issue for the pre-existing RTL ordering.
- Carry F2.
- Own hosted/act acceptance, including the in-progress `suites` jobs at this head.
- Build the merge-turn current-dev candidate.
- Apply the merge bar of two independent positive reviews.

R488-1 FINISHED
