[A595] One AECP command model: generate F06.14 and the µcode's dispatch data from it, gate every other consumer against it

Closes #73

## What this changes

- **The command table.** `hdl/aecp/ucode/aecp_commands.json` (schema
  `aecp-command-table/1`) has one row per command the AECP engine serves: 30 AEM
  commands and MVU GET_MILAN_INFO. Each row carries the opcode and the engine constant
  that decodes it, the command and response sizes as `control_data_length`, the status
  set, the F03.7 hazard class, the lock, notify, GET_DYNAMIC_INFO and oversize flags, and
  the µPC programs the engine dispatches the command to. The table also holds the
  Table 7-141 status codes, the hazard-class codes, the statuses every command of a
  message type can answer, and the F06.14 rows of the commands the engine does not serve.
- **Generated from it.**
  - F06.14: `python3 scripts/check_aecp_commands.py --write` rewrites the rows between
    the markers in 06 section 6.
  - `hdl/aecp/ucode/gen_ucode.py` reads three things from the table when it generates
    the ROM: its status codes, the MVU command_type, and `DISPATCH`, which maps each
    command to its programs. Generation stops if the table names a program that was
    never placed.
- **Gated against it** by `scripts/check_aecp_commands.py`, as `make check` target
  `aecpcmd`, which CI's docs-gates job runs:
  - `KL_aecp_engine.sv`: its `OP_*_C`, `MVU_GET_MILAN_INFO_C` and `GDI_*_C` constants,
    `gdi_allowed`, every GET_DYNAMIC_INFO record length, the unsolicited
    kind-to-{command_type, body} map, and every `UPC_*_C` entry. These are checked in the
    manner of `check_upc_map.py`.
  - `protocol_processor_top.sv` `hz_classify`, and `pp_pkg`'s hazard codes.
  - `KL_pp_scoreboard.sv` `hz_is_lockprot`.
  - `KL_aecp_notify.sv`'s command-class map.
  - `ucpu_pkg.sv`'s status codes.
  - The generated µcode, walked path by path from every entry under the µCPU's own
    semantics. Exactly the lock-protected commands reach `CHECK_LOCK`. Each program
    enqueues the table's notification class. Every status a path can set is in the
    command's set, and every status in the set is reachable. Every response and
    unsolicited body has the table's size. No path runs into the ROM fill.
  - 06 section 8.1.

  Every failure line names the command and the consumer that disagree. An unreadable
  input or a pattern that parses nothing refuses with exit 2. The self-test runs first in
  `aecpcmd`. It plants 89 defects, one for every finding the gate can print and one for
  every refusal, and requires each to be caught by name.
- **Why the RTL is gated, not generated.** The elaborated engine and every ROM stay
  byte-identical. The reference platform's AECP inventory gate and
  `check_m9_opcodes.py` both read the `OP_*_C` lines, and the reviewed mutation patches
  under `tb/` anchor on the generator's and the engine's own lines. 09 section 8.10
  records this, along with what is still hand-written: the µprograms and ROM layout, the
  engine's command-length floors, the ACMP transition ROM, the descriptor image, F05.3,
  F08.1 and the `tb/` reference models. There is no golden model and no stimulus
  generator.
- **Docs.** The REQ-VER-002 Cov and Arch cells, 09 sections 1, 7 and 8 (new 8.10) and
  06 section 8 record what is generated and what is hand-written. The Cov cell keeps the
  original-document grade A and adds "the tree: P, per Arch".
- **Drift the gate found, fixed in the docs only:**
  - F06.14 gave SET/GET_SAMPLING_RATE and SET/GET_CLOCK_SOURCE 36 B; the engine
    answers 32 B (cdl 20).
  - F06.14 gave GET_AUDIO_MAP 32 + 8·N; the engine answers 36 + 8·N (cdl 24 + 8·N).
  - 06 section 8.1 had no SET/GET_NAME row.
- **Export for the parent.** The Mark II firmware tables are to consume the table itself:
  `protocol-processor/hdl/aecp/ucode/aecp_commands.json`, JSON, schema tag
  `aecp-command-table/1`, one `commands` row per served command. The parent gate is a
  follow-up lane.
- **Known limitation, recorded in 09 section 8.10.** The `tb/pp_top` and `tb/ucpu` build
  rules list `gen_ucode.py` alone as `ucode.hex`'s prerequisite. After an edit to the
  table alone, run `make clean` in those suites before building again; CI builds from a
  fresh checkout. Adding the table to those rules is a follow-up.

No register-map change, no top-level port or parameter change, and no `.sv` file
changes.

## Validation

Base is main `2cbed0a9`, head is `39cac06`. Verilator 5.050 is the CI pin. The portability
gate ran with sv2v v0.0.12 and Yosys 0.66. The base and head records were taken in the
same checkout, with every rc 0 and no output piped.

