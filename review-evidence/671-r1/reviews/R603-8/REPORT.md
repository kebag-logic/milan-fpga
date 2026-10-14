[R603] POSITIVE - exact head d5cd863561ba1ee7bc6342fb1b00f57dd786bd97

External independent review, issue #671 / PR #715, round R603-8.
Tree: `029737bc62cb0fc1bbf45e3aed82a39160ee41da`.
Source base: `e8454e2751d05b02ee8e5a571857589ab358ab86`.
Reviewed delta: `9b32002cc0c3aafae9e864af7b4f08c1089a188a..d5cd863561ba1ee7bc6342fb1b00f57dd786bd97`.
Merged dev: `fa8209889411e8ca95757174c981f720dbcd95a2`.

All five lenses are CLEAN for the authorized delta. No new BLOCKER, MAJOR or MINOR was found. Earlier substantive findings remain resolved. Two previously filed RESIDUE items and two optional SUGGESTIONs remain, dispositioned below. This is a source-review verdict, not merge authorization or final workflow acceptance.

**Scope and independent reconstruction**

I read the operating contract, CONTRIBUTING.md and documentation index; the issue's frozen acceptance and public scope decisions; linked saved-state authorities; the source-base diff and history; then public executable evidence. `independent-verdict.md` records my verdict and five-lens ledger before consulting prior public review findings. No private author material, management workspace, or another current-round report was used. Formal and inline review endpoints supplied no additional findings.

