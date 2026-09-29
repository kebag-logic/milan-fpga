[R394] POSITIVE - exact head 35f58b9cca1de9215f787872734e6a9040f82c19

# R394-4: internal review of PR #618 (#617), round 4

- **Head:** `35f58b9cca1de9215f787872734e6a9040f82c19`, tree `9c090dda1d69b1572a763a9fa7bf29218bfd5fdb`.
- **Delta reviewed:** `ddb07747..35f58b9c`, three commits, under the round-4 ruling (issue 617 comment 5881942681).
- **Whole lane:** `ce550952..35f58b9c`.
- **Verdict:** POSITIVE. There is no open BLOCKER, MAJOR or MINOR. Two SUGGESTIONs and one out-of-scope classification follow.
- **Lenses:** all five applied, each with its own evidence at this head.

## Summary

1. **Hosted, exact head, executed.** `rtl-full` run 36518018770, job 109244655191, `Verilator shard 1/5`, success.
   - The run is on the PR merge ref `76576f83` (parents `eaa88a32`, `35f58b9c`).
   - `capture_coherence` passes in **992.85 s** against the 1,800 s guard: a margin of 807 s, **44.8%**.
   - At `ddb07747` it took 1,441.84 s and failed.
   - The artifact `suite-logs-1` (11013615495) holds:
     - junction 20,832 / 0;
     - dp 332 / 0;
     - arm `29 builds on 4 worker(s)` and `30 checks: 30 PASS, 0 FAIL`.
   - Those 30 checks are the two build checks, the eight leg controls (dp and dp-band among them), and 20 mutants caught. The dp and dp-band mutants and RM9 are among them.
   - The other four shards pass as well, with every suite that ruling 1 of round 3 named.
2. **The nested-make fix holds, and both new checks can fail.**
   - Both `$(shell $(MAKE))` calls carry `--no-print-directory`. `build()` runs with `MAKEFLAGS=""` and keeps its output, and a failed build prints its last 40 lines.
   - My round-3 reproduction now builds under `''` and `'w'`, on GNU make 4.4.1 and on GNU make 4.3.
   - The make 4.3 chain (`make -C` -> recipe with `MAKEFLAGS=w` -> committed `build('dp')`) builds.
   - The inherited-`MAKEFLAGS=w` check fails with `--no-print-directory` removed from either call or from both.
   - The planted-break check fails when the build keeps no log, or when nothing is planted. It prints `%Error: .../milan_datapath.sv:<line>:15: syntax error`.
   - Each fix alone makes the dp build succeed. With both removed, it fails.
3. **Parallel arm.**
   - One worker per CPU in the process affinity. The datapath units start first.
   - `dp` and `dp-band` share one control build, and only they share: the recipe, source and override keys are identical.
   - The ROM images are made once, before the pool. Tags are unique (20 of 20 mutants). Each unit has its own staged source, object directory and log.
   - Recipes and harnesses write nothing into the suite directories except the ROM images made before the pool.
   - The verdict lines match line for line, in the same order:
     - 4 hosted workers against 8 local workers (make 4.3 chain, 30/30, 270.0 s);
     - 1 worker against 8 on an 8-unit subset.
   - Every mutant stays in the PR gate: 19 before, 20 now (RM9 added), none removed. `scripts/run_all_suites.sh` is untouched.
4. **RM9.** `mga_keepoff.py` refuses these bindings by name ("does not bind LOCK_KEEPOFF_CYC_P to MGA_KEEPOFF_CYC_C"), exit 1:
   - literal `128` or `256`;
   - the binding removed;
   - `MGA_KEEPOFF_CYC_C + 0`;
   - another constant.

   The head binding and a whitespace variant pass. In the arm, RM9 is caught only by that refusal.
5. **Documents.** Each is accurate against my round-3 measurements and the hosted record:
   - the below-nominal wording (a sharp limit near +67 ppm, a gradual stretch below);
   - the CRF-settle restatement (it grades the approach; the converged lock is cited as RECORDED);
   - `TRIMW_P = 18` beside the NCO area in the PR body (101->106 / 46 / 35->37 at 50 MHz, and 103->104 / 47 / 35->37 at 100 MHz, the same as my round-3 OOC receipt);
   - the absolute-`MDIR` run targets (media_nco 410/410 through an absolute `MDIR`).
