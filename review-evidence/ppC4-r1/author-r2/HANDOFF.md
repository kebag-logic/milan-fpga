# [A454] HANDOFF — lane C4 (ACMP), PR #137, round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin confirmed)
- Branch `c4-acmp-coverage` (local, not pushed); round-2 start head `a9ce0fa2e0b8b120703c6e541668d4281cec286e` (confirmed)
- Round-2 head: `616cbdf1e54a56420e35b53cd161116702f7172d`
- Assignment: #45 comment 5903960934 (R410-1 F-1, the parent disposition, R411-1 S1, R411-1 S4, R410-1 S-1)
- STOP at `bf764ac` (#45 comment 5906502273), then the ruling (#45 comment 5906539259): option (b), withdraw item 4 by a revert commit of `dbd8624`, record S4 as retained, re-measure, re-run, REVIEW READY
- Status: **REVIEW READY** at `616cbdf`. Items 1, 2, 3 and 5 done; item 4 withdrawn by the revert `616cbdf`. Every processor gate is rc 0, `acmp_mutants.py` is 19 of 19 KILLED, and the 16 parent consumer commands are rc 0 with the combined adaptation plus the one disposition line.

## Session history

- Round 2 ran items 1-5 to `bf764ac`, then stopped: item 4's per-run timeout made the parent's `measure_test_evidence.py --check` rc 1 (wall-clock ratchet 4 > 3), so item 2's gate was 15 of 16.
- Ruling: #45 comment 5906539259, option (b). Reasons, as ruled:
  - S4 was a suggestion, and R411-1 itself says a hang cannot give a false KILLED: it yields no tally, so its only cost is wall time.
  - The wall-clock ratchet may only go down; raising it for a suggestion defeats it.
  - `d3_mutants.py` follows the same pattern without a timeout.
- Resume 1 (after the ruling), from `bf764ac` with the tree clean:
  - Revert `616cbdf` (one-line subject, no body): `tb/pp_top/acmp_mutants.py` is byte-identical to `a9ce0fa`'s and to `f55a25f`'s, and `tb/pp_top/README.md` loses only the timeout usage and rule text. `git grep` for `--timeout`, `SURVIVED/TIMEOUT` or `RUN_TIMEOUT` is rc 1.
  - Scratch parent reset (`git checkout -- .`, `git clean -fdX`); gitlink at `616cbdf` (scratch commit 0811d8d); the patch and the line re-applied.
  - Processor gates at `616cbdf` up to name_wr_mutant: all rc 0.
- Host power-off (10:30; back 11:34) cut d3_mutants at mutant 17 of 83. Those partial records are not used.
- Resume 2 (11:36): head `616cbdf`, tree clean, nothing running, no REVIEW READY posted yet.
  - The completed receipts at `616cbdf` are reused.
  - d3_mutants and both `git diff --check` runs were re-run in full, then the 16 parent commands, all from scratch.
- No tree commit after `616cbdf`: the recorded ACMP mutation table ("measured 2026-09-30 at the lane head", `tb/pp_top/README.md:1213`) re-measures record for record at `616cbdf`.

## Commits (one-line subjects, no body, no trailers)

| Commit | Item |
|---|---|
| 9151e8b | 1. R410-1 F-1: F00.2 GAP-15 open residue reads "none found" |
| (none) | 2. the parent disposition line (PR body only) |
| f55a25f | 3. R411-1 S1 / R410-1 S-2: IEEE 1722.1 edition on the message_type / flags citations and on F09.4 |
| dbd8624 | 4. R411-1 S4: per-run timeout in `acmp_mutants.py` (withdrawn: reverted by 616cbdf) |
| 06a84f5 | 5. R410-1 S-1: AS6 ACMP queue empty before the GET_RX_STATE; answer read as the next frame |
| bf764ac | records: `tb/pp_top` mutation table remeasured (section AC 43 checks) |
| 616cbdf | the revert of dbd8624, per the ruling (item 4 withdrawn, S4 retained) |

`git diff b2db3a97..616cbdf -- hdl` is empty. Round-2 net files (`a9ce0fa..616cbdf`):
- docs/00 (1 line), docs/architecture/09 (1 line)
- tb/acmp_listener/{README.md,sim_main.cpp}
- tb/acmp_nvm/sim_main.cpp (comments)
- tb/pp_top/{README.md,sim_main.cpp}
- tb/rx_validator/sim_main.cpp (comment)

`tb/pp_top/acmp_mutants.py` is unchanged net.

## Item 1 — R410-1 F-1 (9151e8b)

- Change: `docs/00_MILAN_COMPLIANCE_REVIEW.md:509`: the GAP-15 Open residue cell changes from #45 to "none found". Nothing else in 00 changes (a one-line diff).
- Rule: the F00.2 caption (`:513-517`): "none found" = the resolution is implemented and a suite of the named category (GAP-15: TOL) grades it. The residue #45 carried (REQ-ACMP-001, Milan v1.2 §5.5.2.2; no ACMPDU > 56 B fed) is graded by rx_validator F29 and pp_top AL. The ruling on F-1 applies it in the PR that closes #45 (precedent 05fd9e1, the GAP-03 row).
- Checked that no other issue carries GAP-15: exact "GAP-15" count is 0 in the body and comments of #83, #80, #21, #79, #52, #53, #60, #78, #15 and #47.
- PR body: round 1's "per that table's own rule it reads none found" (R411-1 S2) is replaced by an accurate statement: the rule defines "none found", and the ruling applies it when the residue issue closes.
- `make check` rc 0.

## Item 2 — the parent disposition (no tree change)

The line (in the d3_mutants.py form), for the parent's `scripts/measure_test_evidence.py` DUT_READER_DISPOSITIONS:

```
    "protocol-processor/tb/pp_top/acmp_mutants.py":
        "mutation campaign; it plants one ACMP listener, validator, top SRP-service, bound-view or "
        "SRP matcher defect from its own table into an isolated copy and requires every named check "
        "to fail in a completed run; no expected value is read from the text",
```

Proof: the parent consumer gate table below, 16 of 16 rc 0 at `616cbdf` with the combined adaptation plus this line. `measure_test_evidence.py --check` reports "0 <= 0 unexplained DUT-source reader(s), 3 <= 3 wall-clock-dependent suite file(s)".

## Item 3 — R411-1 S1, R410-1 S-2 (f55a25f)

Checked in the standards (IEEE 1722.1-2021 and 1722.1-2013 clause 8):

| Field | 2021 | 2013 |
|---|---|---|
| message_type | §8.2.1.4 Table 8-2 | §8.2.1.5 Table 8.1 (same codes) |
| status | §8.2.1.5 Table 8-3 | §8.2.1.6 Table 8.2 |
| control_data_length | §8.2.1.6 = 84 (96-B ACMPDU, Figure 8-1) | §8.2.1.7 = 44 (56 B) |
| flags | §8.2.1.16 Table 8-4 | §8.2.1.17 Table 8.3 |
| command timeouts | Table 8-1 | Table 8.4 |

- The lane's "2021 Table 8-2" was correct. `tb/acmp_nvm`'s "Table 8.1" was 2013 numbering with no edition; its flags "Table 8.2" was wrong in both editions (2013 status table).
- F09.4's "2013 96-B" is the wrong edition: 96 B is 2021's (§8.2.1 NOTE 2), and 56 B is the 2013 length (Milan v1.2 §5.5.2.2 keeps it).
- Edits, each naming the edition:
  - `tb/acmp_listener/README.md:69`
  - `tb/acmp_listener/sim_main.cpp:1209-1210,1221` (array comment column narrowed; Rule 11 split kept)
  - `tb/pp_top/README.md:1141`
  - `tb/pp_top/sim_main.cpp:8812,8976-8977,9018`
  - `tb/rx_validator/sim_main.cpp:754`
  - `tb/acmp_nvm/sim_main.cpp:176,185`
  - `docs/architecture/09_verification.md:62`
- Comments and one docs row only. acmp_nvm 360, acmp_listener 2988 and rx_validator 495 are unchanged; `make check` rc 0.
- Not in item 3's list, observed and unchanged: 03 V3 "96-B IEEE form" (no edition); `hdl/acmp/KL_acmp_talker.sv:228,294` and 05:135 "IEEE Table 8-3" (2021 numbering, no edition).

## Item 4 — R411-1 S4: withdrawn (dbd8624, reverted by 616cbdf); S4 retained

- What dbd8624 did (`tb/pp_top/acmp_mutants.py`):
  - a per-run bound (3600 s default, `--timeout`);
  - at the bound, SIGKILL of the command's whole process group;
  - the copy recorded SURVIVED/TIMEOUT (a golden BROKEN/TIMEOUT), never KILLED.
- Scratch probes, copies in `probes/`:
  - `timeout_probe.py`: a bench hanging after its full failing tally was SURVIVED/TIMEOUT, and no process was left;
  - a golden under a 3 s bound was BROKEN/TIMEOUT.
- Parent consequence (the STOP): `protocol-processor/tb` is a SUITE_TREE of the parent's `measure_test_evidence.py`, and a `.wait(timeout=...)` in a suite file counts towards the wall-clock ratchet. `scripts/test_evidence.budget` ratchet 4 is 3 and "may only go down", so the gate failed: "4 wall-clock-dependent suite file(s) > ratchet 3". In scratch:
  - `f55a25f` + the line: rc 0 (3 <= 3);
  - `bf764ac` with the budget raised to 4: rc 0 (4 <= 4). That option was (a); `parent-option-ratchet4.patch` is its scratch patch, not proposed.
- Ruling (b): revert `dbd8624` by a new commit, `616cbdf`; no history rewrite. S4 is retained with the ruling's reason (see Session history). Recorded in the PR body, "4. R411-1 S4: retained" and "What remains".

## Item 5 — R410-1 S-1 (06a84f5)

- Change (`tb/pp_top/sim_main.cpp`):
  - `get_rx_state(seq, next)` at :8916: with `next`, the answer is the next ACMP frame, so nothing is skipped
  - AS6 at :9258-9261: `CHECK(q_acmp.empty())` "AS6: no ACMP frame from the UNBIND_RX_RESPONSE to the GET_RX_STATE"; then the queue is cleared, so a stray frame counts once; then `get_rx_state(0x4816, true)`
- README AS6 text updated. Clause: Milan v1.2 §5.5.3.5.45.
- Section AC is 43 checks (was 42); pp_top 7931.
- Discrimination (`probes/as6_probe.py`, run with the driver's own judge()): the planted defect adds A5 to the SOK UNBIND cell in `gen_ltn_rom.py`, so one PROBE_TX follows the UNBIND_RX_RESPONSE.
  - On the round-1 bench (a9ce0fa export): SURVIVED, 0 failing checks.
  - At the round-2 bench: KILLED on the new check alone (1 of 43).
  - Goldens PASS on both.
  - A first version without the queue clear also failed "GET_RX_STATE unbound" and "1.5 s", a cascade; the clear keeps the attribution to one check.

## Parent-visible list (as in PR-BODY.md)

- No interface or behaviour change; `hdl/` untouched. The two docs edits change no parent reference: the parent cites processor 00 and 09 only at a pinned older commit and for other rows (SAVED_STATE_MATERIALIZATION.md).
- One registry entry: DUT_READER_DISPOSITIONS for `protocol-processor/tb/pp_top/acmp_mutants.py` (the item-2 line). The d3_mutants.py entry is in the combined adaptation.
- No parent budget change: `scripts/test_evidence.budget` untouched (wall-clock 3 <= 3; DUT readers 0 <= 0 with the line).
- Suite totals: acmp_listener 2988, rx_validator 495, pp_top 7931; sweep 1,016,817. No parent file at ec0cc0c1 quotes them.
- MILAN_COMPLIANCE_MATRIX.md §1.6 row "5.5.2 / 5.5.3" can cite the grading.

## Suite table (processor, at 616cbdf)

Verilator 5.052. A scratch PATH wrapper rewrites the suites' `--build -j 0` to `-j 8`; drivers run with `--jobs 1`, one heavy build at a time. The `bf764ac` run gave the same rc, totals and records throughout.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites PASS, 1,016,817 checks, 0 failing (455 s); acmp_listener 2988, acmp_nvm 360, rx_validator 495, pp_top 7931 |
| `./scripts/lint_hdl.sh` | 0 | 41 LINT OK |
| `make check` | 0 | lint 41 mermaid + 18 wavedrom, links 976, matrix 115 REQ / 17 GAP, modmatrix 94 rows 0 untested, params 26 |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | 19 of 19 KILLED, 3 goldens PASS (281 s); every record equal to the bf764ac run but the withdrawn `timeout` field |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected, golden + restored PASS (788 s) |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | decode killed, golden + restored PASS (33 s) |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` | 0 | 83 of 83 KILLED; goldens acmp_nvm / pp_top / rx_validator PASS (4933 s, after the power-off) |
| `git diff --check b2db3a97 HEAD` | 0 | also a9ce0fa2..HEAD |

Tree after the gates: `git status --porcelain` empty.

Not re-run (their inputs are untouched by the whole lane: `hdl/`, `scripts/` and their own suite dirs; none reads a changed tb dir): `make -C tb/srp_top mutants`, `make -C tb/nvm_port figures`, `./syn/yosys/run.sh`, `tb/srp_admission/mutants.py`, `tb/acmp_talker/retry_mutants.py`.

## Mutant table (acmp_mutants.py at 616cbdf; failing checks)

| Mutant | Suite | Failing |
|---|---|---|
| msg_ok_forced | acmp_listener / pp_top AC | 93 of 2988 / 1 of 43 |
| guard_ctlr_dropped | acmp_listener | 50 of 2984 |
| guard_talker_eid_dropped | acmp_listener | 40 of 2984 |
| guard_talker_uid_dropped | acmp_listener | 30 of 2984 |
| cdl_not_44_rejected | rx_validator / pp_top AC | 27 of 495 / 19 of 43 |
| st_ls_settle_as_withdraw | pp_top AC | 7 of 43 |
| st_ls_teardown_as_declare | pp_top AC | 1 of 43 |
| st_ls_sid_da_swapped | pp_top AC | 7 of 43 |
| st_ls_state_none | pp_top AC | 7 of 43 |
| st_ls_vid_dropped | pp_top AC | 7 of 43 |
| st_ls_index_zero | pp_top AC | 6 of 43 |
| st_ls_teardown_lost | pp_top AC | 2 of 43 |
| bound_view_not_latched | pp_top AC | 2 of 43 |
| bound_dmac_from_sid | pp_top AC | 2 of 43 |
| bound_view_not_cleared | pp_top AC | 1 of 43 |
| matcher_da_ignored | pp_top AC | 5 of 43 |
| matcher_vid_ignored | pp_top AC | 5 of 43 |
| (scratch probe, item 5) unbind-then-probe | pp_top AC | round-1 bench 0 (SURVIVED); round-2 bench 1 of 43 (KILLED) |
| (scratch probe, withdrawn item 4) hang-after-tally | rx_validator | SURVIVED/TIMEOUT under dbd8624 (27 FAILs logged, never KILLED) |

## Parent consumer gate table (at 616cbdf)

Scratch parent setup:
- `git archive` of the trusted checkout at ec0cc0c1. Its index equals the trusted index (977 entries, compared with `git ls-files -s`) but for the gitlink.
- `gptp-processor` 5dce647 and `third_party/verilog-axis` 48ff7a7 cloned from their public URLs at the pins. `external` is a gitlink only, uninitialized as in the trusted checkout.
- `protocol-processor` is a scratch clone of the lane at `616cbdf`, staged as the gitlink (scratch commit 0811d8d). `git submodule status` shows ' ' for all three initialized.
- `parent-adaptation-132-c1.patch` applied with `git apply`; the item-2 line inserted exactly before the retry_mutants.py entry. The 13 changed files are byte-equal to a fresh apply of both on HEAD, and `scripts/test_evidence.budget` is untouched.
- No build products before the bank (only pycache).

| # | Command | rc at 616cbdf |
|---|---|---:|
| 1 | python3 scripts/check_cpp_idiom.py | 0 |
| 2 | python3 scripts/check_py_idiom.py | 0 |
| 3 | python3 scripts/xvlog_gate.py --check | 0 (xvlog run alone: PASS, 4 findings == ratchet, pinned at protocol-processor@616cbdf1; 137 s) |
| 4 | python3 scripts/check_rtl_source_lists.py | 0 |
| 5 | python3 scripts/pp_srcs.py --check --selftest | 0 |
| 6 | python3 sw/builder/test_builder.py | 0 (940 s; "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11 needs a build tree absent here) |
| 7 | make -C tb/verilator/pp_shadow -j8 | 0 (295 checks, 0 failures) |
| 8 | python3 scripts/check_port_contracts.py | 0 |
| 9 | python3 scripts/measure_naming.py --check | 0 (96 recorded) |
| 10 | python3 scripts/measure_test_evidence.py --check | 0: "0 <= 0 unexplained DUT-source reader(s), 3 <= 3 wall-clock-dependent suite file(s)" |
| 11 | python3 scripts/docs_check.py | 0 (0 findings) |
| 12 | make -C tb/verilator/nvm_cosim lint | 0 |
| 13 | make -C tb/verilator/nvm_cosim quick | 0 (315/315) |
| 14 | make -C tb/verilator/milan_dp -j8 | 0 (1515 s) |
| 15 | make -C tb/verilator/milan_dp_render -j8 | 0 (326 s) |
| 16 | python3 scripts/lint_rtl.py --check | 0 (90 <= 90) |

Result: 16 of 16 rc 0, one at a time. #10 re-run after the builds: rc 0, same line. The five round-1 failures (#132/#133) are cleared by the combined adaptation. At `bf764ac` (before the revert) the same set was 15 of 16: only #10 failed, "4 > ratchet 3".

## Scratch and tools (outside the tree and this directory)

- Scratch: `$VALIDATION_STORAGE/ppC4-a454`:
  - logs/ (`proc-gates-616cbdf-summary.txt`, `parent16-616cbdf-summary.txt` and per-command logs)
  - mutants-616cbdf/, d3-616cbdf/, gsi-616cbdf/, namewr-616cbdf/
  - the bf764ac equivalents
  - parent/
  - export-a9ce0fa/ for the AS6 probe
- Verilator 5.052 (`/usr/bin/verilator` sha256 098b09b1...). The scratch wrapper `bin/verilator` (sha256 532caac0...) only rewrites `-j 0` to `-j 8`.
- Commands past the 10-minute tool cap (run_suites, the gsi/d3 drivers, the parent bank) were run detached in their own session and waited on in the foreground with `tail --pid`, until they exited. Nothing of this lane is left running.
- The lane tree is clean (`git status --porcelain` empty) at 616cbdf. Only gitignored build products under `tb/*/obj_*` remain, as before round 2.

## Posted

- TAKEN: #45 comment 5903969450.
- STOP: "[A454] STOP, head bf764ac8323c6ff5fd501ca3f16ed675733957ae" on #45, comment 5906502273.
- REVIEW READY: "[A454] REVIEW READY, head 616cbdf1e54a56420e35b53cd161116702f7172d" on #45, comment 5910710727.
