[R371] POSITIVE - exact head 9c18068512dec844d24fdff7fe0a3eb0d63c14f5

External independent review, round R371-3, of issue #75 phase 2 / PR #604.

- Head `9c18068512dec844d24fdff7fe0a3eb0d63c14f5`, tree `52012dcea83c4cd6a8b419eeeeffce89962ca526`, parent `5c7577e51702b00683a121f97a9806c167eb072b`, source base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
- The round-3 delta (`5c7577e5..9c180685`, one commit by [A391]) changes two files: `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md` (+118/-11) and `docs/findings/README.md` (one row). There are no RTL, firmware, tooling or gitlink changes.
- The round-3 addendum is `review-evidence/75-r1/author-r3/` at evidence-branch tip `a07c7345177e1836c1e138c69ef91ea77cd52a91`.

All four round-3 assignment items are met, and so are my round-2 finding F5 and suggestion S5, which the assignment took.

- My own probes run on the public records:
  - `hold_declaration_probe.py`: 89 checks, 0 failing.
  - `stop_probe.py`, the round-2 probe run on the round-3 ledger: 44 checks, 0 failing.
- Planted faults make both probes fail.
- The author's controls also fail on planted regressions of the replay.
- The assigned gates return rc 0 in three contexts: with submodules, without submodules, and without Git metadata.

I have no open BLOCKER, MAJOR or MINOR finding. Every lens is clean at this head. The five suggestions below are optional. #75 stays open.

## Reconstruction (public state only)

- **Order read:**
  - AGENTS.md and CONTRIBUTING.md.
  - docs/README.md.
  - Issue #75: body, acceptance criteria and "How we prove it" line.
  - The recorded decisions on #75: phase-2 assignment 5859652809, round-2 decision 5860261220 (including the accepted class of clock and entity identifiers), round-3 assignment 5860554971, [A391] TAKEN 5860563147 and REVIEW READY 5860674129, and review start 5860694999.
  - Issues #606 and #608.
  - PR #604 metadata: open, not draft, base `dev`, head `9c180685`, no closing reference.
  - `git diff 8bc97021..9c180685` and `git diff 5c7577e5..9c180685`, and the three commit messages (one line each, no trailers, no closing keyword).
  - The page at head (1287 lines) and `docs/findings/README.md`.
  - The round-3 addendum, which has 99 files. Its `MANIFEST.sha256` verifies 97/97 entries. The only unlisted file is the empty-list stub `OMITTED.txt`.
  - The round-1 packet `author/` and the round-2 addendum `author-r2/`.
- **Baseline:** my own round-2 report, R371-2 (PR comment 5860551143).
- **Probe continuity:** `stop_probe.py` is my round-2 probe with one added option that selects the addendum ledger. `hold_declaration_probe.py` is new in this round. The round-2 packet contained no probe by that name.
- **Other reviews:** I read the other reviewer's round-2 report (PR comment 5860541544) only after my independent pass and draft verdict were complete, and used it only for the resolution table. I have not read the in-flight R370-3.

## Focus-item verification

### 1. Talker cycle 1 and the declaration census (R370-2-F1, assignment item 1): RESOLVED

**Exception stated accurately.** Page lines 229-241 say what the public record `author/talker-001/msrp.tsv` shows (`receipts/hold_declaration_probe.txt`, section C):

- After the disconnect response, the DUT sends Talker Advertise `Lv` at +0.120687323 s, then only `Mt` at +0.520682079 s and +1.720684762 s.
- The DUT makes no declaration from the disconnect response to the reconnect response.
- Its first declaration comes 0.111313165 s after the response. Bridge Listener Ready follows 0.006299407 s later, and CRF another 0.000123512 s later.
- Those three intervals sum to the 0.117736084 s latency. That latency equals the ledger value and is the talker restart maximum.

**Census re-derived from declaration events only.** I counted `New`, `JoinIn` and `JoinMt` as declarations, in the window [disconnect response, connect command). The result is 99/100 holds carrying a DUT Talker Advertise declaration, with cycle 1 the only exception. The page (line 220), `declarations-summary.json` and the PR body state the same.