6. **No RTL logic change.** Both touched RTL files preprocess to identical token streams (comments stripped). A planted one-digit change is detected. No gitlink moved.

## Findings

None at BLOCKER, MAJOR or MINOR.

```text
[R394] SUGGESTION Robustness, Docs — tb/verilator/capture_coherence/mutants.py:306-314 (stop), :552-574 (run_units), :76-86 (docstring) — the kill handler is re-entered by make's forwarded SIGTERM
Requirement/evidence: The docstring says the guard's kill "kills each one's process group, starts nothing more and removes the temporary directory".
  Under the sweep's own chain (`timeout T make -C <suite>`), timeout(1) signals its process group, and GNU make also forwards SIGTERM to its recipe child, so the driver takes SIGTERM twice.
  The second one re-enters stop(), whose sys.exit aborts pool.shutdown()'s join. The TemporaryDirectory cleanup then races live worker threads.
  receipts/arm-run-B-make43-4cpu.log (make 4.3) and receipts/arm-killpath.txt (make 4.4.1) show two SystemExit 143s, then "OSError: [Errno 39] Directory not empty". A 12-16 KB directory of build logs stays in TMPDIR, and the recipe exits 1, not 143.
  A third kill (make 4.3, 150 s) exited cleanly. The race depends on timing.
Impact: Cosmetic in effect.
  No process survived any kill (checked each time), and the sweep's verdict comes from timeout's status (TIMEOUT, UNKNOWN), so no gate result changes.
  The residue is a few KB per guard kill, plus the cc*.s temporaries any SIGKILLed g++ leaves. The docstring promises more than the code guarantees.
Required change (optional): Make stop() idempotent, for example by ignoring further SIGTERM/SIGINT once STOPPING is set, or by removing the directory tolerantly after the join. Or narrow the docstring.
Verification: scripts/r394_killpath.sh, repeated kills: one SystemExit, no traceback, no directory left.
```

```text
[R394] SUGGESTION Tests — tb/verilator/capture_coherence/mutants.py:443-473 (grade_mutant, clean_control) and every leg's Verilator `--build -j 0` — dead helpers and nested oversubscription
Requirement/evidence: grade_mutant() and clean_control() are no longer called by the driver: main() runs arm_units()/run_units(). Only an importing probe reaches them.
  Each parallel unit's Verilator build still uses `-j 0` (the capture_coherence, chmap_capture and media_nco VFLAGS, and milan_dp's print-dp-vflags), so N workers each start about N compiler jobs.
  It passed hosted (4x4) and locally (8 workers), so this is a note, not a defect.
Impact: Unused code can drift from the driver it once was. The oversubscription is harmless at 4 CPUs, but it grows with the square of the CPU count on a large workstation.
Required change (optional): Delete or re-route the two helpers. Consider passing the build a bounded -j.
Verification: grep; the arm's tally is unchanged.
```

### Classification of the flagged nested-make pattern (pp_shadow, milan_dp_render)

**Out of scope for this PR, and a follow-up Issue for the manager to file. It is not a finding here.** Neither file is in the lane's diff, and #617 does not cover them.

- **Safe where the sweep runs it.** The author's claim holds for both suites' default targets.
  - Their nested lists are parsed by the top-level `make -C <suite>`, and they come out clean under make 4.3 (`receipts/nested-make-pp_shadow-milan_dp_render.txt`).
  - `milan_dp_render`'s default recipe runs `tdm8_render_mutants.py --leg-defects` against binaries already on disk, with no rebuild.
  - Both suites pass hosted at this head: shard 1 `pp_shadow`, shard 0 `milan_dp_render`.
