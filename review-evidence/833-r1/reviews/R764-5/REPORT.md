[R764] NEGATIVE - exact head a67eaf66c99b6b07c7ef206ad3489cb9555e00ca

Round R764-5, external independent review of issue #833 / PR #834. Head `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca`, tree `433c822f557ad40546a462a97a902b4a59d8f399`. Source base `1f29f189279f9fc0132f4918e47342b87d22f33a`. The reviewed delta is round 5, `c1b29617..a67eaf66`: five one-line commits with no trailers (`receipts/round5_commits.txt`). It touches `docs/testing/TESTING.md`, `scripts/process_test_support.py` and `scripts/test_suite_cancellation.py`. `scripts/owned_process.py` is byte-identical to `c1b29617` (`git diff --quiet` rc 0).

## Summary

- **The round answers what it set out to answer.** R764-4-F1 is resolved at its cause, and R764-4-S1, R764-4-S2 and R764-3-R1 are resolved too.
- **The committed list is exactly the published set.** It holds the 44 distinct mutated texts (43 mutants and `none`) that every published mutant reduces to. Each named control fails with its words at this head (`--mutants` rc 0).
- **Nothing was narrowed.** The new controls cost +0.9 s on the whole preflight.
- **The verdict is NEGATIVE for one new MINOR, R764-5-F1 (Tests, Docs).** I tried nine mutants of my own against the committed list. Three survive every owner control and the whole test, and each one breaks a line that `TESTING.md` states:
  - `:219` stable handles;
  - `:224` SIGKILL to every other descendant by 4 s;
  - `:232` a vanishing listing's 10 s.
- **This is the class rule the round adds at `TESTING.md:281`:** "A stated cleanup behaviour is one some control pins." It does not hold yet. The PR body also says `owner_stated_seconds` pins `TESTING.md:223-232`. It does not pin `:224` for a non-leaf, or `:232`.
- **The product is correct at this head on all three points.** A deterministic probe shows that. The gap is in the controls, not the code.

## Findings

**R764-5-F1 - MINOR - Tests, Docs - `scripts/test_suite_cancellation.py:657-811` (owner controls) and `scripts/process_test_support.py:266-414` (`MUTANTS`) vs `docs/testing/TESTING.md:219`, `:224`, `:232`, `:281`; PR body, Round 5, "The class" table row "The stated seconds ... `TESTING.md:223-232`"**

- **Authority and evidence.**
  - `TESTING.md:281` (new in this round): "A stated cleanup behaviour is one some control pins." The manager's round 5 ruling: a reviewer's mutant that survives and breaks a stated behaviour is a finding.
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
- **The mutants**, in `probe_mutants.py`, applied to a copy of `scripts/` exactly as `mutant_tree()` applies them. `receipts/own_mutants_matrix.log` has each mutant against all 10 owner controls and the whole `scripts/test_suite_cancellation.py`, with `none` green on all 11:
  1. `rv-vanishing-waits-30s-more`: `(owned or clock >= limit + REAP_SECONDS)` becomes `(owned or clock >= limit + 3 * REAP_SECONDS)` (`owned_process.py:290`).
     - It breaks `TESTING.md:232`: "A listing that dies inside every census waits 10 s more: under 44 s."
     - It is green on all 11. `owner_vanishing` (`:657-678`) has a 15 s wall bound with `REAP_SECONDS=0.3`, so a tripled wait passes. `owner_stated_seconds` (`:761-796`) never builds a listing that dies inside the census: its `_reap` is `set`.
  2. `rv-parent-spared-past-kill-all`: `elif clock < kill_all:` becomes `elif clock < kill_all or any(parent == pid and child in live ...)` (`owned_process.py:324`). A parent whose child outlives its SIGKILL is not sent SIGKILL until the verdict.
     - It breaks `TESTING.md:224`: "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell".
     - It is green on all 11. Every control's SIGKILL target is either a leaf or the guarded shell. In `owner_stated_seconds`, the trap command is a placeholder that `_live` never sees, so the shell has no live child once its window ends.
     - #833's own evidence shows children in state D for up to 2.07 s after SIGKILL. That is exactly the case where this mutant changes behaviour.
  3. `rv-signal-by-number`: `_send` still opens the pidfd and rechecks the start time. It then signals with `os.kill(pid, ...)` instead of through the handle (`owned_process.py:250-251`).
     - It breaks `TESTING.md:219`: "Stable process handles prevent signalling reused numeric identities." The PR body maps that line to `owner_reused_identity`.
     - It is green on all 11. `owner_reused_identity` (`:799-810`) pins only the start-time recheck: `no-start-recheck` is red there. It does not pin that the signal goes through the handle.
