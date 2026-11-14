[R842] NEGATIVE - exact head 4958ca4f630da1f715bdcd78113b798bbe332b81

External independent review R842-1, issue #911 / PR #913. Tree `cc92bd5f2ef6d44d1510157a612578458e1e0ab6`; base `b7d692952305e4e0e132abb8f99c339eeb17a873`. All five lenses applied. One MINOR operational-documentation finding remains; one wording-only RESIDUE is non-blocking. No source implementation defect was found in this delta.

## Authority and independence

Reconstructed from AGENTS.md / CONTRIBUTING.md, docs/README.md, issue #911's frozen acceptance and scope decisions (issuecomment-6876968816 and issuecomment-6877123911), REQUIREMENTS.md REQ-VER-02 through REQ-VER-06, #818, #395's commercial-grade/margin decisions, and the QSPI_FLASHBOOT.md, BOARD_DEPLOYMENT.md, BUILDING.md and BOARD_PORTING_AX7101.md authorities. Examined all ten commits and the complete 24-file delta before reading published executable evidence at archive `6d63052bdb9a30e8d4e15e0bcbf404f8e045f512`, and the manager's evidence comment issuecomment-6880720568 on PR #913.

This verdict and ledger were written before inspecting prior public review findings or another reviewer's report. Prior-finding reconciliation follows separately below.

## Findings

### R842-1-F1 - MINOR - Conformance, Docs

**Artifact:** `docs/integration/BUILDING.md:472`, including the following AEM sentence at line 473.

**Title:** The deployment authority still states the AX7101 flash geometry as a universal rule.

**Authority/evidence:** Issue #911 requires the variant's flash layout and integrator instructions to agree. BUILDING.md says every profile keeps its bitstream in a dedicated 4 MiB slot, then places the bare-metal AEM at 4 MiB. The newly added `ax7a200t` bare-metal recipe instead uses 10 MiB and AEM at `0xA00000`: `sw/litex/milan_soc.py:156`, `sw/litex/flash_map.py:55`, and the correctly updated BOARD_DEPLOYMENT.md variant table. `boundaries.log` independently checks both layouts. Even the published compressed payload exceeds 4 MiB by 1,372,528 B.

**Impact:** The general deployment section gives an integrator an incorrect slot budget and AEM location for the new variant, contradicting its manifest and the variant section. The checked commands use the correct manifest; this is not an allegation that they write the wrong addresses. The operational geometry claims make this more than wording-only RESIDUE under the supplied rule.

**Required outcome:** Scope the 4 MiB statements explicitly to AX7101 and describe the variant's layout-derived 10 MiB boundary, or replace the universal paragraph with the per-variant layout authority. Retain the firmware-in-ROM and 64 KiB AEM facts.

**Verification:** Compare the corrected general deployment section with `flash_map.load_map()` for both dies and the generated guide table. It must no longer imply an AEM address inside the XC7A200T bitstream. Re-review Conformance and Docs at the corrected head.

### R842-1-R1 - RESIDUE - Docs

**Artifact:** `docs/integration/BUILDING.md:312` and `:363`.

**Title:** Two references use the old checker-table name.

**Authority/evidence:** The document names `BUILD_PARTS` in `scripts/check_sweep_shape.py`; the existing declaration is `BUILD_DIES` at line 73, consumed at line 468.

**Impact:** Readers cannot find the named symbol. No recipe, value, measurement or check result changes.

**Exact fix / required outcome:** Replace both `BUILD_PARTS` references with `BUILD_DIES`.

**Verification:** Both references resolve to the existing declaration. This wording-only residue does not unclean a lens; the manager carries it to the residue checklist.

## Results by lens

**Conformance:** Acceptance 1 and 2 are supported by the published image/signoff receipts; acceptance 3 by the qualified input identity evidence. Acceptance 4's executable paths passed focused checks, but F1 leaves its documentation inconsistent. `cfg_ax7a200t` derives `cfg_ax7101`, keeps the 1x1 TDM8 YAML and adds the selected die. The 5,566,832-B compressed payload exceeds 4 MiB. The release `.bit` is 9,730,856 B including its 204-B header; the programmed payload is 9,730,652 B, leaving 755,108 B in 10 MiB. The instantiated flash module supplies N25Q128A13 / 16 MiB / JEDEC `0x20ba18`.

