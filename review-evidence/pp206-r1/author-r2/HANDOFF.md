# [A691d] processor #206, round 2 on PR #208 — HANDOFF

**Status: REVIEW READY at head `c836105`.** Every gate the round-2 assignment names returned rc 0. Two commits on
top of the round-1 head `e9272b5`; no RTL change, so no STOP condition was met.

TAKEN: issue #206 issuecomment-6443319415 (2026-10-27). REVIEW READY with the head: issuecomment-6444729032.
Assignment: issue #206 issuecomment-6443309884 (the latest [A10] comment, round 2). It answers R724-1
(PR #208 issuecomment-6443301891: F1 MINOR, S1 SUGGESTION, W1 RESIDUE) and R723-1's residue RES-01
(issuecomment-6438933031). Round-1 handoffs: `pp206-a691/` (head `9abb41f`) and `pp206-a691c/` (head `e9272b5`).

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before the first commit) |
| Branch | `206-gsi-settled-gate` (local; not pushed) |
| Base (processor main) | `097a79875f20c27f0a5987a193c165c5086f3cf5`, tree `e496f4f6faa5d95dbf531f743ecd0dc7a3f72f4a` |
| Round-1 head | `e9272b5635e76bf12a69376d59fd21d059cae320`, tree `0482079467bc4e40ebac7997441c9569b4cc4a8f` (HEAD before the first commit, checked) |
| Commit 1 | `7919c9a3a962ac78a0f4cc7806c8ac6ae9871dab` Claim every flag in section GI's settled-gate integrator and add the over-clearing mask arm, so a gate that clears more than 0x52000000 fails by name (issue #206) |
| **Head** (commit 2) | **`c836105351297947a7660952df7c4d92500a09ec`**, tree `1a4a8fe48ece11f134a6a03dbfbb6990451b86ed`: Rewrap the 133-column line in 06_aecp_engine.md's GET_STREAM_INFO ownership paragraph (issue #206) |
| `e9272b5..c836105` | 5 files, +54 −24: `tb/pp_top/sim_main.cpp`, `tb/pp_top/gsi_internal.hpp`, `tb/pp_top/gsi_mutants.py`, `tb/pp_top/README.md`, `docs/architecture/06_aecp_engine.md` |
| RTL, top-level ports, parameters, register map | unchanged: `git diff --stat e9272b5 c836105 -- hdl` is empty (`receipts/records/base-head-records.txt`) |
| Lane tree | clean, ignored files included (`git status --porcelain --ignored` empty) |
| Simulator | `verilator` on PATH, Verilator 5.052 (as in round 1) |

## 2. Changes (file:line at head, clause or finding)

