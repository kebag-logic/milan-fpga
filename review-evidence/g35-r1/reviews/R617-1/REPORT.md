[R617] NEGATIVE - exact head 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3

Full external independent review of issue #35 / PR #80, round R617-1. The any-byte refusal repair works, the required donor gates pass, and independently reapplied defects fail by name. One MAJOR acceptance mismatch remains open: the frozen issue requires zero bank writes, while this head and its new tests allow writes before and on the flagged byte. No public maintainer/manager ruling explicitly authorizes that relaxation. This verdict does not allege a demonstrated regression in the shipping parent, which ties the error input low.

Base: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. Head tree: `9a2ecff812f209bf90eb6714690e864a4ec4f582`. Four commits, 11 changed files, +393/-18. Only the parser RTL, parser tests and current documentation change; no engine RTL, microcode, generated image or gitlink changes. Final verification confirms all 105 tracked file blobs and Git modes, the index tree, HEAD and worktree; zero required gitlinks and empty status, including ignored files. See [final verification](receipts/final_clone_verify.txt).

The interrupted session's completed work was retained after checking its scripts, raw outputs, expected negative results and checkout identity. The resumed pass independently reconstructed the authorities, reviewed the full diff and surrounding consumers, verified public receipts, and added a focused bank-write acceptance probe. [The independent verdict and five-lens ledger](receipts/independent_verdict.md) were written before reading the earlier public review. Its findings were then reconciled below. No private author material or another reviewer's unpublished packet was used.

**Reconstruction and authorities.**

