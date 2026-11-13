[R840] POSITIVE - exact head 860e47493ad5a92c4662fef601fd196b0143c4bb

# R840-1: external independent review of FPGA-gPTP PR #105 (issue #104)

- Exact head `860e47493ad5a92c4662fef601fd196b0143c4bb`, tree `4db845568b856f2f71bb624b508fa0d22e0bbc2c` (verified in the isolated clone).
- Range `a64be73de32f3ec5084cf908a530218e9006453e..860e474`: five commits, 6 files (`docs/TEST_DEVELOPER.md`, `tb/mutation_jobs_test.py`, `tb/mutation_order_test.py` (new), `tb/verilator/engine/Makefile`, `tb/verilator/engine/mutants.py`, `tb/verilator/engine/path_mutants.py` (new)). Nothing under `hdl/`, `syn/` or `bench/` changes, and no ROM file changes.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR is open. Three RESIDUE items (prose and PR-body wording only) and four SUGGESTIONs are recorded below. All five lenses are CLEAN.
- Prior public review findings on this PR: none. At review time the PR had two review-start notices, no review, no review comment and no reported check, so nothing needed resolving.

## How the review was done

I reconstructed the scope in this order:
1. The repository README, `docs/README.md` and the test guide. This repository has no AGENTS.md or CONTRIBUTING.md.
2. Issue #104's body, which holds the frozen acceptance items 1 to 5. Its only comments are the author's TAKEN and REVIEW READY notices.
3. The PR body.
4. The full raw diff and the history of the five commits.
5. The author's public evidence archive: milan-fpga `274bc30e` `review-evidence/gptp104-r1`, 46 files, hashes in `receipts/author-evidence-274bc30e.sha256`. I used the receipts and did not rely on the handoff narrative.

I then ran my own probes. All of them used the pinned Verilator 5.050 (wrapper sha256 `905795b9…`; the host default is 5.054, so it was not used), ccache 4.14.1, and ccache directories and TMPDIR under the packet scratch tree. The scripts are in `scripts/` and the receipts in `receipts/`.

## Acceptance check (issue #104 items 1 to 5)

| # | Requirement | Result | Evidence |
|---|---|---|---|
| 1 | Parent idiom gates pass at the new head, with no ratchet changed; `mutants.py` ≤ 1,000 lines; four public functions annotated and four documented | **Met** | I ran the parent's `check_py_idiom.py` and `check_cpp_idiom.py` on a fresh parent clone at live dev `b7d69295`. `protocol-processor` sat at its pin `801ef228` and the `gptp-processor` gitlink was moved to each commit, as the consumer gate requires. At `860e474`, Python rc 0 (`long module 10 <= 10`, `unannotated public function 0 <= 0`, `undocumented public function 0 <= 0`, over-long line 0) and C++ rc 0. At `a64be73d`, Python rc 1 on exactly those three ratchets (11 > 10, 4 > 0, 4 > 0), and `--list` names `mutants.py` (long module, 4 unannotated, 3 undocumented) and `mutation_jobs_test.py` (1 undocumented). The pin `1616fc8f` gives rc 0. The budget files are unchanged in all three runs. `mutants.py` is now 863 lines and `path_mutants.py` 279. Receipts: `receipts/parent-idiom/`. |
| 1 | Table moved verbatim, same 159 mutants in the same order | **Met** | `scripts/dump_mutations.py` imports each tree's arm and writes every `MUTATIONS` tuple as JSON. Both files are byte-identical: 159 tuples, sha256 `04780586…`, 89 generator-only and 70 RTL, names unique. The removed block (base lines 565 to 793) and its helpers (`PARSER_EDITS`, `PATH_*`, `tails`) also match `path_mutants.py` 50 to 278 as text. Receipts: `receipts/table/`. |
| 2 | ccache only when it is on PATH; one documented off switch; build paths kept out of the key; cache outside the tree | **Met** | `compiler_env()` (`tb/verilator/engine/mutants.py:597`) and `Makefile:30-33` checked by `receipts/ccache/ccache-probe.log` and `receipts/suite/`, summarised below this table. |
| 2 | Failure mode of an unwritable cache is documented | **Met** | The guide (`docs/TEST_DEVELOPER.md:76-78`) says "A ccache that cannot write its cache fails the build", and that matches what happens. A mode-555 or uncreatable `CCACHE_DIR` makes `build()` return None. The in-tree `make run` stops with rc 2 and `ccache: error: Failed to create directory …/lock: Permission denied`. The documented remedy, `OBJCACHE=`, builds. |
| 3 | Verdicts unchanged; output byte-identical with ccache off and on, cold and warm, at `--jobs 1` and `--jobs 8`; a test compares them | **Met** | Three sources, summarised below this table: the author's six-run receipt, my own full arm run at the head, and reduced-arm runs of the jobs test with planted defects. |
| 4 | `make all` measured before and after on the same 16 CPUs, with a cold and a warm cache | **Met**, stated as measured | Receipt figures: before `a64be73d` wall 2894.77 s (engine driver 2288.62 s); cold 2810.59 s (2226.96 s, ccache 212 hits / 76 misses); warm, clone at another path, 2797.06 s (2205.85 s, 287 / 1). All three ran on CPU affinity 48-63, one after another (16:27 → 17:15 → 18:02 → 18:49), and each rc 0. These match the PR table, including −2.9 % and −3.4 % and the h:mm:ss values. The cold row ran at `ad06db3`, not the head; see RESIDUE R840-1-R2. |
| 5 | #103 residue fixed; order check inside `make all` | **Met** | `docs/TEST_DEVELOPER.md:62` reads exactly "By default, up to eight engine mutants run at once." `Makefile:37` is `all: run mutants-order-test mutants`, and `make -n all` lists the order test between the suite and the arm. My order-test run passed 10/10 in about 2 s. |

