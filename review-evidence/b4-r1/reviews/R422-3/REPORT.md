[R422] POSITIVE - exact head ae98b30b04e95f38df784ba490da208c57534303

Round R422-3, a confirmation round. This is the internal independent review of PR #627 (Refs #451, bench lane B4, the timing item).

- **Exact head:** `ae98b30b04e95f38df784ba490da208c57534303`, tree `bae15aec6847292bd50025203035e3b902bdac79`.
- **Base:** dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`, which is also the live dev tip at review time (`receipts/remote_refs.txt`).
- **The round-3 commit:** one commit on my round-2 head `c39312b4`. It changes one paragraph of `docs/findings/451_TDM8_TIMING_SOC_BOARD.md`: hunk `@@ -350,2 +350,3 @@`, 3 lines added and 2 deleted.

All five lenses were applied at this head.

R422-2 F1 is resolved:

- The talker-to-unbind interval at `:350` now reads "60.0 s before the unbind, on the controller host's clock".
- My script, re-run on the packet's `runs/timing-long`, gives 60.038 s on the controller host's clock. Its output is byte-identical to the round-2 receipt.
- The PR body's matching line agrees.
- R422-2 S1 is taken.
- Nothing else on the page changed: all 12 tables are byte-identical to `c39312b4`.
- The docs gates return rc 0.

No BLOCKER, MAJOR or MINOR finding is open.

## Reconstruction

These are the authorities, read in this order:

- AGENTS.md; CONTRIBUTING.md; docs/README.
- The #451 frozen scope as carried through rounds 1 and 2: the issue body, the SoC-board amendment 5729936674, the owner decisions 5916029287 and 5924157808, the B4 assignment 5924192573 and the ruling 5924950994.
- The round-3 assignment 5925502698, which is the frozen scope of this round:
  - make the interval one the packet supports on a single clock;
  - make the PR body's matching line agree;
  - take R422-2 S1 if cheap;
  - change nothing else and keep the measurement tables byte-identical;
  - pass the docs gates.
- The A470 TAKEN 5925511375 and REVIEW READY 5925580411, and the review start 5925595873.
- `git diff e4b771f9..ae98b30b`, the round-3 diff `c39312b4..ae98b30b`, and the commit history.
- The public evidence at `e7686d89:review-evidence/b4-r1`, in `author/`, `author-r2/` and `author-r3/`. 182 files equal the packet's `MANIFEST.json` published hashes. The six manifest entries whose published bytes differ from the original are the redacted copies the packet declares (`receipts/evidence_packet_check.txt`).
- The live PR #627 body, which is byte-identical to `author-r3/PR-BODY.md` (SHA-256 `a1be4a83...`), and the exact-head check runs.

I fixed my verdict and ledger in a draft at 2026-10-01T05:56:48Z. Only after that did I read the round-2 external review (R423-2, comment 5925499736). I read no `reviews/` content under the evidence tree.

## What was verified

### R422-2 F1, the interval

- **The page.** `:350-352` reads "The talker also ended 60.0 s before the unbind, on the controller host's clock, because the stalled capture held the SoC board's console until its deadline. Both counters clear only on reset."
- **Both stamps come from the controller host:**
  - The talker's `end` record (`controller-logs.txt:141`, t 1790828918.128055) comes from `aaf_talker.py:40`, `time.time()`. It runs over ssh on the controller host (`run_timing.py:98-102,135-137`).
  - The unbind command's start record (`ctl-unbind.jsonl` line 1, t 1790828978.166264) comes from `avdecc_rw.py:82` through `avdecc_ro.emit` (`avdecc_ro.py:53-54`). That also runs over ssh on the controller host (`run_timing.py:68-74`).
  - The difference is 60.038 s, which rounds to 60.0 s.
  - The mixed-clock 58.655 s is gone.
  - The controller clock reads at least 1.36 to 1.38 s ahead of the orchestrator for the same commands (`receipts/talker_unbind_interval.json`, byte-identical to the R422-2 receipt).
- **The check can fail.** `scripts/check_page_interval.py` reads the page sentence and compares it against the packet (`receipts/page_interval_check.txt`).
  - The page at `ae98b30b` gives AGREE, rc 0.
  - Four cases give DISAGREE, rc 1:
    - the round-2 page text (58.7 s, no clock named);
    - a page copy perturbed to 60.1 s;
    - a page copy with the clock clause removed;
    - a packet copy whose unbind stamp is moved onto the orchestrator's clock.
  - All of these ran on copies under the scratch directory.
- **Nothing else on the page contradicts the figure.** The events table (`:277-283`) is on the bench host's clock and lists neither stamp.

### The PR body

- The round-2 R422-1 S2 line now reads "Round 3 states the interval on one clock: 60.0 s, on the controller host's clock (R422-2 F1)".
- The Round 3 note's "changes only the page's `:350-352`" matches the hunk.
- It names the start record correctly: the end record against the unbind's start record, both stamped on the controller host.

### R422-2 S1, taken

- The PR body's FSYNC verdict cell equals the page's `:36` verdict cell.
- Its evidence cell equals the page's, less the closing "See [Frequencies](#frequencies)" link.
- I checked this programmatically. Relative to the round-2 packet's body, the only table line that differs is that row.

### Nothing else changed

- `git diff --raw c39312b4 ae98b30b` lists one file. `--numstat` is 3/2, in one hunk at `:350`.
- `receipts/table_identity.txt`:
  - All 12 page tables are byte-identical to `c39312b4`, with the same SHA-256 each.
  - Against `35a60c8d`, the only differing table line is still the round-2 FSYNC verdict row.
- `docs/findings/README.md` is unchanged since round 2, at blob `a501c5a9`.
- The 11 evidence-file rows on the page still equal the packet in bytes and SHA-256 (`receipts/page_hashes.txt`). The raw capture row is off-packet.

### Gates

`receipts/gates/gates-summary.txt`: all 12 invocations return rc 0 at the exact head. They ran in the hash-locked renderer (cmarkgfm 2025.10.22, html5lib 1.1) with pyyaml 6.0.3, and with bytecode writing off.

| Gate | Result |
|---|---|
| `docs_check.py` | 0 findings across 182 md files, scrub self-test 23/23 |
| `check_doc_style.py` | rc 0 |
| `gen_toc.py --check` | rc 0 |
| `gen_toc.py --verify-anchors` | 283 links |
| `check_em_dash.py --base e4b771f9` | 0 findings over 394 added lines |
| `check_em_dash.py --base c39312b4` | 0 findings over 3 added lines |
| `check_doc_paths.py` | 861 paths |
| `ci_scope.py --selftest` | PASS |
| `check_baremetal_only.py --check` | 0 findings over 951 files |
| `check_feature_status.py --self-test` | 46/46 |
| `git diff --check` | quiet against both bases |

### Commit and PR hygiene

- The commit message is one line, with no body and no trailers.
- The PR body carries `Refs #451` and no closing keyword. Its issue references are #451 and #626 only.
- The three added lines name no private host, path, address, peer or tool (`receipts/pr_body_and_privacy.txt`).

