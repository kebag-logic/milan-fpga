[R799] POSITIVE - exact head a88772f1cf0c3c3b269294bd4ceaf436646ca5a1

Round R799-2 is the internal cleared-context delta review of PR #861 (issue #665 S6b, the two-placement `milan_dp` twin). The exact head is `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1`, tree `f8114fa174c093957ad04c6a07e4431675557883`. The reviewed delta is `e69d243a..a88772f1` (5 commits, 22 files, +113/-78), the head my round R799-1 reported on. The authority is the [A10] round 6 ruling on #665, issuecomment-6727748772: "text and one plant", with no grade, ledger row or owed row allowed to change. Out of scope and not re-judged: R800-1 SUG-1 and R799-1 S2-S4.

**Verdict: POSITIVE.** All four ruling items are met at this head, and I reproduced each one myself.
- No added source line carries a comment ID, ruling ID or lane label.
- Table 7-2 is cited in both lines.
- The split-cdc count is twelve in both places.
- The new `leave-all-omission` plant is refused by the Table 10-3 grade's own words. It is the only plant that catches the two grade mutants that escaped in round 1.

Every prior finding is resolved. No BLOCKER, MAJOR or MINOR is open. Two wording items are recorded as RESIDUE and one formatting item as a SUGGESTION.

## What I ran (exact head, clean clone under the packet's scratch, Verilator 5.050 identified by `--version`)

| Check | Result | Receipt |
|---|---|---|
| `make -j8 twin` | rc 0, `twin: 0 finding(s)`. 6 `[LEDGER]` rows, 6 `[OWED]` rows and 1 `[TAIL]` note, nothing else. The split half has 260 frames and the fabric half 195 | `receipts/make_twin.filtered.log`, `make_twin.rc`, `make_twin.rows.txt` |
| Printed rows at `e69d243a` (my round-1 receipt) against this head | the 6 LEDGER rows and the TAIL note are byte-identical. In the 6 OWED notes only the "owed to" suffix differs. Every name, fabric/split assertion, clause and cause is identical | `receipts/rows_e69d243a_vs_head.diff` |
| `make -j6 twin-plants` | rc 0. 40 `REFUSED`, 0 `ESCAPED`, 20 plants each refused twice. `leave-all-omission` is refused in both controls by `[MRP] split MSRP Domain value 06030002: nothing at ms 27910 (a LeaveAll) is not an Applicant's message: from AA, QA, Table 10-3's txLA! sends JoinMt or Mt` | `receipts/make_twin_plants.filtered.log`, `make_twin_plants.summary.txt`, `make_twin_plants.rc` |
| Captures against the author's (`author-r6/receipts/twin/captures-sha256.txt`) | `fabric.json`, `split.json`, `report.json` and `split-leave-all-omission.json` all have the same sha256. The first two are also identical to the `e69d243a` captures (`fa6a5a12`, `ee143865`) | `receipts/twin_captures_sha256.txt`, `receipts/twin_capture/` |
| My round-1 omission probe (written independently in R799-1, unchanged) against the new plant | the probe and the plant change the same single frame (index 129, ms 27910), from 201 bytes to 194: a VectorHeader, the 4-byte Domain FirstValue and one ThreePackedEvents octet. Both outputs are byte-identical frame for frame. The head grade gives the plant's words, plus the knock-on `JoinMt at ms 28110 ... from LO` | `receipts/probe_leaveall_omission.txt`, `receipts/compare_omission_frames.txt`, `scripts/probe_leaveall_omission.py`, `scripts/compare_omission_frames.py` |
| My round-1 eighteen-arm `twin_mrp.py` mutation probe. The only change is that `leave-all-omission` is added to its plant list | head clean, 12 of 18 caught (10 in round 1). `txla-qa-bracketed` and `txla-aa-sends-nothing` are now caught, and only by `leave-all-omission (self)` and `leave-all-omission` (between). `periodic-dropped` is also caught by it. The 6 that still survive are S2's, which is out of scope | `receipts/probe_mrp_mutants.txt`, `scripts/probe_mrp_mutants.py` |
| Comment-rule scan of added non-Markdown lines, my round-1 rule re-derived as `scripts/scan_comment_rule.py` | reproduces my round-1 43 lines exactly at `6584b7bf..e69d243a`. At `6584b7bf..a88772f1` it finds **0** | `receipts/scan_calibration_e69d243a.txt`, `receipts/scan_head.txt` |
| The same scan widened (bare `S<n>`, `A/B/R<n>`, "plan's", "lane", "round") | 23 hits, none a lane label or ID: `1'b0` literals, "round(" and "each round", "lane 0" and "little lane order" (byte lanes), and the generic "the lane that fixes it" (no lane named) | `receipts/scan_head_broad.txt` |
| The other review's published scan script, run unchanged (sha256 `b3742b25...f869`) | 42 lines at `e6d27f3a..e69d243a`, its own count. 0 at `e6d27f3a..a88772f1` and 0 at `6584b7bf..a88772f1` | `receipts/scan_external_script_head.txt` |
| Table 7-2 | `git grep "Table 7\.1" -- sw/firmware/ctrl` is empty. `test_aecp.cpp:437`, `aecp_mutants.py:408` and `ctrl_app_aecp.c:106` cite IEEE 1722.1-2021 Table 7-2 | `receipts/table_7_2.txt` |
| split-cdc count | `split_cdc_check.py` `PLANTS` holds 12, and the file is unchanged since `e69d243a`. `CI_WORKFLOWS.md:437-442` and the `rtl-fast.yml` template comment (`:321-324`) both say twelve, split 4 + 5 + 2 + 1. Each group matches the plant names | `receipts/split_cdc_count.txt` |
| `docs_check`, `check_doc_style`, `check_doc_paths`, `DOC_MAP.gen.py --check`, `check_py_idiom`, `check_cpp_idiom`, `check_sv_idiom`, `check_hygiene --check`, `check_todo_ownership`, `ci_events --check`, `ci_gate_workflows --check` | all rc 0. `ci_events`: 2271 contract items OK | `receipts/gates/*.log`, `*.rc`, `SUMMARY.txt` |
| Author receipts `author-r6` (evidence commit `50cf8d3c`) | every receipt's first line names this head. The CI replay table has 546 steps at rc 0, 0 failed, and 86 not run with a reason each (APT resolution, GitHub API, source builds of pinned tools). 63 steps were adapted to this host, each noted. Also recorded: `make split-cdc` 13/0, `test_ctrl_firmware` PASS (570 of 570 mutants), both scans empty, and the author's omission-mutant probe PASS | `review-evidence/665s6b-r1/author-r6/receipts/` (read by section, not copied) |
| Hosted checks at the exact head (snapshot 01:12Z) | 17 success and 1 skipped by its `if:` (Physical gPTP). Success includes `split-cdc`, `firmware-unit`, `firmware-aecp-mutants`, `firmware-verilator`, `docs-check-no-git`, `docs-gates-2`, `yosys-elaboration` and `verilator-lint`. 28 were still in progress or queued | `receipts/hosted_checks_snapshot.txt` |

