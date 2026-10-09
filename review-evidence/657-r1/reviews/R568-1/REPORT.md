[R568] POSITIVE - exact head 62c261c2d1b899a9cf90c901b25b5a85846dfef6

# R568-1: internal independent review of PR #701 (Relates to #657)

- **Scope.** Issue #657 is the `tdm8render-mutants` campaign. This round is the first review of PR #701.
- **Head under review.** `62c261c2d1b899a9cf90c901b25b5a85846dfef6`, tree `a8ed9acaec2e3c7d0ff5ff1ea64ff68a4ab1027d`. It is one commit on dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`, which carries PR #672: the #645/#647 settle recentre and loopback depth 16.
- **Diff.** Four files, all test, campaign or documentation:
  - `sim_tdm8_render.cpp`, +54/-1;
  - `tdm8_render_mutants.py`, +6/-5;
  - `TESTING.md`, +16/-2;
  - `MEDIA_CLOCK_FOLLOWING.md`, +7.
- **Untouched.** No `hdl/`, `configs/` or submodule path changed (`receipts/diff_scope.txt`).
- **Commit message.** One line, with no trailers.

**Verdict: POSITIVE.** This round has:

- no BLOCKER, MAJOR or MINOR;
- no RESIDUE;
- one SUGGESTION (S1).

All five lenses are covered clean at this exact head.

## Context reconstructed (public state only)

I read these sources, in this order:

1. AGENTS.md, then the CONTRIBUTING.md workflow and commit rules.
2. The issue #657 body.
3. The assignment: issue comment 6082915356.
4. TAKEN, issue comment 6082947082.
5. REVIEW READY, issue comment 6086879361.
6. The law in `docs/design/MEDIA_CLOCK_FOLLOWING.md`:
   - "Switching sources" and "Settle recentre", lines 1036-1130;
   - the test plan, lines 1590-1659.
7. The #386 trigger and the settle recentre in `hdl/milan/milan_datapath.sv`, lines 6501-6600.
8. The underrun counter in `hdl/ieee1722/aaf/KL_tdm_render_master.sv`, lines 444-451 and 528-536.
9. The diff and its history.
10. The public evidence bundle `review-evidence/657-r1/author` at `7fe5c1c1`.
11. The hosted checks at the head.

No PR comment and no other reviewer's report was read before this verdict and ledger were written.

Frozen acceptance, from the issue body and assignment 6082915356:

- (1) the `--epoch-only` clean leg passes, or its four T30 CRF recentre checks are corrected to the declared law, with the reason stated;
- (2) "uncounted repeat" is killed by a named check, or argued equivalent;
- (3) `make -C tb/verilator/milan_dp_render tdm8render-mutants` exits rc 0 with the pinned Verilator;
- (4) no RTL change;
- (5) the default suite stays within its hosted budget, timed as PR #672 did, and the TESTING.md campaign row is updated;
- (6) the builder bank and docs gates pass.

## Executed evidence (this round, exact head, pinned Verilator 5.050)

I verified the compiler's identity before use:

- the wrapper is `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, sha256 `905795b9...e92f`;
- it reports `Verilator 5.050 2026-07-01 rev v5.050`;
- the system `verilator` is 5.052, so I forced the pinned one through a PATH shim and `VERILATOR=`.

All concurrent jobs ran on disjoint CPU sets inside the 12 GB unit.

The receipts are listed in `MANIFEST.sha256`. In `campaign.log` and `default.log`, the compiler's include-path home prefix is replaced by `<home>`; nothing else is edited.

