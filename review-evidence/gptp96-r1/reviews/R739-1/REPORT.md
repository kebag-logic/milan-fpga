[R739] NEGATIVE - exact head 8607347675743fe8d1ccaa370c63905c5ca1ccd5

# Independent review R739-1: Mister-M-alt/FPGA-gPTP PR #97 (issue #96)

- Head `8607347675743fe8d1ccaa370c63905c5ca1ccd5`, tree `7791e003a4c235379f7dcdb2efc215b22c85c105`.
- Base main `135afd043309369a87ddbc8d6550aff8ec52a157`.
- Scope: the whole PR. That is 11 Markdown files plus `scripts/check_docs.py`, part of parent kebag-logic/milan-fpga#797.

## Order of work

- The independent pass was written to disk and sealed before any issue or PR comment, manager comment or other review was read.
- The sealed text is preserved as `INDEPENDENT.md`: sha256 `5c4aedb8d4506d5cc6032e5a3988000bec87bb7fa2bf63d113f6bf4aea39e428`, recorded in `receipts/verdict_written_before_comments.sha256`.
- That sealed verdict was already NEGATIVE, on F1 and F2 below.
- After the seal, the only prior public review findings on this PR (R740-1, F1 to F4) were read. Each is resolved below against the source at this head.
- Three are retained as open findings here, and two of those upgrade items the sealed pass had graded lower. The ledger below is the final, reconciled one; the sealed ledger is in `INDEPENDENT.md`.

## Verdict basis

- **Clause error on a Current page (F1):** a new page marked Current cites the Sync message clause for the Follow_Up message.
- **Interface error (F3):** the new summaries state a wire-level publication atomicity that the RTL does not provide.
- **Gate guarantee does not hold (F4):** the new constants gate silently skips stale rows written in ordinary Markdown formats.
- **Single-source rule not met (F5):** the issue's binding rule "values live in one table and are linked, never copied" is not met. A copied threshold table can drift with the gate still passing.
- **Archive pointer (F2):** a moved evidence link names the wrong artifact.

Issue #96 acceptance item 2, "no document marked current contradicts the code or a clause", is not met (F1, F3).

What holds at the head:
- the ROM budget and generator-command corrections;
- the 2011 renumbering of the peer-delay and role-selection clauses, consistent with the source;
- the status table and its gate;
- the ROM-budget gate;
- the delta scope (no RTL, generator, generated-file or test change);
- the start-here path and anchors;
- privacy.

## Findings

### F1 - MINOR - Conformance, Docs (independent; same defect as R740-1 F4)

- **Where:** `docs/GLOSSARY.md:19`, row `| Follow_Up companion | Two-step message carrying the precise transmit time | 11.4.3 |`.
- **Authority:** IEEE 802.1AS-2011 numbers the message-format clauses this way: 11.4.3 is the Sync message, 11.4.4 the Follow_Up message (preciseOriginTimestamp 11.4.4.2.1, information TLV 11.4.4.3), and 11.4.7 the Pdelay_Resp_Follow_Up message.
- **Evidence in this tree:**
  - `hdl/wire/KL_gptp_rx_parser.sv:30-31`, `:172-175` cite 11.4.4.3 and 11.4.4.2.2.
  - `hdl/ucode/gen_gptp_ucode.py:224`, `:955` cite 11.4.4 for pairing.
  - `tb/verilator/engine/sim_main.cpp:124` cites 11.4.4; `:1851` cites 11.4.5 for Pdelay_Req.
  - The independent decoder's 802.1AS-2011 protocol descriptions that `tb/tsngen` loads head the Sync file "11.4.3: Sync message", the Follow_Up file "11.4.4" and the Pdelay_Resp_Follow_Up file "11.4.7".
  - Nothing else cites 11.4.3 for Follow_Up.
- **Impact:** a new Current page points a new engineer to the wrong normative message definition. This contradicts a clause. The author's published clause list (`review-evidence/gptp96-r1/author/HANDOFF.md`, "Verification method") does not include 11.4.3.
- **Required outcome:** `| Follow_Up companion | Two-step message carrying the precise transmit time | 11.4.4, 11.4.7 |`. If the row is meant to cover only Sync's companion, cite 11.4.4 alone.
- **Verification:** `grep -n 'Follow_Up companion' docs/GLOSSARY.md`; `make docs` exits 0.

### F2 - MINOR - Docs (independent; not raised by R740-1)

