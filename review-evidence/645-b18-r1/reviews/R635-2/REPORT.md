[R635] POSITIVE - exact head b3f7a696713a96b42265e08a8c3a04a430b7b5ed

R635-2, external independent delta review of issue #645 / PR #747.
Tree: `57d505ff2fcb01a2f51f631c9784701f41716e8f`.

The provenance finding is resolved at its cause. All three suggestions and the PR counter-sentence residue are addressed. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION was found. All five lenses are CLEAN for this delta. The documented observations support the manager's #645 close condition. This verdict does not authorize merge or discharge the remaining manager gates.

## Scope and independence

Examined the full change from base `9ef717727e6fdac11ee7f01672fefae948452343`, then judged the delta from `480c5e916f8bf711c47e1985ba3efe2b2471bdda`: one findings page, +35/-12 lines. No code, test, interface, submodule, table cell or measured figure changed in round 2. Unchanged implementation coverage carries forward under the owner's later-round rule; no fresh full-bank coverage is claimed.

Read the operating contract, contribution rules, documentation index, issue acceptance and public scope decisions, linked design/register/flash authorities, history and diff, then public receipts. The independent verdict and five-lens ledger were written before reading prior reviewer reports. Afterwards, only the findings sections of public comments 6200475354 and 6200518911 were consulted for reconciliation. No private author material or another checkout was used.

Authorities: issue #645 body; [close ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217); [B18 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6199691564); [round-2 scope](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6200530754); `docs/design/MEDIA_CLOCK_FOLLOWING.md:1092` and `:1264`; `docs/reference/REGISTER_MAP.md:1878` and `:2017`; `docs/design/TIME_SYNC.md:384`; `docs/integration/QSPI_FLASHBOOT.md:66`.

The earlier ruling publicly disposed the original switch acceptance. This review covers the remaining INTERNAL-bind acceptance and documentation delta, not a new switch campaign.

## R635-1-F1 disposition

**R635-1-F1 | prior MAJOR | Conformance, Tests, Docs | RESOLVED**

Artifact: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:5036`, the [manager provenance packet](https://github.com/kebag-logic/milan-fpga/tree/bbc53aabb02a1654812ba2eaa1642f5e36e69ce0/review-evidence/645-b18-r1/manager-provenance), and [continuity statement](https://github.com/kebag-logic/milan-fpga/pull/747#issuecomment-6200503436).

Authority/cause: acceptance requires attribution to the installed image containing PR #742. VERSION and AEM CRC alone cannot establish it. The prior finding required public build/image, verified-installation and cold-boot receipts connected to the measurements.

Verified chain:

1. `01-clone.status` names source `9ef717727e6fdac11ee7f01672fefae948452343` and tree `8979dd5abcb94b5af62c492f72343369dba6a64e`. Both match the Git objects. The merge incorporates PR #742. Shape/render receipts identify the 1x1 TDM8 build with eight render slots.
2. `provenance.json` records bitstream SHA-256 `4b5a391af524cb3b490099381c0fd9e3275383fc51c163a75fb78cdb054ffcca`, 3,825,992 bytes. Its AEM SHA-256 `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d`, 7,512 bytes, matches `flashboot_layout.json`; the layout CRC is `5ba355eb`. The layout separately records bitstream payload digest `d35ab1680127318b0c7abb84f69d13d87957b4d320dcf7f5c517656bed0e6c54`; this is not confused with the full bitstream-file digest.
3. `flash.log` names that target build over the earlier image. AEM write/verify precedes bitstream write/verify. Both verification phases complete, followed by `FLASH_RC=0`, a cold power cycle and `POWERCYCLE_RC=0`. Subsequent BOOTSTS records normal configuration without fallback. The operation spans 18:42:24 to 18:44:49 UTC.
4. `console-after-flash.log` records `CSR ID=4d494c4e VERSION=00020060`, AEM 7,512 bytes / CRC `5ba355eb`, and fabric entity enablement.
5. The identity lock window begins at 18:50:11.845 UTC; all eleven identity checks pass. The first bind is 18:50:56.251 UTC. The cycles finish at 18:59:53 UTC. The public manager statement supplies continuity: no intervening flash or power cycle, with actions serialized under the bench lock. The end baseline follows at 18:59:58 UTC.

The published flash log hashes to `a1539c67fc8c6490034332976024248decf3046fdc8da72a9c867762e09d9d46`, exactly the retrieval hash in R635-1-F1. This supplies the missing record without a new bench run. All sixteen provenance files equal their bytes at the page-linked `bbc53aab` revision.

Impact/required outcome: the missing image attribution is now public and linked. The page retains the explicit statement that no device read distinguishes the images. The image-specific acceptance claim is supported at this head. Verification: the read-only `verify_review.py` exits 0; see `verification.log` and `verification.rc`.

## Other prior items

| ID | Prior severity / all assigned lenses | Disposition and artifact | Evidence |
|---|---|---|---|
| R634-1-S1 | SUGGESTION / Conformance | RESOLVED, findings page:5142. Names c01/c10, the 0.05 s shortfall, poll timing and cumulative coverage. | Raw last-poll bounds are +31.702083 s and +31.700514 s. All later reads, including the end baseline, remain zero. Bind does not clear the counter; those later reads cover the tails under the recorded no-reset continuity. |
| R634-1-S2 | SUGGESTION / Robustness, Docs | RESOLVED, page:5123, :5159, :5275. All three say “the design's earliest firing time.” | Design requires 2,048 consecutive settled/disengaged ticks. `milan_datapath.sv:6645` and the pending-dwell logic restart the dwell on disturbances. No fixed observed firing instant is claimed. |
| R634-1-S3 | SUGGESTION / Docs | RESOLVED, page:5019. Names `review-evidence/645-b18-r1/author`, branch `645-b18-review-evidence`, commit `2e913519`. | All 90 original author files equal the bytes at the named commit. The page also directly links the provenance packet. |
| R634-1-RS1 | RESIDUE / Docs | RESOLVED, current PR body, “Counters that moved.” Uses the requested “other error counters stayed at 0; MEDIA_LOCKED read 1 at both reads.” | Decoded all twenty raw cycle start/end payloads: DUT MEDIA_LOCKED and AVB_INTERFACE LINK_UP remain 1; named DUT error counters remain 0. Snapshot: `receipts/pr-body.md`. |

No prior finding is retained or deferred. No source-comment residue is introduced: this delta has no source comments. Existing source-comment lane labels remain unchanged under the owner's #746 disposition.

## Reviewer-owned lens ledger

Evidence packet: `review-evidence/645-b18-r1` at `1a86b31dd03c479a196ece2b532d2141279be4d1`. “Page” means `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` at the reviewed head. CLEAN rows are artifact-specific PASS results.

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page:4982, :5036, :5142; frozen assignment/ruling; provenance and cycle receipts. Image attribution is supported, ten held binds meet the ruled close condition, and the tail clarification preserves acceptance evidence. | R635-2 | b3f7a696713a96b42265e08a8c3a04a430b7b5ed |
| RTL | CLEAN | `delta.diff`; `hdl/milan/milan_datapath.sv:6615`, :6645; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:1002`, :1050, :1142; `REGISTER_MAP.md:1878`, :2017. No implementation/interface change. Timing language matches the dwell logic; cumulative counters support the tail explanation. Prior unchanged-code coverage carries forward. | R635-2 | b3f7a696713a96b42265e08a8c3a04a430b7b5ed |
| Robustness | CLEAN | Page:5123, :5142, :5275; design settle table; 800 raw polls and baseline-end receipt. No saturation, missing reads or counter discontinuity. Later zero reads cover short tails. Disturbed dwell, unseen firing, early residual and following-mode limits remain explicit. | R635-2 | b3f7a696713a96b42265e08a8c3a04a430b7b5ed |
| Tests | CLEAN | `verification.log`; packet `author/cycles/c01` through `c10`, both baselines, both summary tables, `author-r2/gates/gates-r2.txt`. Rechecked every poll, digest, identity ordering and twenty table rows. Seven author gates name this exact head. No changed test or grader. | R635-2 | b3f7a696713a96b42265e08a8c3a04a430b7b5ed |
| Docs | CLEAN | Page:5019-5058, :5123, :5142, :5159, :5275; current PR body; `delta.diff`; public scope/provenance. Linked evidence bytes match, requested wording is present, and no figure, grade or clause claim changed. | R635-2 | b3f7a696713a96b42265e08a8c3a04a430b7b5ed |

