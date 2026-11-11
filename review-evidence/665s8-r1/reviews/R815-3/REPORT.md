[R815] POSITIVE - exact head dbe54e46f09802ab8b9bd3f3223d36bf4891394b

# R815-3: internal independent review of PR #879 (issue #868, S8 wire timing), delta `e3f96a67..dbe54e46`

Head `dbe54e46f09802ab8b9bd3f3223d36bf4891394b`, tree `5225f4c7df78c9b0de56148aca56d7996c9b4e2b`. Previously reviewed head `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53` (R815-2 NEGATIVE, one MINOR; R816-2 POSITIVE). Lane merge base on `dev-soft-core` is `1d6bf555`.

**Verdict: POSITIVE.** R815-2 F1 is resolved at its cause. My R815-2 mutant script, rerun at this head, kills 14 of 14 mutants. The only change to the script is the expected control for `over-delivery-check-gone`: it now expects the new `load-offer-over-delivered` control. The unchanged script still kills 13; its fourteenth mutant fails the self-test, but only through that new control. A wider probe of 7 more load-accounting mutants kills 6. The one survivor is a narrower case that F1 did not ask for, so it is recorded as a SUGGESTION. No BLOCKER, MAJOR or MINOR is open. All five lenses are CLEAN. There is one RESIDUE (wording in two places) and one new SUGGESTION. R815-2 R1 is resolved, and R815-2 S1/S2 and R816-2's RES-1 and SUG-A to SUG-D are carried as they were.

## Scope as reconstructed

- **Contract.** #868 acceptance 1-5 and the round 2 and round 3 rulings, as reviewed in R815-2. The round 4 ruling (#868 issuecomment-6805224780) limits this round to controls only. It adds controls that can fail for the load accounting's armed-only, delivered-only and expiries-met counts and the frame equation, exactly as R815-2 F1's Required outcome and Verification state. It changes no harness behaviour, figure or firmware. Its gates are the wire-timing self-test, `run.py --ci`, the docs gates and `git diff --check` on a clean clone.
- **Delta** (`receipts/delta-scope.txt`). One commit by the round 4 executor, touching two files:
  - `tb/verilator/ctrl_wire_timing/wire_selftest.py` (+30 -13);
  - `tb/verilator/ctrl_wire_timing/README.md` (+5 -3).

  It does not touch the grader (`wire_grade.py`, byte-identical to `e3f96a67`), the model, the scenario, the build or reuse guard, the CI files, the firmware, any RTL or any gitlink. `git diff --check e3f96a67..dbe54e46` returns rc 0. **The ruling's scope holds.**
- **What the delta does.** `loaded()` gains four things:
  - a MAAP arm at 1630 ms + 1000 cycles (deadline 1720 ms), cancelled by an op-2 `TMR` write 500 cycles later. Its offer's burst is delivered whole.
  - The MAAP-arm scan now keeps only op-1 writes (`>> 30 == TMR_ARM`) and numbers them in cycle order (`sorted`).
  - A last AECP offer at 1795 ms with 1 of its 3 frames received.
  - An optional fourth frame under `load-acmp-0`'s tag.

  `LOADED` now expects MAAP 5 queued / 5 armed / 4 delivered / 3 met and AECP 2 queued / 1 whole / 1 partial / 4 frames. There is a new control, `load-offer-over-delivered`, and the words of `received-frame-unaccounted` follow the larger log (17 delivered, 26 received). The README's self-test section and control table are updated to match.

## What this review executed (receipts in this packet)

