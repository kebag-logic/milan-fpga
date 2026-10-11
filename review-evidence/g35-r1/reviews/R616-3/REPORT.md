[R616] POSITIVE - exact head 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c

# R616-3 internal independent review: FPGA-gPTP PR #80 (issue #35), delta after the main merge

Exact head `49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c`, tree `526a366bd9aff5cd8d0ad0278217dab22ac921ea`. The parents are `a70e38804cb16435c089d024c58e8c3fb4d39ff6`, the pre-merge head that R616-2 and R617-2 reviewed POSITIVE, and `155de13789ac85bab7a14bea0ae86d1c376b490a`, main with PR #79 and PR #81. Their merge base is source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. Main is still `155de137`, and that is the PR's recorded base.

## Summary

- The merge is a plain merge plus the conflict resolution. Recomputing the merge of the two parents gives conflicts in `README.md` and `docs/MANAGER.md` only. The published tree differs from that recomputed tree in those two files only, and only by:
  - removing the conflict markers;
  - removing the branch-side lines that main had already replaced;
  - dropping main's #35 entry: the README bullet and the MANAGER.md open-risks table row.
- Every other file is a plain merge. The `hdl/`, `tb/`, `bench/` and `scripts/` trees have the same tree ids as at `a70e3880`.
- The branch's own changes survive the merge unchanged. Measured against main they have the same patch-ids as against base, for:
  - `docs/HDL_DEVELOPER.md`, `docs/INTEGRATION.md` and `docs/TEST_DEVELOPER.md`;
  - the parser RTL and `sim_main.cpp`.
- `docs/SOURCE_EVIDENCE.md` is the one exception, and only because main rewrote one context row. The hunk contents are identical.
- Main's own changes reach the head byte-for-byte on every path the branch did not touch.
- The merged README and MANAGER.md:
  - keep all of #48's gap list, table and parent citations at `ac2c5e77`, and those citations resolve at the parent;
  - carry no #35 open-risk entry, which is correct because this PR closes #35.
- `docs/INTEGRATION.md:84-106` still states the ruled `rx_err_i` contract, and the parent tie-off citation still holds (`KL_gptp_shadow.sv:666` at `ac2c5e77`).
- At this head, run with the pinned Verilator 5.050:
  - `make docs`, `make contract` and `make lint` return rc 0;
  - every `make tb` component passes;
  - the parser suite's output is identical to the pre-merge head's.
- New this round: one RESIDUE (PR-body wording) and one SUGGESTION (a docs-gate gap that predates this PR). No open BLOCKER, MAJOR or MINOR.

## Reconstruction (order followed)

1. The repository has no `AGENTS.md`, `CONTRIBUTING.md` or `.gitmodules`. Read: `README.md`, `docs/README.md` (truth order), `docs/MANAGER.md`, `Makefile`.
2. Issue #35:
   - body and frozen acceptance;
   - lane scope ruling (safer default);
   - netlist ruling (comment 6105366046: a hierarchical +1 `$mux` is accepted);
   - bank ruling 6105869522 (writes up to and including the flagged byte; none after; no stale data in the next accepted event);
   - author REVIEW READY posts.
   Issue #48 and PRs #79 and #81, for the merged-in authorities.
3. Interface authorities:
   - the parser header (`hdl/wire/KL_gptp_rx_parser.sv:49-66`), port (`:113-116`), latch (`:652`) and eof gate (`:632`);
   - `docs/INTEGRATION.md:63-106`;
   - parent `ac2c5e77` files fetched read-only: `milan_datapath.sv:73`, `GPTP_PLANE.md:6,43-49,350-366`, `ARCHITECTURE_HW_SW_SPLIT.md:165-175`, `README.md:167-170`, `docs/guides/gptp/MANAGER.md:33-35` and `KL_gptp_shadow.sv:666`.
4. `git diff 5dce647a..49b9d0f`, history and merge topology, then the delta `a70e3880..49b9d0f` and the recomputed plain merge.
5. Public evidence at `kebag-logic/milan-fpga@3e8c823a/review-evidence/g35-r1`: the author round-2 gate receipts at `a70e3880` (identity, rc and counts). Manager comments 6106554371, 6106693225 and 6106715000.
6. Prior public review findings (R616-1, R617-1, R616-2, R617-2), read only after my independent verdict and ledger were written. Pre-read record: `receipts/independent_verdict_before_prior_findings.md`, timestamped 2026-10-11T08:00:25Z.

## Lenses

### Conformance: CLEAN