- **All 100 holds:** the census windows equal the round-2 stop ledger's anchors. Every event in `hold-events.csv` lies inside its window. My predicate agrees with the `is_declaration` column, and the per-hold declaration, Lv and Mt counts I re-derive equal `hold-declarations.csv`.
- **Event kinds:** the only kinds present are JoinMt, Lv and Mt. Mt appears in cycles 1 and 61 only, and Lv only in cycle 1.
- **The eight public talker cycles** (1-5, 13, 24 and 75): the hold events I decode from each `msrp.tsv` equal `hold-events.csv` exactly.
- **What rests on the author's replay:** for the other 92 cycles, the census rests on the author's raw replay. See the real limits below.

**Inference qualified.** The two sentences that made the withdrawn universal claim are gone:

- "Numbered reconnects instead retain DUT Talker Advertise through the hold."
- "The initial bind therefore differs in DUT-side state too."

Lines 243-251 now read "That shared absence alone cannot explain the initial-bind delay", "The other 99 holds carry declarations; causal attribution remains open", and "[#606] must consider cycle 1 when investigating the first-bind path". The PR body repeats the pointer. Issue #606 itself is untouched (see Pending manager duties).

**Backing check derives its count from the data.** `declarations.py` computes `holds_with_dut_declaration` and `holds_without_dut_declaration` from the `DECLARATIONS = {'New', 'JoinIn', 'JoinMt'}` predicate. No count is a literal. `check_controls.py` shows that the old universal claim is rejected on the recorded census: `require_all_holds_declared` raises for cycle 1.

**Mutation controls on my probe** (`receipts/mutations.txt`). Each planted fault fails the probe:

| Planted fault | Failing checks |
|---|---|
| Cycle 1 given a declaration in the census | 5 |
| Cycle 50's declarations removed | 3 |
| Public cycle-1 record given a declaration | 3 |

### 2. The talker non-stops, cycles 13, 24 and 75 (R371-2-F5 and R370-2-S1, assignment item 2): RESOLVED

**The published records are the originals.** `receipts/hold_declaration_probe.txt`, section A:

- Each of the three directories' `MANIFEST.sha256` covers exactly its 16 files and verifies.
- Every file matches `published-records.csv`. In that ledger only `raw-artifacts.json` is transformed.
- `result.json`, `analysis.json`, both snapshots and `cycle.jsonl` equal the hashes in the round-2 `input-hashes.csv`, which was published before round 3.
- The relative `raw-artifacts.json` entry agrees with the round-1 `RAW-ARTIFACTS.json` and with the round-2 ledger's sha256 and size.
- The DUT STREAM_START/STREAM_STOP counters are unchanged in the published before and after snapshots.

**Chronology stated.** The page's two tables (lines 624-646) match the bridge Listener events I decode from the three published `msrp.tsv` files, row for row. They also match `listener-events.csv`.

| Cycle | Bridge Listener `Lv` after disconnect response | First re-declaration (`New`) after reconnect response |
|---|---|---|
| 13 | +0.009770679 s | +0.073776413 s |
| 24 | +0.010356881 s | +0.018704540 s |
| 75 | +0.025307595 s | +0.018687732 s |

- Each cycle has exactly one bridge Listener `Lv`, and all bridge Listener events carry value 2.
- No bridge Listener declaration occurs between the `Lv` and the reconnect response.
- No ACMP DISCONNECT_TX_COMMAND (message type 2) crosses the tap.
- The ledger shows 1000 hold PDUs and a maximum gap of 0.002000053 s for each cycle.
- Every Listener event is bracketed by CRF PDUs at most 0.002000037 s apart.
- The PDU counts from `Lv` to re-declaration (1036, 1009, 1001) fit the 2 ms cadence over the stated spans.
- The cycle-75 withdrawal at 25.3 ms falls outside the 9.5-11.0 ms range I had inferred in F5. The addendum handoff says so explicitly, and the page states the measured value.

**Attribution given with its reason.** The page supports "DUT-side non-stop behavior at the tapped boundary" (lines 648-661):

- the withdrawal crossed the DUT's segment;
- no Listener re-declaration and no DISCONNECT_TX followed before reconnect success;
- CRF continued;
- STREAM_START/STOP stayed at zero.

It also states the limit: the record "does not prove the DUT internally accepted that withdrawal". This is the attribution the tapped data supports, and it does not over-claim.

**Owner linked.** #608 is open and names cycles 13, 24 and 75. The page links it in the Stop checks section (line 615), the acceptance row for at least 100 physical restarts (line 962), and the findings index row (`docs/findings/README.md:11`). Acceptance row 1 (line 959) links it as well. #75 keeps the three missing demonstrated restarts.

