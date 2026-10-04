[R461] POSITIVE - exact head a8669732b30436c641d51829950c204defd57a30

# R461-1 external independent review: processor issue #85 (GAP-16) / PR #152

- Exact head `a8669732b30436c641d51829950c204defd57a30`, tree `0bb0763a562807b53ecaed11a4109473139aa982` (verified in the review clone; see `receipts/clone-integrity.txt`).
- Source base `5c71928ad2bf1a854a5538d69b77214dfdf1697f`. Diff: 14 files, +389/-69, all under `docs/` and `tb/adp_engine/`. `hdl/`, `syn/` and `scripts/` are byte-identical to the base (`git diff --quiet base head -- hdl syn scripts`).
- Review start: PR #152 comment 5975140540.
- Verdict: **POSITIVE**. No open BLOCKER, MAJOR or MINOR finding. One RESIDUE (wording only) and three SUGGESTIONs.

## 1. What I reconstructed, in order

1. Repository conventions. The repository has no AGENTS.md or CONTRIBUTING.md at this head; I searched the whole tree. Author conventions come from `docs/README.md`: plain-text clause citations, Milan wins (Δn), single-source rules, and `make check` before commit.
2. Frozen scope:
   - the body of issue #85, with acceptance items 1 to 4;
   - the lane assignment in issue comment 5974306370. It limits scope to tests and the docs they cite, with no RTL change. It reframes item 4 as adjudication against the standard and the published B6/B7/B8 enumerations, read-only: "If only a live controller can settle it, state that and leave the limit restated. Do not STOP for it". It asks for "Closes #85" only if every item is met, and for #39 #40 #41 to be cited as "Relates to";
   - the TAKEN and REVIEW READY comments.
3. Authorities:
   - `docs/architecture/04_adp_engine.md`: F04.2, F04.3 and §5, plus the new F04.7 and F04.8;
   - `docs/00_MILAN_COMPLIANCE_REVIEW.md`: GAP-16 and REQ-ADP-011 to REQ-ADP-014;
   - `docs/architecture/09_verification.md`;
   - the engine `hdl/adp/KL_adp_engine.sv`, which is unchanged.
4. The diff and the six commits from `c291f89` to `a866973`.
5. Public evidence: `kebag-logic/milan-fpga@4b05825f:review-evidence/pp85-r1`. It holds only the author's HANDOFF, PR-BODY and the three adoption patches; the published PR-BODY is byte-identical to the live PR body. I also read the parent's published B6, B7 and B8 enumerations and the parent's `docs/reference/REGISTER_MAP.md` at dev `5fabb46e`.
6. Prior public review findings: issue #85 and PR #152 carry no review findings at this head, only two "INDEPENDENT REVIEW STARTED" notices (R460-1 and R461-1). There is nothing to resolve or retain. I read no other reviewer's report.

## 2. Executed evidence

All runs are at the exact head. They use the pinned simulator `Verilator 5.050 2026-07-01 rev v5.050` through `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`. The host default is 5.052 and was not used.

