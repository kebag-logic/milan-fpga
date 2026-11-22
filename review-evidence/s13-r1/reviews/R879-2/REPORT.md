[R879] NEGATIVE - exact head 9413958c66c0dcd632b3e0e7ac44505314fed41a

R879-2, the internal independent review of issue #665 / PR #960 (the flip, S13), round 2. This is a delta re-review: from `62477be4` (round 1) to `9413958c`, which adds 7 commits, tree `83b2c214071b7f3f74c0eda10048ec674e3d5fdc`. I rebuilt the context from public state in this order: AGENTS/CONTRIBUTING; the issue body and the TAKEN and both REVIEW READY comments; the delta diff and its history; and the published evidence at `491ffed7` (`review-evidence/s13-r1/author-r2`). I read the prior public findings (R880-1, R879-1) only after my own pass over the delta.

**Why NEGATIVE.** One MINOR is open: R879-2-F1. The published identity packet leaves out 5 of the 224 operands its own `MANIFEST.sha256` lists. Because of that, the author's replay fails its manifest check and stops with a traceback. The author's planted-defect driver also cannot run on the published packet.

The carry itself is not in doubt. I wrote my own diff (standard library) and ran it over the 219 operands that are published, and every checked claim holds. My diff also refuses all 11 kinds of planted defect. So the bench evidence carries by identity, and the full 64-part CPU re-measure is not needed. What is missing is that the public record cannot yet reproduce the author's own replay and plant claims.

Every other named finding is resolved at its cause.

## Findings

### R879-2-F1 | MINOR | Tests, Docs | the published identity packet omits 5 listed operands; the published replay and plant driver fail on it

- **Artifact:** `review-evidence/s13-r1/author-r2/receipts/identity/` at `491ffed7`. Its `MANIFEST.sha256` lists 224 files, but these 5 are absent from the published tree:
  - `shipping/1x1/dump/bench.cells.xz`
  - `shipping/1x1/dump/flip.cells.xz`
  - `groups/1x1/declaring-outputs/aecp-outputs.measured.log.gz`
  - `groups/8x8-1if/declaring-outputs/aecp-outputs.head.log.gz`
  - `groups/8x8-1if/declaring-outputs/aecp-outputs.measured.log.gz`

  The publication's own `review-evidence/s13-r1/MANIFEST.json` lists 485 files and none of these 5. I found no other public copy of them.
- **Evidence:**
  - `receipts_replay_published.txt`: `python3 -I tools/replay.py .` was run over an unmodified copy of the published directory.
    - Section 1 reports `FAIL 224 listed files hash as listed` and `FAIL ... missing [5 files]`.
    - Section 3 reports `FAIL 1x1 cells dump: present for both checkpoints`.
    - Section 5 ends in `AttributeError: 'NoneType' object has no attribute 'read_bytes'` at the first missing log. It never reaches its RESULT line.
  - `receipts_rmutants_published.txt`: `tools/rmutants.py` was run over the published directory.
    - Plant 1 ("a configuration bit outside the ROM frames") is `MISSED` by its own criterion. Its only semantic guard at 1x1 is the absent cells dump. The replay still exits 1, but only on the operand-hash binding.
    - The driver then crashes with `FileNotFoundError` at plant 5, which edits the absent `1x1/dump/flip.cells.xz`.
  - So two statements in the REVIEW READY (issuecomment-7072252167) cannot be reproduced from public state: "replay: ALL CLAIMS HOLD" and "11 defects planted ..., 11 refused".
- **Impact:** a cold reviewer who runs the published replay gets FAIL and a traceback. Two comparisons cannot be checked by anyone from public material:
  - the 1x1/1if cell-level INIT mapping;
  - the `aecp-outputs` raw-log comparison (1x1 measured, and both 8x8/1if logs).

  This does not overturn the carry. The R880-1-F2 resolution below shows the identity holds without these files: the 1x1 frame bits sit in the BRAM-content frames, and the JSON leaves of that group are equal at both points. It does mean that the evidence published for R880-1-F2 does not yet support the replayable-packet claim the author made for it.
- **Required outcome:** the public evidence tree holds every file the identity `MANIFEST.sha256` lists, hash-equal. The published `tools/replay.py .` then ends `== RESULT: ALL CLAIMS HOLD`, and `tools/rmutants.py` reports 11 of 11 from the public tree. If the files cannot be published, re-seal the packet without them and restate the replay and plant claims to match. That publication step belongs to the manager; the head needs no source change.
- **Verification:** run `sha256sum -c MANIFEST.sha256`, the replay and `rmutants.py` from a fresh fetch of the evidence commit. My `tools/r879_identity.py` then reports no absent operands and exits 0.