- **Deterministic proof of effect.** `receipts/probe_effect.log` comes from `probe_effect.py` and `run_effect.py`. It uses the head's own `starved_clock` and `starved_cleanup` at production constants, where pass n is at (n - 1)/2 s:

  | Tree | Vanishing listing: verdict | Placeholder parent of a live child: SIGKILL | `_send` when the process exits after its check |
  |---|---|---|---|
  | head (`none`) | pass 49, 24.0 s (14 + 10, as `:232` states) | pass 9, 4.0 s (as `:224` states) | through the handle: returns, nothing raised |
  | `rv-vanishing-waits-30s-more` | pass 89, 44.0 s | pass 9 | handle |
  | `rv-parent-spared-past-kill-all` | pass 49 | not until the verdict, pass 29 | handle |
  | `rv-signal-by-number` | pass 49 | pass 9 | `ProcessLookupError`: it signalled the number after the process was gone |

  Each scenario takes milliseconds.
- **Impact.**
  - A regression to any of the three would pass the preflight and the committed `--mutants` campaign, while `TESTING.md` says the behaviour holds and `:281` says some control pins it.
  - `rv-signal-by-number` reopens the PID-reuse race that the handle exists to close, between the identity check and the signal.
  - `rv-parent-spared-past-kill-all` keeps a parent alive for the whole REAP window behind a child in state D.
  - The PR body's class table claims `owner_stated_seconds` pins the stated seconds at `TESTING.md:223-232`. For `:224`'s non-leaf SIGKILL and for `:232`, it does not.
- **Required outcome.** For each of the three, one of these:
  - a control that is red under the mutant, green unmutated, and whose words appear in the `MUTANTS` entry; the mutant joins `MUTANTS` with its named control;
  - or the statement (`TESTING.md:219`, `:224` or `:232`) is narrowed to what is pinned. In that case, also correct the PR body's class-table row `:223-232`.

  Both the vanishing and the parent case fit the existing starved-clock harness at sub-second cost. Shapes are not prescribed.
- **Verification.**
  - `python3 scripts/test_suite_cancellation.py --mutants` passes, with the three as new entries.
  - `python3 -I probe_mutants.py <clone> 8` from this packet shows each of the three red on at least one owner control.
  - `none` stays green, and no other row of the round 5 table changes.

**R764-5-R1 - RESIDUE - Docs, Tests - `scripts/test_suite_cancellation.py:772-773`**

- The comment reads "A live process the census lists as the shell's child ... so it is a stubborn leaf. It is never signalled."
- Yet the control's expected events, at `:791`, include `(1, "SIGTERM", "child")` and `(5, "SIGKILL", "child")`. What is true is that `send` is replaced, so nothing is delivered.
- Wording only.
- **Exact fix:** "It is never really signalled: this control's send only records the signal."

**R764-5-S1 - SUGGESTION - Tests, Docs - `scripts/process_test_support.py:266-414`**

Three more of my mutants survive every control and the whole test (`receipts/own_mutants_matrix.log`). Each changes a behaviour that only a product comment states, not `TESTING.md`, so none is a finding under `:281`:
- `rv-no-sigcont-after-send`: no SIGCONT after a signal (`owned_process.py:251`), so a stopped descendant cannot act on SIGTERM during grace.
- `rv-sigterm-to-new`: SIGTERM also goes to descendants new since the first census during grace (`:320-323`, "Let terminal traps run their cleanup commands during grace").
- `rv-no-leaf-first`: parents are no longer spared for their stubborn leaf until grace + 1 s (`:325-327`, "Kill stubborn leaves first").

Optional: list them in `MUTANTS` with "none, and why", or state and pin them, so the next reviewer sees that they were considered.

Four more of my mutants are red on a control. `rv-clock-always-cap` is red on `shell_window`, `stated_seconds` and the whole test. `rv-killed-not-recorded` is red on `survivor` and the whole test. `rv-vanishing-waits-no-more` is red on `late_exit` and the whole test. The list may take these too.

## Manager-ruled checks