**Mutation control.** Planting a bridge Listener JoinIn inside cycle 24's hold fails 6 checks.

### 3. Replay fail-closed and derived outcome (R371-2-S5 and R370-2-S2, items 3-4): RESOLVED

**No assert-based checks** (`receipts/replay_checks.txt`):

- The syntax trees of `recompute.py`, `declarations.py`, `check_controls.py`, `publish_records.py` and `check_packet.py` contain no `assert` statement and no `except AssertionError`.
- `classify_stop` is two plain `if` statements and a return.

**Refusal under optimisation.** The `sys.flags.optimize` refusal is the first statement after the imports, so it runs before any input is read.

- `-O`, `-OO` and `PYTHONOPTIMIZE=1` each give rc 1 and "REFUSED", even with nonexistent inputs.
- `declarations.py` and `check_controls.py` inherit the refusal through the import.
- In the unoptimised control, the same missing inputs give a file error, not a refusal.

**Derived outcome.** `outcome_lines` applied to the 200 published ledger rows reproduces `replay-receipt.json` exactly. With talker 24 removed and listener 1 failed, it prints "196 PASS; 3 FAIL ... listener-001, talker-013, talker-075". `classify_stop` agrees with the ledger's classification and stop-check columns on all 200 rows. At the boundary, a first post-settle PDU exactly at the response counts as RESTART and one nanosecond earlier as NOT_RESTART.

**Numbers unchanged.** The round-3 `stop-checks.csv`, `recomputed-summary.json`, `input-hashes.csv`, `stop-table.md` and `capture-size-table.md` are byte-identical to round 2. My `stop_probe.py` reproduces everything on the round-3 ledger (`receipts/stop_probe.txt`):

- 197 restarts; non-restarts talker 13, 24 and 75.
- Quantiles, slope intervals and blocks.
- The +97/+97 and +100/+100 counter reconciliation.

Its three mutation controls still fail with 9, 3 and 6 checks. Its old section-8 INFO line reporting "page text mentions Listener leave ... False" used a round-2 phrase match. Section D of the new probe supersedes it.

**Author controls.** `check_controls.py`, rerun on a disposable copy, passes 14/14 and regenerates a byte-identical `controls.json`. Planted regressions in the copied `recompute.py` each make it fail (`receipts/control_mutations.txt`):

- the refusal removed;
- one settled PDU tolerated;
- early resumption tolerated;
- an assert-based classifier reintroduced.

### 4. Public hygiene of the round-3 addendum, page and PR body: CLEAN

Source: `receipts/hygiene_scan.txt`.

**Nothing forbidden found.** Across all 99 addendum files, the page, the index and the live PR body, there is none of the following:

- an absolute or temporary path;
- the site-local command-wrapper name or the lane-root variable;
- a host, instrument, vendor, tool or model name;
- a colon-form MAC address or a serial.

**Identifiers stay in the accepted class.** Every 48- or 64-bit hex string in the three new cycle directories is either already present in the round-1 public talker records, or is not an identifier: float digits in `analysis.json` and `integrity.json`, and the monotonically increasing `TAI_NS` console values. The same holds for `recomputed-summary.json`. The newly published records carry the same stream identifiers as cycles 1-5, the class the round-2 decision accepted.

**Paths removed.** `capture.txt` carries the `<capture-interface>` placeholder, and `raw-artifacts.json` now holds a relative identifier.

**Positive control.** The unchanged round-1 `author/tools` still trips the wrapper-name, lane-variable and path patterns. Path values are withheld from the receipt.

**Prior packets untouched.** The live PR body equals `author-r3/PR-BODY.md` apart from a trailing newline. The `author/` and `author-r2/` tree ids are identical before and after the round-3 archive commit, and that commit changes nothing outside `author-r3/` except the packet-level `MANIFEST.json` (`receipts/evidence_packet.txt`).

### Gates and links

**Gates.** The nine assigned gates, plus `check_doc_style.py --selftest` and both `git diff --check` forms, return rc 0 in the review clone with populated submodules (`receipts/gates_with_submodules.txt`). They also return rc 0 in a fresh exact-head clone without submodules (`receipts/gates_without_submodules.txt`). `docs_check.py` and `check_feature_status.py` return rc 0 in a Git-less export (`receipts/gates_without_git.txt`).