- Contract versus authority: the latch at `:652` sets `bad_r` on every valid byte, below the sof arm, and the eof term is at `:632`. This matches:
  - the lane ruling (any byte, exactly one drop, no event);
  - the bank ruling (no write after the flagged byte's edge);
  - the header (`:49-66`), the port (`:113-116`) and `docs/INTEGRATION.md:84-106`.
  The merge changed none of these: the `hdl/` tree id equals `a70e3880`'s, and the INTEGRATION.md branch hunk has the same patch-id.
- #48 consistency:
  - The merged `README.md:21-35,49-55` and `docs/MANAGER.md:16-27,100-116,120-124` are main's text with only the #35 entry removed (`receipts/verify_merge.txt`).
  - Each #48 parent citation still says what the guide claims at `ac2c5e77`: default on at `:73`, fabric owner at `:6`, verification-only off at `:49` and `ARCH:165-175`, the gaps at `guides/gptp/MANAGER.md:33-35`, and the asymmetry exclusion at `:350-366` (`receipts/parent_citations_ac2c5e77.txt`).
  - #48's acceptance ("remaining donor and hardware gaps stay visible") still holds: #58, parent #117 and parent #64/#488 remain in both files.
- Dropping #35 is consistent with this PR's `Closes #35`. `docs/SOURCE_EVIDENCE.md:46` lists #35 under closed work. `docs/INTEGRATION.md:102` keeps "Current parent integration drives `rx_err_i` low", which matches the parent at `KL_gptp_shadow.sv:666`.

### RTL: CLEAN

- The merge left the `hdl/` tree unchanged (`6c4a8031…` at both `a70e3880` and head). The parser patch-id against main equals its patch-id against base.
- Independent read of `:385-405`, `:407-426`, `:623-653`:
  - the latch sits after the sof clear, so a first-byte flag survives it;
  - the eof byte's own flag reaches `fin_ok_r` directly;
  - later writes are gated by `!bad_r` (for example `:478`).
- `make lint` rc 0 with Verilator 5.050 (`receipts/head_make_lint.log`). No other RTL file differs from main.

### Robustness: CLEAN

- `git diff --check` is clean for `155de137..head` and for `a70e3880..head`.
- No tracked file at head contains a conflict marker.
- No file mode differs between the recomputed merge and head (`receipts/tree_hygiene.txt`).
- Disposable docs fault probes on exact-head exports (`scripts/docs_probes.sh`, `receipts/docs_probes.txt`, `receipts/probes/`):

  | planted fault | `make docs` |
  |---|---|
  | none (control) | accepted |
  | parser anchor `#L393` shifted to `#L392` | rejected (rc 2) |
  | leftover conflict markers in README.md | accepted |
  | `## Open risks` heading renamed | accepted |
  | stale #35 row restored | accepted |

- The gate therefore would not have caught a bad conflict resolution. I verified the resolution directly: `scripts/check_md_anchors.py` resolves every intra-doc fragment at head (8 current-guide fragments OK, 0 unresolved, 0 markers; `receipts/md_anchors_head.txt`). Run on the probe trees, the same script rejects the planted markers and the broken `#open-risks` anchor (`receipts/md_anchors_probe_controls.txt`), so the check is not vacuous. The gate gap predates this PR (main's `check_docs.py:240` drops fragments) and is recorded as R616-3-S1.
- The merged-in OOC clock checker selftest passes at head: 30 arms (`receipts/head_ooc_clock_selftest.log`). No Vivado run.

### Tests: CLEAN

Run at exact head, in disposable exports, with the pinned Verilator `5.050 2026-07-01 rev v5.050` (`receipts/verilator_identity.txt`):

| gate | result at head | receipt |
|---|---|---|
| ucpu | 768/768 | `head_make_tb.log` |
| parser | 337/337; mutation arm 9/9, each mutant failing all of its named checks | `head_make_tb.log` |
| engine | 1613/1613 x3 (default, seeded, Sync-seeded) | `head_make_tb.log` |
| engine mutation arm | 34/34 (control plus 33 caught) | `head_engine_mutants_parallel.log` |
| gaskets | 81/81 + 5/5 | `head_tb_gaskets.log` |
| tsngen | 288/288 + 4/4 | `head_tb_tsngen.log` |
| bench tag test | PASS | `head_tb_bench.log` |
| `make contract` | rc 0, PHC contract PASS | `head_make_contract.log` |
| `make lint` | rc 0 | `head_make_lint.log` |
| `make docs` | rc 0; 11 current / 17 historical pages; 20 exact anchors; all selftests PASS | `head_make_docs.log` |

- The parser suite's summary and INFO output at head is byte-identical to the pre-merge head's, run the same way (`receipts/parser_out_diff.txt`, rc 0). It matches the PR body's before/on/after table and the author's round-2 receipt at `a70e3880`.
- See Limits for how `make tb` was split.

### Docs: CLEAN (one RESIDUE)

- Merged `README.md`:
  - Known risks `:49-55` lists #58, parent #117 and parent #64/#488, plus the manager-guide pointer;
  - there is no #35 line, and every current-guide link and fragment resolves.
- Merged `docs/MANAGER.md`:
  - the open-risks table `:100-106` has three rows, all #48's;
  - the parent paragraphs `:108-114` and the line "Parent gitlink updates require separate review." (`:116`) survive from main;
  - the branch's earlier "Physical acceptance remains product-specific." bullet is gone, correctly, because main replaced it with the parent #117 row.
- `INTEGRATION.md`, `SOURCE_EVIDENCE.md` (anchors `#L393` and `#L475` exact at head) and `HDL_DEVELOPER.md`/`TEST_DEVELOPER.md` hold both sides' content without interleaving.
- The PR body still says the #35 "risk bullets" were removed from both files; after the merge, the MANAGER.md entry is a table row (R616-3-RES1).

## Findings (new this round)

### R616-3-RES1: RESIDUE (Docs)

- **Artifact:** the PR #80 body, `## Change`, the "Docs" list: "The #35 risk bullets are removed from `README.md` and `docs/MANAGER.md`."
- **Evidence:** after the merge of main (`155de137`), the MANAGER.md entry removed at head is the open-risks table row "Mid-frame receive errors | Fix in review; not merged here", not a bullet (`receipts/verify_merge.txt`).
- **Impact:** prose precision in the PR body only. It changes no code, test, measurement, verdict or claim.
- **Required outcome (exact fix):** replace that sentence with "The #35 risk entries are removed: the README known-risks bullet and the `docs/MANAGER.md` open-risks table row."
- **Verification:** compare against `git diff 155de137 49b9d0fd -- README.md docs/MANAGER.md`.
- The manager carries this to the residue checklist.

### R616-3-S1: SUGGESTION (Docs, Robustness)

- **Artifact:** `scripts/check_docs.py:240`. It strips the `#fragment` of local links, and no gate scans for merge-conflict markers.
- **Evidence:** planted conflict markers in README.md, and a renamed `## Open risks` heading that breaks `#open-risks` from `README.md:55`, `docs/INTEGRATION.md:49` and `docs/history/v1/PROJECT_STATUS.md:26`, both pass `make docs` (`receipts/docs_probes.txt`).
- **Impact:** a future bad merge resolution in the guides would pass the docs gate. The gap predates this PR, and this head is clean.
- **Optional outcome:** in a separate change, resolve local Markdown fragments against heading slugs and reject conflict-marker lines, each with a selftest arm.
- **Verification:** the two planted probes go red; the clean tree stays green.
- Not required for this PR.

## Prior public findings: disposition at this head

| ID | Severity | Lenses | Disposition at 49b9d0fd | Evidence |
|---|---|---|---|---|
| R617-F1 (R617-1) | MAJOR | Conformance, RTL, Tests, Docs | RESOLVED, unchanged by the merge | Bank ruling 6105869522; the before/on/after oracle and stale-word checks run at head with output identical to `a70e3880` (`parser_out_diff.txt`); `hdl/` and `tb/` tree ids unchanged |
| R616-1-RES1 | RESIDUE | Docs | RESOLVED | The exact sentence remains at `KL_gptp_rx_parser.sv:60-63` |
| R616-1-S1 | SUGGESTION | Docs, Tests | RETAINED (optional) | `docs/SOURCE_EVIDENCE.md:12` still links the parser without an anchor. It is related to, but distinct from, R616-3-S1 |
| R616-1-S2 | SUGGESTION | Tests, Robustness | RETAINED IN PART (optional) | Announce was added to the oracle. Padding, other types, runts and adjacency remain probe-only |
| R616-2-RES1 | RESIDUE | Docs | RETAINED; carried by the manager (milan-fpga #495) | `docs/TEST_DEVELOPER.md:96` still reads "Proves refused frames leave no stale words." and `tb/verilator/parser/README.md:16` "It proves refused frames leave no stale words." Exact fixes as stated by R616-2: `- Proves no refused frame's word reaches the next accepted event.` and `It proves no refused frame's word reaches the next accepted event.` |
| R616-2-S1 | SUGGESTION | Tests, Robustness | RETAINED (optional) | The sweep frames still end at the declared length; no padded-error case is committed |

R617-2 raised no new finding ID; it dispositioned the R616 items above.

## Reviewer-owned ledger

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #35 body, lane ruling, netlist ruling 6105366046, bank ruling 6105869522; parser header `:49-66`, port `:113-116`, latch `:652`, eof gate `:632`; `INTEGRATION.md:63-106`; #48 body; parent `ac2c5e77` cited lines and tie-off `KL_gptp_shadow.sv:666` | R616-3 | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| RTL | CLEAN | `hdl/` tree id equal to `a70e3880`; parser patch-id equal against base and main; independent read of the latch, eof and write gates; `make lint` rc 0 | R616-3 | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| Robustness | CLEAN | Recomputed plain merge (only README.md and MANAGER.md differ: the resolution); per-path main/branch blob comparison; `diff --check`; marker and mode scan; five docs fault probes; independent anchor resolver with planted controls; OOC checker selftest | R616-3 | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| Tests | CLEAN | ucpu 768; parser 337 + arm 9/9; engine 1613 x3; engine arm 34/34; gaskets 81 + 5/5; tsngen 288 + 4/4; bench tag PASS; contract PASS; parser output identical to `a70e3880` | R616-3 | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |
| Docs | CLEAN (RESIDUE R616-3-RES1; R616-2-RES1 retained) | Merged README.md and docs/MANAGER.md; INTEGRATION.md, SOURCE_EVIDENCE.md, HDL/TEST guides, parser README; `make docs` rc 0; intra-doc fragments; PR #80 body | R616-3 | 49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c |

## Real limits

- **`make tb` was not one uninterrupted invocation.** The first run, concurrent with docs, contract and lint, passed ucpu, parser plus its arm, and engine x3, then was stopped by a session time limit inside the serial engine mutation arm. The remaining targets were rerun individually at the same head:
  - gaskets, tsngen and bench through their own Makefiles;
  - the engine arm through `scripts/engine_mutants_parallel.py`. That driver imports the head's `tb/verilator/engine/mutants.py` and calls its `stage`, `generate_image`, `build`, `run_harness` and `verdict` with the same per-mutant decision logic; only the scheduling is concurrent (12 workers).
  
  No single `make tb` rc is claimed.
- **No parent work at this head.** I ran no parent elaboration, Yosys, equivalence or ROM-ledger check here, because a parent bank was not allowed. The parent-identity evidence is the author's at `a70e3880`, whose `hdl/` tree is identical to this head's.
- **No Vivado.** The OOC run was not executed; only the checker selftest ran.
- **No hosted or manager evidence at this head.** There are no check-runs, statuses or Actions runs at this head, and the repository has no workflow directory. No manager source bank ran at this exact head, and none is claimed or inferred. The author's published gate receipts are at `a70e3880`, not at this head; my own runs above are the source-head execution evidence for `49b9d0fd`.
- **No hardware.** Physical calibration was NOT RUN, there is no hardware evidence, and field skips are not hardware proof.
- **Parser-level evidence only.** No engine bench drives `rx_err_i`.

## Pending manager duties

- At the merge turn, build and validate the final current-dev candidate with the builder and native banks (source base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`), and link the receipts on the PR. Candidate validation is distinct from this source-head execution.
- Own hosted and local-workflow acceptance.
- Carry R616-3-RES1 and the retained R616-2-RES1 to the residue checklist. Decide on R616-1-S1, R616-1-S2, R616-2-S1 and R616-3-S1, all optional.
- Parent adoption stays separate: review the new gitlink together with its ROM-ledger row.

## Packet

- `scripts/`: `verify_merge.sh`, `docs_probes.sh`, `check_md_anchors.py` and `engine_mutants_parallel.py`. Each script's header gives its usage.
- `receipts/`: raw logs, rc files and API snapshots. In the build logs, the host install prefix of the pinned toolchain is replaced with a neutral label; no other byte changed (`receipts/REDACTIONS.txt`).
- `MANIFEST.sha256` lists every published file. The clone was never modified: 107 tracked blobs and modes match HEAD, the index equals the HEAD tree, the status is empty including ignored files, and there are no gitlinks (`receipts/clone_integrity.txt`).

R616-3 FINISHED
