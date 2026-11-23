[R898] NEGATIVE - exact head a18f0996f4b1b654a232dfe56fa64ee7ecaf697e

Internal cleared-context review R898-2 of issue #963 / PR #984. Tree `a897a1e08c1cd4b63c37b0e5625b819d4649d568`. This
is a delta re-review from `4cca9569`, the head R898-1 and R899-1 reviewed, to `a18f0996`. All five lenses were applied
to the delta.

**Overall:**
- Every named round-1 finding is resolved at this head: R898-1 F1, R1 and S1, and R899-1-F1 and F2.
- The new test and plant do what the PR says. The order plant is caught by name at the head and escapes the prior
  test.
- **One new MINOR is open, F1 (Tests, Docs).** The PR body and the round-2 REVIEW READY say "a further 4,000 edits
  carry the new mapping". Measured, 469 of them do.
- F1 is a correction to published text only. No code, test or measurement has to change. After the text is corrected,
  a reviewer re-reads it at this same head and Tests and Docs are re-covered.

## 1. Reconstruction

**Order read:**
1. AGENTS.md and CONTRIBUTING.md.
2. Issue #963: the body's frozen acceptance, the TAKEN comment and both REVIEW READY comments.
3. The PR #984 body as published at this head.
4. The linked authorities: Milan v1.2 5.4.2.27-28 and IEEE 1722.1-2021 7.4.45-46, as cited, and #943 and #894.
5. `git diff 4cca9569..a18f0996`, read in full, and `git diff --name-only` from `dd163e41`, `25d3dd7a`, `50d3f10e` and
   `4cca9569`.
6. The author's round-2 packet `review-evidence/963-r1/author-r2` at `7bd1b854`.
7. Only after my own pass over the delta: the round-1 findings (R898-1 issuecomment-7098554389, R899-1
   issuecomment-7097239671).

The other reviewer's round-2 report was not read.

**The delta** (`receipts/delta-and-scans.txt`) is one commit and two files:
- `sw/firmware/ctrl/test/test_aecp.cpp`;
- `sw/firmware/ctrl/test/aecp_map_mutants.py`.

No firmware, RTL, `tb/` or doc file changed after `25d3dd7a`. `25d3dd7a..a18f0996` adds only
`docs/design/SPLIT_CONTROL_MEMORY.md`, and `50d3f10e..4cca9569` is that doc alone.

**Packet integrity:**
- All 349 `author-r2/` entries of `review-evidence/963-r1/MANIFEST.json` (sha256 `dd660e59…f790`) match their files.
- No file in the packet is unlisted.
- Two scripts are flagged as path-redacted.
- The host reports evidence commit `7bd1b854` as unsigned. Integrity here rests on the manifest hashes.

## 2. Independent pass over the delta

### The check order

At `aecp_maps.c:534` the legality flag is tested before `idle()`:
- `legal()` (`:114-125`) refuses a stream channel at or past `format_channels` of the stream's format, at `:117`.
- `idle()` (`:275-289`) reads the port only for an output stream not yet in the edit's table.

The plant `map-read-before-legal` swaps the two tests. Its site text occurs exactly once.

### The definition (`test_aecp.cpp:2869-2991`)

The illegal mapping now also takes the form `{0 or 1, past[in], 0, 0}`:
- `past[in]` is `(fmt >> 22) & 1023`, which equals `format_channels`: bits 31..22 of the 8-byte format are
  `p[4] << 2 | p[5] >> 6`.
- Stream 1 takes stream 0's format (`:2916`), so stream 1 has the same boundary.
- Edit mappings come only from `legal()` (channel < 4) and from `lawful`. So `channel == past` occurs only where it
  was injected, and `past >= 4` is asserted.

`o.unread` is assigned at every mapping. The definition returns at the first refusal, so the value it returns is the
refusing mapping's. It is true only for an output edit refused at an existing-stream illegal mapping whose stream the
edit has not read, which is exactly the case where the plant adds a read.

The RNG sequence of edits 0-3,999 is unchanged:
- `at = next() % size` is the old single draw.
- The extra `next() % 2` stream draw happens only when `c >= ABSENT`.

### Comment rule

The new comments state behaviour with `#963` only. The added lines contain no lane label, round, reviewer ID or
comment ID (scan in `receipts/delta-and-scans.txt`). No RESIDUE.

## 3. Probes (reviewer-owned, at the head; scripts in this packet)

