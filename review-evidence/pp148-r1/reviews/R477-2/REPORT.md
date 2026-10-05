[R477] NEGATIVE - exact head 356c1bbad2e9838659b433736040acf0cc4abf3e

# R477-2: external independent review of issue #148 / PR #159 (delta round)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #159, issue #148.
- Exact head `356c1bbad2e9838659b433736040acf0cc4abf3e`, tree `f43fb15d1a5cb8852b8e680b0f29bbd429cc5f4f`. Parent `bed5f47785839800bb640d7c747f5435f84ab5a3` (the R477-1 head). Source base `07b1469ddf1e2a54e4a42cac06c41f084ecffd6c`.
- Delta under review: one manager commit, `356c1bb`, which rewords the comment above the GET_COUNTERS selection stamp in `hdl/aecp/KL_aecp_notify.sv` to resolve R476-1-F1.

**Verdict: NEGATIVE.** One MAJOR finding is open (R477-2-F1, Tests lens). The comment change itself is correct: it touches comment lines only, the module's sv2v output is byte-identical, and the new text agrees with the banner, with the `N_EMIT_WAIT` comment and with the measured behaviour. But the reworded lines are context lines in a committed mutation patch, `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch`. At this head that patch no longer applies, so `tb/pp_top/ctr_mutants.py`, the ctr campaign, cannot plant one of its 17 arms. Issue #148 acceptance 3 ("the existing notification suites and campaigns stay green") therefore does not hold at this head. The fix is a context refresh of one patch file plus a ctr campaign re-run. One RESIDUE covers PR-body wording.