## Findings

None open from this round.

## Prior public findings, resolved or retained at this head

| Finding | State at `ae98b30b` | Evidence |
|---|---|---|
| R422-2 F1 (MINOR, Docs): cross-clock "58.7 s" | RESOLVED | `:350-352` reads 60.0 s on the controller host's clock. The packet gives 60.038 s on that clock, and the check passes and can fail (above). The PR body agrees |
| R422-2 S1 (SUGGESTION, Docs): PR body FSYNC row | TAKEN | The verdict cell equals the page's `:36`. The evidence cell equals it less the anchor link |
| R423-2 S1 (SUGGESTION, Docs): `:59-61` "every identity value equals that page's" leaves #617's NVM row (seq 230) unexplained | RETAINED, optional, unchanged | Its premise holds: `console-identity.txt:13` reads "authoritative B, image seq 236"; #617 `:48` reads "Slot B seq 230 authoritative"; this page states 236 at `:81-82`. The round-3 assignment did not name it. Being a SUGGESTION, it does not affect coverage |
| R422-1 F1, R422-1 F2 with R423-1 S1, R423-1 F1 (MINOR) | RESOLVED, unchanged since round 2 | The lines that resolved them (`:36,115-117,153-161,244-250,303-320`) and every table are byte-identical to `c39312b4`. R422-2 and R423-2 recorded them resolved there |
| R422-1 S1, R423-1 S2, R423-1 S3 | TAKEN, unchanged | Same lines, unchanged since `c39312b4` |
| R422-1 S2 | TAKEN; its figure corrected by R422-2 F1 | Above |

