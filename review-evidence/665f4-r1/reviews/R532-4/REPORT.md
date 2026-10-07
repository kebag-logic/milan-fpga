[R532] POSITIVE - exact head 6f7deea15a9160761b30aaa93fe152f20d416695

# R532-4: internal cleared-context review of PR #690 (issue #665, lane F4), round 4

- **Head:** `6f7deea15a9160761b30aaa93fe152f20d416695`, tree `485029d20cffa5d1970a608553b169d547838779`, one commit on `c1049de1970e93d2c36ace62891ee9d947cd3191`. lwSRP gitlink is still `23d9a8173b07503a0ee6e8528f922fceab4e67f0`.
- **Delta (`c1049de1..6f7deea1`):** three files, +112/-1.
  - `sw/firmware/ctrl/test/srp_mbx.cpp:819-919`: three new cases.
  - `sw/firmware/ctrl/test/srp_mutants.py:487-495`: three new plants.
  - `sw/firmware/ctrl/srp/README.md:65-66`: the rule now states the Domain-VID exception.
- **Production code:** none changed. `git diff --raw c1049de1..HEAD` lists only those three blobs. No gitlink moved, and no path outside `sw/firmware/ctrl/test/` or a README changed (`receipts/integrity.txt`, `receipts/delta_r4.diff`).
- **Reading order:**
  1. AGENTS.md, CONTRIBUTING.md sections 3 and 6, docs/README.md.
  2. The #665 body; F4 assignment 6030279477; acceptance additions 6009661573 and 6030870481; rounds 6033558691, 6035166787 and 6036454509; rulings 6034653240 and 6036016117; REVIEW READY 6036793241; manager receipt 6036186046.
  3. `srp_mbx.c` (the guards under test) and `srp/README.md`.
  4. The diff and history.
  5. The public author packet `review-evidence/665f4-r1/author-r4/` at evidence commit `76fa75c9`; the PR #690 body; exact-head hosted check runs.
- **Independence:** I fixed the verdict and ledger draft before opening any prior review text (`receipts/draft_verdict_before_prior_findings.txt`, written 13:44:52 local time). I did not read the concurrent other-reviewer round-4 report.

## Findings

No new BLOCKER, MAJOR or MINOR. Retained items from earlier rounds (see the disposition table):

### R532-2-R2 RESIDUE: Docs. Stale publication wording in the PR #690 body (retained)

- **Artifact:** PR #690 body.
  - "How to get into the same state" still opens with `After the integration role publishes this head:`.
  - Status ends with `This round makes no push or PR edit.`, which is the executor's handoff voice on a published head.
- **Authority/evidence:** ruling 6036016117 and the published head `6f7deea1`, whose review start is PR comment 6036805068.
- **Impact:** wording only. It changes no measurement, figure, verdict, test, code, generated artifact, conformance or clause claim, and touches no privacy rule.
- **Exact fix:**
  - Replace `After the integration role publishes this head:` with `To inspect the published head:`.
  - Replace `This round makes no push or PR edit.` with `The executor made no push or PR edit; the integration role published this head.`
- **Verification:** reread the PR body.

### R532-1-S2 SUGGESTION: Conformance, RTL. Generic LV/rJoin extra indication in lwSRP (retained)

- **Status:** a dependency matter for lwSRP PR #12, not re-examined this round.
- **Effect on lenses:** it does not leave a lens unclean.

### Observations (not findings)

- **One plant hangs under a whole-suite run.** Lane plant `reset-leaks-owned-participants` makes a whole-suite `srp_mbx.cpp` run hang until the runner's 600 s timeout. Its named-test run, which is how the lane campaign grades it, catches it (`receipts/runs/plantnamed_L-reset-leaks-owned-participants_2.log`). A hang still grades as FAIL (`NOCOUNT`), so no plant escapes.
- **Cited receipts are missing from the public packet.** The author handoff cites `ROUND4-GATES.json`, `ROUND4-TESTS.md`, `ROUND4-DEVELOPMENT.json` and `round4-receipts/`. The public `author-r4/` folder holds only `HANDOFF.md` and `PR-BODY.md`. I reproduced every claim that bears on this round independently (below), so no verdict rests on the missing files. Publishing or de-referencing them is a manager duty, not a defect at the head.

## Prior public findings: disposition at this head

