Resolve the variables below to absolute paths in the chosen checkout and environment. No host-specific location is part of the procedure.

- `SCRIPT_RUNNER`: the interpreter used for the repository checks.
- `BUILD`: the repository make-command executable.
- `AUDIO_TESTS`: the directory containing the audio `protocol_tb.sv`, `duplex.cpp`, and `check.py`.
- `SIM`: the RTL simulation executable.
- `SCRATCH`: a new output directory within the booked scratch allocation.
- `LEDGER`: the required cleanup log.
- `SHARED_CACHE`: the shared compiler cache directory.
- `RECEIPTS`: this receipt directory.

Set the shared cache and keep two compilation jobs. The default suite records its generated temporary removals before invoking each build:

```sh
"$SCRIPT_RUNNER" -B "$AUDIO_TESTS/check.py" --engine "$SIM" \
  --out "$SCRATCH/default" --jobs 2 --cleanup-ledger "$LEDGER"
```

The extended run uses the actual K=13 window. Before its build, record the exact generated temporary path in the ledger and flush the entry:

```sh
"$SCRIPT_RUNNER" -c 'import os,sys; f=open(sys.argv[1], "a"); f.write("Planned generated temporary removal: "+sys.argv[2]+"\n"); f.flush(); os.fsync(f.fileno()); f.close()' \
  "$LEDGER" "$SCRATCH/duplex/VKL_usbaudio_bridge__ALL.${SIM##*/}_deplist.tmp"
"$BUILD" -C "$AUDIO_TESTS" duplex-build RTL_SIMULATOR="$SIM" \
  MDIR="$SCRATCH/duplex" WINDOW_LOG2=13 JOBS=2
"$SCRATCH/duplex/VKL_usbaudio_bridge" 1000000
```

Use new output directories for the full defect campaigns:

```sh
"$SCRIPT_RUNNER" -B "$AUDIO_TESTS/mutations.py" --engine "$SIM" \
  --out "$SCRATCH/protocol-defects" --jobs 2 --cleanup-ledger "$LEDGER" \
  --temporary-file "Vprotocol_tb__ALL.${SIM##*/}_deplist.tmp" --discard-builds
"$SCRIPT_RUNNER" -B "$AUDIO_TESTS/transport_mutations.py" --engine "$SIM" \
  --out "$SCRATCH/transport-defects" --jobs 2 --cleanup-ledger "$LEDGER" \
  --temporary-suffix "__ALL.${SIM##*/}_deplist.tmp" --discard-builds
```

For image comparisons, fix the generation hash seed to zero on both sides. Use the identical shipping configuration and identical initialized memories. Compare firmware images directly. Before normalizing a memory-file reference in generated top-level logic, require both referenced files to be byte-identical. Preserve the unchanged baseline source checkout and the candidate source checkout separately.

Compare the entire programming-data field, including every configuration word. Container metadata is recorded separately. The extraction helper was independently checked against the baseline Arty flash output, which matched exactly:

```sh
"$SCRIPT_RUNNER" -B "$RECEIPTS/helpers/compare_images.py" \
  "$BEFORE_IMAGE" "$AFTER_IMAGE" --out "$SCRATCH/image-comparison"
```

A nonzero result is a failed identity check. Equal resource counts or matching generated top-level logic do not replace it. Physical builds use the required shared slot wrapper at the lowest priority, with the generated configuration's full route and corner-report commands. Actual audio placement must pass its separate 55-register assertion before routing.

For the accepted Arty image, generate `endstation_arty_usbaudio.yaml` through `endstation_builder.py`. Use its emitted `soc_params.json` argument list with `usbaudio_build.py`, adding `--usb-audio`. The ordinary audio-disabled invocation is the resource baseline. Keep the generated entity header specific to this profile; do not overwrite the shared default header.

Use the existing split-firmware construction procedure: export a seed register/flash map, link the selected control image against those maps, export the final image with that firmware, and require the CSR records excluding comment lines to remain byte-identical, and require the flash-map objects excluding their `source` metadata to remain equal after linking; preserve both raw file hashes. The audio and baseline each need their own pairing. Their accepted firmware and map hashes are in `r2-control-images.json`.

The accepted physical recipe is default synthesis, Explore optimization, ExtraTimingOpt placement, AggressiveExplore post-placement optimization, AggressiveExplore routing and AggressiveExplore post-route optimization. Generation hash seed is zero and each physical job uses two threads. No incremental reference, clock reduction or timing-exception relaxation was used. The 100 MHz control clock and 50 MHz media/bus clocks remain fixed.

After omitting its two leading explanatory comment lines, the executable body of portable `helpers/implement_audio.tcl` expands byte-for-byte to the executed physical script when its path arguments are supplied. Start from the current-source synthesis checkpoint whose digest is in `r2-arty-routes.json`. Resolve these input variables to the repository files: `CLOCK_RULES` = clock_constraints.tcl, `BOUNDARY_TIMING` = usbaudio_timing.xdc, `FIFO_RULES` = the pinned axis_async_fifo.tcl, `BRIDGE_CROSSINGS` = usbaudio_cdc.tcl, `CORNER_RULES` = timing_grade.tcl, `AUDIO_PAD_RULES` = usbaudio_pack.tcl, and `BOARD_PAD_RULES` = iob_pack_check.tcl. Run in a new output directory with the required shared slot wrapper and lowest priority:

```sh
"$LOW_PRIORITY_RUNNER" -n19 "$SLOT_WRAPPER" "$PHYSICAL_RUNNER" -mode batch \
  -source "$RECEIPTS/helpers/implement_audio.tcl" -tclargs \
  "$CURRENT_SYNTHESIS_CHECKPOINT" Explore ExtraTimingOpt \
  "$CLOCK_RULES" "$BOUNDARY_TIMING" "$FIFO_RULES" "$BRIDGE_CROSSINGS" \
  "$CORNER_RULES" "$AUDIO_PAD_RULES" "$BOARD_PAD_RULES"
```

A process exit alone is not timing acceptance. Require zero failing endpoints and nonnegative setup, hold and pulse slack in all four corner reports; inspect the direct skew and flag-pair reports, actual 55-pad placement, route status and design-rule results. Compare resource counts against the matched baseline. Preserve the final checkpoint and both image formats. The complete programming data extracted from the selected container equals its flash output byte for byte.
