[R636] NEGATIVE - exact head 43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e

# R636-2: internal cleared-context delta review of PR #745 for #744

- Head `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e`, tree `9c0a8e43b66f420cd9a581460a81f62184bb05dc`, branch `744-slot-oom` -> `dev`.
- Delta reviewed: `f643377f1..43a25fa7e`, four commits (`1cb7f19bd`, `597c43f92`, `dcd4d98ae`, `43a25fa7e`). Six files: `scripts/check_baremetal_only.py`, `scripts/ci_runtime_workflows.py`, `.github/workflows/rtl-fast.yml`, `scripts/ci_gate_workflows_selftest.py`, `scripts/act_ci.py`, `docs/testing/CI_WORKFLOWS.md`.
- Result: one MINOR (R636-2-F1, Docs), one RESIDUE (R636-2-F2) and two SUGGESTIONs (R636-2-F3, R636-2-F4).
- Every prior finding is resolved at this head: M1 = R636-1 BLOCKER = R637-1-F2, R637-1-F1, R636-2, R636-3 and R636-4. See "Prior findings, resolved or retained".
- The open MINOR leaves Docs unclean, so the verdict is NEGATIVE. The other four lenses are clean.
- The new `scripts/act_ci.py` SHA-256 is `b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8` (698735 bytes, mode 755, blob `dc3ebeeb4970`), as the author reported. It is ready for the manager's re-pin (`receipts/act_ci-sha256.txt`).

## Inputs, in reading order

1. `AGENTS.md` and `CONTRIBUTING.md` (lenses, severities, completion bar), and `docs/README.md` for the authority map.
2. #744: the body; the assignment and clarification comments; TAKEN; REVIEW READY at `f643377f`; the round-2 assignment (issuecomment 6199231775); REVIEW READY round 2 (6200488334).
3. PR #745: the body at this head, manager finding M1 (6199082046) and the round start (6200534438).
4. Authorities:
   - the #259 bare-metal boundary in `scripts/check_baremetal_only.py` and in `docs/testing/CI_WORKFLOWS.md:2341-2366`;
   - the census bound and OOM accounting sections of `docs/testing/CI_WORKFLOWS.md`.
5. `git diff f643377f1..43a25fa7e` and the four commit messages.
6. The author's round-2 packet at evidence commit `67e05179f28b`, `review-evidence/744-r1/author-r2/`.
   - All 41 files match the published SHA-256 in `MANIFEST.json` (`receipts/author-r2-evidence-sha256.txt`).
   - GitHub reports the evidence commit as unsigned. Its integrity rests on the manifest hashes, not on a signature.
7. Hosted check runs at the exact head (`receipts/hosted-checks-snapshot.tsv`).
8. Only after my own pass: R636-1's findings (PR comment 6199187632).
   - I had not read R637-1's report when this verdict and ledger were written.
   - Its two findings are resolved here as the manager's round-2 assignment states them.

## Findings

### R636-2-F1 MINOR: the documented sv2v counts contradict their own published log

- **Severity:** MINOR. Fixing it changes stated measurement figures, so it is not RESIDUE.
- **Lens:** Docs.
  - Conformance is not affected. The peak that #744 item 2 asks to record agrees with its source receipts: 1212036 KiB in this run, and 1213100 KiB as the constant.
- **Where:**
  - `docs/testing/CI_WORKFLOWS.md:2428-2430`: "A second such run, with `/usr/bin/time` around each of its 133 sv2v and 141 Yosys runs, passed the same way. 25 of those sv2v runs elaborated the full datapath, 23 of them above 1205884 KiB and the largest at 1212036 KiB."
  - The PR body's R636-3 row, which REVIEW READY round 2 repeats: "133 sv2v runs, of which 25 elaborated the full datapath, the largest at 1212036 KiB".
- **Evidence:**
  - The cited log is `author-r2/evidence/r2/sv2v-rss-selftest.log`. It is unredacted, and its SHA-256 `d91554a61e08…4f43` matches the manifest.
  - I recounted it with `scripts/sv2v_recount.py` (`receipts/sv2v-recount.txt`):
    - 133 sv2v runs, 10 of which exited nonzero, and the largest at 1212036 KiB. These agree with the doc.
    - **20** runs are above 1205884 KiB, not 23. The whole log has only 20, so no subset of it can have 23.
    - **120** runs are at or above 1.0 GB (1168056 to 1212036 KiB), not 25. The other 13 are at or below 972388 KiB.
