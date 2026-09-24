[R309] POSITIVE - exact head 8544472a19a4b4d3853d64b15dea22f999372a32

# R309-2 external independent delta review: issue #548 / PR #556

- **Head:** `8544472a19a4b4d3853d64b15dea22f999372a32`, tree `b7a11e8d2ac0d88826925877180806ee145208d8` (the published PR head was confirmed read-only to be the same SHA).
- **Source base:** `573f0052a0e4412e81f0845438fcec2086ce5d55`. **Round-1 head:** `e41703b2948ef53e5cb0dd01a1e13c5632637615`.
- **Round-2 delta:** one commit, `8544472a` "Correct CTLR_DIAG structural-zero comments". It changes only `hdl/common/csr/milan_csr.sv`, +10/-8, and every changed line is a `//!` comment.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md;
  - the issue #548 body and frozen acceptance;
  - the maintainer decision 5821224656 and the round-2 assignment 5822084957;
  - the author's round-2 REVIEW READY (5822209532);
  - REGISTER_MAP.md;
  - the full base..head diff and the round-2 delta;
  - public evidence at `29dce329:review-evidence/548-r1/author-r2/`;
  - exact-head hosted check runs, read-only.
- **Prior public findings:** read only after this round's own verdict and ledger were fixed.

## Verdict basis

The PR's round-1 NEGATIVE rested on one finding (R309-F1, which R308-1-F1 duplicates). That finding is closed at this head. The comment-free RTL is identical to the base, and nothing else in any lens's scope changed since round 1. The round-1 results for Robustness and Tests still stand at this head, and this round re-applied both lenses to the delta.

## Findings

No open BLOCKER, MAJOR or MINOR at this head.

### Resolution of prior public findings

