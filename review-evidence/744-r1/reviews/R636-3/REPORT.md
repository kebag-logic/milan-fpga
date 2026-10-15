[R636] POSITIVE - exact head 7997eeb348c3af302079c7273d1b3092eee4dc6c

Internal independent re-review, round R636-3, of issue #744 / PR #745. Exact head `7997eeb348c3af302079c7273d1b3092eee4dc6c`, tree `0c1f8256e6b5ebc7791d1c0062dafb883402a567`. It is a delta review of `43a25fa7..7997eeb3` (five commits), as assigned on #744 (comment 6200881924).

- **Result:** no BLOCKER, MAJOR, MINOR or RESIDUE is open. All four R636-2 findings are resolved at their cause. Three SUGGESTIONs are recorded (R636-3-S1 to S3). They are optional and leave every lens clean.
- **Scope of the delta:** `.github/workflows/rtl-fast.yml` (regenerated, +2/-2), `docs/testing/CI_WORKFLOWS.md` (+11/-8), `scripts/check_baremetal_only.py` (+9/-3), `scripts/ci_gate_workflows_selftest.py` (+32/-19) and `scripts/ci_runtime_workflows.py` (+2/-2). The delta has no HDL, constraint, firmware or runner (`scripts/act_ci.py`) change.

## Inputs, in reading order

1. `AGENTS.md`, `CONTRIBUTING.md` (by section), `docs/README.md`.
2. Issue #744: the body (defects 1 and 2), the round-3 assignment (comment 6200881924, items 1-4) and the review-start comment 6202091587.
3. The authority sections of `docs/testing/CI_WORKFLOWS.md` that the delta touches: lines 2036-2052 (census budget), 2357-2369 (host memory reads) and 2418-2440 (resource bounds).
4. `git diff 43a25fa7..7997eeb3`, read in full, and the lane's diff from `84f9e300` for comment-label residue only.
5. Public evidence at `7b102ada:review-evidence/744-r1`. Each file I used matches `MANIFEST.json`'s `published_sha256` (`receipts/author-evidence-check.txt`, 15 of 15 OK). The evidence commit is unsigned, so the integrity anchor is the manifest digest.
6. I read the prior public findings (my own R636-2 report) only after my independent pass over the diff. I read no other reviewer's report.

## Findings

### R636-3-S1 SUGGESTION: three cross-declared-file pairings are skipped by the new arms

- **Lenses:** Tests, Docs.
- **Where:**
  - `scripts/check_baremetal_only.py:1302-1305`: the `others` filter skips a `.yml` destination for any unindented line.
  - The affected lines are `scripts/act_ci.py` line 0 and `scripts/ci_runtime_workflows.py` lines 0 and 1, each planted in `.github/workflows/rtl-fast.yml`.
  - The doc claim is at `docs/testing/CI_WORKFLOWS.md:2366-2369` ("the same line in another file, including another declared one … the self-test proves each refusal").
- **Evidence:** `receipts/yml-skip-probe.txt` (script `scripts/yml_skip_probe.py`).
  - Each of the three lines, planted alone as the whole of `rtl-fast.yml`, is a parseable YAML file. The shipped gate refuses it as `[R]` at line 1.
  - Under the pooled-lines mutant, the same three plants are ACCEPTED.
  - So the stated reason, "a workflow's block scalar holds only an indented line unchanged", covers the `run: |` shape only. The bare-line shape is a valid destination that no arm plants.
- **Why it is not a defect:**
  - The shipped code refuses all three pairings.
  - The assigned mutant (pooled lines) is caught by 39 arms.
  - Only a mutant that admits these unindented lines into the workflow file alone would survive.
- **Suggestion:** for an unindented line, plant it in the `.yml` destination as a bare document (no `run: |` header). Alternatively, narrow the doc sentence to the pairings that are proved.

### R636-3-S2 SUGGESTION: re-wrap the shortened comment

- **Lenses:** Docs.
- **Where:** `scripts/check_baremetal_only.py:359-365`.
- **Detail:** the first line is now `# #744: the act slot's OOM accounting and the census`, half the width of the six lines below it. That was the exact text R636-2-F2 prescribed, so this is cosmetic only. Re-flowing the paragraph is optional. No line in the paragraph is a declared line.

### R636-3-S3 SUGGESTION: the MemTotal reason also covers a zero value

- **Lenses:** Robustness.
- **Where:** `scripts/ci_runtime_workflows.py:63` and `.github/workflows/rtl-fast.yml:438`.
- **Detail:** a `MemTotal: 0 kB` line, or a non-kB unit, also prints `no MemTotal in kB`. The step still refuses, so behaviour is correct, and only the reason text is approximate. The control (`no MemTotal`) plants the absent case only. Optional: `no positive MemTotal in kB`.

## Prior findings, resolved or retained at this head