| # | What | Result | Receipt |
|---|---|---|---|
| E1 | `tb/adp_engine` `make run` on a pristine export of head | rc 0, **1330 checks: 1330 PASS**; P13 prints `F04.2 45 cells (N 12, I 20, S 6, C 7), F04.3 33 cells (N 13, I 15, S 2, C 3), 8 arcs` | `receipts/suite-head.log/.rc` |
| E2 | the same on the base `5c71928a` (control) | rc 0, 1328 PASS. The two new checks are the 45-of-45 and 33-of-33 citation counts | `receipts/suite-base.log/.rc` |
| E3 | the head's own campaign, `mutants.py --jobs 10`, run from a pristine export | **2 controls PASS** (`adp_engine run`, `pp_top adp-config`), **38 of 38 arms KILLED**, `40 checks: 40 PASS`, rc 0 | `receipts/campaign-full.log/.rc` |
| E4 | every arm's failure count compared with its README row | 38 of 38 agree; the two pp_top rows that state a newer count inline (9 and 7) match that count | `receipts/readme-count-compare.txt` |
| E5 | `make check` and `scripts/gen_matrix.py --check` on a local clone of head | both rc 0: lint 41 mermaid and 18 wavedrom blocks, 1120 links, 115 REQ rows, 17 GAP findings, 94 module rows with 0 untested, 28 parameters | `receipts/docs-gates.log/.rc` |
| E6 | 18 reviewer probes of my own: 13 RTL mutants and 5 perturbations of the expectation table, each in its own scratch export | **18 of 18 turned the suite red at the check I predicted** (one probe of mine was ineffective in its first form and was corrected; both logs are kept) | `probes/`, `receipts/probe-*.log`, `receipts/probes-summary.txt` |
| E7 | the README's B6/B7/B8 figures recomputed from the five published `adp-discover.jsonl` records | every figure reproduces (section 3.4) | `receipts/bench-index-recompute.txt` |
| E8 | hosted checks at exact head (read-only) | `docs-gates` and `portability` executed and succeeded on both push and pull_request. `suites` was **still in progress** at query time (01:05Z), so it is neither a pass nor a skip | `receipts/hosted-checks.txt` |
| E9 | clone integrity after all work | HEAD and tree as published, index tree = HEAD tree, porcelain status empty including ignored files, 512 tracked blobs hash-equal with modes equal. **No gitlinks and no `.gitmodules` at this head**, so there is no submodule gitlink to check | `receipts/clone-integrity.txt` |

All builds and probes ran under `scratch/` from `git archive` exports or a local clone. The review clone was never written. In `receipts/suite-*.log` the host install path of the pinned simulator is redacted to `<pinned-verilator-root>`; nothing else in any receipt was edited. The scripts are in `scripts/`: `env.sh`, `run_suite_at.sh`, `run_campaign.sh`, `run_probe.sh`, `run_docs_gates.sh` and `bench_index_recompute.sh`.

## 3. Lens findings and evidence

### 3.1 Conformance

- **F04.2 cells.** I compared each of the 45 C++ `ADV` cells (`tb/adp_engine/sim_main.cpp:198-259`) with F04.7 (`docs/architecture/04_adp_engine.md:168-215`) on next state, frame, timer action, the Milan clause and the IEEE clause. They agree cell by cell.
- **The seven re-cited cells.** The PR body names seven cells whose citation changed. Each one changed as described:
  - the two not-started timer cells now cite §5.6.1, and the not-started SHUTDOWN cell cites §5.6.1;
  - TMR_DELAY in DELAY's draw phase cites §5.6.3.5.9, as a stray;
  - ENTITY_DISCOVER of another entity cites §5.6.3.1 in DOWN and in both DELAY phases.
- **F04.3 arcs.** The 33 `DISC` cells (`sim_main.cpp:286-324`) and the 8-entry `F043_ARCS` list (`:327-336`) agree with F04.8 (`04_adp_engine.md:240-258`) on guard, action, Milan step and IEEE clause. The arcs and their cells:

  | Arc | Walked as |
  |---|---|
  | entry | BIND x unbound |
  | match | match x NOT |
  | mismatch | GM mismatch, index <= last, x NOT |
  | fresh | fresh x DISCOVERED |
  | restart | stale match x DISCOVERED |
  | stale foreign | stale GM mismatch x DISCOVERED |
  | departing | DEPARTING x DISCOVERED |
  | aged | TMR_NO_ADP x DISCOVERED |

  The fresh arc carries no GM guard, which matches §5.6.4.5.2 step 3 and the RTL (`KL_adp_engine.sv:356-360`).