## Per-lens results, with evidence

[R422] PASS Conformance - `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:350-352` and the live PR #627 body at ae98b30b, against round-3 assignment 5925502698; `receipts/talker_unbind_interval.json`, `receipts/page_interval_check.txt`, `receipts/table_identity.txt`, `receipts/diff_scope.txt` - What I checked:

- Every assignment item is met:
  - single-clock interval, 60.0 s against 60.038 s;
  - the PR body line agrees;
  - S1 is taken;
  - nothing else changed;
  - tables byte-identical;
  - gates rc 0.
- No verdict, measured figure or #451 scope statement changed.
- The PR claims no issue state change and has no closing keyword.

[R422] PASS RTL - `receipts/diff_scope.txt` (`git diff --raw e4b771f9..ae98b30b`: two `.md` files; gitlinks identical to base; 0 changed `hdl/`, `.sv` or `.v` paths); `hdl/milan/milan_datapath.sv:1008-1012,1053-1057` and `hdl/ieee1722/aaf/KL_tdm_capture_master.sv:46-62` at ae98b30b - What I checked:

- No RTL changed.
- The round-3 text makes no RTL claim.
- The page's RTL premises that R422-2 checked are on unchanged lines, so they still hold at this head: BCLK = SLOTS x WORD_BITS x fs; a one-BCLK FSYNC pulse; `DATA_DELAY_P = 1'b1` on both master instantiations.

[R422] PASS Robustness - `author/runs/timing-long/{controller-logs.txt,ctl-unbind.jsonl,events.jsonl}` and `author/tools/{run_timing.py,aaf_talker.py,avdecc_ro.py,avdecc_rw.py}` at e7686d89, against page `:343-352` at ae98b30b; `receipts/talker_unbind_interval.json` - What I checked:

- The ordering claim is confirmed on one clock, with a 60.04 s margin: the talker ended before the unbind because the stalled capture held the console.
- The mixed-clock reading (58.66 s) is no longer stated.
- No failure-path statement elsewhere on the page changed: the truncation, the USB loss and the residuals are byte-identical.

[R422] PASS Tests - `scripts/check_page_interval.py` with `receipts/page_interval_check.txt` (1 AGREE, 4 mutations that DISAGREE with rc 1); `scripts/talker_unbind_interval.py` re-run (output byte-identical to round 2); `scripts/page_hashes.py` (11/11 equal); `scripts/verify_evidence_packet.py` (182/182) - What I checked:

- The PR adds no executable test.
- The evidence behind the changed sentence re-derives.
- My check of it fails on each of the four mutations, including the round-2 text.
- The decoder and fs evidence is unchanged since round 2, where it was re-derived.

[R422] PASS Docs - `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` (393 lines, blob dde50cd9) and `docs/findings/README.md` (blob a501c5a9, unchanged) at ae98b30b; the live PR #627 body (sha256 a1be4a83...); `receipts/gates/gates-summary.txt` (12/12 rc 0); `receipts/pr_body_and_privacy.txt` - What I checked:

- The F1 wording is exact and unambiguous about the clock.
- The re-wrap is clean, the gates pass, and the PR body is consistent with the page.
- The added lines are privacy-safe.
- R423-2 S1 is an optional SUGGESTION and leaves the lens clean.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:350-352`; PR body; assignment 5925502698 items; interval, table-identity and diff-scope receipts | R422-3 | ae98b30b04e95f38df784ba490da208c57534303 |
| RTL | CLEAN | Diff raw from base (no RTL, gitlinks identical); `milan_datapath.sv:1008-1012,1053-1057`; `KL_tdm_capture_master.sv:46-62` | R422-3 | ae98b30b04e95f38df784ba490da208c57534303 |
| Robustness | CLEAN | `controller-logs.txt`, `ctl-unbind.jsonl`, `events.jsonl`, the stamping tools, against page `:343-352` | R422-3 | ae98b30b04e95f38df784ba490da208c57534303 |
| Tests | CLEAN | `check_page_interval.py` (1 agree, 4 failing mutations); `talker_unbind_interval.py`; `page_hashes.py` 11/11; evidence manifest 182/182 | R422-3 | ae98b30b04e95f38df784ba490da208c57534303 |
| Docs | CLEAN | Whole page and index row; PR body; docs gates 12/12 rc 0; privacy scan of the added lines | R422-3 | ae98b30b04e95f38df784ba490da208c57534303 |