These were read after the verdict draft. Sources: R532-3 (6036450620), which carries the R532-1/2 and R533-1/2 dispositions, and R533-3 (6036369877).

| Prior finding | Disposition at `6f7deea1` | Evidence |
|---|---|---|
| R532-3-F1 MINOR (Tests): round-3 shared-Applicant inheritance not discriminated | **RESOLVED** | See "R532-3-F1" below. |
| R532-3-F2 MINOR (Tests, Docs): Domain-VID guard untested, README omits it | **RESOLVED** | See "R532-3-F2" below. |
| R532-3-R1 RESIDUE (PR body Status stale) | **RESOLVED** | The Status section now carries the exact fix text: "Round 3 was REVIEW READY under ruling 6036016117. The compiler-absent docs entry passed in the manager's run (PR comment 6036186046)...". |
| R532-2-R2 RESIDUE (publication wording), as restated by R533-3 | **RETAINED as RESIDUE** | See above. |
| R532-1-S2 SUGGESTION | **RETAINED as SUGGESTION** | See above. |
| R532-2-F1..F4, R533-2-F1/F2, R532-1/R533-1 findings | **Remain RESOLVED** | R532-3 resolved these at `c1049de1`. Their artifacts (`srp_mbx.c`, lifecycle tests, docs inventory) are byte-identical at this head. Their lane plants are caught in my rerun of all 70 (`receipts/campaign_verdicts.txt`). |

### R532-3-F1: the binding-replacement tests now discriminate shared-Applicant inheritance

The production code under test is `srp_mbx.c:313-325`. Each new test has a lane plant that matches my round-3 plant of the same defect.

**`JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves` (`srp_mbx.cpp:819`)**

- What it does: an ineligible binding joins an already-Ready StreamID from the other slot. The eligible binding then leaves before any service pass.
- What it requires: an Lv for the StreamID, and that no record for it is anything but Lv.
- Coverage: both slot orders, at IF=1 and IF=2.
- Its plant is `joining-binding-loses-applicant` (`srp_mutants.py:487`), which matches my round-3 RP3.

**`ReboundStreamCannotInheritAnotherStreamsReady` (`srp_mbx.cpp:851`)**

- What it does: a StreamID whose Talker is still registered is rebound next to a different StreamID that is already Ready.
- What it requires: a fresh Ready for the rebound StreamID.
- Its plant is `applicant-inherited-across-streams` (`:490`), which matches my round-3 RP10.

**My results**

- Each lane plant is caught by name at IF=1 and IF=2.
- In a whole-suite run, each plant fails only its own new test. So without these tests the defect would have escaped, as round 3 found.
- My four additional plants are each caught by name at IF=1 and IF=2:
  - `R-same-dest-only`: inherit only from a binding with the same destination.
  - `R-inherit-by-vid`: inheritance keyed on VID instead of StreamID.
  - `R-lower-slot-only`: inherit only from lower-numbered slots.
  - `R-higher-slot-only`: inherit only from higher-numbered slots.
- The two slot-order plants fail on opposite orders. The test trace shows `i/1` for lower-only and `i/0` for higher-only. So each slot order discriminates independently.
- Receipts: `receipts/probe_summary.txt` and `receipts/runs/plant_*.log`.

### R532-3-F2: the final-unbind Domain-VID guard is tested and stated

**`FinalDomainVidUnbindKeepsSrClassMembership` (`srp_mbx.cpp:886`)**

- What it does: binds and then finally unbinds one sink on the current Domain VID. It covers startup VID 2 and peer-selected VID 7, both slots, at IF=1 and IF=2.
- What it requires:
  - an Lv for the Listener;
  - no MVRP Lv for the Domain VID;
  - at least one renewed MVRP record for it.

**Plants**

- The lane plant `final-unbind-withdraws-domain-vid` (`srp_mutants.py:493`) matches my round-3 RP5. It is caught by name at IF=1 and IF=2 (including the IF=2 case the round asked for), and in a whole-suite run only this test fails.
- My `R-guard-startup-vid` plant hard-codes VID 2 in the guard. It is caught, and only the peer-selected VID 7 iteration can catch it, so that case is load-bearing.
- My `R-guard-next-domain` plant judges against the pending Domain instead of the committed one. It is also caught.

**README**