- **Impact:**
  - An authoritative measurement record states counts that its own cited receipt refutes.
  - A cold reader who checks the log finds the record wrong.
  - The constant and the bounds are unaffected.
- **Required outcome:**
  - The doc and the PR body state counts that the cited log reproduces. Alternatively, they define "elaborated the full datapath" by a criterion that a reader can apply to the published log or census output.
  - Either way, "23 above 1205884 KiB" must become a figure the log shows (20).
- **Verification:** rerun `scripts/sv2v_recount.py` on the cited log and compare its output with `CI_WORKFLOWS.md` and the PR body.

### R636-2-F2 RESIDUE: a review-finding label in new source comments

- **Severity:** RESIDUE. The defect is comment wording only, and it changes no behaviour or figure.
- **Authority:** the owner's comment rule (2026-10-15). Source comments state behaviour and reason with issue and requirement IDs. They never show review rounds, reviewer IDs or comment IDs, and "M1" is a review-finding label.
- **Where and exact fix:**
  - `scripts/check_baremetal_only.py:359`
    - From: `# #744, decided in M1 on PR #745: the act slot's OOM accounting and the census`
    - To: `# #744: the act slot's OOM accounting and the census`
  - `scripts/check_baremetal_only.py:1283`
    - From: `# the runner policy paragraph's own masked line, the fifth file M1 names`
    - To: `# the runner policy paragraph's own masked line, the fifth file with a host path`
  - `scripts/check_baremetal_only.py:1293`
    - From: `# M1's negative control: an unrelated new reference in the same file is still refused`
    - To: `# an unrelated new reference in the same file is still refused`
- None of these comment lines is a declared line, so the gate is unaffected.

### R636-2-F3 SUGGESTION: no arm binds a declared line against the other declared files

- **Lens:** Tests.
- **Where:** `_arms_host_memory_reads` at `scripts/check_baremetal_only.py:1274-1313`. Its "wrong-file" variant plants each declared line only in `scripts/other.py`, an undeclared file.
- **Evidence:**
  - In `receipts/baremetal-mask-probe.txt`, the mutant "lines pooled across the declared files" survives: `--check` rc 0 and `--selftest` PASS (790).
  - That mutant lets every one of the 14 lines pass in each of the four declared files.
  - The other four mutants are caught: declared lines accepted in every file, declared lines accepted in a product document, a second path on a line masked unbound, and an earlier per-file mask replaced rather than extended.
- **Why it is not a defect:**
  - The shipped code binds each line to its own file (`with_declared_lines`, `:400-409`).
  - The pooled form would admit only these 14 host-tool spellings, and only in the four host-tool files.
  - The refusals M1 ruled on, in another file and in a product document, are proved.
- **Suggestion:**
  - Add a variant that plants each declared line in a different declared file, for example the `scripts/ci_gate_workflows_selftest.py` line in `scripts/act_ci.py`.
  - Or narrow the claim at `CI_WORKFLOWS.md:2363-2366`, "the same line in another file … the self-test proves each refusal", to what is proved.

### R636-2-F4 SUGGESTION: the census refusal controls do not check why they refused

- **Lens:** Tests.
- **Where:** `census_budget` and `census_controls` at `scripts/ci_gate_workflows_selftest.py:235-328`. A refusing case asserts only a nonzero rc and no `GITHUB_ENV` output.
- **Evidence:**
  - The author's `budget-shell-mutants.txt` records "cat failure ignored: SURVIVED".
  - `receipts/budget-equivalence-probe.txt` runs two spellings of that mutant: `|| true`, and an unguarded assignment under errexit.
  - Both still refuse a mode-000 limit and a directory limit before export: the first through the empty-limit case, the second through errexit.
  - So the mutant is outcome-equivalent, and the requirement "refuses before `CI_CENSUS_JOBS` is exported" holds.
- **Suggestion:** assert each refusal's stderr reason ("unsearchable cgroup", "unreadable memory limit", "non-numeric memory limit"). A refusal for an unrelated reason then cannot satisfy a control.

## Prior findings, resolved or retained

