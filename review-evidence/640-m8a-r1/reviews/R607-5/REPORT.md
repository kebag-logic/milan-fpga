[R607] POSITIVE - exact head 42678ae2f77fbbef056f7fb99859e0193181e6d7

External independent review, R607-5, issue #640 / PR #721. Tree `1508b29c3603a36349665938939fa00c871cbd7e`. All five lenses are CLEAN for this delta. No new BLOCKER, MAJOR, MINOR or RESIDUE. R606-4-F1 and R607-4-F1 are resolved. Retained optional suggestions are listed below.

The independent verdict and ledger were written before reading prior public review findings (`receipts/independent-verdict.md`). No private author material, handoff, lane scratchpad, concurrent reviewer report, or management checkout was read. No source edits, commits, pushes, GitHub writes, author contact, delegation, container execution or hardware access occurred.

**Scope and authorities**

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public decisions, linked requirements/interfaces, the requested `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc..42678ae2f77fbbef056f7fb99859e0193181e6d7` diff and history, then public executable evidence. `receipts/full.diff`, `round5.diff` and `history.txt` retain the examined change. The round-5 delta from `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` changes three documentation files only; executable sources, tests and gitlinks are unchanged.

The [M8a assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426), [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877) and [round-5 decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6118560882) govern this review. REQUIREMENTS.md section 1, NFR-SCOUT-01..03 and NFR-RES-01 in `docs/reference/FR_NFR.md`, the split architecture, and the L11/memory-ledger sections of `MARK_II_AREA_PLAN.md` supply the authorities. The binding firmware budget is 224 KiB / 229,376 usable bytes and 56 planned tiles. The 121.5-tile image ceiling preserves a separate 13.5-tile reserve.

This is the M8a-1 fit/documentation correction. Boot, service checks and integrated routing remain M8a-2. The issue-wide 38,040-LUT acceptance and eventual baseline re-record are not claimed complete by this PR.

**Four-point reproduction and mapping evidence**

The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/cbc051a5a2f68a738b90fea17b9f1d882a0e22a2/review-evidence/640-m8a-r1/author-r5/evidence-r5) and [review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6119125404) record the rerun on firmware `8ab2b539`, carrying dev `c6bd08c6`. Selected public artifacts were verified against their Git blob IDs; source URLs and hashes are in `receipts/public-sources.json`.

| Point | Fresh ROM / SRAM need, bytes | Planned tiles | Published mapped RAMB36 / RAMB18 | Mapped tiles | LUT cells / FF |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface | 96,624 / 45,776 | 35.5 | 34 / 2 | 35.0 | 128 / 8 |
| 1x1, two interfaces | 98,056 / 57,152 | 38.0 | 37 / 1 | 37.5 | 89 / 7 |
| 8x8, one interface | 110,344 / 86,336 | 48.5 | 46 / 2 | 47.0 | 417 / 42 |
| 8x8, two interfaces | 111,848 / 112,464 | 55.0 | 53 / 2 | 54.0 | 266 / 34 |

All four freshly linked ELFs have exactly the author's published SHA-256 values. The same runtime links at `ce10328c3d89d81509e47836fa4a48b22ecdbc20` reproduce all four earlier spans and plans. Both requested public probes, `run_fit.py` and `compare_fit.py`, were run unmodified and pass. The comparison's old phrase "not the documented 6144" refers to the round-4 document, not this corrected head.

The runtime was rebuilt from 57 source/header files verified against published hashes, with the pinned SDK installed and verified in scratch. `runtime_probe.py` adds only `-fno-stack-protector` to runtime compilation, as authorized for #723. The source recipe was not edited. Fresh archive hashes are `b9fac818fcf38303b12b7991e08c7360afdebe221172ad62e3f13c4afd1137d0` (libc) and `7827f6ad33349dc2bc577fb8c1e5d483d5e85172df4d9c72463013e5478f1ea8` (compiler runtime); both source revisions used those exact archives. Input and command provenance is retained in `receipts/runtime-inputs.json`, `runtime-provenance.json`, and `runtime.json`.

The author mapping receipt records the isolated eight-top run on 2026-10-12, 07:55:41 to 07:57:46 +02:00, rc 0, using `xc7a100t-fgg484-2` and `AreaOptimized_high`, version 2026.1. All eight utilization reports agree with the primitive TSV, including the distinction between LUT cells and Slice LUTs (`receipts/mapping-crosscheck.log`). The largest ROM region has 169 LUT cells and 161 Slice LUTs; the count includes its bank decode and read multiplexer. The new 512-word ROM bank is the logic-mapped bank at the largest point. Independent emission from the fresh ELFs produces eight tops and 13 initialization files, with exactly the published bank-plan JSON and synthesis recipe (`receipts/ooc-emit.log`, `ooc-generated-digests.json`). Synthesis itself was not rerun here.