## Prior findings, resolved or retained at this head

| ID | Round | Status at `a88772f1` | Evidence |
|---|---|---|---|
| F1 (MINOR, Conformance, Docs): Table 7.1 for `available_index` | R799-1 | **RESOLVED** | `test_aecp.cpp:437` and `aecp_mutants.py:408` cite Table 7-2. The PR body states it for all three files (Status, and the `ctrl_app_aecp.c` row). `receipts/table_7_2.txt` |
| F2 (MINOR, Docs): split-cdc "four planted raw crossings" | R799-1 | **RESOLVED** | both lines state twelve and what they cover. Twelve is the leg's `PLANTS` and the README's count. `receipts/split_cdc_count.txt` |
| R1 (RESIDUE): comment rule, 43 lines | R799-1 | **RESOLVED** | the scan finds 0. Each replacement names #665, #857, #858 or #860, a clause, or what the line does. Every replaced comment ID (`6505997821`, `6715535566`, `6716584453`, `6717765106`, `6722002738`, `6724570965`) is a comment on #665, so `(#665)` cites the right issue |
| S1 (SUGGESTION, Tests): no plant for the LeaveAll-omission arm | R799-1 | **RESOLVED** | `leave-all-omission` plant, `twin_plants.py:201-223`. It is refused by its words and catches both surviving txLA! mutants |
| S2, S3, S4 | R799-1 | out of scope (ruling), retained as suggestions, not re-judged | n/a |
| RES-1 (RESIDUE): comment rule | R800-1 | **RESOLVED** | its script, unchanged, finds 0 at head |
| RES-2 (RESIDUE): Table 7.1 and the PR body | R800-1 | **RESOLVED** | as F1 |
| SUG-1 | R800-1 | out of scope (ruling) | n/a |

## Findings at this head

