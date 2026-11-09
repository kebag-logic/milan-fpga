# #665 S6b round 6, the two-placement simulation: [A746f] handoff

STATUS: REVIEW READY. The four items of issuecomment-6727748772 are implemented, and its three Done conditions hold at the head: `make twin` returns rc 0 with only ledger, owed and tail notes; `make twin-plants` refuses every plant (20 plants, 40 of 40 controls), the new `leave-all-omission` included; and every `run:` step of the dev-soft-core workflows passes on a clean clone of the head (546 ran, all rc 0; 86 not run, each with its reason), the boundary gate included. Both reviews' comment-rule scans find nothing. The full sweep passes as four shards (65 suites).

- Lane: `665-s6b-cosim`, worktree `<lane>`.
- Start: `e69d243a` (round 5, [A746e]), stacked on `origin/665-s6-placement` `e6d27f3a` (S6a, PR #853). S6a did not move (checked at the start and before the gates).
- Head: `a88772f1cf0c3c3b269294bd4ceaf436646ca5a1`, five commits on `e69d243a`. Nothing pushed.
- Assignment: [A10] issuecomment-6727748772 (the four items), with -6724570965, -6722002738, -6717765106 and -6716584453 where not changed.
- TAKEN: issuecomment-6727812882 (its text is `TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6729655350 (head `a88772f1`; its text is `REVIEW-READY-COMMENT.md`).
- Output directory: this round wrote only here (`665s6b-a746f`). The assignment's last line names `665s6b-a746e` as the output directory. That is round 5's directory, holding the handoff this round was told to read, so nothing was written there.

## 1. What this round delivers

| Ruling item | State |
|---|---|
| (1) No lane labels or comment IDs in source | Every line either review lists is rewritten: 43 lines in 18 files (R799-1's list), which hold R800-1's 42. Each issue-comment ID, ruling ID and lane label is gone. In its place, the issue (#665, #857, #858, #860), the clause, or what the line does. R800-1's `comment_rule_scan.sh`, run unchanged, prints nothing at the head. R799-1 published its list, not a script. `tools/r799_scan.sh` (R800-1's scan, with `issuecomment-` matched with or without digits after it) reproduces that list exactly at `e69d243a` and prints nothing at the head. |
| (2) Table 7-2 | `test_aecp.cpp:437` and `aecp_mutants.py:408` cite IEEE 1722.1-2021 Table 7-2. `git grep "Table 7\.1" -- sw/firmware/ctrl` prints nothing. The PR body no longer lists the mutant's citation as left. |
| (3) The split-cdc plant count | `docs/testing/CI_WORKFLOWS.md:437-442` and `.github/ci-templates/rtl-fast.yml:321-324` state the twelve plants `split_cdc_check.py` `PLANTS` holds, grouped as the leg's README groups them. No gate derives the count from the leg (`ci_events.py --check` reads neither line), so it is stated as the README states it. The generated `.github/workflows/rtl-fast.yml` drops template comments; `ci_gate_workflows.py --check` passes. |
| (4) A LeaveAll omission plant | `leave-all-omission`: the split's first MSRP LeaveAll frame after 20 s that carries the declared Domain, sent without the Domain's vector (its LeaveAll kept). Refused in both controls by `[MRP] split MSRP Domain value 06030002: nothing at ms 27910 (a LeaveAll) is not an Applicant's message: from AA, QA, Table 10-3's txLA! sends JoinMt or Mt`. It catches both grade mutants R799-1 found surviving every earlier plant (`txla-qa-bracketed`, `txla-aa-sends-nothing`). |

No grade, ledger row or owed row changes. `make twin`: rc 0, 0 findings, 6 ledger and 6 owed notes and one tail note. `make twin-plants`: 20 plants, 40 of 40 controls refused.

## 2. Changes, file:line and reason

Commits on `e69d243a`:
- `5bcf5278`: item 3 (and the comment ID on those two pages' lines).
- `d19f7154`: item 2 (and the comment ID on `test_aecp.cpp:439`).
- `8a46e42d`: item 1.
- `f73715e1`: item 4, the plant.
- `a88772f1`: item 4, its docs.

**Item 1.** Each line, what it cited, and what it says now:
- `tb/verilator/milan_dp/Makefile:867-868` (the `split` rule): `issuecomment-6724570965, item 3` -> `#665`. `:882-883` (the twin's header): `issuecomment-6715535566 item 1, and issuecomment-6716584453` -> "the host-compiled firmware on the RTL mailbox", the method that ruling item named.
- `split_parallel.py:7` -> `#665`; `:39` -> "the run beside the link it needs", what the race is.
- `tb_split_top.sv:61`: `#665 S6b` -> `#665`.
- `twin.hpp:14` -> `#665`. `:23-25`: `issuecomment-6717765106, item 6` -> "a row no stimulus reaches is unproven" (that item's reason), and `issuecomment-6722002738, item 6` -> `#858`. `:68-69` -> `#665`, "so MAAP's frames compare as raw bytes". `:253-254`: "the plan's S6" -> `#665` (a lane label neither list names, the same rule). `:280` -> `#858`.
- `twin_fabric.cpp:17-18`: `issuecomment-` broken over two lines -> `#665`.
- `twin_fw.py:18` -> `#665`, "so MAAP's frames compare as raw bytes".
- `twin_decode.py:189-190` -> `#665`, with that item's reason: Milan v1.2 5.4.5.2 and Table 5.22 send each notice on its own state change and order no two triggers.
- `twin_grades.py:7` -> `#665`; `:16-17` -> IEEE 1722.1-2021 9.2.2.9's own words, "not whether per entity or per controller"; `:22` -> Milan v1.2 4.2.7.2.2 for MSRP's Registrar.
- `twin_mrp.py:6-7` -> `#665`.
- `twin_plants.py:17` -> `#665`; `:24` -> `(OWED_GRADES)`.
- `twin_compare.py:7` (the docstring: "the plan's section S6 as #665 issuecomment-... amend it") -> "#665's two-placement comparison contract". `:191`, `:251`, `:369`, `:371-372`, `:465`, `:545-546` -> `#665`, `#857, #860`, or the reason ("a row no stimulus reaches is unproven").
- **Printed strings** (the `[OWED]` notes' "owed to" field, which both reviews list; R800-1 lists them as runtime strings): `:461` `SRP_ROUND` -> "the SRP adapter entry that takes MAAP's allocation (#665)", `:491` -> "#858 (a release-image defect)", `:531` `ONE_NEW` -> "#860 (a release-image defect)", `:553` -> "#857 (a release-image defect)". These are R799-1 R1's own example fixes. Each row's name, predicates, asserted values and cause are unchanged; no plant's words read the field.
- `scripts/ci_events.py:1344-1345` -> `#665`, "on its own runner so it lengthens no existing job" (the ruling's reason); `:2494` -> `#665`.
- `sw/mailbox/census_plants.py:537`, `publication_census.py:117`, `census_split.py:11` -> `#665`. `census_split.py:66-69`: "(ruling 6715535566 item 3) ... The carrier is S11's" -> `#665`, "The REBOOT carrier is not built yet; until it is, the hold is documented here."
- `sw/firmware/ctrl/app/ctrl_app_aecp.c:108`, `test/test_aecp.cpp:439` -> `#665`.
- `.github/ci-templates/rtl-fast.yml:318`, `docs/testing/CI_WORKFLOWS.md:431-432` -> `#665`.

The design pages (`MAILBOX_SPLIT.md`, the `milan_dp` README) keep their linked comment IDs: the owner rule names source comments, and the ruling names the reviewers' source lines. The README's owed table keeps "the SRP adapter round after S2b" in its Owed-to column: docs may name lanes.

**Item 2.** `sw/firmware/ctrl/test/test_aecp.cpp:437`, `sw/firmware/ctrl/test/aecp_mutants.py:408`: "Table 7.1" -> "Table 7-2". R800-1's wider grep (`-- sw/firmware/ctrl tb/verilator/milan_dp`) still prints one line, `tb/verilator/milan_dp/README.md:620`, "Table 7.159" (IEEE 1722.1-2021 7.4.42.2.5): present at `e6d27f3a` and on `dev-soft-core`, outside this PR's delta, and another table.

**Item 3.** `docs/testing/CI_WORKFLOWS.md:437-442`: twelve plants, each refused by its own words: four raw crossings (a publication, the LINK level, the settings read, a window answer); five wrong takes of the held bus (every cycle, on the commit level, on the request pulse, while the pulse is low, by another flop); a reset from the other domain on each side; a primitive clocked by a level. That is `split_cdc_check.py:258-303` `PLANTS` as the leg's README (`tb/verilator/milan_dp/README.md:1172-1176`) states it. `.github/ci-templates/rtl-fast.yml:321-324`: the same, shorter.

**Item 4.** `tb/verilator/milan_dp/twin_plants.py:201-225` `plant_leave_all_omission`: the first split MSRP frame at or after 20000 ms whose LeaveAll covers the Domain type (4) and that carries the Domain value in a vector of its own (one value, no LeaveAll bits in that vector's header). It removes that vector (VectorHeader, the four-octet value, one ThreePackedEvents octet: 7 octets) and shortens the Message's AttributeListLength by as much. It refuses (`SystemExit`) when no such frame exists. `:378` `SPLIT_PLANTS`; `:19-20` the docstring's plant list.
- `twin_compare.py:86-87` `PLANT_WORDS["leave-all-omission"]`; `:118-119` `PLANTED_PROTOCOL` MSRP. The self control uses the same words (no `SELF_WORDS` entry).
- `Makefile:953` `TWIN_CAPTURE_PLANTS`; `:40` "twenty plants"; `:948-949` the plants comment.
- `README.md:1322-1325` (the grade's rule for an attribute a LeaveAll frame leaves out, and the plant that holds it), `:1407` "twenty plants", `:1433` the plant's row, `:110` the contents line; `MAILBOX_SPLIT.md:1544` "twenty plants".

## 3. New checks, planted defects and failing words

| Plant | Half | Its grade | Planted | Refused by (both controls) |
|---|---|---|---|---|
| `leave-all-omission` | split | MSRP's Table 10-3 grade, txLA! (IEEE 802.1Q-2018 10.7.6.6, 10.7.9) | the split's MSRP LeaveAll frame at 27910 ms sent without the Domain's vector, its LeaveAll kept | `[MRP] split MSRP Domain value 06030002: nothing at ms 27910 (a LeaveAll) is not an Applicant's message: from AA, QA, Table 10-3's txLA! sends JoinMt or Mt` |

Against the unplanted split capture the control also finds `JoinMt at ms 28110 is not an Applicant's message: from LO` (the next frame) and the LeaveAll declarations' difference; every finding names MSRP, as the control requires.

The grade mutants (`tools/probe_omission_mutants.py`, R799-1's two edits of `twin_mrp.py` `TXLA`): `txla-qa-bracketed` (QA's txLA! bracketed) and `txla-aa-sends-nothing` (AA's txLA! may send nothing) each make the new plant ESCAPE in both controls, so each is CAUGHT. The head refuses it in both.

Round 5's nineteen plants keep their words.

## 4. Gate table

Receipts are under `receipts/` (index `receipts/INDEX.md`, generated from the files present). Each receipt's first line names its head. The head is `a88772f1`.

| Gate | Head | rc | Result | Receipt |
|---|---|---|---|---|
| R800-1's `comment_rule_scan.sh <lane> e6d27f3a <head>`, unchanged (sha256 as its MANIFEST) | `a88772f1` | 0 | no line printed | `scans/r800-comment-rule-scan.txt` |
| R799-1's list, re-derived (`tools/r799_scan.sh`; reproduces its 43 lines exactly at `e69d243a`) | `a88772f1` | 0 | no line printed | `scans/r799-list-scan.txt`, `scans/r799-list-at-e69d243a.txt` |
| the reviews' `git grep "Table 7\.1"` verifications | `a88772f1` | 1, 0 | `-- sw/firmware/ctrl`: nothing. `-- sw/firmware/ctrl tb/verilator/milan_dp`: the one pre-existing "Table 7.159" line, outside the delta | `scans/table-7-2.txt` |
| `make -C tb/verilator/milan_dp -j8 twin` (clean clone, own unit) | `a88772f1` | 0 | `twin: 0 finding(s)`; 6 `[LEDGER]`, 6 `[OWED]` and 1 `[TAIL]` notes; captures byte-identical to round 5's (`fabric.json` `fa6a5a12`, `split.json` `ee143865`) | `twin/make-twin.txt`, `twin/report.json.txt`, `twin/captures-sha256.txt` |
| `make -C tb/verilator/milan_dp -j8 twin-plants` (the same clone) | `a88772f1` | 0 | 20 plants, 40 lines `REFUSED`, 0 `ESCAPED`; the three as-run plants (`byte-flip`, `srp-plus-k`, `missing-notification`) among them | `twin/make-twin-plants.txt` |
| `tools/probe_omission_mutants.py` (the new plant against R799-1's two surviving grade mutants) | `a88772f1` | 0 | head refuses it in both controls; `txla-qa-bracketed` and `txla-aa-sends-nothing` each CAUGHT | `twin/probe-omission-mutants.txt` |
| `split_parallel.py --selftest` (the gate clones HEAD twice) | `a88772f1` | 0 | planted old rule: rc 2, `Vmilan_dp_split: No such file or directory`; `make -j8 split` from a clean tree: rc 0, `checks: 71   failures: 0`; `split_parallel: PASS` | `gates/split-parallel.txt` |
| `make split-mutants` (-j8, clean clone) | `a88772f1` | 0 | 24 of 24 caught | `gates/make-split-mutants.txt` |
| `make split-cdc` | `a88772f1` | 0 | 13 checks, 0 failures | `gates/make-split-cdc.txt` |
| `make split` | `a88772f1` | 0 | 71 checks, 0 failures | `gates/make-split.txt` |
| `publication_census.py --check --jobs 4` (both populations: the split census and the all-fabric census) | `a88772f1` | 0 | 6 shapes, 246 checks, 0 failures, `RESULT: PASS`; worker peak 1,636,916 kB (round 5: 1,638,692) | `gates/census-check.txt` |
| `placement_identity.py --compare` (base `a9d69c77`, the head's tool, clean clones) | `a88772f1` | 0 | 6 shapes, every digest equal | `gates/identity-*.txt` |
| `test_builder.py --require-rv32` (clean clone, own unit, the LiteX tree's venv) | `a88772f1` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11's calibration arm, which needs an earlier board build's utilization report on disk (as in rounds 4 and 5) | `firmware/test_builder.txt` |
| `ctrl_boundary.py --require-rv32 --selftest` (whole, clean clone, own unit, the LiteX tree's venv) | `a88772f1` | 0 | `ctrl_boundary: PASS`: 0 findings; 117 boundary, 181 pin and 4 figure controls, 0 misbehaved | `firmware/ctrl_boundary.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test` (whole, clean clone, own unit) | `a88772f1` | 0 | `test_ctrl_firmware: PASS` | `firmware/test_ctrl_firmware.txt` |
| FULL sweep, 4 shards (`run_all_suites.sh --shard k/4`; own clones, MemoryMax 10G, -j4, pinned Verilator 5.050) | `a88772f1` | 0 x4 | 65 suites passed, 0 failed, 0 timed out (15, 17, 17, 16); 2,192,899 checks, 0 in-suite failures | `sweep/shard-*.txt`, `sweep/native-spec.json` |
| `gen_toc.py --check`, `--verify-anchors`, `check_em_dash.py --base a9d69c77`, `docs_check.py`, `check_doc_paths.py` (local, the pinned renderer in /tmp), `check_py_idiom.py`, `measure_naming.py --check`, `ci_events.py --check`, `ci_gate_workflows.py --check` (local) | `a88772f1` | 0 each | em-dash: 0 findings over 701 added lines; ci_events: 2271 contract items | (and the replay's) |
| `check_doc_style.py`, and its `analyze()` on the three touched pages | `a88772f1` | 0 | the gate: `documentation style: OK (23 current documents)`; none of the three pages is in its list. Its 10-word limit flags each page throughout (1235, 812 and 865 findings at `e69d243a`); in the paragraphs this round changed: 8 (`CI_WORKFLOWS.md`), 28 (README), 24 (`MAILBOX_SPLIT.md`) | `docs/doc-style-touched.txt` |
| CI replay: every `run:` step of docs.yml, elaborate.yml, rtl-fast.yml, rtl.yml (69 job instances, each on its own clean clone) | `a88772f1` | 0 each | 546 steps ran, 0 failed; 68 jobs success, `physical-gptp` skipped (its `if:` is false for this event). 86 steps not run, each with its reason | `ci/ci-replay-table.md`, `ci/ci-jobs.json`, `ci/ci-not-run.json`, `not_run.json` |
| ... `firmware-boundary` (`ctrl_boundary.py --without verilator`) and `firmware-verilator` (`--only verilator`) | `a88772f1` | 0, 0 | `ctrl_boundary: PASS` in both: 0 findings; 112 and 6 boundary, 181 pin and 4 figure controls, 0 misbehaved | same |
| ... `verilator-suites` (19 workers: the whole sweep) | `a88772f1` | 0 | every worker succeeded; 2,192,902 checks, 0 in-suite failures; every case union succeeded | same |
| ... `yosys-portability` (4 shards) | `a88772f1` | 0 | expected 62, observed 62, errors 0 | same |
| ... `bdd-conformance` (`cd tests && behave`) | `a88772f1` | 0 | 508 scenarios passed, 0 failed, 0 skipped | same |
| ... `verilator-lint` | `a88772f1` | 0 | LINT GATE: PASS (89 <= 89) | same |
| ... `publication-census` (`--check --selftest`) | `a88772f1` | 0 | RESULT: PASS, 246 checks; selftest 0 of 163 arms failed | same |
| ... `firmware-unit`, `firmware-aecp-mutants`, `firmware-srp-mutants`, `firmware-control-mutants` (`test_ctrl_firmware.py --require-rv32 --self-test`, shards 0 to 3 of 4) | `a88772f1` | 0 x4 | `test_ctrl_firmware: PASS` in each | same |
| ... `split-cdc`, `yosys-elaboration`, `test_ctrl_nvm`, `fw_coverage` | `a88772f1` | 0 each | `split-cdc`: 13 checks, 0 failures | same |
| ... the four builder runs (docs leg 1 and 2, elaborate legs 0 and 1) | `a88772f1` | 0 each | ALL GATES PASS EXCEPT 1 NOT RUN in three; EXCEPT 16 NOT RUN in docs leg 2 (its LiteX arms: the job's interpreter has no LiteX; the standalone run above covers them), as in round 5 | same |
| ... the docs gates (`check_doc_style.py` "Concise audience documentation gate", `check_py_idiom.py`, `measure_naming.py`, `check_em_dash.py`, the per-page contents gate, `measure_test_evidence.py`, `docs_check.py` with and without git, ...) | `a88772f1` | 0 each | | same |
| ... `union-capture_coherence`, first attempt | `a88772f1` | 1 | the replay tool's own clone check, before any step ran: its tick driver and a local worker started the same instance in the same second, and each removed the other's clone. Moved aside (`ci_replay.py again`, kept under `attempts/`), claimed, and run alone: success. No other instance ran twice | `ci/race-capture_coherence-local.txt`, `ci/again-capture_coherence.txt` |
| FULL sweep, first launch | `a88772f1` | 1 x4 | each shard failed in the suite runner's preflight (`check_list_hermetic`: `mktemp` could not create a directory under its TMPDIR), because this round's scratch had no `tmp-sweep` directory. Moved aside unrun; relaunched once it existed (the row above) | (scratch only) |

The replay ran the hosted steps natively with round 5's tool (`tools/ci_replay.py`, overrides `tools/overrides.json`, unchanged but for this round's paths), with round 5's differences from a hosted runner, recorded per step in the table: the scope steps take their replay branch against `origin/dev-soft-core`; apt lines are no-ops; the RV32 SDK installs from a local copy of its pinned archive; the venvs are CPython 3.12.3 with `pidfd_shim.py`; `third_party/tsn-c-stack` keeps its declared origin. Jobs ran as two `local` workers on this round's own 8 CPUs and, whenever a range freed, as units of their own (`tick`).

**The sweep.** `tools/sweep-watch.py` started each shard (`tools/sweep-shard.py`, which launches one exactly as `native-shards.py` launches each) on the next free 8-CPU range with MemAvailable over 30 GB: 56-63, 80-87, 40-47 and 32-39.

**Memory.** Every gate, replay worker and shard ran as its own unit with MemoryMax 10G. MemAvailable stayed above 45 GB.

## 5. Open risks and questions

- `split_parallel.py` is still a local gate (no hosted job runs `make -j8 split`), as round 5 reported.
- The printed "owed to" text of four `[OWED]` notes changed (section 2). A lane that greps the old text will not find it; none in the tree does.
