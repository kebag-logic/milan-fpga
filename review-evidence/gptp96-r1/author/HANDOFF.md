# [A707] FPGA-gPTP #96 documentation sweep: handoff

Status: REVIEW READY. Not pushed, no PR opened (not allowed in this lane).

- Repository: Mister-M-alt/FPGA-gPTP, local branch `96-docs-sweep`
- Base: main `135afd043309369a87ddbc8d6550aff8ec52a157`
- Head: `8607347675743fe8d1ccaa370c63905c5ca1ccd5`
- TAKEN on #96: issuecomment-6518954762
- REVIEW READY on #96 (with head): issuecomment-6519751211
- Commits (one-line subjects, no body, no trailers):
  - `a1cfb2e` Add the start-here path, glossary, status and constants tables, and correct the 2020 clauses, the generator command and the ROM budget (#96)
  - `59d562d` Tie the status, constants and ROM budget tables to the tree in the docs gate (#96)
  - `7260948` State that the parent now carries the slew-active level, closed by parent #545 (#96)
  - `8607347` Link each value-bearing section to the protocol constants table (#96)
- Diff: 12 files. 11 Markdown, plus `scripts/check_docs.py` (a docs gate). No RTL, generator, generated-file or test change.

## Acceptance (issue #96)

| Item | Met | Evidence |
|---|---|---|
| Every document has a status | Yes | `docs/README.md` "Document status" lists all 14 maintained pages plus the archive. `make docs` fails on a missing row. The 18 archive pages carry `[OBSOLETE + date]` / `Status: Historical` banners, which the existing archive check enforces. |
| No current document contradicts the code or a clause | Yes, for every contradiction found | Seven contradictions fixed (C1 to C7 below). Method and limits are under "Verification method". |
| Start-here path exists | Yes | `README.md#start-here`: scope, reading order, repository layout. Plus `docs/GLOSSARY.md`, and a summary at the top of each long page. |
| Docs gates pass | Yes | `make docs` and `make diagrams-check` rc 0 at base and head. See the gate table. |

## Inventory

Status legend:
- **Current**: checked at head against the source and against IEEE 802.1AS-2011 with Cor1/Cor2 and Milan v1.2 chapter 4.
- **Historical**: archived and bannered, never edited for content.

### Maintained pages (14)

| Page | Lines | Purpose | Audience | Describes | Status | Evidence |
|---|---:|---|---|---|---|---|
| `README.md` | 98 | Start here; role routing; risks | Every reader | Repository scope and layout | Current (edited) | Layout table matches `git ls-files` top-level dirs. Risk issues #58, parent #117, #64 and #488 are all OPEN (checked with `gh`). Parent links pin `ac2c5e77`. |
| `docs/README.md` | 88 | Documentation map, truth order, status table | Every reader | All Markdown pages | Current (edited) | The new status gate binds it to the file tree. |
| `docs/GLOSSARY.md` | 52 | Defined terms with clause numbers | Every reader | 802.1AS-2011, Milan 4.2.6, engine terms | Current (new) | Each clause number was checked in the 2011 text: 10.2.4.1, 10.2.4.11, 10.2.3.22, 10.3.8.21, 10.3.12.1.4 g), 10.6.3.1, 11.2.13, 11.2.15, 11.2.16, 8.6.2.1. Engine anchors were resolved by a scratch anchor check. |
| `docs/MANAGER.md` | 125 | Readiness, ROM budget, risks, decisions | Manager | Delivery status, ROM packing | Current (edited) | The ROM budget is gate-bound to the generator: shipping 1,022/1,024, seeded 1,023/1,024. `SERVO@0`, `FUTO@254` and dispatch from 16 match the generator printout and `build()` fixed table. |
| `docs/INTEGRATION.md` | ~890 | External engine contract | System integrator | `KL_gptp_engine` ports, policy, publication, constants | Current (edited) | Port list matches `hdl/top/KL_gptp_engine.sv:62-155`. The constants table is gate-bound to `gen_gptp_ucode.py`. Clauses were corrected to 2011+Cor (C1 to C4). The generator command was fixed (C5) and the slew consumer updated (C7). |
| `docs/HDL_DEVELOPER.md` | ~415 | Module map, state regions, invariants, OOC figures | HDL contributor | `hdl/` | Current (edited: summary, link) | Regions 0 to 5 match the engine header `KL_gptp_engine.sv:19-36`. Flags bits 0 to 3 match `FL_*` at `gen_gptp_ucode.py:598`. Scratch 6/39/45/46 match `S_SSEQFLY`/`S_RSPSEQ`/`S_SYNCSRC`/`S_SRTO`. Timer slots 0 to 6 match `_tmr_slot_dispatch`. ROM word 1022 bit 32 matches `ROM_GMCAP_BIT_C`. Path-present bit 63 of word 12 matches `KL_gptp_rx_parser.sv:398`. The OOC table is dated (main `5dce647a`, 2026-10-11) and is now the single copy. |
| `docs/TEST_DEVELOPER.md` | ~215 | Verification layers, entry points, suite duties | Test developer | `tb/`, `bench/`, `scripts/` | Current (edited) | Entry points now cover all six `make tb` suites (gaskets and tsngen were missing, C6). Mutants targets were checked per Makefile; ucpu has none. |
| `docs/SOURCE_EVIDENCE.md` | 59 | Claim to source line ledger | Reviewer | RTL and generator anchors | Current (unchanged) | `check_source_evidence.py`: 20 exact, 0 findings, at base and head. |
| `docs/diagrams/README.md` | 81 | Diagram sources, render and check | Maintainer | `docs/diagrams/`, `scripts/generate_diagrams.py` | Current (unchanged) | `generate_diagrams.py --check` and `--selftest` rc 0. |
| `tb/verilator/engine/README.md` | 20 | Suite entry point | Test developer | Engine suite | Current (unchanged) | `make` runs the shipping and seeded images (Makefile `run`), then mutants. |
| `tb/verilator/parser/README.md` | 24 | Suite entry point | Test developer | Parser suite | Current (unchanged) | 378 + 16 checks pass. Mutation arm present. |
| `tb/verilator/ucpu/README.md` | 18 | Suite entry point | Test developer | MicroCPU suite | Current (unchanged) | 768 checks pass against the independent model. |
| `tb/verilator/gaskets/README.md` | 20 | Suite entry point | Test developer | Bench MII gasket loopback | Current (new) | Matches `gasket_tb_top.sv` header and Makefile (`all: run mutants`). 81 + 5 checks pass. |
| `tb/tsngen/README.md` | 20 | Suite entry point | Test developer | Independent-decoder cross-check | Current (new) | Matches `run_tsngen.py` docstring (skip rc 0 without checkout, `TSAGEN_DIR`). 288 + 4 checks pass here. |

### Archive pages (19 files: index + 18)

All carry the archive banner and an indexed successor. `check_docs.py` `archive_metadata_findings` enforces the banner, original path, date, successor target, single index row and total (now 18). Content is not edited.

| Page | Lines | Purpose | Status | Successor |
|---|---:|---|---|---|
| `docs/history/v1/README.md` | 49 | Archive index and reading rules | Historical index (row and total updated) | n/a |
| `docs/history/v1/PROJECT_STATUS.md` | 263 | Former README | Historical | `README.md` |
| `docs/history/v1/RESOURCE_VALIDATION.md` | 1063 | 2026-08-14 resource campaign | Historical | `docs/MANAGER.md` |
| `docs/history/v1/RESOURCE_DELTAS_2026_10.md` | 57 | PR #76 and timer-storage OOC deltas, moved out of MANAGER | Historical (new) | `docs/HDL_DEVELOPER.md` |
| `docs/history/v1/BENCH_FIRSTLIGHT.md` | 74 | 2026-08-14 bench | Historical | `docs/MANAGER.md` |
| `docs/history/v1/BENCH_GRANDMASTER.md` | 84 | 2026-08-14 bench | Historical | `docs/MANAGER.md` |
| `docs/history/v1/testing/ENGINE_TEST_RECORD.md` | 199 | Former engine suite README | Historical | `docs/TEST_DEVELOPER.md` |
| `docs/history/v1/testing/PARSER_TEST_RECORD.md` | 140 | Former parser suite README | Historical | `docs/TEST_DEVELOPER.md` |
| `docs/history/v1/testing/UCPU_TEST_RECORD.md` | 26 | Former ucpu suite README | Historical | `docs/TEST_DEVELOPER.md` |
| `docs/history/v1/prototype/ARCHITECTURE.md` | 300 | Prototype-line architecture | Historical | `docs/HDL_DEVELOPER.md` |
| `docs/history/v1/prototype/IP_BLOCKS.md` | 396 | Prototype IP design book | Historical | `docs/HDL_DEVELOPER.md` |
| `docs/history/v1/prototype/FSM_CONFORMANCE.md` | 111 | Prototype FSM audit | Historical | `docs/SOURCE_EVIDENCE.md` |
| `docs/history/v1/prototype/VERIFICATION.md` | 164 | Prototype verification record | Historical | `docs/TEST_DEVELOPER.md` |
| `docs/history/v1/prototype/MGMT_INTERFACE.md` | 105 | Prototype management interface | Historical | `docs/INTEGRATION.md` |
| `docs/history/v1/prototype/INTEGRATION_GUIDE.md` | 419 | Prototype integration guide | Historical | `docs/INTEGRATION.md` |
| `docs/history/v1/prototype/RESOURCE_VALIDATION.md` | 206 | Prototype resource record | Historical | `docs/MANAGER.md` |
| `docs/history/v1/prototype/BENCH_OPERATIONS.md` | 219 | Prototype bench operations | Historical | `docs/MANAGER.md` |
| `docs/history/v1/prototype/BENCH_ASCAPABLE.md` | 94 | 2026-08-15 bench | Historical | `docs/MANAGER.md` |
| `docs/history/v1/prototype/BENCH_TAP_WIRETRUTH.md` | 245 | 2026-08-15 bench | Historical | `docs/MANAGER.md` |

## Changes (file:line at head, reason)

### Contradictions fixed (the doc was wrong; the code was right)

- **C1** `docs/INTEGRATION.md:337-344`. The peer-delay clause table cited IEEE 802.1AS-2020 (11.2.19.3.3, 11.2.19.3.4, 11.2.20). Milan v1.2 4.2.6 profiles 802.1AS-2011 with Cor1/Cor2. It now cites 2011 11.2.2, 11.2.15.2.3 (computePdelayRateRatio), 11.2.15.2.4 (computePropTime) and 11.2.16 (MDPdelayResp).
- **C2** `docs/INTEGRATION.md:615` and `:645`. These cited "802.1AS-2020 10.3.13.2.4" (updtStatesTree). They now cite 2011 10.3.12.1.4 i) (pathTrace = {thisClock} when this system is grandmaster) and 10.3.12.1.4 g) (gmPresent).
- **C3** `docs/INTEGRATION.md:675`. "Annex B.1.1 holdover" named no document. 802.1AS-2011 B.1.1 is Frequency accuracy; the holdover tu rule is Milan v1.2 Annex B.1.1. It now says Milan.
- **C4** `docs/INTEGRATION.md:711-715`. The usable-pair rule was attributed to 10.3.11. 10.3.11 (Figure 10-13) states the ageing. The Sync-with-matching-Follow_Up rule is MDSyncReceiveSM, Figure 11-6 (11.2.13), feeding 10.2.7.2.1 d). Both are now cited.
- **C5** `docs/INTEGRATION.md:811-823`. The generator command passed `--mac 02:a1:b2:c3:d4:e5`. `gen_gptp_ucode.py:2498` parses `--mac` with `int(s, 0)`, so the documented command exits 2 with "invalid <lambda> value". It now uses `0x02A1B2C3D4E5` and says colon form is refused. The output path moved from `/tmp` to the working directory.
- **C6** `docs/MANAGER.md:53-66`. The ROM budget said "1,021 of 1,024 words (99.7%)" and "three words remain free". The generator at base prints `1024 words, 1022 real (99.8%)`, so two are free; seeded images are 1,023. It is now a table bound to the generator by the docs gate.
- **C7** `docs/INTEGRATION.md:523-527`. It said the parent "must carry" `phc_slew_active_o`, with the connection belonging to parent #545. #545 is CLOSED, and parent `dev` 1e80128f carries it (`KL_gptp_shadow.sv:150`, `milan_datapath.sv:7329`). It now states that, with pinned links.

