[R460] POSITIVE - exact head 4811c21d8fe29faa1e9e713a6622bb206189e74b

# R460-3: internal independent review of issue #85 / PR #152 (GAP-16, ADP MTXW walk), round 3

- Exact head `4811c21d8fe29faa1e9e713a6622bb206189e74b`, tree `320166a09c124757e9f217dbb91f822690f87c34`, detached clone. It was verified clean and byte-exact after every run (`receipts/clone-integrity.txt`: 515 index entries, every tracked blob and mode rehashed, 0 gitlinks, no `.gitmodules`).
- Source base `5c71928ad2bf1a854a5538d69b77214dfdf1697f`. Round-3 delta `4298ed25..4811c21d`, tests only.
- Scope read, in this order:
  1. The repository carries no AGENTS.md or CONTRIBUTING.md at this head. I read `README.md` and `docs/README.md` (conventions, single-source rules, `make check`).
  2. Issue #85: body and acceptance; lane 5974306370; round 2 5975300666; round 3 5975655103.
  3. 04 F04.7 and F04.8.
  4. The full diff from the base and the round-3 diff.
  5. Public evidence (`receipts/evidence-read.txt`).
- Prior public reviews were read only after this review's verdict and ledger draft (`receipts/verdict-draft.txt`).
- Simulator: pinned Verilator 5.050 wrapper, identity checked (`receipts/simulator-identity.txt`).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head, and no new RESIDUE. One new SUGGESTION (S3-1).

- R461-2-F1 (MINOR) is resolved: the noted index is now graded exactly, from both sides.
- Every round-3 item of 5975655103 is delivered and verified by execution.

## What round 3 does, and how it was verified

### Item 1: R461-2-F1, the noted index graded exactly

The code (`tb/adp_engine/sim_main.cpp`):
- `walk_discovery_cell` (`:1591`) calls `check_noted_index` (`:1599-1626`) for every cell `notes_index` selects (`:344-346`).
- The lower side: an AVAILABLE repeating the noted index, grandmaster and domain matching, must give EVT_TK_DEPARTED then EVT_TK_DISCOVERED (`:1608`). That proves noted >= N.
- The upper side: the cell is walked again, and an AVAILABLE at N + 1 must give no event (`:1622`). That proves noted <= N.
- Both checks run inside the cell's `fails` window, so a failure clears `cell_ok` (`:1665`) and fails the arc check (`:1674`).
- The messages state what each side proves ("the noted index is at least / at most N").

Why the second walk is needed: the lower side's restart pair notes N again through the restart branch (`KL_adp_engine.sv:361-366`). The re-walk restores the cell's own end state before the upper side runs.

Execution:
- Suite: `receipts/suite-adp_engine.log`: rc 0, `1348 checks: 1348 PASS`, and the `P13 MTXW` summary (F04.2 45 cells: N 12, I 20, S 6, C 7; F04.3 33 cells: N 13, I 15, S 2, C 3; 8 arcs).
- 1348 = 1334 + 14. Each fresh cell grows by 4: two checks for the upper side, two for the re-walk's consumed checks. The restart cell adds 6.
- Campaign (`receipts/campaign.log`, `--jobs 12`): both controls PASS, 41 of 41 arms KILLED, `43 checks: 43 PASS`, rc 0.
  - `arc-fresh-store-plus-one` and `arc-fresh-store-max` are R461-2's q1 and q2 edits, byte for byte (compared with `scripts/prior/r461_probes.py`). Each fails 4 checks: the "at most 701" side of both index > last cells (`got 2 events`), arc 4's check and the arc count.