- **The five cells #85 names.** The table encodes each as the issue requires:
  - DOWN x DISCOVER (eid 0, own), DOWN x GM_CHANGE and DOWN x SHUTDOWN are class I: state DOWN, 0 draws, 0 arms, no cancel allowed, no frame, index unchanged, no event;
  - DELAY x LINK_DOWN goes to DOWN with no frame. The cancel is required in the armed phase; in the draw phase there is no arm and the draw is discarded;
  - DELAY x SHUTDOWN goes to DOWN with an ENTITY_DEPARTING, byte-exact at the held index, and the index then reads 0. This is graded in both DELAY phases.
- **IEEE §6.2.2.x numbering.** The corrected citation for available_index (§6.2.2.9 to §6.2.2.15 in 00 and 04 §5) agrees with every other §6.2.2.x citation in the tree, which follow the 2021 ADPDU field order:

  | Clause | Field |
  |---|---|
  | §6.2.2.5 | valid_time |
  | §6.2.2.8 | entity_model_id |
  | §6.2.2.15 | available_index |
  | §6.2.2.16 | gptp_grandmaster_id |
  | §6.2.2.17 | gptp_domain_number |
  | §6.2.2.18 | current_configuration_index |
  | §6.2.2.20 | interface_index |

  The rule REQ-ADP-011 states ("0 at init; ++ after each ENTITY_AVAILABLE tx; 0 on DEPARTING/power-up") is unchanged and matches the engine (`KL_adp_engine.sv:710-720`, `:905`).
- **available_index adjudication.** I checked the README's argument (`tb/adp_engine/README.md:155-203`) against the recomputed evidence in 3.4 and the parent register map:
  - the former every-ADPDU rule differs from §6.2.2.15 only at ENTITY_DEPARTING;
  - no receiver reads a DEPARTING's index;
  - the only case where the rules differ is absent from all five records;
  - the parent's `REGISTER_MAP.md` at `5fabb46e` (the `0x644` note) does say "increments on EVERY transmitted ADPDU … departing … alike (controllers treat a repeated index as an incoherent entity; bump-on-change-only was silicon-diagnosed 2026-07-12)", as both the README and the PR's parent-visible list state.

  The limit is restated and narrowed rather than closed, as the lane assignment allows. "Closes #85" is consistent with that scope decision.
- **Privacy.** The diff and the PR body name no device. The bench peer is "the reference Milan peer". The only proper names are the two controller software packages already present at the base.

**Conformance: CLEAN.**

### 3.2 RTL

- The PR changes no RTL: `hdl/`, `syn/` and `scripts/` are identical to the base.
- I read the cells the walk grades against the RTL that implements them:
  - advertise SM, `KL_adp_engine.sv:584-669`;
  - send queue, `:672-700`;
  - index manager, `:708-720`;
  - discovery evaluation, `:337-380`;
  - NOADP and unbind handling, `:405-421`;
  - event emitter, `:1060-1075`.

  No cell's behaviour contradicts its clause, so the lane was right not to STOP.
- Each of the 8 `arc-*` patches and the 2 named `walk-*` patches is a minimal edit that breaks exactly the arc or cell its README row describes:

  | Patch | Edit | What it breaks |
  |---|---|---|
  | `arc-not-discovered-no-guard` | the guard becomes `1'b1` | the guard in TK_NOT_DISCOVERED |
  | `arc-restart-skips-guard` | the guard becomes `1'b1` | the guard in the restart pair |
  | `arc-restart-detector-off-by-one` | `>` becomes `>=` | the restart detector at its boundary |
  | the six other arc and walk patches | one line removed or one condition widened | the arc or cell their rows name |

- The engine banner (`KL_adp_engine.sv:33-42`) keeps its earlier wording, as the PR's Notes say. It already cites §6.2.2.15 and says the rule is subject to live-controller adjudication, which agrees with the restated limit. It is not a defect under a no-RTL scope.

**RTL: CLEAN** (nothing changed; the cited RTL lines were examined).

