[R739] NEGATIVE - exact head 8607347675743fe8d1ccaa370c63905c5ca1ccd5

# Independent review R739-1: Mister-M-alt/FPGA-gPTP PR #97 (issue #96)

- Head `8607347675743fe8d1ccaa370c63905c5ca1ccd5`, tree `7791e003a4c235379f7dcdb2efc215b22c85c105`.
- Base main `135afd043309369a87ddbc8d6550aff8ec52a157`.
- Scope: the whole PR. That is 11 Markdown files plus `scripts/check_docs.py`, part of parent kebag-logic/milan-fpga#797.
- Order of work: the independent pass came first, then this verdict and ledger were written to disk. Only after that were prior public review findings and manager comments read; see "Prior public findings" at the end.

## Verdict basis

There is one factual clause error on a page marked Current, added by this PR (F1). Issue #96's acceptance item "no document marked current contradicts the code or a clause" is therefore not met.

One evidence pointer that the PR moved into the archive now names the wrong artifact (F2).

Everything else checked holds at the head:
- the ROM budget and generator-command corrections;
- the 2011 clause renumbering, consistent with the source;
- the constants and status tables;
- the new freshness gate, against planted defects;
- the delta scope (no RTL, generator, generated-file or test change);
- the start-here path and glossary anchors;
- privacy.

## Findings

### F1 - MINOR - Conformance, Docs

- **Where:** `docs/GLOSSARY.md:19`, row `| Follow_Up companion | Two-step message carrying the precise transmit time | 11.4.3 |`.
- **Authority:** IEEE 802.1AS-2011 numbers the message-format clauses this way: 11.4.3 is the Sync message, 11.4.4 the Follow_Up message (preciseOriginTimestamp 11.4.4.2.1, information TLV 11.4.4.3), and 11.4.7 the Pdelay_Resp_Follow_Up message.
- **Evidence in this tree at the head:** the repository's own sources use that numbering.
  - `hdl/wire/KL_gptp_rx_parser.sv:30-31` and `:172-175` cite 11.4.4.3 and 11.4.4.2.2 for the Follow_Up TLV.
  - `hdl/ucode/gen_gptp_ucode.py:224` and `:955` cite 11.4.4 for Sync/Follow_Up pairing.
  - `tb/verilator/engine/sim_main.cpp:124` says "Sync/Follow_Up pairing ... (11.4.4)" and `:1851` cites 11.4.5 for Pdelay_Req.
  - The independent decoder's 802.1AS-2011 protocol descriptions, which `tb/tsngen` loads, head the Sync file "11.4.3: Sync message", the Follow_Up file "11.4.4: Follow_Up message" and the Pdelay_Resp_Follow_Up file "11.4.7".
  - No other current page or source file cites 11.4.3 for Follow_Up.
- **Impact:** a new Current page sends readers to the Sync message clause for the Follow_Up definition. That contradicts a clause, which is acceptance item 2 of #96. The author's published clause-verification list (`review-evidence/gptp96-r1/author/HANDOFF.md`, "Verification method") does not include 11.4.3, so this row was not covered by that check.
- **Required outcome:** cite 11.4.4 for the Follow_Up companion of Sync and 11.4.7 for Pdelay_Resp_Follow_Up. The row then reads `| Follow_Up companion | Two-step message carrying the precise transmit time | 11.4.4, 11.4.7 |`.
- **Verification:** `grep -n 'Follow_Up companion' docs/GLOSSARY.md` shows `11.4.4, 11.4.7`. `make docs` still exits 0.

### F2 - MINOR - Docs

- **Where:** `docs/history/v1/RESOURCE_DELTAS_2026_10.md:31`, "The parent commit [`4999d8d6`](https://github.com/kebag-logic/milan-fpga/commit/4999d8d6344e373e0204995cb36c93cf616e8f9e) records the reports."
- **Evidence:** at base, `docs/MANAGER.md` linked the measurement reports by tree path at that commit (`/tree/4999d8d6.../review-evidence/gptp75-r1/author`). The PR swapped that for a commit link. That parent commit's change set has 97 files, all review-archive receipts for another round. None is a measurement report: 0 files under `/author/`, per `receipts/parent_4999d8d6.txt`. The reports (`baseline-engine_util.rpt`, `candidate-engine_timing.rpt` and the rest) exist only in the tree at that commit, under a path the page no longer gives.
- **Rule:** the history index's own reading rule says "Preserve commit references for reproducibility" (`docs/history/v1/README.md:12`).
- **Impact:** the archived PR #76 figures lose their reproducible evidence pointer. A reader who follows the link sees an unrelated review archive. This is a factual misstatement about an artifact, not just wording. Restoring a precise pointer also touches the label rule, because the original path contains a round label, so it is not RESIDUE.
- **Required outcome:** point at the reports themselves. Either:
  - restore the tree link to the author report directory at `4999d8d6`. The link target carries the path, and the visible text needs no label; or
  - name a commit or tree whose landing view shows the reports.

  Then state it accurately, for example "The parent tree at `4999d8d6` holds the measurement reports."
