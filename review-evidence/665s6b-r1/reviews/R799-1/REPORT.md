[R799] NEGATIVE - exact head e69d243a61a8ec1c1ad8c473f809e1351dab1b61

Round R799-1, the internal cleared-context review of PR #861 (issue #665 S6b, the two-placement `milan_dp` twin co-simulation). Exact head `e69d243a61a8ec1c1ad8c473f809e1351dab1b61`, tree `037c224506ac65797390f90449df3cc743a553db`. The reviewed delta is `e6d27f3a..e69d243a` (30 commits, two of them merges of `665-s6-placement` at `e6d27f3a`): 32 files, +5482/-74. S6a's own commits were not reviewed. The authority is the [A10] rulings on #665: issuecomment-6724570965 (round 5), with -6722002738, -6717765106 and -6716584453 where round 5 does not change them. Out of scope and not reported: the REBOOT carrier, the AECP-owned items (S11), and `aecp/README.md` lines 24-29.

**Verdict: NEGATIVE.** The twin does what the rulings ask, and I reproduced its gates independently at this head. Two MINOR documentation and citation defects are open (F1, F2), so `Conformance` and `Docs` are not clean. `RTL`, `Robustness` and `Tests` are clean. Both fixes are text-only.

## What I ran (exact head, clean clone under the packet's scratch, pinned Verilator 5.050 verified by `--version`)

