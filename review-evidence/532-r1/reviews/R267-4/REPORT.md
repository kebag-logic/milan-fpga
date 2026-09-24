[R267] POSITIVE - exact head 022290e4c94a23b9ee97852b6c1c2ee2c1f25352

# R267-4: external review of PR #533 (issue #532), correction round 3

- Head `022290e4c94a23b9ee97852b6c1c2ee2c1f25352`, tree `b9740a963ee3833cfe7d7be986ef6233ba033d1c`. The review clone was verified byte-exact after every probe (`receipts/clone-integrity-after.txt`).
- Round under review: A232's five commits on `604297bb` (`0a3e66f7`, `4bbd06bd`, `544bfdeb`, `b12fc6f6`, `022290e4`). They answer R266-3 F1-F3 and R267-3 F1-F3, all MINOR self-test coverage findings.
- Source base `ede8d48e`; lane-owned diff `759da623..022290e4`.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open under any lens. All six round-3 findings are resolved, and each is shown by the mutants that exposed it. There is one new SUGGESTION (S1), and one earlier suggestion is still not taken. Neither affects coverage.

## How this round was run

1. **Public record, read in order.** AGENTS.md, then issue #532 with every public comment: the assignment, the DECISION with its A213 and A220 amendments, and the A203, A208, A213, A220 and A232 REVIEW READY records. Then the round diff and the full head `scripts/act_slot_proof.sh`, the memory-cap code and arms in `scripts/act_ci.py`, and `docs/testing/CI_WORKFLOWS.md:1709-2053`.
2. **Own tools.** My round-3 mutant tools came from evidence commit `d2352cdd` (`R267-3/bin`, `evidence-copies`). Their blob ids match the originals at `ead93cd7`.
3. **Order of work.** I wrote my independent pass (`receipts/independent-pass-before-prior-findings.md`) before opening any prior finding text. Only after that did I read R266-3 (issuecomment-5806223294) and R267-3 (issuecomment-5806803318) and replay R266-3's published mutant list.
4. **Where candidate code ran.** All candidate code ran from `git archive` exports or a disposable clone. It ran only inside an unprivileged, network-less namespace sandbox (`bin/sandbox.sh`), as uid 1000 and as uid 0. Nothing ran live: no Docker, act, sudo, privilege, hardware or host act runner. No more than 8 top-level jobs ran at once.

## Findings

No BLOCKER, MAJOR or MINOR.

### R267-4-S1 - SUGGESTION - Tests, Docs - the "neither run reports its own slot daemon" case still holds for a fixed time, so Q23 is killed only while its two runs start within 3 s of each other

**Where:**
- `scripts/act_slot_proof.sh:461-466`: `marked` is false under `slot-unannounced`, so those runs skip `await_judgment` and hold for `FAKE_HOLD` (3 s).
- The case, `:630`.
- The guard it protects, `:224`: `await_holder` requires `act-ci: slot N: own daemon` for a slot and not the generic `act-ci: running`.
- The doc, `docs/testing/CI_WORKFLOWS.md:1986-1996`, names "the case whose runs never overlap" as the only case whose runs hold for a fixed time. The stand-in comment at `act_slot_proof.sh:459-460` also omits the unannounced runs.

**Evidence:**
- `bin/unannounced_skew_probe.sh` grades that case alone and delays run B's start.
- At a 0 s or 1 s delay, mutant Q23 (generic marker accepted) is KILLED. At a 4 s delay it SURVIVES, because the overlap then fails for another reason.
- The head passes the case at every delay: its grading does not depend on timing.
- Q23 is killed only by this case, and in every run here: 4 full runs plus 10 focus repeats, both modes.

**Why this is only a suggestion:**
- The kill fails only if two back-to-back background launches are more than 3 s apart. The self-test never came near that, not even with 8 self-tests running at once (`receipts/proof-selftest-stress-8x2-022290e4.txt`).
- It is not the ordering-dependent gap of R267-3 F2, where the kill rate was about half.
- The doc sentence is about the grading, which is true.