| Receipt | What | Result |
|---|---|---|
| `receipts/selftest-head.log` | `run.py --self-test` at the head | rc 0, `50 controls, 0 failed` (2.7 s) |
| `receipts/delta_mutants.log` (`scripts/delta_mutants.py`) | R815-2's 14 mutants. The only change from R815-2's copy (sha256 `27d4b028…`) is `over-delivery-check-gone`'s expected control, now `load-offer-over-delivered` | **14 of 14 KILLED**: `expiry-met-ignores-arm` and `partial-offers-never-counted` fail `clean-loaded`; `over-delivery-check-gone` fails `load-offer-over-delivered`; the other 11 fail their own controls, as before |
| `receipts/delta_mutants-r815-2-script-unchanged.log` | the R815-2 script, byte-unchanged | 13 KILLED. `over-delivery-check-gone` is scored SURVIVED with rc=1 and `failing=['load-offer-over-delivered']`: the self-test fails, but not through the `clean-loaded` control the old script expects. This matches the author's `round4/delta_mutants.log` |
| `receipts/f1_probe.log` (`scripts/f1_probe.py`) | Part A: the loaded log's MAAP-slot writes, LOAD lines and AECP tagged frames, read off the log. Part B: 7 more in-place load-accounting mutants, each restored | 6 KILLED and 1 SURVIVED (S3 below). Details follow this table |
| `receipts/evidence-manifest-verify.txt` (`scripts/verify_manifest.py`) | archive `fef5fca2` `review-evidence/665s8-r1/MANIFEST.json`, every entry re-hashed from the blob | 2,454 entries, 0 mismatched, 0 missing, 0 unlisted (843 under `author-r4`). The archive commit is **unsigned** (`verification.reason: unsigned`), so integrity rests on the hash manifest |
| `receipts/hosted-state.txt` | the hosted runs at the head, observed at 2026-11-11T20:51Z | `rtl-full`, `rtl-fast`, `docs`, `elaborate`: all `queued`, none executed |
| `receipts/clone-integrity.txt` | the review clone after the probes | HEAD, tree and index tree are `5225f4c7…`. No worktree or index differences in bytes or modes, nothing untracked or ignored, and every initialized submodule is at its gitlink. `external` is uninitialized and its gitlink is unchanged |

`scripts/f1_probe.py` Part B, one line per mutant:

- `delivered-counts-partial`: KILLED (`clean-loaded`).
- `frames-only-whole`: KILLED (`clean-loaded` and `received-frame-unaccounted`). The frame equation now sees a partial offer.
- `armed-only-delivered`: KILLED (`clean-loaded`).
- `partial-includes-undelivered`: KILLED (`clean-loaded`).
- `over-delivery-threshold-doubled`: KILLED (`load-offer-over-delivered`).
- `expiry-ignores-cancel`: KILLED (`clean-loaded` and `maap-expiry-cancelled`).
- `met-counts-partial`: **SURVIVED** (S3).

**Author packet spot-checks** (`fef5fca2`, `author-r4/receipts/round4/`):

- `gates/HEAD` is `dbe54e46…`.
- `gates/extra/logs/wire-self-test.log` reports `50 controls, 0 failed`, rc 0.
- `gates/rtl-fast/logs/rtl-fast__wire-timing__ci_step_21.log` reports `ctrl_wire_timing CI: PASS, wall 564 s`, both runs `0 finding(s)`, and both plants caught.
- `gates/wire-timing-ci-vs-head.txt` shows `results.json`, `wire.log`, `wire.txt` and `uart.txt` identical for both CI runs. So the figures are unchanged.
- `gates/wire-timing-job-table.md` shows 4 steps run, 10 not run with a reason, 0 bad.
- `gates/docs-yml-table.md` shows every docs job's steps at rc 0 or not run with a reason.
- `gates/extra/logs/diff-check.rc` is 0, against `1d6bf555`.
- `round4/delta_mutants.sha256` equals the R815-2 script's sha256.

These agree with the author's REVIEW READY (#868 issuecomment-6806398083) and with this review's own reruns.

## R815-2 F1 at this head