- Arm counts against the README (`receipts/campaign-vs-readme.txt`): 39 of 41 rows equal. The other two are pp_top rows, `cfg-valid-no-reset` (9, row leads with 5) and `gate-enable-dropped-top` (7, row leads with 3). Their own text states those counts ("9 since lane P1's AD8 and AD9"; "At the head of lane P1 it fails 7"). The PR leaves both lines untouched, and round 2 recorded them the same way. The four rows round 3 changed (`disc-fresh-checks-gm` 5, `disc-not-discovered-checks-index` 17, `disc-restart-not-rediscovered` 8, `arc-restart-detector-off-by-one` 13) match their FAIL lists line by line.
- Reviewer probes (`scripts/probes3.py`, `receipts/probes3/probes3-summary.txt`). The control passes 1348.
  - Exact-value faults on the fresh arc fail arc 4: `s5` (notes the index − 1) and `s6` (notes the low byte only).
  - `s7` (the fresh arc notes only on a grandmaster and domain match) fails the GM-mismatch × DISCOVERED cell, where F04.8's grandmaster-free guard puts it.
  - Each side is load-bearing:
    - `t1`: with the upper side neutralised, the +1 fault passes 1348 of 1348.
    - `t2`: with the lower side neutralised, the no-store fault passes 1348 of 1348.
    - With both sides in place, both faults are killed (campaign).

### Item 2: R461-1-S2, the restart cell

- The cell now sends `DISC_LAST - 1` = 699 (`apply_disc`, `:1508`; `noted_index`, `:349-351`) and gets the same two-sided check.
- A restart that notes nothing leaves 700, which the upper side sees as a restart at 700.
- Probes:
  - `s1` (the r7 / q4 edit) fails the restart cell's "at most 699" line, arc 5 and the arc count, plus P9e2.
  - `s2` (+1) and `s4` (maximum) fail the upper side and arc 5.
  - `s3` (−1) fails the lower side and arc 5.
  - `t3`: with the upper side neutralised, `s1` again fails P9e2 only. So the walk-cell kill comes from the new upper side, as item 2 required.
- The index-equal-to-last boundary is still walked. The lower side's repeat sends it, and so do the GM- and domain-mismatch cells. `arc-restart-detector-off-by-one` stays KILLED, with 13 failures.

### Item 3: R461-2-S1, the named constant

- `DISC_LAST = 700` (`:339`) is used at the three sites: `goto_disc` (`:1484`), `apply_disc` (`:1496`) and `noted_index` (`:350`). No 699, 700 or 701 literal remains in the file.
- Probe `t4` moves the constant to 9000: the run passes 1348 of 1348, so every site follows it.
- Probe `t5` makes the same move under the +1 fault: arc 4 fails, at "at most 9001". The check keeps its teeth.

### Item 4: R461-1-R1, exactly

- `tb/adp_engine/README.md:100-101` reads verbatim the fix R461-1 required: "The table above gives each cell's class and, for its N cells, the Milan clause; F04.7 gives every cell's Milan clause and adds its IEEE clause."
- F04.7 (`docs/architecture/04_adp_engine.md:184-211`) gives a Milan and an IEEE clause in every row, so the sentence is true.

### Prior probes rerun unchanged

The script hashes equal their published manifests (`receipts/evidence-read.txt`).

- **R460-1 `probes.py`** (`receipts/r460-1-probes/probes-summary.txt`):
  - The control passes 1348.
  - `r6` and `r7` each fail their walk cell and arc. `r7` now fails arc 5, where at `4298ed2` it failed P9e2 only.
  - `x1` passes 1352; `x2` is red.
  - Compared with round 2 (`receipts/r460-1-probes-vs-round2.txt`):
    - `r6` and `x2` differ only in the reworded "at least" message.
    - `r8` adds the GM-mismatch cell's "at most" line (11 failures).
    - Every other probe gives identical FAIL lines.
- **R461-2 E8 (`r461_probes.py`)** (`receipts/r461-probes.txt`):
  - q0, q1 and q2 each fail arc 4's check (q1 and q2 passed at `4298ed2`).
  - q3 fails the GM-mismatch cell.
  - q4 fails arc 5 and P9e2.
  - q5 reports ANCHOR: the round-2 line it removed is replaced. My `t1` to `t3` take over its vacuity role.
- **R461-2 E9 (`pptop_q2.sh`)** (`receipts/pptop-q2-run.log`): `tb/pp_top` under q2 passes 10416 of 10416, as at round 2. pp_top does not grade the noted index; `tb/adp_engine` does, through `arc-fresh-store-max`.
- **R461-2's `r461_fixcheck.py`** (variants A and B): every unit reports ANCHOR. It patched the round-2 follow-up, which round 3 replaced. The two-sided check it tested for feasibility is now in the tree.

