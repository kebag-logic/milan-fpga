[R702] NEGATIVE - exact head 44d95625bde2c46d7070c090fc29ed0ba85ab64a

External independent review R702-3, issue #665 / PR #795. Tree: `2b5b52bb8d0c1b43d8ce9ef24684d3a5374acde3`. All five lenses were applied. One MAJOR and one MINOR remain open, plus non-blocking wording residue. The principal defect is a successful AECP response promising a setting that the mailbox has not written.

## Scope and authority

Reconstructed in the requested order from `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, the public issue/assignment/rulings, requirements and interface authorities, then the diff/history and public execution evidence. Reviewed all 15 commits in `e76a755afc0536453161e3cd33f6f4d2dcd7641f..44d95625bde2c46d7070c090fc29ed0ba85ab64a`. This is the first published review of PR #795, although the executor and assignment carry round 3; no earlier clean reviewer result was available to bank.

Authorities include `REQUIREMENTS.md:25`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:55`, `docs/reference/FR_NFR.md:330`, the mailbox YAML/generated contract/design, and the memory ledger. Public decisions: [assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409739310), [port/exclusion ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6410169666), [permanent all-fabric placement](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6410301079), and [single-point memory exception](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6412739248). Their relevant text is retained in `scope-comments.json`.

After the independent implementation pass, examined the [published receipt tree](https://github.com/kebag-logic/milan-fpga/tree/50eb576c296d80307eac7c3064129440642d823d/review-evidence/665s1-r1), PR body and [source review-ready evidence](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6416542628). No private author handoff, private management material or other reviewer's report informed this verdict or ledger.

## Findings

### R702-3-F1 — MAJOR — Conformance, Robustness, Tests, Docs

**Artifacts:** `sw/firmware/ctrl/aecp/aecp_face.c:77` (`publish`, particularly the early return and acknowledgement failure handling); `sw/firmware/ctrl/test/test_aecp.cpp:1968`; `docs/design/MAILBOX_SPLIT.md:1230`; `sw/firmware/ctrl/aecp/aecp_face.h:5`.

**Authority/evidence:** The assignment requires each F value before the response promising it. The ruling requires an acknowledged commit before that response. `docs/ARCHITECTURE_HW_SW_SPLIT.md:55` requires state-apply acknowledgements to precede responses, with Milan v1.2 5.4.5.2 and IEEE 1722.1-2021 7.5.2 governing the ordering. `publish()` returns normally when the interface is busy or owed, without writing the new value. A failed acknowledgement wait only increments `late` and sets `owed`. The void `changed` callback lets the successful response proceed.

`probe_ack.py` exercises the real AECP adapter and mailbox model at two interfaces with unmodified firmware. Suppress acknowledgements, SET IDENTIFY to 255, then SET IDENTIFY to 0 while the first commit remains held. The second command succeeds while the mailbox retains 255:

```text
response_status=0 core_identify=0 mailbox_identify=255
commits_before=4 commits_after=4 busy=1 owed=1
```

`ack-probe.log` records the independent failing assertion, `successful response must not promise an unwritten F value`. The existing happy-path ordering test and `ALateCommitIsOwedAndPublishedAgainWhole` both pass in that same binary. The latter accepts success during the held commit and checks eventual replay; it does not check the required response ordering. The description that the value is acknowledged before return is false on this path.

**Impact:** The controller receives success while the datapath retains the preceding setting. Further commands can be coalesced into owed state without their promised intermediate values reaching the mailbox. Eventual replay cannot repair an already-transmitted ordering violation. This mechanism also publishes configuration, formats, offsets and lock state. Initial open ignores an owed publication too (`ctrl_app_aecp.c:236`) and needs the same lifecycle consideration.

**Required outcome:** Preserve bounded service while withholding success or notifications promising unapplied state. Busy/failed commits must propagate into the command/open lifecycle through a defined defer or failure path; replay alone is insufficient. Required initial publication must be acknowledged before opening. Correct the implementation description to match the resulting failure behavior.

**Verification:** `python3 probe_ack.py CHECKOUT` reproduces the defect; at this head the script exits 0 only after observing the expected assertion failure. The corrected firmware must make that assertion pass. Add permanent coverage for delayed/missing acknowledgement, a second state-changing command while busy, recovery, initial open and lock expiry, including both interfaces. Keep normal ordering and bounded-service checks. This is a firmware-consumer defect: the RTL correctly holds the preceding values.

### R702-3-F2 — MINOR — Docs

**Artifacts:** `sw/mailbox/mailbox.yaml:510`, emitted into `hdl/milan/mailbox/KL_mbx_pkg.sv:409`, `sw/firmware/ctrl/mbx/mbx_contract.h:408`, and `docs/reference/MAILBOX_CONTRACT.md:333`.

**Authority/evidence:** The owner's source-comment rule forbids lane names in new source comments. The new description says `the firmware's F1 store`; regeneration copies that lane name into generated source comments. This is classified conservatively as MINOR because the canonical fix changes committed generated artifacts, which the supplied RESIDUE definition excludes.

**Impact:** Generated interface commentary carries a workflow lane identifier instead of the durable component name.

**Required outcome:** Replace `the firmware's F1 store` with `the firmware's saved-state store` in the YAML description and regenerate the outputs. Change no field, layout, version or behavioral statement.

**Verification:** `python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest`; inspect the generated diff for that exact wording replacement only.

### R702-3-R1 — RESIDUE — Docs

New comments/docstrings contain issue-comment IDs and bench-check labels. The complete artifact list and exact fixes are appended under "Wording residue". These comment-only edits do not change behavior, measurements, clause claims or test verdicts and do not leave a lens unclean. No optional SUGGESTION is raised.

## Independent checks and public evidence

| Check | Result and examined artifacts |
|---|---|
| Port census | Independently reran `publication_census.py --check --selftest --jobs 4`: six shapes, 217 ports each, C 25 / F 28 / R 34 / E 6 / M 14 / G 110; 138 arms pass and all 43 rule removals are detected. `census_ports.py:85` lists the three permitted terminal groups, `:104` names the map-writer nets, and `:46` records the placement-switch acceptance item. Receipts: `census.log`, `census.json`. |
| Independent source plants | `probe_census.py` adds a real wrapper input and separately routes `host_rdata_o` via `pp_rdata_w[0]` to `crf_tx.vlan_en_i`. Both disposable elaborations are refused for the intended reason. `census-source-probes.log`. |
| Additivity/regeneration | Parsed the old YAML as a subset of the new: the only existing scalar change is minor 2→3; four event types and the face/counter-change sections are added. `additivity.json`. Generator check, crosscheck and selftest pass; all four generated outputs equal regeneration. `generator.log`. |
| RTL/window/event behavior | Read `mailbox_face.py:257` through commit/window/output logic, generated `KL_mbx.sv`, and `KL_mbx_evt.sv:318` through pending/seen/count updates. Checked held-value refusal, tags, bounded timeout, reset, partial strobes, window holes, interface isolation and coalescing against `suite_face.hpp` and the plants. Concurrent posting/change keeps new work pending. |
| Mailbox execution | Independently ran both adapters at one/two interfaces and the two-interface model: 523 / 568 / 530 / 575 / 488 checks, zero failures (`mbx-suite-retry.log`). All 199 RTL mutants are caught with passing controls (`mbx-mutants.log`). Initial disposable-suite setup lacked the relative common header; corrected the copy and reran without changing tracked sources. |
| CDC boundary | `mailbox.yaml:72`, `:440` and generated ports specify qualified transfers and approved primitives; `milan_soc.py:2645` leaves outputs unread and inputs idle. No new active sys↔milan_cd connection exists here to claim tested. The placement switch owes actual crossing implementation; this review certifies neither future wiring nor physical CDC behavior. |
| Firmware/notifications | Read `aecp_face.c`, `mbx.c:281`, `aecp_commands.c:455`, `aecp.c:425`, and `ctrl_app_aecp.c:141`. Lock/unlock and expiry invoke `AECP_CHANGE_LOCK`. COUNTERS_CHANGED drives pending GET_COUNTERS; existing `counter_at = departure_ms + 1000` and awaiting-completion guards enforce notification spacing. F1 above disproves failure-path publication ordering. |
| Coverage/source gates | Verified published final firmware shards, 528/528 general mutants, 96 AECP mutants and 31-file 100% coverage receipt. `aecp_face.c`: 166/166 lines, 144/144 branches. No new coverage exclusion appears in the delta. Existing exclusions still apply to the overall reported percentages. `published-gate-summary.txt`. |
| All-fabric/VERSION | Independently re-exported all five shipped configs at base/exact head, without synthesis or software compilation. Each pair's 21 non-log generated files matches after documented stamp/hierarchy-comment normalization; six raw files differ only in those permitted ways. Every digest is in `export-digests.json`. Arty uses the documented 100 MHz comparison recipe. This proves the cited normalized export method, not literal equality of timestamp-bearing files. Datapath, VERSION source (`0x0002_0060`), non-mailbox register map, `.github/` and CI generator are unchanged (`unchanged-scope.json`). |
| Memory exception | Examined `ctrl_memory.py:202` and its normal SoC caller. Independently reran all 11 public override plants: all caught, including other image points, default/SoC paths, unknown names and 57.5 tiles. `ledger-probes.log`. |
| Image/area ledgers | Matched `SPLIT_CONTROL_MEMORY.md:153` to final public plans/symbols: 37.0, 40.5, 50.0 planned tiles; 57.0 only for 8×8/two interfaces, one tile owed to S14. Five largest BSS consumers and the shared `-fno-stack-protector` runtime are disclosed. Checked OOC utilization against `MAILBOX_SPLIT.md:1482`: 5,515 LUT, 7,632 FF, one RAMB36 and ten RAMB18. OOC RTL inputs are unchanged since the measured ancestor. These are planned image-memory figures and mailbox-only OOC evidence, not full-image mapping or hardware proof. |
| Docs/behavior/sweep | Independently ran the 69-command docs script: 67 pass initially; two refuse a missing pinned HDL parser, then pass after its hash-locked scratch-only installation (`docs-parser-retry.json`). Published behave: 406 scenarios pass. Exact-head published sweep: 64 suites, 2,191,124 checks, zero failures; field campaigns and associated freshness checks are explicitly skipped. `published-sweep-summary.txt`. Full banks were not rerun. |

The census command took 1,061.113 seconds (17.69 minutes), below 27 minutes, or 60% of the job's 45-minute timeout. That is local command runtime, not the hosted job's setup-plus-execution time. Hosted timeout acceptance remains with the manager. Tool identity and hashes are in `tool-identity.json`; the requested simulator reports 5.050.

## Prior public findings and author STOP causes

After the independent pass, the PR discussion contained review-start notices and no earlier finding report; the review API returned an empty reviews list. There is no earlier named reviewer finding to silently clear or retain, and no prior CLEAN lens is imported. Public author STOP/gate failures were checked at their causes:

| Cause | Disposition at this head |
|---|---|
| Map-record G classification and map-writer reachability | Public ruling supplies one owner, the explicit exclusion and its placement-switch removal obligation. Normal/planted census runs verify that boundary. |
| Largest image exceeds 56 tiles | Explicitly authorized 57-tile measurement exception, owed to S14; other points/default builds cannot inherit it. Independently tested. |
| Undefined event decoded as counted face event | `mbx.c` now limits counted decoding to defined event types. D9 and its restored catch-all plant exist; final public campaign catches all 528 mutants. |
| Missing text-only stack-boundary entry | `census_ports.py` is present in `ctrl_configs.py`; it reads identity/contracts and compiles no stack source. Published boundary receipts cover both legs. |
| Timing-test underflow when request never opens | `suite_face.hpp:706` guards `held - 1`; independent 199/199 mutation completion confirms the campaign terminates. It does not resolve F1. |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1 | Frozen scope; `REQUIREMENTS.md:25`; `ARCHITECTURE_HW_SW_SPLIT.md:55`; YAML/ABI comparison; `aecp_face.c:77`; acknowledgement probe | R702-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| RTL | CLEAN | `KL_mbx.sv` commit/windows; `KL_mbx_evt.sv:318`; `mailbox_face.py`; `milan_soc.py:2645`; `census_ports.py:104`; adapter/model runs and 199 mutants | R702-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| Robustness | UNCLEAN — F1 | Held commit/retry; window timeout/tag/strobe/reset checks; event coalescing; source G-wire/unmapped-port probes; override refusals | R702-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| Tests | UNCLEAN — F1 | `test_aecp.cpp:1851`, `:1968`; independent failing assertion with passing controls; `suite_face.hpp`; census plants/rule removals; coverage/source receipts | R702-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| Docs | UNCLEAN — F1, F2 | `MAILBOX_SPLIT.md:1230`, `:1482`; `SPLIT_CONTROL_MEMORY.md:153`; `aecp_face.h:5`; YAML/generated descriptions; PR/evidence/docs gates | R702-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |

[R702] PASS RTL — `hdl/milan/mailbox/KL_mbx.sv`, `hdl/milan/mailbox/KL_mbx_evt.sv:318`, `sw/mailbox/mailbox_face.py`, `mbx-suite-retry.log`, `mbx-mutants.log` — applied reset, decode, held-value, tag, timeout, width and coalescing checks against contract 2.3. No open RTL finding. The firmware failure is observable because the RTL correctly keeps held values stable.

## Limits, integrity and pending manager duties

All 297 examined public receipt/probe files match the published SHA-256 manifest (`evidence-hashes.json`). This proves correspondence to published bytes, not a signed execution attestation. The supplied evidence commit has no signature header and the supplied packet has no detached signature; a signed packet could not be verified. No manager source bank at this head is claimed or inferred.

The exact-head hosted snapshot showed `rtl-fast`/`rtl-full` queued and docs/elaboration in progress. No queued, skipped or incomplete context counts as executed evidence here. Hosted/act acceptance, including the census job's total runtime, remains the manager's duty. No act, Docker, full builder/native/processor/Yosys bank, synthesis, hardware access, source fix, commit, push or GitHub mutation was performed.

Correction and re-review of F1/F2, the R1 residue checklist, independent clean reviews, final current-dev candidate builder/native validation, required hosted checks, authorized merge and containment remain pending. Source base: `e76a755a`; supplied live-dev snapshot: `76de691e5625cc4ea2f9a19def9e07c1183a14ee`. This source review and the recorded PR base do not substitute for the final candidate. The broader issue #665 remains open.

Physical calibration was NOT RUN; field skips and simulated service bounds are not hardware proof. S6 owes real datapath/CDC wiring and removal of the split-only map-writer exclusion. S14 owes the excess memory tile; the default flip still requires all points at or below 56. Target-runtime work remains outside this lane.

Final integrity verification compares all 1,448 parent tracked blobs, executable/symlink modes, index tree, HEAD and tree ID, plus all tracked blobs/index trees of the five required initialized submodules against their gitlinks (`tree-integrity.json`). All match. No tracked bytes needed restoration. Disposable extractions, probe copies and builds remain solely under `scratch/`, excluded from publication. Public receipts replace local absolute paths with neutral placeholders; original logs remain under scratch. Every publishable receipt/script is listed in `MANIFEST.sha256`.

## Wording residue


Severity: RESIDUE. Lens: Docs.

Authority: the owner's source-comment rule supplied for this review. These are new comment/docstring instances in `e76a755a..44d95625`; existing instances remain outside this review. Runtime strings and test diagnostic labels are not included. The separate generated `F1 store` description is covered by finding R702-3-F2.

Impact: source commentary carries workflow identifiers instead of durable issue and requirement references. No behavior, measurement, clause claim or test verdict changes in the fixes below.

Required outcome: make the following exact textual substitutions in the named comments/docstrings, retaining their surrounding behavioral explanations. Line numbers name the reviewed head.

| Artifact | Exact wording change |
|---|---|
| `hdl/milan/mailbox/KL_mbx_evt.sv:18` | Replace `(#665,` plus the following `ruling 6410169666)` with `(#665)`; reflow those two comment lines. |
| `sw/firmware/ctrl/aecp/aecp.h:71` | Replace `(#665, ruling 6410169666)` with `(#665)`. |
| `sw/firmware/ctrl/aecp/aecp_face.h:2` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666)` across lines 2–3 with `(#665)`. |
| `sw/firmware/ctrl/app/ctrl_app_aecp.h:39` | Replace `(#665, ruling 6410169666 item 4)` with `(#665)`. |
| `sw/firmware/ctrl/mbx/mbx.h:125` | Replace `#665, the assignment 6409739310 and the ruling 6410169666` across lines 125–126 with `#665`. |
| `sw/firmware/ctrl/test/aecp_mutants.py:469` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666)` with `(#665)`. |
| `sw/firmware/ctrl/test/test_aecp.cpp:1718` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666)` across lines 1718–1719 with `(#665)`. |
| `sw/litex/ctrl_memory.py:24` | Replace `(#665 ruling 6412739248)` with `(#665)`. |
| `sw/litex/milan_soc.py:2687` | Replace `#665, comment 6410169666` with `#665`. The preceding pre-existing comment reference is not a new instance. |
| `sw/mailbox/census_plants.py:564` | Replace `(#665, ruling 6410169666 item 5)` with `(#665)`. |
| `sw/mailbox/census_ports.py:5` | Replace `(#665, ruling 6088423771, decision 1)` across lines 5–6 with `(#665)`. |
| `sw/mailbox/census_ports.py:9` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666)` across lines 9–10 with `(#665)`. |
| `sw/mailbox/census_ports.py:14` | Replace `(decision D1 of comment 6409738976)` across lines 14–15 with `(#665)`. |
| `sw/mailbox/census_ports.py:52` | Replace `(comment 6009661573)` across lines 52–53 with `(#637)`. Keep the named map-writer exclusion and placement-switch acceptance item. |
| `sw/mailbox/census_selftest.py:19` | Replace `(#665, ruling 6410169666 item 5)` across lines 19–20 with `(#665)`. |
| `sw/mailbox/mailbox.yaml:63` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666; the disposition scheme D1 of comment 6409738976)` across lines 63–64 with `(#665)`. |
| `sw/mailbox/mailbox.yaml:430` | Replace `(#665, ruling 6410169666; decision D1 of comment 6409738976)` across lines 430–431 with `(#665)`. |
| `sw/mailbox/mailbox.yaml:815` | Replace `(#665, ruling 6410169666)` with `(#665)`. |
| `sw/mailbox/mailbox_face.py:5` | Replace `#665, the assignment 6409739310 and the ruling 6410169666` across lines 5–6 with `#665`. |
| `sw/mailbox/publication_census.py:111` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666)` across lines 111–112 with `(#665)`. |
| `tb/verilator/mbx/mutants.py:481` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666)` across lines 481–482 with `(#665)`. |
| `tb/verilator/mbx/suite.hpp:100` | Replace `(#665, the assignment 6409739310 and the ruling 6410169666)` with `(#665)`. |
| `tb/verilator/mbx/suite_face.hpp:4` | Replace `#665, the assignment 6409739310 and the ruling 6410169666` across lines 4–5 with `#665`. |
| `tb/verilator/mbx/suite_face.hpp:217` | Delete the comment prefix `F1: `. |
| `tb/verilator/mbx/suite_face.hpp:240` | Delete the comment prefix `F2: `. |
| `tb/verilator/mbx/suite_face.hpp:334` | Delete the comment prefix `F3: `. |
| `tb/verilator/mbx/suite_face.hpp:402` | Delete the comment prefix `F4 to F6: `. |
| `tb/verilator/mbx/suite_face.hpp:476` | Delete the comment prefix `F7: `. |
| `tb/verilator/mbx/suite_face.hpp:538` | Delete the comment prefix `F8: `. |
| `tb/verilator/mbx/suite_face.hpp:586` | Delete the comment prefix `F9: `. |
| `tb/verilator/mbx/suite_face.hpp:656` | Delete the comment prefix `F10: `. |
| `tb/verilator/mbx/suite_face.hpp:706` | Replace `T0 has failed` with `the timing check has failed`. |

Verification: inspect only the added source-comment/docstring text against the owner rule; retain issue and requirement references. The checks and their emitted diagnostic strings stay unchanged. This residue does not make any lens unclean.

R702-3 FINISHED