### R879-2-S1 | SUGGESTION | Tests, Robustness | the sweep's self-test does not exercise `prepare()`/`command_export()` wiring

`syn/resmap/soc_sweep.py:104-121,133`. Three mutations pass `soc_sweep.py --selftest` (`gates/soc_sweep_mutants.txt`):
- M1: `prepare` stops passing `--placement` to the builder.
- M2: `prepare` never raises on a missing image.
- M3: `command_export` passes `split` whatever the plan says.

M4, where `missing_images` reads paths against the wrong root, is caught.

The run-time behaviour is fail-safe. M1 or M3 alone hits the missing-image refusal. M2 alone is harmless at all-fabric. Only M1 plus M2 together brings back the round-1 dependency, and even then a fresh export tree has no ELF for it to depend on. The author's fresh-clone control (`f1/rsweep-a9da4c48.txt`) demonstrates this once. Optional: add a self-test arm that runs `prepare()` with the builder call stubbed to emit a split argv, and expects the refusal.

### R879-2-S2 | SUGGESTION | Tests | the raw-log rule accepts any `2`->`3` digit anywhere

`identity/README.md` says "a differing line may differ only by `2` -> `3` digits", and `replay.py` applies it to the whole line. My probe plants a `2`->`3` change in an unrelated line of `groups/1x1/none/control.head.log.gz`. It passes both the author's rule and my own diff, which applies the same rule (`receipts_plants_reviewer.txt`, the "PROBE" case).

The actual data has no defect: all 8 differing lines are the ENTITY `firmware_version` field. On the wire it is `...322e39362e30...` -> `...332e39362e30...` ("2.96.0" -> "3.96.0"), and the mailbox word is `2e320000` -> `2e330000` (`receipts_identity.txt`, groups section). Optional: anchor the rule to that field's context.

### R879-2-S3 | SUGGESTION | Tests | the replay crashes instead of refusing by name when an operand is absent

`identity/tools/replay.py:450` (`find()` returns `None`, then `read()`). Optional: refuse with a named FAIL so the driver reaches its RESULT line.

### R879-2-S4 | SUGGESTION | Robustness | whitespace regression in the sweep

`syn/resmap/soc_sweep.py:134` reads `env ={**os.environ, ...` (round 1 had `env = {`). This came in with `59f91d9f`. No behaviour change, and no repository gate covers it.

### R879-2-S5 | SUGGESTION | Docs | duplicated bench-gate pointer

`docs/reference/MILAN_COMPLIANCE_MATRIX.md:4` ("its bench gate is on #665") and `:7` ("for the flip that evidence is the bench gate on #665", the R879-R1 wording) now say the same thing twice. Optional: drop the clause from line 4.

### R879-2-R1 | RESIDUE | Docs | remaining "all-fabric ships" labels the flip made stale

These lines are pure wording. None of them changes a measurement, a test or a status column. Exact fixes:
- `docs/ENDSTATION_BUILDER.md:3-4`. Replace "This page describes the current all-fabric shipping build. / The default changes only after F2 to F5 acceptance." with "This page describes the builder at both control placements. / The AX7101 configs ship the split since the flip (#665); the all-fabric build stays built and gated."
- `docs/integration/INTEGRATION_GUIDE.md:3`. Replace "This contract describes the current all-fabric shipping control plane." with "This contract describes the all-fabric control plane; the AX7101 builds ship the split since #665."
- `docs/reference/FR_NFR.md:109`. Replace "describes the all-fabric shipping placement." with "describes the all-fabric placement."
- The author's open item 3, same kind:
  - `docs/reference/FR_NFR.md:173`: "`KL_maap` remains the shipping allocator" -> "`KL_maap` is the all-fabric build's allocator (the split builds none, `MAILBOX_SPLIT.md:1608`)".
  - `docs/fpga/FPGA_DESIGN.md:313` and `docs/testing/TESTING.md:731`: "remains the shipping allocator" -> "is the all-fabric build's allocator".

  `FR_NFR.md:173` is inside a normative row. The fix leaves its "MET, in this fabric" status unchanged, but the manager may route it to the owner together with open item 1.

## Prior findings, resolved or retained at this head

