# HANDOFF, round 5: the final head and attempt 2 (#665), [A794]

## Status (21:0x, 11-20): R866-4-F1 ANSWERED WITH EVIDENCE ONLY. THE GATING BITSTREAMS' LOADED FIRMWARE IS THE PRODUCT FIRMWARE AT BOTH POINTS, TWO-SIDED AND RE-RUNNABLE. NO SOURCE CHANGE, NO NEW ROUTE, NO NEW COMMIT

- **The finding:** R866-4-F1 (#945 issuecomment-7049051089), MINOR, Tests and Docs. It found no public
  loaded-image comparison between the new gating ELFs and the head's product images, and the manifests were not
  published.
- **The receipt:** `receipts/step16/gating/loaded-identity/`. Its README maps each claim to a file.
  - **`loaded_identity.py` at both points: PASS** (`loaded-identity.log`, rc 0).
    - **Loaded bytes:** every program header and PT_LOAD's bytes are equal. Every SHF_ALLOC section (`.text`, `.rodata`,
      `.data`, `.bss`, `.stack`) has equal name, type, flags, VMA, LMA and length, and its full sha256 is listed on each
      side and equal.
    - **ROM words:** the repository's rom words of each ELF equal the bitstream build's rom bank init files: 1x1/1if
      `1fd5bc47…`, 31,608 words; 8x8/1if `ac014c6a…`, 34,802 words.
    - **The manifest:** its sha256 is the artifact list's, and it binds the gating ELF. Its bitstream binding equals
      the one recomputed from the `.bit`, and the identity gate re-runs clean.
  - **The planted controls:** two, both refused. A product ELF with one `.rodata` byte flipped, and an artifact list
    with the bitstream digest zeroed.
  - **Why the whole files differ** (`c873a0aa…`/`fe12a3f1…`, `d67fd049…`/`c6355962…`): the two links used different
    SDKs, the gating lane's pinned one (binutils 2.43.1) and the lane's (2.45.1), both GCC 14.3.0.
    - The section header tables are equal, and all 2,474 differing bytes are in `.symtab`.
    - Both symbol tables hold the same 1,267 entries. 612 positions swap a named local with a mapping symbol at the
      same address.
    - No loaded section of the 43 input objects differs.
  - **The published manifests:** `receipts/step16/gating/<point>/build/` (`image_manifest.json`,
    `flashboot_layout.json`, `csr.csv`, `aem_desc.bin`), beside `artifacts.sha256` and `identity.log`, and the bench
    list's section `bench-images-8c5e2b4f.txt`.
  - **`verify_published.py`, run on the receipts alone: PASS.** It checks every published file against its listed
    digest; the manifest's firmware against the compared gating ELF; the bitstream digest against the bench list and
    the binding; the product ELF against `images/product-images.txt`; and the identity lines. Its planted control (a
    manifest naming other firmware) is refused.
- **Files changed this round** (receipts and records only):
  - **New:** `receipts/step16/gating/loaded-identity/` (README.md; `1x1.txt`, `8x8.txt`; `loaded-identity.log` and
    `.rc`; `toolchains.txt`; `plants/`; `verify-published.log` and `.rc`; `verify-published-plant.log`; and in `tools/`
    `loaded_identity.py`, `loaded_identity.sh` and `verify_published.py`).
  - **New:** `receipts/step16/gating/{1x1,8x8}/build/` (4 files each) and `receipts/step16/gating/bench-images-8c5e2b4f.txt`.
  - **Re-copied, content unchanged:** `receipts/step16/gating/{1x1,8x8}/artifacts.sha256` and `identity.log`.
  - **Edited:** `HANDOFF-r5.md` (this status, and the bitstream bullet R866-4 cited), `PR-BODY.md` (its status bullet
    on the gating bitstreams), and `INDEX.md` (regenerated).
- **Untouched:** the pushed branch, the head `8dc85884`, every source, the routes and the bitstreams. The R865-4 review
  is undisturbed.

## Status (END, 20:2x, 11-20; the head and verdicts, unchanged): FINAL HEAD `8dc85884`. ITEM 4 APPLIED AT 1x1/1if AS THE OWNER DECIDED; THE SLICE RULE TAKES 950 us AND THE QUEUED FIGURE 130 ms; EVERY OWNER BOUND HOLDS; THE GATES PASS; THE TWO GATING BITSTREAMS ARE READY

**Final head `8dc85884` on `flip-train-1117-p11`** (composed in the scratch clone `p11`, fetched into the lane;
nothing pushed, nothing posted). The gitlinks stay `1616fc8f` / `801ef228`. The lane worktree stays on
`flip-train-1117-p10`, clean.