- **Where:** `docs/history/v1/RESOURCE_DELTAS_2026_10.md:32`, "The parent commit [`4999d8d6`](https://github.com/kebag-logic/milan-fpga/commit/4999d8d6344e373e0204995cb36c93cf616e8f9e) records the reports."
- **Evidence:**
  - Base `docs/MANAGER.md` linked the reports by tree path at that commit, under the author report directory.
  - The PR swapped that for a commit link. That commit's change set is 97 review-archive files for a different round, and 0 of them are measurement reports (`receipts/parent_4999d8d6.txt`).
  - The `.rpt` reports exist only in the tree at that commit, under a path the page no longer gives.
  - The history index's rule is "Preserve commit references for reproducibility" (`docs/history/v1/README.md:12`).
- **Impact:** the archived PR #76 figures lose their reproducible evidence pointer, and a reader lands on an unrelated review archive. This is a factual misstatement about an artifact. Restoring a precise pointer touches the label rule, because the original path carries a round label, so it is not RESIDUE.
- **Required outcome:** link the reports themselves, for example the tree URL of the author report directory at `4999d8d6`, with label-free visible text. Reword as "The parent tree at `4999d8d6` holds the measurement reports."
- **Verification:** the link lands on the `.rpt` files; `make docs` exits 0.

### F3 - MINOR - RTL, Docs (retained from R740-1 F1; missed by the sealed pass)

- **Where:**
  - `docs/INTEGRATION.md:14`, "Publication outputs change together on `pub_commit_o`."
  - `docs/HDL_DEVELOPER.md:12`, "Publication changes only through one commit."
  - Both lines were added by this PR.
- **Evidence, independently confirmed at this head:**
  - `hdl/top/KL_gptp_engine.sv:994-997` writes `pub_gm_r`, `pub_parent_r` and `pub_flags_r` on separate state-port writes.
  - `:1037-1053` writes the path on its own.
  - `:1134-1146` assigns those registers straight to the `pub_*_o` outputs, with `pub_commit_o` a separate pulse. There is no output latch at commit.
  - The microcode stages fields over several instructions before `COMMIT`. For example, `gen_gptp_ucode.py` BECOME writes publish word 0, then word 1, then scratch, then word 6, then `COMMIT` (around `:1940-1953`).
  - The RTL's own assertion comment at `:874-876` says "Address 7 may change raw path state before publication".
- **Impact:** an integrator reading the summary would treat the outputs as stable and atomic between pulses, but they can show a mixed tuple. The page body has the correct contract: "Sample outputs when `pub_commit_o` rises." (`docs/INTEGRATION.md:551`, `docs/HDL_DEVELOPER.md:319-321`). The summaries contradict the RTL and that body.
- **Required outcome:** reword both summaries to the sampling contract, for example "Sample publication outputs on `pub_commit_o`; they may change while staging." Reconcile the existing equivalent line `README.md:60` ("Publication outputs expose committed protocol state") the same way.
- **Verification:** each statement names `pub_commit_o` as the sampling boundary and claims no wire-level atomicity; `make docs` exits 0.

### F4 - MINOR - Robustness, Tests, Docs (retained from R740-1 F2; the sealed pass graded it SUGGESTION S-1)

- **Where:** `scripts/check_docs.py:110` (`CONSTANT_ROW_RE`) and `constant_findings`; the claim at `docs/INTEGRATION.md:837`, "`make docs` fails when any value drifts from the generator."
- **Evidence:** in disposable copies of the head, `SYNC_RTO_MS_C` was changed from 375 to each of `**376**`, `-1` and `376 ms`. Each passes with rc 0 (`receipts/reconcile_probes.txt`; `receipts/plant_probes.txt` `limit_reformatted_constant_cell`). The plain stale `376` fails correctly. A row naming a constant is silently skipped when its cell does not match the bare-integer pattern. A deleted constant row also passes (`limit_deleted_constant_row`).
- **Impact:** a visible stale value in the authoritative table passes the gate. That contradicts a guarantee stated on a Current page and in the PR text. None of the 23 self-test arms covers it.
- **Required outcome:** match a constants row by its backticked name regardless of the cell's syntax. Then either parse the supported formatting or fail with a named diagnostic on an unparsable cell. Optionally, require the expected set of names so that a deleted row also fails. Add a control that passes and planted defects that fail for each case.
- **Verification:** run `scripts/reconcile_probes.sh` and `scripts/plant_probes.sh` against the fixed tree. The control passes, the three formatted stale cells fail, all existing arms still pass, and `--selftest` shows the new arms.

### F5 - MINOR - Docs (retained from R740-1 F3; the sealed pass graded it RESIDUE RES-4)

