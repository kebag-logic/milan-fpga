[R424] NEGATIVE - exact head e216dfe4f0cab7b0c7352d7973acb4d33c157f70

Round R424-4, internal independent review of PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row). Head `e216dfe4f0cab7b0c7352d7973acb4d33c157f70`, tree `15e18903484842dcb6302159b9f9f1f27d8fc3ed`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. The PR is docs and evidence only: `docs/findings/117_AUDIO_CONTINUITY.md` and its index row in `docs/findings/README.md`.

**Verdict basis.** One MINOR is open, R424-4-F1. It leaves Tests and Docs UNCLEAN, so the verdict is NEGATIVE. Conformance, RTL and Robustness are CLEAN at this head. F1 is one clause on the page (and the same clause in the PR body), and the fix is to correct or drop it. The round 4 work otherwise holds:

- **R424-3 F1 is resolved.** I used only the three directories at archive commit `8e6be432`. Step 1 restores the read record to `2183d57f…` (131,540 bytes). Steps 2 and 3 reproduce `attribution.txt` (`18ebbfc1…`) and `round3_figures.txt` (`9fa0f027…`) byte for byte. All 207 extracted packet files match their manifest `published_sha256`.
- **Every SHA-256 the page cites matches the manifest at the pin (20 of 20, 0 problems).** The `run_a.py`, `grade_a.py` and read-record values are the `original_sha256` of `path_redacted` files, as the page now says.
- **The stream-count ruling is applied on the page and in the live PR body.** No count of the peer's streams, stream ports, stream states or clusters remains there. The peer's clock source selection is kept at `:80` and `:297`, and the format channel counts at `:94` and `:403`.
- **The three suggestions are taken, and each is correct.**
- **The table proof holds.**
- **The docs gates are rc 0 (14 of 14).**

My verdict and ledger were written to `receipts/verdict_ledger_before_prior_findings.txt` (2026-10-01T10:47:57Z) before I read any prior review report.

## Reconstruction

I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md (section 6, wording and privacy, and 6.1, the em-dash gate).
2. `docs/README.md` and `docs/findings/README.md`.
3. Issue #117: its body and acceptance box 4.
4. The B5 assignment (5925737609), the round 4 assignment (5928569912), the stream-count ruling (5929406675) and the round 4 REVIEW READY comments (5929389267, 5929592804).
5. The manager's mask comment on PR #628 (5928569576), which states the redaction is top-only and the history decision is pending the owner.
6. The diff `e4b771f9..e216dfe4` and its five one-line commits.
7. The live PR body and the evidence archive branch `b5-review-evidence`: pin `8e6be432`, tip `cae94a6b`, and the round 4 packet `author-r4/`.

Prior review reports were read only after the verdict receipt was written.

## Findings

### R424-4-F1 - MINOR - Docs, Tests - `docs/findings/117_AUDIO_CONTINUITY.md:511-513`; PR #628 body, Round 4 item 1 ("Both tools now read the masked `summary.json` and `events.jsonl`")

- **What it says.** "`b5_attrib.py` and `b5_round3.py` read the masked `a-long` `summary.json` and `events.jsonl`, and still reproduce both receipts byte for byte at the pinned commit."
- **Evidence.**
  - An openat system-call trace of the two published `figures` commands, run as the page's steps 2 and 3 specify, shows which packet files each opens (`receipts/tool_inputs_strace.txt`):
    - `b5_attrib.py`: `summary.json`, `continuity-events.csv` and the read record (`a-long-reads.json`, `a-long-reads.u16`).
    - `b5_round3.py`: the same files plus `restore/peer-descs-2.jsonl`.
    - Neither opens `events.jsonl`.
  - `b5_round3.py` has no code path that reads `events.jsonl`. `b5_attrib.py` reads it only in `derive` and `wholerun` (`window()`, `author-r2/tools/b5_attrib.py:67-71`), and those modes need the raw files, which are not published.
  - Mutation probe (`receipts/mutation_probe.txt`):
    - Emptying or deleting `author/runs/a-long/events.jsonl` leaves both outputs byte-identical to the receipts.
    - Changing the read record, `summary.json`'s `window_time`, one `continuity-events.csv` row or `peer-descs-2.jsonl` changes the output of the tool that reads that file.