| Check | Result | Receipt |
|---|---|---|
| `make -j8 twin` | rc 0, `twin: 0 finding(s)`. 6 `[LEDGER]` and 6 `[OWED]` rows hold, and one `[TAIL]` note | `receipts/make_twin.filtered.log`, `make_twin.rc`, `twin_capture/report.json` |
| `make -j6 twin-plants` | rc 0. 38 `REFUSED`, 0 `ESCAPED`, 19 plants | `receipts/make_twin_plants.filtered.log`, `make_twin_plants.rc` |
| The captures against the author's published ones (`fe98f210`, `author-r5/receipts/twin/*.json.txt`) | both halves frame for frame identical (195 and 260 frames), and the applied stimulus identical | the comparison was run inline; my captures are in `receipts/twin_capture/` |
| `split_parallel.py --selftest` | rc 0. The planted old rule fails with rc 2 and `Vmilan_dp_split: No such file or directory`. A clean clone of HEAD passes `make -j8 split` with rc 0 and `checks: 71   failures: 0` | `receipts/split_parallel_selftest.log` |
| `make split-cdc` | rc 0, `checks: 13   failures: 0` | `receipts/gates/split_cdc.log` |
| The raw per-half grade before the owed rows | the split has 0 findings. The fabric has 4: the MVRP LeaveAll gap (#857), the Domain JoinMt at 1000 ms (#860), and the VID 2 JoinIn at 6200 and 10201 ms (#860) | `receipts/probe_grades.txt`, `scripts/probe_grades.py` |
| Eighteen-arm mutation probe of `twin_mrp.py`, judged by `make twin` plus every capture-plant control | head clean. 10 mutants caught; 8 survive (see S1, S2) | `receipts/probe_mrp_mutants.txt`, `scripts/probe_mrp_mutants.py` |
| A LeaveAll that leaves out the declared Domain, planted in a copy of the split capture | the head grade refuses it: `nothing at ms 27910 (a LeaveAll) is not an Applicant's message` | `receipts/probe_leaveall_omission.txt`, `scripts/probe_leaveall_omission.py` |
| The Milan v1.2 4.3.2 check given a stream frame at 1000 ms | it fires. At this head it is vacuous only because the stimulus sends no stream frame | `receipts/probe_mvrp_vacuous.txt`, `scripts/probe_mvrp_vacuous.py` |
| How the boundary gate classifies the leg's builders | `twin_compare.py` and `twin_decode.py` are OUTSIDE, `twin_fw.py` is SUITES. No other new leg file is a builder by text | `receipts/probe_classified.txt`, `scripts/probe_classified.py` |
| `docs_check`, `check_doc_style`, `check_doc_paths`, `DOC_MAP --check`, `check_py_idiom`, `check_cpp_idiom`, `check_sv_idiom`, `check_hygiene --check`, `check_todo_ownership`, `ci_events --check`, `ci_gate_workflows --check`, `lint_rtl --check` | all rc 0. Lint is 89 <= 89 | `receipts/gates/*.log`, `*.rc` |
| U+2014 in the added lines of the delta | 0 | `receipts/gates/em_dash_delta_grep.txt` |
| Comment-rule scan of the added non-Markdown lines | 43 lines in 18 files (R1) | `receipts/residue_source_by_file.txt`, `residue_source_lines.txt` |
| Hosted checks at the exact head (snapshots at 21:54Z and 21:59Z) | 22 success and 1 skipped by its `if:` (Physical gPTP). Success includes `firmware-boundary`, `firmware-aecp-mutants`, `firmware-unit`, `firmware-verilator`, `split-cdc`, `docs-gates-0..2` and `yosys-elaboration`. Still running or queued: 17 Verilator shards, `publication-census`, `docs-check` and `elaborate` | `receipts/hosted_checks_final_snapshot.txt` |

Three checks I could not run on this host: `check_em_dash.py` and `gen_toc.py --check` need the pinned Markdown renderer, and `publication_census.py --check` refuses sv2v v0.0.13 because it requires the pinned v0.0.12. I installed nothing. These three rest on the hosted jobs and the author's receipts.

## Findings

**F1 - MINOR - Conformance, Docs - `sw/firmware/ctrl/test/test_aecp.cpp:437`, `sw/firmware/ctrl/test/aecp_mutants.py:408` - the ENTITY descriptor's `available_index` is cited to the wrong table**
- Authority/evidence: both added comments cite "IEEE 1722.1-2021 Table 7.1" for the ENTITY descriptor's `available_index`. That field is in Table 7-2. Ruling issuecomment-6724570965 item 4 says so, and the head's own `ctrl_app_aecp.c:106` and `twin_compare.py:417` cite Table 7-2. Table 7-1 is the descriptor-type table, which is how the repository itself cites it (`docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2162`). Item 4 required the C line fixed in this round "because the line is round 3's own". Both of these lines come from the same round-3 change. The PR body discloses `aecp_mutants.py:408` but not `test_aecp.cpp:437`.
- Impact: a wrong clause citation, beside the test and the mutant that guard the behaviour it describes. A reader checking the requirement goes to the descriptor-type table.
- Required outcome: both comments cite IEEE 1722.1-2021 Table 7-2.
- Verification: `git grep -n "Table 7\.1" -- sw/firmware/ctrl` returns nothing.

**F2 - MINOR - Docs - `docs/testing/CI_WORKFLOWS.md:437`, `.github/ci-templates/rtl-fast.yml:321` - the `split-cdc` job's proof is misstated**
- Authority/evidence: both lines come from S6b's `de709c31a6` and say the job's "four planted raw crossings must each be refused". At this head `split_cdc_check.py` `PLANTS` (line 258) holds 12. The source base `6584b7bf` held 4; S6a's `e6d27f3a` holds 12. The 12 include a reset from the other domain on each side, four held-bus arms and a primitive clocked by a level, which are not raw crossings. My run printed `checks: 13   failures: 0`. The head's own `tb/verilator/milan_dp/README.md` (the `make split-cdc` paragraph before line 1179) states twelve. The merge of S6a made both lines stale, and they were not updated.
- Impact: the authoritative CI policy page understates what the hosted `split-cdc` job proves, and contradicts the leg's README.
- Required outcome: both lines state the twelve plants and what they cover, or refer to the leg README instead of giving a count.
- Verification: the two lines are read against `split_cdc_check.py` `PLANTS`, and `ci_events.py --check` still passes.

**R1 - RESIDUE - the comment rule - 43 added source lines in 18 files** (the full list with lines is `receipts/residue_source_by_file.txt`)
- What: source comments and printed row strings in the delta carry issue-comment IDs (`issuecomment-...`, `ruling 6715535566`, `ruling 6505997821`) or plan-lane names (`S6b`, `S2b`, `S11`, `S12`, `S13`). Examples: `tb/verilator/milan_dp/Makefile:868,883-884`, `split_parallel.py:7,39`, `tb_split_top.sv:61` ("#665 S6b"), `sw/firmware/ctrl/app/ctrl_app_aecp.c:108`, `test_aecp.cpp:439`, `twin_compare.py` (12 lines, among them the `SRP_ROUND` and `ONE_NEW` strings), `twin.hpp` (5), `census_split.py:11,67,70`, `scripts/ci_events.py:1344-1345,2494`, `.github/ci-templates/rtl-fast.yml:318`.
- Exact fix: replace each comment ID with `#665` and the reason or requirement it stands for, and each lane name with the behaviour or owning issue. For example, "owed to the SRP adapter entry (#665)" for `SRP_ROUND`, and "#860 (a release-image defect)" for `ONE_NEW`. No verdict, test or figure changes.
- Note: the design pages add 21 lines with comment IDs, in `MAILBOX_SPLIT.md` and the `milan_dp` README. The owner rule names source comments only. S6a removed the same shape from its docs pages in `31acb6d3`, so doing likewise here is consistent but optional.

**S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/twin_mrp.py:16-20,76-77` - no plant guards the LeaveAll-omission arm.** The docstring says a LeaveAll frame that leaves out an attribute is legal only from a state whose txLA! action is none or bracketed. The arm works at head (the omission probe). But the mutants `txla-qa-bracketed` and `txla-aa-sends-nothing` survive `make twin` and all 38 plant controls, so a regression in the arm would pass silently. A capture plant like the probe would pin it.

**S2 - SUGGESTION - Tests - `twin_mrp.py` cells no trace here can tell apart.** These mutants survive: note 8 dropped, the Milan v1.2 4.2.7.2.2 cell dropped from MSRP or given to MVRP, AA's rJoinIn! dropped, rNew!'s Registrar transition dropped, and `OPER_P2P` false for the split. For the Milan cell the module states why: no message can depend on it (`twin_mrp.py:31-34`). The others go unseen because no MRPDU reaches either half. Each cell agrees with lwSRP's independent Table 10-3 (`third_party/lwSRP/src/core/mrp_mad.c:150-275`), except note 8, which lwSRP leaves out. A received-frame plant for note 4/5 and for rNew! would make these cells observable.

**S3 - SUGGESTION - Conformance, Docs - `tb/verilator/milan_dp/twin_compare.py:653-654`.** Across the halves the comparison also compares the set of MSRP Ethernet headers. Ruling -6722002738 item 3 says to compare "only the declaration state". The check passes at this head and can only find a real difference, but neither the module docstring nor the README's comparison table mentions it. State it there, or have it ruled.

**S4 - SUGGESTION - Tests - `twin_grades.py:215-231`.** The 4.3.2 and 4.4.1 checks are vacuous in this stimulus, and the PR says so. A capture plant for each would show they can fail. The probe shows 4.3.2 does.

Prior public review findings on PR #861: none. The PR has no reviews and no review comments besides the two review-start notices, and #665 has no `[R...]` finding on S6b. There is nothing to resolve or retain.

## Lens results (artifact-specific)

- **Conformance - UNCLEAN (F1).**
  - Examined: `twin_mrp.py:44-101` against IEEE 802.1Q-2018 Table 10-3, its notes 4, 5 and 8, Table 10-4 and 10.7.6.3.
  - Evidence:
    - The rows agree cell for cell with lwSRP's transcription. VN and AN tx! send New. sJ gives JoinIn only with the Registrar IN.
    - MSRP's Registrar carries the Milan v1.2 4.2.7.2.2 cell. MVRP's is Table 10-4 as printed.
    - `OPER_P2P` is TRUE in both halves, as `hdl/milan/KL_pp_shadow.sv:1289` ties `p2p_i` and `srp_mbx.c:252-253` configures both participants.
    - The split's MSRP and MVRP traces pass with 0 grade findings. Across the halves only the LeaveAll-boundary declarations are compared (`compare_declarations`, besides S3).
    - `sequence_id` per IEEE 1722.1-2021 9.2.2.9: `COMMANDS` drops it from the byte compare (`td.without_seq`), and `grade_commands` grades it per destination controller, rising mod 2^16 with gaps allowed and each response matching its command. Measured: the fabric sends [0] and [0, 1], the split [1] and [0, 2].
    - Every ledger row's fabric and split predicates exclude each other, so a row that holds is a real difference at pin `a9e84b66`.
    - The three `OWED_GRADES` rows name #857 or #860, and `entity-available-index` names #858. The two SRP-adapter rows are owed to the SRP adapter round, as ruling -6717765106 item 3 sets. Each row asserts exact traces and prints "has gone" when its plant lands the fix.
- **RTL - CLEAN.**
  - Examined: the delta has no `hdl/` change.
  - `tb_split_top.sv:59-78,331-333` brings the CSR window out, and `sim_split.cpp:97-102` holds it idle for the split leg. No other harness instantiates `tb_split_top`.
  - Both twin halves build and run under Verilator 5.050 (`make_twin.filtered.log`).
  - `lint_rtl --check` gives 89 <= 89, and `make split-cdc` 13/0.
  - `make -j8 split` from a clean tree gives 71/0.
  - The split census is the hosted `publication-census` job, still running.
- **Robustness - CLEAN.**
  - `split_parallel.py:48-80,96-143`: setup failures refuse with rc 2, the selftest needs the rule exactly once, and the verdict needs both rc 0 and `failures: 0`.
  - `twin_split.cpp:413-451` and `twin_fabric.cpp:261,276,355-381`: the AXI timeouts throw, a boot stop, a missing plant or an unwritten capture exit 2, and host timeouts exit 1.
  - `twin_plants.py`: each plant refuses (`SystemExit`) when its anchor is absent.
  - `ctrl_app_aecp.c:113-118`: the value is 0 before the first ENTITY_AVAILABLE and after DEPARTING, and the 2^32 wrap is documented. `test_aecp.cpp:443-482` and the two new mutants guard it, and hosted `firmware-aecp-mutants` and `firmware-unit` pass at this head.
- **Tests - CLEAN** (S1, S2 and S4 are suggestions).
  - All 19 plants are refused twice (38/38), and each plant's words match its row or grade (`twin_compare.py:69-120`, `twin_plants.py`).
  - 10 of 18 grade mutants are caught.
  - The split gate's selftest refuses the old rule without reading any host clock.
  - The captures are reproducible, byte-identical to the author's.
- **Docs - UNCLEAN (F1, F2; R1 is residue).**
  - Examined: `tb/verilator/milan_dp/README.md` (the twin section and its tables, read against my run: the counts, the per-controller ids, the #860 traces, the "second VID 2 JoinIn inside the LeaveAll frame", which `fabric.json` shows as two VID 2 vectors at 10201 ms), `docs/design/MAILBOX_SPLIT.md`, `docs/testing/CI_WORKFLOWS.md:430-440`, the PR body and the REVIEW READY comment.
  - The PR body says it touches S6a's Makefile and S2b's tree.
  - `sw/firmware/ctrl/README.md:255` says 181 pin controls, which matches the author's `ctrl_boundary` receipt and the hosted `firmware-boundary` success. I did not recompute it.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `twin_mrp.py`, `twin_compare.py` (LEDGER, OWED, OWED_GRADES, COMMANDS), `twin_grades.py`, `ctrl_app_aecp.c`, `test_aecp.cpp`, `aecp_mutants.py`, cross-checked against lwSRP `mrp_mad.c` | R799-1 | e69d243a61a8ec1c1ad8c473f809e1351dab1b61 |
| RTL | CLEAN | `tb_split_top.sv`, `sim_split.cpp`, the twin builds, `lint_rtl`, `split-cdc`, `make -j8 split` | R799-1 | e69d243a61a8ec1c1ad8c473f809e1351dab1b61 |
| Robustness | CLEAN | `split_parallel.py`, `twin_split.cpp`, `twin_fabric.cpp`, `twin_plants.py`, the `available_index` edge cases | R799-1 | e69d243a61a8ec1c1ad8c473f809e1351dab1b61 |
| Tests | CLEAN | `make twin-plants` (38/38), the grade mutation probe, the omission probe, the 4.3.2 probe, `split_parallel --selftest`, the capture reproducibility | R799-1 | e69d243a61a8ec1c1ad8c473f809e1351dab1b61 |
| Docs | UNCLEAN (F1, F2) | the `milan_dp` README, `MAILBOX_SPLIT.md`, `CI_WORKFLOWS.md`, the `rtl-fast` template, the `ctrl` README, the PR body | R799-1 | e69d243a61a8ec1c1ad8c473f809e1351dab1b61 |

## Real limits

- I have no copy of IEEE 802.1Q-2018, IEEE 1722.1-2021 or Milan v1.2 on this host. The Table 10-3 and 10-4 check is against lwSRP's independent transcription and the rulings' readings, not the printed standard.
- I did not run the census (sv2v pin), the em-dash and contents gates (renderer), `ctrl_boundary.py`'s pin controls (pinned LiteX tree), the full sweep, `test_builder.py`, the firmware self-test, or the 546 workflow `run:` steps. For those I rely on the author's receipts on `fe98f210` and the hosted jobs.
- I did not re-run the host AECP test and mutants locally. The hosted `firmware-unit` and `firmware-aecp-mutants` passed at this head.
- The CONTROLLER_AVAILABLE response check grades the stimulus's own answer, which echoes the command's id (`twin.hpp:350-351`), as the ruling asks. It does not prove the entity matches responses.
- The 4.4.1 check was not probed.
- Physical calibration NOT RUN. No hardware or field evidence is claimed. No manager source bank exists at this head, and I claim none.
- Probe hygiene: all builds and probes ran in clones under the packet's scratch. The review clone is unchanged: `HEAD` and tree as above, worktree and index clean, `git ls-files -s` equal to `git ls-tree -r HEAD` (same sha256), and all six gitlinks at the recorded commits. I fetched remote refs into it; no tracked bytes changed.

## Pending manager duties

- The hosted contexts still running at 21:59Z: 17 Verilator shards, `publication-census`, `docs-check` and `elaborate`. Hosted acceptance is the manager's.
- The current-dev merge candidate (live `dev` `0a75aa77`, source base `6584b7bf`), with its builder and native banks, at the merge turn. Base ordering: S6a (#853) merges first, then this PR retargets `dev-soft-core`.
- Carry R1 to the residue checklist.
- Re-review at the corrected head for F1 and F2 (`Conformance`, `Docs`). `RTL`, `Robustness` and `Tests` stay covered while no artifact in their scope changes.

R799-1 FINISHED
