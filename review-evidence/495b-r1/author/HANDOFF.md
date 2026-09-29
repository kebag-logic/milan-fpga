# [A433] handoff: #495 builder and tooling residue

Status: REVIEW READY at head `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0`
(continuation after the STOP). The manager's disposition (#495 comment
5882165062) chose option 2. Items 1-7 are committed, plus the item 1 README
follow-up the disposition asked for; the whole gate set is rc 0 at this head.
Posted on #495: `[A433] TAKEN` (5880817674), `[A433] STOP` (5882153376) and
`[A433] REVIEW READY` (5883137691).

- Repository: https://github.com/kebag-logic/milan-fpga.git
- Lane: `$LANES/495-builder-residue`, branch `495-builder-residue`
- Base: dev `eaa88a32eb77adeba9c1c631198c7fb516a11095`
- Assignment: #495 comment 5880790651 (items 1-7, one commit per item, in order)
- Submodules: gptp-processor `5dce647a`, protocol-processor `c951a9ff` and
  third_party/verilog-axis `48ff7a7e` were checked out at their pins, absorbed
  under `.git/modules`, but not registered in `.git/config`, so
  `git submodule status` printed `-` and the code-quality gates refused.
  `git submodule init` on exactly those three registered them (no checkout,
  no fetch; heads and clean state re-verified). `external` is empty and was
  left alone: `git -C external` would fall through to the parent.

## Items

| # | Item | Commit | Status |
|---|---|---|---|
| 1 | AX 1x1 simulated clock from the contract clock | `9e53b116` | committed |
| 2 | `sweep_extra.sh` `--entity-gen-dir` and argument order | `e4197dc9` | committed |
| 3 | contract-clock import cannot be shadowed | `a71b3bec` | committed |
| 4 | equal-clock SKIP in the skip ledger | `8c62982f` | committed |
| 5 | `CI_WORKFLOWS.md:44-45` wording | `51ca45c7` | committed |
| 6 | strict quoted MAC and hex shapes (disposition 5882165062) | `eb23f044` | committed |
| 7 | shipping probe asserts #395 hooks | `a9cecd23` | committed |
| 1b | item 1 wording: `tb/verilator/milan_dp/README.md:85` (disposition) | `859fa5d5` | committed |

The disposition gave the order "item 6, then item 7" and asked for the README
line "as a separate one-line commit" without placing it, so it follows item 7
rather than splitting 6 and 7. Items 1-5 were not redone or amended.

Mutation driver: `mutate.py` (this directory). Each mutant is applied in place,
its check runs, the touched files are restored from the bytes read before the
edit and re-hashed, and the whole worktree diff hash is compared before and
after the run. Specs and logs are under `mutants/`.

### Item 1 (`9e53b116`)

Change:
- `tb/verilator/milan_dp/Makefile:415-426`: `AX_GPTP_HZ` is `CPU_HZ` read from
  `tb/verilator/nvm_capture_cpu/recipe.py` by path (`python3 -I`, `runpy`),
  with the file's own "take the status" guard; `:432` the ROM rule depends on
  the recipe; `:480` the harness gets `-DMILAN_CLK_HZ_TB=$(AX_GPTP_HZ)` beside
  the `-GMILAN_CLK_FREQ_HZ` of the same value.
- `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:57-80`: `kHz = MILAN_CLK_HZ_TB`
  (`#error` without it); the period `kPeriodNs` replaces every `* 20`/`/ 20`
  cycle-time conversion (`:217,462,478,563,583,681,691,738`); `kAafPeriod` is
  six 48 kHz samples of `kHz`; the report lines print `kHz` (`:926-936`). The
  check labels still spell 20 ns / 200 MHz / 28 ns (verify_abort.py reads the
  28 ns ones), so `static_assert(kDelayBoundNs == 28)` stops a build at another
  period rather than mislabelling checks. At 50 MHz the printed output is
  byte-identical (banner and report lines checked in the gate log).