### Omissions fixed

- `docs/TEST_DEVELOPER.md:48-55` and `:22-24`. The gaskets and tsngen suites, both run by `make tb` (`Makefile:13-19`), were missing from the entry points. `tb/mutation_verdict.py`, `tb/tsngen/run_tsngen.py` and `scripts/check_docs.py` were missing from the language layers. The table now notes which suites' bare `make` adds mutants (ucpu has none).
- `tb/verilator/gaskets/README.md` and `tb/tsngen/README.md` are new. They were the only suite directories without a README.

### Rules applied

- **No lane or review labels.** `docs/MANAGER.md` had a "M7 timer-storage measurement" heading, "lane M7" and "lane head" in its text. It also linked a parent path carrying a review label. That material moved to `docs/history/v1/RESOURCE_DELTAS_2026_10.md`, without the labels. The evidence link now points at parent commit `4999d8d6`.
- **Values in one table.**
  - The OOC resource table was duplicated in `MANAGER.md` and `HDL_DEVELOPER.md`. MANAGER now links the HDL table, which is the single copy.
  - New `docs/INTEGRATION.md#protocol-constants` holds 17 generator constants. Each row names the constant and `make docs` checks the value.
  - Cadence literals are in a separate table explicitly marked unchecked.
  - Every value-bearing section (port enable, step versus slew, departure, lost responses, HDL receipt state, engine suite list) links the table.
