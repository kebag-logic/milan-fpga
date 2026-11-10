[R814] POSITIVE - exact head 2131eff48066da1e3bbeb6b417ea0655fa7c7741

# R814-2: external delta review of PR #874 (issue #867, Mark II split S7), round 2

Head `2131eff48066da1e3bbeb6b417ea0655fa7c7741`, tree `b61ef3ca8b8c07a89ba7fb32071eadf3550b31e3`. This is two commits on round 1's `5fb6904f`: `0d8e89bc` (F-1) and `2131eff4` (F-2). The PR base is `dev-soft-core` `1d6bf555`, which is an ancestor of the head.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open. All five lenses are clean at this head. R814-1's F-1 and F-2 are resolved as the round 2 ruling (PR #874 issuecomment-6763709522) and its follow-up (issuecomment-6765717898, option (a)) define them. Three RESIDUE items and four SUGGESTIONs follow. None of them affects coverage.

Scope: I judged the delta `5fb6904f..2131eff4` and both named prior findings at their cause. Code the delta does not touch keeps R814-1's lens verdicts at `5fb6904f`. `git diff --raw 5fb6904f..2131eff4` lists five files, all modes 100644:
- `tb/verilator/milan_dp/srptx_grade.py`, `srptx_plants.py`, `srptx_mutants.py` and `README.md`;
- `sw/firmware/ctrl/srp/README.md`.

There is no HDL, no firmware C and no workflow file (`receipts/delta-5fb6904f-2131eff4.diff`).

## The four questions

1. **F-1: one SVC_MS = 20.** It holds.
   - `srptx_grade.py:64` is the only allowance literal. Every bound is derived from it:
     - `RATE_WINDOW_MS` `:74` = 280;
     - `JOIN_FOLLOW_MS` `:75` = 220;
     - `JOIN_BOUNDS_MS` `:78` = 160 to 260;
     - `LEAVE_ALL_BOUNDS_MS` `:79` = 9,780 to 15,220;
     - the `[608]` window, `:544` (`deadline + SVC_MS`).
   - Searching the three scripts and both READMEs finds no 18, 218, 282, 9,782 or 15,218 figure. The one exception is the history note in the comment at `srptx_grade.py:62-63`, which says what was superseded.
   - The PR body's item 3 row (line 58 of `receipts/pr874-body-snapshot.md`) states 20, 220, 160 to 260 and 9,780 to 15,220.
   - `srptx_plants.py:27` holds a second 20 (`ITEM3_SVC_MS`) on purpose. It is the plants' independent oracle, taken from item 3, and is disclosed in the README and PR body. Deriving it from the grade would let a drifted grade pass its own plants.
   - The literal itself is what the follow-up ruling accepted until #810.
   - `join-late-past-t-svc` sits 1 ms outside the bound, at 221 ms ("followed at ms 222, past JoinTime + T_svc (220 ms"). Its control at 219 ms grades clean.
2. **F-2: JoinTime graded on both sides.** It holds.
   - `grade_time` (`srptx_grade.py:330-336`) grades every Join-timer interval from `join_intervals` (`:400-404`). That is the interval `measure_time` reports, now shared through `causes` (`:385-397`). The bound is 160 to 260 ms: Milan Table 4.3 / `FR_NFR.md` 3.4.1's 180 to 240 ms, widened by T_svc on each side.
   - The 10 cs and 15 cs lwSRP arms are each refused by the new words, in `make srptx-mutants` and in my regrade.
   - With the new check removed, both arms grade with 0 findings. So do the two new plants (`receipts/probe-join.txt` §2, `receipts/probe-regrade.txt`).
3. **Unplanted Join-timer intervals.** All are inside 160 to 260 ms. Every measured block equals the author's round 2 report and R814-1's round 1 report (`receipts/report-compare.txt`).

   | Scenario | MSRP | MVRP |
   |---|---|---|
   | wire | N 104, 198.989 to 200.000 ms | N 104, 198.989 to 200.015 ms |
   | hold | N 34, 198.989 to 200.000 ms | N 32, 198.989 to 200.000 ms |
   | licence | N 8, 198.989 to 200.000 ms | N 5, 198.989 to 200.000 ms |

4. **Nothing outside tb/ and docs changed.** It holds. The delta's only file outside `tb/` is `sw/firmware/ctrl/srp/README.md`, a documentation page with a one-line change at `:384`.
   - Over the whole PR (`1d6bf555..2131eff4`), the files outside `tb/` and `docs/` are:
     - `scripts/measure_test_evidence_readers.py`;
     - `sw/firmware/ctrl/README.md` and `sw/firmware/ctrl/srp/README.md`;
     - `sw/firmware/ctrl/test/ctrl_configs.py`.
   - Round 1 introduced all of these, and R814-1 judged them there, except the srp README line above.

## Prior findings, resolved or retained at this head

| ID | Status | Evidence at `2131eff4` |
|---|---|---|
| R814-1 F-1 (MINOR: 18 ms, not 20) | **RESOLVED** | Q1 above. The probe re-derives the grade at 19 and 21 ms, and each time 5 plants fail (`receipts/probe-join.txt` §3). At 20 ms, 25 of 25 are refused and 3 of 3 controls are clean. So the grade is pinned to item 3's millisecond. |
| R814-1 F-2 (MINOR: early side of JoinTime ungraded) | **RESOLVED as ruled** | Q2 above. R814-1's own probe, run unchanged: `join-10cs` REFUSED (15 findings), `join-15cs` REFUSED (16), `join-30cs` REFUSED (22), `join-17cs` ESCAPED. At round 1, `join-10cs`, `join-15cs` and `join-17cs` all escaped. 170 ms is inside the 160 to 260 ms bound the ruling set, so F-2's verification clause naming 17 cs is superseded by ruling item 2. F-2's other clause ("give the rate rule a stimulus or mutant that exercises it") was not adopted by the ruling. It is carried as S-2. |
| R814-1 S-1 (timer `id` is a heap pointer) | retained, SUGGESTION | My capture hashes differ from the author's (`receipts/captures-sha256.txt` against the author's `srptx/captures-sha256.txt`), while all three reports are equal. |
| R814-1 S-2, S-3 | retained, SUGGESTION | The delta does not touch them. |
| R813-1's four SUGGESTIONs | not re-examined | The ruling sends them to the residue checklist at merge. |

