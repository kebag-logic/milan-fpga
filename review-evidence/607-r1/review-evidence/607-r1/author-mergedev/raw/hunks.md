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