| Required outcome (R815-2 F1) | At `dbe54e46` | Status |
|---|---|---|
| a timer-triggered offer whose arm a later write cancels or supersedes before its deadline, delivered whole and reported as not met | `wire_selftest.py:256-257`: arm at cycle 163,001,000 with deadline 1720 ms, then cancel (`80000102`) at 163,001,500 (`receipts/f1_probe.log` Part A). `wire_grade.py` `expiries()` drops the arm because the cancel precedes its due cycle. The burst is delivered at 171,980,000 (2 frames). `LOADED` maap expects `delivered_offers=4`, `expiries_met=3` (`wire_selftest.py:286-287`) | Met |
| an offer delivered in part, reported in `partial_offers` | `wire_selftest.py:273`: `aecp` offer 1, 3 frames queued, 1 received under `load-aecp-1`. `LOADED` aecp expects `partial_offers=1`, `delivered_frames=4` | Met |
| optional: a control found by the over-delivery words | `load-offer-over-delivered` (`wire_selftest.py:467-468`), found by `LOAD: 4 frames of offer 0 of load acmp were received, 3 were queued` | Taken |
| Verification: `expiry-met-ignores-arm` and `partial-offers-never-counted` KILLED (and `over-delivery-check-gone` if taken); the other 11 still KILLED | `receipts/delta_mutants.log`: 14 of 14 KILLED | **Resolved** |

The ruling also names the armed-only, delivered-only and expiries-met counts and the frame equation. Each now has a killing control: `armed-only-delivered`, `delivered-counts-partial` and `partial-includes-undelivered`, `expiry-met-ignores-arm`, and `frame-equation-gone` and `frames-only-whole`.

**The fixture against the firmware.** The fixture's arm-cancel-arm sequence matches the firmware. In `third_party/tsn-c-stack/src/maap.c:125-141`, the final probe expiry calls `start_timer(m, false)` (arm), then `stop_timer` (cancel, via `sw/firmware/ctrl/maap/maap_mbx.c:22-27` `mbx_timer_cancel`), then `start_timer(m, true)` (the announce arm). The arm numbering stays consistent. Before this round, the scan counted every `TMR` write on the slot, and the clean log held no cancel. Now the op-1 filter excludes the cancel, and `sorted` keeps offer numbering in queue order, which is the order the grader numbers offers in.

## Findings

### RES-1 RESIDUE - Docs - `tb/verilator/ctrl_wire_timing/README.md:294`, `wire_selftest.py:246-247`, PR #879 body line 50, and `README.md:334` - the partial offer is described as one "the log ends inside", and the echo control as the "last" offer

- **Text 1.** README:294: "and a last offer the log ends inside, one of its three frames received". The `loaded()` docstring (wire_selftest.py:246-247) says the same, and so does PR body line 50 ("an offer the log ends inside, delivered in part").
- **Why text 1 is residue.** The fixture's partial offer begins at cycle 179,500,000 (1795 ms). Its frames would follow at +200 and +400 cycles, but the log runs to `MS 179900000 1799`, about 4 ms later (`receipts/f1_probe.log` Part A, and the log's tail). So the log does not end inside the offer; the fixture simply omits two frames. The grader's `partial_offers` does not depend on where the log ends, so no count, control, figure or verdict changes. Only the description of the fixture is inaccurate.
- **Text 2.** README:334 (`echo-skipped-after-the-announce`): "the loaded log's last offer with its echo skipped". The control changes `aecp` offer 0, at 1750 ms (its words name cycle 175,000,000). The new 1795 ms offer is now the loaded log's last.
- **Exact fix.**
  - README:294 and the docstring: replace "a last offer the log ends inside, one of its three frames received" with "a last offer delivered in part, one of its three frames received, as a run that ends while an offer's frames are queued leaves it".
  - PR body line 50: replace "an offer the log ends inside, delivered in part" with "an offer delivered in part".
  - README:334: replace "the loaded log's last offer with its echo skipped" with "the offer after the unrelated frames with its echo skipped".
  - Alternatively, move the offer's first frame to within 200 cycles of the log's last line, so the description becomes literally true. That is a self-test change, and the ruling's scope permits it.

### S3 SUGGESTION - Tests - `tb/verilator/ctrl_wire_timing/wire_grade.py:665`, `wire_selftest.py:241-287` - no control for an armed burst delivered in part

