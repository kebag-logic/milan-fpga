[R632] POSITIVE - exact head ac0142539856222b84ef8e5af414d12132a5bebf

# R632-9: composition review of the #730 merge-train candidate (PR #731)

Role: internal (cleared-context) composition reviewer for issue #730 / PR #731.
Candidate `ac0142539856222b84ef8e5af414d12132a5bebf`, tree
`f0cf7c248d645e4a305ba5bad7d38f6679298bc9`. The first parent is `ada26e56`, the
queued train: dev `49da9fd9` (PR #721 and PR #728), then #726 (candidate
`cdb49e7e`) and B16 (candidate `ada26e56`). The second parent is the PR source
head `b341e875`, whose base is `dc4d06cb`.

This round covers composition acceptance only. The source head has two
independent POSITIVE source reviews (section 6). The question here is whether
the composed tree introduces any defect beyond the reviewed sources.

**Verdict.** The composed tree introduces no defect beyond the reviewed
sources. This round raises no new finding. One earlier RESIDUE, in the PR body
only, is still present and is retained (section 7). It does not affect the
verdict or any lens.

Reading order followed: AGENTS.md and CONTRIBUTING.md (sections 3 and 7, the
candidate-merge rule), docs/README.md, issue #730 (its acceptance, the lane
assignment, the no-replay ruling 6131815815 and the round decisions), the
PR diff and history, then this round's own gates and probes. Prior review
findings were read only after the verdict and ledger below were written.

## 1. What the composition is

Receipt: `receipts/composition/facts.txt`, produced by `composition_facts.sh`.

- `git merge-tree --write-tree ada26e56 b341e875` gives `f0cf7c24`, the
  candidate tree exactly. So the candidate is the automatic merge, with no
  hand edit. The merge base of the two parents is `dc4d06cb`, the PR's base.
- PR #731 changes two files: `scripts/act_ci.py` and
  `docs/testing/CI_WORKFLOWS.md`.
- The train delta `dc4d06cb..ada26e56` changes 54 files. Only one of them is
  also changed by this PR: `docs/testing/CI_WORKFLOWS.md`. In the train it is
  changed by #721 (#640 M8a) and #728 (#727) only. Neither #726 nor B16
  touches it.
- In the candidate, `scripts/act_ci.py` is byte-identical to the PR head (blob
  `15257b8a`). No commit in the train touches it.
- No file under `.github/` changes anywhere in `dc4d06cb..ac014253`. The four
  workflow blobs the runner replays (`rtl.yml`, `docs.yml`, `elaborate.yml`,
  `rtl-fast.yml`) are the same at the base, the train parent, the PR head and
  the candidate. No workflow sets `max-parallel`.
- The candidate's `CI_WORKFLOWS.md` (blob `7e36e7cb`) equals the blob from
  merging the PR head into live dev `49da9fd9` alone. #726 and B16 therefore
  add nothing to this file.

## 2. The shared file: docs/testing/CI_WORKFLOWS.md

Receipts: `receipts/composition/pr_side_changed_lines.txt`,
`candidate_vs_train_parent_changed_lines.txt`, `pred_side_changed_lines.txt`
and `candidate_vs_pr_head_changed_lines.txt`.

- **Both sides are applied verbatim.**
  - The changed lines of `ada26e56..candidate` match those of
    `dc4d06cb..b341e875` byte for byte (175 lines).
  - The changed lines of `b341e875..candidate` match those of
    `dc4d06cb..ada26e56` byte for byte (74 lines).
  - Nothing is dropped, duplicated or interleaved.
- **The two sides edit separate parts of the file.** Line numbers are in the
  candidate.
  - The train's hunks are at lines 120, 138-141, 230-262, 374-377 and
    1282-1294. They cover the gate-read pages, the measured-time Verilator
    split and its 60 % gate, the `milan_dp_gm_steps` owner sentence, and the
    RV32 SDK member of `elaborate`.
  - The PR's hunks are at lines 1588-1592, 1761-1763, 1779-1881, 1885-1928,
    2214-2224 and 2434. They cover the interrupt probe, the act replica's CPU
    shape and monitor, the signal mask and precedence, the self-test list, the
    slot resource bounds and the slot self-test pins.