| Record | Command | base | head | identical |
|---|---|---|---|---|
| suites | `./scripts/run_suites.sh` (Verilator only on PATH, as in CI) | 0, `suites: 1029620 checks total, 0 failing` | 0, same | byte-identical (38 lines) |
| lint | `./scripts/lint_hdl.sh` | 0 | 0 | byte-identical |
| docs gates | `make check` | 0 | 0 | yes, apart from what this PR adds: `links: 1187` -> `1188` (09 section 8.10's new `#fig-09-env` link), `ids: 563 files` -> `564` (the new table under `hdl/`), and the two `aecpcmd` lines `aecp commands selftest: 89 planted defects, 89 caught by name, OK` and `aecp commands: 31 commands, 84 entries walked, F06.14 41 rows, OK` |
| matrix | `python3 scripts/gen_matrix.py --check` | 0, `matrix: OK (94 rows, 0 untested)` | 0, same | byte-identical |
| portability | `./syn/yosys/run.sh` | 0 | 0 | byte-identical (42 tops; the synth_xilinx statistics include `KL_aecp_engine` and its ROM) |

**Generated ROMs.** These were generated from exports of each commit:

| Image | base | head |
|---|---|---|
| `ucode.hex` | `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` | same, byte-identical |
| `ltn_rom.hex` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` | same, byte-identical |

No `.sv` file changes and `ucode.hex` is byte-identical, so the elaborated engine is
unchanged. The portability record above shows the same.

**Planted drifts.** Each drift was planted in an export of the head. The gate exits 1 and
`make aecpcmd` exits 2. Each export passes before its drift is planted.

| Drift | The gate's words |
|---|---|
| an opcode renumbered in the table only (GET_SAMPLING_RATE 0x0015 -> 0x001E) | `engine: GET_SAMPLING_RATE: the table says opcode 0x001E, hdl/aecp/KL_aecp_engine.sv OP_GET_SAMP_RATE_C = 0x0015` (plus the classifier, F06.14 and 8.1 lines) |
| a size changed in the doc table only (F06.14 0x0015 Resp. size -> 36 B (cdl 24)) | `F06.14: row 0x0015 GET_SAMPLING_RATE, column Resp. size, reads '36 B (cdl 24)' where the table gives '32 B (cdl 20)'` |
| an `OP_*_C` changed in the RTL only (OP_GET_SAMP_RATE_C -> 16'h001E) | `engine: GET_SAMPLING_RATE: the table says opcode 0x0015, hdl/aecp/KL_aecp_engine.sv OP_GET_SAMP_RATE_C = 0x001E` |
| a command missing from the table (GET_AS_PATH) | `engine: hdl/aecp/KL_aecp_engine.sv decodes OP_GET_AS_PATH_C = 0x0028 and the table has no command for it` (plus the entry, unsolicited, classifier, F06.14 and 8.1 lines) |
| ROM data changed in the generator only (SET_CLOCK_SOURCE's NOTIFY_ENQ 8 -> 5) | `rom: SET_CLOCK_SOURCE: its programs enqueue notification class [5], the table says [8]` |
| a size changed in the table only (GET_CLOCK_SOURCE response cdl 20 -> 24) | `engine: GET_CLOCK_SOURCE: its GET_DYNAMIC_INFO record is 8 bytes, the table's response is cdl 24 (12 bytes)`, `rom: GET_CLOCK_SOURCE: E_GCLKS answers SUCCESS at cdl 20, the table's response is 24`, and the F06.14 cell |
| a status code changed in the table only (NO_RESOURCES 8 -> 9) | `status: NO_RESOURCES is 9 in the table and ST_NO_RESOURCES_C = 8 in hdl/aecp/ucpu_pkg.sv` |

**Mutation campaigns.** These are every campaign that builds the µcode generator, run at
base and at head. The base runs used `--jobs 2` and the head runs used `--jobs 2`, except d3,
which used `--jobs 1`.

| Campaign | base | head | identical |
|---|---|---|---|
| `python3 tb/pp_top/aecp_dispatch_mutants.py --output OUT --verilator verilator --jobs 2` | 0 | 0 | log byte-identical; results identical |
| `python3 tb/pp_top/aecp_mutants.py --output OUT --jobs 2` | 0 | 0 | log byte-identical |
| `python3 tb/pp_top/ctr_mutants.py --output OUT --jobs 2` | 0 | 0 | log byte-identical |
| `python3 tb/pp_top/notify_mutants.py --output OUT --verilator verilator --jobs 2` | 0, `93 of 93 KILLED` | 0, same | same lines (the driver prints in completion order); results identical |
| `python3 tb/pp_top/gsi_mutants.py --output OUT --verilator verilator --jobs 2` | 0 | 0 | log byte-identical; results identical |
| `python3 tb/pp_top/acmp_mutants.py --output OUT --verilator verilator --jobs 2` | 0, `51 of 51 KILLED` | 0, same | same lines (completion order); results identical |
| `python3 tb/pp_top/name_wr_mutant.py --output OUT` | 0 | 0 | log byte-identical; results identical |
| `python3 tb/name_state/mutants.py --output OUT --verilator verilator --jobs 2` | 0 | 0 | same lines (completion order); results identical |
| `python3 tb/pp_top/d3_mutants.py --output OUT --verilator verilator` | 0, `D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS` | 0, same | same lines (completion order); results identical |

Every `tb/` mutation patch that edits `gen_ucode.py` still applies (`git apply --check`).

**Scratch parent.** milan-fpga dev `e8454e27`, with the `protocol-processor` gitlink
staged at the head:

| Gate | gitlink at base | gitlink at head |
|---|---|---|
| `cd tests && python3 -m behave --no-capture -f plain`, AECP tier included ("the served inventory matches the opcodes the engine RTL decodes") | 0, 404 scenarios passed | 0, same (identical apart from timings) |
| `python3 scripts/check_feature_status.py --self-test` | 0 | 0, byte-identical |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0, byte-identical |
| `syn/yosys/ooc.sh --record-rom-digests`, then `syn/yosys/ooc.sh tcam` | 0, 0 | 0, 0 |

The recorded ROM rows at the head pin match the ledger's rows for the parent's current
pin. The ledger was re-recorded only in the scratch copy and then restored.
