[R607] NEGATIVE - exact head 76605880a20005cbc2acad1b23ba2ccebde64ca8

External independent review, round R607-2, issue #640 / PR #721. Tree: `0d5e91af9d99c5c2f30e5c4aa1723f463dbe303d`. All five lenses were applied. The earlier mandatory findings are resolved at this head. One new MINOR remains: an inconsistent ELF can pass the documented reset-byte rule and export a ROM with the reset code missing.

The independent verdict and ledger were written before either prior public review was read. No concurrent round-2 report or private author material was used. The source checkout was not edited. All generated trees, images, SDK files and builds stayed under this packet's unpublished `scratch/` directory.

**Scope and authorities**

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, linked requirements and interface authorities, the requested `e8454e2751d05b02ee8e5a571857589ab358ab86..76605880a20005cbc2acad1b23ba2ccebde64ca8` diff and history, then public executable evidence. The inherited dev changes were distinguished using `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5..HEAD`.

The [M8a assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426), [ruling on the STOP](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877), and [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105011666) govern this review. M8a-1 covers the split memory map and instantiation, four-point fit, measured ledger rows, named controls, and preservation of the all-fabric default. The ruled firmware allocation is up to 56 RAMB36 equivalents, with the split's conditional storage release and the separate 13.5-tile reserve preserved. The issue-wide LUT target remains an eventual milestone requirement, not a claim that this PR closes #640.

