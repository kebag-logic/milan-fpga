[R928] NEGATIVE - exact head 248d85c1453213b0f1642967a4046f395c82c56b

External independent review, R928-1, of [PR #1004](https://github.com/kebag-logic/milan-fpga/pull/1004) / [issue #878](https://github.com/kebag-logic/milan-fpga/issues/878). Tree `ad0444dbf9089b90ac3693c0bc46421894cfadeb`; reviewed diff from `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. All five lenses were applied. Two acceptance/evidence findings remain open; one source-comment residue is nonblocking. No functional source defect was established by the focused checks.

The independent verdict and initial ledger were written before checking prior PR review findings. The final report incorporates the acceptance cross-check. No private author material or another reviewer's report was used. The public evidence root below is **P**: [review-evidence/artysplit-r1 at 0723eba4bd2175f36b26fa69e1b0b898740853af](https://github.com/kebag-logic/milan-fpga/tree/0723eba4bd2175f36b26fa69e1b0b898740853af/review-evidence/artysplit-r1). Receipt paths are relative to P unless identified as source paths.

**R928-1-F1 — MINOR — Conformance, RTL, Tests, Docs — primary signoff receipts absent from the published packet.**

Artifact: `P/author/REPORT.md:84`, its verification table at line 88, `author/receipts/build-corrected-images-graded-images.json`, and `author/receipts/build-corrected-final-census-qualification.json`. Authority: AGENTS.md sections 1, 6 and 7 require publicly reconstructible evidence and exact-head verification; #878's build acceptance and owner decisions require measured service qualification and corner timing.

Evidence: the actual published Git tree, not merely the local extraction, contains none of the twelve `build-corrected-images-<directive>-digilent_arty_signoff_<corner>_timing.rpt` reports referenced by the grade. It contains no native `.log` or `.log.gz` files under `author/receipts`, including the 145-case census's event traces, and no `receipts/INDEX.md`. The census `.txt` files are stimulus inputs. JSON grades, hashes, statuses, command records, utilization and check_timing reports are available and consistent; decompressed JSON equivalents were accepted where present. This finding concerns missing primary observations, not a filename suffix difference. The report nevertheless links missing execution logs and says the complete traces and reports were preserved. See `evidence-inventory.log` and `audit.log`.

Impact: a cold reviewer can check the arithmetic and summaries but cannot re-grade the native observations or inspect the setup/hold paths behind mandatory measured signoff. This is an evidence-publication defect, not evidence that timing or execution failed.

Required outcome: publish the referenced primary timing and execution receipts, with provenance and hashes tied to this source and firmware, and a correct receipt map. An accessible equivalent public archive is sufficient. Verification: validate its hashes/source binding, re-grade the native traces and all twelve corner reports, and reproduce the selected directive and qualification results. This does not inherently require a source change or rerunning sound original executions.

**R928-1-F2 — RESIDUE — Docs — new source comments retain round chronology.**

Artifacts and exact fixes:
- `tb/verilator/ctrl_service_budget/egress_ledger.py:13`: replace `(#878, round 4)` with `(#878)`.
- `configs/endstation_arty_split.yaml:142`: replace `the RTL reset the MRP timer round corrected.` with `the RTL's corrected MRP timer reset.`
- `configs/endstation_arty_split.yaml:155`: replace `round's reflash` with `image's reflash`.

Authority: the owner's 2026-10-15 source-comment rule requires behavior/reason and issue or requirement references, without review-round chronology; a copied comment in a new file is a new instance in the delta. Impact: prose residue only. Required outcome and verification: make the exact wording changes and inspect the added source comments. Measurements, clauses, code behavior and generated artifacts do not change. This finding does not unclean any lens.

**R928-1-F3 — MAJOR — Conformance, Robustness, Tests, Docs — frozen bench acceptance is not reconciled with the shorter published run.**

Artifacts: [#878 acceptance items 4–7](https://github.com/kebag-logic/milan-fpga/issues/878), [the later bench instruction](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), and [the exact-image bench report](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7146699931), also `P/author/bench/REPORT.md:18` and its “Not covered” section. Authority: AGENTS.md sections 2, 4 and 7 freeze acceptance, require public resolution of conflicting scope, and prohibit silently replacing it.

Evidence: the issue requires offset and peer delay over at least ten minutes, captured stream frames, one hour with both connections up and before/after counters, and a timed saved descriptor change read back after reset. The current report supplies sync/peer-delay polling, explicitly no capture, 1,046 seconds of measured concurrent streaming, and no timed save/reset/readback. Link-up counters over 103 minutes do not establish the required hour of concurrent-stream counter continuity. Earlier issue reports describe other images and even identify unresolved save-time observability; there is no exact-image carry-forward argument for these missing criteria. The later instruction lists boot, enumeration, full-duplex link and one stream each way, but does not explicitly retire or replace the frozen requirements. The clock and held-egress rulings do not resolve this discrepancy.

Impact: the PR proposes to close #878 while the public record supports a shorter bench qualification. It cannot presently establish the issue's complete acceptance or bank the missing soak/reset robustness coverage.

Required outcome: publicly reconcile the acceptance contract. Either publish qualifying evidence for the outstanding criteria on this image (or justified equivalent unchanged artifacts), or obtain and record an explicit owner scope decision identifying which original criteria remain elsewhere or are replaced. Do not turn the shorter run into a one-hour or capture claim. Verification: check the decision against the issue and PR, then check the required bench receipts, including duration, counter endpoints, capture/offset scope, saved value, reset/readback and measured save time as applicable. No reviewer hardware action was taken or requested.

**Conformance examination.** The issue body and public decisions were reconstructed before the diff. The [entity/mode decision](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), [80 MHz decision](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097204685) and [seven-row ledger decision](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930) were checked against `configs/endstation_arty_split.yaml`, `sw/firmware/ctrl/loop/ctrl_loop.h:397`, `tb/verilator/ctrl_service_budget/arty_grade.py`, `egress_ledger.py`, REQUIREMENTS.md and FR_NFR.md section 3.4.1. The shape remains one interface, one AAF talker, one AAF listener and one CRF input. The MII-only PHY policy implements the 100BASE-TX full-duplex restriction.

The 145 published case grades span eight variants; all native statuses are zero, with no reported timeout, trap, bus error or SHARE overrun. They report only the seven authorized held-egress misses. These remain misses against 20 ms, bounded separately at 60 ms plus measured service with 5 percent allowance and upward 0.01 ms rounding; they are not reclassified as ordinary-budget passes. The independently executed stated-cost model and published measured summary agree:

| Quantity | Result | Owner limit |
|---|---:|---:|
| Load | 0.4966771140 | 0.70 |
| txL | 48.74 ms | 49 ms |
| Last notice | 121.84 ms | 140 ms |
| ACMP | 28.82 ms | 30 ms |
| Maximum recorded whole pass | 134507 cycles / 1.6813375 ms | 160000 cycles / 2 ms |

The model is a stated-cost calculation; native summaries are author execution evidence, limited by F1. The derived slice is 950 us, pace 9 ms and queued bound 125 ms. F1 and F3 leave Conformance unclean.

**RTL and architecture examination.** `sw/litex/milan_soc.py:253` fixes the Arty VCO at 800 MHz, with exact divisors 10/32/16/4 for CPU/sys 80, PHY reference 25, datapath 50 and IDELAY 200 MHz. Every output retains margin zero. The focused PLL check accepts this plan and rejects non-exact requests. CPU/sys to datapath CSR crossing uses the existing asynchronous FIFO channels at line 844; frame crossings use `_axis_dp_cdc` at line 1629; split mailbox publication uses `KL_mbx_cdc` around line 3327. The runtime correction registers and their consumers remain in the datapath domain, adding no raw multi-bit clock crossing.

`hdl/milan/milan_datapath.sv:1863`, `hdl/common/csr/milan_csr.sv:122`, `KL_gptp_shadow.sv:397` and `KL_gptp_txret.sv:305` were checked for reset defaults, accepted-write gating, low-16-bit application/high-bit scratch semantics, ingress snapshot timing and signed egress arithmetic. The signed 18-bit intermediate covers the full 0–65535 ns correction range and is sign-extended before timestamp subtraction. The extra pipeline edge is documented and exercised by the added exchange/write tests. The option defaults off, preserving the shared images' constant-correction path.

The published route summaries select ExtraTimingOpt correctly: worst WNS/WHS +0.617/+0.017 ns, versus +0.589/+0.017 for AltSpreadLogic_high and +0.009/+0.021 for ExtraPostPlacementOpt, which fails the +0.030 ns setup floor. Selected Slow reports are +0.617/+0.102 and Fast reports +1.613/+0.017 at both temperature labels, with zero reported failing endpoints. Temperature labels are power metadata, not four independent PVT timing models. F1 prevents independent raw-path signoff and leaves RTL unclean.

The available **post-placement** utilization report records 33411/63400 LUTs (52.70%), 40479/126800 FFs (31.92%), 78.5/135 BRAM tiles (58.15%) and 14119/15850 occupied slices (89.08%). Denominators match `sw/builder/endstation_builder.py:499`. These are not relabeled as independently measured post-route utilization. The firmware ledger, `docs/design/SPLIT_CONTROL_MEMORY.md:3465`, separately records ROM/SRAM live extents 124412/53392 bytes and allocation 44/56 RAMB36 equivalents.

**Robustness examination.** `ctrl_plat_phy.c:213`, `test_plat_phy_mii.cpp`, `ctrl_plat_console.c:168`, `test_plat.cpp`, the timestamp test additions, and the boot/region probe changes were inspected for invalid modes, failed management transactions, retry/repair, reset, malformed decimal input, extra fields, overflow, disabled configuration and in-flight writes. Focused host checks pass both console configurations, MMIO and eight MII cases. Ledger controls reject new misses and one-cycle larger misses. SHARE controls accept 160000 and reject 160001 cycles at 80 MHz. Region observations now follow the shipping cached CPU and its real clock; instruction synchronization is explicit. No additional implementation defect was found. F3 leaves the issue's required soak/reset evidence unclean.

**Tests examination and execution.** `focused.py` launches independent checks concurrently within the job limit and writes a separate log/return code for each. `service_delta.py` completed all 1034 baseline grader assertions and caught both new clock mutations: leaving temporal stimulus at 100 MHz and omitting the build clock at the group factory. Payload bytes/counts and unchanged AX stimulus remain distinct from scaled time quantities. Host checks pass 13 console tests without the option, 13 with it, two MMIO tests and eight MII tests. Owner-bound controls, record-class controls, held-egress controls and PLL controls all pass. `audit.py` verifies 1835 inspected published-file hashes, all 86 qualified source hashes against this head, every census grade/status, model/route arithmetic, memory figures and the 42 generated/product plus 13 raw SoC-export identity comparison results.

The broad service mutation self-test was stopped by this review's 480-second timeout (rc 124); it is not claimed as a pass or a product failure. Its partial receipt is retained. The separate baseline/new-mutation run completed successfully. The author's 297-mutation result remains an author claim whose underlying log is missing under F1. No native 145-case campaign, full bank, synthesis, route or hardware execution was repeated in this review.

Shared-image inspection covered the default-off builder/SoC/RTL option, PHY conditional branch, scheduler defaults and all four pre-existing scheduler blocks. The published comparisons report byte identity for both AX firmware ELFs and controlled raw exports; AX bitstreams were not rebuilt. No full shared-image regression bank was inferred from these focused checks. F1 and F3 leave Tests unclean.

**Documentation and bench examination.** The changed register map at `docs/reference/REGISTER_MAP.md:1035`, clock plan at `docs/litex/CLOCK_DOMAINS.md:105`, gPTP architecture, build instructions, memory ledger and REQUIREMENTS scope describe the optional runtime corrections and exact clock. Source history contains three documentation-only commits before the implementation commit; the qualified-source receipt binds the final 86 changed paths to this head. F1 and F3 leave Docs unclean; F2 is nonblocking.

The bench report identifies the flashed bitstream as `1046292da1e73b2b595f65c66d9c429fb183a43e3466e160d95024651014735c`, with read-back verification, VERSION 0x00030060 and mailbox 2.4. It reports 33/33 descriptor reads, **32** byte-identical bodies and one permitted runtime available_index difference matching ADP. It reports 1,046 seconds of three concurrent streams with zero listed error counters. The two AAF endpoint counter samples differ by one packet; they are not literal equality. None of this is a wire capture.

The new entity ID `024b4cfffe4b4c02` is the declared #840 identity change, not a regression finding. The shared serial string remains as documented. [Issue #1006](https://github.com/kebag-logic/milan-fpga/issues/1006) records the input accumulated-latency observation: valid with zero versus 137445 ns at the peer. It explicitly awaits ingress wire confirmation. This review neither declares that suspicion fixed because it was filed elsewhere nor treats a confirmed code defect as cleared. The report's default 1409/100 correction, temporary 0/0 measurement and restoration are distinguished from physical calibration.

**Prior public findings.** After writing the independent verdict and initial ledger, the PR discussion, submitted reviews and review threads were checked again: three discussion comments, zero submitted reviews and zero inline review threads. The comments are the bench report and two review-start notices. There were no prior public reviewer findings to resolve or retain. The bench observations are assessed above. Another review remains a manager-owned prerequisite; its report was not read.

**Reviewer-owned completion ledger.** All statuses concern this exact head; an UNCLEAN row was examined but banks no clean coverage.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1, F3 | #878 body/rulings; configs/endstation_arty_split.yaml; FR_NFR 3.4.1; arty_grade.py; 145 grades; bench report | R928-1 | 248d85c1453213b0f1642967a4046f395c82c56b |
| RTL | UNCLEAN — F1 | milan_soc.py:253/844/1629/3327; milan_datapath.sv:1863; milan_csr.sv:122; KL_gptp_shadow.sv:397; KL_gptp_txret.sv:305; route/resource receipts | R928-1 | 248d85c1453213b0f1642967a4046f395c82c56b |
| Robustness | UNCLEAN — F3 | ctrl_plat_phy.c; ctrl_plat_console.c; test_plat_phy_mii.cpp; owner/ledger/share controls; timestamp/reset tests; bench duration/reset scope | R928-1 | 248d85c1453213b0f1642967a4046f395c82c56b |
| Tests | UNCLEAN — F1, F3 | focused-results.json; service-delta.log; service graders/probes; qualified-source and identity receipts; missing primary receipts/bench criteria | R928-1 | 248d85c1453213b0f1642967a4046f395c82c56b |
| Docs | UNCLEAN — F1, F3; F2 residue | REQUIREMENTS; REGISTER_MAP:1035; CLOCK_DOMAINS:105; SPLIT_CONTROL_MEMORY:3382; author/bench reports and issue contract | R928-1 | 248d85c1453213b0f1642967a4046f395c82c56b |

**Limits, reproduction and remaining duties.** The scoped simulator identity was checked before any potential use; no RTL simulator build was ultimately run. Physical calibration is NOT RUN. Historical area calibration and field skips are not hardware proof. No cold power-on was tested; it is explicitly out of #878 scope. The partner's own port status and wire capture were not read. Hosted executed/skipped jobs were not audited here, and no hosted acceptance is claimed.

Source-head execution evidence is the author's published receipts. There is **no manager source bank at this head**. The manager still owns hosted/local-replica acceptance and the separate current-dev merge candidate, including builder and native banks, candidate receipts, both independent positive reviews, no review in flight, authorization, merge and post-merge containment. The source base and the assignment's live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` are distinct; this review does not validate that future merge result. F1 needs public primary receipts and re-review; F3 needs explicit acceptance resolution and corresponding evidence; F2 goes to the residue checklist.

Portable reproduction entry points:

```sh
python3 focused.py "$SOURCE" "$PACKET" "$INTEGRATION_PYTHON"
python3 -B service_delta.py "$SOURCE" "$PACKET"
python3 audit.py "$SOURCE" "$PUBLIC_PACKET"
python3 evidence_inventory.py "$SOURCE"
python3 integrity.py "$SOURCE"
```

`PUBLIC_PACKET` is the allowed public extraction rooted at P. `focused.py` retains the recorded 480-second cutoff, so its broad mutation leg may again time out; do not reinterpret that status. All disposable outputs belong under `PACKET/scratch`. Published receipt paths substitute $SOURCE, $PACKET and $INTEGRATION_PYTHON for local paths; measurements and return codes are unchanged. `MANIFEST.sha256` lists the publishable files; scratch is excluded.

Final integrity verification: all 1941 tracked blobs match exact HEAD bytes and modes; the index matches the reviewed tree; the checkout is clean. All six gitlinks match the tree/index, and the five initialized submodule checkouts match their required commits with clean tracked diffs. `external` remains uninitialized and is claimed only as a verified gitlink. No source edit, commit, push, public write, hardware operation or merge was performed.

R928-1 FINISHED