The largest split need totals 224,312 bytes; its banks allocate 225,280, within 229,376. Its planner has 4,096 bytes of additional bank allocation, plus 968 bytes already unused inside the two regions: 5,064 total unused bytes. That is aggregate capacity, not a promise that an arbitrary distribution of growth can consume every byte without rounding. The author also records flat spans 142,256 / 155,056 / 196,144 / 223,776 bytes, all within the firmware limit. The earlier `ce10328c` figures now carry their source explicitly in `SPLIT_CONTROL_MEMORY.md:182`; the one-off original controls likewise name `c20ed894` at line 111.

`SPLIT_CONTROL_MEMORY.md:139`, `MARK_II_AREA_PLAN.md:768` and `AREA_BUDGET.md:230` match the measurements and the following independently recomputed arithmetic:

- Mapped firmware: `87.5 - 6.5 + 6 - 18 + 54 + 2 = 125`; conditional release gives 114, leaving 7.5 below 121.5.
- Every bank in block RAM: 126 before release, 115 after, leaving 6.5.
- The ruled 56-tile firmware maximum gives 116 after release, leaving 5.5.
- Keeping BIOS adds 18: 143 before release and 132 after. Partial placement adds retained AECP's six tiles: 131, or 9.5 over the ceiling.
- The separate 13.5-tile reserve is untouched. Conditional release and replacement debits still require integrated confirmation.

**Checks run in this review**

| Check | Result and receipt |
|---|---|
| Fresh links at exact head and `ce10328c` | Eight links, all rc 0; each four-point driver ran concurrent independent links and joined every child. `receipts/run-fit.log`, `previous-run-fit.log`, individual `fit-*` receipts and root JSON/rc files |
| Requested fit comparison | PASS with identical runtime archives; prior and current spans reproduced. `receipts/compare-fit.log` |
| Independent fit/document audit | PASS: fresh ELF hashes, section/storage/plan values, all four documented rows, mapped primitive sums and both ledger tables. Each real image extended to exactly 56.0 tiles is accepted; 56.5 is refused by `budget`; shape staging sizes match. `receipts/audit-fit.log`, `independent-fit.json` |
| Focused memory checks | PASS: bank decomposition, all 17 registered rules, linked reset/data image versus binary extraction, documented rule registry, baseline simulation and all eight new ROM/SRAM needs. Full decoded-window holes, byte lanes, ROM write protection, alias protection and immediate post-error access pass. All 38 non-SoC mutants caught after green baselines. `receipts/focused-memory.log` |
| OOC emission and published synthesis cross-check | PASS: eight tops, 13 initialization files, matching plan/recipe, all eight utilization reports consistent. `receipts/ooc-emit.log`, `mapping-crosscheck.log` |
| Focused documentation and classification | `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_em_dash.py --base c6bd08c6`, `ci_scope.py --selftest`, `pp_resource_gate.py check-baseline`, and `git diff --check c6bd08c6..42678ae2`: rc 0. Individual receipt files record argv, UTC start, elapsed time and exit status |
| Checkout integrity | PASS before and after: raw blob bytes, file kinds, executable modes, exact index records, head/tree and required populated submodule pins. `receipts/audit-before.log`, `audit-final.log` |

The focused interpreter is a fresh Python 3.12.3 environment with the repository's package pins and PyYAML. The full SoC arm, its six mutations and the seven-member aggregate were not rerun here. Their author receipts report 44/44 and 7/7 at `8ab2b539`; that source is unchanged by round 5, including the tested rule table. The author documentation-job receipt names `42678ae2` and records 83 commands returning zero, with its declared field/environment skips. Neither receipt is a manager source bank. No manager source bank ran at this exact head, and none is inferred.

**Prior public findings: explicit dispositions at this head**

Public comments read after the independent verdict: [R606-1](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6104999232), [R607-1](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6105008317), [R606-2](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107064124), [R607-2](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107065061), [R606-3](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6112081957), [R607-3](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6112082969), [R606-4](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6118557490), [R607-4](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6118122865). No review objects or inline review comments were present when checked.