How the probes ran:
- `probe.py` builds and runs the campaign's own `aecp_arms.core_arm` and grades with the campaign's own `caught()`.
- The arm compiles the clone's own `test_aecp.cpp`. So the probes that need another test write it into the clone and
  restore the head blob afterwards (`run_swapped.sh`, `run_carriers.sh`). The restore is hash-checked.
- After the probes, every tracked blob, mode and index entry and every submodule gitlink equals the head's
  (`receipts/restore-check.txt`). The ignored `__pycache__` directories my imports created were removed.

| Probe | Test | Plant | Result | Receipt |
|---|---|---|---|---|
| control, app arm | head | none | pass: `MapEditsAreTheirDefinitionRowForRow`, `MapEditWorkObservesEachOutputStreamOnce` | `probes/head-control-app.txt` |
| control, work arm | head | none | pass | `probes/head-control-work.txt` |
| order plant | head | `map-read-before-legal` | **caught on its words**, "the edit reads its port once for each output stream its definition reaches" (reads 1 vs 0) | `probes/head-plant-read-before-legal.*` |
| order plant | `4cca9569` | `map-read-before-legal` | **escapes** (rc 0); the prior test passes unplanted | `probes/prior-test-*.txt` |
| boundary plant (mine) | head | `legal()` `>=` -> `>` at `:117` | caught | `probes/head-plant-channel-boundary.txt` |
| boundary plant (mine) | `4cca9569` | same | escapes the edit test | `probes/prior-test-plant-channel-boundary.txt` |
| tallies | head, floors raised to 1,000,000 | none | ADD 0 795, ADD 7 3,023, ADD 8 285, REMOVE 0 1,223, REMOVE 7 2,674, keeps-equal 117, refused-after-read 2,773, **refused at an illegal mapping of an unread stream 86** | `probes/head-tally-floors-raised.*` |
| carriers | head plus a counter | none | **edits 0-3,999: 451 carry the no-stream kind; edits 4,000-7,999: 469 carry the existing-stream kind** | `probes/head-illegal-carriers.*` |

