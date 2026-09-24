[R266] POSITIVE - exact head 022290e4c94a23b9ee97852b6c1c2ee2c1f25352

Round R266-4, internal independent review of issue #532 / PR #533, correction round 3. Exact head `022290e4c94a23b9ee97852b6c1c2ee2c1f25352`, tree `b9740a963ee3833cfe7d7be986ef6233ba033d1c`. Source base `ede8d48e`, merged dev `759da623`, live dev `3d2f3e31` (not built here).

**No open BLOCKER, MAJOR or MINOR.** All five lenses are covered clean at this head. One SUGGESTION (S1) is recorded; it is optional and does not affect coverage.

**The round's six findings are resolved**, each by a case that fails deterministically when its guard is removed:

| Finding | Resolved by |
|---|---|
| R266-3 F1 | slot B's isolation control |
| R266-3 F2 = R267-3 F1 | a failed network query after removal |
| R266-3 F3 = R267-3 F2 | four one-sided overlap cases |
| R267-3 F3 | the realistic OOM-at-cap fixture |

**Mutant results:**

- **Full set.** My round-3 set (56 mutants plus a control) gives 51 KILLED and 6 SURVIVED in each uid mode. The survivors are exactly the control, the two documented no-case guards, and the three mutants ruled not protective.
- **Overlap repeats.** D05-D08 are killed 12 of 12 each, each by its own one-sided case. F06, G07 and G08 are killed 12 of 12 each. The control survives 24 of 24.
- **Live checks.** They are byte-identical to `604297bb`.

This section, the findings and the ledger come from my own pass over the diff and my own probes. The disposition of prior findings follows the ledger. R266-3 was my own previous round; I reused its mutant scripts, but read its report only after this pass.

## Scope reconstructed

- **Governance:** AGENTS.md sections 3-8; CONTRIBUTING.md 2.1; docs/README.md.
- **Issue #532:**
  - body and acceptance 1-6;
  - the A203 DECISION (issuecomment-5796770637) and the round-1 and round-2 amendments;
  - the A10 assignment for this round (issuecomment-5806806703): "Each case must fail deterministically when its guard is removed, with no reliance on timing";
  - the A232 REVIEW READY (issuecomment-5809642460).
- **Interface authority:** `docs/testing/CI_WORKFLOWS.md` "Act-first local replication" (bootstrap rule) and "Parallel replay slots".
- **Diff:** `604297bb..022290e4` is five one-line commits over three files, 105+/37- (`receipts/diff-scope-022290e4.txt`).
  - `scripts/act_ci.py`: +5, one hunk, inside `selftest_slot_memory_cap` (test only).
  - `scripts/act_slot_proof.sh`: +62/-20. Every hunk is inside the stand-in runner (`:367-485`), the stand-in sudo (`:488-555`) or the case table (`:610-655`).
  - `docs/testing/CI_WORKFLOWS.md`: +38/-17.
  - Against the merged dev `759da623`, the PR's own change is still four files, with no `.github/` path (acceptance 6).

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### S1 - SUGGESTION - Tests, Docs - the late-refusal case's collision holder also rests on the fixed hold, which the doc does not list

**Where:**

- `scripts/act_slot_proof.sh:222-232` (`await_holder`: marker grep at `:226`, then status test at `:227`);
- the stand-in's late-refusal holder, `:464-466`;
- `docs/testing/CI_WORKFLOWS.md:1986-1996`;
- PR body, "The stand-in runs hold their slots until the proof has judged them, not for a timer".

**Evidence** (`receipts/hold-sensitivity-022290e4.txt`, `scripts/hold_probe.sh`, `scripts/h01_hold0_repro.sh`):

