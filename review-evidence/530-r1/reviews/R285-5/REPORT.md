[R285] POSITIVE - exact head 8ffd6c616840b161891e2eb714a7ddbbb72c7a0d

Round R285-5. External independent review of kebag-logic/milan-fpga issue #530 and PR #549, round 4 delta. The tree is `ff757231ac361ff2a07f3bb3e838bba267e0f056`. This round covers the whole delta `f814d37d..8ffd6c61`: the dev merge `6556effc`, then `77068c9a` and `8ffd6c61`. RTL and Docs were applied to that delta at the exact head. Conformance, Robustness and Tests carry: the delta changes no logic, harness, Makefile, BDD step or gitlink, and I re-ran the #530 leg and one gate mutant at this head as spot evidence.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open from this round or from any prior round. One SUGGESTION is new, S1 (RTL, Docs). It does not affect coverage. My R285-4 F1 is resolved.

The independent verdict and ledger were written before I read any prior finding: `receipts/08_independent_verdict_before_prior_findings.txt`. Reading the prior findings afterwards did not change either one.

## Findings

### S1 - SUGGESTION - lenses: RTL, Docs - `milan_datapath.sv:6597` still says "the licensed source's own bits"

- **Where:** `hdl/milan/milan_datapath.sv:6597`, in the ADMITTED paragraph: "The lead shows on the licensed source's own bits:".
- **Evidence:**
  - The list that follows (`:6598-6601`) includes `LWSRP_STATUS[6] (ACTIVE ORed over sources)`. That is `lwsrp_res_active = |pp_cd_srp_active_w` (`:6655`), not one source's own bit.
  - `8ffd6c61` removed "own" from the same lead-in on `REGISTER_MAP.md:1130`, `EGRESS_QUEUE_MAP.md:99` and `ieee8021q.md:67` (R285-4 S1). This RTL copy was outside the assigned list. The author disclosed it in REVIEW READY and in the PR body's disposition row.
- **Why a SUGGESTION:** the list qualifies `[6]` correctly in the same sentence, so no reader is sent to a wrong bit. The wording is a comment only.
- **Optional outcome:** drop "own" at `:6597` the next time the file is touched. This needs no new round of its own.
- **Verification:** `git grep -n "own bits" hdl docs` returns nothing.

### Prior findings, resolved or retained at this head (read after the independent pass)

| prior finding | state at `8ffd6c61` | evidence |
|---|---|---|
| R285-4 F1, MINOR (Docs): the PR body presented the `c593cbef` silicon PASS as exact-image evidence for the merged head | **RESOLVED.** The body (fetched read-only, headRefOid `8ffd6c61`, sha256 `c575ea4b...`) meets each required outcome. **(1)** The silicon PASS covers the #530 RTL (the comment-stripped datapath and processor pin `09f9bf38`). **(2)** This head's image differs from the flashed one by the `gptp-processor` pin `c1b61743` -> `e5dcea6e`, with `gptp_ucode.hex` changing from `83f14a7d...` to `4afe436d...`. **(3)** Status, the checkout line and the disposition table name `8ffd6c61`. **(4)** The manager CORRECTION (issue #530 comment 5810084473) corrects the [A241] sentence. Every checkable fact holds: both ROM digests regenerate byte-exact from each pin's generator, and they match `rom_digests.tsv`. The only `hdl/` change between the gPTP pins is `gen_gptp_ucode.py`, and there are 21 first-parent commits. | `receipts/02`, `receipts/09` |
| R285-4 S1 (Docs): the `0x694` `[6]` definition is unqualified; three lead-ins say "own bits" | **RESOLVED** at the four assigned sites (`REGISTER_MAP.md:1169`, `:1130`; `EGRESS_QUEUE_MAP.md:99`; `ieee8021q.md:67`). The RTL copy is retained as this round's S1. | `receipts/10`, diff `f814d37d..8ffd6c61` |
| R284-4 S1 (RTL, Docs): the refused-branch `0x82C` sentence omits the index-0 `[27:19]` mirror; ADMITTED reads `(\|ACTIVE)` | **RESOLVED.** `:6616-6624` scopes the per-index bits to the AAF sources and names the index-0 `[27:19]` mirror of `LWSRP_STATUS[8:0]`, with `[27]`=`[8]` and `[25]`=`[6]`. This is exact against `milan_csr.sv:2826-2827,2871-2873,2916-2920`: `{4'd0, LWSRP_STATUS[8:0], 15'd0, 4 bits}`. `:6600` reads "ACTIVE ORed over sources". | `receipts/10` |
| R284-4 S2 (Docs, PR body) | **RESOLVED** together with R285-4 F1. | `receipts/09` |
| R284-3 F1, MINOR; R284-3 S1 = R285-3 S1; R284-3 S2 | **Remain resolved.** The round-4 text keeps the lobs scoped above index 0 and `[6]` as the OR. | `receipts/10` |
| R284-2 F1 / R285-2 F1, MINOR; R284-1 F1/F2 / R285-1 F1/F2, MINOR | **Remain resolved.** The round-4 delta does not touch the corner branches or the no-shaper text. | diff `f814d37d..8ffd6c61` |
| R284-1 S1 / R285-1 S3 (the 139 s campaign time); R285-1 S3 (an absolute `CRFLIC_MDIR` breaks `make crflic`, `Makefile:391`); R284-1 S2 (the old-pin arm runs by hand only); R285-1 S1 (the t>0 AAF gates are graded by source text only) | **Retained as SUGGESTIONS, unchanged.** `tb/` is untouched by this delta. The body records each as not taken in a docs-only round. None affects coverage. | `Makefile:391,397`, `README.md:406`, `TESTING.md:266` |
| R284-2 S1 (`milan_datapath.sv:1588`, "consulting the admission verdict"); R284-2 S2 = R285-2 S1 (pre-existing "bw-gate" / "CBS slope MUX" terms) | **Retained as SUGGESTIONS, unchanged.** These are pre-existing terms, and the body leaves them for triage. | `milan_datapath.sv:1588,5295,6636`; `REGISTER_MAP.md:1608,1647` |