- `srp/README.md:65-66` now reads "The final binding preserves the current Domain VID. Otherwise, it releases its VID regardless of prior eligibility."
- This matches `srp_mbx.c:334`, `if (old.vid != i->domain.vid && !has_sink(i,&old,false))`.
- It is also consistent with README:87-90: startup declares VID 2 membership, a changed VID is reserved first, and a bound sink retains an old VID.

## Reviewer evidence at the exact head (host model, pinned lwSRP `23d9a817` clone, clean)

| Command / probe | Result | Receipt |
|---|---|---|
| `srp_mbx.cpp`, release, IF=1 / IF=2 | 53 / 53 pass (the 50 from round 3 plus 3 new) | `runs/baseline_srp_mbx.cpp_1.log`, `runs/base-srp_mbx-if2.log` |
| `srp_mbx.cpp` debug arm, IF=1/2; `srp_latency.cpp` IF=1/2; `srp_walk.cpp` IF=1/2 | 3/3, 4/4, 5/5 pass at each count | `runs/baseline_*.log` |
| Built suite, `--gtest_shuffle --gtest_repeat=10 --gtest_random_seed=532`, IF=1 and IF=2 | 10/10 iterations × 53 pass at each count: no order dependence | `runs/shuffle-if{1,2}.log` |
| All 70 lane SRP plants, graded exactly as `srp_mutants.campaign` (IF=2, named test, `caught()`), in parallel | **70/70 caught** | `campaign_verdicts.txt`, `campaign/*.log` |
| The three new lane plants plus 6 reviewer plants, whole-suite runs at IF=1 and IF=2 | 18/18 caught by name | `probe_summary.txt` |
| 54 other lane `srp_mbx.cpp` plants, whole-suite runs at IF=2 | 53 caught by name; 1 hangs whole-suite but is caught by name (observation above) | `probe_summary.txt` |
| `fw_coverage.py --check --lwsrp <pin> --jobs 16` | rc 0; 15 files at 100 % after the existing exclusions; `srp_mbx.c` 441/441 lines and 410/410 branches; ratchet file unchanged | `runs/fw_coverage_check.log` |
| `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c1049de1` and `--base db9aa8c9` (pinned renderer lock in a private venv), `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `measure_test_evidence.py --check`, `check_todo_ownership.py` | all rc 0; em-dash 0 findings over 2 added lines (round 4) and 567 added lines (PR) | `docs_gates_summary.txt`, `runs/gate_*.log` |
| Final clone integrity | 0 untracked/ignored entries after removing my own byte-code caches; index (mode, blob, path) equals the HEAD tree (sha256 `9edb6a2d...`); 1169 tracked files hash to their index blobs; no hidden index flags; gitlinks are stage 0 and equal the pins | `integrity.txt` |

Receipt paths are relative to `receipts/`. Scripts are in `scripts/`: `probe.py`, `lane_campaign.py` and `docs_gates.sh`.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c:170-172,313-337` against README:56-66,87-90 and the assignment's "MVRP for the SR class VID" (6030279477 B.4). New test 3 asserts Domain-VLAN retention; tests 1 and 2 assert Lv for a lost last eligible request and a fresh Ready for a rebound StreamID. Production bytes are unchanged since R532-3 covered Conformance at `c1049de1` | R532-4 (production scope also R532-3 at `c1049de1970e93d2c36ace62891ee9d947cd3191`, an untouched ancestor) | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| RTL | CLEAN | `git diff --raw c1049de1..HEAD`: no hdl/tb/syn/sw/mailbox or firmware production change, and no gitlink move. The binding/inheritance contract `srp_mbx.c:283-340` was read against the new tests. Mailbox contract evidence is retained from R532-3 | R532-4 (contract artifacts: R532-3 at `c1049de1970e93d2c36ace62891ee9d947cd3191`, untouched since) | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| Robustness | CLEAN | New cases cover both slot orders, IF=1/2, startup and peer-selected VID, and join-then-leave before service. Shuffled ×10 at IF=1/2 pass. Slot-order and VID-boundary plants (`R-lower/higher-slot-only`, `R-guard-startup-vid`, `R-guard-next-domain`) are caught. Lifecycle robustness is retained from R532-3 on unchanged code | R532-4 (lifecycle scope also R532-3 at `c1049de1970e93d2c36ace62891ee9d947cd3191`) | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| Tests | CLEAN | `srp_mbx.cpp:819-919`, `srp_mutants.py:487-495`. All 70 lane plants were rerun (70/70). 6 reviewer plants and 3 new lane plants were caught whole-suite at IF=1/2. Coverage ratchet rc 0. R532-3-F1 and F2 are resolved | R532-4 | `6f7deea15a9160761b30aaa93fe152f20d416695` |
| Docs | CLEAN | `srp/README.md:53-66` (README:65-66 matches `srp_mbx.c:334`); PR #690 body Status and Round 4 sections; author-r4 HANDOFF/PR-BODY; 14 docs and quality gates rc 0. R532-2-R2 is RESIDUE only | R532-4 | `6f7deea15a9160761b30aaa93fe152f20d416695` |

