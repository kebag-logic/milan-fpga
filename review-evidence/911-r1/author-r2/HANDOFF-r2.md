# #911 A782 round 2 handoff (answers R841-1 and R842-1 on PR #913)

Status: REVIEW READY round 2 at 8e523a2b (every finding answered; one clean-clone gate pass green at this head).

- Lane: branch `911-ax7a200t-variant`, PR #913 to dev, base b7d69295. Round-1 head 4958ca4f; round-2 head
  **8e523a2b17faf17c4564e5af155b73f95dc2a0a5** (six commits, all one-line subjects, no trailers). Not pushed.
- TAKEN round 2: issuecomment-6881490425. REVIEW READY round 2: issuecomment-6883755663.
- Reviews answered: R841-1 (issuecomment-6881465909) F1-F5 and RS1; R842-1 (issuecomment-6881181571) F1 and R1. Both
  reports read in full (the comment bodies are the REPORT.md files on 911-review-evidence, same bytes).
- Image set: unchanged (round 1's handover/, image commit 1e604e1b). No gateware input changed: see "Gateware inputs".
- Receipts: round2/receipts/ (index: receipts/INDEX.md). Scratch: /data-2/milan/tmp/911-a782/r2 (clones E, mut,
  full/lane-wt; elab/; vivado/; guide/). buildC is kept.

## Commits (b7d69295..8e523a2b adds these six to round 1's ten)

1. `9903f6b2` Scope the 4 MiB slot and AEM at 4 MiB to the AX7101 (BUILDING.md, BAREMETAL_FIRMWARE.md, QSPI caveat,
   build.sh comment), give the 200T's 10 MiB / 0xA00000, name BUILD_DIES.
2. `fa05b4ca` Gate 1e: a 200T image set on its own map through `build.sh flash ax7a200t`; `test_layout_from_soch`.
3. `0b6bae19` check-board refuses any multi-device JTAG chain; gate 1e plants two JEDEC IDs and two-device chains.
4. `630189f8` Guide and QSPI page: pre-#911 layouts refused, what to do, stub-only board check; Digilent FT232H.
5. `6ae7d976` deploy.sh's first board-check refusal names the layout or the die (it said "the FPGA" for both).
6. `8e523a2b` This branch's prose on BUILDING.md, BAREMETAL_FIRMWARE.md and the QSPI page held to check_doc_style's
   limits (those pages are not on the gate's list; the instruction asks for every touched page): a table and short
   sentences, the pre-existing sentences restored, the 200T AEM caveat its own bullet.

## Findings and dispositions

| finding | disposition | file:line at 8e523a2b | mutant -> failing words | receipt |
|---|---|---|---|---|
| R842-1-F1 (MINOR, Conformance+Docs) | Fixed at the cause: every universal 4 MiB statement scoped to the AX7101 and the 200T's layout-derived 10 MiB / 0xA00000 given, with the authority (`FLASHBOOT_BITSTREAM_SLOT` + `layout_for()`, QSPI page section). Firmware-in-ROM and 64 KiB AEM kept. The same universal claim was also in BAREMETAL_FIRMWARE.md's slot table (now labelled the AX7101's, the 200T's offsets below it), the QSPI page's AEM caveat (a 200T bullet beside it) and build.sh's board comment: all three scoped. BUILDING.md gives both dies as a table. | `docs/integration/BUILDING.md:472-491` (a table of both dies); `docs/integration/BAREMETAL_FIRMWARE.md:103-108`; `docs/integration/QSPI_FLASHBOOT.md:252` (caveat bullet); `sw/litex/build.sh:61-64` | docs (no mutant) | `receipts/building-vs-load_map.txt` (the paragraph beside `flash_map.load_map()` for both dies and the guide's generated table) |
| R842-1-R1 (RESIDUE) | Fixed: `BUILD_PARTS` -> `BUILD_DIES` (`scripts/check_sweep_shape.py:73`). | `docs/integration/BUILDING.md:312`, `:363` | -- | `git grep BUILD_PARTS` empty |
| R841-1-F1 (MINOR, Tests) | Fixed. (a) Gate 1e's 200T arm now builds its image sets on the 200T map: `on_200t()` gives the bit part 7a200tfbg484 and a 9,730,652-B payload, and the layout a bitstream budget and AEM offset of 0xA00000; `reset_flash` loads each set's own AEM offset. `build.sh flash ax7a200t` must write `[0xA00000, 0]`, and the fake flash must hold the target payload at 0 and its AEM at 0xA00000. (b) `test_layout_from_soch` (run by `test_timing_grade.py` and the builder gate `test_commercial_timing_grade`): for each die the SoC's own `_add_flashboot_constants` plus the other soc.h constants are rendered by LiteX's `get_soc_header`; `layout_from_soch.main()` must rebuild exactly the SoC's exported image rows (budget = AEM offset = 0x400000 / 0xA00000), the N25Q128A13 and 0x20BA18; the rebuilt 200T layout must pass `validate_artifact_pair` with a 9,730,652-B payload. | `sw/builder/test_builder.py:18779,18822,19125-19169`; `sw/builder/test_timing_grade.py:216-274,313`; `sw/builder/test_builder.py:29548,29564` | **K7** (reviewer's exact anchor, `layout_from_soch.py` budget -> `0x40_0000`): `test_timing_grade.py` rc 1 and builder gate `test_commercial_timing_grade` rc 1, `AssertionError: ('xc7a200t-fbg484-2', [{'name': 'bitstream', 'offset': 0, 'addr': 0, 'budget': 4194304}, {'name': 'aem', 'offset': 10485760, ...}])` (gate 1e rc 0: it has no LiteX). **K9** (reviewer's exact anchor, deploy budget capped at 4 MiB): gate 1e rc 1 with `qspi owner transition REFUSED: installed bitstream payload 9730652 B exceeds 4194304 B slot` in the failing `flash-pair [ax7a200t]` assertion; `test_timing_grade.py` and the builder gate rc 1, `TransitionError: artifact bitstream payload 9730652 B exceeds 4194304 B slot`. Control **C2** (the 200T arm expecting 0x400000): gate 1e rc 1, `AssertionError: [(1, 10485760, 'verify', 'aem.fbi'), (2, 0, 'verify', 'target.bit')]`. | `receipts/mutants/K3-K4-K7-K9-at-head.txt`, `receipts/mutants/K9-words-C1-C2-at-head.txt`; the real 200T soc.h: `receipts/layout-from-soch/compare.txt` |
| R841-1-F2 (MINOR, Conformance+Docs) | (a) The guide's "Update a flashed board" step now has rc 0 receipts on two valid 200T image sets: D (the delivered set with one payload byte flipped and its layout rebound; no second 200T build with another payload exists) -> R (the delivered set) and back, through `INSTALLED_BUILD=<set> sw/litex/build.sh flash ax7a200t:<set>` against the stub programmer: rc 0, stub calls `--detect`, `--detect -f --verbose`, dump 9,730,652 B, write at 10485760 (AEM), then the bit; readback holds the payload at 0 and aem_desc.bin at 0xa00000. Round 1's step 11 was the expected refusal of a compressed build on the 4 MiB map, which its own layout refuses (now stated as that). (b) Acceptance-4 statement corrected in PR-BODY.md. (c) AX7101 comparisons: the AX7101 release's own reports (b7d69295, ExtraPostPlacementOpt) are published beside build C's and compared by script: 16 clock pairs with identical endpoint counts, classification and inter-clock constraint; CDC rules, severities and counts identical (CDC-10 10, CDC-15 199, CDC-26 121, CDC-6 52, ...); 113 used pins identical in signal, pin name, use, I/O standard and bank. The XDC is byte-identical between the dies (identity receipts). | PR-BODY.md "Results"/"Guide run" | -- | `receipts/guide-run/02-*`, `03-*` (+ `.flash.txt`, `stub-calls.log`); `receipts/ax7101-vs-200t.md`, `receipts/ax7101-release/*`, `receipts/buildC-release/*` |
| R841-1-F3 (MINOR, Conformance+Docs) | Fixed. Guide section "The board check" and "Image sets built before #911": (a) a layout without `flash_device`/`flash_jedec_id` is refused as a target on `flash`, `flash-images`, `flash-pair`, and still serves as `INSTALLED_BUILD`; (b) rebuild, or regenerate the layout from the build directory's `soc.h` with `layout_from_soch.py` (command given; a delivered set has no soc.h), or the plain JTAG commands with `P` and `O` set by hand from the variant table (the layout snippet cannot read a flash ID from such a layout); (c) the die and flash ID check has run only against a stub programmer, no bench run recorded on either board. The QSPI page states the AX7101 layout gains the two fields, the check runs on both boards, the refusal, and the stub-only status, and links the guide section. Found while receipting (a): deploy.sh's first refusal line said "the FPGA on the cable is not the image set's part" when the layout named no flash device; it now names both causes (commit 5). | `docs/guides/BOARD_DEPLOYMENT.md:17,309-345`; `docs/integration/QSPI_FLASHBOOT.md:89-107`; `sw/litex/deploy.sh:247-251` | docs; the refusal arms stay in gate 1e (`a layout naming no flash device`) | `receipts/guide-run/04-*` (the snippet on an old layout: KeyError, empty values), `05-*` (old AX7101 release set as target: rc 2, one `--detect` and nothing else), `06-*` (layout_from_soch on the release build's soc.h: adds exactly `flash_device`/`flash_jedec_id`; `X-layout-diff.txt`), `07-*` (old installed set -> regenerated target: rc 0, AEM at 0x400000 then bit) |
| R841-1-F4 (SUGGESTION, taken) | Fixed. The fake programmer prints a second chain device (`OFL_MODEL2`) and a second ID line in the `JEDEC ID: 0x` form (`OFL_JEDEC2`). Gate 1e plants two disagreeing IDs, an XC7A100T + XC7A200T chain and two XC7A100T devices, on flash-pair, flash and flash-images; each is refused before any dump or write (die arms: before the bridge). check-board counted distinct models (a set), so a chain of two equal dies passed; it now counts one entry per device. | `sw/builder/test_builder.py:18669-18683,19105-19112`; `sw/litex/qspi_owner_transition.py:334-341` | **K3**: gate 1e rc 1, `AssertionError: two disagreeing JEDEC IDs in the flash read flash-pair: accepted`. **K4**: gate 1e rc 1, `AssertionError: an XC7A100T and an XC7A200T on one chain flash-pair: accepted`. **C1** (back to round 1's set): gate 1e rc 1, `AssertionError: two XC7A100T devices on one chain flash-pair: accepted`. | `receipts/mutants/*` |
| R841-1-F5 (SUGGESTION, taken) | Done, no rebuild: build C's routed checkpoint (written after post-route phys_opt, `Design State: Physopt postRoute`) opened in Vivado 2026.1 batch (slot wrapper, taskset 96-127, maxThreads 8, rc 0); the image commit's `kl_timing_grade_configure` with build C's arguments; per corner and Tj the raw `report_timing_summary -delay_type min_max -report_unconstrained -no_detailed_paths` and `report_operating_conditions`; `report_cdc` and `report_cdc -details`. Design Timing Summary rows: Slow 0/85 C WNS 0.174 WHS 0.102; Fast 0/85 C WNS 1.633 WHS 0.036; TNS/THS 0, 0 failing endpoints, WPWS 0.264. `report_cdc -details` equals the signoff CDC report below its header. The 1.3 MB signoff per-corner reports are over the receipt limit: their sizes and sha256 are listed. | -- | -- | `receipts/vivado-buildC-route/*` (RUN.txt, reports.tcl, 5 timing summaries, 4 operating, 2 CDC) |
| R841-1-RS1 (RESIDUE) | Fixed: "The JTAG cable is a Digilent FT232H." PR-BODY.md has no "onboard". | `docs/guides/BOARD_DEPLOYMENT.md:394` | -- | -- |

## New checks (planted mutant -> failing words), all at 8e523a2b on a clean clone (receipts/mutants/)

- Baseline: gate 1e, `test_timing_grade.py <litex python>`, builder gate `test_commercial_timing_grade`: rc 0.
- K3 `if len(ids) != 1:` -> `if not ids:`: gate 1e rc 1 `two disagreeing JEDEC IDs in the flash read flash-pair: accepted`.
- K4 `if len(models) != 1:` -> `if not models:`: gate 1e rc 1 `an XC7A100T and an XC7A200T on one chain flash-pair: accepted`.
- K7 layout_from_soch budget -> `0x40_0000`: test_timing_grade rc 1 and test_commercial_timing_grade rc 1,
  `AssertionError: ('xc7a200t-fbg484-2', [{'name': 'bitstream', ..., 'budget': 4194304}, {'name': 'aem', 'offset': 10485760, ...}])`.
- K9 deploy budget `min(..., 0x40_0000)`: gate 1e rc 1 (`installed bitstream payload 9730652 B exceeds 4194304 B slot`),
  test_timing_grade and test_commercial_timing_grade rc 1 (`artifact bitstream payload 9730652 B exceeds 4194304 B slot`).
- C1 chain count back to a set: gate 1e rc 1 `two XC7A100T devices on one chain flash-pair: accepted`.
- C2 200T arm expects 0x400000: gate 1e rc 1 `AssertionError: [(1, 10485760, 'verify', 'aem.fbi'), (2, 0, 'verify', 'target.bit')]`.
- The clone was restored and checked clean after each.

## Gateware inputs unchanged (receipts/identity/)

One clone path, one output path, no Vivado; build inputs = every file the generated Tcl reads (read_verilog /
read_xdc / source), every file of its -include_dirs, and the Verilog's $readmemh init files; the generated Verilog is
compared by body (LiteX's date stamps and its "Hierarchy" comment, whose order differs between any two elaborations of
one commit, aside).

- `build.sh ax7a200t`: 1e604e1b vs 8e523a2b: 3,875 outputs, identical apart from generated-on stamps; 150 inputs,
  list sha256 b77eb73a76bf9acc both. Build C's own Tcl inputs hashed in its clone: the same list (b77eb73a76bf9acc);
  build C's Verilog body, xdc, rom/mem/sram init, Tcl (clone path and the thread cap aside), aem_desc.bin, soc.h:
  identical to the head's.
- `build.sh ax7101`: 1e604e1b vs 8e523a2b: identical (150 inputs, 0e0d547eb2935460 both). b7d69295 vs 8e523a2b:
  150 inputs identical; outputs identical but `flashboot_layout.json`, which adds exactly `flash_device` and
  `flash_jedec_id` (every other key equal): the stated #911 change.
- So the delivered image set stands; no re-route.

## Resource and route timing (build C, image commit 1e604e1b; unchanged from round 1)

| corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|
| Slow 0 C / 85 C | +0.174 | 0.000 | +0.102 | 0.000 |
| Fast 0 C / 85 C | +1.633 | 0.000 | +0.036 | 0.000 |

WPWS +0.264. Raw Vivado rows: receipts/vivado-buildC-route/. Utilisation (xc7a200t-fbg484-2): LUT 53,590/133,800
(40.05 %), FF 54,971 (20.54 %), slices 19,672 (58.81 %), BRAM 87.5/365, DSP 15/740, IOB 109/285 (round-1
receipts/buildC-release/buildC-release-utilization_place.rpt).

## Gate table (head 8e523a2b17faf17c4564e5af155b73f95dc2a0a5, clean clones; receipts/gates/)

| Gate | Result |
|---|---|
| rtl-fast.yml, rtl.yml, docs.yml, elaborate.yml: every `run:` step of every job a pull_request to dev runs (ci_scope rtl=true), each job on a fresh clone of the head | 150 steps rc 0, 522 not run with a stated reason (gates/not_run.json), 0 bad: `verify_wf.py` rc 0 (gates/workflow-steps.md). Per workflow ran / not run: rtl-fast 44 / 55, rtl 21 / 366, docs 62 / 35, elaborate 23 / 66. All 30 job clones clean afterwards. |
| rtl.yml verilator-shards (19 hosted workers) | Not run: no RTL or testbench change this round; the full sweep passed 65/65 at the round-1 head 4958ca4f (round-1 receipts gates/sweep.txt); the instruction does not ask for it. |
| docs-gates-1 builder leg 0 (gate_25_0) | rc 0 at 8e523a2b on the first run. In the superseded 6ae7d976 pass it first failed, environmental: the runner HOME lacked the `br-milan-rv32` SDK link the hosted job provisions (round 1's runner HOME had it), so `--require-rv32` refused; with the link the rerun passed (gates/superseded-6ae7d976/). |
| elaborate-gates-2 LiteX sim leg | rc 0 on the first run this round. |
| `git diff --check b7d69295 HEAD` | rc 0 |
| `scripts/docs_inventory.py --check` | rc 0 |
| docs gates: check_doc_style (+ --selftest; its list holds BOARD_DEPLOYMENT.md, DOCUMENTATION_AUDIT.md and diagrams/README.md of the touched pages), check_doc_paths, docs_check, gen_toc --check / --verify-anchors, check_em_dash --base b7d69295, check_solution_docs (+ --selftest) | rc 0 each (lane gates and docs-gates-0) |
| check_doc_style's own analysis on every touched page (BUILDING.md, BAREMETAL_FIRMWARE.md and QSPI_FLASHBOOT.md are not on its list), counted on this branch's sentences | 0 findings (doc-style-touched.txt; scripts/doc_style_touched.py.txt) |
| lane: check_sweep_shape (+ --self-test), check_deploy_shape (+ --selftest), board_variants (+ --selftest, --layout on the handover set), check_py_idiom, check_sh_idiom, test_timing_grade.py, builder gate test_commercial_timing_grade, gate 1e, build.sh ax7a200t / ax7101 --dry-run, flash_map.py, tree clean after | 27 gates rc 0 (gates/lane-gates.txt) |
| mutants K3, K4, K7, K9 + controls C1, C2 at the head | each red as listed above, baseline green, clone restored clean (mutants/) |

CPU: each unit on an 8-wide range from `cpu_ranges.py pick` (0-95), 4 at once plus the docs-gates-1 rerun, MemoryMax
10G each, MemAvailable 45-54 GB throughout; elaborations, mutants and the guide run in the session on 96-127; the one
Vivado run through the slot wrapper on 96-127 with maxThreads 8.

## Observations (not changed here)

- `layout_from_soch.py` writes no `reserved`, `flash_size` or `erase_block` (pre-existing, the sweep path). The
  deploy write ceilings still stop below the journal: the AEM write is bounded by its 64 KiB budget from soc.h.
- `docs/integration/BAREMETAL_FIRMWARE.md`'s slot table still lists the journal slots as "read and written" by the
  firmware, while QSPI_FLASHBOOT.md says nothing reads or writes them since 2026-08-13: pre-existing, needs its own
  issue.
- `qspi_owner_transition.py --self-test` NameError: pre-existing, #912.

## Log
- 18:30 start; 18:35 TAKEN round 2; 18:37 Vivado reports queued (first run refused `-max_paths` with
  `-no_detailed_paths`; 18:47 rerun rc 0).
- 18:40-18:55 docs, gate 1e, test_layout_from_soch; commits 1-4; 18:56 mutants (630189f8); 18:58 guide run found the
  refusal wording; commit 5 (6ae7d976).
- 19:01 gate pass dispatched (19 units, 4 at once, CPU ranges from cpu_ranges.py pick); 19:02-19:20 identity
  elaborations; mutants, extra controls and the guide run repeated at 6ae7d976.
- 19:32 docs-gates-1 gate_25_0 refused --require-rv32 (runner HOME without the SDK link); link added, rerun 19:33-19:54
  rc 0.
- 20:09 6ae7d976 pass done: verify_wf 150 rc 0 / 522 not run / 0 bad (superseded).
- 20:10 check_doc_style's analysis over every touched page found this branch's long sentences on three pages off its
  list; rewritten (commit 6, 8e523a2b); 20:13 the full pass relaunched at 8e523a2b; identity, mutants, controls,
  guide run and the soc.h rebuild repeated at 8e523a2b.
- 21:28 8e523a2b pass done: verify_wf 150 rc 0 / 522 not run / 0 bad; receipts published; REVIEW READY round 2 posted.