### 3.3 Tests

- **The walk is driven from an independent table.** Expectations come from constexpr tables. The frame model `model_frame` (`sim_main.cpp:57-80`) is built from F04.5 offsets, not from DUT code. My table perturbations show the walk grades against the table, not against the RTL:
  - `t-table-down-gm-answers`: the table says DOWN answers a GM_CHANGE, the RTL is untouched, and the walk goes red at `GM_CHANGE x DOWN`;
  - `t-table-delay-shutdown-silent` goes red at `SHUTDOWN x DELAY(timer armed)`;
  - `t-table-departing-silent` goes red at arc 7.
- **The walk ends with count checks:**
  - `CHECK(adv_cells == 45)` and `CHECK(disc_cells == 33)`;
  - `CHECK(arcs == 8)`. Dropping an arc (`t-arcs-drop-one`) turns it red;
  - the two new citation counts. Removing one Milan clause (`t-cite-drop-one`) turns the 45-of-45 count red.
- **The five cells are graded with teeth.** The author's arms and my probes show each observable in each cell is checked:
  - `walk-down-answers-discover`: 16 failures, all on DISCOVER x DOWN and DISCOVER x NOT STARTED (state, draw, arm, cancel);
  - `walk-down-answers-gm-change`: 8;
  - `walk-down-shutdown-departs`: 1;
  - `walk-delay-ignores-link-down`: 4, on both DELAY phases;
  - `walk-delay-shutdown-silent`: 4, frame and index in both DELAY phases;
  - `walk-departing-keeps-index`: fails the index check in `SHUTDOWN x WAITING` and in both DELAY phases.

  My probes cover what those arms do not:
  - `r-down-shutdown-cancels`, `r-down-gm-cancels` and `r-down-discover-cancels`: a timer touched in an inert DOWN cell is caught by "no cancel";
  - `r-delay-link-down-keeps-timer`: caught by "the running timer is stopped";
  - `r-delay-link-down-departs`: a DEPARTING on DELAY x LINK_DOWN is caught by "0 frames" and the index check in both phases;
  - `r-departing-carries-zero`: caught byte-exact in all three SHUTDOWN cells.
- **Each arc mutant fails its own arc's check.** The campaign counts a kill only when a `FAIL:` line starts with the arm's expected label (`mutants.py:157-161`). For the 8 `arc-*` arms that label is `P13 F04.3 arc <name>`. `cell_ok` is set only when that arc's own cell walk raises no failure (`sim_main.cpp:1606-1626`). In E3, each arc arm's failing lines include its own arc cell's grading line, not only a setup "reached" line. For example, `arc-bind-keeps-discovered` fails `BIND x unbound … ends in TK_NOT_DISCOVERED, got … discovered 1`. Each arm's kill is therefore attributable to its own arc. The counts are 46, 13, 14, 5, 10, 12, 4 and 4, as in the README and the PR body.
- **38 of 38 KILLED, with controls passing**, at `--jobs 10`. This reproduces the author's `--jobs 4` result with identical per-arm counts, so the verdict does not depend on the job count.
- Further probes on the arcs all went red: `r-guard-ignores-domain`, `r-noadp-expiry-keeps-state`, `r-departing-keeps-state`, `r-departing-no-cancel` and `r-stale-foreign-no-cancel`. Two arc actions are caught only by directed phases, not by the walk cell; see SUGGESTION S2.

**Tests: CLEAN.**

### 3.4 Robustness, including the evidence and the campaign harness

