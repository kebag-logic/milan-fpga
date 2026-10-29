[R727] POSITIVE - exact head 2b1565fd9095d6ec8be514849ba9b92b8f4c5b31

# R727-2: internal cleared-context delta review of PR #805 (issue #803, gPTP pin adoption f97c1803)

- Head `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31`, tree `367ade28eae1646e43cac428f797db9136d59450`, base and live dev `5fcec84b1aa72c43048eff28bb63a982add830dd`.
- Scope: the delta `fb182b19..2b1565fd` (six commits by the round-2 executor) against the round 2 ruling on #803 (issuecomment-6483128755), plus every prior finding of R727-1 and R728-1 at its cause.
- Verdict POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE is open. Three SUGGESTIONs and one informational note are below. All five lenses are clean at this head.
- Every prior finding is resolved: F1 (both reviews), F2, R1 and S1 (both reviews).

## Reconstruction order

1. AGENTS.md and CONTRIBUTING.md (the review contract), then docs/README.
2. Issue #803: its frozen acceptance ("all consumer gates rc 0") and the round 2 ruling's six items and STOP rule.
3. Authorities:
   - IEEE 1722.1-2021 7.4.41.2, as cited: `count` is paired with `path_sequence`.
   - `docs/reference/REGISTER_MAP.md:333`: the response snapshots the path before gathering entries.
   - `hdl/milan/milan_datapath.sv:6011-6084, 6295-6311`: the snapshot registers and the entry pick.
   - `gptp-processor/hdl/top/KL_gptp_engine.sv`: the event queue, push, pop and drop logic.
4. `git diff fb182b19..2b1565fd`, then `git diff 5fcec84b..2b1565fd` for scope statements, and the history.
5. Public evidence:
   - the author's round-2 packet at `09a8771f` `review-evidence/803-r1/author-r2/`;
   - the PR body;
   - an exact-head hosted snapshot.

Prior review findings were read only after my own pass over the diff.

## Executed evidence (this round, exact head, disposable copies only)

The copies live under `scratch/`. I used the pinned Verilator 5.050, `Verilator 5.050 2026-07-01 rev v5.050`, and ran the independent legs concurrently.