- **Start-here path.** `README.md:10-37` adds scope, edition, reading order and layout. `docs/README.md:6-8` routes there and to the glossary.
- **Summaries.** Added at the top of `INTEGRATION.md`, `HDL_DEVELOPER.md`, `TEST_DEVELOPER.md` and `MANAGER.md` (the four long pages).
- **Defined terms.** New `docs/GLOSSARY.md`: 13 protocol terms with clause numbers, 17 engine terms with anchors.
- **Retirement.** Superseded measurement paragraphs were archived (above). There were no obsolete current pages to delete.
- **Parent constraints kept.**
  - All `SUBMODULE_DOCS` paths that parent `scripts/check_gptp_docs.py:259-272` requires still exist.
  - The one parent deep-link anchor, `INTEGRATION.md#step-versus-slew-policy`, is unchanged.
  - The parent copies none of the corrected values (grep for `1,021`, `99.7%`, colon MAC, `10.3.13.2.4`: none).

### New freshness gate (`scripts/check_docs.py`)

- `status_findings`. Every maintained Markdown page needs exactly one row in `docs/README.md` "Document status" with status Current. The archive row must be Historical, and every listed page must exist.
- `constant_findings`. Each `| `NAME` | value |` row in "Protocol constants" must equal the integer attribute `NAME` of the imported `hdl/ucode/gen_gptp_ucode.py`.
- `rom_findings`, through `rom_usage`. The script runs the generator as shipped (defaults) and seeded (`--seq-seed 0x200000`) into a temporary directory. The used, depth and free counts must match the MANAGER table.
- **Self-test.** `--selftest` grows from 10 to 23 arms; each planted mutant must produce a finding and each true control none:
  - status: complete table passes; missing row, row for an absent page, wrong status and duplicate row fail.
  - constants: true value passes; drifted value, unknown name and empty table fail.
  - ROM: true budget passes; drifted used count, drifted free count and missing row fail.
