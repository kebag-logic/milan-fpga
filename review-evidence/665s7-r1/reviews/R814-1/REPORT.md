[R814] NEGATIVE - exact head 5fb6904ffe12effc4bde6bf5313faea7a3beebdc

# R814-1: external review of PR #874 (issue #867, Mark II split S7)

- Head `5fb6904ffe12effc4bde6bf5313faea7a3beebdc`, tree `7903e4d6821ca7fbd0e80a5d86220f18daf615f8`. Ten commits on `dev-soft-core` `1d6bf555`.
- Review clone: detached at the head. The worktree and index match HEAD, `git write-tree` = `7903e4d6`, and all six gitlinks equal the head's (`receipts/review_clone_state.txt`).
- Authority used:
  - the issue #867 body (acceptance 1 to 7);
  - the ruling on the executor's STOP (#867 issuecomment-6760813135);
  - the #665 rulings the PR cites (issuecomment-6495692075, issuecomment-6505997821), and the later one that supersedes the first for SRP/MRP (issuecomment-6681686082, item 3);
  - IEEE 802.1Q-2018 10.7.4, 10.7.11, Tables 10-3, 10-4 and 10-7, 10.8.1 and 10.8.2;
  - `docs/reference/FR_NFR.md` 3.4.1.
- The PR carries no prior public review findings: its only comments are the two review-start notices. So nothing is inherited to resolve.

**Verdict: NEGATIVE.** Two MINOR findings (F-1, F-2) leave Conformance, Tests and Docs unclean. RTL and Robustness are clean. Everything else asked for checks out:
- the MRPDU form at the wire;
- the source address from reset;
- LeaveAll spacing on both sides;
- the full TX ring;
- the licence at the policer;
- every plant and mutant, refused by its own words;
- the fixture's confinement;
- no change to RTL, firmware or lwSRP.

## Findings

### F-1 MINOR: the egress grade applies 18 ms, a superseded allowance, not the approved 20 ms

Lenses: **Conformance, Tests, Docs**.

**Where:**
- `tb/verilator/milan_dp/srptx_grade.py:18-20`, `:59-64` (`SVC_MS = min(20, 18)`), `:72-74`, `:522`;
- `tb/verilator/milan_dp/srptx_plants.py:42-43` (`join-late-in-t-svc`);
- `tb/verilator/milan_dp/README.md:1554`, `:1603`, `:1625`;
- `sw/firmware/ctrl/srp/README.md:384`;
- the PR body's item 3 row ("the owner's per-family rule").

