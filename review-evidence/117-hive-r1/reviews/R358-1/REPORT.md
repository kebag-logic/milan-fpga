[R358] NEGATIVE - exact head bcba79a50ecd2eca99db91c4f3802d888eaac7e4

# R358-1: internal independent review of PR #598 (issue #117, acceptance box 4, Hive row)

- Head reviewed: `bcba79a50ecd2eca99db91c4f3802d888eaac7e4`, tree `b9db4da38ef2d848930ea76c3a0b215cfb309657`, one commit on dev `2a2a7bb655e528edc3087c88033cd3a47546feb4` (PR head and base confirmed by a read-only query, `receipts/context_and_hosted.txt`).
- Diff: `docs/findings/117_GPTP_SILICON_EVIDENCE.md` only, 116 insertions / 3 deletions in three hunks: result-table Hive row (:54), Step 5 tool-table Hive row (:464), blocker B4 (:536-650).
- Evidence judged: the public packet `review-evidence/117-hive-r1` at `89aa9f94ffe46cf7fa9df54376d26771e118f103` (branch `117-hive-review-evidence`, still at that commit), issue #117 body, the assignment (issue comment 5858063707), TAKEN (5858076185), REVIEW READY (5858184304), PR body and PR comments. No bench action; no hardware re-measurement.
- Verdict NEGATIVE because of one open MINOR (F1, Docs and Conformance). The measured result itself was reproduced as far as it can be offline and holds; F1 is about how the merged page lets a cold reader find and check the raw artifacts.

## Findings

### F1 - MINOR - Docs, Conformance - `docs/findings/117_GPTP_SILICON_EVIDENCE.md:629-632` (with `:634-645` and the box 5 row `:58`) - B4 evidence has no public locator, calls publication pending, and says entity dumps keep their recorded bytes while their published copies are redacted

- Authority/evidence: issue #117 acceptance box 5 ("Findings include ... raw artifacts, exact hashes ... under `docs/findings/`"); the page's own box 5 row (:58) claims PASS "for the runs recorded here" because packets "are published at a pinned commit with per-file SHA-256 manifests"; the page's established convention in [Raw artifacts] (pinned branch/commit link, and an explicit list of which cited hashes name files published only in redacted form, mapped by `MANIFEST.json`); AGENTS.md section 2 (a cold reviewer must reconstruct from GitHub and the repository alone).
  - :629-630 names only "The coordinator's `117-a373` evidence packet" and says "publication is pending". The packet is now public at `89aa9f94.../review-evidence/117-hive-r1`, but no line of the page at this head names that branch, commit or path (`grep` for `89aa9f94`, `117-hive-r1`, `117-hive-review-evidence`: no hit).
  - :632 says "Entity dumps and enumeration logs retain their recorded bytes." For the public copies this is false for the three dumps: `MANIFEST.json` marks `run-1/2/3.entity.json` `path_redacted: true`, and each published copy has `"serial_number": "<device-serial>"`. The page's SHA-256 values for these three (:639, :641, :643) match the recorded bytes, not the published files. `sha256sum` against the public files fails for them, and the page gives no hint. (The recorded bytes are recoverable: restoring the DUT's configured serial string reproduces all three cited hashes. See `receipts/summarize_recompute.txt`. The data is sound; the page's description of it is not.)
- Impact: the merged page's only pointer to the evidence behind a new PASS row is a private packet name, plus a "pending" state that will be stale on merge. A cold reader who finds the packet anyway gets three hash mismatches, and the page says there should be none. The box 5 PASS row then overclaims for the B4 runs.
- Required outcome: the page names the public pinned location of the B4 packet, the way [Raw artifacts] does for the A200/A202 packets, and drops "publication is pending". It says which B4-cited hashes name files published only in redacted form (the three entity dumps; serial field masked) and that `MANIFEST.json` maps each to its published copy. It no longer states that the dumps keep their recorded bytes in the public packet.
- Verification: at the corrected head, the page contains the pinned locator; `sha256sum` of every B4-cited file at that locator either matches or is listed as redacted with its `MANIFEST.json` mapping; the docs gates stay rc 0; hunk scope is still limited to the Hive rows, B4 and whatever the fix touches in [Raw artifacts] (if the fix puts the locator there).

