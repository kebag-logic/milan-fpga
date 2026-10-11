[R608] NEGATIVE - exact head 9975764846e7e63bccf0b68a5188d5cc7f23f890

# R608-2 internal independent review: issue #73 / PR #174

- Exact head `9975764846e7e63bccf0b68a5188d5cc7f23f890`, tree `5e0b23b212b2fb4da5735821694ec43e66421d0f`; base `2cbed0a987c1e68402658d69459ab7e5aa571adc`.
- Scope is derived from:
  - the issue's acceptance 1-4;
  - the lane scope (issue comment 6100509798);
  - round 2 (6104932386) and its addendum (6105354276).
- This report was written in two steps:
  1. The verdict, findings and ledger below were written after an independent pass and before any prior review was read.
  2. The resolution of prior public findings was then appended. It is the last section before the limits.

## Verdict

NEGATIVE. These all hold at the exact head:
- the table exists;
- both ROMs are byte-identical to base;
- no `.sv` under `hdl/` changed;
- F06.14 is generated from the table;
- the four planted drifts named by the lane each fail by name;
- the 14 standing controls are caught by name;
- the self-test's 153 plants pass;
- `make check` returns 0.

Three MINOR findings remain open:
- **F1:** one size the table carries (the mapping record of ADD/REMOVE_AUDIO_MAPPINGS) is held in one direction only.
- **F2:** three semantic table fields that drive generated F06.14 cells are held to nothing, and the docs do not say so.
- **F3:** the generator's named-refusal claim fails for three defects it reads.

## What was executed at the exact head (receipts under `receipts/`)

| Check | Result | Receipt |
|---|---|---|
| Generated ROMs, base vs head (`git archive` exports) | `ucode.hex` 26624 B and `ltn_rom.hex` 6138 B, byte-identical (sha256 `518b900c…` and `23cc67ee…`). Only `hdl/aecp/ucode/{aecp_commands.json,gen_ucode.py}` change under `hdl/`. The only new `.sv` is the bench wrapper | `rom-identity.txt` |
| `tb/aecp_cmds` suite (pinned simulator 5.050) | rc 0. 585760 trials, 0 timeouts, 176 checks: 176 PASS | `head-aecp_cmds-suite.log`, `.rc` |
| Fresh sweep re-recorded | byte-identical to the tracked `tb/aecp_cmds/decode.json` (sha256 `c7d2a05e…`) | `head-rerecord.log` |
| Standing controls (`tb/aecp_cmds/mutants.py --jobs 8`) | rc 0. 14 of 14 caught by their named failure; golden and restored PASS | `head-aecp_cmds-mutants.log`, `.rc` |
| `make check` (scratch clone at head) | rc 0. Self-test 153/153; gate OK (31 commands, 84 entries, 41 F06.14 rows); links 1188; ids 570 files | `head-make-check.log`, `head-make-aecpcmd.log` |
| `scripts/gen_matrix.py --check` | rc 0 (94 rows, 0 untested) | `head-gen-matrix-check.log` |
| `scripts/lint_hdl.sh` (pinned simulator) | rc 0 | `head-lint_hdl.log` |
| `ucode.hex` prerequisites | in `tb/pp_top`, `tb/ucpu` and `tb/aecp_cmds`, `make -q ucode.hex` gives rc 0 after a build and rc 1 after touching the table | `ucode-prereq.txt` |
| The lane's four planted drifts | each fails by name, rc 1. Opcode renumbered in the table only: `decode: GET_COUNTERS: …`. Size changed in the doc only: `F06.14: row 0x0017 GET_CLOCK_SOURCE, column Resp. size …`. `OP_GET_COUNTERS_C` changed in the RTL only: `engine: GET_COUNTERS: …`, plus the record's digest. Command missing from the table, with and without regeneration: `decode: AEM 0x0029 is no table command …` | `table-probes/accept-*.log` |
| 18 further table drifts, F06.14 regenerated | 9 fail by name. 9 pass the gate: 6 are F1 and F2; `gdi-max-524-to-600` is declared held to nothing; `shared-entry-add-gcfg` and `echo-entries-add-gctrs` only widen a check (F2 note) | `table-probes/`, `summary.txt` |
| 3 engine probes (build, sweep, re-record, gate) | see F1 and S1 | `engine-probes/` |
| Generator run alone on 8 table defects, with and without `-O` | all rc 1, none writes a ROM. 3 stop with a bare traceback (F3) | `generator-probes.txt` |
| Gate-site mutation: each finding or refusal site disabled in turn, then `--selftest` | 106 of 106 finding and refusal sites are needed by the self-test. The 12 survivors are only `decode.json`'s writer formatting lines, which the byte-identical re-record above covers | `gate-mutation/` |
| Hosted run 38125233898 at the exact head (inspected, not owned) | docs-gates: success, and its log shows `153 planted defects, 153 caught by name, OK` and the gate OK. portability: success. suites: in progress at the time of writing | `hosted-ci.txt` |

