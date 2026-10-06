[A531]

# Stage 2e baseline reproduction

The base is dev `fa450d301805881ad713b67521477bf042ddadfd`, without the
lane's logic. The comparison initially used the completed stage-2d candidate
measurement at `b2c81239f686592b224510c9d4f196a6c7aa7f25`, also applicable
to the comment-only `e80dd7ad43574b109b51d4f586efad776d547553`.
Dev then advanced. The required merge produced
`f325c3ab4a9faa0e2b7784e796728ebe6acf3fd3` with an updated processor pin.
A subsequent required documentation-only merge produces
`4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`; the 132 export inputs and
all OOC source bytes are unchanged. Fresh current-head implementation and
acceptance are complete; their recipes and receipts are under `merged/`. The
current ExtraTimingOpt grade remains failed (-0.209 ns WNS), while the required
baseline fails its margin on AltSpreadLogic_high (+0.026 ns WNS). Both failures
remain visible under the stage-2e readiness disposition. The original candidate
receipts below are historical and do not establish timing at the merged head.

Set STAGE_ROOT to an empty external scratch directory, EVIDENCE to this
evidence directory, and dependency locations to the installed tools.
Do not use the lane checkout as the base worktree.

```sh
git worktree add --detach "$STAGE_ROOT/base" fa450d301805881ad713b67521477bf042ddadfd
git -C "$STAGE_ROOT/base" submodule update --init --recursive
export REPO="$STAGE_ROOT/base"
export LITEX_PYTHON=/path/to/litex/environment/bin/python3
export SDK=/path/to/verified/rv32/sdk
export VIVADO_EXE=/path/to/Vivado/2026.1/bin/vivado
export PATH="$SDK/bin:$(dirname "$LITEX_PYTHON"):$(dirname "$VIVADO_EXE"):$PATH"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 MAKEFLAGS=-j16
python3 -B "$EVIDENCE/prepare.py"
python3 -B "$EVIDENCE/run_routes.py"
```

The preparation verifies each submodule's top-level directory before any
further Git command inside it. It verifies the SDK, runs the baseline helper's
self-test, regenerates the shipping arguments, builds initialized firmware,
exports the shipping 1x1 design and prepares the integrated recipe. Generated
images use temporary symlinks in the scratch worktree only, pointing outside it.
Keep those links until implementation and source hashing finish, then remove
the three links: `sw/builder/out`, `configs/generated/ltn_rom.hex` and
`configs/generated/ucode.hex`.

The route driver applies the repository recipe unchanged: part xc7a100t-fgg484-2,
AreaOptimized_high synthesis, ExploreArea optimization, the specified placement
directive, AggressiveExplore physical optimization and routing, 32 threads and
default seed. The alternates reuse the freshly synthesized baseline checkpoint.
Only the placement directive changes. Every implementation invocation holds
`$VIVADO_LOCK`, and the three invocations are sequential. There is no
bitstream generation. Do not overlap another heavy build with these runs.

For this session the long driver ran in the background with a separate driver
log, per-directive log and per-directive return-code file. All monitoring waits
were foreground commands shorter than ten minutes. No result is inferred from
launching the driver: each `.rc`, report and completed log is checked.

After all three runs complete:

```sh
"$LITEX_PYTHON" -B "$EVIDENCE/collect_timing.py" --work "$STAGE_ROOT" \
  --evidence "$EVIDENCE" --directive ExtraPostPlacementOpt
"$LITEX_PYTHON" -B "$EVIDENCE/collect_timing.py" --work "$STAGE_ROOT" \
  --evidence "$EVIDENCE" --directive AltSpreadLogic_high
"$LITEX_PYTHON" -B "$EVIDENCE/collect_timing.py" --work "$STAGE_ROOT" \
  --evidence "$EVIDENCE" --directive ExtraTimingOpt
```

Each collector grades WNS >= +0.030 ns and WHS >= 0. A margin failure returns
1 even when implementation returned 0. Preserve that failure; the stage-2e
ruling determines whether a baseline failure permits review readiness. It does
not change the timing threshold or turn the grade into a pass. The collector
also runs the build's implementation-log constraint check and records critical
warnings. Slow and Fast timing models each have reports at 0 and 85 C power
conditions; these temperature settings do not create four independent PVT models.

`source-comparison.json` binds 134 measured inputs to their prior candidate
receipts and records base/candidate differences after path normalization.
Only the two changed RTL modules differ functionally; the generated top differs
in comments and build paths, as separately checked in
`generated-top-comparison.json`. `shipping-arguments.json` records the matching
design arguments. Raw large logs and checkpoints remain outside this directory;
their sizes and SHA-256 hashes are in the per-directive artifact receipts.

For the comment edit, `pre-edit-search.json` records the exact old-line search
over tracked patch files and mutation tables. Reproduce all affected arm planting
against the candidate (this does not execute a simulation):

```sh
export REPO=/path/to/645-ring-slip
python3 -B "$EVIDENCE/plant_check.py"
```

The five follow-ring and twenty capture-coherence arms must all plant. The unchanged standalone follow-ring inputs are established by
`merged/follow-ring-source-identity.json`. Full-system simulation is rerun at
the merged processor pin. The exact premerge source checks are in
`source/commands.json`; current checks are under `merged/`. The author
correction is comment-only, while the required dev merge changes executable
inputs and therefore invalidates the former full-system evidence.