| Finding | Status at `9413958c` | Evidence |
|---|---|---|
| R880-1-F1 MAJOR (sweep prices a placement whose image it does not build) | **RESOLVED** | See the R880-1-F1 paragraph below the table. |
| R880-1-F2 MAJOR (hashes published, not operands) | **RESOLVED at its cause**; the 5 absent operands are R879-2-F1 | See the R880-1-F2 paragraph below the table. |
| R880-1-F3 MINOR (header bytes by field) | **RESOLVED** | I parsed the header field by field with my own parser. 1x1/1if: 103 = `SW_CRC` 8 + `SW_HDR_SHA256` 63 + date (field `c`) 1 + time (`d`) 5 + CRC register write 4 + 22 FDRI bytes. 8x8/1if: 93 = 8 + 61 + 1 + 4 + 4 + 15. Every other header field is equal, including `b` (part) and `e` (length). Every differing byte falls in one of those classes. `receipts_identity.txt`. |
| R880-1-F4 MINOR (identity paragraph vs gate 23o) | **RESOLVED** | `docs/design/MAILBOX_SPLIT.md:1808-1813` names the one field (ENTITY `firmware_version`) and the two artifacts (`aem_overlay.json`, `aecp_aem_rom.svh`). These match `sw/builder/test_builder.py:24308` (`RECIPE_VERSION_ARTIFACTS = ("aem_overlay", "aem_rom_svh")`), `_version_field_only` at `:24368-24371`, and the `AEM_ROM_OUT_NAME` file names in `endstation_builder.py:2313`. |
| R879-F1 MINOR (register map "shipping SoC/build") | **RESOLVED** | `docs/reference/REGISTER_MAP.md:27,29,154-157,248` label the map and parameters as the all-fabric build's, link the split map at `SPLIT_CONTROL_MEMORY.md#1-memory-map` (the anchor exists, `:29`), and state `CTRL_SPLIT_P` 1. The table row `:262` keeps 0 (all-fabric). The generator `scripts/register_page.py` was checked with `gen_register_reference.py --check` (fresh, 203 registers) and `--selftest` (61/61). |
| R879-F2 MINOR (README pipeline) | **RESOLVED** | `README.md:298-312` states the split build's platform-image prerequisite, ROM boot and `0x00030060`, and labels the picture as the all-fabric release flow (`:307-308`, `BUILD_PLACEMENT=all-fabric`, `0x00020060`). `BUILD_PLACEMENT` is honoured by `sw/litex/build.sh:330`. A missing image stops at `ctrl_memory.read_elf`'s `read_bytes` (`sw/litex/ctrl_memory.py:397`), which names the path. I regenerated `docs/BUILD_FLASH_BOOT.gen.py` in scratch: svg and drawio are byte-identical, and the png via `rsvg-convert -w 2400` is byte-identical (`gates/diagram_cmp.txt`). |
| R879-S1 SUGGESTION (harness argv) | **RESOLVED** | See the R879-S1 paragraph below the table. |
| R880-1-R1, R879-R1 RESIDUE | **APPLIED** | `ARCHITECTURE.md:4,19`, `FULL_FPGA_SOLUTION.md:3,19`, `MAILBOX_SPLIT.md:5,626` (and `:2118-2119`), `MILAN_COMPLIANCE_MATRIX.md:7` read as prescribed. The leftover stale labels are R879-2-R1. |

**R880-1-F1.**
- `syn/resmap/sweep_plan.json:72` names `"placement": "all-fabric"`.
- `soc_sweep.py:65-70`: `plan_placement` refuses a soc section that names no placement.
- `:104-121`: `prepare` passes `--placement` to the builder. Before any `milan_soc.py` export, it refuses an argv whose `--ctrl-firmware` image is not a file in the export tree (`missing_images`, `:73-78`). That tree is read the way `milan_soc.py:4934-4935` reads it, against its `REPO_ROOT`.
- `main` turns the refusal into rc 2 (`:337-342`).
- Self-test: PASS (`gates/soc_sweep_selftest.log`). Its arms catch a plan at split, a plan with no placement, and an empty `missing_images`, as the author's `gates/plants-9413958c.txt` shows. My M4 is also caught.
- `yosys_sweep.py --selftest`: PASS.
- The author's fresh clone at `a9da4c48` (`f1/rsweep-a9da4c48.txt`) shows 0 platform images before export, `ship` and `axilite` accepted, the six expected refusals kept (`l2-8k`, `rv64`, `cpu2`, `rv64-fpu`, `naxriscv`, `l1-caches`), and the split-plan control refused before any export with nothing written. `a9da4c48..9413958c` changes only `docs/DOCUMENTATION_AUDIT.md`.
- `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:129-130` states the placement and the refusal.
- Wiring coverage is SUGGESTION R879-2-S1.