Other checks at the head:
- **The gate's own shard inventory:** `PASS: 1848 live invocations in exactly one shard; shard sizes [88, 827, 391,
  542]` (`receipts/shard-inventory-head.log`).
- **The campaign table:** 390 rows, all names distinct. 17 rows are graded by the edit test, `map-read-before-legal`
  among them, so 16 others (`receipts/delta-and-scans.txt`).

## 4. Round-1 findings, at their cause

| Finding | State at `a18f0996` | Evidence |
|---|---|---|
| R898-1 F1 / R899-1-F1 (MINOR, Tests, Docs): "1,846 plants caught" | **Resolved** | See "How F1 was rechecked" below |
| R898-1 R1 (RESIDUE, Docs): "The port is called exactly as before." | **Resolved** | The PR body's "Its observation" bullet now carries the exact replacement sentence, and the old sentence is gone |
| R898-1 S1 (SUGGESTION, Tests, Robustness): only an absent-stream illegal mapping | **Resolved** | The edit-definition table and the plant table both changed. My probes confirm the plant is caught at the head and escapes at `4cca9569` |
| R899-1-F2 (MINOR, Tests, Docs): verification marked complete | **Resolved** | See "How R899-1-F2 was rechecked" below |

**How F1 was rechecked.** I recounted with my own classifier (`recount.py`, `receipts/recount.txt`) over the
published complete logs:
- Shard 0 at `25d3dd7a`: 88 `[ok] arm` lines and no plant lines.
- Shards 1-3 at `4cca9569`, which has the same firmware, tests and tables as `50d3f10e` (doc-only difference):
  - shard 1: 826 control plants, and the line `mutants: 826 of 826 caught`;
  - shard 2: 389 plants;
  - shard 3: 541 plants and 2 pin controls.
- Total: 1,756 plants, 0 escaped.

The author's 50d3f10e excerpts carry raw-log hashes `6a4aba7c…`, `122c7b6f…` and `e338d933…`, the hashes the tally
quotes.

At the head, the 20 published partitions (all rc 0, all at `a18f0996`) hold 390 distinct `[ok]` rows and no
`[ESCAPED]` row. The PR's inventory line matches my run.

**How R899-1-F2 was rechecked.** In the PR body:
- "Required local verification bar passes" is unchecked.
- The Status table states the native sweep NOT RUN and owed to the candidate.
- Shard 0 is stated not re-run at the final head, and the gate command `--shard 2/4` not run at this head.

The claims also check against their receipts:
- Coverage: `firmware coverage: PASS (40 files)`, `aecp_maps.c 352/352 423/424` (`coverage/coverage-check`, rc 0 at
  the head).
- Docs steps: 43 of 46 rc 0. `gate_24` is rc 124, cut by the cap. Its step script (`test_firmware_compiler.py
  --selftest/--absent`) and `sw/builder/` do not name `sw/firmware/ctrl/test/`.

## 5. Findings

**F1. MINOR. Lenses: Tests, Docs.**
- **Artifacts:**
  - The PR #984 body, Description, "The check order, held by a test": "A further 4,000 edits carry the new mapping,
    and 86 of them are output edits refused at such a mapping of a stream not yet read."
  - #963's round-2 REVIEW READY (issuecomment-7100166169): "A further 4,000 carry the new mapping."
  - The packet copies `author-r2/PR-BODY.md` and `REVIEW-READY.md`.
- **Evidence:** `test_aecp.cpp:2956` injects an illegal mapping only when the edit is non-empty and `next()%8==0`.
  Counted at the head (`receipts/probes/head-illegal-carriers.*`), 469 of edits 4,000-7,999 carry the existing-stream
  kind, and 451 of edits 0-3,999 carry the no-stream kind.
- **Impact:** a published test-evidence figure overstates the new mapping's exposure by about 8.5 times. A cold
  reviewer would take the new path to be exercised 4,000 times. It is a figure, so it is not RESIDUE.
- **Required outcome:** both texts state what was drawn and what carried the mapping. For example: "A further 4,000
  edits are drawn with it as their illegal kind: 469 carry it, and 86 are output edits refused at such a mapping of a
  stream not yet read."
- **Verification:** the corrected figures match `receipts/probes/head-illegal-carriers.gtest.log` (`45100469` = 451 x
  100,000 + 469) and `head-tally-floors-raised.gtest.log` (86).

**RES-1. RESIDUE. Docs.**
- **Artifacts:**
  - The PR body, Status table, shard 0 row: "its 18 AECP arms, the only arms that compile `test_aecp.cpp`".
  - The REVIEW READY: "Only its 18 AECP arms, the ones compiling `test_aecp.cpp`".
- **Why:** `aecp_arms.all_arms` (`aecp_arms.py:172-191`) includes the image arms (`test_aecp_image.cpp`) and the debug
  arm (`test_aecp_debug.cpp`). So not all 18 compile `test_aecp.cpp`. The intended claim is true: every arm that
  compiles `test_aecp.cpp` is among the 18, and only `aecp_arms.py` and `aecp_mutants.py` reference it. The count, 18,
  and the verdict are unchanged.
- **Exact fix:** "its 18 AECP arms, which include every arm that compiles `test_aecp.cpp`".

**SUG-1. SUGGESTION. Tests, Docs (evidence traceability).**
- **Artifact:** `author-r2/receipts/firmware/plant-tally.txt`.
- **Issue:** it quotes raw-file sizes and hashes for `shard0-aecp-arms` (5,064 B, `baa43d78…`) and
  `aecp-campaign-20-partitions` (345,346 B, `bc475c84…`). No published file carries them. The published
  `shard0-aecp-arms/log.txt` is 5,013 B, `f43a9707…`, and the manifest records original = published.
- **Contrast:** the 50d3f10e excerpts carry the raw hash in a header. HOW.md explains that quoted hashes are of raw
  files, so this is not a defect.
- **Suggestion:** quote the published file's hash too, or add a header. Then a cold reader can tie each tally row to a
  published file. Both figures recompute from the published files directly (18 ok; 390 ok).

## 6. Lens results at the head

| Lens | Result | Artifacts examined at `a18f0996` | What was checked |
|---|---|---|---|
| Conformance | PASS | `aecp_maps.c:114-125,275-289,534`; `test_aecp.cpp:2869-2991`; IEEE 1722.1-2021 7.4.45-46; Milan v1.2 5.4.2.27-28 | **Delta:** the new illegal mapping (stream channel at the format's channel count) is refused with BAD_ARGUMENTS before the running check, and no mapping changes. This is what the clauses require for a mapping that references no valid stream channel. **Firmware:** no change since `25d3dd7a`, so R898-1's conformance evidence (harness, differential) carries. **Issue acceptance:** unchanged and still met, since the delta touches no measured artifact |
| RTL | PASS | `receipts/delta-and-scans.txt` (`git diff --name-only` from `4cca9569`, `25d3dd7a` and `dd163e41`); `aecp_maps.c:534` site | No RTL or firmware byte changed in the delta, so R898-1's RTL verdict (`aecp_maps.c`, images, `.su`) carries unchanged |
| Robustness | PASS | `test_aecp.cpp:2888-2902,2956-2959`; probes `head-plant-*`, `prior-test-*` | **S1's invalid-ordering case:** an existing stream mapped past its format is refused before its port is read. This is held in the output and input directions, and with the port running (`streaming`) or unanswered. **Plants:** the order plant is caught and the boundary plant is caught. **Prior test:** both escape it, so the gap S1 named is closed |
| Tests | **UNCLEAN (F1)** | `test_aecp.cpp`, `aecp_map_mutants.py:119-123`; probes; inventory; packet campaign partitions, coverage and docs receipts | **The tests themselves are sound:** the new test can fail for its defect, the floor of 20 has 86, the first 4,000 draws are unchanged, and the 16 other graded rows remain in a fully caught 390-row campaign. **Open:** the published figure "a further 4,000 carry the new mapping" (F1) |
| Docs | **UNCLEAN (F1)** | PR #984 body; #963 REVIEW READY 7100166169; `SPLIT_CONTROL_MEMORY.md:2628` (unchanged, not made stale by the delta); new source comments | **Resolved:** R1, F1-old and F2-old. **Comment rule:** 0 matches. **RES-1:** carried as residue. **Open:** F1 |

## 7. Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_maps.c:114-125,275-289,534`; `test_aecp.cpp:2869-2991`; IEEE 1722.1-2021 7.4.45-46; Milan v1.2 5.4.2.27-28; firmware unchanged since `25d3dd7a`, so R898-1's harness and differential evidence carries | R898-2 | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| RTL | CLEAN | delta name lists (`receipts/delta-and-scans.txt`); no RTL or firmware change; R898-1's RTL evidence carries | R898-2 | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| Robustness | CLEAN | `test_aecp.cpp:2888-2902,2956-2959`; probes `head-plant-read-before-legal`, `head-plant-channel-boundary`, `prior-test-*` | R898-2 | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| Tests | UNCLEAN (F1) | `test_aecp.cpp`; `aecp_map_mutants.py`; probes; shard inventory; `author-r2` campaign, coverage and shard-0 AECP-arm receipts | R898-2 | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| Docs | UNCLEAN (F1) | PR #984 body; #963 issuecomment-7100166169; `SPLIT_CONTROL_MEMORY.md:2628`; added source comments | R898-2 | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |

