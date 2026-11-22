[A815] REVIEW READY

Commit: `9413958c` (`s13-flip-default`, 23 commits on dev-soft-core `59b09884`; round 2 of #960, answering R880-1 and R879-1; local, the manager pushes).

Changed (round 2: 7 commits on `62477be4`; every receipt named below is in this lane's round-2 receipts, which go with the PR's evidence):

| Finding | Cause | Fix | Test | Receipt |
|---|---|---|---|---|
| R880-1-F1 MAJOR | `soc_sweep.prepare()` built the base config at its own placement; since the flip that is the split, whose argv names `sw/builder/out/<cfg>/ctrl_app.elf`, an image nothing in the sweep builds | `59f91d9f`, `a9da4c48`: `sweep_plan.json` names the placement, all-fabric (the #649 figures' own); `prepare()` passes it to the builder and refuses, before any export, an argv naming an image the tree does not hold; the findings page says so | a fresh clone with no platform image anywhere: `ship` and `axilite` accepted, the six refusal cases refused as planned; control (a plan copy naming split): refused before any export, naming the image, nothing written; against base: argv equal, gateware equal but Verilog comments and the XDC's clock-group order (equal as a set). Plants: plan at split, plan with no placement, `missing_images` empty: 3 of 3 caught | `f1/`, `gates/plants-9413958c.txt` |
| R880-1-F2 MAJOR | round 1 published the comparison's hashes, not its operands | `identity/`: both `.bit` pairs, the four platform ELFs, every ROM bank init, the export files, both shapes' routed-checkpoint dumps (every cell and every route, xz; 8x8's newly made), the 16 harness image pairs, the 13 groups' result JSON and raw logs, `binding.json`, and `tools/replay.py` (standard library; `python3 -I tools/replay.py .`) | replay: ALL CLAIMS HOLD; 11 defects planted in copies of the operands, 11 refused (`identity/plants.txt`) | `identity/` |
| R880-1-F3 MINOR | round 1 parsed the design-name string only and counted the date and time fields' bytes into it | the header is parsed by field | 1x1/1if 103 = design name 71 (`SW_CRC` 8, `SW_HDR_SHA256` 63) + date 1 + time 5 + the CRC register write 4 + 22 frame bits in 22 bytes; 8x8/1if 93 = 69 (8 + 61) + 1 + 4 + 4 + 15. Header text is not loaded | `identity/replay-output.txt` |
| R880-1-F4 MINOR | the identity paragraph kept "byte for byte" after gate 23o gained its firmware_version exception | `2f985971`: `MAILBOX_SPLIT.md:1804-1813` states the one field and the two artifacts | against `test_builder.py` `RECIPE_VERSION_ARTIFACTS` | - |
| R879-F1 MINOR | `register_page.py` called the recorded all-fabric export "the shipping SoC/build" | `e4dd762a`: the memory map and build parameters are labelled the all-fabric build's, the split's map is pointed at, and `CTRL_SPLIT_P` 1 is stated | `gen_register_reference.py --check` fresh, `--selftest` 61/61, doc style OK | `gates/docswf-9413958c.txt` |
| R879-F2 MINOR | the pipeline generator drew `build.sh ax7101` with the pre-flip boot and VERSION | `530cdbf9`: the picture is the all-fabric release flow (`BUILD_PLACEMENT=all-fabric`, `0x00020060`); the README states the split build's platform-image prerequisite, boot and `0x00030060` beside it | svg, drawio and png regenerate byte-identical | `gates/round2-checks-a9da4c48.txt` |
| R879-S1 | the harness appended the split pair to an argv that already carries the config's | `bc5a947d`: `build.split_argv` replaces it | the harness's export argv equals the measured runs' at both points again (round 1's named two images); all 16 images unchanged; plants: appending, keeping the config's image: 2 of 2 caught | `s1/`, `gates/plants-9413958c.txt` |
| R880-1-R1, R879-R1 | stale "all-fabric ships" wording | `2f985971`, the reviewers' wording (and `MAILBOX_SPLIT.md:2118`, same kind) | - | - |

Validation:
- IMAGE IDENTITY, from the operands (`identity/replay-output.txt`), at both shapes:
  - bench images hash to the bench re-check's published `c7189218`/`c873a0aa` and `7d903412`/`d67fd049`; flip images to round 1's `68e5308b`, `6a1ff1ef`; their 19 and 16 inputs are equal at `a9da4c48` (`a9da4c48` -> `9413958c` changes one generated docs page);
  - `.bit`: same layout and packet structure; only the header text above, the CRC register write and 22 / 15 frame bits differ;
  - routed checkpoints: every cell's name, type, LOC and BEL and every route equal (1x1 86,465 cells and 95,172 routes; 8x8 109,093 and 119,085); the INIT bits that differ sum to the frame bits, in 8 / 14 cells, each the CSR defaults ROM or a platform ROM bank;
  - platform ELFs: the whole files differ in 6 bytes, all loaded: a `lui`/`addi` pair loading crc32 of `aecp_entity_image` (`38a80323` -> `db1deab5`, `d6dd74b9` -> `b730ec91`) and that image's byte 0x184 `2` -> `3`; `aecp_entity_image` is the export's `aem_desc.bin`; the ROM bank inits are exactly the ELF's load segments;
  - harness: all 16 pairs the same 6 bytes, the same group partitions; each measured image is byte for byte the harness build at the bench head `8c5e2b4f` (8x8/1if was measured at `92de01f7`), each head image the build at `a9da4c48`;
  - 13 groups: every result leaf equal, none excluded; raw logs equal but the ENTITY's firmware_version digit (`2` -> `3`) on the wire and in its mailbox word (`aecp`, `aecp-held`, at both points).
  - Nothing differs beyond the version fields and the integrity and build-stamp fields computed over them: no STOP, and the full CPU re-measure stays not required.
- Gates at this round's heads (no file in the RTL, builder, config, LiteX or firmware scope changed since `62477be4`, so round 1's builder suite, sweep, firmware gate, flip check and timing carry unchanged):
  - the docs workflow's 103 commands at `9413958c`: 99 PASS; the 4 failing are the CI-environment rows round 1 recorded;
  - the quick list's 58 at `2f985971`: 55 PASS, `run.py --self-test` 0 failures; not passing: the all-points flip check (8x8/2if, output identical to base's), the CI tool inventory (CI environment) and the docs inventory, regenerated in `9413958c` and passing there;
  - this round's checks at `a9da4c48`: `soc_sweep.py` and `yosys_sweep.py` self-tests, the diagram regeneration, the harness argv checks, the solution-docs and doc-path gates: 6 of 6;
  - the planted defects at `9413958c`: 5 of 5 caught, the unplanted controls pass, the tree clean after.
- Corrections to round 1, both found here: the header split (F3), and round 1's group driver, which skipped string leaves holding a `/` as paths: they were the 21 `summary` access tuples per group, equal, and now compared.

Acceptance criteria: unchanged from round 1 (issuecomment-7070924358), now with the identity carry's operands published and replayable; each round-2 finding is fixed at its cause or answered with evidence as above.

Open risks/questions:
1. (round 1, unchanged) NFR-SCOUT-02's "switch-over" wording: for the owner.
2. Re-recording the register map from a split export (R879-F1's first option) is deferred and needs a public Issue, which this lane may not open: for the manager.
3. `KL_maap` is still called "the shipping allocator" in `FR_NFR.md:173` (the normative FR-MAAP-01 row), `FPGA_DESIGN.md:313` and `TESTING.md:731`, true of the all-fabric build only; found while fixing R880-1-R1, not edited (outside the findings, partly normative).
4. `syn/resmap/yosys_sweep.py` is unchanged on evidence: its points bind the plan's parameters (all-fabric) and its shapes step gives the same outcomes and shapes at base and `62477be4` (`f1/yosys-shapes-59b09884-vs-62477be4.txt`).

REVIEW READY 9413958c