**RES-A - RESIDUE - Docs - the PR body, Status, first bullet - "four printed `[OWED]` notes"**
- Evidence: the delta changes the "owed to" text of **six** printed `[OWED]` notes, through four strings. `SRP_ROUND` is used by `stream-output-0-notices` and `split-talker-failed`, `ONE_NEW` by both #860 rows, and the #857 and #858 rows each have their own string (`receipts/rows_e69d243a_vs_head.diff`, 6 changed lines).
- Impact: wording only. No row, value or verdict changes.
- Exact fix: "That includes the 'owed to' text of the six printed `[OWED]` notes (four strings)."

**RES-B - RESIDUE - Docs - `tb/verilator/milan_dp/README.md:1376-1377` - the owed table's "Owed to" column no longer reads as the printed note does**
- Evidence: the README column says "the SRP adapter round after S2b". The printed notes now say "owed to the SRP adapter entry that takes MAAP's allocation (#665)" (`twin_compare.py:461`). Both name the same pending work: the PR body's *Known limitations* bridges them, and the README's next paragraph (`:1380-1381`) names the adapter entry. A lane name is allowed in a design page.
- Impact: wording only. A reader matching a printed note to the table sees two names for one owner.
- Exact fix (optional): "the SRP adapter entry that takes MAAP's allocation (the SRP adapter round after S2b)" in both cells.

**SUG-A - SUGGESTION - Docs - reflow of the edited comments**
- Where: shortening the comments in place left ragged lines.
  - `twin_mrp.py:7` (35 characters)
  - `ctrl_app_aecp.c:108` (41)
  - `test_aecp.cpp:439` (46)
  - `Makefile:883` (60) and `:949` (120, among neighbours wrapped at about 78)
  - `twin_fabric.cpp:17-18` (63 and 43)
  - `.github/ci-templates/rtl-fast.yml:324` (54)
- These are cosmetic. No gate refuses them (`check_hygiene`, `check_doc_style` and the idiom checks rc 0).
- Fix: re-wrap each paragraph, or leave it.

No other finding. Some substitutions change what a line says beyond removing the ID, so I checked each against the code:
- `twin_grades.py:22` now cites Milan v1.2 4.2.7.2.2 for MSRP's Registrar, as `twin_mrp.py:8-9` and `REGISTRAR` do.
- `twin_decode.py:189-190` cites Milan v1.2 5.4.5.2 and Table 5.22, as the `stream-output-0-notices` row does.
- `twin.hpp:25` attributes the second ENTITY read to #858, the row it feeds.
- `census_split.py:66-69` drops "S11's" for "not built yet". That states the behaviour, as the ruling allows.

## Lens results (artifact-specific)

- **Conformance - CLEAN.**
  - `twin_plants.py:201-223` reads the frame's LeaveAll types through `td.msrp_frame` (`twin_decode.py:262-267`, IEEE 802.1Q-2018 10.8.2.6: a LeaveAll in a Message applies to its type). It removes the Domain's single-value vector and shortens the Message's AttributeListLength by the vector's 7 bytes. Its txLA! reading matches the `twin_mrp.py:16-20` docstring.
  - The Table 10-3 refusal "from AA, QA ... txLA! sends JoinMt or Mt" agrees with the TXLA row in round 1's lwSRP cross-check.
  - Table 7-2 is cited correctly in all three AECP files.
  - No grade, ledger row or owed row changed: the printed rows differ only in the owed-to suffix. In `twin_compare.py`, the only additions besides comments are the new `PLANT_WORDS` and `SELF_WORDS` entries.
- **RTL - CLEAN.**
  - The delta touches no `hdl/` file. Its only SystemVerilog change is the comment at `tb_split_top.sv:61`.
  - `split_cdc_check.py` is unchanged. Hosted `split-cdc` and the author's `make split-cdc` (13/0) pass at this head.
  - Both twin halves build and run under Verilator 5.050 (`make_twin.filtered.log`).
  - Round 1's RTL verdict otherwise stands: nothing it depends on changed.
- **Robustness - CLEAN.**
  - The new plant refuses with `SystemExit` when no split MSRP frame at or after 20000 ms has a LeaveAll covering the Domain (`twin_plants.py:223`).
  - Its refusal requires its exact words, so a stimulus that moved the frame would escape loudly rather than pass.
  - The other robustness artifacts (`split_parallel.py`, `twin_split.cpp`, `twin_fabric.cpp`, the `available_index` edges) changed only in comments. Round 1's verdict stands.
- **Tests - CLEAN.**
  - 20 plants are each refused twice (40/40).
  - The new plant fails for the defect it claims: both txLA! mutants escape it and nothing else (`probe_mrp_mutants.txt`).
  - My independent probe and the plant are byte-identical. All captures are reproducible against the author's.
  - The comment-only edits to `test_aecp.cpp` and `aecp_mutants.py` leave hosted `firmware-unit` and `firmware-aecp-mutants` green at this head.
