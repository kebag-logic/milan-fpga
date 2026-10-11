[R598] POSITIVE - exact head c0cba330fd485e52fcb90d5ccc69169edf9f0c2b

# R598-2: internal cleared-context review of PR #722 (issue #640, Mark II lane M5, plan L8), round 2

- Head under review: `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b`, tree `bd80ea775d965f843609b1282cce9920279c02f0`. Verified in the review clone: the index writes the same tree, every tracked file's bytes and mode equal its blob, and there are no leftovers. `third_party/verilog-axis`, `protocol-processor` and `gptp-processor` are at their gitlinks and clean (`receipts/verify_clone.log`).
- Round-1 head: `988ec7f653d0a21e0f7b40b03b8c74155d8962cf`. Source base: dev `e8454e2751d05b02ee8e5a571857589ab358ab86`. Live dev: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.
- Delta under review: `988ec7f6..c0cba330`, three one-line commits, each with one parent and no trailers (`5747be31`, `80e41fc1`, `c0cba330`). It touches two files:
  - `docs/design/MARK_II_AREA_PLAN.md` (+4/-2);
  - `hdl/common/csr/milan_csr.sv` (six `//!` lines in one banner).
  - The live PR body changed too.
- Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the issue #640 body;
  - the M5 assignment (6098404907), the manager rulings D1/D3/D7/D8 (5990755268), the owner decisions (5991591637, 5993114362, 6081706413) and the round-2 assignment (6105372796);
  - the executor's TAKEN and both REVIEW READY comments (6098441921, 6104904445, 6105430562);
  - `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:618-669`, `syn/ooc/pp_resource_gate.py` and `hdl/milan/milan_datapath.sv`;
  - the public evidence `review-evidence/640-m5-r1` at `648503cf`. Its `author/HANDOFF.md` and `author/PR-BODY.md` sha256 values equal its MANIFEST.json, and their git blob ids equal the tree's.
- I wrote my own verdict and ledger before reading the prior review reports (`receipts/independent_pass_before_prior_findings.md`). I then read R598-1 and R599-1 to settle their findings (section "Prior findings").

**Verdict: POSITIVE.** Every round-2 item the manager assigned is applied, verbatim where an exact text was prescribed. The RTL edit is comment-only: the token stream and line numbering are identical, so no netlist can change. No anchor is broken. The CSR suite and its planted defects pass at this head with round 1's exact figures. Two wording-only RESIDUE items and one SUGGESTION remain. None leaves a lens unclean.

## Findings

### R598-2-RES-1: RESIDUE (lens Docs). The PR body says the attribution's three figures all come from the route gate's sub-block list

- **Where:** the PR #722 body, section "Round 2", the first bullet: "These are the route gate's own sub-block figures for the M5 route." (`receipts/pr722_body_live_at_review.md`).
- **Evidence:**
  - The gate's sub-block scopes lie under `alinx_ax7101/milan_datapath/pp_shadow` (`syn/ooc/pp_resource_gate.py:108`, `:255-268`; movements are listed at `:395-408`).
  - `csr` is the sibling instance `milan_datapath/csr` (`hdl/milan/milan_datapath.sv:2445-2472` and `:8003-8040`). So the gate lists `wrapper` -342 and `u_pp` -344, but not `csr`.
  - `csr` -121 comes from the routed hierarchy report (HANDOFF r1 section 5), and the -227 is the remainder.
  - The figures themselves are correct and sum to -690. Only the stated source is wrong.
- **Impact:** A cold reader looking in the gate output for `csr` -121 will not find it. No figure, measurement or claim changes.
- **Exact fix:** replace that sentence with "The wrapper and `u_pp` figures are the route gate's sub-block figures for the M5 route; `csr` -121 is the routed hierarchy report's `milan_datapath/csr` scope, and about -227 is the remainder."
- **Verification:** re-read the PR body.

### R598-2-RES-2: RESIDUE (lens Docs). "nearly all of it in `u_pp`", when `u_pp` moved more than the wrapper that contains it

- **Where:** the PR #722 body, Description, bullet "Saving against the plan": "the processor wrapper -342, nearly all of it in `u_pp` (-344, nested inside the wrapper, not added)".
- **Evidence:** `u_pp` (-344) is nested in the wrapper (-342). So the rest of the wrapper moved +2, and `u_pp` is more than all of the wrapper's movement. The phrase follows the example text prescribed in round 1. The figures are right and disjoint.
- **Impact:** wording only. No figure changes.
- **Exact fix:** "the processor wrapper -342, which nests `u_pp` (-344; the rest of the wrapper moved +2; not added)".
- **Verification:** re-read the PR body.

