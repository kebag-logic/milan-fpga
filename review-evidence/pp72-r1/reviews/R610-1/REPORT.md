[R610] POSITIVE - exact head 9540c34526c611a4f8ebac2e1b9dac890727e155

# R610-1 independent review: issue #72 / PR #173, requirement-to-test traceability

- Role: internal independent reviewer, cleared context, own detached clone.
- Exact head: `9540c34526c611a4f8ebac2e1b9dac890727e155`, tree `330588f2998f95d694c5901a8317aed7029fc98d`.
- Source base: main `2cbed0a987c1e68402658d69459ab7e5aa571adc` (4 commits: `a5bc371`, `ae9f0bb`, `8b35915`, `9540c34`).
- Governing scope: issue #72 body and acceptance; lane assignment 6100765289; author STOP 6100887655; lane-owner ruling 6101430201 (option 1: category-matched tracing, `REQ_TAG_LOG` executed evidence, static half in `make check`, executed half in the suites job).
- Review start: PR #173 comment 6104357418.
- Verdict: **POSITIVE**. There is no open BLOCKER, MAJOR or MINOR finding. One RESIDUE of its own (prose only) and two SUGGESTIONs are recorded below. The other reviewer's findings, read after this pass, are dispositioned in section 5a: one more RESIDUE retained, none at MINOR or above.

## 1. What was reconstructed, in order

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head (searched the whole tree). The author conventions come from `docs/README.md` (reading order, ID registries, single-source rules), and the gate list from `Makefile` and `docs/architecture/09_verification.md` section 7.
2. **Scope.**
   - Issue #72 body, acceptance 1 to 6.
   - The assignment's scope and proof bullets: five planted defects, records identical at base and head, tags sampled REQ → file:line → check name.
   - The STOP (RND and STORM suites exist at base).
   - The ruling: option 1 and the stated design. AEM-025 waived against GAP-06 and MAAP-001 against GAP-04. "Correct the stale DOES NOT EXIST wording where the tree's own docs carry it."
3. **Authorities.**
   - 00 section 6, the compliance matrix: 115 REQ rows and the Ver vocabulary.
   - 00 F00.2, the GAP dispositions.
   - 09 section 3, the category definitions F09.3: DIR, MTXW, TOL, TIM, RND, STORM, NVM.
   - 09 sections 7 and 8.4.
   - The suite sources the tags label.
4. **Diff and history.** `git diff 2cbed0a9..9540c345` (25 files, +1149 −125) and the four commit messages.
5. **Public executable evidence.**
   - `kebag-logic/milan-fpga@c47339e8 review-evidence/pp72-r1`: `MANIFEST.json`, `author/HANDOFF.md` and `author/PR-BODY.md`. The downloaded sha256 values match the manifest's `published_sha256`.
   - The PR body and the REVIEW READY comment 6104271127.
   - No manager evidence comment exists on #72 or #173 at review time.
   - Per the assignment, no manager source bank runs at this head, and none is claimed or inferred here.
6. **Other public review findings on PR #173.** When this pass started, the PR had no review objects and no findings, only the review-start comment. While it ran, the external reviewer's R611-1 report was posted (comment 6104770398, POSITIVE at the same head). It was read only after this report's verdict, findings and ledger were written. Each of its findings is resolved or retained in section 5a.

## 2. Executed evidence

All runs used Verilator 5.050 (`verilator --version` → `Verilator 5.050 2026-07-01 rev v5.050`, the version CI pins) from the scoped wrapper, first on `PATH`. Each run had its own scratch clone and its own log and rc file. Receipts are under `receipts/`; scripts are under `scripts/`.