1. **Every published mutant is listed and red on its named control, with its words.**
   - I ran the author's published collector, `author-r5/receipts/tools/collect.py` from the evidence tree `ca3539ba`, against this head's `owned_process.py`. Its output is byte-equal, as JSON, to the published `collected.json`: 131 source mutants, 44 distinct texts, 0 not applicable (`receipts/collect.out`).
   - My own `compare_list.py` applies every committed `MUTANTS` entry to the head and hashes the result. The 44 committed texts equal the 44 published texts one to one, with none missing, none extra and no duplicates (`receipts/compare_list.log`, rc 0).
   - The collector skips only entries whose target is the lifecycle test. Those are `M13-cleanup-does-nothing-lifecycle` and its controls, the same text as the listed `cleanup-does-nothing`.
   - The other published probe scripts mutate the test or run the product unmutated: `R763-1/trapcmd_variant.py`, `R763-4/early_resume_probe.py` and `resume_margin.py`, `R764-1/probe_owner.py`, `R764-4/builtin_phase_probe.py`.
   - `python3 scripts/test_suite_cancellation.py --mutants --jobs 8` gives rc 0: "owned-process mutants: PASS (43 mutants, 42 with a control that must fail)". `none` is green on all 10 controls (`receipts/committed_mutants.log`).
   - The equivalence argument for `sigterm-checks-parent` is sound. Pass 1 builds `initial` from that same census (`owned_process.py:286-287`), so the parent check can only refuse a SIGTERM already in `notified`.
2. **R764-4-F1: `shell-window-one-pass` is red.**
   - In the committed campaign it fails with "the resumed shell was killed inside its own window, with no child to spare it". `shell-window-1s` fails with the same words.
   - Repeated 6 times each, 24 runs at 16 at once (`receipts/repeat_shell_window.log`): both mutants red 6 of 6 at 4.0 to 4.4 s, and the unmutated control green 6 of 6 at 4.6 to 4.7 s.
   - These stay red in the campaign with their words: `no-shell-window*`, `no-trap-window`, `root-killed-unresumed`, `shell-killed-when-resumed` and `trap-commands-*`.
   - The trap's `read -t 0.3 <> idle` on a FIFO opened read-write is a builtin wait with no child. So `owned_process.py:329` cannot spare the shell there, and only `:317` can.
3. **`owner_stated_seconds` pins the stated seconds, except as F1 says.**
   - On the starved clock, pass n is at (n - 1)/2 s. Grace is pass 5 (2 s). The survivor verdict is pass 29 (14 s, `:225`, `:229`). The resume is pass 12 (5.5 s). The shell and its trap command get SIGKILL in pass 32 (15.5 s = resume + 10, `:226`, `:230`). The verdict is pass 52 (25.5 s = resume + 20, `:230`). "At or past" is exact (`:233`), and the cap is 0.5 s (`:228`, `:234`, `:269`). `TESTING.md:278-279` states exactly this.
   - The docstring arithmetic is correct. The placeholders 2^22 + 1 to 2^22 + 4 lie above the kernel's maximum `pid_max` of 2^22.
   - `pass-cap-1s`, `windows-2s`, `reap-window-2s` and `killed-counts-as-gone` are red there with their words.
   - Not pinned: `:224` for a non-leaf, and `:232`. See F1.
4. **Nothing was narrowed.**
   - The `TESTING.md` diff only strengthens `:272` ("in that pass") and `:275` ("even in that pass"), and adds `:274` and `:278-285` plus the campaign row at `:309`.
   - The three changed control docstrings (`owner_reparented`, `owner_shell_window`, `owner_late_cancel`) each add a clause and drop none.
   - `:281` states the rule, but it is not yet true (F1).
5. **Preflight cost.**
   - Per control, 3 runs at load 48 to 49 (`receipts/control_cost.txt`):
     - `owner_shell_window` 4.27 to 4.69 s (the author measured 3.3 s at `c1b29617`);
     - `owner_stated_seconds` 0.11 to 0.14 s;
     - `owner_reused_identity` 0.09 to 0.11 s;
     - `owner_reparented` 0.21 to 0.26 s;
     - `owner_late_cancel` 0.92 to 0.94 s.
   - Whole test, 4 runs at each head, 8 at once at load 45 to 47 (`receipts/preflight_cost.log`): head mean 60.0 s against `c1b29617` mean 59.1 s, all rc 0. So the preflight grows by about 0.9 s, within the author's "about 1.5 s".
   - The `--mutants` campaign is an explicit target, listed at `TESTING.md:309`, not part of the default preflight.