- **Real-tree planted mutants** (scratch copies, each `check_docs.py` rc 1 with the named finding; unmutated control rc 0):
  - `rom_stale`: MANAGER shipping row set to 1,021/3. Finding: "Shipping image reads 1021 of 1024 with 3 free; generator builds 1022 of 1024".
  - `const_drift`: INTEGRATION `SYNC_RTO_MS_C` set to 376. Finding: "SYNC_RTO_MS_C is 376, generator has 375".
  - `status_missing`: tsngen README row deleted. Finding: "no status row for tb/tsngen/README.md".
  - `code_drift`: generator `FU_RTO_MS_C = 126`, docs untouched. Finding: "FU_RTO_MS_C is 125, generator has 126", which shows the gate ties the doc to the code.
- The base `check_docs.py` also passes on the new Markdown (rc 0), so commit `a1cfb2e` is green on its own.

## Findings the docs cannot fix

No current doc was found to state behaviour that the RTL or microcode contradicts, once C1 to C7 were fixed. The findings below are in source comments (not editable here) or are verification limits.

| # | Location | Observation | Clause / source | Which side is wrong |
|---|---|---|---|---|
| F1 | `hdl/ucode/gen_gptp_ucode.py:284` | The v4 round note says asCapable falls "at the fourth" lost response. The microcode clears at the fifth (`LOST_CLEARS_AT_C = LOST_N_C + 2`, `:525`; leg at `:1700-1708`), and the docs agree. `:61` already says that reading "is retired", so it is labelled history, but it reads as current. | 802.1AS-2011 11.2.12.4, 11.5.3, Figure 11-8 as Cor1 changes it (`if (lostResponses <= allowedLostResponses) lostResponses += 1`) | The source comment (stale history note). Code and docs are right. |
| F2 | `hdl/ucode/gen_gptp_ucode.py:292-296` | The v4 note says syncReceiptTimeout "clears the sync-ok verdict". Since #89 the SRTO leg ages the grandmaster when gmPresent and clears sync-ok only when unaged (`:36-49`, `:2223-2248`). | 802.1AS-2011 10.3.11, Figure 10-13 (Cor1): `currentTime >= syncReceiptTimeoutTime && gmPresent` | The source comment (history note). Code and docs are right. |
| F3 | `hdl/ucode/gen_gptp_ucode.py:315-317` | The v4 note lists "the multiple-responder cease rule of Milan 4.2.6.2.5" as "still deliberately out". It is implemented (`CEASE_N_C`, `S_CEASE`, NOTEN #94). `:241` marks a similar list "retired by later rounds"; this one is not so marked. | Milan v1.2 4.2.6.2.5 | The source comment (history note). |
| F4 | `hdl/top/KL_gptp_engine.sv:43-45` | The header comment repeats a phrase: "becomes direct fabric wires becomes wires". | n/a | Source comment wording. |
| F5 | `docs/HDL_DEVELOPER.md` OOC table | Measured at main `5dce647a` (2026-10-11). 27 `hdl/` commits have landed since (#87, #88, #89, #90, #91, #94), so current LUT/FF/WNS may differ. The page labels the figures as dated; this lane runs no synthesis. | n/a | Neither; it needs a re-measurement (`make ooc`, synthesis tool required). |

## Verification method

- **Clauses.** The 802.1AS-2011, Cor1-2013, Cor2-2015, 802.1AS-2020 and Milan v1.2 consolidated PDFs were converted to text in scratch. Each clause number the current docs cite was located and read: 8.6.2.1; 10.2.3.22; 10.2.4.1; 10.2.4.11; 10.2.7.2.1; 10.3.8.21; 10.3.10.2.1 a) to d); 10.3.11 with Figure 10-13 (Cor1); 10.3.12.1.4 a), f), g), i); 10.6.3.1; 11.2.2; 11.2.12.4; 11.2.13 with Figure 11-6; 11.2.15 with Figure 11-8 (Cor1); 11.2.16; 11.5.3; Milan 4.2.6, 4.2.6.1.1, 4.2.6.2.1 to 4.2.6.2.7 and Annex B.1.1.
- **Numbers.**
  - Every protocol constant was checked against `gen_gptp_ucode.py` (now gate-bound).
  - Cadence literals were checked against `_tmr_cadence_gate` (1000, slot 0), `prog_leg_synctx` (125, slot 1), the receipt watch (3000, slot 2) and `prog_leg_anntx` (1000, slot 3).
  - The rate envelope formula matches `ppm_addend`. ROM counts are generator output. Storage sizes match the RTL (`evq_r [0:3]`, `scratch_r [0:63]`, `rf_r [0:15]`, `UCODE_W_C = 48`, `UPC_W_C = 10`, `SLOTS_P = 8`).