## Findings

### R-1 RESIDUE: the PR body still reads as a STOP awaiting a decision

- **Lenses:** Docs.
- **Where:** PR #874 body, line 17 ("STOPPED at the round 2 head …") and line 25 ("This needs a decision (below).") of `receipts/pr874-body-snapshot.md`.
- **Evidence:** The decision was taken: issuecomment-6765717898 chose option (a). There is no decision section below line 25. The "Known limitations" bullet already states the outcome.
- **Impact:** Wording only. A cold reader is told review is blocked when it is not.
- **Exact fix:**
  - Replace line 17's opening with "Round 2 at `2131eff4`, accepted for delta review on the ruling's option (a)."
  - Replace "This needs a decision (below)." with "Option (a) was ruled: the literal stays until #810, and switching to the budget source is on the residue checklist (#495), owned by #810."
- **Verification:** read the PR body.

### R-2 RESIDUE: two garbled phrases in the grade's prose

- **Lenses:** Docs.
- **Where:** `tb/verilator/milan_dp/srptx_grade.py:20-21` (module docstring) and `:331` (comment).
- **Evidence and exact fix:**
  - `:20-21` reads "each a Join timer sends within JoinTime's range (180 to 240 ms) of the one before, on each side (10.7.4.1)". Change it to "each transmit opportunity a Join timer sends within JoinTime's range (180 to 240 ms) of the one before, widened by T_svc on each side (160 to 260 ms; 10.7.4.1, 10.7.11)".
  - `:331` reads "# each a Join timer sent, after the one before it". Change it to "# each transmit opportunity a Join timer sent, against the one before it".