- **Verification:** opening the link shows the `.rpt` files. `make docs` exits 0.

### RESIDUE (wording only; does not change the verdict)

- **RES-1:** `docs/INTEGRATION.md:12`. "PHC outputs are one-cycle step and rate pulses." It leaves out the PHC-face level `phc_slew_active_o` (`hdl/top/KL_gptp_engine.sv:123`). Exact fix: "PHC step and rate writes are one-cycle pulses; `phc_slew_active_o` is a level."
- **RES-2:** `docs/INTEGRATION.md:11`. "`tx_credit_i` and `port_enabled_i` gate initiating transmissions." A low `port_enabled_i` starts no frame at all, responses included (same page, "A low port starts no gPTP frame."). Exact fix: "`tx_credit_i` gates initiating transmissions; a low `port_enabled_i` starts no frame."
- **RES-3:** `docs/MANAGER.md:43-45`. "holds the current synthesis figures. They come from main `5dce647a`, measured on 2026-10-11." The HDL guide summary calls them "dated measurements", and the PR text says later RTL has landed since. The line also copies the commit and date from the HDL table. Exact fix: replace both lines with "The [HDL guide](HDL_DEVELOPER.md#out-of-context-measurement) holds the latest dated synthesis figures."
- **RES-4:** the issue #96 rule "values live in one table and are linked, never copied" is only partly met.
  - About 30 inline restatements of constants-table values remain on Current pages outside the gated tables. Examples: 375 ms ×6, 125 ms ×2, 20 us ×2, 100 us ×5, 200 ppm ×4, "fifth" ×3, word 1022 ×3. One of them is an ungated second value table, the servo-state thresholds at `docs/INTEGRATION.md:364-367`.
  - `receipts/value_copies.txt` lists 40 grep matches. 10 of those are the gated rows, the cadence table and the generator command.
  - Every copy equals the generator today, and each section now links the table. Nothing is wrong, but the copies are not gate-bound.
  - Exact fix: in the threshold table and each listed prose line, replace the literal with the constant name linked to `#protocol-constants`, for example "the [`SYNC_RTO_MS_C`](INTEGRATION.md#protocol-constants) Sync watch". Or record in `docs/README.md` that inline restatements are explanatory and that the constants table governs.

### SUGGESTION (non-blocking)

- **S-1, gate hardening (`scripts/check_docs.py` `constant_findings`):**
  - A row that names a backticked constant but whose value cell does not parse as a bare integer is silently skipped. A planted `| `SYNC_RTO_MS_C` | 376 ms |` passes.
  - Deleting a constant row also passes.
  - Fix: fail on any backticked-name row that does not parse, and require a fixed set of names. Probes: `limit_reformatted_constant_cell` and `limit_deleted_constant_row` in `receipts/plant_probes.txt`.
- **S-2, gate coverage (`rom_usage`):** the "Seeded regression" row is checked only against the `--seq-seed 0x200000` image. The engine suite also builds a `--sync-seq-seed 0x10000` image (`tb/verilator/engine/Makefile:40`). Both are 1,023 words today (`receipts/gen_*.txt` and the variant runs); checking both would keep the single row honest.
- **S-3, gate side effect:** `load_generator` imports the generator in-process, which writes `hdl/ucode/__pycache__/` into the tree on every `make docs`. The base gate did not write it. The directory is git-ignored, so nothing tracked changes. Setting `sys.dont_write_bytecode = True` before the import would keep the tree untouched.

## Check results against the review brief

### (1) Statements against source and clause: 30 spot-checked, 1 wrong (F1)