### R598-2-S1: SUGGESTION (lenses Docs, Conformance). The partial-central consequence substitutes M5 alone, but the merge candidate carries M2's measurement too

- **Where:** `docs/design/MARK_II_AREA_PLAN.md:1027`, and the PR body's "Known limitations".
- **Evidence:**
  - The sentence is correct as stated: 37,957 + (600 - 121) = 38,436, which is 396 over 38,040 (`receipts/prescribed_text_check.log`).
  - Live dev `ac2c5e77` already holds "M2 intermediate measurement": a 34-LUT reproducible saving against M2's 200 estimate.
  - In the merged ledger, two lanes therefore sit below their planning figures. Substituting both gives about 38,602.
- **Optional:** at the merge turn or the week-4 re-measure (D8), state the combined consequence once instead of lane by lane. This is not required at this head.

## Prior findings on this PR: disposition at this head

| Finding | Disposition | Evidence at `c0cba330` |
|---|---|---|
| R598-1-F1 = R599-1-F2 (MINOR, Docs): the -686 attribution double-counted nested scopes | **RESOLVED** in the PR body | The prescribed disjoint text is present once and "-686" is gone (`receipts/prescribed_text_check.log`). Arithmetic: -121 - 342 - 227 = -690. The disjointness was checked against the hierarchy: `csr` and `pp_shadow` are siblings in `milan_datapath`, and `u_pp` is inside `pp_shadow`. Two wording residues remain (RES-1, RES-2). The executor reports a corrected HANDOFF (sections 5 and 7), but no round-2 HANDOFF is published, so that copy is unverified here (see the manager duties). |
| R599-1-F1 (MINOR, Docs, Conformance): the per-stream non-reproduction claim across non-comparable scopes | **RESOLVED** | `MARK_II_AREA_PLAN.md:1023-1024` carries R599-1's example text verbatim, and "do not reproduce" is gone. #649's 210.6 is `milan_csr` inside the `milan_datapath` synthesis (`649_...:623-657`). The slopes recompute from the published HANDOFF r1 tables over N 1 to 8, seven steps: base alone 11.9, proxy 62.3; M5 alone 49.1, proxy 56.0. |
| R598-1-S1 (SUGGESTION): the partial-central consequence | **APPLIED** | `:1027` holds the assignment's exact sentence, beside the M5 measurement. The PR body's "Known limitations" carries the same consequence. |
| R599-1 RES-1: the stale "four-way select" banner | **APPLIED** | `milan_csr.sv:1066-1068` carries RES-1's exact text after whitespace normalisation. `c0cba330` only reflows it: the word stream is the same sha256 at `5747be31` and `c0cba330`. |
| R599-1 RES-2: "measured" became "saved" | **APPLIED** | `MARK_II_AREA_PLAN.md:538` |
| R599-1 RES-3: "apart from the module name" | **APPLIED** | the PR body's `tb/verilator/csr/` row |
| R599-1-S1 (optional alternate placement directives) | **Not run**; optional, carried | No route this round, as the PR body discloses. |
| R598-1 / R599-1 observations: the stage-1 gate is guarded only by `milan_dp_mclk` mutant 13; the reference copy's em dashes | **Unchanged** | The RTL is token-identical to `988ec7f6`, and `tb/` is unchanged. |

## Executed evidence (this round, at the exact head)

