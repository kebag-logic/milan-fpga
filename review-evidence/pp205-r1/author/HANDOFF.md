# [A687] processor #205 — HANDOFF

**Status: REVIEW READY at head `7bad3943`. Every required gate returned 0; no STOP condition met.**
TAKEN: issue #205 issuecomment-6434681484. Assignment: issue #205 issuecomment-6434658917.
REVIEW READY: issue #205 issuecomment-6436855586 (head `7bad3943c6dc3a86814faa43aee53a1e8aab4a4f`).

GET_TX_STATE_COMMAND naming an unknown `talker_unique_id` (out of range, or a disabled source) is
answered TALKER_UNKNOWN_ID with the command's `listener_entity_id` and `listener_unique_id`
(Milan v1.2 5.5.4.3 step 1, Table 5.46; IEEE 1722.1-2021 8.2.5.3); a successful GET_TX_STATE keeps
Table 5.47's zeros. No STOP condition met: no top-level port, parameter or register-map change
(`receipts/records/interface-check.txt`).

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before each commit) |
| Branch | `205-gtx-state-echo` (local; not pushed) |
| Base (processor main) | `097a79875f20c27f0a5987a193c165c5086f3cf5`, tree `e496f4f6faa5d95dbf531f743ecd0dc7a3f72f4a` |
| Commit 1 | `c7250d652f928fc49051b2e7154cbb937d9dd2d4`, tree `8df9ef80721d5a32f3749a288d92610b73f38813`: the fix, tests, arms, documents |
| **Head** | **`7bad3943c6dc3a86814faa43aee53a1e8aab4a4f`**, tree `317c13456cdceac6cdcda6e7b40992c40e300b5f`: the talker README records measured at commit 1 (`git diff c7250d6 7bad394` is `tb/acmp_talker/README.md` only) |
| Scratch parent | `$VALIDATION_STORAGE/scratch/pp205-parent`, local clone of dev `97aab1d0`, push URL invalid, never pushed (§6) |

The lane tree is clean, ignored files included (`receipts/records/base-head-records.txt`).

## 2. Changes (file:line at the head, clause)