| # | Statement (page) | Checked against | Result |
|---|---|---|---|
| 1 | ROM shipping 1,022 of 1,024, 2 free (MANAGER) | generator run, `receipts/gen_shipping.txt` | holds; base text 1,021 was stale, and base and head images are byte-identical (`receipts/gen_shipping_base.txt`) |
| 2 | Seeded 1,023 of 1,024, 1 free (MANAGER) | `--seq-seed 0x200000` (`receipts/gen_seeded.txt`) and `--sync-seq-seed 0x10000` runs | holds |
| 3 | Data words 1022 and 1023 count as used | `build()`: `used += 1` for each | holds |
| 4 | `SERVO@0` in prefix 0..15, `FUTO@254` outside it | generator leg printout; fixed table starts at 16 | holds |
| 5 | `--mac` colon form refused; integer form works | generator: rc 2 "invalid <lambda> value"; integer run rc 0 | holds |
| 6 | Each of the 17 constants rows (INTEGRATION) | `gen_gptp_ucode.py:323,505,510,513,518-547` | all 17 hold |
| 7 | `NPD_LO_C` "largest tolerated negative magnitude" | `:2131-2137` accepts d >= -80 inclusive | holds |
| 8 | `SLEW_SETTLED_NS_C` "band half-width" | `:1034-1035`: \|off\| <= 100 | holds |
| 9 | `LOST_CLEARS_AT_C` 5, "fifth loss clears" | `:525` | holds |
| 10 | Cadences 1 s / 125 ms / 3 s / 1 s on slots 0..3 | `:1615`, `:2314`, `:1595`/`:1854`/`:1887`, `:2356` | holds |
| 11 | `--cease-ms` override; engine suite uses 3,000 ms | `tb/verilator/engine/Makefile:18` | holds |
| 12 | Peer-delay table 11.2.2 / 11.2.15.2.3 / 11.2.15.2.4 / 11.2.16 | 2011 MDPdelayReq/Resp numbering used throughout the source (11.2.15.3 = Figure 11-8 diagram); 2020 11.2.19.3.x maps 1:1 | consistent |
| 13 | 10.3.12.1.4 g) gmPresent; i) self-publication | `gen_gptp_ucode.py:529`, `:2232`; `KL_gptp_engine.sv:137,779,1019` | consistent |
| 14 | Milan Annex B.1.1 holdover | `gen_gptp_ucode.py:1917`, `sim_main.cpp:191` | consistent |
| 15 | Figure 11-6 / 11.2.13 for the usable pair; 10.3.11 Figure 10-13 for ageing | `gen_gptp_ucode.py:50,1929`; `run_tsngen.py:393` | consistent |
| 16 | portEnabled 10.2.4.11 | `KL_gptp_engine.sv:108`; issue #94 title | consistent |
| 17 | pathTrace 10.3.8.21; thisClock 10.2.3.22; asCapable 10.2.4.1 | `KL_gptp_engine.sv:132`; `gen_gptp_ucode.py:228,938` | consistent |
| 18 | syncReceiptTimeout 10.6.3.1; allowedLostResponses 11.5.3 | `gen_gptp_ucode.py:37,521`; `sim_main.cpp:3610` | consistent |
| 19 | **Follow_Up companion 11.4.3** (GLOSSARY) | parser, generator, engine suite and decoder all use 11.4.4 / 11.4.7 | **wrong: F1** |
| 20 | Flags bit 0 gmPresent, bit 1 grandmaster, bit 2 asCapable, bit 3 sync-ok | `gen_gptp_ucode.py:598`, `:1921` | holds |
| 21 | Scratch 64 words, survives warm reset, cleared at configuration | `KL_gptp_engine.sv:30,238,307` | holds |
| 22 | Six state regions | `KL_gptp_engine.sv:20-38` | holds |
| 23 | NOTEN runs on each portEnabled edge (slot 6) | `gen_gptp_ucode.py:1529`, `:2187` | holds |
| 24 | Ports `rst_n`, `tx_credit_i`, `phc_step_o`, `pub_commit_o`; RX has no ready | `KL_gptp_engine.sv:64-155` | holds |
| 25 | Six `make tb` suites; bare `make` adds mutants in parser, engine, gaskets, tsngen but not ucpu | `Makefile:13-19`, each suite Makefile | holds |
| 26 | tsngen skips with rc 0 without its checkout (`TSAGEN_DIR`) | `run_tsngen.py:14-16,34-39` | holds |
| 27 | Gasket README: loopback chain, corrupted-frame drop, mutation arm | `gaskets/sim_main.cpp:1-20`, `mutants.py:1-20` | holds |
| 28 | Parent carries the slew level (`KL_gptp_shadow.sv#L150`, `milan_datapath.sv#L7329` at `1e80128f`); parent #545 closed | parent source at `1e80128f` (identical to `dev`); issue API | holds, `receipts/parent_pins.txt` |
| 29 | README risks: #58, parent #117, #64, #488 open | issue API, `receipts/issue_states.txt` | holds |
| 30 | Archived deltas: 4,773+80 = 4,853; 3,646+6 = 3,652; 4,853-105 = 4,748; 3,652-256 = 3,396 | arithmetic on the moved text | consistent; text moved unchanged apart from removed labels and the F2 link |

### (2) One home per value

- The constants table holds 17 rows, each constant once, and the gate rejects duplicates.
- The status table has one row per maintained page plus the archive row. The gate enforces exactly one row, and 14 pages are listed.
- Pages link to the table. Each value-bearing section opens with a link.
- Inline restatements remain. They are all correct today: RES-4.

### (3) Gate behaviour