- **Commands.** The documented generator command was run (C5). `make` targets and per-suite targets were checked against each Makefile and run.
- **Issue states.**
  - #58, parent #117, #64, #488 and #621: OPEN, matching the docs.
  - #68, #75, #82, #84, #85, #87, #88, #94: CLOSED; the docs cite them as decided contracts.
  - Parent #545: CLOSED (C7).
- **Behavioural sentences.** The step/slew, ageing, cease, port-enable and publication sentences were checked against the generator constants and RTL constructs above. They rely for the rest on the engine suite's named checks (2048 × 3 + 60 at head) and the `SOURCE_EVIDENCE` anchors. Not every one of the roughly 900 integration-guide sentences was re-derived independently.
- **Residual inline values.** About 25 inline restatements of constants remain in prose (e.g. "375 ms", "200 ppm" in `INTEGRATION.md` and `HDL_DEVELOPER.md`). Each section now links the gate-bound table, but the prose copies themselves are not machine-checked. A later gate could bind them.
- **Private data.** Scanned all Markdown for private IPs, home paths, tty devices, MACs and serials. There are no hits beyond clause numbers, generic `ttyUSB` paths in an archive page, and the documented example MAC.

## Gate table

Environment: Verilator 5.050 (pinned), Python 3.14.8, `TMPDIR` set to scratch. Every command ran in the foreground, unpiped, with output redirected to a log and rc taken from the command itself.