[R842] PASS RTL - `sw/litex/platforms/alinx_ax7101.py:297`, `ax7101_timing.py:24`, `milan_soc.py:3857`, `milan_soc.py:4615`, `sw/firmware/milan_baremetal/milan_baremetal.c:1936`, and published `receipts/buildC-release/*` - One platform owns the shared pins and constraints; the part reaches the PLL grade and timing hook. Firmware reads the generated AEM constant; the manifest, reconstruction and diagrams derive its offset. No HDL or gitlink changes occur in this delta.

The image at `1e604e1b4f0aa8015544eb0d363a965fbb4cd985` selects the first ExtraPostPlacementOpt route, with AreaOptimized_high synthesis, ExploreArea optimization and AggressiveExplore timing optimization. The recorded 8-thread implementation differs from the launcher's 32, as disclosed. Slow 0/85 C: WNS +0.174 ns, WHS +0.102 ns. Fast 0/85 C: WNS +1.633 ns, WHS +0.036 ns. TNS/THS are zero, satisfying #818's +0.030/0 ns floors. Endpoint temperatures are power metadata over fixed Slow/Fast models, not independently temperature-prorated timing models. Resources: 53,590 LUT, 54,971 FF, 87.5 BRAM, 15 DSP. Clock interaction retains the four Ethernet max-delay-only crossings; check_timing reports zero unconstrained internal endpoints, no-clock and loop cases.

The two published 140-row AX7101 input lists are byte-identical. Independently matched 135 available files against their hashes at this head; five generated inputs are absent here. Published normalized Verilog/header comparisons and `final-head-inputs.txt` cover the other outputs: AX7101 XDC/Tcl/ROM/RAM/AEM unchanged, layout metadata adds only flash_device/flash_jedec_id. This does not claim an independent bitstream rebuild. The image-to-head build-relevant Python change is only a type annotation/import; the published final-head receipt reports equal 200T outputs after clone-path/thread-setting normalization. Independently compared all 113 raw used-pin rows across the three published 200T builds against the AX7101 release comparison: signal, pin name, bank, standard and use agree. Blank VCCO cells are not voltage measurements.

[R842] PASS Robustness - `sw/litex/deploy.sh:223`, `:235`, `:473`, `:490`, `:533`; `sw/litex/qspi_owner_transition.py:316`; `flash-transaction.log`, `boundaries.log`, `mutation-M1.log` through `mutation-M4.log` - All persistent paths identify the die before bridge load, then flash ID before dump/write. Wrong/missing die, wrong/missing ID and absent flash metadata refuse without writes. Added independent probes reject conflicting identification and six malformed metadata IDs. Exact-slot payloads pass; slot-plus-one fails. The focused transaction gate covers completed-write failures, staging, retries and verified AEM-before-bitstream order. This does not prove safety during a torn erase/program; the documented A/B or MultiBoot limitation remains.

[R842] PASS Tests - `sw/builder/test_builder.py:18613`, `:19064`; `sw/builder/test_timing_grade.py:166`; `scripts/board_variants.py:152`; `scripts/check_sweep_shape.py:121`; local receipts and published `receipts/gates/*` - The focused transaction, platform/timing tests, table check/six controls, shape check/self-test, variant dry-run, boundaries and diagram regeneration pass. Four independent disposable mutations failed for the expected assertions: premature bridge load, removed JEDEC comparison, skipped direct-flash proof, and removed metadata requirement. No production source was edited. Extracted and executed the guide's three JTAG shell blocks with a synthetic image set and stub programmer: layout-derived part, volatile load, AEM at `0xA00000`, then verified bitstream write.

Independently verified all 96 archived files against the published SHA-256 manifest. The workflow table contains 150 rc=0 rows and 522 NOT RUN rows, each with a reason; the separate NOT RUN index groups 254 entries. The four sweep summaries total 65/65 suites, zero failures/timeouts. The first elaborate-gates-2 simulation timed out at 900 s; its log is retained, and the author reports the fresh-clone rerun passing at 532 s. The executable-step table records that rerun at rc 0. These are author source-head receipts, not a manager source bank. The archive contains summaries rather than every referenced raw job log; no full bank was rerun here.