| Prior finding | Status at 8544472a | Evidence |
|---|---|---|
| R309-F1 (MAJOR; Conformance, RTL, Docs): the CSR address-table and read-mux comments still called 0x6F4 a live probe/reply/eviction count | **CLOSED** | `hdl/common/csr/milan_csr.sv:761-765` and `:2397-2401` now read: STRUCTURAL ZERO (#548); reads 0 because the local counter source was deleted; the processor owns the monitor (Milan 5.4.5.3) but exports no replacement count; the address is kept for the ABI; zero is no measurement. This matches the page legend at `REGISTER_MAP.md:101` ("source is deleted and has no replacement"), the row `:1244`, the paragraph `:1248-1257`, and the port comment at `milan_csr.sv:309-312`. The reserved 0x6F8/0x6FC note is kept verbatim (`:766-767`). A search for the old live-count wording ("probes sent", "replies seen", "controllers shed", `evictions[`) finds 0 hits outside `docs/history` (`receipts/tree_search.txt`). |
| R308-1-F1 (MINOR; Conformance, RTL, Docs): the same defect | **CLOSED** | Same evidence as R309-F1. |
| R309-S1 / R308-1-S1 (SUGGESTION; Tests, Robustness): `axi_read` returns 0 on a read timeout and ignores RRESP | Retained as SUGGESTION | `tb/verilator/milan_dp/sim_nxn.cpp:612-626` is unchanged since round 1. The round-1 mutants showed the path delivers data at `:1596-1597`. Optional hardening in a separate change; it does not affect coverage. |
| R309-S2 (SUGGESTION; Docs): the listener-ladder "Timers per the reference" line at `REGISTER_MAP.md:1259-1260` directly follows the CTLR_DIAG paragraph | Retained as SUGGESTION | Unchanged since round 1 and outside #548's scope; it is a candidate for a new Issue. |
| R308-1-S2 (SUGGESTION; Docs): the 0x6F4 row omits a "Was: [31:24]/[23:12]/[11:0]" layout clause | Retained as SUGGESTION | `REGISTER_MAP.md:1244` is unchanged. Optional. |
| Out-of-scope observation in R308-1 (not a finding): `A_ACMPL_DBG` (0x6E8) is still labelled "RO live" at `milan_csr.sv:758` | Concur. It stays outside this PR | `REGISTER_MAP.md:1241` calls 0x6E8 STRUCTURAL ZERO. #548 is scoped to 0x6F4, so this needs its own Issue. It is not a finding against this lane and does not affect any lens here. |

## Per-lens results (this round, exact head 8544472a)

```text
[R309] PASS Conformance - hdl/common/csr/milan_csr.sv:309-312,761-765,2397-2401; docs/reference/REGISTER_MAP.md:101,188,1244,1248-1257; docs/findings/117_GPTP_SILICON_EVIDENCE.md:468-474,524; receipts/tree_search.txt - Acceptance 2 checked against the decision 5821224656 and assignment 5822084957 items 1-3. RTL comments, REGISTER_MAP and the #117 page now all state the STRUCTURAL ZERO verdict. Items 1-3 are met. Test_builder and docs/history are untouched (receipts/delta_structure.txt).
[R309] PASS RTL - receipts/strip_compare_base_head.txt, receipts/strip_compare_r1_head.txt, receipts/delta_structure.txt, receipts/lint_csr_base_head.txt - All 137 tracked HDL files are comment-free identical to 573f0052 and to e41703b2. A nonzero-tie control at milan_datapath.sv:3206 is detected. No non-comment HDL line is added or removed. The four gitlinks are identical to the base. Verilator 5.050 lint-only on milan_csr.sv returns 0 at both base and head.
[R309] PASS Robustness - hdl/milan/milan_datapath.sv:3206; hdl/common/csr/milan_csr.sv:2402; receipts/strip_compare_base_head.txt - The delta is comments only, so no reset, backpressure, decode or malformed-input behaviour can change. The round-1 mutation evidence (nonzero ties read back at sim_nxn.cpp:1596-1597) still applies to identical comment-free RTL.
[R309] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:1594-1597 (unchanged since e41703b2: receipts/delta_structure.txt); exact-head hosted runs receipts/hosted_checks_exact_head.txt - The zero pin and its round-1 mutant kill still apply because the compiled RTL and testbench are unchanged. Hosted rtl-fast, verilator-suites (shards 0-4) and yosys-portability (shards 0-3) passed at 8544472a.
[R309] PASS Docs - hdl/common/csr/milan_csr.sv:761-765,2397-2401; REGISTER_MAP.md:32,188,1244,1248-1257; receipts/tree_search.txt - No current statement anywhere in the tracked tree (top repo and checked-out submodules) calls 0x6F4 or CTLR_DIAG live. The remaining "departing-controller monitor ... live/served" statements (REGISTER_MAP.md:32, KL_pp_shadow.sv:47, FR_NFR.md:147, MILAN_COMPLIANCE_MATRIX.md:144) describe the processor monitor, which is correct. docs/history has one frozen hit and is unchanged. Hosted docs-check and docs-check-no-git passed at the exact head.
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #548 acceptance; decision 5821224656; assignment 5822084957; `milan_csr.sv:309-312,761-765,2397-2401`; `REGISTER_MAP.md:101,188,1244,1248-1257`; `117_GPTP_SILICON_EVIDENCE.md:468-474,524`; tree search | R309-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| RTL | CLEAN | comment-free comparison of all 137 HDL files against 573f0052 and e41703b2, with control; non-comment-line scan; gitlinks; Verilator lint of milan_csr.sv at base and head | R309-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| Robustness | CLEAN | `milan_datapath.sv:3206`; `milan_csr.sv:2402`; comment-free identity; round-1 mutation results (still valid at identical RTL) | R309-2 (delta); R309-1 at e41703b2 for the mutants | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| Tests | CLEAN | `sim_nxn.cpp:1594-1597`, `:612-626` (unchanged since e41703b2); exact-head hosted verilator-suites and rtl-fast | R309-2 (delta); R309-1 at e41703b2 for the runs | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| Docs | CLEAN | RTL `//!` register comments; REGISTER_MAP.md; 117 page; tree search including submodules; hosted docs-check (both modes) | R309-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |

**Why the round-1 heads are valid ancestors for Robustness and Tests:** the round-1 Robustness and Tests evidence came from e41703b2, which is a parent of 8544472a. Between the two, nothing in either lens's scope changed except HDL comments. `receipts/strip_compare_r1_head.txt` shows the comment-free RTL is identical, and `tb/` and `docs/` are byte-unchanged. So this round's coverage of both lenses is banked at 8544472a.

## Probes and commands run this round

- **`scripts/strip_compare.py`** compares comment-stripped HDL between two commits and plants a nonzero-tie control.
  - 573f0052..8544472a: rc=0.
  - e41703b2..8544472a: rc=0.
- **`scripts/tree_search.sh`** runs a tree-wide `git grep` at the head. Its output is `receipts/tree_search.txt`.
- **Scope and structure checks** (`receipts/delta_structure.txt`):
  - the gitlink diff;
  - a scan for non-comment HDL lines;
  - that docs/history and test_builder are untouched;
  - `git diff --check`.
- **Pinned Verilator 5.050 lint-only** on `milan_csr.sv` extracted by `git archive` at the base and at the head. Both return rc=0 (`receipts/lint_csr_base_head.txt`). The tool identity is in `receipts/verilator_identity.txt`; its hash is of the wrapper script.
- **Author evidence cross-check:**
  - the author's `round2.patch` is byte-identical to this round's `receipts/diff_round2_delta.patch` (sha256 129438bd...);
  - the author's tree search and comment-free identity agree with this round's own results;
  - this round's search pattern is broader (it adds `departing.controller`, `evictions[`, the old field wording, and the checked-out submodules).
- **Exact-head hosted check runs**, read-only (`receipts/hosted_checks_exact_head.txt`):
  - all executed jobs succeeded: rtl-fast, verilator-lint, verilator-suites with shards 0-4, yosys-elaboration, yosys-portability with shards 0-3, docs-check in both modes, bdd-conformance, elaborate, wire-accountability, full-ci-gate and changes;
  - "Physical gPTP (nightly and manual)" was SKIPPED. That is not an executed job and not hardware evidence;
  - the legacy combined commit-status API reports `pending` with no status contexts, while every check run completed.
- **Clone state after the review** (`receipts/clone_final_state.txt`):
  - HEAD, tree and index match `b7a11e8d`;
  - there is no worktree or index diff and no untracked file;
  - the four gitlinks are unchanged.
  - No probe modified the clone: the lint used `git archive` extracts under scratch.

## Real limits

- This round did not rebuild or run the `milan_dp` timed notification leg or its mutants. It relies on:
  - the round-1 R309 build and mutant results at e41703b2;
  - comment-free identity of all HDL;
  - byte-unchanged `tb/`;
  - exact-head hosted verilator-suites.
- No full parent, PP, gPTP, Yosys or builder bank was run, as assigned. The docs gates were not re-run locally; exact-head hosted docs-check (both modes) and the author's receipts cover them.
- The comment stripper is a lexical tool, not a parser. The Verilator lint at both heads and the author's independent identity script support it.
- The `external` submodule is not checked out in this clone, so the submodule search covered only gptp-processor, protocol-processor and verilog-axis.
- Physical calibration was NOT RUN. The skipped physical/field contexts are not hardware proof.

## Pending manager duties

- Build and validate the final current-`dev` candidate merge result at the merge turn. The source base is 573f0052 and live `dev` was ffcbd33d at assignment. This source-head review is not candidate evidence.
- Own hosted and local-replica acceptance at the exact head. The legacy combined status reads `pending` with no contexts; confirm branch protection reads the check runs.
- Merge only with explicit maintainer authorization, then run post-merge containment and close #548.
- Open a separate Issue for:
  - the out-of-scope `A_ACMPL_DBG` "RO live" comment (`milan_csr.sv:758`);
  - if wanted, the retained suggestions (R309-S1/R308-1-S1 `axi_read` timeout/RRESP; R309-S2 timers line; R308-1-S2 "Was:" layout).

R309-2 FINISHED
