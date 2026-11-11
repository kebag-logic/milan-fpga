[A768]

## Contents

- **[Status](#status)** -- Ready for review: every acceptance item met, the gates the gPTP revert touches re-run at the head.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, related issues and roles.
- **[Description](#description)** -- The processor gitlink, the parent tests by clause, the campaign arms, the #495 rows and the route.
- **[Authoritative references](#authoritative-references)** -- The clauses, the donor PRs and the rulings.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this PR does not change, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**GREEN, ready for review** at `3c58b143eac812d173b4326423c030b65ec63f9a`; `883-adopt-processor-801ef228` -> `dev` (from `46c971fa`; live `dev` `fa6c094b` merges cleanly, no file in common).

- The processor gitlink moves to `801ef228`. `gptp-processor` stays at dev's `1616fc8f` under the maintainer ruling on #883 (option (b)): the lane moved it to `a64be73d` and reverts that move in a new commit, since FPGA-gPTP PR #103 fails the parent's Python idiom gate. #103 changes no `hdl/`, `syn/` or ROM byte, and it rides with the next adoption.
- At this head, on clean clones and the pull_request merge commit: docs.yml 64 steps rc 0, 33 not run with a reason, 0 failing (`check_cpp_idiom.py` and `check_py_idiom.py` included); `check_cpp_idiom.py --selftest` 83 / 83. At `e18c8225`, which differs from this head only in `scripts/check_cpp_idiom.py` and one `TESTING.md` line: rtl-fast's `yosys-elaboration` every step rc 0; the 11 gPTP consumer suites 40,591 checks, 0 failures, each equal to the full sweep's count.
- The full sweep: 65 / 65 suites, 2,192,633 checks, 0 failures (at `6c6706e5`). rtl-fast, rtl and elaborate: every `run:` step rc 0 (at `f58347df`). None of them reads what the later commits change (below).

## Linked Issue / roles

Closes #883
Closes #857
Closes #858
Closes #860
Relates to #495
Relates to #76

Executor: `[A768]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

| Commit | Change |
|---|---|
| `4bf3eb72` | `protocol-processor` `044cb25f` -> `801ef2283ec793e35a2590fc6593c90313a64041` (processor `main`, PRs #218 and #219), a fast-forward of the old pin on the donor's `main`. It also moved `gptp-processor` to `a64be73d`, reverted in `8edfae99` |
| `a89802c8` | Pin-derived records, each through its generator: ROM ledger rows (`ucode.hex` new; `ltn_rom.hex` equal to the old row), pin table, boundary and time-sync diagrams, the gPTP donor links |
| `14834e71`, `f2f3d9f5`, `6c6706e5` | milan_dp crflic `[MRPAPP]` (#860) and `[MVRPLA]` (#857); six processor arms in `crflic-mutants`, the #851 control now two-layer |
| `b46bd9b5` | milan_dp notify `[AIDX]` (#858); four processor arms in `gsi-mutants` |
| `0a707859`, `654b5795`, `8f3735d7` | `check_cpp_idiom.py`: a brace initialiser's commas are its elements, nested up to three braces deep, while a second declarator beside one still counts (#495 row 6758088112, review F1); eight selftest arms |
| `21fcc20a`, `cc8ee337`, `5ab559f0` | Makefile campaign comments (with #495 row 6731336971's line), compliance matrix, 802.1Q traceability, testing guide, suite README |
| `93d371cb`, `f58347df` | The seventeenth resource record through `pp_resource_gate.py record --write`; area budget, finding 234, pin page, changelog |
| `8edfae99` | `gptp-processor` back to `1616fc8f` (the ruling) |
| `f746d659` | The gPTP pin-derived records back at `1616fc8f` through their generators. Every gPTP-only page and the time-sync diagram are byte-identical to dev's; the boundary diagram differs from dev's only in the processor pin |
| `e18c8225` | The changelog, pin page, area budget, finding 234 and the three records' `measured` notes state the adoption as the processor's alone |
| `3c58b143` | The testing guide's `crflic-mutants` row counts six gate mutants (#495 row 6731336971, item 2) |

**The adopted behaviour, by clause, graded on the AX7101 1x1 shape (`endstation_ax7101_1x1_tdm8`).**

| Issue | Clause | Parent test | New pins (`801ef228`, `1616fc8f`) | Old pins (`044cb25f`, `1616fc8f`), the same harness |
|---|---|---|---|---|
| #860 | IEEE 802.1Q-2018 Table 10-3 (VN tx! sN, AN tx! sN, then QA or AA by note 8) and 10.7.6.3 (sJ is JoinIn only with the Registrar IN) | crflic `[MRPAPP]`: each value's first three messages, over the whole run; no VID or Talker Advertise JoinIn while none is registered | Domain New, New, JoinIn (the switch registers it at boot); VID 2 and both Talker Advertises New, New, JoinMt; no JoinIn | Domain and VID 2 `0 1 1` (one New, then JoinIn); 185 VID JoinIns. The Talker Advertise rows pass at both pins |
| #857 | 802.1Q-2018 10.7.9 and Table 10-5 (the LeaveAll machine runs whatever is declared); Milan v1.2 Table 4.3 (leavealltimer 9.5 to 15.5 s) | crflic `[MVRPLA]`, after `[E]`: every probe window closes and every declaration is withdrawn; VID 2 Lv; then an MVRP LeaveAll every 9.5 to 15.5 s after its timer's last start, two at least, none overdue, no VID declared; MSRP with the Domain alone held to the same bounds | MVRP LeaveAlls 13.0 to 14.6 s after their timer's start, MSRP 10.8 to 13.4 s | no MVRP LeaveAll after the withdrawal (3 checks fail); MSRP passes |
| #858 | IEEE 1722.1-2021 Table 7-2 (available_index is ADP's) and 6.2.2.15; Milan v1.2 5.6.3.5 for the cadence | notify `[AIDX]`: READ_DESCRIPTOR(ENTITY) octets 36 to 39 against the last ENTITY_AVAILABLE on the wire, after three advertisements, after ENTITY_DEPARTING, and after the re-enable; every other octet the image's | the descriptor reads the wire's 31, 32 and 33, then 0 after ENTITY_DEPARTING, then 0 and 1 | the descriptor reads 0 against the wire's 31, 32, 33 and 1 (4 checks fail) |

The crflic leg passes 458 / 458 at the new pins and 451 / 458 at the old; the notify leg 535 / 535 and 531 / 535.

**Planted arms (each the processor's own, in a copy of its `hdl/` tree).**

| Campaign | Arm | Named check that fails |
|---|---|---|
| `crflic-mutants` | the Domain declared at LINK_UP in AN | `MSRP Domain {class A, 3, VID 2}: message 2 is New again (AN tx!: sN)` |
| | a VID's first join in AN | `MVRP VID 2: message 2 is New again (AN tx!: sN)` |
| | every VID Join encoded JoinIn | `no MVRP JoinIn in the whole run: no VID was ever registered (10.7.6.3)` |
| | an MVRP drain that needs a pending VID | `MVRP, nothing declared: at least two LeaveAll MRPDUs after the withdrawal` |
| | the MSRP leavealltimer's expiry lost (`leaveall-expiry-lost`) | `MSRP, the Domain alone: at least two LeaveAll MRPDUs after the withdrawal` |
| | the #851 control, now both layers: the intake takes every push twice and the encoder never merges | `no DUT MRPDU carries one attribute value in two VectorAttributes` (591 MRPDUs) |
| `gsi-mutants` | the microcode copies the image's ENTITY descriptor whole | `[AIDX] A1 ...: available_index (octets 36..39) is the wire's`, 4 of 535 |
| | the AECP engine answers 0 for the index gather | the same, 4 of 535 |
| | ADP serves the next frame's index | the same, 5 of 535 |
| | ADP keeps the last index across ENTITY_DEPARTING | `[AIDX] D ...: available_index (octets 36..39) is the wire's`, 1 of 535 |

`crflic-mutants`: 16 / 16 at `6c6706e5`. `gsi-mutants`: 19 / 19 at `21fcc20a`. `unb-mutants`: 6 / 6. Their inputs, the processor's `hdl/` copy and milan_dp's harness, are unchanged since. `dynmap-mutants`: 69 / 71, the two failures its listener leg's clean control and arm in a clone where `tb/verilator/milan_dp_render` had never been built (below); with that suite's inputs built, `dynmap_mutants.py 36` reads 2 / 2.

**The #851 control went vacuous with this pin, and is fixed here.** At `21fcc20a` the arm "the SRP encoder never merges" survived the crflic leg, with 0 values doubled, and with dev's own harness at processor `801ef228` too. Since processor #216 each Applicant decides one message per tx! and each round's drain waits for its tx!, so no value is handed over twice in one window (processor `tb/srp_top/README.md` group onevec). The processor's own end-to-end control removes both layers (`push-twice-encoder-appends`); the parent arm now does the same, its `KL_srp_top.sv` byte-identical to that patch.

**#495 rows.**

| Row | Disposition |
|---|---|
| 6758088112, `check_cpp_idiom.py` counts a brace initialiser as several declarators | Fixed here (`scripts/check_cpp_idiom.py:269-271`): a balanced one-line `{...}` initialiser up to three braces deep is one declarator's text, and a comma beside it still separates declarators (review F1: the first fix read only flat braces, so a second declarator beside a nested initialiser escaped). Eight selftest arms (`:705-712`): one declarator with flat, once-nested and twice-nested braces gives 0; two declarators beside flat, `{1}`-style, once-nested (either order) and twice-nested braces give 1. Dev's pattern planted back fails the three "a brace initialiser's commas separate elements, not declarators (#495)" arms. The tree stays at 0 |
| 6731336971, four wording items | Item 3, the milan_dp Makefile line, is taken (`tb/verilator/milan_dp/Makefile:667-670`). Item 2, `docs/testing/TESTING.md:357`'s gate-mutant count, is taken: "the six gate mutants". Item 1, `docs/reference/SUBMODULES.md:813`, stays open on #495. Item 4 names the route note's old "-5 slices (80)"; that note is rewritten here but keeps the form, now "+29 slices (80)" (`syn/ooc/pp_resource_baseline.json:451`), so it stays open on #495 too |
| 6758048783, processor #216 residue (GAP-19 owner cell, the 10 section 6.2 reflow, GAP-19's LINK_UP half, R802-2 S1 to S3) | Processor files; stays with the processor's next documentation PR |
| 6777009988, FPGA-gPTP #103 residue (`docs/TEST_DEVELOPER.md:60`, a fast order check in `make all`) | FPGA-gPTP files; with the #102 follow-up that #103's next adoption needs |

The twin's owed rows (`fabric-mvrp-leave-all`, `fabric-domain-one-new`, `fabric-vid2-join-in`, `entity-available-index`) are on #665's unmerged branch, not on `dev`: the lane that lands the twin deletes them at this pin.

**Area and timing (acceptance item 4).** Vivado 2026.1, the recipe's flows, at `a89802c8`; the three #818 directives placed from one synthesis checkpoint:

| Directive | WNS / WHS, worst corner | Slow corners WNS / WHS | Fast corners WNS / WHS | LUT | FF | Slice | Free |
|---|---|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt, selected | +0.334 / +0.017 ns | +0.334 / +0.045 | +1.350 / +0.017 | 53,461 | 54,971 | 15,849 | 1 |
| ExtraTimingOpt | +0.218 / +0.036 ns | +0.218 / +0.102 | +1.548 / +0.036 | 53,474 | 54,974 | 15,850 | 0 |
| AltSpreadLogic_high | +0.162 / +0.039 ns | +0.162 / +0.104 | +1.488 / +0.039 | 53,494 | 54,976 | 15,850 | 0 |

Every route completes with no routing error, and every directive meets the +0.030 ns floor at every corner (0 and 85 C, slow and fast). The worst setup path is the SoC's SDRAM controller on its 10 ns clock, on all three. Against `46c971fa` (whose synthesis inputs are #854's record at `7a19f62b`), best against best, both ExtraPostPlacementOpt:

| Figure | `46c971fa` | This head | Change |
|---|---:|---:|---:|
| LUT | 53,534 | 53,461 | -73 |
| FF | 54,850 | 54,971 | +121 |
| Slice of 15,850 | 15,820 | 15,849 | +29 |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 15 | 74 / 27 / 15 | 0 |
| WNS / WHS | +0.166 / +0.032 ns | +0.334 / +0.017 ns | +0.168 / -0.015 ns |

NFR-RES-01's shipping-image accounting: the image must fit the device and the resource gate holds it at its record. Against the sixteenth record the gate passes all three endpoints (route -73 LUT / +121 FF / +29 slices against 500 / 600 / 80; `ooc-1x1` +214 / +64 against 250 / 250; `ooc-8x8` +218 / +66 against 316 / 339). They are re-recorded through `record --write` because the change moves the shipping image; `check-baseline` and `check` exit 0 against the seventeenth record. One slice is left: the next growth has no slice margin.

**The record holds at this head's pins.** `a89802c8` carried gPTP `a64be73d`. An export at `1616fc8f` reads the same 131 files and six ROM images under the gate's own normalisation. The only file that differs, the generated `alinx_ax7101.v`, differs only inside its `/* */` hierarchy comment, where the exporter lists the same black boxes in another order. So that export's `inputs_sha256` differs from the record's while every byte synthesis reads is equal; no re-route is needed (below).

**Gates** (each on a fresh clean clone; workflow jobs on the pull_request merge commit; each rc is the command's own):

| Gate | Command | Head | rc / result |
|---|---|---|---|
| docs.yml, all five jobs | `wire-accountability`, `docs-check-no-git`, `docs-gates-0..2` | `3c58b143` (merge with `fa6c094b`) | 64 steps rc 0, 33 not run with a reason, 0 failing; each job's tree clean after |
| C++ idiom gate | `python3 scripts/check_cpp_idiom.py --selftest`; the tree scan | `3c58b143` | 83 / 83, rc 0; `multi-declarator declaration: 0 <= 0`. Planted back: dev's pattern fails the three brace-initialiser arms, the flat-brace pattern of `e18c8225` the three nested two-declarator arms, a one-level pattern the three-deep arm |
| Python idiom gate | `python3 scripts/check_py_idiom.py` (docs.yml `gate_39`) | `3c58b143` | rc 0: `long module: 10 <= 10`, `unannotated public function: 0 <= 0`, `undocumented public function: 0 <= 0` |
| rtl-fast.yml `yosys-elaboration` (reads the baseline JSON) | its `run:` steps | `e18c8225` (merge with `fa6c094b`) | 7 rc 0, 3 not run with a reason; `baseline PASS: 3 endpoints` |
| The gPTP consumer suites, each its own run | `make -C tb/verilator/<suite>` for capture_coherence, gptp_plane, gptp_shadow, gptp_tables, gptp_txts, milan_dp, milan_dp_gm_steps, milan_dp_mclk, milan_dp_render, pp_shadow, tsn_fuzz; then `python3 scripts/suite_tally.py <logs>` | `e18c8225` | 11 / 11, 40,591 checks, 0 failures; milan_dp's 19 legs PASS (gptp and gptp-lat 212 / 212 each, crflic 458, notify 535); every suite's count equal to the sweep's |
| Pin and doc gates | `check_submodule_docs.py`, `check_gptp_docs.py --with-submodule`, `check_diagram_pngs.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 46c971fa`, `docs_check.py`, `check_doc_paths.py`, `docs_inventory.py --check`, `pp_resource_gate.py check-baseline` | `e18c8225` | 10 / 10 rc 0 |
| `git diff --check` against the merge base | `git diff --check 46c971fa HEAD` | `3c58b143` | rc 0, empty |
| Full sweep, 4 shards | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, then `python3 scripts/suite_tally.py <union> --quiet --expect-suite-root tb/verilator` | `6c6706e5` | rc 0 each; 65 / 65 suites, 2,192,633 checks, 0 failures, 0 timed out |
| rtl-fast.yml, every `run:` step of its 16 jobs | per job | `f58347df` | every step rc 0 (behave 14 features, 508 scenarios, 2,330 steps; lint `89 <= ratchet 89`; census 0 of 31 rules unproven; the four firmware campaigns PASS) |
| rtl.yml | `full-ci-gate`, `yosys-shards` 0..3 of 4, `yosys-portability` | `f58347df` | every step rc 0; Yosys `expected=61 observed=61 errors=0` |
| elaborate.yml | `elaborate-gates-0..4` | `f58347df` | every step rc 0 |
| `test_builder.py --require-rv32` | `python3 sw/builder/test_builder.py --require-rv32` | `f58347df` | rc 0, `ALL GATES PASS EXCEPT 17 NOT RUN` (no LiteX interpreter); with `MILAN_LITEX_PYTHON` rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b: this make does not re-read MAKEFLAGS mid-parse; gate 11: needs a board build's Vivado report) |
| Campaigns | `crflic-mutants`; `gsi-mutants`; `unb-mutants`; `dynmap-mutants`, then `dynmap_mutants.py 36` | `6c6706e5`, `21fcc20a`, `cc8ee337`, `f2f3d9f5` | 16 / 16; 19 / 19; 6 / 6; 69 / 71 (the listener precondition), then 2 / 2 |
| Resource gate | `pp_resource_gate.py check` (three endpoints), `record --write`, `check-baseline`, `check` | route set at `a89802c8` | check rc 0 at all three against the sixteenth record; after re-record `check-baseline` and `check` rc 0 |
| Old pins | crflic and notify with processor `044cb25f`, gPTP `1616fc8f` | lane tests at `21fcc20a` | 7 and 4 failures, each a new check |

Why the earlier rows stand: `3c58b143` differs from `e18c8225` only in `scripts/check_cpp_idiom.py` and one `docs/testing/TESTING.md` line, both read only by docs.yml steps, re-run above at `3c58b143`. After `f58347df` the lane changes the gPTP gitlink, doc pages, diagrams and the baseline JSON's notes. The gPTP tree's two pins differ only in its `docs/TEST_DEVELOPER.md`, `tb/mutation_jobs_test.py`, `tb/verilator/engine/Makefile` and `mutants.py`; its `hdl/` and `syn/` are equal. Every parent gate that reads a submodule's `docs/` or `tb/` is a docs.yml step; the suites that read the gPTP tree are the 11 re-run above, found from their builds' dependency files and logs; the one rtl-fast job that reads the baseline JSON is re-run above.

## Authoritative references

- IEEE 802.1Q-2018 10.7.6.3, 10.7.7 and Table 10-3, 10.7.9 and Table 10-5, Table 10-4.
- IEEE 1722.1-2021 Table 7-2, 6.2.2.15.
- Milan v1.2 4.2.7.1.1 and Table 4.3; 5.6.3.5.2, 5.6.3.5.5, 5.6.3.5.9.
- Processor PRs #218 (#216) and #219 (#217) and their merge rulings; FPGA-gPTP PR #103 (#102), not adopted here.
- The #883 ruling on the FPGA-gPTP pin, option (b): issuecomment-6805166676.
- #857, #858, #860; #495 rows 6758048783, 6758088112, 6777009988, 6731336971.
- NFR-RES-01; `docs/design/AREA_BUDGET.md`; `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`; the maintainer decision of 2026-11-06 (not needed: the gate passes).

## How to get into the same state

Set `REPO` to the candidate checkout. Point `VERILATOR`, `MAKE43_BIN`, `RV32_SDK`, `LITEX_PYTHON`, `GTEST_1_14` and `VIVADO_BIN` at the local dependencies. Before any command inside a submodule, check its own top-level directory.

```sh
cd "$REPO"
git remote get-url origin
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
test "$(git -C gptp-processor rev-parse --show-toplevel)" = "$PWD/gptp-processor"
git submodule status protocol-processor gptp-processor
python3 scripts/ci_rv32_sdk.py --destination "$RV32_SDK"
export VERILATOR PYTHONHASHSEED=0
export MILAN_RV32_CC="$RV32_SDK/bin/riscv32-linux-gcc"
export PKG_CONFIG_PATH="$GTEST_1_14/lib/pkgconfig" LD_LIBRARY_PATH="$GTEST_1_14/lib"
export PATH="$MAKE43_BIN:$VIVADO_BIN:$PATH"
```

The expected state: origin the project's `milan-fpga` repository, head `3c58b143eac812d173b4326423c030b65ec63f9a`, processor `801ef2283ec793e35a2590fc6593c90313a64041`, gPTP `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, GNU Make 4.3, Verilator 5.050, Yosys 0.66, sv2v v0.0.12.

## How to validate

```sh
make -C tb/verilator/milan_dp crflic
make -C tb/verilator/milan_dp notify
make -C tb/verilator/milan_dp crflic-mutants
make -C tb/verilator/milan_dp gsi-mutants
python3 scripts/check_cpp_idiom.py --selftest
python3 scripts/check_py_idiom.py
python3 syn/ooc/pp_resource_gate.py check-baseline
bash syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code syn/yosys/rom_digests.tsv
python3 scripts/check_submodule_docs.py
python3 scripts/check_gptp_docs.py --with-submodule
python3 scripts/docs_inventory.py --check
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs" --wait
python3 scripts/suite_tally.py "$suite_logs" --quiet --expect-suite-root tb/verilator
(cd tests && behave --no-capture -f plain)
python3 sw/builder/test_builder.py --require-rv32
git diff --check "$(git merge-base origin/dev HEAD)" HEAD
```

Expected result / pass criteria: every command exits 0. The crflic leg reads `checks: 458   failures: 0`, the notify leg `checks: 535   failures: 0`, `crflic-mutants` `16 checks: 16 PASS, 0 FAIL`, `gsi-mutants` `19 checks: 19 PASS, 0 FAIL`; `check_py_idiom.py` reports `long module: 10 <= 10` and 0 unannotated and 0 undocumented public functions; `ooc.sh --record-rom-digests` leaves the ledger unchanged.

## Known limitations / out of scope

- **FPGA-gPTP PR #103 is not adopted here** (the #883 ruling). Its next adoption needs a small FPGA-gPTP follow-up under #102: annotate `named_verdict`, `run_mutant`, `in_list_order` and `planted` in `tb/verilator/engine/mutants.py`; document `control`, `planted`, `task` and `tb/mutation_jobs_test.py`'s `main`; bring `mutants.py` (1080 lines) to 1,000 or fewer. The parent ratchet is not raised.
- **The ROM ledger keeps `a64be73d`'s row.** `syn/yosys/rom_digests.tsv` gained a `gptp_ucode.hex` row for `a64be73d` at `a89802c8`, equal to the `1616fc8f` row. The generator keeps every other pin's rows by design, so re-recording at `1616fc8f` leaves it; it stays true, and the next gPTP adoption records its own row beside it.
- **`dynmap-mutants` on a fresh clone (pre-existing, its own issue).** Its listener leg builds in `tb/verilator/milan_dp_render` with `ltn_rom.hex`, `ucode.hex` and `tdm8r_aemi.bin` marked as inputs the build may not remake, and the campaign target never builds them. Where that suite was never built, its clean control runs without them and fails.
- **The resource gate's input digest depends on a comment's order (pre-existing, its own issue).** `inputs()` strips `//` comments from generated files but not the exporter's `/* */` hierarchy listing, whose black-box order follows object addresses. A fresh export of unchanged sources can digest differently, as the export at this head's pins does.
- **Hosted milan_dp leg windows.** No case is added, so no leg is re-dealt (#804). The crflic case simulates 3.6 M more cycles (+20.6 %) and the notify case about 3 M more; `PIECE_SECONDS` keeps its hosted figures until a hosted run re-measures them.
- **Slice margin.** The selected route leaves 1 of 15,850 slices; Mark II (#640) recovers area.
- The physical qualification on the built image (#839, #396 and the in-house runs) needs the image and a bench; nothing here touches hardware.
- `docs/spec-refs.md` does not exist in this tree; the clauses were read from the standards' text.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