| # | What | Command (portable script) | Result |
|---|---|---|---|
| E1 | Acceptance (3): the full campaign under an outer `make -C` | `run_campaign.sh`: `taskset -c 0-11 make -C tb/verilator/milan_dp_render tdm8render-mutants`, `VERILATOR_JOBS=6` | **rc 0, 34 checks: 34 PASS, 0 FAIL**, 6320.06 s (`receipts/campaign.log`, `campaign.rc`) |
| E2 | Acceptance (5): the cold default, timed the PR #672 way | `run_default_timed.sh`: `make clean`, then `env -u MAKEFLAGS taskset -c 12-15 make -C tb/verilator/milan_dp_render`, `VERILATOR_JOBS=2` | **rc 0, 827.99 s**; shipping 266/0, multi-stream 71/0, `--leg-defects` 5/5. Other jobs ran on disjoint CPUs (`receipts/default.log`, `default.rc`) |
| E3 | Hosted render window at the PR merge ref | job log, run 37973662908 job 113966628806 (Verilator shard 0/5), on `d44e3e4` = this head merged into live dev `7c1b52be` | `milan_dp_render` PASS. Window 18:54:00.284 -> 19:12:22.249 = **1101.97 s**, a margin of 338.03 s to 1440 s and 698.03 s to 1800 s. `follow_ring` took 1192.44 s, under 1260 s (`receipts/hosted_render_window.txt`) |
| E4 | Hosted checks at the head | `gh pr checks 701`; check-runs API | Every executed context succeeded, including `verilator-suites` and its five shards, `yosys-portability` and its four shards, `rtl-fast`, `elaborate`, `docs-check`, `verilator-lint` and `firmware-unit`. "Physical gPTP (nightly and manual)" was **skipped**, not executed (`receipts/check_runs_head.tsv`, `pr_checks*.txt`) |
| E5 | Documentation/source gates at the head | the list in `receipts/docs_gates.log`. The renderer-dependent `gen_toc --check`, `gen_toc --verify-anchors` and `check_em_dash --base 5603c353` were run with the pinned renderer from a private scratch venv | All rc 0: docs_check, doc_style, doc_paths, cpp/py/sh idiom, hygiene, test_evidence, fail_fast, todo_ownership, ci_events, archive, module matrix, solution docs, feature_status. TOC is 140 pages, anchors 417; em-dash has 0 findings, arms 339/339 (`receipts/docs_gates_renderer.log`). On the system interpreter, without the renderer, those three return rc 2 "cannot read Markdown" (environment, not a finding) |
| E6 | Harness and RTL probes, disposable, scratch copy | `probe_build.sh` + `probe_run.sh` (`--epoch-only` and `--serial-only` legs) | See table P below (`receipts/probe_*.log`, `probe_run.rc`) |
| E7 | Was the zero-recentre result a short wait or a lost trigger? | `probe_longwait.sh`: no dwell; the post-selection wait is lengthened from 12 M to 80 M axis cycles (800 ms) and the record from 2,400 to 9,000 PDUs | `PROBE: src pulses 1 render pulses 1 stage 1`. All four T30 recentre checks pass. One unrelated failure, "T30 CRF LAW: PDUs measured", is a probe artefact: the record's PDU field wraps at 4,096 (`receipts/probe_longwait_epoch.log`) |
| E8 | Directory-banner behaviour behind the driver change | `probe_banner.sh` (GNU Make 4.4.1) | With `MAKEFLAGS=w`, a nested `make -s -C` prints "Entering directory" into the query's stdout. `--no-print-directory` suppresses it (`receipts/probe_banner.log`) |
| E9 | Clone integrity after every run | `receipts/clone_integrity.txt` | HEAD and tree are exact, with `write-tree` = `a8ed9aca...`. `diff-index` and worktree diff are clean, with no non-ignored untracked file. Index (mode, blob, path) = `HEAD` tree. Gitlinks: `external`, `gptp-processor`, `protocol-processor`, `third_party/lwSRP` and `third_party/verilog-axis` match their pins. `external` and `lwSRP` are uninitialised, as at checkout. Initialised submodule worktrees are clean. The regenerated tracked `configs/generated/sweep_opts_ax7101.sh` is byte-identical to its blob |

Probe table P. Every variant was built from the reviewed head in a scratch copy with one edit, and each edit was asserted to match exactly once. The harness file was restored from git after each harness variant.

