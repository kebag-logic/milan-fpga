[R510] POSITIVE - exact head afa4e687234b80e9474aa6dd0dc756de16a241bd

# R510-1: internal cleared-context review of PR #676 (issue #667, bench lane B13)

- Reviewer: [R510], internal independent reviewer, round R510-1.
- Exact head: `afa4e687234b80e9474aa6dd0dc756de16a241bd`, tree `2f113aa1eda3744db77e9ea49818ef49309b63de`.
- Source base and live dev at review time: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
- Diff: one commit, a single one-line message with no trailers. It adds one file, `docs/findings/667_TALKER_START_BENCH.md` (503 lines). No RTL, firmware, test, script or submodule gitlink changes. All four gitlinks are byte-identical to the base (`receipts/clone-restore-check.txt`).
- Public evidence: `review-evidence/667-b13-r1` at `b2bb3c89096c8fd4712a39677bae96e5987ccbbd` (1,450 files). All 1,449 MANIFEST.json entries match the published bytes. `author/identity.json` and `author/validation.json` were redacted for publication, and their `original_sha256` differs from `published_sha256` as declared (`receipts/evidence-manifest-check.log`).
- Verdict: POSITIVE. There is no open BLOCKER, MAJOR or MINOR. Two RESIDUE items and five SUGGESTIONs are recorded below.

## 1. Scope reconstructed from public state

The frozen task for this PR is the manager's B13 assignment on issue #667 (comment 6009837251), under the issue body. The executor's TAKEN comment (6009853122) restates it. Items:

1. Identity gate: entity_id, entity name, firmware_version and serial must match. STOP on any difference.
2. Two-hour bidirectional soak. Record the as-found state, apply the binding rule, and bind AAF in both directions, plus CRF. Read GET_COUNTERS on every DUT counter descriptor and the peer's bound inputs every 60 s. Read GET_AVB_INFO and GET_AS_PATH every 5 min. Keep a rolling tap capture. Report start, end and delta for every counter. Any increase in an error-class counter, or a grandmaster or asCapable change, is a finding.
3. 100 two-second DUT-talker binds into the peer's input. Count EARLY and LATE per bind. Record the first 10 PDUs (sequence, tv, avtp_timestamp against the steady offset). Give the first-step distribution and compare it with B12 (2 of 70; -23.6 ms and +521 ms).
4. Restore the as-found state with a read-back of every item.

Further constraints: cite 1722-2016, 1722.1-2021 and Milan v1.2 by clause; no RTL or firmware change. The output is a new `docs/findings/667_TALKER_START_BENCH.md` with a dated section "#667 bench: talker start on dev 28f9666f" and a "Soak record" section, plus a PR body reading "Refs #667".

Issue #667's own steps 2 and 3 (deciding ownership, then a simulation reproduction and a planted check) are not in this PR's scope. The PR says "Refs", not "Closes". The manager opened a separate fix lane in comment 6011846710.

## 2. What was examined and executed

All scripts are portable and live in the packet root. Their outputs are in `receipts/`.

| Script | What it does independently | Result |
|---|---|---|
| `recompute.py` | Decodes raw AAF header bytes (sequence, tv, tu, mr, avtp_timestamp at bytes 12..15), raw GET_COUNTERS payloads (mask and counter words, Milan compact STREAM_OUTPUT layout) and timing receipts. Compares every table and figure on the page: per-bind table, histogram, ranges, 61-row counter table, 145-row soak table, duration, interval, the GM/asCapable/path series and the receipt hash table. | 0 failures (`recompute.log`, rc 0) |
| `check_overlap.py` | For each of the nine soak gaps: the bridge in the adjacent segment starts at the "before" packet, ends at the "after" packet, and advances by exactly one sequence number (mod 256) with increasing tap time. | 9/9 PASS (`check_overlap.log`) |
| `check_binds.py` | For all 100 binds: talker and listener formats are equal before the bind, bind and unbind return Success, and the hold is at least 2 s. | PASS; hold 2014.112 to 2015.555 ms (`check_binds.log`) |
| `check_restore.py` | Compares the start and end effective-state snapshots row by row, ignoring only request bookkeeping. | 44/44 rows equal; 42 observations, 2 inventories, 18 zero bindings (`check_restore.log`) |
| `check_drops.py` | Kernel-drop statements in the capture receipts. | Soak: 434 zero and 1 missing (segment 063 VLAN). Startup: 300 zero (`check_drops.log`) |
| `check_evidence_manifest.py` | Published evidence bytes against MANIFEST.json. | PASS (`evidence-manifest-check.log`) |
| `mutate_probe.sh` | Plants six single defects (four on the page, two in the receipts) and requires `recompute.py` to fail on each. | 6/6 killed (`mutate_probe.log`) |
| Author offline controls rerun | `check_receipts.py` run on a scratch copy of the published packet. | 22 controls passed (`author-controls-rerun.log`) |
| Seven documentation gates at the exact head | docs_check, check_doc_style, gen_toc --check, check_em_dash --base 423ac5d9, check_doc_paths, check_baremetal_only --check, git diff --check. | All rc 0 (`gates.rc`, `gate-*.log`) |