### S1 - SUGGESTION - Docs, Conformance - `:53`, `:462`, `:467` vs `:54`, `:464`, `:538-539` - adjacent FAIL and PASS Milan verdicts with no stated reason for the change

- Evidence: the 2026-09-23 row (:53/:462) records Milan FAIL over the CRF Stream Input counters, "tracked in #529". The new row (:54/:464) records Milan PASS. The library binaries match (build-provenance SHA-256 `95d64fd5...`/`8ef4b008...` equal the :209 prefixes). The enumerator differs from `a200_enum.cpp` only by the DUT filter, the absent-DUT rc and labels (`receipts/a200_enum_vs_enum_probe.diff`). The change comes from the image: `ede8d48e..9e9954e9` contains PR #534 ("Serve the CRF Stream Input counters on GET_COUNTERS"), #529 closed 2026-09-24, and the new dumps show Stream Input 1 serving ten counters. B4 says only that the earlier results "retain their original image and verdicts".
- Optional outcome: one sentence in B4 naming the image difference that plausibly explains the change (#534 / #529), stated as an observation, not a proof. This is optional; the frozen edit set is respected either way.

### S2 - SUGGESTION - Docs - `:31` - Contents description still says "the two blockers that remain"

- B1 to B4 are all RESOLVED at this head. The phrase can be read as "the other two entries", and it was already loose at base (B3 was resolved there), so this is not attributed to the PR. It could be reworded in the same edit as F1 or in a follow-up.

### S3 - SUGGESTION - Docs - `:622-626` - listed build defines are a subset

- The page names four feature defines. `build-provenance.txt` also shows `-DNDEBUG`, `-DHAVE_FMT`, `-DIGNORE_NEITHER_STATIC_NOR_DYNAMIC_MAPPINGS`, `-DCONTINUE_MISBEHAVE_AEM_RESPONSES` and `-DALLOW_RECV_BIG_AECP_PAYLOADS`, and every run log shows that the library itself was compiled with its tolerance options (for example "Ignore Invalid Non Success AEM Responses"). The reviewer verified that all of these are the library's own default CMake options at the recorded revision (`receipts/library_provenance.txt`). One clause saying so would pre-empt a reader's question about leniency. The page's statement that "`build-provenance.txt` records the complete build and linkage flags" is accurate.

## Focus checks (assignment items 1 to 5)

1. **Identity gate: holds.** The reviewer regenerated the AEM image from source at this head, whose product source equals `9e9954e9` (the `9e9954e9..2a2a7bb6` diff is the four documentation/evidence files stated, with no submodule gitlink change). The builder emits 7,352 bytes with SHA-256 `9b077636...14404`, equal to the cited image. The AECP ENTITY (312 B) and CONFIGURATION (106 B) bytes in `identity-aecp.jsonl`, with the 4-byte prefix removed, equal both the image's descriptor rows and image offsets 0x110/0x248. Entity `020000fffe000001`, model `001bc5c40236ba0e`. The UART transcript carries `VERSION=00020060` (the value the CSR simulations expect, `tb/verilator/csr/sim_main.cpp:350`) and ROM/QSPI/AEM CRCs `9b6576a9`/`3c18c276`/`93742dd2`, equal to `expected-crc.txt` for the cited sizes and hashes. The page correctly says these are CRC consistency checks, not SHA-256 readback. Timestamps order the checks correctly: identity UART 17:26:15-17:26:38, AECP 17:27:16, runs 17:29:27-17:30:35, final UART 17:31:53. Receipts: `receipts/probe_aem_identity.txt`, `receipts/probe_page_claims.txt`.
2. **The library's own judgement, able to fail: holds.** `tools/enum_probe.cpp` (SHA-256 `ac552f67...`, equal to the page) never prints PASS. It prints `getCompatibilityFlags()` (:164) and compatibility-change events (:169-170), counts every library log item at Warn or above as a COMPLAINT (:75-79), and serializes the library's own `compatibility_flags` into the dump (:151, :176). The verdict on the page comes from `tools/summarize.py:45`, which demands exactly `["IEEE17221","MILAN"]` and no events. Mutation probe: 11 of 11 non-clean mutants fail `summarize.py` (MILAN dropped in one or all runs, a warning or misbehaving flag added, a compatibility event, a missing cluster, a changed static field, complaints=1, a query error, rc 5, a wrong entity), and the unmodified copy passes (`receipts/probe_summarize_mutations.txt`). A live negative control also exists: the same library binaries and an enumerator identical apart from the DUT filter returned Milan FAIL on this DUT on 2026-09-23. Library tag `v4.3.1.1` resolves upstream to `6d61a92e...`, and the compile options printed in every run log equal the library's default CMake options at that revision. `CONTINUE_MISBEHAVE_AEM_RESPONSES` still raises the Misbehaving flag, so it cannot hide a failure (`receipts/library_provenance.txt`). The probe's process rc does not encode the verdict (rc 0 with no flags would be possible). The page does not claim otherwise: it reports rc and flags separately.
3. **Independent runs, matching inventory: holds.** Three START/END windows that do not overlap, each with rc 0; a fresh `run-N` directory per run (`mkdir(exist_ok=False)`); one controller instance per process. Online-event order and library statistics differ between runs (enumeration 234/229/169 ms; unsolicited 9/8/10), so these are separate enumerations, not copies. Re-running `summarize.py` on the published dumps reproduces `enumeration-summary.txt` and all three inventories byte for byte. The recomputed inventory equals the builder image's declared descriptor set type for type and index for index: 41 descriptors, 14 types, including AUDIO_CLUSTER 0-24 (`receipts/probe_aem_identity.txt`, `receipts/summarize_recompute.txt`).
4. **Scope: holds.** Three hunks only: :54, :464 and the B4 block. Every NOT RUN line other than the two Hive lines is byte-identical to base (`receipts/scope_hunks.txt`). Both Hive rows and B4 link the owner decision as recorded in issue comment 5858063707, and B4 states that box 4 is not cleared.
5. **Public-evidence hygiene: holds for the diff and the packet.** The repository's own scrub rules (`scripts/docs_check.py` `scrub_text`) give 0 hits over the 116 added lines and over all 51 packet files. Reviewer patterns (home paths, toolchain install paths, bench host role tokens, USB by-id, tty devices, IPv4) give no real hits: the IPv4-shaped matches are version strings, and the three serial-field matches are the publisher's masks (`receipts/probe_hygiene.txt`). The packet shows only `$HOME`-relative and `/tmp` paths. The identifiers left in the packet (the DUT entity, the reference peer's entity ID already in `docs/history`, the switch clock identity, a controller EUI-64) fall in the protocol-identifier class the merged page declares as retained. The compiler version on the page repeats the existing Tool revisions entry (:211).

## Clean lenses

```text
[R358] PASS RTL - git diff --stat 2a2a7bb6..bcba79a5 (docs only), git diff 9e9954e9..2a2a7bb6 (4 docs/evidence files, no gitlink change), receipts/probe_aem_identity.txt (builder AEM image from configs/endstation_ax7101_1x1_tdm8.yaml == cited 9b077636..., ENTITY/CONFIGURATION rows == AECP bytes), tb/verilator/csr/sim_main.cpp:350 (VERSION 0x00020060) - no RTL or builder change in the PR; the image the row measures is the one current source emits
[R358] PASS Robustness - review-evidence/117-hive-r1/author/tools/enum_probe.cpp:121-130,154-179 (usage/ABI/guard/absent-DUT exits 2/3/4/5), tools/enumerate_once.py (20 s timeout inside a 23 s bound, fresh run dir), tools/summarize.py:31-45 against receipts/probe_summarize_mutations.txt (11/11 non-clean inputs rejected), library src/controller/avdeccControllerImpl.cpp:6343-6345 at 6d61a92e (MisbehaveContinue still raises the Misbehaving flag) - negative verdicts, absent DUT, library tolerance options and hangs all end in a visible failure
[R358] PASS Tests - receipts/probe_summarize_mutations.txt, receipts/summarize_recompute.txt, receipts/a200_enum_vs_enum_probe.diff with page :53/:462 (same binaries + same enumerator returned FAIL on 2026-09-23), receipts/docs_gates.txt (docs_check, check_doc_style, gen_toc --check, check_em_dash --base 2a2a7bb6 over 116 added lines, check_doc_paths, ci_scope --selftest, check_baremetal_only --check, git diff --check: all RC 0) - the evidence checks can fail for the defects they claim to detect, and every documentation gate at this head is green
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #117 acceptance boxes 4 and 5; comment 5858063707; page :54, :58, :464, :536-650; packet identity, run logs, dumps, summary | R358-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| RTL | CLEAN | diff stat base..head; `9e9954e9..2a2a7bb6` diff; regenerated AEM image and descriptor rows; VERSION constant in the CSR simulation | R358-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| Robustness | CLEAN | `enum_probe.cpp` exit paths; `enumerate_once.py` bounds; `summarize.py` assertions under 11 mutants; library misbehave handling at `6d61a92e` | R358-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| Tests | CLEAN | mutation probe; summary recompute; earlier-enumerator diff and the 2026-09-23 negative control; eight documentation gates rerun at head | R358-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |
| Docs | UNCLEAN (F1) | page diff; Contents :31; Raw artifacts convention; publisher `MANIFEST.json`; hygiene sweep of diff and packet | R358-1 | `bcba79a50ecd2eca99db91c4f3802d888eaac7e4` |

## Prior public findings on this PR

None existed when this round ran. PR #598 had two comments (the review-start notices for R358-1 and R359-1), no reviews and no review comments. The reviewer read them only after recording an independent draft verdict (`receipts/independent_draft_before_prior_reviews.txt`). No other reviewer's report was read.

## Limits

- No bench access, by design. Everything measured on hardware (UART, AECP, the three enumerations, bench-lock and cleanup statements) is judged from the raw artifacts only. Bench-lock use, the absence of binds or writes, and remote cleanup are author statements that no raw artifact proves beyond `cleanup.txt` and `final-uart.txt`.
- The bitstream running on the FPGA is tied to the cited bitstream by QSPI payload CRC32 and the VERSION CSR, not by SHA-256 readback, as the page itself says. The reviewer did not rebuild the bitstream.
- The library and probe binaries are not public. Their identity rests on the recorded SHA-256 values and on the runtime version and option lines in each log. The reviewer checked the upstream source at the recorded revision; the binaries were not rebuilt.
- The recorded bytes of the three entity dumps were reconstructed by restoring the DUT's configured serial string; the originals themselves are not public.
- The scoped simulator was not used: the diff has no RTL or test-bench change.
- The reviewer found no public comment recording the manager's source static/builder and native bank results at this head, so they were not judged here.

## Pending manager duties

- Hosted evidence at `bcba79a5` when checked (17:50Z): `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git` and `full-ci-gate` succeeded; `docs-check` was still in progress; `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `yosys-elaboration` and physical gPTP were skipped (not executed) for this docs-only scope. Hosted and local-replica acceptance stay with the manager.
- Candidate merge validation against the live dev tip, post-merge containment, and the second independent review (R359-1) remain open. A fix for F1 needs a re-review at the new head covering Docs and Conformance.
- Physical calibration is NOT RUN, and field skips are not hardware proof. Acceptance box 4 keeps its NOT RUN rows (behave hardware tier, latency #64/#213, audio continuity deferred to 2026-12-31), and #117 stays open.

## Receipts

Listed in `MANIFEST.sha256`: the four probe scripts (`probe_aem_identity.py`, `probe_summarize_mutations.py`, `probe_hygiene.py`, `probe_page_claims.py`) and `receipts/*`. The clone was restored and verified identical to the exact head: tracked index blob/mode digest, `.git/index` hash, submodule gitlinks and status all match before and after, with no untracked or ignored files (`receipts/clone_state_before.txt`, `receipts/clone_state_after.txt`).

R358-1 FINISHED