- **Impact:** Wording only. No figure, check or output changes. The comment rule is met: issue and clause IDs only.
- **Verification:** `python3 -B srptx_grade.py --help` shows the docstring; `make srptx-plants` is unchanged.

### R-3 RESIDUE: the README names the rate window without its T_svc term

- **Lenses:** Docs.
- **Where:** `tb/verilator/milan_dp/README.md:1554`, the `[TIME]` row: "No four transmit opportunities in 1.5 x JoinTime (280 ms)".
- **Evidence:** 1.5 x JoinTime is 300 ms. The grade's window is 1.5 x JoinTime less T_svc (`srptx_grade.py:74`, and its own words at `:329`). The figure 280 is right; the name is not.
- **Impact:** Wording only.
- **Exact fix:** "No four transmit opportunities in 1.5 x JoinTime less T_svc (280 ms)".
- **Verification:** read the row.

### S-1 SUGGESTION: the Join upper bound assumes the frame before armed the timer

- **Lenses:** Robustness, Tests.
- **Where:** `srptx_grade.py:385-397` (`causes`: a frame is "join" if the latest Join or periodic expiry within `ATTRIBUTE_MS`, 100 ms (`:94`), is a Join expiry) and `:400-404`.
- **Evidence:**
  - lwSRP's Join timer is a hold-off, armed at each transmit (`third_party/lwSRP/src/core/mrp_mad.c:1421`, `:1539-1540`).
  - Suppose a transmit is requested 61 to 99 ms after an idle Join expiry, for example by a peer event off the 1 ms-aligned periodic grid. That frame is attributed to the Join timer and measured 261 to 299 ms from the frame before, so it is refused although nothing was late.
  - No such case occurs in the three scenarios: the maximum is 200.015 ms, and the peer stimuli fall on whole seconds.
- **Impact:** A false refusal: it fails loudly and lets no defect through. It would surface only when a scenario adds off-grid peer events (S2b and later).
- **Suggested outcome:** Attribute a frame to the Join timer only when its egress falls within T_svc of that expiry, or state the assumption in the README's `[TIME]` notes.

### S-2 SUGGESTION: the rate rule and the `[608]` window have no boundary pair