| Prior finding | Status at `43a25fa7` |
|---|---|
| M1 = R636-1 BLOCKER = R637-1-F2: the bare-metal gate fails with 21 findings | **Resolved** |
| R637-1-F1 MAJOR: an unreadable limit was treated as no limit | **Resolved** |
| R636-2 RESIDUE: the manifest's completeness is misdescribed | **Resolved** |
| R636-3 SUGGESTION: the peak was measured over `--check` only | **Resolved** |
| R636-4 SUGGESTION: `valid_build` is named for more than it decides | **Resolved** |

The evidence for each follows.

**M1 = R636-1 BLOCKER = R637-1-F2**

- **Declarations.** `HOST_MEMORY_READS` (`scripts/check_baremetal_only.py:367-391`) declares 14 lines:
  - 5 in `act_ci.py`, 3 in `ci_runtime_workflows.py`, 3 in `rtl-fast.yml` and 3 in `ci_gate_workflows_selftest.py`.
  - Each exists exactly once in its file: `act_ci.py:4618,13301,13302,14791,14792`; `ci_runtime_workflows.py:62,65,81`; `rtl-fast.yml:437,440,456`; `ci_gate_workflows_selftest.py:254-256`.
  - Every other `/proc` or `/sys` line in those files is an earlier #376 or #532 mask (`act_ci.py:176,9105,9188,16679`).
- **Mask.** The mask is `(?<=^before)token(?=after$)`. It is applied per line after the T-class masks, so it fails closed.
- **Rewording.** M1 ruled that prose needing only a word is reworded. M1's six `kernel` hits were reworded to "host cgroup's" or dropped.
- **Gate results.**
  - `--check` reports OK with 0 findings over 1344 files.
  - `--selftest` passes 790 arms, 90 of them new: 5 files × (1 allowed + 3 unrelated), plus 14 lines × 5 variants.
  - Both hold under 3.12 with the pinned dependencies (`receipts/r2gates/`) and under 3.14 (`receipts/baremetal-*-py314.log`).
- **Hosted.** Hosted `docs-gates-0` job 116625786754 executed step 28 "Bare-metal scope gate" at this exact head, with success (`receipts/hosted-docs-gates-0-steps.txt`).
- **Mutants.** The author's six mask mutants are each caught (`baremetal-mask-mutants.txt`). Four of my five are caught; the survivor is R636-2-F3.
- **Full docs-gates set.** All 47 steps exited 0 at this head under Python 3.12.3 (`docs-gates-43a25fa/summary.tsv`), with status-before and status-after both empty.
- **PR body.** The round-1 verification claim is corrected.

**R637-1-F1 MAJOR**

- **Refusals.** `ci_runtime_workflows.py:67-82` and `rtl-fast.yml:442-456` refuse before `CI_CENSUS_JOBS` is written in three cases:
  - an unsearchable cgroup directory on the walk;
  - a present `memory.max` that `cat` cannot read;
  - a non-numeric or empty limit.
- **Absent controller.** An absent `memory.max` keeps the MemTotal fallback ("a cgroup without a memory controller: 16").
- **Controls, executed.** I ran the self-test as uid 1000, so every mode-000 control executed and none skipped (`receipts/r2gates/gen-selftest.log`):
  - mode-000 limit, mode-000 ancestor limit and mode-000 ancestor cgroup: refused;
  - limit and ancestor limit as directories: refused;
  - act container at 8 GiB: 4; 4 GiB ancestor: 2; hosted runner: 4.
- **My edge probes** (`receipts/budget-edge-probe.txt`):
  - the leaf cgroup itself mode 000: refused;
  - an unsearchable cgroup two levels up: refused;
  - a mode-000 limit two levels up: refused;
  - a readable 8 GiB limit two levels up: 4.
- **Round-1 shell.** The author's receipt shows that round 1's `-r` shell fails the new controls (`budget-shell-mutants.txt`).
- **Consistency.** These all pass, and the generator, workflow, contract and docs (`CI_WORKFLOWS.md:2028-2049`) agree:
  - `ci_gate_workflows.py --check`: the generator equals the workflow;
  - `ci_events.py --check` and `--selftest`: 2187 items and 5218 arms.
- **Root skip.** It is stated in `ci_gate_workflows_selftest.py:279-323`, in the docs and in the PR body.

