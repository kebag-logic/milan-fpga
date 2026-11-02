[R764] NEGATIVE - exact head 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c

# R764-2 external review: issue #833 / PR #834, round 2

- Head under review: `1ff8292cd5b761633ef9500a7c5a4b1626a3d92c`, tree `66b77844947516b36de065ed3275efb3ba091e42` (matches the PR's published `headRefOid`).
- Previously reviewed head: `d4d8cff92658e57b11090c97daf7b44edb31b3b6` (R764-1, NEGATIVE, MINOR findings only).
- Round 2 delta `d4d8cff9..1ff8292c`: five commits touching `docs/testing/TESTING.md` (+15 -4), `scripts/process_test_support.py` (+10 -2) and `scripts/test_suite_cancellation.py` (+30 -15). `scripts/owned_process.py` is byte-identical to round 1.
- Source base `1f29f189279f9fc0132f4918e47342b87d22f33a`; live `dev` `503bc97cd4f24ad07596c17e7188f2024617972d` is the manager's merge-candidate base, not validated here.

## Verdict basis

One open MINOR (F1), so the verdict is NEGATIVE. Every round 1 finding of mine is resolved as written (table below). Both new controls go red when their fix is reverted, at this head. F1 is the one new defect.

The derived worst case that round 2 states in three places assumes "That resume comes before 14 s". That premise does not hold when cancellation arrives during cleanup, after the command has already exited. The resume can then come up to 24 s into cleanup, and the stated bounds are exceeded:

- 50.03 s and 53.94 s for the listing that dies inside every census (stated "under 44 s");
- 40.06 s for a real survivor (stated 14 s, or "under 34 s").

My own round 1 derivation (R764-1-F3) stated the same premise. So this gap was already in the required outcome that round 2 met. It is reported here as new, not as a lapse by the author.

## Checks requested

### (1) TESTING.md states the cleanup stages and the owner's clock the head enforces: resolved

`docs/testing/TESTING.md:223-228`, read against `scripts/owned_process.py:37-45,260-336`:

| Statement | Code |
|---|---|
| 2 s of `SIGTERM` | `GRACE_SECONDS` |
| 2 s later `SIGKILL` reaches every other descendant | `kill_all = deadline + KILL_ALL_SECONDS` |
| fails ten seconds after that | `limit = kill_all + REAP_SECONDS` |
| a late-resumed shell's ten seconds | `kill_all = max(kill_all, clock + TRAP_SECONDS)` |
| the owner's clock, advanced by at most 0.5 s a pass | `clock += min(now - last, MAX_PASS_SECONDS)` |

R2 below records one wording residue at line 224.

### (2) A true survivor's deadline: derived and stated identically, but the worst case is not included (F1)

`TESTING.md:229-235`, `scripts/process_test_support.py:19-30` and the PR body's "The deadline's derivation" say the same thing:

- 14 s;
- 20 s after a resume, under 34 s;
- under 44 s for the listing;
- plus at most one 0.5 s pass.

Each figure is correct when the resume comes before 14 s, and the author's probes confirm that case (14.02, 22.03, 33.51, 33.92 s; listing 24.01 s; spot-checked in `author-r2/receipts/bounds/at-head/*.log`). My control probe reproduces the no-cancel listing at 24.01 s (`receipts/probes/late-cancel-none.log`). The premise fails for a cancellation during cleanup: see F1.

### (3) The resumed shell's trap-started command control goes red with its fix reverted: resolved

`scripts/test_suite_cancellation.py:542-579` adds `sleep 1.5 && echo ran > trap-command-ran` to the trap. `sleep` is an external command, and 1.5 s is longer than the 1 s such a command had on `dev`: `git show 1f29f189:scripts/owned_process.py` line 226 reads `now < resumed + 1.0`. The comment's reason checks out too: the sweep's EXIT trap does run `rm` (`scripts/run_all_suites.sh:236-238`).

At this head:

| Run | Result |
|---|---|
| M07 (skip removed) | red: "the resumed shell's trap command was killed inside the shell's window" |
| M07b (my new mutant: the `dev` rule of a 1 s window) | red, same words |
| Both unmutated controls | green: `owner-shell-window: {'trap_ran_after_kill_time': True, 'trap_command_ran': True}` |

### (4) The stall control keeps the product's 10 s window after SIGKILL and catches a stall charged in its own pass: resolved

`scripts/test_suite_cancellation.py:505-539`:

- `stages()` no longer overrides `REAP_SECONDS`, so the child's death after `SIGKILL` has the product's 10 s.
- With `GRACE_SECONDS=1.5`, the cap holds passes 1 and 2 to at most 1.0 s of owner clock, whatever the host load. So `SIGKILL` can come no earlier than pass 3 unless the 2.0 s stall was charged in full. The control is deterministic, not timing-sensitive.

Reds at this head, all with "the stall was charged in full: SIGKILL in pass [2]":

- M03 (wall clock);
- M04 (cap 5 s);
- M04c (my new mutant: cap 1.5 s).

M04d (cap 1.0 s) stays green, as the arithmetic predicts; see S1. Unmutated control: `killed_in_pass` 52.

### (5) The command-table statement in the PR body: resolved

I re-ran each named command at this head:

| Command | Result | Receipt |
|---|---|---|
| `command_table_staleness.py . 1f29f189 d4d8cff9 HEAD` | `pins 149 stale 34 absent 1` on `dev`; `stale 38` at round 1's head and at this head; the 4 extra are this PR's 4 scripts | `receipts/command-table-staleness.txt` |
| `git grep -l -e command-table.json -e ci_command_table HEAD` | 14 files | `receipts/command-table-readers.txt` |
| none of the 14 named in `.github/workflows` or `scripts/run_all_suites.sh` | 0 matches | `receipts/command-table-readers.txt` |

The PR body shows only what these commands print.

### (6) Residue rows: resolved

- **R764-1-R1:** both before cells now read "all at the fixture's 12 s hang bound, none `CLEANUP FAILED`".
- **R764-1-R2:** `TESTING.md:270` is the exact wording I asked for.

### Mutation table, re-run at this head

Each mutant ran in its own fresh clone and its own user+PID namespace. Driver: `scripts/mutate_r2.py`, which is round 1's driver plus M04c, M04d and M07b. The full table with log paths is in `receipts/mutation-table.md`.

| Fix | Mutant | At 1ff8292c |
|---|---|---|
| Identity by start time | M01, M01b (each half) / M01c (both) | green, green / **red** (as in round 1: each half covers the other) |
| Reap after census | M02 | **red** |
| Owner's clock | M03 wall clock / M04 cap 5 s / M04c cap 1.5 s / M04d cap 1.0 s | **red** / **red** / **red** / green (S1) |
| Resumed shell's window | M05 / M06 | **red** / **red** |
| Trap command shares the window | M07 none / M07b 1 s | **red** / **red** |
| SIGKILL before failing | M08 / M09 | **red** / **red** |
| Endless listing bounded | M10 | **red** |
| Survivor fails | M11 | **red** |
| Report states state | M12 | **red** |
| Cleanup does nothing | M13 suite / lifecycle | **red** / **red** |
| Start-time recheck (pre-existing) | M14 | green (probe, as round 1) |
| 10 s windows themselves | M15 | green (R764-1-S1, declined with reason) |
| Unmutated | control-A, control-B, control-lifecycle | green, green, green |

Harness note. The first run of the suite entries that reach `hard_stop(HUP)` (control-A/B, M01, M01b, M04d, M14, M15) timed out at the 60 s fixture bound in `hard-HUP`. My launcher had started them under a SIGHUP-ignoring wrapper, so a HUP could not end the driver. This is the same artifact as the author's published `mutations-r764-driver-hup-ignored-attempt/`. I re-ran those entries, plus M10 and M11, under a launcher whose ignored-signal mask excludes SIGHUP (`SigIgn 0x4`): all green, or red as listed (`receipts/mutations-rerun/`). The first-run logs are kept in `receipts/mutations/`. Every other first-run entry went red at its own assertion before reaching `hard_stop`.

### Comment rule

Added lines in the delta contain no lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs; the only IDs are `#833`. Commits are one line with no trailers.

## Findings

**F1 - MINOR - Conformance, RTL, Robustness, Docs - `docs/testing/TESTING.md:229-232`, `scripts/process_test_support.py:21-30`, PR body ("The deadline's derivation"; Known limitations "fails the run under 34 s of owner clock (44 s for a listing ...)"), behaviour at `scripts/owned_process.py:289-310` - the stated worst case omits a cancellation that arrives during cleanup**

- Evidence (code):
  - `owned_process.py:290` fails the run at `limit` only while `owned` is non-empty. With a listing that dies inside every census, `owned` stays empty, so no verdict comes before `limit + REAP_SECONDS` = 24 s.
  - `_cancel` (`:187-195`) sets `root_notified` whenever it arrives, including during `_cleanup()` after the command has exited and been collected. `run()` keeps `root_fd` open until cleanup ends (`:366-372`).
  - In the next pass, `live - {root_pid}` is empty, so `:304-310` resumes and sets `kill_all = clock + TRAP_SECONDS`. That moves `limit` to `clock + 20` and the listing verdict to `clock + 30`, with `clock` anywhere below 24.
  - So the premise "That resume comes before 14 s" (`TESTING.md:231`, `process_test_support.py:23-24`, PR body) is false on this path.
- Evidence (measured, production constants, every pass under 0.02 s, so the owner's clock equals wall time):

  | Probe | Cancellation at | Verdict at | Stated |
  |---|---:|---:|---|
  | `receipts/probes/late-cancel-none.log` (control) | none | 24.01 s | under 24.5 s |
  | `receipts/probes/late-cancel-20.log` | 20.01 s | **50.03 s** | under 44 s |
  | `receipts/probes/late-cancel-23.9.log` | 23.92 s | **53.94 s** | under 44 s |
  | `receipts/probes/late-cancel-survivor-20.log` | 20.02 s | **40.06 s**, for a real descendant started at 21.03 s, "sent SIGKILL 19.01 s ago" | 14 s for a true survivor; under 34 s after a resume |

  The probes use the same planted listing as the `owner_vanishing` control, so whether a real sweep reaches the listing state is not shown here. That the stated bound fails once it is reached is shown.
- Impact:
  - The authoritative worst case for cleanup is understated by up to 10 s (54 s, not 44 s).
  - A survivor can be judged 19 s after its `SIGKILL`, not 10 s.
  - `process_test_support.py`'s "both inside this bound" becomes 53.94 + 0.5 + 15.1 = 69.5 s against `FINISH_SECONDS = 60`. In that ordering the fixture's hang bound can fire before the owner's own state report. That loses the report but does not create a false pass.
  - This changes figures, so it is not RESIDUE.
- Required outcome: one of these.
  - (a) The code makes the stated bounds true. For example, a resume extends the deadlines only while the notified shell is still owned, since a collected shell has no trap left to run.
  - (b) The three statements derive the bounds including this ordering:
    - on the listing branch the resume comes before 24 s;
    - a survivor's deadline is then under 44 s, and the listing's under 54 s;
    - `FINISH_SECONDS`'s justification is restated or the bound changed.

  Either way, the three places stay identical.
- Verification: `python3 -I scripts/probe_late_cancel.py <clone> 20`, the same with `23.9`, and `scripts/probe_late_cancel_survivor.py <clone> 20`. Each verdict must lie within the stated bound. Under (a), also re-run the mutation table: no row may change, and M05, M06, M07 and M07b must stay red.

**R1 - RESIDUE - Docs - PR body, "The deadline's derivation", third sentence**

"A true survivor still fails the run, where it was 4 s: A true survivor's deadline is 14 s into cleanup on the owner's clock." This repeats its subject and capitalises after a colon. Exact fix: "A true survivor still fails the run, as it did at 4 s before this change. Its deadline is now 14 s into cleanup on the owner's clock." (If F1 is fixed under option (b), the following figures change with it.)

**R2 - RESIDUE - Docs - `docs/testing/TESTING.md:224`**

"Two seconds later `SIGKILL` has reached every other descendant." A cancelled shell that has not been resumed is held back from it (`owned_process.py:315-316`). It receives `SIGKILL` only on the failure path (`:297-298`), which line 274 states. Exact fix: "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell, which keeps its own window."

**S1 - SUGGESTION - Tests - `scripts/test_suite_cancellation.py:514-536`**

The stall control pins the cap only below about 1.5 s per pass: M04d (cap 1.0 s) is green. `TESTING.md:228,269` state half a second. The control does catch what it claims, a stall charged in full. If the 0.5 s figure itself should be pinned, a second stalled pass (or a 0.6 s grace with a 0.7 s stall) would turn a cap above 0.5 s red, at about 1 s of preflight.

## Prior findings (R764-1) at this head

| ID | Status at 1ff8292c | Evidence |
|---|---|---|
| R764-1-F1 (MINOR, Docs) | Resolved | `TESTING.md:223-228` against `owned_process.py:37-45,260-336`; check (1) |
| R764-1-F2 (MINOR, Tests, Docs) | Resolved | M07 and M07b red, controls green; check (3) |
| R764-1-F3 (MINOR, Docs, Robustness) | Resolved as written: the stated figures are in all three places and are true when the resume comes before 14 s. Its cause, the worst case included, is not fully closed. Carried as F1, because round 1's own derivation shared the premise | check (2), F1 |
| R764-1-F4 (MINOR, Docs) | Resolved | check (5) |
| R764-1-R1, R2 (RESIDUE) | Resolved | check (6) |
| R764-1-S1 (SUGGESTION) | Declined with a stated reason (pinning the 10 s value would add about 10 s of preflight). Accepted | PR body, Suggestions |
| R764-1-S2 (SUGGESTION) | Receipt published and spot-checked: 1,403 processes, 200 rounds, median 17.4 ms against 37.6 ms on `dev` | `author-r2/receipts/census/census-cost.log` |

## Clean-lens evidence

```text
[R764] PASS Tests - scripts/test_suite_cancellation.py:405-416,505-579 at 1ff8292c; receipts/mutation-table.md, receipts/mutations/, receipts/mutations-rerun/ - the stall control is deterministic under load (cap bounds passes 1-2 to 1.0 s < 1.5 s grace) and red under M03, M04 and M04c; the shell-window control's trap runs an external 1.5 s command and is red under M07 and M07b; every round 1 red reproduces; control-A, control-B and control-lifecycle green; stages() restores the product constants and no longer shortens REAP_SECONDS; F1 is not attributed here because no fixture reaches the late-cancel listing ordering and FINISH_SECONDS asserts no property under test (S1 optional)
```

Conformance, RTL, Robustness and Docs are unclean at this head because of F1. Within each, everything other than F1 was applied and found clean:

- **Conformance:** #833 acceptance 1 (state in the message; M12 red) and acceptance 2 (a real fix with derived windows; `Relates to` correct while `Probe.ready`'s 15 s handshake remains).
- **RTL:** the delta has no HDL. `owned_process.py` is unchanged; it carries its round 1 verdict except for the late-resume path F1 names.
- **Robustness:** the stall control is now load-independent, and the trap-command window is pinned to more than 1 s.
- **Docs:** `TESTING.md:223-228,233-235,270,273` match the code. The PR body's command-table and before/after text are verified. `check_doc_style.py`, `check_py_idiom.py` and `docs_check.py` are rc 0 at this head (`receipts/gate-*.log`). R1 and R2 are residue only.

## Lens ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #833 body and acceptance; `owned_process.py:187-195,256-336`; `TESTING.md:223-235`; probes `receipts/probes/*` | R764-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| RTL | UNCLEAN (F1) | cleanup state machine `owned_process.py:256-336` (late-resume transition `:304-310`, verdict `:289-301`); no HDL in delta | R764-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| Robustness | UNCLEAN (F1) | cancellation during cleanup after command exit; stall control under load; trap command window; probes and mutants | R764-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| Tests | CLEAN | `test_suite_cancellation.py:405-416,505-579`; mutation table (24 entries) with rerun; lifecycle control | R764-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| Docs | UNCLEAN (F1; R1, R2 residue only) | `TESTING.md:223-273`; `process_test_support.py:17-30`; PR body (fetched at this head); doc gates | R764-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |

## Executed here (each with its own log and rc)

- Mutation re-run, 24 entries in 12 parallel jobs, each in its own clone and user+PID namespace (`receipts/mutations/`). Nine entries were re-run, 9 in parallel (`receipts/mutations-rerun/`).
- Late-cancel probes at production constants: none, 20, 23.9, and a survivor at 20 (`receipts/probes/`).
- `scripts/check_doc_style.py`, `scripts/check_py_idiom.py`, `scripts/docs_check.py`: rc 0.
- `git diff --check 1f29f189 HEAD`: rc 0.
- Command-table commands (`receipts/command-table-*.txt`).
- Evidence manifest: all 1,674 entries of `review-evidence/833-r1/MANIFEST.json` at `cf127b70` match their published blob sha256, 0 mismatches, 0 unlisted files (`receipts/evidence-manifest-check.txt`).
- Hosted checks snapshot (`receipts/hosted-checks-snapshot.txt`).
- Restore check: worktree, index and tree identical to `66b77844`, `write-tree` equal, 0 untracked files, all six gitlinks equal to HEAD (`receipts/restore-verification.txt`). Every mutant ran in a fresh clone; this checkout was never edited.

## Real limits

- No full sweep, builder, gPTP, PP or Yosys bank was run at this head. The author's sweep ran at `d4d8cff9`, not here.
- The evidence packet has a sha256 manifest, but I found no detached signature, and commit `cf127b70` is unsigned. Integrity was checked by hash only.
- The F1 probes plant the listing exactly as `owner_vanishing` does. I did not show a real sweep reaching it.
- The mutation runs shared a host at load average 9 to 15.
- Raw logs carry local absolute paths and need the manager's usual path redaction before publication.
- Hosted contexts at this head: `changes` passed; every other context was pending at the snapshot. No hosted or act evidence is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Merge-candidate validation on live `dev` `503bc97c` (builder and native banks), plus hosted and act acceptance at the exact head.
- Carry R1 and R2 to the residue checklist.
- R763-1-S1 and S2 (manager actions, per the PR body).
- Redact paths in published logs.

## Prior findings of the other round 1 review

I read these after the verdict and ledger above were fixed. They change neither.

| ID | Status at 1ff8292c | Evidence |
|---|---|---|
| R763-1-F1 (MINOR, Docs) | Resolved | same as R764-1-F1; check (1) |
| R763-1-F2 (MINOR, Docs) | Resolved as written: the stated figures are now "under 34 s" plus the listing. Its cause, the real worst case, is carried as F1: the late-cancel ordering extends it to under 44 s for a survivor and under 54 s for the listing | check (2), F1 |
| R763-1-F3 (MINOR, Tests, Robustness) | Resolved: `owner_stall` no longer shortens `REAP_SECONDS` (`test_suite_cancellation.py:518`), so the planted child's death has the product's 10 s, and `stages()`'s docstring says only what it does (`:407`). The wall-clock and pass-cap mutants stay red (M03, M04, M04c) | check (4) |
| R763-1-F4 (MINOR, Tests) | Resolved: the trap runs external `sleep 1.5`; the 1 s rule (M07b, equivalent to `trap-commands-1s`) is red | check (3) |
| R763-1-X1, X2 (RESIDUE) | Resolved: the before cells name the 12 s hang bound; "nothing reads it" is replaced by named commands and their output | checks (5), (6) |
| R763-1-S1, S2 (SUGGESTION) | Open as manager actions, per the PR body | Pending manager duties |

R764-2 FINISHED