## Lens results at `8ffd6c61`

```text
[R285] PASS RTL — hdl/milan/milan_datapath.sv:6596-6624 (77068c9a) + receipts/01,10 — delta f814d37d..8ffd6c61 is comment-only: string-aware comment-stripped, whitespace-normalised datapath sha256 5cd4d5ae... identical at c593cbef, f814d37d, 6556effc, 77068c9a, 8ffd6c61 (canary 50e78097 differs); 0 non-// added/removed hdl lines, 0 metacomment tokens; only hdl file differing from c593cbef is milan_datapath.sv; gitlinks unchanged since f814d37d. New comment claims traced: 0x82C index-0 talker word [27:19]=LWSRP_STATUS[8:0] (milan_csr.sv:2826-2827,2871-2873), above index 0 snap_srp9_w=srp_ctx_rd_stat_w tied 0 (:6722); LWSRP_STATUS[6]=|pp_cd_srp_active_w incl. the CRF slot SRP_TALKERS_C-1 (:6655,:5280-5281,:1628), [8]=lwsrp_stream_gate[0] (:2502-2508). xvlog gate PASS 4==ratchet, 0 in hdl/ (receipts/05).
[R285] PASS Docs — 6556effc FR_NFR.md:149-150, MILAN_COMPLIANCE_MATRIX.md, SUBMODULES.md; 8ffd6c61 REGISTER_MAP.md:1130,1169, EGRESS_QUEUE_MAP.md:99, ieee8021q.md:67; PR #549 body — merge recomputed with git merge-tree: the only conflict is FR_NFR.md, the recorded merge differs from the automatic tree only there, the kept FR-MVU row is byte-equal to dev 3d2f3e31's, the FR-CONN row byte-equal to f814d37d's; dev's MVU/redundancy claims (pp_top M2/M4, no MVU SUID/MCR parameter) still hold at processor 09f9bf38 (424c688f..09f9bf38 changes only hdl/srp + a Domain VID parameter, no M2/M4 hunk); no dev text touches CBS/shaper/ACTIVE/licence; changed pages match the RTL bit trace; docs_check, check_feature_status, check_em_dash (--base 3d2f3e31 and 50e78097), check_doc_style, gen_toc --check/--verify-anchors, check_doc_paths, check_rtl_source_lists rc 0 (receipts/05); PR body silicon scope and image difference verified (receipts/02,09). Open: S1 SUGGESTION only.
[R285] PASS Conformance — issue #530 acceptance items 1-3 vs obj_crflic at 8ffd6c61 (receipts/03) — carried from the covered ancestor f814d37d: no logic, harness or gitlink change in the delta (receipts/01). Spot re-run on the pinned 5.050: crflic 85 checks, 0 failures. Silicon: the A237 PASS covers the #530 RTL; exact-image silicon is the manager's merge-train duty (issue #530 comment 5810084473).
[R285] PASS Robustness — obj_crflic [INV] every-cycle invariants and the Lv-close/refusal arms at 8ffd6c61 (receipts/03) — carried: no logic change; the invariants (licence == ACTIVE[CRF], no AAF gate without ACTIVE, no malformed MRPDU) pass at this head.
[R285] PASS Tests — tb/verilator/milan_dp crflic at 8ffd6c61, gate mutant (receipts/03,04) — carried: tb/, scripts/, syn/, tests/ are unchanged in the delta (receipts/01). At this head, reverting lwsrp_stream_gate to the raw verdict turns 23/85 red (the CRF licence and AAF gate open before a reservation), matching the PR's stated failing arm. Prior Tests SUGGESTIONS are retained unchanged.
```

