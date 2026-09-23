# [A189] Issue #523 / PR #526: correction round for R256-2 and R257-1

Author handoff. Factual; this is implementation evidence, not a review verdict.

## Identity

| Item | Value |
|---|---|
| Branch | `523-isolate-mutation-cancellation` (local only; nothing pushed, PR not edited) |
| Reviewed head | `b5ce20eca8b59709ec5bc6115e5e15bfc312f283`, tree `bfde1313250ae84105754af4b150325f55f5ef33` |
| Live dev merged | `776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d` |
| Merge commit | `86149f2b2a3575dc0e7c99c3f207e3cb7f466538`, tree `c0ad43e5770b9240ba370ddc8c049337f4b11f8c`, identical to the `git merge-tree --write-tree` dry run (exit 0, no conflict); auto-merged `docs/testing/TESTING.md` and `scripts/measure_test_evidence.py` |
| Final head | `6674c278a8db5f0886d036dceff02d33b7ca6a37`, tree `8d634f12cb83c2ca9ccdb7a4b5e7dde9b19a6245` |
| Ancestry | `776bc77d` and `b5ce20ec` are both ancestors of the final head |
| Worktree / index | clean; no index flags; every tracked blob and mode matches (`receipts/90-final-integrity.json`) |
| Gitlinks (unchanged throughout) | `gptp-processor c1b61743`, `protocol-processor 424c688f`, `third_party/verilog-axis 48ff7a7e`; `external efeb541a` uninitialised and not required |

Commits after the reviewed head (one-line subjects, no bodies, no trailers):

1. `86149f2b` Merge live dev 776bc77d into the #523 correction lane
2. `29329cea` Tie owned commands to their owner and refuse missing process facilities
3. `64a6c373` Verify only the shadow build's inputs and accept non-redirecting Git settings
4. `4095fc36` Initialise pinned submodules in a lane instead of copying them
5. `88b17a3e` Control the copied-dependency refusal and make's death with a killed campaign
6. `6674c278` Claim only the controlled hard-stop signals in the sweep contract

Files changed against live dev (13, same set as the reviewed head): `CONTRIBUTING.md`, `docs/testing/TESTING.md`, `scripts/check_baremetal_only.py`, `scripts/measure_test_evidence.py`, `scripts/owned_process.py`, `scripts/process_test_support.py`, `scripts/run_all_suites.sh`, `scripts/test_suite_cancellation.py`, `tb/verilator/gptp_shadow/{Makefile,README.md,mutants.py,private_inputs.py,test_mutant_lifecycle.py}`. This round did not modify `check_baremetal_only.py` or `measure_test_evidence.py`. No `hdl/`, firmware, processor pin, `*.budget`, or #517 pool file changed.

## Resolution per finding

"Mutation" means the correction removed in a disposable export of the final head; each named arm of the committed tests must then fail. All 23 rows fail as required and all 34 baseline arms pass on the unmutated export (`receipts/mutation-controls/mutation-controls.json`, one log per arm).