| ID; prior severity; all attributable lenses | Disposition and evidence |
|---|---|
| R606-4-F1 = R607-4-F1; MINOR; Conformance, Tests, Docs | RESOLVED. Four exact-image reproductions, author remapping, independent plan/recipe emission, revised section 5 and both ledgers, recorded runtime and passing requested probes. The Tests attribution from R607-4 is retained and cleared, not dropped. |
| R606-1-F1; MINOR; Robustness, Tests | RESOLVED, preserved. `ctrl_memory.py:288` refuses writable ROM. Genuine-link refusal and its removal mutant pass in the focused run. |
| R606-1-F2, R607-1-F1; MINOR; Tests | RESOLVED, preserved. Boundary equality/half-tile, reset bytes, NOBITS, LMA overlap, decode/hole width and post-error arms and mutants pass (`test_ctrl_memory.py:349,473,803`). |
| R606-1-F3; MINOR; Tests; R607-1-S1; SUGGESTION; Tests, Robustness | RESOLVED, preserved. Real main-path controls, flag pairing, no-BIOS export and stage-call mutation remain in `test_ctrl_memory.py:729`; author source receipt exercises them. Their code and inputs are unchanged by round 5. |
| R606-1-F4, R607-1-F2; MINOR; Docs | RESOLVED, preserved. Both ledgers give 116 / 5.5 at 56 firmware tiles; lane and future-route text use 56 and distinguish OOC from integrated allocation. |
| R606-1-F5; MINOR; Docs; R607-1-R2; RESIDUE; Docs | RESOLVED. Current 169 denotes the whole ROM region including decode/multiplexer, with 161 Slice LUTs explicitly distinguished. Published report and TSV agree. |
| R607-1-F3; MINOR; Docs; R606-1-R2; RESIDUE; Docs | RESOLVED. Public PR body names round 5 and exact head, records the dev merge and seven-member aggregate, and retains historical gate attribution. |
| R607-1-R1; RESIDUE; Docs | RESOLVED through the refreshed fit. Two mapped tiles are distinguished from one planned tile / 4 KiB and 5,064 aggregate unused bytes. |
| R607-1-S2, R606-1-S3; SUGGESTION; Robustness, Tests | RESOLVED for the reported truncations. Named header/segment/name refusals and their mutants pass. Complete malformed-ELF validation is not claimed. |
| R606-2-F1; BLOCKER; Conformance, Tests, Docs | RESOLVED, preserved. `scripts/ci_scope.py:69` registers the memory page, its classification case remains, and the independent self-test passes. |
| R606-2-F2; MAJOR; Tests, Docs | RESOLVED, preserved. `test_ctrl_memory.py:629,639,928` refuses firmware-data imports, omits only firmware make inputs and requires green baselines before mutation grading. The author source receipt exercises all six SoC mutations; no source change in round 5. |
| R607-2-F1; MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED, preserved. `ctrl_memory.py:246,272,283` validates programmed load coverage. Empty/short reset and missing-data linked controls and all four load-related mutants pass here; pre-export hookup is unchanged and covered by the author source receipt. |
| R606-2-F3; MINOR; Docs | RESOLVED with current figures. Partial placement is `125 + 6 = 131`, 9.5 over; give-way basis is the ruled 56 tiles. |
| R606-1-R1; RESIDUE; Docs | RESOLVED. Both headroom sentences explicitly include M2's unused +2 allowance. |
| R606-3-R1 = R607-3-R1, retained as R606-4-R1; RESIDUE; Docs | RESOLVED. PR Status carries the requested round-4 merge sentence and says the manager validates the current-dev candidate at the merge turn. The stale present-tense dev-tip sentence is gone. |

**Retained optional suggestions**

These are existing public suggestions, not newly discovered mandatory work. Their authority is the linked original review plus the named current artifact. Each remains optional and leaves coverage clean.