- **Evidence.** In `receipts/f1_probe.log`, the mutant `met-counts-partial` survives with `50 controls, 0 failed`. It replaces `whole and offer.at in fired[...]` with `bool(got) and offer.at in fired[...]`, so an armed burst delivered in part counts as meeting its expiry. README:165 defines "expiries met" as "the arms that expired with their burst delivered". The fixture's only partial offer is a step offer (`aecp`), and every MAAP burst is delivered whole or not at all.
- **Why this is not a finding.** F1's Required outcome (one cancelled arm delivered whole and not met, one offer delivered in part) is met in full. The grader line is correct by reading. No published run has a partial offer: every results row reads "0 in part", including the author's round-4 CI log. So no published "expiries met" figure is exposed.
- **Optional.** Make one armed burst partial in the loaded log, for example an ADP or MAAP arm whose deadline falls in the log's last 200 µs with 1 of its frames received. Expect it in `partial_offers` and not in `expiries_met`.

## Prior public review findings at this head

Each was read only after the independent pass over the diff.

| Finding | Required outcome | At `dbe54e46` | Status |
|---|---|---|---|
| R815-2 F1 (MINOR, Tests) | as above | as above | **Resolved** |
| R815-2 R1 (RESIDUE, PR body) | "The CI step at `267fc9815d` (the head keeps its harness, build and stimulus) …" | PR body line 84 now reads exactly that | Resolved |
| R815-2 S1 (SUGGESTION, Docs: cold figure in `CI_WORKFLOWS.md`) | optional | not taken, because the ruling limits the round to controls. `CI_WORKFLOWS.md` is unchanged in the delta | Carried (optional) |
| R815-2 S2 (SUGGESTION: `acmp()` local `window` shadows its parameter) | optional | not taken. `wire_grade.py` is unchanged | Carried (optional) |
| R816-2 RES-1 (RESIDUE, README:46 reuse sentence) | its exact fix | README:46 still reads "So a build is reused only at the tree it was built from." | Retained, for the manager's residue checklist |
| R816-2 SUG-A, SUG-B, SUG-D (optional) | optional | the delta touches none of their artifacts (the model, `acmp()` and `REUSE_CONTROLS` are unchanged) | Carried (optional) |
| R816-2 SUG-C / R816-1 SUG-2 (hosted wall time) | optional | no hosted run has executed at this head (`receipts/hosted-state.txt`: all queued) | Carried (optional) |

## Per-lens results (each applied at `dbe54e46`)