- **Lenses:** Tests.
- **Where:** `srptx_plants.py` (`rate` moves frames by 1 and 2 ms, far inside 280 ms); `srptx_mutants.py` (the #608 arm stops 2 s late).
- **Evidence:**
  - A drift of `RATE_WINDOW_MS`, or of the `[608]` window's `+ SVC_MS` term, is refused by no plant.
  - My ±1 ms SVC drift is caught only through the Join and LeaveAll plants' words.
  - R814-1's `no-join-wait` arm still escapes. It sends 3 MSRP frames 23 µs apart in ms 1, each with no timer cause (`receipts/probe-regrade.txt`). That is within `FR_NFR.md` 3.4.1 ("at most three per 1.5 x JoinTime" for a requested point-to-point opportunity), so it is not an item 3 defect.
- **Suggested outcome:** A plant/control pair at four frames in 279 and 281 ms, and one at the `[608]` deadline + 21 and + 19 ms. Optionally, a code arm the rate rule kills.

### S-3 SUGGESTION: the controls sit exactly on a bound 1 ms tighter

- **Lenses:** Tests.
- **Where:** `srptx_plants.py:96-115`.
- **Evidence:**
  - At SVC_MS = 19 the three controls stay clean, because the comparisons are inclusive. The 1 ms drift is refused only because each plant's words embed the figure (`receipts/probe-join.txt` §3).
  - The README's "holds the grade's bound to the millisecond" is therefore true through the words, not through the controls' numbers.
- **Suggested outcome:** Say so in the README's controls paragraph, or move the controls 2 ms inside.

### S-4 SUGGESTION: keep the plants' figure on item 3 when #810 lands

- **Lenses:** Conformance, Tests.
- **Where:** `srptx_plants.py:27` (`ITEM3_SVC_MS = 20`).
- **Suggested outcome:** When the grade switches to the budget source (#495 residue line, owned by #810), keep the plants' figure tied to #867 item 3 and not to that source, so the oracle stays independent of the grade. Name this on the residue line.

### Comment rule

The delta's added source comments and docstrings (`srptx_grade.py`, `srptx_plants.py`, `srptx_mutants.py`) carry issue and clause IDs and dates only. A search of the delta's added lines for lane labels, reviewer or author IDs, round names and issue-comment IDs found none. The only issue-comment link is in `tb/verilator/milan_dp/README.md:1554`, a documentation page, where it replaced an earlier link. There is no RESIDUE under that rule.

## What I ran at this head, in this clone (all in `receipts/`)

- **Toolchain.** Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, "Verilator 5.050 2026-07-01 rev v5.050").
- **`make srptx`: rc 0** (`make-srptx.log`, `.rc`). Findings per scenario:
  - wire: 0 findings, 1,449 MRPDUs, 600,000 ms;
  - hold: 0 findings, 169 MRPDUs;
  - licence: 0 findings, 69 MRPDUs.
- **`srptx_plants.py obj_srptx`: rc 0.** "25 of 25 refused; 3 of 3 controls inside their bound clean" (`srptx-plants.log`).
- **`srptx_mutants.py`: rc 0.** 5 clean controls, then "12 of 12 refused". The 10 cs and 15 cs arms are refused by "… 98.989 / 148.989 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms" (`srptx-mutants.log`).
- **R814-1's `probes/code_probe.py`, unchanged: rc 0.**
  - Its sha256, `0e5d16ae…736c`, equals the entry in its published MANIFEST.
  - The nine reviewer arms (`r814-1-code-probe.log`): 10 cs, 15 cs, 30 cs, `leaveall-5s`, `no-pdu-endmark`, `msrp-group-on-all` and `lv-fast-leave` are REFUSED; 17 cs and `no-join-wait` ESCAPED, both explained above.
- **My probes** (`probe_join.py`, `probe_regrade.py`; outputs `probe-join.txt`, `probe-regrade.txt`, `unplanted-gaps.txt`):
  - the Join intervals per scenario;
  - the new check ablated: the two new plants and both arms then give 0 findings, and the plant set gives 23 of 25;
  - SVC_MS drift at 19, 21 and 20;
  - the README's claim that a frame 219 ms after the first leaves the next 179.989 ms later: confirmed (gaps 219.000 then 179.989);
  - no same-application gap under 160 ms of any cause in any unplanted run.
- **Docs gates: all rc 0** (`docs/`).
  - Run with the system Python: `docs_check.py`, `measure_test_evidence.py --check`, `check_doc_style.py`, `check_doc_paths.py`, `check_hygiene.py --check`, `check_py_idiom.py`, `check_todo_ownership.py`, and `git diff --check 1d6bf555 HEAD`.
  - Run with the pinned Markdown venv, whose name matches the sha256 prefix of `tools/markdown/requirements.txt` (versions in `docs/md-venv-identity.txt`): `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base 1d6bf555` (0 findings over 235 added lines).
  - The system-Python attempts at those three failed with "renderer not installed". Those logs were overwritten by the venv runs.
- **Author packet** (`evidence-packet-verify.txt`).
  - At archive `75b5cb59`, `review-evidence/665s7-r1/MANIFEST.json` has 206 entries, 43 under `author-r2/`. There are 0 sha256 mismatches and 0 unlisted files.
  - The archive commit has no GPG signature, so the binding is the manifest's hashes.
  - The author's join figures, mutant probe, plant probe and gate verdicts agree with my own runs.
- **Restore** (`restore-check.txt`): `write-tree` = `b61ef3ca…`; 0 index and 0 worktree differences; clean `git status`; all six gitlinks match HEAD (`external` uninitialised, as at the start); lwSRP worktree clean. Only ignored build outputs remain; my probe's `__pycache__` was removed.

**Hosted, at query time** (`hosted-check-runs-2131eff4.tsv`):
- 3 completed success: `full-ci-gate`, `bdd-conformance`, `docs-check-no-git`;
- 1 skipped: `Physical gPTP (nightly and manual)`, a skipped context and not an execution;
- 31 queued or in progress: the 19 Verilator shards, pinned Yosys, docs gates, elaborate gates and fail-fast.

This is inspection only. The manager owns hosted and act acceptance.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srptx_grade.py:58-79`, `:318-375`, `:385-404`, `:544`, against #867 item 3, the ruling and its follow-up, `docs/reference/FR_NFR.md` 3.4.1 (180 to 240 ms; "at most three per 1.5 x JoinTime"), and the 802.1Q-2018 10.7.4.1, 10.7.11 and Table 10-7 citations; the PR body item 3 row; unplanted interval figures | R814-2 | 2131eff48066da1e3bbeb6b417ea0655fa7c7741 |
| RTL | CLEAN | `git diff --raw 5fb6904f..2131eff4` (5 files, no HDL or firmware source, so the RTL scope is untouched since R814-1's clean RTL lens at `5fb6904f`); the datapath arm "the split's ACTIVE term held open" still refused at this head (`srptx-mutants.log`) | R814-2 (delta); R814-1 (unchanged RTL) | 2131eff48066da1e3bbeb6b417ea0655fa7c7741 |
| Robustness | CLEAN | `join_intervals` hold and queue exclusions (`srptx_grade.py:400-404`) on the hold scenario (N 34/32 graded, 0 findings); unplanted gaps of any cause (`unplanted-gaps.txt`); code arms at 10, 15, 17 and 30 cs and `no-join-wait`; `mrp_mad.c:1421`, `:1539-1540`; S-1 | R814-2 | 2131eff48066da1e3bbeb6b417ea0655fa7c7741 |
| Tests | CLEAN | `srptx_plants.py` (25 plants, 3 controls), `srptx_mutants.py` (12 arms), the new-check ablation, SVC_MS drift at 19, 21 and 20, R814-1's probe unchanged; S-2, S-3, S-4 | R814-2 | 2131eff48066da1e3bbeb6b417ea0655fa7c7741 |
| Docs | CLEAN (RESIDUE R-1 to R-3 carried) | `tb/verilator/milan_dp/README.md:108`, `:1554-1556`, `:1600-1612`, `:1617-1662`, `:1676-1682`; `sw/firmware/ctrl/srp/README.md:381-386`; `docs/design/MAILBOX_SPLIT.md:1849-1858` (unchanged, cites no figure); PR body; docs gates rc 0 | R814-2 | 2131eff48066da1e3bbeb6b417ea0655fa7c7741 |

## Real limits

- No manager source bank ran at this head, and I claim none. Source-head execution evidence is the author's published receipts plus my focused runs above.
- I did not run the full sweep, the firmware self-test, the firmware mutant drivers, S2's harness, `test_builder.py`, `behave`, or the rtl and elaborate workflows. The delta touches none of their inputs. The author also did not run them at this head (STOP comment).
- I had no IEEE 802.1Q-2018 or Milan v1.2 text in the repository. Clause readings rest on `FR_NFR.md` 3.4.1 and the clauses the code cites.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The host was heavily loaded (load average about 89) by other lanes, so wall times are not meaningful.

## Pending manager duties

- Validate the current-dev merge candidate (live dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`, builder and native banks), and run hosted and act acceptance at the exact head (31 contexts were still pending at query time).
- Carry R-1, R-2 and R-3, the SVC_MS switch to the budget source (#495, owned by #810, with S-4's note), and R813-1's four SUGGESTIONs to the residue checklist.
- Collect R813-2's verdict at this head. Merge needs explicit maintainer authorisation.

R814-2 FINISHED
