[A531]

# Current-head evidence reproduction

Head: `4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`.
The required processor adoption was measured with pin
`ead8036035affd53ef4b29979190f2f4f67084c0`. The final dev merge changes only
`docs/findings/653_DISCONNECT_ORDER_BENCH.md`; executable inputs remain those
compiled at f325c3ab. `documentation-merge-binding.json` records that bridge.

Set REPO to the candidate root, STAGE_ROOT to empty external scratch, and
EVIDENCE to this directory. Installed dependencies and build products belong
outside EVIDENCE. Before further Git commands inside each submodule, verify
that `git -C <directory> rev-parse --show-toplevel` is that directory.

```sh
export REPO=/path/to/645-ring-slip
export STAGE_ROOT=/path/to/external/current-run
export EVIDENCE=/path/to/evidence/stage2e/merged
export LITEX_PYTHON=/path/to/shipping/environment/bin/python3
export SDK=/path/to/verified/rv32/sdk
export VIVADO_EXE=/path/to/Vivado/2026.1/bin/vivado
export PATH="$SDK/bin:$(dirname "$LITEX_PYTHON"):$(dirname "$VIVADO_EXE"):$PATH"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 MAKEFLAGS=-j16
mkdir -p "$STAGE_ROOT/tmp"
export TMPDIR="$STAGE_ROOT/tmp"
cp "$EVIDENCE/recipes/prepare.py" "$STAGE_ROOT/prepare.py"
cp "$EVIDENCE/recipes/run_routes.py" "$STAGE_ROOT/run_routes.py"
cp "$EVIDENCE/recipes/source_inventory.py" "$STAGE_ROOT/source_inventory.py"
cp "$EVIDENCE/recipes/collect_timing.py" "$STAGE_ROOT/collect_timing.py"
cd "$REPO"
python3 -B "$STAGE_ROOT/prepare.py"
python3 -B "$STAGE_ROOT/source_inventory.py"
python3 -B "$STAGE_ROOT/run_routes.py"
"$LITEX_PYTHON" -B "$STAGE_ROOT/collect_timing.py" --work "$STAGE_ROOT" --evidence "$EVIDENCE" --directive ExtraPostPlacementOpt
"$LITEX_PYTHON" -B "$STAGE_ROOT/collect_timing.py" --work "$STAGE_ROOT" --evidence "$EVIDENCE" --directive AltSpreadLogic_high
"$LITEX_PYTHON" -B "$STAGE_ROOT/collect_timing.py" --work "$STAGE_ROOT" --evidence "$EVIDENCE" --directive ExtraTimingOpt
python3 -B "$STAGE_ROOT/source_inventory.py" --verify
```

The three implementations are sequential under `$VIVADO_LOCK`.
They use the shipping 1x1 recipe, 32 threads and default seed; alternates reuse
the fresh synthesis checkpoint. A margin grade of 1 is retained as a failure.
Slow/Fast timing models are each reported at 0 and 85 C power settings; these
are two timing models, not four independent models. No bitstream is generated.
The complete requested fa450d30 baseline reproduction is one directory above.

Preparation deliberately refuses existing generated-image paths. In this run,
the builder left generated ROM files there; the first export attempt stopped,
those files were preserved in external scratch, and the unchanged export passed.
Keep the three preparation symlinks through implementation and input verification.
Then remove only links whose targets match this run: `sw/builder/out`,
`configs/generated/ltn_rom.hex` and `configs/generated/ucode.hex`.

## Functional and source checks

HANDOFF.md gives the standing commands and expected results.
`recipes/commands.json` records exact argv and working directories;
`recipes/run_jobs.py` records concurrent scheduling and the environment.
External broad, physical and focused test stages hold separate copies of the
369 tracked test files and separate generated images. Their source identity is
recorded in `test-source-identity.json`. These stages are not Git checkouts.
Use `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator` and make -j16.
Capture-coherence ran under a two-CPU affinity because its mutation driver
sizes concurrency from affinity and has no jobs flag; see
`recipes/capture-coherence-command.json` and `recipes/run_coherence.py`.

`source/commands.json` lists all 26 exact source/documentation commands.
The source launcher uses the parent stage2e EVIDENCE directory to locate its
historical command recipe; the measurement launcher uses this merged directory.
A wrong launcher directory stopped before any gate ran; its original log and
corrected launch are recorded separately. No gate was weakened.

In this run, implementation overlaps only existing-binary simulations.
`recipes/render-boundary-builds.json` proves all three boundary binaries were
built and the remaining driver path had no compilation. Full functional return
codes remain mandatory. A reproduction may simply wait for every functional
campaign before starting implementation. Never overlap a vendor invocation
with another heavy build. Each long job has its own log and return-code file;
monitor it with foreground waits shorter than ten minutes, and do not end the
session while jobs remain.

## Area

`recipes/AREA-SOURCES.py` extracts the complete capture module and the ordered
recentre blocks from Git, with the wrappers and constants needed for OOC.
Use the accompanying `area-ooc/ooc.tcl` from external scratch with ONLY set to
each of settle_base, settle_head, cmc_base and cmc_head, sequentially under the
shared lock. Part is xc7a100tfgg484-2; clock is 20 ns; capture shape is four pair
slots, eight TDM slots, one loopback stream and eight loopback channels.

```sh
cp "$EVIDENCE/recipes/AREA-SOURCES.py" "$STAGE_ROOT/AREA-SOURCES.py"
cp "$EVIDENCE/area-ooc/ooc.tcl" "$STAGE_ROOT/ooc.tcl"
cd "$REPO"
python3 -B "$STAGE_ROOT/AREA-SOURCES.py" "$STAGE_ROOT/area-ooc"
cd "$STAGE_ROOT/area-ooc"
for area_tag in settle_base settle_head cmc_base cmc_head
do
    ONLY="$area_tag" flock $VIVADO_LOCK "$VIVADO_EXE" -mode batch -source ooc.tcl -nojournal -log "$area_tag.vendor.log"
    area_rc=$?
    printf '%s\n' "$area_rc" > "$area_tag.rc"
    test "$area_rc" -eq 0 || exit "$area_rc"
done
```

The OOC base is dev 28f9666f. `area-base-source-identity.json` proves both module
sources are byte-identical to the requested routed fa450d30 baseline.
The fresh default routed checkpoint supplies current own-area attribution.
`area-route/ownership.tcl` and `shared-logic.tcl` query both routed checkpoints
under the lock; `prove_shared.py` proves unchanged shared band functions over
all 65,536 signed-error assignments and catches a planted table change.
`compare.py` records every counted/excluded cell and the resulting bound.
Exact arguments, ordering and the <=120 LUT / <=120 FF check are in
`recipes/run_measurements.py`. Its baseline checkpoint is the fresh fa450d30
run recorded one directory above; whole-design differences include the
processor adoption and are not attributed to this lane.

Artifact receipts record SHA-256 and byte size. Files above 200,000 bytes,
binaries, generated sources, checkpoints and build trees remain outside the
evidence directory. Retained text replaces home paths with neutral placeholders.