- **Not safe in two explicit campaigns.**
  - The two campaigns, invoked as `docs/testing/TESTING.md:268,270` documents them:
    - `make -C tb/verilator/pp_shadow pending-mutant`;
    - `make -C tb/verilator/milan_dp_render tdm8render-mutants`.
  - Each recipe's driver starts a nested make: `pending_mutant.py` runs `make run-pending`, and `tdm8_render_mutants.build()` runs `make -s -C HERE ...`.
  - Under GNU make 4.3, that nested make inherits `MAKEFLAGS=w`. Its `$(shell $(MAKE) -s -C ../milan_dp print-srcs)` then starts with `make[1]: Entering directory`. This is the same false-red class as R394-3 F1.
  - These are false reds in reviewer-run campaigns outside the PR gate.
  - The same fix applies: `--no-print-directory` on the nested calls, or an emptied `MAKEFLAGS` in the drivers.

## Lens results at this head

```text
[R394] PASS Conformance — hosted rtl-full 36518018770 job 109244655191 + artifact suite-logs-1 (receipts/hosted-shard1-capture-coherence.txt, hosted-capture_coherence-35f58b9c.log); receipts/hosted-other-shards.txt; ruling 5881942681 items 1-3 — acceptance 1-3 unchanged and still met: junction 20,832/0, dp 332/0, arm 30/30; every NCO/capture suite green on all five shards. Ruling 1: both --no-print-directory, emptied MAKEFLAGS, build tail, R394-3 repro builds, planted break prints %Error. Ruling 2: every mutant kept, no quick/full split, run_all_suites.sh untouched, hosted 992.85 s <= 1,500 s target, 44.8% margin. Ruling 3: RM9, S3 wording, S2/S4 settle, TRIMW_P, absolute MDIR.
[R394] PASS RTL — hdl/ieee1722/aaf/KL_chan_map_capture.sv, hdl/milan/milan_datapath.sv @ddb07747..35f58b9c (receipts/rtl-comment-only.txt) — both preprocess to identical token streams, and a planted 256->255 is detected; no other hdl/ file and no gitlink changed; the reworded comments match the measured envelope (sharp above +67, stretch below, converging ±100 / converged ±150).
[R394] PASS Robustness — mutants.py build()/run_child()/run_units()/control_groups(), tb/verilator/capture_coherence/Makefile:95-106 (receipts/makeflags-*.txt, build-check-negative-probes.txt, arm-suite-dir-writes.txt, arm-killpath.txt, arm-run-B-make43-4cpu.log) — builds are immune to inherited MAKEFLAGS on make 4.3 and 4.4.1; each fix alone suffices; unique tags, per-unit dirs and logs, no suite-dir writes during the pool; the guard kill leaves no process and still reads TIMEOUT (kill-path residue is S1).
[R394] PASS Tests — mutants.py makeflags_result/build_break_result/refusal_result, MUTATIONS (19 -> 20) (receipts/build-check-negative-probes.txt, rm9-mga-keepoff.txt, arm-G1/G2/G3 logs, arm-run-C-make43-8cpu.log, arm-determinism.txt, arm-subset-jobs1/8.log) — both new checks go red when their property is removed; RM9 caught only by name; 30/30 locally through the committed scheduler; verdict lines identical in fixed order across 1/4/8 workers; no mutant removed or weakened.
[R394] PASS Docs — docs/design/TIME_SYNC.md:470,548-559,570; docs/reference/REGISTER_MAP.md:1951-1969; docs/testing/TESTING.md:490; CHANGELOG.md:50-65; coherence_bench.hpp:73-87; sim_main.cpp:70-83; mutants.py docstring; the three Makefile run targets; the PR body at 35f58b9c (lines 182-184, 203-212, 323-326) — the below-nominal figures (426/615/945/1,323/about 1,700 at -63..-67) and the +66/+68 statements match my round-3 receipts; no "63/67" limit remains in the tree; the TRIMW_P = 18 area matches round-3 receipts (ooc-nco-summary.txt); 20 mutants and two build checks as counted. (The kill-path docstring overstatement is S1.)
```

## Ledger (reviewer-owned)