The issue's line numbers are those of `ed211803`; at main `097a7987` the same sites are `:1559/:1561`,
`:1618-1620`, `:24`, `:798` and `:1547-1548`.

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/acmp/KL_acmp_talker.sv:809` (issue `:671`, the comment that also gates the fetch) | `needs_pdu_w` also fetches the command's listener fields from the RX slot for GET_TX_STATE with an unknown `talker_unique_id`; a successful GET_TX_STATE fetches nothing (its latency is unchanged) | Table 5.46 |
| 2 | `hdl/acmp/KL_acmp_talker.sv:1632-1637` (issue `:1317-1319`) | the unknown-ID arm sets `resp_listener_eid_o = pdu_leid_r`, `resp_listener_uid_o = pdu_luid_r` with TALKER_UNKNOWN_ID | 5.5.4.3 step 1, Table 5.46; 1722.1-2021 8.2.5.3 (Figure 8-4), 8.2.5.2.3 |
| 3 | `hdl/acmp/KL_acmp_talker.sv:1629-1631` | the success arm zeroes both listener fields itself | Table 5.47 |
| 4 | `hdl/acmp/KL_acmp_talker.sv:1569-1572` (issue `:1258/:1260`) | the defaults stay 0 as idle values only (comment); no response takes its listener fields from them | — |
| 5 | `hdl/acmp/KL_acmp_talker.sv:24-30`, `:800-804`, `:1553-1558` (issue `:24`, `:671`, `:1246-1247`) | design comments: a successful GET_TX_STATE zeroes the listener fields; every TALKER_UNKNOWN_ID response echoes them (Tables 5.40, 5.44, 5.46) | — |
| 6 | `tb/acmp_talker/sim_main.cpp:498-500` | `L_DIST = 0xF1E2D3C4B5A69788`, a listener EID with eight distinct bytes | — |
| 7 | `tb/acmp_talker/sim_main.cpp:555-562` | B2 (success, command L1/7 → 0/0) tagged REQ-ACMP-008 | Table 5.47 |
| 8 | `tb/acmp_talker/sim_main.cpp:622-629` | C2: source 15 with `L_DIST`/`0x8C17` expects both echoed (was 0/0); tagged REQ-ACMP-008 | Table 5.46 |
| 9 | `tb/acmp_talker/sim_main.cpp:880-886` | H3 (new): disabled source 6, the same echo; tagged REQ-ACMP-008 | 5.5.4.3 step 1, Table 5.46 |
| 10 | `tb/acmp_talker/sim_main.cpp:9-11` | header comment | — |
| 11 | `tb/pp_top/acmp_mutants.py:614-643, 645, 26-28` | group `TX_STATE_ECHO` (three arms), added to `MUTANTS`; docstring names #205 | — |
| 12 | `docs/architecture/05_acmp_engine.md:420-421, 431-439` | F05.11 GET_TX_STATE leaves; the refusal paragraph | Tables 5.46/5.47; 1722.1-2021 8.2.5.3 |
| 13 | `docs/00_MILAN_COMPLIANCE_REVIEW.md:405` | REQ-ACMP-008: both responses, Tables 5.46/5.47, 1722.1-2021 8.2.5.3, issue #205 | — |
| 14 | `tb/acmp_talker/README.md:8, 22-28, 244-248, 282, 315, 367-393` | count 1,561; case list; the issue #205 section (cases, arms, measured line); retry re-measure; two retry counts (782, 144) | — |

Finding on the citation: in IEEE 1722.1-2021, 8.2.4 is the ACMP Listener state machine (its
`txResponse`, 8.2.4.2.5, has the same wording as the talker's); the talker clause is 8.2.5, and
Figure 8-4's GET STATE action is `response = rcvdCmdResp; error = TALKER_UNKNOWN_ID;` for an invalid
ID. Source and documents cite 8.2.5.3 (`receipts/spec/`).

Path to the wire: the top latches every talker response field unchanged
(`hdl/top/protocol_processor_top.sv:3399-3418`) and builds one 56-byte ACMPDU for every talker message
type (`:3376-3379`), so the frame carries what the response port carries. The talker has its own
RX-slot read port in the top (`RXP_TKR_C`) and frees the slot itself, so the added fetch needs no
top change. `tb/pp_top` has no TALKER_UNKNOWN_ID case for any talker command (none before this change
either); the acceptance asks for the talker case.

## 3. New checks, their planted defects, failing words

| Check | Planted defect | Failing words |
|---|---|---|
| C2, H3 listener fields | main's talker RTL (the reported defect), new suite, simulator pin 5.050, rc 2 (`receipts/tests/base-rtl/`) | `FAIL: C2 unknown-id listener_eid got 0000000000000000`, `FAIL: C2 unknown-id listener_uid got 0`, `FAIL: H3 disabled source GET_TX_STATE listener_eid got 0000000000000000`, `FAIL: H3 disabled source GET_TX_STATE listener_uid got 0`; `1561 checks: 1557 PASS, 4 FAIL` |
| C2, H3 | arm `tx_state_unknown_zeroes_listener` (the echo replaced by 0) | the same four lines; KILLED, 4 failing |
| C2, H3 | arm `tx_state_unknown_not_fetched` (the fetch term removed) | the same four lines; KILLED, 4 failing |
| B2 listener fields | arm `tx_state_success_echoes_listener` (every GET_TX_STATE fetched and echoed) | `B2 listener_eid got 1111222233334444`, `B2 listener_uid got 7`; KILLED, 2 failing |

## 4. Processor gates (every rc is the command's own exit status, never through a pipe)

Run through the recorded-gates runner in disposable clones (simulator: the CI pin 5.050), never in the
lane tree. Commit 1 holds every input the suites, campaigns and elaboration read; the head adds README
records only, so the light gates were re-run there.

| Gate | At `c7250d6` | At head `7bad394` |
|---|---|---|
| `scripts/lint_hdl.sh` | rc 0 | (no hdl change) |
| `REQ_TAG_LOG=… scripts/run_suites.sh` (the full sweep, serial: no CPU range was free for shard units, and the shard runner shards the parent's sweep) | **rc 0, `suites: 1030609 checks total, 0 failing`**; `acmp_talker` 1,561, `pp_top` 10,753 (#202: 1,030,593) | — |
| `scripts/check-req-tags.py --suites … --evidence …` (executed half) | **rc 0**, 249 tags, 249 evidence lines, 14 suites | — |
| `make -j1 check` | rc 0 | **rc 0** |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 |
| `syn/yosys/run.sh` | rc 0 | — |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0 | — |
| `make -C tb/acmp_talker run` | in the sweep: 1,561 of 1,561 | **rc 0, `1561 checks: 1561 PASS, 0 FAIL`** |
| `make -C tb/acmp_talker lint` | rc 0 | rc 0 |
| `make -C tb/pp_top` (all seven builds) | in the sweep: 10,753 of 10,753; working-diff run `10753 checks: 10753 PASS, 0 FAIL` | — |
| `make -C tb/nvm_port figures` (with `refs/pull/13/head` fetched, as CI does) | rc 0 (894 s) | (no input change) |
| `git diff --check 097a798 HEAD` | rc 0 | rc 0 |
| `tb/pp_top/acmp_mutants.py --jobs 3` (the whole ACMP campaign) | **rc 0, 101 of 101 KILLED** by their named checks, eight goldens PASS (#202: 98 of 98) | — |
| `acmp_mutants.py --only` the three `TX_STATE_ECHO` arms | rc 0, 3 of 3 KILLED (4, 4, 2), golden PASS | — |
| `tb/acmp_talker/retry_mutants.py --jobs 4` (the talker retry campaign) | **rc 0**, 62 killed, 7 equivalent, 1 performance control; baseline and restored rc 0 at 1,561 checks; `no_command_ready` 771 → 782 and `no_get_tx_state_response` 133 → 144 failures (H3 adds a GET_TX_STATE case), every other count unchanged | — |

## 5. Scratch-parent consumer gate

Scratch parent at `876a55b9` (dev `97aab1d0` + gitlink `7bad3943` + the patch), the seventeen
commands of the #202 consumer run (the manager's spec for `a5ad8cae`), same order, run through the
recorded-gates runner with the simulator pin 5.050; runner rc 0, 06:49Z to 08:06Z
(`receipts/parent/consumer-gate/`).

| # | Consumer gate | Result | #202 consumer run (`a5ad8cae`) |
|---|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | rc 0 | rc 0 |
| 2 | `python3 scripts/check_py_idiom.py` | rc 0 | rc 0 |
| 3 | `python3 scripts/xvlog_gate.py --check` | rc 0 (154 s) | rc 0 |
| 4 | `python3 scripts/check_rtl_source_lists.py` | rc 0 | rc 0 |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | rc 0 | rc 0 |
| 6 | `python3 sw/builder/test_builder.py` | rc 0 (1,389 s); `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11, the calibration arm, needs a place report that is not on this machine | rc 0, the same arm not run; the gate lines differ only in one duration (2 s vs 3 s) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | rc 0, 2,187 checks, 0 failures | rc 0, 2,187 |
| 8 | `python3 scripts/check_port_contracts.py` | rc 0 | rc 0 |
| 9 | `python3 scripts/measure_naming.py --check` | rc 0 | rc 0 |
| 10 | `python3 scripts/measure_test_evidence.py --check` | rc 0 | rc 0 |
| 11 | `python3 scripts/docs_check.py` | rc 0 | rc 0 |
| 12 | `python3 scripts/lint_rtl.py --check` | rc 0 | rc 0 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 | rc 0 |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0, 315 checks, 0 failures | rc 0, 315 |
| 15 | `make -C tb/verilator/milan_dp -j8` (every leg, sidmove and sidmove8 included) | rc 0 (1,867 s), 13,685 checks, 0 failures | rc 0, 13,685 |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | rc 0 (842 s), 347 checks, 0 failures; models built from scratch here (the #202 run reused objects, hence its shorter log) | rc 0, 347 |
| 17 | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 | rc 0 |

Tallied by the parent's `scripts/suite_tally.py`: legs 7, 14, 15 and 16 give 16,534 checks, 0
in-suite failures, byte-identical to the tally of the #202 run's logs (`suite_tally.txt`,
`suite_tally_202_consumer_run.txt`). The builds printed 1,281 non-fatal lint warnings, none in the
processor's `acmp/` sources (all in parent and third-party files). After the run the parent's tracked
tree and the `protocol-processor` worktree were clean. The full parent native sweep
(`scripts/run_all_suites.sh`, the one `native-shards.py` shards) is not part of this consumer gate
and was not run.

