# HANDOFF: [A464], lane C4 (ACMP), PR #137, round 3 (merge only)

Status: **REVIEW READY** at `4e558491c608dc88efc7963a77cb6b49bce2a46e` (2026-10-01).
- Items 1 and 2 are done.
- Every processor suite and entry point is rc 0.
- `acmp_mutants.py` is 19/19 KILLED, `make -C tb/adp_engine mutants` 32/32 and the MAAP campaign 32/32.
- The parent consumer set is 16/16 rc 0.
- No STOP condition arose. The resolution keeps both sides, and the only renames are the ones the assignment allows (F30, M6).
- One judgement to flag for review: commit `4e55849` restates the denominator of a main-side record, "47 FAIL of 497" → "of 555", in two README rows.
  - I read that as part of "keep the README rows consistent". The merge changes the suite size, and the measured failing count is unchanged.
  - It touches no check, section or code. If the manager reads it otherwise, it can be reverted on its own.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c4-acmp-coverage`.
- Start head: `616cbdf1e54a56420e35b53cd161116702f7172d`.
- Merge target: processor `main` `d5f73bac158276a9fcf549185bad5c65c0498dae`.
- Assignment: issue #45 comment 5921008462. TAKEN: 5921016421.
- End head: `4e558491c608dc88efc7963a77cb6b49bce2a46e` (local, not pushed).

## Commits (one-line subjects, no body, no trailers)

| Commit | Item |
|---|---|
| `5609f8f` | 1. Merge of main `d5f73bac` (merge commit; both sides kept; lane validator section F30 / row M6) |
| `4e55849` | 1. The maap_version validator arm's record restated at the merged head (47 FAIL, of 555) |
| (none) | 2. PR-BODY.md Round 3 note (output directory) |

## Item 1: merge main

- Merge commit `5609f8f15aaefeb496b0ecdf0de432d4db92598b`, parents `616cbdf1` (lane) and `d5f73bac` (main). It is a `git merge --no-ff` with a one-line subject, and no rebase was involved.
- Conflicts: exactly the four files the assignment named. Everything else auto-merged.
  - `tb/rx_validator/sim_main.cpp`: main's F29 (maap_version 2, 0 and 31, issue #67, IEEE 1722-2016 B.2.3) is kept as is. This lane's 96-B ACMPDU section (issue #45, Milan v1.2 §5.5.2.2, IEEE 1722.1-2021 §8.2.1.6 cdl 84) collided on the name F29, so it becomes **F30**. The rename covers its banner comment and the three check labels ("F30 BIND_RX cdl 84", "F30 PROBE_TX cdl 84", "F30 truncated reference"). F30 is declared and run after F29. The body is otherwise byte-identical to the lane's.
  - `tb/rx_validator/README.md`: the tally line is `555 checks: 555 PASS, 0 FAIL` (base 437, main +60, lane +58; measured). The V3 bullet cites F30. Main's M5 row (maap_version) is kept, and this lane's row becomes **M6**, citing F30.
  - `tb/pp_top/sim_main.cpp`: main's `one_section` selector gains `acmp_only`, and `run_acmp` runs after `run_d3` and before main's `run_adp_config`. The full-run order is Suite, GI, NW, D3, AC, AD. Every section keeps its own model or tally, and `--acmp-only`, `--maap-internal-only` and `--adp-only` each run one section.
  - `tb/pp_top/README.md`: main's Section MP is kept in place, and this lane's Section AC follows it unchanged.
- Re-anchored:
  - `tb/pp_top/acmp_mutants.py:97`: the `cdl_not_44_rejected@rx_validator` named checks are now "F30 BIND_RX cdl 84" and "F30 PROBE_TX cdl 84". This is the only driver edit.
  - All 19 exact edits in the driver still occur exactly once in the merged `hdl/`. Main's changes to `protocol_processor_top.sv` (the ADPDU configuration mux) move no anchor.
  - Every `.patch` file (srp_top, maap, adp_engine) targets `hdl/` only, which this lane never touches, so none moves.
  - The MAAP campaign's validator arm names the prefix `F29`. After the rename that prefix matches only main's F29a/b/c.
- Check: at the merge commit, `git diff d5f73bac 5609f8f` touches exactly the lane's 11 files. At the end head the count is 12: those 11 plus `tb/maap/README.md`, from the record commit. For six of them the delta is byte-identical to `b2db3a97..616cbdf`. The other five differ only by the lines listed above.

- Records at the merged head, commit `4e558491c608dc88efc7963a77cb6b49bce2a46e`: the MAAP campaign's validator arm `validator-maap-version-1-only` fails the same 47 checks at the merged head (tally 555, 47). Its two records said "47 FAIL of 497", the pre-merge suite size. They now read "of 555": `tb/rx_validator/README.md:87` (M5) and `tb/maap/README.md:241`. This is a record restatement only, like C3's `b27e038` after its merge. The rest of every record stands as measured:
  - this lane's M6 row says "27 FAILs" with no denominator, and it measures 27 of 555;
  - section AC's table is "of 43", unchanged;
  - MP is "of 34", unchanged;
  - `tb/adp_engine/README.md:184` quotes "7,924 checks after the merge of PR #132", which is dated and so still true.

## Item 2: PR body Round 3 note

`PR-BODY.md` in this directory is updated. It keeps the `[A450]` first line and "Closes #45", "Closes #47" and "Closes #48".

- The intro now points to Round 3 and to the F29 → F30 / M5 → M6 rename. The round-1 and round-2 text keeps the names in force at those heads.
- A new "## Round 3" section covers:
  - the commits;
  - the merge and its resolution, with clause references: IEEE 1722.1-2021 §8.2.1.6 (cdl 84), Milan v1.2 §5.5.2.2 ("may accept the longer PDU") and IEEE 1722-2016 B.2.3.2 and B.2.3.4 for main's F29;
  - validation (the processor table, the mutation table and the parent consumer table);
  - the parent-visible list, which replaces round 2's;
  - what remains.
- The body has no absolute paths, no tool or model names and no attribution footer.

Clauses were checked in the standards' text:
- IEEE 1722.1-2021 §8.2.1.6: "set to 84 for this version".
- Milan v1.2 §5.5.2.2: "A Milan device shall send and accept this truncated PDU, and may accept the longer PDU".
- IEEE 1722-2016 B.2.3.1 to B.2.3.4: the maap_version rules main's F29 grades.

## Parent-visible list (as in PR-BODY.md, Round 3)

- **No interface or behaviour change from this lane.** `git diff d5f73bac..HEAD -- hdl` is empty. The RTL differences from the parent pin `b2db3a97` are main's own (#135, #136), and the parent set below runs them.
- **One parent registry entry, unchanged from round 2.** `DUT_READER_DISPOSITIONS["protocol-processor/tb/pp_top/acmp_mutants.py"]`, i.e. `parent-c4-disposition.patch`.
- **No parent budget change.** `scripts/test_evidence.budget` is untouched.
- **Suite totals:**
  - acmp_listener 2988, rx_validator 555, pp_top 7992; sweep 1,017,893.
  - No parent file at e4b771f9 quotes them. Its one `497` is the LUT figure in `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:118`.
- **The section rename.** The lane's validator section is now F30. No parent file at e4b771f9 cites rx_validator F29 or F30. At adoption, MILAN_COMPLIANCE_MATRIX.md §1.6 row "5.5.2 / 5.5.3" can cite rx_validator F30, pp_top AL/AI/AS, and acmp_listener B13/B14.

## Suite table (processor, at `4e558491`)

Tools and setup:
- Verilator 5.050, the hosted workflow's pin. `$VALIDATION_TOOLS/verilator-v5.050/bin/verilator` has sha256 `fb2cc573…` and `verilator_bin` has `51910d8d…`.
- A scratch PATH wrapper `$VALIDATION_STORAGE/ppC4-a464/bin/verilator` (sha256 `9848ce3a…`) only rewrites `--build -j 0` to `-j 8`.
- Heavy builds ran one at a time, and drivers ran with `--jobs 1`.
- tb build products were cleaned (`git clean -fdX -- tb`) before the sweep.

| Command | rc | Result | Wall s |
|---|---:|---|---:|
| `./scripts/run_suites.sh` | 0 | 33 suites PASS, 1,017,893 checks, 0 failing; acmp_listener 2988, acmp_nvm 360, rx_validator 555, pp_top 7992, maap 196, adp_engine 1367 | 655 |
| `./scripts/lint_hdl.sh` | 0 | 41 LINT OK | |
| `make check` | 0 | 41 mermaid + 18 wavedrom, links 981, matrix 115 REQ / 17 GAP, modmatrix 94 rows 0 untested, params 26 | |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested | |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | 19 of 19 KILLED, 3 goldens PASS | 274 |
| `make -C tb/maap mutants` | 0 | 32 checks: 32 PASS (3 controls: maap 196, pp_top maap-internal 34, rx_validator 555; 29 arms KILLED) | 228 |
| `make -C tb/adp_engine mutants` | 0 | 32 checks: 32 PASS (2 controls, 30 arms KILLED) | 327 |
| `make -C tb/srp_top mutants` | 0 | 90 checks: 90 PASS (controls, 78 arms KILLED, assertion coverage 65/65) | 1814 |
| `make -C tb/nvm_port figures` | 0 | all measured figures agree with the tree | 235 |
| `./syn/yosys/run.sh` | 0 | 36 YOSYS OK + YOSYS XILINX OK KL_aecp_engine (Yosys 0.66, sv2v 0.0.13) | 79 |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected, golden + restored PASS | 768 |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | decode killed, golden + restored PASS | 32 |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` | 0 | 83 of 83 KILLED, goldens acmp_nvm / pp_top / rx_validator PASS; the 71 pp_top failing counts equal the `tb/pp_top/README.md` D3 table, `validator_admits_held_aecp` 4 = rx_validator M4 | 4780 |
| `python3 tb/acmp_talker/retry_mutants.py` | 0 | 62 killed, 7 equivalence + 1 performance controls, baseline/restored rc 0 | 373 |
| `python3 tb/srp_admission/mutants.py` | 0 | 12 checks: 12 PASS | 732 |
| `python3 tb/desc_mem_guard/mutate.py` | 0 | hold-deleted mutant detected | 5 |
| `git diff --check` | 0 | `b2db3a97..HEAD`, `616cbdf..HEAD`, `d5f73bac..HEAD` | |

