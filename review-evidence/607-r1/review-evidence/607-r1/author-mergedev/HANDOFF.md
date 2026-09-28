# [A427] Merge-dev round for PR #615 (#607)

Status: **REVIEW READY at merge head `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5`** (tree
`554756a545927a7e1aba734e2b7d8f4e90ba63cd`). The continuation ran after the manager disposition.
The merge, composition proof, three-seed re-sweep and every gate passed. No STOP condition occurred.

- Assignment: issue #607 comment 5874480647 (merge-dev round, executor [A427]).
- Disposition: issue #607 comment 5874542826. After the merge the `protocol-processor`
  gitlink equals dev's `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`; this lane changes no
  processor pin of its own.
- Branch `607-xdc-clock-names` at `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3`; dev
  `7390b43627032c71c470e2aa8d0845eb5b740663`.

## 1. Preconditions (continuation)

| Check | Result |
| --- | --- |
| `git remote get-url origin` | `https://github.com/kebag-logic/milan-fpga.git` |
| `git rev-parse HEAD` before the merge | `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3`, clean worktree |
| `git fetch origin dev`; `git rev-parse origin/dev` | `7390b43627032c71c470e2aa8d0845eb5b740663` |
| `git -C protocol-processor rev-parse --show-toplevel` | the lane's own `protocol-processor` directory (checked before every processor git command) |
| Merge base | `54ce877371ee6e8878cf67294e86c2a8481b62f6` |

Git commands ran with `core.commitGraph` disabled through `GIT_CONFIG_*`, which silences a local
commit-graph warning. No commit hooks are installed in this clone.

## 2. Merge and resolved hunks

`git merge --no-ff --no-commit origin/dev` stopped on exactly the three permitted files:
`docs/integration/BUILDING.md`, `sw/builder/test_builder.py` and
`sw/litex/platforms/alinx_ax7101.py`. `docs/litex/LITEX_SOC.md`, `docs/testing/RUNNING_TESTS.md`
and `sw/litex/milan_soc.py` auto-merged and got no manual edit.

- Merge commit: `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5`, subject
  `Merge dev into 607-xdc-clock-names`, no body, no trailers.
- Parents: `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` and
  `7390b43627032c71c470e2aa8d0845eb5b740663`.
- Tree: `554756a545927a7e1aba734e2b7d8f4e90ba63cd`.
- Gitlinks in the merge tree:
  - `protocol-processor` `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`, dev's pin, as the
    disposition requires;
  - `external` `efeb541a`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e`,
    unchanged.
- After the merge, `git submodule update --checkout protocol-processor` moved the checkout to
  `c951a9ff`. `git submodule status` shows it clean at that commit, and it has no nested
  submodules.
- `git diff --name-only $(git merge-tree --write-tree a9f5e34f 7390b436) HEAD` names only the
  three resolved files.

Resolution rules applied (assignment rule 1):
- **Platform.** Both imports stay. The lane's `BoundedEthVivadoToolchain` replacement still runs
  first. #395's `configure_commands()` pre-placement hooks and its `kl_timing_grade_reports`
  post-route hook come after it, as the lane's comment requires ("Keep all hook configuration
  below this"). Hooks added to the old toolchain would be discarded by the replacement.
- **`test_builder.py`.** Both functions stay, and the run list holds both entries once each:
  `test_commercial_timing_grade` first, as on dev, and `test_clock_crossing_constraints` where the
  lane put it. No gate number collides: the lane adds no `[gate N]` id and dev adds only `36b`.
  No function is defined twice, and no run-list entry repeats among 96 entries.
- **`BUILDING.md`.** Both blocks stay unedited: #395's grade, corner and checkpoint-report text,
  then #607's refusal gate, Ethernet bound and sweep-retention text. The grade block comes first
  because it defines the declared corners that the #607 margin sentence applies.

Each resolved file was rebuilt exactly from its saved conflicted copy by these rules
(byte-equal to the committed file).

### `docs/integration/BUILDING.md`

Hunk 1 (line 517 of the conflicted file). Before, verbatim:

````text
<<<<<<< HEAD
Every completed implementation is checked for rejected constraints (#607).
`milan_soc.py` reads `gateware/vivado.log` before publishing the flash manifest.
Emitted `12-4739`, `20-1307` and `12-5201` diagnostics fail every board's build.
An absent log also fails. All launchers use this same check.
Refusal renames adjacent `*.bit` files to `*.bit.rejected`.
This also applies when the implementation log cannot be read.
Rejected bytes remain available for diagnosis, outside automatic bitstream discovery.
Only compare seeds whose launch succeeded and flash manifest exists.
Require an unquarantined bitstream too; timing summaries alone cannot qualify.

AX7101 Ethernet data crossings to and from the system and Milan clocks have
an 8 ns datapath-only bound. Clock selections derive from the SoC signals.
The post-synthesis hook in
[`clock_constraints.tcl`](../../sw/litex/clock_constraints.tcl) scopes LiteX's
MultiReg false paths away from those pairs before optimization.
Other MultiReg paths retain their false paths, including asynchronous inputs.
Reset-synchronizer PRE pins retain their asynchronous-assert exceptions;
the inter-stage reset bound remains 2 ns. Hold is excluded across Ethernet
clock pairs because their clock phases are unrelated.
Quasi-static tagged registers receive setup-4/hold-3 multicycles in the same
Tcl phase, outside the XDC. An empty tagged class adds no exception.

Retain the implementation log and its emitted critical-warning census,
`*_clock_interaction.rpt`, and `*_exceptions.rpt` with every sweep seed.
The Ethernet data pairs must read `Max Delay Datapath Only`, with no unsafe
pair, and meet the 8 ns bound. Check WNS >= +0.03 ns and WHS >= 0 at every
corner for AX7101, following the
[#395 margin decision](https://github.com/kebag-logic/milan-fpga/issues/395).
These timing margins remain manual acceptance checks.
=======
The AX7101 dev-board release declares **commercial grade, 0 to 85 C junction**
under the [owner decision on #395](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5789765635).
The board's industrial marking does not expand this release claim.
[`TIMING_GRADE`](../../sw/litex/platforms/ax7101_timing.py) is the executable
declaration of the part, grade, temperature endpoints and timing models.
The platform derives its part and pre-placement hook from that declaration.
Before bitstream generation, the hook refuses a changed part, power condition
or disabled setup/hold analysis, then writes `*_signoff_*` reports.

Signoff analyses **both setup and hold at both Slow and Fast corners**.
Artix-7 speed files bound process, voltage and temperature; they do not
provide four separately selectable slow/fast-by-temperature models.
`set_operating_conditions -junction_temp` selects a power-estimation condition,
not a temperature-prorated timing model. Reports at both declared endpoints
therefore repeat each fixed timing model; retain that distinction with the
WNS, TNS, WHS and THS table. See
[UG835 operating conditions](https://docs.amd.com/r/2021.1-English/ug835-vivado-tcl-commands/report_operating_conditions)
and [UG906 max/min analysis](https://docs.amd.com/r/en-US/ug906-vivado-design-analysis/Max-and-Min-Delay-Analysis).

The [margin decision on #395](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611)
requires WNS >= +0.03 ns and WHS >= 0.
Apply both thresholds at every declared corner.
This is the AX7101 margin required after QSPI flashboot corruption.
These thresholds are **not automatically enforced**.
The [margin correction](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860783553)
confirms that `sweep.sh` launches three placement directives; the seed pick is manual.

For a saved routed checkpoint, generate the same report hook without rebuilding:

```sh
python3 -B sw/litex/report_timing_grade.py <routed.dcp> <report-dir>
cd <report-dir>
timeout --foreground 1800 vivado -mode batch -nojournal -notrace \
  -log timing.log -source report.tcl