REQUIREMENTS.md section 1, NFR-SCOUT-01..03 and NFR-RES-01 in `docs/reference/FR_NFR.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, and the L11/memory-ledger sections of `docs/design/MARK_II_AREA_PLAN.md` establish the placement and capacity context. Boot, service checks, integrated fit and routing are M8a-2 after F-INT PR 2. This review does not treat those deferred proofs as missing M8a-1 acceptance.

**R607-2-F1 - MINOR - Conformance, RTL, Robustness, Tests, Docs**

Artifact: `sw/litex/ctrl_memory.py:232`, `:259`, `:297`; `sw/litex/milan_soc.py:2725` and `:2744`; `sw/litex/test_ctrl_memory.py:304`; `docs/design/SPLIT_CONTROL_MEMORY.md:70`. The reset-byte check uses section metadata, while ROM construction uses a different, unchecked population of file-backed load bytes.

Authority/evidence:

- Round-2 item 1 requires the documented refusal rules to have effective checks and tests. The `entry bytes` rule promises to refuse an image with no initial bytes at the reset address. The memory contract also says that ROM is initialized with the linked image. AGENTS.md requires malformed-input review and tests that can fail for their claimed defect.
- `read_elf` marks a section loaded whenever it is not NOBITS. Its LMA lookup uses a segment's memory size, without checking that the section is covered by that segment's file bytes. `check_map` therefore accepts the section as evidence of reset bytes. `rom_words` copies only the segments' actual `p_filesz` bytes.
- `probe_load_soc.py` links the exact-head `ctrl_split_start.S` and `ctrl_split.ld` with the suite's small C probe. The original image passes map and staging checks, and its first instruction is `10003117`.
- The probe changes only `p_filesz` of the PT_LOAD containing `_start` to zero. The section table, entry, file contents, staging symbol and other segments remain unchanged. The real split SoC build returns **0**, emits one Verilog top, and programs **eight zero words** at the beginning of ROM instead of the original reset instructions. See `receipts/load-soc-linked.log` and its rc file.
- `probe_elf_loads.py` also demonstrates acceptance when the reset segment is shortened to four bytes: the first word survives and following reset/code words become zeros. Its header-cut controls are refused by the new named truncation rule. See `receipts/elf-loads.log`.
- The unmodified exact-head suite still passes all 109 checks and catches its 40 standing mutants. Its `entry bytes` arm moves the section away from the entry; it never makes section metadata disagree with programmed load coverage.

Impact: malformed or damaged load metadata can produce a successfully exported image that omits the declared reset code. This is a build-input validation defect; no failure is claimed for the four published well-formed size fixtures. The MINOR classification reflects that boundary. It is not RESIDUE: code, tests, generated initialization data and a documented behavior claim are involved.

Required outcome: before export, refuse by name an initialized section whose required bytes are absent from the load data that actually programs ROM, including an empty or short reset segment. Add a regression using a genuinely linked image, and show that removing or weakening the coverage check causes a named failure. Preserve acceptance and bytes of the unmodified valid image; do not weaken the documented reset-byte rule.

Verification: rerun the linked-image probe with a fresh scratch output directory. The malformed image must be refused before Verilog or ROM initialization files are produced. The valid control must retain its reset words. Cover the zero-length and short-segment variants and rerun the focused suite.

Lens attribution is deliberate: Conformance covers the ruled refusal contract; RTL covers the incorrect generated ROM initialization; Robustness covers malformed metadata; Tests covers the undetected input class; Docs covers the unconditional implemented-refusal claim. These are one defect and one required correction, not five independent findings.

**Exact-head checks and evidence**

| Check | Result and artifact |
|---|---|
| Focused memory suite, with a freshly verified pinned RV32 SDK | 109 checks, zero failures, `RESULT: PASS`; all 40 mutants caught. `receipts/test-ctrl-memory.log`, `receipts/sdk.log` |
| Previous twelve mutation semantics | Each corresponding edit is caught by a named check in the head's standing suite. `receipts/reconciliation.log` maps all twelve names. The previous external driver itself was not rerun. |
| Independent memory-bus scoreboard | 864 address cases pass over 2 KiB, shipping-sized 64/32/8/4/2 KiB, and near-limit 128/64/16/8/4/2 KiB bank sets; both ROM and SRAM, read-only behavior, byte enables, boundaries and holes through word 65535. `receipts/bus-scoreboard.log` |
| Real build controls and flags | The suite observes budget, overlap and wrong-stage refusals before export; both lone flags are refused; the passing split export has the expected banks and initialization, no BIOS ROM/SRAM, and no shipping firmware package. The `main()` staging-call mutant is caught. |
| All-fabric default versus merged dev | Both shipping configurations: **21 files each, zero differences**, including gateware, initialization files and generated interfaces. Only source/output roots, generation stamps and the hierarchy comment were normalized. Software compilation was disabled. `receipts/default-comparison.log` |
| Aggregate harness self-test | rc 0; `receipts/runner-selftest.log`. This is the harness self-test, not a claim that the seven-member aggregate was rerun here. |
| Documentation and quality checks | `docs_check.py`, `check_doc_paths.py`, `gen_toc.py --check`, `check_em_dash.py --base ac2c5e77`, `check_py_idiom.py`, and the requested-range whitespace check all return 0. Separate logs and rc files in `receipts/`. |
| Original checkout integrity | Raw bytes, executable modes, index records and all three required submodule populations match the exact head before and after probes. `receipts/integrity-before.log`, `receipts/integrity-final.log` |

The fit evidence was read from the [published author packet](https://github.com/kebag-logic/milan-fpga/tree/f8cf850337aaf3cf7f7521c076faec0ca606c1f7/review-evidence/640-m8a-r1), then checked against the [round-2 author evidence](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6106342513) and the PR's per-head gate table. Downloaded public files were verified against their Git blob IDs (`public-evidence/provenance.tsv`). No author handoff or private lane material was read.

| Point | ROM / SRAM need, bytes | Planned tiles | Mapped RAMB36 / RAMB18 | Mapped tiles |
|---|---:|---:|---:|---:|
| 1x1, one interface | 95,032 / 45,520 | 35.0 | 33 / 2 | 34.0 |
| 1x1, two interfaces | 96,320 / 56,880 | 38.0 | 37 / 1 | 37.5 |
| 8x8, one interface | 108,680 / 86,080 | 48.5 | 46 / 2 | 47.0 |
| 8x8, two interfaces | 110,056 / 112,208 | 54.5 | 52 / 2 | 53.0 |

`check_receipts.py` independently adds the per-region primitive counts, checks them against all eight utilization reports, and recomputes the ledger. The measured allocation gives `87.5 - 6.5 + 6 - 18 + 53 + 2 - 11 = 113`; the ruled maximum gives **116**, leaving **5.5** below 121.5. The largest ROM region's 231 LUT cells includes decoding and multiplexing; its utilization report gives 220 Slice LUTs. Those are different counting bases. The 13.5-tile reserve is not consumed by this arithmetic. Conditional storage release remains a future integration obligation.

The four size fixtures were not relinked in this round and synthesis was not repeated. The author reports that all four split and four flat ELFs, and the emitted mapping inputs apart from stamps, are unchanged in round 2. The memory-bank construction and linker/reset sources are unchanged since round 1. Source-head execution evidence is the author's published receipts plus the focused reviewer runs above. **No manager source bank ran at this exact head, and none is inferred.**

**Disposition of earlier public findings**

The [prior internal findings](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6104999232) and [prior external findings](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6105008317) were read only after the independent pass, verdict and ledger had been written.

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R606-1-F1 | RESOLVED | `SHF_WRITE` is retained; `check_map` refuses writable data in ROM. The real-link plant and its removal mutant are exercised in the passing focused suite. |
| R606-1-F2; R607-1-F1 | RESOLVED as originally reported | Budget equality and half-tile boundaries, missing entry section, NOBITS, load-address overlap, full-window decode and immediate access after err now have effective arms. All twelve previous mutation semantics are caught. F1 above is a newly demonstrated discrepancy between section metadata and load bytes. |
| R606-1-F3; R607-1-S1 | RESOLVED | The real `main()` build path is tested; the missing-stage-call mutant is caught; passing export and both flag pairings are checked. |
| R606-1-F4; R607-1-F2 | RESOLVED | Both ledgers state 116 and 5.5 at 56 tiles; the lane row names 56; AREA_BUDGET states that 53 is out of context. Arithmetic reproduced. |
| R606-1-F5; R607-1-R2 | RESOLVED | The 231 figure is attributed to the whole ROM region with decode/multiplexer, and the cell versus Slice LUT basis is explicit in docs and the PR body. |
| R607-1-F3; R606-1-R2 | RESOLVED | The examined PR body identifies this head, `08b90b68`, the dev merge and the seven-member aggregate, with evidence heads retained. |
| R607-1-R1 | RESOLVED | SPLIT_CONTROL_MEMORY.md states 3 mapped tiles versus 1.5 planned tiles / 6 KiB growth. |
| R607-1-S2; R606-1-S3 | RESOLVED for the reported truncation cases | Header reads now raise the named `elf truncated` refusal. The standing tests and independent 6/7/16/20/40/51-byte header cuts verify it. This is not a claim of complete validation of every malformed ELF structure. |
| R606-1-R1 | RETAINED as RESIDUE | Exact wording fixes below; the manager explicitly left this outside round 2. |
| R606-1-S1 | RETAINED, optional | The reset entry still does not install a trap vector. The split boot/service proof remains M8a-2. No trap behavior is claimed here. |
| R606-1-S2 | RETAINED, optional | There is still no separate assertion that the initialization-word list fits the planned ROM banks. The opposite coverage failure is demonstrated by new F1; these are not the same reproduction. |
| R607-1-S3 | RETAINED as pre-existing, separate work | The manager assigned the runtime stack-protector issue separately. This review did not rebuild those runtime archives or verify closure of that separate issue. |

**R606-1-R1 - RESIDUE - Docs (retained)**

Artifacts: `docs/design/AREA_BUDGET.md:263`; `docs/design/MARK_II_AREA_PLAN.md:832`. The word “measured” qualifies a ledger total that includes M2's unused +2 allowance. Keep every figure and claim unchanged; make these exact wording substitutions:

- AREA_BUDGET: “With M2's unused +2 allowance, the ledger is 2.5 tiles over 121.5 before conditional reclamation.”
- Plan: “Before the conditional release, with M2's unused +2 allowance, the total is 2.5 tiles over 121.5.”

Impact: wording only. Required outcome and verification: apply those two sentences and confirm the arithmetic remains unchanged. This retained residue does not affect the verdict or lens coverage.

**Reviewer-owned ledger**

Every lens was applied independently; F1 crosses them for the reasons recorded above. No lens is banked clean while that finding remains open.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Issue rulings 6101485877 / 6105011666; REQUIREMENTS.md section 1; ctrl_memory.py:74 and :253; four fit plans and eight utilization reports; ledger arithmetic; actual build controls and default comparison | R607-2 | 76605880a20005cbc2acad1b23ba2ccebde64ca8 |
| RTL | UNCLEAN (F1) | milan_soc.py:2710-2756 bank decoder, error pulse and initialization; ctrl_split.ld and ctrl_split_start.S; 864-case bus scoreboard; linked probe's actual exported ROM bytes; dev/head gateware comparisons | R607-2 | 76605880a20005cbc2acad1b23ba2ccebde64ca8 |
| Robustness | UNCLEAN (F1) | ctrl_memory.py:185-301; malformed load coverage, header truncation, exact budget boundaries, writable ROM, absent stage, overlap, whole-window holes, read-only behavior and byte enables | R607-2 | 76605880a20005cbc2acad1b23ba2ccebde64ca8 |
| Tests | UNCLEAN (F1) | test_ctrl_memory.py, 109 checks / 40 mutants; old-mutation reconciliation; real-build controls; independent load and bus probes; run_litex_sims.sh inventory and self-test | R607-2 | 76605880a20005cbc2acad1b23ba2ccebde64ca8 |
| Docs | UNCLEAN (F1) | SPLIT_CONTROL_MEMORY.md:64-92, fit/reproduction sections; AREA_BUDGET and MARK_II ledgers; mailbox, architecture, testing and CI additions; firmware README; PR body and public source receipts | R607-2 | 76605880a20005cbc2acad1b23ba2ccebde64ca8 |

**Real limits and pending manager duties**

- This is source review with focused execution. No full parent, processor, gPTP, Yosys or builder bank, no synthesis, no CPU boot simulation, no hardware work and no local workflow replica was run. The scoped simulation compiler's identity was verified; it was not needed by these focused checks. Physical calibration is **NOT RUN**; field and hosted physical skips supply no hardware proof.
- The default comparison independently covers gateware and generated interfaces, with software compilation disabled. The author's published comparison includes the compiled BIOS; this review does not reclassify that author evidence as reviewer execution.
- `receipts/hosted-snapshot.json` binds every inspected run to this exact head. At that observation, `elaborate`, `rtl-fast` and `rtl-full` failed. Their selector/classifier steps failed; the simulation and synthesis shards were skipped, and the exhaustive aggregates failed. The docs workflow was still in progress; wire-accountability and docs-check-no-git had succeeded. These skipped jobs did not execute the long gates. No hardware or source-bank success is inferred from them.
- The manager owns hosted/local-replica acceptance and must resolve or supersede those unsuccessful contexts. They are recorded as pending acceptance, not diagnosed here as a new source-code defect. The current-dev merge candidate remains separate: the manager builds and validates it at the merge turn, publishes builder/native-bank receipts, and checks containment afterward. Source base is `e8454e2751d05b02ee8e5a571857589ab358ab86`; the specified live dev is `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.
- Fix and independently re-review F1 at a new exact head. Carry the retained residue to the checklist, settle all review rounds before merge, and retain the M8a-2 boot, service and route obligations. No merge authorization is implied by this report.
- No source fixes, commits, pushes, GitHub writes, author contact or delegated review occurred. Final verification hashes 1,278 parent blobs and 562 / 104 / 214 blobs in the required processor/processor/axis submodules, with matching modes, index entries and gitlinks. The source checkout remains clean.

**Reproduction and packet**

`run_focused.py --repo <exact-head-checkout> --litex-python <interpreter> --sdk-archive <pinned-archive> --verilator <scoped-executable>` creates its disposable copy and SDK, checks the harness, and runs the focused suite. `run_probes.py --litex-python <interpreter> --label <fresh-label>` reproduces the independent ELF, real-build and bus probes. The load probes deliberately return success when they reproduce the reported defect; successful execution of those scripts is not a clean-image verdict. `compare_default_exports.py <checkout> <interpreter>`, `check_receipts.py`, and `verify_checkout.py <checkout>` reproduce the remaining checks.

All review commands stayed under a foreground parent that waited for its children. Independent tasks ran concurrently, with at most six children and no synthesis run alongside them. Public receipts preserve command output with only local-path substitutions; unredacted originals and disposable trees are under unpublished `scratch/`. `MANIFEST.sha256` lists the publishable report, scripts, receipts and selected public source evidence. Unlisted files must not be published.

R607-2 FINISHED