| Run | Result | Receipt |
|---|---|---|
| clean `gptp` leg | rc 0, `202 checks: 202 PASS, 0 FAIL`; `[cut] count beat held 474 cycles; commit seen 1; path-entry request before the commit 0`; `[#207] full-queue window: level 1, rp 1->1, wp 2->2` | `receipts/clean-exec-gptp.log` |
| clean `gptp-lat` leg | rc 0, `202 checks: 202 PASS, 0 FAIL`, the same two diagnostics | `receipts/clean-exec-gptp-lat.log` |
| probe M9: entry 0 from `asp_live_head_w` | rc 2, `FAIL in-flight response remains wholly old GM got 02a1b2fffec3d4e5 exp 00aaccfffe010204` | `receipts/probe-m9.diff`, `receipts/m9-exec-gptp.log` |
| probe M9b: entries 1..7 from `asp_live_path_w` | rc 2, `FAIL in-flight response remains wholly old: ends with thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` | `receipts/probe-m9b.diff`, `receipts/m9b-exec-gptp.log` |
| probe M9c: count from `asp_live_count_w` (falsifies the arm comment's "count" claim) | rc 2, `FAIL in-flight response remains wholly old count two got ...1 exp ...2`, plus the entry 1 check | `receipts/probe-m9c.diff`, `receipts/m9c-exec-gptp.log` |
| harness control H1: the cut without its count-beat hold | rc 2, `path-entry request before the commit 1`; `FAIL empty path commits after first-count snapshot, before entry gather` | `receipts/probe-h1-no-hold.diff`, `receipts/h1-gptp.log` |
| harness control: the #207 window without the held second Pdelay_Req | rc 2, `[#207] full-queue window: level 0, rp 1->2, wp 1->1`; `FAIL the full-queue window pops and pushes no event`, then 14 later `#88` / entry-0-only checks fail | `receipts/probe-s1-no-held-req.diff`, `receipts/s1nob-exec-gptp.log` |
| `scripts/ci_gate_workflows.py --check` | rc 0 | `receipts/ci_gate_workflows-check.*` |
| `scripts/ci_events.py --check` | rc 0, `ci_events: OK (2199 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md)` | `receipts/ci_events-check.*` |
| `scripts/ci_events.py --selftest` | rc 0, `selftest: PASS (2199 contract items, 5258 arms)` | `receipts/ci_events-selftest.*` |
| `scripts/measure_test_evidence_selftest.py` | rc 0 | `receipts/measure_test_evidence-selftest.*` |
| author packet integrity | 16 of 16 fetched files match `MANIFEST.json` `published_sha256` | `receipts/author-evidence-manifest-check.txt` |
| clone integrity after all probes | HEAD and tree exact, nothing untracked or dirty, index modes and blobs equal the HEAD tree, all six gitlinks at their pins | `receipts/clone-integrity.txt` |

All probes are re-plantable with `reproduce.sh <clean clone at head> <workdir>`, with `VERILATOR` set to the pinned 5.050. Every probe diff applies cleanly to the head (`git apply --check`).

## The ruling, item by item

1. **F1 (met).** `tb/verilator/milan_dp/sim_gptp.cpp:426-428` samples `asp_resp_entry_w` and, while `hold_gsi_beat` is set, clears `gsi_srv1_r` after each edge. That holds the GSI count beat inside the processor's bounded gather wait. At `:1481-1498` the arm sets the hold after the capture, commits the empty path, and asserts that the commit happened with no path-entry request since capture.
   - The publication therefore lands between the first-count capture and the entry gather.
   - It was held for 474 cycles, against the 4096-cycle gather wait.
   - M9 and M9b each print FAIL on a named check, one at a time. Both clean legs are 202/202.
   - The count rises from 200 because one ordering check replaced the old wire-order check and two checks were added: entry 1, and the #207 pointer check. Every check passes, which is the intent of "stays 200/200".
   - The arm comment at `:1424-1430` claims what the arm proves. I falsified each named substitution (count, entry 0, entries 1..7), and each fails.
   - The RTL comment at `milan_datapath.sv:6032-6035` is now true as written: H1 shows the ordering check bites. That closes R728-1's second required outcome.
2. **F2 (met).**
   - `docs/reference/SUBMODULES.md:310-314` and `CHANGELOG.md:72-75` now say: no top-level port, parameter or register change; `KL_gptp_shadow.pub_path_o` widens with the engine's to eight entries from entry 0; `gptp_shadow_wrap` adds `pub_path_head_o`.
   - I checked this against `git diff 5fcec84b..2b1565fd`:
     - `KL_gptp_shadow.sv:200` changes `[7*64-1:0]` to `[8*64-1:0]`;
     - `gptp_shadow_wrap.sv` adds `output wire [63:0] pub_path_head_o`;
     - `milan_datapath.sv` has 187 port/parameter declaration lines before and after, and its only `^[-+]` port-pattern hit is a comment;
     - `milan_csr.sv` changes port comments only;
     - the `REGISTER_MAP.md` diff is prose with no address or field change.
3. **R1 (met).** `SUBMODULES.md:334` now reads "Its shipping route meets timing at +0.333 ns WNS."
4. **S1 (met).**
   - At `sim_gptp.cpp:1667-1722`, a second real Pdelay_Req (`s1b`) waits at the queue head behind `s1`'s held response claim. The level is forced only after that, and both pointers are graded equal before and after the window.
   - Clean run: `level 1, rp 1->1, wp 2->2`, so nothing was popped or pushed, and the level is restored to its own value. The engine RTL bears this out:
     - a refused push only increments `ev_drop_r`;
     - `bank_sel_r` flips only on an accepted push (`KL_gptp_engine.sv:341-342, 497-510`);
     - nothing else is left behind.
   - Without `s1b`, the stale pop is caught and later arms fail. So the guard is necessary, and no graded arm now runs on a perturbed engine.
5. **Physical leg (met).**
   - The re-projection follows the README's method (`tb/verilator/milan_dp/README.md:407-435`). The simulation part is scaled by 899637137/849624822 = 1.058864, and the 830 s remainder is held fixed:
     - 4265.7 × r + 830 = 5346.8 s;
     - (5225 − 830) × r + 830 = 5483.7 s;
     - against 6900 s these are 77.5 % and 79.5 %;
     - job margins on 8700 s are 55.9 and 53.6 min.
   - These match the README, `CI_WORKFLOWS.md:537, 656-661` and the author's `projection.txt`.
   - Only the `physical-gptp` job (`Physical gPTP (nightly and manual)`, gated on schedule/workflow_dispatch) changed: `timeout-minutes` 120 to 145 in the template (`.github/ci-templates/rtl.yml:321`) and the generated file (`.github/workflows/rtl.yml:418`).
   - `git diff 5fcec84b..2b1565fd -- .github` contains exactly those two lines. The generator check is rc 0.
   - The suite deadline is `scripts/run_all_suites.sh:259` (`milan_dp_gptp`, selected only by `--physical-gptp`). Its pinned contracts follow: `ci_events.py:178, 2008`, `measure_test_evidence.py:673, 680` and selftest `:297`.
   - No PR-gating job and no other timeout changed.
6. **Slice figures (met; not ruled).**
   - `docs/design/AREA_BUDGET.md:140` gives the head's route: 15,843 placed, 7 of 15,850 free. That is consistent with the PR's route-1x1 row, 15,835 → 15,843.
   - `:141` keeps "needs its own owner decision". The acceptance belongs to the owner, and I make no ruling on it.
7. **Scope, comments, PR body (met).**
   - `git diff --stat fb182b19 2b1565fd` touches no `hdl/`, register map, gitlink or contract file. It covers 15 files, all tests, docs, CI or scripts. The author's scope receipt says the same.
   - An added-line scan of the delta for lane labels, lane names, review rounds, reviewer IDs, issue-comment IDs and private paths found none. Its only hits were `gptp` identifiers.
   - The PR body (snapshot `receipts/pr805-body-at-review.md`) names this head and gives 202/202 for both legs. It says "Relates to #803", and `closingIssuesReferences` is empty.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### S-1 - SUGGESTION - Tests, Robustness - `tb/verilator/milan_dp/sim_gptp.cpp:1693-1720`

- **Evidence:**
  - The "pops and pushes no event" check compares 2-bit `evq_rp_r` / `evq_wp_r` only at the window's two ends. Four pops would wrap undetected.
  - Nothing asserts that `s1b` actually reached the queue: the wait loop at `:1693` can time out with `lvl0 == 0`, and the arm then continues.
  - At this head neither happens. The head is a claim-blocked Pdelay_Req, the clean run shows `level 1`, and the no-`s1b` control is caught.
- **Impact:** none today. A future change that let the head dispatch could pass the endpoint check after a full wrap.
- **Suggested outcome:** add `expect("s1b waits at the queue head", lvl0, 1)`, and check that `evq_rp_r` is unchanged on every cycle of the forced loop.
- **Verification:** the no-`s1b` control still fails, and the clean leg passes.

### S-2 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_gptp.cpp:1499-1505`

- **Evidence:**
  - The in-flight response has the old count two, so only entries 0 and 1 are graded.
  - The comment's "entries 1..7 from the live path" is accurate for the whole-range substitution (M9b, killed). A substitution confined to entries 2..7 would not be seen by this arm, because those entries are count-gated out of a two-entry response.
- **Suggested outcome (optional):** a later cut with an older path of eight entries would grade the whole snapshot tail.

### S-3 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_gptp.cpp:1492-1496`

- **Evidence:** the diagnostic prints "count beat held N cycles". It reports cycles since capture whether or not the hold is active. H1 prints "held 474 cycles" with the hold off.
- **Suggested outcome:** wording such as "N cycles from capture to commit; hold on/off". This is a diagnostic string only and changes no check.

### N-1 - informational - PR body table row "the #207 window without the queued Pdelay_Req"

- The author's control reports `rp 1->0` (three stale pops) and 7 later failures.
- My independent control, which removes only the `s1b` send and its wait, reports `rp 1->2` and 14 later failures.
- The two controls are built differently and both are caught on the named check. No change is required.

## Prior findings at this head

| Prior finding | Lenses | Status at 2b1565fd | Evidence |
|---|---|---|---|
| R727-1 F1, MINOR (snapshot untested) | Tests, Robustness | RESOLVED | M9, M9b and M9c each FAIL a named check; H1 FAILs the ordering check; clean legs 202/202 |
| R728-1 F1, MINOR (same; RTL ordering comment untrue) | Tests | RESOLVED | as above; `asp_resp_entry_w` is now read and asserted (`sim_gptp.cpp:426-427, 1491-1498`) |
| R727-1 F2, MINOR (adoption record scope) | Docs | RESOLVED | `SUBMODULES.md:310-314`, `CHANGELOG.md:72-75`, checked against the base diff |
| R727-1 R1, RESIDUE ("keeps" WNS) | Docs | RESOLVED | `SUBMODULES.md:334` |
| R727-1 S1 / R728-1 S1, SUGGESTION (#207 stale pops) | Tests | TAKEN | pop-free window, pointer check, clean `rp 1->1, wp 2->2`; the control is caught |
| R727-1 / R728-1 pending: physical deadline 99.0-101.6 % of 5400 s | Docs, CI | ADDRESSED as ruled | 6900 s / 145 min; 77.5-79.5 %; hosted confirmation still pending (below) |

## Lens results (clean lenses in the finding format)

- `[R727] PASS Conformance — sim_gptp.cpp:1424-1505; milan_datapath.sv:6027-6072, 6300-6311; REGISTER_MAP.md:333; issue #803 ruling items 1-6 — the in-flight GET_AS_PATH response is graded as one first-count snapshot (IEEE 1722.1-2021 7.4.41.2 count/path_sequence pairing). M9, M9b and M9c are killed. Each ruling item was checked against its artifact. No RTL, register-map or contract change in the delta. Issue acceptance "all consumer gates rc 0": my focused gates are rc 0, and the bank gates rest on the author's receipts (limits).`
- `[R727] PASS RTL — git diff --stat fb182b19 2b1565fd (no hdl/ or gitlink); milan_datapath.sv:6043-6084 (gsi_srv1_r/srv2_r handshake under the harness hold); KL_gptp_engine.sv:341-342, 451-510 (push/pop/drop, bank_sel) — the delta changes no RTL. The harness pokes (gsi_srv1_r cleared after each edge; evq_lvl_r forced, then restored to its own value with both pointers unmoved) stay within the processor's 4096-cycle gather wait (474 cycles held) and leave the engine as found. Prior RTL coverage of the unchanged RTL (R727-1, R728-1 at fb182b19) still stands, because nothing it depends on changed.`
- `[R727] PASS Robustness — sim_gptp.cpp:1481-1498, 1687-1720; receipts h1-gptp.log, s1nob-exec-gptp.log — a publication racing an in-flight gather (the ordering is asserted, and the no-hold control fails); a forced-full queue with no pop or push in the window (the no-held-request control fails, and so do the later arms it would have perturbed). Bounded loops: 3000-cycle commit wait, 20000-cycle claim and level waits, 400-cycle window. Hardening suggestion S-1 is optional.`
- `[R727] PASS Tests — clean-exec-gptp.log, clean-exec-gptp-lat.log (202/202 each); probe-m9/m9b/m9c/h1-no-hold/s1-no-held-req diffs and logs — every new check can fail for its defect, both reviewer probes are killed one at a time, and no existing check was weakened (one check was replaced by a strictly stronger ordering check). Script contracts: ci_gate_workflows --check, ci_events --check/--selftest and measure_test_evidence_selftest are all rc 0. S-1, S-2 and S-3 are optional.`
- `[R727] PASS Docs — SUBMODULES.md:310-334; CHANGELOG.md:72-80; AREA_BUDGET.md:140-141; tb/verilator/milan_dp/README.md:354-355, 426-435; CI_WORKFLOWS.md:537, 656-661; RUNNING_TESTS.md:88; TESTING.md:172-173; milan_dp_gptp/README.md:26-27; run_all_suites.sh:41, 252-254; the PR body snapshot — the scope, WNS wording, slice figures, deadline figures and projection arithmetic are all true at the head. No stale 5400 s / 120 min remains outside historical measurement text (README:411-423, CI_WORKFLOWS:557, 628). The comment rule and the privacy scan of added lines are clean.`

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_gptp.cpp:1424-1505`; `milan_datapath.sv:6027-6072, 6300-6311`; `REGISTER_MAP.md:333`; ruling items 1-6; M9/M9b/M9c runs | R727-2 | `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` |
| RTL | CLEAN | delta stat (no RTL); `milan_datapath.sv:6043-6084`; `KL_gptp_engine.sv:341-342, 451-510`; harness pokes `sim_gptp.cpp:426-428, 1678-1709` | R727-2 | `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` |
| Robustness | CLEAN | race ordering and window-perturbation controls (H1, no-`s1b`); bounded waits | R727-2 | `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` |
| Tests | CLEAN | clean `gptp`/`gptp-lat` 202/202; five probes/controls; ci_gate_workflows, ci_events, measure_test_evidence selftests | R727-2 | `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` |
| Docs | CLEAN | SUBMODULES, CHANGELOG, AREA_BUDGET, milan_dp and milan_dp_gptp READMEs, CI_WORKFLOWS, RUNNING_TESTS, TESTING, run_all_suites.sh comment, PR body | R727-2 | `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` |

## Real limits

- **Not run here; author receipts only:**
  - the full 64-suite sweep;
  - the physical `milan_dp_gptp` leg (205 checks, 0 failures; 5391 s on the author's loaded host, 78.1 % of 6900 s);
  - Yosys, Vivado, lint, xvlog, rtl-fast and the docs workflow and builder legs.
  - These are bank-scale and not allowed in this round. The sixteen receipts I fetched match the packet manifest's hashes.
- **Evidence integrity:** the evidence commit `09a8771f` carries no git signature (`unsigned`), so integrity rests on the published `MANIFEST.json` hashes alone.
- **Physical deadline:** 6900 s is a projection from hosted runs of the previous scenario. No hosted run of the current scenario has completed. The author's local run at 5391 s was taken under unspecified load and cannot be compared with the hosted projection.
- **Hosted contexts** (`receipts/hosted-checks-snapshot.tsv`, at about 02:07Z): 14 success, 20 in progress, 8 queued. `Physical gPTP (nightly and manual)` is a skipped context, which is not proof. I claim no hosted result and no manager source bank.
- **Standard text:** IEEE 1722.1-2021 7.4.41.2 is applied as the issue and REGISTER_MAP cite it. No standard text was opened in this round.
- **Hardware:** physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Current-dev merge-candidate validation (builder and native banks) at the merge turn. Dev is `5fcec84b`; the parallel #799 / PR #802 adoption sets the merge order.
- Exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` acceptance, and act acceptance.
- Owner decision on slice headroom, recorded on #803 before merge: 7 of 15,850 free, +20 over dev's route.
- A completed hosted run of the current physical scenario, to confirm the 6900 s / 145 min deadline.
- Round-2 external review.
- FPGA-gPTP #87 to #91 close only after an image passes the in-house scenarios on the test machine.
- Optional: carry S-1 to S-3 to the author.

R727-2 FINISHED