```

Use a report directory outside the candidate and a physical filesystem path.
The script caps analysis at 16 threads and never writes a checkpoint or bitstream.
Retain the input checkpoint and bitstream hashes, original implementation recipe,
speed-file revision, all four slack metrics, clock interaction, CDC and verbose
unconstrained-path reports. Retain the implementation log's CRITICAL WARNING census,
including diagnostic codes, source locations and original log line numbers.
An absent or rejected constraint limits the signoff claim.
Positive slack cannot clear that missing coverage.
Negative slack is a finding with its paths;
missing I/O constraints and CDC diagnostics remain visible even with positive WNS.
The [shipping-candidate measurement](../findings/COMMERCIAL_TIMING_395.md)
records these limits. Temperature logging and oscillator measurements remain
separate work under #395 items 3 and 4.
>>>>>>> origin/dev
````

After, verbatim:

````text
The AX7101 dev-board release declares **commercial grade, 0 to 85 C junction**
under the [owner decision on #395](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5789765635).
The board's industrial marking does not expand this release claim.
[`TIMING_GRADE`](../../sw/litex/platforms/ax7101_timing.py) is the executable
declaration of the part, grade, temperature endpoints and timing models.
The platform derives its part and pre-placement hook from that declaration.
Before bitstream generation, the hook refuses a changed part, power condition
or disabled setup/hold analysis, then writes `*_signoff_*` reports.

Signoff analyses **both setup and hold at both Slow and Fast corners**.
Artix-7 speed files bound process, voltage and temperature; they do not
provide four separately selectable slow/fast-by-temperature models.
`set_operating_conditions -junction_temp` selects a power-estimation condition,
not a temperature-prorated timing model. Reports at both declared endpoints
therefore repeat each fixed timing model; retain that distinction with the
WNS, TNS, WHS and THS table. See
[UG835 operating conditions](https://docs.amd.com/r/2021.1-English/ug835-vivado-tcl-commands/report_operating_conditions)
and [UG906 max/min analysis](https://docs.amd.com/r/en-US/ug906-vivado-design-analysis/Max-and-Min-Delay-Analysis).

The [margin decision on #395](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611)
requires WNS >= +0.03 ns and WHS >= 0.
Apply both thresholds at every declared corner.
This is the AX7101 margin required after QSPI flashboot corruption.
These thresholds are **not automatically enforced**.
The [margin correction](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860783553)
confirms that `sweep.sh` launches three placement directives; the seed pick is manual.

For a saved routed checkpoint, generate the same report hook without rebuilding:

```sh
python3 -B sw/litex/report_timing_grade.py <routed.dcp> <report-dir>
cd <report-dir>
timeout --foreground 1800 vivado -mode batch -nojournal -notrace \
  -log timing.log -source report.tcl
```

Use a report directory outside the candidate and a physical filesystem path.
The script caps analysis at 16 threads and never writes a checkpoint or bitstream.
Retain the input checkpoint and bitstream hashes, original implementation recipe,
speed-file revision, all four slack metrics, clock interaction, CDC and verbose
unconstrained-path reports. Retain the implementation log's CRITICAL WARNING census,
including diagnostic codes, source locations and original log line numbers.
An absent or rejected constraint limits the signoff claim.
Positive slack cannot clear that missing coverage.
Negative slack is a finding with its paths;
missing I/O constraints and CDC diagnostics remain visible even with positive WNS.
The [shipping-candidate measurement](../findings/COMMERCIAL_TIMING_395.md)
records these limits. Temperature logging and oscillator measurements remain
separate work under #395 items 3 and 4.

Every completed implementation is checked for rejected constraints (#607).
`milan_soc.py` reads `gateware/vivado.log` before publishing the flash manifest.
Emitted `12-4739`, `20-1307` and `12-5201` diagnostics fail every board's build.
An absent log also fails. All launchers use this same check.
Refusal renames adjacent `*.bit` files to `*.bit.rejected`.
This also applies when the implementation log cannot be read.
Rejected bytes remain available for diagnosis, outside automatic bitstream discovery.
Only compare seeds whose launch succeeded and flash manifest exists.
Require an unquarantined bitstream too; timing summaries alone cannot qualify.

AX7101 Ethernet data crossings to and from the system and Milan clocks have
an 8 ns datapath-only bound. Clock selections derive from the SoC signals.
The post-synthesis hook in
[`clock_constraints.tcl`](../../sw/litex/clock_constraints.tcl) scopes LiteX's
MultiReg false paths away from those pairs before optimization.
Other MultiReg paths retain their false paths, including asynchronous inputs.
Reset-synchronizer PRE pins retain their asynchronous-assert exceptions;
the inter-stage reset bound remains 2 ns. Hold is excluded across Ethernet
clock pairs because their clock phases are unrelated.
Quasi-static tagged registers receive setup-4/hold-3 multicycles in the same
Tcl phase, outside the XDC. An empty tagged class adds no exception.

Retain the implementation log and its emitted critical-warning census,
`*_clock_interaction.rpt`, and `*_exceptions.rpt` with every sweep seed.
The Ethernet data pairs must read `Max Delay Datapath Only`, with no unsafe
pair, and meet the 8 ns bound. Check WNS >= +0.03 ns and WHS >= 0 at every
corner for AX7101, following the
[#395 margin decision](https://github.com/kebag-logic/milan-fpga/issues/395).
These timing margins remain manual acceptance checks.
````

### `sw/builder/test_builder.py`

Hunk 1 (line 27795 of the conflicted file). Before, verbatim:

```text
<<<<<<< HEAD
def test_clock_crossing_constraints() -> None:
    """Run shipping elaborations, scoped exceptions and implementation-log controls."""
    python = _litex_or_skip("607 clock constraints")
    if python is not None:
        subprocess.run([python, str(ROOT / "sw/builder/test_clock_constraints.py")],
                       check=True, cwd=ROOT, timeout=2700)
=======
def test_commercial_timing_grade() -> None:
    """Pin the release conditions and prove that the real platform consumes them."""
    from test_timing_grade import test_platform_hooks, test_pll_grade, test_timing_grade_contract

    test_timing_grade_contract()
    python = _litex_or_skip("timing grade platform")
    if python is not None:
        test_platform_hooks(python)
        test_pll_grade(python)
>>>>>>> origin/dev
```

After, verbatim:

```text
def test_clock_crossing_constraints() -> None:
    """Run shipping elaborations, scoped exceptions and implementation-log controls."""
    python = _litex_or_skip("607 clock constraints")
    if python is not None:
        subprocess.run([python, str(ROOT / "sw/builder/test_clock_constraints.py")],
                       check=True, cwd=ROOT, timeout=2700)