- In the late-refusal case the holder cannot wait for its rival, because the rival waits for the holder to exit. So the holder holds only for the fixed `FAKE_HOLD`.
- The live `await_holder` greps the marker and then tests the status file. If the run prints its marker and ends between those two steps, it returns "never held". That path is fail-closed, and R267-3 already noted it under Q25.
- With the stand-in's hold forced to 0 (diagnostic only; the shipped default is 3 s), that happens:
  - The late-refusal case then records `FAIL collision slot 1: the holder never held the slot`.
  - The case grades on the substring `FAIL collision slot 1`, so that line satisfies it.
  - H01 (rival lateness not required) then SURVIVED once in 8 loaded runs, and once in 24 reproduction runs. The kept SUMMARY shows the "never held" line, with the holder's marker in its log.
- At the shipped 3 s hold, H01 and H08 were killed 12 of 12 each under 8-way load, and in both full runs. So the margin is 3 s between two adjacent shell statements.
- The doc names the never-overlap case as the only fixed-time exception. It does not say that the late-refusal holder also holds only for the fixed time.

**Impact:**

- This is a precision gap in the documented residual, not a live-proof hole. The live path fails closed.
- It is the same class as the disclosed honest-path hold: a fixed hold that covers only the proof's immediately following step.

**Optional change:** either of these.

- Name the late-refusal holder beside the honest collision holder in `CI_WORKFLOWS.md:1986-1996`.
- Or make `await_holder` re-check the marker once it sees the status file, which would remove the race. That is a live-check edit, so it would re-open Conformance.

## Focus checks

### 1. The corrections: my round-3 mutants re-run at this head

**Method.**