**Item 2, ccache controls in detail.**
- With `OBJCACHE` unset, it becomes `ccache` when ccache is on PATH and empty when it is not. A command-line or environment `OBJCACHE=` stays empty, and a caller's own `OBJCACHE` or `CCACHE_NOHASHDIR` wins (`receipts/suite/makefile-vars.txt`, ccache probe steps 7 to 7c).
- With `OBJCACHE=`, the cache directory stays empty (probe step 6).
- **Mutant builds in new temporary directories:** after a cold build, the next two builds took 4/4 direct hits with 0 misses (steps 2 and 3). The generated model sources contain no work-directory path at the head.
- **The same probe at base `a64be73d`:** two model `.cpp` files contain the temporary path, and a warm rebuild misses on the model (step 10). This confirms the PR's explanation of why relative source names were needed.
- **A checkout at another path:** 1 miss (the harness `sim_main.cpp`, as the PR states) and 3 preprocessed hits (step 4).
- **In-tree suite:** a second exported tree at another path took 4/4 direct hits through `CCACHE_BASEDIR` (`receipts/suite/suite2-other-path.ccache-stats`).
- **Outside the tree:** suite runs add files only under the ignored `obj_dir`, `seedrun`, `syncseedrun` and `p1run` (`receipts/suite/*.added-dirs.txt`).

**Item 3, verdict and output evidence in detail.**
- **Author receipt** `eq/make.log` at `860e474`: 38 checks, 38 PASS. All six runs exit 0 and print 77458 bytes with sha256 `9fb353df…ccc74b2` and 160 verdicts. Cold runs: 284 compilations, 74 misses. Warm runs: 284 hits, 0 misses.
- **The same output at the base:** `before/engine-arm.stdout` from `make all` at `a64be73d` has the same sha256.
- **My own full arm run at the head** (`--jobs 8`, ccache on, empty cache): rc 0, stdout byte-identical to the base receipt (77458 bytes, the same sha256, `160 checks: 160 PASS, 0 FAIL`), empty stderr, ccache 210 hits and 74 misses (`receipts/fullarm/`).
- **Is the jobs test sensitive?** I ran the head's own `mutation_jobs_test.py` against a reduced copy of the arm: control, two RTL mutants and one generator-only mutant (`receipts/jobs-probe/`).
  - With no defect it passed 38/38.
  - With `build()` reverted to absolute staged paths it failed 36/38: both warm runs got "9 hits, 3 misses".
  - With `compiler_env()` forcing `OBJCACHE=ccache` it failed 36/38: both off runs reported "ccache wrote nothing (67/63 files)".
- **Is the order test sensitive?** Each of four planted ordering defects makes `mutation_order_test.py` exit 1 (`receipts/order-probe/SUMMARY.txt`): results yielded in completion order, lines printed on completion, one mutant dropped, and a shared run directory. The shared run directory is caught by a stub `KeyError` rather than by a named check.

## Lenses

