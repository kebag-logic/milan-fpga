[R877] POSITIVE - exact head 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb

# Round R877-4: internal cleared-context review of PR #959 (issue #948), narrow re-check of the manager's README commit

Head `8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb`, tree `f00413b5354577dded4c76c4098b01bd6c8002bd`, one commit on `64117b77cb9e5c421717835b5be032b5905c447d`.
Whole-PR context is `15168e14..8aeb2f0b`.

## Verdict summary

- I applied all five lenses to the delta. All five are CLEAN.
- There is no open BLOCKER, MAJOR or MINOR.
- There are two new wording-only RESIDUE items (RS1, RS2). One prior RESIDUE (R878-3-R1) is retained. One prior SUGGESTION (R877-2-S1) is retained as optional.
- The delta is one line. `git diff --name-only 64117b77 8aeb2f0b` lists only `sw/firmware/ctrl/README.md`, and its line 255 changes from `185 pin controls` to `192 pin controls`.
  - The commit message is one line with no trailers, as CONTRIBUTING requires (receipts/delta.txt).
- **192 is the self-test's own count** at this head and on the merge with dev-soft-core `aa30d77f`. I derived it from `ctrl_pin.pin_controls`' own arm construction:
  - 186 arms plus 6 lifecycle cases.
  - The base `15168e14` gives 185, which is 179 plus 6.
  - The +7 are exactly seven stack-reaching targets that this PR adds to `tb/verilator/milan_dp/Makefile`.
- `ctrl_boundary`'s figure check and its four figure controls pass at head and on the merge. The page's other three figures (103, 8, 5) equal the self-test's population and do not depend on the pin count. A negative control that puts 185 back on the merge is refused by name.
- The docs gates pass at head and on the merge. `docs_inventory.py --check` is fresh at both.
- No source comment is in the delta, so the comment rule has nothing new to judge.

## Findings

No BLOCKER, MAJOR or MINOR.

### RS1 - RESIDUE - Docs - commit `8aeb2f0b` message and `review-evidence/948-r1/manager-r4/NOTE.md` - "stack-building plants" names seven targets of which three are not plants

- **Authority/evidence:** at base the pin-control arm list has 179 entries, and at head 186 (receipts/count_pin_controls_base_15168e14.txt, receipts/count_pin_controls_head.txt). The seven added arms are the poisoned-`wire.h` arms of these `tb/verilator/milan_dp/Makefile` targets:
  - `twin8-fw` (`:1115`), `build-twin8-sp` (`:1118`) and `twin-fanout` (`:1124`). These are the twin's eight-input fan-out leg, not plants.
  - `twin-fanout-plants` (`:1128`), `fan-stop-plants` (`:1152`), `fan-stop-plant-shared` and `fan-stop-plant-one-index`. These are the plants.
  - The commit message says "this change's stack-building plants". NOTE.md says "#959 adds stack-building plants (... fan_stop_plant.py, twin_fanout_plant.py and their recipes)".
- **Impact:** wording only. The figure, the count, the gate verdict and the code are unchanged and correct.
- **Exact fix:** do not amend the commit, because that would move the head. In any PR or issue text that summarises the change, write: "the seven stack-reaching targets this change adds to `tb/verilator/milan_dp/Makefile`: the twin fan-out leg (`twin8-fw`, `build-twin8-sp`, `twin-fanout`) and its plants (`twin-fanout-plants`, `fan-stop-plants`, `fan-stop-plant-shared`, `fan-stop-plant-one-index`)".
- **Verification:** compare the text against the arm diff in the two count receipts.

### RS2 - RESIDUE - Docs - PR #959 body, lines 16 and 127 - the body still names `64117b77` as the head

- **Authority/evidence:** the PR head is `8aeb2f0b` (`gh pr view 959 --json headRefOid`).
  - The body says "Correction-round source and route gates PASS at `64117b77...`" and gives `git checkout 64117b77...`.
  - The body does not mention the manager's README commit or the `manager-r4` packet.
  - A reader who checks out `64117b77` gets the stale 185 figure, which the hosted `ctrl_boundary` refuses.