## 1. Reconstruction (order followed)

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` at any path. I read `docs/README.md`, which sets the conventions, single-source rules and the `make check` requirement.
2. **Issue #148, frozen acceptance.**
   1. Spacing is measured from send to send.
   2. A check fails on today's behaviour, with a mutant that restarts the spacing at selection.
   3. The existing notification suites and campaigns stay green.

   Scope decisions came from the manager comments 5982500256 (lane items and gates, including "the notify, ctr and pp_top campaigns at their counts"), 5985998608 and 5986055260 (round 1b union).
3. **Authorities.** Milan v1.2 §5.4.5 / Table 5.22 (`T-CTR-NOTIF`, one GET_COUNTERS notification per descriptor per second) and IEEE 1722.1-2021 §7.5.2, as the issue and 06 §7 cite them. The module banner (`KL_aecp_notify.sv:133-136`), 06 §7 (`docs/architecture/06_aecp_engine.md:894-898`) and 09 §8.
4. **Diff and history.** `git diff 07b1469d..356c1bba`. The delta `bed5f477..356c1bba` is one file, +4 -2.
   - The notify blob history is `89c95b3` at base, `9e97f8e` from `82e1664` through `bed5f47`, and `030192f` at `356c1bb`.
   - So the notify file at this head differs in bytes from the measured head `82e1664` and from `4ed463b`.
5. **Public evidence.** `kebag-logic/milan-fpga@1de9179a…/review-evidence/pp148-r1` holds the author's round-1b receipts. `source-provenance.txt` ties them to `4ed463b`/`bed5f477`. `r1c-head-camp-ctr.log` reads 18 of 18, with `ctr-notify-one-window` KILLED on 4 failures. That tree has no receipt at `356c1bba`.
   - The manager's PR comment 5988897133 lists the checks at this head: comment-only diff, sv2v identical, lint 41/41, `tb/aecp_notify` 34/34, CS 9/0. The ctr campaign is not among them.
   - Hosted checks at the exact head, at review time: `portability` and `docs-gates` succeeded, and `suites` was still in progress in both runs. The hosted workflow (`.github/workflows/hdl.yml`) runs no mutation campaign.
   - Physical calibration was NOT RUN. Field skips are not hardware proof.
6. **Prior public findings.** I read these only after my own pass over the delta, and after my verdict and ledger draft was written. They are resolved or retained in §4.

## 2. Executed evidence (this round)

| # | What | Result | Receipt |
|---|---|---|---|
| E1 | `scripts/delta_identity.sh` (bed5f477 vs 356c1bba) | Only `hdl/aecp/KL_aecp_notify.sv` changes (numstat 4/2), and every changed line is a `//` comment. The comment-stripped sources are identical. The sv2v output of the module (with the packages) is byte-identical at `a92a31fc…`. The whole-tree sv2v `all.v` (the Yosys gate's input recipe) is byte-identical at `68c73389…`. The Verilator 5.050 `-E -P` preprocessed module, with blank lines dropped, is byte-identical. Module lint at the head: rc 0 | `receipts/delta_identity.{log,rc}` |
| E2 | `scripts/lint_hdl.sh` at the head (pinned Verilator 5.050, disposable extraction) | 41 of 41 `LINT OK`, rc 0 | `receipts/lint_hdl-356c1bba.{log,rc}` |
| E3 | `scripts/focused_tests.sh`: `tb/aecp_notify make run` and `tb/pp_top gsi-build --spacing-only`, run concurrently | `aecp_notify`: 34 checks, 34 PASS. TW1: last job sent at ms 2600, next round at ms 3603. TW2: last job sent at ms 6504, next round at ms 7507. CS: 9 checks, 0 failures; CS2a/b/c closest rounds 115,077 / 115,070 / 115,077 clocks; at least 4 rounds per row. Both rc 0 | `receipts/focused-356c1bba/` |
| E4 | `scripts/plant_probe.py` at `07b1469d`, `bed5f477` and `356c1bba`. It checks every committed `*.patch` that edits `KL_aecp_notify.sv` with `git apply --check`, and every notify text edit of `notify_mutants.py` (44) and `d3_mutants.py` (2) with the drivers' own exactly-once rule. It builds nothing | Base and `bed5f477`: 10 of 10 patches apply and every anchor is found once. **`356c1bba`: `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch` is REFUSED** ("patch failed: hdl/aecp/KL_aecp_notify.sv:1233 … patch does not apply"). The other 9 patches and all 46 Python anchors still plant | `receipts/plant_probe.{log,rc}` |
| E5 | `scripts/ctr_arm_probe.sh` calls `ctr_mutants.plant()`, the driver's own function, in a disposable tree. No build, no simulation | At `bed5f477`: PLANTED. At `356c1bba`: `plant()` raises `CalledProcessError` from `git apply --check`. A reference copy of the patch, with only its two context comment lines replaced by the head's four and the hunk header refreshed, plants at the head. Its planted sv2v design is byte-identical to the committed patch planted at `bed5f477` (`ecb0824f…`), and it differs from the unplanted design | `receipts/ctr_arm_probe.{log,rc}`, `receipts/reference-ctr-notify-one-window.refreshed.patch` (reference only, not applied to any checkout) |
| E6 | Clone integrity after all probes | HEAD, tree and index tree are exact. `git status --porcelain --ignored` is empty. The worktree equals the index, which equals HEAD. All 558 tracked blobs re-hash to their index entries. Index and HEAD (mode, blob, path) hash the same, `172a5480…`. There are no gitlinks: the repository has no submodules, so there is no submodule pin to check | `receipts/clone-integrity.txt` |

Tool identity: `receipts/environment.txt` (Verilator 5.050 rev v5.050 through the scoped wrapper `905795b9…`; sv2v v0.0.13). I re-ran no campaign. E4 and E5 plant patches only and never build.

## 3. The delta, lens by lens

### Comment-only and byte identity (Focus 1 and 2)

The delta is comment lines only (E1). Removed: "Measure the one-second limit from emission selection, / not from the possibly much earlier pending instant." Added at `:1299-1302`: "Provisional stamp: it keeps the window shut until the / round's first job reaches N_EMIT_WAIT, whose stamp then / follows each job to its send, so the limit runs from the / round's last send (issue #148)." The stamp statements are now at `:1303-1304`.