**Optional change:**
- Let the unannounced runs wait for any `overlap` record, which makes Q23's kill schedule-free at a cost of about 36 s (the proof's `await_holder` bound), or say in the doc that this case also holds for a fixed time.
- Taking neither option leaves coverage unaffected.

### Suggestion carried over, not taken

- **R267-2 S1:** no workflow runs `scripts/act_slot_proof.sh --selftest`. That is still true at this head: 0 matches in the hosted `docs-check` log (`receipts/hosted-docs-check-excerpt-022290e4.txt`).
- It is optional. Taking it would edit a hosted workflow, which acceptance 6 constrains.

## Round-3 findings: resolution at this head

| Finding | Severity; lenses as filed | Status | Evidence at 022290e4 |
|---|---|---|---|
| R266-3 F1: slot B's isolation control has no failing case | MINOR; Tests, Docs | RESOLVED | The new stand-in fault `slot2-reaches-container` (`act_slot_proof.sh:506-510`) makes only slot 2 reach the container. Its case (`:637`) fails on `FAIL isolation slot 2`. R266-3's own G07 and G08, replayed verbatim, are KILLED by that case as uid 1000 and uid 0. My Q62 is KILLED in 14 of 14 runs. The doc lists the case (`CI_WORKFLOWS.md:1977`). |
| R266-3 F2 = R267-3 F1: a failed network query after removal has no case | MINOR; Tests, Docs | RESOLVED | New fault `network-query-fails` (`act_slot_proof.sh:540-541`). Its case (`:646`) fails on `FAIL isolation target not proved absent`. R266-3's F06 and my Q53 are KILLED in every run by exactly that case, and Q52 by the container case (`:645`). The doc text (`CI_WORKFLOWS.md:1978-1980`) now matches the two cases. |
| R266-3 F3 = R267-3 F2: overlap conjuncts killed only by scheduling | MINOR; Tests, Docs | RESOLVED | See the table below. |
| R267-3 F3: the OOM at the cap is pinned only by a two-OOM fixture | MINOR; Tests | RESOLVED | New fixture `oom 1, oom_kill 0, oom_group_kill 0` (`act_ci.py:12206-12210`), refused naming the cap. S04, S07 and S10 are KILLED only by that arm (`failed-arms=` column) in 4 of 4 runs, as uid 1000 and 0. S00 survives. The fixture's comment matches cgroup v2: the slice has no tasks of its own, so its local `oom_kill` stays 0. |
| R266-3 S1 (suggestion) | Docs, Tests | taken, accurate | `CI_WORKFLOWS.md:2001-2005`. With no write bit in the mode, a named-user ACL still shows up in the group bits and is caught by `-perm /0222`. What remains really does need a mode-overriding capability or a filesystem that ignores the mode. |
| R267-3 SG1-SG3 (suggestions) | Tests, Docs | taken, accurate | SG1: `parallel-break-b` (`act_slot_proof.sh:628`) and `slot2-reaches-container`; Q61 and Q62 KILLED in 14 of 14 runs. SG2: `CI_WORKFLOWS.md:1835-1843` rewrapped. SG3: `:1838-1840` is accurate, because memory usage counts page cache and reclaim at `memory.max` raises `max`. |

**How F3 is resolved.** Each of the four one-sided cases (`act_slot_proof.sh:631-634`) leaves exactly one overlap condition false:

| Case | Condition left false (mutant that removes it) | Result |
|---|---|---|
| `a-never-holds`: run A is killed before its lock while B holds its slot | `await_holder A` (Q28 / D05) | KILLED |
| `b-never-holds` | `await_holder B` (Q27 / D06) | KILLED |
| `a-refused-first`: A takes its slot, is refused, and stays alive until judged; B locks only after that | `! ended A` (Q25 / D07) | KILLED |
| `b-refused-first` | `! ended B` (Q26 / D08) | KILLED |