| Finding | Root cause | Correction | Permanent control | Mutation (arm goes red) |
|---|---|---|---|---|
| R256-2 F1, R257-1 F1 (MAJOR) | The launched PID became a Python owner that ran the sweep shell in a new session and handled only INT/TERM. When the owner died without cleanup, the shell kept running detached. | `OwnedProcesses.run` launches every command with a pre-exec binding: `PR_SET_PDEATHSIG(SIGKILL)`, plus a check that the owner is still the parent. The sweep shell, and the campaign's `make`, die with their owner. A command they had already started may finish. Contract documented in `run_all_suites.sh` exit table, `TESTING.md` and the owner docstring. | `test_suite_cancellation.py` `hard_stop` for KILL-entry, HUP-entry and HUP-group. Each checks the shell identity exited before release, no output after the caller saw the stop, no next-suite sentinel, no summary, the lock freed after the in-flight command, and every identity reaped. An unsafe arm without the binding reproduces the reviewed defect (`PASS omega` plus a summary after death). `test_mutant_lifecycle.py` KILL arm: the campaign's `make` dies with the killed driver. | `F1-commands-outlive-owner`: all three `hard_stop` arms and `interrupted:SIGKILL` go red |
| R256-2 F2, R257-1 F2 (MAJOR) | An allowlist of four `GIT_*` names refused every other Git variable, including editor, identity, transport and trace settings. | `REDIRECTS` refuses by name only the variables that redirect the checkout: `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_REPLACE_REF_BASE`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`. Every other Git variable is accepted, and all `GIT_*` are removed from the identity commands' environment. Documented in the suite README. | `accepted:presentation`: 13 ordinary variables run all nine controls. `accepted:scrubbed`: `GIT_GLOB_PATHSPECS=1`, fatal to raw literal-pathspec Git, still runs all nine. One `refusal:git-env-<NAME>` arm per redirect asserts that exact name; the list is written in the test, not imported. | `F2-original-allowlist`: presentation and scrubbed arms red. `F2-git-variables-reach-identity-commands`: scrubbed arm red. `F2-redirect-<NAME>-accepted` for all 11 names: each arm red |
| R256-2 F3 (MINOR) | The first-party population was the whole of `hdl/`, `tb/common` and the suite directory, so unrelated or regenerated files refused the campaign. | The population is asked, not parsed. A new `print-inputs` Makefile target reports the files `run` reads; the driver adds the local quoted C++ includes transitively. Only these are verified and copied. Mutation targets and anchors must be among them. Dependencies follow the same rule; pins are still verified. | `accepted:unrelated` passes with: timestamp-rewritten and dirty `TEST_RESULTS.md` files, a staged README edit, a dirty unrelated `tb/common` header, an untracked `hdl/common` file, and a dirty unrelated axis file. `interrupted` asserts the private tree is exactly the declared population. The two headers are stated in the test independently. `refusal:dirty-input`, `dirty-header`, `dirty-anchor` and `undeclared-target` each assert their own reason. | `F3-directory-scope-population`: unrelated and population arms red. `F3-no-include-walk`: dirty-header and population arms red. `F3-targets-need-not-be-inputs`: undeclared-target arm red |
| R256-2 F4 (MINOR) | CONTRIBUTING section 2.2 prescribed `cp -r third_party/` and deleting its `.git`, a layout the pin refusal rejects. | CONTRIBUTING section 2.2 and its Contents entry now say: never symlink or copy a submodule into a lane; initialise the pinned submodules. The next bullet names the shadow campaign among the pin-proving gates. The README states the refusal. | `refusal:copied-dependency`: a dependency with its files but no `.git` refuses with "required dependency is not at its pin". | `F4-copied-dependency-accepted`: arm red |
| R256-2 F5 (MINOR) | `owner.run` merged stderr into the text that `_records` split into identity records, so a Git warning raised `ValueError` (exit 1). | `OwnedProcesses.run` takes an optional separate `stderr` file. Identity commands and `make print-inputs` parse standard output only; diagnostics appear only in refusal messages. A malformed record is `InputRefused` (exit 2). The fixture `git()` helper also reads stdout only. | `accepted:git-stderr`: `core.fsyncObjectFiles` makes every Git command warn; all nine controls run. `refusal:git-garbage`: a PATH Git shim injects an unreadable record; refused with exit 2 and no traceback. | `F5-stderr-parsed-as-records` and `F5-unreadable-record-crashes`: each arm red |
| R257-1 F3 (MINOR) | Facilities were looked up by attribute, so a missing `prctl`, `os.pidfd_open` or `signal.pidfd_send_signal` raised `AttributeError` (traceback, exit 1). | `_prctl()` resolves all three before any state change and raises `Unsupported` (an `OSError`), which both entry points print as `REFUSED:` with exit 2. `PR_GET_PDEATHSIG` and the pidfd probe run before adoption changes. A failed pre-exec binding is also `Unsupported`. | `unsupported:<mode>` in both tests, for no-prctl, prctl-fails, no-pidfd-open and no-pidfd-signal, through a `sitecustomize` removal: exit 2, `REFUSED:`, no traceback, nothing started. | `F3b-no-facility-resolution`: the no-prctl, no-pidfd-open and no-pidfd-signal arms of both tests red. prctl-fails was already a refusal at the reviewed head |

### Suggestions

| Suggestion | Disposition |
|---|---|
| R256-2 S1, R257-1 S3 (test power) | Partly taken. Refusal arms now assert their specific reason. `S-no-directory-link-check` turns parent-link and dependency-link red; `S-no-index-comparison` turns staged and untracked red. Git-environment rules are per-variable and pins are reason-specific (rows above). Not changed, and still verified only by inspection: the PID-reuse identity recheck, root SIGSTOP ordering, a zombie-aware cleanup return, and the anchors of the two bare-metal masks. |
| R256-2 S2 (missing facility) | Taken as R257-1 F3 above. |
| R256-2 S3 (signal during the final tally prints the counts line) | Not taken. Behaviour is unchanged and re-probed: 130/143, CANCELLED lines, no `logs:` line (`receipts/53-R256-summary-signal.log`). Reordering the summary would change a shape tests and CI read. |
| R256-2 S4, R257-1 S1 (Verilator job default) | Taken. `VERILATOR_JOBS ?= 0` restores the repo convention and the base `-j 0`; the knob is kept. |
| R257-1 S2 (owner line contradicts "logs were not prepared") | Taken. The owner now prints `CANCELLED: signal N; no completed sweep result` (`receipts/51-R257-lock-wait-*.log`). |

## Kept as reviewed

- `MUTATIONS` (9), `NOT_SEPARATELY_OBSERVABLE` (6), `TALLY_RE`, `PLANE/RET/OBS/TIC`, `suite_failed` and `apply_control` are AST-identical to base `483a133e`. See `receipts/47-R257-mutation-tables.log` and `48-R256-mutation-population.log`, both reviewers' scripts, unmodified. Only `main()` changed: it passes the suite directory and the target set.
- Graceful cancellation is unchanged: INT/TERM give 130/143, owned identities are reaped and a foreign sibling survives. Committed arms pass, and both reviewers' lock-wait probes pass (`receipts/51-*`, `52-*`).
- The two host-process masks and their twelve arms are unchanged: bare-metal selftest 354 arms, `--check` 0 findings.
- SHA256SUMS/MANIFEST reconciliation: this round touched no evidence file.

## Validation at the final head `6674c278`

The scoped tool is `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`: Verilator 5.050 rev v5.050, wrapper sha256 `905795b9...`, `verilator_bin` sha256 `44898b22...`. Both match the reviewers' records (`receipts/05-verilator-identity.txt`). System Verilator is 5.052 and was not used. At most 8 jobs throughout.

| Receipt | Command | Result |
|---|---|---|
| `63-real-make-final` | `make -C tb/verilator/gptp_shadow` after `make clean`, with `VERILATOR` set to the scoped tool, `VERILATOR_JOBS=8`, 12 ordinary Git variables exported (editor, sequence editor, pager, author/committer, SSH, askpass, trace, merge autoedit, terminal prompt), and `XDG_CONFIG_HOME` holding a deprecated `core.fsyncObjectFiles` | exit 0, 292 s. Fresh 18-module build. Lifecycle PASS; `309 checks: 309 PASS, 0 FAIL`; 9 controls caught, 6 by name and 3 by the original alternate-failed-check path (observer/crossing latency, credit); 6 notes; `controls: 9 failures: 0`; `RESULT: PASS`. Integrity CLEAN before and after |
| `61-final-gates-*` | lifecycle; cancellation; `check_py_idiom` and selftest; `check_sh_idiom` and selftest; `measure_test_evidence --check` and selftest; `measure_fail_fast --check` and selftest; `check_baremetal_only --check` and selftest; `docs_check`; `check_doc_style`; `check_em_dash --base 776bc77d` and selftest; `check_doc_paths`; `gen_toc --check`; `bash -n run_all_suites.sh`; `make -n` | all 20 exit 0. Lifecycle 47.5 s, cancellation 39.4 s. em-dash: 0 findings over 109 added lines. No ratchet raised |
| `60-mutation-controls-final` | `scripts/mutation_controls.py` | PASS: 23 of 23 mutations red, 34 of 34 baseline arms green |
| `50-R257-real-interrupt-{INT,TERM,KILL}` | R257 real-driver probe, real Verilator, at a live build boundary | INT 130 and TERM 143: private tree removed, nothing alive, no verdict. KILL -9: no verdict; only the deeper Verilator processes survived (stopped by the probe); the driver's `make` did not. Caller integrity 0 problems in all three |

Earlier receipts at `88b17a3e` are in the packet: gates `10-*`, mutations `20-*`, real make `30-*` (incremental) and `32-*` (fresh), tally `33-34`. `88b17a3e` differs from the final head only in comments (the owner docstring and the sweep exit table) and one `TESTING.md` sentence (`git diff 88b17a3e 6674c278`).

### Reviewers' own probes, re-run unmodified

| Receipt | Probe | Result at the corrected head |
|---|---|---|
| `40-R256-sweep-hardstop` | R256 hard stop: KILL and HUP to the entry only | head and base identical: no next suite, no summary, no `PASS omega` |
| `41-R257-hardstop-{head,base}-{KILL,HUP}` | R257 hard stop | head matches base. Survivors are only the in-flight command's processes (timeout, make shim, worker, its child), never the sweep shell. `later_suite_started` and `completed_summary_after_death` are false; nothing is printed after death |
| `42-R257-git-env-head` | R257 Git environment | `GIT_EDITOR`, `GIT_SEQUENCE_EDITOR`, `GIT_ASKPASS`, `GIT_AUTHOR_NAME`, `GIT_COMMITTER_EMAIL`, `GIT_SSH_COMMAND`, `GIT_TRACE=0`, `GIT_MERGE_AUTOEDIT`, `GIT_PAGER`: exit 0, 9 controls each. `GIT_INDEX_FILE`, `GIT_DIR`, `GIT_WORK_TREE`, `GIT_OBJECT_DIRECTORY`: exit 2, 0 controls, refused by name |
| `43-R257-unsupported-*`, `44-R256-unsupported-platform` | missing facilities | `REFUSED: process ownership: ...`, exit 2, command not started |
| `45-R256-refusal-scope` | R256 real-tree refusal scope, on a disposable local clone | the 8 ordinary variables, the timestamp-only `TEST_RESULTS.md`, the untracked `hdl/common` file and the dirty `hdl/ieee1722` doc now start the real campaign (the probe's 60 s timeout ends each with `CANCELLED: signal 15`). `GIT_INDEX_FILE` refused. Table in `receipts/probes/R256-refusal-scope.tsv` |
| `46-R256-dependency-pins` | R256 real-tree pins, on the same clone | refused: parent of pin, uninitialised, `cp -r` copy without `.git`, dirty gptp-processor build input. Accepted: untracked file outside the declared inputs |
| `51-R257-lock-wait-*`, `52-R256-lock-wait-cancel`, `53-R256-summary-signal` | graceful sweep paths | unchanged 130/143; foreign holder untouched; no suite started |

A failed probe attempt is kept, not hidden. Attempt `49-R257-real-interrupt-*` exited 1: I passed `TMPDIR` through the packet symlink, and the probe matches `/proc/<pid>/cwd` (resolved) against the unresolved private path, so it never recognised a boundary. Each attempt instead ran the full real campaign to `RESULT: PASS` with the lane CLEAN. Attempt `50-*` used the resolved path.

## Scripts

Everything is under `scripts/` in this packet:

- `rcpt.py`: receipt runner.
- `integrity.py`: blob, mode, index and gitlink proof.
- `focused_gates.sh`
- `mutation_controls.py`
- `real_shadow_make.sh`
- `reviewer_probes.sh`
- `clone_probes.sh`: builds a disposable local clone, because R256's two real-tree probes edit, then `git checkout`/`git clean`, the tree they are given.

The reviewers' probe scripts were used unmodified from `523-review-evidence` at `4d13acca`. `prepare_scratch.sh CHECKOUT PACKET` recreates everything the runners expect under `scratch/`. The real-interrupt probe needs `TMPDIR` given as a resolved path.

## Open risks and questions (not findings of either report)

- **Job-control stop.** A TSTP (Ctrl-Z) of the entry suspends only the owner. The sweep shell, in its own session, keeps running. Unchanged from the reviewed head; neither report raised it. It needs a reviewer or maintainer decision if it matters.
- **Fork window.** A command the sweep shell forked before the owner finished exiting counts as "already started" and may finish. The kernel refuses a fork once the kill is pending.
- **Inspection-only guards.** The pre-exec parent check (owner died between fork and binding) and the pidfd start-time recheck cannot be driven deterministically; both are verified by inspection only.
- **Hard stop leaves the lock record.** The lock owner record may remain after a hard stop; the lock itself frees when the in-flight command exits. Documented.
- **Dependency narrowing.** Dependency files are narrowed to declared inputs by the same principle as F3. An unrelated dirty axis file no longer refuses; pins are still proven.
- **Host paths in receipts.** Receipts contain literal host paths and must be normalised before publication.

## Not run (manager-owned or not permitted)

Full parent, processor, Yosys and builder banks; trusted act and Docker; hosted checks; hardware; push; PR edits; merge. Disposable exports, clone and fixtures were under `scratch/` and are deleted.

## Public comments

- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/523#issuecomment-5790027153
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/523#issuecomment-5790915806