## Lens findings

- **Conformance: CLEAN.**
  - F04.8's fresh row (`04_adp_engine.md:254`, "note the index", Milan §5.6.4.5.2 steps 1, 3) and restart row (`:255`, steps 2a, 2c, 3) both note the received index.
  - The walk grades exactly the three cells whose arcs take those branches. The fresh guard reads no grandmaster, so both index > last cells are included, and the restart cell is the match, index <= last cell.
  - The RTL takes those branches at `KL_adp_engine.sv:358-366`.
  - The expectations come from F04.8, not from the RTL: the restart pair for an index at or below the last noted one, nothing for a fresh one.
- **RTL: CLEAN.**
  - Round 3 changes nothing under `hdl/`, `docs/`, `syn/` or `scripts/` (`receipts/hdl-comment-only.txt`).
  - Over the whole PR, `hdl/adp/KL_adp_engine.sv` is identical to the base with comments stripped (same sha256).
  - The two new patches apply cleanly, and each changes only the fresh branch's write data (the campaign's `git apply --check`).
- **Robustness: CLEAN.**
  - Every campaign and probe unit ran in a private copy under scratch. The clone was never written.
  - The upper side measures over `idle(20)`. The same window catches the 2-event pair under the q1, q2, `s1`, `s2` and `s4` faults, so a late event cannot slip past it.
  - Each re-walk starts with `goto_disc`, whose unbind disarms the sink, so no state leaks into the next cell. Every later cell and the P10 invariants stay green in the control.
- **Tests: CLEAN.** Covered by suite, campaign, README counts and probes, all above.
- **Docs: CLEAN.**
  - README `:6` (1348) and `:148-158` (the two-sided paragraph, the 699 restart walk, and which arc check each cell feeds) are accurate against the code and the probes. So are `:160-168` (the two new arms), `:264-270` (the third-round campaign sentence and counts) and the changed mutation-record rows (`:296-311`).
  - The PR body's round-3 section agrees with my measurements: 1348, 41 of 41, the q-probe and r-probe outcomes, the restart cell at 699 and `DISC_LAST`.
  - `make check` rc 0 (`receipts/make-check.log`): mermaid and wavedrom lint, links 1120, matrix 115 REQ / 17 GAP, 94 rows with 0 untested, parameters 28. `gen_matrix.py --check` rc 0.
  - S3-1 is a suggestion only.

### S3-1: SUGGESTION (Docs). Ragged source wrap in two README paragraphs

- **Lenses:** Docs.
- **Where:** `tb/adp_engine/README.md:102` and `:157`.
  - `:102` stops at "the PRNG draw". Commit `4811c21` rewrapped one line, but the rest of the paragraph was not reflowed.
  - `:157` runs to 84 columns, where its neighbours stay near 80.
- **Evidence:** read at the head. The rendered Markdown is identical either way.
- **Impact:** none. It changes no rendered text, measurement or claim, so it is below RESIDUE.
- **Suggested outcome:** optional. Reflow both paragraphs when the file is next edited.
- **Verification:** `awk 'length>80' tb/adp_engine/README.md`, and read the lines.