```text
[R532] PASS Conformance - srp_mbx.c:334 / srp/README.md:65-66 / srp_mbx.cpp:886 - final unbind keeps the current Domain VID (startup VID 2 and peer VID 7) and withdraws others; matches startup SR-class membership (README:87, assignment B.4)
[R532] PASS RTL - git diff --raw c1049de1..6f7deea1 (3 blobs, no production or gitlink change); srp_mbx.c:283-340 - binding contract unchanged and consistent with the new tests
[R532] PASS Robustness - srp_mbx.cpp:819/851/886, receipts/runs/shuffle-if{1,2}.log - both slot orders, both interface counts, VID boundary, order-independent ×10
[R532] PASS Tests - srp_mutants.py:487-495, receipts/campaign_verdicts.txt (70/70), receipts/probe_summary.txt - each new plant fails only its named test; reviewer plants caught
[R532] PASS Docs - srp/README.md:65-66 against srp_mbx.c:334; receipts/docs_gates_summary.txt - rule stated, gates rc 0; PR body residue only
```

## Real limits

- **Not run, by assignment:**
  - the full parent, processor, gPTP, Yosys and builder banks;
  - `test_ctrl_firmware.py --require-rv32 --self-test`, whose 100 control plants and RV32 arms I did not replay;
  - the saved-state gate;
  - `make -C tb/verilator/mbx`. I did not invoke the pinned Verilator, so its identity was not needed;
  - Docker/act, host `act_ci`, and hardware.

  None of their inputs changed in this delta. R532-3 covered the mailbox suite and RV32 host gate at `c1049de1`.
- **Physical evidence:** physical calibration is NOT RUN, and field skips are not hardware proof.
- **Host model only:** all behaviour was judged on the host mailbox model.
- **Hosted contexts at `6f7deea1`** (read-only, refreshed at the time in `receipts/hosted_checks_fetched_at.txt`; `receipts/hosted_checks_6f7deea1.tsv`):
  - Executed and passed: `changes`, `full-ci-gate`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, Yosys shards 0-3 and Verilator shards 0 and 3.
  - Executed and failed: `firmware-unit` fails at its submodule fetch because the private lwSRP clone is refused ("could not read Username", `receipts/hosted_failed_excerpt.txt`). `rtl-fast` fails as the aggregate of that job.
  - Still in progress: `elaborate` and Verilator shards 1, 2 and 4.
  - Skipped (not executed): `Physical gPTP (nightly and manual)`.
- **Source versus candidate:** this verdict is on source. The current-dev candidate is built by the manager at the merge turn, from source base `db9aa8c9b135b34ff3d070a979dee70440b37cc6` and live dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.

## Pending manager duties

- **Residue checklist:** carry R532-2-R2. Carry R532-1-S2 to lwSRP PR #12.
- **Missing receipts:** publish the round-4 receipts the author handoff cites, or remove the references: `ROUND4-GATES.json`, `ROUND4-TESTS.md`, `ROUND4-DEVELOPMENT.json` and `round4-receipts/`.
- **Hosted CI:** make lwSRP fetchable so `firmware-unit` and `rtl-fast` can pass. Record the final `elaborate` and Verilator shard 1, 2 and 4 results for this head.
- **lwSRP pin:** merge lwSRP PR #12 and the `f4-applicant-notes` follow-up, then move the pin in a later delta.
- **Merge bar:**
  - run the candidate builder bank, including `test_baremetal_profile_contract`, and the compiler-absent check at this head or the candidate;
  - run the full candidate gates on current dev;
  - run post-merge containment.

  Merge still needs a second independent positive at this head and explicit maintainer authorisation.

R532-4 FINISHED
