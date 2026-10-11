"""Write PR-BODY.md from the recorded results (placeholders where a record is pending)."""
import pathlib, sys
out = pathlib.Path("<home>/milan-fpga-management/2026-09-23/pp151-a593/PR-BODY.md")
table = pathlib.Path(sys.argv[1]).read_text().rstrip("\n")
camp = pathlib.Path(sys.argv[2]).read_text().rstrip("\n")
extra = {k: v for k, v in (a.split("=", 1) for a in sys.argv[3:])}
head = extra.get("head", "PENDING")
closes = extra.get("closes", "Closes #151")
vivado_note = extra.get("vivado_note", "")
ooc = extra.get("ooc", "PENDING")
base_viv = extra.get("base_viv", "PENDING")
viv_mut = extra.get("viv_mut", "PENDING")
body = f"""[A593] Every elaboration guard is a module-scope $fatal, graded as a fatal in every front end

{closes}

Head `{head}`, three commits on main `2cbed0a9`.

## What changes

- **Inventory.** `hdl/` has 31 elaboration-time parameter guards in 13 files, not the 11
  the issue lists: the issue's 11, the AECP set (`KL_aecp_desc_store` 4, `KL_aecp_engine` 5,
  `KL_aecp_notify` 1, `KL_aecp_nvm_writer` 4, `KL_aecp_resp_buf` 3, `KL_aecp_ucpu` 1) and
  `KL_pp_acmp_listener`'s, which sat in an `initial` block. Nothing else in `hdl/` is
  written to stop elaboration (searched: every `$fatal`/`$error`/`$warning`/`$info` in any
  scope, `initial` blocks, `$finish`/`$stop`, constant-function assertions). The table below
  lists all 31 with file:line.
- **Every guard is `if (<condition>) begin : <name> $fatal(1, "<message>"); end` at module
  scope.** 29 `$error(` become `$fatal(1, ` on the same line, continuation lines keeping
  their column as `g_maxp_check` (already `$fatal`) does. The listener's
  `initial begin : parameter_checks if (STRM_TIMEOUT_CYC_P == 0) $fatal(...)` becomes the
  module-scope block `g_strm_tmo_check`, in the same four lines. No condition and no
  message changes, and no line of any RTL file moves.
- **The coding rules record the decision with its measurement**: a new "Elaboration
  guards" row in the HDL engineer guide's section 2, its new section 2.1 (the table below),
  and `hdl/README.md` rule 6.
- **A new suite, `tb/elab_guards`, grades the class of every guard** (`guards.py`, run by
  `make` and so by `scripts/run_suites.sh`). Per guard, a violating case must be refused
  as a `$fatal` of that guard, at its own line, in each front end's own words, and the
  nearest passing case must elaborate clean. Its inventory fails any severity task in
  `hdl/` that is not one of its 31 guards, and any listed guard that is gone. Front ends:
  Verilator lint (`scripts/lint_hdl.sh`'s flags; `%Warning-USERFATAL`), sv2v + Yosys as
  `syn/yosys/run.sh` runs them (`FATAL` or the lowered `$finish`, inside the guard's block),
  and, by `make vivado`, xelab (`[VRFC 10-8279]`) and `synth_design -rtl` (`[Synth 8-6058]`).
  `make mutants` is its proof: for each guard a `$error`, a `$warning` and an
  `initial`-block mutant, plus one mutant per other check, each killed by name.
- **The existing guard benches follow the class.** `tb/nvm_port/elab_bounds.sh` grades the
  deadline guard as a fatal too and gives it the Yosys leg; that leg now accepts Yosys's own
  `FATAL` (sv2v 0.0.12 passes `$fatal` through) besides the lowered `$finish`, and still
  refuses a `$error`'s `ERROR: <message>`. `tb/pp_top/if_guards.py` and `line_guards.py`
  require `USERFATAL`. Five mutation patches (`tb/adp_engine/mutations/if-top-range-*`,
  `tb/pp_top/aecp_dispatch_mutations/line-*`) carry the new task in their context lines;
  all 298 patches under `tb/` apply at the head.

## Why `$fatal`, measured

One probe guard, violating, through each front end (each form elaborates when its
condition is false):

| Violating guard | Verilator 5.050 lint | sv2v 0.0.12 + Yosys 0.66 | sv2v 0.0.13 + Yosys 0.66 | Vivado 2026.1 xelab | Vivado 2026.1 synth_design |
|---|---|---|---|---|---|
| module scope `$fatal(1, ...)` | refused: `%Warning-USERFATAL` | refused: `ERROR: FATAL: .` | refused: `` ERROR: System task `$finish' executed. `` | refused: `[VRFC 10-8279] $fatal` | refused: `[Synth 8-6058] Synth Error` |
| module scope `$error` | refused: `%Warning-USERERROR` | refused: `ERROR: <message>.` | **elaborates** | refused: `[XSIM 43-4462] $error` | refused: `[Synth 8-6058] Synth Error` |
| module scope `$warning` | refused: `%Warning-USERWARN` | **elaborates** | **elaborates** | **elaborates** | **elaborates** |
| module scope `$info` | **elaborates** | **elaborates** | **elaborates** | **elaborates** | **elaborates** |
| `$fatal` in an `initial` block | **elaborates** | refused: ``Can't resolve task name `$fatal'`` | refused: `` System task `$finish' executed. `` | **elaborates** | refused: `[Synth 8-6058] Synth Error` |

This corrects the issue's premise for the pinned toolchain. At sv2v 0.0.12 and Yosys 0.66,
the versions the reference platform's CI pins, a module-scope `$error` *is* refused by
Yosys, because sv2v passes the task through. The miss measured in PR #149 (R449-1 F4, S1)
is sv2v 0.0.13's: it lowers `$error` to an `initial $display`, which Yosys never runs, and
this repository's own hosted `portability` job installs the latest sv2v. Measured on the
real tree with this PR's bench: at base, all 29 `$error` guards elaborate under sv2v 0.0.13.
A per-front-end rule would therefore have kept `$error` and broken on the next sv2v;
`$fatal` is refused under both. Module scope is what Verilator lint and xelab require:
neither runs an `initial` block, so the listener's guard was never seen by either.

## Every guard, every front end (head)

"same text" means Vivado's message is Verilator's, character for character. Yosys 0.66
prints a `$fatal(1, ...)` as `FATAL: .`, taking the finish number for the text; the bench
locates that line inside the guard's block in the lowered file. Rows 28 to 30 have no
violating parameter set (`TMR_AW_C` is `$clog2(TMR_SLOTS_C)`, every base is the running
sum of the extents before it, `TMR_SLOTS_C` is the map's own end; `N_AVB_IF_P = 0` reaches
row 29 only after row 27 refuses), so their violating case moves one derived value by one
in a scratch copy of `hdl/`. Three deadlines pass at 2, not 1: at 1 they elaborate, but
Verilator `-Wall` calls `x >= 32'(N - 1)` constant (`UNSIGNED`).{vivado_note}

<details><summary>31 guards x 5 front ends</summary>

{table}

</details>

At base, the same bench fails 62 checks: 30 Verilator (29 `USERERROR`, and the listener's
guard never reported), 30 Yosys under sv2v 0.0.12 (refused, but as `ERROR: <message>` or
``Can't resolve task name``), and 2 inventory. Under sv2v 0.0.13 the 29 `$error` guards
elaborate. xelab and synth_design at base: {base_viv}.

## Validation

Verilator 5.050 throughout; sv2v 0.0.12 (the binary in the release zip the reference
platform's CI pins, sha256 `ff8c9eea...` for the zip) and Yosys 0.66 built from tag `v0.66`
(`86f2ddeb`); Vivado 2026.1.

| Record | Base `2cbed0a9` | Head | Identity |
|---|---|---|---|
| `./scripts/run_suites.sh` | rc 0, 36 suites, 1,029,620 checks, 0 failing | rc 0, 37 suites, 1,029,775 checks, 0 failing | all 36 suite lines identical; the added line is `PASS elab_guards (155 checks: 155 PASS, 0 FAIL)` |
| `./scripts/lint_hdl.sh` | rc 0, 41 `LINT OK` | rc 0 | identical |
| `make check` | rc 0 | rc 0 | identical but `links: 1187` to `1191` and `ids: 563 files` to `567`: the four links and four files this PR adds |
| `python3 scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | identical |
| `./syn/yosys/run.sh`, sv2v 0.0.12 | rc 0, 42 `YOSYS OK`, parsed once, `YOSYS XILINX OK` | rc 0 | identical but eight Yosys memory warnings whose `all.v:<line>` moves by the one line the lowered listener guard adds; identical with those masked |
| `./syn/yosys/run.sh`, sv2v 0.0.13 | rc 0 | rc 0 | same as above |
| `make -C tb/elab_guards` | (new) | rc 0, 155 of 155 under sv2v 0.0.12 and under 0.0.13 | |
| `make -C tb/elab_guards mutants` | (new) | rc 0, 98 of 98 killed under each sv2v; each `error`, `warning` and `initial` arm killed by both legs under 0.0.12, the `initial` arms by Verilator alone under 0.0.13 | |
| Vivado legs of the campaign (xelab, synth_design) | (new) | {viv_mut} | |
| Netlists | | | 55 of 55 Yosys netlists equal: every `run.sh` top at its defaults (42) and `protocol_processor_top` at 13 more shapes (1x1, 9x9, 4x4, 1x8, 8x1, 16x16, 2x2, 5x5, and the reference platform's five configs as its datapath binds them). Each elaborated in a fresh Yosys as `run.sh` does, written with `-noattr -norename`, compared with source line numbers masked, auto-indices ranked and lines sorted |
| ROM images | `ucode.hex` `518b900c...`, `ltn_rom.hex` `23cc67ee...` | same | identical, and equal to the reference platform's recorded digests for its current pin |
| Vivado out-of-context netlist (`syn/ooc/protocol_processor_ooc.tcl`) | | | {ooc} |

The changed benches' new checks each fail on a planted mutant: `elab_bounds.sh` on
`g_tmo_check` and `g_maxp_check` as `$error` and as `$warning`, under both sv2v (the Yosys
leg alone: `failed, but not at the guard's $fatal` under 0.0.12, `elaborated` under
0.0.13); `if-guards` on `gen_g_avb_if`, and `line-guards` on the engine's three line guards,
as `$error` and as `$warning`. 16 of 16 runs failed their bench.

Every campaign that builds a changed file, base and head, in identical records (output
paths, temp-directory names and seconds masked; drivers that print arms in completion order
compared as sorted lines):

{camp}

## Reference platform, scratch (dev `e8454e27`, gitlink at this head, not committed)

| Gate | gitlink `2cbed0a9` | gitlink head |
|---|---|---|
| `scripts/lint_rtl.py --check --self-test` | rc 0, `LINT GATE: PASS (90 violation(s) <= ratchet 90; 18 waived, 0 justified lint_off)` | identical |
| `syn/yosys/run.sh --mode elaborate` (every top) | rc 0, 61 tops PASS, tap purity PASS | identical (timings masked) |
| its own lint of `milan_datapath` at each of the five shipping configs | no `USER*` diagnostic from any path | identical |

No shipping shape trips a guard. The raw Verilator output was read for that, because of
the finding below.

## Findings outside this PR

- **The reference platform's lint gate cannot see a processor guard.** Its
  `scripts/lint_rtl.py` drops every Verilator diagnostic under `protocol-processor/` before
  its hard-error test, and never reads Verilator's exit status. With `KL_pp_shadow` linted
  at `-GN_STREAM_IN_P=40`, Verilator exits 1 with
  `%Warning-USERFATAL: protocol-processor/hdl/top/protocol_processor_top.sv:911:5: F08.4: owner tags OVERLAP at SI=40 SO=8 (8-bit expiry bus)`
  at this head (`%Warning-USERERROR` at base), and the gate reports 0 hard errors either
  way. Verilator, run as the platform runs it, refuses the guard; the platform's wrapper
  hides it whatever the severity. That needs a change there (for example: a `USERFATAL` from
  any path, or a non-zero exit with no counted finding, is a hard error). The platform's
  Yosys elaboration does stop on it.
- At base, with the pinned sv2v 0.0.12 on PATH, `tb/nvm_port`'s `elab_bounds.sh` failed
  (`YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the guard's $finish`): its Yosys leg
  knew only sv2v 0.0.13's words. Fixed here. The base suite record above is therefore taken
  with sv2v 0.0.13 on PATH, as is the head's.
- Outside this PR's scope and left as they are: `docs/guides/integrator.md:114` ("raises
  `$error`") and the text in `docs/diagrams/21-integration-faces.svg` ("stops the build with
  $error") now name the old task, and `docs/architecture/09_verification.md`'s table has no
  row for `tb/elab_guards`.
- The hosted suites job has no sv2v or yosys, so `tb/elab_guards` runs its Verilator leg
  there (93 checks); its Yosys leg runs wherever both are installed. The `portability` job,
  which has them unpinned, does not run the suite.

## Reproduce

```sh
./scripts/run_suites.sh
./scripts/lint_hdl.sh
make check
python3 scripts/gen_matrix.py --check
./syn/yosys/run.sh
make -C tb/elab_guards
make -C tb/elab_guards vivado
make -C tb/elab_guards mutants MUTANT_OUTPUT=<new directory>
```
"""
out.write_text(body)