- `bin/one_sided_probe.sh` grades each case alone, in natural, forced A-first and forced B-first start order. The head passes all 12 case runs and each mutant is KILLED in all 12, in both uid modes (`receipts/one-sided-probe-022290e4-{user,root}.txt`). So each kill depends on neither the start order nor any other case.
- In the full self-test, Q25-Q28 were KILLED in 4 of 4 full runs and 10 of 10 focus repeats.
- R266-3's D05-D08 were KILLED in both modes.
- The "never overlap" case alone is still order-dependent (`receipts/overlap-order-probe-022290e4-user.txt`), exactly as the doc says (`CI_WORKFLOWS.md:1992-1996`).

## Requested focus checks

1. **The ten live checks are unchanged.**
   - `act_slot_proof.sh` lines 1-365 hash to `571c2d96...` at both `604297bb` and the head. That span holds every check, `record`, `complete`, `await_holder`, `ended`, `isolation`, `parallel`, `collide`, `prove` and the ten-`PASS` gate.
   - `main` is identical too.
   - The round changes only the stand-in runner, the stand-in sudo and the case table (`receipts/diff-scope-604297bb-022290e4.txt`).
   - In `act_ci.py`, only the one fixture row in `selftest_slot_memory_cap` changed. No workflow file changed, and `check_baremetal_only.py` did not change.
2. **Own round-3 proof set, Q00-Q62, on the head.** 4 full runs: uid 1000 twice and uid 0 twice (`receipts/proof-mutants-r267-3-022290e4-*-run*.tsv`).
   - Every run KILLS Q01-Q04, Q06, Q07, Q09-Q23, Q25-Q31 and Q33-Q62.
   - The survivors in every run are Q00 (control), Q08 and Q56 (the two documented no-case guards), and Q05, Q24, Q49 and Q59 (masked or not protective, the round-3 rulings, unchanged).
   - Q32 survived in 1 of the 4 runs.
   - Focus repeats of Q00, Q23, Q25-Q28, Q32, Q52, Q53, Q61 and Q62, 5 per mode (`receipts/proof-mutants-focus-repeats-022290e4-*.tsv`): every named mutant KILLED every time and Q00 SURVIVED every time, except Q32 (user 3 of 5, root 5 of 5).
3. **Own round-3 slot set, S00-S10.** 2 runs per mode (`receipts/slot-mutants-r267-3-022290e4-*.tsv`): S01-S10 KILLED every run, and S00 SURVIVES.
4. **Published sets (no regression).**
   - Slot mutants: A213's 53 plus A220's 3 are all KILLED in both modes, and the control survives (`receipts/published-slot-mutants-022290e4-*.tsv`). `R266 lock-blocking` deadlocks the busy-lock arm and is recorded KILLED by a 240 s bound (rc 124), as at `604297bb`.
   - Proof mutants:
     - A213: 14 of 14;
     - A220: 10 of 10;
     - R267-2: 13 of 13;
     - R266-2: 10 of 11, where M9 (the ten-`PASS` backstop) survives as ruled;
     - R266-3, verbatim: 51 KILLED; the survivors are X00, B03, I02 (documented) and A02, A03, E04 (ruled not protective by that round).
   - Every control survives, and the head proof and runner hashes are EXACT after every set.
5. **Q32 (sequencing only) is an accepted residual.**
   - Without the wait, the rival and the holder race for the lock. If the rival wins, the holder is refused and cannot complete, so the check FAILS. It never proves falsely.
   - The only extra protection the wait gives: it rules out a third-party lock holder that the proof would otherwise mistake for the holder. A stand-in cannot stage that without a timer: the holder would have to wait for an event the head proof never produces.
   - The kill rate here (11 of 14 runs) comes only from the honest case's race.
6. **The fixed 3 s hold on the honest path is an accepted residual.**
   - The collision holder waits for its rival's `.status` file, then holds 3 s to cover the proof's next few shell steps (`ended` at `act_slot_proof.sh:333`).
   - No event marks the end of those steps, because the next write the proof makes (`record`) comes after `wait "$holder"`.
   - It can only fail the honest case under stall, never pass a broken one.
   - Measured: 6 of 6 serial self-tests PASS (44 cases), and 16 of 16 with 8 self-tests running at once.