## 6. Scratch parent

`$VALIDATION_STORAGE/scratch/pp205-parent`, branch `scratch-pp205-a687`, cloned from the trusted dev clone
at `97aab1d0`; origin fetch URL GitHub, push URL `no-push://…` (never pushed). Commits (local):
`06c1e706` pins `protocol-processor` at `7bad3943`; `876a55b9` applies the patch with `git apply
--index` (`git apply --check --index` rc 0 first; the commit's diff equals the patch outside its index
lines). Submodules at dev's pins, initialised from the #202 consumer clone's local copies, then their
URLs reset to the `.gitmodules` values, with no push URL inside any submodule (the parent's pin proof
rejects one). `receipts/parent/PARENT-STATE.txt`.

## 7. Resources

One service unit (16 CPUs, 96-111). `cpu_ranges.py` showed no free 12- or 16-CPU range throughout
(104 to 128 of 128 busy), and `native-shards.py` shards the parent's sweep, not the processor's
`run_suites.sh`, so the processor sweep ran serially in this unit; no shard units were made. The
unit's `memory.peak` (page cache included) is 11.4 GB (10.6 GiB), reached once while the talker
retry campaign overlapped the ACMP goldens and the sweep, above the 10 GB target; anonymous memory
was 2-4 GiB, the rest page cache. `MemoryHigh` was then set to 9 GiB on this unit at runtime, so the
kernel reclaims cache first; the recorded peak did not move afterwards and every later sample was under
6 GB. `MemoryMax` stays 12 GB. Host MemAvailable stayed above 45 GB. No Vivado route was run.

