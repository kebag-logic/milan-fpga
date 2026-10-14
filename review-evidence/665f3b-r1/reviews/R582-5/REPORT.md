[R582] POSITIVE - exact head 7032bca5a51d8d97fcb73d7fc106ca4af21de38e

# R582-5: internal independent review of PR #736 (issue #665, F3b round 5)

- Exact head: `7032bca5a51d8d97fcb73d7fc106ca4af21de38e`, tree `f1c1f47cb4fefb8a6c68418d03dc762f72cbee15`. GitHub `headRefOid` equals it, base `dev`, not draft.
- Scope: a delta review of `6b4feeca..7032bca5`. This is one `--no-ff` merge of dev `fa7347fc` into the lane parent `6b4feeca`. Earlier rounds stand for everything else (R582-4 and R583-4 are POSITIVE at `6b4feeca`).
- Authorities read: AGENTS.md, CONTRIBUTING.md and docs/README.md. Issue #665 round 5 assignment (comment 6158656140, items 1 to 3). The PR body. The author's REVIEW READY (issue comment 6158812839). The published round 5 evidence at `ea046666`, `review-evidence/665f3b-r1/author-r5/`. I did not read the packet's `reviews/` directory.
- Verdict: POSITIVE. There is no BLOCKER, MAJOR or MINOR finding. Three new wording-only items and one carried item are RESIDUE.

## 1. What the merge is

| Claim | Result | Receipt |
|---|---|---|
| Parents are (`6b4feeca`, `fa7347fc`), in that order. The merge is `--no-ff` with no rebase. | Met | `receipts/01_merge_identity.txt` |
| Tree equals `git merge-tree --write-tree 6b4feeca fa7347fc` | Met: both are `f1c1f47c` | `receipts/01_merge_identity.txt`, `receipts/09_merge_provenance_script.txt` |
| The tree equals that of manager candidate `c585f506` | Not verified independently. `c585f506` is not in this clone. I accept the manager's statement. | none |
| `git diff fa7347fc 7032bca5` is exactly the lane's paths (`d40e4e98..6b4feeca`) | Met: 46 identical paths | `receipts/07_path_provenance.txt` |
| No conflict was resolved by hand | Met. 25 of the 28 changed paths carry dev's blob exactly. The three paths both sides changed (`scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md`, `sw/firmware/ctrl/maap/README.md`) carry each side's hunk set byte-identically. | `receipts/07_path_provenance.txt`, `receipts/27_three_way_hunk_identity.txt` |
| Gitlinks are the lane's (tsn-c-stack `70936b77`). The other four are unchanged on both sides. | Met. Dev still pins `405dc683`; the head keeps the lane's `70936b77`. | `receipts/08_all_gitlinks.txt` |
| No stale `405dc683` reference enters with dev's files | Met: zero hits outside `third_party/`. The MAAP README link names `70936b77` (`sw/firmware/ctrl/maap/README.md:19`). | `receipts/24_stack_pin_references.txt` |
| Dev changes no firmware image input | Met. Dev's only `sw/` paths are the MAAP README, `maap_differential.py` and `test_maap_differential.cpp`. None is an image source. | `receipts/28_dev_firmware_inputs.txt` |