1. Repository and ancestor instruction-file check, then `docs/README.md`, root README and current integration/development/test/manager guides. No repository `AGENTS.md` or `CONTRIBUTING.md` exists at this head. The supplied local instruction reference was followed. The documentation map ranks RTL, executable tests, current guides, then dated history; that describes implementation truth, not permission to waive issue acceptance.
2. [Issue #35 body](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35) and all four issue comments. The [scope decision](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35#issuecomment-6104916029) chooses the any-byte latch, exactly one drop including SOF/EOF, unchanged error-free behavior, four-type positional tests, mutation control and donor gates. The [subsequent ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/35#issuecomment-6105366046) explicitly accepts the hierarchical +1 mux. Neither comment addresses the issue body's zero-bank-write requirement.
3. Interface authorities: parser header and ports; `docs/INTEGRATION.md:39-70`; engine input forwarding at `hdl/top/KL_gptp_engine.sv:167`, bank ownership/writes at `:180-310`, consumer reads at `:700-720`, and Announce publication at `:895-912`; bench error generation at `bench/arty/bench_mii_rx.sv:158`; [parent tie-off at the specified live-dev commit](https://github.com/kebag-logic/milan-fpga/blob/ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv#L666). Linked issues #27 and #33 were read for the adjacent drop-count and constant-input context. No new standards-clause claim is introduced by this patch.
4. Full `git diff BASE..HEAD` and four-commit history. The patch is preserved in [source.diff](receipts/source.diff).
5. [Frozen public executable evidence](https://github.com/kebag-logic/milan-fpga/tree/2e3232522119b5ef06bc7d15ea1d46c0c81a07fb/review-evidence/g35-r1), PR body and manager comments. All 57 files under the author's executable-evidence subtree were downloaded and matched their published SHA-256 values: [verification receipt](receipts/public_evidence_verify.log). The source-head evidence is author evidence plus this reviewer's focused execution, not a manager source bank.
6. After recording the independent verdict/ledger, read the [earlier public review](https://github.com/Mister-M-alt/FPGA-gPTP/pull/80#issuecomment-6105577480). There are zero separate submitted reviews and zero inline review comments in the captured API results. That public comment's three findings are explicitly retained below.

**R617-F1 — MAJOR — OPEN — Conformance, RTL, Tests, Docs.**

Artifact: `hdl/wire/KL_gptp_rx_parser.sv:60-62,452,478,645`; `tb/verilator/parser/sim_main.cpp:267,1262`; PR body Acceptance item 2.

Authority: issue #35 acceptance item 2 requires a refused frame to have exactly one drop, no event **and no bank write**, with first/middle/EOF tests. The public scope decision requires the drop/event sweep but does not explicitly remove the bank-write condition. The later ruling concerns hierarchical elaboration only. The author changes the checked acceptance to “no bank write after the flag”; that is weaker than the issue's frozen wording.

Evidence: the write enables use registered `bad_r`; the new latch updates it on the flagged edge. Words completed on that edge still assert `bank_we_o`, and earlier words have already been written. `feed_err` takes its baseline after `tick()` for the flagged byte, deliberately excluding same-byte and prior writes from its oracle. The fresh [focused receipt](receipts/bank_contract/result.csv) measures before/on/after/total writes and returns [rc 1](receipts/bank_contract/run.rc): **24 checks, 12 PASS, 12 FAIL** against literal zero-total-writes acceptance. All four error-free controls dispatch.

| Frame and error position, zero-based | Drops | Events | Writes before | Writes on flagged byte | Writes after | Total |
|---|---:|---:|---:|---:|---:|---:|
| Sync, byte 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Sync, byte 29 | 1 | 0 | 0 | 1 | 0 | 1 |
| Sync, byte 40 | 1 | 0 | 1 | 0 | 0 | 1 |
| Sync, EOF byte 57 | 1 | 0 | 5 | 1 | 0 | 6 |
| Follow_Up, EOF byte 89 | 1 | 0 | 7 | 0 | 0 | 7 |
| Pdelay_Req, EOF byte 67 | 1 | 0 | 4 | 0 | 0 | 4 |
| Pdelay_Resp, EOF byte 67 | 1 | 0 | 7 | 1 | 0 | 8 |

Impact: the refusal/drop behavior is correct, but green tests and checked PR acceptance do not demonstrate the issue's full required observable behavior. No accepted parser event names these refused frames. Prior writes also existed at base, and the shipping parent tie-off makes this path unreachable there; neither fact changes the acceptance condition selected for this fix.

Required outcome: either implement and test the frozen zero-bank-write requirement, or obtain an explicit public scope ruling allowing speculative writes up to and including the flagged edge, then align the issue, module/header guide, PR acceptance and regression oracle with that ruling. This review does not prescribe a buffering redesign if the manager chooses the latter outcome. It cannot classify the mismatch as wording-only RESIDUE: resolving it changes a conformance requirement and the required test oracle.

Verification: count **all** bank writes for first/middle/EOF pulses in the four required types; separately expose before/on/after writes so the approved boundary is unambiguous. Preserve one-drop/no-event assertions, clean recovery controls and named mutation failures. The current later-write tests remain useful but do not substitute for the frozen zero-total-write condition.

**Independent lens evidence.**

Conformance: the any-byte latch, exactly-one-drop rule, EOF handling, port/header disclosure, four-type positional sweep, held-to-EOF controls, unchanged error-free behavior and donor gates are supported. `feed_gap` explicitly drives `rx_err_i=0` at `sim_main.cpp:244`; it already did so at base. Current READMEs contain no parser check count, so dated historical counts were correctly preserved. R617-F1 prevents this lens from being clean. The parent +1 mux is explicitly accepted and is not a finding.

RTL: the new assignment at parser `:645` is inside `rx_valid_i` and after the SOF clear at `:403`, so a first-byte flag wins. The existing direct `!rx_err_i` EOF term at `:625` is essential because the latch updates on the same edge. No extra counter increment is introduced: deferred refusal and the one-byte-runt arm still feed the combined count at `:382-384,650-651`. Idle errors cannot poison a frame. Fresh SOF clears prior poison. Engine bank selection advances only on accepted events; its Announce reservation already releases after a poisoned frame without an event. These observations bound the effect of retained speculative words; no new engine-level error-input simulation is claimed.

The saved, independently constructed parser-only equivalence run proves **749/749 comparison cells** with the port tied low. With it free, `bad_r` remains unproven (748 proven, 1 unproven). See [tied proof](receipts/equiv/equiv_tied.log) and [free comparison](receipts/equiv/equiv_free.log). The different 748-cell count in the author's receipt comes from its wrapper; this review reports its own 749-cell result. The free-mode process returns zero because the script uses non-asserting status; that exit is not an equivalence pass. Flattened parser statistics agree, while written netlist text differs; no byte-identity claim is made for those dumps. R617-F1 remains attributable to RTL's required write behavior.

Robustness: [reviewer head probe](receipts/probe/probe_head.tsv) reports **57/57 PASS** under the disclosed later-write contract; [base probe](receipts/probe/probe_base.tsv) reports 31 PASS / 26 FAIL. It uses independent frame builders and counters across Sync, Follow_Up, Pdelay_Req, Pdelay_Resp, Pdelay_Resp_Follow_Up, Signaling, Announce with one-hop PathTrace, and padded Sync: 560 single-position pulses, held errors starting at every position, 64 multiple-pulse patterns per layout, all-byte errors and clean recovery. It also covers a flagged runt, zero-gap clean/error neighbors, a refused frame immediately followed by a flagged runt (two drops), stray valid bytes, abandoned-frame recovery, valid-low error gaps and combined EtherType/error refusal. No additional robustness defect was established. The probe's exit is intentionally always zero; the reported tally and raw measurements, not the exit, supply the evidence.

Tests: the resumed packet retains completed exact-head gate runs, whose exits and named results were independently audited in [saved_receipt_audit.log](receipts/saved_receipt_audit.log). The scoped simulator reports version 5.050, revision v5.050; [identity receipt](receipts/pinned_identity.txt) records its wrapper hash.

| Executed donor gate | Result and raw evidence |
|---|---|
| `make -j16 tb` | rc 0; microCPU 768/768; parser 298/298 and mutation arm 8/8; engine 1613/1613 three times and mutation arm 34/34; gaskets 81/81 and 5/5; tsngen 288/288 and 4/4; bench tag PASS. [log](receipts/gates_head/gate_tb.log) |
| `make -j16 contract` | rc 0. [log](receipts/gates_head/gate_contract.log) |
| `make -j16 lint` | rc 0. [log](receipts/gates_head/gate_lint.log) |
| `make -j16 docs` | rc 0; diagram bindings/selftests, documentation checks/selftests, 20 exact source anchors and checker selftest. [log](receipts/gates_head/gate_docs.log) |

The parser's seven committed mutations fail all the check names assigned to them: EOF-only reading, lost SOF flag, missing direct EOF term, per-flag overcount, ignoring all errors, poison surviving the frame, and sampling between bytes. The arm's clean control passes. The new 30 checks comprise seven checks per required type plus two gap checks. The total is 298, up from 268.

Four planted defects were independently reapplied in scratch copies and built against the exact-head bench; each returned rc 1 with named assertion failures. [Raw results and summary](receipts/reviewer_mutants/SUMMARY.txt):

| Independent edit | Bench result | Independently audited relevant failure names |
|---|---|---|
| R1: delete latch | 286 PASS, 12 FAIL | all 12 positional drop/event/later-write names |
| R2: move latch before SOF clear | 286 PASS, 12 FAIL | all 12 positional names, including all four required drop names |
| R3: remove direct EOF error term | 288 PASS, 10 FAIL | all eight required positional drop/event names, plus two existing checks |
| R7: move latch outside valid gating | 296 PASS, 2 FAIL | both gap-only error names |

Extra defects excluding SOF or requiring prior `run_r` each fail 12 bench checks; bypassing poisoned header-write gating fails 28. The equivalent change omitting the EOF latch while retaining the direct EOF term passes 298/298, as expected. The arm with base RTL fails its positive control and stale patterns (2 PASS / 6 FAIL, rc 1), as recorded in [arm_against_base_rtl.log](receipts/arm_against_base_rtl.log). The public renamed-check receipt also confirms that a missing named failure is rejected. These successes do not cover the omitted zero-total-write oracle in R617-F1.

Docs: inspected all changed current guides, root/parser READMEs, source-evidence rows, module header/port comments and PR body. The valid-byte, SOF/EOF, pulsed/held and idle-gap contract descriptions match execution. Updated source anchors `:386` and `:468` resolve exactly. Historical measurements remain dated and no new hardware/certification claim is made. Removing the issue risk bullets and presenting acceptance as complete remains premature for the unruled bank-write condition in R617-F1. The separate prose imprecision below is retained as residue.

**Parent and public evidence.**

The inspected author receipts identify scratch parent `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`, with the gPTP pin changed from the stated base to the exact reviewed head. Hierarchical elaboration passes at 3567 and 3568 cells; the parser gains one mux. Eight of nine staged modules are byte-identical; only the parser differs. After tie propagation, both flattened statistics report 2432 cells with identical per-type counts. Together with tied-input parser equivalence and unchanged surrounding modules, this supports the functional identity accepted by the manager. Raw `hier.il` and `flat.il` file hashes differ; those hashes are not byte-identity evidence.

All three generated ROM hashes agree across the pins. The gPTP image digest is `c496ed8af59edd424e7d980aa3442bb725c745f44469ce53ec3a4d219fa30371`; bundle digest is `018e9be9527f8c41ed605c2c4c5e2c8e134f2d84375758c81a022cbfb7646fd2`. The public ROM-ledger receipt explicitly fails before the new pin is recorded, then passes after adding the same-content digest row. These are inspected author measurements; this reviewer did not run a parent bank.

[Exact-head check-run](receipts/public/check_runs.json), [commit-status](receipts/public/commit_status.json) and [workflow-run](receipts/public/workflow_runs.json) queries returned zero entries. Thus there are no executed or skipped hosted jobs to count as source validation here. This is not an assertion that hosted acceptance was satisfied. The manager owns that acceptance.

**Prior public findings: explicit disposition at this head.**

The earlier public review had no open BLOCKER/MAJOR/MINOR. Its conformance discussion treats omission of bank-write language in the later scope comment as permission for speculative writes. This reviewer does not adopt that inference: neither public ruling expressly resolves the issue body's condition. R617-F1 remains open. Its factual observations about same-byte writes, successful refusal and parent identity agree with the independent evidence above.

- **R616-1-RES1 — RESIDUE — Docs — RETAINED.** Artifact: parser header `:60-62` and PR opening/Acceptance prose. Evidence: a word completed by the flagged byte is still written on that edge, demonstrated independently at Sync bytes 29 and 57. Impact: once separated from R617-F1's acceptance decision, the description of the implemented edge boundary is imprecise; clarifying that description changes no code, result or measurement. Exact fix: “No bank write follows the flagged byte's own edge; words written up to and including it stay in the write bank like those of any refused frame, unnamed by any event.” Make the equivalent “after the flagged byte's own edge” and “up to and including” substitutions in the PR. Verification: text review against the before/on/after receipt. Carry to the residue checklist; this wording fix alone does not resolve R617-F1.
- **R616-1-S1 — SUGGESTION — Docs, Tests — RETAINED.** Artifact: `docs/SOURCE_EVIDENCE.md:12` and `scripts/check_source_evidence.py`. The any-byte row links the file without an anchored construct and is outside the checker’s fixed expected map. Impact: future drift in this new claim is not structurally checked; existing functional tests still cover it, and checker edits are outside the stated lane. Optional outcome: when the checker is next changed, anchor the row to the latch and add its expected construct. Verification: the checker reports the new exact anchor and a moved/deleted latch fails its control. Not required for this patch's verdict.
- **R616-1-S2 — SUGGESTION — Tests, Robustness — RETAINED.** Artifact: `tb/verilator/parser/sim_main.cpp:1223-1306`; independent probe receipts. The committed sweep covers the four required types; broader parser types, padding, runts and adjacency are in reviewer probes. Impact: this additional exercised coverage is not permanent in the donor suite. Optional outcome: retain selected additional cases in the suite. Verification: clean cases and appropriate named mutations distinguish the added behavior. No extra mandatory acceptance scope is inferred.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — R617-F1 | Issue body and public rulings; interface authorities; full patch/history; positional bank receipt; parent evidence | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| RTL | UNCLEAN — R617-F1 | Parser latch/SOF/EOF/write/counter paths; engine consumers; tied/free equivalence; lint; parent tie-off | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Robustness | CLEAN | Independent 57-check eight-layout probe; held/multiple pulses; gaps, neighbors, runts, stray bytes and recovery; S2 optional | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Tests | UNCLEAN — R617-F1 | Four donor gate receipts; 298-check parser; seven committed named mutants; four independent reapplications; extra defects; write-oracle probe | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Docs | UNCLEAN — R617-F1 | Changed guides/READMEs; module/port contract; source anchors; PR body; frozen evidence; prior residue and suggestions | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |

**Real limits and pending manager duties.**

No manager source bank ran at this head, and none is claimed or inferred. Full parent/PP/gPTP/synthesis/builder banks were not run by this reviewer; the independent equivalence work was parser-only. No hardware or implementation/timing campaign was run. Physical calibration **NOT RUN**; field skips and historical silicon records are not hardware proof for this head. Engine-level mid-frame-error behavior was assessed through consumer code, not a new engine error-input test. The parser probes cover complete framed traffic; abandoned frames are recovery observations, not proof of counted refusal without EOF.

The manager must resolve R617-F1 publicly, carry the retained residue, and obtain the required positive reviews before merge. At the merge turn the manager builds and validates the final current-dev candidate using the builder and native banks, with source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and stated live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`, then links those receipts on the PR. That candidate evidence is distinct from source-head execution. Hosted/local-workflow acceptance remains the manager's duty. Parent adoption is separate; its gitlink and new-pin ROM-ledger row must be reviewed together.

No source fixes, commits, pushes, GitHub writes, author contact or merge were performed. Disposable probe trees are under packet `scratch/` and are excluded from publication. [Reproduction notes](scripts/REPRODUCE.md) identify portable scripts, expected positive/negative exits, and the distinction between raw outcomes and orchestration status. `MANIFEST.sha256` lists the publishable receipts and scripts; REPORT.md is the terminal report.

R617-1 FINISHED