- **Impact.** The page presents the reproduction as evidence that the masked `events.jsonl` was exercised and is harmless. The reproduction cannot detect anything about that file, so the sentence claims coverage the check does not have. The underlying fact happens to hold: `window()` returns the same window bounds from the pre-mask and the masked `events.jsonl`, checked in scratch. But the page's reason for it is wrong. A findings page's account of what its own reproduction verifies has to be exact.
- **Required outcome.** The sentence names only the masked inputs the reproduction actually reads. That is `summary.json` for both tools. It may add that `continuity-events.csv`, `peer-descs-2.jsonl` and the read record are the other inputs. If the page keeps `events.jsonl`, it must say that `events.jsonl` is read only by the `derive` and `wholerun` modes, which need the raw files. The PR body's Round 4 item 1 is corrected the same way. No table or figure changes.
- **Verification.** Re-run `scripts/tool_inputs.sh` and `scripts/mutation_probe.sh` over the pinned extraction. The page's list of masked inputs the tools read must equal the masked files in the trace output (`summary/a-long/summary.json` only). Then re-run the docs gates.

### R424-4-S1 - SUGGESTION - Docs - `docs/findings/117_AUDIO_CONTINUITY.md:6-13`

The header names the round 1 operator and the round 2 and round 3 executors with their assignments, but not round 4 ([A476], 5928569912, and the ruling 5929406675). Round 4 added the packet-location paragraph, the masked-hash statement, the AUDIO_CLUSTER qualification, the p95 rule and the count-free wording. Adding one sentence would keep the page's own provenance pattern complete. The git history records the authorship either way. Optional.

### R424-4-S2 - SUGGESTION, manager-owned - Docs, Robustness - the archive the page pins (`review-evidence/b5-r1` at `8e6be432`, still unchanged at tip `cae94a6b`)

The page and the live PR body are clean. The archive the page links into still carries material that the lane's public-text rules exclude. The ruling scoped itself to "the page and the PR body", and the manager's mask comment leaves history to an owner decision, so I do not count any of the following against this head:

- **Peer stream counts.** The scan's derived peer-count family hits:
  - `author/REVIEW-READY.md:53` (and its `.readback`);
  - `author/restore/census-compare.txt`, whose entry totals give the stream count, as the round 4 executor itself noted;
  - `author-r2/REVIEW-READY.md:28` (and its `.readback`);
  - `author-r2/PR-BODY.md:46`;
  - `author-r3/PR-BODY.md:46` and `:57`;
  - lines in the archived review reports of rounds 1 to 3.

  The same counts are in #117 comments 5926301675 and 5927093074, which the project's rules forbid editing. So masking the archive cannot make them non-public.
- **Peer cluster indices.** `reviews/R425-1/REPORT.md:35` and `:37` still restate cluster indices from the peer's dynamic map that the mask replaced in `author/HANDOFF.md`.
- **Pre-mask history.** `ef3a7091` is an ancestor of the pin. The unmasked originals of the 15 masked lane-packet files are reachable there, and the page's `original_sha256` values identify `run_a.py` and `grade_a.py` exactly (`receipts/archive_pin_to_tip.txt`).
- **Pin fragility.** If the owner decides to rewrite that history, `8e6be432` stops existing. The page's pin, its link and its reproduction steps would then need a new commit.
- **A virtual interface name.** `author/restore/host-start.txt:11` still carries a container bridge interface name, a generated network id rather than a physical interface. It is optional to mask.

**Suggested outcome.** Record the owner or manager decision on the archive before merge, so that the page is not re-pinned after it lands. Either the residuals are accepted as they stand, as the PR's own commit history was accepted, or they are masked at a new archive commit and the page is re-pinned and its steps rechecked in the same round.

## Round 3 findings judged at this head