| # | Run | Result | Receipt |
|---|---|---|---|
| E1 | `./scripts/run_suites.sh` at base | rc 0; 34 suites PASS, `suites: 1029620 checks total, 0 failing` | `receipts/sweep-base/` |
| E2 | `./scripts/run_suites.sh` at head, `REQ_TAG_LOG` unset | rc 0; output **byte-identical** to E1 (sha256 `b1205c5d…36f5`); no file left behind in the tree | `receipts/sweep-head/` |
| E3 | `REQ_TAG_LOG=<file> ./scripts/run_suites.sh` at head (the CI form), then `check-req-tags.py --suites --evidence` on that same run | run_suites rc 0, output **byte-identical** to E1; executed half rc 0: `req-tags executed: 225 evidence lines, 13 suites, OK`. The file holds 230 lines, 225 distinct (5 pp_top tags run in two builds of the same suite) | `receipts/sweep-headlog/` |
| E4 | Per-suite `make` logs kept for all 13 tagged suites, base vs head (variable unset) | all rc 0/0. After masking only the tree path, Verilator's walltime line and unittest's duration, **0 differing lines** in every suite (pp_top 313 lines, srp_top 6859 lines, …) | `receipts/persuite-*`, `receipts/persuite-normdiff.txt` |
| E5 | `make check` at base and head | rc 0/0. Head adds exactly the two `reqtags` lines after `matrix`, and `ids: 563 files` → `565 files`. Nothing else differs | `receipts/{base,head}-make-check.txt` |
| E6 | `check-matrix.py`, `gen_matrix.py --check`, `lint_hdl.sh` at base and head | each rc 0/0 and **byte-identical** | `receipts/{basestatic,head}-*.txt` |
| E7 | `make reqtags` at head | `req-tags selftest: 29 cases, OK`; `115 REQ rows: 101 traced, 8 waived, 6 need no check; 225 tags in 18 files, OK` | `receipts/head-make-reqtags.txt` |
| E8 | 16 static planted faults, one at a time, in a disposable head clone | each fails by name, or passes where designed (section 4); the clone restored to head | `receipts/static-probes/` |
| E9 | Executed planted fault: tb/srp_encoder's tagged E1 check and its tag wrapped in a never-taken branch | static half rc 0 (as designed); srp_encoder still PASS (580 checks, was 581); executed half rc 1: `DEAD TAG REQ-SRP-003 tb/srp_encoder/sim_main.cpp:496`. The unplanted control gives rc 0 | `receipts/executed-probe/` |
| E10 | Mutation campaigns at head that build a changed file: maap, srp_top, adp_engine, aecp-dispatch (the four of these that CI runs), gsi, desc_store lint-suppression | all rc 0: maap 32 of 32, srp_top 137 PASS (assertion coverage 86/86), adp_engine 62, aecp_dispatch 44, gsi 20 detected (golden and restored PASS), lint-suppression 56 of 56 killed with the control passing | `receipts/campaigns-head/` |
| E11 | Hosted CI at the exact head, read only | docs-gates **success** in both the push run (38102577653) and the pull_request run (38102579661). In both suites jobs, step 5 "Lint + every suite" and step 6 "Every REQ tag ran, in a suite that passed" completed **success**. The later campaign steps were still in progress when observed | `receipts/hosted-snapshot.txt` |

`syn/yosys/run.sh` was not run. The diff touches no file under `hdl/` or `syn/` (`git diff --stat 2cbed0a9..9540c34 -- hdl syn` is empty), so the elaboration inputs are byte-identical at base and head.

## 3. Lenses

### 3.1 Conformance (CLEAN)

- **Scope bullets.**
  - Tags sit in the test sources, next to the check, in one parsed format. There is no hand-kept list.
  - The gate fails by name on each of the following, each probed in section 4 and E9:
    - an uncovered row;
    - an unknown REQ;
    - a tag that did not execute: the executed half, on the suites job's own `run_suites.sh` run made with `REQ_TAG_LOG`, as the ruling designs it;
    - a waiver without a GAP or without a reason.
  - It runs in CI: the static half in `make check` (`reqtags`, right after `matrix`, `Makefile:16`); the executed half as its own step of the suites job (`.github/workflows/hdl.yml:58-70`, `set -o pipefail` added at `:62` so the `tee` cannot mask a failing sweep).