| Lens | Result | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | hosted shard 1/5 job 109244655191 + suite-logs-1; shards 0, 2, 3 and 4 verdicts; ruling 5881942681; issue acceptance 1-3 | R394-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| RTL | CLEAN | `KL_chan_map_capture.sv`, `milan_datapath.sv` delta (preprocessed token comparison); gitlinks | R394-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| Robustness | CLEAN (S1 open as SUGGESTION) | `mutants.py` build and kill paths; `capture_coherence/Makefile` nested calls; make 4.3 and 4.4.1 chains; kill probes | R394-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| Tests | CLEAN (S2 open as SUGGESTION) | the two new build checks with fault injection; RM9 refusal; committed arm 30/30 locally and hosted; determinism across worker counts | R394-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| Docs | CLEAN | `TIME_SYNC.md`, `REGISTER_MAP.md`, `TESTING.md`, `CHANGELOG.md`, harness headers, Makefile headers, PR body | R394-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |

Earlier rounds covered the unchanged RTL behaviour (R394-3 at `ddb07747`). Round 4 changes RTL comments only, which R394-4 re-covers above. Every lens is banked at the exact head.

## Prior findings at this head

I read these only after the verdict and ledger above were written. Each is re-checked at `35f58b9c`.

| Prior item | Status at this head | Evidence |
|---|---|---|
| R394-3 F1 (MAJOR) = R395-3 F1 (BLOCKER): the dp and dp-band legs never built on the hosted runner; the suite's time against its guard | **RESOLVED** | Hosted shard 1/5 at this head: dp and dp-band controls and mutants built and caught; arm 30/30; 992.85 s, 44.8% margin. Locally: repro and make 4.3 chain build; both new checks red under fault injection. |
| R394-3 S1: RM9, binding-level keep-off | **TAKEN** | `mga_keepoff.py` refusal; RM9 in the arm, caught by name, hosted and local (`rm9-mga-keepoff.txt`). |
| R394-3 S2 = R395-3 S4: CRF-settle grades a converging lock | **TAKEN (citation route)** | Headers, TIME_SYNC, REGISTER_MAP and CHANGELOG say "approach" / "converging", and cite the converged lock as RECORDED 150,000-column runs. My round-3 ±100/±150 150k receipts agree (255-256 off, spread ≤3). |
| R394-3 S3 = R395-3 S1: the below-nominal limit | **TAKEN** | "Gradual stretch below, sharp about +67 above", everywhere; no "63/67" limit remains. My -63..-67 columns match. The other review's +67 figure (a dwell to column 1,143 rather than a carry-across) sits inside the word "about". |
| R394-3 S4: headroom against the guard | **TAKEN** | 44.8% margin measured hosted; no quick/full split. |
| R395-3 S2: name `TRIMW_P = 18` with the NCO area | **TAKEN** | PR body lines 182-184; the figures match my round-3 OOC at `TRIMW_P=18`. |
| R395-3 S3: absolute `MDIR` in `media_nco` `make run` | **TAKEN** | Also in `chmap_capture` and `capture_coherence`; media_nco 410/410 through an absolute `MDIR` (`absolute-mdir.txt`). |
| Rounds 1-2 (R394-1 F1; R395-1 F1-F3; R394-2 F1-F2; R395-2 F1-F3) and their taken suggestions | **REMAIN RESOLVED** | Round 4 touches no RTL logic and no harness grading. Their guards stay killed in the arm at this head: band and dp-band binding mutants, RM1-class `[F1]`, the NCO `==` restore (nco and fine), RM5, RM7 and RM8. |

## Reproduction and evidence

Tools:

- Verilator 5.050. The assigned path under `372-manager-candidate1` does not exist; I used the `372-manager-r2` wrapper. Its sha256 `905795b9...` matches my round-3 record and the `617-manager-r4` wrapper.
- GNU make 4.4.1 (host), and GNU make 4.3 built in scratch from the GNU release tarball (sha256 `e05fdde4...`).
- Python 3.14.7.

Details are in `receipts/tool-identity.txt`. Every probe ran on a `git archive` of this head with its three submodules, under `scratch/`. Nothing was built in the clone.