The tree is clean after each gate (`git status --porcelain` empty). Logs are in `$VALIDATION_STORAGE/ppC4-a464/logs/`, and the drivers' records are in `$VALIDATION_STORAGE/ppC4-a464/{acmp-mutants,maap-mutants,adp-mutants,srp-top-mutants,gsi-mutants,name-wr,d3-mutants,talker-retry,srp-admission-mutants,dmg-mutate}/`.

## Mutant table (`acmp_mutants.py` at `4e558491`; failing checks)

Every count equals round 2's. The only change is the rx_validator denominator, 495 → 555.

| Mutant | Suite | Failing | Named checks |
|---|---|---|---|
| msg_ok_forced | acmp_listener / pp_top AC | 93 of 2988 / 1 of 43 | B13 arms / AI3 |
| guard_ctlr_dropped | acmp_listener | 50 of 2984 | B14 wrong controller_entity_id PWR, PW2 |
| guard_talker_eid_dropped | acmp_listener | 40 of 2984 | B14 wrong talker_entity_id PWR, PW2 |
| guard_talker_uid_dropped | acmp_listener | 30 of 2984 | B14 wrong talker_unique_id PWR, PW2 |
| cdl_not_44_rejected | rx_validator / pp_top AC | 27 of 555 / 19 of 43 | F30 BIND_RX cdl 84, F30 PROBE_TX cdl 84 / AL1-AL4 |
| st_ls_settle_as_withdraw | pp_top AC | 7 of 43 | AS4 Ready New, AS4 class-D, AS5 |
| st_ls_teardown_as_declare | pp_top AC | 1 of 43 | AS6 Lv on the wire |
| st_ls_sid_da_swapped | pp_top AC | 7 of 43 | AS4, AS4 class-D, AS5 |
| st_ls_state_none | pp_top AC | 7 of 43 | AS4, AS4 class-D, AS5 |
| st_ls_vid_dropped | pp_top AC | 7 of 43 | AS4, AS4 class-D, AS5 |
| st_ls_index_zero | pp_top AC | 6 of 43 | AS4 class-D, AS4 one TK_ATTR_REGISTERED, AS5 |
| st_ls_teardown_lost | pp_top AC | 2 of 43 | AS6 Lv, AS6 no Listener declared |
| bound_view_not_latched | pp_top AC | 2 of 43 | AS2, AS5 bound view |
| bound_dmac_from_sid | pp_top AC | 2 of 43 | AS2 |
| bound_view_not_cleared | pp_top AC | 1 of 43 | AS6 bound view cleared |
| matcher_da_ignored | pp_top AC | 5 of 43 | AS3 x3 |
| matcher_vid_ignored | pp_top AC | 5 of 43 | AS3 x3 |