**R880-1-F2.** My own diff, `tools/r879_identity.py` (`receipts_identity.txt`), was written without reusing the author's driver and run over the 219 published operands. These are its results:
- **Hash binding.** The bench `.bit`/ELF hash to the published `c7189218`/`c873a0aa` (1x1/1if) and `7d903412`/`d67fd049` (8x8/1if), as stated in issuecomment-7063917242. The flip `.bit` files hash to round 1's `68e5308b`/`6a1ff1ef`.
- **The `.bit` files.** They are the same length, with the same header field lengths and an identical packet structure (956,434 words classified). The only differences are the header text above, the CRC register write, and FDRI frame data. At 1x1/1if that is 22 bits in 7 frames; at 8x8/1if, 15 bits in 7 frames.
- **The platform ELFs.**
  - Same size, load segments and symbol table.
  - 6 differing bytes, all loaded. One is `aecp_entity_image+0x184` `'2'`->`'3'` ("2.96.0"->"3.96.0"). The rest are one `lui`/`addi` pair whose value equals `zlib.crc32(aecp_entity_image)`: `38a80323`->`db1deab5` at 1x1/1if, `d6dd74b9`->`b730ec91` at 8x8/1if.
  - `aecp_entity_image` is the export's `aem_desc.bin` on both sides.
  - The ROM bank inits differ in exactly the ELF's differing bits: 21 at 1x1/1if (bank1 20 + bank3 1) and 14 at 8x8/1if. Every non-ROM gateware init is equal.
  - Frame bits = ELF bits + 1 at both shapes. The extra bit is VERSION bit 16 (`0x0002_0060`->`0x0003_0060`).
- **Export files.** They differ only in the LiteX timestamp comment, the AEM CRC32 constant and SHA-256, the payload SHA-256, and the manifest VERSION/ELF hash.
- **Routed checkpoints.** Nets dumps are equal at both shapes (95,172 and 119,085 routes). At 8x8/1if the cells and bram dumps put the 15 INIT bits in 14 block RAMs: the CSR defaults ROM (`INITP_00`) and 13 ROM banks. Every name, type and placement is equal.
- **The 1x1/1if cell-level gap.** The 1x1/1if cells dump is absent (R879-2-F1). Its 22 frame bits are frames 7826-8854 of a single FDRI block. Frame address auto-increment puts all BRAM-content frames after all logic frames. Frame 7736 already holds BRAM INIT content at 8x8/1if on the same part. So every 1x1/1if differing frame is BRAM content, and no logic or routing bit changes.
- **Harness images.** All 16 measured/head pairs: same layout and symbols; 6 bytes each, of the same kind; `parts.json` equal.
- **The 13 groups.** Every JSON leaf is equal, with no exclusions. The raw logs I could compare (11 of 13 groups at both points, plus `aecp-outputs` head at 1x1) differ only in the `firmware_version` field.
- **Planted defects.** `tools/r879_plants.py` (`receipts_plants_reviewer.txt`) plants the author's 11 kinds into hard-linked copies with the manifest re-sealed. The cell-placement plant is moved to 8x8 because 1x1 is absent. The unplanted control is CLEAN, and the diff catches 11 of 11.

So every difference is the version word, the firmware string, the integrity words computed over them, or named header/build-stamp metadata, and the bench evidence carries by identity. The carry to this head holds:
- `62477be4..9413958c` touches no file under `hdl/`, `sw/`, `configs/` or the LiteX scope.
- The harness change (`split_argv`) produces the measured runs' argv again (R879-S1 below), so the export, and with it the images, is unchanged.

**R879-S1.**
- `tb/verilator/ctrl_service_budget/build.py:355-369`: `split_argv` drops the config's `--ctrl-mailbox`/`--ctrl-firmware <image>` pair and appends the harness's pair once, refusing a trailing value-less flag. `:382-386` uses it.
- `selftest.py:753-757` checks, for both shapes, that the result equals the all-fabric argv plus the harness pair. `build_checks` run standalone gives 4 of 4 PASS (`gates/harness_build_checks.log`).
- The author's two plants (appending; keeping the config's image) are caught (`gates/plants-9413958c.txt`).