| Prior finding | Status | Evidence at `7997eeb3` |
|---|---|---|
| R636-2-F1 MINOR (Docs): the sv2v counts contradicted their log | **Resolved** | `CI_WORKFLOWS.md:2430-2436` now states 133 sv2v runs, 10 nonzero, 120 peaking at 1168056 to 1212036 KiB, 20 above 1205884 KiB, and the largest, 1212036 KiB, as that run's largest process. My new recount (`scripts/sv2v_recount3.py`, `receipts/sv2v-recount3.txt`) on the cited log (sha256 `d91554a6…3f75`, manifest OK) gives exactly 133 / 10 / 120 / 1168056-1212036 / 20 / max 1212036. None of the 120 large runs exited nonzero. "Elaborated the full datapath" is dropped. The second run's step-wide `Maximum resident set size` is 1212036 KiB (`author-r3/evidence/r2/census-capped-jobs4-selftest-time.txt`), and the first run's is 1213100 KiB (`author-r3/evidence/census-capped-jobs4-time.txt`). 1213100 × 1024 = 1242214400 = `CENSUS_WORKER_BYTES`. Yosys max 380492 KiB and scope peak 5569384448 match their logs. In the live PR body (identical to the published `author-r3/PR-BODY.md` apart from one trailing blank line), lines 43, 76 and 87 state the same reproducible figures. |
| R636-2-F2 RESIDUE: review labels in source comments | **Resolved** | `scripts/check_baremetal_only.py:359`, `:1283` and `:1293` carry the exact prescribed texts. A grep of every added line in `43a25fa7..7997eeb3` and of every added non-Markdown line in `84f9e300..7997eeb3` finds no review label, round, reviewer ID, lane label or comment ID. |
| R636-2-F3 SUGGESTION (taken): no arm planted a declared line in another declared file | **Resolved** | There are 39 new `declared-file-` arms (selftest 790 → 829 arms, `receipts/bm-selftest.log`). Under my pooled-lines mutant they are not caught: 39 failures, all `declared-file-` arms (`receipts/mutants/m1-pooled.log`). The same mutant with the new arms removed passes all 790 (`m1-pooled-old-arms.log`), so the new arms are what detect it. One residual pairing gap is S1. |
| R636-2-F4 SUGGESTION (taken): the census refusal controls did not check why they refused | **Resolved** | Each of the 9 refusal cases asserts `got is None` and that its last stderr line equals its own stated reason (`ci_gate_workflows_selftest.py:339`). Each of the 7 passing cases asserts empty stderr. All 16 cases pass non-root (`receipts/gate-selftest.log:57-73`). My mutant M2 (an unreadable limit swallowed and refused later as non-numeric) and M3 (the CPU and MemTotal reasons removed) fail the new controls by reason. Both pass the pre-delta controls (`receipts/mutants/summary.txt`). |

The earlier round-1 findings were recorded as resolved at `43a25fa7` (R636-2). The delta changes nothing they depend on: the walk, the `[ -e ]` test, the `HOST_MEMORY_READS` declarations and the masks are unchanged. Only the two `test` lines gained reasons, and the arm set grew.

## What was checked, per lens

```text
[R636] PASS Conformance — docs/testing/CI_WORKFLOWS.md:2430-2436, scripts/ci_runtime_workflows.py:47-90, .github/workflows/rtl-fast.yml:432-461 at 7997eeb3 — against #744 defect 2 (bound by measured per-sv2v peak) and round-3 assignment items 1-4: every stated count reproduces from its cited log (receipts/sv2v-recount3.txt) and the step-wide time receipts; CENSUS_WORKER_BYTES and every bound unchanged; the refusal semantics (refuse before CI_CENSUS_JOBS is written) unchanged, now with a stated reason on every refusal path; generated workflows equal the generator (receipts/regen-equality.txt, ci_gate_workflows.py --check rc 0)
[R636] PASS RTL — no HDL, constraint, firmware or SoC source in 43a25fa7..7997eeb3 (git diff --stat, 5 files, all CI scripts/docs); the census worker model scripts/ci_runtime_workflows.py:47-51 and its regenerated copy .github/workflows/rtl-fast.yml are unchanged except for the two reasoned test lines; the #259 boundary contract (scripts/check_baremetal_only.py HOST_MEMORY_READS, declared_line_mask, with_declared_lines) is unchanged; --check 0 findings over 1344 files (receipts/bm-check.log)
[R636] PASS Robustness — scripts/ci_runtime_workflows.py:59-87: under set -euo pipefail, `test … || { echo …; exit 1; }` refuses on a zero, empty or non-integer value with its own reason and writes no export; executed over zero CPUs, missing MemTotal, mode-000 leaf/ancestor limit, mode-000 ancestor cgroup, directory limits, non-numeric and empty limit (receipts/gate-selftest.log:64-72); shipped gate refuses each declared line in every other declared file including the three skipped yml pairings (receipts/yml-skip-probe.txt); S3 is wording of one reason only
[R636] PASS Tests — scripts/ci_gate_workflows_selftest.py:235-341 (reason-bound refusals, empty-stderr passes; mutants M2, M3 caught, both survive the pre-delta controls); scripts/check_baremetal_only.py:1274-1318 (829 arms; pooled-lines mutant fails exactly the 39 new arms and survives without them); author receipts r3/budget-reason-mutants.txt (5/5 caught) and r3/baremetal-pooled-mutant.txt (39 arms) agree with mine; author docs-gates-7997eeb/summary.tsv 47/47 rc 0 at head 7997eeb3; residual pairing gap is S1 (SUGGESTION)
[R636] PASS Docs — docs/testing/CI_WORKFLOWS.md:2046-2050 (each refusal prints its own reason as the step's last error line, matches selftest :339), :2366-2369 (cross-declared-file refusal, proved for 39 of 42 pairings and refused for all 42: S1), :2430-2436 (counts reproduce); PR #745 body lines 43, 76, 87 and 89-90 consistent with the code and receipts; no review label in any new source comment; S2 is cosmetic
```

