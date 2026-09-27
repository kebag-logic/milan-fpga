# Protocol processor baseline recipe

This recipe measures the two AX7101 product configurations.
It changes no RTL or processor checkout.
The [baseline](../findings/PP_SHADOW_BASELINE.md) records the measured revisions.

## Contents

- **[Prerequisites](#prerequisites)** -- Prepare the checkout and build environment.
- **[Export the shipping builds](#export-the-shipping-builds)** -- Derive commands and compile firmware.
- **[Integrated measurements](#integrated-measurements)** -- Route 1x1 and synthesize 8x8.
- **[Boundary-preserving attribution](#boundary-preserving-attribution)** -- Preserve ownership across synthesis optimization.
- **[Complete hierarchy rankings](#complete-hierarchy-rankings)** -- Include every reported direct child.
- **[Standalone measurements](#standalone-measurements)** -- Bind parameters from integrated elaboration.
- **[Yosys comparison](#yosys-comparison)** -- Map the same numeric geometry.
- **[Hierarchical mapping comparison](#hierarchical-mapping-comparison)** -- Locate the raw logic-count gap.
- **[Evidence checks](#evidence-checks)** -- Verify images and retain reports.

## Prerequisites

Use the [shipping build environment](../integration/BUILDING.md).
Initialize the three public submodules at their gitlinks.
Install the repository's required LiteX patch series.
Use Vivado 2026.1, sv2v, Yosys and the pinned SDK.
The [SDK installer](../../scripts/ci_rv32_sdk.py) verifies that compiler.

Set these shell variables to absolute paths:

```sh
export REPO="$PWD"
export WORK=/path/to/empty/external/build-directory
export LITEX_PYTHON=/path/to/litex/environment/bin/python3
export SDK=/path/to/verified/rv32/sdk
export PATH="/path/to/Vivado/2026.1/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c \
  'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
mkdir -p "$WORK/builder" "$WORK/roms"
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only
python3 syn/ooc/pp_baseline.py --selftest
```

Use a clean checkout with no existing `sw/builder/out/`.
Redirect its generated artifacts into the external work directory.
The symlink contains no build tree inside the checkout.

```sh
test ! -e sw/builder/out
ln -s "$WORK/builder" sw/builder/out
test ! -e configs/generated/ltn_rom.hex
test ! -e configs/generated/ucode.hex
ln -s "$WORK/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$WORK/roms/ucode.hex" configs/generated/ucode.hex
```

## Export the shipping builds

Run the launcher's preview for each named configuration.
Its preview regenerates the configuration's design arguments.
The 8x8 preview reports the tracked-header ownership mismatch.
Its explicit configuration include selects the correct measurement shape.
Keep the shipping header unchanged; this is measurement only.

```sh
bash sw/litex/build.sh ax7101 --dry-run > "$WORK/ax7101-dry-run.log"
bash sw/litex/build.sh ax8x8 --dry-run > "$WORK/ax8x8-dry-run.log"
```

Execute the printed commands in the foreground.
Change only the output directory and omit `--build`.
Firmware still compiles; vendor execution becomes a separate step.

```sh
python3 - <<'PY'
import json
import os
from pathlib import Path
import shlex
import subprocess

root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"])
python = os.environ["LITEX_PYTHON"]
for shape in ("ax7101", "ax8x8"):
    preview = (work / f"{shape}-dry-run.log").read_text()
    lines = [line for line in preview.splitlines()
             if "exec python3 milan_soc.py " in line]
    assert len(lines) == 1
    argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
    argv.remove("--build")
    argv[argv.index("--output-dir") + 1] = str(work / shape)
    (work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
    with (work / f"{shape}-elaboration.log").open("w") as log:
        subprocess.run([python, *argv], cwd=root / "sw/litex",
                       stdout=log, stderr=subprocess.STDOUT, check=True)
PY
```

Keep `--timing-opt`, `--floorplan` and every emitted design argument.
Keep `--vivado-max-threads 32`.
Never substitute an uninitialized firmware ROM.

## Integrated measurements

Prepare scripts from the generated shipping Tcl.
The helper retains sources, constraints and synthesis options.
It promotes missing-image diagnostics to errors.
The 1x1 endpoint follows the recipe through routing.
The 8x8 endpoint stops after synthesis.

```sh
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware"
python3 syn/ooc/pp_baseline.py "$WORK/ax8x8/gateware" --synthesis-only
(
  cd "$WORK/ax7101/gateware"
  vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log
)
(
  cd "$WORK/ax8x8/gateware"
  vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log
)
```

The helper omits bitstream generation after the measurement endpoint.
It retains the shipping IOB packing check before routing.
No hardware operation belongs to this recipe.

Repeat implementation with the repository's other two placement directives.
Reuse the same synthesis checkpoint for both comparisons.
Only the placement directive changes between these runs.
All placement runs use the default seed.

```sh
python3 - <<'PY'
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess

root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"])
gateware = work / "ax7101/gateware"
spec = importlib.util.spec_from_file_location(
    "baseline", root / "syn/ooc/pp_baseline.py")
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
source = (gateware / "alinx_ax7101.tcl").read_text()
_, tail = baseline.split_once(source, "# Add pre-optimize commands")
tail, _ = baseline.split_once(tail, "# Bitstream generation")
old = "place_design -directive ExtraPostPlacementOpt"
assert tail.count(old) == 1
for directive in ("AltSpreadLogic_high", "ExtraTimingOpt"):
    output = work / f"ax7101-{directive}"
    output.mkdir()
    shutil.copy2(gateware / "alinx_ax7101.xdc", output)
    script = "set_param general.maxThreads 32\n"
    script += f"open_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n"
    script += tail.replace(old, f"place_design -directive {directive}")
    script += baseline.REPORTS + baseline.PP_REPORTS
    script += baseline.SCOPE_TIMING + "\nquit\n"
    (output / "baseline_implementation.tcl").write_text(script)
    subprocess.run(["vivado", "-mode", "batch", "-source",
                    "baseline_implementation.tcl", "-nojournal",
                    "-log", "baseline.log"], cwd=output, check=True)
PY
```

## Boundary-preserving attribution

Keep the default run's whole-design totals as the baseline.
Repeat the export steps using a separate work directory.
Prepare that export with the additional attribution switch:

```sh
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware" --attribution-only
python3 syn/ooc/pp_baseline.py "$WORK/ax8x8/gateware" \
  --synthesis-only --attribution-only
```

Run the generated integrated scripts exactly as above.
The switch reads one additional constraint before synthesis:

```tcl
set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]
```

The wrapper boundary stays preserved during synthesis optimization.
Children retain the default rebuilt-hierarchy behavior.
Part, sources, parameters, images, directives and clocks remain identical.
Record attribution results separately from default-flow fit and timing.
A preserved boundary changes optimization opportunities and placement.
Its whole-design totals cannot replace the default measurement.

Use both public review probes on each attribution checkpoint.
The [review packet](https://github.com/kebag-logic/milan-fpga/tree/e21bc530eb89f7bd325f8d774aad5b5d95c70c1c/review-evidence/231-r1/reviews/R333-1/probe_boundary)
binds their exact source and default-run receipts.
Fetch those files into a temporary directory, then remove it.
Copy the required probes into the external measurement directory.

```sh
vivado -mode batch -source "$PROBES/boundary.tcl" -nojournal \
  -log "$WORK/boundary.log" -tclargs "$CHECKPOINT" "$WORK/boundary.tsv"
vivado -mode batch -source "$PROBES/loads.tcl" -nojournal \
  -log "$WORK/loads.log" -tclargs "$CHECKPOINT" \
  milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn "$WORK/loads.tsv"
```

Set `CHECKPOINT` to each synthesis checkpoint, then the 1x1 route.
Use distinct report filenames for every checkpoint.
The probes retain their original two-thread setting.
Their counts describe primitive cells, not combined Slice LUTs.
External loads include legitimate wrapper outputs.
Zero external loads are therefore not a required result.
Report the measured residual, including its named load stems.

## Complete hierarchy rankings

Every report disables the small-instance filter explicitly:

```tcl
report_utilization -hierarchical -hierarchical_depth 10 \
  -hierarchical_min_primitive_count 0 -file baseline_hierarchy.rpt
```

Reopen older checkpoints with this command before ranking them.
The default report silently omits small instances.
Generate separate LUT and FF ranks with the maintained parser:

```sh
python3 syn/ooc/pp_baseline_rank.py "$REPORT" --root "$ROOT" > "$RANKING"
```

Use `KL_pp_shadow` for the standalone report root.
Use `alinx_ax7101/milan_datapath/pp_shadow` for integrated reports.
The threshold is zero: every reported direct child appears.
The wrapper and processor each include their own logic.
Reconciliation rows retain the report's cross-child LUT-sharing adjustment.
Storage and DSP counts must sum exactly, without adjustments.

## Standalone measurements

Generate each standalone script from its integrated synthesis log.
Vivado's wrapper parameter block supplies the elaborated overrides.
Literal unreported defaults come from the wrapper declaration.
The script refuses ambiguous blocks and unsupported default expressions.

```sh
for shape in ax7101 ax8x8; do
  python3 syn/ooc/pp_baseline.py "$WORK/$shape/gateware" \
    --output "$WORK/$shape-ooc" \
    --integrated-log "$WORK/$shape/gateware/baseline.log"
  (
    cd "$WORK/$shape-ooc"
    vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log
  )
done
```

The source set and include order remain the integrated build's.
The synthesis directive remains `AreaOptimized_high`.
The standalone constraint is 10 ns, loaded before synthesis.
Only the top and out-of-context mode change.
Standalone ports remain unconstrained except for their clock.
These timing estimates cannot establish placed timing closure.

Product 1x1 includes two processor sinks and sources.
Product 8x8 includes nine processor sinks and sources.
CRF accounts for each additional sink and source.
The shipping 1x1 timer parameters still describe 50 MHz.
Its 100 MHz OOC constraint is a separate measurement target.

## Yosys comparison

Use the same complete numeric parameter set.
The existing Yosys recipe generates and verifies its ROMs.
Its ledger binds processor images to their gitlink revisions.

```sh
for shape in ax7101 ax8x8; do
  case "$shape" in
    ax7101) config=endstation_ax7101_1x1_tdm8 ;;
    ax8x8) config=endstation_ax7101_8x8 ;;
  esac
  export OOC_CHPARAM="$(cat "$WORK/$shape-ooc/baseline_chparam.txt")"
  export OOC_SHAPE="$REPO/configs/generated/$config"
  export OOC_TMP="$WORK/$shape-yosys"
  export YOSYS_MALLOC=none
  bash syn/yosys/ooc.sh KL_pp_shadow
done
```

The mapping is `synth_xilinx -family xc7 -flatten`.
Yosys reports no WNS and proves no placed fit.
Count distributed RAM through the recipe's `LUTRAM` column.
Compare `LUT_TOT`, not only its logic-LUT column.

## Hierarchical mapping comparison

Run each flattened mapping first, as described above.
Reuse its converted source, ROMs and complete numeric parameters.
Remove only `-flatten` from the mapping command:

```sh
python3 - <<'PYMAP'
import os
from pathlib import Path
import subprocess

work = Path(os.environ["WORK"])
for shape in ("ax7101", "ax8x8"):
    output = work / f"{shape}-yosys"
    values = (work / f"{shape}-ooc/baseline_chparam.txt").read_text().split()
    script = f"read_verilog {output}/KL_pp_shadow.ooc.v; "
    for item in values:
        key, value = item.split("=", 1)
        script += f"chparam -set {key} {value} KL_pp_shadow; "
    script += "synth_xilinx -family xc7 -top KL_pp_shadow; "
    script += "stat; write_json hierarchical.json\n"
    (output / "hierarchical.ys").write_text(script)
    with (output / "hierarchical.log").open("w") as log:
        subprocess.run(["yosys", "-s", "hierarchical.ys"], cwd=output,
                       stdout=log, stderr=subprocess.STDOUT, check=True)
PYMAP
for shape in ax7101 ax8x8; do
  python3 syn/ooc/pp_baseline_mapping.py \
    "$WORK/$shape-yosys/hierarchical.json" \
    "$WORK/$shape-yosys/KL_pp_shadow.ooc.json" \
    "$WORK/$shape-ooc/baseline_cells.tsv" > "$WORK/$shape-mapping.tsv"
done
```

The parser expands module instances with their measured multiplicity.
Library blackboxes count as primitives, despite retained simulation cells.
Each source scope contributes a disjoint raw logic-LUT count.
The final residual records flattened minus hierarchical optimization.
Those contributions sum to the original raw mapping gap.
No residual is assigned speculatively to an individual module.

## Evidence checks

The baseline also records integrated 1x1 synthesis before implementation.
Reopen its checkpoint for the same complete resource and timing reports.
This step changes no netlist.

```sh
python3 - <<'PYREPORT'
import importlib.util
import os
from pathlib import Path
import subprocess

root = Path(os.environ["REPO"])
work = Path(os.environ["WORK"])
spec = importlib.util.spec_from_file_location(
    "baseline", root / "syn/ooc/pp_baseline.py")
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
output = work / "ax7101-synth-reports"
output.mkdir(exist_ok=True)
checkpoint = work / "ax7101/gateware/alinx_ax7101_synth.dcp"
script = "set_param general.maxThreads 32\n"
script += f"open_checkpoint {{{checkpoint}}}\n"
script += baseline.REPORTS + baseline.PP_REPORTS + baseline.SCOPE_TIMING
(output / "reports.tcl").write_text(script + "\nquit\n")
subprocess.run(["vivado", "-mode", "batch", "-source", "reports.tcl",
                "-nojournal", "-log", "reports.log"], cwd=output, check=True)
PYREPORT
```

The same report commands can reopen any saved measurement checkpoint.
The recorded `ax8x8-synth-reports` and `ax7101-route-reports` use those reopens.
Their measurements agree with their original run's reports.

Retain each command's exit status without piping its output.
Require zero diagnostic occurrences of `Synth 8-4445`.
The echoed severity-setting command is not a diagnostic.
Rehash `baseline_images.json` inputs after each run.
The helper checks complete control-ROM and generated-ROM geometry.
Its self-test exercises real preparation on a synthetic export.
Run the maintained enforcement-removal mutants alongside the positive control:

```sh
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
```

The unmodified control must pass; every removal must fail.
Both commands also run in the fast CI workflow.
The report-accounting self-test runs alongside them.
The empty writable SRAM initialization is explicitly distinguished.

| Artifact | Location relative to each measurement directory |
|---|---|
| Executed recipe | `baseline_integrated.tcl` or `baseline_ooc.tcl` |
| Input bytes and hashes | `baseline_images.json` |
| Bound standalone parameters | `baseline_parameters.json`, `baseline_chparam.txt` |
| Hierarchical resource counts | `baseline_hierarchy.rpt` |
| Device resource counts | `baseline_utilization.rpt` |
| Exact primitive census, including carry | `baseline_cells.tsv` |
| Timing summary | `baseline_timing.rpt` |
| Integrated wrapper utilization | `baseline_pp_utilization.rpt` |
| Integrated wrapper boundary paths | `baseline_pp_boundary_timing.rpt` |
| Internal hierarchy timing | `baseline_scope_timing.tsv` |
| Integrated synthesis checkpoint | `alinx_ax7101_synth.dcp` |
| Integrated placed and routed checkpoints | `alinx_ax7101_place.dcp`, `alinx_ax7101_route.dcp` |
| Standalone synthesis checkpoint | `baseline_synth.dcp` |
| Yosys log and mapped netlist | `KL_pp_shadow.ooc.log`, `KL_pp_shadow.ooc.json` |

Scoped timing requires both endpoints inside the named instance.
It excludes crossings between sibling instances.
The wrapper row includes those internal cross-instance paths.
Read boundary paths and whole-design timing alongside scoped timing.

After measurement, remove the three temporary artifact symlinks.
Retain the external build directories for independent inspection.

```sh
test -L sw/builder/out
unlink sw/builder/out
unlink configs/generated/ltn_rom.hex
unlink configs/generated/ucode.hex
git diff --check
```