Clause citations were checked against the standards texts:

- Milan v1.2: Section 5.3.7.7 with Table 5.4, Section 5.3.8.10 with Table 5.6 (including "reset ... from not bound to bound"), and Section 5.4.2.25 with Tables 5.13 to 5.17.
- IEEE 1722-2016: Sections 4.4.4.3 (mr) and 4.4.4.5 to 4.4.4.9 (tv, sequence_num, tu, stream_id, avtp_timestamp), and Clause 7 (AAF).
- IEEE 1722.1-2021: Sections 7.4.40 to 7.4.42 (GET_AVB_INFO, GET_AS_PATH, GET_COUNTERS), and 8.2.1, 8.2.4 and 8.2.5 (ACMP PDU, Listener and Talker state machines).

Further observations from the receipts, beyond what the page states:

- **PDU 1 is the outlier in all 14 EARLY binds.** PDUs 2 to 10 sit on the stream's trend, with steps of 124,999 to 125,020 ns in every bind. PDU 1's avtp_timestamp is 279,884,746 to 544,594,384 ns later than that trend predicts. PDU 1 still left on schedule: its tap spacing to PDU 2 is 124,992 to 125,025 ns.
  - The signed reading of the 2^32 ns timestamp (PDU 1 presented later than the trend, so in the future) agrees with the listener's choice of EARLY over LATE. That cross-checks the modulo-2^32 sign convention.
- **Binds 072 and 073 read EARLY=1 already at the pre-bind poll.** This is left over from the previous bind: Milan Table 5.6 does not reset on unbind. The attribution to 072 and 073 still holds:
  - the counters reset at the bind (FRAMES_RX fell from 15954 to 82 in 072 and from 15952 to 89 in 073, and MEDIA_UNLOCKED from 1 to 0 in both), so the post-bind EARLY=1 is new;
  - the wire shows a backward first step in both binds.
- **All 14 EARLY increments appear on the first post-bind poll that saw frames.** That is the 20-PDU poll in 13 binds. In bind 065 it is the 100-PDU poll, because the 20-PDU poll still read FRAMES_RX 0.
- **Four soak counters change only between checkpoints 0 and 1, and none changes afterwards.** These are DUT CLOCK_DOMAIN LOCKED, DUT STREAM_INPUT 1 MEDIA_LOCKED, and DUT STREAM_OUTPUT 0 and 1 MEDIA_RESET (each 0 to 1).
  - Both DUT outputs carry mr=1 from their first soak PDU, and the wire shows no mr toggle inside the window.
  - This fits the RTL's consecutive-PDU mr comparison (`hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:176-178`) and the Table 5.4 reset at stream start. It is not an error-class event under the assignment.
- **The one AAF mr toggle (sequence 159 to 160) follows the DUT's UNBIND_RX response for its CRF input by 57 µs on the tap clock** (`soak-final-wire-boundary.json` records 40 and 41). That is after `soak_end`, as the page says.

## 3. Findings

### R510-1-F1 - RESIDUE - Docs - `docs/findings/README.md:16` (Current entries table) - the new findings page is not indexed

- Authority/evidence: `docs/findings/README.md` lists every current findings page under "Current entries", and earlier bench lanes added their row (for example 653 in `6f76d612a`). `667_TALKER_START_BENCH.md` has no row at this head.
- Impact: the page can't be reached from the findings index. No measurement, figure, verdict, test, code or clause claim changes, so this is wording only.
- Exact fix: after the 653 row, insert:
  `| [667_TALKER_START_BENCH.md](667_TALKER_START_BENCH.md) | #667 bench lane B13 on dev `28f9666f`, seed `asl`: a two-hour bidirectional AAF/CRF soak with every counter at each checkpoint, and 100 two-second DUT-talker binds into the reference peer's input with the first ten AAF headers per bind (#667) | Soak: 145 checkpoints, no error-class increase, grandmaster, asCapable and path unchanged. Startup: EARLY in 14 of 100 binds, each with a backward first-to-second timestamp step of -544,469,385 to -279,759,747 ns; LATE 0; gPTP correlation NOT RUN; ownership open in #667 |`