### Repository gates

| Gate | Base `135afd04` | Head `86073476` |
|---|---|---|
| `make docs` (check_docs + selftest, source evidence + selftest, diagrams) | rc 0 (selftest 10 arms; 20 exact) | rc 0 (14 current, 18 historical; selftest 23 arms; 20 exact) |
| `make diagrams-check` | rc 0 | rc 0 |
| `make contract` | rc 0 | rc 0 |
| `make lint` | rc 0 | rc 0 |
| `make -C tb/verilator/ucpu` | rc 0 (768/768) | rc 0 (768/768) |
| `make -C tb/verilator/parser` (run + mutants) | rc 0 (378, 16) | rc 0 (378, 16) |
| `make -C tb/verilator/engine run` | rc 0 (2048 × 3, 60) | rc 0 (2048 × 3, 60) |
| `make -C tb/verilator/gaskets` (run + mutants) | rc 0 (81, 5) | rc 0 (81, 5) |
| `make -C tb/tsngen` (run + mutants) | rc 0 (288, 4) | rc 0 (288, 4) |
| `make -C bench/arty test` | rc 0 | rc 0 |
| `make -C tb/verilator/engine mutants` | NOT RUN | NOT RUN |
| `make ooc` | NOT RUN | NOT RUN |

- **Engine mutants.** About 137 mutants, each a full Verilator rebuild, with no subset option (`mutants.py:956`). This exceeds a foreground command. Its inputs (`hdl/`, generator, `tb/verilator/engine/*`) are byte-identical between base and head (`git diff --stat 135afd04..86073476` touches only Markdown and `scripts/check_docs.py`).
- **`make ooc`.** Needs the synthesis tool; out of scope.
- Base gates ran in the lane before the first commit; gaskets, tsngen and bench ran in a scratch worktree at base (since removed).

### Parent consumer gates

These are required because `scripts/check_docs.py` changed. Setup: a scratch clone of kebag-logic/milan-fpga at PR #805 head `e06ade31`, with `protocol-processor` and `gptp-processor` initialised. The gitlink was set with `update-index` and the checkout with `--show-toplevel` verified before each git command. Nothing was committed or pushed.

| Gate | Gitlink `f97c1803` (PR #805 pin) | Gitlink base `135afd04` | Gitlink head `86073476` |
|---|---|---|---|
| `check_gptp_docs.py` | 0 | 1 | 1, findings identical to base |
| `check_gptp_docs.py --with-submodule` | 0 | 1 | 1, identical to base |
| `check_gptp_docs.py --selftest` | 0 | 1 | 1, identical to base |
| `make -C gptp-processor docs` | 0 | 0 | 0 |
| `check_submodule_docs.py` | 0 | 1 | 1, identical to base |
| `check_submodule_docs.py --selftest` | 0 | 0 | 0 |
| `measure_naming.py --check` | 0 | 0 | 0 |
| `measure_fail_fast.py --check` | 0 | 0 | 0 |
| `measure_test_evidence.py --check` | 0 | 0 | 0 |
| `check_hygiene.py --check` | 0 | 0 | 0 |
| `check_gptp_docs.py --with-submodule`, parent docs re-pinned from `f97c1803` to the gitlink (8 files, scratch only) | n/a | 0 | 0 |

- **The rc 1 rows are pin-driven.** Parent pages deep-link to `f97c1803`, and `check_submodule_docs.py` compares the documented pin and the boundary diagram. Any gitlink move fails them until the parent re-pins, so base fails the same way.
- With the pins rewritten, as an adopting PR does, the gPTP docs gate passes at base and head.
- The parent's code-quality ratchets see the changed script and stay green.

## Not done / follow-ups

- Engine mutation arm and `make ooc`: not run (see above).
- F1 to F4: source-comment cleanups for a code lane. F5: re-measure OOC.
- Optional: bind the remaining inline prose values to the constants table.