| ID; severity; all lenses | Artifact and evidence | Impact | Optional outcome and verification |
|---|---|---|---|
| R606-2-S1; SUGGESTION; Robustness | `ctrl_memory.py:264`, `ctrl_split_start.S:12`: no comparison against startup copy/clear ranges | An orphan SRAM section could remain uninitialized | Check linker-symbol ranges; verify with orphan-section links |
| R606-2-S2; SUGGESTION; Robustness | `ctrl_memory.py:222,237,238`: malformed indices or zero symbol stride can fail unnamed | Poor diagnostic while still failing closed | Add named refusals; verify malformed table controls |
| R606-2-S3 = R606-1-S1; SUGGESTION; RTL, Robustness | `ctrl_split_start.S:10`: no trap-vector installation | Pre-installation trap behavior depends on reset defaults | Define/install and verify in the boot vehicle |
| R606-2-S4 = R606-1-S2; SUGGESTION; RTL, Robustness | `milan_soc.py:2750`, `ctrl_memory.py:312`: no independent upper bound on surplus initialization words | Surplus segment bytes can be truncated by bank slicing | Add a bound and oversized-load control |
| R606-2-S5 = R607-1-S3; SUGGESTION, pre-existing; Tests, Docs | `ctrl_image_runtime.py:35`, separate #723; recipe remains unchanged | SDK stack-protector default requires the recorded workaround | Resolve in its assigned lane; reproduce without the shim there. This review does not close #723 |
| R606-3-S-a; SUGGESTION; Tests | `test_ctrl_memory.py:928`: any first failed assertion can count as a kill | Weaker attribution of a mutation's specific effect | Match per-property failure; verify a wrong-property control |
| R606-3-S-b; SUGGESTION; Robustness | `ctrl_memory.py:246`: coverage by address does not compare conflicting section and segment file bytes | Inconsistent metadata can describe different contents | Add inconsistent-ELF controls and explicit equality validation |
| R606-3-S-c; SUGGESTION; Tests | `test_ctrl_memory.py:579`: binary-extractor name derived from compiler name | Alternate compiler naming may fail without useful explanation | Select explicitly or refuse by name; verify an alternate-name control |
| R606-4-S1; SUGGESTION; Tests, Robustness | `ctrl_srp_image.py:96`, `test_ctrl_memory.py:970`: no standing real-largest-image fit gate | Headroom erosion appears at explicit image planning/export | Optionally add the real largest-image fit to CI; grow the fixture and require a named budget refusal |

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Scope rulings; REQUIREMENTS.md section 1; `SPLIT_CONTROL_MEMORY.md:139`; fresh four-point links and `receipts/audit-fit.log`: limits, staging and updated fit acceptance satisfied | R607-5 | 42678ae2f77fbbef056f7fb99859e0193181e6d7 |
| RTL | CLEAN | `milan_soc.py:2727,2759`; `ctrl_memory.py:295`; `ctrl_split.ld:13`; `ctrl_split_start.S:10`; `ctrl_memory_ooc.py:46`; `receipts/ooc-emit.log`, `mapping-crosscheck.log`: bank construction, map/reset ownership, mapped costs and unchanged executable delta checked | R607-5 | 42678ae2f77fbbef056f7fb99859e0193181e6d7 |
| Robustness | CLEAN | `ctrl_memory.py:264,339`; `test_ctrl_memory.py:349,473,559`; `receipts/focused-memory.log`, `audit-fit.log`: malformed loads, budget edges, wrong shape, bank boundaries, ROM protection, holes and error recovery | R607-5 | 42678ae2f77fbbef056f7fb99859e0193181e6d7 |
| Tests | CLEAN | `test_ctrl_memory.py:803,928`; `ci_scope.py:69`; both public fit probes; `scripts/audit_fit.py`; focused mutation baseline, all 38 kills, actual-image checks, author six-SoC-mutation receipt and source equivalence | R607-5 | 42678ae2f77fbbef056f7fb99859e0193181e6d7 |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md:139`; `MARK_II_AREA_PLAN.md:768`; `AREA_BUDGET.md:230`; PR body; current/earlier source attribution, primitive units, all ledger arithmetic and headroom, focused documentation receipts | R607-5 | 42678ae2f77fbbef056f7fb99859e0193181e6d7 |

**Real limits and pending manager duties**

- This is a delta review. Full SoC export, all-fabric digest comparison, full parent/processor/gPTP/builder banks and exhaustive synthesis/simulation banks were not repeated here. The unchanged source and the author's explicitly attributed receipts support preservation of earlier resolved work. The scoped simulator identity was verified but it was not used for a bank run.
- No independent synthesis run, integrated route, WNS result, split boot, CPU execution, service-time proof or persistence campaign is claimed. Physical calibration NOT RUN; field skips and the skipped physical hosted context are not hardware proof.
- `receipts/hosted-checks.json` is one exact-head snapshot: several jobs completed successfully, including all four synthesis shards, while documentation, elaboration, simulation shards and parts of the fast workflow were still running. The physical job was skipped. No aggregate completion is inferred from that snapshot; the manager owns hosted and local workflow-replica acceptance.
- Source-head validation remains distinct from the final current-dev candidate. The manager must construct and validate that candidate at merge time, run its builder and native banks, and link the receipts. The supplied source base and live dev are both `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`; a later dev change requires the manager's candidate handling.
- The manager must obtain the other independent verdict, ensure no review remains in flight, finish the full merge bar, and perform post-merge containment. This positive review is not merge authorization and does not close issue #640.

`receipts/audit-final.log` confirms exact head/tree, tracked bytes, modes and index. The populated pins are protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gPTP processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, and lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. The unused external gitlink remains `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` and uninitialized. No restoration of tracked source was necessary.

`REPRODUCE.md` describes the portable scripts. Scratch contains only unpublished disposable data. All publishable receipts are enumerated by relative path in `MANIFEST.sha256`. Public logs normalize local source/output/install roots and the synthesis host header; measurement values, results and image hashes are preserved.

R607-5 FINISHED
