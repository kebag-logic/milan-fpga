# [A595] HANDOFF - processor #73, one AECP command model

Status: REVIEW READY at head 39cac06 (posted on #73 as comment 6104386579). Every acceptance item of #73 and every proof item
of the lane comment is met (see the tables below). Resumed 2026-10-10 21:34 after an
external usage-limit stop at 21:06; no gate had failed. TAKEN was posted once (comment
6100517434) and is not repeated.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: pp73-command-model (local only; never pushed)
- Base: main 2cbed0a987c1e68402658d69459ab7e5aa571adc
- Head: 39cac060f6f3730cf8172adc6424c275cd268517

## Commits (one-line subjects, configured identity)

| Commit | Subject |
|---|---|
| 6433bdc | Take the µcode status codes, MVU command type and dispatch map from one AECP command table |
| b96268c | Generate F06.14 from the AECP command table and gate every engine, ROM and doc consumer against it |
| 3b6b049 | Run the AECP command gate in make check and so in the CI docs-gates job |
| 7053ccd | Record what the AECP command table generates and gates in REQ-VER-002, 06 section 8 and 09 sections 7 and 8 |
| 67bf163 | Drop unused gate fields and refuse a message type the table cannot render |
| 39cac06 | Plant a defect for every finding and refusal of the AECP command gate, and record the suites' ucode.hex prerequisite |

Files changed against base: `hdl/aecp/ucode/aecp_commands.json` (new),
`scripts/check_aecp_commands.py` (new), `hdl/aecp/ucode/gen_ucode.py`, `Makefile`,
`.github/workflows/hdl.yml`, `docs/00_MILAN_COMPLIANCE_REVIEW.md`,
`docs/architecture/06_aecp_engine.md`, `docs/architecture/09_verification.md`. No `.sv`,
`.svh`, `.v`, `.hex`, `.tcl` or `.xdc` file changes (`git diff --stat 2cbed0a..HEAD -- '*.sv'
'*.svh' '*.v' '*.vh' '*.hex' '*.mem' '*.tcl' '*.xdc'` is empty). No register-map, top-level
port or parameter change.

## The command table

`hdl/aecp/ucode/aecp_commands.json` (24555 B, sha256
8aabc52ce6841bab0744227fcdf041184bf3177e02b0769d15a9ad1c3ac88e1a), schema
`aecp-command-table/1`, 31 served commands (30 AEM + MVU GET_MILAN_INFO). Per command:
name, message, opcode, engine constant (`rtl`), clause, command and response sizes as cdl
(fixed, `per` N records, `plus` descriptor/records, `echo`, failure `stub`, engine-built),
status set, hazard class, lock, notify (`class` the µprogram enqueues, or null for an engine
event; unsolicited `kind`; `body` program), GDI and oversize flags, µPC `entries` (success
program first), F06.14 prose. Top level: Table 7-141 status codes (with their `ucpu_pkg`
names), hazard-class codes, `common_status` per message type (AEM ENTITY_MISBEHAVING, MVU
NOT_IMPLEMENTED), the shared echo programs, the shared entries, and the F06.14 rows of
unserved commands.

## Consumers: generated or gated (file:line at head 39cac06)

Gate = `scripts/check_aecp_commands.py`; `make check` target `aecpcmd` (Makefile:48) runs
`--selftest` (:1351) and then the gate.

| Consumer | Form | Where | Gate check |
|---|---|---|---|
| F06.14 rows | generated (`--write`, :1378) | docs/architecture/06_aecp_engine.md:247-291 (markers) | check_doc :845 (rows :800, render :824) |
| status codes ST_* | generated (read at ROM generation) | hdl/aecp/ucode/gen_ucode.py:42-53 | the ROM walk maps every status a path sets to the table, check_rom :699 |
| MVU command_type | generated | hdl/aecp/ucode/gen_ucode.py:141 | ROM byte identity (digest below) |
| DISPATCH (command -> entries -> address) | generated; generation asserts each entry is a placed program | hdl/aecp/ucode/gen_ucode.py:2438 | check_rom :699 compares it to the table |
| OP_*_C, MVU_GET_MILAN_INFO_C, GDI_*_C | hand-written, gated | hdl/aecp/KL_aecp_engine.sv:698-827 | check_engine :506 |
| gdi_allowed | hand-written, gated | hdl/aecp/KL_aecp_engine.sv:1090 | check_engine :506 |
| GET_DYNAMIC_INFO record lengths and UPCs | hand-written, gated | hdl/aecp/KL_aecp_engine.sv:1111 | check_engine :506 |
| uns_kind_map (kind -> command_type, body) | hand-written, gated | hdl/aecp/KL_aecp_engine.sv:1404 | check_engine :506 |
| UPC_*_C entries (claimed by command, body or shared list) | hand-written, gated | hdl/aecp/KL_aecp_engine.sv:838-923 | check_engine :506 (addresses: check_upc_map.py) |
| hz_classify (opcode -> class) | hand-written, gated | hdl/top/protocol_processor_top.sv:1645 | check_classifier :599 |
| PP_HZ_* codes | hand-written, gated | hdl/common/pp_pkg.sv:53-61 | check_classifier :599 |
| hz_is_lockprot | hand-written, gated | hdl/packet_engine/KL_pp_scoreboard.sv:112 | check_scoreboard :624 |
| notify class -> kind, queued classes | hand-written, gated | hdl/aecp/KL_aecp_notify.sv:597, :834 | check_notify :633 |
| ST_*_C | hand-written, gated | hdl/aecp/ucpu_pkg.sv:106-119 | check_status_codes :657 |
| the µprograms (lock, notify class, status set, sizes, fill) | hand-written, gated on the generated ROM | hdl/aecp/ucode/gen_ucode.py (programs) | walk :310, check_rom :699 |
| 06 §8.1 inventory | hand-written, gated | docs/architecture/06_aecp_engine.md:1210 | check_inventory :875 |
| the table's own shape | - | hdl/aecp/ucode/aecp_commands.json | check_schema :448 |
| make check | wiring | Makefile:15, :48 | `aecpcmd` (self-test, then gate) |
| CI | wiring | .github/workflows/hdl.yml:30-35 (docs-gates job runs `make check`) | |
| REQ-VER-002, 09 §1/§7/§8.10 | docs | docs/00_MILAN_COMPLIANCE_REVIEW.md:535; docs/architecture/09_verification.md:29, :127, :135, :458 | |

Why the RTL is gated and not generated (recorded in 09 §8.10): the elaborated engine and
every ROM stay byte-identical; the parent's AECP inventory gate and `check_m9_opcodes.py`
read the `OP_*_C` lines; the reviewed mutation patches under `tb/` anchor on the
generator's and the engine's own lines.

## Findings the gate made on the base tree (fixed in the docs, RTL untouched)

- F06.14 gave SET/GET_SAMPLING_RATE and SET/GET_CLOCK_SOURCE "36 B"; the engine answers
  32 B (cdl 20): tb/pp_top W9b/W10 grade cdl 20, and the parent model's SERVED says 20.
- F06.14 gave GET_AUDIO_MAP "32 + 8·N"; the engine answers 36 + 8·N B (cdl 24 + 8·N, as
  06 §8.1 and gen_ucode.py:876 say).
- 06 §8.1 ("what it answers today") had no SET_NAME / GET_NAME row; both are served.
- UPC_NAMEERR_C is declared in the engine and never dispatched (a branch target of the
  name programs); recorded as a shared entry rather than claimed by a command.

## Known limitation (recorded in 09 §8.10, not changed: outside this lane's file scope)

`tb/pp_top/Makefile:236` and `tb/ucpu/Makefile:20` list `gen_ucode.py` alone as
`ucode.hex`'s prerequisite. After an edit to the table alone, an incremental build there
keeps the old ROM until `make clean`; CI builds from a fresh checkout. Changing those
Makefiles is a follow-up (they are suite build files, and the head campaigns copy
`tb/pp_top`).

## Planted drifts (at head)

Each applied to a fresh `git archive` export of the head 39cac06 under the scratch
directory (never committed); the export first passes unplanted (rc 0), then the planted
gate `python3 -B scripts/check_aecp_commands.py` exits 1 and `make aecpcmd` exits 2 (its
self-test stops first, because its precondition, a passing tree, fails, and prints the
same lines). The same seven drifts at 67bf163 gave byte-identical gate output; only
make's own `Makefile:48` became `Makefile:49` (the comment above the target grew a line).

| # | Drift | Failing gate words (verbatim) |
|---|---|---|
| 1 | an opcode renumbered in the table only (GET_SAMPLING_RATE 0x0015 -> 0x001E) | `engine: GET_SAMPLING_RATE: the table says opcode 0x001E, hdl/aecp/KL_aecp_engine.sv OP_GET_SAMP_RATE_C = 0x0015`; also `classifier: hdl/top/protocol_processor_top.sv hz_classify names 0x0015, which no table command carries`, `F06.14: row 0x001E GET_SAMPLING_RATE is missing (run --write)`, `F06.14: row 0x0015 GET_SAMPLING_RATE is not in the table`, `8.1: GET_SAMPLING_RATE (AEM 0x001E) is served and section 8.1 does not list it`, `8.1: section 8.1 lists AEM 0x0015 and the table serves no such command` |
| 2 | a size changed in the doc table only (F06.14 row 0x0015 Resp. size 32 B (cdl 20) -> 36 B (cdl 24)) | `F06.14: row 0x0015 GET_SAMPLING_RATE, column Resp. size, reads '36 B (cdl 24)' where the table gives '32 B (cdl 20)'` |
| 3 | an OP_*_C changed in the RTL only (OP_GET_SAMP_RATE_C 16'h0015 -> 16'h001E) | `engine: GET_SAMPLING_RATE: the table says opcode 0x0015, hdl/aecp/KL_aecp_engine.sv OP_GET_SAMP_RATE_C = 0x001E` |
| 4 | a command missing from the table (the GET_AS_PATH row deleted) | `engine: hdl/aecp/KL_aecp_engine.sv decodes OP_GET_AS_PATH_C = 0x0028 and the table has no command for it`; also `engine: UPC_GASP_C is claimed by no command, notification body or shared entry of the table`, `engine: uns_kind_map's PP_UNS_ASP_C arm is no command's notification`, `classifier: hdl/top/protocol_processor_top.sv hz_classify names 0x0028, which no table command carries`, `F06.14: 41 rows where the table generates 40`, `F06.14: row 0x0028 GET_AS_PATH is not in the table`, `8.1: section 8.1 lists AEM 0x0028 and the table serves no such command` |
| 5 | ROM data changed in the generator only (SET_CLOCK_SOURCE's NOTIFY_ENQ imm 8 -> 5) | `rom: SET_CLOCK_SOURCE: its programs enqueue notification class [5], the table says [8]` |
| 6 | a size changed in the table only (GET_CLOCK_SOURCE response cdl 20 -> 24) | `engine: GET_CLOCK_SOURCE: its GET_DYNAMIC_INFO record is 8 bytes, the table's response is cdl 24 (12 bytes)`; `rom: GET_CLOCK_SOURCE: E_GCLKS answers SUCCESS at cdl 20, the table's response is 24` (and its NO_SUCH_DESCRIPTOR, BAD_ARGUMENTS and E_TIZ4NS NOT_SUPPORTED arms); `F06.14: row 0x0017 GET_CLOCK_SOURCE, column Resp. size, reads '32 B (cdl 20)' where the table gives '36 B (cdl 24)'` |
| 7 | a status code changed in the table only, which the generator reads (NO_RESOURCES 8 -> 9) | `status: NO_RESOURCES is 9 in the table and ST_NO_RESOURCES_C = 8 in hdl/aecp/ucpu_pkg.sv` |

The self-test (`--selftest`, first in `make aecpcmd`) plants 89 defects, one for every
finding the gate can print and for every refusal (85 in memory, 4 in a temporary copy of
the input files: a table that is not JSON, an unreadable input, a generator that does not
run, a generator of another shape), and requires each caught by name:
`aecp commands selftest: 89 planted defects, 89 caught by name, OK`. A check that a wrong
expectation is reported as missed passes too (scratch probe, not committed).

## ROM digests and record identity (base vs head)

Generated from `git archive` exports of each commit in scratch.

| Image | base 2cbed0a9 | head 39cac06 | identical |
|---|---|---|---|
| ucode.hex (26624 B) | 518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8 | 518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8 | yes (cmp) |
| ltn_rom.hex (6138 B) | 23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956 | 23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956 | yes (cmp) |
| descriptor image, milan_min (3224 B; 67bf163, generator untouched since) | 11d6491b7f16642392961a0c2c9c04a91dfeab9b626169cac3a32b6c0843a8fb | 11d6491b7f16642392961a0c2c9c04a91dfeab9b626169cac3a32b6c0843a8fb | yes |

Both ROM digests equal the parent ledger's rows for its current pin 2ad2f845, and the
scratch parent's `ooc.sh --record-rom-digests` with the gitlink at 39cac06 recorded the
same two digests. Elaborated engine: no `.sv` input changed (`git diff --stat 2cbed0a..HEAD
-- '*.sv' '*.svh'` is empty), its `$readmemh` image `ucode.hex` is byte-identical, and the
`syn/yosys/run.sh` record (which elaborates and synthesises `KL_aecp_engine`) is
byte-identical at base and head.

## Parent export

The parent's Mark II firmware tables are to consume the table itself: superproject path
`protocol-processor/hdl/aecp/ucode/aecp_commands.json`, JSON, `"schema":
"aecp-command-table/1"`, one `commands[]` row per served command (fields as above). The
parent gate is a follow-up lane after this merges.

## Toolchain identities

- Verilator 5.050 (2026-07-01 rev v5.050), the pinned wrapper
  $VALIDATION_TOOLS/pinned-verilator-5.050/verilator, exported for every run (host default
  5.052 never used).
- sv2v v0.0.12: binary sha256 b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b
  (the release zip sha256 ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00).
- Yosys 0.66 (git sha1 86f2ddebc-dirty, distribution package 0.66-1), binary sha256
  ec566d8fbb0d24e09ce7ab4e86c55c7169f24097d90611ee354b446925f36b5b.
- Neither sv2v nor Yosys is under $VALIDATION_TOOLS as the brief says (re-checked on resume:
  `find $VALIDATION_TOOLS -iname '*sv2v*' -o -iname '*yosys*'` finds only Verilator's own
  test files). The host's copies were used and are identified above. The CI portability job
  installs the distribution Yosys and sv2v "latest", not a pinned release.

## Suites (base and head in the same directory: the scratch parent's processor submodule)

| Record | Command | Toolchain on PATH | base rc / summary | head rc / summary | identical |
|---|---|---|---|---|---|
| suites | `./scripts/run_suites.sh` | Verilator 5.050 only (the CI suites job's) | 0, `suites: 1029620 checks total, 0 failing` | 0, same (02:16) | byte-identical (38 lines, the UPC map and M9 gates included) |
| lint | `./scripts/lint_hdl.sh` | Verilator 5.050 | 0 (41 lines) | 0 | byte-identical |
| docs gate | `make check` | mmdc 11.16.0, WaveDrom venv | 0 | 0 | identical except what the change adds: `links: 1187` -> `1188` (09 §8.10's new `#fig-09-env` link), `ids: 563 files` -> `564` (the new table under `hdl/`), and the two new `aecpcmd` lines `aecp commands selftest: 89 planted defects, 89 caught by name, OK` and `aecp commands: 31 commands, 84 entries walked, F06.14 41 rows, OK` |
| matrix | `python3 scripts/gen_matrix.py --check` | - | 0, `matrix: OK (94 rows, 0 untested)` | 0, same | byte-identical |
| portability | `./syn/yosys/run.sh` | sv2v v0.0.12, Yosys 0.66 | 0 (71 lines, 42 tops) | 0 | byte-identical (every top's elaboration and the synth_xilinx statistics, KL_aecp_engine and its ROM included) |

The head records were produced at 01:46-01:49 on 2026-10-11 by a chain started once base
d3 had passed: the submodule fetched the lane's branch and checked out 39cac06 detached,
and `git clean -fdX -- tb hdl syn scripts docs` removed the base runs' build products
(the WaveDrom venv at the root kept). A preview of lint, matrix and Yosys in the lane
checkout at 23:10 on 2026-10-10 gave the same bytes.

Pre-existing, toolchain-dependent, not this lane's: with sv2v v0.0.12 on PATH,
`tb/nvm_port`'s optional Yosys arm (`elab_bounds.sh`, run by its `make`) fails at base:
`YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the guard's $finish` (sv2v 0.0.12 lowers
`$fatal` so that Yosys 0.66 stops with `ERROR: FATAL: .` instead of the `$finish` the arm
greps for). sv2v v0.0.13 passes that arm, and CI's suites job has no sv2v at all, so the
arm SKIPs there. The suites are therefore recorded with the CI suites job's toolchain
(Verilator only) at both base and head.

## Campaigns (every campaign that builds the changed generator)

Every driver copies `hdl/`, `tb/common` and its suite into a private temporary tree, so
`aecp_commands.json` travels with `gen_ucode.py`. Base ran in the scratch submodule at
2cbed0a9, head in the lane checkout (which stayed clean: `git status --porcelain --ignored`
empty); the stdout logs carry no paths. The head runs other than d3 started at 67bf163;
`git diff --stat 67bf163 39cac06 -- hdl tb` is empty, so every campaign input is the head's.
Memory: each Verilator build runs its own `make -j 16`; this unit peaked at the 12 GB cap
once (see d3) and otherwise at 9.2 GB.
All `tb/` mutation patches that touch `gen_ucode.py` apply at head (`git apply --check`).

| Campaign | Command | base rc / tally | head rc / tally | identical |
|---|---|---|---|---|
| aecp_dispatch | `python3 tb/pp_top/aecp_dispatch_mutants.py --output OUT --verilator verilator --jobs 2` | 0 | 0 | log byte-identical (275 lines); results.json identical |
| aecp | `python3 tb/pp_top/aecp_mutants.py --output OUT --jobs 2` | 0 | 0 | log byte-identical (700 lines) |
| ctr | `python3 tb/pp_top/ctr_mutants.py --output OUT --jobs 2` | 0 | 0 | log byte-identical (113 lines) |
| notify | `python3 tb/pp_top/notify_mutants.py --output OUT --verilator verilator --jobs 2` | 0, `C6 notification mutations: 93 of 93 KILLED by their named checks; goldens PASS` | 0, same | log identical as a sorted multiset (107 lines; the driver prints in completion order); results.json identical sorted |
| gsi | `python3 tb/pp_top/gsi_mutants.py --output OUT --verilator verilator --jobs 2` | 0 | 0 | log byte-identical (23 lines); results.json identical sorted |
| acmp | `python3 tb/pp_top/acmp_mutants.py --output OUT --verilator verilator --jobs 2` | 0, `ACMP mutations: 51 of 51 KILLED by their named checks; goldens PASS` | 0, same | log identical as a sorted multiset (58 lines; completion order); results.json identical sorted |
| name_wr | `python3 tb/pp_top/name_wr_mutant.py --output OUT` | 0, `Name-write mutation: decode killed; golden and restored PASS` | 0, same | log byte-identical (4 lines); results.json identical |
| name_state | `python3 tb/name_state/mutants.py --output OUT --verilator verilator --jobs 2` | 0 | 0 | log identical as a sorted multiset (17 lines; completion order); results.json identical sorted |
| d3 | `python3 tb/pp_top/d3_mutants.py --output OUT --verilator verilator --jobs N` (base N = 2, head N = 1) | 0, `D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS` (00:04-01:46) | 0, same (00:36-03:53) | log identical as a sorted multiset (117 lines; completion order); results.json identical sorted |

d3 history, all recorded in `campaigns.meta`: the first d3 runs (base from 23:22, head from
23:33) were both ended by an external SIGTERM at the same second, 00:03:16 (rc 143 on both
sides; only the python drivers were signalled, their parent shells exited normally; no OOM
event in this unit; nothing in this session sent it). Before the signal every golden printed
PASS and every mutant verdict was KILLED (34 base, 24 head); the partial logs are kept as
`d3-sigterm-0003.log`. Both were re-run from the start at 00:04. With both sides' goldens
building at once this unit's memory reached its 12 GB cap (`memory.events` max 2759, swap
absorbed it, `oom_kill` 0), so this session stopped the head re-run at 00:15 and started it
again at 00:36 with `--jobs 1` beside base. A later restart with more jobs was not made (the
command was refused), so the head record above is the uninterrupted `--jobs 1` run.

Every campaign: base rc 0 and head rc 0. `bin/compare_camp.py` in scratch compares each
stdout log byte for byte and as a sorted multiset, and each results.json with its records
sorted and the random temporary-tree paths removed. Per-trial build logs are not records:
they carry that path and make's interleaving.

## Scratch parent

kebag-logic/milan-fpga dev e8454e2751d05b02ee8e5a571857589ab358ab86, cloned under the
scratch directory; never committed or pushed. Gates run with the `protocol-processor`
gitlink staged at the submodule's checkout.

| Gate | Command | base (gitlink 2cbed0a9) | head (gitlink 39cac06) | identical |
|---|---|---|---|---|
| BDD tiers, AECP included (`aecp_response_contract.feature`: "the served inventory matches the opcodes the engine RTL decodes", "the served MVU inventory matches the MVU command types the engine RTL decodes") | `cd tests && python3 -m behave --no-capture -f plain` | 0, `14 features passed, 0 failed, 0 skipped`, `404 scenarios passed` | 0, same | yes apart from per-step timings (2840 lines) |
| feature status self-test | `python3 scripts/check_feature_status.py --self-test` | 0 | 0 | byte-identical |
| processor source list | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 | byte-identical |
| ROM-digest ledger, record at the pin | `syn/yosys/ooc.sh --record-rom-digests` | 0; rows for 2cbed0a9: ltn_rom.hex 23cc67ee..., ucode.hex 518b900c... | 0; rows for 39cac06: ltn_rom.hex 23cc67ee..., ucode.hex 518b900c... | yes; both equal the rows of the parent's current pin 2ad2f845 |
| ROM-digest verify | `syn/yosys/ooc.sh tcam` | 0 | 0 | byte-identical |

Identity at head: parent HEAD e8454e2751d05b02ee8e5a571857589ab358ab86, staged gitlink
39cac060f6f3730cf8172adc6424c275cd268517, submodule HEAD 39cac06, gptp gitlink 5dce647. The
ledger is re-recorded for the staged pin in scratch (the ledger refuses an unrecorded pin,
by design) and restored by `git checkout` afterwards; the parent's gates themselves are
unchanged. `git status --short` in the parent after the run: `M  protocol-processor`
(the staged gitlink) only.

The scratch parent was cloned at dev e8454e27 (resolved with `git rev-parse`) and is left
with its submodule checked out at 39cac06 and the gitlink staged there; nothing in it was
committed or pushed. Before every git command in the submodule its
`git rev-parse --show-toplevel` was checked to be that directory.

## Not used, and follow-ups

- Vivado was not needed by any gate of this lane and was not run (so the lock was never
  taken). No hardware, bench, push, PR or rebase.
- Follow-up: add `aecp_commands.json` to the `ucode.hex` prerequisites in
  `tb/pp_top/Makefile` and `tb/ucpu/Makefile` (outside this lane's file scope; recorded in
  09 §8.10).
- Follow-up (parent): the parent gate that holds the Mark II firmware's AECP tables to
  `protocol-processor/hdl/aecp/ucode/aecp_commands.json`.
- Observation, not this lane's: CI's portability job installs sv2v "latest" rather than a
  pinned release; the records here used v0.0.12.

## Scratch locations (not in the tree, not in this directory)

Records under the scratch directory $VALIDATION_STORAGE/pp73-a595: `logs/` (base-* and head-*
logs, rc and meta files, chain.log, memsample.log), `camp/{base,head}/` (campaign logs, rc
files, outputs, campaigns.meta), `pgates/{base,head}/`, `drifts-final/` (39cac06) and
`drifts-67bf163/`, `rom-base/`, `rom-final/`, and the helper scripts in `bin/`.