| Finding | State at `e216dfe4` | Evidence |
|---|---|---|
| R424-3 F1 (MINOR, Docs): reproduction steps do not say where the packets are published | RESOLVED | `:452-459` names branch `b5-review-evidence`, pins `8e6be4329008137a152f9171638e48a43e549fb7` with a tree link, and maps `b5-a472` to `author/`, `b5-a473` to `author-r2/` and `b5-a474` to `author-r3/`. `:206-209` and the Contents entry point there. From those three directories at the pin alone, steps 1 to 3 pass (`receipts/reproduce_pinned.txt`). Both tools read the masked `summary.json`. The `events.jsonl` part of the new paragraph is the new F1. |
| R425-3 F1 (MINOR, Conformance and Docs): the round 1 packet exposes capture layout, link type, an interface name and the SoC family | RESOLVED at the archive tip, per its own required outcome (mask by label, manifest updated, history left to the manager) | `receipts/public_scan.txt` covers the tip `cae94a6b`: 405 text files, plus the page, index row, live PR body, commit messages and added lines. The derived families built from the mask commit (capture channel count, capture channel index, capture layout, interface, SoC USB function, bus positions, peer map) have 0 hits on the page, index row, PR body, commits and added lines. In the lane packets they have 0 hits too. The only derived hits are in an archived review report (S2). The generic classes have 0 hits outside other reviewers' scan-tool pattern lists, except one virtual bridge interface name (S2): link type, SoC product, instrument vendor, host name and wiring. `summary.json` `channel_identification` is `<capture-channel-layout>` in both summaries (`receipts/channel_identification.txt`). The history residual is S2. |
| R424-3 S1: name the three unaligned skips in the final row and Limits | TAKEN | `:28` and `:437-439` name the 72, 78 and 108-frame skips (258 frames) as not attributed, consistent with `:243-250`. |
| R425-3 S1: qualify the AUDIO_CLUSTER sentence against the repository's 7.2.16 encoding | TAKEN, correct | `:378-386`. `avdecc/aem_descriptors.py:590` writes `signal_type` from its argument, with the comment "0xFFFF (input) / AUDIO_UNIT (output)". `NO_STRING = 0xFFFF` (`:105`). `avdecc/aem_assemble.py:289-294` passes `NO_STRING` for the input clusters and `AUDIO_UNIT` for the output clusters. AUDIO_CLUSTER `0x0014` and AUDIO_MAP `0x0017` (`aem_descriptors.py:103`) match the walk-defect paragraph. |
| R425-3 S2: how the p95 is computed | TAKEN, correct | `grade_a.py:266` computes `srt[ceil(0.95 n) - 1]`, the nearest rank. Recomputed from the page's per-cycle table (`receipts/restart_stats.txt`): rank 29 of 30 is 0.0389 s, cycle 20, and linear interpolation gives 0.0344 s, as `:320-322` states. Min, median, max, below-1 s count, medians and slope interval re-derive to within the rounding of the printed per-cycle values. |
| R424-3 S2, R424-2 S4, R424-1 S1: forward pointers from the #117 ledger and the #75 row | RETAINED by the manager (assignment item 4), a SUGGESTION | Outside the lane's fixed output. It affects no lens. |

Earlier MINORs stay resolved at this head:

- R424-1 F1 and R425-1 F1 (attribution strength): `:25`, `:28`, `:240-301` and `:424-443` keep the stall-aligned, not-separated and by-inference wording.
- R424-1 F2 (controller revision): `:520-527`.
- R425-1 F2 (reproducibility): reproduced at the pin.
- R425-1 F3 and R425-2 F2 (Direction B reason): `:27` and `:373-388`.
- R424-2 F1 and R425-2 F1 (published read record): step 1 restores `2183d57f…`.

Round 4 removed no measurement figure. The words removed since round 3 are the peer counts the ruling withdrew, and nothing else (word diff, checked locally and not published, because it would restate them).

## Lens results