## Lens results (artifact-specific)

```text
[R879] PASS Conformance - syn/resmap/sweep_plan.json:72, soc_sweep.py:65-121; receipts_identity.txt (both .bit pairs, ELFs, ROM inits, exports, 16 harness pairs, 13 groups); MAILBOX_SPLIT.md:1804-1813 vs test_builder.py:24308-24371; REGISTER_MAP.md:248,262 - the validation plan's image-identity carry independently re-derived (only VERSION, firmware string, integrity words, header stamps differ); the sweep prices the placement its recorded figures were taken at; the stated split/all-fabric VERSIONs and CTRL_SPLIT_P match the RTL chain round 1 cleared
[R879] PASS RTL - git diff 62477be4..9413958c -- hdl/ sw/ configs/ (empty); receipts_identity.txt nets equal both shapes, frame bits all BRAM content - the delta touches no RTL, LiteX or config artifact; the shipped netlist/placement/routing equal the bench images'; R879-1's RTL verdict at 62477be4 stands (an ancestor with nothing in RTL scope touched since)
[R879] PASS Robustness - soc_sweep.py:73-78,104-121,337-342; build.py:355-369; gates/soc_sweep_mutants.txt; author f1/rsweep-a9da4c48.txt control - missing image, value-less flag, absent placement, split plan and duplicate image pair are each refused or replaced by name before any export; fail-safe under single mutations (wiring coverage is SUGGESTION S1)
[R879] NEGATIVE Tests - review-evidence/s13-r1/author-r2/receipts/identity (MANIFEST.sha256, tools/replay.py, tools/rmutants.py); receipts_replay_published.txt, receipts_rmutants_published.txt - R879-2-F1 open: the published replay and plant driver fail on the published packet; the new self-test arms (soc_sweep --selftest PASS; harness build_checks 4/4) can each fail for their defect
[R879] NEGATIVE Docs - identity packet publication (R879-2-F1); README.md:296-312, REGISTER_MAP.md, MAILBOX_SPLIT.md:1804-1813,2118-2119, 649_RESOURCE_MAP_AND_SENSITIVITY.md:129-130, overview pages, docs gates in gates/ - R879-2-F1 open (public evidence cannot reproduce the REVIEW READY's replay/plant claims); every changed page otherwise accurate; residues R879-2-R1
```

Docs-workflow gates I ran at this head (18 commands), all rc 0 (`gates/`):
- `docs_check` (0 findings);
- `check_feature_status`;
- `check_doc_style` and its `--selftest`;
- `check_em_dash --base 59b09884` (0 findings over 172 added lines);
- `check_solution_docs`;
- `check_doc_paths`;
- `gen_toc --verify-anchors` (755 links) and `--check`;
- `docs_inventory --check` (`DOCUMENTATION_AUDIT.md` fresh);
- `check_diagram_pngs`;
- `DOC_MAP.gen --check`;
- `memory_map.gen --check`;
- `gen_register_reference --check` and `--selftest` (61/61);
- `check_py_idiom`;
- `check_hygiene --check`;
- `measure_fail_fast --check`.

The renderer-dependent gates ran in a disposable environment with the hash-locked `tools/markdown/requirements.txt` plus `wavedrom==2.0.3.post3`. A first attempt without those packages refused by name, and was re-run.

Comment rule: added lines in the delta carry no lane labels, lane names, review rounds, reviewer IDs or comment IDs. I scanned every `+` line of `git diff 62477be4..9413958c` for those patterns and found 0 hits.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | sweep plan and `soc_sweep.py` placement path; identity operands (both `.bit` pairs, ELFs, ROM inits, exports, 16 harness pairs, 13 groups) re-derived by own diff; gate-23o paragraph vs `test_builder.py`; register map statements | R879-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |
| RTL | CLEAN | delta touches no RTL/LiteX/config file; bitstream and route identity from operands; prior RTL verdict | R879-1 (RTL scope untouched since), confirmed R879-2 | 62477be4cb90336ca9b59ae7ab8377546e72557a (ancestor; nothing in RTL scope changed through 9413958c) |
| Robustness | CLEAN | `soc_sweep.py` refusals, `split_argv`, mutation probes M1-M4, author's fresh-clone control | R879-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |
| Tests | UNCLEAN (R879-2-F1) | published replay and plant driver over the published packet; `soc_sweep --selftest`; `yosys_sweep --selftest`; harness `build_checks`; own 12-case plant set | R879-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |
| Docs | UNCLEAN (R879-2-F1; R879-2-R1 non-blocking) | README, BUILD_FLASH_BOOT generator and renders, REGISTER_MAP and its generator, MAILBOX_SPLIT, 649 findings page, overview pages, compliance matrix, DOCUMENTATION_AUDIT, docs gates, published evidence packet | R879-2 | 9413958c66c0dcd632b3e0e7ac44505314fed41a |

