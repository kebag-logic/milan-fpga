[R848] POSITIVE - exact head d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b

External independent review R848-2 of PR #931, issues #923 and #924. Tree: `c6c0397815848b804297d8fe001d88e722b35f49`. All five lenses are CLEAN. Every named prior MINOR and source-comment RESIDUE is resolved. No new BLOCKER, MAJOR, MINOR or RESIDUE finding. Four prior optional suggestions remain below.

**Scope and independence.** Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, issue bodies and public scope decisions, REQUIREMENTS.md and interface authorities, then the source-base diff/history and public author evidence. The reviewed delta is the four commits in `70c100da..d06ded5a`, within `16ba667d..d06ded5a`. Its five files contain tests, mutation definitions, documentation and planner comments. Untouched implementation retains its prior lens result where dependencies remain unchanged.

The independent verdict and five-lens ledger were written before reading [R848-1](https://github.com/kebag-logic/milan-fpga/pull/931#issuecomment-6928957357) and [R847-1](https://github.com/kebag-logic/milan-fpga/pull/931#issuecomment-6929792570). Their findings were then reconciled at their causes. No other current-round review report or private author material was read.

Authorities include #923's [memory ruling](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6906679024), the [scope correction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6904832963), and the [corrected timing floor](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6930885185). Protocol interpretation follows the frozen public Milan v1.2 5.4.2.7/.27/.28 and 5.3.10.1 obligations, IEEE 1722.1 configuration/stream-info obligations, the mailbox contract and the pinned release interface. Original standards publications were not independently reobtained.

**Prior findings resolved at this head.**

**R848-1-F1; MINOR; Tests, Robustness; RESOLVED.**
Artifacts: `sw/firmware/ctrl/test/test_aecp.cpp:3985,4346,4377,4417`; `sw/firmware/ctrl/test/aecp_map_mutants.py:333`; `sw/firmware/ctrl/aecp/README.md:184`.
Authority/evidence: #923 requires store/GET_AUDIO_MAP agreement; `protocol-processor/hdl/aecp/KL_aecp_engine.sv:465` reserves the transaction at phase 1 and requires phases 5/2 without backpressure. Previously the fixture dropped the write with the reply while its assertions accepted disagreement.
Impact addressed: a green timeout test could hide the original map-divergence class.
Required outcome met: the fixture applies phase 5/2 before returning SILENT; early unanswered beats remain untaken. The existing phase-5/phase-2 cases now call `agree(14)`. New two-record ADD/REMOVE and boot removal/addition cases lose each record's reply in turn and check the counter, map and agreement; commands check SUCCESS. The README excludes delivery loss after commit-begin without inventing rollback.
Verification: both application controls pass. `old-write-drop.log` fails all three late-reply tests on agreement. `stop-at-lost-reply.log` fails both new command/restore tests on agreement. The published `window-lost-reply-stops-the-commit` plant catches both tests by name.

**R847-1-F1; MINOR; Tests; RESOLVED.**
Artifacts: `sw/firmware/ctrl/test/test_aecp.cpp:4396`, `aecp_map_mutants.py:339`, `sw/firmware/ctrl/aecp/aecp_face.c:273`.
Authority/evidence: the callback's selected-record contract and AGENTS.md's discriminating-test rule. Previously every face test used identity selection, so ignoring `pick` passed.
Impact addressed: the face could commit a held mapping instead of a new mapping while tests stayed green.
Required outcome met: ADD {held, fresh} and REMOVE {held, held, fresh} cross the face and EDIT window. The test asserts validation/commit records, COUNT 1/2, map counts, successful responses through `receive`, and agreement after each.
Verification: unplanted arms pass. `ignore-pick.log` fails the new test, including “the records the core picked are committed.” Published receipts also show the original `--only face-pick-ignored` probe red, its control green, and `window-pick-ignored` caught by name.

**R848-1-F2 / R847-1-F2; MINOR; Docs; RESOLVED.**
Artifact: `sw/firmware/ctrl/plat/README.md:111`.
Authority/evidence: published ROM measurements and `docs/design/SPLIT_CONTROL_MEMORY.md:286,564`.
Impact addressed: confusing former spare space with current overflow understated a measurement supporting the ledger exception.
Required outcome met: the sentence now states 1,280 B past the previous allocation.
Verification: `132352 - 131072 = 1280`; `131072 - 130184 = 888` was the former spare space. The ledger is unchanged.

**R848-1-F3 / R847-1-R1; RESIDUE; Docs; RESOLVED.**
Artifact: `sw/litex/ctrl_memory.py:243`.
Authority/evidence: the owner's source-comment rule.
Impact addressed: wording-only lane-label residue.
Required exact fix met: “debt owed to the cold-code-to-flash work” and “until that work lands” replace the two S14 references, retaining issue references and figures.
Verification: direct delta inspection and equal Python syntax trees excluding comments. No behavior changed.

**Retained optional suggestions.** All remain SUGGESTION; none affects lens cleanliness.

- **R847-1-S1; SUGGESTION; Tests.** Artifacts: `tb/verilator/milan_dp/Makefile:1009`, `twin_split.cpp:688`. Evidence: the standing plant cuts the edit port after the first boot; the second boot composes a fresh port. The prior public restore-cut probe failed MAPS-SAVED by name, proving that check can discriminate. Impact: this integration negative control is not permanent, although a unit plant covers the omission. Optional outcome: add a standing restore-cut twin plant. Verification: nominal persistence passes; the plant fails the saved-map/store check. Unchanged.
- **R847-1-S2; SUGGESTION; Tests.** Artifact: `sw/firmware/ctrl/aecp/aecp_maps.c:589` and clipped-reset-set tests. Evidence: the prior public `>= 82u` to `> 82u` probe survived; shipped descriptors are longer. Impact: the minimum-length boundary lacks a discriminating case. Optional outcome: add length 82. Verification: the correct predicate passes and the strict-greater mutation fails. Unchanged; that probe was not rerun here.
- **R847-1-S3; SUGGESTION; Tests.** Artifact: `tb/verilator/milan_dp/twin_split.cpp:633`. Evidence: twin-maps uses 1x1 STREAM_PORT_INPUT 0; output edits have face-model coverage but this scenario does not exercise the RTL output reservation path. Impact: limited integration coverage. Optional outcome: add an output-port case. Verification: assert output-store agreement with a named negative control. Unchanged.
- **R847-1-S4; SUGGESTION; Robustness.** Artifacts: `sw/firmware/ctrl/aecp/aecp_face.c:261,309`, pinned engine interface at line 465. Evidence: late silence increments a counter and the reserved edit proceeds; the interface forbids backpressure then. Impact: a future delivery stall would require a changed guarantee. Optional outcome: expose/assert the counter when extending that integration. Verification: any future delivery-loss support needs explicit recovery/containment tests. The new README clarifies the existing boundary; no further diagnostic was added. No current product delivery-loss defect is established.

**Results by lens.**

[R848] PASS Conformance - `protocol-processor/hdl/aecp/KL_aecp_engine.sv:465`, `docs/reference/MAILBOX_CONTRACT.md:369,718`, `sw/firmware/ctrl/aecp/README.md:184`, `test_aecp.cpp:4377,4396,4417` - Checked the revised fixture against the reserved transaction and #923 agreement contracts. Nonidentity selection crosses the real face/window adapter. No production command or #924 status/length behavior changed; both application arms pass the configuration and 48-byte request/84-byte response cases. Prior conformance coverage of unchanged production code remains valid.

[R848] PASS RTL - `hdl/milan/milan_datapath.sv:4801,4816,5133,5185`, engine interface, `checkout-audit.txt`, public image receipts - The store's boot-only wait, phase-5 writes and finish behavior support the revised fixture. No RTL, mailbox contract, constraint or submodule pin changed. Planner syntax-tree equality proves its delta is comments only. Unchanged product inputs preserve the prior CDC/reset/width and route review.

[R848] PASS Robustness - `test_aecp.cpp:4346,4377,4396,4417`; `old-write-drop.log`, `stop-at-lost-reply.log` - Applied early-timeout, lost-first/lost-second reply, finish-reply loss, boot removal/addition, duplicate and held/new mapping cases. Every exercised supported late case asserts agreement. Suppressing a write cannot pass as a complete edit. Arbitrary delivery-loss recovery remains outside the documented contract.

[R848] PASS Tests - `aecp_map_mutants.py:333,339`, `test_aecp.cpp:4396`, `probe-summary.json`, published workflow/twin/sweep receipts - Both application arms pass 164 tests independently. Three negative controls have nonzero suite exits and the required assertion failures. These close the two gaps by demonstrating discrimination, beyond branch coverage. The published standing plants and original pick probe agree.

[R848] PASS Docs - `sw/firmware/ctrl/aecp/README.md:184`, `sw/firmware/ctrl/plat/README.md:111`, `sw/litex/ctrl_memory.py:243`, `docs/design/SPLIT_CONTROL_MEMORY.md:286,564`, public decisions and evidence - The guarantee, excluded delivery-loss boundary, numerical debt and comment wording agree with their authorities. The corrected timing floor supersedes the old hold-miss interpretation.

**Independent execution.**

Run `python3 -B run_probes.py <checkout>`. Three foreground-supervised workers use four compile jobs each, at most twelve in total. Disposable builds/copies are under this packet's `scratch/`. Mutant suite exits are distinct from the probe verdict: each expected failing suite exits 1; the driver exits 0 only after matching its named failures.

| Probe | Result | Raw receipt |
|---|---|---|
| Application, one interface | 164 tests, zero failures | app-if1.log / app-if1.rc |
| Application, two interfaces | 164 tests, zero failures | app-if2.log / app-if2.rc |
| Old write-dropping fixture | All three late-reply agreement tests fail | old-write-drop.log / old-write-drop.rc |
| Stop after lost reply | Both new command/restore agreement tests fail | stop-at-lost-reply.log / stop-at-lost-reply.rc |
| Ignore selection | New selection test fails | ignore-pick.log / ignore-pick.rc |

**Published evidence and carry-forward.**

Source: [archive 43bf7e3e](https://github.com/kebag-logic/milan-fpga/tree/43bf7e3e6fe2065df264dbf23256381436f7eed6/review-evidence/923-r1), author-r1/r2/r3, and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6931638262). `verify_packet.py` verifies all 151 author files against their published SHA-256 values, including 13 redacted publications. The archive commit has no signature header: this establishes content integrity, not independently authenticated cryptographic signing. Selected receipts retain author-relative paths under `public-evidence/`.

`receipt-audit.txt` independently counts 118 rc-0 steps and 130 NOT RUN entries in the published workflow table; no nonzero executed step. The companion author receipt reports AECP 331/331, SRP 421/421, control 716/716 and coverage PASS on 39 files. The table references job logs but does not contain the full raw job-log bank. These are author source-head receipts, not a manager source bank. Full campaigns/coverage were not independently rerun.

The four prior sweep receipts total 65 passing suites and 2,713,040 checks, with zero failed or timed-out suites. The prior twin receipt records 20 passing checks and three named edit-cut failures. Product-source identity and the published image chains support retaining those RTL results, CPU-budget results and routes while the changed firmware tests were rerun.

Published image hashes match the prior-head/routed receipts:
- 1x1/1if platform `ctrl_app.elf`: `caec0abc5d730cbeeb4c82a628406ed51161a2ccb783523afc90d20004c0587d`.
- 8x8/1if platform `ctrl_app.elf`: `59b9b736f410e2b2de2f8e7bd27d21f3ee16870081c778fa296e6cf3149c84cd`.
- 1x1 release `bios.bin`: `860d4771decf5b92bd167e57c690892d665eec8075902a3468b68e3b3f56041f`.
- 8x8 release `bios.bin`: `d8851b6d470e811cfd1c95b3aa3a6d3e9c367f3e1fddaac38270d484291aea99`.

Init-byte equality, Verilog equality outside comments and equivalent constraint ordering are published author evidence. Image bytes were not rebuilt or independently rehashed here. Prior record-class receipts retain the measured costs and reported-only 8x8/1if rows; those overruns and seven inherited backlog-owed rows are not silently represented as every bound passing.

Timing uses #818's corrected **+0.030 ns setup and 0 ns hold** floor. The 1x1/1if +0.014/+0.015-ns hold measurements pass; the old “owed to #927” hold-miss interpretation is superseded. Inspected ExtraPostPlacementOpt signoffs give worst-corner 1x1 +0.256/+0.015 ns and 8x8 +0.295/+0.036 ns. No new timing finding.

**Reviewer-owned ledger.** CLEAN denotes source-review coverage within the stated limits, not merge authorization. R848-2 applies every changed scope and verifies the basis for retaining R848-1's unchanged scope.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #923/#924; engine:465; EDIT ABI; aecp README; command/restore/selection tests and application receipts | R848-2 | d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b |
| RTL | CLEAN | milan_datapath.sv:4801,5133,5185; engine:465; checkout-audit.txt; public image/route receipts; unchanged pins | R848-2 | d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b |
| Robustness | CLEAN | test_aecp.cpp:4346,4377,4396,4417; old-write-drop.log; stop-at-lost-reply.log; S4 optional | R848-2 | d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b |
| Tests | CLEAN | aecp_map_mutants.py:333,339; five independent probe receipts; public workflow/twin/sweep evidence; S1-S3 optional | R848-2 | d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b |
| Docs | CLEAN | aecp/README.md:184; plat/README.md:111; ctrl_memory.py:243; SPLIT_CONTROL_MEMORY.md:286,564; scope and packet receipts | R848-2 | d06ded5ad3d6eb26bfd79787260adcdcc7d3f80b |

**Real limits and pending manager duties.**

No full parent/processor/builder/synthesis banks, simulator runs, routes, hardware operations, shared installs, source fixes, commits, pushes, GitHub writes, author contact or delegated work were performed. No manager source bank exists at this exact head and none is inferred. Hosted/act acceptance was not independently checked here and remains the manager's responsibility; skipped contexts are not executed jobs. Physical calibration was NOT RUN; field skips and simulation are not hardware proof. Known #926 and #929 retain their assigned scope treatment.

The manager owns publication, reconciliation with the other independent review, exact-head hosted/local acceptance, and the final current-dev candidate's builder/native banks and receipts. Source base `16ba667d` is not candidate validation against live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` or its later tip. Bench acceptance of #923/#924 remains due: mapping-dependent format refusal/acceptance, persistence and actual rendered audio. Merge requires explicit maintainer authorization and post-merge containment before closure/Done.

`audit_checkout.py` checks actual tracked bytes, file kinds/executable modes, stage-zero indexes and required submodule pins, including lwSRP. Its final receipt is clean. The optional uninitialized external gitlink is retained in the root tree/index check. `MANIFEST.sha256` lists the publication set; disposable `scratch/` trees are excluded.

R848-2 FINISHED