- **Ruling 1, category-matched tracing.**
  - `row_states` (`scripts/check-req-tags.py:246-265`) traces a row only by a tag whose category equals the row's Ver. Probe x1 (REQ-AEM-005 retagged DIR) gives `UNCOVERED REQ-AEM-005 (RND)`.
  - A waiver must name one of the row's own Finding GAPs. Probe x3 gives `WAIVER NAMES ANOTHER ROW'S GAP`.
  - AEM-025 → GAP-06 and MAAP-001 → GAP-04, as ruled. NOT-001, NOT-003, AEM-016, NOT-002 and AEM-005 are traced to the checks the STOP listed: `notify_phases.hpp:1146` ST1b; `:1211`, `:1216` ST2/ST2b; `:1356` CS; `:1635`, `:1636` RN; `tb/originator/sim_main.cpp:882` R.
- **Ruling 2, executed evidence.**
  - With the variable unset or empty, `REQ_TAG` returns before any I/O (`tb/common/req_tag.hpp:42-44`; `tb/common/req_tag.py:31-33`).
  - Byte identity holds: E2, E3 and E4.
  - The gate requires each tag's suite to PASS in the same run and the tag's line in the evidence: E3 and E9.
- **Ruling 3, the CI split.** As above. Hosted step 6 succeeded at the exact head (E11).
- **Ruling 4, records.**
  - Every Cov cell ends with the row's state. `receipts/cov-diff.txt` shows every Cov change is the suffix alone, with no C/P/A/I grade changed and no Ver changed. The only other matrix cells changed are REQ-VER-001's Arch and Doc.
  - 09 section 8.10 carries the coverage table and the 8 waivers; the gate holds both (probes x4, x11).
  - Stale "DOES NOT EXIST" wording: a case-insensitive search of `docs/`, `scripts/` and the suite READMEs finds no such claim about RND or STORM suites at head, so there was nothing to correct. 09 section 8.10 states which RND/STORM rows the section 8.4 suites trace.
- **Coverage figures** match the gate's own output (E7): 101 traced (RND AEM-005, AEM-016, NOT-002; STORM NOT-001, NOT-003), 8 waived (AEM-019 GAP-05, AEM-025 GAP-06, MAAP-001 GAP-04, MVU-003/004 GAP-03, NET-004 GAP-05, NET-005 GAP-04, SCP-001 GAP-12), 6 needing no check.
- **Waiver reasons checked against the tree.**
  - AEM-025 "RN c" stays under 30 s: `notify_phases.hpp:1645`.
  - AEM-019 and NET-004: K9 to K16 grade a bench store that plays the integrator (`counters_phases.hpp:1-28`).
  - NET-005: W23a2 exists (`sim_main.cpp:6727`).
  - MVU-003/004: M4 grades only the NOT_IMPLEMENTED answer (`sim_main.cpp:3030-3037`).
  - MAAP-001: `tb/prng` E grades the kind-7 draw's bounds and spread, a single-draw model and not a multi-controller session, so the RND waiver is consistent with F09.3's definition.
  - SCP-001: M2 features_flags carries the SCP-002 tag.
- **"Relates" rather than "Closes" (acceptance 1).**
  - Acceptance 1 asks for every row with a dynamic Ver to be linked to at least one check tag. Six waived DIR rows (AEM-019, NET-004, NET-005, MVU-003, MVU-004, SCP-001) carry no tag at all, so acceptance 1 is not literally met. AEM-025 and MAAP-001 do carry tags, of other categories.
  - The assignment and the ruling make a GAP-and-reason waiver the designed outcome for a row with no check of its category. "Relates" is therefore the accurate, conservative keyword. It does not overclaim closure, and it matches acceptance 1 as frozen.
  - Acceptance 2 is met in spirit: with in-source tags there is no separate map to go stale. A removed sole tag gives UNCOVERED, a tag that does not run gives DEAD TAG, and an evidence line with no tag gives STRAY. The gate runs beside check-matrix.py in `make check` and CI.
  - Acceptance 3 is replaced by the ruling, and met.
  - Acceptance 4 is met: the 09 section 8 "To add" line no longer lists REQ-ID coverage (`09_verification.md:533-535`).
  - Acceptance 5 and 6 duplicate 2.
  - Whether the waivers close #72 is a lane-owner decision (section 8).

### 3.2 RTL (CLEAN)

- No file under `hdl/` or `syn/` changes. No port, parameter, register map or generated ROM changes.
- `scripts/lint_hdl.sh` is rc 0 and byte-identical at base and head (E6).
- Every suite's output and check count are identical (E2, E4). So the DUT's observable behaviour under every existing check is unchanged.
- No RTL change means no elaboration or synthesis delta. Yosys was not run (see section 2).

### 3.3 Robustness (CLEAN)

- **Gate failure modes.** All 16 static probes fail with the documented name, or pass where designed (section 4). The executed half names a dead tag (E9).
- **Executed-half inputs.** A suite missing from the PASS lines gives `SUITE NOT PASSED`, and a run without the `0 failing` total gives `SUITES RUN INCOMPLETE` (self-test case 18). Stray and malformed evidence are cases 19 and 20. An absent evidence file is read as empty (`check-req-tags.py:352-354`), so every tag is DEAD.
- **Malformed matrix rows.** A short row and an empty Ver both pass `check-matrix.py`, but `check-req-tags.py` fails them as `UNKNOWN VER` (probes x6, x7). The new gate is stricter than the existing one, never looser.
- **Comment-out and untracked-file evasion.** A commented-out tag is `MALFORMED TAG` and its row is UNCOVERED (x8). A tag in an untracked, non-ignored file is still read (x10).
- **Suite attribution and copied trees.**
  - The C++ tag takes the suite from `getcwd()` and the Python tag from `Path.cwd().name`. A suite whose run left `tb/<suite>` would fail loudly (STRAY plus DEAD), not pass silently. At head every evidence line attributes correctly (E3).
  - All 15 tree-copying drivers copy `tb/common` beside the suites they build (14 mutation drivers and the nvm_port figures script, each checked), so the relative `#include "../common/req_tag.hpp"` and the by-path Python loader resolve in their scratch copies.
  - The one driver that rewrites a tb source (`acmp_talker/retry_mutants.py:341-346`) anchors on the CHECK macro body, which the tags do not touch.
