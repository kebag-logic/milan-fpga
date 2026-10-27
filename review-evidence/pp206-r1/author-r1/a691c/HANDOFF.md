# [A691c] processor #206 — HANDOFF (continuation of [A691])

**Status: REVIEW READY at head `e9272b5`.** Every gate this commit touches returned rc 0. One commit on top of [A691]'s REVIEW READY head `9abb41f`:
`tb/pp_top/gsi_mutants.py`'s `mutations()` was split, so the parent's Python idiom gate (Rule 12 of the parent's
`docs/development/CODE_QUALITY.md`, long function, ratchet 9) passes with this head as the gitlink and the #202
patch applied. Nothing else changed.

TAKEN: issue #206 issuecomment-6437479570 (2026-10-27). REVIEW READY with the head: issuecomment-6437981897.
Assignment: issue #206 issuecomment-6434829865; this continuation's task came from the manager after [A691]'s REVIEW
READY (issuecomment-6437442827). [A691]'s handoff and PR body at `9abb41f` are kept verbatim as
`receipts/prior-9abb41f/HANDOFF-9abb41f.md` and `PR-BODY-9abb41f.md`, and its receipts as `receipts/prior-9abb41f/`.

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before the commit) |
| Branch | `206-gsi-settled-gate` (local; not pushed) |
| Base (processor main) | `097a79875f20c27f0a5987a193c165c5086f3cf5`, tree `e496f4f6faa5d95dbf531f743ecd0dc7a3f72f4a` |
| Previous head ([A691]) | `9abb41f9f539fde8d940ff23b4b594f46658a46a`, tree `ac9a94c068f955e63a4d20c6fe7cbd8d6edd2e65` |
| **Head** | `e9272b5635e76bf12a69376d59fd21d059cae320`, tree `0482079467bc4e40ebac7997441c9569b4cc4a8f` |
| Commits | `9abb41f` Report an input's stream_id, destination MAC and VLAN and their flags in GET_STREAM_INFO only while it is PROBING_COMPLETED (issue #206); `e9272b5` Split the settled-gate arms out of gsi_mutants.py's mutations() so no function exceeds 100 lines (issue #206) |
| `9abb41f..e9272b5` | `tb/pp_top/gsi_mutants.py` only, +35 −27 |
| Top-level ports, parameters, register map | unchanged (`e9272b5` touches no `hdl/` file; `receipts/prior-9abb41f/records/base-head-records.txt` for `9abb41f`) |
| Lane tree | clean, ignored files included (`git status --porcelain --ignored` empty) |

## 2. Changes (file:line at head, clause)

Rows 1-6 are [A691]'s `9abb41f` change, with the same line numbers at `e9272b5` (`receipts/prior-9abb41f/HANDOFF-9abb41f.md` §2).

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/top/protocol_processor_top.sv:3532`, `:3554-3564` | `gsi_settled_w`: an in-range index whose committed status `gsi_status_w[7:5]` is `PB_COMPLETED_C`, the test selector 6 used inline | Milan v1.2 5.3.8.5, 5.3.8.6 Table 5.5 value 3; IEEE 1722.1-2021 7.4.16.2 |
| 2 | `hdl/top/protocol_processor_top.sv:3573-3574` | selector 6 reads the same wire; behaviour unchanged | Milan v1.2 Table 5.9 (stream_vlan_id) |
| 3 | `hdl/top/protocol_processor_top.sv:3578-3588` | while unsettled: selector 0 `& ~0x52000000`, selector 2 = 0, selector 4 `[63:16]` = 0 | Milan v1.2 5.4.2.10.1, Table 5.9 |
| 4 | `docs/architecture/06_aecp_engine.md:384-397`, `:460-461`, `:479-480`, `:491-493` | §6.2 and the F06.12/F06.13 rows | issue #206 acceptance item 3 |
| 5 | `docs/architecture/02_interfaces.md:430`, `docs/guides/integrator.md:600-609`, `docs/00_MILAN_COMPLIANCE_REVIEW.md:435` | the same rule where the integrator's words are described | issue #206 acceptance item 3 |
| 6 | `tb/pp_top/README.md:494-515`, `:576-581` | section GI's settled-gate steps and the six arms | — |
| **7** | **`tb/pp_top/gsi_mutants.py:28-59`** (new `settled_gate_mutations(top)`, 32 lines), **`:140`** (`*settled_gate_mutations(top),` in `mutations()`, now `:62-161`, 100 lines) | the six #206 arms moved out of `mutations()` unchanged, spliced in at their old position; the issue #206 comment becomes the docstring | parent Rule 12 (long function over 100 lines); issue #206 |

Row 7 is a pure move. Importing both versions shows `mutations()` returning the same 29 tuples in the same order
(`old == new: True`). The driver's results are therefore read in the same declared order as before. `mutations()`
is at exactly 100 lines, the most the rule allows (it fires at over 100). The next arm added to it has to go into a
function of its own, or into this one.

## 3. Checks, planted mutants and failing words

The checks and arms are unchanged from `9abb41f` (`receipts/prior-9abb41f/HANDOFF-9abb41f.md` §3): section GI
`settled_gate()` (`tb/pp_top/gsi_internal.hpp:606-742`, 119 checks), six arms, now at `tb/pp_top/gsi_mutants.py:35-58`:

| Arm | Plant | Named failing words |
|---|---|---|
| `settled-gate-removed` (the defect as reported) | `if (!gsi_settled_w)` → `if (1'b0)` | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` |
| `settled-gate-flags-passed` | selector 0 mask → `gsi_data_i` | `GI GATE PASSIVE-STALE solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear` |
| `settled-gate-sid-passed` | selector 2 zero → `gsi_data_i` | `GI GATE PASSIVE-STALE solicited: stream_id sink 0 is zero` |
| `settled-gate-dmac-passed` | selector 4 `[63:16]` zero → `gsi_data_i[63:16]` | `GI GATE PASSIVE-STALE solicited: stream_dest_mac sink 0 is zero` |
| `settled-gate-closed` | `if (!gsi_settled_w)` → `if (1'b1)` | `GI GATE SETTLED solicited: stream_id sink 0 is the settled stream's` |
| `settled-means-bound` | `== PB_COMPLETED_C` → `!= 3'd0` | `GI GATE PROBING solicited: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear` |

The check for this commit is the parent's own gate. With `9abb41f` as the gitlink it fails with
`FAIL: long function 10 > ratchet 9`, and `--list` blames `protocol-processor/tb/pp_top/gsi_mutants.py long function=1`
(`receipts/parent-py-idiom-764d1253/`). With `e9272b5` it passes at `long function: 9 <= 9`. The two `--list`
outputs differ only in that line.

## 4. Processor gates

At `e9272b5`, each in a disposable clone of the lane; every `.rc` is the command's own status:

| Gate | Result | Receipt |
|---|---|---|
| `python3 tb/pp_top/gsi_mutants.py --output <dir> --jobs 3` | rc 0 (17 min 46 s); "GSI mutations: 29 detected by named checks; golden and restored PASS"; all 31 records `passed`. The variant order and every named failure line are identical to the `9abb41f` run's `gsi-results.json`. The six #206 arms are killed by the words in §3 | `receipts/campaigns/gsi-e9272b5/` (`results/results.json`; logs over 190 KB kept as size and sha256 in `RAW-RECORDS.csv`, plus tail and FAIL lines; `VOID.md`) |
| `make check` | rc 0; output identical to `9abb41f`'s except for one host-path line in pip's notice | `receipts/processor/head-e9272b5/` |

Carried from `9abb41f` (`receipts/prior-9abb41f/`). `e9272b5` changes no file these gates read: the processor's
sweep, CI and Makefiles never name `gsi_mutants.py` (`git grep gsi_mutants` finds only the README's command line,
which is unchanged).

| Gate | Result |
|---|---|
| full sweep `bash scripts/run_suites.sh` with `REQ_TAG_LOG` | rc 0; 1,030,712 checks, 0 failing; pp_top 10,872 |
| `python3 scripts/check-req-tags.py --suites … --evidence …` | rc 0; 247 tags |
| `python3 tb/pp_top/acmp_mutants.py --only gsi_vlan_external parent_vlan_shifted stored_vlan_truncated retry_probe_status_cleared` | rc 0; 5 of 5 killed |
| `bash scripts/lint_hdl.sh` | rc 0; 41 modules |
| base GI / head tests on the base RTL | rc 0, 6,254 checks / 82 FAIL lines, 32 `GI GATE` |

## 5. Scratch parent consumer gate

The scratch parent is a local clone of milan-fpga dev `97aab1d0`. Its push URL is invalid and it was never pushed.

| Commit | Content |
|---|---|
| `c3139895` | dev + the #202 wiring patch (sha256 `ff5068d295872d1f872b89890ff76f9bb1d3fd0738ad650282dbe45d9e171275`) + processor `097a7987` |
| `c7d5887d`, `764d1253` | gitlink → `9abb41f`; its ROM digest rows ([A691]'s gated pin) |
| `73dd3db7` | gitlink → `e9272b5` (one line) |
| **`10bb22af`** | `./syn/yosys/ooc.sh --record-rom-digests` (rc 0) rows for `e9272b5`: `ltn_rom.hex` `23cc67ee…e956`, `ucode.hex` `1f78804e…a80a8e`, equal to the `9abb41f` and `ed211803` rows. **The gated pin.** |

Parent tree clean before and after every gate (`PARENT-STATUS*.txt`).

| Consumer gate | Pin / gitlink | Result | Receipt |
|---|---|---|---|
| **`python3 scripts/check_py_idiom.py`** | `10bb22af` / `e9272b5` | **rc 0**; `long function: 9 <= 9`, every ratchet holds | `receipts/parent-static-10bb22af/01.*` |
| `python3 scripts/check_py_idiom.py --selftest` | same | rc 0 | `02.*` |
| `python3 scripts/check_py_idiom.py --list` | same | rc 0; no `gsi_mutants.py` line | `03.*` |
| **`python3 scripts/check_cpp_idiom.py`** | same | **rc 0**; every ratchet holds | `04.*` |
| `python3 scripts/check_cpp_idiom.py --selftest` | same | rc 0 | `05.*` |
| `python3 scripts/measure_test_evidence.py --check` / `--selftest` (its registry names this file) | same | rc 0 / rc 0 | `06.*`, `07.*` |
| `python3 scripts/check_hygiene.py --check` / `--selftest` | same | rc 0 / rc 0 | `08.*`, `09.*` |
| `python3 scripts/measure_fail_fast.py --check` / `--selftest` | same | rc 0 / rc 0 | `10.*`, `11.*` |
| `python3 scripts/check_todo_ownership.py` / `--selftest` | same | rc 0 / rc 0 | `12.*`, `13.*` |
| `python3 scripts/check_doc_paths.py` | same | rc 0 | `14.*` |
| `python3 scripts/measure_naming.py --check` / `--selftest` | same | rc 0 / rc 0 | `15.*`, `16.*` |
| `python3 scripts/check_py_idiom.py` (before) | `764d1253` / `9abb41f` | rc 1: `FAIL: long function 10 > ratchet 9` | `receipts/parent-py-idiom-764d1253/` |
| ROM digests `./syn/yosys/ooc.sh --record-rom-digests` | `73dd3db7` → `10bb22af` | rc 0; the same contents as the `9abb41f` rows | the `10bb22af` diff (two rows) |

Carried from [A691]'s gate at pin `764d1253` (gitlink `9abb41f`; `receipts/prior-9abb41f/parent/`, table in
`HANDOFF-9abb41f.md` §5). `e9272b5` changes only a processor test-driver Python file. In the parent, only the static
scanners above read it, and they were re-run.

| Consumer gate (pin `764d1253`) | Result |
|---|---|
| static: `lint_rtl.py --check --self-test`, port contracts, wire accountability, SV idiom, RTL source lists, behave, yosys elaboration, `xvlog_gate.py --check` | all rc 0 |
| full default sweep (4 shards; shard 2 per suite and `capture_coherence` in CI piece form) + `suite_tally.py --expect-suite-root tb/verilator` | rc 0; 64 suites exactly once; 2,190,635 checks, 0 failures |
| milan_dp `[GSI]` leg base vs head | rc 0 both; 461 checks; 234 `[GSI]` lines identical |
| `make -C tb/verilator/milan_dp gsi-mutants` | rc 0; 11 of 11 caught |
| `./syn/yosys/ooc.sh KL_pp_shadow` head / base | rc 0 / rc 0; +664 LUT (+1.1%), +12 FF |

## 6. Completion

Task done exactly: the long function is split (§2 row 7), and both parent idiom gates pass with this head as the
gitlink and the patch applied (§5). The gsi driver still kills every arm (29 of 29, unchanged), `make check` passed (§4), and the handoff
and PR body are updated, with both idiom gates in the consumer table. Acceptance for #206 is as at `9abb41f` (items 1-4, `HANDOFF-9abb41f.md` §6), so `PR-BODY.md`
keeps "Closes #206".

No push, PR creation or edit, merge, rebase, sub-agent, hardware or bench access, flashing, or top-level interface
change. On issue #206 this continuation posted only TAKEN, plus REVIEW READY at the end.

Resources: the lane unit stayed at or under 7.1 GiB through the counted campaign (sampled every 5 s,
`receipts/campaigns/gsi-e9272b5/MEMORY.txt`). A first `--jobs 4` launch reached 8.7 GiB and was stopped on memory
(`VOID.md`). Host MemAvailable stayed above 55 GB. No sweep or route was run.

## 7. Receipts

`INDEX.md` is generated from the files present (a hash-and-size listing script kept outside this directory).
Receipts carry no host paths: the `make check` log's one path line is normalized to `<work>`.