## Reproduction and integrity

Run `python3 verify_review.py /path/to/candidate`. The clone must contain evidence revision `1a86b31dd03c479a196ece2b532d2141279be4d1` and its ancestry. The script reads Git objects and files; it runs no packet-supplied executable.

Exit 0: 200 published author/provenance hashes verified, excluding reviewer reports; source/tree and packet-link consistency checked; receipt ordering checked; all 800 polls and twenty counter payloads rechecked; both ten-row tables match. The raw counter digest remains `2c5e8d6ff8220cb16a9a3d0535279dfd7f04b5642c9aee2d9f97cdefcd939bdb`.

All 1,370 tracked blob bytes/modes and every index record match HEAD. All six submodule gitlinks match, including protocol-processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` and gPTP processor `e4869fd0c42889b2ac806587cc5c78afb1c33461`. Submodule worktrees are uninitialized; no submodule execution is claimed. The working tree is clean. No source mutation/restoration was needed.

The author round-2 receipt records seven successful documentation/source-hygiene gates at this exact head, including 338 added Markdown lines. These are author source-head execution receipts. This reviewer independently ran the focused receipt verifier and whitespace diff check, not the full banks.

## Real limits and pending manager duties

- The bitstream binary is absent from this packet. Its full-file hash and build attribution rely on the public manager record, cross-checked against layout/install/boot receipts. No independent rebuild or physical readback was performed.
- Evidence commits `1a86b31d` and `bbc53aab` are unsigned according to the repository API. Their content hashes were checked; no signed-packet claim is made. Source merge `9ef71772` is reported verified, reason `valid`. See `receipts/signature-status.json`.
- Cold-boot-to-measurement continuity rests on the public manager statement and dated receipts, not an independent hardware monitor. The unchanged VERSION/AEM identity does not distinguish images.
- No raw capture replay in this delta review. Existing summaries and unchanged figures were spot-checked; raw counters were fully rechecked. Printed precision is not calibrated accuracy. Physical calibration is NOT RUN; field skips supply no hardware proof.
- Ten INTERNAL binds on one DUT/peer configuration are bounded evidence. The recentre is not observable through these CSRs. Earliest-window disturbance coverage, the #743 residual and binds under following remain limits. Held counters do not prove an exact firing time.
- No manager source bank exists at this head, and none is inferred. Final current-dev candidate validation is separate, even with the supplied source base and live dev both `9ef717727e6fdac11ee7f01672fefae948452343`.
- The manager owns publication, hosted/local-replica acceptance and final candidate construction with builder/native-bank receipts. Hosted contexts were not inspected here; executed jobs must remain distinct from skipped contexts. Merge authorization, containment, issue closure and project completion remain manager duties.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch material is excluded.

R635-2 FINISHED