The sv2v output, the whole-tree `all.v` and the preprocessed module are all byte-identical (E1). So every compiled consumer of the RTL (Verilator suites, Yosys, OOC synthesis) sees the same design as at `bed5f477`. That design also equals `82e1664`'s, because the notify blob is unchanged from `82e1664` to `bed5f477`.

### Agreement of the new comment (Focus 3)

- **Banner `:133-136`:** "their one-second limit runs from a round's last send". The new comment ends the same way. They agree.
- **`N_EMIT_WAIT` comment `:1441-1444`:** "the stamp follows the clock while a job waits for the engine and the TX slot, and holds its send, so the next round waits a second from this round's last send". The new comment says "whose stamp then follows each job to its send". They agree.
- **RTL reading:**
  - At the claim (`:1295-1304`), `ctr_last_r[pick_ctr_ix_w] <= now_ms_i` makes `now - last = 0`, so the window check at `:1099-1101` stays shut.
  - `N_EMIT_RD` reaches `N_EMIT_WAIT` within at most `N_CTRL_P` skip cycles, or ends the round.
  - In `N_EMIT_WAIT`, `:1445` overwrites the stamp each cycle until `core_done_w`.
  - So the claim stamp is provisional, and the last write is the round's last send, as stated.
  - Edge case, examined and accepted: in a round with no valid row, no job reaches `N_EMIT_WAIT`. The provisional stamp then stands, and the next round waits a second from that selection. Nothing is sent, so no spacing rule is at stake. The comment's "until the round's first job reaches N_EMIT_WAIT" does not misdescribe this case.
- **Measured behaviour (E3):** TW1 and TW2 present the next round 1,003 ms after the round's last send (2600 → 3603, 6504 → 7507). CS leaves at least 115,070 clocks between rounds. This matches "the limit runs from the round's last send".
- **06 §7 (`:894-898`)** states the same rule.

### PR body byte-identity claims (Focus 4)

These are no longer literally accurate at this head. The sentences that need correction are listed in RESIDUE R477-2-RES1. The design-level fact behind them still holds, by E1:
- PR body l.73-74: "notify RTL is byte-identical to that measured head".
- l.33-34: "Every compiled input at `4ed463b` equals the final head's".
- The current-head line (l.6) and the line references `:1443` and `:1299-1302` (l.111, l.115) are stale.

### Lenses

- **Conformance: CLEAN.** The delta changes no logic (E1). The R477-1 Conformance verdict stands at this head.
- **RTL: CLEAN.** The comment is accurate (above), sv2v is identical, and lint passes 41/41 (E1, E2). R476-1-F1 is resolved (§4).
- **Robustness: CLEAN.** No logic change. The R477-1 Robustness verdict stands.
- **Tests: UNCLEAN.** See R477-2-F1. The delta breaks the planting of a committed ctr campaign arm. The focused suites themselves pass (E3).
- **Docs: CLEAN**, with one RESIDUE (R477-2-RES1, PR-body wording) and the retained R477-1-RES1. The in-source comment, the banner, 06 §7 and the READMEs agree.