## Commands and receipts (exact head, clone `r636-3-744`, non-root)

- `python3 scripts/ci_gate_workflows.py --check`: rc 0 (`receipts/gen.rc`). All four generated workflows equal `rendered()` (`receipts/regen-equality.txt`).
- `python3 scripts/check_baremetal_only.py --check`: rc 0, 0 findings over 1344 files.
- `python3 scripts/check_baremetal_only.py --selftest`: rc 0, PASS (829 arms).
- `python3 scripts/ci_gate_workflows_selftest.py`: rc 0, with 16 census cases and no loud skip, since the run was non-root.
- `scripts/mutants.sh` ran six probes in disposable copies under `scratch/mut/`. Results are in `receipts/mutants/summary.txt`:
  - m1-pooled: rc 2, 39 caught.
  - m1-pooled-old-arms: rc 0, survives.
  - m2-swallow: rc 1, caught.
  - m2-swallow-old-test: rc 0, survives.
  - m3-silent: rc 1, caught.
  - m3-silent-old-test: rc 0, survives.
- `python3 -I scripts/sv2v_recount3.py <cited log>` → `receipts/sv2v-recount3.txt`.
- `python3 -I scripts/yml_skip_probe.py <tree>`, run on the shipped tree and on the pooled-lines mutant → `receipts/yml-skip-probe.txt`.
- **Clone restored and verified** (`receipts/clone-integrity.txt`):
  - HEAD and tree are exact, the porcelain status is empty, and the worktree and index equal HEAD.
  - The index tree is `0c1f8256…`.
  - The six gitlinks match HEAD, and `external` is not initialised.
  - `ls-files -s` sha256 is `1e963be2…ff06`.
  - No probe wrote to the clone.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | CI_WORKFLOWS.md:2430-2436; ci_runtime_workflows.py:47-90; rtl-fast.yml:432-461; cited sv2v, Yosys and time logs; #744 defect 2; assignment items 1-4 | R636-3 | 7997eeb348c3af302079c7273d1b3092eee4dc6c |
| RTL | CLEAN | delta file list (no HDL); census worker model; #259 boundary declarations; bare-metal --check | R636-3 | 7997eeb348c3af302079c7273d1b3092eee4dc6c |
| Robustness | CLEAN | emitted budget shell refusal paths (executed); cross-file refusal probe including the skipped pairings | R636-3 | 7997eeb348c3af302079c7273d1b3092eee4dc6c |
| Tests | CLEAN | ci_gate_workflows_selftest.py:235-341; check_baremetal_only.py:1274-1318; 6 own mutants; author r3 mutant receipts | R636-3 | 7997eeb348c3af302079c7273d1b3092eee4dc6c |
| Docs | CLEAN | CI_WORKFLOWS.md:2046-2050, 2366-2369, 2430-2436; live PR #745 body; new source comments | R636-3 | 7997eeb348c3af302079c7273d1b3092eee4dc6c |

Code that the delta does not touch keeps its R636-2 verdict at `43a25fa7`. The delta changes nothing that code depends on.

## Real limits

- My gate runs used the local Python 3.14.7, bash 5.3 and PyYAML 6.0.3, not the pinned CPython 3.12.3. The 3.12.3 source-head evidence is the author's published `docs-gates-7997eeb` set: 47 of 47 rc 0, with head file `7997eeb3`.
- I ran as non-root, so the root loud-skip path of the three mode-000 cases was not exercised.
- I re-ran no sv2v, Yosys, census or cgroup-capped measurement. The memory figures are the author's native measurements, which I checked only against their own receipts.
- I ran no manager source bank, builder bank, act replay, Docker or hardware. No physical calibration was run, and field skips are not hardware proof.
- Hosted checks at this head were mostly queued or in progress when I looked: `publication-census`, the Verilator shards and `docs-gates-0/1/2` were not yet concluded. A few completed contexts were successes, and Physical gPTP was skipped. I make no hosted acceptance claim.
- The evidence commit `7b102ada` is unsigned. Integrity rests on the manifest digests.

## Pending manager duties

- Hosted and act acceptance at the exact head. The act replay is held for #748, the shared tool-cache race.
- The merge of current `dev` (`9ef71772…`) into PR #745 after #748 lands, with its own merge-only check. The candidate-merge validation (builder and native banks) is to be linked on the PR.
- Carry S1-S3 as optional items. No RESIDUE is open from this round.

R636-3 FINISHED