## 8. Completion

Every assignment item is met: the fix (item 1); C2/H3 echo checks, B2 success case and the arm that
zeroes the echo, killed (item 2, plus two arms for the fetch and the success zeros); 05 and
REQ-ACMP-008 (item 3); the talker and processor-top suites, `acmp_mutants.py`, `make check` and the
parent consumer gate, all rc 0 (item 4). Two commits on main `097a7987`: `c7250d65`, `7bad3943`.
No push, PR creation or edit, merge, rebase, sub-agent, hardware or bench operation, flashing, or
top-level port, parameter or register-map change was performed. No existing comment was edited.

## 9. Receipts

`INDEX.md` and every `receipts/**/INDEX.md` are generated from the files present. Host paths in
receipts are normalized (`<scratch>`, `<lanes>`, `<tmp>`, `<home>`, `<mgmt>`, `<pinned-tool>`).
Raw logs over 190 KB are kept as their size, sha256 and last 80 lines (`*.over-limit.txt`);
`receipts/RAW-RECORDS.csv` lists every raw record's size and sha256, copied or not (per-arm and
per-case campaign logs are listed there, not copied).

| Receipt | What it holds |
|---|---|
| `receipts/spec/` | Milan v1.2 5.5.4.3 and Tables 5.40/5.44/5.46/5.47; IEEE 1722.1-2021 8.2.5.2.3, 8.2.5.2.5, Figure 8-4 |
| `receipts/tests/base-rtl/` | the new suite on main's talker RTL (pin 5.050): the four failing lines, rc 2 |
| `receipts/tests/first-runs/` | first runs on the working diff before the first commit (host simulator 5.052; not gates) |
| `receipts/processor/gates-c7250d6/` | the twelve processor gates at commit 1 (spec, per-command logs, results, the tag evidence) |
| `receipts/processor/gates-head-7bad394/` | `make check`, the matrix, the talker suite and lint, `git diff --check` at the head |
| `receipts/campaigns/acmp/` | the whole ACMP campaign at commit 1 (log, rc, times, per-arm summary, the three new arms' records and logs) |
| `receipts/campaigns/acmp-new-arms-c7250d6/` | the three new arms run alone at commit 1 |
| `receipts/campaigns/retry/` | the talker retry campaign at commit 1 (log, rc, coverage, baseline, restored, the two moved counts' logs) |
| `receipts/parent/` | the scratch parent state; the consumer gate (spec, per-command logs, results, tallies) |
| `receipts/records/` | base and head records, the full diff, the interface check, the sweep against #202, resources |

## 10. Issue comments posted

Only two, both on processor issue #205: `[A687] TAKEN` (issuecomment-6434681484) and
`[A687] REVIEW READY — head 7bad3943c6dc3a86814faa43aee53a1e8aab4a4f` (issuecomment-6436855586).
