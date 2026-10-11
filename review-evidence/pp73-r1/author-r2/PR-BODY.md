[A595]

One AECP command model: generate F06.14 and the µcode's status codes from it, hold the engine's observed decode and dispatch and every other consumer to it

Closes #73

## What this changes

- **The command table.** `hdl/aecp/ucode/aecp_commands.json` (schema
  `aecp-command-table/1`) has one row per command the AECP engine serves: 30 AEM
  commands and MVU GET_MILAN_INFO. Each row carries:
  - the opcode and the engine constant that decodes it;
  - the command and response sizes as `control_data_length`, with a `floor` where the
    engine accepts a shorter command;
  - the status set and the F03.7 hazard class;
  - the lock, notify, GET_DYNAMIC_INFO and oversize flags;
  - every µPC program the engine dispatches the command to, on any outcome.

  The table also holds the Table 7-141 status codes, the hazard-class codes, the statuses
  every command of a message type can answer, the program unserved commands reach, the
  F06.14 rows of the commands the engine does not serve, and a `fields` reference that
  separates the machine semantics from the F06.14 prose.
- **Generated from it.**
  - F06.14: `python3 scripts/check_aecp_commands.py --write` rewrites the rows between
    the markers in 06 section 6.
  - `hdl/aecp/ucode/gen_ucode.py` takes its status codes and the MVU command_type from
    the table. A field it cannot read stops it with a line naming the command and the
    field, and so does an entry that names a program it never placed. Its `DISPATCH`
    map selects no ROM word.