```text
[R424] PASS Conformance - docs/findings/117_AUDIO_CONTINUITY.md:21-28, :76-80, :94, :297, :373-388, :403, :410, :452-478, :501-516; PR #628 body; receipts/reproduce_pinned.txt, hash_check.txt, public_scan.txt, table_proof.txt - round 4 assignment items 1-4 and ruling items 1-3 against #117 box 4's continuity row: R424-3 F1 paragraph and reproduction at 8e6be432; 20 of 20 cited hashes against MANIFEST.json (original vs published as stated); peer counts gone from page and live PR body, clock-source selection and format channel counts kept; verdicts (integrity PASS, continuity FAIL as measured, restarts PASS, Direction B NOT RUN, row FAIL as measured) unchanged and not overclaimed; Refs #117 only (no closing keyword in the five commit messages or the PR body).
[R424] PASS RTL - git diff --name-only e4b771f9..e216dfe4 (two docs files, no HDL, firmware, script or config); page :34-39, :211-216 against docs/design/TIME_SYNC.md:478 (one whole-frame slip every 1.958 s, counted once on SLIP_TDM) and docs/reference/REGISTER_MAP.md 0x8D8 SLIP_TDM row (one event per frame); avdecc/aem_descriptors.py:103,105,590 and avdecc/aem_assemble.py:289-294 for the cited encoding - no RTL artifact in scope, and the RTL-behaviour claims the page relies on match the authoritative documents.
[R424] PASS Robustness - receipts/reproduce_pinned.txt, mutation_probe.txt, archive_pin_to_tip.txt; page :206-209, :470-478, :501-507 - reproduction from the masked archive: the masked summary.json still reproduces both receipts; window() bounds equal pre- and post-mask; the gunzip -kf path restores the hashed record over the masked copy; the masked run_a.py and grade_a.py fail to compile, as the page says they do not run as published; the pin's manifest entries are unchanged at the tip (0 of 355 changed, only author-r4/ added); the comparison fails on a mutated input the tools read.
```

**Tests: UNCLEAN.** The finding is R424-4-F1. The reproduction is stated to cover a masked input it never reads. The other checks are clean:

- Steps 1 to 3 reproduce byte for byte.
- The mutation probe shows that each input the tools read can change the result.
- The restart statistics re-derive from the page's own table (`receipts/restart_stats.txt`).

**Docs: UNCLEAN.** The finding is R424-4-F1, at `:511-513` and in the PR body. The other checks are clean:

- The docs gates are all rc 0 at the head in the pinned Markdown environment (`receipts/gates.txt`, 14 of 14). The set is `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e4b771f9` and `--selftest`, `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, and `git diff --check` against `e4b771f9`, `cf38633a` and `c5804007`.
- The public-text scan finds nothing private on the page, the index row, the PR body, the commit messages or the added lines (`receipts/public_scan.txt`):
  - The derived peer-count hits in the PR body are false positives: "19 entries" of the raw-artifact index, and "16.46 ppm".
  - The generic peer-count hits on the page are the DUT's own stream state count and the analysis's skip clusters.
  - The one generic clock word on the page is the DUT's own gPTP state in the frozen Restore table (`:415`), "grandmaster unchanged". It names no device.
- The tables (`receipts/table_proof.txt`) are 15 tables with 119 table lines at the head:
  - Against `c5804007`, 14 of 15 are byte-identical. The one changed line is the Restore table's stream-state cell.
  - Against round 3 `cf38633a`, 13 of 15 are byte-identical. Two tables change one cell each: the final summary row's Evidence cell and the Restore stream-state cell. So the "14 of 15 to round 3" phrasing in the assignment is off by one table, while the "only those two cells" part holds.
  - Every measurement table (T02 to T12, T14, T15) is byte-identical to round 1 `bf9e5d82`.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:21-28`, `:76-80`, `:94`, `:297`, `:373-388`, `:403`, `:410`, `:452-516`; PR body; #117 box 4; round 4 assignment and ruling; `reproduce_pinned.txt`, `hash_check.txt`, `public_scan.txt`, `table_proof.txt` | R424-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| RTL | CLEAN | Diff name list (docs only); `TIME_SYNC.md:478`; `REGISTER_MAP.md` 0x8D8; `aem_descriptors.py:103,105,590`; `aem_assemble.py:289-294` | R424-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| Robustness | CLEAN | `reproduce_pinned.txt`, `mutation_probe.txt`, `archive_pin_to_tip.txt`; masked-copy compile check; pre/post-mask `window()` | R424-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| Tests | UNCLEAN (R424-4-F1) | `tool_inputs_strace.txt`, `mutation_probe.txt`, `reproduce_pinned.txt`, `restart_stats.txt` | R424-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |
| Docs | UNCLEAN (R424-4-F1) | Page (all 541 lines), index row, live PR body, commit messages; `gates.txt`, `public_scan.txt`, `table_proof.txt` | R424-4 | `e216dfe4f0cab7b0c7352d7973acb4d33c157f70` |

## Limits

- **Docs-only head.** No RTL, simulation, Verilator or Yosys was run. The scoped Verilator was not used, so its identity was not checked. No full bank was run.
- **Raw captures are not public.** Figures that need them were not re-derived: the whole-run integrity counts, the zero-frame ordinals, `derive` and `wholerun`. They rest on the pinned raw-artifact hashes (all 19 index entries keep bytes and SHA-256 through the mask, `receipts/raw_index_mask_check.txt`) and on rounds 1 to 3.
- **What the hash check covers.** The bytes behind `original_sha256` for the 15 masked lane files were checked only for `run_a.py` and `grade_a.py`. Their pre-mask history bytes hash to the page's values.
- **The scan's scope.** Its derived families cover only the values the archive's mask commit replaced and the peer counts the ruling withdrew. The other classes are patterns. Hits inside other reviewers' archived reports were located by path and line, and inspected only to classify them: scan-tool pattern lists, a scan receipt's class labels, a variable name, and the two peer-map lines in S2.
- **Hosted checks.** At the exact head, `rtl-fast`, `changes`, `bdd-conformance`, `docs-check-no-git`, `elaborate`, `full-ci-gate` and `wire-accountability` succeeded. `docs-check` was still in progress when read. The `verilator-*`, `yosys-*` and physical-gPTP contexts were skipped, which is not a result (`receipts/hosted_check_runs.txt`). No act replica was run.
- **Not hardware proof.** Physical calibration was NOT RUN and Direction B was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- R424-4-F1: a round to correct `:511-513` and the PR body's Round 4 item 1. Then re-review at the new head: F1, and Docs and Tests coverage.
- R424-4-S2: record the owner or manager decision on the archive residuals and the history before merge, since a history rewrite would require re-pinning the page.
- Hosted `docs-check` completion and the hosted/act acceptance at the exact head.
- The final current-dev candidate. A scratch `git merge-tree` of the head into live dev `ea3fb388` merges with no conflict (tree `8a7b0a6d`). Live dev adds a findings page and an index row. No gate was run on the merged tree.
- The retained forward pointers (R424-1 S1 and its successors).

## Receipts

Listed in `MANIFEST.sha256`. Scripts are under `scripts/` and run from this directory:

- `reproduce_pinned.sh`: steps 1 to 3 from the pin alone, plus a manifest check.
- `hash_check.py`: every cited hash.
- `table_proof.py`: tables across all five commits. It never prints old cell text.
- `restart_stats.py`: restart statistics and p95.
- `tool_inputs.sh`: openat trace of the figures commands.
- `mutation_probe.sh`: input mutations.
- `public_scan.py`: derived, repository-rule and generic classes, with planted controls. Derived values are built in memory and never written.
- `run_gates.sh`: the docs gates.

Raw outputs are under `receipts/`. `receipts/clone_integrity.txt` shows the review clone at `e216dfe4` and tree `15e18903` after all probes: 0 status entries, index equal to HEAD, 0 tracked blobs differing, and 4 gitlinks equal to HEAD. All probes ran on scratch copies.

R424-4 FINISHED