- **CI.** `set -o pipefail` keeps `run_suites.sh | tee` failing on a red sweep. The executed-half step runs only after it succeeds. `REQ_TAG_LOG` is set on that one command, so the later campaign steps run with the tags inert.
- **Weakness, not a defect.** The C++ name check is a substring match over up to 8 lines (S-01).

### 3.4 Tests (CLEAN)

- **Self-test.** 29 cases, OK (E7). Cases 2 to 6 are the assignment's five planted defects; the rest cover the gate's other findings, both halves.
- **Planted defects re-run independently in the real tree.**
  - p1 tag removed: `UNCOVERED REQ-AEM-005 (RND)`.
  - p2 unknown REQ: `UNKNOWN REQ REQ-ADP-099 tb/adp_engine/sim_main.cpp:706`.
  - Executed dead tag: `DEAD TAG REQ-SRP-003 …:496`, with the static half passing.
  - p4 waiver without GAP: `WAIVER WITHOUT GAP REQ-AEM-025`.
  - p5 row added: `UNCOVERED REQ-AEM-027 (DIR)`.
- **Tag sampling.**
  - All 225 tag and check pairs were read in `receipts/tag-context.txt`: the tag, the line above it, and the statement it labels.
  - Every traced row's own-category tag stands directly above a check of that F09.3 category:
    - STORM ST1b is the fan-out to the full registry;
    - STORM ST2, ST2b and CS are counter churn at the rate limit;
    - RND RN is 20 controllers against a registry model;
    - RND R is 16 owners against an inflight model;
    - NVM D3R1, D3N, D3C, D3K, D3V and BW2 are restore and volatility across a cut;
    - MTXW covers the listener 112-cell walk, the ADP 45 and 33 cells, the SRP Δ13 cells and the MAAP Table B.7 scenarios;
    - TOL covers ACMP 56-B/96-B, MRPDU prefix handling and the NOT_IMPLEMENTED echo;
    - TIM covers compressed timers and T-BUDGET.
  - Off-category tags (AEM-003 L7 DIR, AEM-011 D3N1 NVM, AEM-017 U2 TOL, AEM-025 ×3, AEM-026 A6 DIR, NOT-001 U8c DIR, NOT-002 NP DIR, MAAP-001 U1/U17 DIR) label their checks and trace nothing, as the ruling requires.
  - Loops and guards: `adp_engine/sim_main.cpp:997` (`if (a >= 0) CHECK`, preceded by `CHECK(a >= 0)`), `d3_phases.hpp:3275` (`named` used as `named[0]` and `named[1]` right after), and the Python `for mutation in mut.MUTATIONS` (non-empty, held by `test_every_check_has_a_mutation`). In each case the tag running implies the check runs.
