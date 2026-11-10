# HANDOFF — #823 round 6 (format only), [A753f]

Status: DONE. REVIEW READY posted on #823 as issuecomment-6778926856 (21:5x CET), head
`2905c8749a4573450b9999dd546bb20ae5c7fc38` (not pushed). Text: `REVIEW-READY.md`; PR body: `PR-BODY.md`.

- Lane: `$LANES/823-format`, branch `823-format`, started at `30ca4b21` (round 4).
- Base: `origin/dev-soft-core` `1d6bf555` (merge base; verified 13:33 CET).
- TAKEN: issue #823 issuecomment-6767475589 (13:3x CET).
- Not touched: branch `823-nvm-format` (#876, PR #863, head `7c97e99f`) and its checkout (read only: `git diff`/`git show`).
- Scratch: `/data-2/milan/tmp/823-a753f`.

## Commits (30ca4b21..2905c874), all one-line, no trailers

| Commit | Items |
|---|---|
| `249cca50` | N1 (SPLIT_CONTROL_MEMORY: 3,344 against 13,264, KLJ2 stage sizes of the `c20ed894` run), N2 (QSPI_FLASHBOOT: owners as FASTCONNECT section 5), RS5, RS6 (FASTCONNECT contents entry and status row) |
| `8e29bc74` | page: section 4 designed here and built under #876 (status line, contents, section 4 lead, sections 3, 7, 9, test-plan state cells via the generator); R806-5 R2 (room taken from the all-fabric 404.71 ms, conservative for the split); #818 waiver sentence in section 7 |
| `64c3565e` | RS-a (nvm_klj2.c, nvm_klj2.h, nvm_shape.h headers), RS-b (six places in test_nvm_write.cpp), RS-d (nvm_rig.hpp, nvm_suite.hpp) |
| `4d0353e3` | S-a: `LINE_CITE_RE` refuses `path:N`, a range, a list, unquoted, "`path` line N", `#LN`; six plants |
| `0d9e9b50` | S-b: codec compiles at 255 input entries (`at_width`), control `mapin_limit_one_early`; S-c: `#error` for `NVM_DOCTORED_MAPIN` without `NVM_HOST_TEST` (defined only by `nvm_bench.build_suite`), check `doctored_outside`, control `doctored_error_removed`; T17 row; README |
| `e0adcc09` | RS-a's other comment instances ("the F1 store" in nvm_layout3.h, nvm_layout3.py, nvm_klj3.py, check_nvm_klj3.py, endstation_builder.py, test_builder.py), block line counts kept where other docs cite line numbers |
| `2905c874` | fix after the first gate pass: the S-a list-form plant cited `sw/firmware/ctrl_nvm/nvm_store.c`, which contains the boundary's builder name `sw/firmware/ctrl`, so `firmware-boundary` (ctrl_boundary) refused the drift gate as an unregistered program naming the firmware's tree (log kept: `first-attempt/`); the plant now cites `scripts/nvm_klj3.py:408,465` |

Not re-authored as part of this round (save path, #876): the append-path text of FASTCONNECT section 5, the
MATERIALIZATION DR2a supersession note, SPLIT_CONTROL_MEMORY's append-path table, the store-constants drift check.

## Quick checks on the working tree before the gate pass (not receipts)
- drift gate 0 findings, self-test PASS (incl. 6 line-number plants); 1x1 store suite rc 0 (112 tests, at width and
  doctored-outside lines present); controls run alone: all 5 caught; check_nvm_klj3 + self-test rc 0; gate 39 rc 0;
  py/cpp idiom, hygiene, em dash, doc paths, gen_toc check/anchors, docs_check rc 0. Label scan of the delta: none.

## Gate pass on e0adcc090b0c636044fa953901009c301ba6d080 (from 13:58)
- Drivers (in my unit, niced, `taskset` 16 CPUs each so `nproc` = 16): A firmware jobs (96-111), B docs + small
  rtl-fast (112-127). C (elaborate + rtl) and the extras follow. Root `gates/final`, logs `drive-*.log`.
- Sweep: `tools/sweep_waiter.py` books one `cpu_ranges.py pick` range per shard with holder units
  `milan-823-a753f-hold<k>`, then `native-shards.py 823-a753f-sweep` (shard 2 = capture_coherence on 4 CPUs).
- #818 waiver evidence: `tools/elab_soc.sh` elaborates ax7101 1x1 and arty shipping SoCs (no vendor run) at
  `1d6bf555` and head, out `elab/`, compare `gateware.sha256`.

## Open
- Hosted CI has not run (not pushed); all evidence is local. The manager opens the PR to `dev-soft-core`.
- Generated SoC RTL compared for the AX7101 shipping SoC only: the Arty launch line fails identically at both commits in
  the LiteX environment (PLL); the split SoC needs a firmware image (memory table is its evidence, as ruled).
- Found, not changed: `nvm_bench.py` `Bench` docstring says "how nvm_klj2.py packs them"; `make_bench` uses nvm_klj3.py.
- PR-BODY uses "Closes #823" (round 6 instruction) rather than the generic "Relates to"; it relates #876 and #877.

## First pass on e0adcc09 (13:58-15:30), superseded where its tree changed
- Failures, both kept in `first-attempt/` (copied before any re-run):
  - `rtl-fast.firmware-boundary__ci_step_9` rc 2: REFUSED, `scripts/check_nvm_format_32x32.py names the firmware's
    tree and is a program ...` (cause: the S-a plant string). Fixed by `2905c874`.
  - `elaborate.elaborate-gates-1__gate_15_1` rc 1: `test_nvm_firmware.py --self-test` timed out after 1200 s inside
    builder leg 1 (host load 145-165, my four jobs overlapping on 32 CPUs). Contention, not a tree finding; re-run at
    the final head as part of `elaborate-gates-1`.
- Passed at e0adcc09 and carried to 2905c874 (they read no file e0adcc09..2905c874 changes, which is only
  `scripts/check_nvm_format_32x32.py`): `rtl-fast firmware-unit`, `elaborate elaborate-gates-0`, extra
  `ctrl_nvm_selftest` (running), the base/head SoC elaboration (head re-elaborated at 2905c874 too).
- Driver A died at 15:24:44 inside `firmware-verilator` ci_step_14 (no OOM event; cause not in any log); drivers B and
  C were stopped at 15:3x by process group when the head moved. Their partial logs stay in `gates/final`, not counted.
- Drivers at 2905c874 from 15:30: `r6-a.txt` (boundary, verilator, three mutant campaigns), `r6-b.txt` (docs, small
  rtl-fast), `r6-c.txt` (rtl, elaborate, elaborate-gates-1 last); root `gates/final2`. Sweep spec head -> 2905c874;
  16:08 the waiter held 40-47, 0-7, 24-31, 16-23 and native-shards started units milan-823-a753f-sweep-shard0..3 on
  40-47, 0-7, 24-27 (shard 2, capture_coherence), 16-23 (rc 0; MemAvailable 58.8 GB); holders stopped 16:08:51. Extras at 2905c874: drift_gate_final rc 0, diff_check_final rc 0.

## Host restart (about 18:00), resumed 18:05
- Finished at 2905c874 before the restart (root `gates/final2`, each `__DONE` "failed 0"): docs wire-accountability,
  docs-check-no-git, docs-gates-0; rtl full-ci-gate, yosys-tool, yosys-shards 0/4, 1/4, 2/4.
- Killed by the restart, kept and not counted: firmware-boundary (ci_step_9), docs-gates-1, yosys-shards 3/4 (partial
  logs in `gates/final2`); the sweep in `sweep/` (8, 12, 5, 11 suite logs per shard, no summary); the e0adcc09 store
  self-test (`extra.ctrl_nvm_selftest.log`, header only: its output was block-buffered).
- 18:06 sweep relaunched at 2905c874 into `sweep2/` (waiter log `sweep2_waiter.log`): shards on 40-47, 8-15, 24-27
  (shard 2, capture_coherence), 16-23, rc 0, MemAvailable 64.3 GB.
- 18:07 drivers at 2905c874 in a fresh root `gates/final3`: `r7-a.txt` (boundary, verilator, three mutant campaigns),
  `r7-b.txt` (docs-gates-1, docs-gates-2, docs-check, small rtl-fast), `r7-c.txt` (yosys-shards 3/4, portability,
  elaborate, elaborate-gates-1). Store self-test at 2905c874 as extra `ctrl_nvm_selftest_final`, unbuffered, so the
  e0adcc09 one is no longer carried. Carried from e0adcc09: firmware-unit and elaborate-gates-0 only.
- 18:54 `elaborate-gates-1` gate_15_1 rc 1 again: `test_soc_options.py` timed out after 300 s at host load about 250
  (log kept: `restart-attempt/`). Driver C stopped (its gate_19 partial, not counted). The builder union needs both
  elaborate legs at one head and tree (`ci_builder_legs.py union`), so `elaborate-gates-0` runs at 2905c874 too and
  is no longer carried; only `rtl-fast firmware-unit` is carried from e0adcc09.
- 19:03 both elaborate gate jobs run as gate unit `milan-823-a753f-elab` on booked range 64-71 (cpu_ranges pick),
  MemoryMax 10G, not niced, root `gates/final4`, list `r8-c.txt`, log `drive4-c.log`.
- Sweep at 2905c874 (`sweep2/`): shards 0, 1 and 3 exit 0 (shard 3 16/16, 21,575 checks). Shard 2 exit 1: 16 PASS, 0
  FAIL, capture_coherence TIMEOUT at its 2400 s on 4 CPUs (result unknown, not a failure), 284,186 checks, 0 in-suite
  failures. Re-run alone with `tools/rerun_suites.sh` (the sweep's own timeout and masked-verdict check) from shard 2's
  clone on 4 CPUs of a booked range, via `tools/rerun_waiter.sh` (unit milan-823-a753f-rerun, out `sweep2-rerun/`).
- elaborate-gates-1 at 2905c874 (`gates/final4`): every step rc 0; leg 1 "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11,
  no placed build tree); LiteX simulations 8 of 8 PASS.
- 20:1x CPUs 96-127 measured 100% busy with peer sessions at nice 0; my nice-10 drivers got about 15% of a CPU
  (renice to 0 refused: unprivileged). Lists `r7-a.txt`/`r7-b.txt` truncated in place so drivers A3 and B3 end after
  their running jobs (firmware-boundary, docs-gates-1). The rest moves to gate units on booked ranges, not niced, root
  `gates/final5`: `fwa` = `r9-a.txt` (firmware-verilator, control/aecp/srp mutants), `docb` = `r9-b.txt` (docs-gates-2,
  docs-check, small rtl-fast), each started by `tools/unit_waiter.sh` when `cpu_ranges.py pick` succeeds.
- 20:2x the bash waiters (`unit_waiter.sh`, `rerun_waiter.sh`) had died: since the restart a detached bash loop that
  calls `sleep` does not outlive the tool call that started it (probe: it died with the call). Python waiters survive.
  Relaunched as `tools/unit_waiter.py` for `fwa`, `docb` and `rerun` (capture_coherence, first 4 CPUs of its range).
  `pick` hands out nothing while a release hold collects CPUs (p0_acquiring), so these wait behind the release.
- Correction: the bash waiters had not died (my `ps` filter missed them), so at 20:41 a bash and a Python waiter raced
  for each unit; systemd refused each duplicate by unit name. Running: `fwa` and `docb` both on 8-15 (two waiters took
  the same pick in the same second), `rerun` (capture_coherence) alone on 88-91. No waiter left.
- docs-gates-1 at 2905c874 (`gates/final3`): failed 0; leg 0 "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 1b's MAKEFLAGS
  mutation, which this make does not honour).
- 20:42 firmware-boundary at 2905c874 (`gates/final3`): failed 0, `ctrl_boundary: PASS`.
- 21:1x builder unions at 2905c874 from the docs-gates-2 job's clean clone: docs (legs from final3 and final5) and
  elaborate (legs from final4), each `builder: 107 gates exactly once`, rc 0 (`gates/union`).
- 21:16 extra `ctrl_nvm_selftest_final` at 2905c874: rc 0, `OK across 5 shape(s), 506 tests, and all 132 planted
  defects reddened` (127 + 5 controls), tree clean. RV32 sizes equal round 4's (30ca4b21) at all 5 shapes, so the
  store's code is unchanged and the memory table at 30ca4b21 holds.

## Final (21:46-21:5x)
- All gate units ended; `tools/assemble6.sh` built `receipts/` (SUMMARY.md, INDEX.md of 645 files, host prefixes
  replaced, over-200 KB files in LARGE.tsv). `verify_final.py`: 152 steps ran (145 at 2905c874, 7 of firmware-unit
  carried from e0adcc09), 198 not run with a reason, 0 bad. Jobs and their roots: `receipts/gates/JOBS.tsv`.
- Sweep: 64 PASS in shards, capture_coherence PASS on its uncontended re-run (2262 s, 21,721 checks); 65/65.
- Sweep clone shard 3: tsn_fuzz rewrote the date line of two tracked TEST_RESULTS.md (by design); diff kept in
  `receipts/sweep/shard-3/tree-after.diff`, clone restored.
- Lane clean at 2905c874 (tracked and ignored: the session-made `__pycache__` and `sw/builder/out` removed).
  Scratch 19 GB. No unit of this round left running. Remote dev-soft-core still 1d6bf555; 823-nvm-format still 7c97e99f.
- No push, PR, merge, rebase, force or amend. Comments on #823: TAKEN and REVIEW READY only.