| Variant | Leg | Result |
|---|---|---|
| clean | `--epoch-only` | 127 checks, 0 failures |
| clean | `--serial-only` | 66 checks, 0 failures. The nominal window grades 839 frames with 0 repeats, so the pre-existing "T6 ORDER: every repeat is a counted underrun" was vacuous. The burst gives `T6 UNDERRUN: 23 frames, 11 forced repeats, 0 uncounted repeats, 0 skipped events` |
| harness, the #657 dwell removed (`sim_tdm8_render.cpp:4450`) | `--epoch-only` | 127/4, exactly the four T30 recentre checks, each `got=0 exp=1`, as in the issue |
| harness, burst never raised | `--serial-only` | 66/1: only "T6 UNDERRUN: the faster serial clock forced repeated frames" fails. 11 frames, 0 repeats |
| RTL, the campaign's frozen counter | `--serial-only` | 66/1: only "T6 UNDERRUN: every forced repeat is a counted underrun" fails, `got=11` |
| RTL, each underrun counted twice (`+ 16'd2`) | `--serial-only` | 66/1: the same named check fails, `got=11` |
| RTL, the counter saturating at 3 (`&unders_b_r[1:0]`) | `--serial-only` | 66/1: the same named check fails, `got=11`. 4 underruns were already counted at prefill before the window |

## Acceptance, item by item

1. **Met; no check is weakened.**
   - **What changed.** The only change on this leg's path is one line at `sim_tdm8_render.cpp:4450`: `--epoch-only` now takes `kBootPullInCycles` (30 M axis cycles) before `phase_crf()`. That is the same dwell `--crf-only`, `--law-only`, `--law-boundary` and `--pullin` already take.
   - **Checks preserved.** The four T30 recentre checks keep their exact text and expectation of 1:
     - `:3616-3617`, `:3619` and `:3621`, at base `:3570-3575`;
     - `:3636`, at base `:3590`.

     The diff's only removed harness line is the clock accumulator line it generalises.
   - **Law.** `milan_datapath.sv:6501-6565` arms the #386 trigger on a change of the selected index. It fires after 2,048 ticks inside the 1/64-sample band, or at the `SRC_SETTLE_CEIL_C` = 32,768-tick ceiling (`:6519-6520`). The docs' settle-recentre section (`MEDIA_CLOCK_FOLLOWING.md:1084-1086`) keeps that trigger unchanged beside the #645 action.
   - **Mechanism.** The selection now happens after the boot pull-in, and the 120 ms (12 M-cycle) wait at `:3615` then covers the 2,048-tick settle.
   - **The stated reason is correct.** Without the dwell the selection lands inside the boot pull-in, and the trigger has not fired by 120 ms (P, nodwell). With an 800 ms wait and no dwell it fires exactly once at all three counters (E7). So the zeros came from the test's timing, not from a lost or doubled recentre. The ceiling bounds the trigger whatever the history.
   - **Documented.** The new bullet `MEDIA_CLOCK_FOLLOWING.md:1653-1659` states this reason. A settle recentre cannot enter the T30 counts in this window: it fires only after 8 LOCKED servo windows (4.096 s), or at its 21.8 s ceiling.
2. **Met; the mutant is killed by a named check.**
   - **The new check.** `prove_serial_underruns_are_counted` (`sim_tdm8_render.cpp:2376-2413`) doubles the shared audio/serial clock for two PDU periods (`:412`). 782 < 1591, so the rate is exactly 2x. The packet grid stays nominal, which forces serializer frame starts with no fresh frame.
   - **The RTL path it exercises.** `KL_tdm_render_master.sv:447-450`: active frame retained, `unders_b_r` incremented.
   - **Grading.** It grades the pins with the existing oracle (`grade_frames`, `:1766-1872`) and requires all of: repeats > 0; each repeat's sampled counter = previous + 1 (`:1858-1859`); identity, padding and zero skips intact.
   - **Mutant expectation.** The campaign's expected check is `tdm8_render_mutants.py:192-196`. The campaign kills the mutant by that name (E1). It cannot pass vacuously: suppressing the burst fails the exercised-repeat guard (P).
   - **Over-counting is outside this check but already covered.** The existing nominal-window checks "T30 CRF ALIGNED / INTERNAL (A2-a): ...and NO underrun" (`:3350`, `:3377`) catch an over-counting counter.