| Run | Result | Receipt |
|---|---|---|
| Comment-only probe, `scripts/comment_only_probe.sh` (`988ec7f6` vs `c0cba330`) | rc 0. 3,225 = 3,225 lines. The only differing lines are 1066-1071, and each differs only after `//`. The Verilator preprocessor output is IDENTICAL both with and without `` `line `` directives at four shapes (ax7101 1x1_tdm8, ax7101 8x8, arty current, arty 4x4). All 7 `lock_mutants.py` anchors occur exactly once at both revisions. Generated includes and `configs/` are unchanged, and `tb/` is unchanged. | `receipts/comment_only_probe.log`, `.rc` |
| Sensitivity control, `scripts/pp_sensitivity_control.sh` | rc 0. A one-token code change (`\|` to `^` in stage 2) is detected, and a comment-only edit is not, so the comparison can fail. | `receipts/pp_sensitivity_control.log`, `.rc` |
| CSR suite, `MAKEFLAGS=w make` in `tb/verilator/csr` (pinned Verilator 5.050, clean build) | rc 0. Legacy legs 408/408/121/44/408 and reset bits 408, 0 failures. lock1: 5/5, 340,861 cycles, 28,167 random-traffic reads, 0 mismatching cycles. lock8: 5/5, 374,265 cycles, 22,750 reads, 0 mismatching cycles. `lock_mutants.py`: 8 checks, 8 PASS (control plus 7, each failing its named check). These equal the executor's figures for both rounds. | `receipts/csr_suite.log`, `.rc`, `.env` |
| Prescribed-text and arithmetic check, `scripts/prescribed_text_check.py` | rc 0, 10/10 | `receipts/prescribed_text_check.log`, `.rc` |
| Markdown gates under the pinned renderer, installed into a private hash-pinned venv in scratch (`receipts/md_venv_freeze.txt`): `docs_check.py` (with and without git metadata), `check_em_dash.py --base e8454e27` (0 findings over 68 added lines) and `--base 988ec7f6` (0 over 4), `check_doc_style.py`, `check_gptp_docs.py`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `gen_module_matrix.py --check` | all rc 0 | `receipts/gate_*` |
| RTL-file text gates: `check_sv_idiom.py`, `check_hygiene.py --check`, `git diff --check e8454e27 HEAD` | rc 0 | `receipts/gate_*` |
| The system interpreter's first attempts at `check_em_dash`, `gen_toc --check` and `--verify-anchors` | rc 2 ("cannot judge": the renderer was absent). Superseded by the venv runs above, which overwrote those receipts. | as above |
| Hosted check-runs at the exact head, read-only, 2026-10-11T04:51:09Z | Success: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0-3, Verilator shard 3/5. In progress: `docs-check`, `elaborate`, `firmware-unit`, Verilator shards 0, 1, 2 and 4. Skipped (not executed): "Physical gPTP (nightly and manual)". | `receipts/hosted_check_runs_c0cba330.tsv` |
| Clone integrity after all runs, `scripts/verify_clone.sh` | rc 0, CLONE VERIFIED | `receipts/verify_clone.log`, `.rc` |

## Per-lens results (artifact at this head)

```text
[R598] PASS Conformance — issue #640 comment 6105372796 items 1-4 vs PR #722 body (receipts/pr722_body_live_at_review.md) and docs/design/MARK_II_AREA_PLAN.md:538,1023-1024,1027; receipts/prescribed_text_check.log — every assigned item is applied (prescribed texts verbatim, the old claims gone); the disjoint attribution sums to -690 over sibling scopes (milan_datapath.sv:2445-2472, :8003-8040; pp_resource_gate.py:108); the per-stream slopes and 38,436/+396 recompute from published tables; the delta changes no RTL behaviour, so the round-1 acceptance evidence stands
[R598] PASS RTL — hdl/common/csr/milan_csr.sv:1063-1072 vs :1153-1161, :2636-2662; receipts/comment_only_probe.log, receipts/pp_sensitivity_control.log — the banner now matches the RTL (stage 2 is `r_data <= live_mux_q | shadow_qq` on rd_pend2); the change sits only in comment text, with no pragma or lint directive; the preprocessed token stream and line numbering are identical at four shapes, so no netlist or source-attribute change is possible
[R598] PASS Robustness — receipts/comment_only_probe.log, receipts/csr_suite.log (lock1/lock8 reset-values, snapshot-freshness, lockstep with periodic resets and random backpressure) — no reset, ordering, backpressure or configuration path changed; the reset and random-traffic lockstep phases still hold 0 mismatching cycles at both shipping shapes at this head
[R598] PASS Tests — tb/verilator/csr/lock_mutants.py:50-80, gen_lockstep.py:37-38,89-97; receipts/csr_suite.log, receipts/comment_only_probe.log — tb/ is unchanged; all 7 exact-text mutation anchors match once at this head; the frozen-reference digest check passes (lock legs built); lock_mutants 8/8 with each defect failing its named check; no tb/**/*.patch exists (the only *.patch files are under sw/litex/), and the only other copy of the old banner text is the SHA-pinned milan_csr_ref.sv, which is not derived from the head
[R598] PASS Docs — docs/design/MARK_II_AREA_PLAN.md:538,1016-1028; hdl/common/csr/milan_csr.sv:1063-1071; PR #722 body; receipts/gate_*.log — figures are traced to the HANDOFF r1 tables and #649 :623-657; the docs gates are rc 0 under the pinned renderer; R598-2-RES-1/RES-2 are wording-only residue in the PR body and do not affect coverage
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round-2 assignment 6105372796; PR body; `MARK_II_AREA_PLAN.md:538,1023-1027`; `649_RESOURCE_MAP_AND_SENSITIVITY.md:623-657`; HANDOFF r1 sections 1, 4 and 5; `pp_resource_gate.py:108,255-268,395-408`; `milan_datapath.sv:2445-2472,8003-8040`; `prescribed_text_check.log` | R598-2 | `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b` |
| RTL | CLEAN | `milan_csr.sv:1063-1072` against the RTL at `:1153-1161,2636-2662`; `comment_only_probe.log`; `pp_sensitivity_control.log` | R598-2 | `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b` |
| Robustness | CLEAN | `comment_only_probe.log` (no behavioural change); `csr_suite.log` lock1/lock8 reset, freshness and random-traffic phases | R598-2 | `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b` |
| Tests | CLEAN | `tb/verilator/csr/{lock_mutants.py,gen_lockstep.py,Makefile}` (unchanged since `988ec7f6`); anchor counts; `csr_suite.log` including `lock_mutants.py` 8/8 | R598-2 | `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b` |
| Docs | CLEAN (RES-1 and RES-2 are residue only) | `MARK_II_AREA_PLAN.md:538,1016-1028`; the `milan_csr.sv` banner; PR #722 body; docs gates `receipts/gate_*` | R598-2 | `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b` |

