[A815] REVIEW READY

Commit: `62477be4` (`s13-flip-default`, 16 commits on dev-soft-core `59b09884`; local, the manager pushes and opens the PR against dev-soft-core, "Relates to #665").

Changed:
- The flip: `configs/endstation_ax7101_1x1_tdm8.yaml` and `_8x8.yaml` state `control: {placement: split}` (the two bench-gated shapes; the Arty configs stay all-fabric). The tracked AX7101 sweep fragment is regenerated, `sweep.sh`'s AX7101 row and `deploy.sh` follow it, and `build.sh ax7101` launches the split.
- VERSION: `milan_csr.sv` states `VERSION_SPLIT_MAJOR = 16'h0003` beside `VERSION`; the datapath's `CTRL_SPLIT_P` selects it, so a split image reads `0x0003_0060` (firmware 3.96.0) and an all-fabric one keeps `0x0002_0060` (2.96.0). One minor, stated once. RTL behaviour is otherwise unchanged; the mailbox contract and every CPU-budget bound are untouched.
- The switch: `endstation_builder.py <config> --placement all-fabric`, and `BUILD_PLACEMENT=all-fabric ./build.sh ax7101` for the release image. All-fabric stays built and gated, so the flip reverts in one commit; the processor is not deleted (NFR-SCOUT-02).
- Section 7's chain: `sim_split.cpp` pins the split datapath's VERSION and major 3, with a planted defect in `split_mutants.py`; `milan_dp/sim_main.cpp` adds the all-fabric major 2; the split stand-ins answer `0x0003_0060`; the UART grader takes major 2 or 3. Builder gates 1e, 23g, 23m-23p, 24, 25c, the entity-shape, feature-status, sweep-shape and clock-constraint gates, the census and the control-memory test are placement-aware, each new rule with a planted defect.
- Docs: every "which placement ships" statement, the split contract's section 7, the feature ledger (`gateware.current-version` `0x0003_0060`), the generated register map, the changelog, the documentation inventory (D0-001/033/056 retired).

Validation:
- IMAGE IDENTITY, the gating recipe at `822e3af0`, ExtraPostPlacementOpt, 16 threads; its inputs equal the head's (19 and 16 files compared):
  - 1x1/1if `68e5308b` vs `c7189218`: 103 bytes differ: 77 in the `.bit` header's `SW_CRC`/`SW_HDR_SHA256` text, 4 in the configuration CRC word, 22 bits in 7 of 9,464 frames. The checkpoints hold all 95,172 routes and all 86,465 cell placements equal; 8 block RAMs hold the 22 bits: the CSR defaults ROM 1 (VERSION), ROM bank 1 20 (the AEM image's CRC32 `0x38a80323` -> `0xdb1deab5`, a `lui`/`addi` pair), ROM bank 3 1 (`'2'` -> `'3'`).
  - 8x8/1if `6a1ff1ef` vs `7d903412`: 93 bytes: 74 header, 4 CRC word, 15 bits in 7 frames, held by 14 of 111 block RAMs in the same pattern (1 + 13 + 1). All 149 Vivado phase checksums equal.
  - Firmware: 6 loaded bytes at both points, the string and its CRC; layout equal.
  - Nothing else changes. The AEM CRC32 is not itself a version field: it is the integrity word of the descriptor image carrying the string, as the CRC word and header digests are the bitstream's.
- Flip check at the owner's bounds: 1x1/1if load 0.511 (0.70), last queued notice 127.31 ms (tree 130, owner 140), ACMP 29.06 (30), txL 47.88 (49); 8x8/1if load 0.744 (0.75): PASS. The all-points check reports 8x8/2if, not held, byte-identical to base.
- Timing floor (#818), every corner: ExtraPostPlacementOpt 1x1/1if +0.131/+0.102, +1.636/+0.036 ns; 8x8/1if +0.176/+0.102, +1.523/+0.036 ns (the bench images' figures exactly). ExtraTimingOpt: 1x1/1if +0.002/+0.102, +1.660/+0.036 (0.028 ns under the setup floor alone); 8x8/1if +0.059/+0.102, +1.660/+0.036. AltSpreadLogic_high: 1x1/1if +0.046/+0.102, +1.660/+0.036; 8x8/1if +0.150/+0.102, +1.660/+0.036. Best of three: met at every corner at both points.
- Gates, at `62477be4` unless named (each run's inputs unchanged after its head but comments):
  - the builder suite `--require-rv32 --require-elaboration`: ALL GATES PASS EXCEPT 2 NOT RUN (recorded: a make that does not re-read MAKEFLAGS; gate 11's bench-local calibration report);
  - the firmware gate, four shards `--require-rv32 --self-test` (`f7139ce1`): rc 0 x 4;
  - the sweep (`15db681a`), 4 shards: 65 of 65 suites PASS, 0 failures; 14 killed by the wall clock under host load were rerun alone and passed (`milan_dp` 14,085 checks among them);
  - the twin with its plants and the maps leg, `avtp_rxmon`, the split boot at both shapes (the grader on VERSION=0x00030060), `ctrl_boundary` both ways, the platform ledger, `split-cdc`, `split_parallel.py`, `split_mutants.py` 32 of 32, BDD 2,346 steps, `xvlog_gate` and Yosys x 4: all PASS;
  - the docs workflow's 103 commands: 99 PASS; the 4 failing are CI-environment rows (`GITHUB_EVENT_PATH`, the act install dir), as the train's;
  - the quick list's 58 (harness model checks and self-tests incl. `run.py --self-test` 0 failures, `rows_tiers`, `shape_costs`, `record_classes`, generators, idioms, census, shape and identity gates): all PASS but the all-points flip check (8x8/2if, above) and the CI-environment tool inventory.
- CPU-budget harness: all 16 arm images (8 x 2 points) differ from the measured ones in the same 6 bytes; the descriptor-reading groups and `control` re-measured identical, every leaf. 13 of 13 groups (7 at 1x1/1if, 6 at 8x8/1if) identical, 0 budget and 0 share misses.
- Release (all-fabric) image: `BUILD_PLACEMENT=all-fabric` export vs base: every loaded file equal (`bios.bin` `603b9ca3`, AEM `bdfde7cf`, ROM/SRAM/mem init), Verilog equal outside comments, argv equal.

Acceptance criteria: the validation plan of the TAKEN (issuecomment-7065258935) is met as above. The image identity found nothing beyond the version fields and their integrity words, so no STOP. Every figure here has its command, head and receipt in this lane's receipts, which go with the PR.

Open risks/questions:
1. NFR-SCOUT-02 and REQUIREMENTS section 1 tie the processor's deletion to "the switch-over". This PR follows issuecomment-6410301079: the flip changes the default, deletion waits for the full qualification. REQUIREMENTS section 1 is restated to that order; the normative NFR-SCOUT-02 row is not edited. For the owner to confirm.
2. The full CPU-budget re-measure (64 parts a point) was not completed: at this host's load it needed 8-12 h more. Owed if the reviewers want it.
3. The register map keeps its recorded all-fabric SoC export (now stated on the page); re-recording it from a split export restates its memory map and the 0x920 window. Follow-up.
4. Not gated and not changed: `syn/resmap/soc_sweep.py` reads the base config's argv, now the split's; the CPU-budget harness appends the split flags to an argv that now carries them (argparse takes its own image; images verified); the BUILD_FLASH_BOOT diagram describes the all-fabric BIOS flow.