- Prose: `sw/builder/test_builder.py:17100` print text; `docs/integration/
  BAREMETAL_FIRMWARE.md:2036-2039` (was `:2017` on the older base). PR #609
  (head `1f039cfe`, merge base `7a7582f0`) edits that page only at base lines
  71, 1895-1904, 1907, 1932 and 1940, and nothing between its merge base and
  `eaa88a32` shifts line 2036, so the line is outside #609's hunks and was
  reworded.

Check: `sw/builder/test_clock_contract.py` `test_sim_clock` (wired into the
builder bank, `test_builder.py` main). It dry-runs `make -n -B ax1x1gptp`
with the real recipe and with a planted `CLOCK_RECIPE` (`CPU_HZ + 1`) and
requires `--clk-hz`, `-GMILAN_CLK_FREQ_HZ=` and `-DMILAN_CLK_HZ_TB=` of that
value exactly once each; an absent recipe must stop make by name; the harness
must take `kHz` from the define and spell neither the contract value nor its
MHz form.

Before/after and mutants (`mutants/item1.log`): control PASS; BEFORE
(Makefile and harness at `eaa88a32`) KILLED; M1a Makefile literal, M1b ROM
literal, M1c define dropped, M1d elaboration literal, M1e harness literal,
M1f report literal, M1g status not taken: all KILLED.

### Item 2 (`e4197dc9`)

Change (`sw/litex/sweep_extra.sh`, whole file):
- `parse_args` (`:38-51`): `--dry-run` in any position; any other option, a
  missing or extra argument, an empty tag or an unknown board exits 2 with a
  usage line before anything runs.
- The venv `PATH` export now precedes reading the configuration (`:61`), as
  `sweep.sh`'s `setup_env` does (R355-1 SG4, second half).
- `config_options` (`:14-33`) prints the clocks and `--entity-gen-dir
  <ROOT>/<GEN_CONFIG_DIR>/<name>` from the builder's own constant; a launch
  first runs `eb.build` (as `sweep.sh` `entity_defs` runs the builder) and
  refuses when the builder wrote the entity definition elsewhere (a
  configuration outside `configs/`), which would otherwise include the tracked
  shape.
- `BASE` is an array; the dry run prints it shell-quoted, so a configuration
  path with a space stays one argument.

