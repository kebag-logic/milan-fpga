[R624] NEGATIVE - exact head 0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5

Round R624-3: an internal, independent review of PR #725 for issue #629 (bench lanes B16, B16b and B16c; docs and findings only). Documents only, under the [round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508). It ran in a cleared context against a detached clone.

- Head `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5`, tree `dd6c3f3cb7bc5059aa9e976a9131a4e19212d103`, source base `c20c85bd`.
- Diff `c20c85bd..0782c55f`: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+1,312) and one row of `docs/findings/README.md`. Five one-line commits with no trailers. No file under `hdl/`, `tb/`, `sw/`, `syn/` or `scripts/` changes, and the gitlinks equal the base's.
- Read in this order:
  - AGENTS.md, CONTRIBUTING.md (sections 3, 4 and 6) and docs/README.md;
  - the #629 body;
  - the B16 assignment (6117305187), the rulings 6117672835 and 6118365090, and the round 2 and round 3 assignments (6119316763, 6119906508);
  - the author's TAKEN, STOP, STOP (B16b), REVIEW READY (B16c) and both later REVIEW READY comments;
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Bench) and `docs/reference/REGISTER_MAP.md` (`0x8D4`, `0x8E0`, `0x8F8`);
  - the diff and its history;
  - the published packet [`review-evidence/629-b16-r1` at `b84584e4`](https://github.com/kebag-logic/milan-fpga/tree/b84584e4ccb069248909f0fdeb7f8b72a1c41ae4/review-evidence/629-b16-r1), `author-r3/`;
  - the PR #725 body and title.
- The prior public findings (R624-1, R625-1, R624-2, R625-2) were read only after this round's own pass over the diff and the receipts.

## Verdict

One MINOR finding is open, under Docs, so the verdict is NEGATIVE. It alleges no DUT defect, changes no figure and reverses no bench verdict. Conformance, RTL, Robustness and Tests are clean at this head.

Every prior public finding is resolved at this head, or is an optional suggestion the author declined (reconciliation table below).

Every figure the round-3 assignment names was re-derived from the published receipts by this round's own scripts. Those scripts read the per-block and per-poll records, not the author's figures check:

- the positive control's floor counts;
- B16c's LOCKED brackets;
- R625-2-F1's medians;
- B0's floor, runs and overlap split;
- the source-state counts;
- the B16 ACMP record.

**The packet's figures check, run here:**

- `python3 -I tools/check_b16_figures.py <page> <author-r3> <rows> <coverage>` at this head exits 0.
- It reports 1,610 rows, all OK, and 1,815 tokens, 205 of them in identifier categories and none uncovered. Its two outputs are byte-equal to the published `r3/figures-rows.tsv` and `r3/figures-coverage.tsv`.
- Its scope covers the B16 section, the introduction and Contents entry on lane B16, and lane B16's part of the index row. So every summary and attribution figure is in scope.
- No row's key is a literal. Every key reads a receipt; 61 rows quote a superseded figure from the page at `e20fd282` or `35e332b6`.
- The excluded tokens are indices, ordinals, tone names, commits, citations, units and quoted phrases (`receipts/audit_rows.txt`).
- `r3_figures_build.py` regenerates the check byte-for-byte from `r3_figures_spec.py`.
- The author's five controls re-run here pass 5 of 5.
- This round's own six probes, each on an altered copy, all make the check fail:
  - B0's 169 shown as 170;
  - one digit of an evidence hash;
  - the index row's 2.585 shown as 2.586;
  - 23 shown as 24;
  - the source receipt's 618 changed to 619;
  - "thirteen" shown as "fourteen".

## Findings

### R624-3-F1 MINOR (Docs): lane B16's section never says where its lane packet is published

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2318-2320`: "Paths such as `runs/loop2/events.jsonl` are in the lane packet, `629-b16-a603`, whose publication is the manager's; see [B16: artifact hashes]".
  - `:2566-2598`, `:2901-2954` and `:3313-3360` (the three artifact-hash subsections) do not say where it is published either.
  - `:3485-3509`: the figures check "is in the packet, not the tree", and its hash and outputs' hashes "are in the packet's `MANIFEST.sha256`, not on this page".
- **Authority and evidence:**
  - AGENTS.md section 2: "A future cold reviewer must be able to reconstruct the task from GitHub and the repository alone". The Docs lens requires "enough evidence for another cold reviewer".
  - Every earlier lane on this page carries a "**Where the packet is.**" paragraph giving the branch, a pinned commit and the label-to-path mapping: lane B6 at `:647`, B7 at `:1235`, B8 at `:1833` and B15 at `:2252`. Lanes B7 and B15 added it in answer to their reviews (`f4eb39d3`, `1df3ac18`).
  - The B16 packet has been public since round 1, on branch `629-b16-review-evidence`: round 2 at `7affd601`, round 3 at `b84584e4`, under `review-evidence/629-b16-r1/author*/`.
  - Neither the page, the PR body nor any author comment names that location. Only the reviewers' comments link it.
  - The cross-reference at `:2320` points at a subsection that does not answer it.
- **Impact:**
  - After merge, a reader of the durable findings page cannot reach any of the packet files the page cites by hash. That includes the round-2 reduced receipts and the round-3 figures check that the corrections rest on.
  - So the page's hash tables cannot be checked from the repository and the page. The pointer is missing information, not wording.
  - Adding it also adds hash or commit tokens that the figures check must claim, so its receipts regenerate. That makes this MINOR, not RESIDUE.
- **Required outcome:** lane B16's section states where the packet is, as lane B15's does:
  - the evidence branch and a pinned commit;
  - the mapping of `629-b16-a603` and its rounds to `review-evidence/629-b16-r1/author/`, `author-r2/` and `author-r3/`;
  - that `MANIFEST.json` there binds each file's original and published hash, including the 31 path-redacted files (17 in `author-r3/`).

  The figures check is updated so that its new tokens are claimed or categorised.
- **Verification:**
  - The stated commit and paths resolve, and the files hash to the page's rows.
  - `check_b16_figures.py` passes at the new head with 0 uncovered tokens.

## Prior public findings, reconciled at this head

| Prior item | Disposition | Evidence at `0782c55f` |
|---|---|---|
| R624-2-F1 (positive control's floor counts) | RESOLVED | `:2708-2709`, `:3121-3122` and `:2711-2714` count only blocks wholly inside the playback. Recomputed from `summary/{pts2,b0-2,bcrf,baaf}/d-extcap-pair.json` per-block records: blocks 0 and 1 precede the playback and block 2 holds its start. `pts2` has 11 of 13 at the floor, with its repeats at blocks 6 and 12; `b0-2`, `bcrf` and `baaf` have 303 of 303. The `pts2` taps have 15 of 15 (`receipts/verify_b16_figures.json`) |
| R624-2-F2 (LOCKED bracket) | RESOLVED | `:3139-3143`, `:2972-2973`, `:3136-3137`, `:3162` and the index. Recomputed from `r2/{bcrf,baaf}-poll-trace.tsv` with `MCSRV_STAT[2:0]`: the last ACQUIRE polls 44 and 52 start at 2.585 s and 6.602 s, and the first LOCKED polls 45 and 53 end at 3.161 s and 7.180 s. All 596 window polls read LOCKED in each case (`receipts/verify_polls.json`) |
| R624-2-R1 (two source-state statements) | RESOLVED, exact fix | `:2749-2751` and `:3223-3226` equal the fixes word for word. Counts: 2,262, 1,255, 1,007, 4 differing (2 settings and 2 monitoring-mix entries), 618 with 0 differing, 668 with 2 differing (`r2/source-receipt.json` `compare`) |
| R624-2-R2 (pre-set `SLIP_LB` steps) | RESOLVED, exact fix | `:3175-3178`. The trace shows 5 IDLE steps in each case before the set (from 0.14 to 0.15 s after the binds to 1.38 to 1.39 s before the set), then 1 and 2 ACQUIRE steps, and none from the first LOCKED poll to the end |
| R624-2-R3 (PR body antecedent) | RESOLVED, exact fix | The PR body, section "#629": "Direction B's INTERNAL mismatch control did not run: B0 had the peer following the DUT, and the exception covers B-CRF and B-AAF only." |
| R624-2-S1 (servo status bit 4) | TAKEN | `:3303-3305`. Bit 4 is set at 657 of 657 ACQUIRE and LOCKED polls in each case |
| R624-2-S2 = R625-2-S1 = R624-1-S1 = R625-1-S1 (census wording) | RETAINED as optional | Declined by the author; "45 of 46 entries" is true under the tool's definition |
| R625-2-F1 (attribution at (a)) | RESOLVED, exact replacement | `:3206` is the replacement verbatim. From `summary/{bcrf,baaf}/a-peer-tap.json` per-block records: medians -123.98/-123.97 and -123.98/-123.98 dB, every worst block -123.93 dB |
| R624-1-F1 = R625-1-F3 (B0 figures) | RESOLVED, still at this head | Recomputed from `summary/b0-2/c-b9-grade.json` blocks: floor -123.98/-123.95 dB over 169 blocks; runs 0 to 18, 28 to 31, 43 to 44, 46 to 54 and eleven later; recording start 06:38:05.2, 26 s after the binds (`:2638`, `:2663-2667`). `r2_b0_receipt.py` reproduces `r2/b0-2-receipt.json` byte for byte |
| R624-1-F2 = R625-1-F4 (lane B6's four terms) | RESOLVED, still at this head | `:3157-3169` matches lane B6's rule at `:330-332`. The timed ratio is NOT RUN with no decision replacing it, in the acceptance row (`:3283`), the limits (`:3298-3300`), the index and the PR body |
| R625-1-F1 (attribution inside and beyond the taps) | RESOLVED, still at this head | 131 at (c): 23 lie inside whole blocks 0 to 33 of the 1,637,452-frame overlap, and 108 beyond it in 13 runs (43 to 251). The worst inside is block 7 at -100.61/-80.63 dB, and beyond it block 224 at -100.47/-80.48 dB. Labelled inference at `:2797-2809`, `:2895-2898`, `:3217-3222`, `:3308-3310`, in the index and in the PR body |
| R625-1-F2 = R624-1-S2 (reduced receipts) | RESOLVED, still at this head | `r2/` is bound to the raw poll hashes and the twelve source-read hashes, with the extraction commands at `:3429-3434`. It names no peer or capture identity and carries no layout detail, address or host path |
| R624-1-R1 = R625-1-R1 (title) | RESOLVED | The live PR title equals the fix |
| R624-1-R2 = R625-1-R2 (first counter mark) | RESOLVED | `:3004-3006`, `:3059-3061`; `runs/{bcrf,baaf}/events.jsonl` `window-mark-0` |

## Per-lens results

```text
[R624] PASS Conformance - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2281-3575, docs/findings/README.md:15, PR #725 body; author-r3 runs/*/events.jsonl, summary/loop2/acmp-peer-tap.json, restore/census-*.jsonl - judged against the B16 assignment, both rulings, #629's bench items, docs/design/MEDIA_CLOCK_FOLLOWING.md:1661-1673 and REGISTER_MAP 0x8E0/0x8F8.
  B16: the loopback's PROBE_TX (CONNECT_TX, sent by the peer 99.6 ms and 299.6 ms after the unbind command) is never answered: no CONNECT_TX_RESPONSE in 49.6 s. 14 listener polls per run read flags 0x0002, stream ID 0 and talker connection count 0. The STOP at step 2 follows the assignment.
  B16b: the four points and B0 are graded as ruled, sample-exact. B-CRF and B-AAF stopped for the clock-loop decision.
  B16c: per case, the peer is set to 0 and read back 0, the DUT to 1 or 2 and read back, the DUT restored to 0, then the peer restored to 1 after the unbinds, every set read back. The marks read DUT 1/2 and peer 0, and after the restore 0 and 1.
  Restore: the DUT's clock source is set only on the DUT as the listener. Formats were already equal, so none was set. The B16 start census equals the B16c end census in 45 of 46 entries; the other is the DUT's propagation delay. The peer's STREAM_INPUT 0 and 8 are bound back to the DUT's AAF and CRF talkers, and the peer's CLOCK_DOMAIN is on source 1.
  Attribution: the source-route and clock-setting changes are attributed outside the lane and never claimed as DUT behaviour.
  Lane B6's four terms are stated, with the timed ratio NOT RUN. The INTERNAL mismatch control is stated as not run (:3288-3291, :3306-3307, the index, the PR body).
  The design's B AAF row is met at (d), at the loop's floor in 303 of 303 blocks. AAFM_STAT 0x001e0007 decodes as stated.
[R624] PASS RTL - git diff --name-status c20c85bd..0782c55f (two .md files) and git ls-tree 160000 entries at both commits - no HDL, testbench, firmware, synthesis or gitlink change. The REGISTER_MAP readings the page relies on (MCSRV_STAT [2:0], [4] and [6]; [31:16] trim in 1/16 ppm; SLIP_LB 0x8D4; AAFM_STAT fields) are decoded the same way in this round's trace recomputation.
[R624] PASS Robustness - author-r3 r2/*-poll-trace.tsv, summary/*/d-extcap-pair.json, restore/*, runs/b0/events.jsonl and tools/check_b16_figures.py - the negative and boundary records:
  the failed b0 run is excluded from grading and its raw files hashed;
  pre-playback blocks are excluded from the floor counts;
  partial overlap blocks are counted as beyond the taps;
  the poll brackets cover the state read;
  the overwritten B16b playback log is stated as not retained, cited to HANDOFF.md step b17;
  in the figures check, 6 of 6 reviewer probes and 5 of 5 author controls fail closed on altered copies.
[R624] PASS Tests - receipts/check_b16_figures.stdout (rc 0; rows and coverage byte-equal to the published r3/), receipts/verify_b16_figures.json, receipts/verify_polls.json, receipts/verify_hash_tables.json (120 of 120 hash rows: 106 packet files by size and SHA-256, 14 raw files by RAW-ARTIFACTS.json), receipts/probe_figures_check.json, receipts/r3-controls-rerun.json, receipts/b0-2-receipt.rerun.json and receipts/b16c-tables.rerun.md (both byte-equal to the published files), receipts/packet-manifest-check.json (1,680 of 1,680 published hashes; author-r3 MANIFEST.sha256 equal to the 525 original hashes, 17 path-redacted) - the check is non-vacuous and covers every summary and attribution figure in scope.
[R624] MINOR Docs - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2318-2320, :2566-2598, :3485-3509 - lane B16's packet location is never stated (R624-3-F1).
  The rest of the Docs lens is clean:
  - gates at this head, all rc 0: docs_check, check_doc_style, check_doc_paths, check_em_dash --base c20c85bd (0 findings over 1,313 added lines), gen_toc --check and --verify-anchors in the pinned Markdown environment, ci_scope --selftest, check_baremetal_only --check and --selftest, check_feature_status --self-test, git diff --check c20c85bd..HEAD;
  - the reference peer and the external capture are named only by role, and the added text carries no host path, address or bench identity;
  - inference is separated from direct evidence in the findings, the index and the PR body.
```

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:2281-3575`, the index row, the PR body; `author-r3` runs, summaries, restore census, ACMP decode; the assignment, both rulings, #629, the design's Bench rows, REGISTER_MAP | R624-3 | `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` |
| RTL | CLEAN | `git diff --name-status c20c85bd..0782c55f`; the gitlinks at the base and the head; the REGISTER_MAP decodes used by the page | R624-3 | `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` |
| Robustness | CLEAN | Exclusions, brackets and incident handling in the page and receipts; the figures check fail-closed probes | R624-3 | `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` |
| Tests | CLEAN | The figures check, run and probed; independent recomputation of the B0, B16c, (a), (d) and poll figures; 120 hash rows; packet manifest; re-run author tools | R624-3 | `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` |
| Docs | UNCLEAN | R624-3-F1 open; doc gates rc 0; privacy and role naming clean | R624-3 | `0782c55f77e7f44df2e39da1ca9d8643f2dd1dc5` |

Coverage is banked against `0782c55f`. A commit answering F1 touches only the Docs scope and the packet's figures check (Tests). It re-opens Docs, and Tests for the check's rows and coverage only.

## Real limits

- **Raw files.** The raw captures, raw console polls, the tone source's reads and class map, and the playback logs are not public. This round checked their hashes against `RAW-ARTIFACTS.json` and the receipts' bindings, not their bytes. Figures derived from them are checked against the published reduced receipts and summaries.
- **B16b's five underruns** rest only on the operator's record (`HANDOFF.md` step b17). The page states this.
- **Causal claims.** The page states two causes as inference, and this round accepts them as labelled, not proven:
  - that the tone source's clock setting caused the step at (a);
  - that the peer does not answer its own probe internally.
- **No hardware.** This round ran no bench action and no hardware. Physical calibration is NOT RUN, and printed precision is not calibrated accuracy. Field skips are not hardware proof.
- **No source bank.** No manager source bank runs at this head, and none is claimed or inferred. The author's gate receipts are the source-head execution evidence; this round re-ran the documentation gates listed above.
- **Hosted contexts** at this head, read at 2026-10-12T08:58:58Z (`receipts/hosted-check-runs.tsv`):
  - completed with success: `changes`, `full-ci-gate`, `rtl-fast` (3 s), `wire-accountability`, `bdd-conformance`, `elaborate`, `docs-check-no-git`;
  - skipped: `verilator-suites`, `yosys-portability` and their shards, `verilator-lint`, `yosys-elaboration`, `firmware-unit`, `publication-census` and physical gPTP;
  - still in progress: `docs-check`.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the in-progress `docs-check` context.
- The current-dev merge candidate (source base `c20c85bd`, live dev `c6bd08c6`): builder and native banks at the merge turn, with their receipts linked on the PR.
- Publication of this report and the files listed in `MANIFEST.sha256`.
- After F1 is answered, a re-review of the Docs lens, and of the Tests lens for the figures check's rows and coverage, at the new head.

R624-3 FINISHED
