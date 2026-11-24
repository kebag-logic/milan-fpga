# HANDOFF route: [A834] 8x8/1if split route, head dbba60e6 vs base aa30d77f

Status (05:00 CET 2026-11-24): **DONE.** Both sides routed, fit, and meet #818's floor on the first directive
(ExtraPostPlacementOpt). Directives 2 and 3 were not owed and were not run. Nothing of this lane is running.
ETA: none.

The merge condition: **met.** The head fits, and it meets the floor at every corner on its first directive. Its LUT
delta against the base is **-77** (the bound is +50).

## Results (post-route utilization, `baseline_utilization.rpt`; signoff corners from `*_signoff_<corner>_timing.rpt`)

| | Head `dbba60e6` | Base `aa30d77f` | Head - base |
|---|---:|---:|---:|
| Slice LUTs (of 63,400) | **43,068** (67.93 %) | **43,145** | **-77** |
| Slice Registers (FF) | **51,015** | **51,005** | **+10** |
| RAMB36 | 78 | 78 | 0 |
| RAMB18 | 33 | 33 | 0 |
| Block RAM tiles | 94.5 | 94.5 | 0 |
| DSP | 11 | 11 | 0 |
| Placed LUT / FF (`*_utilization_place.rpt`) | 43,068 / 51,015 | 43,143 / 51,005 | -75 / +10 |

| Corner | Head WNS / TNS | Head WHS / THS | Base WNS / TNS | Base WHS / THS |
|---|---|---|---|---|
| Slow_85C | +0.194 / 0.000 | +0.061 / 0.000 | +0.193 / 0.000 | +0.102 / 0.000 |
| Slow_0C | +0.194 / 0.000 | +0.061 / 0.000 | +0.193 / 0.000 | +0.102 / 0.000 |
| Fast_85C | +1.636 / 0.000 | +0.032 / 0.000 | +1.512 / 0.000 | +0.036 / 0.000 |
| Fast_0C | +1.636 / 0.000 | +0.032 / 0.000 | +1.512 / 0.000 | +0.036 / 0.000 |
| **Worst** | **+0.194** | **+0.032** | **+0.193** | **+0.036** |

Both sides have 0 failing setup and 0 failing hold endpoints. The #818 floor is WNS >= +0.030 ns and WHS >= 0 at every
signoff corner: **MET at both sides** (`signoff.py` rc 0). The stricter WHS >= +0.030 the train's tool also prints is
met too (head +0.032). Both routes are complete (0 nets with routing errors). The IOB pack check passes; its only
CRITICAL WARNING is `Place 30-722` on 8x8's documented parked `tdm_dout` (INERT). No ERROR.

**Where the delta sits** (`receipts/hier-delta.txt`). The RTL and the constraints are identical, so every difference
comes from the ROM contents and from synthesis and placement following them:
- The top cell, which holds the ROM banks: -14 LUT, +13 FF. The +13 FF is the OOC map's figure for 8x8/1if from
  round 1.
- `KL_mbx_dma`: -73 LUT.
- `milan_datapath` (own logic): -25 LUT.
- `KL_mbx_cdc` (own logic): +23 LUT.
- `KL_mbx_cdc/u_edit`: -13 LUT.
- The rest moves by 15 or fewer.

## Firmware the head image embeds (`receipts/head/fw-identity.txt`)