## 4. Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R477-2-F1 | MAJOR | Tests | `tb/pp_top/ctr_mutations/ctr-notify-one-window.patch:5-6` (context lines quoting the pre-`356c1bb` comment), against `hdl/aecp/KL_aecp_notify.sv:1299-1302` | Issue #148 acceptance 3; lane gate "the notify, ctr and pp_top campaigns at their counts" (5982500256); `ctr_mutants.py:78-82` plants with `git apply --check` under `check=True`. E4: the patch is REFUSED at `356c1bba` and applies at `bed5f477` and `07b1469d`. E5: the driver's own `plant()` raises at the head | At this head the ctr campaign cannot plant arm 9 of 17. `in_order` re-raises a unit's exception when its turn comes (`tb/common/mutant_pool.py:37`), so the campaign stops with an exception instead of 18/18. Acceptance 3 is unmet at the head. A merge would leave the ctr campaign broken on `main`. The manager's checks at this head (5988897133) do not exercise it | Refresh the patch's context to the four current comment lines (and its hunk header to the current line). `receipts/reference-ctr-notify-one-window.refreshed.patch` is a reference: it plants a design byte-identical to the committed arm at `bed5f477`. Re-run `ctr_mutants.py` at the new head. State the result in the PR body's ctr row and in the compiled-input sentence (l.33-34) | `python3 scripts/plant_probe.py <repo> <scratch> <new-head>` reports 0 refused. `ctr_mutants.py --jobs N` at the new head: control PASS, 17 of 17 KILLED, rc 0, and `ctr-notify-one-window` fails K15 x2, K16, K17 as in the published head record |
| R477-2-RES1 | RESIDUE | Docs | PR #159 body (as fetched; sha256 of body text `a1ef7d61…`, `receipts/pr-body-excerpts.txt`), l.6, l.23 table, l.71-74, l.111, l.115 | E1, and the blob history in §1.4 | Wording only. Each sentence below is stale or literally false at this head. The design they describe is unchanged (E1), so no figure, verdict or measurement moves | Exact fixes, listed after this table | Read the edited PR body against this head |
| R477-1-RES1 | RESIDUE (retained) | Docs | PR body l.41, "Six `pp_top` builds" Head cell: "TD 6 probes" | As recorded in R477-1. The cell is unchanged at this head | Wording only | Replace with "default 9,956; other five unchanged (TD 3 checks, 6 monitor probes answered, as at base)" | Read the edited PR body |