Check: `test_clock_contract.py` `_sweep` now runs under an empty temporary
HOME and asserts nothing was written there and nothing launched;
`_assert_sweep_clocks` requires one `--entity-gen-dir` naming the
configuration (and, for tracked ones, a `gen/adp_shape_defaults.svh` naming
it); new `test_extra_sweep_invocation` covers the three `--dry-run`
positions, five refusals, the ungenerated-entity launch refusal and the build
interpreter reading the configuration (a marker interpreter at the venv path
read from the script's own `export PATH` line).

Before/after and mutants (`mutants/item2.log`, `mutants/item2-order.log`):
control PASS; BEFORE KILLED (no `--entity-gen-dir`); BEFORE-ORDER: the base
script given `ax7101 --dry-run order` took `--dry-run` as the tag and went for
a launch (stopped only by the empty HOME at `settings64.sh`), KILLED; M2a-M2h
(entity dir dropped, old positional parse, unknown option as argument, extra
arguments ignored, empty tag, guard skipped, PATH exported late, word-split
launch line) all KILLED.

### Item 3 (`a71b3bec`)

Change: `sw/builder/endstation_builder.py:70-74` and `sw/litex/milan_soc.py:
73-77` read `CPU_HZ` with `runpy.run_path(<root>/tb/verilator/nvm_capture_cpu/
recipe.py)`; `tb/` is a namespace package, so a regular `tb` package anywhere
on `sys.path` won the old import. `BAREMETAL_FIRMWARE.md:45-46` says "read it
by its path".

Check: `test_clock_contract.py` `_assert_clock_source`, used by
`test_builder_clock_source` (builder bank) and at the start of
`test_soc_clock_contract` (LiteX environment, `--soc` and
`sw/litex/test_pp_mem_bridge.py`). A subprocess imports the tool below a
regular `tb` package declaring `CPU_HZ + 2`, with recipe.py's bytes replaced
in memory by `CPU_HZ + 1` through `open_code` and an empty pycache prefix; the
tool's clock must be the planted value, and the same process must show the
shadow is live for a namespace import.

Before/after and mutants (`mutants/item3.log`): controls PASS (builder, SoC);
BEFORE builder and BEFORE SoC (the `eaa88a32` imports) KILLED with the shadow
value; B5 (builder literal) and S7 (SoC literal) KILLED; namespace imports
restored in either tool KILLED; an importlib path loader in the builder PASSES
(the plant does not depend on the loading mechanism).

### Item 4 (`8c62982f`)

Change: `sw/builder/test_clock_contract.py:111-137` `test_gptp_rom_clock` takes
a `skip(gate, why)` callable (default `_print_skip`, which prints when the
module runs alone) and reports the equal-clock control through it as "not
applicable". `sw/builder/test_builder.py:27816-27864`: the bank runs it as
`test_rom_clock_contract`, which passes the bank's own `skip`, so the arm lands
in `SKIPPED` and the verdict reads `ALL GATES PASS EXCEPT n NOT RUN`.
`test_builder.py` runs as `__main__`, so a second import of it from
`test_clock_contract` would have had a ledger the verdict never reads; the
ledger is passed, not imported.

Check: `test_rom_clock_skip_reaches_the_ledger` (bank) plants an equal-clock
variant of `ax7101_1x1_tdm8` as the only shape, requires exactly one
`("clock contract", ..., "row")` entry naming it, removes that planted entry
again, and requires the bank's `for fn in (...)` run list to name
`test_rom_clock_contract` and never the bare `test_gptp_rom_clock`.

Before/after and mutants (`mutants/item4.log`, `probe_eq_verdict.py`): the
R354-3 probe EQ through the bank's own run list, with the planted shape beside
the tracked five, prints `ALL GATES PASS` at `eaa88a32` (KILLED) and
`ALL GATES PASS EXCEPT 1 NOT RUN` naming the arm at this head (PASS). M4a (SKIP
printed, not recorded), M4b (wrapper drops the ledger), M4c (run list uses the
bare function; killed by the self-check and by probe EQ) and M4d (condition
inverted) KILLED.

### Item 5 (`51ca45c7`)

Change: `docs/testing/CI_WORKFLOWS.md:43-50`. The lead definition now states
the classifier's rule: documentation less the pages a gated module reads,
where a gated module is code under the six roots other than the builder bank
that `docs-check` runs whole, so a page stays relevant even where `docs-check`
runs the same check (the tap page). `scripts/ci_scope.py` is not edited.

Check: `probe_ci_lead.py` loads `scripts/ci_scope.py` by path (read only) and
requires: the classifier files `docs/AAF_LATENCY_TAPS.md` relevant and its
reader is a gated module outside `DOCS_JOB_PY`; the lead no longer states
"reads without `docs-check` reading it too"; `DOCS_JOB_PY` is the builder bank
alone and `docs.yml` runs it; the lead cites the `GATED_ROOTS` count and names
the exemption and the tap page. `mutants/item5.log`: PASS at this head, KILLED
at `eaa88a32`. No code mutants: a prose change. `ci_scope.py --selftest` and
`ci_events.py --check` stay rc 0.

Remaining part of the item (not edited, as assigned): `scripts/ci_scope.py:12-13`
and `:18-20` (docstring: "Documentation is a path no gate that the docs-only
path skips reads without `docs-check` reading it too") and `:66-68` (the
`DOCS_JOB_PY` rationale) still state the #444 criterion that the tap page's
classification departs from.

### Item 6 (`eb23f044`)

The first session stopped on the item's condition (#495 5882153376): the
assignment's shapes would refuse the documented example `"020000000002"` and
the documented underscore rules. The disposition (5882165062) chose option 2
and fixed the accepted and refused forms; this commit implements exactly those.

Change:
- `sw/builder/endstation_builder.py:1338-1342`: `HEX_TEXT` (an optional
  `0x`/`0X`, then ASCII hex digits with at most one underscore between two
  digits; `fullmatch`, so no sign, no whitespace, no trailing newline) and
  `MAC_OCTETS` (six two-digit octets sharing one `:` or `-` via a
  backreference). `:80` adds `MAC48_MAX` beside `EUI64_MAX`.
- `:1345-1363` `_hex_text(v, bits, ctx, what)`: the quote refusal for
  non-strings (unchanged text), then the shape refusal (`<ctx>: '<v>' is not
  <what> (...)`), then the width refusal when the digit count, leading zeros
  included, exceeds `bits // 4` (`<ctx>: '<v>' is outside <bits> bits (<n> hex
  digits, at most <bits/4>)`). `int()` never sees raw text any more, so
  `int()`'s own leniencies (whitespace, a sign, `0x_1`, Unicode digits such as
  U+0660) cannot reach a value.
