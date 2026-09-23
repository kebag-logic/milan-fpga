[R257] POSITIVE - exact head 015edd9ab2248289ff000f6ef14890be1812ba7b

External independent review, round R257-3, of issue #523 / PR #526.

- Head `015edd9ab2248289ff000f6ef14890be1812ba7b`, tree `fc03d0313af978c147bf734f9905fdc427a2b758`. Its parent is `26353960`, the head of my previous round (R257-2).
- Source base `776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d`, an ancestor of the head. Live `dev` is `ede8d48ecd7c7f589a14b957951f040d92c99c70`. The current-dev candidate is manager-owned and was not reviewed here.
- **Reconstruction order.**
  1. AGENTS/CONTRIBUTING and docs/README (the authority order).
  2. The #523 body (frozen acceptance 1-4), the settled decision 5783211002, and the manager assignment 5793839744.
  3. REQ-VER-01/02/04.
  4. `git diff 776bc77d..015edd9a` and its history, with the delta `26353960..015edd9a` in full.
  5. The author's REVIEW READY 5794119960, and after my own pass, the public correction-a195 packet at `9eea4205`.
- **Isolation.** I read my own R257-2 report at the start, because this round follows it up. I read the other reviewer's R256-3 comment, which also tabulates R256-2, only after my own pass over the diff and my probes. I read no private author material, no management files, and nothing under the evidence tree's `reviews/` directory.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head.

R257-2-F1 (MINOR, Tests) is resolved. The sweep's cancellation report is now asserted at every graceful boundary, for both signals, and each assertion is load-bearing:
- 20 single-defect copies of the production sweep, plus an unmodified copy, were each run against the parent's test and against the head's test.
- 16 defects passed the parent's test and turn the head's test red. That includes all four named in R257-2-F1.
- 3 defects were already red under the parent's test and remain red.
- The one survivor reorders statements inside `prepare_logs`, where no deterministic boundary exists. It is not a defect.

The delta is one test file. I re-applied every lens that file touches, including Robustness, because the sweep's own preflight runs this test. One new SUGGESTION: the new lock-wait arm needs the `flock` binary.

## Findings

No BLOCKER, MAJOR or MINOR.

### R257-3-S1 (SUGGESTION)

```text
[R257] SUGGESTION Tests, Robustness, Docs - scripts/test_suite_cancellation.py:211-242 (lock_wait, queued), scripts/run_all_suites.sh:211-232, issue comment 5794119960 and correction-a195/HANDOFF.md:84 - The new lock-wait arm needs the flock(1) binary, while the sweep keeps a supported mkdir fallback
Authority/evidence: The arm holds the tree lock with fcntl and waits for a "flock" child under the entry (test_suite_cancellation.py:215,231-235). Without flock(1) the sweep takes its mkdir fallback (run_all_suites.sh:219-231), which that hold does not block. With flock(1) hidden from PATH (receipts/12-no-flock-binary.json), the sweep ran to completion and the head test failed at lock_wait:236, its message the whole sweep transcript. The parent's test passed on the same PATH. The author's statement that the arm needs flock(1) "as the existing lock_free() hard-stop check already does" is therefore inaccurate: lock_free() (test_suite_cancellation.py:282-290) calls fcntl.flock(2), not the binary. Through the normal entry on such a host, the preflight would ABORT with exit 2, as receipts/20 shows for a red arm. That failure is closed, and no verdict is produced.
Impact: On a Linux host without flock(1) the normal sweep refuses to run, with a misleading assertion text. No documented environment is affected: Containerfile.dev uses an Arch base that includes util-linux, and the hosted jobs run on ubuntu-latest. Before this commit the sweep ran there.
Required outcome (optional): the arm holds the lock the sweep actually uses in the fallback configuration, or it fails naming flock(1) as a missing prerequisite. Alternatively, TESTING.md lists flock(1) as a sweep prerequisite. Do not skip the arm silently.
Verification: rerun receipts/12's PATH-shadow arm; the head test passes or fails with a message naming flock(1).
```

### Retained suggestions (production bytes are unchanged, so the R257-2 evidence stands)