- Verification: the row is present, and `docs_check.py`, `check_doc_paths.py` and `gen_toc.py --check` return 0.

### R510-1-F2 - RESIDUE - Docs - PR #676 body - the body does not use the PR template

- Authority/evidence: `CONTRIBUTING.md:405` and `.github/PULL_REQUEST_TEMPLATE.md` require Status, Linked Issue / roles, Description, Authoritative references, How to get into the same state, How to validate, Known limitations / out of scope, and Definition of Done. The body at this head is four untitled paragraphs.
- Impact: this is PR-body wording only. All of the content is already present.
- Exact fix: put the existing paragraphs under the template headings.
  - Status: the head and the gate tally.
  - Linked Issue / roles: "Relates to #667", Executor [A549], internal reviewer [R510], external reviewer [R511].
  - Description: the soak and startup paragraph.
  - Authoritative references: the page's authority table.
  - How to validate: the seven gate commands with expected rc 0.
  - Known limitations: the existing Limits paragraph.
  - Definition of Done: the checklist.
- Verification: the body shows the template headings and keeps "Refs/Relates to #667" without "Closes".

### R510-1-S1 - SUGGESTION - Docs, Conformance - `docs/findings/667_TALKER_START_BENCH.md:20-21` - image identity that discriminates

- Console VERSION `0x00020060` and AEM CRC `5ba355eb` are identical on the earlier image `bbf704ec` (REGISTER_MAP at both commits; `653_DISCONNECT_ORDER_BENCH.md:64`). The four ATDECC fields don't distinguish the two images either.
- The console read is retained only as a hashed `/tmp` artifact (`retained-artifacts.jsonl`, `console-identity.txt`), and the author HANDOFF's pointer to `identity.json` for it does not hold.
- The page does name the assigned image and links the assignment, which records flash-and-verify, so this is not a defect.
- Optional: record a bitstream payload CRC readback, as 653 does, or link the flash-and-verify record next to the identity sentence.

### R510-1-S2 - SUGGESTION - Docs - page line 39 - rate comparison

- "they establish no rate trend" is accurate as a hedge.
- Still, 2/70 against 14/100 is a notable difference (two-sided Fisher exact p ≈ 0.016) under different hold distributions and images.
- Optional: state the difference and that no cause is attributed.

### R510-1-S3 - SUGGESTION - Docs - page lines 68-71 - sign of "First offset"

- Optional: add that a positive offset means PDU 1's presentation time is later than the trend (further in the future), which is the EARLY direction.

### R510-1-S4 - SUGGESTION - Docs - page lines 195-198 - checkpoint-1 counter changes

- Optional: add one sentence on the four 0-to-1 changes between checkpoints 0 and 1 (section 2 above), so a reader does not have to infer them from the table.

### R510-1-S5 - SUGGESTION - Robustness, Docs - page lines 488-492 - durability of raw artifacts

- Raw captures and console transcripts are kept only under `/tmp` on the bench hosts, indexed by size and SHA-256.
- No rule requires durable retention for this lane, but `/tmp` is not durable.
- Optional: move them to retained storage and state where.

### Prior public review findings

At the time of this pass (2026-10-06T08:03Z) the PR had no review findings: zero review comments, zero reviews, and only the two "INDEPENDENT REVIEW STARTED" comments. Issue #667 had none either. The two new issue comments are a separate fix lane's assignment and TAKEN. Nothing needs resolving or retaining.

## 4. Per-lens results

[R510] PASS Conformance - `docs/findings/667_TALKER_START_BENCH.md` @afa4e687 against B13 assignment items 1-4, with `recompute.log`, `check_binds.log` and `check_restore.log`:
- identity PASS;
- 145 checkpoints with nine GET_COUNTERS each (every 1722.1 Section 7.4.42 counter-bearing DUT descriptor plus two peer inputs), maximum interval 55.727 s, timing read every checkpoint, no error-class change between any two consecutive checkpoints on decoded payloads;
- 100 binds at least 2 s each with formats matched;
- 14 EARLY and 0 LATE, matching the 14 backward steps one-for-one;
- B12 figures match `653_DISCONNECT_ORDER_BENCH.md:805-806`;
- restoration equal;
- every cited clause verified against the 1722-2016, 1722.1-2021 and Milan v1.2 texts;
- ENTITY NOT_SUPPORTED is allowed, because Milan v1.2 Section 5.4.2.25 Tables 5.13-5.17 do not include ENTITY.