**Conformance: CLEAN.**
- Every frozen item is met (table above). No mutant, check, verdict rule or tally is removed, merged or weakened: the tuples are identical, and the head arm reproduces main's 77458 bytes with 160/160.
- Comment rule (owner 2026-10-15): I scanned every added line in the range for bench lane labels, lane names, review rounds, reviewer IDs and issue-comment IDs. There are none. The new comments name only issue IDs (#102, #104, #85, #87, #88) and behaviour.
- The parent's consumer gate reproduces at the live dev tip (`b7d69295`), which is newer than the parent base in the author's receipt (352 against 353 C/C++ units). The result is the same: rc 0 at the head and rc 1 at the base.

**RTL: CLEAN.**
- No `hdl/` or `syn/` byte changes. Every mutant pattern still matches exactly once: the full head arm planted, built and graded all 159 with no "pattern appears" failure.
- `make lint` rc 0 with the pinned Verilator.
- The in-tree engine suite at the head passes `2098 checks: 2098 PASS` three times and `61 checks: 61 PASS` once, in both exported trees.
- Running Verilator from the staged directory with relative RTL names changes only the source names written into the model. It does not change elaboration: the output is byte-identical to the base.

**Robustness: CLEAN.**
- Off, absent-ccache, caller-override, unwritable-cache and moved-checkout behaviour were all probed; see the table and the item 2 detail.
- The jobs test drops every caller `CCACHE_*` and `OBJCACHE` variable for its runs, and gives each run its own cache directory under its own temporary root. Warm runs start from copies of a finished cold cache, with their counters zeroed.
- An unwritable cache fails loudly; it does not silently skip mutants. The control build fails first, so `mutants.py` prints "[FAIL] the unmutated sources did not build" and exits 1.
- SUGGESTIONs S1 to S3 below are improvements, not defects.

**Tests: CLEAN.**
- `mutants-order-test` (10 checks) runs in seconds inside `make all`. It checks list order, the tally, one run directory per entry, and that the entries really finished out of order. Four planted defects each fail it.
- `mutants-jobs-test` covers {jobs 1, jobs 8} × {off, cold, warm}. On a reduced arm it fails on both planted cache defects and passes clean. The author's receipt shows it passing 38/38 on the full arm at the head.

**Docs: CLEAN** (three RESIDUE items).
- The guide's entry table and its ccache, OBJCACHE, unwritable-cache, order-check and jobs-test sentences match the code and the probes.
- `make docs` rc 0: docs check PASS on 14 current and 18 historical pages, selftest 127 arms, source evidence 20 exact with 0 findings, its selftest 7 arms.
- `make diagrams-check` rc 0 (selftest 10 arms), `make contract` rc 0, OOC clock selftest 30 arms. These match the PR's gate list.

## Findings

### R840-1-R1: RESIDUE (Docs)
- **Where:** `docs/TEST_DEVELOPER.md:86` ("It takes about seven hours on sixteen CPUs.") and `tb/verilator/engine/Makefile:79-80` ("the test about seven hours on sixteen CPUs").
- **Evidence:** the only complete run at the head took 20909.9 s, which is 5 h 48 min (`eq/summary.json`, affinity 80-95). The earlier sentence at `ad06db3` said "about six hours". The PR body discloses both figures. The manager directed that this class be noted and not block.
- **Impact:** it is an operator's runtime estimate, not a measurement, verdict or test claim. It overstates the measured runtime by about 20 %.
- **Required outcome:** change both places to wording that matches the measurement. For example, in the guide: "It takes about six hours on sixteen CPUs." In the Makefile: "and the test about six hours on sixteen CPUs". Or give a range, such as "six to seven hours, depending on host load".
- **Verification:** read both lines against the 20909.9 s receipt.

### R840-1-R2: RESIDUE (Docs, PR text)
- **Where:** the PR #105 body, item 4's measurement table, row "after, cold cache".
- **Evidence:** `after-cold/summary.json` records head `ad06db3b508366c788c935abbb2c6ba4397c95e6`, not `860e474`. `git diff ad06db3 860e474` changes only one guide sentence and three Makefile comment lines. So the code that was measured is the head's code, and the figure stands.
- **Impact:** measurement provenance is incomplete in the PR text only. No figure changes.
- **Required outcome:** add to the table or its note: "The cold run was at `ad06db3`; `ad06db3..860e474` changes only the jobs-test runtime sentence in `docs/TEST_DEVELOPER.md` and a Makefile comment."
- **Verification:** the PR text names the cold run's commit.

### R840-1-R3: RESIDUE (Docs)
- **Where:** `docs/TEST_DEVELOPER.md:64` ("Its `--jobs` option sets that number.").
- **Evidence:** the required rewording of line 62 to "By default, up to eight engine mutants run at once." removed the singular noun "the engine arm" that "Its" referred to.
- **Impact:** the pronoun has no antecedent. This is prose only.
- **Required outcome:** "The engine arm's `--jobs` option sets that number."
- **Verification:** read lines 62 to 64.

### SUGGESTIONs (no lens impact)

- **S1 (Robustness):** `mutants.py`'s `compiler_env()` could also default `CCACHE_BASEDIR` to the repository root, as the Makefile does for `run`. The harness `sim_main.cpp` compile would then hit from a checkout at a new path too; today it costs one miss per new checkout path.
- **S2 (Tests, Robustness):** `mutation_jobs_test.run_env` removes the caller's `CCACHE_*` variables but not ccache's own configuration file. Pointing `CCACHE_CONFIGPATH` at an empty file for each run would stop a user's `ccache.conf` (for example `remote_storage` or `hash_dir`) from changing the hit and miss counts the test asserts.
- **S3 (Robustness):** when the control build fails, `mutants.py` prints only "did not build". Printing the last lines of the build's stderr would show the ccache "Failed to create directory" cause without a rerun.
- **S4 (Docs, Tests):** the guide could say that `mutants-jobs-test` needs ccache 4.x on PATH. Without ccache it FAILs by design, and `--print-stats` needs ccache 4.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #104 items 1-5; PR body; parent `check_py_idiom.py` and `check_cpp_idiom.py` at dev `b7d69295` against gptp `860e474`, `a64be73d` and `1616fc8f`; MUTATIONS JSON at base and head; textual block diff; comment-rule scan of all added lines | R840-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| RTL | CLEAN | Diffstat (no `hdl/`, `syn/` or `bench/` change); `make lint`; in-tree suite in two exported trees (2098×3 + 61 PASS); full arm, 159 patterns planted, 160/160 | R840-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| Robustness | CLEAN | `compiler_env`, `build()`, `Makefile:20-33`; ccache probe steps 1-10 (cold, warm, moved checkout, off, absent from PATH, caller override, mode-555, uncreatable, base comparison); in-tree suite with an unwritable cache; jobs-test environment isolation and scheduling | R840-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| Tests | CLEAN | `tb/mutation_order_test.py` (10/10 plus 4 planted defects, each rc 1); `tb/mutation_jobs_test.py` on a reduced arm (38/38 clean, 36/38 with abs-paths, 36/38 with objcache-on); author `eq/make.log` 38/38; my full arm output equal to the base receipt sha256 `9fb353df…` | R840-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| Docs | CLEAN (RESIDUE R1-R3) | `docs/TEST_DEVELOPER.md` (entry tables, lines 62-86); Makefile and module docstrings and comments; `make docs`, `make diagrams-check`, `make contract`, OOC selftest; `ad06db3..860e474` prose delta | R840-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |

## Real limits

- I did not rerun the six-run `mutants-jobs-test` on the full arm at the head; it takes about 6 hours. Its full-arm result comes from the author's receipt. I checked its logic independently on a reduced arm, with and without planted defects, and reproduced the arm's full output once at `--jobs 8` with a cold cache.
- I did not rerun the `make all` measurements. The figures above are read from the author's receipts and checked for arithmetic and internal consistency (start and end times, affinity, rc, ccache counters). My host was shared and heavily loaded (load average 28-43 on 32 CPUs; my full arm took 3578 s), so none of my wall times are comparable with the receipts.
- The parent idiom gate ran on live parent dev `b7d69295`, which is newer than the author's parent base. Both are rc 0 at the head.
- No hosted check is reported on the PR branch. I made no claim about hosted, act, builder or native banks, and none ran at this head on my side.
- Physical calibration NOT RUN. This change is test infrastructure only and makes no hardware claim.

## Pending manager duties

- Build and validate the current-dev merge candidate: source base `a64be73d`, live dev `b7d69295`, builder and native banks. Link those receipts on the PR at the merge turn.
- At adoption, rerun the parent's `check_py_idiom.py` and `check_cpp_idiom.py` with the gitlink at the merged commit.
- **Hosted, act and builder images that have ccache on PATH** now compile the engine builds through ccache. They therefore need a writable cache directory (default `~/.cache/ccache`, or `CCACHE_DIR`), or they must set `OBJCACHE=`. Otherwise `make all` fails by design. Confirm this in the hosted and act acceptance, which the manager owns.
- Carry RESIDUE R840-1-R1, R2 and R3 to the residue checklist.

R840-1 FINISHED