6. **R764-4-S1 margin, and R764-3-R1.**
   - Each pass adds `min(now - last, 0.5)` (`owned_process.py:284`), and `now - last` includes `time.sleep(0.02)` (`:339`). So pass n is at least 0.02 (n - 1) s on the owner's clock.
   - The control lets the child's SIGKILL through from pass 61 (`len(passes) < 61` refuses it before then). The resume needs the child dead (`:303-304`), so it comes at pass 62 or later: at least 1.22 s, past `deadline + 1.0` = 1.2 s (`:327`).
   - The margin is derived, not measured, and cannot be lost to stalls. The comment at `:582-584` states this.
   - R764-3-R1: `:683` now reads exactly "A re-armed window would hold the verdict past the 15 s bound below: TRAP_SECONDS is 30 s."

Matrix spot-check with the committed driver (`receipts/matrix_spotcheck.log`, rc 0, 61 s at 16 jobs). These three rows equal the PR body's Round 5 table:
- `send-checks-parent`: red on `reparented`, `stated_seconds` and the whole test;
- `resume-while-listed`: red on `late_cancel` and the whole test;
- `pass-cap-1s`: red on `stated_seconds` and the whole test.

`none` is green on all 11.

**Comment rule.** I grepped the added lines of the delta for reviewer IDs, lane labels, round names and issue-comment IDs. The new source comments state behaviour and reason, with #833. No new instance was found. `TESTING.md:284` "the next reviewer's mutant" is a role word in a doc, not an ID.

## Prior findings at this head