- **Docs - CLEAN** (RES-A and RES-B are residue, SUG-A is a suggestion).
  - `CI_WORKFLOWS.md:430-442` and the `rtl-fast.yml` template `:318-326` state twelve plants, which matches `PLANTS`.
  - The `milan_dp` README twin section (`:1319-1325`, `:1407`, the plants table's 20 rows including `leave-all-omission` with its exact words), `MAILBOX_SPLIT.md:1544` (twenty) and the Makefile header `:40` all match my run.
  - No stale "nineteen plants" or "four planted" text is left in the repository.
  - The PR body agrees on Table 7-2, the twelve plants, and the 20 plants in 40 controls.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `twin_plants.py:201-223`, `twin_decode.py:262-267`, `twin_mrp.py:1-40`, `twin_compare.py` (LEDGER, OWED, OWED_GRADES, PLANT_WORDS, SELF_WORDS), the printed rows against `e69d243a`, `ctrl_app_aecp.c:106`, `test_aecp.cpp:437`, `aecp_mutants.py:408` | R799-2 | a88772f1cf0c3c3b269294bd4ceaf436646ca5a1 |
| RTL | CLEAN | delta has no `hdl/` change, `tb_split_top.sv:61` (comment), `split_cdc_check.py` unchanged, the twin builds, hosted `split-cdc` | R799-2 | a88772f1cf0c3c3b269294bd4ceaf436646ca5a1 |
| Robustness | CLEAN | `twin_plants.py:201-223` (anchor refusal), the comment-only edits in `split_parallel.py`, `twin_fabric.cpp`, `ctrl_app_aecp.c` | R799-2 | a88772f1cf0c3c3b269294bd4ceaf436646ca5a1 |
| Tests | CLEAN | `make twin-plants` 40/40, the grade mutation probe (12/18, both txLA! arms caught only by the new plant), the independent omission probe (byte-identical), capture hashes | R799-2 | a88772f1cf0c3c3b269294bd4ceaf436646ca5a1 |
| Docs | CLEAN | `CI_WORKFLOWS.md:430-442`, `.github/ci-templates/rtl-fast.yml:315-326`, `tb/verilator/milan_dp/README.md` (twin section, plants table), `MAILBOX_SPLIT.md:1544`, `Makefile:40,945-955`, both comment-rule scans, the PR body | R799-2 | a88772f1cf0c3c3b269294bd4ceaf436646ca5a1 |

## Real limits

- I have no copy of IEEE 802.1Q-2018, IEEE 1722.1-2021 or Milan v1.2 on this host. The Table 10-3 reading rests on lwSRP's independent transcription (round 1) and the rulings, and the Table 7-2 citation on the rulings and the repository's own usage, not on the printed standards.
- I did not run the 546 workflow `run:` steps, the full sweep, the census, `ctrl_boundary.py`, `test_builder.py`, the firmware self-test, `make split`, `split-mutants` or `split-cdc` at this head. For these I rely on the author's `author-r6` receipts, which name this head, and on the hosted jobs. The 86 steps the author could not run on its host, and the 63 it adapted, are executed only by hosted CI.
- `check_em_dash.py` and `gen_toc.py --check` need the pinned Markdown renderer, which is not on this host. I did not run them, and installed nothing.
- I ran the other review's scan script read-only, after my own scan and verdict pass. I did not read that review's round-2 work.
- Physical calibration NOT RUN. No hardware or field evidence is claimed. No manager source bank exists at this head, and I claim none.
- Probe hygiene:
  - All builds and probes ran in a clone under the packet's scratch. That clone is also clean, with tracked files unchanged.
  - The review clone is unchanged: `HEAD` and tree as above, an empty `git status`, and the index hash equal to the `HEAD` tree hash. All six gitlinks are at their recorded commits (`receipts/review_clone_integrity.txt`).
  - I fetched nothing into the review clone. The evidence commit was fetched into a separate scratch repository.

## Pending manager duties

- Hosted acceptance at this head: 28 contexts were still in progress or queued at 01:12Z.
- The current-dev merge candidate (source base `6584b7bf`, live `dev` `0a75aa77`), with its builder and native banks, at the merge turn. Base ordering is unchanged: S6a (#853) first, then this PR retargets `dev-soft-core`.
- Carry RES-A and RES-B to the residue checklist.

R799-2 FINISHED