| Check | Result | Receipt |
|---|---|---|
| Hosted shard 1/5 timing and arm | 992.85 s, 44.8% margin; 30/30; before: 1,441.84 s FAIL | `hosted-shard1-capture-coherence.txt`, `hosted-capture_coherence-35f58b9c.log` |
| Hosted other shards | 13 affected suites PASS | `hosted-other-shards.txt` |
| R394-3 repro, make 4.4.1 | `''` and `'w'` both build, clean `DP_SRCS` | `makeflags-dp-build-repro-make441.txt` |
| make 4.3 chain + repro | recipe `MAKEFLAGS='w'`; `build('dp')` builds; `[PASS]` makeflags check | `makeflags-chain-make43.txt` |
| Build-check fault injection | 8 probes as expected | `build-check-negative-probes.txt` |
| RM9 and variants | 5 refused by name, 2 accepted | `rm9-mga-keepoff.txt` |
| Committed arm, whole, make 4.3 `-C`, 8 workers | 30/30, 270.0 s (host load 44-58 on 16 CPUs) | `arm-run-C-make43-8cpu.log` |
| Committed arm by unit groups | 6 + 15 + 9 = 30 PASS | `arm-G1-datapath.log`, `arm-G2-junction-chmap-nco.log`, `arm-G3-band-band50-fine.log`, `arm-unit-list.txt` |
| Determinism | hosted (4) = local (8); subset 1 = 8 workers | `arm-determinism.txt`, `arm-subset-jobs1.log`, `arm-subset-jobs8.log` |
| Suite-dir writes | ROM images only | `arm-suite-dir-writes.txt` |
| Kill path | double SIGTERM, residue, no survivors | `arm-run-B-make43-4cpu.log`, `arm-killpath.txt` |
| Nested make elsewhere | explicit campaigns polluted under 4.3; top level clean | `nested-make-pp_shadow-milan_dp_render.txt` |
| Absolute MDIR | resolves; media_nco 410/410 | `absolute-mdir.txt` |
| RTL comment-only | identical token streams | `rtl-comment-only.txt` |
| Clone integrity | 953 blobs and modes match the index; gitlinks match; clean | `r394-clone-integrity.txt` |

Scripts are in `scripts/`: `env.sh`, `r394_mf_repro.py` (round-3, unchanged), `r394_chain.py`/`.sh`, `r394_neg.py`, `r394_arm_units.py`, `r394_arm_compare.py`, `r394_killpath.sh`, `r394_rtl_nocomment.sh` and `hosted_timing.py`.

## Limits

- **Hosted evidence is on the PR merge ref.** It ran on `76576f83` = `35f58b9c` merged into dev `eaa88a32`, not on the source base `ce550952` or the current live dev `13eda870`. `eaa88a32` touches `milan_datapath.sv` and `tb/verilator/milan_dp/Makefile`. The arm's datapath patterns still matched there, and the planted-break line moved from 7824 to 7821.
- **My whole-arm run was not a clean timing sample.** It ran at a host load of about 45-60 on 16 CPUs, shared with other lanes. My 4-worker whole-arm attempt was cut at 590 s by my own per-command wrapper, so timing rests on the hosted record, not on my runs.
- **I did not run the whole `capture_coherence` suite locally in one command.** The junction and dp legs are unchanged except for comments. Their counts come from the hosted artifact.
- **Some below-nominal figures are not mine.** The -70 ppm figures (column 2,918, 6 cycles) and the ±80 ppm and 264-cycle converged-lock figures come from the other review and the author's recorded runs. My own receipts cover -63..-67, +66/+68 and ±100/±150.
- **Physical calibration NOT RUN.** Bench acceptance 4 is out of scope, and field skips are not hardware proof.

## Pending manager duties

- Candidate merge build against live dev `13eda870`, including re-matching the arm's datapath patterns there.
- The builder and native banks, and hosted/act acceptance.
- Decide whether S1 and S2 are taken, and file the follow-up Issue for the explicit `pending-mutant` / `tdm8render-mutants` campaigns under GNU make 4.3.

R394-4 FINISHED
