# #665 S6b round 5, the two-placement simulation: [A746e] handoff

STATUS: REVIEW READY. Every item of issuecomment-6724570965 is implemented, and its three Done conditions hold at the head: `make twin` returns rc 0 with only ledger and owed rows; `make twin-plants` refuses every plant (19 plants, 38 of 38 controls); and every `run:` step of the dev-soft-core workflows passes on a clean clone of the head (546 ran, all rc 0; 86 not run, each with its reason), the boundary gate included. `make -j8 split` passes from a clean tree and its gate refuses the old rule. The full sweep passes as four shards (65 suites).

- Lane: `665-s6b-cosim`, worktree `<lane>`.
- Start: `2e8e790c` (round 4, [A746d]), stacked on `origin/665-s6-placement` `e6d27f3a` (S6a, PR #853). S6a did not move (checked at the start and before the replay).
- Head: `e69d243a61a8ec1c1ad8c473f809e1351dab1b61`, six commits on `2e8e790c`. Nothing pushed.
- Assignment: [A10] issuecomment-6724570965 (the four items), with -6722002738, -6717765106 and -6716584453 where not changed.
- TAKEN: issuecomment-6724671794 (its text is `TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6727379485 (head `e69d243a`; its text is `REVIEW-READY-COMMENT.md`).

## 1. What this round delivers

| Ruling item | State |
|---|---|
| (1) #860, the fabric's MSRP Domain | `OWED_GRADES` row `fabric-domain-one-new`, owed to #860: the fabric's Domain exactly `New x1 from ms 200, JoinMt x79 from ms 1000; received no MSRPDU, its Registrar MT throughout`. It covers only the fabric's Domain Table 10-3 findings while that holds. Plant `vanished-domain-new` (the fix: New twice, then JoinMt) and `domain-trace-moved` (defect kept, trace changed). The split's grade is unchanged. |
| (2) MVRP's Table 10-3 grade, per half | `twin_mrp.py` grades MVRP's attributes as it grades MSRP's, with MVRP's Registrar Table 10-4 as printed (Milan v1.2 4.2.7.2.2 is "for the MSRP application"). **The split's MVRP passes** (JoinMt from 12 ms: Join!, VO, VP, AA, QA). The fabric's VID 2 fails at 6200 ms and at the second VID 2 JoinIn in its 10201 ms LeaveAll frame; `OWED_GRADES` row `fabric-vid2-join-in`, owed to #860, asserts it exactly: `New x1 from ms 5200, JoinIn x15 from ms 6200, Lv x1 from ms 20000; received no MVRPDU, its Registrar MT throughout`. Plants `vanished-vid2-join-in` (the fix) and `vid2-registrar-in` (defect kept, Registrar no longer MT); split plants `mvrp-join-in` and `mvrp-received-join` for the grade. The Milan v1.2 4.3.2 and 4.4.1 checks stay beside the grade. |
| (3) S6a's `make split` race | `split: build-split` then `$(MAKE) --no-print-directory exec-split` (S6a's Makefile). Gate `split_parallel.py`: clones HEAD, submodules at their gitlinks, runs `make -j8 split`, rc 0 and the leg's `failures: 0`; `--selftest` plants the old rule in another clean tree and requires the missing-binary failure. |
| (4) `ctrl_app_aecp.c:106` | IEEE 1722.1-2021 Table 7-2. |

## 2. Context read

- Round 4's HANDOFF and STOP; the four [A10] rulings; #860.
- Milan v1.2 4.2.7.2.1, 4.2.7.2.2 ("For the MSRP application"), 4.2.7.3, 4.3.2, 4.4.1; IEEE 802.1Q-2018 Table 10-3, Table 10-4 (rLv!, rLA!, txLA! take IN to LV), 10.7.6.3 (sJ: JoinIn only with the Registrar IN), 10.7.9 (local copies).
- `protocol-processor/hdl/srp/KL_srp_vlan.sv` (the fabric's MVRP participant: events New, JoinIn and Lv only, no `p2p_i`), `KL_srp_top.sv:144` (`p2p_i`, MSRP's), `hdl/milan/KL_pp_shadow.sv:1289` (tied 1); `sw/firmware/ctrl/srp/srp_mbx.c:252-253` (both participants point_to_point true) and `:532` (MVRP declares with Join, never New).

## 3. Changes, file:line and reason

Commits on `2e8e790c`:
- `0661ac60`: the split rule and its gate.
- `7487832b`: `ctrl_app_aecp.c:106`.
- `a3031ee3`: the twin's code (MVRP grade, #860 rows, six plants, the plant lists).
- `1333f19b`: the docs.
- `c8459f24`: the gate's self-test plants the old rule under the real simulator (a first stand-in simulator slept, which `measure_test_evidence.py` counts as host-clock dependence: 4 > 3).
- `e69d243a`: the gate prints the lines it judged and the clean tree's commit.

**Item 3, the race.** `tb/verilator/milan_dp/Makefile:866-871`: `split: build-split` and the run in a sub-make, the pattern round 3 gave the twin targets (`twin:`, `twin-plants:`). This is S6a's file; the PR body says so. `exec-split` itself is unchanged, so `run-split` and the sweep's `sim_pool` path are as before.

**The gate.** `tb/verilator/milan_dp/split_parallel.py` (new, 147 lines): `clean_tree` (:60) clones HEAD, checks out the commit, takes each of `SUBMODULES` (:38, the four the hosted suite jobs fetch) from the checkout's own clone at its gitlink and resets its origin to `.gitmodules`' URL, and refuses a dirty clone. `run_split` (:83) is `make -C <tree>/tb/verilator/milan_dp -j8 split`; `passed` (:90) wants rc 0 and every `checks: N failures: 0` line with 0. `arm` (:96) prints the lines it judged; `selftest` (:112) plants `RACE` (`split: build-split exec-split`) for `RULE` in a second clean tree and wants rc != 0 with `Vmilan_dp_split: No such file or directory`. It names neither `sw/firmware/ctrl` nor `ctrl_build`, so the boundary gate needs no entry; it adds no make target, so the pin-control count stays 181.

**Item 4.** `sw/firmware/ctrl/app/ctrl_app_aecp.c:106`: "Table 7.1" -> "Table 7-2". The same miscitation is in `sw/firmware/ctrl/test/aecp_mutants.py:408` (round 3's commit `8a9a2e29` too); the ruling names only the C line, so it is reported, not changed.

**Item 2, MVRP's grade.** `tb/verilator/milan_dp/twin_mrp.py`:
- `TABLE_10_4` (:79) is Table 10-4 as printed; `REGISTRAR` (:91) gives MSRP the Milan cell (rLv! IN -> MT) and MVRP the table as printed.
- `APPLICATIONS` (:94), `Participant` (:107), `participant` (:116): the application, its Registrar and the port's `operPointToPointMAC` (`OPER_P2P` :101, TRUE in both halves for both participants).
- `frame_events` (:121): an MVRP frame's events, its LeaveAll covering type 1 (the VID). `label_of` (:129): `VID 0002`.
- `step`, `transmit`, `opportunity`, `settle`, `illegal` (:224, now naming the application), `advance`, `grade_attribute` take the participant; `observations` (:269) and `grade` (:302) take the application (default MSRP, so the MSRP comparison is unchanged); `declarations` (:316) reads the grade's application.
- `trace_shown` (:328): an attribute's message runs with their first millisecond, and the frames of its application received; what the #860 rows assert.
- `twin_grades.py:215` `grade_mvrp` keeps 4.3.2 and 4.4.1 and drops its own "VID 2 withdrawn before declared (10.7)" check, which Table 10-3 refuses too (a Lv from VO); `:234` `grade_applicant` grades both applications and reports `mvrp_leave_all_declarations` beside MSRP's.

**Items 1 and 2, the #860 rows.** `tb/verilator/milan_dp/twin_compare.py`:
- `:523` `DOMAIN_KEY`, `VID2_KEY`; `:526` `FABRIC_DOMAIN`; `:528` `FABRIC_VID2`; `:530` `ONE_NEW`.
- `:533` `applicant_findings` (a row covers only the all-fabric half's Table 10-3 findings of its attribute), `:539` `traced`.
- `:547` `OWED_GRADES`: `fabric-domain-one-new` (:554), `fabric-vid2-join-in` (:559), each with its clause, cause (`KL_srp_domain.sv`; `KL_srp_vlan.sv`) and owing step (#860). `apply_grade_rows` is unchanged: a row whose findings have gone is "the defect has gone"; a row whose trace differs is "does not hold" and covers nothing.
- `PLANT_WORDS`, `SELF_WORDS`, `PLANTED_PROTOCOL` (:69, :101, :114): the six new plants.

**Plants.** `tb/verilator/milan_dp/twin_plants.py`: `vid2_events` (:216, MVRP's vectors, 10.8.1.2/11.2.3.1), `vid2_frame` (:236, a peer's MVRPDU), `plant_mvrp_join_in` (:244), `plant_mvrp_received_join` (:255), `fabric_domain` (:294), `plant_vanished_domain_new` (:303), `plant_domain_trace_moved` (:312), `plant_vanished_vid2_join_in` (:321), `plant_vid2_registrar_in` (:336), `SPLIT_PLANTS` (:347), `FABRIC_PLANTS` (:355). `Makefile:953-956` the two lists; `:40` "nineteen plants".

**Docs.** `tb/verilator/milan_dp/README.md`: the split section (the rule and its gate, with the command); the contract list (issuecomment-6724570965); the grades list; "The MRP Applicant grade" (renamed from "The MSRP Applicant grade", its one in-page link updated; the contents block lists H2 only), with each application's Registrar; the owed-grade table (two #860 rows); the plants (nineteen; six new rows); "What it finds at this head" (rc 0; the split's Domain and VID 2; the fabric's two #860 traces). `docs/design/MAILBOX_SPLIT.md`: the twin bullet (MVRP graded, #860, nineteen plants, nothing beyond the rows), the split leg's paragraph (the rule and its gate), the open item.

## 4. New checks, planted defects and failing words

Each plant is refused twice: against the unplanted capture of the half it plants (every finding about the planted protocol; the words, `SELF_WORDS` where they differ), and between the placements (the words in a finding the unplanted comparison does not make).

| Plant | Half | Its grade or row | Planted | Refused between the placements by |
|---|---|---|---|---|
| `mvrp-join-in` | split | MVRP's Table 10-3 grade (10.7.6.3) | the split's second VID 2 message (212 ms), a JoinMt with its Registrar MT, re-encoded JoinIn | `[MRP] split MVRP VID 0002: JoinIn at ms 212 is not an Applicant's message: from AA, Table 10-3's tx! sends JoinMt` |
| `mvrp-received-join` | split | MVRP's grade, through a received MVRPDU and MVRP's Registrar | a peer's VID 2 JoinIn applied at 30500 ms | `[MRP] split MVRP VID 0002: JoinMt at ms 31012 is not an Applicant's message: from AA with the Registrar IN, QA with the Registrar IN, Table 10-3's tx! sends JoinIn or nothing` |
| `vanished-domain-new` | fabric | `fabric-domain-one-new` (#860), where the fix lands | the fabric's first Domain JoinMt (1000 ms) sent as a second New | `owed row fabric-domain-one-new: the defect has gone` |
| `domain-trace-moved` | fabric | `fabric-domain-one-new`'s exact trace | the fabric's first Domain JoinMt sent as JoinIn (still illegal) | `owed row fabric-domain-one-new does not hold: the all-fabric half sent MSRP Domain value 06030002: New x1 from ms 200, JoinIn x1 from ms 1000` |
| `vanished-vid2-join-in` | fabric | `fabric-vid2-join-in` (#860), where the fix lands | the fabric's first VID 2 JoinIn (6200 ms) sent as a second New, each later JoinIn as JoinMt | `owed row fabric-vid2-join-in: the defect has gone` |
| `vid2-registrar-in` | fabric | `fabric-vid2-join-in`'s exact trace (its Registrar MT) | a peer's VID 2 JoinIn applied to the fabric at 6000 ms | `owed row fabric-vid2-join-in does not hold: the all-fabric half sent MVRP VID 0002: New x1 from ms 5200, JoinIn x15 from ms 6200, Lv x1 from ms 20000; received 1 MVRPDU(s)` |

Against the unplanted capture: `vanished-domain-new` by `the planted half no longer makes: [MRP] all-fabric MSRP Domain value 06030002: JoinMt at ms 1000`; `domain-trace-moved` by `[MRP] all-fabric MSRP Domain value 06030002: JoinIn at ms 1000 is not an Applicant's message`; `vanished-vid2-join-in` by `the planted half no longer makes: [MRP] all-fabric MVRP VID 0002: JoinIn at ms 6200`; `vid2-registrar-in` by `[MRP] all-fabric MVRP VID 0002: JoinIn at ms 6200 is not an Applicant's message: from AN with the Registrar IN`; the split's two by their words above.

Round 4's thirteen plants are kept, with their words unchanged.

**The race gate's plant.** `split_parallel.py --selftest`: the old rule (`split: build-split exec-split`) planted in a clean tree; refused by `make -j8 split` rc 2 with `make: ./obj_split/Vmilan_dp_split: No such file or directory`. HEAD's rule passes with `checks: 71   failures: 0`.

## 5. Gate table

Receipts are under `receipts/` (index `receipts/INDEX.md`, generated from the files present). Each receipt's first line names its head. The head is `e69d243a`.

| Gate | Head | rc | Result | Receipt |
|---|---|---|---|---|
| `make -C tb/verilator/milan_dp -j8 twin` (clean clone, own unit) | `e69d243a` | 0 | `twin: 0 finding(s)`; 6 ledger and 6 owed notes (`OWED` 3, `OWED_GRADES` 3) hold | `twin/make-twin.txt`, `twin/*.json.txt` |
| `make -C tb/verilator/milan_dp -j8 twin-plants` (the same clone) | `e69d243a` | 0 | 19 plants, 38 of 38 controls REFUSED, none ESCAPED | `twin/make-twin-plants.txt` |
| the same two at `1333f19b` (the code commit's head; the captures byte-identical to the head's) | `1333f19b` | 0, 0 | 0 findings; 38 of 38 | `twin/superseded-1333f19b/` |
| `split_parallel.py --selftest` (the gate clones HEAD twice) | `e69d243a` | 0 | planted old rule: rc 2, `make: ./obj_split/Vmilan_dp_split: No such file or directory`; `make -j8 split` from a clean tree: rc 0, `checks: 71   failures: 0`; `split_parallel: PASS` | `gates/split-parallel.txt` |
| `make split-mutants` (-j8, clean clone) | `e69d243a` | 0 | 24 of 24 caught | `gates/make-split-mutants.txt` |
| `make split-cdc` | `e69d243a` | 0 | 13 checks, 0 failures | `gates/make-split-cdc.txt` |
| `make split` (no -j, the same clone) | `e69d243a` | 0 | 71 checks, 0 failures | `gates/make-split.txt` |
| `publication_census.py --check --jobs 4` (both populations) | `e69d243a` | 0 | 246 checks, 0 failures; worker peak 1,638,692 kB (round 4: 1,633,132) | `gates/census-check.txt` |
| `placement_identity.py --compare` (base `a9d69c77`, the head's tool, clean clones) | `e69d243a` | 0 | 6 shapes, every digest equal | `gates/identity-*.txt` |
| `check_py_idiom.py`, `measure_test_evidence.py --check`, `measure_naming.py --check`, `check_cpp_idiom.py`, `check_hygiene.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `check_sh_idiom.py` (local) | `e69d243a` | 0 each | every ratchet at or under budget (wall-clock suite files 3 <= 3) | (and the replay's) |
| `gen_toc.py --check`, `--verify-anchors`, `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `check_em_dash.py --base a9d69c77` (local, the pinned renderer in /tmp) | `e69d243a` | 0 each | em-dash: 0 findings over 691 added lines | (and the replay's) |
| `check_doc_style.py`'s analyzer on the two touched pages | `e69d243a` | n/a | Neither page is in its 23-page list, and the gate passes. Its 10-word limit flags each page throughout: 783 and 864 findings at `2e8e790c`; in this round's new text, 60 (README) and 12 (`MAILBOX_SPLIT.md`) | `docs/doc-style-touched.txt` |
| a first `split_parallel.py` at `c8459f24`, before it printed what it judged | `c8459f24` | 0 | PASS; superseded | `gates/superseded-split-parallel-c8459f24.txt` |

| `ctrl_boundary.py --require-rv32 --selftest` (whole, clean clone, own unit, the LiteX tree's venv) | `e69d243a` | 0 | `ctrl_boundary: PASS`: 0 findings; 117 boundary, 181 pin and 4 figure controls, 0 misbehaved | `firmware/ctrl_boundary.txt` |
| `test_builder.py --require-rv32` (clean clone, own unit, the LiteX tree's venv) | `e69d243a` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11's calibration arm, which needs an earlier board build's utilization report on disk (as in round 4) | `firmware/test_builder.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test` (whole, clean clone, own unit) | `e69d243a` | 0 | `test_ctrl_firmware: PASS` | `firmware/test_ctrl_firmware.txt` |
| FULL sweep, 4 shards (`run_all_suites.sh --shard k/4`; own clones, MemoryMax 10G, -j4, pinned Verilator 5.050) | `e69d243a` | 0 x4 | 65 suites passed, 0 failed, 0 timed out (15, 17, 17, 16); 2,192,899 checks, 0 in-suite failures | `sweep/shard-*.txt`, `sweep/native-spec.json` |
| CI replay: every `run:` step of docs.yml, elaborate.yml, rtl-fast.yml, rtl.yml (69 job instances, each on its own clean clone) | `e69d243a` | 0 each | 546 steps ran, 0 failed; 68 jobs success, `physical-gptp` skipped (its `if:` is false for this event). 86 steps not run, each with its reason | `ci/ci-replay-table.md`, `ci/ci-jobs.json`, `ci/ci-not-run.json`, `not_run.json` |
| ... `firmware-boundary` (`ctrl_boundary.py --without verilator`) and `firmware-verilator` (`--only verilator`) | `e69d243a` | 0, 0 | `ctrl_boundary: PASS` in both: 0 findings; 112 and 6 boundary, 181 pin and 4 figure controls, 0 misbehaved | same |
| ... `verilator-suites` (19 workers: the whole sweep) | `e69d243a` | 0 | every worker succeeded; 2,192,902 checks, 0 in-suite failures; every case union succeeded | same |
| ... `yosys-portability` (4 shards) | `e69d243a` | 0 | expected 62, observed 62, errors 0 | same |
| ... `bdd-conformance` (`cd tests && behave`) | `e69d243a` | 0 | 508 scenarios passed, 0 failed, 0 skipped | same |
| ... `verilator-lint` | `e69d243a` | 0 | LINT GATE: PASS (89 <= 89) | same |
| ... `publication-census` (`--check --selftest`) | `e69d243a` | 0 | RESULT: PASS, 246 checks; selftest 0 of 163 arms failed | same |
| ... `test_ctrl_firmware.py --require-rv32 --self-test`, shards 0 to 3 of 4 (`firmware-unit` and the three campaign jobs) | `e69d243a` | 0 x4 | `test_ctrl_firmware: PASS` in each | same |
| ... `split-cdc`, `yosys-elaboration`, `test_ctrl_nvm`, `fw_coverage` | `e69d243a` | 0 each | `split-cdc`: 13 checks, 0 failures | same |
| ... the four builder runs (`test_builder.py --require-rv32`: the docs and elaborate workflows' legs 0 and 1) | `e69d243a` | 0 each | ALL GATES PASS EXCEPT 1 NOT RUN in three; EXCEPT 16 NOT RUN in the docs leg 1 (its LiteX arms: the job's interpreter has no LiteX; the standalone run above covers them), as in round 4 | same |
| ... the docs gates (`docs_check.py` with and without git, `check_py_idiom.py`, `measure_naming.py`, `check_doc_style.py`, `check_em_dash.py`, `gen_toc.py`, `measure_test_evidence.py`, ...) | `e69d243a` | 0 each | | same |
| ... `verilator-shards` 12, first attempt | `e69d243a` | 2 | `scripts/test_suite_cancellation.py`'s hard-KILL arm: `CLEANUP FAILED: owned descendants remain`, before any suite ran, on a fully booked host. The suite runner's own cancellation control; this round changes nothing under `scripts/`, and round 4 passed it. Moved aside (`ci_replay.py again`, kept under `attempts/`) and run again: success | `ci/attempt1-rtl-verilator-shards-12.txt` |

The replay ran the hosted steps natively with round 4's tool (`tools/ci_replay.py`, overrides `tools/overrides.json`, unchanged but for this round's paths), with round 4's differences from a hosted runner, recorded per step in the table: the scope steps take their replay branch against `origin/dev-soft-core`; apt lines are no-ops; the RV32 SDK installs from a local copy of its pinned archive; the venvs are CPython 3.12.3 with `pidfd_shim.py`; `third_party/tsn-c-stack` keeps its declared origin. Jobs ran as three `local` workers on this round's own 8 CPUs and, whenever a range freed, as units of their own (`tick`).

**The sweep.** All 128 CPUs were booked for most of the round, and four free ranges never coexisted, so `native-shards.py` (which launches all four at once) could not start. `tools/sweep-shard.py` launches one shard exactly as `native-shards.py` launches each (its own `--shared` clone, the spec's suite command with `--shard k/4`, `run-recorded-gates.py`, MemoryMax 10G, -j4), and `tools/sweep-watch.py` started each on the next free 8-CPU range with MemAvailable over 30 GB: 96-103, 32-39, 0-7 and 64-71.

**Memory.** This round's own unit stayed near 2.6 GB. Every gate, replay worker and shard ran as its own unit with MemoryMax 10G; the highest anonymous and shared memory seen in one was 4.7 GB (a replay worker during the firmware jobs).

## 6. Open risks and questions

- **`split_parallel.py` is a local gate.** No hosted job runs `make -j8 split`. The suites build each case in a sub-make and run it through `sim_pool.py`, and `run-split` builds before it runs, so the race never reached them. Wiring the gate into a hosted job (it needs Verilator) would touch the generated workflows and their contract; that is left for a ruling.
- **`sw/firmware/ctrl/test/aecp_mutants.py:408`** cites "IEEE 1722.1-2021 Table 7.1" for the same field, in a comment from round 3's commit `8a9a2e29`. The ruling names only `ctrl_app_aecp.c:106`, so the mutant's comment is unchanged.
- **The fabric's LeaveAll MVRPDU at 10201 ms carries VID 2 twice** (two vectors, JoinIn each). The grade reads the first as the attribute's txLA! and the second as a tx! of its own, which Table 10-3 refuses with the Registrar not IN. Both VID 2 findings are #860's (JoinIn with the Registrar MT), and the #860 row asserts the whole trace.
- `make twin`'s other notes are unchanged from round 4: VID 2's 4.3.2 and 4.4.1 checks hold vacuously in this stimulus (no stream frame, no settled sink).