The controlling assignment is [round 8, comment 6161596895](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895): merge dev, rerun affected gates, remeasure affected quantities, and make no other change. Authorities examined include the [issue](https://github.com/kebag-logic/milan-fpga/issues/671), REQUIREMENTS.md sections 1/8, FASTCONNECT sections 6.2/7, MATERIALIZATION section 6.3, SNAPSHOT_OWNERSHIP sections 7/18, the [authority decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5997929153), [read-agreement decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999350068), and [capture decision](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112).

Earlier round-7 reviews stand for untouched behavior. I independently applied every lens to this merge and receipt delta and checked prior coverage through exact path identities. This is not a new design review of every feature imported from dev.

**Merge and change boundaries**

`audit_delta.py`, `delta-integrity.log` and `integrity-final.log` establish:

- `f3bb2014d065141930ae1a473c966b419d1040aa` has exactly two ordered parents: round-7 head `9b32002c` and dev `fa820988`. Their merge base is `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
- `git merge-tree --write-tree` succeeds without conflict and produces exactly the published merge tree, `7a2041b6a0b7ea13c019a3b5be08f0eb3555f8ac`. There is no hand-resolved tree difference.
- Exactly 15 lane-owned paths differ from dev. At the merge, every blob and mode equals its round-7 entry. This includes production firmware, host model, generated fault campaign, restart support, builder test, co-simulation driver and lane documentation.
- The complete 160-path merge delta equals dev's delta since `c6bd08c6`, including preimages and postimages. All other paths equal dev.
- The only gitlink change is dev's addition of `third_party/tsn-c-stack` at `70936b77dc41981e192438388cd0aced69954f18`. Processor and stream-library pins are unchanged.
- The final commit changes only `tb/verilator/nvm_capture_cpu/measurements.json` and section 18 of `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`. Text outside section 18 is identical. Receipt changes are confined to `date`, `base`, `tree`, `remeasurement_assignment` and `provenance`.

No lane firmware, test, register, record-format, A/B write-path or processor change was introduced. The staged read, three-attempt judgement/re-stage, validated-only generation, fallback and cold/restart hold remain intact at `milan_baremetal.c:740-839,1547-1560,1601-1613,1669-1760`. Earlier acceptance 1-3 coverage remains applicable.

**Capture and retained measurements**

I audited the author's public executable receipts at the specified [evidence commit](https://github.com/kebag-logic/milan-fpga/tree/10d91cdbd763f66c41fc87f3356d516a5610e746/review-evidence/671-r1/author-r8/receipts/r8). Each downloaded blob was checked against its Git object ID; `public-provenance.json` records paths and hashes.

Remeasurement was justified. Every one of the six public compilation commands contains seven dev-changed capture inputs: `hdl/ieee1722/aaf/KL_aaf_packetizer.sv`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`, `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv`, `hdl/ieee1722/crf/KL_crf_rx.sv`, `hdl/ieee1722/maap/KL_maap.sv`, and `hdl/milan/milan_datapath.sv`. The fresh six-arm execution addresses this dependency; a passing compiler-free receipt gate alone would not establish unchanged RTL timing.

`audit_public_capture.py` verifies that each per-arm summary appears in its successful run log and equals the committed summary and rows. All six logs identify the recorded 5.052 simulator release. The superseded interrupted 5.050 attempt is excluded. All **96 captures** repeat round 7's complete rows, including cycles, census, ownership, mismatches and traffic counts.

Firmware, harness, configuration and recorded processor identities match the reviewed tree. Every recorded CPU-netlist, instrumented-firmware, BIOS and microcode hash equals round 7. The public product comparison reports generated-header equality after timestamp/build-directory normalization; this is not literal timestamp equality.

| Point | Maximum over ON/OFF | Interpretation |
|---|---:|---|
| 1x1, 50 MHz CPU / 100 MHz system | 3.96548 ms | Contract; 12.3566 floor ratio |
| 8x8, 50 MHz CPU / 100 MHz system | 13.86328 ms | Contract; 10.63672 ms below 24.5 ms; 3.5345 floor ratio |
| 8x8, 100 MHz CPU / 100 MHz system | 10.42973 ms | Non-contract comparison |

The receipt binds measured commit `f3bb2014`, its exact tree, and firmware SHA-256 `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`. The final commit changes no measurement input. Section 18's identities and figures agree. Public `assemble.log`, `refresh.log` and `GATES.json` record generator invocation and successful assembly/refresh. The original round-8 assembler/refresher source files are absent from the pinned public packet; I verified their resulting data and limited text changes independently rather than claiming to rerun those generators.

Carry-forward claims remain justified within these limits:

- **Firmware size:** source and relevant capture build inputs are unchanged. Fresh public compilation against merged capture headers gives text 14,473 to 16,523 bytes and bss 68 to 84: again +2,050 text and +16 bss. Earlier product-header absolutes, 17,579 text and 104 bss, use a different recipe. They are not the absolute sizes measured by this capture-header build.
- **Boot read cost:** firmware, capture/service harnesses, CPU/BIOS identities, flash model/controller inputs and clocks remain unchanged. Dev's control-memory addition is opt-in; neither harness selects it (`nvm_capture_cpu/soc.py:139-160`, `sw/litex/milan_soc.py`). Cycle-exact capture repetition corroborates these simulated scenarios. The 16.4/17.1 s boot figures remain estimates assembled from measured component costs, not newly measured boot times or universal latency guarantees.
- **Backend area:** `hdl/milan/KL_nvm_backend.sv` is unchanged. Its isolated synthesis rows retain their original scope and establish no new whole-design placement result.
- **Writer runtime:** the suite and firmware are byte-identical. The public source selftest passes in 271.15 s at the merge; prior hosted runtime is still only an estimate for future runners. The builder timeout remains 1,200 s.

**Checks performed and evidence attribution**

Independent checks overlapped in a foreground driver with at most four workers. No job was left running. No full capture, builder, parent, processor, time-synchronization or synthesis bank was executed by this reviewer.

| Reviewer execution | Result | Receipt |
|---|---|---|
| Exact merge, path/mode equality, receipt comparison, full tracked-byte/index audit | PASS, rc 0 | `delta-integrity.log`, `integrity-final.log` |
| `python3 scripts/check_nvm_capture.py` | PASS, rc 0 | `capture.log`, `.rc` |
| Five `--mutation` arms: bytes, records, clock, ignore-off-timing, receipt-opt-out | Each rc 1 for its intended reason | `capture-*.log`, corresponding `.rc` |
| `python3 scripts/ci_scope.py --selftest` | PASS, rc 0 | `ci-scope.log`, `.rc` |
| `python3 scripts/ci_events.py --check` | PASS, 2,174 contract items | `ci-events.log`, `.rc` |
| Public capture/provenance audit | Six arms/96 rows agree; 28 selected logs match published SHA-256 | `public-capture-audit.log`, `.rc` |
| `python3 -B scripts/docs_check.py` | 0 findings; 206 Markdown, 1,292 text files; controls 23/23 and 4/4 | `docs.log`, `.rc` |
| `python3 -B scripts/check_doc_style.py` | PASS, 22 documents | `doc-style.log`, `.rc` |
| `git diff --check e8454e27..HEAD` | No diagnostics | `diff-check.log` |

The capture gate executes the slower-OFF maximum fixture, exact half-floor boundary and one-tick-over refusal. Its opt-out control rejects a receipt arm claiming a mutation to escape the production bound. These tests validate the new receipt, without replacing timing execution.

Source-head execution evidence belongs to the **author**, not the manager. I examined public records/raw receipts for the five-shape writer campaign (3,550 cases per shape, 61 firmware plants, nine comparison-check arms), term census/matrix/views, 54 full-control comparisons, co-simulation 465/465 with 39/39 controls, service budget, and six builder partitions covering 103 functions. The merge-to-final delta changes none of their executable inputs. Two builder omissions remain explicit: an ineffective `MAKEFLAGS += -e` control on that implementation, and gate 11's absent physical implementation calibration report. Neither counts as executed proof.

I did **not** execute `act_ci.py` or its selftest on the host. Both final-head selftest layouts were audited from public author records and logs ending `selftest: PASS`. Their commands specify the disposable read-only, networkless boundary. This is author execution, not independent local-workflow acceptance.

**Prior public findings at this head**

After recording my independent verdict, I read and reconciled all prior public findings. `prior-findings-index.json` identifies the 14 earlier review comments. Formal and inline review responses were empty.

| Prior IDs | Disposition | Evidence at this head |
|---|---|---|
| R603-4-F1, MAJOR, all five lenses | RESOLVED, retained | Prefix CRC plus separate trailer comparison at `milan_baremetal.c:768-779`; trailer-inclusive plant rejected on three shapes in the public selftest. |
| R602-5-F1 / R603-5-F1, MAJOR, Tests/Robustness | RESOLVED, retained | Four terms at `read_fault_cases.py:24-27`, each with a class/control; public matrix preserves 32 own-class catches per term/shape and views preserve 384 isolated cases. Files equal round 7. |
| R603-1-F1; R603-2-F1 / R602-2-F1; R603-3-F1 / R602-3-F1 | RESOLVED, original lens attributions retained | Body/both-valid/fallback, restart hold, exact read counts and re-stage bounds remain covered; corresponding plants fail in `public/host-selftest.log`. |
| R603-1-F2 / R602-1-F1; R602-3-F2 | RESOLVED, retained | Long-slot cost is explicitly estimated; PR body distinguishes historical base reproduction. No executable delta invalidates the corrections. |
| R603-1-S1 to S3 and R1; R602-1-S1 to S3 and R1 to R4; R603-2-S1/S2/R1; R602-2-S1/R1; R603-3-S1; R602-3-S1 | RESOLVED, retained | Byte-identical firmware/docs retain operator-wipe exception, actual retire/hold causes, other-slot re-stage identity, read bound, restart hold and publication explanation. |
| R602-6-R1; R602-7-R1 | RETAINED, RESIDUE, Docs | Exact dispositions below. |
| R602-4-S1; R602-4-S2 | RETAINED, optional SUGGESTION | Exact dispositions below. |
| R603-2-OBS-1 / R602-2-S2 | RETAINED OUTSIDE APPROVED SCOPE | Runtime prefill remains #717. Neither it nor the sibling-store comparison defect is claimed fixed by this lane. |

**Retained finding details**

**R602-6-R1 | RESIDUE | Docs | `sw/firmware/nvm_hosttest/README.md:165-168`.** Authority/evidence: the parenthetical lists blank-other sequences while the correct main clause covers every group and 32 cases. Both-valid cases exist in code and receipts. Impact: incomplete examples only; no figure, test, verdict, measurement or conformance change. Exact required wording: replace the parenthetical with `(1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF with the other slot blank, and 0x5A5A5 and the wrap with both slots valid, the newer or the older one faulted)`. Verification: compare against `term_class`/`GROUPS` and pass documentation checks. Carry to the residue checklist; Docs stays CLEAN.

**R602-7-R1 | RESIDUE | Docs | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1635-1642`.** Authority/evidence: linked assignments and identities are correct, but multiple historical receipts still use “the previous one.” Round 8 adjusts the leading chain without eliminating that older ambiguity. Impact: relative prose only; no figure, receipt identity, measurement or clause claim changes. Exact fix on corresponding lines: `required the round-5 receipt`; `required the round-4 receipt`; `required the round-3 receipt`; `required the round-2 receipt, for the console report of the writer's hold`; `required the first #671 receipt, for the boot read-fault rule`. Verification: each link names its receipt explicitly and documentation checks pass. Carry to the residue checklist; Docs stays CLEAN.

**R602-4-S1 | SUGGESTION | Tests | `sw/firmware/nvm_hosttest/test_nvm_firmware.py:774`, check 13.** Authority/evidence: `read faults=` is not graded numerically; exact-read, hold and data assertions remain. Impact: count-only diagnostic regressions could escape. Optional outcome: grade the documented floor count independently. Verification: a count-only mutation fails its diagnostic assertion. Unchanged and optional.

**R602-4-S2 | SUGGESTION | Tests, Robustness | `sw/firmware/nvm_hosttest/read_fault_cases.py`, generated cases.** Authority/evidence: scenarios fault one slot per boot, not both simultaneously. Impact: simultaneous corruption combinations are outside the matrix. Optional outcome: add bounded two-slot cases preserving existing assertions. Verification: show expected hold/recovery and named failing controls. Unchanged and optional.

**Lens results and reviewer-owned ledger**

[R603] PASS Conformance - issue/assignment; FASTCONNECT 6.2/7; `milan_baremetal.c:740-839,1601-1760`; `delta-integrity.log` - authorized merge/re-measure scope is met and prior authority/sequence/A/B behavior is unchanged.

[R603] PASS RTL - merge tree `7a2041b6`; `KL_nvm_backend.sv`; seven capture inputs in `public-capture-audit.log`; optional memory changes in `milan_soc.py` and capture instantiation at `soc.py:139-160` - imported RTL/gitlinks equal dev; affected capture inputs were remeasured; retained area/latency arguments preserve their limits.

[R603] PASS Robustness - `check_nvm_capture.py:58-167`; `capture-*.log`; unchanged fault campaign and judgement/re-stage/hold code; public term receipts - both traffic arms, bound boundaries and opt-out attempts are graded, and earlier fault/hold protections remain covered.

[R603] PASS Tests - `focused-results.json`, `public-capture-audit.log`, public source gate records, host/term/co-simulation logs and final disposable runner selftests - focused checks pass and public execution supports the source head without inventing manager evidence.

[R603] PASS Docs - snapshot-ownership section 18, receipt, public generator output logs, PR body and `docs.log` - identities/figures agree; boot estimates, normalized header comparison, physical limits and retained wording residues are explicit.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue/assignment; FASTCONNECT 6.2/7; firmware read/hold; merge audit | R603-8 delta; R603-7 retained for unchanged behavior | d5cd863561ba1ee7bc6342fb1b00f57dd786bd97 |
| RTL | CLEAN | Merge tree; seven capture inputs; backend; processor pins; optional memory placement | R603-8 delta; R603-7 retained for unchanged lane interfaces | d5cd863561ba1ee7bc6342fb1b00f57dd786bd97 |
| Robustness | CLEAN | Capture bound/mutations; unchanged read/fallback/hold; public term/campaign evidence | R603-8 delta; R603-7 retained for unchanged campaign | d5cd863561ba1ee7bc6342fb1b00f57dd786bd97 |
| Tests | CLEAN | Focused checks; six public capture runs; source receipts; CI checks | R603-8 delta | d5cd863561ba1ee7bc6342fb1b00f57dd786bd97 |
| Docs | CLEAN, two retained residues | Section 18; receipt; PR; public evidence; documentation checks | R603-8 delta | d5cd863561ba1ee7bc6342fb1b00f57dd786bd97 |

Retained round-7 coverage is at `9b32002cc0c3aafae9e864af7b4f08c1089a188a`. Exact artifact identity, not ancestry alone, proves its continued applicability. The ledger does not claim a new independent design review of all 160 imported dev paths.

**Hosted observation, limits and manager duties**

I read exact-head check runs and job steps at **2026-10-14 09:24:45 UTC**, recorded in `hosted-snapshot.json` and `.log`: nine completed successes, twelve jobs in progress, four queued, one skipped physical context. No failed check was present then.

Successes were `changes`, `full-ci-gate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `firmware-aecp-mutants`, and Yosys shards 1/4 and 2/4. Other exhaustive shards and fast jobs were pending/running. Required `docs-check` and `elaborate` were running; final `rtl-fast`, `verilator-suites` and `yosys-portability` aggregate verdicts were not yet present. Within `docs-check`, builder was running and hosted capture, writer and runner-contract steps remained pending. Pending steps are not passes. The physical gPTP context was skipped and supplies no hardware evidence.

Physical calibration was **NOT RUN**. Field skips, simulated timing and host fault injection do not establish physical DDR ordering, hardware timing, cold-cut release acceptance or fault frequency. Identical wrong read views and accepted address substitutions retain the documented detection limits. Constructed CRC collisions test comparison sensitivity, not prevalence. Full capture timing and original generator execution were audited from public receipts, not rerun locally.

No manager source bank ran at this head and none is inferred. No hardware, shared installation, privilege, local workflow orchestration, source fix, commit, push, GitHub write or merge was performed. The focused work needed no simulator executable.

The manager still owns exact-head hosted/local-workflow acceptance, the second independent verdict and ledger reconciliation, both residue checklist entries, and the final **current-dev candidate** build with builder/native banks and linked receipts at the merge turn. The source base and merged dev parent do not replace final candidate validation if dev moves. Explicit maintainer merge authorization, no reviews in flight, post-merge containment/integrity, issue closure and project completion remain required.

Final integrity verification hashes all 1,316 tracked superproject blobs and checks file kinds, executable modes and the complete index. It also checks required initialized submodules, their pins, tracked blobs, modes and indexes: protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, time-synchronization processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, stream library `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, and control stack `70936b77dc41981e192438388cd0aced69954f18`. All passed. `status-final.log` is empty; no tracked bytes required restoration.

Portable entry points, from the candidate checkout: `python3 PACKET/audit_delta.py`, `python3 PACKET/run_focused.py`, `python3 PACKET/fetch_evidence.py`, `python3 PACKET/audit_public_capture.py`, and `python3 PACKET/hosted_snapshot.py`. Scripts locate the packet relative to themselves. Only REPORT.md and files in MANIFEST.sha256 are designated for publication; scratch is excluded. All executions have finished.

R603-8 FINISHED