- **Observed and held to it: what the engine decodes and dispatches.** The new suite
  `tb/aecp_cmds` drives `KL_aecp_engine` alone and records the µPC it hands the µCPU and
  the response it sends. Every opcode 0x0000-0x007F gets the same sweep: every cdl 12-100,
  descriptor types 0x0000-0x0028 and 0xFFFF, idle and streaming, the other message types, MVU command_types
  under right and wrong protocol ids, GET_DYNAMIC_INFO records and unsolicited kinds.
  585760 trials take about 45 s.
  - Per served command: the programs its opcode reaches on every outcome, the MVU
    sub-decode included, are exactly its `entries`.
  - The shortest command dispatched to its first entry is its command cdl, or its declared
    `floor`.
  - A per-record command is accepted only at whole records.
  - Every response the bench saw has a status of the set and the table's size.
  - Every opcode the table does not serve reaches only `NOTIMPL`, on every message type
    swept.
  - The GET_DYNAMIC_INFO members, record lengths and empty aggregate, and every
    unsolicited job's command_type, body and size, are the table's.

  The suite holds a fresh sweep to the table and to its recorded copy
  `tb/aecp_cmds/decode.json`. `make check` holds the table to that file. The file carries
  the digest of every input the sweep was made of (the engine's SystemVerilog by its code,
  the bench, the image's inputs, the ROM), so an engine edit without a re-sweep fails
  `make check` by file name and the suite by command name. Nothing reads the decode or the
  dispatch off the engine's text. Fourteen standing controls, `make -C tb/aecp_cmds
  mutants` (CI's suites job), each plant one exact engine or generator edit and must fail
  by name. They include a redirected success arm and a decode keyed on another opcode.
- **Gated against it** by `scripts/check_aecp_commands.py` (entry point) and
  `scripts/aecp_gate/` (one module per consumer), as `make check` target `aecpcmd` in CI's
  docs-gates job:
  - `KL_aecp_engine.sv`'s declared `OP_*_C`, `MVU_GET_MILAN_INFO_C` and `GDI_*_C` values,
    and its `UPC_*_C` names;
  - `protocol_processor_top.sv` `hz_classify` and `pp_pkg`'s hazard codes;
  - `KL_pp_scoreboard.sv` `hz_is_lockprot`;
  - `KL_aecp_notify.sv`'s command-class map;
  - `ucpu_pkg.sv`'s status codes, and the table's codes against IEEE Table 7-141;
  - the generated µcode, walked path by path from every entry under the µCPU's own
    semantics. Exactly the lock-protected commands reach `CHECK_LOCK`, and each program
    enqueues the table's notification class. Every status a path can set is in the set,
    and every status in the set is reachable. No path runs into the fill. Every response
    and unsolicited body has the table's size:
    - a fixed rule and a failure stub exactly;
    - a per-record rule as its fixed part plus whole records, with some SUCCESS path
      building them;
    - a descriptor rule as a copy that starts at its fixed part;
  - an echo row's response size is its command size;
  - 06 section 8.1.

  Every failure line names the consumer, and the command that disagrees with it (or,
  where no command is involved, the opcode, the table field or the file). An unreadable
  input or a pattern that parses nothing refuses with exit 2. The self-test runs first.
  It plants 153 defects, one for every finding and every refusal. The table defects the
  generator reads are planted in a file copy, so that the generator re-runs on them. The
  self-test requires each defect to be caught by name.
- **Still hand-written and held to no table** (09 section 8.10, REQ-VER-002):
  - the µprograms' field values;
  - the ROM layout (held to the engine by `check_upc_map.py`);
  - ACQUIRE_ENTITY's and REGISTER_UNSOLICITED_NOTIFICATION's command cdl (the engine
    accepts both from 12, and only the echo rule ties them);
  - GET_DYNAMIC_INFO's 524 ceilings;
  - opcodes above 0x007F;
  - the ACMP transition ROM, the descriptor image, F05.3, F08.1 and the `tb/` reference
    models.

  There is no golden model and no stimulus generator.
- **Docs.** The REQ-VER-002 Cov and Arch cells, 09 sections 1, 7 and 8 (8.10) and 06
  section 8 record what is generated, observed, gated and still hand-written.
- **Drift found in the base tree, fixed in the docs only:**
  - F06.14 gave SET/GET_SAMPLING_RATE and SET/GET_CLOCK_SOURCE 36 B; the engine answers
    32 B (cdl 20).
  - F06.14 gave GET_AUDIO_MAP 32 + 8·N; the engine answers 36 + 8·N (cdl 24 + 8·N).
    GET_AUDIO_MAP's response cdl is now held by the ROM walk and by the sweep: cdl 20 or
    28 in the table fails by name.
  - 06 section 8.1 had no SET/GET_NAME row.
- **Build rules.** `tb/pp_top`, `tb/ucpu` and `tb/aecp_cmds` list the table beside
  `gen_ucode.py` as a `ucode.hex` prerequisite.
- **Export for the parent.** The Mark II firmware tables are to consume the table itself:
  `protocol-processor/hdl/aecp/ucode/aecp_commands.json`, JSON, schema tag
  `aecp-command-table/1`, one `commands` row per served command, with the fields described
  in its `fields` object. The parent gate is a follow-up lane.
- **Parent adaptation owed at the next adoption.** `tb/aecp_cmds/mutants.py` plants edits
  into a copy of the engine, so the parent's `scripts/measure_test_evidence.py` classifies
  it as a DUT-source reader and needs one disposition in
  `scripts/measure_test_evidence_readers.py`. The patch is in the lane evidence
  (`parent-aecp-cmds-evidence.patch`, sha256 `19d41c7b...`), the same kind of adaptation
  `parent-name-evidence.patch` is for `tb/name_state`.

No register-map change, no top-level port or parameter change, and no `.sv` change under
`hdl/` (the one new `.sv` is the `tb/aecp_cmds` testbench wrapper). Both ROMs are
byte-identical.

## Round 2

This round answers R608-1 and R609-1, both NEGATIVE at `39cac060`, and the manager's
addendum on the parent consumer's Python rule. It adds ten commits on `39cac060`, with no
rebase and no amend.

- **R608-1-F1 (decode and dispatch held to no table).** These are now held by behaviour:
  `tb/aecp_cmds`, `decode.json` and the standing controls, as above. R608-1's q1 and q2
  are standing controls. Re-applied with R608-1's own `drift_probes.py`, each fails
  `make check` by file name (`decode: tb/aecp_cmds/decode.json was swept from another
  hdl/aecp/KL_aecp_engine.sv ...`). In the same tree the suite fails it by command name:
  - q1: `decode: SET_CLOCK_SOURCE: the table's entries name SCLKS, which the engine never
    dispatches AEM 0x0016 to (the fresh sweep)`;
  - q2: `decode: GET_CLOCK_SOURCE: the engine dispatches AEM 0x0017 to SCLKS, which is not
    one of the table's entries (the fresh sweep)`.

  The table's `about`, 06 section 8, 09 section 8.10 and REQ-VER-002 no longer say the
  table drives the dispatch.
- **R609-1-F1 (10 response sizes and every command size held to nothing).**
  - The ROM walk keeps the fixed part where a loop widens it, and the copy start of a
    descriptor answer.
  - Echo rows' response cdl equals their command cdl.
  - Each command cdl is held to the engine's observed decode floor. Three commands
    declare `floor: 12`.
  - R609-1's `size_sweep.py`, unchanged, at the head: `response: 31 held by a consumer, 0
    held to the table alone` and `command: 31 held by a consumer, 0 held to the table
    alone`.
  - `rom_size_probe.py`, unchanged: every reachable NOP fails by name.
  - GET_AUDIO_MAP response cdl 20 and 28, with the doc regenerated, each fail by name; 24
    passes.
  - A NOPed header field in E_GAMAP, E_GAVB, E_GASP and E_RDESC is a self-test plant, and
    each fails by name.
- **R608-1-F2 (generator-read defects nameless).**
  - The schema check refuses them by command and field before the generator runs, and the
    generator refuses them itself with `SystemExit`, which holds under `python3 -O`
    (R608-1-S2 = R609-1-S3).
  - R608-1's p5e: `schema: GET_MILAN_INFO: message 'AAU' is neither AEM nor MVU`, rc 1.
  - R608-1's p8: `decode: GET_CLOCK_SOURCE: the table's entries name SCFGRUN2, ...` and
    `engine: GET_CLOCK_SOURCE: entry SCFGRUN2 has no UPC_SCFGRUN2_C, ...`, rc 1. The
    generator alone gives `aecp_commands.json: GET_CLOCK_SOURCE: entries names SCFGRUN2,
    and gen_ucode.py placed no E_SCFGRUN2 program`.
  - The self-test plants seven such defects in a file copy and five with the generator
    run alone.
- **F3 (doubled plurals).** Fixed and regenerated. `grep -c 'mappingss\|entriess'
  docs/architecture/06_aecp_engine.md` gives 0.
- **R608-1-F4 = R609-1-F2 (`ucode.hex` prerequisites).** Fixed in all three suites. After
  a build, touching the table makes `make -q ucode.hex` return 1 in `tb/pp_top`, `tb/ucpu`
  and `tb/aecp_cmds`.
- **Suggestions.** Taken:
  - the `fields` reference (R608-1-S1, R609-1-S4);
  - Table 7-141 held in the gate (R609-1-S1: STREAM_IS_RUNNING 12 -> 13 now fails);
  - a documented row without a name is a named schema finding (R609-1-S2).
- **Addendum (the parent's Rule 12 ratchets).** The 2374-line gate is now an entry point
  plus `scripts/aecp_gate/`. No module is over 1000 lines, no function over 100, none
  takes more than six parameters, and every public function is annotated and documented.
  - The split changes no output: a harness ran the pre-split gate and the package on every
    plant, on the `--observed` verdict, on the record text it writes and on `--write`.
    The outputs are identical once the random temporary-directory names are masked.
  - The new bench's C++ also meets the parent's Rule 11 gate (no multi-declarator lines).
  - At the parent's consumer dev `ac2c5e77`, with the pp170 patch and this lane's patch
    applied and the gitlink at the head, `check_py_idiom.py` passes at its budget: long
    function 9 <= 9, long module 10 <= 10, unannotated 0 <= 0, undocumented 0 <= 0, too
    many parameters 7 <= 7.
  - Every other gate there that reads the processor passes too, apart from the pin record
    `check_submodule_docs.py`, which fails identically at `39cac060`.
- **Self-test coverage.** Three plants were added for the findings only the suite's
  verdict prints. Every one of the 111 finding and refusal sites in the gate prints, under
  some plant, a line carrying that plant's words. Breaking each newly planted check in
  turn makes the self-test fail by name.

## Validation

Base `2cbed0a987c1e68402658d69459ab7e5aa571adc`; head
`9975764846e7e63bccf0b68a5188d5cc7f23f890`. All results below are local at those
commits; the new commits have not been pushed.

| Processor command | Base | Head | Record comparison |
|---|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1029620 checks | rc 0, 1029796 checks | Every existing suite record is byte-identical; the new command sweep adds 176 checks |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | Byte-identical |
| `make check` | rc 0 | rc 0 | Existing checks pass; adds the 153-plant self-test and command gate; link/file counts reflect the additions |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | Byte-identical |
| `syn/yosys/run.sh` | rc 0 | rc 0 | Byte-identical, including engine elaboration and synthesis |

All nine existing campaign pairs (`aecp_dispatch`, `aecp`, `ctr`,
`notify`, `gsi`, `acmp`, `name_wr`, `name_state`, `d3`) return 0 at both commits.
Their records match after sorting completion-order output and normalizing
scratch paths where needed. D3 detects all 110 mutants at each commit. The new
`aecp_cmds` campaign returns 0 with all 14 controls caught by name and both
golden runs passing.

Both generated ROMs are byte-identical at base and head:

| Image | Bytes | SHA256 at both commits |
|---|---|---|
| `ucode.hex` | 26624 | `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` |
| `ltn_rom.hex` | 6138 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |

All 46 HDL source files match byte for byte. The preprocessed engine also matches:
SHA256 `7ebbeda1420ffd265838a81d6ebc9791095da14f089ecbbcbf84af475e8c6cd4`.
The reviewer probes, 153 self-test plants and 111 covered finding/refusal sites
are detailed above and in the handoff receipts.

The scratch parent at dev `e8454e27`, with each processor pin in turn, passes
its BDD (404 scenarios), feature-status, source-list and ROM checks. Records
match apart from BDD elapsed times and the ROM ledger's commit key. At consumer
dev `ac2c5e77`, the Python gate and its listing pass with unchanged budgets;
35 of 36 consumer commands return 0 at both pins. The sole remaining failure
is the identical moved-pin documentation check, which the parent adoption must
record. The head uses the two documented evidence-disposition patches; base
uses only its applicable name-evidence patch. An initial base run incorrectly
included the head-only disposition and failed its two evidence checks; those
failed receipts are retained alongside the corrected passing runs. No parent
ratchet was changed and no parent change was committed.