Other campaigns at the merged head:
- MAAP `validator-maap-version-1-only`: rx_validator 47 of 555 (F29a/b/c), pp_top MP7 4 of 34.
- MAAP `compare-mac-forward`: pp_top MP4 5 of 34.
- ADP `gate-enable-dropped-top`: pp_top adp-config 3.

## Parent consumer gate table

Scratch parent `$VALIDATION_STORAGE/ppC4-a464/parent`:
- `git archive` of the trusted checkout at `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`, extracted and committed as scratch commit 1. Its `git ls-files -s` equals the trusted index (980 entries), and its tree is `1788a7de…`, the same as the trusted tree.
- Submodules:
  - `gptp-processor` 5dce647 and `third_party/verilog-axis` 48ff7a7 are cloned from their public URLs at the pins.
  - `protocol-processor` is a scratch clone of this lane, detached at `4e558491`, staged as the gitlink in scratch commit 2.
  - `external` is a gitlink only and uninitialized, as in the trusted checkout.
  - `git submodule status` shows ' ' for the three initialized submodules.
- `parent-c4-disposition.patch` was applied with `git apply` (`--check` first). The only working-tree change is `scripts/measure_test_evidence.py` (+4).
- The trusted checkout was never modified.

The commands ran sequentially in one detached session, waited on in the foreground (`parent_bank.sh`), with Verilator 5.050 (the parent's pin) through the capped wrapper. Logs are in `$VALIDATION_STORAGE/ppC4-a464/logs/parent/`.

| # | Command | rc | Notes | Wall s |
|---:|---|---:|---|---:|
| 1 | python3 scripts/check_cpp_idiom.py | 0 | | 1 |
| 2 | python3 scripts/check_py_idiom.py | 0 | | 3 |
| 3 | python3 scripts/xvlog_gate.py --check | 0 | PASS, 4 findings == ratchet; pinned at protocol-processor@4e558491, gptp-processor@5dce647a; ran alone | 138 |
| 4 | python3 scripts/check_rtl_source_lists.py | 0 | | 1 |
| 5 | python3 scripts/pp_srcs.py --check --selftest | 0 | | 0 |
| 6 | python3 sw/builder/test_builder.py | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the mf48 build tree is not on this host) | 960 |
| 7 | make -C tb/verilator/pp_shadow -j8 | 0 | pp_shadow 311 checks, 0 failures | 205 |
| 8 | python3 scripts/check_port_contracts.py | 0 | | 3 |
| 9 | python3 scripts/measure_naming.py --check | 0 | 96 recorded | 0 |
| 10 | python3 scripts/measure_test_evidence.py --check | 0 | 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock files (73 <= 77 suites without a mutation arm; "can be lowered to 73" is informational) | 6 |
| 11 | python3 scripts/docs_check.py | 0 | 0 findings | 4 |
| 12 | make -C tb/verilator/nvm_cosim lint | 0 | | 1 |
| 13 | make -C tb/verilator/nvm_cosim quick | 0 | 315/315 | 27 |
| 14 | make -C tb/verilator/milan_dp -j8 | 0 | milan_datapath 235 checks (two builds) and 232, media_aclk 191, all 0 failures | 1457 |
| 15 | make -C tb/verilator/milan_dp_render -j8 | 0 | | 318 |
| 16 | python3 scripts/lint_rtl.py --check | 0 | 90 <= 90 | 4 |