- **Bench figures.** I recomputed them from the published records (receipt E7).
  - Peer: 12817 → 42441 → 44513 → 44851 → 45061, at 6.000, 6.004, 5.992 and 5.983 s per increment. The README's "6.00, 6.00, 5.99 and 5.98" holds.
  - Processor: 13215 (B6), then 85 (B7, after a reload; the index fell), then 1865 and 2156 (B8), then 19 (B8, after a power cycle; the index fell). Within a boot the cadence is 6.988 s (B7 → B8) and 6.965 s (B8 → B8 resume). The README's "6.99 and 6.96 s" holds; the corrected 6.96 s in the last commit is right.
  - The "within a boot" reading of the B7 → B8 pair is an inference. It is consistent with the data: same model_id, and 1780 increments at the 7 s mean cadence.
  - All five records are dated 2026-10-01 to 2026-10-03 UTC, contain no ENTITY_DEPARTING, and carry entity_capabilities `0x0000C588`, the F04.6 value.
  - B6 belongs to parent issue #629: its published handoff names it.
- **Campaign harness.** Every arm runs in its own temporary copy, and the review clone was never written. Controls run first. Results are read in declared order, so the summary is the same at any `--jobs N`. `--jobs` is supported (`mutants.py:179`); see S3 for the Makefile.
- **Determinism.** The suite gives the same counts at head on repeated runs: author record, E1, and the E3 control.

**Robustness: CLEAN.**

### 3.5 Docs

- F04.7 and F04.8 are new anchored figures in their one host document. The README, 09 §3 and the C++ comments link to them rather than copying them.
- `make check` passes (E5).
- The README states 1330 checks, which matches E1.
- The mutation-record rows match E3.
- 00 and 04 §5 now cite §6.2.2.15.
- 09's MTXW paragraph cites F04.7 and F04.8.
- The PR body's evidence table and mutation record agree with my runs.
- One wording defect, recorded as RESIDUE R461-1-R1 below.

**Docs: CLEAN** (RESIDUE does not make a lens unclean).

## 4. Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R461-1-R1 | RESIDUE | Docs | `tb/adp_engine/README.md:100` | The sentence "The table above gives each cell's class and Milan clause; F04.7 adds its IEEE clause." The README table at `:88-98` shows a clause for the N cells and for WAITING x ENTITY_DISCOVER only. The other I, S and C cells show the class alone, for example ENTITY_DISCOVER x DOWN, which the code and F04.7 cite to §5.6.3.1, and TMR_DELAY x DELAY(draw), cited to §5.6.3.5.9. | Wording only. The clauses in the code and in F04.7 are right and complete, and no figure, test or clause claim changes. | Replace the sentence with: "The table above gives each cell's class and, for its N cells, the Milan clause; F04.7 gives every cell's Milan clause and adds its IEEE clause." | Read `README.md:100` against `:88-98` and F04.7. |
| R461-1-S1 | SUGGESTION | Tests, Docs | `tb/adp_engine/sim_main.cpp:1580-1598` | The 45-of-45 and 33-of-33 citation checks test only a string prefix (`5.` or `Table 5.`, and `6.2.`). They do not tie a cell's citation to its F04.7 or F04.8 row. I verified all 78 cells against the doc tables by hand. | None today. The doc and the tables could drift apart silently later. | Optional: generate one from the other, or add a docs-check that compares F04.7 and F04.8 with the C++ tables. | `t-cite-drop-one` shows the current count reacts to a missing clause, but not to a wrong one. |
| R461-1-S2 | SUGGESTION | Tests | `sim_main.cpp:1567`; P9e2 `:1033`; P9j `:1100` | Two F04.8 arc actions are caught by directed phases rather than by the walk cell. Probe `r-noadp-fixed-20s` (T-ADP-NOADP fixed at 20 s) fails only P9j, because the walk uses one valid_time (10, which is 20 s). Probe `r-restart-no-store` (the restart pair does not store the new index) fails only P9e2. | None for #85's acceptance: the suite turns red for both. The arc checks alone would not. | Optional: walk two valid_time values, and follow the restart cell with one probe AVAILABLE at the stored index. | `receipts/probe-r-noadp-fixed-20s.log`, `receipts/probe-r-restart-no-store.log` |
| R461-1-S3 | SUGGESTION | Tests, Robustness | `tb/adp_engine/Makefile:23-24` | `make mutants` always runs at the driver's default of 4 jobs. The PR body pairs `make … mutants` with `--jobs N`. The README documents that `make mutants` runs the default. | Convenience only. | Optional: add `MUTANT_JOBS ?= 4` and forward `--jobs $(MUTANT_JOBS)`. | Read the Makefile. |

