[R513] POSITIVE - exact head 669ded57b1fabc2bbf274b8ad05493c7593e0a0a

Issue [#69](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69), PR [#165](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165), round R513-3. Tree `4bce83358cf24f551909ab46aeb19c5f93787106`. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR; no new RESIDUE or SUGGESTION.

This is the requested delta review of round-two head `75c4eee4589e9317aca3d07b91f94a38b4cc86af`, the merge of processor main `2ad2f845dd583f8310075fa2380cb60a04fd091a`, and the final storage-table correction. Prior judgments for untouched artifacts stand. The result covers the non-redundant fabric implementation's extension seam, not a complete redundant product or hardware conformance.

**Independent reconstruction.** No repository or applicable ancestor AGENTS.md/CONTRIBUTING.md was present. The supplied instructions were followed, then docs/README, frozen issue acceptance and public scope decisions, requirements/interface authorities, the full `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8..669ded57b1fabc2bbf274b8ad05493c7593e0a0a` diff and history, and public evidence. Authorities include F01.5, Δ12, REQ-SCP-003, REQ-AEM-016, 02's RX/counter contracts, 06's registry/storage contracts and the cited Milan provisions. No independently obtained standards PDF was used. The controlling [lane assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69#issuecomment-6010216843) and [merge assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69#issuecomment-6024309003) require the seam and both branches' checks to survive.

The [independent verdict and ledger](receipts/independent-verdict.md) were written before reading prior public reviewer report bodies; the [freeze receipt](receipts/independence-freeze.json) records its digest and time. No private author material, management checkout, lane scratchpad, other checkout or subordinate reviewer was used. The [full diff](receipts/full-diff.patch), [delta](receipts/round3-diff.patch), [history](receipts/history.txt) and [reconstruction record](receipts/reconstruction.json) are retained.

**Merge and identity.** The actual no-fast-forward merge `600ef13` has exactly the two stated parents. Subsequent commits record the campaign, restore the 100-line limit, then change only the one documentation row. Compared with round two, every RTL file, both ADP/notification suites, top IF checks, wrapper, Makefile and interface guards are byte-identical. Main's entire notification-phase file survives byte-identically. The README's DN section equals main's; its IF section equals round two's. The control inventory is exactly the prior 77 plus main's nine DN controls, with unchanged edits, suite commands and named checks. `main()` is exactly 100 physical lines. [Structural receipt](receipts/delta-check.json), [README comparison](receipts/readme-merge.json).

Count-one identity therefore survives this delta by unchanged RTL and unchanged prior test/control definitions. The new DN checks add coverage. The earlier accepted distinction remains: equal cell counts do not mean every statistics file is byte-identical, because port/wire metadata and derived names changed in earlier rounds. The public round-two PR body reports paired OOC 1x1 results of 23,179 LUT / 19,779 FF at both endpoints, delta 0 LUT / 0 FF. Those are carried measurements; no new area measurement is claimed. Comparing the whole PR directly with frozen base also includes inherited main changes and must not attribute them to this merge delta.

**Fresh executable evidence.** The required pinned simulator identity was checked before use. Foreground coordinators waited for all children; independent work ran concurrently with explicit campaign jobs, `make -j16`, bounded compiler fanout, and separate logs/status files. Campaign elapsed time was 694.579 seconds. Recorded peak memory was 8,807,636,992 bytes under the 12 GiB cap. All build/probe trees were confined to packet scratch.

| Check | Result | Receipt |
|---|---|---|
| Complete notification campaign | **86/86 KILLED; ten goldens PASS**; zero build failures, incomplete runs or missing named failures | [raw results](receipts/notify/results.json), [campaign summary](receipts/campaign-summary.json), [log](receipts/notify.log) |
| Main's DN checks and nine controls | 15/15 golden checks; all nine controls killed; failure counts exactly match README | [DN golden](receipts/notify/golden-pp_top-domain-notify-only.log), campaign summary |
| Integrated two-interface IF | 6/6; includes held REGISTER/DEREGISTER and distinct row sequence IDs | [IF golden](receipts/notify/golden-pp_top-obj_if2_Vpp_top_if2.log) |
| Notification unit suite | 64/64: 41 shipping, 4 identify, 19 PT/CK/PD/CA | [suite golden](receipts/notify/golden-aecp_notify-run.log) |
| Prior IF/PD/CA/counter controls | All 21 killed; documented failure counts match exactly | campaign summary and individual raw logs under receipts/notify |
| ADP, both shapes | 1,359/1,359: 1,348 shipping + 11 interface checks | [ADP log](receipts/adp.log) |
| Interface-count guard | 1/2 elaborate cleanly; 0/3 refused by name, 4/4 | [guard log](receipts/if-guards.log) |
| Documentation gates | Links, parameters, IDs, figures and module matrix PASS, including their selftests | [documentation log](receipts/docs.log) |

The counter-stamp correction at `docs/architecture/06_aecp_engine.md:931` is `(streams in + out + 1 + P-N-AVB-INTERFACES) × 32 bits`. It agrees with `N_CTR_DESC_C` at `hdl/aecp/KL_aecp_notify.sv:435` and the array at `:446`. Independent elaboration checked the actual constant and array extent/element width:

| Streams in/out | Interfaces | Stamps | Bits |
|---|---:|---:|---:|
| 1/1 | 1 | 4 | 128 |
| 1/1 | 2 | 5 | 160 |
| 8/8 | 1 | 18 | 576 |
| 8/8 | 2 | 19 | 608 |

These are declaration sizes, not physical utilization. Raw elaboration logs and [shape results](receipts/delta-check.json) are included.

**Prior public findings.** Read only after the independent verdict/ledger. The reviewed reports are [R512-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165#issuecomment-6016189510), [R512-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165#issuecomment-6024562233) and [R513-2](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165#issuecomment-6024563661); R513-1 had no open finding. Formal review submissions and inline-comment inventories were empty. [Disposition receipt](receipts/prior-findings.json).

| ID; original severity; all attributable lenses | Authority, original impact and required outcome | Exact-head resolution and verification |
|---|---|---|
| R512-1-F1; MINOR; RTL, Robustness, Tests | The monitor's command-supersedes-probe contract: two registrations could leave one probe uncancelled and remove a live row. Every superseded probe must be cancelled and late reports harmless. | **RESOLVED.** `KL_aecp_notify.sv:714` pending cancellation, live-probe report routing and owner settling survive unchanged. `port_tuple.hpp:463` CA1/CA1b/CA2/CA3/CA4 pass; all five cancellation/report/owner controls are killed. |
| R512-1-F2; MINOR; Tests, Docs | Assignment item 5 and the README claimed command-port provenance that the old test did not prove. Held commands and distinguishable rows must reject wrong-source/wrong-port controls. | **RESOLVED.** `tb/pp_top/interface_phases.hpp:127,224` and 09 §8.9 retain the strengthened scenario. `rgy_port_from_latest_frame` fails IF3 and IF3b; `dereg_matches_other_port` fails IF3b; the golden passes. |
| R512-1-F3; MINOR; Conformance, Docs | F01.5, Δ12 and Milan §5.3.4.2 require capacity per interface; a shared table was insufficient. Key capacity and align the requirements. | **RESOLVED.** Notify `:364` uses `N_CTRL_P * N_IF_P`, port-restricted allocation and slot-based expiry routing. PD1–PD3 pass; all five depth/tag/expiry controls are killed. F01.5, REQ-AEM-016 and REQ-SCP-003 agree. The prior 32-row production-depth judgment stands on unchanged bytes; it was not rerun here. |
| R512-2-F4 = R513-2-F1; MINOR; Docs | Storage table versus notify `:435,446`: the old count-two claim omitted one 32-bit stamp. The formula must describe both legal counts. | **RESOLVED.** `06_aecp_engine.md:931` now has the requested formula; all four elaborated shapes above agree and documentation gates pass. |
| R512-1-S1; SUGGESTION; Tests | The historical 96 inventory mixed mutations with observation anchors. Enumerate the categories reproducibly. | **RESOLVED.** PR body §5 still explicitly gives 70 + 20 + 3 + 1 = 94 arms and two BFM anchors. No new claim of 96 distinct mutants is made. |

The known count-one simultaneous drain/command cancellation defect remains separate [issue #167](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/167), explicitly predating this PR. Its unchanged status follows the frozen count-one preservation scope; it is not represented as fixed or defect-free. At count two, CA1b and its control still establish both cancellations.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue 69 frozen scope; F01.5, Δ12, REQ-SCP-003/REQ-AEM-016; 02 contracts; preserved per-interface depth; DN/IF/PD evidence | R513-3 delta; R513-2 standing scope | 669ded57b1fabc2bbf274b8ad05493c7593e0a0a |
| RTL | CLEAN | Full diff/history; all RTL bytes versus round two; top frame/command latches; notification rows/owner/counter geometry; four elaborated shapes | R513-3 delta; R513-2 standing RTL | 669ded57b1fabc2bbf274b8ad05493c7593e0a0a |
| Robustness | CLEAN | Held IF commands; capacity/expiry PD checks; CA cancellation, late reports and settling; boundary guards; associated killed controls; issue 167 limit | R513-3 re-execution; R513-2 unchanged production-depth coverage | 669ded57b1fabc2bbf274b8ad05493c7593e0a0a |
| Tests | CLEAN | Merge inventory 77+9; 86 completed kills; ten goldens; ADP and guard runs; README failure-count reconciliation | R513-3 | 669ded57b1fabc2bbf274b8ad05493c7593e0a0a |
| Docs | CLEAN | 06:931 versus RTL/elaboration; DN and IF README sections; 09 coverage descriptions; focused documentation gates; prior-findings closure | R513-3 | 669ded57b1fabc2bbf274b8ad05493c7593e0a0a |

**Evidence limits and manager duties.** The fixed [public evidence directory](https://github.com/kebag-logic/milan-fpga/tree/83221a43e3d1f5922143becbaba0661fef2c201b/review-evidence/pp69-r1) contains first-round author summaries and a consumer patch, plus their manifest. All three published hashes match. It does not contain executable raw round-three bank receipts. The task supplies the manager's statement that full source static/builder and native banks passed at this head; that is separate from the executions above. No additional bank-results comment was present in the retrieved issue/PR snapshots. The manager should publish/link those exact-head completion receipts.

At the final [hosted checkpoint](receipts/hosted-summary.json), both exact-head runs ([PR](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37540577805), [push](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37540570371)) have successful docs-gates and portability jobs with substantive steps executed. Their suites jobs remain in progress; later campaigns are pending. The cached simulator-build step was skipped. Neither entire workflow is counted as passed. Hosted/container acceptance belongs to the manager.

No full parent/processor/time-sync/synthesis/builder banks, container execution, physical build, field run or hardware test was performed here. Physical calibration is **NOT RUN**; field skips are not hardware proof. The manager must obtain the other independent verdict, complete the owned acceptance checks, and build/validate the final current-dev candidate at the merge turn. Source base `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8` and live dev `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0` are distinct contexts. This source verdict does not certify that future candidate.

**Integrity and reproduction.** The documentation runner initially encountered archive/Git-metadata setup failures. A temporary worktree setting introduced by that attempted workaround was removed, and the checks passed in the ordinary checkout; [setup receipt](receipts/documentation-setup.json) and failed-attempt logs are retained. No source defect is inferred from those harness failures. All 581 tracked blob bytes and modes, index tree, detached HEAD and actual worktree root are verified against the exact published head. Required submodule gitlinks: none in this processor tree. [Final integrity receipt](receipts/tree-integrity.json).

No source fixes, commits, pushes, merges, GitHub writes or author contact occurred. [Portable scripts](scripts/README.md), raw logs and relative receipt links are included. MANIFEST.sha256 enumerates publishable files; scratch is excluded. All foreground work has completed.

R513-3 FINISHED