- **No check changed.** Every non-tag line the diff adds under `tb/` is an `#include` or the Python loader. The diff deletes no line under `tb/` (`receipts/tb-diff-nontag-lines.txt`).
- **Records identical.** E2, E3, E4, E5 and E6. Campaigns pass at head (E10).

### 3.5 Docs (CLEAN, one RESIDUE)

- **00 section 6.**
  - The Cov key states the three states.
  - Every cell carries its state, which the gate checks.
  - The GAP-11 landed note and F00.2 GAP-11 "Verified by" name the gate and both halves.
  - REQ-VER-001's Arch and Doc point at the tags and at 09 section 8.10.
- **09.**
  - Section 2 points at section 8.10, and section 7 lists `reqtags` with what it fails.
  - Section 8.10 states the tag format, the two halves, the executed half by hand, the RND/STORM disposition, the coverage table and the eight waivers.
  - The section 8 "To add" line keeps only the single-source scan.
  - Each 8.10 claim checked against the tree (section 3.1) holds, including the text 9540c34 added: build-tool lines differ run to run (E4), and `tb/prng` E grades the kind-7 draw.
- **Links.** `make check` `links: 1187 checked, OK` (E5).
- **One prose list was left stale.** See RES-01. A second prose undercount, `09_verification.md:143`, is retained from the other review (section 5a).

## 4. Planted-fault receipts (static half, real tree, one at a time)

| Probe | Plant | Gate output (rc) |
|---|---|---|
| p1 | delete REQ-AEM-005's RND tag | `UNCOVERED REQ-AEM-005 (RND)` (1) |
| p2 | REQ-ADP-006 tag → REQ-ADP-099 | `UNKNOWN REQ REQ-ADP-099 tb/adp_engine/sim_main.cpp:706` and `UNCOVERED REQ-ADP-006 (DIR)` (1) |
| p4 | blank AEM-025's waiver GAP | `WAIVER WITHOUT GAP REQ-AEM-025` (1) |
| p5 | add row REQ-AEM-027 (DIR) | `UNCOVERED REQ-AEM-027 (DIR)` (1); check-matrix OK |
| x1 | AEM-005 tag category RND → DIR | `UNCOVERED REQ-AEM-005 (RND)` (1) |
| x2 | tag name not in its check | `NAME NOT AT CHECK …:706` (1) |
| x3 | AEM-025 waiver names GAP-04 | `WAIVER NAMES ANOTHER ROW'S GAP` and `COV RECORD` (1) |
| x4 | AEM-005 Cov says waived | `COV RECORD REQ-AEM-005` (1) |
| x5 | waiver on traced AEM-005 | `STALE WAIVER REQ-AEM-005` (1) |
| x6, x7 | short row / empty Ver | `UNKNOWN VER REQ-AEM-027` (1); check-matrix passes both |
| x8 | comment out a tag | `MALFORMED TAG` and `UNCOVERED` (1) |
| x9 | shorten a tag name to "U1" | passes (0): see S-01 |
| x10 | tag in an untracked file | `UNKNOWN REQ REQ-ZZZ-001 …extra.cpp:1` (1) |
| x11 | drop AEM-005 from the 8.10 table | `COVERAGE RECORD traced RND` (1) |
| x12 | waiver GAP cell `GAP-06, GAP-06` | `WAIVER NAMES ANOTHER ROW'S GAP` (1) |

## 5. Findings

### R610-1-RES-01: RESIDUE (Docs)

