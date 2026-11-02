# #833 round 5 HANDOFF ([A726e])

Status: REVIEW READY, posted on #833 as issuecomment-6582095970 (`receipts/ready.md`). Base: round 4 head `c1b29617`. Head `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca`, 5 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6579710362 (`receipts/taken.md`).

Sources read: R764-4 (PR #834 issuecomment-6579673529, NEGATIVE, one MINOR) and its packet; R763-4 (issuecomment-6579452887, POSITIVE, no finding); every review packet R763-1..4 and R764-1..4 on `833-review-evidence` at `d519e1f3` (`receipts/review-evidence-fetch-head.txt`); round 1's own mutation table (`833-a726/receipts/load-tools/mutate.py`) and round 3's two own mutants (`833-a726d/receipts/tools/matrix3.py`).

## The finding

**R764-4-F1 (MINOR, Tests and Docs; R764-4 only. R763-4 is POSITIVE and has no matching ID).** `owner_shell_window` pinned only the resume-pass half of the guard at `scripts/owned_process.py:315-318`. After that pass, `:329` also spared the shell, because the trap's `sleep 1.5` was a live child. So `shell-window-one-pass` and `shell-window-1s` were green everywhere, and `TESTING.md:273` and the docstring claimed more than the control pinned.

**Change (commit `682dc31b`):** `scripts/test_suite_cancellation.py:552-603`. The trap now ends `read -t 0.3 <> idle; echo done > trap-finished` (`:556-565`). `idle` is a FIFO (`:558`) opened read-write, so `read` waits 0.3 s as a builtin, with no child. The new assertion at `:601` reads "the resumed shell was killed inside its own window, with no child to spare it". Docstring: "runs its whole trap". `TESTING.md:274`: "That holds through builtins after its last command, with no child left to spare it." This is R764-4's required outcome, option 1: a resumed shell past grace + 1 s spends census passes inside its trap with no live child, and its last trap step is observable.

**Control:** `owner_shell_window`, in the preflight (`main()` at `:827`, which calls it at `:836`). With R764-4's own `mutants.py`, `matrix.py` and `repeat_control.py`, unchanged, on a fresh clone of the head:
- Against R764-4's `receipts/matrix-table.md`, exactly two rows change. `shell-window-one-pass` and `shell-window-1s` are now RED(3/3) on `shell_window`. The second is the optional one.
- 16 runs each: `none` red 0/16; `shell-killed-when-resumed` 16/16; `shell-window-one-pass` 16/16 and `shell-window-1s` 16/16, with the words above.
- Receipts: `receipts/r764-4/`.

The class-wide answer is below. `owned_process.py` is byte-identical to `c1b29617`, and no mutant showed the product wrong.

## The class (manager rule, items 1-3)

**Collection.** 131 published mutants of `scripts/owned_process.py` reduce to 43 distinct mutated files, plus `none`:
- Both reviewers' R763-1..4 and R764-1..4 tables, round 1's own table, and round 3's own mutants.
- Each was applied to the head, and every edit still matches exactly once (`receipts/tools/collect.py`, `collected.json`).
- Equal mutated files are grouped, with every source name kept.
- Lifecycle-only entries (`M13`-lifecycle and R763-3's lifecycle probe) have the same edits and ran separately (`receipts/lifecycle/`, same result as round 4).
- R763-1's `trapcmd_variant.py` rewrites a control, not the product, so it is not a mutant.

**One driver.** The committed `python3 scripts/test_suite_cancellation.py --mutants [--matrix] [--jobs N] [NAME ...]` (item 3):
- It copies `scripts/` per mutant, applies its edits, and runs `--control NAME`, or with no argument the whole test, from that copy.
- The output goes to a file, so leaked descendants cannot hold the run open.
- The caller's `OwnedProcesses` collects whatever a mutant leaks.

The receipts runs:
- **Baseline at `c1b29617`**: the same driver code placed on the round 4 controls (`receipts/baseline-c1b29617/driver-on-c1b29617.diff`). It ran `--matrix`, each part in its own user+PID namespace.
- **Head `a67eaf66`**: `--matrix` in 3 parts, 506 runs, in namespaces (`receipts/matrix/`). Then the default mode, as a user runs it, with no namespace: rc 0 in 54.7 s, clone clean afterwards, and no leftover process.
- **`ff006178`**: the same runs (`receipts/matrix-ff006178/`). The cells are identical.

**Baseline greens.** At `c1b29617`, 10 mutants were green on every control and on the whole test:
- `shell-window-one-pass` and `shell-window-1s`: F1.
- `no-start-recheck`, `pass-cap-1s`, `windows-2s`, `reap-window-2s` and `killed-counts-as-gone`: each breaks a stated behaviour.
- `send-checks-parent` and `resume-while-listed`: each breaks a stated behaviour only within one pass.
- `sigterm-checks-parent`: equivalent.

**Decision per stated behaviour.** Every gap was strengthened and nothing was narrowed. Each change costs well under 1 s of preflight (cost in item 4).

| Gap | Stated where | Strengthened control (commit `682dc31b`) | Turns red |
|---|---|---|---|
| A late shell's window after its last child | `TESTING.md:273-274`, `owner_shell_window` docstring | `owner_shell_window` builtin tail, above | `shell-window-one-pass`, `shell-window-1s` |
| The stated seconds: grace 2 s, 10 s after SIGKILL, 14 s for a survivor, a late resume's 10 s window and its 20 s, 0.5 s a pass | `TESTING.md:223-232`, `:269`, new `:278-279` | New `owner_stated_seconds` (`:761-796`, helpers `:719-758`). Its pure census lists placeholder PIDs above any real PID, and `starved_clock` (`:719-731`) makes every pass take one second of the owner's clock, twice the cap. The production constants are checked pass by pass. Survivor: SIGTERM in pass 1, SIGKILL in pass 5, verdict in pass 29. Late resume: SIGCONT in pass 12; the shell and its trap command get SIGKILL in pass 32; verdict in pass 52 | `pass-cap-1s`, `windows-2s`, `reap-window-2s`, `killed-counts-as-gone`, and also most window, guard and verdict mutants. Words: "a survivor's stated seconds were not kept on the owner's clock" |
| A reused number is never signalled | `TESTING.md:219`, new `:280` | New `owner_reused_identity` (`:799-810`). `_send` with a wrong start time to a live `sleep` must return False and leave it running | `no-start-recheck`: "a census entry whose process was replaced was signalled" |
| SIGTERM to a re-parented descendant, in the pass whose census names its old parent | `TESTING.md:272` ("in that pass" added), docstring | `owner_reparented` notes the pass of the child's SIGTERM and requires pass 1 (`:459-487`) | `send-checks-parent` (it waited for pass 2): "the re-parented descendant's SIGTERM waited for a later census" |
| No window after the shell was collected, even when the cancel lands after that pass's reap | `TESTING.md:275` ("even in that pass" added), docstring | `owner_late_cancel` also lists the collected shell in the census, and the pass's reap returns it (`:704-707`) | `resume-while-listed` (it resumed the collected shell): "a cancel after the shell was collected resumed it". `no-reap-after-census` and `owned-is-census` also turn red here |

`send-checks-parent` and `resume-while-listed` were argued as harmless in earlier rounds. I pinned them rather than argue: each control costs nothing, and `resume-while-listed` can open a window when the cancel lands after the same pass's post-census reap. That is literally "after the shell was collected". This takes R763-3-S1 on its merits, which is also R764-4-S2's point. The stated seconds and the cap value are now pinned too, which answers the substance of R763-2-S1 and R764-2-S1.

**The one equivalent mutant.** `sigterm-checks-parent` (R764's `M01`) adds `initial.get((pid, start)) != _parent` before a SIGTERM. In pass 1, `initial` is built from that pass's census, so the parents are equal. Every descendant of the first census, except the notified shell (spared before this check) or one that pass 1 already finds past grace, is sent SIGTERM in pass 1. `notified` then suppresses every later SIGTERM to the same `(pid, start)`. A `(pid, start)` whose `_send` failed is gone or replaced, and a replacement is not in `initial`. So the check can refuse only a SIGTERM already sent. `MUTANTS` records it with that reason and no control.

**Artifacts, stated so nobody mistakes them for coverage:**
- On `stated_seconds`, `send-checks-parent` and the `identity-*` mutants that recheck `/proc` before sending are red only because its census lists placeholder PIDs that `/proc` does not have.
- Each has its genuine red elsewhere: `reparented`.

## Full mutant table

At the head `a67eaf66`, each mutant's named control is red with its words in the default campaign (`receipts/matrix/default.log`, rc 0). `none` is green on all 10 controls and on the whole test. Line numbers refer to `docs/testing/TESTING.md` at the head. `CUT` is the 150 s bound: `cleanup-does-nothing` on `late_exit` hangs at the control's own `child.wait()`, as in R763-1's table.

| Mutant | Published as | Breaks | Red at c1b29617 | Red at the head | Named control: failing words, or why none |
|---|---|---|---|---|---|
| `none` | every table's control | nothing | none | none | the product as it stands; every control passes |
| `cleanup-does-nothing` | R763-1/cleanup-does-nothing, R764-1/M13-cleanup-does-nothing-suite, R764-2/M13-cleanup-does-nothing-suite, R764-3/M13-cleanup-does-nothing-suite, A726/cleanup-does-nothing | every cleanup statement | reparented, late_exit, stall, shell_window, survivor, vanishing, late_cancel, whole | reparented, late_exit, stall, shell_window, survivor, vanishing, late_cancel, stated_seconds, whole | `reparented`: "re-parented descendant was treated as new and never got SIGTERM" |
| `identity-start-holds-parent` | R763-1/identity-includes-parent | `:272` a re-parented descendant keeps its identity | reparented, whole | reparented, whole | `reparented`: "re-parented descendant was treated as new and never got SIGTERM" |
| `identity-keys-hold-parent` | R763-2/identity-includes-parent | `:272` a re-parented descendant keeps its identity | reparented, whole | reparented, stated_seconds, whole | `reparented`: "re-parented descendant was treated as new and never got SIGTERM" |
| `identity-first-census-holds-parent` | R763-3/identity-has-parent | `:272` a re-parented descendant keeps its identity | reparented, survivor, whole | reparented, survivor, stated_seconds, whole | `reparented`: "re-parented descendant was treated as new and never got SIGTERM" |
| `identity-includes-parent` | R764-1/M01c-identity-includes-parent-both, R764-2/M01c-identity-includes-parent-both, R764-3/M01c-identity-includes-parent-both | `:272` a re-parented descendant keeps its identity | reparented, whole | reparented, stated_seconds, whole | `reparented`: "re-parented descendant was treated as new and never got SIGTERM" |
| `identity-checks-parent-before-send` | A726/identity-includes-parent | `:272` a re-parented descendant keeps its identity | reparented, whole | reparented, stated_seconds, whole | `reparented`: "re-parented descendant was treated as new and never got SIGTERM" |
| `sigterm-checks-parent` | R764-1/M01-identity-includes-parent, R764-2/M01-identity-includes-parent, R764-3/M01-identity-includes-parent | none (equivalent) | none | none | equivalent: the first pass sends SIGTERM to every descendant of the first census under the parent that census read, so this refuses only a SIGTERM already sent |
| `send-checks-parent` | R764-1/M01b-send-recheck-includes-parent, R764-2/M01b-send-recheck-includes-parent, R764-3/M01b-send-recheck-includes-parent | `TESTING.md:272` SIGTERM to a re-parented descendant in that pass | none | reparented, stated_seconds, whole | `reparented`: "SIGTERM waited for a later census" |
| `no-start-recheck` | R764-1/M14-no-start-recheck, R764-2/M14-no-start-recheck, R764-3/M14-no-start-recheck | `:219`, `:280` a reused number is never signalled | none | reused_identity, whole | `reused_identity`: "a census entry whose process was replaced was signalled" |
| `no-reap-after-census` | R763-1/no-reap-after-census, R763-2/no-reap-after-census, R763-3/no-reap-after-census, R764-1/M02-no-reap-after-census, R764-2/M02-no-reap-after-census, R764-3/M02-no-reap-after-census | `:271` a child exiting during a census is collected | late_exit, whole | late_exit, late_cancel, whole | `late_exit`: "CLEANUP FAILED: owned descendants remain" |
| `owned-is-census` | A726/no-reap-after-census | `:271` | late_exit, whole | late_exit, late_cancel, whole | `late_exit`: "CLEANUP FAILED: owned descendants remain" |
| `deadline-wall-clock` | R763-1/deadline-wall-clock, R763-2/deadline-wall-clock, R763-3/pass-unclamped, R764-1/M03-wall-clock, R764-2/M03-wall-clock, R764-3/M03-wall-clock, A726/deadline-is-wall-clock | `:228`, `:269` at most 0.5 s a pass | stall, whole | stall, stated_seconds, whole | `stall`: "the stall was charged in full" |
| `pass-cap-1s` | R764-2/M04d-clamp-1.0s, R764-3/M04d-clamp-1.0s | `:228`, `:269` | none | stated_seconds, whole | `stated_seconds`: "a survivor's stated seconds were not kept" |
| `pass-cap-1.5s` | R763-2/pass-cap-1.5s, R764-2/M04c-clamp-1.5s, R764-3/M04c-clamp-1.5s | `:228`, `:269` | stall, whole | stall, stated_seconds, whole | `stall`: "the stall was charged in full" |
| `pass-cap-5s` | R763-1/pass-cap-5s, R763-2/pass-cap-5s, R764-1/M04-clamp-5s, R764-2/M04-clamp-5s, R764-3/M04-clamp-5s | `:228`, `:269` | stall, whole | stall, stated_seconds, whole | `stall`: "the stall was charged in full" |
| `windows-2s` | R764-1/M15-windows-2s, R764-2/M15-windows-2s, R764-3/M15-windows-2s | `:225`, `:226`, `:229` the 10 s windows, 14 s | none | stated_seconds, whole | `stated_seconds`: "a survivor's stated seconds were not kept" |
| `reap-window-2s` | R763-2/reap-window-2s | `:225`, `:229` 10 s after SIGKILL, 14 s | none | stated_seconds, whole | `stated_seconds`: "a survivor's stated seconds were not kept" |
| `no-shell-window` | R764-1/M05-no-trap-window, R764-2/M05-no-trap-window, R764-3/M05-no-trap-window, R764-4/M05-no-trap-window, A726/no-shell-window | `:226`, `:273` a late shell's own window | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| `no-shell-window-kept` | R763-1/no-shell-window | `:226`, `:273` a late shell's own window | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| `no-shell-window-pass` | R763-2/no-shell-window | `:226`, `:273` a late shell's own window | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| `no-trap-window` | R763-3/no-trap-window, R764-4/no-trap-window | `:226`, `:273` a late shell's own window | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| `root-killed-unresumed` | R763-4/root-killed-unresumed, R764-1/M06-root-killed-unresumed, R764-2/M06-root-killed-unresumed, R764-3/M06-root-killed-unresumed, R764-4/M06-root-killed-unresumed | `:224` a cancelled shell keeps its own window | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| `shell-killed-when-resumed` | R763-3/shell-killed-when-resumed, R764-4/shell-killed-when-resumed, A726c/R763-3-shell-killed-when-resumed | `:273`-`:274` the whole window, through builtins | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| `shell-window-one-pass` | R764-4/shell-window-one-pass | `:273`-`:274` the whole window, through builtins | none | shell_window, stated_seconds, whole | `shell_window`: "the resumed shell was killed inside its own window, with no child to spare it" |
| `shell-window-1s` | R764-4/shell-window-1s | `:273`-`:274` the whole window, through builtins | none | shell_window, stated_seconds, whole | `shell_window`: "the resumed shell was killed inside its own window, with no child to spare it" |
| `trap-commands-no-window` | R763-3/trap-commands-no-window, R764-1/M07-trap-child-no-window, R764-2/M07-trap-child-no-window, R764-3/M07-trap-child-no-window, R764-4/trap-commands-no-window | `:273` and the commands it starts | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the resumed shell's trap command was killed inside the shell's window" |
| `trap-commands-never-spared` | R763-2/trap-commands-no-window | `:273` and the commands it starts | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the resumed shell's trap command was killed inside the shell's window" |
| `trap-commands-1s` | R763-1/trap-commands-1s, R763-2/trap-commands-1s, R763-4/trap-commands-1s, R764-2/M07b-trap-child-1s-window, R764-3/M07b-trap-child-1s-window, R764-4/trap-commands-1s | `:273` and the commands it starts | shell_window, whole | shell_window, stated_seconds, whole | `shell_window`: "the resumed shell's trap command was killed inside the shell's window" |
| `resume-collected-shell` | R763-3/new-fix-reverted, R764-3/M16-resume-collected-shell, A726c/A726c-resume-collected-shell | `:275` no window after the shell was collected | late_cancel, whole | late_cancel, whole | `late_cancel`: "a cancel after the shell was collected resumed it" |
| `window-without-resume` | R764-3/M16b-window-without-resume | `:275` | late_cancel, whole | late_cancel, whole | `late_cancel`: "cleanup never reached a verdict after a late cancel" |
| `rearm-without-sigcont` | A726c/A726c-rearm-without-sigcont | `:275` | shell_window, late_cancel, whole | shell_window, late_cancel, stated_seconds, whole | `late_cancel`: "cleanup never reached a verdict after a late cancel" |
| `resume-while-listed` | R763-3/new-fix-census-not-owned, R764-3/M16c-resume-while-listed, A726c/R763-3-new-fix-census-not-owned | `:275` even in that pass | none | late_cancel, whole | `late_cancel`: "a cancel after the shell was collected resumed it" |
| `no-kill-before-raise` | R763-1/no-kill-before-raise, R763-3/no-kill-before-raise, R764-1/M08-no-kill-before-fail, R764-2/M08-no-kill-before-fail, R764-3/M08-no-kill-before-fail, A726/no-kill-before-fail | `:276` takes the stopped shell with it | survivor, whole | survivor, stated_seconds, whole | `survivor`: "stopped shell left behind" |
| `no-kill-before-raise-empty` | R763-2/no-kill-before-raise | `:276` | survivor, whole | survivor, stated_seconds, whole | `survivor`: "stopped shell left behind" |
| `kill-before-fail-spares-shell` | R764-1/M09-kill-before-fail-spares-shell, R764-2/M09-kill-before-fail-spares-shell, R764-3/M09-kill-before-fail-spares-shell | `:276` | survivor, whole | survivor, stated_seconds, whole | `survivor`: "stopped shell left behind" |
| `endless-unbounded` | R763-1/endless-unbounded, R763-2/endless-unbounded, R763-3/listing-unbounded, R764-1/M10-endless-unbounded, R764-2/M10-endless-unbounded, R764-3/M10-endless-unbounded, A726/endless-listing-unbounded | `:232` a vanishing listing reaches a verdict | vanishing, late_cancel, whole | vanishing, late_cancel, whole | `vanishing`: "cleanup never reached a verdict" |
| `survivor-never-fails` | R763-1/survivor-never-fails, R763-3/survivor-never-fails, A726/survivor-does-not-fail | `:276` a survivor fails the run | survivor, vanishing, late_cancel, whole | survivor, vanishing, late_cancel, stated_seconds, whole | `survivor`: "a survivor never failed the run" |
| `survivor-never-fails-guarded` | R763-2/survivor-never-fails | `:276` | survivor, vanishing, late_cancel, whole | survivor, vanishing, late_cancel, stated_seconds, whole | `survivor`: "a survivor never failed the run" |
| `trust-sigkill` | R764-1/M11-trust-sigkill, R764-2/M11-trust-sigkill, R764-3/M11-trust-sigkill | `:276` | survivor, whole | survivor, stated_seconds, whole | `survivor`: "a survivor never failed the run" |
| `killed-counts-as-gone` | R763-1/killed-counts-as-gone | `:225`, `:229` 14 s for a survivor | none | stated_seconds, whole | `stated_seconds`: "a survivor's stated seconds were not kept" |
| `report-without-state` | R763-1/report-without-state | `:277` state, wait channel, parent and age | report, survivor, whole | report, survivor, whole | `report`: "('state S'" |
| `report-without-wchan` | R763-1/report-without-wchan | `:277` state, wait channel, parent and age | report, survivor, whole | report, survivor, whole | `report`: "('wchan '" |
| `report-without-state-or-wchan` | R763-2/report-without-state, R763-3/report-without-state, R764-1/M12-report-without-state, R764-2/M12-report-without-state, R764-3/M12-report-without-state, A726/report-without-state | `:277` state, wait channel, parent and age | report, survivor, whole | report, survivor, whole | `report`: "('state S'" |

The matrix (`receipts/matrix/matrix-table.md`) has one row per mutant, a column for each of the 10 controls, and `whole` (the whole `scripts/test_suite_cancellation.py`). Every mutant with a named control is also red on `whole`.

## Item 3: a home for the next mutant (commit `99284ca5`)

- `scripts/process_test_support.py:261-414`, `MUTANTS`: the 43 mutants and `none`. Each entry carries its named control and words, or `None` with the reason, then its exact edits. Names describe behaviour, with no reviewer IDs. `emit_table.py` generated the edits from `collected.json`, and the result was checked byte-equal.
- `:417-487`: `mutant_tree`, `run_mutant` and `mutation_campaign`. Every mutant must be red on its control with its words, and `none` must be green on every control. `--matrix` also runs every mutant on every control and the whole test.
- `scripts/test_suite_cancellation.py`:
  - `OWNER_CONTROLS` (`:812-815`), checked at start-up against every `owner_*` function, so a new control joins the matrix.
  - `run_control` (`:818-824`).
  - The `argparse` entry (`:868-882`). With no argument it is `main()`, as the preflight calls it.
- `TESTING.md:281-285` states: "A stated cleanup behaviour is one some control pins." Each published mutant names the control it must fail, with words; the next reviewer's mutant joins `MUTANTS`. The campaign runs beside the preflight, and its row is in the explicit-campaign table (`:309`).
- Beside, not in, the preflight: the default campaign takes 55 s with 8 jobs. It is not a preflight step.
- `test_suite_cancellation.py` stays under the 1000-line module ratchet (882 lines), which is why the table lives in the support module.

## Item 4: R764-4-S1, DERIVED (commit `ff03b757`)

`scripts/test_suite_cancellation.py:568-588`. The control's child is now held by census passes, not wall time.
- `counted()` counts the owner's census passes, and `late()` drops the child's SIGKILL until pass 61.
- Each pass sleeps 0.02 s before the next (`owned_process.py:339`), and the cap is longer, so pass n is at least 0.02 (n - 1) s on the owner's clock, however the owner stalls.
- The child dies from pass 61, and the resume after it is at least pass 62: 1.22 s, past grace + 1 s = 1.2 s.
- The 0.3 s wall margin is gone. A stalled owner can no longer bring the resume back under grace + 1 s.

Cost, host load 100 to 115 (`receipts/cost/cost.txt`, 3 runs each, Python start-up included):

| Control | Before | After |
|---|---|---|
| `owner_shell_window` | 3.3 s at `c1b29617` | 3.6-3.7 s with the F1 tail (`99284ca5`); 4.7 s with S1 (head) |
| `owner_stated_seconds` | new | 0.14 s |
| `owner_reused_identity` | new | 0.12 s |
| `owner_reparented` | 0.26 s | 0.26-0.27 s |
| `owner_late_cancel` | 0.95 s | 0.95 s |

So item 2 costs about 0.4 s plus about 0.1 s for the two new controls, and S1 about 1.0 s. The preflight grows by about 1.5 s in all. In a PID namespace the control takes 3.2 s, because its census is cheap there.

## Item 5: residue R764-3-R1 (commit `ff006178`)

`scripts/test_suite_cancellation.py:683` now reads: "A re-armed window would hold the verdict past the 15 s bound below: TRAP_SECONDS is 30 s." This is the exact fix. Both values are true: `stages(... TRAP_SECONDS=30.0 ...)` at `:684`, and the `< 15` bound at `:703`.

## Commits

| Commit | Item | Subject |
|---|---|---|
| `682dc31b` | 2 | Pin what published mutants broke unseen: a resumed shell's builtin tail, the product's seconds pass by pass, a same-pass SIGTERM and late cancel, a reused identity |
| `99284ca5` | 3 | List every published owned-process mutant with the control it must fail and its words, and run the list beside the preflight |
| `ff03b757` | 4 | Hold the shell-window control's child for 61 census passes, so its resume is past grace + 1 s on the owner's clock however the owner stalls |
| `ff006178` | 5 | Name the late-cancel control's 15 s bound and the 30 s window that would hold the verdict past it |
| `a67eaf66` | 2 (fix) | Word the stated-seconds control's placeholder-PID comment within the bare-metal scope gate |

One-line subjects, empty bodies, no trailers. The fifth commit is a deviation from one commit per item, and it is disclosed here. At `ff006178`, docs.yml `docs-gates-0` gate_21 (bare-metal scope) failed on a retired-stack term in a comment added by `682dc31b` (`:770`). The only fix that adds commits on top, without amending or rebasing, is a fifth commit. `git diff ff006178 a67eaf66` is that one comment line. `git diff --stat c1b29617 HEAD`: `TESTING.md` +12 -2, `process_test_support.py` +231, `test_suite_cancellation.py` +170 -23. `owned_process.py` is untouched (`git diff --quiet` rc 0).

## Gates

All at head `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca`, one log and one rc each, never piped. The lane gates ran on a fresh clean clone (`receipts/gates/lane.sh`), and `tree-after.txt` is empty with `--ignored`.

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` (round 1's `run_docs_yml.py` and `verify_docs_yml.py`, paths pointed at this round's scratch, `not_run.json` unchanged; fresh venv identical to round 1's freeze, `venv-freeze*.txt`; fresh HOME) | 0 | Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. `git status` clean after each job (`docsyml/*tree-after.txt`). Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. SIGHUP not ignored (`sigign.txt`, 0x4) | `receipts/gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml/` (`gate_41`'s log is over 200 KB: sha256 and size in `LARGE-LOGS.txt`, tail in `docsyml/`). The aborted run at `ff006178`: `gates/aborted-ff006178/` (gate_21 rc 1) |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`. `owner-shell-window: {... 'trap_finished': True}`, `owner-stated-seconds: {'grace_pass': 5, 'survivor_verdict_pass': 29, 'resume_pass': 12, 'window_end_pass': 32, 'resumed_verdict_pass': 52}`, `owner-reused-identity: {'signalled': False}` | `receipts/gates/lane/test_suite_cancellation.*` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `receipts/gates/lane/lifecycle.*` |
| Mutation table, old and new (all 43 published mutants and `none`) | 0 | `--mutants` (default, no namespace): `owned-process mutants: PASS (43 mutants, 42 with a control that must fail)` in 54.7 s. `--matrix` in 3 parts, 506 runs, each rc 0 and PASS. R764-4's own packet: only its two `shell-window-*` rows change, 16/16. Lifecycle entries as at round 4 | `receipts/matrix/`, `r764-4/`, `lifecycle/`; baseline `baseline-c1b29617/` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `receipts/gates/lane/behave.rc`, `behave.log.tail`; the log is 235,280 bytes, sha256 in `LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `receipts/gates/lane/diffcheck.*` |
| `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check` (also inside docs.yml) | 0 each | before each commit, on the working tree; bare-metal from the fix on | scratch only; the docs.yml receipts are the evidence at the head |
| Full sweep | not run | Round 5 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

## Not taken

- R763-2-S2 (manager actions) and R763-2-S3 (the census-cost comment): unchanged, on the manager's checklist.
- No full sweep: round 5 changes only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1.

## Incidents, no harm

- At `ff006178`, docs.yml gate_21 failed (above). I stopped my own runner by its process group (`kill -TERM -<pgid>` of the `setsid` session I started) and kept its partial logs as `run1-ff006178-aborted` in scratch. I relaunched at `a67eaf66` and re-ran every gate and the whole mutation table there.
- During development the driver used a pipe, and `cleanup-does-nothing`'s leaked children held it open until the 150 s bound. The committed driver writes to a file. The baseline row for that mutant was re-run with the file driver (`baseline-c1b29617/base-3.log`).
- The first `owner_stated_seconds` draft listed the placeholder shell's parent as `1`, which is this process's own PID inside a PID namespace. That made the child a "parent" and moved its SIGKILL to pass 7. All placeholder PIDs are now above any real PID. The control is green in and out of namespaces.
- Nothing was signalled by name, and nothing outside my own session group was signalled. No `.pyc` was written to the lane: every run used `-B` or `PYTHONDONTWRITEBYTECODE`. The lane's ignored `scripts/__pycache__`, `tb/verilator/gptp_shadow/__pycache__` and `sw/builder/out` predate this session (2026-11-01 and 2026-11-02 before 13:00).
- Memory of this unit stayed well under 12 GB.

## Files

- `PR-BODY.md`: round 4's body with a Round 5 section and the status, roles, validation and limitation lines updated.
- `receipts/`:
  - `taken.md`, `ready.md`, `review-evidence-fetch-head.txt`.
  - `tools/`: the collector, table emitter and tabulators, plus names, expectations and the collected edits.
  - `baseline-c1b29617/`, `matrix/`, `matrix-ff006178/`, `r764-4/`, `lifecycle/`, `cost/`.
  - `item-checks/`: the whole suite at the item 2 state, and the development matrix.
  - `gates/`.