Coverage note: the round-1 body of the change (`e8454e27..988ec7f6`) was covered by R598-1 and R599-1 at `988ec7f6`. Within the scope of RTL, Robustness and Tests, nothing changed since then except comment text. This round re-applied those lenses at this head by proving token identity and by re-running the CSR suite and its planted defects. It did not re-derive the round-1 equivalence argument.

## Real limits

- This is a delta review. The round-1 RTL equivalence argument, the reviewer mutant sets and the non-shipping lockstep variants are R598-1's and R599-1's, at `988ec7f6`. They carry to this head because the token stream is identical. They were not repeated.
- Not run at this head, because the RTL is token-identical and `tb/`, `syn/`, `sw/` and `configs/` are unchanged:
  - `tcam_csr`, `milan_dp` (any leg), `milan_dp_mclk`, `milan_dp_render`, `capture_coherence`, `follow_ring`, `pp_shadow`, `milan_dp_gptp`;
  - firmware host tests, builder, `behave`;
  - lint ratchet, Yosys;
  - `measure_naming`, `measure_fail_fast`, `check_todo_ownership`, `measure_test_evidence`, `check_port_contracts`, `check_rtl_source_lists`;
  - the gate self-tests.
- GNU make here is 4.4.1, not the 4.3 the PR names for the CSR suite's Makefile check.
- No Vivado, route or resource-gate run. The figures (-690, -342, -344, -121, the OOC tables) are the executor's published round-1 receipts. This round checked their arithmetic and scope structure, not their production.
- No round-2 HANDOFF or PR-BODY evidence is published. The PR body was verified live, at 2026-10-11T04:5x UTC; the HANDOFF correction the executor reports is not verified.
- Hosted contexts were partly in progress at the snapshot, and the manager owns hosted and act acceptance. The PR's `rtl-fast` context did not appear by that name in the check-run list at the snapshot.
- No manager source bank ran at this head, and none is claimed or inferred. Physical calibration was NOT RUN. The skipped field/physical context is not hardware proof.

## Pending manager duties

- Carry R598-2-RES-1 and R598-2-RES-2 (exact texts above) to the residue checklist. Weigh R598-2-S1 at the merge turn or the week-4 re-measure.
- Publish the round-2 HANDOFF and PR-BODY evidence, so that the corrected HANDOFF sections 5 and 7 can be checked publicly (R598-1-F1's "if republished" clause).
- Accept the hosted contexts at the exact head: `docs-check`, `elaborate`, `firmware-unit`, Verilator shards 0, 1, 2 and 4, and `rtl-fast`. Run the manager-owned act replication.
- At the merge turn, build and validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, and link the receipts. That candidate also merges M2's ledger entries into `MARK_II_AREA_PLAN.md` beside M5's.
- Collect the external round-2 review. Two independent positives are required.
- Rule on the L8 saving that falls below its estimate (D8 week-4 re-measure). Post-merge: the bench boot readback and containment.

Packet contents:
- `REPORT.md`;
- `scripts/`: `comment_only_probe.sh`, `pp_sensitivity_control.sh`, `prescribed_text_check.py`, `verify_clone.sh`;
- `receipts/`: raw logs and rc files, with home-directory paths redacted as `<HOME>`.

Only files listed in `MANIFEST.sha256` are published. `scratch/` is not published.

R598-2 FINISHED
