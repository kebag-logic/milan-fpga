[R664] POSITIVE - exact head eef90b4238b6c19b679b44adc6f09362809be153

Round R664-2, external independent source review of PR #767, issues #761/#762.
Tree: `ba15df1ef198a7d86150b4e33726fe0a4a10f589`.
Source base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
Previously reviewed head: `4191b0987d1313abc86c747ad6a9c3c0963f17da`.
Delta: `ba9ac06a`, `492207f7`, `2cd2750d`, `eef90b42`.

All five lenses were applied. No open BLOCKER, MAJOR or MINOR remains in this source review. One wording residue and two optional suggestions are recorded below. This is not merge authorization or a completed current-dev candidate validation.

**Scope and authority**

Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, both issue bodies, the frozen assignment, the public scope decisions, REQUIREMENTS.md, the architecture/integration contracts, the full source-base diff and four-commit delta, then executable evidence. Prior public findings were considered after the independent delta inspection. No current-round reviewer report was used.

The governing decisions are the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/767#issuecomment-6260976498), [stopped-silence ruling](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6260976223), and [stopped-gap extension](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6265746720). The latter retains AAF-return restart behavior outside scope. Clause interpretation is carried from the prior round except for those explicit decisions: Milan v1.2 5.3.8.7, 5.3.8.10/Table 5.6, 5.4.2.19/.20, and IEEE 1722-2016 4.4.4.3. This later-round review does not claim a fresh full-standard audit.

The exact governing text is retained in `receipts/public-scope.txt`. The internal monitor gains a stopped-state input; the public datapath ports, parameters, register addresses and layouts do not change.

**Prior findings, explicitly disposed**

| Finding | Disposition at this head | Evidence |
|---|---|---|
| R663-1-F1, BLOCKER, Tests/Docs | Resolved in source; hosted acceptance remains a manager duty | `scripts/ci_case_receipts_selftest.py:118` derives the actual driver inventory; `:174` refuses `len(names)+1`. The largest legal split remains accepted. Local clean selftest passes and the disposable `len(names)` plant fails specifically with `receipt control accepted: shard 0/34`. Published gate_50 records 14/14 rc 0. |
| R664-1-F1, MAJOR, Conformance/RTL/Robustness/Tests | Resolved | `KL_avtp_rx_monitor_ctx.sv:903` captures eligibility at expiry; the Unbind clear is removed. `:1069` consumes and clears the mark while queuing the ordinary counter write. Local N=1/N=8 sweeps pass; restoring the clear in both engine and reference fails the named independent count checks. |
| R664-1-F2, MAJOR, all five lenses | Resolved under the public ruling | Both engines now exclude stopped-input silence and gaps. The ruling settles the previous scope conflict. `REGISTER_MAP.md:871`, compliance row 5.4.2.25, and `TESTING.md:614`/`:625` describe the decided behavior. Independent silence, STOP/live-traffic, START-recovery and Unbind checks pass. |
| R663-1-F2, MINOR, Conformance/Robustness/Docs | Resolved | The AAF mark reads `!stopped_i[s]`; CRF timeout reads `en_i && !stop_i`. Both gap paths also read the addressed input's started state. The documentation states the same rule for both engines. |
| R663-1-F3, MINOR, Tests/Docs | Resolved | `sim_lockstep.cpp:319`, `:794`, `:845` derive expiry from reset, the millisecond grid and observed acceptance, then demand the exact count at each offset. Equality with the modified reference is not the oracle. The paired consume-race plant fails `[SI]`, with no reliance on lockstep disagreement. |
| R663-1-S1, SUGGESTION, Tests | Retained, optional | See the suggestion below. |

**Applied-lens evidence**

