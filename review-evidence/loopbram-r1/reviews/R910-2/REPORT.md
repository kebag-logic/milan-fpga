[R910] NEGATIVE - exact head dc78aedae34c25a97125ecd6816a1f645db5575f

External independent review R910-2 of issue #979 / PR #987.
Tree: `41223b89427673df91715a56a7e8a647d9a339e4`.
Implementation base: `3cda030c174b325e36c26af6420487ff91346d15`.
Delta re-reviewed: `2e278379c1ae9ea09063b3e3cb183d0e8a3f0929..dc78aedae34c25a97125ecd6816a1f645db5575f`, six commits, 22 changed files. The full base-to-head diff supplied the context for changed dependencies; unchanged code retains the preceding review's scope.

Two MAJOR findings remain: the concurrent-output test accepts a completely missing talker, and the changed enabled 8x8 implementation lacks current routing evidence. Neither finding asserts an observed defect in the unmodified product RTL. All five lenses were applied. An independent initial verdict and ledger were written before reading the preceding public review findings; their dispositions follow below. No current concurrent review report, private implementation material, or private management directory was read.

**R910-2-F1 — MAJOR — Conformance, Tests — a missing output stream passes the concurrent integration check.**

Artifacts: `tb/verilator/input_loopback_dp/sim_main.cpp:483`, `:495`, `:503`, `:710`, `:715`; disposable plant at `hdl/milan/milan_datapath.sv:1728`; `receipts/parent-missing-talker7.log`, `receipts/missing-talker-probe.json`, and `scripts/probe_parent.py --missing-talker`.

Authority/evidence: #979 requires received audio retransmitted through the input mapping. R910-1-F1's required outcome explicitly includes all destinations and output streams concurrently at 8x8; R909-1-F3 requires the full-slot enabled parent check. The new scoreboard checks samples only when a packet arrives. `ALL_TALKERS_TRANSMIT` compares one aggregate packet count with `20*kStreams`; it has no per-stream minimum. Expected samples left in `pending_wire[stream]` are neither bounded nor checked at completion, and clipping clears these queues.

The clean 8x8 run passes 122,517 checks with 704 packets. A disposable one-line parent connection plant changes `.stream_en_i (aaf_stream_en_w)` to `.stream_en_i (aaf_stream_en_w & N_STREAMS'(8'h7f))`, suppressing talker 7 throughout both traffic phases. It compiles and still passes: **113,805 checks, zero failures, 616 packets**. All 34,004 capture words are still graded; the seven remaining talkers satisfy the aggregate threshold. This is a runtime surviving fault, not a compile failure or an edited assertion.

Impact: the claimed eight-output end-to-end check can pass with one entire output absent, leaving its seven mapped loopback destinations unverified on the wire. The parent-integration portion of the earlier findings is substantially repaired, but its required concurrency proof is not complete.

Required outcome: grade delivery separately for every configured output stream in the relevant traffic phases. Account for expected words that never arrive, allowing an explicitly bounded partial-packet tail or draining to a defined completion point. Preserve the existing sample, silence, mapping, and deadline assertions. Add a missing-output negative control.

Verification: both clean supported shapes pass; suppressing any required output at 8x8 fails a named runtime delivery/completeness assertion. The plant above must no longer pass. No product behavior change is prescribed.

**R910-2-F2 — MAJOR — Conformance, RTL, Tests — enabled 8x8 routing acceptance is outstanding after the RTL changes.**

Artifacts: issue #979 acceptance; `docs/design/INPUT_MAPPED_LOOPBACK.md:381`, `:395`, `:401`; `hdl/ieee1722/aaf/KL_render_queue.sv:777`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:1370`; public `author-r4/REVIEW-READY.md` physical-evidence section and `author-r4/receipts/route-summary.json.txt`.

