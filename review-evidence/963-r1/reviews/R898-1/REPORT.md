[R898] NEGATIVE - exact head 4cca956932073b3f704f12f81c53f2934cfa215c

# [R898] Round R898-1: internal cleared-context review of PR #984 (issue #963)

- **Head under review:** `4cca956932073b3f704f12f81c53f2934cfa215c`, tree `2f4e963dcaf2e5739003fbd3059610fe2f2ee9b0`.
- **Source base:** `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`, the flip's reviewed head, merged as `854bd723`.
- **Delta:** 10 commits, 5 files: `aecp_maps.c`, `test_aecp.cpp`, `aecp_map_mutants.py`, `aecp_output_mutants.py` and `docs/design/SPLIT_CONTROL_MEMORY.md`. No RTL, no `tb/` file, no gitlink, no workflow.
- **Verdict:** NEGATIVE.
  - One MINOR is open: F1, the PR's and the REVIEW READY's firmware-gate plant tally. It names shard 0's 88 suite arms as caught plants, so the 1,846 total is not a plant count.
  - Everything else this round checked holds at this head, most of it reproduced by this round rather than read from receipts.
  - F1 is a correction to the published evidence text only. No code, test or measurement changes.
- **Prior public review findings on this PR:** none. At review time the PR carries only the two review-start comments and no review. Nothing is to be resolved or retained.

## 1. What this round executed at the exact head (and the base)

Every command below was run by this round, in disposable copies of the exact head (and of the base for the base arms) under the packet's `scratch/`.
- **Tools.** Pinned Verilator 5.050 (identity printed: `Verilator 5.050 2026-07-01 rev v5.050`). The pinned RV32 SDK was verified by `scripts/ci_rv32_sdk.py --verify-only`: archive sha256 `d42680e9...`, the CI pin. The product LiteX tree.
- **CPU budget.** Every campaign was pinned to 16 CPUs.
- **Receipts.** Each one is in `receipts/<name>/` with `argv.txt`, `head.txt`, `rc`, `start.txt`, `end.txt` and `log.txt`.