[R664] PASS Conformance - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:903`, `:1017`; `hdl/ieee1722/crf/KL_crf_rx.sv:401`, `:550`; `hdl/milan/milan_datapath.sv:3247` - checked against the public #761/#762 contract and rulings.

A silence counts once only if bound and started at expiry. An Unbind or STOP on/before expiry prevents that silence count; one after expiry cannot erase it. A Controller Unbind adds nothing. A qualifying sequence gap counts on a started input, not a stopped one, and counts again after START. Sequence-mismatch observation remains active. The gap boundary is the AAF accept verdict or CRF accept edge, as documented. Selected CRF loss/gain still share the XOR request beneath the selection gate; received-mr and existing AAF causes remain unchanged. The round-2 delta does not alter the #761 implementation or its edge mutants.

[R664] PASS RTL - `KL_avtp_rx_monitor_ctx.sv:823`, `:903`, `:1069`, `:1144`; `KL_crf_rx.sv:530`, `:550`, `:637`; `milan_datapath.sv:5392`, `:6308` - checked event lifetime, counter writers, addressing, reset and integration.

The pending mark survives controller changes until the unlock walk consumes it. The queued SI increment uses the existing yielding RMW path; reset and bind-era clearing still remove prior-era state. CRF timeout and gap writes remain mutually exclusive when started; stopped gaps now generate neither competing SI write nor a playback event. The new AAF vector comes from the existing bound-and-stopped state in the same datapath domain. No CDC, width, counter-layout, top-level-port or parameter change is introduced. Public route receipts meet the resource policy; they are source implementation evidence, not hardware execution.

[R664] PASS Robustness - `tb/verilator/avtp_rxmon/sim_lockstep.cpp:589`, `:654`, `:706`, `:794`, `:845`; `tb/verilator/crf_rx/sim_main.cpp:1511`, `:1635`, `:1725` - checked ordering, repeated events, delayed walks, stopped observation and recovery.

The silence sweep grades every cycle from -12 through +24 plus far offsets, with both Unbind and STOP, idle and busy, at N=1 and N=8. The independent oracle requires exactly one MU, exactly the decided SI count, and no extra change after a further timeout. At N=8 the clean receipts show up to 136 cycles of delayed unlock and actual PDU service between MU and SI writes. The gap sweeps cover STOP and START from -4 through +20 of the input pulse, including before/on/after the verdict and delayed acceptance. Repeated stopped gaps, another input's STOP, reset during an update, bind-era clearing and resumed counting are covered. CRF directly grades stopped silence after established lock, STOP with live traffic, START recovery and Unbind/timeout coincidence.

[R664] PASS Tests - `scripts/ci_case_receipts_selftest.py:118`, `:174`; `tb/verilator/avtp_rxmon/lockstep_mutants.py:118`; `tb/verilator/crf_rx/mutants.py:44`, `:72`; packet scripts and receipts - checked that defects fail independent named checks.

Local focused execution, after verifying the prescribed simulator identity:

| Check | Result | Receipt |
|---|---|---|
| Receipt selftest | rc 0; actual inventory 34; over-shard 0/35 refused | `receipts/receipt-selftest.log` |
| Vacuous legal-split plant | Expected rc 1; specifically rejects accepting 0/34 as a negative control | `receipts/receipt-vacuous.log` |
| AAF clean pair | N=1: 116 checks; N=8: 119; zero failures | `receipts/aaf-clean-N1.log`, `aaf-clean-N8.log` |
| AAF paired consume-race plant | Both shapes rc 1, independent `[SI]` boundary failures | `receipts/aaf-consume-race-N1.log`, `aaf-consume-race-N8.log` |
| AAF paired delayed-stop-state plant | Both shapes rc 1, independent gap-boundary failures | `receipts/aaf-gap-stop-late-N1.log`, `aaf-gap-stop-late-N8.log` |
| CRF clean counter harness | 15,202 checks, zero failures | `receipts/crf-clean.log` |
| Seven paired CRF controls | All compile and fail their named count check with the defect in both RTL and replica | `receipts/crf-both.log` and the seven per-control logs |

The seven paired CRF controls cover missing silence, missing gap, counted Unbind, counted Unbind/timeout coincidence, counted stopped silence, counted stopped gap, and STOP permanently disabling subsequent gap counts. Repository `mutants.py` currently pairs the two stopped-gap controls; this review's portable `scripts/crf_both.py` additionally pairs the five existing unit controls. Do not infer that all seven paired plants are already in the repository driver. The normal driver requires the named count failure even for its single-engine plants. The reviewer probes confirm those checks remain effective when replica equality cannot expose the defect.

[R664] PASS Docs - `docs/reference/REGISTER_MAP.md:871`, `docs/reference/MILAN_COMPLIANCE_MATRIX.md:131`, `docs/testing/TESTING.md:614`, `:625`, and PR #767 - checked the decided counter rules, boundary descriptions, evidence provenance and limits. Added source comments describe behavior/reasons without new prohibited bench or reviewer labels. Historical unchanged comments are outside this delta's wording cleanup.

**Published evidence and its limits**

The [published evidence tree](https://github.com/kebag-logic/milan-fpga/tree/32af21b0d0ae35008fa65c3199b282419f171274/review-evidence/761-r1) supplies the author source-head receipts. `scripts/audit_public.py` verified all 176 selected round-2b receipts and their index against the manifest's `published_sha256`, including files whose public paths were redacted. See `receipts/public-digest-audit.log`.

Cryptographic signature authentication is NOT established: the publication commit reports `verified=false`, `reason=unsigned`, with no signature/payload, and no detached signature was identified in the packet. The verified claim is published-content digest identity, not a signed execution attestation (`receipts/evidence-signature.json`).

Spot-checked the focused raw logs, mutation outcomes, gate_50 results, suite summaries/union, static-gate exceptions, source identity and route reports. Their reported 63/63 suites sum to 2,188,354 checks with no suite failures/timeouts; the published 63-entry shard union equals the full inventory. The focused logs report AAF mutants 14/14, CRF mutants 18/18, and the unchanged mclk campaign 34/34. These are author executions, not newly executed full banks by this reviewer.

For source head `eef90b42`, route-1x1 reports LUT 49,597 (-16), FF 52,400 (+47), SLICE 15,680 (-45), RAMB36/18 74/25, DSP 14, WNS +0.189 ns and WHS +0.014 ns, fully routed. The receipt identifies 2026.1 build 6511674, `xc7a100tfgg484-2`, post-route physical optimization; the public handoff attests the unchanged recipe/default seed. `docs/design/AREA_BUDGET.md:416` permits +500 LUT, +600 FF, +80 slices and requires WNS >= +0.030 ns and WHS >= 0. Raw utilization/timing and the recorded gate agree. No new route was run here.

Builder calibration gate 11 is NOT RUN. Two other source static selftests record host-specific failures, disclosed in the public handoff; the source packet is not an unconditional all-gates-green claim. No manager source bank exists at this head. Physical calibration, field skips, simulation and routing supply no hardware proof.

**Findings and retained suggestions**

- **R664-2-R1 | RESIDUE | Docs**
  - Artifact: PR #767, Known limitations, sentence ending `the head is not pushed`.
  - Authority/evidence: the live PR identifies the published exact head; its hosted checks exist. The statement is stale publication wording in the current body.
  - Impact: confusing handoff timing; no changed measurement, test or source verdict.
  - Exact fix: replace `Hosted CI and the act replica were not run: the head is not pushed.` with `At the author handoff, hosted CI and the local replica had not been run. Their acceptance remains with the manager.`
  - Verification: current PR wording distinguishes the historical handoff from current publication; retain every result and exception.

- **R663-1-S1 | SUGGESTION | Tests | retained**
  - Artifact: `milan_datapath.sv:3247`; `milan_dp_mclk/sim_mclk.cpp:887`; builder initializer check at `sw/builder/test_builder.py:11379`.
  - Authority/evidence: the selected-source guard remains correct and statically pinned. The prior public finding identified no dynamic mclk rejection of an ungated rising edge. The relevant implementation/tests are unchanged in this delta.
  - Impact: optional behavioral evidence would complement the static wiring pin; this is not an open correctness defect.
  - Suggested outcome: relock CRF while INTERNAL or AAF is selected and grade zero restart requests/toggles.
  - Verification: an ungated-gain-edge plant fails that dynamic row while the clean source passes.

- **R664-2-S2 | SUGGESTION | Tests, Docs**
  - Artifact: `tb/verilator/crf_rx/mutants.py:44`, `:72`; `sim_main.cpp:1723`; packet `scripts/crf_both.py`.
  - Authority/evidence: the built-in driver pairs only the two stopped-gap plants. This review demonstrated the five earlier unit plants also fail independent named checks when paired with their replica edits.
  - Impact: no uncovered count defect remains, but preserving these paired probes would make future independence checks easier and clarify the scope of the comment saying every #762 mutant is paired.
  - Suggested outcome: incorporate the paired unit plants; until then, say `both stopped-gap mutants` in that function's comment.
  - Verification: the clean harness passes and all seven paired controls fail their named count checks, as in the attached receipts.

**Reviewer-owned coverage ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ctx expiry/gap guards; CRF timeout/gap guards; datapath selected-CRF request; public scope rulings | R664-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| RTL | CLEAN | ctx event capture, RMW and era reset; CRF counter writers; datapath stopped vector; route-1x1 reports | R664-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| Robustness | CLEAN | AAF silence/gap sweeps at N=1/N=8; CRF stopped/recovery/Unbind cases; paired ordering probes | R664-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| Tests | CLEAN | real-inventory over-shard control; count oracles; paired mutants; local receipts and public gate receipts | R664-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| Docs | CLEAN | register counter contract; compliance row; testing descriptions; scope decisions; PR evidence and stated limits | R664-2 | eef90b4238b6c19b679b44adc6f09362809be153 |

The artifact-specific PASS paragraphs above define each row's evidence. Unchanged code retains its earlier assessment except where the stopped-state/event-lifetime delta changes a dependency. RESIDUE and SUGGESTION do not make a lens unclean under the owner's rule.

**Remaining manager duties and integrity**

At the single hosted observation, docs-gates-0/1/2 were still in progress; required aggregate acceptance was not established. `receipts/hosted-observation.tsv` preserves each observed status and URL, including skipped contexts. No polling or hosted/local-replica acceptance was performed here.

The manager must complete hosted and local-replica acceptance, validate the exact current-dev merge candidate with builder/native and other required banks, and publish its receipts. The source base is e9cbb676; the assigned live-dev reference is `e26f1816e456dc8027924bc2e5d327a8aa6e46db`, to be refreshed at merge time. This report supplies no composition verdict. Two independent positive reviews, no review in flight, explicit merge authorization, post-merge containment, current docs and issue/project closure remain required. Hardware/field obligations remain separately outstanding.

No source fixes, commits, pushes, GitHub writes, contact, delegation, hardware access, container execution or full validation banks were performed. Disposable builds and mutated copies are confined to packet `scratch/`. After probes, raw blob bytes, modes and index were checked against HEAD, including all four required submodules at their gitlinks; all match (`receipts/checkout-integrity.log`). The parent worktree is clean. Only REPORT.md and files in MANIFEST.sha256 are publication material; scratch is excluded.

R664-2 FINISHED
