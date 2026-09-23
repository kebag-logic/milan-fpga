[A189] REVIEW READY

Commit: 6674c278a8db5f0886d036dceff02d33b7ca6a37
Tree: 8d634f12cb83c2ca9ccdb7a4b5e7dde9b19a6245
Base: live dev 776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d, merged conflict-free at 86149f2b (merge tree equals the dry-run tree). The reviewed head b5ce20ec is an ancestor. Tree and index are clean. Gitlinks are unchanged: gptp-processor c1b61743, protocol-processor 424c688f, verilog-axis 48ff7a7e. Source is local and unpublished.

Changed (same 13 files against dev; no hdl/, firmware, pin, ratchet or #517 pool file):
- Every owner-launched command now dies with its owner. A hard stop therefore cannot leave a detached sweep.
- Only redirecting Git variables are refused.
- The shadow campaign verifies exactly what its build reads.
- Git identity output is parsed from stdout only.
- A missing process facility is refused cleanly.
- CONTRIBUTING prescribes initialised submodules.

| Finding | Resolution | Permanent control (removing the fix turns it red) |
|---|---|---|
| R256-2 F1 / R257-1 F1 MAJOR | Commands start with a parent-death KILL binding and an owner-still-parent check. The sweep shell (and the campaign's make) die with the owner; a command already running may finish. Documented in the sweep exit table and TESTING.md. | Sweep hard-stop arms for KILL, HUP and group HUP. Each requires: shell exited before release, no output after the caller saw the stop, no next-suite sentinel, no summary, lock freed, identities reaped. An unsafe arm reproduces the detached sweep. The campaign KILL arm requires its make to die. |
| R256-2 F2 / R257-1 F2 MAJOR | Refused by name: GIT_DIR, GIT_WORK_TREE, GIT_COMMON_DIR, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_REPLACE_REF_BASE, GIT_CONFIG_PARAMETERS/COUNT/GLOBAL/SYSTEM. Every other Git variable is accepted, and none reaches the identity commands. Documented in the suite README. | Thirteen ordinary variables run all nine controls. GIT_GLOB_PATHSPECS still runs, proving the scrub. One arm per redirect asserts its exact name; the list lives in the test. |
| R256-2 F3 MINOR | Population = `make print-inputs` plus local C++ includes. Targets and anchors must be inputs; dependencies follow the same rule. | An unrelated-state arm passes: rewritten TEST_RESULTS.md, staged README, dirty unrelated header, untracked hdl file, dirty unrelated axis file. The private tree must equal the declared population. Dirty input, header and anchor, and an undeclared target, each refuse with their own reason. |
| R256-2 F4 MINOR | CONTRIBUTING 2.2 and its Contents entry: never symlink or copy a submodule; initialise it at its pin. | A copied dependency without `.git` refuses: "not at its pin". |
| R256-2 F5 MINOR | Identity commands and the input query parse stdout; stderr appears only in refusal text. A malformed record is exit 2. | A deprecated-config warning run passes all nine. A garbled-record Git shim refuses with exit 2 and no traceback. |
| R257-1 F3 MINOR | prctl, pidfd_open and pidfd_send_signal are resolved before any state change. A missing one prints `REFUSED:` and exits 2 at both entry points. | Four facility-removal arms in each test. |

Suggestions:
- Taken: Verilator job default restored to `?= 0`; neutral owner cancellation line; refusal arms assert specific reasons (directory-link and index-comparison guards now load-bearing).
- Not changed: the final-tally signal ordering (status and CANCELLED lines remain authoritative); the inspection-only PID-reuse and SIGSTOP guards; the mask anchors.

Validation at 6674c278:
- `make -C tb/verilator/gptp_shadow` after `make clean`: verified Verilator 5.050, VERILATOR_JOBS=8, twelve ordinary Git variables exported, a global config that makes Git warn on stderr. Exit 0. Lifecycle PASS; 309/309; nine detections (six named, three via the unchanged alternate-failed-check path); six notes; RESULT PASS. Integrity clean before and after.
- Lifecycle test, cancellation test, Python/shell idiom and selftests, test-evidence, fail-fast, bare-metal check and selftest (354 arms), docs, doc style, em-dash, doc paths, contents, `bash -n`, `make -n`: all 20 exit 0.
- Fix-removal mutations in disposable exports: 23 of 23 turn their arms red; 34 of 34 baseline arms green.
- Mutation tables, six reasons, TALLY_RE, suite_failed and apply_control are AST-identical to base.

Both reviewers' published probes were re-run unmodified at this head:
- Hard stop: KILL/HUP now match base. No later suite, no summary; only the in-flight command survives.
- Git environment: ordinary variables run nine controls; redirects are refused.
- Refusal scope: presentation variables and unrelated files proceed, on a disposable clone.
- Dependency pins: off-pin, uninitialised, copy without `.git` and dirty input are refused.
- Missing facilities: exit 2.
- Real driver at a live build boundary: INT 130 and TERM 143 leave nothing alive; KILL gives no verdict and a clean caller.
- Lock wait and final-tally signal: unchanged.

Acceptance: criteria 1-3 are implemented and exercised; the author-owned part of 4 passes.

Open risks/questions (not findings of either report):
- A job-control stop of the entry (TSTP) suspends only the owner; the sweep shell continues. This is unchanged from the reviewed head.
- A command forked while the owner was still exiting counts as already started.
- The owner-still-parent check and the pidfd start-time recheck are verified by inspection only.
- A hard stop may leave the lock owner record.
- Dependency files are narrowed to declared inputs.
- Receipts carry literal host paths.

The factual HANDOFF, the proposed PR body, exact command/exit receipts, the failed probe attempt and reproducible scripts are in the author handoff directory for manager publication.

Remaining manager/external bar: trusted act, exact-head hosted checks, publication, current-dev candidate validation, full banks, R256 and R257 re-review with a clean lens ledger, maintainer-authorized merge and post-merge containment. This is implementation evidence, not review approval. A189 stops at this source.