| Commit | What |
|---|---|
| `8c5e2b4f` | Ruling item 4 at 1x1/1if (#665 issuecomment-7044585511), the prepared patch: the AECP notice item 210 -> 150 us and the long notice 365 -> 315, from their measurement; the map edit 315, SET_STREAM_INFO 250, ADP's donor record 105 and the centisecond 170, by the rule. Then what follows from them: the slice rule's 950 us (was 900) and the queued rule's 130 ms (was 140; the owner's bound stays 140). Five controls re-anchored to the rows; the docs |
| `8dc85884` | Docs only: the design doc records the re-measure, and its summary states 950 us and 130 ms |

**The verdicts. Every owner bound holds.**
- **1x1/1if, measured again in full at `8c5e2b4f`** (64 of 64 parts at rc 0, `CPU-TABLE-8c5e2b4f.md`):
  - 0 of 68 statements are exceeded, and the AECP records by class PASS.
  - The costs are `92de01f7`'s cycle for cycle, except the centisecond, 15,672 (15,976), and ACMP's event, 13,859
    (13,781), which the slice's scheduling moves.
  - The groups: 241, with 0 refusals and 0 of 388,313 passes over the share. The only misses are the seven held-egress
    rows (tsn-c-stack #26), as before.
  - The rows by every source:

    | R4 | R5 | R6 | first | last | R4L | ACMP | ADP | MAAP | tx | txL | load |
    |---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
    | 13.26/20 | 73.88/90 | 69.75/90 | 14.69/20 | 127.31/130 (owner 140) | 203.48/238 | 29.06/30 | 27.51/30 | 27.61/30 | 33.44/49 | 47.88/49 | 0.5114/0.70 |

- **8x8/1if:** not re-measured. Its CPU-budget and product images are byte-identical, and no statement it reads moved.
  So `92de01f7`'s measurement stands: 0 of 68 exceeded, and the load 0.7436 of the owner's 0.75. Its projected rows
  equal `92de01f7`'s.
- **8x8/2if:** the base's findings, reported and not held, unchanged.

**The gates at `8c5e2b4f`: ALL PASS,** with the previous heads' exceptions (detail below). At `8dc85884` the docs
checks pass and `git diff --check fb083864 8dc85884` is clean. Only `SPLIT_CONTROL_MEMORY.md` differs from `8c5e2b4f`.

**THE GATING BENCH BITSTREAMS** (of `8c5e2b4f`, which are `8dc85884`'s inputs; `--eth-port e2`; the gating lane's
recipe; both through `vivado-slot.sh`):

| Point | Bitstream | sha256 | #818's floor (Slow WNS/WHS, Fast WNS/WHS) |
|---|---|---|---|
| 1x1/1if | `<scratch>/gate15/work/g1x1/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit` | `c7189218a128b71d632edc82157ea6f31b303383a6fe302d50265ad816332a28` | +0.131/+0.102, +1.636/+0.036 ns: met |
| 8x8/1if | `<scratch>/gate15/work/g8x8/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit` | `7d90341299cc65e8c0da249139471a61019255132b66d5207ef9ffb4a5d0b773` | +0.176/+0.102, +1.523/+0.036 ns: met |

**Housekeeping:**
- **Receipts:** `receipts/step16/` (gates, images, measure, gating, item4b), sanitized, 0 residual host tokens.
  `INDEX.md` is regenerated: 3,692 files, 199,736 B. The privacy scrub finds 0 findings over 3,693 files.
- **Scratch:** 31 GB. Superseded build trees were removed, each logged in `disk-cleanup.log`. The new measure's
  logs are gzipped.
- **Units:** no unit of this lane is running. The two-hour re-pin loop reached its tool time limit at 19:5x, one part
  before the measure's end, and was not restarted.
- **For the bench:** both bitstreams are of this head and new to the bench. At 1x1/1if the firmware carries the
  950 us slice. At 8x8/1if the firmware is the SRP cut's head's, byte for byte (its product image equals
  `fb083864`'s).

### The detail behind the 17:5x-18:3x updates (kept)

- **Head `8c5e2b4f`** on `flip-train-1117-p11`, one composition fix on `fb083864`. It contains item 4's patch as
  prepared, with each statement's comment naming #665 issuecomment-7044585511.
- **The consequence the patch did not show:** at the restated statements, #894's slice rule (`rows_tiers.ruled`, "the
  slice the tree must state at 1x1/1if") takes **950 us**, not the 900 the header stated.
  - The patch's own grading had shown this as the escaped control "the built design's slice not the rule's". That
    control is the only check of the ruling, so it was not re-anchored: the tree now states the rule's slice.
  - At 950 us the last queued notice's row is 127.31 ms, and the queued rule makes `CTRL_LOOP_QUEUED_MS` **130**, not
    the 135 asked for. 135 is refused at 950 (`queued_bound.controls`), and 900 is refused by the slice rule.
  - The owner's 140 ms bound does not move.
- **Projected 1x1/1if rows** at the cut's measured costs: last 127.31 of 130, ACMP 29.06 of 30, txL 47.88 of 49. All hold.
- **The controls:** five re-anchored (three as foreseen, two new from 130 = 8x8/1if's 130), none weakened.
  - THE TRANSMIT's control (in `rows_tiers` and `flip_grade`) is now planted one under its row rounded up, not one
    under the statement. 35 ms now stands over the 33.44 row.
  - The shape table's queued fallback control plants its own table apart.
  - run.py's queued-constants check now reads (130, 130, 62).
  - All three self-tests refuse every plant: 616/616, 1033/1033 and 25/25. Each re-anchored control still escapes
    against a blinded or off-by-one detector.
- **The images (18:0x):**
  - The 8 CPU-budget images at 8x8/1if and 8x8/2if are byte-identical to `fb083864`'s.
  - The 4 at 1x1/1if differ, each in 10 bytes: five `addi`/`li` immediates (900 -> 950, and the values derived from
    it). Their sections, symbols and data are equal, so the layout does not move.
  - The product images: `8x8-if1` `c6355962…`, `8x8-if2` `28f9129d…` and `1x1-if2` `747c2772…` are byte-identical.
    `1x1-if1` is now `fe12a3f1…`, with the same five immediates as its only change. The ledger passes, controls 9 of 9,
    and 8x8-if1's ROM is still 139,208 of 139,264.
  - No changed statement is shared with 8x8/1if (`poll_grade.ONE` is 1x1/1if's own), so 8x8/1if is not re-measured.
- **THE GATING BENCH BITSTREAMS OF `8c5e2b4f`, READY (18:2x).** Built with the step-12b recipe: the gating lane's
  `gprep.sh`/`gbuild.sh` with only the scratch path changed, `--eth-port e2`, ExtraPostPlacementOpt, through
  `vivado-slot.sh`, both at once.
  - **1x1/1if:** `<scratch>/gate15/work/g1x1/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
    - bitstream sha256 `c7189218a128b71d632edc82157ea6f31b303383a6fe302d50265ad816332a28`;
    - platform image `ctrl_app.elf` `c873a0aa8b9c39a003d7a78616c83d6469935debb5bb1107ad477b900ee607fb`, AEM blob
      `bdfde7cf…`;
    - #818's floor met at every corner: Slow WNS +0.131 / WHS +0.102 ns, Fast WNS +1.636 / WHS +0.036 ns;
    - the identity gate passes, and the split boot simulation passes on its clone.
  - **8x8/1if:** `<scratch>/gate15/work/g8x8/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
    - bitstream sha256 `7d90341299cc65e8c0da249139471a61019255132b66d5207ef9ffb4a5d0b773`;
    - platform image `ctrl_app.elf` `d67fd049a9d20b6522a635cb4aa7d6abc536e61ec036cc0c32485c64f69af0c4`, AEM blob
      `723225a5…`;
    - #818's floor met at every corner: Slow WNS +0.176 / WHS +0.102 ns, Fast WNS +1.523 / WHS +0.036 ns;
    - the identity gate passes, and the split boot simulation passes on its clone.
  - **Their firmware is the head's.** The loaded sections (`.text`, `.rodata`, `.data`) are byte-identical to the
    ledger's link of the head's product images. Their rom words' sha256 is 1x1/1if `1fd5bc47…` and 8x8/1if
    `ac014c6a…`, the same on both sides and in the build's rom init files.
    - **The two-sided receipt** (R866-4-F1) is `receipts/step16/gating/loaded-identity/`, with its README. It covers
      every loaded section's VMA, LMA, length and full sha256 on each side, every PT_LOAD, and why the whole files
      differ (`.symtab` order alone).
    - **The manifests** are in `receipts/step16/gating/<point>/build/`, with their artifact lists.
    - **The bench list's section** is `receipts/step16/gating/bench-images-8c5e2b4f.txt`. The original
      `../fg4-bench-images.txt` lies outside the packet.
- **The gates at `8c5e2b4f`: ALL PASS, with the same exceptions as the previous heads** (`receipts/step16/gates/`).
  - **The four firmware shards:** all PASS. The control campaign catches 826 of 826, as at `92de01f7`, and no plant is
    removed.
  - **Also PASS:** `fw_coverage --check` (40 files); the twin and its plants; `avtp_rxmon`; the split boot simulation
    at both shapes; `ctrl_boundary` twice (the full run: 0 findings, 117 boundary, 185 pin and 4 figure controls; and
    `--only verilator`: 0 findings); the ledger (9 of 9 controls); run.py `--self-test` (0 failures); `load_grade`
    `--check` and `--selftest` (28 of 28); `flip_grade --selftest` (616 of 616); `flip_grade --check --point 1x1/1if`;
    `rows_tiers` (1033 of 1033); `shape_costs` (25 of 25); `record_classes`; the docs, style, paths, TOC and anchors,
    em dash, hygiene, the Python and C++ idioms, `docs_inventory` and the generated checks.
  - **The exceptions, unchanged:** `flip_grade --check` reports the base's findings at 8x8/2if, reported and not held.
    Its 8x8 rows equal `fb083864`'s line for line. `ci_tool_inventory_check` is CI-environment-bound. The docs
    workflow list fails the same environment-bound rows as at `92de01f7`.
  - **The release export:** byte-identical where loaded (`bios.bin` `603b9ca3…`, the AEM blob `bdfde7cf…`, the
    ROM/SRAM/mem init files), and the Verilog is equal outside its comments.
- **Running:** the full 1x1/1if re-measure at `8c5e2b4f` (CPUs 0-63, from 17:50, about 2 h; the measured images match
  the image build).

## Status (16:5x, 11-20; superseded above): THE SRP CUT LANDS; 8x8/1if HOLDS 0.75. STOP AT 1x1/1if: TWO OWNER BOUNDS BREAK BY THE USUAL RULE, AND ITEM 4 WOULD BE THE ONLY THING HOLDING THEM

**Head `fb083864` on `flip-train-1117-p11`** (composed in the scratch clone `p11`, fetched into the lane; nothing pushed):

| Commit | What |
|---|---|
| `92de01f7` | The SRP cut (#665's ruling of 2026-11-20, `RULING-1120.md`, item 3), `srp_mbx.c`, each change exactly equivalent: lwSRP's reclaim owed only where an attribute may be freed; the receive filter's sink pass made only from a Talker indication on; a Listener looked up among the sources once a use (`sources_of`); the walk-free snapshot's capture made in place. `srp_listeners.cpp`'s differential against the adapter before the cut and four direct tests; 10 plants (`srp_reclaim_mutants.py`) |
| `fb083864` | Two existing SRP plants re-targeted where the cut leaves their defects observable; tests only |

**The full CPU re-measure at `92de01f7`** (`CPU-TABLE-92de01f7.md`):
- **The run:** every arm and group, 64 parts a point, 128 of 128 at rc 0.
- **The crash:** the host crash of 13:31 cut 8x8/1if mid-run. Its unfinished 55 parts re-ran on the arms' own builds,
  whose image hashes are the measured ones.
- **Identity:** `fb083864`'s CPU-budget images (all 8 arms at both points) and its four product images are
  byte-identical to `92de01f7`'s.

**8x8/1if: PASS. The cut lands.** 0 of 68 statements exceeded.

| Cost | `c1e95dc1` | `92de01f7` | By the rule | Stated |
|---|---:|---:|---:|---:|
| `record.srp` | 35,846 | **34,803** | 370 us | 375 |
| `item.record` (held to `item.retained`) | 35,536 | **34,550** | 365 us | 375 |
| `item.reclaim` | 3,840 | **995** (`none`'s `srp`; 0 in `srp-talker-held`) | 15 us | 40 |

- **The margins:** `record.srp` is 911 cycles (2.6 %) under 375 us's 35,714, and `item.reclaim` 2,814 under 40's.
- **The load:** 0.7436 against the owner's 0.75, no statement restated.
- **THE TRANSMIT's held line:** tx 76.81 ms against 77.

**1x1/1if: STOP.** 3 of 68 statements are exceeded by the rule, and two AECP records by class are over theirs:

| Cost | `c1e95dc1` | `92de01f7` | By the rule | Stated |
|---|---:|---:|---:|---:|
| The paced map edit (REMOVE_AUDIO_MAPPINGS), held | 29,468 | **29,993** | 315 us | 310 |
| SET_STREAM_INFO (0x000e), held | 23,167 | **23,726** | 250 us | 245 |
| `record.adp` (the graded column) | 8,901 | 9,585 | 105 us | 100 |
| `centisecond` | 13,011 | 15,976 | 170 us | 150 |

Why they moved:
- **The two AECP records:** the cut does not touch AECP, so they moved by layout alone, the cut's 284 bytes of code.
- **`centisecond` and `record.adp`:** the cut's own cache effect. Without the reclaim walk warming lwSRP's attributes
  each pass, 1x1/1if's records and ticks take those refills. Its `record.srp` rose 23,153 to 24,662, still 260 us of
  285.

The owner bounds (`project.py`, each statement planted; `step15/measure/project-verdicts-92de01f7.txt`):

| Bound | Point | As stated | The usual rule (the four raised) | And item 4 too | Bound |
|---|---|---:|---:|---:|---:|
| The last queued notice | 1x1/1if | 137.97 ms | **141.53, OVER** | 132.93 | 140 (135 with item 4) |
| ACMP | 1x1/1if | 29.93 ms | **32.74, OVER** | 29.01 | 30 |
| txL | 1x1/1if | 48.89 ms | 48.98 | 47.83 | 49 |
| The load | 1x1/1if | 0.5224 | 0.5234 | 0.5114 | 0.70 |
| The load | 8x8/1if | 0.7436 | 0.7436 | 0.7436 | 0.75 |
| THE TRANSMIT's held line | 8x8/1if | tx 76.81 ms | as stated | as stated | 77 |
| The load | 8x8/2if | 0.7988 | reported, not held: the base's finding, as before | | 0.70 |

- **What breaks them:** the two AECP records. The map edit at 315 alone takes last to 141.39. SET_STREAM_INFO at 250
  alone takes last to 141.45 and ACMP to 32.72.

**Why nothing is restated for 1x1/1if** (a conflict published for the owner, not chosen here):
- Ruling item 4 restates the two notice-path statements because "the rows already hold", and "it is not used to pass
  a missed bound".
- At this head the rows hold by the usual rule only with item 4, so applying it would pass two missed bounds.
- The standing instruction is not to restate around a broken owner bound but to STOP with the figures.

**What item 4 would take** (prepared in a scratch clone and not committed; `receipts/step15/item4/`):
- **The statements:** the AECP notice item 210 → 150 us (14,084 cycles); the long notice 365 → 315 (29,652); and the
  four raises above.
- **The queued bound:** its own rule takes `CTRL_LOOP_QUEUED_MS` 140 → 135 at 1x1/1if (`queued_bound.py`). The firmware
  code does not read it, but the CPU harness's notice windows do, so those groups would want measuring again.
- **The self-tests:** one `flip_grade` control and two `rows_tiers` controls tied to the old statements escape, so
  they would need re-anchoring.
- **The check:** `flip_grade --check --point 1x1/1if` then PASSES: last 132.93 of 135, ACMP 29.01, txL 47.83.

**The owner's options as they stand:**
- (a) Allow item 4 here: the patch, the controls and a re-measure of the notice windows.
- (b) A further AECP cut, or a layout-neutral cut, to bring the two records back to 310 and 245.
- (c) The 1x1/1if bounds themselves.

**The gates at the head: ALL PASS, with the same exceptions as step 12.**
- **The four firmware shards:** shards 0 to 2 at `92de01f7` (826 of 826 control plants). Shard 3, the SRP campaign,
  at `fb083864`'s content: the cut's 10 plants in all three campaigns, and the two re-targeted ones.
- **The other suites:** `fw_coverage --check` PASS (40 files; `srp_mbx.c` 100 % of its counted branches). The twin
  and its plants, the receive monitor, and the split boot at both shapes PASS.
- **The firmware boundary:** PASS in both runs: 3,849 sources `--without verilator`, 1,240 `--only verilator`.
- **The ledger:** PASS at every point. 8x8/1if's product ROM is 139,208 of 139,264 B, 56 B spare. No RAM grows.
- **Docs, generated checks and `git diff --check`:** PASS. The CI-environment-bound set is the same as before, and
  `flip_check`'s output is identical to the step-14 head's.

**The images:**
- **The release:** byte-identical where loaded (`bios.bin`, the AEM blob, the ROM, SRAM and memory init files). The
  Verilog is equal outside its comments.
- **The split product images** (sha256): 1x1/1if `f6a575ae752cc376…`, 1x1/2if `747c2772344aaf43…`, 8x8/1if
  `c635596216d95671…`, 8x8/2if `28f9129dfe8bce1f…` (full hashes in `receipts/step15/`).
- **The split gateware: UNCHANGED at both points.** The same rom bank depths, the Verilog equal outside its comments,
  the constraints equal; only the rom init (the firmware) differs. So no routes are owed.

**A finding for its own Issue:** the walk-free snapshot's copy of a continuing kind is covered by no test, before the
cut as after (RESOLUTIONS).

---

## Status (04:3x, 11-20; superseded above): STOP. AN OWNER BOUND BREAKS: 8x8/1if's LOAD AT 0.751 OF 0.75. ATTRIBUTED: #953 CROSSES THE LOAD; record.srp WAS OVER BEFORE IT; #951 ADDS NOTHING

### The attribution experiment (the manager's resume of 02:3x, 11-20)

No commit to p11. Scratch clones only, the head unchanged.

**The method:**
- **The group:** 8x8/1if's valid-destinations arm, its `srp-talker-held` group alone.
- **The build:** as the full re-measure built it (`legs.py build`: CPU regions cover, the split placement's L1, no
  XIP).
- **The runs:** three repeats per image on one build, at once, on booked CPUs.
- **The reading:** each repeat surveyed alone by the full re-measure's reading (`survey_point4.py`, round 28's tools).
- **The notice path:** the same, in the answering-ports arm, with its two notice groups (`aecp-fanout` for the AECP
  notice item, `aecp-largest-notice` for the long notice).
- **Two images added:** D separates #953 from what came before it, and E separates #951's value from its layout.

| Image | Tree | `ctrl_app.elf` (valid-destinations) | `.text` |
|---|---|---|---:|
| A | `c05d5acb`: step 13 (#953), no #951 | `8b319d57eac48cd9` | 0x198ec |
| B | `c1e95dc1`: the head (steps 13 and 14, the boundary fix) | `ed5857d33591c64e`, the full re-measure's own | 0x198f0 |
| C | B with only `SRP_REDECLARE_CS` at step 12's expression (2,027 cs) | `8b319d57eac48cd9`: **byte-identical to A** | 0x198ec |
| D (added) | `01765bb0`: step 13's first parent, before #953 | `ebf4d51bd31740ab` | 0x197d4 |
| E (added) | B with only `SRP_REDECLARE_CS` at 2048u | `15c27a842628fc02`: **2 loaded bytes from B**, the immediate; every symbol at B's address | 0x198f0 |

**The figures.** The spread is **0**: all three repeats of every image agree to the cycle, on every figure and on
the run's whole summary.
- Each cell is cycles, then the rule's microseconds in brackets, then the stated figure.
- The rule's bounds: 375 us allows at most 35,714 cycles, and 40 us at most 3,809.

| Image | `record.srp` | `item.reclaim` | `item.retained` | AECP notice item | Long notice | 8x8/1if load, restated by the rule | The same, with the AECP notice item as it now costs |
|---|---:|---:|---:|---:|---:|---:|---:|
| U (`unit375`, round 5's candidate) | 35,547 (375) | 3,562 (40) | - | - | - | 0.744 | - |
| D | 35,831 (**380**) / 375 | 3,418 (40) / 40 | 35,634 (375) / 375 | 13,183 (140) | 29,199 (310) / 320 | **0.7461**, within | 0.7191 |
| A | 36,114 (**380**) / 375 | 3,838 (**45**) / 40 | 35,800 (**380**) / 375 | 13,461 (145) | 29,605 (315) / 320 | **0.7517, OVER** | 0.7257 |
| C | = A | = A | = A | = A | = A | **0.7517, OVER** | 0.7257 |
| B | 35,846 (**380**) / 375 | 3,840 (**45**) / 40 | 35,536 (375) / 375 | 13,497 (145) | 29,498 (310) / 320 | **0.7512, OVER** | 0.7252 |
| E | = B | = B | = B | (not run) | (not run) | 0.7512, OVER | 0.7252 |

The loads come from #955's `project.py` at the head's rules, with each image's exceeded statements planted
(statements are never lowered). A's and D's own trees' rules give the same figures. As stated, the load is 0.7436 at
every image.

**The attribution:**
- **#951 by its value (C against B):**
  - `record.srp` −268 cycles, `item.reclaim` +2 and `item.retained` −264.
  - All of it is layout. E has B's layout, and its hold-off acts in this group as A's does. E equals B to the cycle over
    the whole run: the simulated and CPU cycles, instructions, ROM fetches and every pass count.
  - The group runs 17.9 s simulated. No hold-off runs out in either image: 2,027 cs is 20.27 s and 3,027 cs is 30.27 s,
    and `held_cs` is only set, decremented and tested against 0.
  - The value acts by its encoding alone. 3,027 needs `lui` + `addi` where 2,027 fits one `li`: 4 bytes more `.text`,
    with 358 of 614 symbols moved.
- **#951's layout without its value (A against C):** nothing. The images are byte-identical.
- **#953 (D against A):**
  - `item.reclaim` +420 cycles, 3,418 to 3,838: 40 to **45 us**.
  - `item.retained` +166, to 380 us, and `record.srp` +283.
  - **This is what crosses the load: 0.7461 at D, 0.7517 with #953.**
  - #953 changes only the AECP path (`ctrl_app_aecp.c`'s STREAM_OUTPUT answer, `aecp_commands.c`, `aecp_maps.c`) and
    adds 280 bytes of `.text`. This experiment does not separate its work from its layout.
- **Before #953 (U against D):**
  - **`record.srp` is already over at D:** 35,831 cycles, 117 past 375 us, and +284 on U's 35,547.
  - U to D spans step 11 (#939), step 12 (#947) and the F-G5 fix. No CPU measurement was owed between them.
  - At D the only break is bookkeeping: `CTRL_LOOP_SRP_UNIT_US` and `OWN_MEASURED`. The load restated is 0.7461,
    within.
- **So `record.srp` moves about ±300 cycles with layout alone** (B, C and E run the same SRP logic), against U's
  167-cycle margin.

**The two notice-path statements, as they now cost:**
- **The AECP notice item:** 140 to 145 us at every image.
  - 8x8/1if's load takes 8x8/2if's 275 us as its NEAREST point's, and OWN only raises.
  - If 8x8/1if's own measured item entered its load instead, the loads would be 0.7191 (D), 0.7257 (A, C) and 0.7252
    (B, E): **all within 0.75**, `record.srp` and `item.reclaim` restated as above.
  - The plant moves 8x8/2if's own load too (0.7988 to 0.7728). Only the 8x8/1if figure is read here.
- **The long notice (`aecp_long`):** not a term of 8x8/1if's load. It is graded against its own 320 us, and measures
  310 to 315 us at every image, within.

**The STOP stands:** with #953, the load restated by the rule is over 0.75 at every image. The receipts are
`receipts/attr/`: per image, its head, edit, build and each repeat's survey; `images.txt` with the comparison and the
disassembly; and the projections.

### The STOP (02:4x, 11-20), unchanged

**HEAD `c1e95dc1` on `flip-train-1117-p11`** (composed in the scratch clone `p11`, fetched into the lane repo; nothing
pushed). The full CPU re-measure is complete at both points. **No statement is restated:** restating the two 8x8/1if
costs the measurement exceeds would break the owner's 0.75 load ceiling, and the instruction is not to restate around
a broken owner bound. The owner decides between the options in #955's STOP.

**Why it is a STOP.** At 8x8/1if two stated costs are exceeded by the rule. Both are in the valid-destinations arm's
`srp-talker-held`, the group #951's `srp_mbx.c` change runs through:

| 8x8/1if cost | Measured at `c1e95dc1` | By the rule | Stated | At `unit375` (round 5's measured candidate) |
|---|---:|---:|---:|---:|
| `record.srp` (its own, `load_grade.OWN`; `CTRL_LOOP_SRP_UNIT_US` follows it) | 35,846 cycles | **380 us** | 375 | 35,547 (375 us) |
| `item.reclaim` (`poll_grade` (1, 9, 9)) | 3,840 cycles | **45 us** | 40 | 3,562 (40 us) |

The load gate's rule, held by the flip check's own rules at this head (#955's `project.py` with each statement planted):

| 8x8/1if load | Figure | Ceiling (owner) | Verdict |
|---|---:|---:|---|
| as stated | 0.7436 | 0.75 | within |
| `record.srp` 380 alone | 0.7461 | 0.75 | within |
| `item.reclaim` 45 alone | 0.7487 | 0.75 | within |
| **both, as the rule owes** | **0.7512** | 0.75 | **OVER** |

Nothing else breaks with both restated:
- 8x8/1if's held THE TRANSMIT line is 77 ms against a tx row of 76.84 ms.
- Its first notice is 19.07 of 20 ms.
- The 1x1/1if rows and loads are unchanged.

The two other findings the restatement raises are the commit's own bookkeeping, which a restatement would carry:
- `CTRL_LOOP_SRP_UNIT_US` must follow its record, 375 → 380. That changes 8x8/1if's firmware, so the image would need
  measuring again.
- `OWN_MEASURED` must name the new measurement.

**The full CPU table** is in `round5/CPU-TABLE-c1e95dc1.md`: every stated cost at both points against its measurement,
with the long notice and the records by class. 1x1/1if: 0 of 69 statements exceeded. 8x8/1if: the two above.

**The owner bounds, as the image is measured (statements as stated; the restatements' effect beside them):**

| Bound | Point | Figure | Bound | Verdict |
|---|---|---:|---:|---|
| The last queued notice | 1x1/1if | 137.97 ms | 140 | within (+2.03) |
| ACMP | 1x1/1if | 29.93 ms | 30 | within (+0.07) |
| txL | 1x1/1if | 48.89 ms | 49 | within (+0.11) |
| The load | 1x1/1if | 0.5224 | 0.70 | within |
| The load | 8x8/1if | 0.7436 as stated; **0.7512 restated by the rule** | 0.75 | **OVER once restated** |
| THE TRANSMIT's held line | 8x8/1if | tx 76.81 ms (76.84 restated) | 77 (at most 80) | within |
| The rows by every source | 8x8/1if | reported, not held (owed to #872), as before | | as before |
| The load | 8x8/2if | 0.7988 | 0.70 | over: the base's known finding, reported and not held, as at step 12 |

**The figures #955's STOP asks for** (this image; the AECP records by class, `record_classes.py`, PASS at both points):

| Figure | Point | Measured | By the rule | Stated | Note |
|---|---|---:|---:|---:|---|
| The map edit (REMOVE_AUDIO_MAPPINGS, paced), held | 1x1/1if | 29,468 cycles | **310 us** | 310 | at its statement. #955: last breaks from 312 us |
| The map edit in the declaring-outputs arm, **reported, not held** | 1x1/1if | 30,232 | **320 us** | 310 | that arm holds only records that ran a completion. If held: last **141.47 ms, over 140** |
| The held SET_STREAM_INFO (0x000e) | 1x1/1if | 23,167 | **245 us** | 245 | at its statement. #955: ACMP and txL break at 260 |
| The largest legal command, held | 8x8/1if | 163,497 | **1720 us** | 1720 | at its statement. The declaring-outputs arm reports 1765 and 1725 us, not held; no row moves (#955: none from 1,850) |
| The largest legal command, held | 1x1/1if | 91,625 | 965 us | 975 | within |
| The AECP notice item (stated 210 us) | 1x1/1if | 14,111 | **150 us** | 210 | #955's option (a) restates it to 150 |
| The long notice (stated 365 us) | 1x1/1if | 29,780 | **315 us** | 365 | #955's option (a) restates it to 315 |
| The long notice | 8x8/1if | 29,498 | 310 us | 320 | within |

So at 1x1/1if the margins #955 projected are exactly where this image sits:
- **The map edit and SET_STREAM_INFO:** the held map edit and the held SET_STREAM_INFO each measure at their
  statements.
- **The unheld map edit:** the declaring-outputs arm's unheld map edit is 10 us past its statement, which would break
  the last row if it were held.
- **The two notice-path statements:** they are 60 and 50 us above their measured costs, the room #955's option (a)
  takes.

**The measurement:**
- **Where and when:** `c1e95dc1`, every arm and group, 64 parts a point on CPUs 0-63 (booked through `cpu_ranges.py`;
  re-pinned against the host's affinity reset), one point after the other.
  - 1x1/1if: 21:08 to about 23:10.
  - 8x8/1if: 23:22 to about 02:00.
- **Parts:** 128 of 128 at rc 0.
- **Budget misses:** the only ones are the known owed-frame backlog row's (62-64 ms against 20), recorded and not held,
  as at step 10.
- **Raw logs:** kept, gzipped (`gunzip` before any `--regrade`).

| Commit | What |
|---|---|
| `c05d5acb` | Step 13: #953 (#943) at its frozen head `a16899b1` (R871-2 and R872-2 POSITIVE). Auto-merged, no conflict; both sides kept |
| `4b9f66c5` | Step 14: #952 (#951) at `f09d82e0` (R869-1 POSITIVE; R870-2 NEGATIVE pending this re-measure). Auto-merged, no conflict; both sides kept |
| `c1e95dc1` | Composition fix: `sink_mutants.py` (#946) and `talker_notice.py` (#936) classified in `ctrl_configs.py`'s `OUTSIDE`, as the boundary gate's taxonomy says for builders found by text that compile nothing |

**The gates at `c1e95dc1`: ALL PASS, with the same exceptions as step 12** (`receipts/step14/`):
- **The four firmware shards:** PASS.
  - The control campaign catches **826 of 826**.
  - The AECP campaign catches **385**, #943's 14 output plants among them, with 0 escaped.
  - The SRP shard catches 513 with 0 escaped, #951's plants among them.
- **Coverage, suites and boot:** `fw_coverage --check` PASS (40 files). The twin and its plants PASS, the receive
  monitor PASSES, and the split boot simulation at both shapes PASSES.
- **The firmware boundary** (`ctrl_boundary.py --require-rv32 --selftest`): **PASS** in both runs. `--without verilator`
  judged 3,849 sources, and `--only verilator` 1,151.
- **The ledger:** PASS with 9 of 9 controls. Every point holds its entry: 1x1 45 and 46, 8x8/1if 58.0 and 8x8/2if 63.0,
  each with about 280 B more `rom`, all S14 debt as before. `test_ctrl_memory.py` has 0 failures, and the size
  fixture's six arms build.
- **Docs, generated checks and `git diff --check`:** PASS, but the CI-environment-bound set, the same as before.
  `flip_grade --check`'s output is identical to step 12's (8x8/2if's base eleven, reported and not held).

**The images:**
- **The release:** byte-identical where loaded. `bios.bin`, the AEM blob and the ROM, SRAM and memory init files are
  EQUAL; the Verilog is equal outside its comments.
- **The split product images** (sha256):
  - 1x1/1if `ace8644e0fb5e4e2e90ba14833c8b51ff2e6dea9ebf0848d05b15ff3569583ad`;
  - 1x1/2if `402a759dd9067384a7742a5b4ab26d8097cc4cdf9093211c51a53e46611fe939`;
  - 8x8/1if `cf14a5f649f2d6c467a3c4c7af6906555a09be9fd9422ad72e6fd626c5c9c03d`;
  - 8x8/2if `1845007c2c46e803cacfdac19c2d78d163d0d0c6639ac6c4436efbd118a2b0f0`.
- **The split gateware: UNCHANGED at both points**: the same rom bank depths, the Verilog EQUAL outside its comments,
  and the constraints EQUAL against `01765bb0`'s export. So no routes are owed.

**The arms measured:** arm A, then answering-ports (all 100 groups), answering-every-port, valid-destinations,
answering-later, shutdown-entry, talker-notices and #953's declaring-outputs, every group of each, at 1x1/1if and
8x8/1if. The figures are at the top of this status and in `round5/CPU-TABLE-c1e95dc1.md`; the receipts are
`receipts/step14/measure/`.

---

## Status (14:0x, 11-19; superseded above)

**F-G5: HEAD `01765bb0` on `flip-train-1117-p11`, the composition fix on `0839453f`.** It was composed in the scratch
clone `p11` and fetched into the lane repo. Nothing is pushed.

- **The cause:** the boot restore judged a saved stream format by the datapath's verdict. Its bit 1 ("every mapped
  channel kept") reads the datapath's map store, and before the face opens that store still holds its reset set.
  - At 1x1/1if that set maps input 0's 8 channels, so the narrowed 1-ch format got verdict 1 and its restore was
    refused (`NVM_REFUSED`). The 8-ch default stayed, and the saved empty map was restored after it.
  - At 8x8/1if input ports have no reset mappings, so the restore was taken.
  - Not the other suspects: the format list (bit 0 admits 1 ch), the restore order, or #947's context writes (1x1 has
    no contexts, and the NVM mark precedes the wrapped port).
  - Full analysis in RESOLUTIONS.md.
- **The fix:** `aecp_face.c`, `format`. Before the open, bit 1 is not read; from the open on, exactly 3 as before.
- **The tests**, each FAILING by name on `0839453f` and passing with the fix (`receipts/fg5/before.log`,
  `after.log`):
  - `Sinks.S12ANarrowedInputFormatIsKeptAcrossAPowerCut`: it FAILS at 1x1/1if and PASSES at 8x8/1if, the bench's
    pattern. Its far model keeps the map store as the RTL does.
  - `Face.BeforeOpenAFormatVerdictJudgesSupportAlone`.
  - Three plants, and a `platsinks1` arm.
- **The gates at `01765bb0`: ALL PASS, with the same exceptions as step 12** (`receipts/fg5/`):
  - **The four firmware shards:** PASS. The control campaign catches **826 of 826**, the new
    `restore-format-survival-read` among them, caught by S12 in `platsinks1`. The AECP campaign catches **368**, with
    **0 escaped**, its two new face plants among them.
  - **Sinks:** 12/0 at both shapes.
  - **`fw_coverage --check`:** PASS (40 files).
  - **The twin and its plants**, the receive monitor's suite, and the split boot simulation at both shapes: PASS.
  - **The ledger:** `plat_ledger.py --self-test` PASS, 9 of 9 controls. Every point holds its entry: 1x1 45 and 46,
    8x8/1if 58.0, 8x8/2if 63.0, each with 16 B more `rom`.
  - **The quick lists** (docs, style, paths, TOC, hygiene, idioms, inventory, generated checks, `run.py --self-test`,
    `load_grade`, `ctrl_memory`): PASS, but the same exceptions as at `7650a02d`. `flip_grade --check`'s output is
    identical (the base eleven at 8x8/2if), and the CI-environment-bound set is the same.
  - **`git diff --check`:** clean.
- **The images:**
  - **Release:** byte-identical where loaded. `bios.bin`, the AEM blob and the ROM, SRAM and memory init files are
    EQUAL, and the Verilog is equal outside its comments.
  - **Split platform images:** CHANGED at every point, 16 B more `rom` each, within every ledger entry:
    - 1x1/1if `86c6f802…`;
    - 1x1/2if `5091687e…`;
    - 8x8/1if `e814cce6…`;
    - 8x8/2if `e3b62740…`.
  - **The 12 CPU budget images:** CHANGED, because `aecp_face.c` is linked into them. In their hot region the
    addresses and opcodes are identical, and 72 instructions differ only in immediates: cold code and `.rodata` moved
    16 B. In the budget harness the format port's window is never answered, so the changed expression is never
    reached. Yet the layout moves the measured timing, because cold code and `.rodata` shift under the split's
    caches.
  - **The CPU budget: DECISION NEEDED.**
    - **The confirmation:** step 11's seven groups were re-run on the new images (`receipts/fg5/confirmation/`).
      They are all **within bound**: 0 budget misses in every group, every slice under its stated figure, every join
      in 181-239 ms, the save durable within its worst case, and the same work-pass counts over the share.
    - **But the figures move**, up and down, by up to about 5%, against step 11's confirmation:
      - 8x8/1if `srp-talker-held`: SRP's records 129,393 → 133,080 cycles (slice 147,500), THE TRANSMIT's build
        132,085 → 132,171, the longest pass 109,204 → 109,457.
      - 8x8/2if `aecp-fanout`: THE TRANSMIT's build 28,881 → 30,439, the longest pass 72,457 → 73,449.
      - 1x1/1if `aecp-fanout`: the longest pass 21,424 → 21,590.
    - **What follows:** the rows do not carry byte for byte. Re-establishing every row and the restated figures (among
      them 8x8/1if's SRP record at 375 us and THE TRANSMIT at 77 ms, the held line 76.81 of 77 ms) needs the full
      measurement at every point.
    - **My recommendation:** measure once, at the final head after steps 13 and 14, since #943's bridge change and
      #951's `srp_mbx.c` change move the same measured path again.
    - **Scratch:** the full measurement needs about 7 GB, so it needs the round-4 measurement trees (`r4meas`, 16 GB)
      cleared first, which I have not done without your word.
    - **Not done:** the full measurement at `01765bb0`.
  - **Gateware: UNCHANGED at both points, so no split routes are owed.** The platform-image export at `01765bb0` was
    compared with round 2's (`gateware15.py`): the same rom bank depths, the Verilog EQUAL outside its comments, and
    the constraints EQUAL. Only the banks' init, the firmware, differs.

**Plan: steps 13 and 14, when the manager says.** Both lanes branch from `0839453f`, and both merge clean onto
`01765bb0` by `git merge-tree`. #951 also merges clean onto the predicted step 13.
- **Step 13, #943** (lane `943-out-status`, A800; at its reviewed head, now `8f077ee4`, 5 commits, 10 files: a
  declaring STREAM_OUTPUT's stream_dest_mac and its Listener flags in the bridge, `ctrl_app_aecp.c`):
  1. Fetch the reviewed head from origin, check it equal to the lane, and `git merge --no-ff` onto the train head.
  2. A resolution row, then the gates:
     - the four shards, with the AECP campaign's new `aecp_output_mutants.py` (14);
     - fw_coverage, the twin and plants (#943 deletes the owed twin row `stream-output-0-dest-mac` and plants its zero
       stream), the docs and generated checks, the boot simulations and the ledger.
  3. The CPU budget images (the bridge is linked in), with the rows confirmed or re-measured.
  4. The release byte-identical, and the split images listed.
- **Step 14, #951** (lane `951-redeclare`, A801; now `e5dee83b`, 1 commit, 5 files: SRP's hold of a withdrawn
  Talker's changed destination over two of the longest LeaveAll periods, `srp_mbx.c`):
  1. The same merge and resolution row.
  2. The same gates, the SRP campaign's plants among them.
  3. The CPU budget images and the SRP rows (`srp_mbx.c` is on the measured path, so they are re-measured), the
     release, and the split images.
  4. Its lane has four uncommitted doc edits, `MAILBOX_SPLIT.md` among them, which this fix also edits. If they land
     in its reviewed head, they may conflict there.
- **Then:** the gating bench bitstreams of the final head at both points, `--eth-port e2`, for the bench's re-check
  of F-G5 and the rest.

---

## Status (02:3x, 11-19; superseded above)

**FINAL HEAD: `0839453f` on `flip-train-1117-p11`, ready for the train candidate and merge.** It was composed in the
scratch clone `p11` and fetched into the lane repo. Nothing is pushed; the manager pushes.

- **`0839453f`:** merges #947's frozen head `fe297847` `--no-ff` onto `7650a02d`.
  - **Reviews:** R867-3 POSITIVE at `fe297847` (#947 issuecomment-6996096094) and R868-2 POSITIVE at `9f4f3de0`
    (issuecomment-6993952183).
  - **Round 3:** tests and docs only, 4 files.
  - **Conflict:** one, in `ctrl_memory.py`'s ledger comment, which takes the train's side. Round 3's rename of the debt
    owner is in a sentence that only #947's own comment has.
  - **The other three files** carry round 3's diff line for line. The gitlinks stay `1616fc8f` / `801ef228`.
  - RESOLUTIONS.md records it.
- **The images: no product image differs, so there is no STOP.**
  - **The platform images at all four points are byte-identical to `7650a02d`'s**, whole file.
  - **Their loaded sections equal the gating bitstreams' firmware:** 1x1/1if `ff21e091…` and 8x8/1if `f2f81d5f…`. So
    the gating run's `7650a02d` bitstreams are the final head's images.
  - **The CPU budget images:** all 12 EQUAL to step 11's.
  - **The release:** byte-identical where loaded, with `bios.bin` `603b9ca3…`, the AEM blob `bdfde7cf…`, and the
    ROM, SRAM and memory init files equal. The Verilog is equal outside its comments.
  - The comparison is in `receipts/step12c/images/`.
- **The ledger:** `plat_ledger.py --self-test` PASS, controls 9 of 9; the points as at `7650a02d`.
- **The quick gates at `0839453f`: ALL PASS**, with the same exceptions as `7650a02d` and step 12
  (`receipts/step12c/`):
  - **The control campaign (shard 1/4): 825 of 825 caught.** That is 823 plus round 3's 2, and no plant is removed.
  - **Sinks at both shapes** (shard 0/4, the `platsinks` arms): 8x8/1if 11/0 and 1x1/1if 11/0. Shard 0 passes in full.
  - **`fw_coverage --check`:** PASS (40 files).
  - **Docs and checks:** the docs, style, paths, TOC and anchors, em dash, hygiene, the Python and C++ idioms,
    `docs_inventory`, the generated checks and `git diff --check 7650a02d 0839453f` all PASS.
    - The exceptions: `ci_tool_inventory_check` is CI-environment-bound, as before. `flip_grade --check`'s output is
      identical to step 12's: the base eleven at 8x8/2if, reported and not held.
  - **The ledger self-test:** PASS, 9 of 9 controls.
- **PR-BODY.md:** step 12 is #947 at `fe297847` with both review links; the F-G4 withdrawal is recorded. Its Status
  reads: final head, ready for the train candidate and merge.
- **Housekeeping:**
  - **Receipts:** collected, sanitized and indexed (2,502 files; INDEX.md 198,257 B), and the scrub found 0 findings.
  - **Scratch: 37 GB.** This round's twelve CPU budget arms' Verilator builds were removed after their hashes were
    taken, each logged in `disk-cleanup.log`.
  - **Units:** no unit of this lane is running.
  - **Lane worktree:** it stays on `flip-train-1117-p10`, clean. `refs/heads/flip-train-1117-p11` is
    `0839453f6d7135063e904bcaf4ac1852ad6b522a`.

---

## Status (02:2x, 11-19; superseded above): STEP 12 WITH ROUND 2 DONE

**STEP 12 WITH #947's ROUND 2: the head is `7650a02d` on `flip-train-1117-p11`** (composed in the scratch clone `p11`
and fetched into the lane repo; nothing pushed, the manager pushes after #947's round-3 review).

- **`7650a02d`:** merges #947's round-2 head `9f4f3de0` (R868-2 POSITIVE) `--no-ff` onto `967b1ca9`.
  - **Conflicts:** seven files, all the ROM ledger's or its prose, as the #946 lane found. Each takes the train's side,
    and the README's two ROM hunks take the train's text.
  - **No raise is owed:** the train's side already holds 8x8/2if at 63.0.
  - **Round 2's own delta is carried line for line** outside the ledger (RESOLUTIONS.md). The gitlinks stay
    `1616fc8f` / `801ef228`.
- **The ledger: PASS, controls 9 of 9.**
  - 1x1 45 and 46 RAMB36, within 56.
  - 8x8/1if 58 at its 58.0 entry.
  - 8x8/2if 63 at its 63.0 entry.
  - `test_ctrl_memory.py` 0 failures.
- **The CPU budget images: all 12 EQUAL to step 11's** (and step 12's) by sha256.
- **The release export: byte-identical where it is loaded.** `bios.bin` `603b9ca3…` and the AEM blob `bdfde7cf…` equal
  step 12's, and the Verilog is equal outside its comments.
- **The gating bench bitstreams** (the gating lane's own `gprep.sh`/`gbuild.sh`, copied with only the scratch path
  changed; `--eth-port e2`, ExtraPostPlacementOpt, through `vivado-slot.sh`):
  - **8x8/1if, READY (01:52):** `<scratch>/gate13/work/g8x8/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
    - **Bitstream sha256:** `b449f2caa3675d2a70a536e5dcd379bdef100da9240d0679dff4b71d796f730b`.
    - **Platform image** `ctrl_app.elf`: `a2862a30900691c51323a9ca3de003fcf908c3746143053fe5cf32bd33a28a03`.
    - **AEM blob:** `723225a5…`.
    - **Checks:** the identity gate passes, with 0 routing errors, and all user timing constraints are met. The split
      boot simulation PASSED on its clone.
    - **#818's floor, met at every corner:** Slow WNS +0.176 / WHS +0.102 ns, Fast WNS +1.523 / WHS +0.036 ns. Both the
      build gate's floor (WNS >= +0.030, WHS >= 0) and the ruling's (both >= +0.030) are met.
    - **argv:** the recipe's, then `--eth-port e2 ... --place-directive ExtraPostPlacementOpt --vivado-max-threads 16
      --build`.
    - **Files:** the absolute path and the build directory are in `../fg4-bench-images.txt`'s gating section.
  - **1x1/1if, READY (01:48):** `<scratch>/gate13/work/g1x1/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
    - **Bitstream sha256:** `550e2d8d3b72a8aca6feff387b83677dbf4ab7c6ea84a318d17bf1f5c66f6543`.
    - **Platform image** `ctrl_app.elf`: `caec03c8807619d0384f0d523071490e02565e32b6dd655f1fa7dd1020923e31`.
    - **AEM blob:** `bdfde7cf…`, the train's.
    - **Checks:** the identity gate passes, with 0 routing errors, and all user timing constraints are met. The split
      boot simulation PASSED on its clone.
    - **#818's floor, met at every corner:** Slow WNS +0.276 / WHS +0.102 ns, Fast WNS +1.641 / WHS +0.036 ns. Both
      floors are met.
    - **argv:** the recipe's, then `--eth-port e2`, as for 8x8/1if.
  - **The firmware in each bitstream is the train's.**
    - **Loaded sections** (`.text`, `.rodata`, `.data`): byte-identical in the gating build, the ledger's link and
      this lane's split export. That is `ff21e091…` at 1x1/1if and `f2f81d5f…` at 8x8/1if.
    - **Whole-file hashes:** these differ only by symbol order, which follows the stand-in export's generation
      timestamp. The gating lane traced the same at step 11.
- **The gates at `7650a02d`: ALL PASS, with the same exceptions as step 12** (`receipts/step12b/`):

  | Gate | Result |
  |---|---|
  | The four firmware shards | **all PASS**; the control campaign **823 of 823** caught (797 + #947's 26; no plant removed) |
  | `fw_coverage --check` | PASS (40 files) |
  | The twin and its plants (twin, twin-plants, twin-maps, twin-maps-plants) | **all PASS** |
  | The receive monitor (`avtp_rxmon`, `make run`) | **PASS**: flat 97/0, N=4 stack 218/0, lockstep N=1 116/0 and N=8 119/0, lockstep mutants 14/14, format mutants 13/13, #947's N=8 format contract 96/0 and its mutants 5/5 |
  | The split boot simulation at 1x1/1if and 8x8 | **both PASS** (0 findings); it passes on both gating clones too |
  | `plat_ledger.py --self-test`, `test_ctrl_memory.py` | PASS, 9 of 9 controls; 0 failures |
  | `run.py --self-test`, `load_grade --check` and `--selftest`, `flip_grade --check --point 1x1/1if` and `--selftest`, rows_tiers, record_classes, shape_costs, egress_ledger, mailbox_margins | **PASS** |
  | `flip_grade --check` (every point) | rc 1, its output **identical to step 12's**: 8x8/2if's base eleven, reported and not held |
  | Docs, style, paths, TOC and anchors, em dash, hygiene, the Python and C++ idioms, `docs_inventory --check`, `git diff --check`, the docs workflow's commands and the generated-table checks | **PASS**, except the CI-environment-bound checks, which are **the same set as step 12's**: no pinned HDL parser or wavedrom in the workflow venv, no `GITHUB_EVENT_PATH`, no checksum-pinned shfmt. The wavedrom, register-reference and HDL-reference checks pass in the generated-checks venv |
- **The gateware question (item 4): UNCHANGED at both points, so no split routes are owed.** The split export at
  `7650a02d` was compared with step 12's (`gateware13.py`).
  - **At 1x1/1if and 8x8/1if:** the rom banks have the same depths, the Verilog is EQUAL outside its comments, and the
    constraints are EQUAL.
  - **What differs:** only the rom banks' init files, which are the firmware.
  - **The split product images** (sha256, against step 12), each 8 B smaller:
    - 1x1/1if `e937ca14…`;
    - 1x1/2if `3e67aaea…`;
    - 8x8/1if `4818bec6…`;
    - 8x8/2if `9c67031d…`.

    The CPU budget images inside the same exports are equal.

**F-G4: WITHDRAWN** (the manager's resume of 01:2x; the bench's second reading).
- The DUT's own PHY advertises 1000BASE-T full alone, and has no link with a 10BASE-T-half-only partner. The test
  machine was negotiating with the inline capture tap.
- It is recorded in RESOLUTIONS.md, and it has left the PR body's known limitations.
- The diagnostic and candidate branches stay as scratch.
- Candidate B's gap is listed as #495 residue for a later ticket.

**Housekeeping:**
- **Receipts** are collected, sanitized and indexed (2,444 files; INDEX.md 193,770 B), and the scrub found 0 findings.
  - The index now drops its first-line column, to stay within 200 KB.
  - The sanitizer now also replaces the gating lane's scratch path and the tap's product name and MAC. They occur in
    the bench lane's copy `fg4-board-reading2.md`; its original stays in that lane's HANDOFF.
- **Scratch: 37 GB**, within its cap. Every removal is logged in `disk-cleanup.log`, all of them build intermediates
  whose verdicts are receipted:
  - the F-G4 diagnostics' boot trees and checkpoints;
  - steps 10 and 11's route checkpoints;
  - step 12's and this round's CPU budget images' Verilator builds;
  - this round's ledger fixture builds.
- **Units and remote:** no unit of this lane is running. Nothing is pushed, and nothing is posted.

---

## Status (01:1x, 11-19; superseded above)

**F-G4, THE ADDRESS FIX: STOP. No commit; `flip-train-1117-p11` stays `967b1ca9`.** The board reading, the board's
pinout and the bench's topology contradict the premise that address 0 is not the negotiating PHY. Together they
point to a device between the DUT and the test machine. As AGENTS.md section 2 requires, I am publishing the conflict
rather than choosing between the two readings. A second diagnostic image, which settles it in one read, is built
below.

**1. The per-port answers, from the repository**
(`sw/litex/platforms/alinx_ax7101.py:53-97`; `docs/integration/BOARD_PORTING_AX7101.md` sections 1 and 5;
`sw/litex/milan_soc.py:4863,5085`):

- **Which MDIO bus belongs to each port:**
  - e1: MDC J17, MDIO L16.
  - e2: MDC AB21, MDIO AB22. The platform records e2's pair as "already proven on this board".
  - Each MDIO pin has its own pull-up.
- **Whether the PHYs share a bus:** no. These are two separate buses, one RTL8211E each.
- **What `--eth-port` selects:** `--eth-port e2` selects pad group 1 (`eth_phy_index=1`), which carries e2's GMII pins
  and e2's MDIO pair together. So on these images the poll's bus is e2's bus, and nothing else is on it.
- **Which PHY address belongs to each port:** the repository states none. It is not in the platform, the board doc,
  the configs or #590. Both firmwares probe PHYID1 from address 0 upward and take the first address that answers.
- **Whether address 0 is the other port's PHY, or a broadcast or alias address:** it cannot be the other port's PHY,
  because the buses are separate. Whatever answers on e2's bus is e2's PHY. If address 0 is the part's broadcast
  address rather than its strap address, it still reaches the same register file.

**2. Correction: my "#590's hardware probe found the PHY at address 1" was wrong.**

- #590's `mdio-phase.log` is the reviewer probe `probe_mdio_phase.py` run against a simulated peer. Its `true=` values
  and its `phy_address=1` are the model's (#590's HANDOFF, its MDIO section). No board record gives an address.
- The bench reading's point 5 ("the composition lane gives the PHY as address 1") rests on my error.
- It is corrected in the 23:0x STOP below, in RESOLUTIONS.md and in `receipts/step12/fg4/fg4-analysis.txt`.

**3. Why the reading contradicts the address hypothesis**

The bench reading is `fg4-board-reading.md`; the test machine's `ethtool` is in the bench lane's
`receipts/rel/fg4read.txt`.

- **Address 0 is e2's PHY.** It is on e2's bus (item 1). It reports e2's link: down during the outage and up after it
  (the reading's point 3). It holds every write (point 2).
- **The pause bit.** Address 0's register 4 has pause (bit 10) set at every read: `05e1` at the cold boot, `0401` after
  the write. No firmware clears it. Yet the test machine reads "Link partner advertised pause frame use: No" at every
  point, the release image's cold-boot link included.
- **1000BASE-T half.** At the cold boot, before any write, address 0's register 9 is `0200`, which does not advertise
  half duplex. The partner shows 1000baseT/Half.
- **So the device advertising to the test machine never carried address 0's register set**, not even the PHY's own
  power-on defaults. Nor does it look like another board RTL8211E at those defaults (pause, no 1000 half). No address
  change in the DUT's firmware can alter what that device advertises.
- **The 10 Mb/s link.** With the test machine at 10BASE-T half alone, its carrier came up at 10 Mb/s half duplex. No PHY
  advertising what address 0 holds (1000BASE-T full alone) can resolve that.
- **The bench's topology.** The S12b gating HANDOFF has the bench's inline capture tap passing traffic, "link 1G both
  sides", and the harness's Ethernet stop/start goes through it.
  - An active tap has a PHY facing each side. The test machine's "Link partner advertised" is then the tap's PHY (six
    modes, no pause), and the DUT's PHY negotiates with the tap's other side.
  - That fits every point: the writes land and verify; address 0 follows the link; the wire view differs from address
    0 even before the first write; the release behaves the same; and a 10 Mb/s link forms on the test machine's side.

**4. What I did not do, and why**

- **No port-derived address fix.** The repository states no address for either port, so a per-port table would be a
  constant I chose. A fix keyed to "e2 is address 1" would also move the poll off the address that the board shows
  holding e2's writes and reporting e2's link. If address 1 does not answer, the poll finds nothing and publishes link
  down.
- **No train tests, gates or fixed-head bench images**, because there is no fixed head. The two-PHY model the manager
  asked for is written as the second diagnostic's host test, `diag_quick2.c`: two PHYs on one open-drain bus, at
  addresses 1 and 3. The poll's writes land at the address it found, and the other PHY stays at its defaults. It
  becomes a train test when there is a fix to pin.
- **The release is unchanged.**

**5. What decides it: one bench read, either of two ways**

- **(i) Without recabling.** Flash the second diagnostic below. Type `milan_mdio` and `milan_phy` at point B, and once
  while the test machine offers 10BASE-T half alone.
  - **The tap.** Address 0 answers. Its R5 has the 10/100 bits set and both pause bits clear, and its R10 has bits 11
    and 10 set (about `3c00`). R17 resolves 1000 full. During the 10 Mb/s phase the DUT stays at 1000 full
    (`LINK=0000000d`, R17 at 1000) while the test machine sits at 10.
  - **A direct cable.** R5 and R10 show the test machine's own advertisement: no 10/100 bits and R10 bit 11 alone at B,
    then 10BASE-T half alone during the 10 Mb/s phase. Then point 3's contradiction stands unexplained. Look first at
    the scan's other responders, and at an address that `MDIO_ACK` shows but the probe never reaches.
- **(ii) By recabling.** Cable the DUT straight to the test machine, with any existing image (the release, or the first
  diagnostic).
  - **If the tap was the cause,** the test machine reads 1000baseT/Full only, with pause Symmetric (register 4's bit
    10). With 10BASE-T half alone, no link forms.
  - **The bench's acceptance check** ("the partner sees 1000baseT/Full only", "no link with 10BASE-T half alone") can
    be judged on a direct cable only, never through an active tap.

**6. What follows from each outcome**

- **If the read shows the tap:** F-G4 is a bench-topology finding, not a defect of the train, the split or the release,
  and the train needs no commit.
  - Candidates A, B and C stay staged, none of them owed for F-G4.
  - B's test still shows a real gap that wants its own ticket: through a 600 ms erase under constant input, the poll
    published a loss only after the save.
- **If the read shows a direct cable and another responder:** I will make the manager's fix, keyed to the address the
  scan names, with its tests, gates and bench images. The release shares the source: `milan_baremetal.c` also probes
  from address 0. So the release would take the same small change, with its resource gate re-run.
- **If you rule the fix regardless,** name the address per port and I will make it.

**7. The second diagnostic's bench images** (the bench lane flashes and reads them; this lane does not touch the bench):

- **Source:** the scratch branch `fg4-diag2-967b1ca9` at `46af043b`, on top of the first diagnostic (`round5/fg4/
  diagnostic2.diff`, README there). It is not `flip-train-1117-p11`, and nothing is pushed.
- **Recipe:** as before, through `vivado-slot.sh`, with `--eth-port e2`, ExtraPostPlacementOpt and 16 threads.
- **Checked:** `diag_quick2` PASS; the `platboot` arm 52 of 52; the split boot simulation PASS at both points.
- **1x1/1if, READY (01:00):** `<scratch>/fg4/v2work1x1/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
  - **Bitstream sha256:** `4f49291d41875b733643904ee3c9ee55868365db4d577ae633d0c80a17cb900b`.
  - **Platform image** `ctrl_app.elf`: `9de5397ae0b221296167c45a5ea1ca176e08e1e0cfa79fb6837132c7ab84e7a0`.
  - **AEM blob:** `bdfde7cf…`, the train's.
  - **Checks:** the identity gate passes, with 0 routing errors.
  - **#818's floor, met at every corner:** Slow WNS +0.369 / WHS +0.102 ns, Fast WNS +1.641 / WHS +0.036 ns.
- **8x8/1if, READY (01:05):** `<scratch>/fg4/v2work8x8/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
  - **Bitstream sha256:** `920e75e6e048ab68786bbf61a78f9c0e5044231524d92967ef88fe33261f40ef`.
  - **Platform image** `ctrl_app.elf`: `5f5a3325545a21567586b1966dce2846d8d97d0094b40f60177be6b5011017c8`.
  - **AEM blob:** `723225a5…`.
  - **ROM:** the image is within the diagnostic's 58.5 entry.
  - **Checks:** the identity gate passes, with 0 routing errors.
  - **#818's floor, met at every corner:** Slow WNS +0.266 / WHS +0.135 ns, Fast WNS +1.691 / WHS +0.038 ns.
- **Where the files are:** the absolute paths, manifests and the read recipe are in `../fg4-bench-images.txt`. The
  first diagnostic's images are kept there too.

**Scratch:** the five candidate boot-simulation trees (`cb-a`, `cb-b`, `cb-c`, `cbc-tdm8`, `cbc-8x8`, 920M) are
removed. Their verdict logs were already in the receipts, and each removal is logged in `disk-cleanup.log`. That made
room for these two builds. Scratch is at 40 GB, its cap, and no unit of this lane is running.

---

## Status (23:52, 11-18; superseded above)

**F-G4 DIAGNOSTIC IMAGES (the manager's decision of 23:1x): building. The train is unchanged at `967b1ca9`.**

- **Where the diagnostic lives:** the scratch branch `fg4-diag-967b1ca9`, off `967b1ca9`, in the scratch clone `d12`.
  It is not `flip-train-1117-p11`, and nothing is pushed.
  - `9cd6000c` and `6a95474e`: a new console command, `milan_phy`, printing one line. That leaves `milan_status`'s
    graded lines untouched.
  - `fcdb9f6c`: raises the 8x8 one-interface ROM entry to 58.5 for this image only. The command's code needs 92 B
    of `rom` past 58.0, so that image has one more ROM bank than the train's.
- **What `milan_phy` prints** (type it on the console):

  `PHY_ARMED= FOUND= ADDR= STAGE= ADV= RENEG= POLLS= WRITES= RESTARTS= LINK= R4_BEFORE= R9_BEFORE= R4= R9= R9_NOW= R4_NOW= R0= SPIN=`

  - the poll armed, the PHY found, and its address;
  - its stage, and `adv` (0 verified, 1 or 3 owed, 4 a 10/100 PHY);
  - the renegotiations, the polls started, the advertisement's write frames and their restarts;
  - the last published link word (hex);
  - registers 4 and 9 before the writes and their read-back;
  - registers 9 and 4 as the latest poll's resolution read them, and register 0 before the restart;
  - the half period's spin.

  In the register fields, `fffffffe` means never read and `ffffffff` an unacknowledged read.
- **Checked:**
  - a quick host test: the real poll and console against a pin-level PHY at address 1 that changes only when a write
    lands. It shows 3 writes and 1 restart, read-back `R4=00000001 R9=00000200`, and
    `R9_NOW=00000200`;
  - the harness's `platboot` arm: 52 of 52 pass;
  - the split boot simulation: 1x1/1if PASS; 8x8/1if running inside its build.
- **What the readout tells apart:**
  - `POLLS` not rising between two reads 1 s apart: cause (b), the poll stalled;
  - `WRITES` and `RESTARTS` rising each poll while `R4`/`R9` read back the defaults: cause (c), the writes never
    land;
  - `ADV=0`, read-back gigabit-only, but `R9_NOW` back at `00000300`: cause (a), the PHY returned to its defaults
    after the boot's write;
  - `ADV=0`, the read-back gigabit-only and `R9_NOW=00000200`, yet the partner sees every mode: the PHY does not
    advertise what its registers hold. That one is hardware-side.
- **The two bench bitstreams** (S9's recipe as the gating lane builds it, with the bench override `--eth-port e2`,
  ExtraPostPlacementOpt, 16 threads, through `vivado-slot.sh`):
  - **1x1/1if, READY (23:35):** `<scratch>/fg4/work1x1/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
    - bitstream sha256 `21aa68e11e8d9cb4cce0c43c5808dadd949448b4db452f2dcbaecbe325413814`;
    - from `6a95474e`; platform image `ctrl_app.elf` sha256 `b615a9275a8c1c4a7e3a1cdb977bf8acb219f4275a8c2faabab95cde3aefe43f`;
    - AEM blob `bdfde7cf…`, the train's; manifest and artifacts in `work1x1/artifacts.sha256`;
    - the identity gate passes; 0 routing errors;
    - #818's floor met at every corner: Slow WNS +0.156 / WHS +0.050 ns, Fast WNS +1.687 / WHS +0.016 ns;
    - the boot simulation PASS.
  - **8x8/1if, READY (23:44):** `<scratch>/fg4/work8x8/build_ExtraPostPlacementOpt/gateware/alinx_ax7101.bit`
    - bitstream sha256 `d4e4141fc54842785486025e96b67eaef866b066fb670d3901949655bdadee76`;
    - from `fcdb9f6c`; platform image `ctrl_app.elf` sha256 `bfa21c32375fa023d0606b16e5165fff601d8b06cfe1cb4df51cc2abdcae0340`;
    - AEM blob `723225a5…`; manifest and artifacts in `work8x8/artifacts.sha256`;
    - the identity gate passes; 0 routing errors;
    - #818's floor met at every corner: Slow WNS +0.064 / WHS +0.102 ns, Fast WNS +1.636 / WHS +0.036 ns;
    - the boot simulation PASS.

  `<scratch>` is this lane's scratch directory. The packet carries no host paths, so the absolute paths are in
  `../fg4-bench-images.txt`, beside this round's folder and outside the packet.

  Both are built as the gating lane builds them, with `--eth-port e2`. The bench lane flashes and reads them; this
  lane does not touch the bench.

**The fix candidates are staged**, one per cause, and none is committed to p11 (`round5/fg4/README.md`, the diffs
beside it). Each diff applies to `967b1ca9`, and each has a test that fails on the old code by name and passes with
the fix, in the `platboot` arm (53 of 53):

| Candidate | Cause | Fix | Test, before and after | Boot simulation |
|---|---|---|---|---|
| A (`fg4-fix-a`, `63fb939d`) | (a) the PHY back at its defaults after the boot's write was verified, with no published loss | the advertisement re-verified by each poll's own register 9 read; no extra frame | P14B: FAIL, then PASS | 1x1/1if PASS (frame 145.43 us) |
| B (`fg4-fix-b`, `f27ee40f`) | (b) the poll starved through a save under input, every aged call carrying the save's step | a poll a whole period late takes the call's frame ahead of the store's centisecond step. Needs #665's word on THE STEP's order | B13: FAIL (the loss published only after the save), then PASS | 1x1/1if PASS |
| C (`fg4-fix-c`, `9af3e35a`) | (c) the split's bit lowering MDC and changing the data in one write | the release's bit; the frame's stated cost restated by the rule to 170 us (157.92 and 157.57 us measured) | P19: FAIL, then PASS | 1x1/1if and 8x8 PASS at 170 us |

B's test shows a real gap in the model whatever the bench finds: through a 600 ms erase under constant input, the
poll published a link loss only after the save. Each candidate still needs the full gates before it is a train
commit: shards, coverage, twin, docs, the split routes and the image hashes.

**Scratch cleanup (the manager's go-ahead):** the three ledger runs' build trees are removed, each exact path logged
in `disk-cleanup.log`. They were `r5led11`, `r5led12` and `r5led12b`, each `pl/` (26M) and `fx/` (1.1G). The cited
ELFs are kept first in `r5img/plat-b1f1161b`, `r5img/plat-967b1ca9` and `r5img/fx-967b1ca9`. Scratch is back at 40 GB, its cap, with the two diagnostic
bench builds, which the bench needs until it has flashed them. No unit of this lane is running.

**F-G4 (23:0x): STOP. The cause is not found in software, so there is no fix commit, and the head stays `967b1ca9`.** The
bench reports that the PHY advertises every mode, so a 10BASE-T partner gets a silent 10 Mb/s link. I could not
reproduce that in any model, and the code is correct against IEEE 802.3 22.2.4.5 (`receipts/step12/fg4/fg4-analysis.txt`):

- **The split's write path is the release's**, frame for frame:
  - ST 01, OP 01, PHYAD, REGAD, TA 10 and 16 data bits, all 64 driven after a 32-one preamble;
  - the same MDIO pins and CSR bits;
  - the same probe from address 0;
  - the same register 9, 4 and 0 values.

  The differences are the bit routine, the half period and the pacing:
  - the split lowers MDC and changes the data in one CSR write; the data is still held a half period around each
    rising edge;
  - its half period is a calibrated spin rather than `cdelay(32)`;
  - it takes one frame per step call.
- **Every model lands the writes.** The host PHY model does. So does the split boot simulation, which runs the real
  image on the real split CPU and bus, with LiteEth's MDIO logic and a PHY at address 1. At `967b1ca9` it shows the
  boot's (9, 0x200), (4, 0x1), (0, 0x1200) and the writes after each loss landing. MDC is high 950 ns and low 1120 ns.
  So the pins carry correct write frames.
- **Two premises do not hold as stated:**
  - The release's advertisement was never measured on hardware. #840 says "No hardware was used", and no later
    record shows it on this board. So the release is no proof of the board's address or pins.
  - The bench's LINK counts cannot show that the poll runs. The counters follow `eff_link = i_link_up & cfg_sw_link
    & guard`, and the "+2 per flap" is the hardware link guard's own pair (`milan_datapath.sv:3404-3414`). The bench
    never read MAC_STATUS or the published word.
- ~~**What is known of the board:** #590's hardware probe found its RTL8211E at **address 1** (PHYID1 0x001c, BMSR
  0x796d). So the address and pins are right for reads, and nothing points to the PHY strap or the board.~~
  **CORRECTED 00:4x, 11-19: this was wrong.** #590's `mdio-phase.log` is a reviewer probe run against a simulated
  peer, and its `phy_address=1` is the model's. No record gives a board PHY address. See the status at the top.
- **Candidates the models cannot reach:**
  - (a) the PHY drops writes it receives. One mechanism: the split's frames come within milliseconds of LiteEth's
    256-cycle, 2.56 us PHY reset pulse at FPGA start, where the release's come after the BIOS. That would not explain
    the writes after a later loss.
  - (b) the poll is not running, or not publishing, on the board after boot. `i_link_up` would then sit at its reset
    value (up) and the guard alone gate the link. That fits every bench observation.
  - (c) the PHY handles a write frame in a way 22.2.4.5's model does not, sparing reads.
- **What decides it:** one boot reading the poll's state. That is task 3's console field: the address and found flag,
  stage, `adv` and `renegotiations`, polls started, the last published word and the last read-back of registers 4 and
  9. It changes no mailbox contract and needs a new split image. **I have not made it**, since without the cause it
  would ship an image change on its own. It is about a half-day with its tests and the gates. It waits for the
  manager's word, and so does any fix.

The step-12 state below is unchanged.

**STEP 12: the head is `967b1ca9` on `flip-train-1117-p11`** (fetched into the lane repo; nothing pushed, the manager
pushes after #947's reviews).

**Scratch is at 41 GB, 1 GB past its 40 GB cap**, after the step-12 routes, ledgers and gate clones. Clearing the three
ledger runs' build trees (`r5led11`, `r5led12`, `r5led12b`: `pl/` and `fx/`, about 3 GB) would bring it back under.
Their verdicts are in their logs, which are collected. The cited platform ELFs would be kept beside the image hashes
first. My removal was refused by the session's permission mode, so it waits for the manager's go-ahead. No unit of
this lane is running.

- `d09c7118`: #947's `66c6edf3`, fetched from origin's `946-ctx-fmt` and checked equal to its lane, merged `--no-ff`
  on `b1f1161b`. No conflict: four files auto-merged in hunks apart. The gitlinks stay `1616fc8f` / `801ef228`.
- `967b1ca9`: the one composition fix. The platform's 8x8 two-interface ROM entry goes 62.5 to 63.0: its image needs
  140,008 B of `rom`, 744 B past the 139,264 B 62.5 holds beside its `sram`. That is S14 debt by the owner's rule.
  The ledger's cases and planted ledgers move with it, and its case writer is re-anchored to reach 63.5 (it reached
  63.0 at most). The S14 debt is recorded where the train records S14 debt: SPLIT_CONTROL_MEMORY.md section 5's list,
  now 63.0 RAMB36, debt 7.0 (28,672 B), with the history in `ctrl_memory.py`. DEBT-640.md is the release image's area
  debt, so it is not the place. Every other point holds its entry (`receipts/step12/ledger/`):

| Ledger point at `967b1ca9` | `rom` / `sram`, B | RAMB36 | Its entry | Step 11 |
|---|---|---:|---|---|
| platform 1x1/1if (shipping) | 125,792 / 56,736 | 45.0 | within 56 | 124,832 B, 44.5 |
| platform 1x1, two interfaces | 127,400 / 59,040 | 46.0 | within 56 | 126,432 B, 45.5 |
| platform 8x8/1if (shipping) | 138,432 / 98,160 | 58.0 | its 58.0, 832 B of `rom` left | 137,472 B, 58.0 |
| platform 8x8, two interfaces | 140,008 / 115,504 | 63.0 | its 63.0 (was 62.5), 1,304 B left | 139,048 B, 62.5 |
| the size fixture, six arms | 130,952 to 131,448 / 114,320 to 114,384 | 60.0 to 60.5 | within its 60.5 | unchanged |

| Gate at `967b1ca9` | Result |
|---|---|
| The four firmware shards | **all PASS**; the control campaign **816 of 816** caught (797 + #947's 19) |
| `fw_coverage --check` | PASS (in the docs extras and the quick list) |
| The twin and its plants (twin, twin-plants, twin-maps, twin-maps-plants) | **all PASS** |
| The receive monitor's suite (`avtp_rxmon`, `make run`), the one RTL suite #947 touches | **PASS**: flat 97/0, N=4 stack 218/0, lockstep N=1 116/0 and N=8 119/0, lockstep mutants 14/14, format mutants 13/13, **#947's N=8 format contract 96/0 and its mutants 5/5** |
| The split boot simulation (the platform image on the split SoC) at 1x1/1if and 8x8 | **both PASS** (0 findings) |
| The platform ledger (`plat_ledger.py --self-test`) and `test_ctrl_memory.py` | PASS, 9 of 9 planted ledgers as required; 0 failures |
| `run.py --self-test`, `load_grade --check`, `flip_grade --check --point 1x1/1if`, and the rest of the quick list | **PASS** |
| `flip_grade --check` (every point) | its verdict lines are **identical to the candidate's**: 8x8/2if's base eleven and 8x8/1if's HELD line (76.81 of 77 ms) |
| Docs, idiom, hygiene, `git diff --check`, `docs_inventory --check`, every command of the docs workflow, the other generated-table `--check`s | **all PASS**, but the CI-environment-bound ones, as at `b1f1161b` (`receipts/step12/gates/`) |

| Image | Step 11 | Step 12 | |
|---|---|---|---|
| The CPU budget harness's twelve images | `hashes.txt` | equal, every one | so the CPU rows carry |
| **The platform's split image 1x1/1if** (the bench's) | `a00828fe` | **`f04caf59`** | CHANGED |
| **The platform's split image 8x8/1if** (the bench's) | `5edbba3a` | **`22ada381`** | CHANGED |
| The platform's split image, 1x1 two interfaces | `76eae358` | `0a9a8201` | CHANGED |
| The platform's split image, 8x8 two interfaces | `d090b8d6` | `dcec0148` | CHANGED |
| The release (all-fabric) image | | **byte-identical** | `bios.bin`, the AEM blob, the ROM/SRAM/memory init files equal; `bios.elf` equal with debug stripped; the Verilog equal outside comments (`receipts/step12/images/release-export-12.txt`) |

**The split GATEWARE changes, because the firmware is in it.** The control firmware is the control memory's block
RAM: `rom` is initialised with the linked image and its banks are sized from it (SPLIT_CONTROL_MEMORY.md section 2).
The bench builds its image with the split recipe: `ctrl_plat_image.py --interfaces 1`, then `milan_soc.py
--ctrl-firmware <image> --build`. So a firmware change is a new synthesis input and a new bitstream. Nothing of the
control firmware is in flash. Evidence (`receipts/step12/images/split-gateware-12.txt`):

- **1x1/1if: the gateware itself changes.** `rom` passes a granule, so `rom_bank4` grows from 512 to 1,024 words: 5
  Verilog lines outside comments (the bank, its address width, the decode). The routed design moves by +104 LUTs and
  +10 registers, with block RAM totals equal. The constraints are the same set (clock-group pairs written in another
  order).
- **8x8/1if: only the firmware payload changes.** The bank depths, the Verilog outside comments and the constraints
  are equal, and only the two banks' init contents differ. The integrated route's placed utilisation is identical to
  step 11's in every line, with the same timing.

**So the split routes were run** (three directives each, through the slots):

| Point | ExtraPostPlacementOpt | ExtraTimingOpt | AltSpreadLogic_high | #818's floor |
|---|---|---|---|---|
| 1x1/1if | **+0.334 / +0.034** | +0.231 / +0.028 | +0.179 / +0.025 | met on all three (step 11: +0.141 best) |
| 8x8/1if | **+0.073 / +0.034** | +0.064 / +0.027 | +0.006 / +0.036 | met on its best of three, **step 11's three figures exactly** |

**What the bench must re-run.** Both split images are new bitstreams, and the release image is not.

- **Rebuild both split images** from the pushed step-12 head, 1x1/1if and 8x8/1if, by the recipe. The loaded sections
  of their `ctrl_app.elf` must equal this lane's (`f04caf59`, `22ada381`; the whole-file hash follows the stand-in
  export's symbol order, as the gating lane found). Each meets the floor here on ExtraPostPlacementOpt, the recipe's
  directive.
- **8x8/1if, every item on the new image:**
  - (a) flash, cold boot, banner and BOOTSTS/STAT;
  - (b) identity, since the manifest's firmware hash changes;
  - (c) enumeration;
  - (d) gPTP for at least 10 minutes;
  - **(e) streams: #946's acceptance.** Inputs 1 to 7 each receive, with FRAMES_RX rising and UNSUPPORTED_FORMAT +0.
    Input 0, the CRF input and outputs 0 and 8 must pass as before. Include a SET_STREAM_FORMAT on an unbound input,
    then its bind;
  - (f) the 40 cold power cycles and (g) the 1-hour soak, which were pending;
  - (h) as planned.
- **1x1/1if, every item on the new image as well:** (a) to (g), (h) as planned. Its gateware changed (the larger
  `rom` bank), and its firmware's boot path changed, although it writes no context at 1x1. Its (e) is a regression
  check: 4 streams as before.
- **The release (all-fabric) image: nothing.** It is byte-identical.
- **The CPU budget rows: nothing.** Their images are hash-equal, so they carry.

**Before (16:46): the final head was `b1f1161b` on `flip-train-1117-p11`**: `73272666` plus one docs-only commit. Nothing was pushed;
the manager pushes.

**Why:** the train candidate's builder failed on `docs_inventory.py --check` ("docs/DOCUMENTATION_AUDIT.md: STALE"),
and it reproduced on `73272666`. Each first-parent commit's own script locates the cause
(`receipts/step11/docs/audit-bisect.txt`):

- the script and its page arrive with step 9, #934, fresh at #934's own head `544fd72c` (540 lines);
- the step-9 merge `8f6fbb84` is the first stale commit (122 lines at the check), since steps 1 to 8's pages were
  never inventoried; step 10's merge `49f005b9` adds one line more;
- the heads of steps 10 and 11 (`d1aa4c44`, `0297a19a`) do not carry the script.

My docs check list had no `docs_inventory`, so the stale page went unseen. That list now holds the docs workflow's
every command.

**`b1f1161b`** is `docs_inventory.py --write`: `docs/DOCUMENTATION_AUDIT.md` alone, +13 / -12 lines. It lists step 1's
`tb/verilator/ctrl_reboot/README.md` (#881, not in #934's history). It restates six pages' cited paths
(`MAILBOX_SPLIT`, `REBOOT_RESET`, `FR_NFR`, the plat, srp and split-boot READMEs) and the counts. The diff from
`73272666` touches that one docs file; the gitlinks stay `1616fc8f` / `801ef228`; `git diff --check` over the train is
empty.

| Check (run on the regenerated tree, then the docs set again at `b1f1161b`) | Result |
|---|---|
| Every `python3` command of `.github/workflows/docs.yml` (103, `receipts/step11/docs/q-docswf-pre/`) | all pass but the environment-bound ones. Seven need `wavedrom` or the pinned HDL parser and pass under the tools environment that has both, below. `act_ci` and three `ci_fail_fast` steps need the hosted CI's event and checkout. `docs_inventory --check` now passes; it failed at `73272666` |
| The same with the pinned packages, plus the other generated-table `--check`s found (`receipts/step11/docs/q-docsx-pre/`) | **all PASS**: the HDL reference self-test, the wavedrom self-test and its three diagrams, the register reference check and self-test, the memory map, `ci_events`, the one-valued table, the mailbox contract (`gen_mailbox --check`), `pp_srcs`, the publication census, the firmware coverage ratchet. `ci_tool_inventory --check` refuses outside the CI image (`CI_IMAGE_SHFMT`); it is the CI image's inventory, not a docs table |
| `docs_inventory`, `docs_check`, `doc_style`, `doc_paths`, `check_em_dash`, `hygiene`, `py_idiom`, `gen_toc --check` and `--verify-anchors` at `b1f1161b` | **all 9 PASS**, clean tree (`receipts/step11/gates/q-b1f1161b/`) |
| The 12 split firmware images at `b1f1161b` | **all EQUAL** to `3e908539`'s (`receipts/step11/images/hashes-b1f1161b.txt`) |

The PR body has the new row in its composition fixes table, the new head in its status, and `docs_inventory.py
--check` in its validation commands.

**Before (15:16): `73272666` on `flip-train-1117-p11`, ready for the composition review.** RULING-1118f (#665
issuecomment-6981065172) resolves the CDC stop below. CDC-15 on the gray-pointer LUTRAM FIFO is the expected report,
accepted with no waiver. So the record-only re-baseline is made: `73272666`, on `05dc1791`. Nothing is pushed; the
manager pushes.

| Check at `73272666` | Result |
|---|---|
| `pp_resource_gate.py record … --write`, on p11's three release routes | rc 0; the written record is the dry run's, byte for byte (`receipts/step11/release/record-write.txt`): LUT 54,002, FF 55,203, SLICE 15,849, 84.5 block RAM tiles, RAMB36 71, RAMB18 27, DSP 15, CARRY4 3,760, WNS 0.194 / WHS 0.017 ns, ExtraTimingOpt selected. The endpoint's provenance note (`measured`) is restated with the rulings, the head and the attribution. Every tolerance, floor and ceiling is unchanged. One file, `syn/ooc/pp_resource_baseline.json`; the gitlinks stay `1616fc8f` / `801ef228` |
| `pp_resource_gate.py check --endpoint route-1x1` (both comparisons) | **exit 0, RESULT: PASS**, every figure 0 delta (`receipts/step11/release/gate-after.txt`) |
| `check-baseline`; `--selftest`; the set, placement and baseline-report self-tests | all exit 0 (`baseline PASS: 3 endpoints`) |
| The docs, idiom and hygiene checks | all 8 PASS, clean tree (`receipts/step11/gates/q-73272666/`). `doc_paths` counts 1 allowlisted build artifact here and in the lane, against 2 at 14:10; the count follows which build outputs are present in a checkout, not the commit |
| `git diff --check origin/dev-soft-core...HEAD` | prints nothing |
| The 12 split firmware images | **all EQUAL** to `3e908539`'s (`receipts/step11/images/hashes-73272666.txt`) |

**Not changed, by ruling (record-only):** `docs/design/AREA_BUDGET.md`:158-159 (the utilisation table's LUT and FF
column) and `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`'s record table still quote the previous record, 53,461 LUT
and 54,971 FF. The composition review may ask for them; they would be a docs-only follow-up.

**The PR body** (`round5/PR-BODY.md`) records:

- the three rulings (1118d, 1118e, 1118f) and the hierarchy table;
- the CDC check: covered, 201 of 201 Safe, and CDC-15 x192 on the render crossing beside the capture crossing's x50;
- the safety argument, and that the check closes R863's stated limit;
- the corrected premise and the re-baseline;
- Status: ready for the composition review at `73272666`.

`round5/DEBT-640.md` carries the attribution of 1118e item 5, the commit and one line on the CDC-15 rows (the #495
residue).

**RULING-1118e's STOP (15:08), resolved by RULING-1118f:** the render crossing's CDC-15 rows were held as a flag, and
the re-baseline was not made until the ruling.

RULING-1118e (#665 issuecomment-6979996755) resolves the 1118d stop below and asks for one check first, from the
existing routed checkpoints (no new route): `u_fcdc`'s new crossing, the RAM32M storage written on the write clock and
read into the 192-bit register on the read clock, must be covered by the crossing's timing exceptions and clean in the
CDC report, or the lane stops. It is covered, and it is not clean (`receipts/step11/cdc/fcdc-summary.txt`):

| Image (routed checkpoint) | Covered by an exception | `report_cdc` rows naming `u_fcdc` | `report_methodology` |
|---|---|---|---|
| p11's release image, ExtraTimingOpt (the selected route) | **yes:** every storage-to-register path is `Timing Exception: Asynchronous Clock Groups`, slack inf (`set_clock_groups -asynchronous` between `milan_clk` and `audio_clk`; `report_exceptions` lists none, since a clock group is not a path exception) | **CDC-15 Warning x192** ("Clock enable controlled CDC structure detected": each storage leaf's write clock to a `rdata_o` bit, depth 0), and CDC-2 x2 and CDC-5 x2 on its pointer synchronizers (missing `ASYNC_REG`) | no line names `u_fcdc` |
| p11's 1x1/1if split image, ExtraPostPlacementOpt (its best) | yes, the same | the same: CDC-15 x192, CDC-2 x2, CDC-5 x2 | no line names `u_fcdc` |
| p11's 8x8/1if split image, ExtraPostPlacementOpt (its best) | not applicable | none: this image carries no render master and no `u_fcdc`; its only `cdc_pair_fifo` is the capture's `u_tcdc` | no line names `u_fcdc` |
| for comparison, the candidate `c8ff391a`'s release image (block RAM, before #927) | | CDC-2 x2 and CDC-5 x2 only: the block RAM holds the crossing inside the primitive, so no storage row | three SYNTH-6 lines on its block RAMs (no output register merged) |

**What the flag is.** Vivado's summary puts all of the write clock's endpoints into the read clock in its **Safe**
column (201 of 201 at release and 1x1/1if; 0 unsafe, 0 unknown; 9 without `ASYNC_REG`, as before). CDC-15 is the
clock-enable-controlled structure: the read register loads only on `ren_i && !rempty_o`, and `rempty_o` comes from the
synchronized write pointer. That matches the safety argument both reviews made (R863: "Each entry is read at least
two synchronizer stages after its write"). **The same rule already fires on the base's unchanged TDM capture FIFO
`u_tcdc`**, whose LUTRAM storage has CDC-15 x50 (x52 at 8x8/1if) in every image, the candidate's included. The project
has not waived CDC-15 anywhere (`docs/findings/COMMERCIAL_TIMING_395.md` lists 249 and says they "have not been waived
or repaired"). What #927 adds is 192 more of the same rows. There is no new CDC-26 (LUTRAM read/write collision), and
nothing Critical. The two TIMING-47 lines in every image are on the sys and milan clocks, not this crossing.
**The reviews:** neither recorded a CDC report. R863 (#939 issuecomment-6978630716) states the limit: "the distributed
RAM's inter-clock arc was judged from 0 failing endpoints, not read in the report". R864 checks the branch identity and
the plants.

**The decision needed:** whether CDC-15 on `u_fcdc`'s storage, classified Safe and the same rule the shipping `u_tcdc`
already carries, counts as clean for item 3. If it does, items 3 to 5 are ready: the record by
`pp_resource_gate.py record … --write` with the dry run's figures, then the gate, the checks and the hashes. The PR body
states both outcomes. The #640 note (`round5/DEBT-640.md`) is written to be posted with the re-baseline commit;
it describes the record moving by that commit.

**Done at 15:12:** item 1 (this check; `receipts/step11/cdc/`); item 2 (the wording: no train docs or comments call
the distributed-RAM option split-only; the PR body's step-11 row and its route note, and this handoff's FIFO cell,
now say the render master's crossing is shared and the release image takes it, 74 to 71 RAMB36); item 4 (the PR
body); item 5 (`DEBT-640.md`). Item 3 is held.

**RULING-1118d's STOP (14:17), resolved by RULING-1118e item 1: the re-baseline was not made.** A release-image CDC FIFO instance changed
primitives and its flop count. `KL_tdm_render_master`'s frame crossing `u_fcdc` (`cdc_pair_fifo`, WIDTH 192, LOG2D 2)
holds its storage in **3 RAMB36E1** in the candidate's routed release image and in **32 RAM32M (128 LUTRAMs)** in p11's.
Its flops go from **24 to 216**: the 192-bit read register, which the block RAM's output register held before. This is
#927's `DIST_RAM_P = 1` on that one instance. #927's comment gives the reason: the slot bank's registers are written
straight into the storage, and "a block RAM's write-data hold requirement left those writes about +0.014 ns of hold at
the fast corner". So #927 states the change as intended, but the ruling stops on any primitive change of a release
FIFO, so task 5 (the record-only commit) is held. The other release FIFO, the TDM capture's `u_tcdc`, keeps its
storage and flops (34 LUTRAMs, 82 flops, no block RAM). **Decided by RULING-1118e item 1:** `u_fcdc`'s move from
block RAM to distributed RAM in the release image is accepted, and the re-baseline is the record alone, by the gate's own
`pp_resource_gate.py record … --write`. Run without `--write` at `05dc1791`, on p11's three routes, it prints the
record it would store (`receipts/step11/release/record-dryrun.txt`; rc 0; nothing written, the tree clean):
ExtraTimingOpt selected; LUT 54,002, FF 55,203, SLICE 15,849, 84.5 block RAM tiles, RAMB36 71, RAMB18 27, DSP 15,
CARRY4 3,760, WNS 0.194 ns and WHS 0.017 ns.

**The release image's delta by hierarchy**, from the two routed checkpoints (ExtraPostPlacementOpt; the candidate
`c8ff391a`'s release route and p11's; `report_utilization -hierarchical`; `receipts/step11/release/hier-diff.txt`):

| Where | LUT | FF | RAMB36 | LUTRAM | Step 11 changes its RTL? |
|---|---:|---:|---:|---:|---|
| The whole image | 53,571 to 53,971, **+400** | 54,944 to 55,206, **+262** | 74 to 71, **-3** | 3,822 to 3,950, +128 | |
| `u_fcdc`, the render master's frame FIFO, with its storage | +121 (logic -7, LUTRAM +128) | **+192** | **-3** | **+128** | yes: #927's `DIST_RAM_P = 1`. The 32 RAM32M are named `milan_datapath/u_fcdc/g_mem.mem_r_reg*`, so the report counts them in the datapath's own cells |
| `KL_aaf_clock_meter` | +41 | -18 | 0 | 0 | yes: #927, the group reference loaded through its adder (two registers, 53 bits, become one of 32) |
| The datapath's EDIT-window claim registers (`amap_edit_oclaim_expect_r`, `amap_edit_oclaim_word_r`) | | +96 (112 to 208 bits kept) | | | #927 moved the capture-source word's encode out of `amap_edit_validate`; all-fabric it is the same combinational function, and synthesis keeps 96 more of these bits |
| Every other module | about +238 | about -8 | 0 | 0 | no. The largest are `milan_csr` +338 and `KL_render_queue` -213; three transmit arbiters (-152) are absorbed into the datapath's own cells; the soft core is -25 and the top's own cells -45. `ptp_clock_validity`'s +64 flops are `gsi_gm_q_r`, moved there from the datapath's own cells |

So the -3 RAMB36 is `u_fcdc` alone, and most of the +262 flops are `u_fcdc` (+192) and the EDIT claim registers
(+96). The LUTs are `u_fcdc`'s storage (+128) and the meter (+41), plus about +230 of synthesis and placement
variation in modules whose RTL step 11 leaves unchanged (`git diff c8ff391a 05dc1791 -- hdl` touches seven files:
`cdc_pair_fifo`, the render master, the meter, two mailbox files that only the split build carries, the datapath and
a README). Vivado counts a LUT that packs logic from two instances in each of them, so the rows are each instance's own
report line and do not sum exactly.

**In short.**

- **The CPU verdict:** PASS, on U (unit 375) over every arm, at the candidate `4374cc27`.
- **p11 is at `05dc1791` (task 1 done, 14:12).** `74481d2e` plus one commit that drops the blank line `6ad5c259` left at
  the end of `plat_mutants.py`. `git diff --check origin/dev-soft-core...HEAD` now prints nothing over the whole train;
  that was its only hit. The docs, idiom and hygiene checks (`docs_check`, `doc_style`, `doc_paths`, `emdash`,
  `hygiene`, `py_idiom`, `toc_check`, `toc_anchors`) all PASS, with a clean tree. All 12 split firmware images are
  hash-equal to `3e908539`'s (`receipts/step11/images/hashes-05dc1791.txt`). p10 has the same blank line; it was not
  asked for there.
- **The receipts (task 3), regenerated at the end:** every cited file is under `receipts/`, re-collected from scratch;
  host paths, account names and the host's name are replaced (0 residual tokens); the repository's privacy scrub
  (`docs_check.scrub_files`) finds nothing over the whole folder; no file is over 200 KB; `INDEX.md` is generated
  from the files present.
- **Step 11, p11:**
  - every firmware image is hash-equal to the candidate's;
  - the confirmation diff is empty in all 7 groups, so the CPU rows carry;
  - the split routes meet #818's floor at both points: 1x1/1if +0.141 / +0.033 ns and 8x8/1if +0.073 / +0.034 ns
    (+0.005 before #927; the EDIT path no longer binds);
  - every gate passes.
- **The release image's resource gate:** exit 1 on LUTs alone, 54,002 against the record's 53,461 (+541 past 500).
  #927 brings about +400 of it. RAMB36 falls 74 to 71, and timing holds (+0.194 / +0.017). Re-baselined at
  `73272666` (RULINGs 1118d, 1118e and 1118f); the gate now exits 0.
- **`cdc_pair_fifo`'s default branch:** behaviour-identical by reading and by a bounded proof, complete at every LOG2D a
  default instance takes: **LOG2D 2, 3 and 4, no counterexample in 30 steps** (`fifo-bmc4` ended 14:25:40, rc 0;
  LOG2D 4 took 1,184 s, 220,519 variables). Vivado alone maps it identically at three of four parameter sets; at 48/4, an instance not in these
  images, it uses 2 fewer LUTs.

**THE CPU VERDICT: PASS.** U, the image that carries 8x8/1if's SRP unit at 375 us, holds every test of RULING-1118b
item 2b at 8x8/1if over every arm (arm A, answering-every-port, answering-ports, valid-destinations; complete 12:25;
`receipts/regrade/verdict-unit375-final.txt`):

| Test (item 2b) | U, unit 375 |
|---|---|
| the SRP record within its unit | 35,547 cycles, 375 us, **within 375** (167 cycles of margin) |
| every statement within its figure | one over, then restated by the unchanged rule: ADP's record 12,779 cycles in arm A's `backlog-adp-refill`, 135 us against 130 (as on B's image). Restated, so 0 exceeded |
| the load at 0.75 or less | **0.744** (with ADP's 135) |
| THE TRANSMIT's row within its figure | 76.81 ms of 77 |
| no budget miss | none, apart from the seven `backlog-owed` egress-hold rows the harness README ledgers ("miss their budget at every point"; the scenario's 60 ms hold), as at every point since round 4 |
| join intervals in range (181 to 239 ms) | 119 lines, 187.15 to 190.41 ms |
| the code: shards, the control campaign, the twin; no plant removed | PASS (797 of 797 caught; twin and its plants) |
| the 1x1/1if and 8x8/2if images byte-identical to the measured head's | yes, every arm (hash table below) |

**The lowest unit that holds is 375**, so U+1 (380) is not taken. U+1 holds too, over every arm: the SRP record within 380 by 643 cycles, the same ADP restatement, the load 0.744, 119 join lines in range and the seven egress-hold rows (`receipts/regrade/verdict-unit380-final.txt`).

**The final step-10 candidate is `flip-train-1117-p10` at `4374cc27`.** It is `c8ff391a` plus ADP's restatement, with
`load_grade`'s two own-record controls re-anchored to read the measurement's figure from `OWN_MEASURED` rather than a
literal 130 (28 of 28 refused, before and after). The images are unchanged. Its quick list passes but for `flip_check`, which reports exactly 8x8/2if's base eleven and, at 8x8/1if, only THE TRANSMIT's HELD line (76.81 of 77). `run.py --self-test` has 0 failures and `load_grade` 28 of 28.

**Step 11 (RULING-1118c): `flip-train-1117-p11`, final head `b1f1161b`**: #939's `0297a19a` merged on the candidate
(`3e908539`), then `4374cc27` carried (`74481d2e`), then the preflight fix (`05dc1791`), then the record-only
re-baseline (`73272666`), then the regenerated documentation audit (`b1f1161b`). Its RTL and images are `3e908539`'s. Nothing is pushed; the manager pushes.

| Step 11 item | State | Lands (estimate) |
|---|---|---|
| Hashes: every split firmware image at p11, per arm and point, against the candidate's | **all 12 EQUAL** (`receipts/regrade/image-hashes-p11.txt`) | done |
| Confirmation run on p11's RTL against the candidate's receipts: 8x8/1if `srp-talker-held` and the answering-ports arm (`aecp`, `aecp-largest-notice`, `aecp-fanout`); 1x1/1if `aecp-largest-notice` and `aecp-fanout`; 8x8/2if `aecp-fanout` | **EMPTY DIFF, all 7 groups:** the same stimulus, byte-identical logs (`srp-talker-held` alone is 761,187 SPAN lines, every one equal) and every measured figure equal (`receipts/regrade/confdiff-final.txt`). **The CPU rows carry to p11** (RULING-1118c item 2: hashes equal and the diff empty) | done 12:50 |
| Split routes at p11, three directives each, #818's floor (WNS >= +0.030 ns, WHS >= 0 at every corner) | **8x8/1if: MEETS on its best of three**: ExtraPostPlacementOpt **+0.073 / +0.034** (both floors; #927's own head +0.073 on that directive), ExtraTimingOpt +0.064 / +0.027 (met), AltSpreadLogic_high +0.006 / +0.036 (not met). Its worst paths are now on the mailbox clock (`KL_mbx` register read, `u_rx`). The datapath clock's worst is +0.835 to +0.989 ns, so the EDIT-window path no longer binds (+0.005 before #927). **1x1/1if: MEETS on all three**: ExtraPostPlacementOpt **+0.141 / +0.033** (the best; both floors), ExtraTimingOpt +0.054 / +0.036, AltSpreadLogic_high +0.031 / +0.036 (`receipts/regrade/fit-summary-p11.txt`) | **done 13:15** |
| The release (all-fabric) image's route set and resource gate at p11 | **Timing: the floors hold.** ExtraPostPlacementOpt +0.115 / +0.033, AltSpreadLogic_high +0.053 / +0.017, ExtraTimingOpt **+0.194** / +0.017 (selected); the route is complete. **`pp_resource_gate.py check --endpoint route-1x1`: exit 1, MATERIAL REGRESSION, on LUTs alone:** 54,002 against the record's 53,461, +541 past the 500 tolerance. FF 55,203 (+232, ok), SLICE 15,849 (0), **RAMB36 74 to 71** (the gate recommends a re-baseline for that), RAMB18 27, DSP 15, WNS 0.194 (record 0.334, a fall under the warning), WHS 0.017. The sub-block movements are protocol-processor LUTs of +-53 or less (not gated). At synthesis the candidate's release image has 56,526 LUTs and p11's 56,946 (+420). **Attribution, on the same directive** (ExtraPostPlacementOpt): the candidate's release image (`c8ff391a`, before #927) places 53,571 LUTs, 54,944 flops and 87.5 block RAM tiles, and p11's 53,971, 55,206 and 84.5. So **#927 brings about +400 LUTs** (+420 at synthesis), +262 flops and -3 tiles. The train before it is +110 over the record, inside the tolerance, and #927's share takes the image past it. RULING-1118d's re-baseline is held at its item 2, since `u_fcdc` changed primitives (the STOP above; `receipts/step11/release/resource_gate.log`, `receipts/step11/release/hier-diff.txt`) | done 13:40; the hierarchy 14:17 |
| Gates at p11: four shards, the twin, the milan_dp suites #927 touches | **ALL PASS:** the four shards (797 of 797 caught), the twin and its plants and maps legs, split, split-mutants, split-cdc, dynmap, maprec8, maprec4, aaf_clock_meter all and mutants, tdm8render and tdm8render-mutants (32 of 32), mbx all and dma-mutants (`receipts/step11/gates/`) | done 13:28 |
| `cdc_pair_fifo.sv`'s default branch (review point) | **Behaviour: identical by reading.** The write fires on `wrst_n && wen_i && !wfull_o`, as the old write sat in the reset's `else`. `rdata_o` resets on `!rrst_n` and loads on `ren_i && !rempty_o`, on the same clock. **A bounded Yosys equivalence of the old against the new module** (a miter; both clocks free under `clk2fflogic`, so any interleaving of write and read edges; from the zero state; every output equal at each of 30 steps; WIDTH 4, since no logic crosses data bits, at each LOG2D a default instance takes) finds **no counterexample at LOG2D 2, 3 and 4** (`SAT proof finished - no model found`; LOG2D 4 at 14:25:40; `receipts/step11/fifo/bmc4.out`). The 40-step full-width runs timed out without a counterexample. **Inference:**
(1) Vivado's standalone synthesis of the module alone is **identical, primitive for primitive, at 48/3, 52/3 and 192/2**. 52/3 is the TDM capture's `u_tcdc`, the default-branch instance the shipping images carry. At **48/4** (the I2S playback's FIFO) the storage and flops are identical (32 LUTRAMs, 88 flops), but the control logic maps to **22 LUTs instead of 24** (LUT6 14 to 11). It is not identical there, and that is the reviewer's to judge; that instance is in none of the release or split images measured here, whose reports list only `u_tcdc` and `u_fcdc` (`receipts/regrade/fifo-ooc-vivado.txt`).
(2) Yosys maps all four sets to identical Xilinx cells.
(3) In the built images, `u_tcdc` keeps 36 LUTRAMs, no block RAM and the same flops at 1x1/1if, 8x8/1if and the release image, and its logic LUTs move with the context (+1 and -1 at the split points; 32 to 21 at the release image).
Only `KL_tdm_render_master`'s `u_fcdc` takes `DIST_RAM_P = 1`: 3 RAMB36 to 0 and 24 flops to 216, so the 1x1/1if split image falls from 83 to 80 block RAM tiles, and the release image from 74 to 71 RAMB36: the render master's crossing is shared, not split-only, so every image that carries it takes the distributed storage (RULING-1118e item 2). The sims (split, split-mutants, split-cdc, dynmap, maprec, the meter, tdm8render, the twin) PASS | done 14:25 |

## The step-10 candidate and how it was built

**The candidate is a real commit on `flip-train-1117-p10`, now `4374cc27`** (`c8ff391a` until 12:40). It is B (`41d2bc2b`, the notice and listener
cuts on the final head) with:

- `3cdc613b`: 8x8/1if's `CTRL_LOOP_TX_MS` 77 (its row 76.81 rounded up; at most 80, so `SRP_REDECLARE_CS` stays
  8 cs) and its `CTRL_LOOP_SRP_UNIT_US` 375, with `record.srp` restated to 375 there;
- `0cfe1ddc`: every other restated statement;
- `7a536fc5`: one control re-anchored;
- `0b054867`: the prose;
- `c8ff391a`: a self-test check re-anchored to item 2b (`run.py --self-test`: 0 failures);
- `4374cc27`: 8x8/1if's ADP record restated to 135 (U's arm A), the two own-record controls reading it;
- `bf2c1184`: the ledger.

**Its images hash-equal the measured ones**, `ctrl_app.elf` sha256 per arm (`receipts/regrade/image-hashes.txt`):

| Point | Arm A | answering-every-port | answering-ports | valid-destinations | Equal to |
|---|---|---|---|---|---|
| 1x1/1if | `55484254` | `4e7b53c7` | `6971e95c` | `8ca50418` | B's, every arm |
| 8x8/1if | `175418f4` | `ea87356a` | `3c15ec34` | `e764b2fe` | U's, every arm |
| 8x8/2if | `ba343fd4` | `f64be15e` | `8c9fe28b` | `cf299386` | B's, every arm |

So U's 8x8/1if measurement is the candidate's, and B's 1x1/1if and 8x8/2if measurements stand for it. `CTRL_LOOP_TX_MS`
reaches the image only through `SRP_REDECLARE_CS`'s `(TX + 9) / 10`, 8 at both 75 and 77. The unit changes one
immediate.

**Done:** B at every point. The candidate's shards (797 of 797) and twin at `0b054867`, whose images `c8ff391a` keeps.
The quick list at the final tip `c8ff391a` passes but for 8x8/2if's base eleven (`flip_check`: exactly those 11; at
8x8/1if only THE TRANSMIT's HELD line, 76.81 of 77), with `run.py --self-test` at 0 failures. Fit and the timing floor
are in on the candidate at both points (below). U's answering-ports, valid-destinations and answering-every-port arms
are complete.

**B is complete at every point**, graded against the candidate's tables: 1x1/1if and 8x8/2if (the candidate's
images there) have no statement exceeded. The paced records are 310 of 310 and 585 of 595. The only budget findings
are the seven `backlog-owed` egress-hold rows at each point, as at round 4's tip.

**The candidate's own routes, before step 11** (the candidate `3cdc613b`, the AX7101 split route by the #810 route lane's recipe,
08:51 to 10:00; the floor is WNS >= +0.030 ns and WHS >= 0 at every signoff corner, and the stricter WHS >= +0.030
too; `receipts/regrade/fit-summary.txt`):

| Point | Directive | Worst WNS (Slow) | Worst WHS (Fast) | Failing setup / hold | LUT | BRAM tiles | Floor |
|---|---|---:|---:|---:|---:|---:|---|
| 1x1/1if | ExtraPostPlacementOpt (integrated) | +0.119 ns | +0.032 ns | 0 / 0 | 32,095 (50.6 %) | 83 | **met, both floors (the best set)** |
| 1x1/1if | ExtraTimingOpt | +0.002 ns | +0.014 ns | 0 / 0 | | | not met |
| 1x1/1if | AltSpreadLogic_high | +0.147 ns | +0.014 ns | 0 / 0 | 32,193 (50.8 %) | 83 | met; the stricter WHS not |
| 8x8/1if | ExtraPostPlacementOpt (integrated) | +0.005 ns | +0.036 ns | 0 / 0 | 43,361 (68.4 %) | 94.5 | not met |
| 8x8/1if | ExtraTimingOpt | **-0.019 ns** | +0.036 ns | 5 / 0 | 43,317 (68.3 %) | 94.5 | not met |
| 8x8/1if | AltSpreadLogic_high | +0.005 ns | +0.036 ns | 0 / 0 | 43,313 (68.3 %) | 94.5 | not met |

The routes carry the target platform's image at one interface, linked from the candidate (`ctrl_app.elf` sha256
`a00828fe` at 1x1/1if and `5edbba3a` at 8x8/1if). They are measurement routes: checkpoints and reports, with no
bitstream written.

**1x1/1if meets the floor on its best of three** (ExtraPostPlacementOpt: +0.119 / +0.032, both floors).

**8x8/1if MISSES the timing floor on all three directives:** best +0.005 ns, 0.025 short of +0.030. Hold is met at
every corner. Every directive's worst path is the same one, on the datapath clock (`milansoc_crg_clkout1`): from the
map edits' EDIT-window request in the mailbox's clock crossing (`KL_mbx_cdc/u_edit/rq_r[80..82]`) to a clock enable
in the datapath's AAF map state (`milan_datapath/amap_edit_oclaim_expect_r`, `amap_out_owner_r`). It has 33 to 38
logic levels and 71 to 74 % routing, over 19.5 to 19.7 ns. It is the same path family the #810 route lane's report
names at that PR's head (30 to 40 levels there, +0.001 ns on one directive, +0.292 on its best): placement-sensitive
RTL in the mailbox's EDIT window and the datapath's AAF map.

**The miss is the composed train's, not the candidate's.** The candidate changes no RTL, and its 8x8/1if image differs
from B's in the ROM's contents only. B's own image (`bf2c1184`, firmware `d0e19e37`, 2 bytes from the candidate's),
routed the same way, gives the same three results on the same paths: +0.005, -0.019 (5 failing) and +0.005 ns.
This lane may not change RTL. The cut would be the RTL's: pipelining the EDIT request into the AAF map's claim and
owner clock enables, or narrowing that cone. It belongs to the EDIT window's owner, and the owner decides whether
8x8/1if's floor gates the flip.

**Already in.**

- **B's 1x1/1if, every arm complete, graded against the candidate's tables** (the candidate's images there are B's):
  no statement exceeded. The paced record is 29,331 cycles, 310 of 310, and the long record 865 of 975. Its 7 BUDGET
  findings are all the `backlog-owed` group's egress-hold rows (`backlog.owed*`, `backlog-owed.service.*.last`, 62 to
  64 ms against 20). They are set by the scenario's 60 ms egress hold, which the harness README says "miss their
  budget at every point" and records without failing; the egress ledger holds them. Round 4's tip had the same 7
  there and at 8x8/1if. No other budget finding.
- **A self-test check re-anchored (to commit):** `run.py --self-test` failed one check at the candidate. It asserted
  8x8/1if's `record.srp` equal to 8x8/2if's, the nearest-point premise that item 2b replaces. Now every 8x8/1if
  record and event must be 8x8/2if's raised to its own where OWN states one, which covers more keys and still fails
  when the two disagree. The re-run is in progress; the images do not change.
- **The candidate's gates at `0b054867`:** the four firmware shards PASS, the control campaign catching 797 of 797
  (no plant removed; one re-anchored this round, `7a536fc5`). The twin PASSES: the two-placement comparison, its
  plants, the maps leg and its plant.
- With the candidate's tables, B's 1x1/1if PASSES (ACMP 29.93 of 30, txL 48.89 of 49, the last queued notice 137.97
  of 140; the load 0.522) and 8x8/2if has the base's eleven findings only (its tx row 104.69 within its 105).
- At 8x8/1if the tables pass `flip_grade.py --check` on B's figures: THE TRANSMIT's row 76.81 ms within 77, the load
  0.744 of 0.75. U's own figures replace B's there as they land.
- The host tests that read `CTRL_LOOP_TX_MS` (`srp_talker.cpp`: `kHoldOffMs` and `kLatestLeaveMs`) PASS at 1x1/1if,
  8x8/1if and 8x8/2if (16 of 16 each; `receipts/regrade/talker81.txt`). The suite runs them at 1x1/1if and 8x8/2if;
  8x8/1if was run in addition, since its figure moved.

**S12b.** The gating S12b runs, uncut, on the final bitstream only (RULING-1118c item 3), that is p11's image once
#939's two reviews are POSITIVE at its frozen head. A run on a pre-#927 image is a rehearsal. p11's split routes meet
#818's floor at both points so far (status table); the release image's route and gate land about 13:45. The CPU pass
is in, so nothing on this lane's side holds S12b beyond those routes and #939's reviews.

## The rule for the pass (RULING-1118b, item 2b), at 8x8/1if over every arm of the image that carries the unit

- the SRP record within its unit, and every statement within its figure;
- the load at 0.75 or less;
- no budget miss, and join intervals in range;
- the code passing the firmware shards, the control campaign and the two-placement comparison, with no plant removed;
- the 1x1/1if and 8x8/2if images byte-identical to the measured head's (shown above).

The lowest unit that its own image holds is taken: 375 (U) if it holds, else 380 (U+1).

## The figures at each point (B's restated tables, now the candidate's)

The figures are `flip_grade.py --check --point` (`receipts/regrade/rows-0cfe1ddc.md`, the tables before the 8x8/1if
unit and figure moved). A row's figure is against its bound, and a negative margin is inside. 1x1/1if's and
8x8/2if's carry to the candidate unchanged.

### 1x1/1if: PASS

| Row | Figure, ms | Bound, ms | Margin, ms |
|---|---:|---:|---:|
| R4 | 13.43 | 20 | -6.57 |
| R5 | 76.55 | 90 | -13.45 |
| R6 | 74.05 | 90 | -15.95 |
| first | 14.75 | 20 | -5.25 |
| last (queued notice) | 137.97 | 140 | -2.03 |
| R4L | 203.58 | 238 | -34.42 |
| ACMP | 29.93 | 30 | **-0.07** |
| ADP | 28.14 | 30 | -1.86 |
| MAAP | 28.23 | 30 | -1.77 |
| tx | 34.30 | 49 | -14.70 |
| txL | 48.89 | 49 | **-0.11** |

The load is 0.522 of 0.70. The one restatement is the paced record: 29,331 cycles, **310 us** (stated 305; 192 cycles
from 315, at which the last notice would be 141.39 ms of 140).

### 8x8/1if: decided on U's figures

- **On B's image** (the unit at 365): the load 0.744 of 0.75; THE TRANSMIT's row 76.81 ms, which `CTRL_LOOP_TX_MS`
  now states as 77 (RULING-1118b, item 2a: the figure follows its row and is not an owner bound; txL's 49 ms, held at
  1x1/1if, is). The rows are reported, not held (#872).
- **The SRP record**, 35,547 cycles (375 us), restated to 375 with the unit (item 2b). U measures it on the image
  that carries the unit.
- **Restated by the rule:** the polls base **300** (28,417 cycles), the apply **375** (35,350), the MAAP record **180**
  (16,682, `srp-talker-loss`) and the SRP record **375**.
- **The tx row against the figure**, for reading U's figures (the candidate's tables, `events_none` 45 from 8x8/2if
  by the nearest-point rule): a polls base of 295 gives 76.65 ms, 300 gives 76.81, 305 gives 76.97, and 310 gives
  77.13. So 77 holds while U's base is 305 us or less (29,047 cycles; B's 28,417 is 630 under). Past that, the figure
  follows the row up, and it must stay 80 or less. The base's heaviest pass and its cause are traced in the evidence
  below.

### 8x8/2if: the base's eleven findings, no twelfth

| Row | Figure, ms | Bound, ms | Margin, ms |
|---|---:|---:|---:|
| R4 | 45.24 | 20 | +25.24 |
| R5 | 209.68 | 90 | +119.68 |
| R6 | 199.36 | 90 | +109.36 |
| first | 21.13 | 20 | +1.13 |
| last | 867.89 | 125 | +742.89 |
| R4L | 211.12 | 238 | -26.88 |
| ACMP | 69.22 | 30 | +39.22 |
| ADP | 69.16 | 30 | +39.16 |
| MAAP | 73.41 | 30 | +43.41 |
| tx | 104.69 | 49 | +55.69 |
| txL | 474.19 | 49 | +425.19 |

The load is 0.799 of 0.70. The eleven are the base's: the load, R4, R5, R6, first, last, ACMP, ADP, MAAP, tx and
txL. **THE TRANSMIT's held figure is within: the tx row's 104.69 ms against `CTRL_LOOP_TX_MS` 105** (0.31 ms
margin). The notice item is 25,561 cycles (270 of 275 us, 629 cycles inside); before attempt 2 it was
28,960, the twelfth finding. Restated by the rule: the MAAP record **160** (14,770), a pass's events' fixed part
**45** (4,069) and AECP's timer event **120** (11,404, its cause traced below).

### The fixture and the platform ROM (S14 debt)

The size fixture is within its 60.5 in all six arms (130,952 to 131,448 B of `rom`; S14 debt of 4.5, unchanged). The
platform's 8x8/1if image needs 137,472 B, 256 B past 57.5, so **its entry is 58.0, S14 debt of 2.0** (`bf2c1184`). Its
other points are within their entries.

## Owed at the final tip

- The #495 residue (RULING-1118f item 5): the timing findings document is to list the render crossing's CDC-15 x192
  beside the capture crossing's; the waiver question waits for after the flip.
- Everything else of RULING-1118c is in: the routes, the release route set and gate, the confirmation, the hashes, the
  gates and the FIFO review point.

## The evidence (the measurements and traces behind the figures above)

- **B, the answering-ports arm** (all three points): the 8x8/2if notice item is 25,561 cycles (270 of 275 us, 629
  cycles of margin), and the 8x8/2if paced record (SET_CONFIGURATION) 55,239 (585 of 595). The 1x1/1if paced record is
  29,331 (310 us by the rule, restated from 305; 192 cycles from 315).
- **The 8x8/1if polls base**, the heaviest pass of `srp-talker-held` (sys about 5.04e8, the pass after a Listener
  Ready licenses a declared Talker): **B 28,417 cycles (300 us), 322 past the 28,095 that 295 holds**; A 28,258 (300);
  the final head `b5802de9` 30,631 (325); round 4's tip 29,933. In that pass every source's Listener presence changes,
  so the listener cut saves nothing there. Its polls: `maap_mbx:poll` 8,367, `ctrl_app_aecp:deliver` 7,736,
  `aecp_mbx:poll` 6,192 (a 3,582-cycle transmit in it), `ctrl_app_srp:deliver` 2,545, `srp_mbx:poll` 2,310, ACMP's
  and ADP's 620. B's SRP record there is 35,547 (375 us) and its apply 35,350 (375).
- **The first re-grade with B's figures** (06:30, superseded by the tip's figures above; real edits, the rest at round 4's: 1x1/1if paced 310, 8x8/1if base 300,
  apply 375, SRP record 375, MAAP event 240, 8x8/2if MAAP record 160 and AECP event 120, the notice item within its
  275): 1x1/1if PASS (the last notice 137.97 of 140, ACMP 29.93 of 30, txL 48.89 of 49); 8x8/2if the base's eleven
  only (its tx row 104.50 of 105); **8x8/1if: THE TRANSMIT's row 76.61 ms against the 75 then stated**, the load 0.743
  of 0.75. At a base of 295 the same tables give 74.89 ms, the manager's figure, so the step lies between 295 and 300
  and the base must be measured at 28,095 cycles or less.
- **Gates.** At the p10 tip `bf2c1184`: the four firmware shards PASS, the control campaign catching 797 of 797
  (as at `082d0037`; no plant removed, three re-anchored), and the twin (the two-placement comparison, its plants and
  the maps leg) PASS. At the step-9 head `112ab9b1`: the four shards PASS (797 of 797), the twin PASS and firmware
  coverage PASS (40 files; T8 restores `mbx.c`'s 194 of 194). At `7b3c1c94` (the listener cut, before T8): the four
  shards and the twin PASS.
- **The ROM ledger at the p10 tip `bf2c1184`**, restated to the measured images: PASS at four points, 9 of 9 controls,
  and `test_ctrl_memory` PASS. The size fixture needs 130,952 to 131,448 B over its six arms, within its 60.5 (S14 debt
  of 4.5, unchanged). The platform's 8x8/1if image needs 137,472 B, 256 B past the 137,216 that 57.5 holds, so its
  entry is **58.0, S14 debt of 2.0**. `ctrl_plat` is 18,048 B at 1x1/1if and 21,568 at 8x8/2if (#936's 64 B).
- **The 8x8/1if miss's measured cause** (B's heaviest pass traced by committed PC on B's own build, `cut/b81-base`):
  28,417 cycles, 4,550 instructions, CPI 6.2, fetch-bound. 855 cycles run in code the list leaves cold, among them
  `aecp owed_drain` (470) and `aecp_mbx fan_end` (347). `owed_drain` is one of the filter's two drops: the 8x8/2if
  images do not link it, but 8x8/1if's do. By function, the dearest:

  | Function | Instr. | Cycles |
  |---|---:|---:|
  | `ctrl_app_srp deliver` | 445 | 2,317 |
  | `aecp fan_out` | 122 | 1,719 |
  | `ctrl_app_srp source` (ACMP's forwarding source callback, 9 calls) | 54 | 1,674 |
  | `acmp acmp_declaring` (TSN stack) | 468 | 1,366 |
  | `srp_mbx poll` | 199 | 1,283 |
  | `ctrl_mem memset` (ACMP's source state, each source) | 405 | 1,206 |
  | `ctrl_app_aecp deliver` | 159 | 1,188 |
  | `aecp arm` | 266 | 1,114 |
  | `maap_mbx refresh_demand` | 120 | 1,076 |
  | `aecp_nvm_poll` | 188 | 981 |

  MAAP's demand, which asks ACMP's `acmp_declaring` about each of the nine sources every pass (through `memset`, the
  forwarding callback and the fixture's source port, with ACMP's `now`), is about 6,600 cycles of it. The store and
  face publication (`aecp_nvm_poll`, `nvm_mark`, `ctrl_app_aecp_store_words`, `nvm_rec_id_known`, the face's
  `publish`) is about 4,900. This is the pass after a Listener Ready licenses a declared Talker, in which every module's
  state moves at once. So a cut that skips unchanged work saves nothing here, as the listener cut showed. A cut must
  make the change itself cheaper, take it out of `acmp_declaring` (the TSN stack, a pin move), or move code into the
  fetch cache's reach (the list's procedure, a ruling).
- **What the filter costs at 8x8/1if, measured** (a moot option since RULING-1118b keeps the LINKED gate; the manager
  stopped N and NU at about 08:40, and their finished legs are receipts). N is B's code with its traced list unfiltered (268 entries:
  `aecp owe` and `aecp owed_drain` kept where the trace put them; `21486e00`, scratch). In `srp-talker-held` its 8x8/1if
  polls base is **27,792 cycles (295 us), 303 cycles inside the 28,095**, and 625 under B's 28,417. Its SRP record is
  35,589 (375) and its apply 35,392 (375). Both entries link in the 8x8/1if and 1x1/1if images; only the size
  fixture's 8x8/2if images lack them, and with the gate unchanged the LINKED rule refuses those builds. The target
  platform's image already links the same script without that check, where "an entry it lacks places nothing there".
  So the cut the 8x8/1if row needs is exactly what ruling item 1's filter took away there.
- **The 8x8/2if `event.AECP`, traced before it is restated** (as asked). B's dearest AECP timer event (TIMER#6) is
  11,404 cycles (120 us against its 115; round 4 measured the same 120), in the answering-every-port arm's
  `notice-burst-6`. The traced one is the same burst step in `notice-burst-3` (`aep/part1`, CPU cycle 306,501,852),
  11,381 cycles. Traced by committed PC on B's own build
  (`cut/b2-aecp-event`): 1,770 instructions, all in listed code. `aecp arm` is 975 instructions and 3,790 cycles, and
  `aecp_poll` 398 and 3,683. The rest is the loop's take and the other modules' event stubs (about 150 cycles each).
  The event runs the core's `aecp_poll` (`aecp_mbx.c` `event`). Each time the core re-arms its timer, `arm()`
  (`aecp.c:181`) walks every registration on both interfaces and then the live notice list, to find the earliest
  deadline. In a notice burst with every port's controllers registered, that walk is the cost. It is the core's
  design, unchanged by attempt 2 (`git diff ed5855fe 41d2bc2b -- sw/firmware/ctrl/aecp/aecp.c` touches only the
  notice fan-out: `address`, the new `source` and `fan_out`), so it is restated by the rule: **120**. A cut would keep the earliest registration deadline
  as registrations change instead of scanning on each arm.
- **The 8x8/1if SRP record and its header constant** (raised at 06:25; RULING-1118b, item 2b, settles it: the unit
  follows its record on the image that carries it). The record (`srp-talker-held`'s
  Listener Ready) is 35,571 cycles at `b5802de9` (375 us) and 35,805 at round 4's tip (380), against a statement of
  365. `load_grade.py --check` refuses a `record.srp` other than `ctrl_loop.h`'s `CTRL_LOOP_SRP_UNIT_US` at the point's
  shape (its `srp_unit` check). The manager's what-if restates `OWN['8x8/1if']['record.srp']` to 380 but runs only
  `flip_grade.py`, so that check does not run. With the real edit, restating the record moves the header constant,
  which ruling item 2 rules out, though ruling item 3 says the record holds "its statement (restated)". The unit is
  not an immediate the measurement can ignore. In `b5802de9`'s run, 49 SRP records start between 1,095 and 1,120 us
  into their 1,475 us slice, which a unit of 380 would defer. So a moved unit needs 8x8/1if measured again, which the
  precedent did too ("every one-interface leg was measured again").
- **Ruling item 3, why the relearned list costs the SRP record.** The three windows are 1x1/1if arm A's (backlog,
  backlog-adp, aecp-largest-notice), and none runs SRP's Listener path. The relearned list therefore leaves cold what
  the pre-relearn 206-entry list (step 9's) kept hot: `memcmp`, `msrp_attr_cmp`, `rx_on_attr`, `parse_pass`, `same`,
  `mrp_attr_registered_ports`, `interested_msrp`, `apply_receive`, `msrp_decode_attr` and `listener`. In round 4's
  trace of this record, 21,396 of its 35,506 cycles ran in cold code. #930 measured the record at 32,936 cycles on the
  older list.
- **Ruling item 3, measured: the relearned list is no worse for the SRP record at any point.** The old list was run on
  B's own code (`b4f9f26c`, a scratch commit of `6448e431` with `082d0037`'s list and link script) in
  `srp-talker-held`, the group holding the SRP record at every point (other groups' records are 21,000 to 23,000
  cycles at 8x8/1if). Cycles, each run's whole group (`results.json`, and its heaviest `srp_mbx:receive` span):

  | Point | SRP record, relearned (B) / old | Its apply, relearned / old | Polls base, relearned / old |
  |---|---:|---:|---:|
  | 1x1/1if | **23,103 (245)** / 23,662 (250) | 22,748 / 23,188 | 19,248 / 18,908 |
  | 8x8/1if | **35,547 (375)** / 36,377 (385) | 35,350 / 36,012 | 28,417 / 27,814 |
  | 8x8/2if | **30,391 (320)** / 30,898 (325) | 30,061 / 30,405 | 27,633 / 27,443 |

  Keeping the SRP receive path hot does not help: in the 4 KiB direct-mapped fetch cache, where code lands outweighs
  whether it is listed. The old list measures better on the polls base, by 190 to 600 cycles. At 8x8/1if that is
  27,814 (295), inside the 28,095 target, but the list is not the ruled procedure's, so it is a measurement, not an
  option.

## Heads

| Head | Branch | What |
|---|---|---|
| `112ab9b1` | `flip-train-1117`, the step-9 branch with the cuts | `ed5855fe` (round 4); the notice cut `067c319d` and its include fix `0bc158a7`; the listener cut `7b3c1c94`; the DMA driver's T8 test `112ab9b1` |
| **`4374cc27`** | `flip-train-1117-p10`, the step-10 candidate (the CPU pass) | rebuilt from `ed5855fe` (round 4's tip kept as `refs/ref/p10-r4`): #944's frozen head `d1aa4c44` merged (`49f005b9`); the idiom fix `082d0037`; the filtered relearn `b5802de9`; the cuts carried and re-traced (`26f30fea`, `3e1c3dd9`, `68c97849`, `08c28218`, `41d2bc2b` = B); T8 (`6448e431`); the ledger (`bf2c1184`); a control re-anchored (`7a536fc5`); B's restatements (`0cfe1ddc`); 8x8/1if's TX 77 and SRP unit 375 (`3cdc613b`); the prose (`0b054867`); a self-test check re-anchored (`c8ff391a`); ADP's restatement (`4374cc27`). From `41d2bc2b`'s cuts on, its 8x8/1if images are U's measured ones and its other images B's |
| `b1f1161b` | `flip-train-1117-p11`, step 11 (RULING-1118c), the step-11 head (`05dc1791`, the record-only re-baseline `73272666` (RULING-1118f), then the documentation audit regenerated) | #939's frozen `0297a19a` merged on `c8ff391a` (`3e908539`), then `4374cc27` carried (`74481d2e`), then the preflight fix: `plat_mutants.py`'s blank line at the end dropped. Built in a scratch clone and fetched into the lane repo. No re-baseline commit (the STOP at RULING-1118d item 2) |
| **`967b1ca9`** | `flip-train-1117-p11`, step 12: `b1f1161b`, then #947's `66c6edf3` merged (`d09c7118`), then the ROM ledger at 63.0 (`967b1ca9`) |

Nothing is pushed. The scratch variants (`b4f9f26c` old list, `21486e00` N, `dd5f60e0` NU, `40a6c1a5` U, `b1a8424f` U+1)
exist only in their clones.

## The re-grade before measuring (ruling item 4), by real edits

Round 4's figures, restated by the unchanged rule as real edits to `edit_rows.PACED`, `load_grade.OWN`,
`poll_grade.EIGHT_ONE` and `TWO`, and `load_grade.STATED_US` / `STATED_US_DONOR` at 8x8/2if, at `082d0037`.
`flip_grade.py --check` reproduces the ruling's figures: 8x8/1if's load is 0.752 of 0.75 and THE TRANSMIT's row 77.09
against 75 ms; at 8x8/2if a twelfth finding, THE TRANSMIT's row 107.79 against 105 ms; 1x1/1if holds, ACMP's margin
0.07 ms.

| Case (the rest as round 4 measured) | 8x8/1if | 8x8/2if |
|---|---|---|
| polls base 295, the 8x8/2if notice item 305 | FAIL: load 0.752 | twelfth finding (tx 107.79) |
| polls base 295, the notice item kept at 275 | PASS: load 0.746, tx 74.89 of 75 | the eleven only |
| polls base 295, SRP 370 / apply 365, the notice item 305 | PASS | twelfth finding (tx 107.79) |

So attempt 2 needs both: the 8x8/1if polls base measured at 28,095 cycles or less (295 us by the rule), and the
8x8/2if notice item at 26,190 or less (275 us). The 1x1/1if paced record must stay within 310 us (29,523 cycles).

## The final head, `d1aa4c44` merged

#944's frozen head (GitHub head checked) merged `--no-ff` on the rebuilt p10, round 4's resolutions reused
(RESOLUTIONS.md). The size moves of #936's last commit left the union's `run.py` at 1,013 lines; `082d0037` moves
#936's talker-notice plants' verdict into `talker_notice.py`, its body unchanged, so `run.py` is 994 and the idiom
gate passes. At `082d0037`: the four shards PASS (the control campaign 797 of 797), the twin and its plants PASS,
and the quick list PASSES but for the base's eleven 8x8/2if flip findings.

**The hot list, ruling item 1.** Re-traced by the three windows at `082d0037`: 269 functions, the same set as round 4's.
The filter kept every entry whose section links in every split image `ctrl_srp_image.py` holds to the list: the
size fixture at the three points in all six arms, as itself and as the SoC plan's stand-in and mapped images (54
link maps). It drops `aecp owe` and `aecp owed_drain`, which the 8x8/2if images lack in every arm; 267 are kept
(`b5802de9`). The target platform's image links the same script but is not held to it. On the stricter reading
that counts the platform's four images as served, five more would go: the size fixture's own `ctrl_aecp_image`
functions (`source`, `allocation`, `notice`, `a_random`) and `ctrl_loop_run`, none of which the platform links.
That reading was not taken, and it is flagged for the manager.

**At the final head (`b5802de9`), the answering-ports arm** (cycles; by the rule):

| Point | Long record | Paced record | Other record | `aecp` notice item |
|---|---:|---:|---:|---:|
| 1x1/1if | 83,269 (875 of 975) | **29,998 (315 of 305)** | 22,138 (235 of 245) | |
| 8x8/1if | 153,733 (1,615 of 1,715) | 56,826 (600 of 685) | 19,911 (210 of 265) | |
| 8x8/2if | 148,840 (1,565 of 1,650) | 55,926 (590 of 595) | 18,780 (200 of 265) | **28,960 (18 over 27,500)** |

So the final head without attempt 2 cannot pass. The 8x8/2if notice item gives the twelfth finding, and a paced
record at 315 puts the last queued notice at 141.39 of 140 ms (ruling item 2).

## Attempt 2, cut 1: a notice's per-recipient work (`067c319d`, `0bc158a7` on the step-9 branch)

The 8x8/2if notice item (the `aecp:transmit` span, 32 recipients), traced by function in round 4's variant:
`mbx_tx_begin` 3,200 instructions / 10,753 cycles in 33 calls, `fan_out` 2,439 / 10,522, `mbx_tx_commit` 1,223 /
4,840 in 35 calls, `aecp_mbx fan` 320 / 1,024, about 850 cycles a recipient. The cut:

- a buffer's source MAC is stored only when its interface changes (the fan port's two buffers alternate, and each
  keeps its source from one recipient to the next);
- the port's calls and context and the registration's sequence_id are read once (a frame's byte stores could
  alias them, so the compiler reloaded them for every recipient);
- the transmit's commit and the record mover's wait are inline in `mbx_tx_begin` (`CTRL_CC_INLINE` in `ctrl_cc.h`,
  GNU always_inline, plain inline in the portable build), so a transmit calls nothing and saves no registers.

No record, frame or response changes. Three plants were re-anchored to the same defect: `aecp_fan_mutants.py`'s
`notice-source-of-the-first-interface` and `notice-sequence-low-byte-unwritten`, and `poll_items.py`'s `FAN_NOW`,
the walk `notice-fan-out-as-it-was` replaces. Every other anchor of every test module was checked against the
changed files.

| The 8x8/2if notice item, `aecp-fanout`, the same old list | Cycles | Over 27,500 |
|---|---:|---:|
| the final head's code (`082d0037`) | 28,828 | 20 |
| the source and read-once parts alone | 27,852 | 3 |
| **the whole cut** | **25,785** (275 us, the statement exactly) | 0 |

## Attempt 2, cut 2: SRP's delivery tells ACMP only a changed Listener presence (`7b3c1c94`)

The 8x8/1if polls base (the valid-destinations arm's `srp-talker-held`, 29,933 cycles at round 4's tip) traced by
function: 4,861 instructions at CPI 6.2, no function over 2,400 cycles. Its per-source work: MAAP's demand asks
ACMP's `acmp_declaring` for each source every pass, through `memset` and three forwarding `source` callbacks; and
SRP's delivery calls `acmp_listener_registered` for every source every pass. Both entries are in the TSN stack
(changed only through its own review and a pin move). The forwarding callbacks cost 3,114 cycles for 90
instructions (fetch), but ACMP's environment holds one context for every callback, so a hop cannot go without
widening that interface. SRP's delivery can skip the call where ACMP's flag already equals the presence: the call
sets that flag and nothing else (`enter`'s cleared clock cache is cleared by every ACMP entry), so ACMP's state is
the same at every point. That is nine calls a pass at 8x8/1if (252 instructions, 662 cycles in round 4's trace).

## Rejected: the paced record's echo inline

The 1x1/1if paced record (a one-row REMOVE in the answering-ports arm's `aecp-fanout`) is fetch-bound: 3,990
instructions in 29,445 cycles at round 4's tip (CPI 7.4), its `memcpy` echo of one mapping 1,492 cycles for 57
instructions. Echoing one or two mappings by an inline byte loop measured worse on the same list (29,426 cycles
without it, 29,872 with it: 310 and 315 us), the code's placement outweighing the call, so it was not taken.

## Attempt 2's heads, the answering-ports arm (cycles; by the rule against the statement)

| Point | Long record | Paced record | Other record | `aecp` notice item |
|---|---:|---:|---:|---:|
| 1x1/1if, A | 82,292 (865 of 975) | 29,466 (310 of 305; 310 restated) | 21,597 (230 of 245) | 13,492 (of 21,000) |
| 8x8/1if, A | 152,799 (1,605 of 1,715) | 56,486 (595 of 685) | 19,465 (205 of 265) | 13,095 (of 14,500) |
| 8x8/2if, A | 149,525 (1,575 of 1,650) | **56,969 (600 of 595)** | 20,454 (215 of 265) | **25,730 (275 of 275)** |

The re-grade with A's 8x8/2if paced record restated to 600 (and the rest as above) holds: 8x8/1if PASS if its
polls base is 295 or less, and 8x8/2if the eleven findings only.