def test_commercial_timing_grade() -> None:
    """Pin the release conditions and prove that the real platform consumes them."""
    from test_timing_grade import test_platform_hooks, test_pll_grade, test_timing_grade_contract

    test_timing_grade_contract()
    python = _litex_or_skip("timing grade platform")
    if python is not None:
        test_platform_hooks(python)
        test_pll_grade(python)
```

Hunk 2 (line 27824 of the conflicted file). Before, verbatim:

```text
<<<<<<< HEAD
    for fn in (test_baremetal_clock_contract, test_gptp_rom_clock, test_extra_sweep_clocks, test_tap_clock_docs,
               test_declaration_contracts, test_clock_crossing_constraints,
               test_all_configs_build, test_baremetal_profile_contract,
=======
    for fn in (test_commercial_timing_grade,
               test_baremetal_clock_contract, test_gptp_rom_clock, test_extra_sweep_clocks, test_tap_clock_docs,
               test_declaration_contracts, test_all_configs_build, test_baremetal_profile_contract,
>>>>>>> origin/dev
```

After, verbatim:

```text
    for fn in (test_commercial_timing_grade,
               test_baremetal_clock_contract, test_gptp_rom_clock, test_extra_sweep_clocks, test_tap_clock_docs,
               test_declaration_contracts, test_clock_crossing_constraints,
               test_all_configs_build, test_baremetal_profile_contract,
```

### `sw/litex/platforms/alinx_ax7101.py`

Hunk 1 (line 19 of the conflicted file). Before, verbatim:

```text
<<<<<<< HEAD
from clock_constraints import BoundedEthVivadoToolchain
=======
from platforms.ax7101_timing import TIMING_GRADE, configure_commands
>>>>>>> origin/dev
```

After, verbatim:

```text
from clock_constraints import BoundedEthVivadoToolchain
from platforms.ax7101_timing import TIMING_GRADE, configure_commands
```

Hunk 2 (line 304 of the conflicted file). Before, verbatim:

```text
<<<<<<< HEAD
        if toolchain == "vivado":
            # Replace before adding any hooks; state on the old toolchain
            # would be discarded. Keep all hook configuration below this.
            self.toolchain = BoundedEthVivadoToolchain()
=======
        for command in configure_commands():
            # LiteX formats these strings once while writing the build Tcl.
            self.toolchain.pre_placement_commands.append(
                command.replace("{", "{{").replace("}", "}}"))
>>>>>>> origin/dev
```

After, verbatim:

```text
        if toolchain == "vivado":
            # Replace before adding any hooks; state on the old toolchain
            # would be discarded. Keep all hook configuration below this.
            self.toolchain = BoundedEthVivadoToolchain()
        for command in configure_commands():
            # LiteX formats these strings once while writing the build Tcl.
            self.toolchain.pre_placement_commands.append(
                command.replace("{", "{{").replace("}", "}}"))
```

## 3. Composition proof

**Auto-merged `milan_soc.py`.** Dev's only changes there are the PLL speed grade derived from the
platform part (`sw/litex/milan_soc.py:230`) and the shipping AEM image check (`:3311-3325`). The
lane's lines are unchanged and still apply: the import (`:62`), the CRG bounded/async clock lists
(`:246-269`, `:425-459`), `add_quasi_static_constraints` (`:1519`), `add_eth_constraints` (`:2735`)
and the implementation-log gate after every `--build` (`:3966`).

**Merged platform (`sw/litex/platforms/alinx_ax7101.py:296-322`).** The part is `TIMING_GRADE["part"]`.
The lane's toolchain replacement comes first, then #395's two `configure_commands()` pre-placement
lines, then `bitstream_commands` with `kl_timing_grade_reports {build_name}_signoff` first. The
lane's `report_clock_interaction`/`report_exceptions` hooks are appended by the SoC afterwards.

**Real emitted Tcl.** This is `alinx_ax7101.tcl` from the asl seed build at the merge head; eto and
eppo have the same line numbers, and `collect_sweep.py` asserts the order for each. Lines are
verbatim, except that the `synth_design` include list is shortened:

```text
258: synth_design -directive AreaOptimized_high -top alinx_ax7101 -part xc7a100t-fgg484-2 -include_dirs {...}
265: write_checkpoint -force alinx_ax7101_synth.dcp
269: source {$LANES/607-xdc-clock-names/sw/litex/clock_constraints.tcl}
270: kl_quasi_static_constraints
271: milan_eth_constraints eth_clocks0_rx [list milansoc_crg_clkout0 milansoc_crg_clkout1] [list milansoc_crg_pll_audio_fb milansoc_crg_audio_ref_raw milansoc_crg_audio_mclk_raw milansoc_crg_clkout2 milansoc_crg_clkout3 milansoc_crg_clkout4]
275: opt_design -directive ExploreArea
279: source {$LANES/607-xdc-clock-names/sw/litex/timing_grade.tcl}
280: kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}
284: place_design -directive AltSpreadLogic_high
303: route_design -directive AggressiveExplore
305: write_checkpoint -force alinx_ax7101_route.dcp
314: kl_timing_grade_reports alinx_ax7101_signoff
320: report_clock_interaction -delay_type min_max -file alinx_ax7101_clock_interaction.rpt
321: report_exceptions -file alinx_ax7101_exceptions.rpt
325: write_bitstream -force alinx_ax7101.bit 
```

- The Ethernet hook (`milan_eth_constraints`, with its `clock_constraints.tcl` source and
  `kl_quasi_static_constraints`) is still between `synth_design` and `opt_design`, in the
  pre-optimize phase.
- #395's `kl_timing_grade_configure` runs between `opt_design` and `place_design`, and
  `kl_timing_grade_reports alinx_ax7101_signoff` runs after `route_design`, before `write_bitstream`.
- The two lanes write different report names: `alinx_ax7101_signoff_clock_interaction.rpt` (#395) and
  `alinx_ax7101_clock_interaction.rpt` (#607). No file collides.
- Each seed's `vivado.log` shows the Ethernet hook applied (`CONSTRAINTS: quasi_static cells=112
  setup=4 hold=3`, `eth=eth_clocks0_rx bounded=milansoc_crg_clkout0 milansoc_crg_clkout1 ...
  budget_ns=8.000`, `MultiReg eth=12 part=198 other=0`).
- #395's corner reports ran in every seed build: `alinx_ax7101_signoff_grade.txt` plus the
  `_{Slow,Fast}_{0,85}C_{operating,timing,negative}.rpt` sets, `_all_timing.rpt`,
  `_clock_interaction.rpt`, `_cdc.rpt` and `_check_timing.rpt`. The grade file reads
  `part xc7a100tfgg484-2 grade commercial min_c 0 max_c 85 corners {Slow Fast}`.
- The build gate accepted every seed (`[constraints] .../vivado.log: no 12-4739, 20-1307 or 12-5201
  diagnostics`). Each gateware directory holds `alinx_ax7101.bit` and no `.bit.rejected`, and
  `flashboot_layout.json` exists.
- The ROMs the builds generated from the `c951a9ff` processor checkout match dev's
  `syn/yosys/rom_digests.tsv` rows for that pin: `ltn_rom.hex` `23cc67ee…` and `ucode.hex` `23605682…`.

The shipping-hook test, #395's timing-grade test and the pins-only bank are in the gate table
(section 4).

## 4. Gate table (all at merge head `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5`)

`run_gates.py <mode>` writes `gate-results-c7ee5cbd4-<mode>.json` for the modes pins, hooks,
builder, live, hdlref and docs. `run_all_gates.sh` ran pins, hooks, builder, live and docs in
sequence after the sweep had finished, so only one writer used the lane at a time. Each command:
- runs directly from the lane (the physical `/data` path), with stdout/stderr to its own log under
  `$VALIDATION_STORAGE/607-a427/gates-c7ee5cbd4/` and nothing piped;
- has HEAD asserted before it runs;
- has a receipt recording the command, rc, duration, and log size and SHA-256.

At the end, all 90 receipts were re-verified: head `c7ee5cbd`, log hash matches, and all rc 0 except
the two refused rows below. The worktree was clean after every mode. The long runs were supervised
background jobs awaited in back-to-back foreground waits. Nothing was left running, and nothing ran
concurrently in the lane.

Environments:
- **pins**: `pins_env.sh` only. Fresh pins-only environment built by `setup_pins_env.sh` (rc 0,
  `setup-pins-env.log` under the work directory): CPython 3.12.13, exactly `sw/litex/litex_pins.txt`,
  the VexiiRiscv checkout, the patch series and the digest-checked RV32 SDK. No
  `pythondata_software_picolibc` or `compiler_rt`. Dev changed none of these inputs, nor
  `.github/workflows`.
- **bench**: system `python3` with `MILAN_LITEX_PYTHON` set to the bench LiteX interpreter,
  `PYTHONHASHSEED=0` and `TMPDIR` under `/data`.
- **docs**: the pinned Markdown environment `$VALIDATION_TOOLS/md-venv-40cdefe08ebd` first on
  `PATH`, so `python3` and `sys.executable` are both that interpreter, for every docs-check-job gate.
- **Bases**: the em-dash gate and the committed `git diff --check` use dev `7390b436`, the merge's
  dev parent, which is what the hosted PR event computes as its merge base.
- **Commit graph**: `git` commit-graph use is disabled through `GIT_CONFIG_*`.

| Gate | Mode | Command | rc | Seconds |
| --- | --- | --- | ---: | ---: |
| pins-bank | pins | `sh <packet>/pins_env.sh <lane> <work> python3 sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | 643.34 |
| shipping-hook-bench | hooks | `<bench python> -B sw/builder/test_clock_constraints.py` | 0 | 8.28 |
| shipping-hook-pins | hooks | `sh <packet>/pins_env.sh <lane> <work> python3 -B sw/builder/test_clock_constraints.py` | 0 | 7.33 |
| timing-grade-bench | hooks | `python3 -B sw/builder/test_timing_grade.py <bench python>` | 0 | 0.41 |
| timing-grade-pins | hooks | `sh <packet>/pins_env.sh <lane> <work> python3 -B sw/builder/test_timing_grade.py python3` | 0 | 0.36 |
| builder-present | builder | `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration` | 0 | 770.32 |
| builder-absent | builder | `python3 -B <packet>/run_builder_absent.py` | 0 | 571.18 |
| live-plant | live | `<bench python> -B sw/builder/test_clock_constraints.py --vivado <vivado> --checkpoint <shipping routed checkpoint> --evidence-dir <work>/live-plant-c7ee5cbd4` | 0 | 32.63 |
| gen_hdl_reference-selftest | hdlref | `python3 -B scripts/gen_hdl_reference.py --selftest` | 0 | 0.21 |
| gen_hdl_reference-output | hdlref | `python3 -B scripts/gen_hdl_reference.py --output <work>/hdl-reference-c7ee5cbd4` | 0 | 1.52 |
| docs_check | docs | `python3 -B scripts/docs_check.py` | 0 | 4.62 |
| check_em_dash-base | docs | `python3 -B scripts/check_em_dash.py --base 7390b43627032c71c470e2aa8d0845eb5b740663` | 0 | 2.92 |
| check_em_dash-selftest | docs | `python3 -B scripts/check_em_dash.py --selftest` | 0 | 3.02 |
| check_doc_style | docs | `python3 -B scripts/check_doc_style.py` | 0 | 0.06 |
| check_doc_style-selftest | docs | `python3 -B scripts/check_doc_style.py --selftest` | 0 | 0.06 |
| check_gptp_docs | docs | `python3 -B scripts/check_gptp_docs.py` | 0 | 0.16 |
| check_gptp_docs-selftest | docs | `python3 -B scripts/check_gptp_docs.py --selftest` | 0 | 0.21 |
| DOC_MAP.gen-check | docs | `python3 -B docs/DOC_MAP.gen.py --check` | 0 | 0.41 |
| DOC_MAP.gen-selftest | docs | `python3 -B docs/DOC_MAP.gen.py --selftest` | 0 | 0.46 |
| timesync_chain.gen-check | docs | `python3 -B docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.36 |
| timesync_chain.gen-selftest | docs | `python3 -B docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.41 |
| check_solution_docs | docs | `python3 -B scripts/check_solution_docs.py` | 0 | 0.11 |
| check_solution_docs-selftest | docs | `python3 -B scripts/check_solution_docs.py --selftest` | 0 | 2.57 |
| submodule_boundaries.gen-check | docs | `python3 -B docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.36 |
| submodule_boundaries.gen-selftest | docs | `python3 -B docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.46 |
| check_submodule_docs | docs | `python3 -B scripts/check_submodule_docs.py` | 0 | 0.41 |
| check_submodule_docs-selftest | docs | `python3 -B scripts/check_submodule_docs.py --selftest` | 0 | 0.06 |
| gen_wavedrom-selftest | docs | `python3 -B scripts/gen_wavedrom.py --selftest` | 0 | 0.16 |
| gen_wavedrom-wd_axis_backpressure.json | docs | `python3 -B scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.31 |
| gen_wavedrom-wd_cdc_handshake.json | docs | `python3 -B scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.41 |
| gen_wavedrom-wd_gptp_pdelay.json | docs | `python3 -B scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.36 |
| check_diagram_pngs | docs | `python3 -B scripts/check_diagram_pngs.py` | 0 | 0.36 |
| check_diagram_pngs-selftest | docs | `python3 -B scripts/check_diagram_pngs.py --selftest` | 0 | 6.52 |
| check_feature_status-self-test | docs | `python3 -B scripts/check_feature_status.py --self-test` | 0 | 0.71 |
| check_feature_status | docs | `python3 -B scripts/check_feature_status.py` | 0 | 0.71 |
| gen_module_matrix-check | docs | `python3 -B docs/traceability/gen_module_matrix.py --check` | 0 | 0.97 |
| check_gptp_docs-with-submodule | docs | `python3 -B scripts/check_gptp_docs.py --with-submodule` | 0 | 0.16 |
| measure_control_flow-selftest | docs | `python3 -B scripts/measure_control_flow.py --selftest` | 0 | 0.16 |
| measure_cohesion-selftest | docs | `python3 -B scripts/measure_cohesion.py --selftest` | 0 | 0.06 |
| check_baremetal_only-check | docs | `python3 -B scripts/check_baremetal_only.py --check` | 0 | 15.29 |
| check_baremetal_only-selftest | docs | `python3 -B scripts/check_baremetal_only.py --selftest` | 0 | 6.38 |
| test_firmware_compiler-selftest | docs | `python3 -B sw/builder/test_firmware_compiler.py --selftest` | 0 | 1.37 |
| test_firmware_compiler-absent | docs | `python3 -B sw/builder/test_firmware_compiler.py --absent --audit <work>/firmware-absent-c7ee5cbd4.jsonl` | 0 | 439.24 |
| check_nvm_record_space | docs | `python3 -B scripts/check_nvm_record_space.py` | 0 | 2.07 |
| check_nvm_record_space-self-test | docs | `python3 -B scripts/check_nvm_record_space.py --self-test` | 0 | 31.44 |
| check_nvm_capture | docs | `python3 -B scripts/check_nvm_capture.py` | 0 | 0.77 |
| test_nvm_firmware-self-test | docs | `python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 39.13 |
| check_soc_sources | docs | `python3 -B scripts/check_soc_sources.py` | 0 | 0.11 |
| check_soc_sources-selftest | docs | `python3 -B scripts/check_soc_sources.py --selftest` | 0 | 0.21 |
| iob_pack_selftest | docs | `python3 -B sw/litex/iob_pack_selftest.py` | 0 | 2.07 |
| check_rtl_source_lists | docs | `python3 -B scripts/check_rtl_source_lists.py` | 0 | 1.42 |
| check_rtl_source_lists-selftest | docs | `python3 -B scripts/check_rtl_source_lists.py --selftest` | 0 | 2.67 |
| measure_naming-check | docs | `python3 -B scripts/measure_naming.py --check` | 0 | 0.46 |
| measure_naming-selftest | docs | `python3 -B scripts/measure_naming.py --selftest` | 0 | 0.46 |
| check_port_contracts | docs | `python3 -B scripts/check_port_contracts.py` | 0 | 2.32 |
| check_port_contracts-selftest | docs | `python3 -B scripts/check_port_contracts.py --selftest` | 0 | 2.62 |
| measure_fail_fast-check | docs | `python3 -B scripts/measure_fail_fast.py --check` | 0 | 1.47 |
| measure_fail_fast-selftest | docs | `python3 -B scripts/measure_fail_fast.py --selftest` | 0 | 1.42 |
| check_todo_ownership | docs | `python3 -B scripts/check_todo_ownership.py` | 0 | 1.47 |
| check_todo_ownership-selftest | docs | `python3 -B scripts/check_todo_ownership.py --selftest` | 0 | 1.47 |
| measure_test_evidence-check | docs | `python3 -B scripts/measure_test_evidence.py --check` | 0 | 5.52 |
| measure_test_evidence-selftest | docs | `python3 -B scripts/measure_test_evidence.py --selftest` | 0 | 5.63 |
| check_hygiene-check | docs | `python3 -B scripts/check_hygiene.py --check` | 0 | 0.36 |
| check_hygiene-selftest | docs | `python3 -B scripts/check_hygiene.py --selftest` | 0 | 0.36 |
| check_sv_idiom | docs | `python3 -B scripts/check_sv_idiom.py` | 0 | 0.41 |
| check_sv_idiom-selftest | docs | `python3 -B scripts/check_sv_idiom.py --selftest` | 0 | 0.41 |
| check_cpp_idiom | docs | `python3 -B scripts/check_cpp_idiom.py` | 0 | 1.22 |
| check_cpp_idiom-selftest | docs | `python3 -B scripts/check_cpp_idiom.py --selftest` | 0 | 1.32 |
| check_py_idiom | docs | `python3 -B scripts/check_py_idiom.py` | 0 | 3.52 |
| check_py_idiom-selftest | docs | `python3 -B scripts/check_py_idiom.py --selftest` | 0 | 3.52 |
| check_sh_idiom | docs | `python3 -B scripts/check_sh_idiom.py` | 0 | 0.21 |
| check_sh_idiom-selftest | docs | `python3 -B scripts/check_sh_idiom.py --selftest` | 0 | 0.26 |
| ci_events-check | docs | `python3 -B scripts/ci_events.py --check` | 0 | 0.21 |
| ci_events-selftest | docs | `python3 -B scripts/ci_events.py --selftest` | 0 | 14.94 |
| check_doc_paths | docs | `python3 -B scripts/check_doc_paths.py` | 0 | 0.11 |
| check_archive | docs | `python3 -B scripts/check_archive.py` | 0 | 0.31 |
| check_archive-selftest | docs | `python3 -B scripts/check_archive.py --selftest` | 0 | 0.06 |
| gen_toc-selftest | docs | `python3 -B scripts/gen_toc.py --selftest` | 0 | 0.82 |
| gen_toc-verify-anchors | docs | `python3 -B scripts/gen_toc.py --verify-anchors` | 0 | 1.72 |
| gen_toc-check | docs | `python3 -B scripts/gen_toc.py --check` | 0 | 2.92 |
| gen_aem_store-self-test | docs | `python3 -B avdecc/gen_aem_store.py --self-test` | 0 | 0.06 |
| check_sweep_shape-self-test | docs | `python3 -B scripts/check_sweep_shape.py --self-test` | 0 | 11.75 |
| check_deploy_shape-self-test | docs | `python3 -B scripts/check_deploy_shape.py --self-test` | 0 | 0.42 |
| check_entity_shape-self-test | docs | `python3 -B scripts/check_entity_shape.py --self-test` | 0 | 41.35 |
| check_wire_accountability-self-test | docs | `python3 -B scripts/check_wire_accountability.py --self-test` | 0 | 0.26 |
| gptp-docs | docs | `make -C gptp-processor docs` | 0 | 0.71 |
| git-diff-worktree | docs | `git diff --check` | 0 | 0.03 |
| git-diff-committed | docs | `git diff --check 7390b43627032c71c470e2aa8d0845eb5b740663 HEAD` | 0 | 0.03 |

88 passing rows.

**Two refused rows, superseded (environment routing, not a tree finding).** In the docs mode, the two
HDL-reference rows ran in the Markdown environment, which does not carry `pyslang==11.0.0`
(`tools/hdl_reference/requirements.txt`). Both refused before doing any work:
`gen_hdl_reference: REFUSED: the pinned parser is unavailable`. These are not Markdown gates. The
`hdlref` mode re-ran them the round-1/round-3 way: system `python3` with the read-only
`$VALIDATION_STORAGE/607-a408-work/docdeps` (which holds `pyslang` 11.0.0) on `PYTHONPATH`. Both were rc 0
(self-test 44/44 arms). The refused logs are kept under `gates-c7ee5cbd4/docs-mode-refused/` and still
match the docs receipt's hashes.

| Gate | Mode | Command | rc | Seconds |
| --- | --- | --- | ---: | ---: |
| gen_hdl_reference-selftest | docs | `python3 -B scripts/gen_hdl_reference.py --selftest` | 2 | 0.11 |
| gen_hdl_reference-output | docs | `python3 -B scripts/gen_hdl_reference.py --output <work>/hdl-reference-c7ee5cbd4` | 2 | 0.36 |

Mode verdicts:
- **pins** (hosted `elaborate` step): `ALL GATES PASS EXCEPT 1 NOT RUN`.
  - The NOT RUN is gate 11, the historical Arty calibration report, as in every earlier bank.
  - The `--require-elaboration` verdict holds, and 96 `test_*:` arms ran. That is the lane's
    91 plus dev's five new entries (`test_commercial_timing_grade` and four shipping-image contract
    entries), or dev's 95 plus the lane's `test_clock_crossing_constraints`.
  - `test_commercial_timing_grade` is first and prints its three `[timing grade]` lines.
    `test_clock_crossing_constraints` prints the four `[constraints] shipping ... PASS` lines.
  - The RV32 compiler is the pins-home SDK.
- **builder-present**: `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11), 96 arms, 4 shipping PASS lines and
  3 `[timing grade]` lines.
- **builder-absent**: `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 11, plus the compiled CSR census, which
  is intentionally unavailable with the three RV32 compilers made absent. 96 arms, 4 shipping PASS
  lines and 3 `[timing grade]` lines.
- **hooks**: the committed #607 entry `sw/builder/test_clock_constraints.py` runs the shipping
  hook arm, scoped-exception, CRG and log-gate controls. In both environments it prints the four
  shipping PASS lines for 1x1 TDM8 and 8x8 on e1 and e2. #395's `test_timing_grade.py` prints its
  three lines in both environments: 19 wrong-condition refusals, the platform hooks and the PLL grade.
- **live**: the committed planted wrong-name control against the read-only shipping checkpoint. The
  vendor exit was 0, with 3 × 12-4739, 1 × 12-5201 and 1 × 20-1307 emitted, and the build gate
  REFUSED. The checkpoint is unchanged: 115,715,651 B, `5f7a442b6a9327ad5d41aa0b10e18c84d9ca4c0aacd573d2ad25d444f5b2f5d1`.

Not run, deliberately: `python3 scripts/act_ci.py --selftest` (the docs job's "Local act runner
contract gate"). AGENTS.md section 5 allows the candidate copy's `--selftest` only inside the
disposable CI job boundary, not on the host. The act replica belongs to a later stage.

## 5. Three-seed re-sweep (AX7101 1x1 TDM8, merge head `c7ee5cbd`)

**Result: every seed meets every bound at every #395 declared corner.** No timing failure.

Recipe: `run_sweep.py` (this packet). It is the round-1 recipe with only the head and output
directories changed:
- `sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml`, then
  `milan_soc.py` with the emitted shipping argv and `--entity-gen-dir`;
- `AreaOptimized_high` synthesis, `ExploreArea` optimization and the three canonical place
  directives;
- `--vivado-max-threads 16` and `PYTHONHASHSEED=0`, with each build and report process under
  `taskset -c 0-15`;
- sequential runs, fresh output directories, and the head, clean tree and `c951a9ff`
  gitlink/checkout asserted before each seed.

After each build, `report_seed.tcl` (byte-identical to round 1) opened the routed checkpoint
read-only and wrote per-corner Ethernet crossing and interaction reports. `collect_sweep.py` →
`sweep-summary.json` re-derives every figure below from the raw reports. For every seed and corner,
it asserts that the in-build #395 signoff report equals the read-only acceptance report.

Outputs are under `$VALIDATION_STORAGE/607-a427-work/build_ax7101_{asl,eto,eppo}_c7ee5cbd4`; the driver log is
`sweep-driver.log` there. The collector run was rc 0.

| Seed (directive) | Worst WNS ns | TNS ns | Worst WHS ns | THS ns | Worst Ethernet slack vs 8 ns | Build s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| asl (AltSpreadLogic_high) | +0.312 | 0.000 | +0.036 | 0.000 | +6.141 | 3562 |
| eto (ExtraTimingOpt) | +0.309 | 0.000 | +0.014 | 0.000 | +6.279 | 3401 |
| eppo (ExtraPostPlacementOpt) | +0.063 | 0.000 | +0.036 | 0.000 | +6.136 | 1737 |

The +0.030 ns rule holds for all three seeds. eppo has the least margin, +0.033 ns above the rule.

### 5.1 WNS, TNS, WHS and THS at every #395 corner

These come from the in-build `alinx_ax7101_signoff_<corner>_<Tj>C_timing.rpt` written by
`kl_timing_grade_reports`, and they are identical to the read-only acceptance reports. The
`negative` column counts `Slack (VIOLATED)` paths in `..._negative.rpt`. As #395 documents, Artix-7
Slow/Fast are fixed models, so 0 C and 85 C repeat each model.

| Seed | Model | Tj C | WNS ns | TNS ns | WHS ns | THS ns | Negative paths |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| asl | Slow | 0 | +0.312 | 0.000 | +0.072 | 0.000 | 0 |
| asl | Fast | 0 | +1.633 | 0.000 | +0.036 | 0.000 | 0 |
| asl | Slow | 85 | +0.312 | 0.000 | +0.072 | 0.000 | 0 |
| asl | Fast | 85 | +1.633 | 0.000 | +0.036 | 0.000 | 0 |
| eto | Slow | 0 | +0.309 | 0.000 | +0.102 | 0.000 | 0 |
| eto | Fast | 0 | +1.498 | 0.000 | +0.014 | 0.000 | 0 |
| eto | Slow | 85 | +0.309 | 0.000 | +0.102 | 0.000 | 0 |
| eto | Fast | 85 | +1.498 | 0.000 | +0.014 | 0.000 | 0 |
| eppo | Slow | 0 | +0.063 | 0.000 | +0.069 | 0.000 | 0 |
| eppo | Fast | 0 | +1.633 | 0.000 | +0.036 | 0.000 | 0 |
| eppo | Slow | 85 | +0.063 | 0.000 | +0.069 | 0.000 | 0 |
| eppo | Fast | 85 | +1.633 | 0.000 | +0.036 | 0.000 | 0 |

### 5.2 Ethernet crossing slack against the 8 ns bound (worst over the four corners)

| Seed | eth -> sys | sys -> eth | eth -> Milan | Milan -> eth | Requirement |
| --- | ---: | ---: | ---: | ---: | --- |
| asl | +6.141 | +6.644 | +6.465 | +6.591 | 8.000 ns datapath-only |
| eto | +6.279 | +6.719 | +6.583 | +6.591 | 8.000 ns datapath-only |
| eppo | +6.136 | +6.826 | +6.443 | +6.691 | 8.000 ns datapath-only |

`clkout0` is `sys` and `clkout1` is `milan`. All 16 rows per seed (`seed_crossings.tsv`) have
requirement 8.000 ns.

### 5.3 `report_clock_interaction` for the Ethernet pairs

Each seed has seven interaction reports: the combined read-only report, the four per-corner
read-only reports, the lane's in-build `alinx_ax7101_clock_interaction.rpt` and #395's
`alinx_ax7101_signoff_clock_interaction.rpt`. In every report, all four Ethernet pairs read
`Max Delay Datapath Only` at 8.00 ns, and no row naming `eth_clocks0_rx` is unsafe. The combined
rows:

`build_ax7101_asl_c7ee5cbd4/acceptance/seed_interaction.rpt`

```text
eth_clocks0_rx               milansoc_crg_clkout0         rise - rise     6.14     0.00            0           13             8.00                                           0           13                   Ignored              Max Delay Datapath Only
eth_clocks0_rx               milansoc_crg_clkout1         rise - rise     6.47     0.00            0           50             8.00                                           0           50                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout0         eth_clocks0_rx               rise - rise     6.64     0.00            0           16             8.00                                           0           16                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout1         eth_clocks0_rx               rise - rise     6.59     0.00            0           14             8.00                                           0           14                   Ignored              Max Delay Datapath Only
```

`build_ax7101_eto_c7ee5cbd4/acceptance/seed_interaction.rpt`

```text
eth_clocks0_rx               milansoc_crg_clkout0         rise - rise     6.28     0.00            0           13             8.00                                           0           13                   Ignored              Max Delay Datapath Only
eth_clocks0_rx               milansoc_crg_clkout1         rise - rise     6.58     0.00            0           50             8.00                                           0           50                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout0         eth_clocks0_rx               rise - rise     6.72     0.00            0           16             8.00                                           0           16                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout1         eth_clocks0_rx               rise - rise     6.59     0.00            0           14             8.00                                           0           14                   Ignored              Max Delay Datapath Only
```

`build_ax7101_eppo_c7ee5cbd4/acceptance/seed_interaction.rpt`

```text
eth_clocks0_rx               milansoc_crg_clkout0         rise - rise     6.14     0.00            0           13             8.00                                           0           13                   Ignored              Max Delay Datapath Only
eth_clocks0_rx               milansoc_crg_clkout1         rise - rise     6.44     0.00            0           50             8.00                                           0           50                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout0         eth_clocks0_rx               rise - rise     6.83     0.00            0           16             8.00                                           0           16                   Ignored              Max Delay Datapath Only
milansoc_crg_clkout1         eth_clocks0_rx               rise - rise     6.69     0.00            0           14             8.00                                           0           14                   Ignored              Max Delay Datapath Only
```

The fifth `eth_clocks0_rx` row in each report is the intra-clock `eth_clocks0_rx -> eth_clocks0_rx`,
`Clean` / `Partial False Path`. It is not a crossing, and round 1 shows the same classification.

### 5.4 Implementation-log warning census (emitted lines only)

| Seed | WARNING | CRITICAL WARNING | ERROR | 12-4739 | 20-1307 | 12-5201 | Quasi-static |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| asl | 884 | 0 | 0 | 0 | 0 | 0 | `cells=112 setup=4 hold=3` |
| eto | 884 | 0 | 0 | 0 | 0 | 0 | `cells=112 setup=4 hold=3` |
| eppo | 884 | 0 | 0 | 0 | 0 | 0 | `cells=112 setup=4 hold=3` |

The round-1 census at `350af5dc` read 877-878 WARNING and 0 CRITICAL WARNING. That is a reference
only, not an identity comparison.

### 5.5 Artifact identities (sizes and SHA-256 in `sweep-artifacts.json`, 174 files)

| Seed | Routed checkpoint | Bitstream | Tcl | XDC | vivado.log |
| --- | --- | --- | --- | --- | --- |
| asl | 107601402 B `f3509ea37a7b52f5…` | 3825992 B `855f263339da7dfc…` | 29692 B `5ee502520b8a17b5…` | 19504 B `81bbf89c34dd0e91…` | 698546 B `cecd888cd9e6edfd…` |
| eto | 107816853 B `64bbe506bc427dba…` | 3825992 B `b31e1efa638e5310…` | 29687 B `b8796af38e05e74b…` | 19504 B `81bbf89c34dd0e91…` | 610101 B `bfb707410c12bab2…` |
| eppo | 107093925 B `09d0124178f769a4…` | 3825992 B `06d82705c6320212…` | 29695 B `fc0866a61e5c97c5…` | 19504 B `81bbf89c34dd0e91…` | 686471 B `b51677d11a2bb08b…` |

No checkpoint, bitstream or log was copied into this packet.

## 6. Stale-statement commit: none made

The assignment allows one separate commit for stale statements. I found none, so the merge commit is
the head. Checked in the merged tree:
- **Docs both lanes touched:**
  - `docs/integration/BUILDING.md` section 5 (the resolved block);
  - the auto-merged `docs/testing/RUNNING_TESTS.md` section 5, where #395's grade text is followed
    by #607's test text;
  - the auto-merged `docs/litex/LITEX_SOC.md`, with #607's bound in 2.1 and #395's grade at the end.

  The #607 lines repeat the #395 margin rule ("WNS >= +0.03 ns and WHS >= 0 at every corner") and
  do not contradict the #395 text around them ("every declared corner"). Repetition is not
  staleness, so I left it.
- **#395 statements about constraints:**
  - "An absent or rejected constraint limits the signoff claim" concerns saved checkpoints, and it
    still holds for them.
  - `docs/findings/COMMERCIAL_TIMING_395.md` and its index row describe the `9e9954e9` checkpoint
    and name #607 as the owner of the fix. That is still true, and a findings record is dated
    evidence.
  - `docs/design/SAVED_STATE_*` say to use "#607's corrected constraints" for future evidence. The
    merge makes that possible and does not falsify it.
- **The lane's `sw/litex/sweep.sh` header:** "grep -A6 "Design Timing Summary"
  build_*_<tag>/gateware/vivado.log". Each merged build's log still has exactly one summary, and it
  equals the worst of #395's four corner reports (asl: `0.312 / 0.036`). The advice still holds.
- **The lane's platform comment:** "Keep all hook configuration below this". With #395's hooks it is
  more relevant, and it is honoured by the resolution.
- **`docs/litex/CLOCK_DOMAINS.md`:** the lane's "Inspect `milan_eth_constraints` between
  `synth_design` and `opt_design`" matches the emitted Tcl (section 3).

## 7. Result

- **Merge head: `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5`** ("Merge dev into 607-xdc-clock-names",
  one line, no body, no trailers).
- **Merge tree: `554756a545927a7e1aba734e2b7d8f4e90ba63cd`.**
- Parents: `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` and dev
  `7390b43627032c71c470e2aa8d0845eb5b740663`.
- `protocol-processor` gitlink and checkout: `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`, dev's pin.
  No lane pin changed.
- Conflicts were exactly the three permitted files, resolved per rule 1. No other file got a manual
  edit, and there is no stale-statement commit.
- Composition (rule 2) is proved:
  - in the three real builds (section 3);
  - by the shipping-hook and timing-grade tests;
  - by the pins-only bank.
- Re-sweep (rule 3): all three seeds meet WNS >= +0.030 ns and WHS >= 0 with TNS = THS = 0 at every
  #395 corner. The Ethernet pairs meet 8 ns with no unsafe pair. There are 0 critical warnings. No
  STOP condition occurred.
- Gates (rule 4): all rc 0 at the merge head. The Markdown gates ran in the pinned environment, and
  the diff/em-dash bases are the merge's dev parent. The two misrouted HDL-reference rows are
  recorded and superseded (section 4).
- The worktree is clean. Nothing was pushed.

Not done, by assignment: push, PR edit, rebase, force operation, merge to dev, act replica, hardware,
firmware or RTL edit. No existing issue or PR comment was edited or deleted. The delta review
([R382]) and the later candidate, composition review, act and merge stages are pending.

Packet contents (all small): `HANDOFF.md`, `PR-BODY.md`, `run_sweep.py`, `report_seed.tcl`,
`collect_sweep.py`, `run_gates.py`, `run_all_gates.sh`, `run_builder_absent.py`, `setup_pins_env.sh`,
`pins_env.sh`, `REVIEW-READY.md`, `review-ready-url.txt`, `sweep-results.json`, `sweep-summary.json`, `sweep-artifacts.json` and six
`gate-results-c7ee5cbd4-*.json` receipts. Logs, build trees, the pins-only environment and the
conflicted-file copies stay under `$VALIDATION_STORAGE/607-a427-work` and `$VALIDATION_STORAGE/607-a427`.

Publication:
- `[A427] TAKEN`: issue #607 comment 5874528754 (first session; not re-posted, as instructed).
- `[A427] STOP`: comment 5874531827 (first session).
- Manager disposition: comment 5874542826.
- **`[A427] REVIEW READY` for `c7ee5cbd`**: https://github.com/kebag-logic/milan-fpga/issues/607#issuecomment-5877640842
  (`REVIEW-READY.md` holds the text; `review-ready-url.txt` holds the URL).

## 8. History: the first session's STOP

Kept as written. The continuation above supersedes its status.

Status then: **STOPPED before the merge.** No merge commit, no file edit, no gate run,
no vendor run. The lane is unchanged at `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3`
with a clean worktree.

Assignment: issue #607 comment 5874480647 (merge-dev round, executor [A427]).

### Why STOP

The lane instructions require the `protocol-processor` gitlink to **stay
`16be6768` after the merge**. A faithful merge of dev `7390b436` cannot do that,
because dev itself moved the gitlink after this branch's base.

| Tree | `protocol-processor` gitlink |
| --- | --- |
| Merge base `54ce877371ee6e8878cf67294e86c2a8481b62f6` | `16be6768f710e79450aace277abacd6c2c3336e5` |
| Branch head `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` | `16be6768f710e79450aace277abacd6c2c3336e5` (unchanged by the lane) |
| Dev `7390b43627032c71c470e2aa8d0845eb5b740663` | `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` |
| `git merge-tree --write-tree HEAD origin/dev` result `b3ce3bf18723be43f94a7e04329d2dc76252d92b` | `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` |

- The only dev commit since the base that touches the gitlink is
  `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744`, "Adopt processor retry and LeaveAll
  fixes with parent regressions" (PR #613, issues #606/#608).
- `c951a9ff` is a descendant of `16be6768` (processor PRs #129 and #130).
  `git -C protocol-processor merge-base --is-ancestor 16be6768 c951a9ff` returns 0.
  The commit object is present in the lane's submodule store.
- The same dev commit records the new pin in parent files that merge in cleanly:
  - `docs/reference/SUBMODULES.md`, where the pin table now reads `c951a9ff`;
  - `syn/yosys/rom_digests.tsv`, which gains `c951a9ff` `ltn_rom.hex` and
    `ucode.hex` rows;
  - `tb/verilator/pp_shadow/*` parent regressions;
  - the submodule boundary diagram.

A merge that keeps `16be6768` would revert #613's pin inside the merge commit,
while leaving those dependent parent changes in place. That is a change beyond
the conflict resolution, and it would undo #613 on dev when #615 lands. I did not
do it.

The pin also decides the re-sweep inputs. The SoC build generates the ACMP ROM
and the AECP microcode from the processor tree, and it instantiates
`protocol_processor_top` (`sw/litex/milan_soc.py:946-967`). So the three-seed
AX7101 timing evidence depends on which pin the merge head carries. Running it
before the decision could waste the whole sweep.

### Checks done (read-only)

| Check | Result |
| --- | --- |
| `git remote get-url origin` | `https://github.com/kebag-logic/milan-fpga.git` |
| `git rev-parse HEAD` | `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` |
| `git fetch origin dev`; `git rev-parse origin/dev` | `7390b43627032c71c470e2aa8d0845eb5b740663` |
| `git -C protocol-processor rev-parse --show-toplevel` | `$LANES/607-xdc-clock-names/protocol-processor` (the submodule itself) |
| `git submodule status` | `protocol-processor` checked out at `16be6768`, clean |
| Merge base | `54ce877371ee6e8878cf67294e86c2a8481b62f6` |
| Conflict set (`git merge-tree --write-tree --name-only --messages HEAD origin/dev`) | exactly `docs/integration/BUILDING.md`, `sw/builder/test_builder.py`, `sw/litex/platforms/alinx_ax7101.py`. Auto-merged: `docs/litex/LITEX_SOC.md`, `docs/testing/RUNNING_TESTS.md`, `sw/litex/milan_soc.py`. |
| Merged-tree gitlinks | `protocol-processor` `c951a9ff`; `external` `efeb541a`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` unchanged |

So the conflict set matches the assignment. The gitlink precondition is the only
failure.

Merge-tree output, verbatim (exit status 1 = conflicts):

```text
b3ce3bf18723be43f94a7e04329d2dc76252d92b
docs/integration/BUILDING.md
sw/builder/test_builder.py
sw/litex/platforms/alinx_ax7101.py

Auto-merging docs/integration/BUILDING.md
CONFLICT (content): Merge conflict in docs/integration/BUILDING.md
Auto-merging docs/litex/LITEX_SOC.md
Auto-merging docs/testing/RUNNING_TESTS.md
Auto-merging sw/builder/test_builder.py
CONFLICT (content): Merge conflict in sw/builder/test_builder.py
Auto-merging sw/litex/milan_soc.py
Auto-merging sw/litex/platforms/alinx_ax7101.py
CONFLICT (content): Merge conflict in sw/litex/platforms/alinx_ax7101.py
```

### Decision needed

1. **Recommended: accept `c951a9ff` as the merge head's gitlink.** This is the
   natural merge result. Before any gate or the sweep, the lane's
   `protocol-processor` checkout moves to `c951a9ff`, so the gates and the
   bitstream use the pin the tree records. Then the round runs as assigned.
2. Keep `16be6768`. This needs the merge commit to revert #613's pin against its
   dependent parent changes. Not recommended.

### Not done

- No merge, resolution, stale-statement commit, gate, pins-only bank or vendor run.
- `PR-BODY.md` is unchanged, because there is no merge to describe.
- No push, PR edit, rebase, force operation, hardware, firmware or RTL action.
- No existing comment edited or deleted.

Issue #607 comments posted: `[A427] TAKEN` and `[A427] STOP`.

Posted: TAKEN https://github.com/kebag-logic/milan-fpga/issues/607#issuecomment-5874528754 ; STOP https://github.com/kebag-logic/milan-fpga/issues/607#issuecomment-5874531827