| Campaign | Tree | Result | Receipt |
|---|---|---|---|
| Harness `aecp-largest-notice`, 8x8-1if, answering-ports, strict (no `--record-share-findings`) | head | rc 0; 0 of 106 work passes over THE SHARE; longest 149,307 | `h-head-8x8-ap/` |
| same | base | rc 1; `SHARE ... 2 of 108 ... the longest 222,104`; ADD's taking pass 215,566 | `h-base-8x8-ap/` |
| Harness, 8x8-1if, declaring-outputs, strict | head | rc 0; 0 of 106; longest 153,071 | `h-head-8x8-do/` |
| same | base | rc 1; 2 of 108; longest 227,112; ADD's 220,503 | `h-base-8x8-do/` |
| Harness, 1x1, answering-ports, strict | head / base | rc 0 / rc 0; 0 of 107 both; longest 136,285 / 145,380 | `h-head-1x1-ap/`, `h-base-1x1-ap/` |
| Differential of the group's log and probe verdicts, base vs head, 3 point-arm pairs | both | identical: every WIRE frame (59, in order, byte for byte), TXC, RXS/RXE/RXC, MARK, PARTICIPANT, RESULT, probe status and verdicts | `differential/*.txt` |
| Image comparison, base vs head, the three harness images built above | both | no section or symbol moved; `aecp_map_command` 2,204 B (8x8) / 2,208 B (1x1) in both; every differing byte (1,062 / 1,060) inside it; stack frame 2,544 B in both | `images/*.txt` |
| Head tests on the base's `aecp_maps.c` (planted fix removal) | head tests, base firmware | rc 1: exactly `Core.MapEditsAreTheirDefinitionRowForRow` (reads 3, want 1) and `Core.MapEditWorkObservesEachOutputStreamOnce` (observed `{0,1,0,0,1,...}`, want `{0,1}`) fail, in the app and work arms; 2 failures of 178 checks; every other arm passes | `probe-head-tests-base-maps/` |
| Firmware gate shard 0/4 (`--require-rv32 --self-test --jobs 4`) | head | PASS; 88 arms ok; `named plants not caught: none` | `fw-shard0/` |
| Firmware gate shard 1/4 | head | PASS; `mutants: 826 of 826 caught` | `fw-shard1/` |
| Firmware gate shard 2/4 (AECP's campaign) | head | PASS; 389 of 389 plants `[ok]`, 0 ESCAPED; the four `map-stream-*` plants and the re-anchored rows caught on their words | `fw-shard2/` |
| Firmware gate shard 3/4 | head | PASS; 543 `[ok]` (SRP plants and the two pin controls), 0 ESCAPED | `fw-shard3/` |
| Coverage ratchet (`fw_coverage.py --selftest`, `--check --jobs 4`) | head | rc 0; self-test 29 of 29; `firmware coverage: PASS (40 files)`; `aecp_maps.c` 352/352 lines, 423/424 branches | `fw-coverage/` |
| Harness portable self-test (`run.py --self-test`) | head | rc 0; `self-test: 0 failures` (a first attempt in the foreground was stopped by this round's own 590 s timeout, rc 124, kept as `harness-selftest-cut-by-timeout/`; it is not a failure) | `harness-selftest/` |
| Reviewer-owned plants through `aecp_mutants.campaign` (`scripts/extra_plants.py`) | head | 2 of 3 caught on their words; 1 escaped (see S1) | `probe-extra-plants/`; a first run with a malformed plant of this round's own (it did not compile) is kept in `probe-extra-plants-run1/` |
| Docs gates: `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `check_em_dash.py --base dd163e41` (pinned renderer) | head | rc 0 each; em dash: 0 findings over 1 added line | `docs/` |
| Hosted check-runs at the exact head (read only) | head | snapshot: 8 success, 1 skipped (physical gPTP: skipped, not executed), the rest queued or in progress, none failed | `hosted-checks-snapshot.tsv` |

The probe and differential scripts are portable and in `scripts/`:
- `launch.sh` and `harness.sh`: the campaign wrappers.
- `log_diff.py`: the differential.
- `image_compare.py`: the image comparison.
- `extra_plants.py`: this round's own plants.

**The differential's treatment of the testbench's own lines** (stated, not masked):
- **EVW lines** are the testbench's stimulus writes into the event ring (`sim_main.cpp:132`): TICK records every 10 ms. They are compared up to the earlier of the two runs' ends.
  - The base runs about 0.12 M cycles longer, because the head finishes its script sooner. So the base's raw count has one more TICK (328 vs 324).
  - The first 324 are identical.
- **The ENTRY trace's `completion_source`** is the declaring-outputs arm's per-pass bridge entry. It counts loop passes (base 40,374, head 40,428) and is reported apart.
  - Its in-record completions, the findings the arm grades, are graded by the harness itself and pass.
  - Every other ENTRY line is identical in order.
- Neither is device output. Every wire frame is identical.

## 2. Lens results

### Conformance

**Acceptance (issue #963, frozen):**
- **Every work pass of the group at 8x8/1if within THE SHARE, at both arms:** met, reproduced.
  - Head: rc 0 and 0 of 106 in both arms.
  - Base: rc 1, rc 1 and 2 of 108.
  - The figures are the author's exactly: 149,307, 153,071, 222,104, 215,566, 227,112 and 220,503.
- **The graded rows unchanged:** met for this group at the three pairs run.
  - Probe status and every verdict are identical.
  - Each probe's `budget_ms` and `ceiling_ms` are unchanged.
  - The 481-group claim is the author's receipt (`harness-final/strict-diff.txt`). This round did not rerun all 481 groups.
- **The cause named:** met.
  - The per-module cycles of the taking pass (`differential/pass-modules-all.txt`) show where the cut lands. At 8x8 answering-ports REMOVE, base against head:
    - `aecp_commands` (`observe`, `aecp_stream_read`): 32,220 against 9,838;
    - `ctrl_mem` (the zeroing): 32,093 against 6,661;
    - `ctrl_app_aecp` (the port callback): 12,924, then gone from the top six.
  - That is the 63 observations, each zeroed twice. At 1x1, an input map, only the zeroing goes: `ctrl_mem` 18,887 against 10,319.
  - It matches the author's committed-PC trace (`cause/`).
- **A cut, not a restatement:** met. `ctrl_loop.h` (THE SHARE), the stated costs and every row limit are outside the diff.
- **Images within their ledgers:** met for the three harness images, which are byte-identical outside `aecp_map_command` and of the same size.
  - The target platform's image (139,208 B, 58.0 RAMB36) is the author's receipt only. It follows from the same sources at the same function size, but this round did not rebuild it.

**The disclosed behaviour change, against its clauses:**
- **The clauses.** Milan v1.2 5.4.2.27 (ADD) and 5.4.2.28 (REMOVE) cite ATDECC 7.4.45 and 7.4.46.
  - The manager's brief names 7.4.44/7.4.45. In 1722.1-2021, 7.4.44 is GET_AUDIO_MAP. That path (`cmd == 43u`, `aecp_maps.c:441-462`) returns before the edit and is untouched.
  - This round judged against 7.4.45/7.4.46, read in the standards themselves (Milan v1.2 5.4.2.26-28: "as specified in [ATDECC, Clause 7.4.44]", "7.4.45", "7.4.46"; the excerpts are not republished).
  - Milan: without TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING, a mapping that references a channel of "a currently streaming Stream Output" is invalid, BAD_ARGUMENTS, nothing added or removed.
  - 1722.1-2021 7.4.45.1 and 7.4.46.1: validity "at a particular point in time is governed by a set of vendor defined rules".
- **One observation suffices.** The condition is a property of the Stream Output, so one observation of each Stream Output per command decides it for all of its mappings. The head's form is an evaluation of the command at one point, consistent with the matrix's "atomic validation" (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:134`).
- **Can any controller-visible response differ?** Only if a stream's observation changes inside one record. The two inputs to it:
  - **`running`.** It is LICENCE.ACTIVE read from the mailbox (`aecp_face.c` `stream`, `mbx.c:304`). Its only writer is this CPU's SRP owner (`srp_mbx.c:182,664` through `mbx_pub_licence`, `mbx.c:214`), which runs in the same cooperative loop. The interrupt enables are wake-up causes for the wait (`ctrl_loop.c:115`, `mbx_plat_mmio.c`), and no handler runs SRP. So `running` cannot change inside an AECP record, and the source comment's "which nothing else runs beside" holds.
  - **The face's word-0 gather read.** A window that answers a stream's first read and fails a later one in the same record is the one case the PR discloses. There the base refused at the later mapping and the head keeps the first answer. Both are a refusal-or-acceptance of the whole command evaluated at one instant, and neither breaks the clauses.
  - The differential found no response or notice byte changed in any arm run.
- **Status ordering is unchanged:** `ILLEGAL`, then the running check, then `BARRED`, then EARLIER or FOUND, at each mapping in command order (`aecp_maps.c:532-537`).

`[R898] PASS Conformance - sw/firmware/ctrl/aecp/aecp_maps.c:258-289,476-539; receipts/h-*-8x8-*/table.md; receipts/differential/; Milan v1.2 5.4.2.27-28 and IEEE 1722.1-2021 7.4.45-46 - acceptance reproduced at 8x8/1if (both arms) and 1x1, the observation once a stream judged against Milan v1.2 5.4.2.27-28 and IEEE 1722.1-2021 7.4.45-46 and 9.2.2.6 (524 octets, 63 mappings), every response and notice byte the base's`

### RTL (firmware architecture, widths and contracts; no RTL file is in the diff)

- **Indexing.** `observed[r->stream / 32u % MAP_IDLE_WORDS]` is reached only by a mapping that passed `legal()` and `place()` (`aecp_maps.c:500`), so `r->stream < MAP_FIRSTS`.
  - At 8x8/1if `MAP_FIRSTS` = 9 (`AECP_ENTITY_KEY_STREAMS 9u` in the built image's `aecp_entity_gen.h`), so `MAP_IDLE_WORDS` is 1 and the reduction is a no-op.
  - `1u << (r->stream % 32u)` is below 32. The arithmetic is unsigned.
- **The table.** `uint32_t observed[MAP_IDLE_WORDS] = {0}` is a zero-initialized local, one per record.
- **The observation.** `info` is uninitialized except `brief`. `aecp_stream_read` reads only `brief` before `memset` (`aecp_commands.c:116-122`), and the failure path short-circuits before `info.running` is read.
- **The stream-port interface contract is unchanged.** It is called with `brief` set and the same type and index, and each port receives the same zeroed struct as before.
- **Hot placement.** `aecp_stream_read` is on the split image's hot list (`ctrl_split_hot.txt:257`, `ctrl_split.ld:251`), which is the reason the `running` form was set aside.
- **Resources.** The image comparison shows `aecp_map_command` at the base's size and its stack frame at 2,544 B in both. No other byte moved in the three images built.
- The mailbox contract, the RTL and the interfaces are untouched.

`[R898] PASS RTL - sw/firmware/ctrl/aecp/aecp_maps.c:173-179,249-289,485,532-537; sw/firmware/ctrl/aecp/aecp_commands.c:99-122; receipts/images/harness-*.txt; built aecp_entity_gen.h - index domain, shift width, initialization, port contract and placement checked; image bytes outside aecp_map_command identical at 8x8/1if (two arms) and 1x1`

### Robustness

Each path below was checked by a test and a plant, or by this round's own plant:

| Path | Evidence |
|---|---|
| A stream found running | `map-stream-running-accepted` |
| An unanswered observation | the `silent` case |
| A stream's first mapping refusing after its bit is set | the refusal ends the edit, so the set bit is never reused |
| Per-edit reset | the last case of the new test; `map-stream-idle-uncleared`; this round's `review-table-kept-across-edits` (a `static` table) caught |
| An input port's edit observing nothing | this round's `review-input-port-observed` caught by `MapEditsAreTheirDefinitionRowForRow`'s reads |
| The largest legal command (63 mappings) | ADD and REMOVE |
| Repeated mappings of one stream | the 63-row edit over two streams |
| Feature- and shape-dependent behaviour | 1x1 (input map) against 8x8/1if (output map), both run |

There is no concurrency inside a record (see Conformance).

`[R898] PASS Robustness - sw/firmware/ctrl/test/test_aecp.cpp:2978-3015; receipts/fw-shard2/log.txt (map-stream-*); receipts/probe-extra-plants/ - running, unanswered, reset, repeated, maximum-length, input and output paths each failing a test when broken`

### Tests

- **The changed and new tests fail on the base firmware, on their own words.** In that probe nothing else fails (`probe-head-tests-base-maps/`).
- **AECP's plants.** The campaign catches all 389 at the head, the four new ones on their named words. The re-anchored rows are caught as follows:
  - `edit-before-the-checks` is now on executable code, `size_t additions = 0;`, unique in the file;
  - `map-idle-reads-whole` is now on `info.brief = true;`;
  - `map-port-rows-unread` and `map-owners-unread` are now caught by the edit's map, and remain caught by their test.
- **Shard 0 at the exact head.** Rerun: PASS, with the same 88 arms and the same caught lines as the author's receipt at `25d3dd7a`. So the partition question is settled by execution.
  - The claim also holds on reading: shard 0 is the `suites` phase (`test_ctrl_firmware.py:169`, `PHASES`; `:241-260`), which runs no plant table.
  - `50d3f10e` changes only `aecp_map_mutants.py` rows, read by the `aecp` phase.
- **Shards 1 and 3** at the exact head: see the table.
- **Coverage ratchet:** PASS.
- **The twin:** not rerun. Its map edits are STREAM_PORT_INPUT 0's only (`tb/verilator/milan_dp/twin_split.cpp:608-674`), where the new check returns before any read. The author's receipt at `50d3f10e`, firmware-identical to this head (`git diff 50d3f10e..4cca9569` is the design doc only), says `twin: 0 finding(s)`.
- **The gap.** One of this round's plants escapes: S1 below, a pre-existing gap and not this lane's.

`[R898] PASS Tests - sw/firmware/ctrl/test/test_aecp.cpp:2867-3015; sw/firmware/ctrl/test/aecp_map_mutants.py:104-138,260-264; sw/firmware/ctrl/test/aecp_output_mutants.py:75-77; receipts/fw-shard{0,1,2,3}/, fw-coverage/, probe-head-tests-base-maps/ - every new test fails on the base for its own defect, every plant caught at the exact head`

Every finding under Tests is F1. Tests is UNCLEAN while F1 is open.

### Docs

- **The design doc's added bullet** (`docs/design/SPLIT_CONTROL_MEMORY.md:2628`):
  - Its pass figures agree with this round's reproduction: 222,104, 215,566, 227,112, 220,503, 149,307 and 153,071.
  - Its record, load and image figures agree with the author's receipts. Its link targets resolve, and `#5-fit` holds the 58.0 ledger at line 139.
  - The docs gates pass.
- **Source comments in the delta** (133 added lines) carry issue and requirement IDs only. No lane label, round, reviewer ID or comment ID appears (`receipts/comment-rule/`: 0 matches). No RESIDUE under the comment rule.
- **The PR and the REVIEW READY:**
  - They state the change, the cause, the disclosure and the not-run sweep.
  - Their firmware-gate tally is F1.
  - One sentence contradicts the disclosure: R1.

Every finding under Docs is F1 (and R1, which does not affect coverage). Docs is UNCLEAN while F1 is open.

## 3. Findings

**F1, MINOR. Lenses: Docs, Tests.**
- **Artifact:** the PR #984 body, Status, "Gates: the firmware gate's four shards (1,846 plants caught, none escaped)". Also #963's REVIEW READY ([issuecomment-7096625846](https://github.com/kebag-logic/milan-fpga/issues/963#issuecomment-7096625846)), "Plants caught 88 (shard 0, at `25d3dd7a`), 826, 389 (AECP's campaign) and 543", and the packet's `author/HANDOFF-r1.md` gate table.
- **Evidence:**
  - Shard 0 is the `suites` phase (`test_ctrl_firmware.py:169,241-250`). It runs the normal suites and no plant table.
  - Its 88 are the 88 `[ok] arm ...` lines, suite arms, in the author's receipt `gates-current/firmware-0/gate.log` and in this round's `receipts/fw-shard0/log.txt`. The shard inventory counts invocations too: `shard sizes [88, 827, 390, 542]`.
  - Shard 0's suites self-check some named plants of their own, not 88 of them. Its log reads `18 planted defects caught`, eight `[caught]` hot-list plants and three `plant ...: caught` mailbox plants.
  - So "1,846 plants caught" adds 88 suite arms to 1,758 plant outcomes (826 + 389 + 543, which this round confirms for shards 2 and 3 at the exact head, and shard 1 as 826 of 826 at the exact head).
- **Impact:** a published test-evidence figure overstates the plant campaign by 88 and labels suite runs as caught defects. A cold reviewer reading the tally cannot tell what the gate proved. It is a figure, so by the owner's rule it is not RESIDUE.
- **Required outcome:** the PR body and the evidence comment state shard 0 as its suites (88 arms, PASS) and the plant total as the three campaigns' count (1,758), or state each shard's own unit.
- **Verification:** the corrected text's numbers match `receipts/fw-shard{0,1,2,3}/log.txt` and the gate's own inventory line.

**R1, RESIDUE. Docs.**
- **Artifact:** the PR #984 body, Description, "The cut", "Its observation": "The port is called exactly as before."
- **Why:** the same PR discloses that the port is now read once a stream an edit maps, not once a mapping. What is unchanged is each call's form (a brief observation of the STREAM_OUTPUT, the same arguments).
- **Exact fix:** replace that sentence with "Each observation calls the port as before: a brief observation of the mapping's STREAM_OUTPUT."

**S1, SUGGESTION. Tests, Robustness.**
- **Artifact:** `sw/firmware/ctrl/test/test_aecp.cpp:2869,2946`.
- **The gap.** The edit definition's only illegal mapping names stream 65535, which no descriptor holds. So `observe()` refuses before the port is reached in either order of the checks.
- **The plant.** This round's plant `review-observed-before-legal` moves the running check before the geometry's refusal (`aecp_maps.c:534`), and it escapes. An illegal mapping of an existing STREAM_OUTPUT, a channel past its format, would then be observed before its refusal:
  - an extra port read;
  - the same status, BAD_ARGUMENTS, at the same mapping.
- **Why it is only a suggestion.** It is pre-existing (the base's test and table have the same gap) and is cost only, not controller-visible.
- **Optional:** add such a mapping to the seeded edits, and add the order plant.

## 4. Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_maps.c:258-289,404-574`; `aecp_commands.c:99-122`; `aecp_face.c` `stream`; `mbx.c:214,304`; `srp_mbx.c:182,664`; Milan v1.2 5.4.2.27-28; IEEE 1722.1-2021 7.4.45-46, 9.2.2.6; harness runs and differential (8x8/1if both arms, 1x1) | R898-1 | `4cca956932073b3f704f12f81c53f2934cfa215c` |
| RTL | CLEAN | `aecp_maps.c:173-289,476-539`; `aecp_commands.c:116-122`; `ctrl_split_hot.txt:257`; built images and `.su` stack files at both points | R898-1 | `4cca956932073b3f704f12f81c53f2934cfa215c` |
| Robustness | CLEAN | `test_aecp.cpp:2978-3015`; shard 2's `map-stream-*`; this round's plants | R898-1 | `4cca956932073b3f704f12f81c53f2934cfa215c` |
| Tests | UNCLEAN (F1) | `test_aecp.cpp`, `aecp_map_mutants.py`, `aecp_output_mutants.py`; the four shards, the coverage ratchet and the harness self-test at the head; the base-firmware probe | R898-1 | `4cca956932073b3f704f12f81c53f2934cfa215c` |
| Docs | UNCLEAN (F1) | `SPLIT_CONTROL_MEMORY.md:2628`; added source comments; PR #984 body; #963 REVIEW READY; docs gates | R898-1 | `4cca956932073b3f704f12f81c53f2934cfa215c` |

F1 touches no code, test, measurement or source document. A correction of the PR body and of the evidence comment alone does not change the head, so it re-covers Tests and Docs at this same head once a reviewer re-reads the corrected text.

## 5. Real limits

- **Not rerun by this round:**
  - the 481-group sweep of every arm at both points and its strict differential;
  - the record-class audit (`record_classes.py`) and the measured load (0.48911, 0.60082);
  - the other 13 harness arm images;
  - the target platform's images (139,208 B at 58.0 RAMB36);
  - the twin;
  - the author's committed-PC trace.
- **What this round did instead.** It reproduced the group in three point-arm pairs, with identical wire bytes and verdicts. It compared three images byte for byte. The rest is judged from the author's receipts, which are consistent with everything this round measured.
- **The record classes.** The receipts show every held class within its statement and none above the base. The one REPORTED class over its statement (1x1/1if declaring-outputs paced: 30,688 cycles, 325 us against 315 us) is the base's too (30,839). The head removes two base REPORTED rows at 8x8/1if.
- **Path latencies.** The probes' path latencies move with pass alignment: the 8x8 ADD path is 330,586 at the base and 334,346 at the head, and `collision_indices` is 167,480 and 226,511. Verdicts and budgets are identical. These are path spans, not the record statements.
- **Toolchains.** The host GoogleTest is 1.18.0, through pkg-config. The author's receipts record it as absent from pkg-config. The gate's results agree.
- **The full native Verilator sweep was not run** (no CPU ranges booked). No RTL or `tb/` file changes. CONTRIBUTING 2.1 step 7 requires the full sweep on the candidate merge tree, so it is owed to the candidate and does not block this source-head verdict.
- **Not inferred:** no manager source bank is claimed or inferred.
- **Not run, and not hardware proof:** physical calibration. The skipped hosted context (physical gPTP) is not hardware proof.

**Receipts are scrubbed.** Host paths in the text receipts are replaced by placeholders (`scripts/scrub.py`): `<packet>`, `<review-clone>`, `<pinned-rv32-sdk>`, `<pinned-verilator>`, `<tools>`, `<home>`. The compressed group logs carry no host path and match their recorded sha256.

**This round's footprint on the review clone.** Fetching the evidence commit `e31126d8` added objects to the review clone. Every tracked byte, mode, index entry and gitlink of the review clone is the exact head's (`receipts/clone-integrity.txt`).

## 6. Pending manager duties

- Carry F1's correction and R1 to the PR body and the evidence comment, and have a reviewer re-read them at this head.
- Build and validate the current-dev merge candidate:
  - source base `dd163e41`, live dev `e275d795`;
  - builder and native banks, the full Verilator sweep and Yosys, per CONTRIBUTING 2.1 step 7;
  - with the composition of #958's answering-ports statements and the train, which is the manager's.
- Accept the hosted exact-head contexts (most still queued at this round's snapshot), and the act replica.
- Post-merge containment.

R898-1 FINISHED