## Findings

### F1 - MINOR - the per-record size of the echo rows is held one way only

- **Lenses:** Robustness, Tests, Docs.
- **Where:**
  - `scripts/aecp_gate/record.py:296`: `_floor` only requires each accepted cdl to be `floor + k·per`.
  - `scripts/aecp_gate/table.py` `_sizes`: an echo response's `per` is tied only to the command's.
  - `hdl/aecp/ucode/aecp_commands.json:371,383`: `per: 8` on ADD/REMOVE_AUDIO_MAPPINGS.
  - Neither the ROM walk nor any other check holds `per` on an echo row.
- **Authority:**
  - Round-2 item 2 (R609-1-F1): every size held.
  - The PR body claims `command: 31 held by a consumer`.
  - 09 §8.10 says the table's size rules are held.
  - The lane scope: a drift in any consumer fails by name.
- **Evidence:**
  - `table-probes/per-echo-8-to-4.log` and `per-echo-8-to-2-add-only.log`: `per` is 8 → 4 (or 2) on both rows, and F06.14 is regenerated to `20 + 4·N` and `32 + 4·N B echo`. Gate rc 0.
  - `engine-probes/amap-record-4-bytes` and `amap-record-16-bytes`: the engine's length check is `20 + 4·count` (or `16·count`). The suite fails only by record drift (`decode.json is not what the engine does`), naming no command against the table. After the documented `make record` step, both the suite (176/176) and the gate are green, and the table still says `per: 8`.
- **Impact:** for the only two commands with a per-record command size, the record size can drift in the table and in the published F06.14 to any divisor, or in the engine to a multiple, with every check green once the record is re-taken.
- **Required outcome:** hold `per` exactly. One way is to require the gcd of the first entry's accepted offsets (cdl − floor) to equal `per`; the sweep's count templates already give offsets 8 and 16. Another is a count-1 stimulus at `floor + per`, which must be accepted, and at `floor + per/2`, which must be refused. Plant the drift in the self-test. Alternatively, declare the record size held to nothing everywhere the held set is stated (docstring, 09 §8.10, REQ-VER-002, PR body).
- **Verification:**
  - `python3 -I scripts/table_probes.py --only per-echo-8-to-4 per-echo-8-to-2-add-only` gives rc 1, naming ADD_AUDIO_MAPPINGS.
  - `engine_probes.py` with the two amap probes gives step 3 rc 1, naming the command.

### F2 - MINOR - semantic table fields held to nothing and not declared: `common_status`, `engine_status`, `oversize`

- **Lenses:** Robustness, Tests, Docs.
- **Where:**
  - `scripts/aecp_gate/record.py:310` and `scripts/aecp_gate/rom.py:350`: statuses in `common_status` or `engine_status` are exempt from both status-set checks. Only the schema reads these fields (`table.py:86-90`, that the names exist).
  - `scripts/aecp_gate/doc.py:51`: `oversize` is rendered into the F06.14 Oversize column. Apart from the schema's boolean check, nothing reads it.
  - 09 §8.10:468 lists the oversize flag among what the table carries. It appears neither among the held consumers nor under "Still hand-written and held to no table" (09 §8.10:504). The same is true of the docstring's HELD TO NOTHING list (`scripts/check_aecp_commands.py:63`).
