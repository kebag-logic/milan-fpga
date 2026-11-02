[R763] NEGATIVE - exact head 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c

# R763-2: internal cleared-context review of PR #834 (issue #833), round 2

Head `1ff8292cd5b761633ef9500a7c5a4b1626a3d92c`, tree `66b77844947516b36de065ed3275efb3ba091e42`. Round 1 head `d4d8cff92658e57b11090c97daf7b44edb31b3b6`; source base `1f29f189279f9fc0132f4918e47342b87d22f33a`.

Verdict basis: one open MINOR (F1). The stated worst-case bound for "a listing that dies inside every census" is false on a reachable path. It is stated in three places and supports the `FINISH_SECONDS` derivation. A production-constant probe shows the run failing at 50.02 s and 53.03 s, against a stated "under 44 s". F1 is attributable to all five lenses, so every lens is UNCLEAN at this head. Every round 1 finding is resolved at its cause, except that the derivation which answered R763-1-F2 / R764-1-F3 still has this one gap. Two RESIDUE wording items and three SUGGESTIONs are listed below.

## Scope reconstructed

- #833 acceptance: (1) the message prints each descendant's `/proc/<pid>/stat` state; (2) from that evidence, a fixed deadline or a real fix, "with no suite left to fail by chance. A longer deadline with no evidence does not close this."
- Round 2 scope (the executor's public TAKEN on #833): answer the round 1 MINOR and RESIDUE items only, one commit per finding, with no change to `scripts/owned_process.py`.
- Delta `d4d8cff9..1ff8292c`: 5 commits. Files: `docs/testing/TESTING.md` (+15 -4), `scripts/process_test_support.py` (+10 -2, comment only; `FINISH_SECONDS = 60` unchanged), `scripts/test_suite_cancellation.py` (+30 -15).
- Confirmed: `git diff --quiet d4d8cff9 HEAD -- scripts/owned_process.py tb/` holds. Commit subjects are one line each, with no bodies or trailers.
- Comment rule: the added lines contain no lane label, round, reviewer ID or comment ID (scan of `+` lines for `[ABR]<digits>`, `round`, `lane`, `reviewer`, `issuecomment`: rc 1).
- New source comments carry `#833`. The claim at `scripts/test_suite_cancellation.py:547-548` was checked against code:
  - "the 1 s such a command had before #833": base `owned_process.py` has `now < resumed + 1.0`.
  - "the sweep's EXIT trap runs rm": `scripts/run_all_suites.sh:223,236,238`.

## Findings

**R763-2-F1: MINOR. Lenses: Conformance, RTL, Robustness, Tests, Docs.** The stated worst case for an endless listing (and the derivation premise "That resume comes before 14 s") is false when a cancellation arrives during cleanup. It appears in:
- `docs/testing/TESTING.md:231-232`;
- `scripts/process_test_support.py:23-29`, which carries the `FINISH_SECONDS` argument "59.6 s for the listing";
- the PR #834 body: "The deadline's derivation" paragraph, and the Known limitations bullet "under 34 s … (44 s for a listing that dies inside every census)".

- Authority/evidence:
  - **The code.** `scripts/owned_process.py:187-195` latches `root_notified = True` whenever a handled SIGINT/SIGTERM arrives while `root_fd` is open. `run()` keeps that descriptor open through `_cleanup()` (`:366-372`), including the cleanup after a command that exited normally. In that case the shell is already reaped and the signal to it is a no-op.
  - **Where the premise fails.** Take a listing that dies inside every census: `owned` is empty, so `live` is empty. The first pass after such a late cancel then takes the resume branch (`:304-310`) at whatever clock it has reached, below the 24 s at which the unresumed listing would fail (`:289-290`). It sets `kill_all = clock + TRAP_SECONDS`, so the listing now fails at cancel time + 30 s: up to just under 54 s, plus one ≤0.5 s pass. A resume of a live shell is indeed always below 14 s, because a live shell keeps `owned` non-empty and `:290` raises first. The premise fails only when the shell is gone.
  - **Probe.** `scripts/late_cancel_listing.py` uses production constants. A real `true` runs through `OwnedProcesses.run`; its cleanup sees the same listing substitution as the `owner_vanishing` control; SIGTERM arrives at a set wall time. Receipts are in `receipts/probes/`, all with rc 0, `root_notified=True`.

    | Cancel at | Cleanup fails after | Stated bound |
    |---|---|---|
    | 5 s | 35.03 s | under 44 s: inside it, consistent with `t + 30` |
    | 20 s | **50.02 s** | under 44 s |
    | 23 s | **53.03 s** | under 44 s |

    Passes were fast (`slowest 0.00 s`), so these times are owner clock.
  - **Round 1 requirement.** R763-1-F2 and R764-1-F3 required the derived worst case to be stated, "worst case included". The `FINISH_SECONDS` argument "59.6 s for the listing: both inside this bound" becomes 54.5 + 15.1 = 69.6 s on this path. That is outside 60 s.
- Impact: a figure and a bound on the cancellation timeout path are wrong in the authoritative guide, a source comment and the PR body, and so is the stated reason 60 s covers it. No current fixture drives this path, so no test result changes today. But it is a figure and a derivation, so it is not RESIDUE.
- Required outcome: one of the following.
  - (a) All three statements give the bound on this path: an endless listing fails at most 30 s after a cancel that arrives during cleanup, so under 54 s. The `FINISH_SECONDS` paragraph either covers it or states why no fixture reaches it.
  - (b) The code no longer re-arms the trap window for a shell that is no longer listed, with a control that goes red when that is reverted. Then "That resume comes before 14 s" and "under 44 s" hold as written.

  No particular design is required.
- Verification: `python3 -I scripts/late_cancel_listing.py <clone>/scripts 23`. Under (a), its reported time lies within the stated bound. Under (b), it reports under 44 s and the new control is red under the reverted change.

**R763-2-X1: RESIDUE. Lenses: Docs.** `docs/testing/TESTING.md:230`, `scripts/process_test_support.py:23-24` and the PR body: "One started by a resumed shell's trap has its deadline 20 s after the resume."
- After a resume, `limit = kill_all + REAP_SECONDS` applies to every remaining descendant (`owned_process.py:289,310`), not only to one the trap started.
- Exact fix: "After a resume, every remaining descendant's deadline is 20 s after the resume, including one the trap started." Fold this into F1's edit.

**R763-2-X2: RESIDUE. Lenses: Docs.** `docs/testing/TESTING.md:224`: "Two seconds later `SIGKILL` has reached every other descendant."
- A notified shell is not sent SIGKILL then (`owned_process.py:315`). Line 226 implies this but does not say it.
- Exact fix: "Two seconds later `SIGKILL` has reached every other descendant except a stopped shell, which keeps its own window."

**R763-2-S1: SUGGESTION. Lenses: Tests.** Retained from R764-1-S1. No control pins the 10 s windows themselves: my `reap-window-2s` mutant is green on all 7 owner controls. The PR body's reason for not taking it (pinning 10 s costs about 10 s of preflight) is stated and reasonable. Optional.

**R763-2-S2: SUGGESTION.** Carried forward for the manager: R763-1-S1 (an Issue for the stale `ci/image/command-table.json` pins: 34 on `dev`, 38 here) and R763-1-S2 (where `Probe.ready`'s 15 s handshake belongs).

**R763-2-S3: SUGGESTION. Lenses: Docs.** The census-cost source comment at `scripts/owned_process.py:84` still says 13 ms against 30 ms for 1300 processes. The new receipt in the PR body says 17.4 ms against 37.6 ms for 1,403. Both are relative measurements and the comment is outside the delta (#746 territory for comment upkeep). Align them when that file is next touched.

## Round 1 findings at their cause, at this head

| Prior finding | Status | Evidence at this head |
|---|---|---|
| R763-1-F1 = R764-1-F1 (guide states old stages) | RESOLVED | `TESTING.md:223-228` read against `owned_process.py:37-45,260-336`: 2 s of SIGTERM, SIGKILL to all by 4 s, verdict 10 s later, 10 s trap window, clock capped at 0.5 s a pass. Wording residue X2 only |
| R763-1-F2 = R764-1-F3 (survivor bound) | RESOLVED for the survivor cases; listing case reopened as **R763-2-F1** | The 14 s case was rerun: production-constant `owner_survivor` failed after **14.01 s** (`receipts/probes/survivor-production.log`). The <34 s premise holds for a live shell (see F1). Author receipts `author-r2/receipts/bounds/at-head/` (14.02, 22.03, 33.51, 33.92, 32.54, 24.01 s) match the PR body exactly. The listing's "under 44 s" is falsified by F1's probe |
| R763-1-F3 (stall control's 2.5 s death window) | RESOLVED | `test_suite_cancellation.py:518`: `REAP_SECONDS` is no longer shortened. Arithmetic: SIGKILL at ≥1.5 s, limit 2 + 10 = 12 s, so a death delay below 10.5 s passes. The author's `stall-window/` receipts agree: 10.4 s PASS, 11.0 s FAIL. The verdict is deterministic: the product clock after pass 2 is ≤ 1.0 s < 1.5 s. Mutants `deadline-wall-clock`, `pass-cap-5s` and `pass-cap-1.5s` are red; see the table below |
| R763-1-F4 = R764-1-F2 (no trap-command control) | RESOLVED | `test_suite_cancellation.py:549,578`: `sleep 1.5 && echo ran`. `trap-commands-1s` and `trap-commands-no-window` are both red: "the resumed shell's trap command was killed inside the shell's window". Head is green, and green at production constants (`receipts/probes/shell-window-production.log`) |
| R764-1-F4 = R763-1-X2 (command-table text) | RESOLVED | Three commands rerun (`receipts/command-table/`): `pins 149 stale 34 absent 1` at `1f29f189`, `stale 38` at both later heads, with the 4 delta scripts named; 14 reader files; the reader-name grep over `.github/workflows` and `scripts/run_all_suites.sh` has rc 1. All match the PR body |
| R763-1-X1 = R764-1-R1 (before/after rows) | RESOLVED | Round 1 receipts `author/receipts/final-fullsuite-L48/before` and `final-lifecycle-L48-M6/before`: 10 of 10 and 18 of 18 `timed out after 12 seco[nds]`, rc 2, 0 files with `CLEANUP FAILED`. The PR body rows now say so |
| R764-1-R2 (stalled-owner line) | RESOLVED | `TESTING.md:270` carries the exact wording |
| R764-1-S1 | Retained as SUGGESTION S1 | `reap-window-2s` is green |
| R764-1-S2 | Answered by a published receipt (not re-measured here) | S3 notes the comment/receipt figure gap |
| R763-1-S1, S2 | Open, manager actions | S2 |

## Mutation table, re-run at this head

Every round 1 fix and every round 2 control. Each mutant is one reverted fix in a copy of the head's `scripts/`, applied by `scripts/make_mutants.py`; every edit must match exactly once (diffs in `receipts/mutations/mutants.diff`). Each run executes one owner control through `scripts/control_driver.py` inside an outer owner, as the preflight's `main()` does: 14 mutants × 7 controls = 98 runs, at most 10 parallel jobs. Logs and rc files are in `receipts/mutations/`, and the table is `receipts/mutations/summary.txt`.

| mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | red |
|---|---|---|---|---|---|---|---|---:|
| none | ok | ok | ok | ok | ok | ok | ok | 0 |
| deadline-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| identity-includes-parent (census key and send recheck) | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| no-shell-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| pass-cap-1.5s | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| pass-cap-5s | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| reap-window-2s | ok | ok | ok | ok | ok | ok | ok | 0 |
| report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | 2 |
| survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| trap-commands-1s | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| trap-commands-no-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |

Every fix, old and new, has a red control when reverted alone. The failing messages match the PR body's: stall "the stall was charged in full: SIGKILL in pass [2]"; shell_window "the resumed shell's trap command was killed inside the shell's window". The only green mutant is `reap-window-2s`, the window values (S1). My first `identity-includes-parent` variant changed the census key and its checks but not the send's recheck, and it stayed green. That agrees with the PR body's account that M01 alone is green and both halves (M01c) are red.

## Lens results

| Lens | Result | Examined artifacts |
|---|---|---|
| Conformance | UNCLEAN (F1) | #833 acceptance 1-2 and the round 2 TAKEN scope against the delta. F1's derivation against `owned_process.py:187-195,260-336`. Prior Conformance artifacts are unchanged (`owned_process.py` untouched); their round 1 verdict stands apart from F1 |
| RTL (architecture of the cleanup state machine; no HDL in this PR) | UNCLEAN (F1) | `owned_process.py:187-195,289-310,366-372`: the resume transition re-arms the trap window for a shell already gone, a path the stated contract excludes. Probe `receipts/probes/late-cancel-listing-*.log` |
| Robustness | UNCLEAN (F1) | Cancellation arriving during cleanup (an ordering/timeout path), from the F1 probes. `owner_stall`'s determinism margin (clock after pass 2 ≤ 1.0 s < 1.5 s grace). The trap control's `&&` gating. The production-constant survivor at 14.01 s |
| Tests | UNCLEAN (F1) | `test_suite_cancellation.py:405-579` delta. Mutation table above (98 runs). Head `python3 scripts/test_suite_cancellation.py` rc 0, `suite cancellation: PASS`, `owner-stall: {'stalled_seconds': 2.0, 'killed_in_pass': 26}` (`receipts/head-suite/`). `process_test_support.py:19-30`: the `FINISH_SECONDS` justification fails on F1's path |
| Docs | UNCLEAN (F1; RESIDUE X1, X2) | `TESTING.md:223-235,269-275`; `process_test_support.py:19-29`; the PR body Description, Known limitations and Round 2 sections (line citations `TESTING.md:223-228,229-235,270`, `test_suite_cancellation.py:505-539,542-579,407` checked and correct); command-table text rerun |

## Executed (each with its own log and rc)

- `python3 scripts/test_suite_cancellation.py` at head: rc 0 (`receipts/head-suite/`).
- 98 mutation runs (`receipts/mutations/`).
- Production-constant probes (`receipts/probes/`):
  - `owner_survivor`: rc 0, failed after 14.01 s;
  - `owner_shell_window`: rc 0;
  - late-cancel listing at 5, 20 and 23 s: 35.03, 50.02 and 53.03 s.
- Command-table commands rerun (`receipts/command-table/`).
- Evidence packet `review-evidence/833-r1` at `cf127b7028b4267bd3059b79e48da83be2cd0818`: 1674 `MANIFEST.json` entries, 0 hash mismatches, 0 unlisted files, 742 round 2 entries (`receipts/evidence-manifest.txt`, `scripts/verify_evidence_manifest.py`).
- Host paths in receipts are redacted to `<packet>` and `<clone>`.
- Clone integrity after the probes (`receipts/clone-integrity.txt`):
  - HEAD and tree are exact;
  - index and worktree match HEAD, and `status --ignored` is empty;
  - delta blobs and modes are listed;
  - the 6 gitlinks are unchanged (`external` efeb541a, `gptp-processor` 135afd04, `protocol-processor` a9e84b66, `third_party/lwSRP` 08ee86e8, `third_party/tsn-c-stack` 70936b77, `third_party/verilog-axis` 48ff7a7e).
  - The probes had left a `scripts/__pycache__/` directory; I removed it before this check.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #833 acceptance; round 2 scope; `owned_process.py:187-336`; F1 probes | R763-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| RTL | UNCLEAN (F1) | `owned_process.py:187-195,289-310,366-372`; `receipts/probes/` | R763-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| Robustness | UNCLEAN (F1) | late-cancel path; `owner_stall` margin; trap gating; `receipts/probes/` | R763-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| Tests | UNCLEAN (F1) | `test_suite_cancellation.py:405-579`; `receipts/mutations/summary.txt`; `receipts/head-suite/`; `process_test_support.py:19-30` | R763-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |
| Docs | UNCLEAN (F1; X1, X2 RESIDUE) | `TESTING.md:223-235,269-275`; `process_test_support.py:19-29`; PR #834 body; `receipts/command-table/` | R763-2 | 1ff8292cd5b761633ef9500a7c5a4b1626a3d92c |

## Real limits

- My mutants and probes ran without PID namespaces, at low host load. Each control's population is scoped to its own process tree. Load-dependent behaviour (D-state tails, host stalls) is judged from the author's published receipts, not reproduced here.
- I did not rerun `make -C tb/verilator/gptp_shadow lifecycle`, the full sweep, `behave`, the builder legs or the `docs.yml` steps. The delta changes no lifecycle test and no constant (`process_test_support.py` changes only a comment), so these keep their round 1 verdicts on the author's published receipts.
- The evidence packet carries a hash manifest. I verified the hashes; I found no detached signature to verify.
- The F1 probe substitutes the census and reap, as the `owner_vanishing` control does. It does not build a real process that dies inside every census.
- Hosted contexts at this head were mostly `pending` at my snapshot (`changes` and `bdd-conformance` pass). I make no hosted or act claim.
- No manager source bank ran at this head, and none is inferred.
- Physical calibration: NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance on the exact head.
- Current-dev merge-candidate validation (builder and native banks) at the merge turn: source base `1f29f189`, live `dev` `503bc97c`.
- Carry X1 and X2 to the residue checklist.
- S2: the command-table Issue and the `Probe.ready` handshake record on #833.

R763-2 FINISHED