Every lens is covered at the merge-candidate source head. Any later commit that touches the page un-covers all five lenses.

## Erratum to my own round-2 report

R422-2 described the page at `c39312b4` as "all 393 lines". It had 392. The page has 393 lines at `ae98b30b`. The R422-2 gate figure "393 added lines" was correct, because it counted both files. This changes no finding.

## Real limits

- The 730,595,328 B raw capture is off-packet, so I did not re-decode it. No figure changed this round.
- I had no bench, instrument or hardware access. Physical calibration was NOT RUN, and nothing here is pin-level proof. FSYNC width, edges, levels and absolute ppm remain with #626.
- I ran no full parent, PP, gPTP, Yosys or builder bank, and no simulation. The diff is docs-only. The scoped Verilator was not needed and not used.
- The manager's full source static/builder and native bank results at this head are stated by the manager. I found no bank receipt for `ae98b30b` in the evidence tree at `e7686d89`, so I did not inspect them.
- **Clone integrity** (`receipts/clone_integrity.txt`):
  - HEAD, tree and index tree are `ae98b30b` / `bae15aec`.
  - Status, including ignored and untracked files, is empty. The cached and worktree diffs are quiet, and no index flags are set.
  - Both PR files hash to their tree blobs, mode 100644.
  - The four gitlinks equal the tree. The three initialized submodules are at their pins and clean. `external` stays uninitialised by design.
  - The gates ran with bytecode writing off, so no cache was created.
- **Gate summary paths.** The gate summary's interpreter paths were replaced with `<packet>` after the run. The published `run_docs_gates.sh` does the equivalent substitution itself.

## Pending manager duties

- **Hosted snapshot at 2026-10-01T05:56:11Z** (`receipts/hosted_check_runs.tsv`):
  - Executed and successful: `rtl-fast`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `bdd-conformance`, `changes` and `full-ci-gate`.
  - Still in progress: `docs-check`.
  - Skipped contexts, the docs-only path, not executed evidence: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, their shards, and Physical gPTP.
  - Hosted and act acceptance stays with the manager.
- Candidate-merge validation against the live dev tip at the merge turn. Source base and live dev were both `e4b771f9` at review time.
- The second independent review at this head.
- **Owner items carried by the PR:**
  - re-attaching the SoC board's USB function on the bench host;
  - whether the 1,016 unexplained whole-frame discontinuity clusters get their own Issue;
  - whether `KL_tdm_capture.sv`'s DSP-mode comment does (out of scope here; see R422-2);
  - whether to take R423-2 S1;
  - closing #451's timing item by hand once the merge bar is met, with #626 holding the oscilloscope version.

R422-3 FINISHED