- R257-2-S1 (Tests): two process guards (root stop before forwarding; the shell's own session) have no control of their own.
- R257-2-S2 (Tests): the two exact-line bare-metal mask anchors are unpinned.
- R257-2-S3 (Robustness): a signal during the final tally leaves the counts line printed before the CANCELLED lines.
- R257-2-S4 (Robustness, Docs): a job-control stop suspends only the supervisor.
- R257-2-S5 (Robustness, Docs): Git itself exports refused names in hook, worktree `rebase --exec`, `-c` alias and `submodule foreach` contexts.
- R257-2-S6 (Docs): the PR body's Status still names source `6674c278`. The issue's A195 REVIEW READY covers `015edd9a`.

### Observation (not a finding)

`logs-ready-before-clear` survives. It moves `LOGS_READY=1` above `mkdir`/`rm` inside `prepare_logs` (run_all_suites.sh:262-266). A signal can only land inside that sub-millisecond span, so no handshake can separate the two orders. Either order gives the same report at every deterministic boundary.

## Prior public findings at this head

| Prior finding | State at 015edd9a | Evidence |
|---|---|---|
| R257-2-F1 MINOR Tests, the cancellation report had no failing test | **RESOLVED** | `cancel_report()` (test_suite_cancellation.py:114-127) runs in all 8 graceful cancellation arms (line 190) and both lock-wait arms (line 240). It requires three things: the shell's own `CANCELLED: INT\|TERM; no completed sweep result` line, exactly `partial logs: <requested OUT>` after preparation, and the not-prepared line with no `partial logs:` line and the previous logs unchanged before it. The four defects named in R257-2-F1's verification, rebuilt as independent edits in this round's probe, are red under the head's test (receipts/10) and green under the parent's (receipts/11). The full table is below. Normal-entry ownership: receipts/20. |
| R256-2 F1-F5, R257-1 F1-F3 | RESOLVED (unchanged since 26353960) | Resolved at `26353960` (R257-2 and R256-3 agree). `git diff --raw 26353960..015edd9a` changes only scripts/test_suite_cancellation.py (receipts/01), so every production file that resolved them is byte-identical at this head. The lifecycle test, which imports `fixture` from the changed file, passes at the head (receipts/30). |
| R257-2 S1-S6 | RETAINED as suggestions | See above. |
| R256-3 suggestions | Not re-litigated | They are SUGGESTIONS on production files the delta does not touch. |

## Test power at this head

Each arm below is a disposable `git archive` copy of `scripts/` at the head, with one edit to `run_all_suites.sh`. Both test versions ran unmodified: the parent's test (`26353960`) and the head's test (`015edd9a`). Receipts: receipts/10, 11 and 14, with transcripts in receipts/arm-logs/. Script: scripts/probe_report_mutations.py.

| Mutant | What it breaks | Parent test | Head test (failing frame) |
|---|---|---|---|
| `none` | unmodified | GREEN | GREEN |
| `logs-ready-early` | claims this run's logs before any preparation | GREEN | RED cancel_report:125 |
| `logs-ready-never-set` | denies partial logs that exist | GREEN | RED cancel_report:123 |
| `no-partial-logs-message` | prepared boundary prints no logs line | GREEN | RED cancel_report:123 |
| `no-term-trap` | shell's TERM report gone | GREEN | RED cancel_report:119 |
| `no-int-trap` | shell's INT report gone | RED | RED cancel_report:119 |
| `no-unprepared-message` | unprepared boundary prints nothing | GREEN | RED cancel_report:125 |
| `report-inverted` | reports swapped | GREEN | RED cancel_report:125 |
| `report-by-out-exists` | attribution by OUT existing, not by preparation | GREEN | RED cancel_report:125 |
| `partial-logs-wrong-dir` | names the default directory | GREEN | RED cancel_report:123 |
| `partial-logs-basename` | names a relative basename | GREEN | RED cancel_report:123 |
| `both-report-lines` | not-prepared line at every boundary | GREEN | RED cancel_report:123 |
| `int-reported-as-term` | INT reported as TERM | GREEN | RED cancel_report:119 |
| `no-cancel-line` | shell drops its CANCELLED line | GREEN | RED cancel_report:119 |
| `no-trap-exit` | trap returns, shell continues | RED | RED cancellation:186 |
| `prepare-before-lock` | logs cleared and claimed before the lock wait | GREEN | RED lock_wait:240 / cancel_report:125 |
| `prepare-before-selection` | logs cleared and claimed before selection | GREEN | RED cancel_report:125 |
| `no-wait-queue` | `--wait` no longer queues | GREEN | RED lock_wait:236 |
| `no-stale-clear` | previous logs survive into OUT | RED | RED cancellation:199 |
| `clear-before-lock` | queued sweep deletes the holder's previous logs, report unchanged | GREEN | RED lock_wait:240 / cancel_report:127 |
| `logs-ready-before-clear` | order inside prepare_logs | GREEN | GREEN (observation above) |

Every new assertion line is the failing line for at least one mutant:
- 119, the shell's line;
- 123, the prepared report;
- 125, the unprepared report;
- 127, previous evidence unchanged, which also pins TESTING.md:237 "Old logs are cleared after locking";
- 236 and 240, the lock-wait boundary.

The lock-wait arm is the only control for `prepare-before-lock`, `no-wait-queue` and `clear-before-lock`.

## What was verified at this head

- **Delta scope** (receipts/01).
  - One blob changes, `scripts/test_suite_cancellation.py` (`abb73afb` to `839a8703`), mode 100644 unchanged.
  - No gitlink, hdl/ or workflow change. `git diff --stat 776bc77d..015edd9a` on hdl, gitlinks, third_party and external is empty.
  - The commit message is one line with no trailers.
  - The head descends from `26353960` and `776bc77d`.
- **Normal-entry ownership** (receipts/20, entry-logs/). The real `bash scripts/run_all_suites.sh OUT` ran in archive copies with a PATH `make` guard.
  - `logs-ready-early` and `prepare-before-lock` each exit 2 with `ABORTING: sweep cancellation controls failed.`, failing at cancel_report:125 and lock_wait:240 in the sweep's own preflight log. No suite ran and the guard was never hit.
  - The unmodified copy, with `SUITE_SWEEP_LOCK` exported at a shared path, logged both `cancel-lock-wait-*` arms and `suite cancellation: PASS`.
  - TERM to that entry then gave 143 with `CANCELLED: TERM; no completed sweep result` and `partial logs: <OUT>`.
- **Repeatability.** Six concurrent unmodified runs, at host load 15-17 on 16 CPUs, all passed in 40 s each (receipts/13). The documented command in the clone passed in 40 s (receipts/31). The runtime is 40 s against 39.4 s for the parent.
- **Import compatibility.** `make -C tb/verilator/gptp_shadow lifecycle` at the head exits 0 in 49 s, with `mutant lifecycle: PASS`, nested-SIGINT 130 and nested-SIGTERM 143 (receipts/30).
- **Focused static gates** (receipts/gates/SUMMARY.txt). All 19 exit 0:
  - Python and shell idiom, with their selftests;
  - fail-fast, and test-evidence with its selftest;
  - docs_check, em-dash against base with its selftest, doc style, doc paths, TOC check and anchors;
  - bare-metal `--check` and `--selftest`, ci_scope selftest;
  - AST parse of the test, `bash -n` on the sweep.
- **Evidence integrity** (receipts/61). correction-a195 at `9eea4205` has 259 files, and every outer `published_sha256` matches.
  - The nested MANIFEST.sha256 has 257 OK and 1 FAILED. The failure is the one `path_redacted` file (receipts/30-gptp-shadow-lifecycle.txt), whose nested digest equals its `original_sha256`.
  - The author's mutation table agrees with my independent results for all 11 shared names.
- **Hosted, inspected only** (receipts/60). At the exact head, 21 contexts executed and concluded success: `rtl-fast`, `verilator-suites` (shards 0-4), `yosys-portability` (shards 0-3), docs, elaborate, lint and others. `Physical gPTP (nightly and manual)` is a skipped context, not hardware evidence. Acceptance belongs to the manager.
- **Manager source banks.** The assignment states they passed at this head. The public evidence branch tip `9eea4205` holds source/manager and act-ready records for `b5ce20ec` only, and no issue or PR comment after the A195 hand-off carries them (receipts/62). I neither verified nor rely on them.
- **Review clone.** It was EXACT before and after every probe, and the two records are identical (receipts/00, receipts/99): 866 tracked entries.
  - gptp-processor `c1b61743` (103), protocol-processor `424c688f` (222) and verilog-axis `48ff7a7e` (214) are each at their pin, own top level, with every blob verified.
  - `git status --ignored` is empty. My gate run's `scripts/__pycache__` (11 files, all created during this round) was removed.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Changed artifact at this head: acceptance 3 ("attributable partial logs") and decision 5783211002's required "partial-log attribution" sweep control, against test_suite_cancellation.py:114-127,190,225-242 and run_all_suites.sh:122-133,262-266 (receipts/10, 11, 14, 20). Unchanged production scope (acceptance 1-4, owned_process.py, private_inputs.py, mutants.py, run_all_suites.sh) byte-identical since R257-2 (receipts/01) | R257-3 (delta); R257-2 (unchanged production files) | 015edd9ab2248289ff000f6ef14890be1812ba7b; R257-2 at 26353960ae2763cc09741d0f7bcc720621bd5148, an ancestor untouched in this scope |
| RTL | CLEAN | Not touched by the delta: `git diff --raw 26353960..015edd9a` has no hdl/, gitlink, Makefile, owned_process.py or run_all_suites.sh change (receipts/01). R257-2 examined the gptp_shadow Makefile SRCS/VFLAGS and the owned_process.py state machine, with the real build at 309/309 | R257-2 | 26353960ae2763cc09741d0f7bcc720621bd5148 (ancestor; nothing in RTL scope changed since, receipts/01) |
| Robustness | CLEAN (SUGGESTION R257-3-S1) | Changed artifact as a sweep preflight gate: flock-less host (receipts/12), concurrency and load (13), nesting under the real entry with SUITE_SWEEP_LOCK exported (20), runtime (13, 31), fixture lock isolated from the real tree (test_suite_cancellation.py:104-105,231). Unchanged production robustness: R257-2 receipts/10, 12, 13, 21, 22, 30, 40a, 41, 42 | R257-3 (delta); R257-2 (unchanged production files) | 015edd9ab2248289ff000f6ef14890be1812ba7b; R257-2 at 26353960ae2763cc09741d0f7bcc720621bd5148, an ancestor untouched in this scope |
| Tests | CLEAN | scripts/test_suite_cancellation.py:1-395 at this head; 20 mutants plus an unmodified copy against the parent and head tests (receipts/10, 11, 14); normal-entry ownership (20); repeatability (13, 31); lifecycle import (30); idiom, fail-fast and test-evidence gates (gates/). The unchanged tests (test_mutant_lifecycle.py, process_test_support.py) pass at this head (30, 31) | R257-3 | 015edd9ab2248289ff000f6ef14890be1812ba7b |
| Docs | CLEAN (SUGGESTIONS R257-3-S1, R257-2-S6) | Test docstrings, comments and PASS line (test_suite_cancellation.py:23-24,109-127,211-242,387-390) against owned_process.py:294 and run_all_suites.sh:122-133; TESTING.md:210-256 unchanged and now backed at 212, 237 and 239; docs gates (gates/); issue A195 REVIEW READY and correction-a195 integrity (61); PR body (stale head, S6). Unchanged docs: R257-2 | R257-3 | 015edd9ab2248289ff000f6ef14890be1812ba7b |

No finding was moved to another Issue.

## Real limits

- **Not run** (not permitted): the full parent, PP, gPTP, Yosys and builder banks; Docker/act; host act_ci or its selftest; hardware. Physical calibration NOT RUN; field skips are not hardware proof.
- **Synthetic parts.** Mutation and entry probes ran in `git archive` copies (`scripts/`, plus `tb/verilator/` and `syn/yosys/` for the entry probe). The fixtures use the test's own synthetic `make` and stubbed prerequisites, and the entry probe used a PATH `make` guard.
  - The flock-less host was emulated with a PATH shadow on this Linux host. No real flock-less distribution was run.
- **Hosted.** Check-run conclusions only. The sweep writes its preflight output to a log file and prints it only on failure, so I did not confirm from job logs that the new arms ran on hosted runners.
- **Manager banks.** No public exact-head evidence was found (receipts/62).
- **Reviewer probe defect, disclosed.** My first mutation batch failed all 20 arms with a relative-path error in my probe ("can't open file"), before any test ran. I fixed it by resolving paths and reran into a fresh directory. Receipts/10 is that rerun.
  - Later, two edits were made to the probe script. Support for `name@k` repeat labels came after receipts/10, 11, 12 and 20. The `clear-before-lock` mutant was added before receipts/14. Neither changes the edit or verdict logic of earlier arms.
- **Shared host.** Load was 10-17 on 16 CPUs from unrelated work throughout.
  - Process containment used only this probe's own adopted descendants, through pidfds with start-time checks. Every probe reported none left over.
  - No process was selected by command line.
- **Normalisation.** Host path prefixes in receipts are replaced by `<packet>`, `<clone>` and `$HOME` (scripts/normalise.py). The scratch directory is unpublished.

## Pending manager duties

- Publish this report and packet.
- Publish exact-head evidence for the full source static/builder and native banks at `015edd9a`. The public tree at `9eea4205` carries `b5ce20ec` records only.
- The trusted serial act replica and exact-head hosted acceptance for `015edd9a`.
- **The internal review.** R256-3's POSITIVE ledger is at `26353960`, and this delta changes an artifact within its Tests scope. Under AGENTS section 7, that lens must be covered again at a head that includes `015edd9a` before the two-positive bar is met.
- The final current-dev candidate at the merge turn: source base `776bc77d`, live dev `ede8d48e`.
- Optional: R257-3-S1, and a refresh of the PR body to the current head.
- Maintainer-authorized merge, post-merge containment, and moving the card to Done.

## Receipts and scripts

Every published file is listed with its sha256 in MANIFEST.sha256. Scripts take the clone path and a scratch path as arguments:
- `verify_head.py`: integrity;
- `probe_report_mutations.py`: test power and the flock-less PATH arm (`PROBE_PATH_OVERRIDE`);
- `probe_entry_ownership.py`: normal-entry ownership;
- `run_gates.sh`: focused gates;
- `normalise.py`: path placeholders.

R257-3 FINISHED