3. **Met.** E1 gives rc 0 at 34/34.
   - **Where the count went from 32 to 34.** PR #672 (in `5603c353`) added two campaign checks:
     - the mutant "the settle recentre never pulses" on `ship --pullin` (git diff `fea346e7..5603c353` of the driver);
     - with it, a sixth (elaboration, mode) pair, so a sixth positive control.
   - **The tables.** They now hold 22 mutants, 3 clean controls, 3 leg defects and 6 positive controls, which is 34. At the issue's dev, 21 + 3 + 3 + 5 = 32.
   - **Arms affected by this head.** All 34 pass. They include both arrival-skew clean controls, the clean epoch leg and all six `--epoch-only` mutants, which are still caught after the dwell.
4. **Met.** No RTL, configuration or submodule path changed (`receipts/diff_scope.txt`).
5. **Met.**
   - **Local.** The cold local default took 827.99 s (E2); the author's figure is 809.21 s.
   - **Hosted.** The hosted window at the PR merge ref is 1101.97 s against the 1440 s line (E3), and the earlier 8e4b1e53 window was 1218.7 s.
   - **Cost of the burst.** It adds 2 x 25,000 axis cycles per leg; the epoch dwell lies outside the default.
   - **The rows.** The campaign row (`TESTING.md:273`) and its runner row (`:614`) are updated, and the timing paragraph is at `:349-361`.
6. **Docs gates: met at the head** (E5). **Builder bank:** this round may not run it.
   - The diff touches no builder input.
   - The author's receipt (`builder-receipt.json`, rc 0) is the only source-head execution evidence for it.
   - The manager runs the builder bank on the merge candidate.

## Findings

**S1. SUGGESTION.**