- **At the head:** `make docs` exits 0 with "14 current pages, 18 historical pages", selftest 23 arms, source evidence 20 exact. `make diagrams-check` and `make contract` exit 0. `make lint` exits 0 with the pinned simulator, identity checked as 5.050.
- **At base:** `make docs` exits 0 with selftest 10 arms (`receipts/base_make_docs.log`).
- **Planted defects** (`scripts/plant_probes.sh`, `receipts/plant_probes.txt`, `receipts/plant_probes_full.log`): 14 planted stale cases each fail with exit 1 and the matching finding:
  - stale shipping ROM row, stale seeded row, stale free count only, deleted ROM row;
  - drifted constant, drifted comma-grouped constant, drifted `DEPTH`, unknown constant name;
  - a generator constant changed with the docs untouched;
  - deleted status row, wrong status value, row for a missing page, a new page without a row, deleted archive row.

  The unmutated control and a comment-only generator edit both pass. Four coverage limits pass silently, as expected: deleted constant row, unparsable value cell, cadence literal, prose copy. See S-1 and RES-4.
- **CI hygiene:** the repository carries no hosted workflow files. Its local gates are the Makefile targets above.

### (4) Delta scope

`git diff --name-status 135afd04..8607347` shows 11 `.md` files and `scripts/check_docs.py`, with no other path and no mode change (`receipts/delta_scope.txt`). There is no RTL, generator, generated-file or test change, and there are no submodule gitlinks. At the head (`receipts/head_*.log` / `.rc`):
- lint passes;
- ucpu 768/768, parser 378/378, gaskets 81/81, tsngen 288/288;
- engine 2048 ×3 plus 60, all pass;
- bench tag test passes.

The clone was restored to exact head bytes afterwards (`receipts/clone_integrity.txt`).

### (5) Start-here path and glossary

`README.md#start-here` gives scope, edition, reading order and layout, and the layout matches the top-level directories. All 37 intra-repo anchors on the changed pages resolve (`scripts/check_anchors.py`, `receipts/anchors.txt`). The glossary is readable. Its engine terms link to existing sections. Its protocol terms carry clause numbers, with one wrong (F1).

### (6) Privacy and labels

The 590 added lines were scanned for host or device names, home or scratch paths, tool or model names, and lane, round or reviewer labels. There are no hits. "Reviewer" appears only as an audience role. The PR removed the "lane M7" text and the round-labelled evidence path from `docs/MANAGER.md`. The PR body's leading role label is allowed in PR text. The new `check_docs.py` docstrings carry no labels and match the file's existing comment style.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | GLOSSARY clause column; INTEGRATION peer-delay, self-publication, gmPresent, ageing and constants clauses; generator, RTL and test clause citations; decoder protocol descriptions | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| RTL | CLEAN | delta scope (no `hdl/` change); `make lint` rc 0; ports, regions, scratch, flags and timer slots read in the RTL and generator against the docs | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Robustness | CLEAN (S-1..S-3 only) | `scripts/check_docs.py` new functions; 19 planted probes; generator subprocess and temp-dir use; tree cleanliness after the gate | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Tests | CLEAN | docs selftest 23 arms; planted probes; head suites ucpu, parser, engine, gaskets, tsngen and bench tag; contract | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Docs | UNCLEAN (F1, F2) | all 11 changed Markdown files, the status and constants tables, the archive move and index, the anchors, the summaries; RES-1..RES-4 | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |

## Real limits

- The clause text of IEEE 802.1AS-2011 (with Cor1/Cor2) and Milan v1.2 was not available in this review environment. Clause numbers were checked against:
  - the repository's own RTL, generator and test citations;
  - the independent decoder's protocol descriptions;
  - the 2011 to 2020 numbering map.
- Not independently confirmed against the standard text: the Milan subclause numbers this PR introduces (4.2.6.2.1, 4.2.6.2.2, 4.2.6.2.3, and 4.2.6.1 for BTCA), 11.2.13 / Figure 11-6, 10.3.8.21, and 8.6.2.1. They are internally consistent and not contradicted by any source.
- The engine mutation arm and `make ooc` were not run. Their inputs are byte-identical to base.
- Parent consumer gates were not run; that would be a parent bank.
- No source bank was run at this head by the manager, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus the focused runs listed here.
- Physical calibration was NOT RUN. Simulation is not hardware proof.

## Pending manager duties

- Validate the current-dev merge candidate (source base `135afd04`, live dev `1e80128f`) with the builder and native banks at the merge turn, and link the receipts.
- At the parent bump, re-pin the parent gPTP docs and submodule-docs pages to the new gitlink. The author's receipts show those parent gates fail identically at base and head until re-pinned.
- Carry RES-1..RES-4 to the residue checklist.
- Hosted/act acceptance.

## Prior public findings

PENDING: these are read only after this verdict and ledger were written.

R739-1 FINISHED
