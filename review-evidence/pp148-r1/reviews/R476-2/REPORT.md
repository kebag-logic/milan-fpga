[R476] NEGATIVE - exact head 356c1bbad2e9838659b433736040acf0cc4abf3e

# R476-2 internal independent review: PR #159 (issue #148), delta round

- **Exact head:** `356c1bbad2e9838659b433736040acf0cc4abf3e`, tree `f43fb15d1a5cb8852b8e680b0f29bbd429cc5f4f`.
- **Delta:** one manager commit on top of `bed5f477` (reviewed in R476-1). Source base `07b1469d`.
- **Scope of this round:** the delta. The round-1 verdicts on the other lenses stand at `bed5f477` unless this delta touches them. No campaign was re-run.

**Verdict: NEGATIVE.** One MAJOR is open (R476-2-F1, lens Tests). The new comment is correct, and R476-1-F1 is resolved. But the delta changes two context lines of a reviewed mutation patch. `git apply` now refuses `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch`, so `make -C tb/pp_top ctr-mutants` cannot complete at this head. One RESIDUE covers the PR body's head and byte-identity sentences.

## 1. What the delta is

`git diff bed5f477 356c1bba` changes one file, `hdl/aecp/KL_aecp_notify.sv` (+4 -2). It replaces the two-line comment above the selection stamp ("Measure the one-second limit from emission selection, not from the possibly much earlier pending instant.") with four lines at `:1299-1302`:

> Provisional stamp: it keeps the window shut until the round's first job reaches N_EMIT_WAIT, whose stamp then follows each job to its send, so the limit runs from the round's last send (issue #148).

Checks (`delta_identity.sh`, `receipts/delta_identity.log`, rc 0):

| Check | Result |
|---|---|
| Files changed | `hdl/aecp/KL_aecp_notify.sv` only |
| `git diff --check` | clean |
| Changed lines that are not `//` comments | none |
| Source with `//` comments and blank lines stripped, `bed5f477` vs head | identical |
| sv2v v0.0.13 output of `pp_pkg.sv` + `KL_aecp_notify.sv` | byte-identical, sha256 `290c210e…9d068c` at both |
| Pinned Verilator 5.050 `-E -P` preprocessed output | byte-identical, sha256 `d7f143a5…1fc93fd43` at both |
| `pp_pkg.sv` | unchanged |

The notify blob was `9e97f8e7` at `82e1664`, `a369cdd`, `4ed463b` and `bed5f47`. It is `030192f9` at this head.

**The comment agrees with the code and the measurements:**
- **The code.** At the claim (`:1303-1304`), `ctr_sent_r` is set and `ctr_last_r` takes `now_ms_i`. The window check (`:1099-1101`) keeps a dirty descriptor from pending until `now_ms_i - ctr_last_r >= 1000`. `N_EMIT_WAIT` (`:1445`) rewrites the stamp every cycle a counter job waits, and the last write is the cycle of `uns_done_i`. So the claim stamp is provisional: the first job's wait overwrites it, and the round's last send is the final value.
- **The banner** (`:133-136`) says "their one-second limit runs from a round's last send". This agrees.
- **The `N_EMIT_WAIT` comment** (`:1441-1444`) says the stamp "follows the clock while a job waits ... and holds its send, so the next round waits a second from this round's last send". This agrees.
- **Measured.** I ran `tb/aecp_notify` `make run` at head with the pinned simulator (`receipts/aecp_notify_head.log`, rc 0): 34 checks, 34 PASS. TW1 sent its last job at ms 2600 and presented the next round at ms 3603. TW2 sent at ms 6504 and presented at ms 7507. Both match `tb/aecp_notify/README.md` §TW and the PR body. The README's `counter_stamp_at_send_only` control (TW2 at ms 6508) shows the provisional stamp is load-bearing: without the stamp following the wait, the claim stamp alone opens the window inside the round.
- **Zero-send round.** If every row is skipped, no job reaches `N_EMIT_WAIT` and the claim stamp stays. The window then runs from selection. This is conservative: no controller can receive two notifications less than a second apart. The comment does not claim otherwise, and the behaviour is unchanged from `bed5f477`. Not a finding.

## 2. Findings

### R476-2-F1 - MAJOR - lens: Tests

- **Where:** `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch:4-6`, the hunk's context lines. Its driver is `tb/pp_top/ctr_mutants.py:78-82` (`plant`), wired as `make -C tb/pp_top ctr-mutants` (`tb/pp_top/Makefile:146-147`).
- **Authority:**
  - `tb/pp_top/README.md:1398-1436`: the campaign is a reviewed gate. Its record at the #148 head is "control PASS, 17 of 17 KILLED". `ctr-notify-one-window` must fail 4 checks: K15 x2 (named), K16, K17.
  - `docs/architecture/09_verification.md:386-392`: the 17 arms are the negative controls for K9-K17.
  - `ctr_mutants.py:15-17,79`: an arm is applied with `git apply --check`, "refusing drift".
  - The PR body's union table: "Ctr campaign | 1 control, 17 KILLED | same".
- **Evidence:**
  - The patch carries the two replaced comment lines ("Measure the one-second limit from emission selection," / "not from the possibly much earlier pending instant.") as context. The delta removed exactly those lines.
  - `plant_check.py` checks every planting arm without simulating: every `tb/**/*.patch`, plus every exact-text edit in `notify_mutants.py` and `d3_mutants.py`. At `bed5f477`, 440 of 440 arms plant. At head, 439 of 440 plant. The one refusal is `ctr-notify-one-window.patch`: "patch failed: hdl/aecp/KL_aecp_notify.sv:1233" (`receipts/plant_check.log`, rc 1).
  - I called the driver's own `ctr_mutants.plant()` on a scratch copy of each tree. It plants at `bed5f477`. At head it raises `CalledProcessError` from `git apply --check` (`receipts/ctr_driver_plant.log`).
  - `trial()` raises in its worker, and `tb/common/mutant_pool.py:in_order` re-raises a unit's exception "when its turn comes". So the ninth arm aborts the campaign: no tally, nonzero exit, and arms 10-17 are cancelled.
  - The hosted `suites` job runs `aecp-mutants` and `aecp-dispatch-mutants` but not `ctr-mutants` (`.github/workflows/hdl.yml:56-74`), so hosted checks cannot catch this. The delta's published checks (lint, `tb/aecp_notify`, `--spacing-only`) do not plant any arm.
- **Impact:**
  - The RTL is not affected.
  - At this head a reviewed verification gate cannot run. The README's and PR body's "17 of 17 KILLED" cannot be reproduced at the head they describe.
  - The arm guards K15, the "interface and a Stream Input throttled apart" property next to the stamp this PR moves. Its record is one of the PR's two intended campaign changes (3 to 4 failing checks).
- **Required outcome:**
  - Refresh only the patch's context to the new comment. The four comment lines replace the two, and the header becomes `@@ -1233,10 +1233,11 @@`. Its `-`/`+` lines stay as they are.
  - A ready candidate is `ctr-notify-one-window.refreshed.patch` in this packet.
  - No other file needs to change.
- **Verification:**
  - Disposable probe (`receipts/ctr_refresh_probe.log`): the refreshed patch applies at head and refuses at `bed5f477`. The head planted with it gives sv2v output byte-identical to `bed5f477` planted with the original (sha256 `72904c92…87cea`), and different from the unplanted head. So the arm's verdict is expected to be unchanged.
  - After the fix: `plant_check.py` reports 440 of 440 at the new head.
  - `make -C tb/pp_top ctr-mutants` (or `ctr_mutants.py --only ctr-notify-one-window`) prints control PASS, and the arm prints KILLED with its 4 failing checks per `tb/pp_top/README.md:1436`.
  - `git diff 356c1bba` touches only that patch's context lines (plus any PR-body note).

### R476-2-R1 - RESIDUE - lens: Docs (PR body only)

- **Where:** the PR #159 body, as published at `2026-10-05T05:52:35Z`.
- **Evidence:** the head moved from `bed5f477` to `356c1bba`, and the notify RTL now differs from the measured head's in comments only. Several sentences still describe `bed5f477`:
  1. "current head `bed5f47785839800bb640d7c747f5435f84ab5a3`".
  2. "Every compiled input at `4ed463b` equals the final head's". The notify file differs, in comment lines.
  3. "notify RTL is byte-identical to that measured head". The blob is now `030192f9`, not `9e97f8e7`.
  4. §2: "`:1443`, in `N_EMIT_WAIT`" is now `:1445`. "The selection stamp (`:1299-1302`)" is now the comment at `:1299-1302` and the stamp at `:1303-1304`.
- **Why RESIDUE:** the delta is comment-only. Comment-stripped source, sv2v output and preprocessed output are all byte-identical to `bed5f477`. So the retained OOC 1x1 area, every suite tally and every campaign verdict still apply as stated. Correcting these sentences changes no measurement, figure, verdict, test, code or artifact.
- **Exact fix:**
  1. "current head `356c1bbad2e9838659b433736040acf0cc4abf3e` (`bed5f477` plus manager commit `356c1bba`, which rewords the comment at `KL_aecp_notify.sv:1299-1302` only)".
  2. "Every compiled input at `4ed463b` equals `bed5f477`'s; `356c1bba` changes only comment lines, and the module's sv2v output is byte-identical".
  3. "notify RTL differs from that measured head only in the comment at `:1299-1302`; its sv2v output is byte-identical".
  4. Use `:1445`, and "the selection stamp (`:1303-1304`, its comment `:1299-1302`)".
- Once F1 is fixed, the body should also name the refreshed patch.

### Examined and accepted (not findings)

- **Tracked line references.** No tracked Markdown, script or patch cites a `KL_aecp_notify.sv` line number, so the +2 shift after `:1300` stales no tracked document. No `.vlt` waiver is anchored by line.
- **Other planting arms.** All 439 other arms still plant at head (above): 276 of the 277 `tb/**/*.patch` files, including `mutations/fanout-never-ends.patch` and the other eight notify arms in `ctr_mutations/`; the 53 `notify_mutants.py` arms; and the 110 `d3_mutants.py` arms, two of which edit the notify file.
- **#158** (DEREGISTER mid-round) remains out of scope, as in round 1. The delta changes no logic.

## 3. Prior public findings on this PR, at this head

| Finding | Status at `356c1bba` | Basis |
|---|---|---|
| R476-1-F1 (MINOR, RTL, Docs): stale comment at `:1299-1300` | **Resolved** | The comment now describes the stamp as provisional, in the wording F1 asked for. It agrees with the banner (`:133-136`), the `N_EMIT_WAIT` comment (`:1441-1444`) and TW. F1's verification holds: comment-only diff and byte-identical sv2v (§1). The manager reports lint 41/41 at head. `tb/aecp_notify` 34/34, executed here. |
| R476-1-S1 (SUGGESTION, Tests): TW/CS lower bounds have slack | Retained as SUGGESTION (optional) | Untouched by the delta. |
| R476-1-S2 (SUGGESTION, Tests): the kind guard at the `N_EMIT_WAIT` stamp (now `:1445`) survives | Retained as SUGGESTION (optional) | Untouched by the delta. |
| R477-1-RES1 (RESIDUE, Docs): PR body cell "TD 6 probes" | **Retained** as RESIDUE | The PR body still reads "default 9,956; other five unchanged; TD 6 probes" (union table, row "Six `pp_top` builds"). Its exact fix stands. Carry it with R476-2-R1. |
| R477-1-S1 (SUGGESTION, RTL, Docs): the comments at `:1299-1300` and `:399-401` | **Resolved in part.** The claim-site half is resolved by `356c1bba` (above). The `:399-402` half is retained as SUGGESTION. | `:399-402` still says a stamp "is written in the cycle that sets the bit". That is still true for the reset argument, but incomplete: the stamp is also rewritten at every later claim and every `N_EMIT_WAIT` cycle. It is optional and comment-only. |
| R477-1-S2 (SUGGESTION, Robustness, Conformance): carry the stamp follow through an interleaved DEREGISTER job when #158 is fixed | Retained as SUGGESTION, for #158 | The guard has moved from `:1443` to `:1445`. The logic is unchanged. |

## 4. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan Table 5.22 `T-CTR-NOTIF` spacing per R476-1. The delta changes no logic: comment-stripped source, sv2v and preprocessed output identical. TW1/TW2 re-measured at head (3603, 7507). | R476-1 (logic); R476-2 (delta) | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| RTL | CLEAN | `KL_aecp_notify.sv:1299-1304` new comment against `:133-136`, `:399-404`, `:1099-1101`, `:1441-1445`. sv2v and Verilator `-E -P` byte-identity. R476-1-F1 resolved. | R476-1; R476-2 | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| Robustness | CLEAN | Withdrawal, reset and DEREGISTER per R476-1. Zero-send round re-examined against the new comment. No logic change. | R476-1; R476-2 | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| Tests | UNCLEAN (F1) | `tb/aecp_notify` executed at head, 34/34. 440 planting arms checked at `bed5f477` and head. Driver `plant()` called on both trees. Refreshed-patch probe. Hosted workflow coverage read. | R476-2 | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| Docs | CLEAN (residue R476-2-R1, R477-1-RES1 carried) | Module banner and inline comments; tracked line references (none to the notify file); `tb/aecp_notify/README.md` §TW; `tb/pp_top/README.md:1398-1436`; `09_verification.md:386-392`; PR body head, identity and line references (R1). | R476-1; R476-2 | 356c1bbad2e9838659b433736040acf0cc4abf3e |

## 5. Real limits

- **No campaign was re-run, as instructed.** F1's failure mode is shown in three ways: by the driver's own `plant()` on both trees, by `git apply --check`, and by reading `mutant_pool.in_order`. I did not execute `make ctr-mutants`. The refreshed patch's expected KILLED verdict rests on the planted sv2v netlist being byte-identical to `bed5f477`'s planted netlist. I did not simulate it.
- **Not run here:** the manager's banks (suites, lint, Yosys, parent consumer set, donor banks). For those I rely on the public evidence at `kebag-logic/milan-fpga@1de9179a` `review-evidence/pp148-r1` (round-1b receipts at `bed5f477`) and the manager's delta comment on the PR.
- **Hosted checks were read only** at `2026-10-05T05:58Z` (`receipts/hosted_checks.txt`). For both check suites at the exact head, `docs-gates` and `portability` had completed with success. `suites` was still in progress. That job does not run `ctr-mutants`.
- **Vivado not run.** The OOC 1x1 area is the executor's retained measurement. The delta is comment-only, so it carries over (§1).
- **No hardware.** Physical calibration NOT RUN. Field skips are not hardware proof.

## 6. Pending manager duties

- Return R476-2-F1: refresh the context of `ctr-notify-one-window.patch` and re-run `ctr-mutants` at the new head. The control must PASS, and the arm must be KILLED with its 4 recorded checks.
- Consider adding `ctr-mutants` (or the plant-only check) to the delta-round checklist, since the hosted job does not run it.
- Carry R476-2-R1 (PR body sentences 1-4) and R477-1-RES1 (the "TD 6 probes" cell) to the residue checklist.
- Build the final current-dev candidate at the merge turn: source base `07b1469ddf1e2a54e4a42cac06c41f084ecffd6c`, live dev `fa450d301805881ad713b67521477bf042ddadfd`.
- Hosted and act acceptance at the final head, including the `suites` job in progress here.
- Keep #158 separate.

## 7. Clone restoration

- All probes ran in scratch extractions made with `git archive`. Nothing was written into the review clone.
- The clone is at exact head `356c1bba`, tree `f43fb15d`, with HEAD detached.
- `git status --porcelain --ignored` is empty, and the worktree and index are clean.
- The index (mode, blob, path) hashes the same as the HEAD tree, `172a5480…08cdf8`, before and after the probes (`receipts/environment.txt`).
- The repository has no gitlinks, so there is no submodule pin to check.

## 8. Packet

All files listed below appear in `MANIFEST.sha256`. In the receipts, absolute local paths are replaced by `<PACKET>`, `<CLONE>`, `<PINNED_VERILATOR>` and `<VERILATOR_PREFIX>`.

- `delta_identity.sh`: comment-only diff, stripped-source, sv2v and preprocessor identity, `bed5f477` vs head. Output in `receipts/delta_identity.{log,rc}`.
- `plant_check.py`: checks that every mutation arm plants, without simulating. Output in `receipts/plant_check.{log,rc}`.
- `ctr-notify-one-window.refreshed.patch`: the candidate fix for F1, with context only refreshed. Output in `receipts/ctr_refresh_probe.log`.
- `receipts/ctr_one_window_apply.log`: `git apply --check` of every `ctr_mutations/` patch at both revisions.
- `receipts/ctr_driver_plant.log`: the driver's own `plant()` on both trees.
- `receipts/aecp_notify_head.{log,rc}`: `tb/aecp_notify` `make run` at head with the pinned simulator.
- `receipts/hosted_checks.txt`: hosted check runs at the exact head, read at `2026-10-05T05:58Z`.
- `receipts/environment.txt`: tool identities and clone state.

R476-2 FINISHED