| # | File:line | Change | Answers |
|---|---|---|---|
| 1 | `tb/pp_top/sim_main.cpp:1290-1297` | `gsi_fold_identity`'s comment and the new `H::GSI_FOLD_FLAGS = 0xFFFFFFFF`: in the settled-gate mode the harness integrator claims every flag in every STREAM_INPUT flags word: the three Table 5.9 flags, and BOUND, MSRP_ACC_LAT_VALID, MSRP_FAILURE_VALID and every other flag besides. The processor owns no selector 0 bit (06 §6.2: "all validity flags remain integrator-owned"); it only clears `0x52000000` while unsettled | R724-1-F1 (preferred form: every bit outside `0x52000000`) |
| 2 | `tb/pp_top/sim_main.cpp:2059` | the fold ORs `GSI_FOLD_FLAGS` into selector 0 (was `0x52000000`) | R724-1-F1 |
| 3 | `tb/pp_top/gsi_internal.hpp:626-634` | `gate_expected`: every body carries `GSI_FOLD_FLAGS & ~0x52000000` unsettled and `GSI_FOLD_FLAGS` settled, so the byte-exact check grades every other flag in both | R724-1-F1; Milan v1.2 Table 5.9 |
| 4 | `tb/pp_top/gsi_internal.hpp:659-663` | new named check in `gate_frame`, on every graded response (15 per run): `GI GATE <step> <kind>: every other flag the integrator claims passes for sink 0, BOUND, MSRP_ACC_LAT_VALID and MSRP_FAILURE_VALID among them` | R724-1-F1 |
| 5 | `tb/pp_top/gsi_internal.hpp:611-621` | section comment: the harness claims every flag; why selector 4's failure-code byte stays zero (SRP's matcher armed by A15, disarmed by A8 on every F05.3 arc out of SNR/SOK) | R724-1-F1, R724-1-S1 |
| 6 | `tb/pp_top/gsi_mutants.py:32-33`, `:60-64` | `settled_gate_mutations()` docstring and the seventh arm `settled-gate-mask-overclears` (selector 0 mask widened by BOUND, `~0x5600_0000`). The function is 38 lines; `mutations()` stays 100 | R724-1-F1 |
| 7 | `tb/pp_top/README.md:497-502`, `:514-521`, `:589` | the harness now claims every flag; settled or not every other claimed flag passes; W1's sentence exactly ("Premise checks read the binding view at RESET, PROBING, SETTLED, REPROBE, PASSIVE-STALE and UNBOUND."); the S1 reason; the new arm's row | R724-1-F1, R724-1-W1, R724-1-S1 |
| 8 | `docs/architecture/06_aecp_engine.md:397-401` | the 133-column line broken after "owners." and the paragraph's tail rewrapped (75-79 columns); its words unchanged | R723-1-RES-01 |

## 3. Checks, planted mutants and failing words

New check (row 4) and the new arm, at head:

| Arm | Plant (`hdl/top/protocol_processor_top.sv`, one site) | Named failing words (driver) |
|---|---|---|
| `settled-gate-mask-overclears` | `4'd0: aecp_gsi_data_w = gsi_data_i & ~64'h0000_0000_5200_0000;` → `... & ~64'h0000_0000_5600_0000;` | `GI GATE RESET solicited: every other flag the integrator claims passes for sink 0` (22 FAIL lines: the new check and byte-exact at every unsettled response) |

The reviewer's own probes, `reviewer_probes.py` from the R724-1 packet, run unchanged (sha256 `148ed335…d505`), on a clone at `c836105`:

| Variant | Edit | Result |
|---|---|---|
| `R-mask-overclears-bound` | mask `~0x56000000` | `run_rc` 1, complete; 22 FAIL lines, all `GI GATE`, first `GI GATE RESET solicited: every other flag the integrator claims passes for sink 0, …`; GI 6,388 checks, 22 failures |
| `R-mask-overclears-acclat` | mask `~0x72000000` | `run_rc` 1, complete; 22 FAIL lines, all `GI GATE`, same first line; GI 6,388 / 22 |
| `base-rtl` | this head's tests over the base RTL | `run_rc` 1; 82 FAIL lines, 32 `GI GATE`: the same counts as round 1. The base clears nothing, so it passes the new other-flags check, as it should |

Receipts: `receipts/reviewer-probes/` (`probes.log`, `out/results-R-mask-overclears-bound.json`, run logs, `INPUTS.txt`, `base-rtl/`).

The six round-1 arms and their words are unchanged (`pp206-a691c/HANDOFF.md` §3). The campaign below shows them
killed by the same lines as at `e9272b5`.

## 4. R724-1-S1: the failure-code byte while unsettled

**The listener cannot register a Talker Failed while the input is not PROBING_COMPLETED, so no step can carry a
non-zero failure code there.** Reasons, with the state-machine references (excerpts in `receipts/records/S1-reachability.txt`):

1. The top's selector 4 byte is `srp_snk_fail_code_w[sink]` (`protocol_processor_top.sv:3546`). SRP drives it as
   `msrp_fail_code_o = (tk_reg_state_o == FAILED) ? fcode : 0`, and `tk_reg_state_o` is 0 unless the sink's matcher
   `armed_r` is set (`KL_srp_listener_fsm.sv:1268-1275`).