What the merge brings in, relative to the lane parent: the lane was based on `d40e4e98` (the #697 branch tip), not on dev `a0f39ad4`. So `6b4feeca..7032bca5` carries #696 (`ebac072b`) and #734 (`fa7347fc`). Through #705's merge `0136de16`, it also carries #725 (`6c810c45`) and #730 (`a0f39ad4`). That includes `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and most of the `scripts/act_ci.py` growth. All of those paths carry dev's bytes unmodified (`receipts/07_path_provenance.txt`, `receipts/03_delta_stat_lane_to_head.txt`). I judged them as dev content merged without alteration; I did not re-review them. See R582-5-R2 for the PR-body wording.

## 2. Focused execution at the exact head

| Check | Result | Receipt |
|---|---|---|
| `python3 scripts/ci_scope.py --selftest` | rc 0, 202 `ok` arms, 0 FAIL. Includes the #734 scope-history arms, run from `scripts/ci_scope.py:529,532`. | `receipts/10_ci_scope_selftest.log` |
| `python3 scripts/ci_scope.py docs/design/MAILBOX_SPLIT.md` | `true` (relevant) | `receipts/11_ci_scope_mailbox_split.log` |
| `MAILBOX_SPLIT.md` in `GATE_READ_DOCS` after #734 | Present once, at `scripts/ci_scope.py:72`. Its classification case is at `:293`. All 8 registered pages are named in `CI_WORKFLOWS.md:179-202`. | `receipts/20_gate_read_registration.txt` |
| Registration mutants in a disposable archive (remove the entry; flip the case to `False`) | Both caught. Each gives selftest rc 1 with the named MAILBOX_SPLIT failures. The baseline copy passes, and restoring the file classifies `true`. | `receipts/23_scope_mutation_probe.txt`, `receipts/26_scope_registration_mutants_script.txt`, `scripts/scope_registration_mutants.sh` |
| `ci_events.py --check` / `--selftest` | rc 0: 2174 contract items; 3096 arms | `receipts/12_ci_events_check.log`, `receipts/13_ci_events_selftest.log` |
| `docs_check.py`, `check_doc_style.py`, `check_submodule_docs.py`, `check_rtl_source_lists.py` (+`--selftest`), `gen_mailbox.py --check --crosscheck --selftest` | All rc 0 | `receipts/14_*` to `receipts/19_*` |
| MAAP differential `--self-test`. This is where #696's KL_maap and test change meet the lane's adapter and pin. | Stack at `70936b77`. Baseline 12 tests, 0 failures; differential mutants 17/17 caught, including #696's `parent-ignores-mac`. | `receipts/30_maap_differential_selftest.log` |
| KL_maap harness (`tb/verilator/maap`, `make run`) | 186 checks, 0 failures | `receipts/31_maap_rtl_harness.log` |
| KL_maap integration (real CSR-to-MAAP datapath path, #696 M4) | 5 checks, 0 failures | `receipts/32_maap_integration.log` |
| KL_maap mutation campaign (`mutants.py`) | 65 checks, 0 failures | `receipts/33_maap_rtl_mutants.log` |
| Review clone after the probes | Clean. No untracked or ignored files. Index tree is `f1c1f47c`. All five initialized submodule HEADs equal their gitlinks and are clean. | `receipts/40_clone_integrity_after_probes.txt` |

The tools were the pinned Verilator 5.050 (rev v5.050), local Python 3.14.7 and GCC 16.2.1 (`receipts/00_tool_identity.txt`). The MAAP RTL suite ran in an archive of the head under scratch. Its first attempt failed only because the archived processor submodule had no Git index, which `pp_srcs.py` needs. I indexed the scratch copy, checked that its file list equals the pin's 562 files, and reran.

Hosted, read at 2026-10-14T01:55:53Z (`receipts/21_hosted_check_runs.txt`):

- Hosted jobs ran on test-merge `dbd88172`, whose tree is `f1c1f47c` (`receipts/22_hosted_changes_scope.txt`).
- `changes` used #734's new PR classification. Its changed-file list is exactly the lane's 46 paths, and it reports RTL/tooling relevant `true`.
- These completed with success: `rtl-fast`, `changes`, `firmware-unit`, `firmware-boundary`, `firmware-verilator`, `firmware-control-mutants`, `firmware-aecp-mutants`, `firmware-srp-mutants`, `publication-census`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`, and Yosys shards 0/4 to 3/4.
- Still in progress: Verilator shards 0/5 to 4/5, `docs-check` and `elaborate`.
- `Physical gPTP` was skipped. Skipped is not executed.

No act receipt was published when I read it. Hosted and act acceptance are the manager's.

## 3. Findings

### R582-5-R1 - RESIDUE - Docs - PR #736 body line 224 (also `author-r5/REVIEW-READY-ROUND5.md` and issue comment 6158812839)

- Evidence: line 224 says "Nothing else changes: every path keeps one side's bytes". The REVIEW READY says "Each path keeps one side's bytes". Three paths carry neither side's blob. They hold both sides' hunks (`receipts/07_path_provenance.txt`). The next bullet and `round5/integrity.py`'s docstring ("unless both sides changed it") state this correctly.
- Impact: none on any tree, test, figure or verdict. The sentence contradicts the bullet after it.
- Required wording: "Nothing else changes: every path changed on only one side keeps that side's bytes; the three paths below carry both sides' hunks unchanged, the gitlinks keep the lane's, and the diff against dev is the lane's 46 paths."
- Verification: read the body.

### R582-5-R2 - RESIDUE - Docs - PR #736 body line 221

- Evidence: "Merge: dev `fa7347fc` (#696 `ebac072b` and #734) into `6b4feeca`". The lane parent's base is `d40e4e98`, so the merge also brings #725 and #730 through #705's merge `0136de16` (`receipts/01_merge_identity.txt`, `receipts/03_delta_stat_lane_to_head.txt`). The tree and every check are unaffected.
- Required wording: "Merge: dev `fa7347fc` into `6b4feeca`. Relative to the lane's base `d40e4e98` it brings #725 and #730 (through #705's merge), #696 `ebac072b` and #734; every such path carries dev's bytes."
- Verification: read the body.

### R582-5-R3 - RESIDUE - Docs - PR #736 body line 29

- Evidence: "`7032bca5…` is the head to publish on PR #736". The head is published: `headRefOid` = `7032bca5…`. This repeats the R582-3-R1 class.
- Required wording: "`7032bca5a51d8d97fcb73d7fc106ca4af21de38e` is the published head of PR #736."
- Verification: read the body.

### R582-4-R1 (retained) - RESIDUE - Docs - PR #736 body line 34

- Evidence: "Round 5 local checks pass; exact-head hosted acceptance follows the manager's push." The push has happened and hosted runs exist at this head.
- Required wording: "Round 5 local checks pass; exact-head hosted acceptance is the manager's."
- Verification: read the body.

No BLOCKER, MAJOR, MINOR or SUGGESTION finding at this head.

## 4. Prior public findings at this head

I read these after my own pass over the diff.

| Finding | Status at `7032bca5` | Evidence |
|---|---|---|
| R583-1-F1 (core source-validity predicate), R582-1-F1 (scratch Git maintenance), R583-1-F2 (service-bound recomputation) | Still resolved. Their artifacts are lane-side paths with lane bytes, and hosted firmware jobs pass on tree `f1c1f47c`. | `receipts/07_path_provenance.txt`, `receipts/21_hosted_check_runs.txt` |
| R582-2-F1 / R583-2-F1 (MAILBOX_SPLIT gate-read registration) | Still resolved through #734's rewrite. The entry is at `scripts/ci_scope.py:72` and the case at `:293`. Both mutants are caught. | `receipts/20_*`, `receipts/26_*`, `receipts/27_*` |
| R582-3-F1 / R583-3-F1 (stale page count) | Still resolved. `CI_WORKFLOWS.md:179` reads "These pages" with no count, and all 8 pages are named. | `receipts/20_gate_read_registration.txt` |
| R582-3-R1 / R583-3-R1 (published-head sentence) | The R582-3-R1 class has regressed in the round 5 body. It is recorded as R582-5-R3 (RESIDUE). | `receipts/29_pr736_body.md:29` |
| R582-4-R1 (RESIDUE, "follows the manager's push") | Retained as RESIDUE | `receipts/29_pr736_body.md:34` |
| R583-3-S1 | Moot, as before | none |
| R582-1-S2, R582-1-S3, R582-2-S1 test options (SUGGESTION) | Remain optional. The merge touches none of their artifacts. | `receipts/07_path_provenance.txt` |

## 5. Lens results

- `[R582] PASS Conformance` - Artifacts examined: issue #665 comment 6158656140 items 1 to 3 against `receipts/01_*`, `09_*`, `10_*`, `11_*`, `12_*` and `29_pr736_body.md:219-249`. The merge commit, the tree equality, the scope self-test, the events check and the MAILBOX_SPLIT registration are all met, and the body states the tree. Lane protocol bytes are unchanged (`07_*`). #696's Annex B KL_maap behaviour, composed with the lane's pin `70936b77`, passes the MAAP differential (`30_*`: 12/0, 17/17). Item 2's `act_ci.py --selftest` was not run by this reviewer, because that is outside my allowed actions. `act_ci.py` carries dev's bytes exactly, and the author's receipt reports PASS.
- `[R582] PASS RTL` - Artifacts examined: `hdl/milan/milan_datapath.sv:7184-7185` and `hdl/ieee1722/maap/KL_maap.sv`, which carry dev's bytes. The lane's only HDL change is a comment above `hdl/milan/mailbox/KL_mbx_pkg.sv:304`. The KL_maap harness (186/0), integration (5/0) and mutants (65/0) pass on the pinned simulator. Hosted `verilator-lint`, `yosys-elaboration` and Yosys shards 0 to 3 succeeded on tree `f1c1f47c`.
- `[R582] PASS Robustness` - Artifacts examined: the three merged files. Each side's hunks are intact (`27_*`), and no stale pin enters (`24_*`). #734's new PR classification at this head: hosted `changes` classified exactly the 46 lane paths as RTL relevant, so nothing is misfiled as documentation only (`22_*`). Registration-removal and case-flip mutants are refused (`26_*`).
- `[R582] PASS Tests` - Artifacts examined: `scripts/ci_scope.py:526-533`, where the merged selftest runs both the gate-read arms and `ci_scope_history.selftest`. Selftest is 202/0, and both planted registration defects fail it. The MAAP differential mutants are 17/17 and the RTL mutants 65/65. Hosted firmware unit, boundary, Verilator and the three mutant jobs succeeded on tree `f1c1f47c`.
- `[R582] PASS Docs` - Artifacts examined: `docs/testing/CI_WORKFLOWS.md:179-202` (8 pages, no count) against `scripts/ci_scope.py:69-78`. Also `sw/firmware/ctrl/maap/README.md:19,109-160,217-223` and `docs/design/MAAP_FABRIC.md:308-313`, which are consistent with the split predicate. `docs_check`, `check_doc_style` and `ci_events --check` all pass, and so do `check_submodule_docs` and `gen_mailbox --check`. Three new PR-body items and one carried item are RESIDUE, which leaves the lens clean.

## 6. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round 5 items 1 to 3; merge identity, provenance and gitlinks; MAAP differential at pin `70936b77` | R582-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| RTL | CLEAN | `milan_datapath.sv:7184-7185`, `KL_maap.sv` (dev bytes), `KL_mbx_pkg.sv:304` (comment); KL_maap harness, integration and mutants; hosted lint and Yosys | R582-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| Robustness | CLEAN | Three-way hunk identity; hosted `changes` scope; registration mutants; stale-pin scan | R582-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| Tests | CLEAN | `ci_scope.py` selftest (202) with mutants; MAAP differential (17/17) and RTL mutants (65/65); hosted firmware jobs | R582-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| Docs | CLEAN (RESIDUE R582-5-R1, R2, R3 and R582-4-R1 carried) | `CI_WORKFLOWS.md:179-202`, MAAP README, `MAAP_FABRIC.md:308-313`, doc gates, PR body | R582-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |

For everything outside this merge delta, coverage stands from R582-4 / R583-4 at `6b4feeca`. Every lane path at this head keeps `6b4feeca`'s bytes, apart from the dev hunks added to the three merged files, which this round covered.

## 7. Real limits

- I did not run `scripts/act_ci.py --selftest` (outside my allowed actions). I rely on the author's receipt, and the runner carries dev's bytes.
- I did not verify the tree equality with candidate `c585f506` (the object is not local). The builder and native bank results for that candidate are the manager's claims.
- At read time, hosted Verilator shards 0/5 to 4/5, `docs-check` and `elaborate` were still in progress. No act receipt was published.
- I did not rerun the full firmware campaigns locally. No firmware input changed (`28_*`), and the hosted firmware jobs succeeded on tree `f1c1f47c`.
- Local Python was 3.14.7, not the documented CPython 3.12.3.
- I judged #725, #730, #696 and #734 content only as unmodified dev bytes. I did not re-review it.
- My one read-only `git fetch` of evidence commit `ea046666` added objects to the clone's object store. Tracked state is unchanged.
- Physical calibration was NOT RUN. Skipped field and hardware contexts are not hardware proof.

## 8. Pending manager duties

- Exact-head hosted acceptance, once the Verilator shards, `docs-check` and `elaborate` finish, and the act replica at this head.
- Candidate-merge validation against live dev (builder and native banks) at the merge turn, with receipts linked on the PR.
- The external review (R583-5) and the full completion bar.
- Explicit maintainer merge authorization, and post-merge containment.
- Carry R582-5-R1, R582-5-R2, R582-5-R3 and R582-4-R1 to the residue checklist.

R582-5 FINISHED