- **Where:** these Current pages restate constants-table values outside the gated tables:
  - an ungated second value table, the servo-state thresholds at `docs/INTEGRATION.md:364-367` (20 us, 100 us, against `STEP_LINKUP_NS_C` and `STEP_LOCKED_NS_C`);
  - in `docs/INTEGRATION.md`: 375 ms at `:394`, `:495`, `:707`, `:725`; 125 ms at `:497`, `:749`; 20 us at `:381`; 100 us at `:406`, `:436`, `:446`, `:537`; 200 ppm at `:414`, `:438`, `:444`; fifth at `:803`;
  - in `docs/HDL_DEVELOPER.md`: `:166`, `:174`, `:203`, `:255`;
  - in `docs/TEST_DEVELOPER.md`: `:129`, `:143`, `:154`;
  - in `docs/MANAGER.md`: `:47` and `:64`.

  The full grep is in `receipts/value_copies.txt`.
- **Authority:** issue #96 Rules, "Values live in one table and are linked, never copied." Parent #797's sweep decision (issuecomment-6518880512) states "The rules are the issue's", so the rule binds this sweep.
- **Evidence:** every copy equals the generator today. However, changing the threshold table to 21 us, or the HDL-guide prose to 376 ms, leaves `check_docs.py` at rc 0 (`receipts/reconcile_probes.txt`). The author's handoff acknowledges about 25 remaining restatements.
- **Impact:** several independently editable homes for each value remain, so a stale copy can appear on a Current page with the gate still passing.
- **Required outcome:** keep each value in its constants row only. Elsewhere, name the constant and link its row, for example "the [`SYNC_RTO_MS_C`](INTEGRATION.md#protocol-constants) Sync watch". Keep dated measurements and test stimuli clearly distinct from configuration values.
- **Verification:** an audit grep over the current pages finds each constants-table value only in its row, and `make docs` exits 0.

### RESIDUE (wording only; does not change the verdict)

- **RES-1:** `docs/INTEGRATION.md:13`. "PHC outputs are one-cycle step and rate pulses." This leaves out the level `phc_slew_active_o`. Exact fix: "PHC step and rate writes are one-cycle pulses; `phc_slew_active_o` is a level."
- **RES-2:** `docs/INTEGRATION.md:12`. "`tx_credit_i` and `port_enabled_i` gate initiating transmissions." A low port starts no frame at all (`:233`). Exact fix: "`tx_credit_i` gates initiating transmissions; a low `port_enabled_i` starts no frame."
- **RES-3:** `docs/MANAGER.md:45`. "holds the current synthesis figures." The figures are dated, and later RTL has landed. Exact fix: "holds the latest dated synthesis figures." The copied commit and date on `:47` are covered by F5.

### SUGGESTION (non-blocking)

- **S-2:** `rom_usage` checks the "Seeded regression" row only against `--seq-seed 0x200000`. The engine suite also builds `--sync-seq-seed 0x10000` (`tb/verilator/engine/Makefile:40`). Both images are 1,023 words today; checking both keeps the single row honest.
- **S-3:** `load_generator` writes `hdl/ucode/__pycache__/` into the tree on every `make docs`, which the base gate did not do. The directory is git-ignored. Set `sys.dont_write_bytecode = True` before the import.

## Resolution of prior public findings (R740-1, the only prior review on this PR)

| Prior finding | Resolution at this head | Here |
|---|---|---|
| R740-1 F1, publication atomicity in summaries | **Retained.** Independently confirmed in the RTL (see F3). | F3 |
| R740-1 F2, constants gate skips formatted or negative cells | **Retained.** Reproduced: `**376**`, `-1` and `376 ms` all pass. The sealed S-1 is upgraded because a stated guarantee does not hold. | F4 |
| R740-1 F3, values copied, contrary to the one-table rule | **Retained.** Reproduced: a drifted copy table and drifted prose both pass. Parent #797 binds the issue's rules. The sealed RES-4 is upgraded. | F5 |
| R740-1 F4, glossary Follow_Up 11.4.3 | **Retained.** It is the same defect as the independent F1. | F1 |

The issue #96 comments are assignment and readiness notices only. PR #97 has two review-start notices and the R740-1 report, and no review or inline-comment entries. No manager evidence comment or manager source bank is present.

## Check results against the review brief

### (1) Statements against source and clause: 30 spot-checked independently, 1 wrong (F1); F3 added at reconciliation