## Prior public findings at this head

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R461-2-F1 (MINOR, Tests): noted index only lower-bounded | **Resolved** | Two-sided check `sim_main.cpp:1599-1626`; q1 and q2 planted as arms and KILLED through arc 4; probes `s5`, `s6`, `t1`, `t2` |
| R461-2-S1 (SUGGESTION): index literal duplicated | **Resolved** | `DISC_LAST` at three sites; probes `t4`, `t5` |
| R461-1-S2 (SUGGESTION): restart store and NOADP value caught by directed phases only | **Restart half resolved**: `r7` / q4 / `s1` now fail the restart walk cell and arc 5. **NOADP-value half retained** as SUGGESTION, outside round 3's assignment: the walk still uses one valid_time | probes `s1` to `s4`, `t3` |
| R461-1-R1 (RESIDUE): README `:100` wording | **Resolved**, verbatim | `README.md:100-101` |
| R461-1-S1 (SUGGESTION): citation counts test a prefix only | **Retained** (open by assignment) | R460-1 `t3` gives the same result |
| R461-1-S3 (SUGGESTION): `make mutants` jobs | **Resolved** (round 2), still holds | `tb/adp_engine/Makefile:5`, `:25` |
| R460-2 R2-1 (RESIDUE): "and so arc 4's check" | **Resolved** | README `:157-158`, extended to the restart cell and accurate; PR body round 2 item 1 carries the exact fix |
| R460-2 S2-1 (SUGGESTION): name the index | **Resolved** | as R461-2-S1 |
| R460-1 F-1 (MINOR): fresh noted index graded nowhere | **Resolved** (round 2), still holds | `r6`, `arc-fresh-no-store` KILLED |
| R460-1 R-1 (RESIDUE): PR body `--jobs` wording | **Resolved** (round 2), still holds | PR body item 3 |
| R460-1 S-1, S-2 (SUGGESTION) | **Taken** (round 2), still hold | comment-only engine (`receipts/hdl-comment-only.txt`); `JOBS` in Makefile |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 04 F04.8 fresh and restart rows against `notes_index`, `noted_index`, `apply_disc`, `check_noted_index`; RTL branches `KL_adp_engine.sv:356-370` | R460-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| RTL | CLEAN | Round-3 diff (no `hdl/`); base vs. head engine with comments stripped; the two new patches against `:356-360` | R460-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| Robustness | CLEAN | Private copies for every unit; clone integrity; observation window under faults; re-walk isolation | R460-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| Tests | CLEAN | Suite 1348/1348; campaign 2 controls + 41/41 KILLED; counts vs. README; probes3 (12 probes + control); R460-1 `probes.py`, R461-2 E8 and E9, rerun unchanged | R460-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |
| Docs | CLEAN (S3-1 suggestion only) | README `:6`, `:100-101`, `:148-168`, `:264-311`; F04.7; PR body round 3 (sha256 in `receipts/evidence-read.txt`); `make check`, `gen_matrix --check` | R460-3 | 4811c21d8fe29faa1e9e713a6622bb206189e74b |

## Real limits

- Not run: full processor, parent, gPTP, Yosys or builder banks; `run_suites.sh`; lint. Not allowed in this review.
  - The PR body reports 33 suites rc 0 at this head.
  - The manager's statement says the source static/builder and native banks passed. In the pinned public evidence directory (`pp85-r1@4b05825f`) I found only round-1 author material, and no bank receipt for this head. Those results are taken as stated, not reproduced.
- I ran `make check` in a git-less extraction, where the `stale` gate cannot compare commit times. Round 3 touches no diagram source or export.
- Hosted runs at the exact head, as of 03:01Z (`receipts/hosted-check-runs.tsv`): `docs-gates` and `portability` succeeded in both contexts. `suites` was still `in_progress` in both contexts, so it is not evidence here.
- Physical calibration NOT RUN. No hardware. Field skips are not hardware proof.
- Issue item 4 (available_index interop) was adjudicated read-only, as the lane scope directed. A live-controller check remains out of scope.

## Pending manager duties

- Hosted `suites` at the exact head: the manager owns acceptance, along with hosted/act acceptance generally.
- Build and verify the final current-dev candidate at the merge turn: source base `5c71928a`, live dev `241f9184`.
- Residue checklist: no new RESIDUE from this round. R461-1-R1 and R2-1 are now resolved in-tree. Carry the retained suggestions (R461-1-S1, R461-1-S2's NOADP half, S3-1) as optional.
- Merge still requires two independent POSITIVE reviews at the exact head.

## Packet

- `scripts/`:
  - `probes3.py`: this round's probes.
  - `run_all.sh`: the driver.
  - `compare_counts.py`, `strip_compare.py`, `verify_clone.sh`, `redact.py`.
  - `prior/`: the four prior scripts, unchanged.
- `receipts/`: suite, campaign (with one log per arm), comparisons, probes, docs gates, clone integrity, simulator identity, hosted runs, evidence read, verdict draft.
- Host paths are replaced by labels (`<SCRATCH>`, `<PACKET>`, `<CLONE>`, `<SIM_ROOT>`, `<SIM_WRAPPER_DIR>`).
- Every published file is listed in `MANIFEST.sha256`.

R460-3 FINISHED