- **Impact:** stale prose for a cold reader. No measurement, figure or verdict changes, and the statement about `64117b77`'s gates stays true for that commit.
- **Exact fix:**
  - After the line-16 sentence, add: "Manager commit `8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb` then corrects `sw/firmware/ctrl/README.md:255` to 192 pin controls, the self-test's count with this change's seven stack-reaching Makefile targets (evidence: `review-evidence/948-r1/manager-r4`)."
  - Change the checkout line to `git checkout 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb`.
- **Verification:** read the body against `headRefOid`.

### Retained from prior rounds

- **R878-3-R1 - RESIDUE - Docs - PR #959 body line 18:** this line still says the correction "is committed locally on `pf-948-1` for the manager to push". RETAINED with the exact fix R878-3 gave. It can be combined with RS2.
- **R877-2-S1 - SUGGESTION - RTL, Robustness - `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv`:** the suggestion is to make a late enqueue pulse fail safe. RETAINED and optional. The delta does not touch the file.

## Prior public findings, resolved or retained at this head

I read these only after my own pass over the delta. Every artifact the prior findings name is byte-identical between `64117b77` and `8aeb2f0b`: `git diff --quiet 64117b77 8aeb2f0b -- hdl docs/testing/TESTING.md tb` exits 0. So each disposition that R878-3 published at `64117b77` stands at this head. I spot-checked the two MINORs from my own role's prior round at their cause.

| Finding | Severity / lenses | Disposition at `8aeb2f0b` |
|---|---|---|
| R877-2-F1 | MINOR / RTL, Robustness, Tests, Docs | RESOLVED (R878-3 at `64117b77`; artifacts untouched since). Spot-check: `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:363-364` declares both pending tallies `[DEPKT_PEND_W_C-1:0]`, and `:492-493` raises the urgent drain on either tally's top bit. |
| R877-2-F2 | MINOR / Docs | RESOLVED. Spot-check: `docs/testing/TESTING.md:706` names 81, 66, 99, 60, 93, 70 and 63 octets. |
| R877-2-RS1..RS5 | RESIDUE | RESOLVED per R878-3; artifacts untouched. |
| R878-2-R1 | RESIDUE / Docs | RESOLVED per R878-3. |
| R878-1-F1, R878-1-F2, R877-1-F1, R877-1-R1, R877-1-S1 | as published | Remain RESOLVED or IMPLEMENTED; artifacts untouched. |
| R878-3-R1 | RESIDUE / Docs | RETAINED (PR body line 18), see above. |
| R877-2-S1 | SUGGESTION / RTL, Robustness | RETAINED, optional. |

A note on cause, recorded for the ledger and not as a finding against this head:
- The seven targets arrived in `e8a877a0` (the twin fan-out leg) and `ce61b2a2` (the STOP plants). From then until `64117b77`, the README carried the base's 185.
- None of the five prior public verdicts on this PR mentions `ctrl_boundary`. No receipt in `review-evidence/948-r1/MANIFEST.json` other than `manager-r4`'s is named for it. NOTE.md says the merge candidate's native bank does not run it.
- The hosted firmware-verilator job caught it. This round covers the gap with the count probe and the figure check described below.

## Lens results

[R877] PASS Conformance - `sw/firmware/ctrl/README.md:255` against `sw/firmware/ctrl/test/ctrl_boundary.py:155-164,412-428` (FIGURES, population, figures); issue #948 body gates line 6 - the README's figure is a repository-gate claim about the self-test's population, and the self-test reads it as such. The delta touches no IEEE 1722/1722.1/Milan behaviour, no wire field and no acceptance-criterion evidence. Issue #948's gates list (failing test first, RTL suites and twin, service budget, fit and timing) is unchanged by a figure line. The count it must equal is 192 at head and on the merge (receipts/count_pin_controls_head.txt, receipts/count_pin_controls_merge_aa30d77f.txt).

[R877] PASS RTL - `git diff --name-only 64117b77 8aeb2f0b` (receipts/delta.txt): one Markdown file. `git diff --quiet 64117b77 8aeb2f0b -- hdl tb` exits 0 - no RTL, testbench or Makefile byte changed. The prior RTL verdict (R878-3 at `64117b77`) stands for untouched code, and nothing it depends on moved.