- `:1366-1368` `_eui64` and `:3704-3706` `_declared_uint` are `_hex_text` at
  their widths; `:2063` `_srp_dmac` parses at the MAC-48 width, which replaces
  its "wider than a MAC-48" value check (no committed test pinned that text).
- `:3210-3239` `_mac48`: `MAC_OCTETS`, or `HEX_TEXT` with exactly twelve digits;
  anything else is `'<v>' is not a MAC-48 (...)`. The value range check reduces
  to zero (twelve digits cannot exceed 48 bits): `'<v>' is the all-zero MAC-48`.
  The I/G refusal is unchanged.
- Docs: `sw/builder/README-parameters.md:161-171` and
  `docs/ENDSTATION_BUILDER.md:890-893` state exactly the disposition's forms.
  `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:289` ("optional `0x` prefixes and
  underscores are accepted") was a third statement of the rule the inventory
  had not listed; it now says "single underscores between digits". It is the
  one edit outside the two passages the disposition named.

Width source, per field (the disposition asked for it):

| Field | Digits | Source in the builder | Why that width |
|---|---|---|---|
| `platform.mac_address` | 12 (MAC rule) | `MAC48_MAX` (`:80`) in `_mac48` | a station MAC-48; it becomes the AVTP stream_id prefix and the ATDECC entity_id |
| `srp.stream_dmac_base` | 12 | `MAC48_MAX` in `_srp_dmac` (`:2063`) | a MAC-48 destination: the `KL_lwsrp_ctx` record carries it as `dmac[119:72]` (`:2529`), and the base refused "wider than a MAC-48" |
| `entity.entity_model_id`, `entity.model_id_pin`, `entity.entity_id` | 16 | `EUI64_MAX` (`:79`) in `_eui64` | EUI-64 identities (1722.1-2021 Table 7-2) |
| stream `formats` entries, `clocking.crf_format`, `clocking.crf_output.format` | 16 | `EUI64_MAX` via `_fmt64` | 64-bit stream format words (1722.1-2021 Table 7-8 entries are 8 octets) |
| `entity.vendor_oui` | 6 | `_vendor_oui` passes 24 (`:3717`) | a three-octet OUI |
| `entity.entity_capabilities` | 8 | `_verify_entity_capabilities` passes 32 (`:3736`) | `ADP_ENTITY_CAPS_C` is `logic [31:0]` (`protocol-processor/hdl/adp/pp_adp_pkg.sv:53`) |

Checks (`sw/builder/test_declarations.py`, run by the bank as gate 40):
- `test_mac_shape_contract` (`:287`) over `MAC_SHAPE_REFUSALS` (`:248`): nine
  named rules, 30 spellings, each loaded through `load_config` (YAML-dumped, so
  whitespace and newlines survive; the round trip is asserted) and required to
  refuse with the message prefix `platform.mac_address: '<v>' is not a MAC-48 (`.
  Rules: sign; leading or trailing whitespace; fewer than twelve digits; more
  than twelve digits; short or unpadded octet (including `2:000:00:00:00:02`,
  twelve digits with unpadded octets); mixed separators; separator next to an
  underscore; leading, trailing or doubled underscore; `0x` on octets. The
  first spelling of each rule differs from a legal unicast MAC only by that
  fault. R388-1's `"-2"`, `"0:2"`, `"2"`, R389-1's `"2:0:0:0:0:2"` and
  `"02:00:00:00:02"` are in the table.
- `test_hex_shape_contract` (`:331`) with `_assert_hex_shape` (`:316`): all ten
  quoted hex fields (`HEX_FIELDS`, `:98`, plus the OUI and capabilities), each
  loaded through `load_config`: eight named shape rules (sign, leading
  whitespace, trailing whitespace, leading underscore including `0x_`, trailing
  underscore, doubled underscore, non-ASCII digit, no digits) must refuse with
  `<field>: '<v>' is not `; one extra digit (a leading zero, with and without
  `0x`) must refuse with `<field>: '<v>' is outside <bits> bits (`; `0X` and a
  single `_` group must load. The widths in `HEX_FIELDS` are the test's own
  oracle (64, 48, 24, 32), not read from the builder.
- `test_station_mac_string_contract` (`:203`): the eight accepted pins stay and
  four accepted forms are added (`0X020000000002`, `0200_0000_0002`,
  `02_00_00_00_00_02`, `0a-1B-2c-3D-4e-5F`).

Committed pins that changed, all refusal pins (every accepted-form pin is
unchanged and green, as the disposition required):
- `test_declarations.py:237-238`: `("0", "out of MAC-48 range")` and
  `("1000000000000", "out of MAC-48 range")` became `("000000000000", "is the
  all-zero MAC-48")` and `("00:00:00:00:00:00", ...)`. `"0"` and
  `"1000000000000"` moved into the named table (fewer / more than twelve
  digits), where they are still refused, now for their shape.
- `test_declarations.py:392`: `"-1"` left the "outside bits" row, replaced by
  `f"0{digits}"` (a leading zero past the width); `-1` is in the named sign
  rule for both fields.
- `sw/builder/test_builder.py:25738-25739` (gate 25b, "vendor_oui negative"):
  the refusal reason for `"-1"` is now `is not a hex integer` (the sign rule)
  instead of `outside 24 bits`. Still refused; the reason changed with the rule.

Before/after (`probe_item6.py`, `mutants/item6-probe.json`, logs in
`mutants/item6-probe-logs/`): with the builder at `51ca45c7`, 67 of the 90
named spellings are accepted (22 of 30 MAC spellings, 45 of 60 hex spellings
across the 24/32/48/64-bit parsers); at `eb23f044`, none.

Mutants (`gen_item6_spec.py` -> `mutants/item6.json`, `mutants/item6.log`,
per-mutant logs in `mutants/item6-logs/`): controls PASS (the named tests, the
#595 pins, gate 25b alone). BEFORE (builder at `51ca45c7`) KILLED under each of
the three checks. M6a sign in `HEX_TEXT`, M6b hex `strip()`, M6c MAC `strip()`,
M6d free underscores, M6e `\d` for `0-9` (Unicode digits), M6f value width
instead of digit count, M6g fewer MAC digits, M6h more MAC digits, M6i
unpadded octets with twelve digits, M6j mixed separators, M6k underscores
deleted before the octet match, M6l `0x` on octets, M6m stream DMAC at 64 bits,
M6n all-zero MAC (killed by the #595 pins), M6o `0X` refused, M6p `_eui64` and
M6q `_declared_uint` back on lenient `int()`: all KILLED; 0 mismatches.

Inventory under the disposition's forms (`inventory_item6_head.py`, output
`inventory_item6_head.txt`, graded by the head parsers, exit 0): every tracked
YAML value is accepted (the table in the STOP comment, unchanged); every quoted
example in `docs/ENDSTATION_BUILDER.md`, `sw/builder/README-parameters.md` and
`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` matches its documented verdict
(the six accepted examples at README-parameters `:162-170` accept; `"0:2"` and
`"2:0:0:0:0:2"` at `:171` refuse). The first session's inventory
(`inventory_item6.py`, `inventory_item6.txt`) graded the assignment's original
shapes and is kept as the STOP evidence.

Not changed (outside the hex rule): the `maap` selector of
`srp.stream_dmac_base` is still compared after `strip().lower()`
(`endstation_builder.py:2060-2061`), so `" MAAP "` selects MAAP. It is a
selector, not hex text, like `hash-derived` and `mac-derived` (which are
compared exactly).

### Item 7 (`a9cecd23`)

Change: `sw/builder/test_shipping_clock_constraints.py:30-44`
`assert_timing_grade_hooks(commands)`, called at `:97` on the real emitted
build Tcl of every shipping elaboration: exactly one
`kl_timing_grade_configure`, before the first `place_design`; exactly one
`kl_timing_grade_reports`, after the last `route_design` and before
`write_bitstream`. `docs/testing/RUNNING_TESTS.md:188-189` states the two
checks beside the Ethernet-hook ones.

Before/after and mutants (`gen_item7_spec.py` -> `mutants/item7.json`,
`mutants/item7.log`; check `run_ship_probe.py`, one real shipping elaboration
in the pins-only environment, as R382-4's receipt 07 ran it): controls PASS
(1x1 e1, 1x1 e2, 8x8 e1). MD and ME are receipt 07's edits of
`sw/litex/clock_constraints.py`, verbatim (branch `607-review-evidence` at
`14d271cc`, `review-evidence/607-r1/reviews/R382-4/scripts/merge_mutants.py`).
The probe at `eb23f044` PASSES under MD and under ME (the gap R382-4 recorded);
at this commit MD (`reports missing or duplicated: []`) and ME (`configure
missing or duplicated: []`) are KILLED, on 1x1 e1 and on 8x8 e2. Own mutants
MF (configure moved to pre-routing), MG (reports moved before routing), MI
(reports moved after `write_bitstream`) and MH (a second configure line) are
KILLED. `mutants/item7-grade.log`: `test_timing_grade.py` (the #395 hook test
on a bare `Platform()`) stays green under MD and ME, as R382-4 found; 0
mismatches in both runs.

### Item 1 follow-up (`859fa5d5`)

`tb/verilator/milan_dp/README.md:85`: the `obj_ax1x1gptp` row's shape cell
said "50 MHz"; it now names the [contract clock] and links
`docs/integration/BAREMETAL_FIRMWARE.md#build-contract`, the wording item 1
used at `BAREMETAL_FIRMWARE.md:2036-2039`. Check: `grep -n "gPTP ON, 50 MHz"
tb/verilator/milan_dp/README.md` matches line 85 at `a9cecd23` and nothing at
`859fa5d5`; `gen_toc.py --verify-anchors` and `check_doc_paths.py` accept the
link. A prose change: no code mutants.

Left in that README (not named by the disposition, not edited): `:121`
("Default 100 MHz, not deployment's 50 MHz", the `obj_ax1x1` shape table),
`:160` ("Milan and PHC | 50 MHz aliases; nominal PHC increment 20 ns", the
`obj_ax1x1gptp` clock model, which the item 1 `static_assert` ties to the
harness's 20 ns labels) and `:502` ("At 50 MHz, those cycles represent 60--100
ns", a conditional statement).

## Gate table

All at head `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0`, run by `run_gates.py`
(each command's own rc, never piped; the head is re-read after each run and
matched). Per-gate rc, seconds, log size and log sha256 are in
`gates-fast-859fa5d5.tsv`, `gates-tests-859fa5d5.tsv`,
`gates-long-859fa5d5.tsv` and `gates-gptp-859fa5d5.tsv`; the specs are the
same `gates-*.json` the `51ca45c7` run used. Logs stay under
`$VALIDATION_STORAGE/a433/gates-859fa5d5/` (not copied here; hashes recorded).

**No receipt from `51ca45c7` is reused.** Every gate in the set was rerun at
`859fa5d5`. The later commits change `endstation_builder.py`, which the builder
banks, the changed tests, the shipping probe and the `ax1x1gptp` target
(`tb/verilator/milan_dp/Makefile:436` runs the builder) all execute, so none of
those could be carried over; the Markdown and code-quality gates are cheap and
were rerun rather than argued. The `51ca45c7` TSVs stay as the item 1-5
evidence at that head.

The two banks, the compiler-absent audit and the gPTP suite run longer than
one foreground command may last here, so each was started detached through
`run_gates.py` and waited on in the foreground until it exited; nothing else
touched the worktree while they ran. The gate order was: fast, tests, long,
gPTP, then the mutants (which edit the worktree) after the gPTP suite exited.

Environments: unchanged from the `51ca45c7` run.
- Pins-only: fresh venv `$VALIDATION_STORAGE/a433/pins-venv` from
  `setup_pins_env.sh`: Python 3.12.13, `pyyaml==6.0.3`, exactly
  `sw/litex/litex_pins.txt`, `scripts/ci_litex_env.py` (VexiiRiscv
  `235753e2`), `sw/litex/patches/apply.sh` (3 patches), sv2v v0.0.12
  (digest checked); picolibc and compiler-rt data packages absent, as in CI.
  Own HOME for the pins-only tests; the builder banks keep the real HOME so
  the RV32 SDK selector (`riscv32-linux-gcc` 14.3.0) resolves.
- Markdown: `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python` (cmarkgfm
  2025.10.22, html5lib 1.1, PyYAML 6.0.3).
- Verilator 5.050 from `$VALIDATION_TOOLS/verilator-v5.050`.

| Gate | Command | rc at `859fa5d5` |
|---|---|---|
| Builder bank, compiler present | `pins-venv python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration` (490 s; `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11, the historical Arty calibration report is not on this host; gate 40 prints `[495 MAC] 9 named shape rules, 30 spellings refused` and `[495 hex] 10 hex fields`) | 0 |
| Builder bank, compiler absent | `pins-venv python3 -B run_builder_absent.py` (the bank with `--require-elaboration`, the three RV32 candidates hidden; 350 s; `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 11 and gate 1b's compiled CSR census, which needs the compiler; the same two as at `51ca45c7`) | 0 |
| Compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit $VALIDATION_STORAGE/a433/rv32-absent.jsonl` | 0, 0 |
| Pins-only builder tests | `test_clock_constraints.py` (four shipping PASS lines, now with the #395 hook check), `test_timing_grade.py <python>`, `test_clock_contract.py --soc` | 0, 0, 0 |
| Changed tests | `test_clock_contract.py`, `test_declarations.py` (includes both #495 shape tests), `sw/litex/test_pp_mem_bridge.py` (113/113, pins-venv) | 0, 0, 0 |
| milan_dp AX 1x1 gPTP | `make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4` (the `ax1x1gptp` target and `verify_abort.py`) | 0 (3493 s; compiled with `-DMILAN_CLK_HZ_TB=50000000`, `-GMILAN_CLK_FREQ_HZ=50000000`, `--clk-hz 50000000`; `ax1x1gptp physical: checks: 137 failures: 0`; `verify_abort.py` setup abort 6/0, no-TX 20/0, no-Pdelay 14/0; log 102278 bytes, sha256 `fb3d5ab693ccd9bf...` in the TSV) |
| Markdown gates (19) | `docs_check` (+`--selftest`), `check_em_dash --base eaa88a32` (+`--selftest`), `check_doc_style` (+`--selftest`), `check_doc_paths`, `gen_toc --selftest/--verify-anchors/--check`, `DOC_MAP.gen.py --check/--selftest`, `check_solution_docs` (+`--selftest`), `check_archive` (+`--selftest`), `check_feature_status --self-test`, `gen_module_matrix --check`, `git diff --check eaa88a32 HEAD` | all 0 |
| Code-quality gates (24) | Rules 3-13: `check_rtl_source_lists`, `measure_naming --check`, `check_port_contracts`, `measure_fail_fast --check`, `check_todo_ownership`, `measure_test_evidence --check`, `check_hygiene --check`, `check_sv_idiom`, `check_cpp_idiom`, `check_py_idiom`, `check_sh_idiom`, each with `--selftest`; `measure_control_flow --selftest`, `measure_cohesion --selftest` | all 0 |
| Policy and shape gates (13) | `ci_scope --selftest`, `ci_events --check/--selftest`, `pp_srcs --check --selftest`, `check_baremetal_only --check/--selftest`, `check_nvm_capture`, `check_soc_sources` (+`--selftest`), `check_sweep_shape`/`check_deploy_shape`/`check_entity_shape --self-test`, `bash -n sw/litex/sweep_extra.sh` | all 0 |
| Mutants at the head | `mutate.py` over `mutants/item{1,2,2-order,3,4,5,6,6-probe,7,7-grade}.json` (`mutants/item*-head-859fa5d5.log`, per-mutant logs in `mutants/head859-logs-*/`) | 0 mismatches each (81 entries: 59 killed as expected; 22 controls, gap probes and before/after probes passing as expected) |

The item 6 and item 7 mutant runs described in their sections were first taken
on the worktree that became `eb23f044` and `a9cecd23` (`mutants/item6.log`,
`mutants/item7.log`); the rows above are the reruns at the final head.

Earlier runs, kept for the record: the `51ca45c7` gate set
(`gates-*-51ca45c7.tsv`, all rc 0, items 1-5), and the item 1 run
`make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4` at `9e53b116` content
(`SUITE_RC=0` in 3510 s, 137/0, log sha256
`bf0e0463e0749e80df24ce391b1d379c077350600ab891ae76a154274a54a416`).

Not run: hardware, Vivado implementation, act replays, the parent/PP/gPTP/Yosys
native banks (not in the assignment's gate list).

## Head and tree

- Head `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0`, tree
  `ca4085da7d014dbeeedaffa51f185d520ed70c66`, on dev `eaa88a32`; not pushed.
- Commits (one-line subjects, no body, no trailers):
  `9e53b116` item 1, `e4197dc9` item 2, `a71b3bec` item 3, `8c62982f` item 4
  (amended once in the first session, before item 5, to add a nested
  function's docstring that `check_py_idiom.py` required), `51ca45c7` item 5,
  `eb23f044` item 6, `a9cecd23` item 7, `859fa5d5` item 1 README follow-up.
  Nothing after `51ca45c7` was amended or rebased.
- After the gates and mutants: worktree equals HEAD; `git clean -X -d -f`
  removed only ignored byproducts (`sw/builder/out/`, two
  `configs/generated/*.hex`, bytecode caches, the `milan_dp` build outputs);
  `git status --short --ignored` is empty; gptp-processor `5dce647a`,
  protocol-processor `c951a9ff` and verilog-axis `48ff7a7e` at their pins with
  nothing untracked (each checked with `rev-parse --show-toplevel` first).
- Read-only refs fetched into the lane in the first session (no checkout):
  `origin/607-review-evidence` (`14d271cc`, the R382-4 packet, read again for
  item 7's MD and ME) and `origin/pr-609` (`1f039cfe`, item 1's hunk check).

## Files in this directory

- `HANDOFF.md`, `PR-BODY.md` (the body for a new PR).
- `mutate.py` (mutation driver), `mutants/` (specs, logs, per-mutant logs).
- `probe_eq_verdict.py` (item 4 entry-point probe), `probe_ci_lead.py` (item 5).
- `inventory_item6.py`, `inventory_item6.txt` (item 6 inventory against the
  assignment's original shapes: the STOP evidence).
- `inventory_item6_head.py`, `inventory_item6_head.txt` (item 6 inventory by
  the committed parsers), `probe_item6.py` (before/after of every named
  spelling), `gen_item6_spec.py` (writes `mutants/item6.json`).
- `run_ship_probe.py` (item 7 check: one real shipping elaboration),
  `gen_item7_spec.py` (writes `mutants/item7.json`).
- `run_gates.py`, `gates-*.json`, `gates-*-51ca45c7.tsv`,
  `gates-*-859fa5d5.tsv` (gate runner, specs, results).
- `setup_pins_env.sh` (pins-only environment), `run_builder_absent.py`
  (compiler-absent bank).
