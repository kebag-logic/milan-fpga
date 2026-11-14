# #911 A782 handoff (XC7A200T variant: release image + integrator docs)

Status: REVIEW READY. Image set delivered (handover/); final gate pass at head 4958ca4f green.

- Lane: branch `911-ax7a200t-variant` from dev b7d69295. TAKEN posted (issuecomment-6876945749).
- Scope changes applied: issuecomment-6876968816 (kit cancelled; docs + deploy.sh + handover dir) and
  issuecomment-6877123911 (BOARD_DEPLOYMENT.md "Flash an image set over JTAG", INSTALLED_BUILD defined).
- Image commit: 1e604e1b (build C). Final head: 4958ca4f. The commits after 1e604e1b add tests, move the table
  check into its own module and fix idiom findings. At 4958ca4f the 200T's gateware inputs are byte-identical to
  build C's and the AX7101's to b7d69295's (receipts/final-head-inputs.txt); the README's guide links at 1e604e1b
  are complete there (the one later guide edit names the new checker script).
- Scratch: /data-2/milan/tmp/911-a782 (clones A B C E; buildA buildB buildC; full/ the gate pass; units/).

## Deliverables
- `handover/`: `gateware/alinx_ax7101.bit`, `aem_desc.bin`, `flashboot_layout.json` (the image set in the layout the
  guide names), `SHA256SUMS`, `README.md` (13 lines: commit, the two guide links at 1e604e1b, untested-on-silicon
  statement, the three things to confirm). 9.4 MB. (The bitstream is over the 200 KB receipt limit by nature; the
  manager's handover instruction requires the image set here.)
- SHA256SUMS:
  - `b7d7dc4ec9ce9254a089fc99d6699d13eba1b8271ed889d000bded46be64954f  gateware/alinx_ax7101.bit` (9,730,856 B; payload
    9,730,652 B, payload sha256 095a7963560a36e21e0154f5ccb7da99ab67c18ff9731216fdbba95f8dfb6c90, header part 7a200tfbg484)
  - `bdfde7cf448ed032ffb1663b0898aeef9ded3bb11b4ead5dc36dfa3df873f180  aem_desc.bin` (7,512 B)
  - `73c2d40e3f3d6ae122b93b71b896abdf75a2f75e9014411b84dced32289a1837  flashboot_layout.json` (916 B)
- No `.bin`: the ax7101 platform writes none (the layout-bound `.bit` is what deploy.sh and openFPGALoader write).
- `receipts/` (index: receipts/INDEX.md), `PR-BODY.md`.

## Changes (file:line, reason)
- `sw/litex/build.sh:384` `cfg_ax7a200t` = `$(cfg_ax7101) --fpga-part xc7a200t-fbg484-2` (derived, not restated);
  `:197` recipe_config binds it to the 1x1 TDM8 YAML; `:71` board_facts programmer part xc7a200tfbg484 (flash path);
  gptp_owner_for_config fabric.
- `sw/litex/platforms/ax7101_timing.py:24` `BOARD_PARTS`; `:27` `board_part()` (refuses another part); `:44`
  `configure_commands(part)` (the timing grade's part check follows the die).
- `sw/litex/platforms/alinx_ax7101.py:301,308` `Platform(part=)`: one platform file, its pins and constraints for both.
- `sw/litex/milan_soc.py:4029` `--fpga-part` (choices BOARD_PARTS; refused with --board arty); `:156`
  `FLASHBOOT_BITSTREAM_SLOT` (the one number: 10 MiB for the 200T); `:159` `flashboot_layout(part)`;
  `_add_flashboot_constants` uses the platform's layout and records `flash_device` (`:3879`) and `flash_jedec_id`
  (`:194` `flash_jedec_id()`, from the litespi module the SoC drives); `:4614` `MILAN_AEM_FLASH_OFFSET` from the die's
  layout (the constant the firmware reads).
- `sw/litex/flash_map.py:55` `layout_for()` (the slot rule, stated once; milan_soc and the diagram call it); `:68`
  `load_map(part)`.
- `sw/litex/layout_from_soch.py:66` `_flash_device()` (soc.h SPIFLASH_MODULE_NAME -> litespi JEDEC); `:108` bitstream
  budget = the compiled AEM offset (4 MiB / 10 MiB).
- `sw/litex/qspi_owner_transition.py:290,294,300,316` `check-board`: die from the `--detect` model line, JEDEC ID from
  `--detect -f --verbose`, refusing a die other than the bitstream's, a flash other than the layout's, unreadable
  output, and a layout naming no flash device.
- `sw/litex/deploy.sh:223,235` `run_detect`, `prove_board`, called before the first dump or write of `flash`,
  `flash-images` and `flash-pair`; usage documents FPGA_PART and the check.
- `scripts/check_sweep_shape.py:67,73,468` BUILD_CFGS + BUILD_DIES (the die joins the config's expected emission, so
  the flag-for-flag comparison grades it; the file stays at the 1000-line limit); plants `:124,:126`.
- `scripts/board_variants.py:81,115,132,152,169` (new) the guide's variant table derived from build.sh's board facts
  and recipe, FLASHBOOT_LAYOUT/FLASHBOOT_BITSTREAM_SLOT through `flash_map.layout_for()`, and the SoC's flash module;
  `--layout <recipe> <json>` checks a built layout, `--write` regenerates the block. check_solution_docs.py is back
  at b7d69295 (it was at the 1000-line limit).
- `sw/builder/test_builder.py:18663,19067,19112` gate 1e: fake programmer answers `--detect`; refusal arms on all
  three paths; `on_200t()` and `run_pair(named=<recipe>)`: the 200T named flash-pair path succeeds on a 200T die and
  refuses on the AX7101's. `:25536` gate 24d's anchor follows `Platform(part=args.fpga_part)`.
- `sw/builder/test_timing_grade.py:166,216` `test_board_parts`, `test_board_variant_docs` (both called from builder
  gate test_commercial_timing_grade).
- `docs/diagrams/flash_layout.gen.py:53,59` one map per die (`flash_layout_xc7a200t.*` generated beside), drawn by
  mutating the module's containers in place (no `global`).
- Docs: `docs/guides/BOARD_DEPLOYMENT.md` (variant table, "Flash an image set over JTAG", INSTALLED_BUILD, FPGA_PART,
  "What is untested on the XC7A200T"), `docs/integration/QSPI_FLASHBOOT.md` ("The XC7A200T variant", contents
  separator `--` per the em-dash gate), `docs/integration/BUILDING.md` (`ax7a200t` section, "Adding a configuration"
  item 4), `docs/diagrams/README.md`, `docs/DOCUMENTATION_AUDIT.md` (regenerated).

## New checks (planted mutant -> failing words)
- shape gate plants: "cfg_ax7101 gains the XC7A200T die" -> `cfg_ax7101: design flag --fpga-part:`;
  "cfg_ax7a200t loses its die" -> `cfg_ax7a200t: design flag --fpga-part:` (self-test rc 0).
- gate 1e (receipts/mutants/gate1e-final.txt, re-run after the helper refactor), each rc 1:
  - M1 die check before the bridge removed -> `XC7A200T on the cable flash-pair: loaded the bridge`
  - M2 JEDEC comparison removed -> `a 256 Mbit flash on the board flash-pair: accepted`
  - M3 `flash` skips the board proof -> `XC7A200T on the cable flash: accepted`
  - M4 layout flash-device requirement removed -> `a layout naming no flash device flash-pair: no 'names no flash device'`
- test_board_parts (receipts/mutants/timing-grade-probe.txt), each rc 1:
  - P1 200T slot entry removed -> `KeyError: 'xc7a200t-fbg484-2'`
  - P2 platform ignores the part -> `AssertionError: xc7a100t-fgg484-2`
  - P3 constants ignore the die -> `AssertionError: ('xc7a200t-fbg484-2', {... 'MILAN_FLASHBOOT_AEM_OFFSET': 4194304`
  - P4 unknown part accepted -> `AssertionError: xc7a35t-fgg484-2 accepted`
- board_variants.py --selftest, 6 controls, each -> `board flash variant table differs from source`: guide variant
  part, variant programmer part (board_facts), variant die (cfg_ax7a200t), variant bitstream slot
  (FLASHBOOT_BITSTREAM_SLOT), entity model offset (FLASHBOOT_LAYOUT), board flash module (milan_soc.py).

## QSPI decision
- Compression tried first. AX7101 b7d69295 route compressed: 3,230,930 B (3,825,992 uncompressed).
- Build A (6b69129a, 200T compressed, AEM at 0x400000): payload 5,566,832 B, over the 4,194,304-B slot by 1,372,528 B.
  So no compression; the region moves for the 200T only: bitstream 0x000000..0x9FFFFF (10 MiB), AEM 0xA00000 (64 KiB),
  journal/user unchanged. The uncompressed 200T payload is 9,730,652 B for any design: 755,108 B margin.
- Flash: the AX7101 design assumes the N25Q128A13 (litespi), 16 MiB, JEDEC 0x20BA18. Vivado 2026.1 has no n25q128
  entry; its successor mt25ql128-spi-x1_x2_x4 (receipts/cfgmem). The guide's `write_cfgmem` ran on the handover set
  (rc 0; 10,493,272 B; payload at 0, AEM at 0xa00000).

## 200T release route (build C at 1e604e1b; receipts/buildC-release)
- Recipe: `build.sh ax7a200t` launch line, flow AreaOptimized_high / ExploreArea / ExtraPostPlacementOpt, phys_opt and
  route AggressiveExplore (--timing-opt), Vivado 2026.1, maxThreads 8 (deviation from the 32 of build.sh: author
  pool), PYTHONHASHSEED=0. First route met the floor, so no #818 directive set was needed.
- Signoff (commercial grade, Tj 0 and 85 C, both models):

  | corner | WNS ns | TNS ns | WHS ns | THS ns |
  |---|---:|---:|---:|---:|
  | Slow 0 C / 85 C | +0.174 | 0.000 | +0.102 | 0.000 |
  | Fast 0 C / 85 C | +1.633 | 0.000 | +0.036 | 0.000 |

  WPWS +0.264. Floor +0.030 WNS / 0 WHS met at every corner. (AX7101 release b7d69295 eppo: Slow +0.334/+0.045, Fast
  +1.350/+0.017.)
- Utilisation (xc7a200t-fbg484-2): LUT 53,590/133,800 (40.05 %), LUTRAM 3,826, FF 54,971 (20.54 %), slices
  19,672/33,450 (58.81 %), BRAM 87.5/365, DSP 15/740, IOB 109/285, BUFG 11, MMCM 1, PLL 2. 0 routing errors.
- check_timing: 0 no_clock, 0 unconstrained internal endpoints, 0 loops; 46 inputs and 87 outputs without I/O delay,
  all under false paths (same counts as the AX7101 release). Clock interaction and CDC categories as the AX7101 release
  (CDC-10 Critical 10, CDC-15 199, CDC-26 121, CDC-6 52, ...: the same design, not new).
- I/O: 113 used pins identical to the AX7101 release in pin name, bank, I/O standard and use; banks 13-16 LVCMOS33,
  34/35 SSTL15/DIFF_SSTL15/LVCMOS15 (receipts/io-200t-vs-ax7101.md). IOB packing 21 PASS 0 FAIL.
- B (scratch cddc4114, identical gateware inputs) and C give byte-identical configuration payloads.

## AX7101 unchanged (acceptance 3; receipts/ax7101-identity)
- `build.sh ax7101` elaborated at b7d69295 and at 1e604e1b in one clone path: 140 build inputs identical; Verilog body,
  xdc, tcl, init files, soc.h/csr.h/mem.h/csr.csv (timestamp lines aside) identical; the LiteX hierarchy comment
  differs between any two elaborations (also between the release build and a re-elaboration of b7d69295).
- The one AX7101 output that changes: flashboot_layout.json gains `flash_device`, `flash_jedec_id` (justified: the
  flash-device refusal #911 asks for). Its bitstream inputs are unchanged, so no re-route.

## Guide run (acceptance 4; receipts/guide-run), stub programmer, no cable opened
- 01 read part/offset/ID from the layout as written: `part xc7a200tfbg484, entity model at 0xa00000, flash ID 0x20ba18`.
- 02 check-images (FPGA_PART=xc7a200tfbg484) rc 0; 03 default part refused rc 2; 04 flash-images without the escape
  refused rc 2; 05/07 a 100T board refused (flash-images, flash) rc 2; 06 another flash (0x20ba19) refused rc 2;
  08 flash-images rc 0; 09 flash rc 0 (stub flash readback: payload at 0, AEM at 0xa00000); 10 identical installed
  refused rc 2; 11 update from build A refused rc 2 (A's own layout: payload exceeds its 4 MiB slot); 12 ax7101 recipe
  on the 200T set refused rc 2; 13 `build.sh ax7a200t --dry-run` rc 0. Refused steps wrote nothing (2 writes total).
- The successful update path is gate 1e's `ax7a200t` named arm (synthetic image sets).
- The plain openFPGALoader commands were not run against the real tool: it would scan the bench's FTDI cables.

## Gate table (head 4958ca4f630da1f715bdcd78113b798bbe332b81, clean clones; receipts/gates/)
| Gate | Result |
|---|---|
| rtl-fast.yml, rtl.yml, docs.yml, elaborate.yml: every `run:` step of every job (pull_request to dev; ci_scope rtl=true) | 150 steps rc 0 at the head, 522 not run with a stated reason (gates/not_run.json), 0 bad: `verify_wf.py` rc 0 (gates/workflow-steps.md) |
| rtl.yml verilator-shards (19 hosted workers) | the full sweep instead: `scripts/run_all_suites.sh` in 4 native shards, 65/65 suites passed, 0 in-suite failures (gates/sweep.txt) |
| elaborate-gates-2 LiteX sim leg | first run TIMEOUT at 900 s wall clock (host load ~150; the runner reports "result unknown, not a failure"), rerun on a fresh clone PASS (532 s); the 56009532 pass had it at 654 s (gates/elaborate-gates-2-gate_19_0-timeout-under-load.log) |
| `git diff --check b7d69295 HEAD` | rc 0 |
| `scripts/docs_inventory.py --check` | rc 0 |
| docs gates (docs_check, check_doc_style, check_doc_paths, gen_toc --check/--verify-anchors, check_em_dash --base b7d69295, check_solution_docs + selftest) | rc 0 (in docs-gates-0 and the lane gates) |
| lane: check_sweep_shape (+ --self-test), board_variants (+ --selftest, --layout on the handover set), py/sh idiom, test_timing_grade, gate 1e, build.sh ax7a200t/ax7101 --dry-run, flash_map | all rc 0 (gates/lane-gates.txt) |

Superseded passes: 56009532 found gate 24d's anchor (docs-gates-2 builder leg 1) and the Python/shell idiom
ratchets (docs-gates-0 gate_39/gate_40); every other step that ran there passed. 1e604e1b: stopped.

## Deviations
- No 16-wide range was free: all three Vivado runs used the author pool 96-127 with maxThreads 8.
- No 0-95 range came free for 25 min: queue lines run as transient units on 96-127 (pool_dispatch.py), and the sweep as
  native-shards.py's four units on 96-127. A runner left in the session cgroup kept writing old-head logs (ps in this
  sandbox does not list it); found through the cgroup, killed by PID, its files removed, the pass rerun at the head.
- C was first launched at 52665c88 and stopped at synthesis for a guide fix; relaunched at 1e604e1b.

## Pre-existing defect found (not fixed, out of scope)
- `python3 sw/litex/qspi_owner_transition.py --self-test` raises NameError (`sw` undefined at self_test, dev b7d69295);
  no workflow runs it. Needs its own issue.

## Log
- 12:56 start; 13:00 AX7101 compressed measurement; 13:01 TAKEN.
- 13:06 A, 13:07 B launched; 13:40 A rc 0 (5,566,832 B: no fit); 13:47 B rc 0 (all corners met).
- 13:50 C relaunched at 1e604e1b; 14:15 C rc 0; 14:16 handover; 14:16-14:20 guide run, cfgmem, receipts.
- 14:09 gate pass at 56009532 (units); 14:17 sweep shards; 15:02 gate 24d anchor; 15:15 idiom ratchets.
- 15:30 final pass at 4958ca4f launched (sweep shards + 19 queue lines); 16:58 elaborate-gates-2 LiteX sim timeout
  under load; 17:17 sweep 65/65; 17:26 elaborate-gates-2 rerun PASS; 17:27 verify_wf 0 bad.
- 17:30 REVIEW READY posted (issuecomment-6880655385). Scratch trimmed to the release build C, its clone and the gate logs.
