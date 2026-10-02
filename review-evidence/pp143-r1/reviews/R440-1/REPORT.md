[R440] POSITIVE - exact head 7d9fabf13ea3ef08d7d204c0297820561054b04a

# R440-1: internal independent review of PR #146 (issue #143), round 1

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #146, closes #143
- Exact head: `7d9fabf13ea3ef08d7d204c0297820561054b04a`, tree `739f75ea8d7bbebed4c78478c9f624803f3816a2`
- Under review: the author's commits `85da751` and `ab8a50b` (REVIEW READY at `ab8a50be`) on `main` `631eeb34`, plus the manager's `--no-ff` merge of `main` `88969246` (PR #144)
- Review base for the diff: `88969246cbb82bf9d4975496f93a5420bbe3aa21..7d9fabf1`. This is 15 files: 8 drivers, `tb/common/mutant_pool.py` and 6 READMEs.
- Reconstruction order:
  1. The repository README and `docs/README.md`. The repository has no `AGENTS.md` or `CONTRIBUTING.md`.
  2. Issue #143: its body and acceptance list, and the assignment comment (lane opening).
  3. The PR body.
  4. The diff and history.
  5. The public author packet `kebag-logic/milan-fpga@e87e0642:review-evidence/pp143-r1/author`.
  6. Exact-head hosted CI, read only.
- Prior public review findings on this PR: none. At this head the PR carries only the two review-start notices. Nothing is to be resolved or retained.

## Verdict

POSITIVE. All six acceptance items of #143 hold at the exact head, and each was checked with this review's own runs:

- Five drivers ran in full at `--jobs 1` and `--jobs 8`: retry, adp, maap, srp_admission and srp_top. Three more ran as subsets at both N, covering every make target: gsi, aecp_dispatch and aecp.
- In every pair the summary is byte-identical, and every receipt is identical in its FAIL and tally lines.
- Every count compared equals its README.

There are no open MINOR, MAJOR or BLOCKER findings. One RESIDUE (wording only) and one SUGGESTION are recorded below.

## Findings

### R440-1-F1: RESIDUE (Docs). "The table's order" is not the printed order for maap and aecp

- **Where:**
  - `tb/maap/README.md:237`
  - `tb/pp_top/README.md:1005-1006` (aecp)
  - The same phrase appears at `tb/acmp_talker/README.md:209`, `tb/adp_engine/README.md:171`, `tb/pp_top/README.md:382` and `tb/pp_top/README.md:1076`.
- **Evidence:** The drivers print in the declared order of their table in code (`MUTANTS`), through `mutant_pool.in_order`. Two README tables do not follow that order:
  - The maap README table lists `seed-clamp-off-by-one`, `release-waits-for-draw`, `seed-rearmed-on-idle-release-only` (`tb/maap/README.md:259-261`). `tb/maap/mutants.py:48-49` declares `seed-rearmed-on-idle-release-only` before `seed-clamp-off-by-one`.
  - The aecp README table has 47 rows for 55 arms. Its row 10 (`dl-preempt-after-effect-top`) comes before the declared `dl-preempt-after-effect`.
  - Receipts: `receipts/table_order.txt`, and `receipts/maap_vs_readme.txt` (same rows by arm: True; same order: False).
  - For retry, adp, dispatch and gsi the README table order equals the declared order.
- **Impact:** None on behaviour. Every count matches by arm, and the summary order is deterministic and declared. The sentence only misnames which order is meant. It changes no measurement, figure, verdict, test, code or conformance claim, and touches no privacy rule.
- **Required outcome (exact fix):** In `tb/maap/README.md:237` and `tb/pp_top/README.md:1005-1006`, replace "printed in the table's order" with "printed in the driver's declared order (`MUTANTS`)". Optionally apply the same edit to the other four occurrences for uniformity.
- **Verification:** `python3 scripts/table_order.py <repo>` (packet) shows that only the maap and aecp tables differ. Grep the six lines after the edit.

### R440-1-S1: SUGGESTION (Robustness, Docs). State a worker's memory cost where `--jobs` is documented

- **Where:** `tb/pp_top/README.md`, at the three `--jobs N` paragraphs (lines 376-386, 997-1007 and 1064-1080), and `tb/common/mutant_pool.py:25-29`.
- **Evidence:** Every suite builds with Verilator `-j 0`, which uses one compiler thread per available CPU. At the default of 4, a wide host therefore runs four full-width `pp_top` builds at once, where the serial drivers ran one. The author's packet measures about 0.5 GB plus 0.25 GB per compiler thread for each `pp_top` worker. In this review, six campaigns at once (three of them at `--jobs 8`, four CPUs each) drove this 12 GiB unit to its memory limit 79 times (`memory.events max 79`). There was no OOM kill, and every verdict was still identical (`receipts/memory_events_after.txt`, `receipts/monitor.txt`).
- **Not a defect:**
  - The default and its meaning are mandated by #143: "the same meaning and default as d3_mutants.py", which has the same property.
  - The hosted runner (4 vCPU, 16 GB) fits: about 6 GB at 4 workers.
- **Possible outcome:** One sentence beside `--jobs` in the pp_top README, for example: "each `pp_top` worker needs about 0.5 GB plus 0.25 GB per compiler thread; under a memory cap, pin CPUs or lower N". This is not required for this PR.

### Pre-existing observations, out of #143's scope, not findings against this PR

The issue forbids any recorded-count change, so these stay unedited by this lane:

- `tb/srp_admission/README.md:94-95` records the srp_top control at 1527 checks (dated 2026-09-24). It now prints 2200 (`receipts/srpadm-j1/control-srp-top.log`, digest only). The author's packet reports the same observation. All nine mutant failing counts in the README are equal.
- `tb/srp_top/README.md`'s tables from rounds 1 and 2 are historical round records. Several of their counts differ from today's campaign. The README's current statement, `90 checks: 90 PASS, 0 FAIL` with assertion coverage 65/65 (`:231`), holds (`receipts/srptop_vs_readme.txt`).

## Acceptance of #143, item by item

| # | Acceptance | Evidence at the exact head | Result |
|---|---|---|---|
| 1 | Each listed driver has `--jobs N` with d3's meaning and default, and every worker uses its own private copy and `obj_dir` | See the detail below this table. | MET |
| 2 | `--only` and `--jobs` combine | See the detail below this table. | MET |
| 3 | Results do not depend on N, and the README records both wall times | See the detail below this table. | MET |
| 4 | The summary follows declared order | Every j1/j8 summary pair is byte-identical. `receipts/pool_probe.txt` shows declared order under shuffled finish times at N = 1, 3, 8, 64, 0 and -2. | MET |
| 5 | CI keeps passing with the hosted core count | `.github/workflows/hdl.yml` is unchanged against both `631eeb34` and `88969246`. The repository is public, so `ubuntu-latest` is the 4 vCPU / 16 GB runner, and `suites` has no `timeout-minutes` (default 360 min). The exact-head hosted runs are listed below this table. | MET for the steps that have executed; the manager owns hosted acceptance |
| 6 | `tb/pp_top/README.md` and the other campaign READMEs state the option, and the merge keeps both sides | All six READMEs state `--jobs N` with its default and both wall times (gsi, aecp and dispatch in the pp_top README). The merge was recomputed with `git merge-tree --write-tree ab8a50b 88969246` and gives tree `739f75ea…`, equal to the head tree. The only file both sides changed is `tb/pp_top/README.md`. Its hunks against `main` equal the author's hunks, and its hunks against the author side equal `main`'s hunks (`receipts/merge_check.txt`). | MET |
| out of scope | No mutant, control, patch or recorded count changes | AST comparison of every module-level constant and gsi `mutations()` between `631eeb34` and the head, and between `88969246` and the head: none changed or removed; only `RTL` (retry) and `Variant` (gsi) were added (`receipts/ast_tables_*.txt`). The judging functions (`run`, `run_case`, `tally`, `failures_of`, `completed`, `judge`, `build_tree`, `run_suite`, `mutations`) are AST-identical (`receipts/ast_functions_631_head.txt`). `git diff 88969246 HEAD` over `hdl/`, every `mutations/` directory, the tb C++, SV and Makefiles, `scripts/` and `.github/` is empty (`receipts/nonscript_diff.txt`, 0 bytes). | MET |

Detail for item 1:

- All eight drivers call `mutant_pool.add_jobs_argument`, which adds `type=int`, default `DEFAULT_JOBS = 4` and a pool of `max(1, N)`. This equals `tb/pp_top/d3_mutants.py:547,564`.
- Every unit (control, golden, baseline, arm, restored) runs in its own `tempfile.TemporaryDirectory` copy.
- No path two workers could race on:
  - Per-unit log names are unique for seven drivers.
  - srp_top's five shared receipt names are written by the consumer in declared order (`receipts/log_names.txt`).
  - ROMs are generated inside each copy (`*.hex` is never copied). The generators write only `-o`.
  - The one fixed filename the benches write, `obj_dir/build_tally.txt`, is per copy.
  - Patches touch `hdl/` only, so a fresh copy is equivalent to the old restore of `hdl/`.
  - No suite uses a fixed `/tmp` name, a lock or ccache.
- Watched live: up to 8 simultaneous private copies per `--jobs 8` driver, and 518 distinct copy directories in total, all removed at the end (`receipts/concurrency_summary.txt`, `receipts/monitor*.txt`).
- The source clone was unchanged apart from git-ignored `__pycache__` (`receipts/src_status_*.txt`).

Detail for item 2:

- gsi: `--only bridge-gate-removed wrong-sink latency-cmp-low8 failure-code-zero` ran exactly the golden, those 4 variants in declared order (not argument order), and restored.
- srp_admission: `--only pending-absent` ran the 3 controls plus its 3 suite runs (`6 checks: 6 PASS`).
- An unknown name gives a usage error with rc 2 on both drivers (`receipts/runs/*-only-unknown.out`).
- `--only` with `--jobs` ran correctly on the other six drivers: retry, srp_top (a label on two suites, whose receipt is the later row's), maap (an arm on two suites), adp, dispatch and aecp. Every selected arm was KILLED by its named check (`receipts/runs/*-only-*.stdout`).

Detail for item 3: see the equivalence table below. All six READMEs record both wall times.

Exact-head hosted runs for item 5 (`receipts/hosted_ci_head.txt`):

- Runs 37070771201 (pull_request) and 37070750896 (push).
- `docs-gates` and `portability`: success.
- `suites`: the lint+suites, SRP, MAAP and ADP campaign steps have completed with success, in 31.8, 3.6 and 7.6 min for the three campaigns. The same three took 42.3, 5.3 and 9.2 min serially at `631eeb34`.
- The AECP deadline step was in progress and the AECP dispatch step pending at 23:11 UTC.

### Equivalence runs (Verilator 5.050, pinned to CPU sets, private copies under a scratch TMPDIR)

| Driver | Units | `--jobs 1` (CPUs) | `--jobs 8` (CPUs) | Summary | Receipts (FAIL and tally lines) | FAIL lines | Against the README |
|---|---|---|---|---|---|---:|---|
| retry | baseline, 70 cases, restored | 645 s (4) | 569 s (4) | 71 lines, identical | 73/73 identical, `coverage.txt` included | 2,640 | 62/62 KILLED counts equal; 7 equivalence and 1 performance controls; 1342 checks baseline and restored |
| srp_admission | 4 variants x 3 suites | 908 s (4) | 322 s (4) | 13 lines, identical | 12/12 identical | 8,358 | all 9 mutant counts equal (402/5473/105, 175/1067/205, 146/695/90) |
| srp_top | 11 controls, 78 arm runs | 2,837 s (4) | 1,473 s (4) | 91 lines, identical | 84/84 identical | 687 | `90 checks: 90 PASS, 0 FAIL`, coverage 65/65 |
| maap | 3 controls, 29 arm runs | 328 s (4) | 175 s (4) | 101 lines, identical | 32/32 identical | 189 | 29/29 "N FAIL of M" equal by arm |
| adp | 2 controls, 30 arms | 473 s (4) | 638 s (2) | 211 lines, identical | 32/32 identical | 178 | 30/30 counts equal |
| gsi (subset) | golden, 4 variants, restored | 575 s (2) | 399 s (2) | 7 lines, identical; `results.json` identical | 13/13 identical | 4,288 | 4 detected by the named check |
| aecp_dispatch (subset: all 4 targets, 3 microcode arms) | 4 controls, 9 arms | 599 s (4) | 618 s (2) | 69 lines, identical; `results.json` identical | 14/14 identical | 55 | 9/9 counts equal |
| aecp (subset: all 5 suite targets, 2 microcode arms) | 5 controls, 13 arms | 477 s (4) | 662 s (2) | 195 lines, identical | 18/18 identical | 176 | 13/13 counts equal |

The host carried a load of 38 to 60 from other work, so these wall times measure equivalence, not speed. Some `--jobs 8` runs were pinned to 2 CPUs to stay inside the 12 GiB cap. The author's equivalence table (all eight drivers in full at `85da751`) agrees with these results wherever they overlap: the same FAIL-line totals 2,640, 178, 189, 8,358 and 687.

## Lens detail

- **Conformance:** All six acceptance items and the out-of-scope rule are met (table above).
  - The PR body's 18 `path:line` references resolve at the head (`receipts/pr_body_line_refs.txt`).
  - The body's description of each driver matches the code.
  - The STOP conditions of the assignment (an RTL, test-arm or count change, or a parent-visible change) are not met: no `hdl/` change, and no driver's DUT-source-reader status changed. Retry, gsi and srp_admission still read `hdl/` paths; the helper names none.
- **RTL:** No RTL, microcode, generator or bench source changed (empty diff). All mutation patches are unchanged and touch `hdl/` only. At the head, every exercised campaign kills each arm by its named check, at its README count.
- **Robustness:** `in_order` was probed directly (`receipts/pool_probe.txt`):
  - It returns results in declared order at any N, including N of 0 or less.
  - A unit's exception is raised at its turn: 2 results before it, 5 of 12 units started.
  - Leaving the block early cancels the unstarted units (3 of 29 started), and no worker thread survives.
  - The ordering, cancellation and gating checks in the drivers:

    | Driver behaviour | Checked by |
    |---|---|
    | A control that fails returns inside the block, so the pool cancels the rest (dispatch, aecp, adp, srp_top) | reading |
    | The golden or baseline still runs first and alone (retry, gsi) | reading and runs |
    | gsi's affinity cap is set before the pool threads exist, so they inherit it | reading |
    | Every temporary copy is removed | the empty TMPDIR after the runs |
    | No OOM kill across 21 runs | `memory.events` |

  - The memory scaling is recorded as S1.
- **Tests:**
  - Equivalence of j1 and j8 was shown for 5 drivers in full and 3 in subset.
  - `--only` was tested on all 8 drivers, including the selection by gsi and srp_admission and their rejection of unknown names.
  - Counts were compared with the READMEs: retry, srp_admission, srp_top summary, maap, adp, and the dispatch and aecp subsets.
  - The pool helper was probed directly.
- **Docs:**
  - All six READMEs state `--jobs N`, its default and meaning, and both wall times, and the merge preserved both sides.
  - One wording inaccuracy is recorded as RESIDUE F1.
  - The new docstrings in all eight drivers accurately describe private copies and declared order.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #143 body and acceptance 1-6; assignment comment; PR body (18 line references); AST tables and functions at `631eeb34`, `88969246` and the head; recomputed merge tree | R440-1 | 7d9fabf13ea3ef08d7d204c0297820561054b04a |
| RTL | CLEAN | `git diff 88969246..HEAD` over `hdl/`, every `mutations/` and `aecp_dispatch_mutations/`, tb sources and Makefiles (empty); the patch target set (`hdl/` only); the ROM generators' write paths; campaign kills at the head | R440-1 | 7d9fabf13ea3ef08d7d204c0297820561054b04a |
| Robustness | CLEAN (S1 is a suggestion) | `tb/common/mutant_pool.py`; the 8 workers and consumers; the pool probe; log-name collisions; live copy watching (518 copies, up to 8 at once per driver); `memory.events` (0 OOM kills); the clone's state before and after | R440-1 | 7d9fabf13ea3ef08d7d204c0297820561054b04a |
| Tests | CLEAN | 21 campaign runs, all rc 0 (16 j1/j8 runs, 5 `--only` smoke runs), 2 rejection checks for unknown names, and comparisons with the README counts | R440-1 | 7d9fabf13ea3ef08d7d204c0297820561054b04a |
| Docs | CLEAN (F1 is RESIDUE) | the 6 changed READMEs and the order of their tables; the 8 driver docstrings; the merged `tb/pp_top/README.md` | R440-1 | 7d9fabf13ea3ef08d7d204c0297820561054b04a |

## Real limits

- aecp, aecp_dispatch and gsi ran as declared subsets at `--jobs 1` and `--jobs 8`, not in full. They cover all their make or suite targets and include microcode arms. The full j1/j8 runs of these three are the author's, at `85da751`, whose driver code equals the head's. The full campaigns at the head are covered by the manager's banks and by the hosted `suites` job (aecp and dispatch were still running when this report was written).
- Wall times were taken on a shared host at a load of 38 to 60. They do not reproduce the README's figures and were not meant to.
- The parent consumer set (16), the donor bank (9), the full processor suite bank, the Yosys and builder banks, and act/Docker were not run (not allowed).
- The parent idiom and evidence predicates were not run by this review.
- Hosted CI was read only; its `suites` job was not complete at 23:11 UTC.
- No physical calibration or hardware. Field skips are not hardware proof.
- This repository has no submodule gitlinks (`git ls-files -s` has no 160000 entries). After the probes the clone is at the exact head:
  - the index tree equals `739f75ea…`;
  - all 479 tracked blobs hash-equal the index;
  - the 14 executable modes match;
  - the work tree is clean, with no untracked or ignored files (`receipts/restore_verify.txt`).

## Pending manager duties

- Confirm that the exact-head hosted `suites` job finishes green, including the `AECP deadline` and `AECP dispatch` campaign steps, on runs 37070771201 and 37070750896.
- Run the donor bank (9) and the parent consumer set (16) at this head, with `parent-adoption-c4c6-ea3fb388.patch`.
- Carry RESIDUE R440-1-F1 to the residue checklist.
- Build the final current-dev candidate at the merge turn: source base `88969246`, live dev `cdf49d1a`.

## Packet

- Scripts: `scripts/`
  - `env.sh`, `run_one.sh`, `monitor.sh`, `wait_rc.sh`
  - `compare_runs.sh`
  - `ast_tables.py`, `ast_functions.py`
  - `log_names.py`, `table_order.py`, `pool_probe.py`
  - the `*_vs_readme.py` comparators
- Receipts: `receipts/`, holding the summaries, run metadata and comparison outputs.
- Raw per-unit build and simulation logs stay unpublished because they carry local toolchain paths. Each is listed by digest in `receipts/raw_receipts.sha256`.
- Published files are listed in `MANIFEST.sha256`.

R440-1 FINISHED