| # | Statement (page) | Checked against | Result |
|---|---|---|---|
| 1 | ROM shipping 1,022 of 1,024, 2 free (MANAGER) | generator run (`receipts/gen_shipping.txt`) | holds; base 1,021 was stale; base and head images byte-identical (`receipts/gen_shipping_base.txt`) |
| 2 | Seeded 1,023 of 1,024 | `--seq-seed 0x200000` (`receipts/gen_seeded.txt`), `--sync-seq-seed 0x10000` | holds |
| 3 | Data words 1022 and 1023 count as used | `build()` | holds |
| 4 | `SERVO@0` in prefix 0..15; `FUTO@254` outside it | generator leg printout; fixed table from 16 | holds |
| 5 | Colon `--mac` refused; integer form works | rc 2 "invalid <lambda> value"; rc 0 | holds |
| 6 | All 17 constants rows | `gen_gptp_ucode.py:323,505,510,513,518-547` | hold |
| 7 | `NPD_LO_C` largest tolerated negative magnitude | `:2131-2137`, d >= -80 inclusive | holds |
| 8 | `SLEW_SETTLED_NS_C` band half-width | `:1034-1035` | holds |
| 9 | `LOST_CLEARS_AT_C` 5 | `:525` | holds |
| 10 | Cadences 1 s / 125 ms / 3 s / 1 s on slots 0..3 | `:1615`, `:2314`, `:1595`/`:1854`/`:1887`, `:2356` | holds |
| 11 | `--cease-ms`; engine suite 3,000 ms | `tb/verilator/engine/Makefile:18` | holds |
| 12 | 11.2.2 / 11.2.15.2.3 / 11.2.15.2.4 / 11.2.16 | 2011 MDPdelayReq/Resp numbering in source; maps 1:1 from 2020 11.2.19.3.x | consistent |
| 13 | 10.3.12.1.4 g) and i) | `gen_gptp_ucode.py:529,2232`; `KL_gptp_engine.sv:137,779,1019` | consistent |
| 14 | Milan Annex B.1.1 holdover | `gen_gptp_ucode.py:1917`; `sim_main.cpp:191` | consistent |
| 15 | Figure 11-6 / 11.2.13; 10.3.11 Figure 10-13 | `gen_gptp_ucode.py:50,1929`; `run_tsngen.py:393` | consistent |
| 16 | portEnabled 10.2.4.11 | `KL_gptp_engine.sv:108`; issue #94 | consistent |
| 17 | pathTrace 10.3.8.21; thisClock 10.2.3.22; asCapable 10.2.4.1 | `KL_gptp_engine.sv:132`; `gen_gptp_ucode.py:228,938` | consistent |
| 18 | syncReceiptTimeout 10.6.3.1; allowedLostResponses 11.5.3 | `gen_gptp_ucode.py:37,521`; `sim_main.cpp:3610` | consistent |
| 19 | **Follow_Up companion 11.4.3** | parser, generator, engine suite, decoder | **wrong: F1** |
| 20 | Flags bits 0..3 | `gen_gptp_ucode.py:598,1921` | holds |
| 21 | Scratch 64 words, warm-retained, cleared at configuration | `KL_gptp_engine.sv:30,238,307` | holds |
| 22 | Six state regions | `KL_gptp_engine.sv:20-38` | holds |
| 23 | NOTEN on portEnabled edges, slot 6 | `gen_gptp_ucode.py:1529,2187` | holds |
| 24 | Ports `rst_n`, `tx_credit_i`, `phc_step_o`, `pub_commit_o`; RX has no ready | `KL_gptp_engine.sv:64-155` | holds |
| 25 | Six `make tb` suites; which bare `make` adds mutants | `Makefile:13-19`; suite Makefiles | holds |
| 26 | tsngen skips rc 0 without its checkout | `run_tsngen.py:14-16,34-39` | holds |
| 27 | Gasket README | `gaskets/sim_main.cpp:1-20`, `mutants.py:1-20` | holds |
| 28 | Parent carries the slew level at `1e80128f`; parent #545 closed | parent source (identical to `dev`); issue API (`receipts/parent_pins.txt`) | holds |
| 29 | README risks #58, parent #117, #64, #488 open | `receipts/issue_states.txt` | holds |
| 30 | Archived delta arithmetic | moved text | consistent |
| 31 (post-seal) | Publication outputs change together on commit | `KL_gptp_engine.sv:994-997,1037-1053,1134-1146` | **wrong: F3** |

### (2) One home per value

- The constants table holds each of its 17 constants once, and the gate rejects duplicate rows.
- The status table lists the 14 maintained pages once each plus the archive row, and the gate enforces it.
- Each value-bearing section links the table, but copies remain and can drift silently (F5).

### (3) Gate behaviour