No BLOCKER, MAJOR or MINOR finding is open.

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | F04.7 and F04.8 against the C++ `ADV`, `DISC` and `F043_ARCS` tables (78 cells, 8 arcs); 04 §5, 00 GAP-16 and REQ-ADP-011; the §6.2.2.x numbering across the tree; the interop adjudication against the B6/B7/B8 records and the parent register map; privacy sweep of the diff and PR body | R461-1 | a8669732b30436c641d51829950c204defd57a30 |
| RTL | CLEAN | `hdl/syn/scripts` unchanged from base; `KL_adp_engine.sv` advertise SM, send queue, index manager, discovery evaluation, NOADP and unbind handling, event emitter; the 10 named mutation patches against those lines | R461-1 | a8669732b30436c641d51829950c204defd57a30 |
| Robustness | CLEAN | `mutants.py` and `mutant_pool.py` isolation and kill rule; campaign at `--jobs 10` against the author's `--jobs 4` counts; bench figures recomputed from five published records; clone integrity | R461-1 | a8669732b30436c641d51829950c204defd57a30 |
| Tests | CLEAN | E1 (1330/1330), E2 (base 1328/1328), E3 (2 controls PASS, 38/38 KILLED), E4 (38/38 counts), E6 (18/18 reviewer probes red at the predicted check), the arc kill attribution per arm | R461-1 | a8669732b30436c641d51829950c204defd57a30 |
| Docs | CLEAN (1 RESIDUE) | 04 F04.7, F04.8 and §5; 00; 09 §3; `tb/adp_engine/README.md`; PR body against the published PR-BODY (byte-identical); `make check` and `gen_matrix --check` rc 0 | R461-1 | a8669732b30436c641d51829950c204defd57a30 |

## 6. Real limits

- **No copy of the standards.** I had no copy of Milan v1.2 or IEEE 1722.1-2021 in this session. I checked the clause numbers for internal consistency: the ADPDU field order, F04.7 and F04.8 against the tables, README, 00 and 09, and REQ-ADP-011 as transcribed before this lane. I did not check them against the printed text. In particular, I could not read verbatim the README's quotation of §6.2.2.15, or the sub-clause numbers §6.2.4.1.3, §6.2.4.2.2, §6.2.5.2.2, §6.2.7.2 and Figure 6-5.
- **No full banks.** By instruction I ran no full processor bank (`run_suites.sh`), no Yosys, no lint bank, no parent consumer set and no builder. The parent consumer set of 17, including gate 16's T30 failures attributed to parent #643, is the author's record in the published HANDOFF and PR body; I did not reproduce it. The public evidence directory contains author material only; I found no separate manager bank receipt there, or in the issue or PR comments.
- **Hosted `suites` not finished.** At 01:05Z hosted `suites` was still in progress at exact head. Only `docs-gates` and `portability` had executed.
- **No hardware.** Physical calibration was not run. The bench records are read-only enumerations, not hardware proof, and no live controller observed an ENTITY_DEPARTING. That is the restated open limit.

## 7. Pending manager duties

- Build and gate the final current-dev candidate at the merge turn, from source base `5c71928a` onto live dev `241f9184`.
- Own hosted and act acceptance, including the completion of hosted `suites` at the final head.
- Carry RESIDUE R461-1-R1 to the residue checklist.
- Confirm the parent consumer set, and that gate 16's T30 failures belong to #643 / PR #648.
- Merge requires the second independent positive review (R460-1).

R461-1 FINISHED