**R636-2 RESIDUE**

My round-1 exact texts are in place:
- at `CI_WORKFLOWS.md:2016-2017` and `:2522-2524`;
- in the PR body's limitations bullet: "its completeness does not read the slot's memory events".

**R636-3**

- **Constant.** `CENSUS_WORKER_BYTES` = 1242214400 = 1213100 × 1024. That is the largest process in round 1's capped `--check --selftest --jobs 4` run.
- **Attribution.** In round 2's per-tool run, the largest sv2v was 1212036 KiB, equal to that run's largest process (`census-capped-jobs4-selftest-time.txt`). That supports attributing the larger round-1 figure to sv2v.
- **Bounds.** They are unchanged, by arithmetic:

  | Memory | 2M / 3C | Workers |
  |---|---|---|
  | 8 GiB | 4.61 | 4 |
  | 4 GiB | 2.30 | 2 |
  | 2 GiB | 1.15 | 1 |
  | Hosted runner, 16 GiB and 4 CPUs | 9.2 | 4 (capped at nproc) |

- **Executed checks.** The self-test asserts 4·3C ≤ 16 GiB < 5·3C. The author's real-cap receipt gives 4 at 8G, 2 at 4G and 1 at 2G.
- The surrounding counts are R636-2-F1.

**R636-4**

- `slot-memory.json` now carries `"oom_free"` (`act_ci.py:4609-4612`), and its self-test assertions are updated (`:7021`, `:7028`). No `valid_build` remains in the tree.
- The docs are updated at `CI_WORKFLOWS.md:2517-2524`.
- The printed `valid build: False` line stays, as #744 item 1 names it.
- The author's runner self-test receipt (`docs-gates-43a25fa/44.log`) passes the renamed arms in both the direct and isolated forms.

## What was checked, per lens

```text
[R636] PASS Conformance — scripts/check_baremetal_only.py:359-409 (HOST_MEMORY_READS, declared_line_mask, with_declared_lines), scripts/ci_runtime_workflows.py:44-90, .github/workflows/rtl-fast.yml:432-461, scripts/act_ci.py:4606-4612 and sha256 b8a786ce...3ba8 at 43a25fa7 — against #744 items 1-3, round-2 assignment items 1-5 and the M1 ruling (each host read declared whole by exact spelling and file; prose reworded; unrelated reference refused; --check, --selftest and the full docs-gates set rc 0); receipts/r2gates/*, hosted docs-gates-0 step 28 success, author summary.tsv 47/47
[R636] PASS RTL — no HDL, constraint or RTL source in f643377f1..43a25fa7; census worker model scripts/ci_runtime_workflows.py:44-51 (C = 1242214400, bounds 4/2/1/4 by arithmetic) and generated .github/workflows/rtl-fast.yml:459; generator equals workflow (receipts/r2gates/gen-check.rc 0); contract scripts/ci_events.py (events-check and events-selftest rc 0); the #259 boundary contract is extended only by line-and-file declarations
[R636] PASS Robustness — emitted budget shell scripts/ci_runtime_workflows.py:62-87 under unsearchable leaf and ancestor, mode-000 limits at depth 0, 1 and 2, directory limits, non-numeric or empty limit, missing MemTotal, zero CPUs, absent controller (receipts/r2gates/gen-selftest.log, receipts/budget-edge-probe.txt, receipts/budget-equivalence-probe.txt); gate mask scripts/check_baremetal_only.py:393-409 fails closed under prefix, suffix, other-path, other-file and product-doc variants (selftest 790 PASS, receipts/baremetal-mask-probe.txt)
[R636] PASS Tests — scripts/check_baremetal_only.py:1274-1313 (90 arms; each refusal arm expects the exact file:line [R] finding); scripts/ci_gate_workflows_selftest.py:235-328 (16 cases, 5 new denial controls, executed non-root); author mask mutants 6/6 caught; author budget mutants 2/3 caught, the third shown outcome-equivalent; my mask mutants 4/5 caught (survivor: SUGGESTION R636-2-F3); renamed runner arms PASS in author receipt docs-gates-43a25fa/44.log
```

**Docs: UNCLEAN (R636-2-F1)**