7. **The case list against the doc.** The 44 cases are 1 honest, 7 bad starts and 36 broken cases (6 completion, 3 interrupt, 8 parallel, 12 isolation, 7 collision). They map one to one onto the doc's list at `CI_WORKFLOWS.md:1959-1984`. The count and the timing paragraph (`:1986-1996`) match the stand-in, apart from the omission in S1. The runner pin at `:2042-2047` matches the new arm.

## Lens results (all five applied at 022290e4)

[R267] PASS Conformance - #532 acceptance 1-6 and the DECISION as amended, against `receipts/diff-scope-604297bb-022290e4.txt` and `scripts/act_ci.py:4455-4494`, `:12203-12216`. The round changes no runner behaviour, live proof check or workflow, and weakens no refusal (acceptance 6). The acceptance-5 self-tests grow: the runner has 425 arms, one added and none lost (`receipts/act-ci-selftest-label-diff-604297bb-022290e4.txt`); the proof has 44 cases. Acceptance 1 still waits on the manager's live proof (see pending duties). The round-3 assignment's bar, "fail deterministically with no reliance on timing" for the four named guard groups, is met (`receipts/one-sided-probe-*`).

[R267] PASS RTL - no `hdl/`, `tb/`, `syn/`, constraint or processor path in `759da623..022290e4`. For the runner's architecture and interfaces: its live code is byte-identical to `604297bb` apart from the self-test row (diff-scope receipt). The proof's line contract with the runner is unchanged (`act_slot_proof.sh:171`, `:218`, `:224`, `:239-240`): the live section's hash is identical, and the stand-in prints exactly the lines those greps read.

[R267] PASS Robustness - checked `act_slot_proof.sh:378-391` (`await_judgment` and `await_path`, bounded at 1200 x 0.05 s), the SIGKILL arm at `:424-425`, the refusal arms at `:446-453` and the fault routing at `:500-548`, all under the mutants above. Every stand-in wait is bounded, so a mutant that never writes the awaited file ends rather than hangs; the one hang, `R266 lock-blocking`, is in the runner arm and was bounded at 240 s. The new cap fixture pins the realistic single OOM with no local kill.

[R267] PASS Tests - `act_slot_proof.sh:366-654` under my round-3 sets Q00-Q62 and S00-S10, the published A213, A220, R266-2, R266-3 and R267-2 sets, the one-sided, forced-order and skew probes, and the stress runs (receipts listed below); `act_ci.py:12188-12260` with 425 arms in both modes. Every named mutant is KILLED on every run, every control survives, and the survivors match the documented rulings. S1 is a suggestion only.

[R267] PASS Docs - `CI_WORKFLOWS.md:1832-1844` (cap count), `:1954-2005` (proof self-test cases, timing, unstaged guard), `:2042-2047` (runner pin), checked against the code and the case table. Also `docs_check` (0 findings), `check_em_dash --base 759da623` (0 findings over 359 added lines), `gen_toc --check` and `--verify-anchors`, `check_doc_paths` and `check_doc_style`, all rc 0 (`receipts/focused-gates-022290e4.log`). S1 is a suggestion only.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #532 acceptance 1-6 and the DECISION as amended; diff-scope receipt; `act_ci.py:4455-4494`, `:12203-12216`; runner self-test label diff | R267-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| RTL | CLEAN | no HDL path in the lane diff; runner live code identical to 604297bb; proof/runner line contract `act_slot_proof.sh:171,218,224,239-240`; live section hash | R267-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| Robustness | CLEAN | stand-in waits, faults and SIGKILL arm `act_slot_proof.sh:378-548`; cap fixture `act_ci.py:12206-12210`; bounded hang mutant | R267-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| Tests | CLEAN | proof self-test `:366-654` under Q00-Q62 (4 full runs plus focus repeats), one-sided, order and skew probes, published sets A213, A220, R266-2, R266-3, R267-2; runner arms `act_ci.py:12188-12260` under S00-S10 and A213/A220 (57); 425 arms and 44 cases in both modes | R267-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |
| Docs | CLEAN | `CI_WORKFLOWS.md:1709-2053` against the code and the case table; focused doc gates | R267-4 | 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 |

## Other evidence