- **No heading changes.** Neither side adds, removes or renames a heading.
  These pages link into this file, and all their links still resolve on the
  candidate: `docs/testing/TESTING.md`, `docs/testing/RUNNING_TESTS.md`,
  `tb/verilator/milan_dp/README.md`, `tb/verilator/milan_dp_gptp/README.md`
  and `docs/README.md`.
- **Each side's text is still correct in the merged file, and neither side
  makes the other false.**
  - This PR describes:
    - per-container CPU ranges: each slot owns `20N..20N+19`; slot 0 stages
      on `0-3` and uses `4-19`;
    - how long a reservation lasts: until `destroy`, or until an inspect shows
      the container is gone;
    - the derivation from `max-parallel` and `CONCURRENT_JOB_LIMIT`: shipping
      `rtl-full` derives 4, the other three workflows derive 1;
    - the `CLEANUP_SIGNALS` mask and its act window;
    - which failure wins when several occur, and the exact diagnostics.
  - #727 describes:
    - suites placed onto five workers by measured hosted time;
    - the 60 % `timeout-minutes` gate, read from `rtl.yml`;
    - the refresh and new-suite procedure;
    - the reworded `milan_dp_gm_steps` owner sentence.
  - #640 M8a describes the seventh gate-read page (`SPLIT_CONTROL_MEMORY.md`)
    and the split SoC member of `elaborate`.
- **Where the two sides' subjects meet**, checked by reading:
  - **Worker and container counts.** The act text says "five Verilator
    workers, four Yosys workers" and "at most four containers at once"
    (lines 1776-1778). Both still hold. #727 keeps five workers: `rtl.yml`
    still has `shard: [0, 1, 2, 3, 4]` and `total: [5]` in an unchanged blob,
    and no `max-parallel` was added. So `rtl-full` still derives 4 concurrent
    containers, as the PR says.
  - **Timing figures.** #727's figures and 60 % gate are claims about hosted
    runs only. The PR makes no claim about a worker's wall clock in a replay;
    it says the effect is "not measured yet (#730)" (line 1880). No figure is
    contradicted.
  - **The page count.** #640's "Seven pages under `docs/`" (line 120) still
    holds. `act_ci.py` names no documentation page, and
    `ci_scope.py --selftest`, which derives that list, passes on the
    candidate.
  - **Old slot wording.** The pre-#730 `4N` to `4N+3` slot wording appears
    only in the PR's own sentence about mixed runner versions (line 2223).

## 3. Gates run on the candidate

Script `run_composition_gates.sh` (with `MD_PYTHON` set to an interpreter that
has the pinned renderer). Receipts are in `receipts/gates/`: `*.log`, `*.rc`
and `SUMMARY.txt`. All 26 gates return rc 0. The interpreter is CPython 3.14.7
with PyYAML 6.0.3. The renderer gates used `cmarkgfm==2025.10.22` and
`html5lib==1.1` (`receipts/gates/md_venv_freeze.txt`). Without those two
packages, the em-dash and TOC gates refuse to give a verdict. They do not
fail falsely.