| Field | Content |
|---|---|
| Lenses | Docs |
| Location | `docs/testing/TESTING.md:360-361` |
| Authority/evidence | "The candidate's hosted timing remains pending publication." This was accurate when written: the lane could not push. Hosted run 37973662908 now gives a 1101.97 s render window at the PR merge ref (E3). PR #672 recorded its hosted window in this section (`:328-343`) |
| Impact | None on any acceptance claim. The paragraph already says the earlier hosted figures do not establish this head's acceptance, and hosted acceptance is the manager's. After merge, the "pending" sentence reads as stale history |
| Optional outcome | At the merge turn, the manager may record the hosted window that accepts the merged head (run, job, seconds, margins), as PR #672 did |
| Verification | `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `check_em_dash.py` stay rc 0 |

No other finding. Several items were checked and are not defects:

- **Directory banner.** The removed "run from the suite directory" guidance matches the E8 behaviour. E1 proves the replacement under an outer `make -C`.
- **Burst order.** The burst runs after every CRF/LAW grading in the full leg (`:4459`, before `phase_bind_loss`) and at the end of `--serial-only` (`:4463`). The full leg still passes 266/266, and the three leg-side defect arms are still caught by their named checks (E1, E2).

## Lens ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Every acceptance item above. `MEDIA_CLOCK_FOLLOWING.md:1036-1130,1590-1659`. `milan_datapath.sv:6501-6565` (#386 trigger and ceiling) and the settle recentre after it. `sim_tdm8_render.cpp:3588-3640` (T30 checks unchanged against base `:3570-3590`) and `:4450`. Probes P (nodwell) and E7 (longwait). E1 34/34. E3 hosted window | R568-1 | `62c261c2d1b899a9cf90c901b25b5a85846dfef6` |
| RTL | CLEAN | `git diff --name-status 5603c353..62c261c2` touches no `hdl/`, `configs/` or gitlink (`receipts/diff_scope.txt`). `KL_tdm_render_master.sv:444-451,528-536`: the repeat-and-count path and its gray crossing are what the new check observes, and the contract is unchanged. `milan_datapath.sv:6501-6565`. Mutants frozen/plus2/sat3 built from that RTL. Hosted `elaborate`, `verilator-lint`, `yosys-elaboration` and `yosys-portability` succeeded | R568-1 | `62c261c2d1b899a9cf90c901b25b5a85846dfef6` |
| Robustness | CLEAN | Burst bounded and cleared (`sim_tdm8_render.cpp:2376-2390`, `:412`). Its order after CRF/LAW and before `phase_bind_loss` (`:4455-4463`). The serial-only defect legs that now also reach the burst are still caught by name (E1). Saturation probe sat3 and over-count coverage (`:3350,:3377`). The #386 trigger's ceiling bounds the selection-during-boot history (E7) | R568-1 | `62c261c2d1b899a9cf90c901b25b5a85846dfef6` |
| Tests | CLEAN | `prove_serial_underruns_are_counted` `:2376-2413` and `grade_frames` `:1766-1872`. The new named check fails for the frozen, double-count and saturating counters, and the guard fails without the burst (P). The epoch leg fails exactly the four checks without the dwell and passes with it (P). Campaign 34/34 (E1); default 266/71/5 (E2); hosted shards green (E4). No check text or expectation was removed or relaxed: the only removed harness line is `acc += kAudNum;`, generalised at `:412` | R568-1 | `62c261c2d1b899a9cf90c901b25b5a85846dfef6` |
| Docs | CLEAN (S1 optional) | `MEDIA_CLOCK_FOLLOWING.md:1653-1659`, each sentence checked against E7, P and the RTL. `TESTING.md:273`, the 32 -> 34 account at `:614`, the `make -C` claim against E1/E8, and the timing paragraph `:349-361` (arithmetic 1440 - 809.21 = 630.79; 1800 - 809.21 = 990.79). Driver docstring `tdm8_render_mutants.py:77-81`. Gates E5 all rc 0 | R568-1 | `62c261c2d1b899a9cf90c901b25b5a85846dfef6` |

## Real limits

- **Not run by this round.** I did not run the `tdm8render-pullin` (19 legs) or `tdm8render-law-boundary` (81 checks) explicit targets, and both are outside the issue's gates.
  - The burst reaches the `--with-pullin` history leg only after `phase_pullin`.
  - The driver's `--no-print-directory` change is the same `build()` that E1 exercised for all 22 rebuilt arms.
  - The author's pull-in receipt reports 19/19.
- **Prohibited for this round.** I did not run the builder bank, the full parent, PP, gPTP or Yosys banks, `act`, or the host-side runner.
- **Concurrency.** E2's local time was measured while other jobs ran on disjoint CPUs. It is local evidence only. E3 is the hosted figure, and it was measured on the merge ref `d44e3e4`, not on the bare source head.
- **No hardware.** Physical calibration was NOT RUN. The skipped "Physical gPTP" hosted context is not hardware proof.
- **No manager source bank.** No manager source bank runs at this head, and this report claims none.

## Pending manager duties

- Validate the current-dev merge candidate (source base `5603c353`, live dev `7c1b52be`): builder and native banks, plus hosted/act acceptance, and link the receipts on the PR.
- Post or link the lane's self-test evidence as a PR comment (DoD row).
- Optionally act on S1.
- Obtain the external review ([R569]) and the clean-lens ledger acceptance.
- Run post-merge containment.
- Close #657 by hand or by keyword. The PR says `Relates to #657`.

## Prior public review findings on PR #701

I read these only after the verdict and ledger above were written. That covered every issue comment, PR comment, PR review and inline review comment on PR #701, plus the PR body.

**Findings.** There are none to resolve or retain. The PR holds only the two review-start notices (6086958823 for R568-1, 6086965984 for R569-1). It has no review object and no inline comment. Issue #657 carries only the assignment, TAKEN and REVIEW READY. This round therefore confirms that no earlier public finding is open at this head, and the verdict stands unchanged.

**PR body.** I checked it against the evidence above:

- Its claims match: 34/34; 266/71/5; the four-file test- and docs-only scope; the dwell and burst description.
- Its "hosted timing ... pending" status line is dated to publication. E3 now supplies the hosted figure.
- Its unchecked Definition-of-Done row "Self-test evidence is posted in a PR comment" stays open. The lane's evidence is on issue #657 (REVIEW READY 6086879361) and in the published bundle, so posting or linking it on the PR is a manager duty. It is not a defect in the head.

R568-1 FINISHED