- **Runner self-test** (`receipts/act-ci-selftest-022290e4-{user,root}.log`): 425 ok and 0 FAIL in both modes. Against `604297bb`: one label added (the new cap arm), none lost.
- **Proof self-test** (`receipts/proof-selftest-022290e4-*.log`): PASS with 44 cases, 3 runs per mode; 16 of 16 PASS with 8 running at once.
- **Focused gates** in the sandbox on a disposable clone with pinned submodules, all rc 0:
  - `bash -n`;
  - `git diff --check` from `759da623` and from `604297bb`;
  - `check_py_idiom` and `check_sh_idiom`;
  - `docs_check`, `check_em_dash`, `gen_toc --check` and `--verify-anchors`, `check_doc_paths`, `check_doc_style`;
  - `check_baremetal_only --check` (0 findings over 847 files) and `--selftest` (441 arms).
- **Hosted, exact head** (`receipts/hosted-check-runs-022290e4.tsv`), for information only; the manager owns hosted and act acceptance:
  - 21 executed contexts completed `success`, including `rtl-fast`, `docs-check`, `elaborate`, `verilator-suites` and `yosys-portability`.
  - `Physical gPTP (nightly and manual)` was **skipped**. It is not evidence of anything.
  - The hosted `docs-check` ran `act_ci.py --selftest` with 425 ok, including the new arm.

## Real limits

- Nothing ran live: no Docker, act, sudo, slot daemon, firewall, namespace or cgroup. The runner's live slot behaviour and the proof's ten checks are graded only against stand-ins. The live proof is **NOT RUN**.
- Physical calibration is **NOT RUN**, and the hosted physical context was skipped. Neither is hardware proof.
- The manager's full-source static, builder and native banks for this head are separate. I have not seen them and I claim nothing about them. No parent, protocol-processor, gPTP, Yosys or builder bank was run here.
- This is source validation at the lane head. The current-dev candidate merge result is not validated here: base `ede8d48e`, live dev `3d2f3e31`.
- The kill tallies for Q32 and Q23 are statistical over the runs recorded, as described above.
- The survivors B03/Q08 (non-root writability) and I02/Q56/M9 (the ten-`PASS` backstop) stay unstaged, as documented.

## Pending manager duties

- Run `act_slot_proof.sh --selftest` and then the audited live proof with an `rtl-full` pair, for acceptance 1 and the live halves of 2 and 3. The run logs record each slot's peak and cap-hit count.
- Accept the hosted and act evidence at the exact head; the full-source banks; candidate-merge validation against live dev; post-merge containment.
- Publish this packet: `REPORT.md` and the files in `MANIFEST.sha256`.

## Packet

- **`bin/`:** the portable scripts.
  - My round-3 tools, unchanged: `sandbox.sh`, `clone_integrity.sh`, `proof_mutants_r267_3.py`, `slot_mutants_r267_3.py`, `proof_one_case.py`, `overlap_order_probe.sh` and `replay_published_proof_mutants.py`.
  - `replay_published_slot_mutants.py`, with `--range` and `--mutant-timeout` added.
  - New this round: `one_sided_probe.sh`, `unannounced_skew_probe.sh`, `split_published_mutants.py` and `focused_gates.sh`.
- **`receipts/`:** the raw results cited above.
- **Published mutant lists** were used verbatim from evidence commits, by blob:
  - `ead93cd7`: `correction-a213/bin/slot-mutants.py` 6dd1f0e8, `correction-a220/bin/slot-mutants-a220.py` 09d96f2e, `correction-a213/bin/proof-mutants.py` 706131dd, `correction-a220/bin/proof-mutants-a220.py` 9807175e, `reviews/R266-2/scripts/proof_mutants_r266_2.py` 1e0a0d10, `reviews/R267-2/scripts/proof_mutants.py` b7046d7f;
  - `d2352cdd`: `reviews/R266-3/scripts/proof_mutants.py` (sha256 1de4955a, split into two verbatim halves; `receipts/r266-3-proof-mutants-split.txt`).
- The first unsplit attempt at the published slot replay exceeded the command bound and printed nothing. It was re-run in ranges, and those range receipts are the ones listed.

R267-4 FINISHED