- Repo `dbba60e68a6e4a46f80e381c30ff823ee4ff7484`, lwSRP `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b`.
- The linked ELF (`ctrl_plat_image.py`, against the export's CSR map and flash map), sha256
  `a24015a42f2d1daad91466feca4ccb72c05c0eb4ab7a7f4a0ee2a3c678a6cbf0` (172,208 B). The copy the recipe's
  `--ctrl-firmware` names and the image manifest's `ctrl_firmware` record are the same sha256.
- `check_image_identity.py` passed: the ROM banks hold the ELF word for word.
- ROM 139,368 B in banks 131,072 + 8,192 + 2,048 (58.5-tile ledger), as round 1's ledger recorded.
- `mrp_mad.o` `.text` in the link map: 8,196 B at the head and 8,136 B at the base, so +60 B. This is the pin's +60 B.
- Base ELF `4c30879ff1a18aaa413f6c67f00aafb20e766bace1d2b59a8498a5c1391da0d5` (lwSRP `08ee86e8`).

| Image hashes (sha256) | Head | Base |
|---|---|---|
| ctrl_app.elf | `a24015a4…a6cbf0` | `4c30879f…1da0d5` |
| rom_bank0.init | `d2eb1705…ce0bd42` | `3fb2cda2…f345d536` |
| rom_bank1.init | `7e61a494…909a41a` | `bfdd21c8…8c17b42` |
| rom_bank2.init | `160edc60…2721fd` (234 B) | `fbe90e88…f484c556` (90 B) |
| routed checkpoint `alinx_ax7101_route.dcp` | `814c2945…88ea4cc` | `36918aa0…7473367d` |

Full hashes are in `receipts/<side>/fw-identity.txt` and `summary.txt`. **No bitstream exists.** The release flow's
measurement route (`pp_baseline.py`'s integrated script, the composed train's recipe) stops after routing, as
`PP_SHADOW_BASELINE_RECIPE.md` states ("The helper omits bitstream generation"). So the image hash is the ELF, ROM and
routed-checkpoint set above, and the manifest's `bitstream` field is null.

## Recipe (the composed train's 8x8 route, unchanged apart from paths)

From `train1117-a794/round5/receipts/fit/tools/` (the #810 route lane's recipe, which the train's #818 receipts used):
1. The split boot, `tb/verilator/ctrl_split_boot/run.py --shape endstation_ax7101_8x8`, for the stand-in image and
   runtime archives. PASS at both sides.
2. `route_image8.sh`:
   - `endstation_builder.py configs/endstation_ax7101_8x8.yaml --placement split`;
   - the builder's `soc_params.json` argv, plus `--synth-directive AreaOptimized_high --opt-directive ExploreArea
     --place-directive ExtraPostPlacementOpt --vivado-max-threads 32`;
   - the stand-in export, the flash map, the platform image link and the split export;
   - the identity gate;
   - `pp_baseline.py --placement full-split --single-thread-synthesis`.
3. `baseline_integrated.tcl` in `vivado-slot.sh` (head slot 2, 03:37:56 to 04:14:28; base slot 0, 04:14:27 to
   04:54:35, after waiting for a slot). Then `signoff.py`.

**On "first directive"**, two points:
- ExtraPostPlacementOpt is the first of `build.sh`'s `SWEEP_DIRECTIVES` and the train's integrated route.
- `build.sh`'s plain `cfg_ax8x8` names AltSpreadLogic_high, but the #818 gate and the train's route set use the
  three-directive sweep. Under the #818 rule, the first directive alone already settles the floor here.

## Notes

- **Foreground.** The tool's foreground commands are capped at 10 minutes. So each side ran detached (`setsid nohup`,
  as BUILDING.md section 3 requires for builds), and this session waited in the foreground on each step, in loops of
  about 9.5 minutes, until it finished. Vivado runs never exceeded 2 at once. Another lane (loopbram-a826) held the
  other slots, and the base queued behind it. MemAvailable stayed 52 GB or more at every check.
- **A process-kill slip, no effect.** One `pkill -f tools/summ.py` (stopping a hung report parser of my own) matched,
  and so ended, only its own shell. The base route was checked and was unaffected.
- **Housekeeping.** These remain:
  - the head worktree `/data-2/milan/tmp/lwsrppin-a834/route/repo-head` (detached `dbba60e6`, submodules from the
    lane's local copies; builder outputs make it dirty);
  - the base worktree (also dirty with builder outputs now);
  - about 0.9 GB of route scratch.

  To clear them, run `git worktree remove --force` on both and delete `/data-2/milan/tmp/lwsrppin-a834/route`. The
  disk was 96 % full (17 GB free) at the end.
- No commits, pushes, comments, bench or board access.

ROUTE DONE head 43068/51015 base 43145/51005 floor PASS