```text
[R815] PASS Conformance — receipts/delta-scope.txt, wire_selftest.py:241-287, third_party/tsn-c-stack/src/maap.c:125-141, sw/firmware/ctrl/maap/maap_mbx.c:22-27, author-r4 round4/gates/wire-timing-ci-vs-head.txt — the delta changes no stimulus, grader clause or figure (the grader is byte-identical to e3f96a67, and the CI runs' results.json and wire.log are identical at the head); the new fixture's arm, cancel and announce-arm sequence is the firmware's final-probe-expiry sequence; the "expiries met" semantics (an arm that expired with its burst delivered whole; an arm a later write precedes does not expire) are what LOADED now asserts; #868 acceptance 1-4 figures are unchanged from R815-2's check
[R815] PASS RTL — receipts/delta-scope.txt — no path under hdl/ or rtl/, no .sv, no mailbox.yaml, no firmware source, no Makefile and no gitlink in the delta; the model and build sources are unchanged, so R815-2's RTL coverage at e3f96a67 holds for everything this lens depends on
[R815] PASS Robustness — wire_grade.py:642-675 (unchanged) under wire_selftest.py's new cases, receipts/f1_probe.log, receipts/delta_mutants.log — the grader's failure paths now exercised by the delta: a cancelled arm before its deadline (expiry-ignores-cancel killed by clean-loaded and maap-expiry-cancelled), over-delivery under an offer's tag (found by its own words; doubled-threshold mutant killed), a partial offer at the run's end, and the frame equation with a partial offer (frames-only-whole killed by received-frame-unaccounted); refusal and reuse-guard paths are unchanged since R815-2
[R815] PASS Tests — wire_selftest.py:241-287,462-480, receipts/selftest-head.log, receipts/delta_mutants.log, receipts/f1_probe.log — 50 controls, 0 failed; R815-2 F1's Verification met (14 of 14 KILLED); 6 of 7 further load-accounting mutants killed; the survivor is S3 (SUGGESTION, beyond F1's Required outcome and with no published exposure); the new control can fail for the defect it names (over-delivery-check-gone and over-delivery-threshold-doubled both fail it)
[R815] PASS Docs — tb/verilator/ctrl_wire_timing/README.md:289-296,322-336, PR #879 body lines 19, 50, 52, 84, 160, 181, 186-190, #868 issuecomment-6806398083 — the README's counts (5/4/3 MAAP, 2/1/1 AECP) and both changed control words match LOADED and the self-test output verbatim; the PR body's 50 controls and mutant account match the receipts; the gate table's "49 controls" is correctly scoped to round 3's pass at e3f96a67; R815-2 R1 is fixed; the added source comments state behaviour and reason with an issue ID only (no lane label, round, reviewer ID or comment ID); RES-1 is wording only and carried to the residue checklist
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the delta scope (grader, stimulus and figures unchanged); the new fixture against `tsn-c-stack/src/maap.c` expiry; `LOADED` against the README's count definitions; the author's CI-vs-head identity | R815-3 | `dbe54e46f09802ab8b9bd3f3223d36bf4891394b` |
| RTL | CLEAN | `receipts/delta-scope.txt` (no RTL, firmware, mailbox, Makefile or gitlink) | R815-3 | `dbe54e46f09802ab8b9bd3f3223d36bf4891394b` |
| Robustness | CLEAN | `loads()`/`expiries()` under the new cancel, partial and over-delivery cases; `f1_probe.py` mutants | R815-3 | `dbe54e46f09802ab8b9bd3f3223d36bf4891394b` |
| Tests | CLEAN (S3 optional) | self-test run (50 controls); `delta_mutants.py` (14/14); `f1_probe.py` (6/7, survivor S3) | R815-3 | `dbe54e46f09802ab8b9bd3f3223d36bf4891394b` |
| Docs | CLEAN (RES-1 to the residue checklist) | harness README self-test section and control table; PR body; REVIEW READY; comment-rule scan of the added lines | R815-3 | `dbe54e46f09802ab8b9bd3f3223d36bf4891394b` |

## Real limits

- **No build or simulation was run by this reviewer.** The delta changes no model, build or stimulus. Source-head execution evidence is the author's published round-4 receipts (hash-verified, spot-checked above). No manager source bank runs at this head, and none is claimed.
- **Hosted evidence.** At observation, all four hosted workflows at this head were `queued`, and none had executed. So acceptance 5's hosted wall time is still unproven. Locally, the author's round-4 CI step passed in 564 s on four uncontended CPUs with the netlist cached. The cold fresh-runner replica took 1,299 s at `fbe5acc983` (R815-2).
- **Unsigned packet.** The evidence archive commit `fef5fca2` is unsigned, so integrity rests on its hash manifest, verified at 2,454 of 2,454.
- **Physical calibration was not run.** Field skips are not hardware proof.
- **The mutation probes are in-place source edits of a pure-Python grader**, checked only against the synthetic self-test logs. They were not rerun against the published loaded `wire.log` files, which are over 200 KB and present only as sha256 values.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `dev-soft-core`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`; the lane's merge base is `1d6bf555`), and link its builder and native-bank receipts.
- Own hosted and act acceptance at the exact head: `rtl-fast` (including `wire-timing`, acceptance 5's hosted wall time), `docs`, `elaborate`, and `rtl-full` once marked ready.
- Decide the second positive. R816-2 is POSITIVE at the ancestor `e3f96a67`. This delta changes artifacts in the Tests and Docs lenses' scope (`wire_selftest.py`, the README). Under AGENTS.md section 7, those two lenses' coverage at `e3f96a67` does not carry to `dbe54e46` without a covering round at a head that includes the change.
- Carry the residue checklist items: this report's RES-1 and R816-2 RES-1.
- The out-of-lane Issue for the CPU budget harness's GET_AVB_INFO row (`tb/verilator/ctrl_service_budget/scenario.py:464`, round 3 ruling item 2), as the author's open risks list.

R815-3 FINISHED