| Finding | Severity | Status at `a67eaf66` | Evidence |
|---|---|---|---|
| R764-4-F1 (resumed shell's window pinned only for the resume pass) | MINOR | **RESOLVED at cause** | Check 2: red 6/6 under both window mutants, and the unmutated control green 6/6. `TESTING.md:274` and the docstring at `:553` match what the control pins |
| R764-4-S1 (0.3 s wall-time margin) and R763-4-S1 (same) | SUGGESTION | **RESOLVED**: derived, not widened | Check 6 |
| R764-4-S2 and R763-3-S1 (the "listed" half of the resume condition) | SUGGESTION | **RESOLVED** | `resume-while-listed` is red on `owner_late_cancel` ("a cancel after the shell was collected resumed it"); the census lists the shell in its collecting pass (`:704-707`) |
| R764-3-R1 (`:683` "this bound") | RESIDUE | **TAKEN, exact fix** | Check 6 |
| R763-2-S1 and R764-1-S1 (10 s values unpinned); R764-2-S1 (0.5 s cap pinned only below about 1.5 s) | SUGGESTION | **RESOLVED** | `windows-2s`, `reap-window-2s` and `pass-cap-1s` are red on `owner_stated_seconds`. The vanishing listing's 10 s is the new F1 |
| R763-4-X1 (`TESTING.md:224`'s exception list omits the commands a resumed shell's trap started) | RESIDUE (other review) | **Retained, not taken**; the PR body's Round 5 section does not mention it | `:224` is unchanged. Exact fix as published: "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell and any command its trap started, which keep the shell's own window." It does not interact with F1's `:224` mutant, which concerns a parent of a live child |
| R763-2-S2 (manager actions R763-1-S1/S2), R763-2-S3 (census-cost comment `owned_process.py:84`) | SUGGESTION | Retained, optional | `owned_process.py` is unchanged |
| R763-3-F1, R763-2-F1 = R764-2-F1, R763-2-X1/X2, R764-2-R1/R2, and the round 1 findings | various | Resolved in earlier rounds; the delta does not touch what they depend on | `owned_process.py` is byte-identical; all rows from the earlier tables are red on their named control in the campaign |

## Lens results

```text
[R764] PASS Conformance - scripts/owned_process.py (byte-identical to c1b29617; 240-339 read against TESTING.md:219-235,269-280); receipts/probe_effect.log (head row) - the head does what TESTING.md:219, :224 and :232 state (handle-only signalling, SIGKILL to a parent of a live child in pass 9 = 4.0 s, vanishing verdict 24.0 s); issue #833 acceptance 1-2 unchanged because the product is unchanged; the round changes no requirement or interface
[R764] PASS RTL - git diff --stat c1b29617..a67eaf66 (3 Python/Markdown files) and receipts/restore_check.txt (gitlinks identical to 1f29f189) - no HDL, constraint, synthesis or submodule change; the cleanup state machine is unchanged
[R764] PASS Robustness - scripts/test_suite_cancellation.py:552-603,719-811; receipts/repeat_shell_window.log, receipts/preflight_cost.log, receipts/control_cost.txt - product unchanged; the new and changed controls are deterministic under 16-way load at host load 45-112 (unmutated green 6/6, whole test rc 0 4/4); the starved clock is restored before the owner's own cleanup on exit; the 61-pass hold is derived
[R764] MINOR Tests - scripts/test_suite_cancellation.py:657-811, scripts/process_test_support.py:266-414 - R764-5-F1 (three surviving mutants of stated behaviour); everything else in the delta checked green: receipts/committed_mutants.log, compare_list.log, matrix_spotcheck.log
[R764] MINOR Docs - docs/testing/TESTING.md:219,224,232,281; PR body Round 5 class table - R764-5-F1 (":281 A stated cleanup behaviour is one some control pins" and the ":223-232" pinned claim are wider than the controls); RESIDUE R764-5-R1; retained RESIDUE R763-4-X1
```

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `owned_process.py:240-339` vs `TESTING.md:219-235,269-280`; issue #833 acceptance; `receipts/probe_effect.log` | R764-5 | `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca` |
| RTL | CLEAN | `git diff --stat c1b29617..a67eaf66`; `receipts/restore_check.txt` (gitlinks) | R764-5 | `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca` |
| Robustness | CLEAN | `test_suite_cancellation.py:552-603,719-811`; `receipts/repeat_shell_window.log`, `preflight_cost.log`, `control_cost.txt` | R764-5 | `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca` |
| Tests | UNCLEAN (R764-5-F1 open) | `test_suite_cancellation.py:459-811,818-881`; `process_test_support.py:261-487`; `receipts/committed_mutants.log`, `own_mutants_matrix.log`, `compare_list.log`, `matrix_spotcheck.log`, `probe_effect.log` | R764-5 | `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca` |
| Docs | UNCLEAN (R764-5-F1 open; residue R764-5-R1 and R763-4-X1) | `TESTING.md:212-309`; the PR body's Round 5 section as fetched at review | R764-5 | `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca` |

## Limits

- I did not run the full `--matrix` (506 runs). I spot-checked three rows, plus `none` on all 11 targets.
- I did not run, at this head:
  - every `run:` step of `docs.yml`;
  - `behave`;
  - `make -C tb/verilator/gptp_shadow lifecycle`;
  - any builder leg or the full sweep.

  For those, source-head evidence is the author's published gate receipts. I did not re-verify them beyond `git diff --check 1f29f189 HEAD` (rc 0).
- I ran no probe in a user or PID namespace. The mutant runs used the committed driver's own owner containment, and the probe set-ups used placeholder PIDs.
- The host load was 45 to 112 on 16 CPUs while I worked.
- For list completeness, I ran the author's published collector and then cross-checked its output independently by mutated-text hash. I did not re-parse all 131 sources by hand. I read the R764-4, R763-4 and R764-3 sources and the remaining probe scripts to check what the collector skips.
- No hosted context exists at the exact head: 0 check runs, 0 statuses, 0 workflow runs (`receipts/hosted_checks.txt`, `hosted_runs.txt`).
- Physical calibration NOT RUN. Field skips are not hardware proof.
- No manager source bank ran at this head, and none is claimed.
- After the probes, the clone is at exact head bytes. Index and HEAD listing hashes are equal, every tracked blob re-hashes to its index entry, no modes changed, there are no untracked or ignored files, and the six gitlinks equal `1f29f189`'s (`receipts/restore_check.txt`).

## Pending manager duties

- Carry R764-5-F1 to the author. Tests and Docs re-cover at the corrected head.
- Residue checklist: R764-5-R1 and R763-4-X1, with their exact fixes above.
- Optional: R764-5-S1, R763-2-S2 and R763-2-S3.
- Hosted exact-head `rtl-fast`, `verilator-suites` and `yosys-portability`, and the act replica, are the manager's.
- So is the current-dev merge candidate: source base `1f29f189`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`, builder and native banks, at the merge turn.

R764-5 FINISHED
