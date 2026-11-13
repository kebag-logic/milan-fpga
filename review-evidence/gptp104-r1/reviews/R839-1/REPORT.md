[R839] POSITIVE - exact head 860e47493ad5a92c4662fef601fd196b0143c4bb

# R839-1: independent review of FPGA-gPTP PR #105 (issue #104)

- Repository: Mister-M-alt/FPGA-gPTP, PR #105, branch `104-ccache-idiom`
- Exact head reviewed: `860e47493ad5a92c4662fef601fd196b0143c4bb`, tree `4db845568b856f2f71bb624b508fa0d22e0bbc2c`
- Source base: `a64be73de32f3ec5084cf908a530218e9006453e` (main, #103 merged). Delta: five commits, 6 files, +687 -316.
- Reviewer: internal independent reviewer (R839), cleared context, own detached clone. Round R839-1.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open. Three RESIDUE items (pure wording in the guide, a Makefile comment and the PR body) go to the residue checklist. All five lenses are CLEAN.

## 1. What I reconstructed, in order

1. Repository rules: there is no `AGENTS.md` or `CONTRIBUTING.md` at this head. `docs/README.md` sets the truth order: RTL and microcode, then executable tests, then the current guides, then history. The comment rule (owner, 2026-10-15) and the RESIDUE rule (owner, 2026-10-02) come from the review brief.
2. Issue #104 body (frozen acceptance, items 1-5) and its comments: TAKEN and REVIEW READY only, with no scope change. The parent rulings it rests on are milan-fpga #883 issuecomment-6805166676, ruling (b): annotate four functions, document four, bring `mutants.py` to 1,000 lines or fewer, no ratchet raised. The #103 residue is milan-fpga #495 issuecomment-6777009988: the `:60` wording, and optionally a fast order check inside `make all`.
3. PR #105 body and comments: two review-start comments only. There are no prior review findings on the PR or on the issue, so none had to be resolved or kept.
4. `git diff a64be73d..860e4749`, each commit on its own, and `git diff ad06db3..860e474`. That last diff is one guide sentence and one Makefile comment, with no code.
5. The public evidence packet, milan-fpga `274bc30e`, `review-evidence/gptp104-r1` (author receipts, PR-BODY, HANDOFF), checked against the code and against my own runs.

## 2. Focus items, checked against code and receipts

| # | Claim | My evidence | Result |
|---|---|---|---|
| 1 | Parent `check_py_idiom.py` passes on the arm's files. The table moved verbatim. Same 159 mutants in the same order. | I ran the parent gate on a scratch clone of milan-fpga **live dev `b7d69295`**, the gate as `docs.yml` gate_38/39 runs it. `gptp-processor` was pinned at the head through a scratch-index gitlink, which `code_quality_scope.py` accepts. `git diff HEAD -- scripts/` was empty. At the head, `check_py_idiom.py` gave rc 0 (`long module 10 <= 10`, `unannotated public function 0 <= 0`, `undocumented public function 0 <= 0`), `check_cpp_idiom.py` rc 0, and both selftests passed (54/54 and 83/83). Same clone with `gptp-processor` at a64be73d: rc 1 on exactly `long module 11 > 10`, `unannotated 4 > 0`, `undocumented 4 > 0`. The parent's own `scan()` per file finds those 1+4+3 hits in main's `mutants.py` and 1 in `mutation_jobs_test.py`, and all four files clean at the head. `mutants.py` is 863 lines. I also dumped the generated `MUTATIONS` list at a64be73d, 60a2e3d and the head: 159 entries each, with byte-identical reprs (sha256 `967816bf…`). The moved table (old :565-793 to `path_mutants.py` :50-278) and its helpers (old :118-133 to :28-43) are byte-identical. | Met |
| 2 | ccache only when it is on PATH. `OBJCACHE=` turns it off. No absolute build path in the key. Cache outside the tree. The failure of an unwritable cache is documented. | I probed the **real** Makefile `run` recipe (a stand-in `$(VERILATOR)` that prints the environment), a plain recipe, and `compiler_env()`. ccache on PATH gives `OBJCACHE=ccache CCACHE_NOHASHDIR=1`, plus `CCACHE_BASEDIR=<checkout>` for `run` only. Without ccache on PATH it gives `OBJCACHE=` empty. `make OBJCACHE=` and `OBJCACHE=` in the environment both give empty. A caller's `CCACHE_BASEDIR=/x CCACHE_NOHASHDIR=0` is kept. With the arm's own `build()` and an empty cache: a rebuild from a new temporary directory got 4/4 direct hits; a copy of the checkout at another path got 3/4 (`sim_main.cpp` misses on its absolute path). No generated `.cpp` or `.h` names the work directory. Only Verilator's `.d` and `verFiles.dat` do, and those are not compiled. Same probe at main: the two model `.cpp` files embed the staged temporary path, and the model misses in a new directory, so the fix is both needed and effective. Suite build: built cold in one clone, then from a clone at another, deeper path, it got 4/4 direct hits (`CCACHE_BASEDIR`). With `CCACHE_DIR` unwritable (mode 555), `build()` returns no executable. ccache reports `Failed to create directory …/lock: Permission denied`, Verilator's make exits 2, and with `OBJCACHE=` the same build succeeds. That matches `docs/TEST_DEVELOPER.md:76-78`. Every clone was clean afterwards apart from pre-existing ignored outputs (`obj_dir/`, `*run/`, `__pycache__/`), and no ccache file landed in a tree. | Met |
| 3 | `mutants-jobs-test`: `--jobs 1` and `8`, each with ccache off, cold and warm. Byte-identical to main's output (77458 bytes). 38/38. | The published receipt `eq/make.log` was run at 860e474 on 16 CPUs, rc 0, 20909.9 s. Its six runs print 77458 bytes, sha256 `9fb353df…`, 160 verdicts. It reports 284 compilations, 74 cold misses and 284/0 warm. The result is 38 checks: 38 PASS. That sha equals the published main reference `before/engine-arm.stdout`. My own runs: the **full arm at main a64be73d**, uncached, `--jobs 8`, and the **full arm at the head**, ccache default (`OBJCACHE` unset, so it was discovered on PATH), empty cache, `--jobs 8`. Both gave rc 0, 77458 bytes, sha256 `9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2`, `cmp`-identical to each other and to the published reference, with empty stderr and `160 checks: 160 PASS, 0 FAIL`. The head run's cache: 210 direct hits and 74 misses = 284 compilations, the receipt's own numbers. Warm, build-only, every model the arm builds (71 = control + 70 RTL mutants), new temporary directories, a copy of that cache: from the cold run's checkout path, 284 hits and 0 misses (273 direct + 11 preprocessed, the receipt's own split). From another checkout path, 8 misses; a second pass there gave 0 misses, so the 8 were the harness unit compiled by the first 8 concurrent builds. Tests of the test: a three-entry fake driver passes 38/38. Output that differs at `--jobs 8` gives 6 FAIL. A driver that ignores `OBJCACHE` gives 4 cold/warm FAIL. A driver that ignores an empty `OBJCACHE` gives 2 off FAIL. | Met |
| 4 | Measurement table: 2894.8 s before, 2810.6 cold, 2797.1 warm, on 16 CPUs, from the receipts and stated as measured. | `before`, `after-cold` and `after-warm` `summary.json` and `walls.json`: affinity 48-63 (16 CPUs) in all three, rc 0. Wall times 2894.77 / 2810.59 / 2797.06 s. Engine driver 2288.62 / 2226.96 / 2205.85 s. ccache stats: before 0; cold `local_storage_hit 212`, `cache_miss 76`; warm `287` / `1`. -2.9 % and -3.4 % check out arithmetically. The PR presents the gain as small and simulation-bound, with parser-arm noise of about 20 s, which the receipts support. The cold run's commit is ad06db3, not the head. The table does not say so (RESIDUE F3). The code is identical, as checked above. | Met (F3 wording) |
| 5 | #103's residue at `docs/TEST_DEVELOPER.md:62`, and the order check `mutants-order-test` inside `make all`. | `:62` reads "By default, up to eight engine mutants run at once.", verbatim from the residue checklist. In the engine Makefile, `all: run mutants-order-test mutants` (:37). The top-level `tb` target runs the engine sub-make's default goal, and the published after-warm `make all` log shows the order test at 509-512 s, 10/10. I ran it at the head: 10/10 in about 2.5 s. Negative probes: making `in_list_order` yield in completion order gives 2 FAIL (list order, same bytes), rc 1. Dropping the last entry gives 4 FAIL (count, tally), rc 1. | Met |
| note | Runtime sentence "about seven hours" against the 5 h 48 min idle rerun | Recorded as RESIDUE F1, note only, as directed. | Note |

## 3. Findings

No BLOCKER, MAJOR or MINOR.

### R839-1-F1: RESIDUE. The jobs test's runtime sentence overstates the measured run

- Lenses: Docs.
- Where: `docs/TEST_DEVELOPER.md:86` "It takes about seven hours on sixteen CPUs." and `tb/verilator/engine/Makefile:79-80` "about seven hours on sixteen CPUs".
- Evidence: published `eq/summary.json` reports 20909.9 s (5 h 48 min) on 16 CPUs, rc 0, on a nearly idle host. The longer figure comes from the pace of an earlier run on a loaded host, a run the power-off killed (HANDOFF). The test's work and verdicts are unaffected.
- Impact: a reader plans for about an hour more than the measured run took. No verdict, test or code changes.
- Required outcome (exact fix): guide `:86` becomes "It takes six to seven hours on sixteen CPUs.", and the Makefile comment's "about seven hours" becomes "six to seven hours". A manager note, not a block, as the review brief directs.
- Verification: `make docs` rc 0 after the edit.

### R839-1-F2: RESIDUE. "Its `--jobs` option" lost its antecedent

- Lenses: Docs.
- Where: `docs/TEST_DEVELOPER.md:62-64`.
- Evidence: before #104, `:60` read "The engine arm runs up to eight mutants at once." and "Its" meant the arm. After the residue rewording, the sentence before reads "By default, up to eight engine mutants run at once.", so "Its" has no singular referent.
- Impact: a wording ambiguity only.
- Required outcome (exact fix): `:64` becomes "The engine arm's `--jobs` option sets that number."
- Verification: `make docs` rc 0 (the 10-word sentence rule holds; it is 7 words).

### R839-1-F3: RESIDUE. The PR body's measurement table does not name the commit of the cold run

- Lenses: Conformance, Docs (PR text only).
- Where: PR #105 body, item 4 table row "after, cold cache", and the "Gates" paragraph.
- Evidence: `after-cold/summary.json` has `"head": "ad06db3b…"`, while `before` is at a64be73d and `after-warm` at 860e474. `git diff ad06db3 860e474` changes one guide sentence and one Makefile comment, with no code, so the figure is valid for the head's code. The published HANDOFF says this. The PR body does not.
- Impact: provenance wording only. No figure changes.
- Required outcome (exact fix): the row label becomes "after, cold cache (at ad06db3; the head adds only a guide sentence and a Makefile comment)".
- Verification: the PR text matches `after-cold/summary.json`.

### Not findings (examined and accepted)

- **Default ccache can now fail a build that used to pass.** This happens when ccache is on PATH but its cache directory is not writable. It is the accepted design of issue item 2, it fails loudly (no executable comes back, and the arm prints the "did not build" FAIL and exits 1), and the guide documents it with the remedy. I list it under the manager's duties below for consumer environments.
- **The harness unit misses once per new checkout path.** The arm compiles `sim_main.cpp` by its absolute path. This is stated in the PR, costs a few seconds of CPU and touches no verdict.
- **The order test's "finished out of list order" check could in principle flake.** That would need 159 seeded random delays to finish exactly in list order with 8 workers, which is practically impossible. The check guards against a vacuous pass, which is correct.
- **Comment rule.** The delta's new comments and docstrings carry issue IDs only. The `G1`/`G2` and `E402` tokens are moved check names and a lint code, not lane labels. No new instance.

## 4. Lenses

- **Conformance.** Mapped every item of issue #104 (1 to 5) and the parent rulings against code and receipts, and ran the parent idiom gates myself on live dev, at main and at the head. The only issue is the RESIDUE F3 provenance wording.
- **RTL.** The diff touches no `hdl/`, `syn/`, `bench/` or ROM file. All 70 RTL and 89 generator mutation patterns still apply exactly once: the head's arm passed 160/160 with no "pattern appears" line. The build change (relative RTL names, `cwd=srcdir`) leaves the staged temporary path out of the model's C++ and changes no printed output, because `verdict()` strings carry no harness text. The engine suite at the head with pinned Verilator 5.050 passed 2098/2098 ×3 and 61/61 (`make lint` rc 0).
- **Robustness.** Checked the ccache switch in five cases, through the real recipe and `compiler_env()`. An unwritable cache fails loudly. 8 concurrent writers to one cache left identical outputs. No ccache file in any tree. A caller's `CCACHE_*` wins, and the jobs test strips the caller's `CCACHE_*` and `OBJCACHE` itself.
- **Tests.** The order test passes 10/10 and two negative probes make it fail. The jobs test's checks catch three planted faults on a fake driver. My full arm runs at main and at the head are identical to the published reference. A warm build-only probe got 284/284 from the cache. The published 38/38 receipt is consistent with all of this.
- **Docs.** Checked guide lines 23-24, 50-51, 62-86 and the Makefile and module comments against code and probes. `make docs`, `make diagrams-check` and `make contract` all rc 0. The only issues are RESIDUE F1 and F2.

### Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #104 items 1-5; milan-fpga #883 ruling (b), #495 residue; parent `check_py_idiom.py`/`check_cpp_idiom.py` on dev b7d69295 at head (rc 0) and at a64be73d (rc 1, the three ratchets); receipts `before/after-cold/after-warm/eq`; PR body (F3 RESIDUE) | R839-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| RTL | CLEAN | `git diff --stat` (no hdl/syn/bench/ROM); `build()` relative-name change; generated model C++ at main and head; head arm 160/160 (every pattern applied once); engine suite 2098×3 + 61 PASS; `make lint` rc 0 | R839-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| Robustness | CLEAN | Makefile :20-33, `compiler_env()` :597-609, `build()` :612-629; switch probes (5 cases); unwritable-cache probe; cache-key probes (new dir, new path, main); suite `CCACHE_BASEDIR` cross-path build; tree cleanliness | R839-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| Tests | CLEAN | `tb/mutation_jobs_test.py`, `tb/mutation_order_test.py`; order test 10/10 + 2 negative probes; jobs-test fake-driver probes (good + 3 faults); full arm main uncached and head cold, both sha `9fb353df…`; warm build-only probe 284/0; published `eq` 38/38 | R839-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |
| Docs | CLEAN | `docs/TEST_DEVELOPER.md` :23-24, :50-51, :60-90; engine Makefile comments; `mutants.py`/`path_mutants.py` docstrings; `tb/verilator/engine/README.md`; comment rule over the delta; `make docs` rc 0 (F1, F2 RESIDUE) | R839-1 | 860e47493ad5a92c4662fef601fd196b0143c4bb |

## 5. Real limits

- I did not run `mutants-jobs-test` itself; it took 5 h 48 min. I rely on its published receipt (`eq/make.log`, run at 860e474), together with my own full arm runs (main uncached and head ccache-cold, both `--jobs 8`), my warm build-only probe (no simulation) and my fake-driver probes of the test's checks. I did not simulate a full arm on a warm cache.
- I did not run `make all` (a full gPTP bank, out of scope), and I did not re-measure the timing table. My arm wall times (3640 s main, 3629 s head) were on a shared host beside other work and are **not** a measurement of the claim. The table is checked against its receipts only.
- I ran the parent gate on live dev `b7d69295`, not the author's `fa6c094b8e`. It passes on both. The pin was a scratch-index gitlink only; nothing was committed.
- The repository has no hosted workflows. The exact head has 0 check runs and 0 statuses, so there is no hosted evidence to inspect.
- No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof. `make ooc` (Vivado) was not run; the diff touches no `syn/` or `hdl/` file.

## 6. Pending manager duties

- At the merge turn, validate the current-dev merge candidate (builder and native banks), including the parent consumer legs with `gptp-processor` at the merge pin (`docs.yml` gate_38/39), and link the receipts on the PR.
- Confirm that every consumer environment with `ccache` on PATH has a writable cache directory, or sets `CCACHE_DIR` or `OBJCACHE=`. By default an unwritable cache now fails the engine build. That is documented, and it is by design.
- Carry RESIDUE R839-1-F1, F2 and F3 to the residue checklist.
- Hosted/act acceptance, and the second independent review the merge requires.

## 7. Receipts and scripts (all listed in MANIFEST.sha256)

- `receipts/parent-idiom/`: parent dev head and pin; py and cpp gates and their selftests at the head; py gate at main; per-file `scan()` at main and head.
- `receipts/mutation-list/`: `MUTATIONS` dumps at three commits, their hashes, and the byte comparison of the moved block.
- `receipts/ccache-switch/`: switch probes (real recipe and `compiler_env`), cache-key probes, unwritable-cache probe.
- `receipts/arm/`: full arm at main (uncached) and at the head (ccache cold): stdout, stderr, rc, wall, ccache counters, comparison; warm build-only probe.
- `receipts/order-test/`: the head's order test and its negative probes.
- `receipts/jobs-test-probe/`: fake-driver probes of `mutation_jobs_test.py`.
- `receipts/suite/`: engine suite at the head, and the suite build from another path (`CCACHE_BASEDIR` hits).
- `receipts/gates/`: `make contract`, `make docs`, `make lint`, `make diagrams-check` at the head.
- `receipts/integrity/review-clone.txt`: the review clone after all probes. HEAD and tree are exact, the status is empty (ignored files included), the index modes and blobs equal the HEAD tree, every worktree blob rehashes equal, and there are no gitlinks in this repository. Every probe ran in disposable copies under the packet's scratch directory.
- `scripts/`: the portable probe scripts these receipts came from.

R839-1 FINISHED