## Completion ledger (reviewer-owned)

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #530 body, manager decisions and CORRECTION; `crflic` 85/0 on 5.050 (`receipts/03`); comment-only proof (`receipts/01`) | R285-5 | `8ffd6c616840b161891e2eb714a7ddbbb72c7a0d` |
| RTL | CLEAN | `milan_datapath.sv:6596-6624,6640,6655,6722,2502-2508,5280-5281`; `milan_csr.sv:2824-2827,2870-2873,2913-2920`; stripped-sha proof; xvlog gate (`receipts/01,05,10`) | R285-5 | `8ffd6c616840b161891e2eb714a7ddbbb72c7a0d` |
| Robustness | CLEAN | `obj_crflic` invariants and Lv/refusal arms at the head (`receipts/03`); unchanged logic (`receipts/01`) | R285-5 | `8ffd6c616840b161891e2eb714a7ddbbb72c7a0d` |
| Tests | CLEAN (SUGGESTIONS only) | `crflic` 85/0; gate mutant 23/85 red (`receipts/03,04`); tb/ untouched in the delta | R285-5 | `8ffd6c616840b161891e2eb714a7ddbbb72c7a0d` |
| Docs | CLEAN (S1 SUGGESTION only) | merge recompute and row identity; `REGISTER_MAP.md:1130,1169`, `EGRESS_QUEUE_MAP.md:99`, `ieee8021q.md:67`, `FR_NFR.md:149-150`, `MILAN_COMPLIANCE_MATRIX.md`, `SUBMODULES.md`; PR body; static docs gates (`receipts/01,02,05,09`) | R285-5 | `8ffd6c616840b161891e2eb714a7ddbbb72c7a0d` |

## Receipts and scripts

- `check_delta.sh` and `strip_sv_comments.py` -> `receipts/01_check_delta.txt`. These cover:
  - identity;
  - the comment-only proof;
  - changed paths, modes and gitlinks;
  - the merge-tree recompute;
  - FR_NFR row identity;
  - `git diff --check`;
  - that the dev tip is an ancestor of the head.
- `receipts/02_gptp_rom_digests.txt`: `gptp_ucode.hex` regenerated from each pin's `gen_gptp_ucode.py`, compared against `rom_digests.tsv`.
- `run_crflic_probe.sh` -> `receipts/03_crflic_v5050.log` (clean, 85/0) and `receipts/04_mutant_gate_sr_admitted.log` (23/85 FAIL).
  - Both ran in a disposable clone under the scratch directory.
  - The simulator is the pinned 5.050: `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9...`.
  - The simulator include root is redacted in both logs.
- `receipts/05_static_gates.log`: the docs and source gates, all rc 0.
  - The first xvlog attempt refused because the scratch clone's submodules were unregistered. That is an environment condition, and the log records it.
  - After the submodules were registered, the xvlog gate reports PASS, 4 == ratchet.
- `receipts/06_hosted_checks.tsv`: a snapshot of the hosted check runs at the head, taken 08:21 UTC.
- `receipts/07_clone_integrity.txt`: the review clone was never modified.
  - HEAD, tree and index write-tree are all `ff757231...`.
  - `ls-files -s` equals `ls-tree -r`.
  - Every tracked blob rehashes to its index entry, and every 100755 file is executable.
  - The gitlinks are `external efeb541a`, `gptp-processor e5dcea6e` and `protocol-processor 09f9bf38`, and the submodule worktrees are clean.
- `receipts/08`: the independent verdict, written before the prior findings were read.
- `receipts/09`: the PR body and the merge-claim checks.
- `receipts/10`: the RTL comment bit trace.

## Real limits

- No full parent, PP, gPTP, Yosys or builder bank was run; those belong to the manager. Only `crflic` and one mutant ran, on the pinned 5.050. `crflic-mutants`, `gmstep`, `gptp`, behave and the full `milan_dp` sweep were not re-run by this round. Their earlier tallies carry on the comment-only proof.
- Hosted evidence was only inspected. At 08:21 UTC the following had succeeded: rtl-fast, verilator-lint, yosys-elaboration, Yosys shards 0-3, Verilator shard 2/5, docs-check-no-git, bdd-conformance, wire-accountability, changes and full-ci-gate. Still in progress: Verilator shards 0, 1, 3 and 4, docs-check and elaborate. Physical gPTP was skipped, which is not hardware evidence. No act or Docker run.
- Silicon: the A237 PASS is on `c593cbef`. It is not exact-image evidence for this head, which carries the `e5dcea6e` gPTP ROM. Physical calibration was not run. No hardware was touched by this round.
- The merge-train tip `b7ad74d9` was not probed: it is not public.

## Pending manager duties

- Hosted acceptance: the exact-head `verilator-suites` shards, `docs-check` and `elaborate` must complete green.
- Build and validate the current-dev candidate merge at the merge turn. The source base is `50e78097`; live dev is `3d2f3e31`, which this head already contains.
- Run exact-image silicon on the merge-train candidate: gPTP lock plus #530 acceptance (a) and (b), per the CORRECTION. Because the body says `Closes #530`, this must happen before the merge, or the issue must be reopened if it does not pass.
- Post-merge containment.
- Optionally, triage the retained SUGGESTIONS into Issues.

R285-5 FINISHED