[R510] PASS RTL - `git diff --name-status 423ac5d9..afa4e687` shows one docs file only, and the gitlinks are identical (`clone-restore-check.txt`). Checked:
- The page's counter-semantics claims agree with `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:32-40,171-178` and `docs/reference/REGISTER_MAP.md:955`: FRAMES_TX is an observation-interval count, and MEDIA_RESET is a consecutive-PDU mr toggle.
- The decode uses the Milan compact STREAM_OUTPUT layout (slot 2 MEDIA_RESET, slot 4 FRAMES_TX), confirmed by the raw final-boundary values [1,0,1,0,7201].
- The page makes no claim about the talker's start-path RTL.

[R510] PASS Robustness - startup and soak receipts @b2bb3c89:
- modulo-2^32 sign cross-checked by the listener's EARLY;
- pre-bind leftover EARLY in 072 and 073 is handled correctly (reset shown by FRAMES_RX and MEDIA_UNLOCKED);
- all nine soak gaps are bridged packet-for-packet (`check_overlap.log`);
- the one missing drop statistic is disclosed, and all other 734 receipts read 0;
- no counter decreased during the soak;
- STOP rules were defined and not triggered;
- the truncated-header and rollover controls were rerun and pass.

[R510] PASS Tests - `receipts/author-controls-rerun.log` (22/22), `recompute.log` (0 failures) and `mutate_probe.log` (6/6 planted defects killed). The PR adds no executable test, and none is owed: the assignment forbids RTL and firmware changes, and issue #667's simulation step belongs to the separate fix lane.

[R510] PASS Docs - `docs/findings/667_TALKER_START_BENCH.md` @afa4e687:
- seven gates rc 0 (`gates.rc`);
- every table and figure recomputed from raw receipts;
- the receipt hash table matches the published bytes;
- the B12 anchor and the contents anchors resolve;
- the required section titles and "Refs #667" are present;
- no bench-identifying text;
- RESIDUE F1 and F2 are wording only.

## 5. Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page; B13 assignment and issue body; `start-*.json`, `start-*-wire.json`, `counters-soak-*.jsonl`, `timing-soak-*.jsonl`, `restore-*.jsonl`; standards texts | R510-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| RTL | CLEAN | Diff name list, gitlinks, `KL_talker_diag_ctx.sv:32-40,171-178`, `REGISTER_MAP.md:955`, raw STREAM_OUTPUT payloads | R510-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| Robustness | CLEAN | Overlap bridges, drop statements, pre-bind leftovers, sign convention, counter monotonicity, author adverse controls | R510-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| Tests | CLEAN | Author offline controls (rerun), independent recompute and its mutation probe | R510-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| Docs | CLEAN (RESIDUE F1, F2 carried) | Page, findings index, PR body, seven gates, hash table, anchors | R510-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |

## 6. Real limits

- **Physical measurements were not repeated.** No hardware was touched and no physical calibration was run. The bench figures come from the published receipts, re-derived from their raw header and payload bytes.
- **The raw pcaps and console transcripts are not published.** They sit under `/tmp` on the bench hosts and are identified only by size and SHA-256. Anything that depends on them, beyond the decoded header bytes and receipts, was not re-derived: the 28-byte tap prefix, the capture filters, and the console VERSION and AEM CRC read.
- **Absolute gPTP correlation was NOT RUN by the lane and cannot be reconstructed.** The page says so, and it does not claim to assign ownership.
- **The hosted jobs were not run by this reviewer.** At 2026-10-06T08:03Z (`receipts/hosted-checks.tsv`):
  - executed and successful: rtl-fast, bdd-conformance, changes, docs-check-no-git, elaborate, full-ci-gate, wire-accountability;
  - still in progress: docs-check;
  - skipped contexts, which are not evidence: verilator-suites, yosys-portability, verilator-lint, yosys-elaboration, both shard matrices, Physical gPTP.
- **The full parent/PP/gPTP/Yosys/builder banks were not run,** as instructed. The manager's source banks at this head are taken as the manager's evidence.

## 7. Pending manager duties

- Carry RESIDUE F1 (findings index row) and F2 (PR body template) to the residue checklist.
- Hosted and act acceptance at the exact head, including docs-check's final conclusion.
- Build and validate the current-dev candidate merge result at the merge turn. The source base and live dev are both 423ac5d9 at review time.
- External review (R511), and the full CONTRIBUTING completion bar before any authorized merge.
- Keep issue #667 open: steps 2 and 3 belong to the fix lane.

## 8. Clone state after review

- HEAD and tree are the exact published values, and `git write-tree` equals the head tree.
- The index and worktree are clean, with zero untracked or ignored entries. The `scripts/__pycache__` files created by the gate run were removed.
- All 1,106 regular tracked files match the index in bytes and mode.
- All four gitlinks are at their pins (`receipts/clone-restore-check.txt`).

R510-1 FINISHED