Result: 16 of 16 rc 0. #10 was re-run after the builds: rc 0, with the same line. Afterwards the scratch parent's `git status` shows only the patched `scripts/measure_test_evidence.py`, and the processor clone is clean.

## Scratch and tools (outside the tree and this directory)

- Scratch root: `$VALIDATION_STORAGE/ppC4-a464`. It holds `bin/verilator` (wrapper), `gate.sh` and `wait.sh` (detached runner and foreground waiter), `parent_bank.sh`, `logs/`, the driver output directories, `parent/` (the scratch parent) and `std/` (text extracts of the three standards, for clause checks).
- Commands longer than the 10-minute per-command tool limit ran detached in their own session through `gate.sh`. I waited on each in the foreground until its rc file appeared, and nothing ran concurrently with a heavy build. Nothing of this lane is left running.
- The pre-commit check builds (rx_validator, pp_top `--acmp-only`) ran in the working tree before the merge commit. Their products are gitignored, and the tb products were cleaned before the gate sweep.
- The lane tree at the end is clean (`git status --porcelain` empty). Only gitignored build products remain.

## Posted

- TAKEN: #45 comment 5921016421.
- REVIEW READY: "[A464] REVIEW READY, head 4e558491c608dc88efc7963a77cb6b49bce2a46e" on #45, comment 5923627539.