- **Authority:**
  - Round-2 item 5: claim exactly what the gate holds, and list anything still hand-written.
  - The docstring, the PR body and 09: "every status a path can set is in the set".
  - The lane scope: a doc-row drift fails by name.
- **Evidence (`table-probes/`, F06.14 regenerated by the gate's own `--write`, gate rc 0 in each):**
  - `common-status-hides-stream-is-running`: STREAM_IS_RUNNING is added to `common_status.AEM` and removed from SET_CONFIGURATION, SET_STREAM_FORMAT and SET_STREAM_INFO. The three F06.14 Status-set cells lose a status the engine's programs answer.
  - `common-status-adds-unreachable`: NO_RESOURCES is added as common to every AEM command.
  - `engine-status-add`.
  - `oversize-flags-flipped`: F06.14 then says GET_CONFIGURATION needs the oversize slot and READ_DESCRIPTOR does not.
  - Related, and not by itself a hidden drift: `echo-entries-add-gctrs` (rc 0) widens the size check for that program.
- **Impact:** two generated F06.14 columns (Status set, Oversize) can be made wrong by a table-only edit with every gate green. The stated status-set invariant can be bypassed through `common_status`. The hand-written F06.14 sentence on common statuses (06 §6, above the markers) is tied to nothing.
- **Required outcome:** either hold these fields or declare them held to nothing:
  - **Hold them.** For example:
    - each `common_status` entry must come only from a shared entry or engine path (DLKILL, a failed response memory) that every command of that message type can reach;
    - a status a command's own programs set definitely may not be excused as common;
    - `oversize` is derived from, or held to, the response rule (above cdl 524 possible) or Milan §5.4.1's list;
    - the common-status sentence is generated.
  - **Or declare each one held to nothing** in the docstring, 09 §8.10, REQ-VER-002 and the PR body.
- **Verification:** the four probes return rc 1 by name, or the declarations are present.

### F3 - MINOR - the generator's named-refusal claim fails for three defects it reads

- **Lenses:** Robustness, Docs.
- **Where:**
  - `hdl/aecp/ucode/gen_ucode.py:157-160`: an `0x`-prefixed non-hex MVU opcode reaches `int(…, 16)`.
  - `hdl/aecp/ucode/gen_ucode.py:2459-2461`: `_cmd['name']` and `_cmd['entries']` are indexed without a named refusal.
- **Authority:**
  - The PR body: "A field it cannot read stops it with a line naming the command and the field".
  - 09 §8.10:480: "a status code or MVU row it cannot read stops the generator with a line naming the command and the field".
- **Evidence:** `generator-probes.txt`, rc 1 in each case, with and without `-O`:
  - a missing `entries` gives `KeyError: 'entries'`;
  - a missing `name` gives `KeyError: 'name'`;
  - MVU opcode `0xZZZZ` gives `ValueError: invalid literal for int() with base 16: '0xZZZZ'`.

  No ROM is written. The gate's schema check names all three before it runs the generator, so round-2 item 3 ("or a schema check run before it loads") is met inside `make check`. Every suite build (`tb/pp_top`, `tb/ucpu`, `tb/aecp_cmds`) and `syn/` runs the generator alone.
- **Impact:** the stated behaviour is not what the code does; a suite build on such a table stops with a traceback that names neither the command nor, for the MVU opcode, the field.
- **Required outcome:** either refuse these with a `SystemExit` naming the command and the field, or narrow both claims to the defects the generator names.
- **Verification:** `python3 -I scripts/generator_probes.py` shows named lines for all eight plants.

### R1 - RESIDUE - stale push statement in the PR body

- **Lenses:** Docs (wording only).
- **Where:** the PR body, Validation section: "All results below are local at those commits; the new commits have not been pushed."
- **Why:** the head is published, and hosted run 38125233898 ran at it.
- **Exact fix:** "All results below were taken locally at those commits, before the head was pushed."

### Suggestions (verdict-neutral)

- **S1. Unswept MVU protocol-id bytes.** The MVU sweep never makes the protocol-id byte @22 or @24 wrong. `engine-probes/mvu-pid-first-byte-unchecked` compares only the low byte of @22..@23, and it changes nothing the sweep records: after a re-record everything is green. Flip every protocol-id byte.
- **S2. Undigested sweep inputs.** `decode.json`'s input digests omit `hdl/aecp/desc/model_lint.py` and `model_rules.py` (both `image.bin` prerequisites in `tb/aecp_cmds/Makefile`), and `tb/common/verilator_harness.hpp`. Add them.
- **S3. Stimuli the bench never drives.** The bench never drives:
  - a held lock (`lock_held_i` = 0);
  - a deadline kill (`dl_kill_i` = 0);
  - a bound-but-not-streaming split;
  - a nonzero descriptor_index.

  These are covered in general by "outcomes no stimulus of the sweep reaches". Naming them in 09 §8.10 would make the limit concrete.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The table against Table 7-141, the F06.14 rows and the observed responses. The base-tree size fixes (SET/GET_SAMPLING_RATE and SET/GET_CLOCK_SOURCE cdl 20; GET_AUDIO_MAP 24 + 8·N) confirmed by the fresh sweep. REQ-VER-002 Cov/Arch cells against acceptance 4. The parent export named (path, format, schema tag) | R608-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| RTL | CLEAN | No `.sv` change under `hdl/` (name-status diff). Both ROMs byte-identical. `lint_hdl.sh` rc 0. The bench wrapper's observation is the `u_ucpu` dispatch handshake (`disp_valid_i && disp_ready_o`, `disp_upc_i`), built with the pinned simulator | R608-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| Robustness | UNCLEAN (F1, F2, F3) | 23 table, doc and RTL drift probes; a 66-variant size sweep; 3 engine probes; 8 generator-alone probes; 118-site gate mutation; standing controls; record reproducibility | R608-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| Tests | UNCLEAN (F1, F2) | `tb/aecp_cmds` (`sim_main.cpp`, wrapper, Makefile, README, `decode.json`, `mutants.py`); the self-test (153 plants, every finding and refusal site needed); `ucode.hex` prerequisites; CI wiring in `.github/workflows/hdl.yml` and `Makefile` | R608-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |
| Docs | UNCLEAN (F1, F2, F3); RESIDUE R1 | 06 §6 F06.14 and its preamble, 06 §8 and §8.1; 09 §1, §7 and §8.10; REQ-VER-002 row; the gate docstring; `tb/aecp_cmds/README.md`; the PR body against the published evidence | R608-2 | 9975764846e7e63bccf0b68a5188d5cc7f23f890 |

## Acceptance (issue #73) at this head

| # | Item | At this head |
|---|---|---|
| 1 | One tracked machine-readable command table (opcode, sizes, status set, hazard class, lock/notify flags) | met: `hdl/aecp/ucode/aecp_commands.json`, `aecp-command-table/1`, 31 served rows |
| 2 | gen_ucode.py dispatch data and F06.14 generated from it, or gated by a script in `scripts/` | met in form. F06.14 is generated. The generator takes its status codes and MVU command_type from the table. The engine's decode and dispatch are held through the observed sweep, and the remaining consumers are gated. The size holding has the F1 gap and the field holding has the F2 gap |
| 3 | The gate runs in CI | met. `aecpcmd` runs in docs-gates, which succeeded at the head. The sweep is in `run_suites.sh` (glob) and the standing controls are a suites-job step. The hosted suites job had not finished when read |
| 4 | REQ-VER-002 Cov/Arch and 09 §8 record generated vs hand-written | not met as written. The record omits the fields of F2 and overstates F1 and F3 |
| Lane | ROMs and the elaborated engine byte-identical; the four planted drifts fail by name; the parent export named | met (receipts above). The parent consumer gates are the manager's |

## Prior public findings at this head

Prior findings were read only after the verdict and ledger above were written. Each was checked against this head.

| Prior finding | Status at 9975764 | Evidence |
|---|---|---|
| R608-1-F1 (decode and dispatch held to no table) | RESOLVED | Held by behaviour through `tb/aecp_cmds`. q1 and q2 are standing controls, both caught by name in my run (`head-aecp_cmds-mutants.log`). The table's `about`, 06 §8, 09 §8.10 and REQ-VER-002 no longer say the table drives the dispatch |
| R608-1-F2 (generator-read defects nameless) | RESOLVED | p5e (`AAU`) and p8 (`SCFGRUN2`) are named by the schema check and the gate. The generator alone names them too (`generator-probes.txt`). The self-test plants them in a file copy. The residual overclaim for three other generator-read defects is new finding F3 |
| R608-1-F3 = R609-1-F3 (doubled plurals) | RESOLVED | `grep -c 'mappingss\|entriess'` on 06 gives 0. `make check` rc 0 |
| R608-1-F4 = R609-1-F2 (`ucode.hex` prerequisites) | RESOLVED | `ucode-prereq.txt`: rc 1 after touching the table, in all three suites |
| R608-1-S1 = R609-1-S4 (field reference) | TAKEN | `fields` object in the table |
| R608-1-S2 = R609-1-S3 (`assert` under `-O`) | TAKEN | `SystemExit`. The refusals hold under `python3 -O` (`generator-probes.txt`) |
| R609-1-F1 (MAJOR: 10 response sizes and every command size held to nothing) | RESOLVED for the cdl values; a narrower gap is RETAINED as F1 | My own sweep (`size-sweep-r608.txt`) moves each served command's response cdl, then its command cdl, by +4. An echo row moves both, so the echo rule alone cannot catch it. 29 of 31 fail by name in each direction. The 2 that pass are ACQUIRE_ENTITY and REGISTER_UNSOLICITED_NOTIFICATION, whose command cdl is disclosed in 09 §8.10, the docstring and REQ-VER-002 as tied only by the echo rule. GET_AUDIO_MAP response cdl 20 and 28 fail by name; 24 passes. The per-record step of the echo rows is still held one way only (F1) |
| R609-1-S1 (Table 7-141 held) | TAKEN | STREAM_IS_RUNNING 12 → 13 gives `schema: status STREAM_IS_RUNNING is 13 in the table, IEEE 1722.1-2021 Table 7-141 gives 12` |
| R609-1-S2 (documented row without a name) | TAKEN | a named schema line, rc 1 |

## Real limits

- **Not run here:**
  - the full processor suite bank (`run_suites.sh`) and the nine existing campaigns;
  - `syn/yosys/run.sh`;
  - any parent or consumer gate, including the parent's Python idiom ratchet (Rule 12) that the addendum names.

  For these, this review relies on the RTL being unchanged, the ROMs being byte-identical, and the focused runs above. Their execution evidence is the author's published receipts. No manager source bank ran at this exact head, and none is claimed.
- **Hosted run 38125233898:** suites was in progress when read. Only the docs-gates and portability conclusions, and the docs-gates log lines, are cited. The manager owns hosted and local CI-runner acceptance.
- **Bounded sweep:** the sweep's guarantees are those of its stimulus. The table itself declares held to nothing:
  - opcodes above 0x007F;
  - cdl above 100;
  - outcomes the sweep never drives (S3).
- **Toolchain:** probes were built with the pinned simulator 5.050 (wrapper sha256 `905795b9…`).
- **No hardware:** physical calibration NOT RUN; no hardware was used, and no field skip is hardware proof.
- **Clone state:** every probe ran in a disposable copy. The clone was never modified. HEAD and tree are exact, the index equals the HEAD tree, and all 606 working-tree blobs and modes match. The repository has no gitlinks (`clone-integrity.txt`).

## Pending manager duties

- **Merge-turn validation:** the current-dev merge candidate (source base `2cbed0a9`, live dev `ac2c5e77`) with the builder and native banks, and its published receipts.
- **Hosted acceptance:** hosted suites and local CI-runner acceptance at the exact head.
- **Parent consumer bank at this head:**
  - the `parent-aecp-cmds-evidence.patch` disposition (sha256 `19d41c7b…`) for `tb/aecp_cmds/mutants.py` in `measure_test_evidence_readers.py`;
  - `check_py_idiom.py` at its budgets;
  - the moved-pin record (`check_submodule_docs.py`) at adoption.
- **Residue checklist:** R1.
- **Follow-up lane:** the parent gate over the exported table.

R608-2 FINISHED