- The environment was disposable, with the hash-locked renderer from `tools/markdown/requirements.txt` plus pyyaml, installed unpinned as the hosted docs workflow does.
- A first run before pyyaml was installed gave the bare-metal gate's "pyyaml is unavailable" refusal, rc 2. That was environmental; the rerun with pyyaml is rc 0.

**Links.** The round-3 delta adds only GitHub issue links (#606, #608, #75) and the index row's page link, and none points into a submodule. Planting a broken relative link in the no-submodule clone makes `docs_check.py` return rc 1 "broken link" (`receipts/link_audit.txt`).

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### Suggestions (optional; they do not affect coverage)

- **S7 - Tests - `author-r3/declarations.py` (`if cycle == 1:` block) and `author-r3/check_controls.py` ("remaining declared holds pass the same predicate").**
  - The cycle-1 chronology in `declarations-summary.json` is keyed to the literal cycle 1, not to the derived `holds_without_dut_declaration` set, and nothing checks that the two agree.
  - The control `require_all_holds_declared([r for r in holds if r['declaration_count']])` filters to declared holds and then asserts they are declared, so it cannot fail for any data.
  - The census itself is data-derived, and the page does not rely on that control. Keying the chronology to the derived exceptions, and dropping or replacing the vacuous control, would make both carry weight.
- **S8 - Tests - `author-r3/recompute.py:259`; `author-r3/render_tables.py`; `author-r3/run_gates.py`.**
  - The capture-size table's explanation column still pins `r['cycle'] == 13` ("Continuous hold; shorter tail").
  - `render_tables.py` (6 statements) and `run_gates.py` (8 statements) still use `assert`, so under `-O` they would report success unchecked. They back the page's "every table renders" and gate-table claims.
  - S5 was scoped to the replay, and this does not affect any number. Extending the same refusal to these two tools is optional.
- **S9 - Docs - page line 1273, "Consistency checks also use explicit conditions, preserving every original check."**
  - Two round-2 checks were dropped: the pinned rejected-cycle equality, which item 4 asked to remove, and the redundant re-assertion on RESTART rows, which classification now covers.
  - The handoff discloses the first. Replacing "preserving every original check" with "every original check except the pinned rejection list" would be exact.
- **S10 - Robustness, Docs - page lines 611-671; for #608.** Two recorded facts would help #608.
  - No bridge LeaveAll crossed the tap between the disconnect and reconnect responses in any of the three non-stop holds. In public restart cycles 1-4 one did; in cycle 5 none did. So a lost or ignored single `Lv` had no MRP recovery event before reconnect.
  - The first Listener re-declaration comes at least 2.0024 s after the withdrawal (cycle 75; 2.0173 s and 2.0734 s in cycles 24 and 13). That rules out the "race with a quick re-declaration" hypothesis in #608's to-do item 2 for these three cycles.
  - Source: `receipts/hold_declaration_probe.txt`, section D, INFO lines.
- **S6 (retained from R371-2, still optional) - Docs - page line 215.** "It then repeats every second while Ready remains absent" simplifies the recorded spacing of the DUT's Talker Advertise declarations: 0.2 s, then 1.0 s six times, then 0.2 s after the bridge LeaveAll.

## Prior public review findings on PR #604: resolved or retained at this head

| Finding | Status at `9c180685` | Evidence |
|---|---|---|
| R371-2 F5 MINOR (non-stops unattributed, no owner) | RESOLVED | Focus 2; #608 open and linked at page:615, 959, 962 and README:11; records published and verified; `receipts/hold_declaration_probe.txt` sections A and D |
| R371-2 S5 (assert-based classification) | TAKEN | Focus 3; `receipts/replay_checks.txt`, `receipts/control_mutations.txt` |
| R371-2 S6 (initial-bind cadence wording) | Not taken; optional | Retained above as S6 |
| R370-2-F1 MINOR (cycle 1 contradicts "retain Talker Advertise"; the check could not fail) | RESOLVED | Focus 1. The page states the exception; the census is re-derived from declaration events (99/100, cycle 1); the inference is qualified; #606 is pointed at cycle 1 by the page and PR body; `check_controls.py` rejects the old claim on the recorded census |
| R370-2-S1 (characterise non-stops against the Listener withdrawal) | TAKEN | Focus 2 |
| R370-2-S2 (derive the printed outcome) | TAKEN | Focus 3 |
| R371-1 F1-F4 and R370-1 F1-F3 | RESOLVED at `5c7577e5` (R371-2, R370-2); unchanged by this delta | Round-3 diff touches none of the resolving text except to add #608 links and the qualified census |
| R371-1 S1-S3, R370-1 S1-S4 | Taken at `5c7577e5`; unchanged | none |
| R371-1 S4 (restart decomposition) | Not taken; optional | none |

## Clean-lens evidence

[R371] PASS Conformance - page lines 211-254, 588-671 and 955-965; `docs/findings/README.md:11`; `author/talker-001/msrp.tsv`, `author/talker-setup/msrp.tsv`, `author-r3/talker-0{13,24,75}/{msrp.tsv,result.json,analysis.json,snapshot-*.jsonl}`; `author-r3/{hold-declarations.csv,hold-events.csv,listener-events.csv,declarations-summary.json}`; #75 criteria and decisions 5860261220 and 5860554971; #606; #608 - The census uses the 802.1Q declaration events (New/JoinIn/JoinMt; In, Mt, Lv and LeaveAll excluded). The MSRP three-packed and four-packed decoding in `declarations.py` matches the attribute types, FirstValue widths and event order. Every cycle-1 and non-stop figure is re-derived from public records. The attribution is scoped to the tapped boundary. Acceptance rows keep talker 97/100 NOT MET and link #606 and #608. #75 stays open with "Refs #75".

[R371] PASS RTL - `git diff --name-only 8bc97021..9c180685` (two Markdown files); gitlinks identical at base and head (`external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor 870ff88a`, `third_party/verilog-axis 48ff7a7e`; `receipts/clone_integrity.txt`); page lines 50-66 unchanged by the round-3 delta - No RTL, firmware, constraint, interface or gitlink change. The page's architecture statements, verified in R371-2 against the pinned SRP document and the retired context module, are untouched. #608 records a possible DUT talker stop-path behaviour for a future lane. This PR neither changes nor mis-describes RTL, and the page explicitly leaves the responsible state or timer undetermined.

[R371] PASS Robustness - page lines 588-671 against `author-r3/talker-0{13,24,75}` records, `listener-events.csv` and `author-r2/stop-checks.csv`; `author-r3/recompute.py` refusal and classification paths; `receipts/hold_declaration_probe.txt` (sections A and D), `receipts/replay_checks.txt` (optimisation modes, missing inputs, boundaries) - Non-stop continuity is bracketed at every Listener event, and counters are zero. Withdrawal/re-declaration ordering is established per cycle. The replay fails closed under all three optimisation modes before reading inputs, and classification boundaries are exact. The census window's start is inclusive and its end exclusive, and the tool checks this.

[R371] PASS Tests - `receipts/gates_with_submodules.txt`, `receipts/gates_without_submodules.txt`, `receipts/gates_without_git.txt` (all rc 0); `receipts/link_audit.txt` (negative control rc 1); `author-r3/check_controls.py` rerun (14/14, byte-identical `controls.json`) and its planted regressions (`receipts/control_mutations.txt`, 4/4 fail); my probes (`receipts/hold_declaration_probe.txt` 89/89, `receipts/stop_probe.txt` 44/44) and their 7 mutations (`receipts/mutations.txt`, 7/7 fail) - The round-3 controls can fail for the defects they claim to detect. The backing census check rejects the old claim on real data. S7 and S8 are optional strengthening.

[R371] PASS Docs - the whole round-3 delta and the page at head (1287 lines, tables checked against the records); `docs/findings/README.md:11`; live PR #604 body; `author-r3/README.md`, `HANDOFF.md`, `REVIEW-READY.md` and `MANIFEST.sha256` (97/97); `receipts/hygiene_scan.txt`; `receipts/evidence_packet.txt` - The changed statements are accurate and linked to their owners. The withdrawn claim is removed. The artifact hash table (page lines 1216-1228) matches the addendum bytes and sha256. The round-1 and round-2 packets are unchanged. The hygiene scan is clean. S9 and S6 are wording suggestions only.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page 211-254, 588-671, 955-965; README:11; public talker-001/setup and published 13/24/75 records; round-3 census tables; #75 decisions; #606; #608 | R371-3 | `9c18068512dec844d24fdff7fe0a3eb0d63c14f5` |
| RTL | CLEAN | diff name list (docs only); gitlinks at base and head; page 50-66 unchanged | R371-3 | `9c18068512dec844d24fdff7fe0a3eb0d63c14f5` |
| Robustness | CLEAN | non-stop bracketing and counters; withdrawal/re-declaration ordering; replay refusal, missing-input and boundary behaviour; census window bounds | R371-3 | `9c18068512dec844d24fdff7fe0a3eb0d63c14f5` |
| Tests | CLEAN | gates in three contexts; link negative control; author controls and 4 planted regressions; own probes and 7 mutations | R371-3 | `9c18068512dec844d24fdff7fe0a3eb0d63c14f5` |
| Docs | CLEAN | whole delta and page; index row; PR body; addendum README/HANDOFF/REVIEW-READY/manifest; hygiene scan; prior-packet immutability | R371-3 | `9c18068512dec844d24fdff7fe0a3eb0d63c14f5` |

The ledger's head is the merge candidate's source head. If any later commit touches the page, the index or the evidence it cites, the lenses in that scope are un-covered and must be covered again.

## Real limits

- **Private raw data.** Raw captures and the per-cycle records outside talker 1-5, 13, 24, 75 and setup are private.
  - For the other 92 talker holds, the census is checked for internal consistency: windows against the ledger, events against counts, and the predicate against the column. It is not re-decoded from raw frames. It rests on the author's raw replay, which reports a match for all 100 TSVs and the setup.
  - The claims that the PDU counts from `Lv` to re-declaration are exact, and that the 0.002000053 s maximum gap also covers reconnect response to first re-declaration, likewise rest on private captures. I checked them only for plausibility against the 2 ms cadence.
- **Internal behaviour.** The tapped record cannot show whether the DUT received or processed the withdrawal. The page says so.
- **Hardware.** There was no bench access. Physical calibration was NOT RUN. Hosted skipped contexts and field skips are not hardware proof.
- **Banks not run.** The scoped Verilator was not used, because the delta has no RTL. No parent, protocol-processor, gPTP, Yosys or builder bank was run.
- **Hosted checks at this head.** The read-only snapshot (`receipts/hosted_check_runs.txt`, 2026-09-27T23:18Z) shows:
  - 13 success, including `rtl-fast`, `docs-check-no-git`, `verilator-lint`, `yosys-elaboration`, all four Yosys shards and Verilator shard 3;
  - 1 skipped: the physical gPTP context;
  - 6 in progress: `docs-check`, `elaborate`, and Verilator shards 0, 1, 2 and 4.
  - I do not treat this as acceptance.
- **Environment.** pyyaml in the disposable gate environment is unpinned, matching the hosted docs workflow.

## Pending manager duties

- **Hosted and act acceptance at the exact head.** This includes completion of `docs-check`, `elaborate` and the remaining Verilator shards.
- **Candidate-merge validation** against live dev `20aa4eab` at the merge turn. Source base `8bc97021` is distinct from it.
- **#606 body.** It still says reconnects "stayed under 0.12 s in 100/100 cycles" and "the DUT kept its Talker Advertise through the hold". Both are now contradicted: the page shows 97 demonstrated talker restarts, and cycle 1 is the exception. The executor made no comment on #606, as its handoff states. Pointing #606 at cycle 1 there, and correcting its body, is for the issue owner.
- **#608 body.** It infers from matching MSRP profiles that the bridge `Lv` reached the segment in the non-stop cycles, and quotes a 9.5-11.0 ms `Lv` range seen in public restart cycles. The measured non-stop values (+9.8 ms, +10.4 ms and +25.3 ms) are now published and may replace that inference. S10's two facts may also be worth recording there.
- **PR body.** Its last line, "No push, PR edit, or hardware action performed.", describes the executor's own actions and may read oddly on the published body. It is cosmetic.
- **Round-1 packet tools.** `author/tools` still carries the wrapper name, the lane-root variable and temporary paths. The round-2 decision left that packet as is, and round 3 did not touch it.
- **#75 stays open.** AAF is unmeasured, and the talker 100-restart line is NOT MET.

## Clone state

- No tracked file was modified. Gates ran with bytecode writing disabled.
- HEAD is `9c180685`, and `git write-tree` equals tree `52012dce`.
- `ls-files -s` equals `ls-tree` for all 945 entries (mode, blob, path).
- There are zero porcelain entries, including ignored and untracked files.
- The four gitlinks are unchanged, with `external` uninitialised, and the three initialised submodule worktrees are clean (`receipts/clone_integrity.txt`).
- Probe copies, the disposable gate environment, the no-submodule clone, the Git-less export and the fetched evidence branch are all under the packet's unpublished scratch directory.

R371-3 FINISHED
