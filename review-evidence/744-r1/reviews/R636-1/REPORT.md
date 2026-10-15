[R636] NEGATIVE - exact head f643377f15c0d939d875ae5698672f1b0a99a644

# R636-1: internal cleared-context review of PR #745 for #744

- Exact head: `f643377f15c0d939d875ae5698672f1b0a99a644`, tree `3e77395e26cb6216d0908fbec71cec87421d826f`.
- Source base and live `dev`: `84f9e3001b7d9b77835c4a9a599dbe6230a8031b`.
- Diff reviewed: `84f9e3001..f643377f1`, three commits, 8 files, +541/-134.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Result: one BLOCKER (R636-1), one RESIDUE (R636-2) and two SUGGESTIONs (R636-3, R636-4). Only Robustness is clean.

## Inputs, in reading order

1. `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
2. #744: the assignment (comment 6197842304), its clarification (6197855588), the author's TAKEN and the author's REVIEW READY.
3. The interface authorities:
   - `docs/testing/CI_WORKFLOWS.md`: the census job paragraph, the CPU and memory budgets, Parallel replay slots, and the bare-metal scope paragraph at 2341-2348.
   - `docs/testing/CI_SIGNATURE.md` 108-144: the local manifest collector.
   - `scripts/ci_manifest.py` and `scripts/ci_local_manifest.py`.
   - `.github/ci-templates/docs.yml:183-186`, with its contract in `scripts/ci_events.py:1034-1035`.
4. The full diff, including all of `scripts/act_ci.py` (587 diff lines) as the trust boundary, and the history.
5. Public evidence:
   - `review-evidence/744-r1` at `36ab73f9`: every file's bytes match its `MANIFEST.json` `published_sha256` (`receipts/author-evidence-sha256.txt`).
   - The PR body.
   - The exact-head hosted runs 38781738587 (docs), 38781738337 (rtl-fast), 38781738041 (rtl-full) and 38781738032 (elaborate).

## Findings

### R636-1 BLOCKER: the required bare-metal scope gate fails at the head

- **Severity:** BLOCKER.
- **Lenses:** Conformance, RTL, Tests, Docs.
- **Where:** `scripts/check_baremetal_only.py --check` reports 21 findings. Every one is on a line this PR adds:
  - `.github/workflows/rtl-fast.yml:437,440,451`
  - `scripts/ci_runtime_workflows.py:58,61,72`
  - `scripts/act_ci.py:4618,7012,13301,13302,13305,14758,14760,14791,14792`
  - `scripts/ci_gate_workflows_selftest.py:249,250,251`
  - `docs/testing/CI_WORKFLOWS.md:2039,2489,2505`
- **Authority:**
  - The gate is a required step of the `docs` workflow: "Bare-metal scope gate" at `.github/ci-templates/docs.yml:183-186`, in the source contract at `scripts/ci_events.py:1034-1035`. It enforces #259's bare-metal scope.
  - `docs/testing/CI_WORKFLOWS.md:2341-2348` sets the boundary. Host-tooling literals are masked only in their exact code contexts in `scripts/act_ci.py`, and "the same literals in any other context or file, or in a product document, are still refused".
  - #744 says "Run every touched gate, all rc 0". `AGENTS.md` section 7 requires the local gates to pass and "Existing regressions remain green".
- **Evidence:**
  - At the head, `check_baremetal_only.py --check` exits 1 with "FAIL (21 finding(s) across 1344 scanned file(s))" (`receipts/baremetal-head.log`).
  - At dev `84f9e300` it exits 0 with "OK (0 findings across 1344 tracked first-party file(s))" (`receipts/baremetal-dev.log`).
  - Hosted run 38781738587, job 116583405450 (`docs-gates-0`): step 28 "Bare-metal scope gate" failed at 18:00:23Z, listing the same 21 lines (`receipts/hosted-exact-head-excerpts.txt`). It is the first failure at this head.
  - Fail-fast then cancelled the other workflows. Hosted `publication-census` was cancelled while building Yosys, and its census step (14) was skipped, so no hosted census has run at this head.
  - The author's gate table (`final-gates.tsv`) and the REVIEW READY list both omit this gate.
- **Impact:**
  - The `docs` workflow is red at the head, so the PR cannot meet the hosted or local gate bar.
  - The four-job act replay that #744 item 2 needs as its receipt includes `docs`. It is expected to hit the same failure and cancel the whole replay (`scripts/act_ci.py:5928-5930`). The item-2 receipt therefore cannot be obtained at this head.
  - The REVIEW READY claim that every touched gate passes is not true.
- **Required outcome:**
  - `python3 scripts/check_baremetal_only.py --check` and `--selftest` both exit 0 at the fix head, without weakening the gate.
  - One way is to keep the new host-side reads, and their prose and fixtures, off the refused surfaces.
  - Masking the new contexts would extend a #259 scope boundary beyond `scripts/act_ci.py`: into the generator, the generated workflow, a self-test and a product-tree document. That needs a public decision first, and the gate's self-test must still prove the same literals are refused everywhere else. Manager finding M1, published after this verdict, records that decision; see Prior public review findings.
  - The author's validation list names this gate.
- **Verification:**
  - Both commands exit 0 at the new head.
  - Hosted `docs-gates-0` passes its "Bare-metal scope gate" step at that head.
  - Conformance, RTL, Tests and Docs are re-reviewed at that head.

### R636-2 RESIDUE: the manifest's completeness is misdescribed

- **Severity:** RESIDUE.
- **Lens:** Docs.
- **Where:** `docs/testing/CI_WORKFLOWS.md:2494-2496` and `:2016-2017`, and the PR body's limitations bullet.
- **Defect:**
  - The text says "The manifest's own completeness reads only job receipts, so `slot-memory.json` decides whether a slot run is valid evidence".
  - Completeness also reads environment provenance, the image digest and the action pins (`scripts/ci_manifest.py:176-197`).
  - A local manifest is always incomplete in round one, because the collector sets `image` to None (`scripts/ci_local_manifest.py:132`, `docs/testing/CI_SIGNATURE.md:139`).
  - The runner's behaviour is correct, so this is wording only.
- **Exact fix:**
  - At 2494-2496: "The manifest's completeness does not read the slot's memory events, so `slot-memory.json` and the exit status 2 carry an OOM's invalidity."
  - At 2016-2017: "`slot-memory.json` retains an isolated slot's memory accounting and whether an OOM invalidated it."
  - In the PR body bullet: "its completeness does not read the slot's memory events".

### R636-3 SUGGESTION: the measured peak covers `--check` only

- **Severity:** SUGGESTION.
- **Lens:** Tests.
- **Where:** `CENSUS_WORKER_BYTES` at `scripts/ci_runtime_workflows.py:47-50`.
- **Observation:**
  - The constant was measured over `--check --jobs 1` only.
  - In the author's capped `--check --selftest --jobs 4` run, the largest descendant reached 1213100 KiB (`census-capped-jobs4-time.txt`). That is 7216 KiB (0.6%) above the 1205884 KiB constant.
  - The one-third headroom absorbs this: the capped run passed with every memory event at zero.
- **Suggestion:** measure the per-tool peak over the self-test arms as well, or record this observation beside the constant. Either would make the constant a true upper bound for the workload it gates.

### R636-4 SUGGESTION: `valid_build` is true for any slot without an OOM

- **Severity:** SUGGESTION.
- **Lens:** Docs.
- **Where:** `"valid_build": not self.exhausted` in `SlotMemory.evidence()`, `scripts/act_ci.py:4608-4612`.
- **Observation:** in `slot-memory.json`, `"valid_build": true` means only that no OOM invalidated the slot. The same run's manifest is incomplete regardless.
- **Suggestion:** name the field for what it decides, or say so where it is documented, so a reader does not take a clean slot file for a valid build.

## What was checked, per lens

### Conformance: UNCLEAN (R636-1)

**Item 1 conforms in source.**

- `read_slot_memory` (`scripts/act_ci.py:4621-4651`) reads the slice's hierarchical `memory.events` fields `oom`, `oom_kill` and `max`, and its `memory.peak`. It no longer reads `memory.events.local`.
- It refuses whenever the counts cannot be proved:
  - the events are unreadable, malformed or incomplete;
  - there is not exactly one cgroup2 mount at the cgroup root;
  - the mount carries `memory_localevents`.
- It reads after container cleanup and before teardown: `execute_workflows` at `:5943-5953`, then `replay_slot` at `:4693-4704`, before the `finally` that releases the slice.
- `SlotMemory.exhausted` is `oom or oom_kill` (`:4584-4587`).
- On exhaustion, `slot-memory.json` records `valid_build: false`, the printed line ends `valid build: False`, and a Refusal gives `RC_REFUSED` = 2 (`:75`), whatever act returned.
- I read the full `act_ci.py` diff as the trust boundary. It adds no host command, credential, Docker or network path. Its only new host read is `/proc/self/mounts`, read in-process (`SlotHost.read_text = pathlib.Path.read_text`, `:4066`).
- The kernel propagates `memory.events` to ancestors when each event happens, so kills in child cgroups stay counted after those cgroups are removed. My real-kernel control read the slice after its killed scope had gone.
- The counters start at zero for each run: acquisition refuses an active slice (`:4304-4306`), and teardown proves the cgroup path is gone (`:4484`).

**Item 2 conforms in source.**

- The bound is emitted by the generator: `scripts/ci_runtime_workflows.py:47-80`, inserted at `:90-91`.
- The template (`.github/ci-templates/rtl-fast.yml:316`) and the contract (`scripts/ci_events.py:2476`) both use `"$CI_CENSUS_JOBS"`.
- The workflow is regenerated, not hand-edited:
  - `ci_gate_workflows.py --check` passes.
  - The step at `.github/workflows/rtl-fast.yml:432` equals `census_budget_step()["run"]` and is byte-identical to the author's `budget-step-as-executed.sh`.
  - It runs after the CPU budget step and before the census.
  - Only `publication-census` names `CI_CENSUS_JOBS`.
- The formula is `max(1, min(nproc, floor(2M/(3*1234825216))))`, with 1234825216 = 1205884 KiB × 1024 (`receipts/arithmetic.txt`).

**Item 3:**

- The head's `scripts/act_ci.py` SHA-256 is `9ce3a6604486c99209333430b09f8892bc2a5c0f5ed87b052a2ddc85577ffee8` (698675 bytes, mode 755).
- Dev's is `7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd` (`receipts/act_ci-sha256.txt`).

**Unclean:** R636-1 breaks the frozen requirement "every touched gate rc 0" and blocks the item-2 receipt.

### RTL: UNCLEAN (R636-1)

- No HDL changed in `84f9e300..f643377f1`.
- I applied the architecture side to the census resource bound and its worker model:
  - `sw/mailbox/census_selftest.py:182-195` and `publication_census.py:598-607` run one forked worker per `--jobs`.
  - Each arm calls the census with `jobs=1`, so a worker runs one sv2v and then one Yosys at a time. That matches the constant's model.
- The #259 bare-metal scope boundary is an existing architecture contract, and the head breaks it (R636-1).

### Robustness: CLEAN

[R636] PASS Robustness — `scripts/act_ci.py:4567-4704,5943-5953` and `scripts/ci_runtime_workflows.py:53-80` at f643377f1 — failure, malformed-input, ordering and configuration paths, checked against #744 and the cgroup v2 event semantics

**Runner accounting:**

- A body that raises keeps its own exception, with the accounting printed beside it (`:4697-4700`).
- `report_slot_memory_beside` can only meet a Refusal: `read_slot_memory` turns OSError, ValueError and KeyError into one.
- If the read inside the run is clean but the slot-exit read is not, the run still refuses.
- Negative counts are truthy, so they refuse.
- A duplicate or stacked cgroup2 mount refuses.

**Census budget step:**

- An empty or non-numeric `memory.max` exits 1.
- The walk up the parents ends at `/sys/fs/cgroup`, both on v1 (an empty `0::` entry) and for cgroup-namespaced paths.
- The arithmetic cannot overflow, since M ≤ MemTotal.

**Executed controls:**

- The emitted step under real cgroup caps (`receipts/budget-step-real-caps.txt`):

  | Memory bound | `CI_CENSUS_JOBS` |
  |---|---:|
  | 8G scope | 4 |
  | 4G scope | 2 |
  | 2G scope | 1 |
  | This 12 GiB unit | 6 |

  The hosted rtl-fast run at this head printed `census workers: 4 of 4 CPU(s) within 16765378560 bytes of memory`.
- The real-kernel control (`receipts/real-oom-control.txt`):
  - A 400 MiB allocation was killed in a 200 MiB scope under a fresh slice.
  - The slice read `oom 1 oom_kill 1` hierarchically and zero locally.
  - Dev's reader printed `the cap was hit 0 time(s), with no OOM at it`.
  - The head's reader returned `exhausted = True`, evidence `valid_build: False`, and the refusal text.

**Documented residual limits, all accepted:** slot 0 has no slice; on cgroup v1 only `MemTotal` is read; reclaim at a limit without an OOM keeps the verdict.

### Tests: UNCLEAN (R636-1)

**Re-executed at the head**, all rc 0 (`receipts/gates-summary.tsv`, `receipts/gates/`):

- `ci_gate_workflows.py --check`.
- `ci_gate_workflows_selftest.py`: 11 `Census budget:` cases, plus the owner and order line.
- `ci_events.py --check`.
- `ci_events.py --selftest`: `PASS (2187 contract items, 5218 arms)`.
- `ci_runtime_evidence_selftest.py` and `ci_manifest_selftest.py`.
- `check_py_idiom.py`, `check_sh_idiom.py` and `check_hygiene.py --check`.
- Doc gates, with the pinned renderer in a disposable venv:
  - `check_em_dash.py --base 84f9e300`: 0 findings over 92 added lines.
  - `gen_toc.py --check` and `--verify-anchors`.
  - `check_doc_style.py`, `check_doc_paths.py` and `docs_check.py`.

**Mutation probes** of the census budget step, run in the clone and then restored (`receipts/census-budget-mutants.txt`). The self-test kills all ten:

- no headroom
- leaf-only, plus a behavioural variant
- max instead of min
- no nproc cap
- no floor of one
- a garbage limit ignored
- MemTotal ignored
- the step not added
- the step placed after the census

**Runner arms, read but not run:**

- `selftest_slot_memory_cap` (`:14734`), `selftest_slot_memory_report` (`:14813`) and `selftest_slot_memory_evidence` (`:6991`).
- They cover:
  - #742's shape: hierarchical kills with clean local events;
  - the verbatim kernel fixture `OOM_KILLED_EVENTS` (`:13307`), with act rc 0 and with rc 3;
  - an OOM without a kill, and a kill without an OOM;
  - the malformed inputs and the mount guards;
  - the report printed beside a body's exception.
- The author's `mutants.txt` shows seven mutants caught.

**Unclean:** an existing regression, the bare-metal scope gate, is red, and the author's validation omitted it (R636-1).

### Docs: UNCLEAN (R636-1)

- Every figure in `CI_WORKFLOWS.md` 2013-2042, 2392-2412 and 2477-2525, and in `MAILBOX_SPLIT.md:1030-1036`, matches the published receipts:
  - sv2v 1167000 to 1205884 KiB, Yosys 386824 KiB;
  - 234 checks, 0 of 120 arms, 31 rules, 591 s;
  - 5806784512 bytes, 67.6% of the cap;
  - at jobs 16: 113 of 120, `oom_kill 209`, `oom 2298`;
  - the real control;
  - 5,218 arms, which I reproduced.
- Three of R636-1's 21 lines are documentation lines.
- R636-2 is a RESIDUE.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R636-1) | #744 items 1-3; `scripts/act_ci.py` full diff; generator, template, contract and regenerated workflow; digest | R636-1 | f643377f15c0d939d875ae5698672f1b0a99a644 |
| RTL | UNCLEAN (R636-1) | No HDL in the diff; census worker model (`census_selftest.py:182-195`, `publication_census.py:598-607`); #259 scope contract | R636-1 | f643377f15c0d939d875ae5698672f1b0a99a644 |
| Robustness | CLEAN | `act_ci.py:4567-4704,5943-5953`; `ci_runtime_workflows.py:53-80`; real-cap and real-kernel controls | R636-1 | f643377f15c0d939d875ae5698672f1b0a99a644 |
| Tests | UNCLEAN (R636-1) | Re-executed gates; 10 budget-step mutants; runner arms read; author `final-gates.tsv` and `mutants.txt` | R636-1 | f643377f15c0d939d875ae5698672f1b0a99a644 |
| Docs | UNCLEAN (R636-1) | `CI_WORKFLOWS.md` changed sections; `MAILBOX_SPLIT.md:1030-1036`; `CI_SIGNATURE.md:108-144`; PR body | R636-1 | f643377f15c0d939d875ae5698672f1b0a99a644 |

## Prior public review findings

- **Before the verdict:** when this round's verdict and ledger were written, no review finding had been published on PR #745 or #744.
- **After the verdict:** one finding was published, read only after the verdict and ledger were written.
- **Manager finding M1** (PR comment 6199082046), the bare-metal scope gate failing at `f643377f`: **RETAINED at this head.**
  - It is the same defect as R636-1, at the same 21 lines.
  - Its account that the manager's act replay of this head failed at `docs/docs-gates-0` and cancelled the replay confirms R636-1's predicted impact on the item-2 receipt.
  - M1 records the public decision that R636-1's required outcome asked for:
    - each host-tooling literal is declared by exact spelling and file in `scripts/check_baremetal_only.py`'s declaration table, as #738 did;
    - prose that only needs the word is reworded instead.
  - R636-1 is therefore cleared by a head where that decision is implemented, `check_baremetal_only.py --check` and `--selftest` exit 0, and the whole docs-gates set passes.

## Real limits

- **Runner self-test, act and Docker were not run.** They are outside this review's authority.
  - For the runner self-test I relied on the author's receipts (610 arms direct, 608 isolated, seven mutants) and on reading the arms.
  - My real-kernel control imports only the reader functions, from read-only copies of the head and dev files, and runs no runner command.
- **Interpreter:** my gates ran on CPython 3.14.7 with PyYAML 6.0.3, not the documented 3.12.3.
- **The census was not rerun.** The capped `--jobs 4` pass and the `--jobs 16` negative control are the author's native receipts. I checked them for consistency and arithmetic.
- **No Docker cgroup namespace.** The budget step has not run inside one. It ran on planted fixtures, real user scopes, and the hosted runner (4 of 4).
- **No physical calibration.** It was NOT RUN, and no hardware was used. Field skips are not hardware proof.
- **Hosted results:** I separated the one failure that actually executed (`docs-gates-0`, the bare-metal scope gate) from the cancellations and aggregate failures that followed it. Hosted acceptance is the manager's.

## Pending manager duties

- After R636-1 is fixed, run the full four-job act replay at the fixed head. It is #744 item 2's receipt and is not yet published.
- Re-pin `scripts/act_ci.py`. The digest above holds for this head only, and nine of R636-1's lines are in that file, so fixing them changes it.
- Run the exact-head hosted gates, the current-dev candidate merge validation and the post-merge containment check.
- Carry R636-2 to the residue checklist.

## Receipts

Everything below is listed in `MANIFEST.sha256`.

- `receipts/`:
  - gate logs and rc files;
  - the bare-metal gate at the head and at dev;
  - hosted excerpts;
  - the real-cap and real-kernel controls;
  - mutants;
  - digests;
  - author-evidence hashes;
  - index state before and after the probes.
- `scripts/`: the portable probe scripts.

**Clone state after the probes:**

- HEAD, tree, index and every tracked file are byte-identical to the head, with no status entries.
- Submodule gitlinks are unchanged: `third_party/verilog-axis` 48ff7a7e, `protocol-processor` 2ad2f845, `gptp-processor` e4869fd0 (`receipts/index-after.txt`).

R636-1 FINISHED
