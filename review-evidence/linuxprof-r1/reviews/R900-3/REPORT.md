[R900] POSITIVE - exact head 58f7673b8c57a80230e716bc1774ff9cc2f71ddc

External independent delta review R900-3 of [issue #983](https://github.com/kebag-logic/milan-fpga/issues/983) / [PR #986](https://github.com/kebag-logic/milan-fpga/pull/986). All five lenses are CLEAN. R902-1-F1 is resolved at its cause. Prior wording residues are resolved. No new finding was established. The existing optional robustness suggestion remains optional.

Tree: `6dbb2ebaa80cf656a39b93c10c46e98fa6b92d2a`. Source base: `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. Previous reviewed head: `66b4def34dcbc0d371ce4eb339d3d0226875befa`. One commit changes four files, +252/-88. This is source-head review, not current-dev candidate validation or merge authorization.

## Scope and authorities

Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, frozen issue acceptance and public decisions, requirements/interfaces, full diff/history and the one-commit delta. The independent delta pass preceded consulting prior public review comments. No private author material or management checkout was accessed. [source.diff](source.diff) and [delta.diff](delta.diff) retain both comparisons.

The [manager scope ruling](https://github.com/kebag-logic/ti-sitara-am65x-bsp/issues/29#issuecomment-7096504049) authorizes descriptor-only generation and a host-only (1,1,2) scheduling entry, with unchanged AEM/Milan checks, FPGA validation and artifacts. It does not restore an FPGA operating-system product path. Authorities examined: REQUIREMENTS sections 1/8; NFR-SCOUT-03 and the shape contract in FR_NFR:403; ARCHITECTURE; PP_DESCRIPTOR_OWNERSHIP:27; ENDSTATION_BUILDER sections 3/6; and the executable `shape_costs.listed()` interface. Untouched generator behavior retains its prior disposition; dependencies affected by this delta were checked again.

## Prior findings and dispositions

Public findings: [R900-1](https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7099822461), [R900-2](https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7100511968), [R902-1](https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7101347692). Submitted reviews and inline threads were empty at retrieval. [public-state.json](public-state.json) retains the public snapshot.

| Prior ID | Severity / attributable lenses | Disposition at this head |
|---|---|---|
| R902-1-F1 | BLOCKER / Conformance, RTL, Tests | RESOLVED. The 39-line FPGA chain and reader match base. Budget checks reach base verdicts. Exact prior header bytes kill current gate 41. |
| R900-1-F1 | MINOR / Conformance, Robustness, Tests | Remains RESOLVED. `endstation_builder.py:4802` still uses `_req`; gate 42's three malformed-board regressions pass. The builder blob is unchanged since the previous head. |
| R900-1-F2 | MINOR / Docs | Remains RESOLVED. ENDSTATION_BUILDER:1248 and the source explanation describe the shared widest advertised format at the configured rate. Gate 41 retains 217 rather than 73 octets. |
| R900-1-R1, R900-2-R1, R902-1-R2 | RESIDUE / Docs | RESOLVED in the live PR body: published head is 58f7673b; source evidence and hosted acceptance are separated; checkout no longer says “once pushed”. |
| R902-1-R1 | RESIDUE / Docs | RESOLVED. ENDSTATION_BUILDER:1233 uses H1-H9; row 5d at :1031 references H2. Gates 32/41 pass. |
| R902-1-S1 | SUGGESTION / Tests | IMPLEMENTED. The contract is force-included; the probe prints and asserts MBX_N_IF; FPGA rows are exercised at one/two interfaces. |
| R902-1-S2 | SUGGESTION / Robustness | RETAINED as optional, unchanged base behavior; disposition below. |

**R902-1-S2: SUGGESTION; Robustness.** Artifact: `sw/builder/endstation_builder.py:3834`, `_gptp_clock_accuracy_key`. Authority/evidence: the prior public finding established that a non-integer clock_accuracy such as 'x' raises ValueError on base FPGA and host paths; this function and callers are unchanged by the delta. Impact: callers catching only ConfigError can receive an uncontrolled exception. Optional required outcome: handle malformed values through the validation exception in separately scoped work, alongside the disclosed non-iterable board cases. Verification: valid FPGA/host controls load and invalid values raise ConfigError in both paths. No follow-up issue was created in this read-only review. This suggestion leaves coverage clean.

## Five-lens results

[R900] PASS Conformance - `sw/firmware/ctrl/loop/ctrl_loop.h:360`; `tb/verilator/ctrl_service_budget/shape_costs.py:102`; `focused-gates.log`; `evidence-compare.log` - The frozen shape-table boundary and issue acceptance hold.

The chain from its first FPGA #if through its #error and closing #endif is exactly 39 byte-identical lines at base/head, SHA-256 `f1bbae922af5c477519369c00cc87e4650db3db3fc014646dcad6933347a9d89`. Its four shapes remain (1,2,2), (1,9,9), (2,2,2), (2,9,9). The reader and all of tb/ are untouched. No figure is newly defined outside that chain in ctrl_loop.h.

Repeated gates verify the 5,784-byte host image, Configuration-backed inventory, ADP 1 source/2 sinks, AAF plus CRF inputs, AAF output, stated AVB_INTERFACE dataset, agreeing generators and refusal of gateware generation. Shared AEM/Milan checks remain on their existing path. FPGA identity manifests contain 245 matching entries at base, prior head and current head. This establishes the descriptor-only boundary, not board compliance or host media-clock operation.

[R900] PASS RTL - `ctrl_loop.h:365`; `host/ctrl_loop_host.h:26`; `sw/firmware/ctrl/test/ctrl_plants.py:596`; `object-probe.log` - Compiler selection and firmware/FPGA boundaries are preserved.

The host header is selected before the chain only with CTRL_HOST_PLATFORM at (1,1,2). Its own guard rejects standalone/non-host use and other shapes. Its eight figures remain 950/1010/735/285/85/34/130/35. No repository build input defines the macro. The all-fabric arty_current config happens to have this shape: it takes host figures only when an external build explicitly defines the macro, and remains refused without it.

Placement under host/ is material. ctrl_plants.BASE compiles every loop/*.h in its ordinary non-host header census. An exclusively host header there would break that base. host/ is outside the census and beside the mailbox model.

The published comparison covers 12 preprocessor points, printing actual MBX_N_IF values of 1/2, and six compiling object pairs. I independently compiled all six ctrl_loop.o pairs against base/head headers with strict C warnings: all are byte-identical. No HDL, firmware C implementation, SoC interface, clock/reset/CDC contract or submodule gitlink changes in this PR. No simulator was needed or invoked.

[R900] PASS Robustness - `test_builder.py:30643`, `:30795`, gate 42; `delta-probe.log` - Selection near misses fail closed and prior refusal coverage remains intact.

The independent 20-point preprocessing matrix spans one/two interfaces, five source/sink combinations and both macro states. Only the four listed FPGA shapes or explicit host shape succeed; other shapes report THE SHAPES refusal. Direct inclusion of the host header is rejected. Gate 41 additionally checks host streams at two interfaces, both compiled macro settings, and host figures equal to 1x1/1if. Gate 42 passes 31/31 plants including all three malformed-board regressions. Descriptor-dependent work and host preemption remain unmeasured assumptions, explicitly disclosed by the header.

[R900] PASS Tests - `test_builder.py:30696`, `:30704`, `:30722`, `:30751`; `delta-probe.log`; `prior-reader.log`; budget logs - The regression detects the prior defect and binds text-reader results to compiled rows.

_shapes_reader loads the real unchanged reader. _shapes_as_read requires a readable FPGA-only table and one definition of each figure per row. _check_shapes_text plants the host row inside the chain and host figures beside it. _check_fpga_rows compares compiled values to the reader and macro-enabled build at both interface counts. Force-including the contract and asserting the observed count fixes the earlier -I override weakness.

I redirected current gate 41's header input to an exact disposable copy of 66b4def3's header. The complete gate fails with “shape_costs.py does not read THE SHAPES”, at the original cause. Current header passes. Published receipts additionally kill all five mutants: old placement, figures beside the chain, missing macro guard, always-true macro guard, changed host slice. The unchanged published probe_shape_costs.py, retained as probe_shape_costs_prior.py, independently reads identical rows and at(1)/at(2) at base/head.

| Command / check | Result |
|---|---|
| Gates 32, 41, 42 and test_bad_configs_rejected | 4/4 pass; FPGA keys 116/116; host keys 64; refusals 31/31 |
| shape_costs.py --check | rc 0; output byte-identical to published base/head |
| shape_costs.py --selftest | rc 0; 25/25 controls refused; identical output |
| load_grade.py --check | rc 0; identical output |
| flip_grade.py --check --point 1x1/1if | rc 0; identical output |
| flip_grade.py --check | rc 1; identical output including base's documented 8x8/2if FAIL |
| Independent FPGA object pairs | 6/6 byte-identical |
| Independent shape/macro matrix | 20/20 expected outcomes; direct header misuse refused |

The all-points flip failure is the existing state documented at ctrl_service_budget/README.md:218, separate from the merge gates. It is neither a new regression nor a passing all-points result.

[R900] PASS Docs - `docs/ENDSTATION_BUILDER.md:1031`, `:1193`, `:1275`; `host/ctrl_loop_host.h:4`; PR body; `docs-check.log` - Documentation matches selection, reader behavior, limits and public state.

Section 6 correctly describes the separate header, conditional selection, unchanged reader, interface refusal, host assumptions and key labels. Added comments explain behavior/reason with #983 and introduce no bench labels, reviewer IDs, review-round markers or issue-comment IDs. docs_check reports zero findings over 223 Markdown and 1,912 scrubbed text files. Published docs/quality receipts report 25 passing commands; their hashes verify. Publication residues are corrected while incomplete verification remains disclosed.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #983 and board #29 ruling; ctrl_loop.h:360; shape_costs.py:102; focused-gates.log; evidence-compare.log | R900-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| RTL | CLEAN | delta.diff; ctrl_loop_host.h:26; ctrl_plants.py:596; object-probe.log; integrity-result.json | R900-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| Robustness | CLEAN | test_builder.py:30643 and :30795; delta-probe.log; gate 42; unchanged loader disposition | R900-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| Tests | CLEAN | test_builder.py:30696-30829; focused-gates.log; prior-reader.log; shape/load/flip logs; evidence-compare.log | R900-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |
| Docs | CLEAN | ENDSTATION_BUILDER:1031/1193/1275; ctrl_loop_host.h:4; docs-check.log; public-state.json | R900-3 | 58f7673b8c57a80230e716bc1774ff9cc2f71ddc |

## Evidence limits and pending manager duties

The [published packet](https://github.com/kebag-logic/milan-fpga/tree/ad3798bc641ff3f9d1f3827c5acf6a30fab0ac4b/review-evidence/linuxprof-r1/author-r3) is anchored to immutable commit ad3798bc641ff3f9d1f3827c5acf6a30fab0ac4b. All 87 author-receipt hashes across three revisions match MANIFEST.json; [packet-audit.log](packet-audit.log) records them. **No cryptographic signature is present in that commit or as a signature-named packet file.** This verifies publication hashes, not a signed attestation. Attribution comes from public issue statements and immutable publication.

[evidence-compare.log](evidence-compare.log) recomputes equality of all 245 FPGA manifest entries and checks the published 240-file full-tree receipt. At board commit afc350641dc2d93cee39bb4c62258b6d55f00ccb, the published host-build receipt reports 35/35 identical objects and the same binary across 66b4def3/58f7673b. Loop-object hash: `204afd952f53cfd9a040ddb521d99b2398864ce59df6c95e22c07f80738ef10e`; binary: `1c9240b21ce566a743c010bc33144ea520d292e67f376fdee3486d923270f00a`. Generated headers match; entity.conf and NVM-header differences are revision comments only. I checked these published receipts and independently reproduced FPGA object equality; I did not rebuild the entire board program or repeat the full artifact campaign. Board repinning/integration remain separate duties.

**The 580-second timeout does not block this delta verdict.** Base/head run.py --self-test receipts both end at rc 124, with identical captured progress and no traceback. That resolves the named regression's requirement to grade as at base rather than raise immediately. It does **not** establish a completed or passing self-test at either revision. I did not repeat that long timeout. Before declaring candidate validation complete, the manager must obtain a completed candidate budget self-test verdict with an adequate bound, alongside explicit shape/load/flip checks. Partial progress cannot become PASS.

**No manager source bank ran at this head, and none is inferred.** The earlier author suite covers 114/115 functions at 677d605f, not a complete bank at this head. Gate 1b and firmware shards/mutation campaigns remain outstanding. The manager owns complete builder/native banks and union evidence on the actual current-dev candidate, plus required source-head hosted/act acceptance. Source base 854bd723 differs from the assignment's live dev e275d7950ef3385753e6a15d2e191ba855b171ed; no candidate was constructed here.

The exact-head hosted snapshot shows four queued workflows (rtl-full, elaborate, rtl-fast, docs), none with a conclusion. No executed job or skipped context is credited. Required checks, two independent positive reviews, no review in flight, explicit merge authorization and post-merge containment remain manager duties.

Physical calibration is NOT RUN. Field skips and desk checks are not hardware proof. Host preemption, media-clock consumption, installation, physical timing and release campaigns were not exercised. The stated host scheduling profile does not discharge them.

No full parent/processor/gPTP/Yosys/builder banks, hardware, shared installs, privilege, Docker/act, source fixes, commits, pushes, GitHub writes, author contact or sub-agents were used. Independent light checks ran concurrently in a joined foreground driver, at most four processes; object pairs used two. Disposable files remain under packet scratch/.

One independent probe initially omitted the mailbox include directory and failed before its boundary matrix. The initial log/status and driver result are retained. Adding the required include to the probe produced the final 20/20 result. Production tests/source were unchanged. Published traceback paths are redacted to <PACKET>/<REPO>; result text is unchanged.

[integrity-result.json](integrity-result.json) proves exact HEAD/tree, raw bytes and modes of all 1,937 tracked root blobs, the complete stage-zero index, absence of hidden index flags, and pins/raw bytes/modes/index of all five required initialized submodules. The unused external gitlink remains unchanged/uninitialized. Tracked source was never mutated; restoration was unnecessary. Final status is clean.

## Reproduction and packet

Scripts accept the isolated repository path: packet_audit.py, delta_probe.py, run_focused.py, object_probe.py, integrity_probe.py. evidence_compare.py takes no arguments and compares downloaded receipts with local logs. probe_shape_costs_prior.py REPO REV... is the unchanged published prior probe. run_focused.py joins every check before returning. The initial driver result preserves its setup failure; final-results.json records corrected individual statuses.

MANIFEST.sha256 lists publishable files with packet-relative paths. Verify using sha256sum -c MANIFEST.sha256. Do not publish scratch/.

R900-3 FINISHED