- `scripts/proof_mutants.py` is my round-3 set, unchanged (its MUTANTS list is byte-identical to R266-3's). Every edit applies exactly once to the head file (sha256 `939c76db...`).
- The runs used `scripts/run_parallel_mutants.sh`, four self-tests at a time. Each ran inside `scripts/sandbox.sh`: new user and network namespaces with only `lo`, as uid 1000 and as namespace uid 0.
- Baseline at the head: `--selftest` PASS, 44 cases, in both modes, about 26 s each (`receipts/proof-selftest-head-*.txt`).

**Results** (`receipts/proof-mutants-head-uid1000.txt` and `-uid0.txt`; identical in both modes):

| Outcome | Mutants |
|---|---|
| KILLED (51) | A01, A04-A06, B01, B02, B04, B05, C01-C08, D01-D08, E01-E03, F01-F07, G01-G08, H01-H08, I01 |
| SURVIVED, documented no-case guards | B03 (non-root writability), I02 (ten-`PASS` backstop) |
| SURVIVED, ruled not protective in R266-3 | A02, A03, E04 (rulings unchanged; live code unchanged) |
| Control X00 | SURVIVED |

**Overlap repeats** (`receipts/proof-mutants-repeats-022290e4.txt`; 8 self-tests at a time; 6 runs per mode):

- **D05-D08: 12 of 12 KILLED each, every time by its own one-sided case.**

  | Mutant | Its own case |
  |---|---|
  | D05 | "run A dies before taking slot A while run B holds slot B" |
  | D06 | "run B dies ..." |
  | D07 | "run A is refused after taking slot A ..." |
  | D08 | "run B is refused ..." |

  - "the parallel runs never overlap" also failed in 3-7 of the 12 runs, varying with start order, as the doc states.
  - At round 3, D05, D06 and D08 were each killed only 3 of 6.
- **F06, G07 and G08: 12 of 12 KILLED each,** by "the isolation network cannot be queried after removal" and "only slot B reaches the default daemon's container" respectively.
- **H01 and H08: 12 of 12 KILLED each.**
- **Control X00: SURVIVED 24 of 24.**
- Across 262 self-test runs at the default hold, the honest case failed only under mutants that break it on purpose (C08, D01, Z01, Z02). No honest-case failure was spurious.

**Hold-independence of the round's kills** (`receipts/hold-sensitivity-022290e4.txt` C). With the stand-in's fixed hold forced to 0 under 8-way load:

- D05-D08, F06, G07 and G08 were still killed by their own case in 8 of 8 runs each. So their grading is event-driven, not timed.
- Only the honest case (documented) and the late-refusal attribution (S1) moved.

### 2. The live checks are byte-identical to 604297bb

`receipts/diff-scope-022290e4.txt`:

- lines 1-366 of `act_slot_proof.sh` (everything before `fake_runner_source`, which holds all ten live checks): sha256 `c8212f21...` at both heads;
- `main()`: `9819b1fe...` at both heads;
- the 18 hunks all map inside the stand-ins or the case table;
- `act_ci.py` has one hunk, `@@ -12205,0 +12206,5 @@` in `selftest_slot_memory_cap`.

### 3. The documented residuals

**Q32, "sequencing only": agreed.**

- My Z01 is the same edit as R267-3's Q32: the collision rival starts without `await_holder`. Z02 judges the collision without `wait "$holder"`. Both are killed 8 of 8, only through the honest case (`receipts/sequencing-mutants-022290e4.txt`).
- R267-3's own Q32 was killed as root and survived as user in one run each (`receipts/r267-3-proof-mutants-022290e4.tsv`).
- Analysis at `act_slot_proof.sh:322-343`: without the wait, either of two things happens.
  - The holder takes the lock first. The rival is then refused on the lock while the holder holds, which is a genuine collision.
  - The rival takes it first. The holder is then refused, never completes, and the check records `FAIL`.
- Without `wait "$holder"`, the holder's verdict file does not exist yet, so `complete` fails.
- No path yields a false `PASS`. Removing either wait costs liveness only.

**The fixed 3 s hold on the honest path: acceptable, with S1 as its missing sibling.**

- Its only failure mode is a spurious self-test `FAIL`, which is fail-closed.
- At hold 0 the honest case still passed 6 of 6 when run alone. It flaked only under 8-way load.
- At 3 s the honest case never failed spuriously in 262 loaded runs.
- The doc discloses it (`CI_WORKFLOWS.md:1989-1991`).

### 4. The case list against the doc

- The table (`act_slot_proof.sh:611-654`) has 44 rows: honest 1, bad starts 7, completed-run grading 6, interrupt gate 3, parallel 8, isolation 12, collisions 7.
- `CI_WORKFLOWS.md:1954-1984` lists the same groups and members, one for one.
- "Each of those last four leaves exactly one of the overlap check's four conditions" holds. Each case's stand-in, read at `:423-453`, falsifies exactly one conjunct of `:307-308`, and D05-D08 confirm it.
- "Two guards have no case" (`:1998`) matches B03/I02.
- The restated reason for B03 (`:2001-2005`) is accurate. It needs a mode-overriding capability, such as the one my round-3 probe used in a user namespace, or a file system that ignores the mode. That resolves R266-3 S1.

### 5. The OOM-at-cap runner arm

- **The arm.** `act_ci.py:12206-12210` adds `low 0 high 0 max 7 oom 1 oom_kill 0 oom_group_kill 0`, which must be refused with "... 1 time(s)". This is the realistic slice-local file.
  - In cgroup v2, `oom` is counted on the memcg whose limit was hit, and `oom_kill` on the victim's own memcg.
  - The slice holds no process, under the no-internal-process rule. So its own `oom_kill` stays 0.
  - The comment at `:12206-12207` states this correctly.
- **Static check** (`receipts/r267-3-slot-mutants-static-022290e4.txt`; `act_ci.py` was not executed). R267-3's published S00-S10 each apply exactly once to the head. On a model of the guard:
  - S04, S07 and S10 stop refusing only the new fixture, so only the new arm can kill them.
  - At `604297bb` no OOM fixture caught them.
  - S06 loses both fixtures.
- **Hosted execution.** The `docs-check` check run attached to this head ran `python3 scripts/act_ci.py --selftest` with 425 `ok` and 0 FAIL, including the new arm (`receipts/hosted-docs-check-act-ci-selftest-excerpt-022290e4.txt`).
- **Doc.** The memory-cap bullets (`CI_WORKFLOWS.md:1832-1844`, `:2042-2047`) match the arms. The new sentence that cached-file reclaim makes a nonzero `max` count routine is accurate.

## Gates and hosted evidence at the head

**Focused gates, all rc 0** (`receipts/focused-gates-summary.txt`, logs in `receipts/gates/`):

- `check_baremetal_only.py --check` and `--selftest`;
- `docs_check.py`;
- `check_em_dash.py --base` from `759da623`, `ede8d48e` and `604297bb`;
- `check_py_idiom.py`, `check_sh_idiom.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_doc_paths.py`, `check_doc_style.py`, `ci_events.py --check`, `check_feature_status.py`;
- `git diff --check` from `759da623`, `604297bb` and `ede8d48e`;
- `bash -n` on the proof script.

None of them executes `act_ci.py`.

**Hosted, exact head** (`receipts/hosted-check-runs-022290e4.tsv`, fetched 08:05Z):

- 22 check runs: 21 executed and succeeded, including the seven required contexts (`rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites`, `yosys-portability`).
- Verilator shards 0-4/5 and Yosys shards 0-3/4 executed, with nonzero durations.
- One skipped: "Physical gPTP (nightly and manual)", which is not hardware proof.
- The manager owns hosted and act acceptance.

## Lens results

```text
[R266] PASS Conformance - issue #532 acceptance 1-6 and the DECISION as amended vs receipts/diff-scope-022290e4.txt (act_slot_proof.sh live lines 1-366 and main() byte-identical to 604297bb; act_ci.py changed only inside selftest_slot_memory_cap; no .github path in 759da623..HEAD) - acceptance 2-6 hold as at 604297bb, no refusal weakened, no workflow change; acceptance 1 is pending the manager's live proof and is not banked
[R266] PASS RTL - scripts/act_ci.py at 022290e4: runner lifecycle and cap placement unchanged from 604297bb (one hunk, @@ -12205,0 +12206,5 @@, test only); the runner/proof line contract act_slot_proof.sh:171, :218, :224, :239-240 unchanged; the new fixture's cgroup-v2 semantics (oom on the limiting memcg, oom_kill on the victim's) checked against act_ci.py:4470-4486 - interfaces and ordering hold
[R266] PASS Robustness - act_slot_proof.sh:222-232, :268-281, :322-343 (unchanged, fail-closed, including the marker/status race under hold 0, receipts/hold-sensitivity-022290e4.txt); the new stand-in waits :378-391, :418, :426-428, :452, :463-465 are each bounded (1200 x 50 ms) so a broken proof cannot hang its self-test; SIGKILL cases leave no lock - no unbounded or fail-open path
[R266] PASS Tests - act_slot_proof.sh:367-655 at 022290e4 under 56 mutants plus a control (both uids), 12-run repeats of D05-D08, F06, G07, G08, H01, H08, a hold-0 probe, 2 sequencing probes, and R267-3's Q25-Q28, Q32, Q52, Q53, Q61, Q62; act_ci.py:12206-12210 vs R267-3's S00-S10 (static) and the hosted 425-ok run - every protective check has a case that fails deterministically at the shipped hold; S1 is a suggestion
[R266] PASS Docs - docs/testing/CI_WORKFLOWS.md:1832-1844, :1954-2005, :2042-2047 at 022290e4 against the 44-row table, the stand-in code and the runner arms; act_ci.py:12206-12207 comment; PR body - accurate; S1 (a precision gap in the residual's wording) is a suggestion
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #532 acceptance 1-6 and the DECISION as amended. `receipts/diff-scope-022290e4.txt`: live proof lines 1-366 and `main()` byte-identical to `604297bb`; one test-only hunk in `act_ci.py`; no workflow path. The proof's ten checks (`act_slot_proof.sh:139-364`) against `CI_WORKFLOWS.md:1916-1952`. Acceptance 1 is a pending duty, not banked. | R266-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| RTL | CLEAN | No HDL, TB or synthesis path in the PR. Runner lifecycle and cap check `act_ci.py:4455-4494`, unchanged. Runner/proof output contract `act_slot_proof.sh:171`, `:218`, `:224`, `:239-240`. The new fixture's cgroup-v2 semantics. | R266-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| Robustness | CLEAN | `act_slot_proof.sh:222-232`, `:268-281`, `:322-343` (fail-closed, incl. under hold 0). The new bounded stand-in waits `:378-391`, `:418`, `:426-428`, `:452`, `:463-465`. `act_ci.py:4470-4486` refusal paths. | R266-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| Tests | CLEAN | Proof self-test `act_slot_proof.sh:367-655` with 57 mutants in both uids, repeats, hold-0 and sequencing probes, and R267-3's relevant set. Runner arm `act_ci.py:12206-12210` with the static S00-S10 check and the hosted 425-ok run. | R266-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| Docs | CLEAN | `CI_WORKFLOWS.md:1832-1844`, `:1954-2005`, `:2042-2047`; `act_ci.py:12206-12207`; PR body. S1 is optional. | R266-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |

## Prior public findings, resolved or retained at this head

Read after the verdict, findings and ledger above were written (R267-3: issuecomment-5806803318; R266-3: issuecomment-5806223294).

| Finding | Severity; lenses as filed | Status at 022290e4 | Evidence |
|---|---|---|---|
| R266-3 F1: slot B's isolation control has no failing case | MINOR; Tests, Docs | RESOLVED | New fault `slot2-reaches-container` and case "only slot B reaches the default daemon's container" (`act_slot_proof.sh:506`, `:510`, `:637`). G07 and G08 KILLED 12 of 12 each, both uids. R267-3's Q62 KILLED in both uids. Doc `CI_WORKFLOWS.md:1976`. |
| R266-3 F2 = R267-3 F1: a failed network query after removal has no case | MINOR; Tests, Docs | RESOLVED | Fault `network-query-fails` (`:539-541`) and its own case (`:646`); the old case is renamed to the container's (`:645`). F06 KILLED 12 of 12, both uids. R267-3's Q52 and Q53 KILLED in both uids. The doc sentence matches the two cases. |
| R266-3 F3 = R267-3 F2: overlap guards killed only by a race | MINOR; Tests (R267-3: Tests, Docs) | RESOLVED | Four one-sided cases (`:631-634`), stand-in `:423-453`. D05-D08 KILLED 12 of 12 each, each by its own case, and also 8 of 8 at hold 0. R267-3's Q25-Q28 KILLED in both uids. The doc states which case is order-dependent and why each condition has its own case. |
| R267-3 F3: OOM-at-cap refusal pinned only by a two-OOM fixture | MINOR; Tests | RESOLVED | Arm `act_ci.py:12206-12210` ("oom 1, oom_kill 0"). By static check, S04, S07 and S10 lose only that fixture, so only it can kill them. Hosted exact-head run: the arm `ok`, 425 ok, 0 FAIL. The author's receipts record S04, S07 and S10 KILLED; I did not re-execute them (limits). |
| R266-3 S1: the reason the writability guard has no case | SUGGESTION; Docs, Tests | TAKEN, accurate | `CI_WORKFLOWS.md:2001-2005`. |
| R267-3 SG1: slot-B variants of the verdict and isolation faults | SUGGESTION; Tests | TAKEN | Q61 and Q62 KILLED in both uids. |
| R267-3 SG2: the long line at 1835 | SUGGESTION; Docs | TAKEN | Rewrapped (`:1832-1844`). |
| R267-3 SG3: a nonzero cap count is routine | SUGGESTION; Docs | TAKEN, accurate | `:1838-1841`. |
| R266-1 F1-F6, R267-1 F1-F5, R266-2 F1, R267-2 F1-F2, manager source validation r1 | as filed | still RESOLVED | Resolved at `604297bb` by R266-3 and R267-3. Since then only the stand-ins, the case table, one runner arm and the doc changed, and the runner's live code and the proof's live checks are byte-identical (`receipts/diff-scope-022290e4.txt`). Every mutant pinning them in my set is still KILLED. `check_baremetal_only.py --check` reports 0 findings. |

Nothing is retained.

## Real limits

**Runner not executed.** This round did not run `scripts/act_ci.py`: not host-side, not imported, and not its self-test.

- Its 425-check result rests on the hosted `docs-check` check run attached to this head.
- The S04, S07 and S10 kills rest on a static check plus the author's receipts; they were not re-executed here.

**Nothing live.**

- No Docker, act, sudo, host privilege, slot, cgroup or hardware was used.
- The cgroup-v2 counter semantics were checked by reading.
- Acceptance 1 is NOT MET until the manager's audited live proof.
- Physical calibration was NOT RUN. The skipped hosted context is not hardware proof.

**Probe method.**

- All proof self-tests and mutants ran on scratch copies, in new unprivileged user and network namespaces. R267-3's published driver ran in its own published namespace sandbox.
- Kill rates were measured with 4 or 8 self-tests at a time, on a 128-thread host.
- `FAKE_HOLD=0` is a diagnostic environment setting; the proof's bytes were unchanged.

**Not run, not claimed.**

- No full parent, PP, gPTP, Yosys or builder bank was run.
- The scoped Verilator was not used, because no HDL is in the diff, so its identity was not checked.
- The manager's source static/builder and native banks for this head are still running.
- The final current-dev candidate was not built (source base `ede8d48e`, live dev `3d2f3e31`).

**Clone state** (`receipts/clone-integrity-022290e4.txt`, RESULT EXACT):

- HEAD, tree and index are exact; there are no hidden index flags and 0 untracked or ignored entries.
- All 873 tracked files match their blob and mode.
- `gptp-processor` `c1b61743`, `protocol-processor` `424c688f` and `third_party/verilog-axis` `48ff7a7e` are at their pins and clean. `external` (`efeb541a`) is uninitialised.
- The focused gates had left five ignored bytecode files, created at 09:58 by this round. They were removed before the final check.

## Pending manager duties

1. **Live proof.** Run it with an audited, installed copy of the reviewed runner: `act_slot_proof.sh --selftest` first, then the ten checks, including an `rtl-full` pair whose logs record each slot's peak and cap-hit count. This covers acceptance 1 and the live halves of 2 and 3.
2. **Banks and acceptance.** Publish the source static/builder and native banks for this head, and own hosted and act acceptance.
3. **Merge turn.** Build and gate the current-dev candidate (source base `ede8d48e`, live dev `3d2f3e31`). After merge, run containment, then close the issue and move the card. The merge bar also needs the external review's verdict and the full completion bar.
4. **S1 is optional.** If it is taken as a live-check edit (`await_holder`), Conformance, Robustness and Tests need re-covering at that head.

## Packet (every file below is listed in MANIFEST.sha256)

**Scripts:**

- `scripts/sandbox.sh`
- `scripts/proof_mutants.py` (the R266-3 set, unchanged)
- `scripts/run_parallel_mutants.sh`
- `scripts/r4_sequencing_mutants.py`
- `scripts/hold_probe.sh`
- `scripts/h01_hold0_repro.sh`
- `scripts/r267_3_slot_static.py`
- `scripts/focused_gates.sh`
- `scripts/clone_integrity.sh`

**Receipts:**

- `receipts/proof-selftest-head-uid1000.txt` and `-uid0.txt`
- `receipts/proof-mutants-head-uid1000.txt` and `-uid0.txt`
- `receipts/proof-mutants-repeats-022290e4.txt`
- `receipts/hold-sensitivity-022290e4.txt`
- `receipts/sequencing-mutants-022290e4.txt`
- `receipts/r267-3-proof-mutants-022290e4.tsv`
- `receipts/r267-3-slot-mutants-static-022290e4.txt`
- `receipts/diff-scope-022290e4.txt`
- `receipts/focused-gates-summary.txt` and `receipts/gates/*.log`
- `receipts/hosted-check-runs-022290e4.tsv`
- `receipts/hosted-docs-check-act-ci-selftest-excerpt-022290e4.txt`
- `receipts/clone-integrity-022290e4.txt`

R266-4 FINISHED