- **At the head:** `make docs` exits 0 (14 current, 18 historical; selftest 23 arms; 20 exact anchors). `make diagrams-check` and `make contract` exit 0. `make lint` exits 0 with the pinned simulator, identity checked as 5.050.
- **At base:** `make docs` exits 0 with 10 arms.
- **Planted defects** (`scripts/plant_probes.sh`; `receipts/plant_probes.txt`, `receipts/plant_probes_full.log`): 14 planted stale cases fail with rc 1 and the matching finding:
  - stale shipping, seeded and free-only ROM rows, and a deleted ROM row;
  - drifted plain, comma-grouped and `DEPTH` constants, and an unknown name;
  - a generator constant changed with the docs untouched;
  - deleted status row, wrong status, row for a missing page, a new page without a row, deleted archive row.
- **Controls:** the unmutated tree and a comment-only generator edit both pass.
- **Escapes** (`receipts/reconcile_probes.txt`): formatted and negative stale cells (F4), plus copied values in prose and in the threshold table (F5).
- The repository has no hosted workflow files.

### (4) Delta scope

- 11 `.md` files plus `scripts/check_docs.py`. No other path, no mode change, no submodule gitlinks (`receipts/delta_scope.txt`).
- Head runs (`receipts/head_*`):
  - lint passes;
  - ucpu 768/768, parser 378/378, gaskets 81/81, tsngen 288/288;
  - engine 2048 ×3 plus 60, all pass;
  - bench tag test passes.
- The clone is restored to exact head bytes: tracked tree, index and worktree match HEAD, the ignored `__pycache__` was removed, and there are 0 gitlinks (`receipts/clone_integrity.txt`).

### (5) Start-here path and glossary

The start-here section has scope, edition, reading order and layout, and the layout matches the top-level directories. All 37 intra-repo anchors resolve (`scripts/check_anchors.py`, `receipts/anchors.txt`). The glossary is readable, with one wrong clause (F1).

### (6) Privacy and labels

The 590 added lines have no host or device names, private paths, tool or model names, or lane, round or reviewer labels. The PR removed the earlier lane text and the round-labelled path from `docs/MANAGER.md`. The PR body's role label is allowed in PR text. The new docstrings carry no labels.

## Ledger (reviewer-owned, final after reconciliation)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | GLOSSARY clause column; INTEGRATION clause tables and citations; generator, RTL and test citations; decoder descriptions | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| RTL | UNCLEAN (F3) | delta scope (no `hdl/` change); lint; ports, regions, scratch, flags, timer slots; publication staging and output assigns | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Robustness | UNCLEAN (F4) | `check_docs.py` new functions; 25 planted and reconciliation probes; subprocess and temp-dir use; tree cleanliness | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Tests | UNCLEAN (F4) | docs selftest 23 arms and its coverage; probes; head suites ucpu, parser, engine, gaskets, tsngen and bench tag; contract | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |
| Docs | UNCLEAN (F1-F5) | all 11 changed Markdown files; status and constants tables; archive move and index; anchors; summaries; RES-1..RES-3 | R739-1 | 8607347675743fe8d1ccaa370c63905c5ca1ccd5 |

The sealed independent ledger (`INDEPENDENT.md`) graded RTL, Robustness and Tests CLEAN. They changed only by retaining R740-1 F1 and F2 after independent confirmation. Four line references in the sealed text (F2 and RES-1..RES-3) are off by one or two lines; this report carries the corrected ones.

## Real limits

- The clause text of IEEE 802.1AS-2011 (with Cor1/Cor2) and Milan v1.2 was not available in this environment. Clauses were checked against:
  - the repository's RTL, generator and test citations;
  - the independent decoder's protocol descriptions;
  - the 2011 to 2020 numbering map.
- Not confirmed against the standard text, though consistent and uncontradicted: the Milan subclauses 4.2.6.2.1, 4.2.6.2.2 and 4.2.6.2.3, and 4.2.6.1 for BTCA, which this PR introduces; 11.2.13 / Figure 11-6; 10.3.8.21; 8.6.2.1.
- The engine mutation arm and `make ooc` were not run. Their inputs are byte-identical to base.
- Parent consumer gates were not run; that would be a parent bank.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus the focused runs here.
- Physical calibration was NOT RUN. Simulation and field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `135afd04`, live dev `1e80128f`) with the builder and native banks at the merge turn, and link the receipts.
- At the parent bump, re-pin the parent gPTP docs and submodule-docs pages. The author reports that those gates fail identically at base and head until re-pinned.
- Carry RES-1..RES-3 to the residue checklist.
- Hosted/act acceptance.

R739-1 FINISHED