**Docs:** Examined all three integration guides, variant table, both rendered maps and editable masters, generator, inventory changes, author handoff and manager evidence. Both SVG/master pairs regenerate byte-identically. INSTALLED_BUILD is defined, both part/offset values are present, the raw JTAG sequence and configuration-memory fallback are specified, and the absence of XC7A200T silicon testing is explicit. The published fallback receipt records a 10,493,272-B combined file, payload at zero and AEM at `0xA00000`. F1 leaves this lens unclean; R1 is residue only. No added source comment introduces a reviewer identity, review round, bench lane label or issue-comment ID.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #911 acceptance/decisions; #818/#395; build.sh; flash_map.py; BUILDING.md:472; image/gate receipts | R842-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| RTL | CLEAN | Platform/timing hooks; milan_soc.py; firmware AEM consumer; buildC timing/clock/CDC/pin reports; input hashes | R842-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| Robustness | CLEAN | deploy.sh; qspi_owner_transition.py; flash-transaction.log; boundaries.log; mutation-M1 through M4 logs | R842-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| Tests | CLEAN | Focused transaction; test_timing_grade.py; board_variants.py controls; shape controls; receipt-audit.log | R842-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| Docs | UNCLEAN (F1) | BOARD_DEPLOYMENT.md; QSPI_FLASHBOOT.md; BUILDING.md; both flash maps; author/manager evidence | R842-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |

## Limits and pending manager duties

- No hardware, physical calibration, cold boot, soak or power-cycle campaign ran. NOT RUN and field skips are not hardware proof. Package speed grade, physical flash/cable and #395 temperature/oscillator work remain physical checks. This is pre-release source review, not REQ-VER-05/06 qualification.
- Existing diagnostics remain: 46 inputs without input delays but with false paths, 87 outputs without output delays, and CDC categories including ten CDC-10 critical rows. The published comparison reports the existing AX7101 categories. Positive internal slack does not clear these diagnostics or prove full board-interface timing.
- The binary image set, checkpoint and individual raw timing reports are not in the archive and were not independently rebuilt/rehashed. Recorded bit hash: `b7d7dc4ec9ce9254a089fc99d6699d13eba1b8271ed889d000bded46be64954f`; AEM: `bdfde7cf448ed032ffb1663b0898aeef9ded3bb11b4ead5dc36dfa3df873f180`; layout: `73c2d40e3f3d6ae122b93b71b896abdf75a2f75e9014411b84dced32289a1837`.
- The author's update from compressed build A correctly refused because that installed artifact exceeds its own slot. The successful named-update evidence is synthetic; no physical update of build A is claimed.
- The pre-existing standalone qspi_owner_transition.py self-test NameError is #912, out of scope. The focused transaction function runs and passes.
- The manager owns hosted/local-replica acceptance and must distinguish executed jobs from skipped contexts. Neither was independently accepted here. There is no manager source-head bank at this commit. The current-dev candidate still needs the manager's builder/native banks and linked receipts, two independent positive reviews, no review in flight, explicit merge authorization and post-merge containment.
- After probes, all 1,731 superproject tracked blobs, modes and index entries match this head; the four required submodules match their gitlinks and actual bytes/modes/index. The optional external submodule remains uninitialized. No source fix, commit, push, GitHub write, hardware operation or merge occurred.

## Reproduction and receipt interpretation

Portable scripts take the review checkout and packet directory; `run_focus.py` also takes the pinned LiteX Python path. `mutation_probe.py` accepts optional M1/M2/M3/M4 selectors. Disposable trees/images live only in `scratch/`, which is excluded from publication. The initial shape-control call used `--selftest` and exited 2; the corrected `--self-test` run exits 0 and is retained separately. Reviewer fixture setup errors were corrected before mutation/boundary verdicts; only completed probes support the results above.

Prior-public-finding reconciliation: after writing this independent verdict and ledger, checked the public PR conversation, submitted reviews and inline review threads. The conversation contains only manager evidence/start/reset notices; submitted reviews and inline threads are empty. The earlier abandoned start was explicitly stopped before a finding. There are no prior public findings to resolve or retain at this head. No other reviewer's report was read.

R842-1 FINISHED