**Authority and evidence:**
- Acceptance item 3 bounds the spacing by "the approved service allowance (T_svc 20 ms)".
- The SRP/MRP figure of min(T_svc, ceiling) = 18 ms comes from the 2026-10-29 decision (#665 issuecomment-6495692075).
- That figure was superseded by the maintainer's decision of 2026-11-06 (#665 issuecomment-6681686082, item 3): "The SRP/MRP bound is relaxed to T_svc = 20 ms. It was min(T_svc, 10 % ceiling) = 18 ms; the 2026-10-29 per-family figure for SRP is superseded."
- The grader, its docstring, both READMEs and the PR body still present 18 ms as the approved rule and cite the 2026-10-29 comment.
- The plant `join-late-in-t-svc` is written to *refuse* a 219 ms Join follow-up, which its own description says is "inside JoinTime + T_svc". It turns the superseded figure into a pass/fail boundary.

**Impact:**
- Every `[TIME]` bound and the `[608]` stop window is 2 ms tighter than the frozen acceptance allows: 218 instead of 220 ms, a 282 instead of 280 ms rate window, 9,782 to 15,218 instead of 9,780 to 15,220 ms, and +18 instead of +20 ms.
- A device whose egress falls in the 18 to 20 ms band meets item 3 but fails `make srptx`.
- The documentation tells a later reader that a superseded figure is the owner's rule.
- No measurement at this head lies in that band, so no result here changes. The defect is in the check's bound and its stated authority.

**Required outcome:** one of the following.
- Grade at the approved allowance (20 ms), citing acceptance item 3 and issuecomment-6681686082 item 3. Re-derive the plant at the new bound, and restate the grader docstring, both READMEs and the PR body.
- Or record a public ruling that 18 ms is intended for this check, and cite that ruling instead.

**Verification:**
- `grep -n SVC_MS srptx_grade.py`.
- `make srptx`, `srptx-plants` and `srptx-mutants` all rc 0.
- A capture with a 221 ms Join follow-up is refused, and one with 219 ms is not.

### F-2 MINOR: `[TIME]` holds JoinTime spacing only on the late side; a short Join timer passes

Lenses: **Tests, Conformance**.

**Where:**
- `tb/verilator/milan_dp/srptx_grade.py:313-364` (`grade_time`): only `JOIN_FOLLOW_MS` (lateness) and the 4-in-`RATE_WINDOW_MS` rate rule;
- `:402`: the JoinTime interval error is computed in `measure_time` but never graded;
- `README.md:1554`.

**Authority:**
- Acceptance item 3: JoinTime spacing at egress within 10.7.4 and Table 10-7, plus the allowance.
- IEEE 802.1Q-2018 10.7.4.1: jointimer controls the interval between transmit opportunities, and its value comes from 10.7.11 and Table 10-7.
- Milan v1.2 Table 4.3: JoinTime 200 ms (`FR_NFR.md` 3.4.1 row: 180 to 240 ms).
- LeaveAll is graded on both sides (9,782 to 15,218 ms). JoinTime is graded only from above.

**Evidence:** reviewer code arms, each planted in a copy of the adapter or of lwSRP and built and run through the author's own `srptx_mutants.build()` and `run()` (`probes/code_probe.py`, `receipts/logs/p1-code-probe.log`, `receipts/join_lower_side.txt`):

| Arm | What changes at egress | Measured JoinTime interval error | Findings |
|---|---|---|---|
| JoinTime 10 cs | MSRP New at 1, 100, 200 ms | about -100 ms | 0 |
| JoinTime 15 cs | | | 0 |
| JoinTime 17 cs | MSRP New at 1, 170, 340 ms | about -30 ms | 0 |
| lwSRP's Join-timer pacing removed | three MSRP frames in ms 1 | | 0 |
| JoinTime 30 cs (control: the late side works) | | | 7, `[TIME]` |

- The rate rule is never approached by a real capture. In my independent check of the wire run, the shortest span of four consecutive frames is 600 ms (`receipts/indep_check.txt`).
- The rate rule has a capture plant but no code mutant that it kills.

**Impact:**
- A Join timer shortened outside Table 10-7 / Milan Table 4.3 passes `make srptx`, even though the grade's own measurement shows a JoinTime interval error far outside the allowance.
- Item 3 is held only for late egress.
- At this head the measured error is -1.01 to +0.02 ms, so the shipped behaviour is right. The gap is in the check.

**Required outcome:** one of the following.
- Grade each timer-driven Join interval on its low side as well (at least JoinTime less the allowance, or Milan's 180 ms). Add a code mutant (a short Join timer) that only this grade refuses. Give the rate rule a stimulus or mutant that exercises it.
- Or publish the point-to-point reading that egress before JoinTime is bounded only by the rate rule, obtain a ruling on #867, and state that limit in the README and the PR.

**Verification:** `code_probe.py` arms `join-10cs`, `join-15cs` and `join-17cs` are refused, and `make srptx` / `srptx-mutants` stay rc 0.

### Suggestions (do not affect coverage)

- **S-1 (Tests).** Timer events in the capture carry a heap pointer as their `id` (`srptx.hpp:481`).
  - Two runs of one binary differ only there (`receipts/capture_determinism.txt`), so the published capture hashes cannot be reproduced byte for byte.
  - My three graded reports equal the author's published reports field by field (`receipts/capture_hashes.txt`).
  - An index instead of the pointer would make the captures reproducible.
- **S-2 (Tests, Docs).** The `[608]`/`[LIC]` finding text always appends the fixture note, even for a capture recorded with `"fixture": false`. My fixture-off probe printed it (`receipts/logs/p2-nofix-run.log`). Make the suffix conditional on `doc["fixture"]`, or refuse a licence capture recorded without the fixture.
- **S-3 (Robustness).** Item 2 is held from power-on reset only. A datapath or link reset during the run (the #839 class after a later reset) is not exercised. That is worth a scenario when S2b's adapter lands.

## What was checked, per question

1. **Item 1, MRPDU form.**
   - `walk()` and `grade_wire()` check ProtocolVersion, AttributeType and AttributeLength, the MSRP AttributeListLength with its EndMark at its end, vectors, ThreePacked range and padding, each EndMark, zero trailing bytes, 1,500 octets plus the project's 1,500-byte frame rule (#665 issuecomment-6087462816), one Message per AttributeType, no value twice, a LeaveAll on every AttributeType, and the group address.
   - All five author `[WIRE]` plants are refused. 20 further malformations of real wire frames are refused, 20 of 20 (`receipts/grader_probe.txt`).
   - My own checker, written from 10.8.1.2, 10.8.2 and 35.2.2 with no shared code (`probes/indep_check.py`), finds 0 errors in 1,449 + 169 + 69 MRPDUs. The largest MRPDU is 187 octets (`receipts/indep_check.txt`).
   - Two extra code arms are refused: the PDU EndMark omitted, and MVRP sent to the MSRP group.
2. **Item 2, source address.**
   - The recorder is on before `half.reset()` and boot (`twin_split.cpp` `srptx_main`). The first MRPDU leaves at 1 ms, and every MRPDU carries the port's MAC `020000000001`, a constant independent of the DUT.
   - The author's code arm (first frame zero) is refused by `[SA]` alone.
3. **Item 3, spacing.**
   - LeaveAll is held on both sides. A draw of 5 s is refused, and a draw past 1.5 x LeaveAllTime is refused.
   - A late Join is refused.
   - The 18 ms widening is not the approved allowance (F-1). The early side of Join is not graded (F-2).
4. **Item 4, a full ring.**
   - In the hold run the ring held 507 of 512 words when the adapter refused a 30-word MSRP record. The refusal reached lwSRP (rc != 0), and lwSRP retained the MRPDU (`mrp_transmit` keeps `prepared_pdu`; the adapter keeps `owed_frame`, `srp_mbx.c:547-571`). It was sent first on release.
   - All 169 MRPDUs left in order, byte for byte. The 5 `[TX]` plants and the "refused MRPDU reported sent" arm are refused.
5. **Item 6, the licence at the policer.**
   - In `milan_datapath.sv` the split generate drives `pp_cd_srp_active_w` and `pp_cd_srp_sr_admitted_w` from `i_ctl_pub_licence` (`:9981-9982`).
   - `lwsrp_stream_gate`, `aaf_gate`, `crft_res_active_w`, the slope and reservation terms are outside the generate (`:8831-8848`, `:2320`, `:7150`). That is one RTL in both placements.
   - `make split` passes, 82 checks and 0 failures, with `[POL]` per bit at both talkers.
   - `split-mutants` catches 26 of 26, including the two new arms. The srptx arm "ACTIVE held open" is refused by `[LIC]`.
6. **Item 7, plants and mutants.**
   - `srptx-plants`: 23 of 23 refused. `srptx-mutants`: 10 of 10, after clean controls.
   - Re-running all ten author code arms with per-section grading, each is refused by its own words and by no other section. So each escapes without its own check (`receipts/logs/p1-code-probe.log`).
   - For capture plants, `[WIRE]` and `[TIME]` plants are also caught by `[TX]`. That is only because a capture plant edits the MAC bytes but not lwSRP's record; the code arms show the real separation.
7. **The fixture.**
   - `__wrap_srp_mbx_init` lives in `srptx.hpp`. That header is included only by `twin_split.cpp`, which is linked only into the bench binary `Vmilan_dp_twin_sp` (Makefile `build-twin-sp`, `SRPTX_WRAPS`).
   - Nothing under `sw/`, `syn/`, `hdl/` or the SoC references it, and the fixture is armed only by `scenario("licence")`.
   - Wire and hold run with `fixture: false`, no LICENCE write and no stream frame (`receipts/fixture_scope.txt`).
   - With the fixture switched off in a disposable copy, the licence run is refused: "source 0 never held its licence" (`receipts/logs/p2-nofix-run.log`). So the #608 check is not vacuous, and item 5 cannot be met in the production composition at this base, as the STOP states.
   - The wrappers pass straight through outside `--srptx`. The twin's split capture is byte-identical at base and head (`ee143865…`, `receipts/capture_hashes.txt`, also equal to the author's published hash). The adapter and lwSRP are unedited (no diff under `sw/firmware/ctrl/srp/*.c`, and the `third_party/lwSRP` gitlink is unchanged).
8. **No production change.**
   - `git diff --raw 1d6bf555 HEAD` touches only `tb/verilator/milan_dp/*`, three READMEs or design docs, `ctrl_configs.py` (gate classification) and `measure_test_evidence_readers.py`.
   - Nothing under `hdl/`, `syn/`, `sw/mailbox`, the firmware sources, `third_party/` or `sw/litex` changed. All six gitlinks are unchanged.
   - The commits are one line with no trailers.
9. **Gates run here** (clean clones at the head, pinned Verilator 5.050, sha256 `905795b9…`; all rc 0):
   - `make srptx` (wire, hold and licence: 0 findings each) and `srptx-plants` (23/23);
   - `make srptx-mutants` (10/10);
   - `make split` (82 checks, 0 failures) and `split-mutants` (26/26);
   - `exec-twin-sp` at base and head (identical captures);
   - docs and idiom gates: `docs_check`, `check_doc_paths`, `check_doc_style`, `check_em_dash --base 1d6bf555`, `gen_toc --check` and `--verify-anchors`, `check_py_idiom`, `check_cpp_idiom`, `check_sv_idiom`, `check_hygiene --check`, `check_todo_ownership`, `measure_test_evidence --check`, `measure_naming --check`, `measure_fail_fast --check`, `check_rtl_source_lists`, `check_soc_sources`;
   - `git diff --check 1d6bf555 HEAD` (`receipts/logs/`).
   - Not run here: the full sweep, `make twin` / `twin-plants`, the firmware self-test, the builder test and the budget harness. Their evidence is the author's published receipts.

**Comment rule.** The added source comments (`srptx.hpp`, `twin_split.cpp`, `sim_split.cpp`, `tb_split_top.sv`, the Python docstrings) carry issue and clause IDs only. They contain no lane label, review round, reviewer ID or issue-comment ID, so there is no RESIDUE. The issue-comment links are in `tb/verilator/milan_dp/README.md`, a documentation page that already carried 19 of them at the base.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-1, F-2) | `srptx_grade.py` against 802.1Q-2018 10.7.4, 10.8 and Tables 10-3/4/7, acceptance 1 to 7, #665 6495692075 and 6681686082; independent checker; code probes | R814-1 | 5fb6904ffe12effc4bde6bf5313faea7a3beebdc |
| RTL | CLEAN | `tb_split_top.sv:104-111,398-404` (probes only); `milan_datapath.sv:2320,7150,8831-8848,9891-9892,9981-9982` (licence path, both placements); `make split` + `split-mutants` 26/26; twin capture identical base/head; `git diff --raw` (no `hdl/` change) | R814-1 | 5fb6904ffe12effc4bde6bf5313faea7a3beebdc |
| Robustness | CLEAN | `srptx_grade.py:142-194` on 20 malformed and truncated frames; the hold scenario (`twin_split.cpp` `tick_ms`/`drain`, `srp_mbx.c:547-571`, `mrp_mad.c:1421-1540`); fixture-off run; `--srptx` argument refusal (`twin_split.cpp` `srptx_main`); S-3 recorded | R814-1 | 5fb6904ffe12effc4bde6bf5313faea7a3beebdc |
| Tests | UNCLEAN (F-1, F-2) | `srptx_plants.py` (23, section ablation), `srptx_mutants.py` (10, re-run with ablation), 9 reviewer code arms, `split_mutants.py:47-54`, `sim_split.cpp:321-349`, `twin_fw.py --replace` | R814-1 | 5fb6904ffe12effc4bde6bf5313faea7a3beebdc |
| Docs | UNCLEAN (F-1) | `tb/verilator/milan_dp/README.md:1488-1669`, `sw/firmware/ctrl/srp/README.md:380-391`, `docs/design/MAILBOX_SPLIT.md:1849-1858`, `sw/firmware/ctrl/README.md:255`, PR body; docs gates rc 0 | R814-1 | 5fb6904ffe12effc4bde6bf5313faea7a3beebdc |

## Real limits

- **Time model.** The firmware runs in zero simulated time. `[TIME]` therefore measures lwSRP's timers plus the RTL path. It never exercises the T_svc allowance it widens by, and the CPU's cost is the CPU budget harness's figure.
- **Shape.** One interface at the AX7101 shape only.
- **Item 5.** Held only under the test fixture. The production-composition run is owed (#867 stays open, per issuecomment-6760813135).
- **No manager source bank at this head.** The source-head execution evidence beyond what I ran is the author's published receipts (archive `fe59e758`).
- **Hosted evidence at the exact head** (`receipts/hosted_checks.txt`, read-only):
  - both runs, `rtl-full` 42769473532 and `rtl-fast` 42769473762, concluded **cancelled** on attempt 1;
  - cancelled jobs: `rtl-fast`, `publication-census`, 9 of 19 Verilator shards and 4 of 4 Yosys shards;
  - the union jobs and the `verilator-suites` / `yosys-portability` aggregates then failed on missing cases;
  - jobs that executed all succeeded (10 Verilator shards; the firmware, docs and elaborate jobs; `split-cdc`; `bdd-conformance`);
  - so there is no successful exact-head `rtl-fast`, `verilator-suites` or `yosys-portability` verdict. I do not infer a cause.
- **Hardware.** Physical calibration NOT RUN. No bench or hardware evidence; skips are not hardware proof.

## Pending manager duties

- Hosted and local-replica acceptance at the PR head (the exact-head runs were cancelled).
- The current-dev merge candidate (builder and native banks), against live `dev` `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`.
- A decision on F-1's allowance and F-2's reading, if a ruling rather than a code change is chosen.
- The #608 production-composition round once #810 lands.
- Filing the two found-not-fixed items the PR names (AAF `stream_id` 0; the twin half's late follow-on frame) as Issues, if not already filed.

R814-1 FINISHED