2. `armed_r` is set only by the A15 settle and cleared by the A8 teardown (`KL_srp_listener_fsm.sv:933-935`, `:964-966`;
   the listener's `act_settle_o` / `act_teardown_o`, `KL_pp_acmp_listener.sv:1313`, `:1204`).
3. A15 is the only writer of `PB_COMPLETED_C` (`KL_pp_acmp_listener.sv:1311`), and it runs only on the PROBE_OK arcs
   PWR/PW2 → SNR (`hdl/acmp/rom/gen_ltn_rom.py:69-71`, F05.3 row 5).
4. Every F05.3 arc that leaves SNR or SOK carries A8: BIND_NEW (`:48-55`), UNBIND (`:57-64`), TMR_NOTK (`:83`, `cond/A8`),
   TK_UNREG (`:97`, `cond/A8`). The other SNR/SOK cells stay settled (BIND_SAME, GETRX, TK_REG SNR→SOK) or are `ign`
   (PROBE_OK/FAIL, TK_DISC, TK_DEP). The canonical action order runs A8 before every pbsta-writing action (A10, A12,
   A17, A4, A5) in the same arc (`KL_pp_acmp_listener.sv:608-628`). So REPROBE and PASSIVE-STALE, which keep the old stream
   *published* in the binding view, have already disarmed SRP's matcher. This is Milan v1.2 Table 5.30 / §5.5.3.5 as transcribed in F05.3.

The reason is in the section comment (`gsi_internal.hpp:615-617`) and the README (`:516-519`).
Not established (pre-existing, outside #206): a teardown reaches SRP through the one-deep listener stage of the SRP
service adapter (`protocol_processor_top.sv:2660-2722`). That takes a few cycles after the listener commits its new
pbsta, and that stage counts an overrun (`svc_drop_r`) rather than queueing it. This round did not measure that window
or establish whether such an overrun is reachable.

## 5. Processor gates (at `c836105`, each in a disposable clone; every `.rc` is the command's own status)

| Gate | Result | Receipt |
|---|---|---|
| `make -C tb/pp_top run` (the full suite, seven builds) | **rc 0**; 10,887 checks, 0 failures (default 10,332, fixture 20, identify 178, line 292, timebase 56, defaults 3, interfaces 6). That is 10,872 + 15, the new check on each graded response; GI 6,388 (was 6,373) | `receipts/processor/head-c836105/pp_top_run.*` |
| `python3 tb/pp_top/gsi_mutants.py --output <dir> --jobs 3` | **rc 0** (19 min 19 s); "GSI mutations: 30 detected by named checks; golden and restored PASS". The 31 prior records (golden, 29 arms, restored) have the same order and identical named failures as at `e9272b5`; the new arm is the one addition | `receipts/campaigns/gsi-c836105/` (`results/results.json`, `RAW-RECORDS.csv`) |
| `make check` | **rc 0** | `receipts/processor/head-c836105/make_check.*` |
| reviewer probes (§3) | both over-clear variants fail with named `GI GATE` lines | `receipts/reviewer-probes/` |
| RES-01 / W1 verifications | `awk 'NR>=394 && NR<=401 && length > 90'` and `awk 'NR>=394 && NR<=400 && length > 90'` print nothing; paragraph words equal; W1 sentence present | `receipts/records/residue-and-length-checks.txt` |

Carried from round 1, not re-run (no file they compile or read changed in a way that bears on them): full processor sweep
`scripts/run_suites.sh` (1,030,712 checks at `9abb41f`; its pp_top part is the suite above), `check-req-tags.py` (no REQ_TAG
added or moved), `acmp_mutants.py` arms, `scripts/lint_hdl.sh` (no `hdl/` change). The CI campaigns `make -C tb/pp_top
aecp-mutants` / `aecp-dispatch-mutants` were not run: the harness change acts only while `gsi_fold_identity` is set, which
only section GI's settled gate sets, and their goldens are the default build, which passes above.

## 6. Scratch parent consumer gate

Scratch parent: local clone of milan-fpga dev `97aab1d0` (push URL invalid; never pushed). Commits: `c3139895`
(the #202 wiring patch, sha256 `ff5068d295872d1f872b89890ff76f9bb1d3fd0738ad650282dbe45d9e171275`, + processor `097a7987`),
`c7d5887d`/`764d1253` (`9abb41f` and its ROM rows), `73dd3db7`/`10bb22af` (`e9272b5` and its ROM rows), and this round's
**`0dea6860`** ("scratch: pin processor c836105", a one-line gitlink change). `git submodule status`: protocol-processor
`c836105`, gptp-processor `55680bff`. Parent tree clean before and after (`PARENT-STATUS*.txt`).

| Consumer gate (pin `0dea6860`, gitlink `c836105`) | Result | Receipt |
|---|---|---|
| **`python3 scripts/check_py_idiom.py`** | **rc 0**; `long function: 9 <= 9`, every ratchet holds | `receipts/parent-static-0dea6860/01.*` |
| `python3 scripts/check_py_idiom.py --selftest` / `--list` | rc 0 / rc 0 (no `gsi_mutants.py` line) | `02.*`, `03.*` |
| **`python3 scripts/check_cpp_idiom.py`** | **rc 0**; every ratchet holds | `04.*` |
| `python3 scripts/check_cpp_idiom.py --selftest` | rc 0 | `05.*` |
| `measure_test_evidence.py --check`/`--selftest`, `check_hygiene.py --check`/`--selftest`, `measure_fail_fast.py --check`/`--selftest`, `check_todo_ownership.py`/`--selftest`, `check_doc_paths.py`, `measure_naming.py --check`/`--selftest` | all rc 0 | `06.*`-`16.*` |

All 16 logs are byte-identical to round 1's at gitlink `e9272b5`, except the Python idiom gate's module line count
(262,464 → 262,470, the new arm). No ROM digest rows were recorded for `c836105`: no `hdl/` file changed, so the ROM images
are the `e9272b5` ones. Carried from round 1, not re-run (this round changes only processor test-bench and doc files, which no parent build
compiles): the parent sweep (2,190,635 checks), milan_dp `[GSI]` (461 checks, base = head), the parent `gsi-mutants` 11/11,
the OOC area (+664 LUT / +12 FF).

## 7. Completion

Every item in the assignment is done: (1) the harness integrator claims every flag; `gate_expected` keeps the other flags in
settled and unsettled bodies; a new named check, a new driver arm killed by name, and both reviewer variants fail with
named `GI GATE` lines; (2) S1 answered "cannot", with the state-machine references (§4); (3) W1 and RES-01 applied as written;
(4) gates: full `make -C tb/pp_top run`, `gsi_mutants.py`, `make check`, both parent idiom gates on the scratch parent, all rc 0.
No RTL change. `PR-BODY.md` keeps "Closes #206".

No push, PR creation or edit, merge, rebase, sub-agent, hardware or bench access, flashing, or top-level interface change.
On issue #206 this round posted only TAKEN, and REVIEW READY at the end.

Resources (`receipts/records/MEMORY.txt`, the unit's memory.current sampled every 5 s): full suite max 3,376 MiB; driver
`--jobs 3` max 8,084 MiB; probes max 4,588 MiB. All were under the 9 GB cap and run one at a time. Host MemAvailable stayed above 40 GB. No
sweep or route was run.

## 8. Receipts

`INDEX.md` is generated from the files present. Published logs carry no host paths: the clone path is replaced by
`<work>`. Files over 200 KB and every compile log are listed by size and sha256 in `RAW-RECORDS.csv` / `RAW-RECORDS.txt`.