- **Examined.** These were compared with the code at this head and with the author's published receipts:
  - `docs/testing/CI_WORKFLOWS.md:2016-2017`, `:2028-2049`, `:2357-2366`, `:2416-2437` and `:2512-2535`;
  - the PR body;
  - the `check_baremetal_only.py` module docstring at `:53-59`.
- **Doc gates.** All pass:
  - `check_em_dash.py`: 0 findings over 119 added lines;
  - `gen_toc.py --check`;
  - `docs_check.py`;
  - the cited-path gate, in the author's 47 of 47.
- **Finding.** One measurement statement contradicts its own receipt: R636-2-F1.
- R636-2-F2 is RESIDUE in source comments and does not affect the lens.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #744 items 1-3; round-2 items 1-5; M1 ruling; `check_baremetal_only.py:359-409`; `ci_runtime_workflows.py:44-90`; `rtl-fast.yml:432-461`; `act_ci.py` digest; `receipts/r2gates`; hosted `docs-gates-0` step 28 | R636-2 | `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e` |
| RTL | CLEAN | No HDL in the delta; census worker model and constant; generator equals workflow; `ci_events` contract | R636-2 | `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e` |
| Robustness | CLEAN | Budget shell denial and absence paths, including my depth-2 probes and the mutant-equivalence probe; mask fail-closed variants | R636-2 | `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e` |
| Tests | CLEAN (SUGGESTIONs F3 and F4 only) | 90 bare-metal arms; 16 census cases executed non-root; the author's and my mutants; renamed runner arms in the author's receipt | R636-2 | `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e` |
| Docs | UNCLEAN (R636-2-F1) | `CI_WORKFLOWS.md` delta sections; PR body; gate docstring; doc gates | R636-2 | `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e` |

## Real limits

- **Runner self-test.** I did not run `scripts/act_ci.py --selftest`; the assignment forbids it. The runner evidence is the author's receipt (`docs-gates-43a25fa/44.log`), with `selftest: PASS` in both the direct and the isolated form. The `act_ci.py` delta is only a field rename, a docstring and self-test strings.
- **What I ran.**
  - No act, Docker, census, builder or full gate bank.
  - My gate runs used CPython 3.12.13 in a scratch venv with the pinned `ci/requirements-evidence.txt` and `tools/markdown/requirements.txt`. The author used 3.12.3.
  - I also ran the bare-metal gate under 3.14.7.
- **Hosted runs.** They were still in flight when snapshotted (`receipts/hosted-checks-snapshot.tsv`).
  - Completed with success: `docs-gates-0`, `docs-gates-2` and `docs-check-no-git`.
  - Queued or in progress: `publication-census`, `docs-gates-1`, `yosys-elaboration` and the Verilator shards.
  - Skipped: "Physical gPTP". A skipped context is not hardware proof.
  - The manager owns hosted and act acceptance.
- **Dangling symlink.** A dangling `memory.max` symlink is treated as absent (`receipts/budget-edge-probe.txt`). cgroupfs never contains symlinks, so this is not a finding.
- **Evidence integrity.** The evidence commit is unsigned. Integrity rests on `MANIFEST.json`, where all 41 author-r2 entries match.
- **Hardware.** Physical calibration was NOT RUN, and no hardware was used.
- **Restoration.** The probes rewrote `scripts/check_baremetal_only.py` and `scripts/ci_runtime_workflows.py` in place and restored them. Afterwards (`receipts/restore-verification.txt`):
  - the worktree matches the index, and the index matches HEAD;
  - `write-tree` gives `9c0a8e43…`;
  - the touched blobs and modes equal HEAD's;
  - the submodule gitlinks are unchanged.

## Pending manager duties

- **#744 item 2 receipt.** Run the full four-job act replay at this head and publish it. When this report was written, no replay receipt at `43a25fa7` had been posted on #744 or PR #745, and this review does not claim one.
- **Re-pin.** Re-pin `scripts/act_ci.py` to `b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8`.
- **Hosted contexts.** Accept or refuse the exact-head contexts still in flight, distinguishing executed jobs from skipped ones.
- **Merge candidate.** At the merge turn, validate the current-dev merge candidate with the builder and native banks: source base `84f9e300`, live dev `9ef71772`. No manager source bank ran at this head.
- **Residue.** Carry R636-2-F2 to the residue checklist.

R636-2 FINISHED
