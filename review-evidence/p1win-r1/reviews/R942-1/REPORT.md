[R942] NEGATIVE - exact head 85569e241625d8e4176aae7d77c524783dff30cd

External independent review, round R942-1, of #1009 / PR #1017. All five lenses were applied. Two MINOR findings remain open. This verdict releases neither merge nor board acceptance.

Reviewed tree: `89dc2ac457b7506fe6e76e877f8635bf757101a5`. Reviewed range: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350..85569e241625d8e4176aae7d77c524783dff30cd`: six commits, 31 changed files. Reconstruction followed the requested order. An independent verdict and ledger were written before the predecessor reviews were opened. The concurrent review report was not consulted. PR #1017 had no earlier public findings, formal reviews or inline threads at inspection; `public_review_status.txt` records this check.

Authority: [#1009 ruling 3](https://github.com/kebag-logic/milan-fpga/issues/1009#issuecomment-7176978406), the issue's earlier decisions as superseded there, AGENTS.md, CONTRIBUTING.md, REQUIREMENTS.md, `docs/design/SAVED_STATE_MATERIALIZATION.md:2394` (DR2a), the store's flash/state interfaces, and Milan v1.2 5.5.3.5.3 and 5.3.8.3 as cited by the ruling. Step 1 is the 100 ms binding-class window on whole commits; every other class retains 1,000 ms. Strict save-before-response belongs to #1012 and is not a defect here.

**R942-1-F1 - MINOR - Conformance, RTL, Tests, Docs - The routed LUT excess has no supporting attribution or accepted disposition.**

Artifact: the PR resource table and [author/receipts/win/images.txt](https://github.com/kebag-logic/milan-fpga/blob/a7eb193aa6d85f970500c8ca64ea45189a8ba7a3/review-evidence/p1win-r1/author/receipts/win/images.txt), sections `8x8-base` and `8x8`; `source_audit.log`.

Authority/evidence: the assigned resource review includes the project's approximately 50 LUT band, alongside ruling 3's timing, unchanged-ledger and block-RAM requirements. The same pre-registered directive gives 45,814 LUTs at the base and 45,973 at the implementation: **+159**, approximately 0.347%, outside the approximately 50 LUT comparison band supplied for this review. That band is not stated as a hard LUT cap in ruling 3. Registers fall by six; block RAM stays 98.5 tiles. The packet supplies one route per endpoint and no synthesis/placement-stage counts or changed-cell attribution. The hardware sources, submodule pins and memory policy are unchanged, but the firmware contents change. That fact does not establish identical optimized hardware or bound implementation variability.

Impact: this is measured routed resource growth outside the stated band. **Placement noise is not established.** Neither a functional logic-growth cause nor a statistical noise explanation can be proved from these totals alone. The resource attribution requested for this review remains unresolved; positive timing does not supply that attribution.

Required outcome: publish comparable intermediate/hierarchical resource evidence that explains the +159, and record its public disposition relative to the stated comparison band. If placement variation is the explanation, show evidence sufficient to distinguish it from growth introduced by changed image contents. Do not select a different favorable directive after seeing the results.

Verification: reconcile base and implementation counts under the same recipe, identify the cells/stage responsible, retain the +0.030 ns corner floors and unchanged block-RAM totals, and re-review the resulting evidence. No hardware build was rerun in this review.

**R942-1-F2 - MINOR - Conformance, Tests, Docs - The public execution packet does not establish reproducible source identity for the required campaigns.**

Artifacts: [author/receipts/win/gates.txt](https://github.com/kebag-logic/milan-fpga/blob/a7eb193aa6d85f970500c8ca64ea45189a8ba7a3/review-evidence/p1win-r1/author/receipts/win/gates.txt), `bind-groups.txt`, `interchange.txt`, and the packet manifest at that commit.

Authority/evidence: AGENTS.md requires public, reconstructible evidence and exact validation commands; the predecessor R931-1-F6 specifically requires both full budget runs' `results.json` and exit status. The six published files are prose and extracted receipt lines. Examples: `st-1x1` and `st-8x8` identify `c34e7d8b dirty 24`; `mut` identifies `c34e7d8b dirty 23`; `hst2` identifies `8a4ad2c4 dirty 5`. The budget regrades identify `cd9ea485 dirty 1` but publish neither the input identity records nor the underlying results/logs. A dirty-path count cannot identify the bytes executed. Interchange names `xchg.py, one-off, not committed`, without that script or either journal. The public PR comments contain review-start notices, not additional campaign receipts.

Impact: the summaries report the requested runs, but a cold reviewer cannot check that their execution inputs match this head, inspect the full timing rows, or replay the interchange from the published artifacts. This is an evidence gap, not an assertion that those runs failed or that all earlier-head evidence is invalid. The clean routed build at `8a4ad2c4a9009693d45d2178bf538e02ef7cdfa2` is distinguishable: the later delta consists only of documentation and the coverage ratchet, as independently checked in `source_audit.log`.

Required outcome: publish the existing source-input identities, exact commands, full budget results/logs and exit statuses for both points, split-target case results, and the interchange script/journals. Demonstrate equality of relevant tested inputs to this head, or replace the affected source receipts. Keep this source evidence separate from the manager's eventual current-dev merge-candidate validation; no manager source bank is requested or assumed.

Verification: validate artifact hashes, regrade the recorded runs using the unchanged graders, check every required group and timing row, and execute the published interchange procedure. This retains the evidence-closure portion of R931-1-F1 and R931-1-F6; moving the obligation to candidate validation does not resolve source provenance.

**Implementation examination and acceptance accounting**

File shorthand below resolves to `sw/firmware/ctrl_nvm/` for store files, its `test/` directory for host tests, `tb/verilator/ctrl_service_budget/` for budget traces and graders, and `tb/verilator/nvm_split_target/` for target cases and graders.

`sw/firmware/ctrl_nvm/nvm_store.c:941` classifies only the unsigned binding-ID interval; its callers reject unknown records. At :973 the earliest due time wins, so subsequent changes do not restart a window. `nvm_capture_begin` closes the previous window, capture joins remain bounded, a later binding opens another window, and other-class in-flight work retains its first-idle behavior. `nvm_idle:553` checks retry backoff before either window; the 100 ms change does not bypass DR2c. Reset, OFF and HELD behavior, failure accounting, authoritative-slot selection, blank checking and complete verification were inspected. No product HDL, CDC primitive, port, submodule pin, layout, reservation area or flash-frame format changes in the reviewed delta.

`sw/firmware/ctrl/app/ctrl_app_aecp.c:249` marks binding records; the pinned binding owner's `record_of` / `finish` path includes bound, unbound and started/stopped projections. These commands therefore reach the same class. The format/codec files are byte-identical to `2509db68`; the boot and commit framing paths are unchanged by this PR. The public interchange receipt reports both directions, with matching name and binding responses; its reproduction limitation is F2.

The following timings are **author-published simulation results**, not independent board measurements. Their source-artifact qualification is F2. Independent focused execution is listed separately below.

| Ruling 3 item | Examination and result |
|---|---|
| Idle bind, unbind, start, stop <=800 ms, both points | `bind_save.py:110` sends all four, requires successful responses and each command's own complete save. Published maxima: 304.535 ms at 1x1/1if and 550.481 ms at 8x8/1if. Modeled erase 120 ms, page 0.5 ms. Board timing and <=10 ms brackets remain owed. |
| In-flight bound, at least eight phases | `bind_save.py:140` defines ten arrivals: capture-end/seal-start, mid-seal, early/late erase, early/late blank check, early/late program, early/late verify. Phase and two-save checks prevent an idle run from substituting. Worst published values: 394.959 ms against 450 and 891.169 ms against 950, both at capture-end. The other nine range 298.517-392.866 and 552.760-880.349 ms. DR2a and PR text state the distinct bound and lack of safety at a 1 s cut. The board's 8x8 <=1,000 ms remains owed. |
| Swept cut 0-3 s | `test_nvm_window.cpp:233` / `nvm_rig.cpp:315` sweep idle cuts every 10 ms plus effect start/midpoints, require old or new and new from 800 ms, then another save and reboot. :249 adds nine in-flight arrival phases with 25 ms cuts and 450/950 ms gates. Both ports, five shapes; erase 150 ms, page 0.5 ms. These host cuts start at the synthetic state change, not a real wire response, and do not prove physical power timing. |
| Split-target boot/restore | `target_cases.py:57` moves all-record marking to the first tick after the rename; `target_grade.py:338` retains one erase, all pages, reference decoding, saved name and binding checks. :365 checks the shortened window. Published cases `commit`, `valid`, `absent`, `torn`, `version`, `guard` and all controls pass at both points; erase delays 128.4/206.9 ms. Independent self-test: 79 checks, zero failures. Full execution closure remains subject to F2. |
| Full service budgets at both points | Public receipt reports 113 groups each, zero refusals. It reports seven deliberate egress-hold misses at each point and one 8x8 work-pass overrun assigned to existing #977; these are not an all-rows-clean result. The 1x1 baseline comparison is within 0.05 ms, and the PR states 8x8 stays below the existing egress ledger. Full notice <=140 ms and ACMP <=30 ms rows are not published for inspection: F2 retains that requirement. No new allowance is introduced by the diff. |
| Load and #920 | Independent static load calculation: 0.512 at 1x1 and 0.744 at 8x8/1if, below the assigned 0.70/0.76 ceilings. The script directly holds 1x1; the 8x8 comparison here uses its reported value. Published save-burst/flight: 1,097.438/147.073 ms at 1x1, 1,353.998/650.995 ms at 8x8, below 5 s. These other-class simulations have zero device busy delay. |
| 64-bind burst | `bind_save.py:122` constructs 64 binds/unbinds, 10 ms apart, and checks each sink's final value, save kind and erase cap. Latest published convergence: 306.463 ms at 1x1, 646.392 ms at 8x8; four and two saves, respectively, one 64 KiB erase each. Host burst also checks final values after reboot. |
| No raised ledger entry or extra block RAM | Memory policy files are unchanged. Public platform totals remain 45.5/46.5/59.5/64.5 planned tiles across the four points; ROM grows 72/72/64/64 bytes, SRAM unchanged. Fixture arms retain their individual tile plans. Routed tiles remain 80.5 at 1x1 and 98.5 at 8x8/1if. LUT acceptance remains F1. |
| Routed floors | Implementation 8x8 slow WNS +0.045 ns, least hold +0.036 ns; 1x1 +0.126/+0.036 ns. Both pass +0.030 ns at every reported corner. Base 1x1's +0.013 ns hold does not pass that floor; the implementation does. One route per endpoint does not show a trend. |
| Board power-cycle cases | Owed and running, not discharged here. Each required cut must establish an idle store at bind, response-referenced timing, durability before power loss and at least 250 ms before the final frame. Simulation summaries do not establish these conditions. |

**Disposition of predecessor findings**

Read only after the independent pass: [R931-1](https://github.com/kebag-logic/milan-fpga/pull/1014#issuecomment-7176835261) and [R932-1](https://github.com/kebag-logic/milan-fpga/pull/1014#issuecomment-7175810289).

| Finding | Disposition at this head |
|---|---|
| R931-1-F1 | Source/case/document correction verified; container checks were not weakened and the 79-check self-test passes. Public execution closure at both points is retained under F2 pending identifiable full receipts. |
| R931-1-F2 | The 800 ms claim is now explicitly idle-only under ruling 3. Ten phase-checked arrivals and the in-flight cut sweep implement the separately ruled bounds. The earlier unconditional requirement is superseded, not silently relaxed; reported measurements meet the new bounds, subject to F2. |
| R931-1-F6 | Full 113-group summaries now exist, but required results and input identities are absent. Retained under F2. The static-load portion was independently repeated. |
| R931-1-F7 | Closed for the whole-commit scope: whole-save completion, burst erase caps, idle/in-flight ownership, and actual modeled flash times are graded. All 26 relevant mutants were independently caught. Frame/no-erase expectations belong to #1014, not this step. |
| R931-1-F8 | Corrected: current store counts, modeled-busy-time qualification, unchanged ledger values, and shortened staged-save-window descriptions agree with their executable sources. No new numerical documentation defect found. |
| R932-1-F2 | Grader defect closed: trace runs terminate at writes; raw post-program coverage is unique-byte coverage; cross-write runs are refused. Seven independent complete-save reconstruction probes and the relevant mutants confirm rejection of partial, duplicate and pre-program reads. Regenerated measurement provenance remains within F2. |

The frame, lag, reserve, maintenance-capture and frame-chain boot defects from #1014 are absent from this whole-commit implementation; this review grants no closure to #1014 itself. No new prohibited source-comment label or review identity was found in the added lines. No RESIDUE or SUGGESTION is filed.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | #1009 ruling 3; REQUIREMENTS.md; DR2a at SAVED_STATE_MATERIALIZATION.md:2394; nvm_store.c:553/:948; public image and gate receipts | R942-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| RTL | UNCLEAN: F1 | Complete 31-path delta; nvm_store.c state machine; nvm_shape.h:150; ctrl_app_aecp.c:249; flash/state interfaces; unchanged HDL/pins/memory policy; routed totals | R942-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| Robustness | CLEAN | test_nvm_window.cpp:69/:110/:156/:190/:233/:249; nvm_rig.cpp:315; failure/HELD/reset paths; host flash fault model; save_grade.py:32/:75/:86; binding_grade.log | R942-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| Tests | UNCLEAN: F1, F2 | All changed store, budget and split-target tests/graders; 16 store plants; 26 grader mutants; independent read-coverage probes; source_audit.log; public packet manifest | R942-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| Docs | UNCLEAN: F1, F2 | All changed Markdown and coverage exclusions; PR body; DR2a amendment; public author packet; source-comment delta | R942-1 | 85569e241625d8e4176aae7d77c524783dff30cd |

[R942] PASS Robustness - `sw/firmware/ctrl_nvm/test/test_nvm_window.cpp:233`, `nvm_rig.cpp:315`, `tb/verilator/ctrl_service_budget/save_grade.py:75`, `binding_grade.log` - examined window ordering, backoff, capture joins, reset/held behavior, modeled cut recovery and complete post-program read coverage against DR2a/DR2c and ruling 3. No open robustness finding at this head. This scoped clean result is not physical qualification.

**Independent execution and limits**

| Independent execution | Raw receipt and outcome |
|---|---|
| Normal store tests at five shipped shapes | `focused_store.log`, `normal-*.log`, `focused_store.rc`: **656 test executions passed** (128 main-suite cases at each shape, plus 16 unit/vector executions). Binaries were built from the unchanged reviewed head in this session, then replayed against regenerated fixtures; hashes are recorded. |
| All 16 binding-window store plants | `plant-*.log`: every plant built successfully and every named killing check failed as expected. **16/16 caught**; aggregate return code 0. Portable `focused_store.py` can build the normal binaries afresh; this run used its documented reuse option. |
| Binding/verify grader baseline and mutants | `binding_grade.log/.rc`: **33 baseline checks pass, 26/26 mutants caught**, seven independent valid-checksum save/readback probes pass; return code 0. |
| Split-target grader | `restore_selftest.log/.rc`: **79 checks pass**, return code 0. This is the grader self-test, not a fresh full target campaign. |
| Full budget grader baseline | `budget_selftest.log`: **1,048 baseline checks pass**. The optional broad mutation rerun was stopped by the reviewer after partial progress; return code -15. No independent 321-mutant pass is claimed. |
| Static loads | `load.log/.rc`: **PASS**, 0.512 and 0.744 at the two points. |
| Source and public packet | `source_audit.log/.rc`: hashes and source relationships **PASS**. |
| Raw final checkout integrity | `integrity_final.log/.rc`: **PASS**, tracked bytes/modes/index and pinned submodule contents. |

The optional broad store mutation campaign was also stopped by the reviewer (return code -15); `store.log` and `store_full_limit.txt` retain that limitation. Its complete normal suites and the required 16 plants were then independently completed by the focused driver above. The author's published 170-control and 321-mutant claims were source-audited, not independently rerun in full. No independent coverage percentage or cross-compiled firmware-size result is claimed. `RECEIPTS.txt` gives reproduction commands and distinguishes expected mutant failures from campaign failures. Independent checks ran concurrently within 13 jobs for the focused run; the initial run used at most 14. No implementation build ran beside them.

The published packet's six files match its manifest hashes (`source_audit.log`). That verifies their bytes, not the provenance missing in F2. The final source remains untouched; the final raw integrity receipt covers all 1,987 superproject blobs, modes and index entries, the four required registered submodule gitlinks and their tracked contents, plus the initialized SRP submodule. The optional external submodule was not used. Temporary builds and mutant copies stayed under packet/scratch.

No full parent, processor, synthesis or builder bank, hardware operation, source fix, commit, push, GitHub write, or merge was performed. No current-dev candidate was built. The default environment lacks the native target build dependencies; no shared installation was attempted. The scoped simulator identity was checked as the requested 5.050 release, but no fresh native target image was built with it. The complete source-to-board timing and physical cut campaign remain unmeasured by this reviewer.

**Pending manager duties**

Resolve F1 and F2 publicly and obtain the required clean reviews. Complete the board obligations with <=10 ms measurement brackets and the separately stated in-flight bound. Physical calibration is **NOT RUN**; field skips are not hardware proof. Finish applicable hosted/local acceptance, counting executed jobs separately from skipped contexts. `hosted_status.json` is a point-in-time observation only, not an acceptance verdict.

There is **no manager source bank at this head**, and none is claimed. At merge time the manager must construct and validate the separate current-dev candidate, publish its builder/native receipts, obtain merge authorization and perform containment. The source base is `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`; the supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`, which must be refreshed at that turn. Do not substitute that future candidate's receipts for missing source identity or close #1009 while its board acceptance is owed.

`MANIFEST.sha256` enumerates the publishable scripts and receipts. Scratch files are excluded. No work remains running in this review when the packet is finalized.

R942-1 FINISHED