Exact fixes for R477-2-RES1:
- **l.6:** replace "current head `bed5f47785839800bb640d7c747f5435f84ab5a3`" with "current head `356c1bbad2e9838659b433736040acf0cc4abf3e`" (or the head after F1's fix).
- **Commit table:** add the row "| `356c1bb` | the selection stamp's comment describes it as provisional (R476-1-F1); comment lines only |".
- **l.71-72:** "gate 15 passes with processor pin `bed5f477`": name the pin at which gate 15 was last run.
- **l.73-74:** replace "notify RTL is byte-identical to that measured head." with "notify RTL differs from that measured head only in four comment lines (`356c1bb`); its sv2v output is byte-identical."
- **l.111:** "`:1443`" becomes "`:1445`".
- **l.115:** "(`:1299-1302`)" becomes "(`:1303-1304`, under its comment at `:1299-1302`)".

### Prior public findings at this head

| Finding | Status at `356c1bba` | Evidence |
|---|---|---|
| R476-1-F1 (MINOR, RTL, Docs; stale selection-stamp comment) | **Resolved.** The comment now carries the reviewer's required wording. All four of its listed verifications hold: comment-only diff, sv2v identical, lint 41/41, `aecp_notify` and `--spacing-only` pass. Its follow-on effect on the ctr patch is new finding R477-2-F1 | E1, E2, E3 |
| R476-1-S1 (SUGGESTION, Tests; no check holds the limiter at exactly 1,000 ticks) | Retained as SUGGESTION. The delta does not touch it | n/a |
| R476-1-S2 (SUGGESTION, Tests; kind guard on the `N_EMIT_WAIT` stamp line, now `:1445`, not graded) | Retained as SUGGESTION. The line moved from `:1443` to `:1445` | E1 |
| R477-1-RES1 (RESIDUE, Docs; "TD 6 probes") | Retained. The PR body is unchanged there | `receipts/pr-body-excerpts.txt` |
| R477-1-S1 (SUGGESTION, RTL, Docs; incomplete comments at `:1299-1300` and `:399-401`) | The `:1299` half is **resolved** by `356c1bb`. The `:399-401` half is retained as SUGGESTION: "is written in the cycle that sets the bit" omits the `N_EMIT_WAIT` rewrites | source at head |
| R477-1-S2 (SUGGESTION, Robustness, Conformance; carry the stamp-follow guard to #158) | Retained, carried to #158 | n/a |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta `bed5f477..356c1bba` (comment-only, E1); `KL_aecp_notify.sv:1099-1101,1295-1304,1440-1453`; 06 §7; issue #148 acceptance; R477-1 conformance evidence carried (logic identical by E1) | R477-2 (delta), R477-1 (rest) | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| RTL | CLEAN | E1 sv2v module and `all.v` identity, preprocessed identity, module lint; E2 `lint_hdl.sh` 41/41; new comment vs banner `:133-136` and `N_EMIT_WAIT` comment `:1441-1444`; R476-1-F1 resolved | R477-2 | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| Robustness | CLEAN | no logic change (E1); empty-round and withdrawal paths re-read against the new comment; R477-1 robustness evidence carried | R477-2 (delta), R477-1 (rest) | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| Tests | UNCLEAN (R477-2-F1) | E3 focused TW/CS runs; E4 all 10 notify patches and 46 driver anchors at base, `bed5f477` and head; E5 the ctr driver's `plant()`; published `r1c-head-camp-ctr.log` (at `4ed463b`) | R477-2 | 356c1bbad2e9838659b433736040acf0cc4abf3e |
| Docs | CLEAN (R477-2-RES1, R477-1-RES1 RESIDUE) | in-source comments `:133-136`, `:399-404`, `:1299-1302`, `:1441-1444`; 06 §7 `:894-898`; 09 §8 TW row; `tb/aecp_notify/README.md`; `tb/pp_top/README.md` references to the last send; PR body identity sentences and line references | R477-2 | 356c1bbad2e9838659b433736040acf0cc4abf3e |

## 6. Real limits

- **No campaign was re-run,** as the brief instructs. F1 rests on `git apply --check`, on the ctr driver's own `plant()` (E4, E5) and on the driver's source. I did not observe the campaign's terminal output at this head.
- **Banks not run here:** the full processor suites (I ran only the focused TW and CS sections), Yosys `run.sh` (I compared only its sv2v input, `all.v`), the notify, d3, aecp, acmp, dispatch, gsi, name-write, ADP and MAAP campaigns, the six `pp_top` build totals, and the parent consumer set.
  - For notify and d3, E4 shows every notify anchor still plants.
  - Any parent-side mutation patch that quotes the old comment text was not searched: the parent checkout is out of bounds. The manager's parent banks at this head were reported as passing, but no public receipt was available to me.
- **No public receipt for this head.** The evidence tree at `1de9179a` holds round-1b receipts for `4ed463b`/`bed5f477` only. The manager's checks at `356c1bba` are known from comment 5988897133.
- **Not run:** Vivado (the OOC figures are the author's receipts; E1 shows the synthesized design is unchanged), hardware, Docker/act, physical calibration.

## 7. Pending manager duties

- Return R477-2-F1: refresh `ctr-notify-one-window.patch` and re-run `ctr_mutants.py` at the new head. Re-check every other committed patch or anchor that quotes `KL_aecp_notify.sv` comment text: E4's script covers the processor side, and the parent side was not checked here.
- Carry R477-2-RES1 and R477-1-RES1 to the residue checklist.
- Hosted acceptance at the final head: `suites` was in progress at review time.
- Build the final current-dev candidate at the merge turn (source base `07b1469d`, live dev `fa450d30`), with the parent consumer set and all five adoption patches, including gate 15.
- Keep #158 open and separate.

## 8. Packet

Scripts are in `scripts/`; raw receipts are in `receipts/`. Every publishable file is listed in `MANIFEST.sha256`. In the build logs, a private install prefix of the Verilator package is replaced by `<VERILATOR_PREFIX>`; nothing else is edited. Disposable trees stayed under `scratch/`, which is not published. The review clone is at the exact head and clean (E6).

R477-2 FINISHED