F1 touches no code, test, measurement or source document. Correcting the PR body and the evidence comment does not
change the head. So a reviewer's re-read of the corrected text at this same head re-covers Tests and Docs.

## 8. Real limits

**What I did not run:**
- No full firmware-gate shard command.
- No native Verilator sweep.
- No Yosys, builder, PP or gPTP bank.
- No harness run.
- No docs gate.

My execution was the focused probes above and the gate's shard-inventory self-check. Source-head gate evidence is the
author's published receipts, which I verified by hash and spot-checked by recount.

**The shard 1-3 recount:** the complete shard 1-3 logs at `50d3f10e` are not published; only first and last 400-line
excerpts are. The recount used the complete published logs at `4cca9569` instead, whose firmware, tests and tables are
identical.

**Hosted contexts at `a18f0996`, snapshot `receipts/hosted-snapshot.tsv` (12:28Z):**
- 14 completed successfully;
- 2 in progress;
- 13 queued, among them `firmware-aecp-mutants`, `firmware-unit`, `firmware-verilator` and the Yosys preparation.

No skipped context was counted as executed.

**Other limits:**
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No manager source bank exists at this head, and none is inferred.
- The evidence commit is unsigned, as the host reports. Packet integrity rests on its manifest hashes.

## 9. Pending manager duties

- Carry F1's correction to the PR body and the REVIEW READY, and have a reviewer re-read them at this head.
- Carry RES-1 to the residue checklist.
- At the merge turn, validate the current-dev merge candidate, with builder and native banks including the owed
  full native Verilator sweep, and link its receipts. The source base is `dd163e41`; live dev is `e275d795`.
- Own hosted and act acceptance at the exact head. The firmware campaigns were still queued at this review's
  snapshot.

R898-2 FINISHED