Closing R879-2-F1 is a publication change, not a head change. Once the 5 operands are public and the published replay and `rmutants.py` run green, Tests and Docs can be re-covered at this same head without touching the other three lenses.

## Real limits

- **No Vivado run, no image rebuild.**
  - Not repeated here: the bench and flip images, the harness rebuilds at `8c5e2b4f`/`a9da4c48` (`binding.json`), the 8x8 routed-checkpoint dumps, and the timing figures. Those are the author's.
  - Established here: the identity between the published operands, and the argv equality that keeps the harness images unchanged.
- **The 5 absent operands** (R879-2-F1).
  - The 1x1/1if cell-level mapping rests on the frame-region argument above.
  - The `aecp-outputs` raw logs were not compared at 1x1 measured or at either 8x8/1if side. Their JSON results were.
- **The full harness `run.py --self-test` did not finish.** It was stopped at the background time limit under host load after 1,011 PASS lines and no FAIL (`gates/harness_selftest.log`, no rc). The changed `build_checks` ran standalone, 4/4. For the full run I rely on the author's quick-list receipt.
- **Not re-run:** the LiteX `soc_sweep export` (the author's fresh-clone receipt was reviewed instead) and the full 103-command docs workflow. I ran the 18 commands listed above.
- **Hosted checks at the exact head** (`receipts_hosted_snapshot.txt`, read-only): 40 completed success, 1 skipped (physical gPTP), 18 still in progress, including Verilator shards, Yosys shard 0/4, `yosys-elaboration` and the firmware jobs. The in-progress and skipped contexts are not executed evidence. The manager owns hosted and act acceptance.
- **No manager source bank** ran at this head, and I claim none.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Clone integrity.** After the probes the clone has worktree and index equal to HEAD. The `git ls-files -s` and `git ls-tree -r HEAD` mode/blob/path digests are equal (`be472d34…`). The six gitlinks are unchanged: `external` efeb541a, `gptp-processor` 1616fc8f, `protocol-processor` 801ef228, `third_party/lwSRP` 08ee86e8, `third_party/tsn-c-stack` 715589c1, `third_party/verilog-axis` 48ff7a7e. The `__pycache__` directories created this session were removed. There are 0 untracked or ignored files.

## Pending manager and owner duties

1. **Manager (R879-2-F1):** publish the 5 listed operands hash-equal under `review-evidence/s13-r1/author-r2/receipts/identity/`, or have the packet re-sealed and its claims restated. Then re-check Tests and Docs at this head.
2. **Manager:** carry R879-2-R1 to the residue checklist. Its `FR_NFR.md:173` item sits in a normative row; route it to the owner if the row's text needs sign-off.
3. **Manager:** handle the author's open item 2. Re-recording the register map from a split export needs a public Issue.
4. **Owner:** decide the author's open item 1, the NFR-SCOUT-02 "switch-over" wording. This round does not change it.
5. **Manager:** build and validate the current-dev merge candidate (source base `59b09884`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`) with the builder and native banks. Also collect exact-head `verilator-suites`/`yosys-portability` evidence.

## Packet

- `tools/r879_identity.py`: the reviewer's independent identity diff (standard library; `python3 -I tools/r879_identity.py <identity-dir>`). Exit 0 means all claims hold, 1 means a claim failed, 3 means all checked claims hold but listed operands are absent.
- `tools/r879_plants.py`: the 11 plant kinds and a rule-strength probe against that diff (`python3 -I tools/r879_plants.py <identity-dir> <work-dir> tools/r879_identity.py`).
- `receipts_identity.txt`, `receipts_plants_reviewer.txt`, `receipts_replay_published.txt`, `receipts_rmutants_published.txt`, `receipts_hosted_snapshot.txt`.
- `gates/`: each gate's log and rc, `soc_sweep_mutants.txt` and `diagram_cmp.txt`.

R879-2 FINISHED