[R877] PASS Robustness - receipts/figures_negative_185_on_merge.txt, receipts/figures_head.txt, receipts/count_pin_controls_*.txt. The figure check refuses the old 185 by name: "gives the pin controls as 185, where the self-test has 192". All four one-more figure controls are refused by name at head and on the merge, with 0 misbehaved. I tried the count once with the merge clone missing its non-stack submodules. The `milan_dp` dry run then yields no targets and the count falls silently to 119. A stated figure of 192 is exactly what makes such a silent shrink fail the gate, so the corrected line strengthens the check. That observation is about pre-existing `ctrl_pin.stack_targets` behaviour (`sw/firmware/ctrl/test/ctrl_pin.py:653-674`), which this delta does not touch.

[R877] PASS Tests - `scripts/count_pin_controls.py` (this packet) over `sw/firmware/ctrl/test/ctrl_pin.py:881-978` and `ctrl_pin_lifecycle.py:94-110`; `scripts/check_figures.py` over `ctrl_boundary.py:412-443`.
- **Count probe:** it rebuilds `pin_controls` from its own source with only the arm-execution loop cut, so the arm list is the self-test's own list. It also builds the six lifecycle cases. Results:
  - base `15168e14`: 179+6=185;
  - head: 186+6=192;
  - merge `aa30d77f`+head (disposable `3b6c87f0`, tree `0e5c07bd`, clean auto-merge, all gitlinks equal to head's): 186+6=192.
  - The arm diff from base to head is exactly the seven targets in RS1.
- **Independent cross-check:** the hosted excerpt in the manager's packet, from the merge ref over `aa30d77f`, prints "192 pin and 4 figure controls, 0 misbehaved".
- **Figure check:** run on the real page with population(192), it gives 0 findings at head and on the merge. The delta changes no test, and no test was weakened.

[R877] PASS Docs - `sw/firmware/ctrl/README.md:185,255`; `git grep` for the figure across the tree (only `:255` states it); gates at head: `docs_check.py` 0 findings across 223 md + 1916 text files, scrub 23/23, routing 4/4; `check_doc_style.py` OK; `check_em_dash.py --base 64117b77` 0 findings over 1 added line, arms 339/339; `--base 15168e14` 0 findings over 75 added lines; `check_doc_paths.py` OK, 1755 paths; `gen_toc.py --check` OK and `--verify-anchors` 755 links reproduced, both with the pinned renderer lock in a disposable venv; `docs_inventory.py --check` fresh, 541 lines. On the merge: `docs_inventory --check` fresh, 538 lines; `docs_check` 0 findings; `gen_toc --check` OK; `check_doc_paths` OK.
- The other three figures on the page (103 defects, 8 passing controls, 5 Verilator defects) equal `population()` and do not change with the pin count.
- The section's own sentence at `:185` ("refuses this section where one of these figures, or the pin controls' below, is not its own count") stays true.
- The PR and commit wording residue is RS1, RS2 and R878-3-R1, all wording only.

## Evidence verified

- **Packet:** `review-evidence/948-r1/manager-r4` at `eea845db`. The three files' sha256 values equal `MANIFEST.json`'s `published_sha256` (receipts/packet_verification.txt).
  - The diff body of `manager-commit.patch` is byte-identical to `git show --format= 8aeb2f0b`.
  - The evidence commit `eea845db` carries no cryptographic signature (GitHub reports `unsigned`). Integrity rests on the manifest hashes.
- **Hosted excerpt:** it shows the failing `[FAIL] ... as 185, where the self-test has 192` from firmware-verilator, run 45191675681 attempt 2, on the merge ref over `aa30d77f`. That matches my derivation.

## Exact-head hosted status, inspected only (the manager owns hosted acceptance)

receipts/hosted_check_runs_8aeb2f0b.tsv holds 69 check runs on `8aeb2f0b`, all completed at the time I read them.
- `elaborate-gates-1` failed because the runner could not fetch a build tool: `[error] [launcher] could not retrieve sbt 1.10.0` (receipts/hosted_elaborate-gates-1_excerpt.txt). That is infrastructure, not this delta.
- Fail-fast then cancelled the rest, **including `firmware-verilator`, the job that runs `ctrl_boundary --require-rv32 --selftest --only verilator`**.
- The aggregators `docs-check` and `Union milan_dp` fail because their needs were cancelled; their logs assert on `"result": "cancelled"`. I read only those two logs. `verilator-suites`, `yosys-portability`, `elaborate`, the other `Union *` jobs and one `Collect CI manifest` also report failure after the cancellation, and I did not read their logs.
- Executed and green: `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `split-cdc`, `bdd-conformance`, `full-ci-gate`, `changes`. `Physical gPTP` was skipped.
- So the hosted run that NOTE.md names as "the verifying run" has not completed at this head.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sw/firmware/ctrl/README.md:255` against `ctrl_boundary.py:155-164,412-428`; issue #948 gates; count receipts at head and merge | R877-4 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |
| RTL | CLEAN | delta name-only and `git diff --quiet 64117b77 8aeb2f0b -- hdl tb`; prior RTL coverage R878-3 at the ancestor `64117b77`, untouched in scope since | R877-4 (delta); R878-3 (untouched RTL) | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb (delta); 64117b77cb9e5c421717835b5be032b5905c447d (RTL, unchanged ancestor) |
| Robustness | CLEAN | negative control 185 on the merge; four one-more figure controls at head and merge; the submodule-less count shrink observed | R877-4 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |
| Tests | CLEAN | `count_pin_controls.py` over `ctrl_pin.py:881-978`, `ctrl_pin_lifecycle.py:94-110` at base, head and merge; `check_figures.py` over `ctrl_boundary.py:412-443`; hosted excerpt cross-check | R877-4 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |
| Docs | CLEAN (RS1, RS2, R878-3-R1 are RESIDUE) | README `:185,:255`; tree-wide figure grep; docs_check, doc style, em-dash (two bases), doc paths, gen_toc check and anchors, docs_inventory check at head; four of them on the merge; PR body; commit message; NOTE.md | R877-4 | 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb |

## Real limits

- I did not run the full `ctrl_boundary.py --require-rv32 --selftest` (RV32 toolchain, Verilator builds and the execution of all 192 pin arms). The count of 192 is proven by building the self-test's own arm list from its own source, and it matches the hosted merge-ref excerpt. Whether each of the 192 arms behaves (0 misbehaved) is shown only by that hosted excerpt over `aa30d77f`, not by a run at this exact head.
- I ran no manager source bank, builder bank, Verilator suite, Yosys run or act replica. No manager source bank runs at this head, and I claim none.
- The merge I probed is with dev-soft-core `aa30d77f`, the PR's base. Live `dev` `e275d7950ef3385753e6a15d2e191ba855b171ed` and `aa30d77f` have diverged (neither is an ancestor of the other). Live `dev`'s README states `171 pin controls`, so a merge onto `dev` will need the figure re-derived on that candidate.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The evidence commit `eea845db` is unsigned. Packet integrity was checked against its manifest only.
- The review clone is restored to exact head bytes after the probes:
  - HEAD, tree and index-tree all `f00413b5`.
  - Porcelain status is empty, and the probe caches are removed.
  - All five initialised submodules are at their gitlinks and clean; `external` is uninitialised, as it was before the round.
  - Evidence: receipts/clone_integrity_after.txt.

## Pending manager duties

1. Re-run the exact-head hosted rtl-fast/firmware-verilator `ctrl_boundary` on `8aeb2f0b`. The current attempt was cancelled by fail-fast after an infrastructure failure in `elaborate-gates-1` (sbt fetch). Then obtain green exact-head `verilator-suites` and `yosys-portability`.
2. Add `ctrl_boundary --selftest`, or at least its figure check, to the merge-candidate validation, as NOTE.md already acknowledges.
3. At the merge turn, re-derive the README's pin-control figure on the actual candidate. Live `dev` states 171 and dev-soft-core states 185, against 192 with this PR.
4. Carry RS1, RS2 and R878-3-R1 to the residue checklist.

R877-4 FINISHED