- **Where:** `docs/guides/hdl-engineer.md:255`, the section 8 "The gates" table.
- **Defect:** the `make check` cell lists every gate `make check` runs (lint, WaveDrom, links, matrix, module matrix, parameters, IDs, figures, staleness) but omits the new `reqtags` gate. The `./scripts/run_suites.sh` row does not say that the CI suites job runs it with `REQ_TAG_LOG` and then the executed half.
- **Authority:** `Makefile:16` (`check: … matrix reqtags …`), `09_verification.md` sections 7 and 8.10. The author's published handoff names this list as deliberately left out of the lane.
- **Impact:** prose only. The cell links to 09 section 7, which is correct. No measurement, figure, verdict, test, code, generated artifact or conformance claim changes.
- **Exact fix:** in that cell, after "compliance-matrix consistency,", insert:

  > the requirement tags in `tb/` against the matrix rows (`reqtags`, [09 §8.10](../architecture/09_verification.md#810-requirement-tags-and-the-traceability-gate-issue-72)),

  Optionally, in the `run_suites.sh` row, append:

  > ; CI runs it with `REQ_TAG_LOG` set and then `scripts/check-req-tags.py --suites … --evidence …`

- **Verification:** `make links` stays OK, and the cell names `reqtags`.

### R610-1-S-01: SUGGESTION (Robustness, Tests)

- **Where:** `scripts/check-req-tags.py:198-213` (`name_at_check`, `CHECK_LINES = 8`).
- **Observation:** for C++ the tag name only has to appear as a substring somewhere in the next statement. The statement is read up to the first line ending in `;`, so a trailing `// comment` extends the window into later statements. Probe x9 shows a shortened name, `"U1"` over `"U1: PROBE byte-exact"`, passing. The same name would also pass over a `"U17: …"` check.
- **Status:** not a defect. The documented rule is "the name must appear in the check statement", and the mapping is reviewer-sampled (done here, all 225 tags).
- **Possible hardening:** match within the first statement only, with comments stripped, and require the name to be a prefix of one of its string literals.

### R610-1-S-02: SUGGESTION (Tests)

- **Where:** `tb/common/req_tag.hpp`, `scripts/check-req-tags.py` executed half.
- **Observation:** the evidence line proves the tag statement ran, not that the labelled check ran. This is the ruling's design. All instances sampled where the check sits in a loop or guard are safe (section 3.4).
- **Possible hardening:** a future refinement could record from inside the check macro itself.

## 5a. Public findings by the other reviewer (R611-1), read after this pass

| R611-1 finding | Disposition at this head | Basis |
|---|---|---|
| R1 RESIDUE: hdl-engineer guide's gate list omits `reqtags` (`docs/guides/hdl-engineer.md:255`, `:258`) | **Retained**; the same defect as R610-1-RES-01 (one residue item, either wording fix) | found independently in section 3.5 |
| R2 RESIDUE: "Two suites are MTXW walks" (`docs/architecture/09_verification.md:143-145`) undercounts against the gated 8.10 record, which traces REQ-SRP-005, REQ-MAAP-003 and REQ-MAAP-005 by MTXW tags in `tb/srp_stream_fsms` and `tb/maap` | **Retained as RESIDUE** (missed in this pass, confirmed now). The sentence is unchanged from base (base line 143) and stays true of the two cell-count walkers. The new record makes it read as exhaustive. Prose only: no gate, figure or test changes. R611-1's exact fix is adequate | `09_verification.md:143`; `receipts/reqtags-table.txt` MTXW rows; F09.3 lists the SRP FSMs and the MAAP Table B.7 matrix as MTXW |
| S1 SUGGESTION: check-name binding is a substring test | **Retained as SUGGESTION**; the same as R610-1-S-01 (probe x9 here) | section 4 x9 |
| S2 SUGGESTION: evidence freshness is trusted; the suite comes from the working directory (`tb/name_state` compiles `tb/pp_top/sim_main.cpp` and runs it from a temporary directory) | **Retained as SUGGESTION**. Both cases fail closed or are safe in CI: `$RUNNER_TEMP` is fresh, the 8.10 recipe begins `rm -f`, and a tag reached from a temporary directory would be `STRAY EVIDENCE`. No such line exists in this review's E3 evidence: its 13 suite names are all `tb/` suites | `tb/name_state/run.py:84,115`; `receipts/sweep-headlog/req-tags.txt` |
| S3 SUGGESTION: REQ-VER-001 keeps Ver `—` while F00.2 GAP-11 says "lint" | **Retained as SUGGESTION**, not a defect. F00.2's "Verified by" does not mirror the rows' Ver elsewhere either (GAP-10 "DIR" against REU rows with `—`). Both values give "no check" | this pass, before reading R611-1 |

None of these changes the verdict. RES-01 and R2 go to the residue checklist.

## 6. Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #72 body and acceptance 1-6; comments 6100765289, 6100887655, 6101430201, 6104271127; PR #173 body; 00 §6 and F00.2; 09 §3, §7, §8.4, §8.10; `receipts/cov-diff.txt`; waiver reasons against `notify_phases.hpp`, `counters_phases.hpp`, `sim_main.cpp`, `tb/prng` | R610-1 | `9540c34526c611a4f8ebac2e1b9dac890727e155` |
| RTL | CLEAN | `git diff --stat -- hdl syn` (empty); `lint_hdl.sh` base/head byte-identical; E2/E4 identical suite output | R610-1 | `9540c34526c611a4f8ebac2e1b9dac890727e155` |
| Robustness | CLEAN (S-01 open as suggestion) | `scripts/check-req-tags.py` (all 560 lines); `tb/common/req_tag.{hpp,py}`; `.github/workflows/hdl.yml`; `Makefile`; 16 static probes; executed dead-tag probe; 15 tree-copying drivers' copy lists; `retry_mutants.py` source patch | R610-1 | `9540c34526c611a4f8ebac2e1b9dac890727e155` |
| Tests | CLEAN (S-02 open as suggestion) | 29-case self-test; E1-E4 sweeps and per-suite logs; executed half 225/13; 225 tag contexts (`receipts/tag-context.txt`); `receipts/reqtags-table.txt`; campaigns maap, srp_top, adp_engine, aecp_dispatch, gsi, lint-suppression | R610-1 | `9540c34526c611a4f8ebac2e1b9dac890727e155` |
| Docs | CLEAN (RES-01 and retained R611-1-R2 to residue checklist) | 00 §6 Cov key and cells, GAP-11 note, F00.2; 09 §2/§7/§8.10/§8 tail; `docs/README.md`; `README.md`; `docs/guides/*.md`; `make check` links | R610-1 | `9540c34526c611a4f8ebac2e1b9dac890727e155` |

The review clone was never modified. Every probe ran in disposable clones under the packet's scratch directory. The clone was checked at the end (`receipts/restore-verify.txt`):

- HEAD `9540c345…`, tree and `git write-tree` both `330588f2…`;
- worktree equals HEAD, and `git status --porcelain --ignored` is empty;
- the index's modes and blobs equal the HEAD tree's;
- 0 gitlinks: this repository has no submodules at this head.

## 7. Real limits

- **Campaigns.**
  - Run at head only, not at base. The claim that base and head give the same verdict per arm is supported by identical suite output (E2, E4), not by base campaign runs.
  - Not re-run: AECP deadline/hazard (`aecp-mutants`, run by CI), notify, d3, acmp, ctr, name_wr, name_state, srp_admission, acmp_talker retry, desc_mem_guard. The nvm_port figures campaign builds no changed file.
- **Executed probe (E9).** It runs srp_encoder for real. Its evidence and tally are spliced into the full head sweep's evidence and output; every other suite's lines are unchanged. It is not a second full sweep of a planted tree. The self-test covers the same DEAD TAG path on a synthetic tree.
- **Per-suite logs (E4).** These are incremental `make` runs over the sweep builds: the compile steps were up to date and every simulation ran in full. The 21 untagged suites' sources are unchanged, so their logs were not compared separately.
- **Not run.**
  - `syn/yosys/run.sh`: no input changes.
  - No parent or consumer gate.
  - No hardware: physical calibration NOT RUN. Field skips are not hardware proof.
- **Host and redaction.** The host was shared and heavily loaded. The two srp_encoder build logs in `receipts/executed-probe/` had a local simulator install path redacted.
- **Hosted CI (E11).** Read once while the suites jobs were still in their campaign steps. Their final conclusion is not recorded here.

## 8. Pending manager duties

- Validate the current-dev merge candidate (source base `2cbed0a9`, live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`): builder and native banks at the merge turn, with receipts linked on the PR.
- Own hosted and act acceptance, including the remaining steps of the exact-head suites jobs (runs 38102577653 and 38102579661).
- Lane owner: rule whether the eight GAP-and-reason waivers satisfy acceptance 1, so that #72 closes after merge, or name what keeps it open. The PR says "Relates to #72".
- Carry RES-01 (= R611-1-R1) and R611-1-R2 to the residue checklist.
- Confirm whether parent adoption is needed. Only `tb/`, `scripts/`, `docs/`, `Makefile` and CI change. The author reports the parent's processor-reading gates at the same rc at base and head; this review did not verify that.

R610-1 FINISHED