| Gate | Result |
|---|---|
| `docs_check.py` | 0 findings across 206 Markdown files |
| `check_doc_style.py` / `--selftest` | OK, 22 documents / rc 0 |
| `gen_toc.py --check` / `--verify-anchors` / `--selftest` | 146 pages OK / 486 cross-page fragment links reproduced / rc 0 |
| `check_em_dash.py --base ada26e56` (candidate parent) | 0 findings over 167 added lines, 1 page |
| `check_em_dash.py --base dc4d06cb` (PR base) | 0 findings over 3222 added lines, 22 pages |
| `check_em_dash.py --base 49da9fd9` (live dev) | 0 findings over 2855 added lines, 14 pages |
| `check_em_dash.py --selftest` | rc 0 |
| `check_doc_paths.py` | all 974 cited paths resolve |
| `docs/DOC_MAP.gen.py --check`, `check_archive.py` | OK |
| `ci_events.py --check` / `--selftest` | 2016 contract items across 4 workflows and `CI_WORKFLOWS.md` / 2828 arms, PASS |
| `ci_scope.py --selftest` | PASS |
| `check_py_idiom.py` / `--selftest` | ratchets 0 <= 0 / 54 PASS |
| `check_baremetal_only.py --check` / `--selftest` | 0 findings / rc 0 |
| `measure_test_evidence.py --check`, `check_hygiene.py --check`, `measure_fail_fast.py --check` | PASS |
| `suite_shards.py --selftest` (#727's selector; reads `rtl.yml`) | PASS |
| `git diff --check ada26e56 HEAD`, and `git diff --check dc4d06cb HEAD` on the PR's two files | clean |

**Probes.** Script `probe_doc_gates.sh`; receipts in `receipts/probes/`. After
each probe, the file was restored to its committed bytes (blob `7e36e7cb`,
re-hashed afterwards).

- **P1.** An em dash committed into a line this PR added, in a disposable
  shared clone. `check_em_dash.py --base ada26e56` KILLED it (rc 1, names line
  1784). A first attempt planted the em dash in the working tree only, and it
  survived. That is expected, because the gate reads committed history. The
  probe was rerun as a commit.
- **P2.** The `## Exhaustive validation` heading renamed.
  `gen_toc.py --verify-anchors` KILLED it (rc 1; four inbound links reported
  as MISS).
- **P3** (informational). The slot-bounds bullet put back to the pre-#730
  wording. `ci_events.py --check` SURVIVED, as expected: no gate reads that
  text, so section 2 judged its composition by reading.

### act_ci.py --selftest on the composed tree

This round did not run the runner or its self-test on any host. Its outcome on
the candidate rests on two facts:

- **The candidate carries the same runner and the same inputs as the PR
  head.**
  - The runner is byte-identical to the PR head.
  - Its self-test reads only two things: its own source, and the four replayed
    workflow files under `.github/workflows/`. The readers are `WORKFLOWS`,
    `load_workflow`, `validate_workflow_sandbox`,
    `replay_container_concurrency`, and the dry-run arm that copies
    `shipping_root / WORKFLOWS[...]`.
  - None of the 54 files the train changes is one of those inputs. The only
    name that matches is `README.md`, inside a comment.
- **A hosted run passed the self-test on the same runner and inputs.**
  - Run 38348813316, job `docs-check` (115136282389), checked out `6dd63a34`,
    which is "Merge b341e875 into 49da9fd9".
  - Its "Local act runner contract gate" step ran
    `python3 scripts/act_ci.py --selftest` and printed `selftest: PASS` with
    531 `ok` lines
    (`receipts/composition/hosted_docs_check_act_selftest_excerpt.txt`).
  - That merge's `act_ci.py`, `CI_WORKFLOWS.md` and workflow blobs equal the
    candidate's.
  - The rest of the candidate (#726, B16) touches no input to the self-test.

## 4. Findings of this round

None. No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is new in this round.

## 5. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #730 acceptance 1-3, checked against the composed tree. Acceptance 3 (no workflow, step or job change): `.github/` is unchanged in `dc4d06cb..ac014253`. Acceptance 1-2: `rtl.yml` has `shard: [0..4]` and no `max-parallel`, so the train changes neither the derived `rtl-full` concurrency of 4 nor the four ranges per slot. `scripts/act_ci.py` blob `15257b8a` equals the PR head. The composition reaches this lens only through the workflow inputs, which are unchanged. Conformance of the source itself is covered by the source reviews (section 6). | R632-9; source: R632-7, R633-7 | `ac0142539856222b84ef8e5af414d12132a5bebf` |
| RTL | CLEAN | The composition does not touch this lens. PR #731 changes no RTL, testbench or tool flow. The train's RTL files (`hdl/ieee1722/...`) and the PR's two files have no file in common, and they share no registry, source list or interface. The source is covered by R632-7 and R633-7. | R632-9 (inapplicable here); source: R632-7, R633-7 | `ac0142539856222b84ef8e5af414d12132a5bebf` |
| Robustness | CLEAN | The composition changes no failure, refusal, signal or cleanup path. `scripts/act_ci.py` is byte-identical to the PR head, and every file it reads (`.github/workflows/{docs,elaborate,rtl-fast,rtl}.yml`) is byte-identical at the base, the train parent, the PR head and the candidate. The source is covered by R632-7 and R633-7. | R632-9 (inapplicable here); source: R632-7, R633-7 | `ac0142539856222b84ef8e5af414d12132a5bebf` |
| Tests | CLEAN | The gate inventories in the composed tree, all rc 0 (`receipts/gates/`): `ci_events.py --check/--selftest` (2016 items, including `CI_WORKFLOWS.md`); `ci_scope.py --selftest`; `check_py_idiom.py` (the train widened its exec inventory); `measure_test_evidence.py --check` (the train added a reader disposition); `suite_shards.py --selftest`. The `act_ci.py --selftest` result rests on blob and input identity plus hosted docs-check run 38348813316 on `6dd63a34` (PASS, 531 arms). Probes P1 and P2 were KILLED. | R632-9 | `ac0142539856222b84ef8e5af414d12132a5bebf` |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md`, blob `7e36e7cb`. Both sides are applied verbatim (changed-line receipts), their hunks are disjoint, and no heading changes. The merged text was read at the PR's sections (1588-1592, 1759-1928, 2212-2232, 2434) and the train's (117-141, 227-262, 371-377, 1279-1294). The docs gates in section 3 all return rc 0, with the em-dash gate run at three bases. The retained RESIDUE R632-7-R1 is in the PR body, not in this file (section 7). | R632-9 | `ac0142539856222b84ef8e5af414d12132a5bebf` |

## 6. Source reviews this round relies on

These are the two POSITIVE reviews of the PR source head `b341e875`. Each
covered all five lenses CLEAN at that head:

- R632-7, internal:
  https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6138928763
- R633-7, external:
  https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6138762918

The composed `scripts/act_ci.py` and its inputs are byte-identical to that
head, so their RTL, Robustness and source-level Conformance coverage carries
to the candidate unchanged. R632-8 (POSITIVE at `d8f01088`) reviewed an
earlier train candidate that included 697c. It is superseded by this round,
and this round does not rely on it.

## 7. Prior public findings on PR #731, at this head

These were read after sections 1-5 were written.

| Finding(s) | Severity, lenses | Status here | Evidence |
|---|---|---|---|
| R633-1-F1..F4, R633-2-F1, R633-4-F1, R633-5-F1 | MAJOR or MINOR, all five lenses | RESOLVED, stays resolved | Resolved at the source head per R632-7 and R633-7. The candidate's `scripts/act_ci.py` is the same blob (`15257b8a`), so the fixes and the arms that check them are unchanged. |
| R632-1-F1, R632-1-F2, R632-2-F1, R632-3-F1, R632-6-F1 | MINOR, Tests (R632-1-F1 also Docs) | RESOLVED, stays resolved | Same blob identity. The hosted self-test on `6dd63a34` passed all 531 arms, including R632-6-F1's six named arms. |
| R632-1-R1, R632-1-R2, R632-5-R1, R632-5-R2 | RESIDUE, Docs | APPLIED, still present in the candidate | The mixed-runner-version sentence is at `CI_WORKFLOWS.md:2222-2224`. The exact beside-signal diagnostic and the "Throughout" paragraph are at `:1859-1878`. The PR body states the refusal on every slot. |
| R632-6-R1, R633-6-R1 | RESIDUE, Docs | SUPERSEDED by R632-7-R1 | The Round 6 wording was corrected. The same staleness recurred for Round 7. |
| **R632-7-R1 = R633-7-R1** | RESIDUE, Docs | **RETAINED** | The live PR #731 body (read during this round; `gh pr view 731 --json body`), Status section, lines 18-20, still says: "local Round 7 head `b341e875…`. The two Round 6 commits are pushed; the PR head is `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`. The new Round 7 commit is local and unpushed." GitHub reports `headRefOid` `b341e875d87c6aa2be355bad17f373782517f723`. **Exact fix (unchanged from R632-7-R1):** replace "The two Round 6 commits are pushed; the PR head is `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`. The new Round 7 commit is local and unpushed." with "The Round 7 commit is pushed; the PR head is `b341e875d87c6aa2be355bad17f373782517f723`." The wording "local Round 7 head" on line 18 should also become "Round 7 head". This is wording only. It changes no measurement, figure, verdict, test, code, generated artifact, or conformance or clause claim, so it leaves Docs CLEAN and the verdict POSITIVE. **Verification:** compare the Status section with `headRefOid`. |
| R632-7-S1..S3, R632-6-S1..S3, and their earlier aliases (R632-2-S3 … R632-5-S4; R632-3-S1 … R632-5-S3; R632-5-S1) | SUGGESTION, Tests or Robustness | RETAINED, optional | The code they name is byte-identical in the candidate. The document lines R632-7-S1 cites (`CI_WORKFLOWS.md:1784-1785` and `:2185-2186` at the source head) are unchanged text, now at `:1817-1818` and `:2219-2220`. |
| R632-1-S1..S4, R632-2-S1, R632-2-S2 / R632-3-S2 / R632-4-S2, R632-5-S2 | SUGGESTION | ADDRESSED at source, unchanged here | Per R632-7 and R633-7. The code is the same blob. |

## 8. Limits

- This round did not run the runner's self-test on any host. Its result on the
  candidate rests on the identity argument and the hosted run in section 3.
- No act replay was run, and no Docker, Verilator, Yosys, builder or native
  bank. When this round looked, hosted Verilator shards 0/5, 2/5 and 3/5 at the
  PR head were still running. This round makes no claim about them.
- No manager source bank exists at this head, and none is claimed. Physical
  calibration was NOT RUN. Field skips are not hardware proof.
- The hosted runs are of `b341e875` merged into `49da9fd9`, not of the
  candidate commit, which is unpublished.
- The pinned-renderer gates used an existing interpreter that already had the
  pinned packages. Nothing was installed.
- After the probes, the clone is back at the exact head
  (`receipts/restore.txt`):
  - worktree = index = HEAD, with no untracked files;
  - the `git ls-files -s` digest equals the `HEAD` tree's (modes and blobs);
  - the gitlinks `gptp-processor` `7dda9c3b`, `protocol-processor` `2ad2f845`
    and `third_party/verilog-axis` `48ff7a7e` are checked out at their
    recorded commits;
  - `external` and `third_party/lwSRP` are uninitialized, as they were at the
    start.

## 9. Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the
  merge turn, and link its receipts on the PR.
- Hosted and act acceptance of the exact merge head, including the Verilator
  shards still pending.
- Carry RESIDUE R632-7-R1 / R633-7-R1 (the exact PR-body fix in section 7) to
  the residue checklist.
- #730 acceptance 4 and the optional acceptance 5: the measured replay after
  the merge, under the no-replay ruling. The PR says "Relates to #730", so the
  merge does not close the issue. Close it by hand once acceptance 4 is
  recorded.

R632-9 FINISHED