Authority/evidence: the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/979) requires both shapes routed at [#818's floor](https://github.com/kebag-logic/milan-fpga/issues/818): every signoff corner must have setup slack at least +0.030 ns and nonnegative hold slack, using the selected qualifying recipe. The [topology ruling](https://github.com/kebag-logic/milan-fpga/issues/979#issuecomment-7096503041) records BRAM overflow as S14 debt; it does not waive routing. The reviewed delta changes sample retention, metadata addressing, scheduling, capture state, timestamp comparison and enabled parent connections. Previous enabled-route evidence therefore does not cover unchanged physical inputs.

The exact-head packet supplies a fresh enabled 1x1 route only and explicitly says the enabled 8x8 route was not repeated. Its four 1x1 corner reports check out: fast corners +1.636/+0.036 ns, slow corners +0.124/+0.102 ns, setup/hold respectively, with zero failing endpoints. That establishes the 1x1 floor, not the 8x8 floor.

Impact: the mandatory enabled 8x8 timing result is unknown for the implementation under review. Disabled netlist equality and the 1x1 route do not prove it.

Required outcome: publish enabled 8x8 routing and resource receipts for this implementation, or a later reviewed implementation, under the unchanged measurement recipe and bounds. A measurement export may continue to identify the 70.5-tile control-memory allocation as S14 debt and retain the ordinary allocator's refusal. If the owner intends to waive routing, obtain an explicit public acceptance change; the existing overflow disposition is not that waiver.

Verification: source-bound routed reports identify the selected directive, all corners, resource counts and routing status, and meet #818. Independent review then clears this finding. No route was run in this review.

**Prior finding reconciliation**

The preceding [external findings](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7116849876) and [internal findings](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7117492309) were read after the independent delta pass. Closure below follows each finding's stated required outcome, not the author's closure label.

| Prior ID | Disposition at this head | Cause-level evidence |
|---|---|---|
| R909-1-F1, BLOCKER | RESOLVED | Both original plants remain. Bind-wipe uses `flush_w`; the PHC-reset plant again matches the restored original instance boundary. Independent `receipts/anchors.log` ends `ANCHORS INTACT 0`. Published exact-head queue log line 112 catches bind wipe and line 129 reports 28/28. Parent log part010 line 1932 catches the PHC-reset plant. Both campaign execution receipts exit 0. Drain, payload and timestamp anchors changed by the later commits were inspected too. |
| R909-1-F2, MAJOR | RESOLVED | Capture retains the original two-bit main FSM; optional pair state is inside `g_input_loopback`. Queue copy state and parent invalidation state are enabled-only. Disabled port widths and shared mapping writer retain the base structure. Both complete-release canonical byte streams rehash to the published equal base/head values; published LUT/FF/BRAM/DSP counts are equal at both sizes. Scope limits are stated below. |
| R909-1-F3, MAJOR | PARTIALLY RESOLVED; concurrency retained as R910-2-F1, Conformance and Tests | Generated enabled parent controls run production command handling, real map transactions, GET pages, clipping and in-copy invalidation. The parent connection plant fails runtime samples. All capture slots are graded, but the wire completeness check accepts an absent talker. |
| R910-1-F1, MAJOR | PARTIALLY RESOLVED; retained as R910-2-F1 under its original Tests lens | Same parent-path repair and remaining concurrency hole. The Conformance attribution is also retained from R909-1-F3. |
| R909-1-F4, MINOR | RESOLVED by its explicitly permitted documentation outcome | `tb/verilator/input_loopback/README.md:47`, design document final paragraph, and parameter contract identify bind-only flush, one-shot claim, expiry, backlog and age as untested in isolation. This is not mutation coverage. No open MINOR is retained for the outcome the original finding expressly allowed. |
| R909-1-F5, MINOR | RESOLVED | Queue line 781 refuses enabled `KMIN_C > 2`. `bounds.py` requires the named elaboration refusal at both sizes. Eight sample pages and the full three-bit claimed address repair overlap retention; published four-page and truncated-address plants build and fail sample checks. |
| R909-1-F6, MINOR | RESOLVED | Queue lines 815-846 derive four clock cycles plus 1000 ppm over K+1 periods plus rounding. Published bounds logs show both signed ramps pass at 84 ns wrapper jitter and fail sample checks at 87 ns, at both shapes. This is injected timestamp error, not an oscillator or hardware drift measurement. |
| R909-1-F7, MINOR | RESOLVED | Capture banner includes two extra cycles per slot; queue banner covers copy before scrub and enabled clock-loss flushing. Parent controls measure claim-to-last-pair spans of 89/873 cycles and apply the deadline check. Packed extension fields match the parameter table. |
| R909-1-R1/R2/R3, RESIDUE | RESOLVED | Session attribution removed from design; off-tree references replaced by PR links; builder row 16g follows 16e. |
| R910-1-R1, RESIDUE | RESOLVED | Design line 107 now refers to fresh leaf measurements on PR #987. |
| R909-1-S1, SUGGESTION | ADDRESSED | PR body and handoff disclose split layout-3 NAME capacity instead of the absent all-fabric 128-record backend; resource ledgers remain unchanged. |

No additional wording residue or suggestion is raised. Added source comments in the six-commit delta contain no new review/session identifiers, bench labels, or issue-comment IDs.

**Evidence and independent checks**

Public evidence was read at [immutable commit e2c78ae95c03c85e4ab16695a6ed4ca8d1e30f46](https://github.com/kebag-logic/milan-fpga/tree/e2c78ae95c03c85e4ab16695a6ed4ca8d1e30f46/review-evidence/loopbram-r1), concentrating on `author-r3` and `author-r4`. `receipts/evidence-audit.json` verifies all 1,645 published author-file hashes and all 1,958 recorded candidate source hashes. Nested manifests have 80 and 60 publication-normalized files respectively, accounted for by the outer manifest. The audit-script token-list redaction named by the publication commit leaves that script's inner hash stale; its current outer hash matches. That script is not a gate-result receipt and is not used as such. The evidence commit has no Git signature (`N`); this review verifies public content hashes and source binding, and does not claim signer authentication.

| Independent operation | Result |
|---|---|
| Mutation-anchor census | All head anchors occur exactly once; `ANCHORS INTACT 0`. |
| Enabled parent 1x1 | 16,169 checks, zero failures, 4,248 capture words, 88 packets, five first-eligible generations, maximum walk span 89 cycles. |
| Enabled parent 8x8 | 122,517 checks, zero failures, 34,004 capture words, 704 packets, five first-eligible generations, maximum walk span 873 cycles. |
| Parent edit-invalidation plant, 8x8 | Executable builds, exits 1 with 1,544 failures including `PARENT_SAMPLE`; compilation is not counted as detection. |
| Missing-talker plant, 8x8 | Executable builds and incorrectly passes with 616 packets; R910-2-F1. |
| Replacement-only invalidation hypothesis | Plant survives, but is not a finding: the production command core rejects conflicting ADD over an occupied key (`aecp_maps.c:494-507`). Supported replacement is REMOVE then ADD, which the parent test exercises. No direct accepted-overwrite behavior is inferred or required by this report. |
| Checkout integrity | Direct blob hashes, executable/symlink modes and index match the exact head; all four required initialized submodules match their gitlinks and their tracked bytes/index. See `receipts/checkout-integrity.json`. |

Canonical release netlists were independently concatenated from the published exact-byte chunks as instructed by their index, with every chunk hash and size checked. The resulting values match both sides in the elaboration receipts:

| Disabled shape | Bytes | Re-derived SHA256 | Base/head LUT, FF, BRAM tiles, DSP |
|---|---:|---|---|
| 1x1/1if | 20,626,655 | `18af89e620ea88ee2a745550bd25b1645702cec071bcba36decced2b5376d9af` | 33,792; 42,649; 80; 11, equal |
| 8x8/1if | 29,443,265 | `fe344bba8709f7b8e72075b38aa81619c316c2207f948e0adaea1540e36da767` | 45,199; 53,086; 99; 11, equal |

The published elaboration recipes use the complete release top and remove only comments, attributes and surrounding whitespace for canonical comparison. Identifiers, widths and connections remain. I inspected the recipe, canonicalizer, changed-connection control and disabled utilization reports. I did not independently rerun release elaboration or synthesis: the independently re-derived hashes cover the published canonical bytes; the two-sided production of those bytes remains author execution evidence. FPGA configuration-bitstream identity and ELF debug-section identity are not claimed.

The exact-head author receipts also cover seven leaf plants, four parent plants, affected regressions, the 114-entry builder union and portability. These are author source-head runs, not manager source banks. The builder union retains the documented calibration row as NOT RUN. Enabled allocation is 47.0 control-memory tiles at 1x1 and 70.5 at 8x8. The latter is +11.5 above the unchanged 59-tile ledger and remains S14 debt; the ordinary allocator still refuses it. This debt is not a substitute for routing evidence.

**Reviewer-owned lens ledger**

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | Issue #979 body/ruling; #818; generated input geometry and AECP map handling; design validation contract; parent command/audio test and physical receipts | R910-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| RTL | UNCLEAN: F2 | Queue lines 596-940; capture lines 928-1522; parent invalidation/wiring and shared writer; disabled canonical recipe/counts; missing enabled 8x8 route | R910-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| Robustness | CLEAN | Queue invalidation, retention, expiry and lead refusal; parent rejected/no-op edits and clipping; bounds receipts; F4's permitted explicit untested-guard disposition | R910-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| Tests | UNCLEAN: F1, F2 | New parent run/scoreboards/plants, leaf bounds, restored mutation anchors, independent controls and missing-talker probe, public exact-head gate receipts | R910-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |
| Docs | CLEAN | Design contract, parameter tables, both test READMEs, capture/queue banners, builder row 16g, PR body and handoffs; prior residues reconciled | R910-2 | dc78aedae34c25a97125ecd6816a1f645db5575f |

[R910] PASS Robustness — `hdl/ieee1722/aaf/KL_render_queue.sv:781`, `tb/verilator/input_loopback/bounds.py`, published bounds/guard receipts — applied lead, retention, invalidation, reset/clock-loss, rejected-edit and clipping review; no remaining finding under this lens, subject to the explicitly untested guards.

[R910] PASS Docs — `docs/design/INPUT_MAPPED_LOOPBACK.md`, `hdl/ieee1722/aaf/README-parameters.md`, test READMEs and changed module banners — interfaces and proof limits match the delta; previous wording items are corrected.

**Limits, reproduction and pending manager duties**

The reviewer used public scope, repository authorities and executable evidence. Milan v1.2 5.4.2.26-.28 govern fixed-page enumeration, atomic ADD validation and REMOVE semantics; the related mono-cluster and port-relative descriptor obligations remain the approved topology's contract. The official consolidated PDF endpoint returned HTTP 403 during this round, so no fresh direct-standard-text verification is claimed. This delta review retained the prior direct-clause review where behavior was unchanged and checked the changed generated defaults and command integration against the repository's cited authorities. The parent harness executes production command handling and the parent transaction server; processor instructions, mailbox transport and full gPTP behavior are outside its scope.

No full parent, processor, timing-processor, portability or builder bank was run independently. No hardware, shared installation, source fix, commit, push, GitHub write, container orchestration or merge occurred. Physical calibration was NOT RUN; field skips and desk checks are not hardware proof. Technical logs preserve all output with local paths normalized, documented in `receipts/log-integrity.json`.

Portable checks, from the packet directory after extracting the public author evidence under `scratch/review-evidence/loopbram-r1`:

```sh
rtk proxy python3 scripts/audit_evidence.py "$CHECKOUT" scratch/review-evidence/loopbram-r1 receipts/evidence-audit.json
rtk proxy python3 scripts/anchor_counts.py "$CHECKOUT" "$CHECKOUT" 3cda030c17 dc78aedae34c25a97125ecd6816a1f645db5575f
rtk proxy python3 scripts/probe_parent.py "$CHECKOUT" "$PACKET" "$SIMULATOR"
rtk proxy python3 scripts/probe_parent.py "$CHECKOUT" "$PACKET" "$SIMULATOR" --integration
rtk proxy python3 scripts/probe_parent.py "$CHECKOUT" "$PACKET" "$SIMULATOR" --missing-talker
rtk proxy python3 scripts/verify_checkout.py "$CHECKOUT" receipts/checkout-integrity.json
```

The simulator identity receipt records verified version 5.050. Foreground probe drivers used at most two builds with eight jobs each; every process completed. All disposable sources/builds remain under `scratch/`. Tracked source bytes were never altered.

The manager still owns hosted/local-workflow acceptance, publication, the other independent review, and construction plus full validation of the current-dev merge candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. There is no manager source-head bank claimed here. Final merge-candidate validation is distinct from these author source receipts and from the missing enabled 8x8 route. Hosted contexts were not independently inspected in this round. No approval or merge is cleared while F1 or F2 remains open; after any corrections, re-review affected lenses at the new exact head and retain post-merge containment duties.

R910-2 FINISHED
