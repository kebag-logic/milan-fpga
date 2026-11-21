[R880] NEGATIVE - exact head 62477be4cb90336ca9b59ae7ab8377546e72557a

External independent review, round R880-1, issue #665 / PR #960.
Tree: `568d04b01d0b137adaed668afb6a8d525a3c8a12`.
Range: `59b09884..62477be4cb90336ca9b59ae7ab8377546e72557a`, 16 commits, 65 changed paths.

All five lenses were applied. The version-selection RTL and focused placement tests pass. Approval is withheld for the resource-sweep regression and evidence/documentation findings below. This verdict does not assert that the shipping payload changed beyond its intended identity fields; the published packet does not permit independent closure of that complete claim.

**Scope and authority**

Reconstruction followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and public scope decisions, linked requirements/interfaces, the diff/history, then public executable evidence. No private author material or other review report was used. The public source evidence is [89a2e4b9, review-evidence/s13-r1](https://github.com/kebag-logic/milan-fpga/tree/89a2e4b95f4dbe916f150c68c4403792f05bffa3/review-evidence/s13-r1).

The operative scope is the default flip: the two AX7101 shapes select split, split reads major 3, and all-fabric stays selectable and gated. Processor deletion and full release qualification remain later work. Authorities examined: ARCHITECTURE_HW_SW_SPLIT.md section 7; REQUIREMENTS.md section 1; FR_NFR.md NFR-SCOUT-02/03; MAILBOX_SPLIT.md's placement/identity contracts; and these issue comments:

- [6410301079](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6410301079): default change and preserved all-fabric choice.
- [6799253003, item 6](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6799253003): flip acceptance.
- [6845315282](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6845315282): 8x8/1if required, two interfaces optional.
- [6930885185](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6930885185): setup >= +0.030 ns, hold >= 0 ns, best of three directives, every corner.
- [7044585511](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7044585511): 1x1 bounds.
- [7063917242](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7063917242): bench re-check, and [7070924358](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7070924358): author REVIEW READY.

REQUIREMENTS section 1 distinguishes the flip from deletion after full qualification. The normative NFR-SCOUT-02 row is unchanged. This review uses the explicitly assigned public flip scope; it does not claim completion of #665 or its end-state qualification. Arty configuration bytes are unchanged.

**Findings**

**R880-1-F1 | MAJOR | Robustness, Tests**

Artifact: `configs/endstation_ax7101_1x1_tdm8.yaml:75`; consumer `syn/resmap/soc_sweep.py:89` and `:118`; `syn/resmap/sweep_plan.json`, `soc.variants.ship`.

Authority/evidence: the resource sweep's `ship` variant is expected to be accepted. The changed default adds `--ctrl-mailbox --ctrl-firmware sw/builder/out/endstation_ax7101_1x1_tdm8/ctrl_app.elf`. `prepare()` emits builder artifacts, but neither it nor `command_export()` creates that ELF. Passing the actual generated ship argv through the existing SoC instance probe raises FileNotFoundError for that ELF before reaching the datapath. Selecting all-fabric on the same configuration reaches the datapath with no firmware file. See `sweep_probe.py` and `sweep-probe.log` (rc 0 means the failure and baseline control were reproduced).

Impact: a fresh resource sweep loses its accepted shipping export, so pricing cannot proceed from it. An existing untracked ELF could conceal the dependency. Author open item 4 is a reproduced regression, not merely an argv spelling concern.

Required outcome: explicitly select the resource sweep's intended placement and prepare its required image, preserving declared accepted/refused cases. A clean export must not depend on a previous unrelated firmware build. If intentionally all-fabric, select and document that placement; if split, prepare the matching firmware.

Verification: clean `ship` and `axilite` exports without a pre-existing ELF, retained expected refusal cases, and a focused missing-image control. No full resource-pricing bank was run here.

**R880-1-F2 | MAJOR | Conformance, Tests, Docs**

Artifact: public `author-r1/receipts/budget/descriptor-groups-remeasured.txt:1`, `budget/harness-images-vs-measured.txt`, `identity/1x1/checkpoint-dump-diff.txt`, `identity/8x8/bram-dump-diff.txt`; `author-r1/HANDOFF-r1.md`'s identity/CPU carry claims.

Authority/evidence: the frozen validation plan carries bench evidence by image identity, and the review assignment requires an independent diff of the built images/ROM words, 16 harness images and 13 descriptor groups. All 108 public manifest entries hash correctly. The packet contains no `.bit`, `.elf`, `.init`, `.dcp`, `.cells`, `.nets` or `.bram` comparison operands. The checkpoint receipts explicitly leave dumps in scratch. Neither the 13 groups' original JSON results nor their stated `hcompare2.py`/`hsubset.sh` drivers is present. Supplied `hcompare.py` describes a different, part-based comparison. See `evidence_audit.py` and `evidence-audit.log`.

Impact: reported arithmetic and generated descriptor bytes can be checked, but complete exclusion of other binary differences and 13-group leaf equality cannot be independently reproduced from the authorized public material. The requested identity-based acceptance remains unclosed. Hashes of absent operands do not supply that comparison.

Required outcome: provide hash-bound access to the compared binaries or complete equivalent load/ROM/configuration dumps, and the actual 13-group operands and driver. Include measured-to-current source/image binding and portable replay commands. Durable downloadable artifacts are sufficient; large blobs need not enter the repository.

Verification: independently diff both shipping payloads and complete ROM/load maps; verify all 16 layouts and six-byte deltas; compare every leaf of the 13 groups with explicit ignored-metadata rules. A complete 64-part CPU rerun is not intrinsically required if this identity carry closes. This finding requests the proof used to avoid that rerun, not new performance bounds.

**R880-1-F3 | MINOR | Tests, Docs**

Artifact: REVIEW READY comment 7070924358's image-identity bullets; public `author-r1/receipts/identity/1x1/bitstream-bitdiff.txt` and `identity/8x8/bitstream-bitdiff.txt`.

Authority/evidence: the summary attributes all 77 differing 1x1 header bytes and all 74 differing 8x8 header bytes to SW_CRC/SW_HDR_SHA256 text. Independently comparing the two complete rendered design-name strings gives 71 and 69 differing bytes. The receipts list six further 1x1 offsets (185, 191, 193, 194, 196, 197) and five further 8x8 offsets (185, 193, 194, 196, 197), outside those strings. `evidence-audit.log` reproduces these counts.

Impact: the complete file-delta classification is false as written. These look like ordinary header metadata differences, but the absent operands prevent parsing their fields here. This is not evidence of an additional fabric behavior change. It changes a quantitative identity claim, so it is not wording-only RESIDUE.

Required outcome: decode and name the extra fields, distinguish nonloaded metadata from configuration payload, and correct the summary to 71+6 and 69+5 header differences with their actual categories. Preserve the separate configuration CRC and frame counts.

Verification: parse complete headers of the hash-bound pairs and account for every changed byte. The reported frame totals independently sum to 22 and 15 bits.

**R880-1-F4 | MINOR | Tests, Docs**

Artifact: `docs/design/MAILBOX_SPLIT.md:1810`.

Authority/evidence: this identity paragraph says the split recipe's shape artifacts are the all-fabric build's byte for byte, citing gate 23o. The changed gate at `sw/builder/test_builder.py:24363` exempts the firmware-version field in two artifacts. The independent packed descriptor comparison finds the intended changed byte at 0x184 for both shapes. The nine-artifact gate passes with its two-artifact exception.

Impact: the authoritative identity paragraph promises equality that its cited test does not establish. This is a test/equality claim, not a harmless placement label.

Required outcome: state the firmware-version exception for the AEM overlay and ROM, retaining equality for other shape artifacts and the no-tracked-write rule.

Verification: compare the corrected paragraph with gate 23o and `descriptor.log`; do not claim equality for the changed fields.

**R880-1-R1 | RESIDUE | Docs**

Artifacts: `docs/overview/ARCHITECTURE.md:4` and `:19`; `docs/overview/FULL_FPGA_SOLUTION.md:3` and `:19`; `docs/design/MAILBOX_SPLIT.md:5` and `:626`.

Evidence/impact: these pages still call all-fabric the current shipping build while edited introductions say split ships. These are stale placement labels, changing no measurement, executable behavior, clause claim or privacy rule.

Exact fix: ARCHITECTURE line 4: “The shipping AX7101 build runs control protocols in firmware.” Line 19: “The implementation sections below describe the all-fabric build.” FULL_FPGA_SOLUTION line 3: “The all-fabric build remains available behind its placement switch.” Line 19: “The implementation inventory below describes the all-fabric build.” MAILBOX_SPLIT line 5: “The all-fabric build remains available behind its placement switch.” Line 626: “The all-fabric placement remains available.”

Verification: search those pages for present-tense all-fabric shipping labels. Carry to the residue checklist; this item does not make a lens unclean. No new prohibited review/lane label was found in added source comments examined in the delta.

**Independent results**

| Check | Artifacts / receipts | Result |
|---|---|---|
| Version chain | `milan_csr.sv:201`, `:2002`; `milan_datapath.sv:2850`; `aem_descriptors.py:59`; builder loader and `with_placement` | One all-fabric VERSION, one split-major declaration, common minor. Placement selects the defaults-ROM word; firmware string derives from the same declarations. No new clock/reset/CDC/FSM behavior in the RTL delta. |
| Integrated split and new mutation | `rtl_probe.py`, `rtl-clean.log`, `rtl-mutant.log`, build logs | Clean: 148 checks, zero failures. Forced major 2: exactly the full VERSION and major-only assertions fail. Pinned simulator identity recorded in `rtl-probe.log`. |
| Builder | `builder_checks.py`, `builder.log` | Eleven selected gates pass, no skips. 23m: seven elaborations, 4/4 binding plants. 23n: defaults and rejection cases. 23o: five configs/both recipes, two recipe and three artifact plants. 1e: 6/6 plants. 23g: 6/6 launchers, 2/2 plants. 24 and 25c pass. Identity gate: both placements and 13/13 bad-image plants. |
| Descriptor/CRC delta | `descriptor_check.py`, `descriptor.log` | Packed AEM sizes 7,512/19,520 bytes, exactly one changed byte at 0x184. CRCs 38a80323 -> db1deab5 and d6dd74b9 -> b730ec91. Published LUI/ADDI words decode to these independently computed CRCs: five bytes, 20/13 bits, plus the string's one byte/one bit. This checks reported words, not absent complete ELF operands. |
| Flip checks | `flip-1x1.log`, `flip-8x8.log`, `flip-plants.log` | Both required points pass; 616/616 controls refused. Optional 8x8/2if aggregate failure is not a finding. No budget changed. |
| Clock constraints | `clock-constraints.log` | Six exports pass: both split shapes on e1/e2 and all-fabric 1x1 on e1/e2. Constraint generation, not a new route or physical measurement. |
| Entity/UART/feature/sweep | `entity.log`, `uart.log`, `feature.log`, `sweep-plants.log`, `entity-plants.log` | All pass. Entity self-test: 239 checks, zero failures, including the split-major plant. UART includes split and unknown-major controls. |
| Register map | `regmap-equipped.log` | Fresh: 203 registers, 34 modules, 240 files. Explicit all-fabric provenance makes retaining this export acceptable for the flip; it is not a newly recorded split memory-map proof. |
| Preserved all-fabric paths | Changed `_config_argv`, census `shapes()`, control-memory `soc_argv()`; author `gates/quick-62477be4.txt`, `release/release-identity.txt`; independent builder/clock checks | Processor census and control-memory baseline explicitly select all-fabric. Author census reports no unproved rule among 57; release receipt reports identical loaded BIOS/AEM/ROM/SRAM and argv. Those full executions were inspected, not rerun here. |

The first builder attempt redirected output without satisfying the probe's fixed lookup path; three elaboration checks failed for missing platform_shape.json. After linking the standard output path to designated scratch output, the same selected checks passed. `builder-initial.log` preserves the setup failure. The first register check lacked its rendering package; the equipped interpreter passed. Neither is a source finding.

The six author route receipts meet the best-of-three rule. ExtraPostPlacementOpt worst-corner setup/hold: +0.131/+0.036 ns at 1x1 and +0.176/+0.036 ns at 8x8. AltSpreadLogic_high passes both; ExtraTimingOpt passes 8x8 and misses 1x1 setup (+0.002 ns). That single-directive miss does not fail best-of-three. Four corners per directive were inspected. These are author routes at 822e3af0 with published carry receipts to the reviewed head, not new routes executed here.

The 16-image and 13-group receipt inventories are internally consistent. Independent descriptor/CRC computation supports the proposed carry but cannot compare absent complete operands: F2 remains open. Author open item 2 does not inherently require a full CPU rerun if that proof closes. Item 3's explicitly labeled all-fabric register export is acceptable. Duplicate harness split flags use last-option selection and are not separately called a defect. The resource sweep differs because it has no prepared ELF and its accepted baseline breaks (F1).

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | #665 decisions; REQUIREMENTS section 1; NFR-SCOUT-02/03; split architecture section 7; AX7101 defaults; descriptor/flip/timing/bench-identity evidence | R880-1 | 62477be4cb90336ca9b59ae7ab8377546e72557a |
| RTL | CLEAN | `milan_csr.sv:201`, `:2002`; `milan_datapath.sv:2850`; `sim_split.cpp:827`; clean/mutated split runs; placement elaborations; constraint exports | R880-1 | 62477be4cb90336ca9b59ae7ab8377546e72557a |
| Robustness | UNCLEAN (F1) | Placement/key/recipe controls; both placement elaborations; identity plants; UART controls; split reset/publication/backpressure checks; resource-sweep probe | R880-1 | 62477be4cb90336ca9b59ae7ab8377546e72557a |
| Tests | UNCLEAN (F1-F4) | Changed builder gates/controls; split VERSION mutation; entity/sweep/UART/feature controls; public identity/CPU scripts and receipts; gate 23o documentation | R880-1 | 62477be4cb90336ca9b59ae7ab8377546e72557a |
| Docs | UNCLEAN (F2-F4; R1 nonblocking) | README/CHANGELOG; REQUIREMENTS; split architecture; mailbox identity; generated register map/fingerprint; feature ledger; inventory removals; public evidence | R880-1 | 62477be4cb90336ca9b59ae7ab8377546e72557a |

[R880] PASS RTL - `hdl/common/csr/milan_csr.sv:2002`, `hdl/milan/milan_datapath.sv:2850`, `rtl-clean.log`, `rtl-mutant.log` - placement-bound VERSION matches section 7; the integrated read passes and removing its placement binding fails the intended assertions. No open RTL finding from this round.

**Prior findings, limits and manager duties**

This verdict and ledger were written before checking other public review findings. The final read-only check returned only the two review-start notices: no prior public findings, inline findings or review verdicts were present to resolve or retain. `prior-findings.json` records that result. No other reviewer's report was read.

No manager source bank exists at this head and none is claimed. Full source-bank execution evidence is the author's; this review added focused checks. The four reported CI-environment docs rows are not findings under the assigned scope. Physical calibration NOT RUN and field/bench skips are not hardware proof. The bench re-check's failures/skips remain failures/skips; identity cannot turn them into qualification passes. Assigned post-flip handling of #954 is not expanded into a source fix here.

No hardware, full parent/processor/gPTP/Yosys/builder bank, hosted acceptance, local workflow replica, commit, push, GitHub write or merge was performed. No shared installation or other checkout was edited. Disposable clone/build/probe trees are under `scratch/`. Parent blob bytes, modes, index and required submodule pins are verified by `verify_tree.py` and `tree-integrity.log`; optional lwSRP is checked too.

The manager still owes corrected-head re-review, the independent review bar, the current-dev merge candidate (live dev identified in the assignment as e275d7950ef3385753e6a15d2e191ba855b171ed), candidate builder/native receipts, and required hosted/local acceptance. This source review does not certify that unbuilt candidate. Merge authorization and post-merge containment remain separate duties.

Only REPORT.md and MANIFEST.sha256-listed files are publishable. Scratch is excluded. Any receipt path normalization is recorded separately.

R880-1 FINISHED
