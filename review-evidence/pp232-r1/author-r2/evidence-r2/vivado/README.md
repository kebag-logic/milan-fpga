# #232 area lane: Vivado evidence (round 2, item 2; R453-1 F1)

Report extracts and whole small reports from the eight Vivado runs the lane's figures
come from. The raw run directories (logs, full timing reports, checkpoints, cell lists)
stay in the lane's scratch area; each extract's `sources.tsv` gives the full sha256 and
size of every raw file it was cut from, and `../MANIFEST.sha256` the sha256 of every
file published here.

- Recipe and tools: milan-fpga PR #638 at `79e53831` (`syn/ooc/pp_baseline.py`,
  `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`), unchanged in dev `241f9184`.
- Vivado 2026.1 build 6511674, `xc7a100t-fgg484-2`, 50 MHz (20 ns),
  AreaOptimized_high / ExploreArea / ExtraPostPlacementOpt / AggressiveExplore,
  32 threads, default seed.
- The round-2 head `2ea3dee2` changes no HDL logic since `6e950fea`: its two HDL
  changes (`KL_aecp_notify.sv`'s index comment and `main`'s `KL_adp_engine.sv`
  comments, PR #152) are comment-only, and the two files are equal with comments
  stripped. So `r1b-head-6e950fea-route-1x1` is the route for the round-2 head.

## Runs

| Directory | Processor | Parent | Run | rc | Start, end (CEST) | `baseline.log` bytes | `baseline.log` sha256 |
|---|---|---|---|---:|---|---:|---|
| `r1-base-f4167536-route-1x1` | `f4167536` (round 1 base) | dev `bbf704ec` + c8 + p2-p1 | integrated route `endstation_ax7101_1x1_tdm8` | 0 | 10-03 18:46, 19:24 | 607592 | `91c14839314a6d5ae8763c6f17ce8de36601d8df192ea415aa5c7640464ddb1a` |
| `r1-head-3ab2e4da-route-1x1` | `3ab2e4da` (round 1 head) | the same | integrated route | 0 | 10-03 19:51, 20:26 | 888632 | `c951b7a679df3c23abb521975c0c81fc0115697554738131b789ef099baf7351` |
| `r1b-main-5c71928a-route-1x1` | `main` `5c71928a` | dev `5fabb46e` + c8 + p2-p1 + c10 | integrated route | 0 | 10-04 03:55, 05:30 | 687698 | `3345c0ac81f8f149bc76f4b62e037bc7134ca2e2a9e2435cc602846ab9679073` |
| `r1b-head-6e950fea-route-1x1` | `6e950fea` (round 1b head) | the same | integrated route | 0 | 10-04 03:09, 03:37 | 806747 | `4d18c2905ff3e81236bf446f76477ed8ef4856f52ff4605fde96626e3eca3f37` |
| `r1-base-f4167536-ooc-1x1` | `f4167536` | dev `bbf704ec` + c8 + p2-p1 | standalone `KL_pp_shadow` synthesis, 1x1 | 0 | 10-03 19:24, 19:42 | 245625 | `46897cb6e929dce0f6a42d167e55fb00d80c4ac9f6a4d688068fe95a78ea9f42` |
| `r1-head-3ab2e4da-ooc-1x1` | `3ab2e4da` | the same | standalone synthesis, 1x1 | 0 | 10-03 20:26, 20:45 | 314436 | `ab9e117f1d659197d9a2eb5b626045530c81d628108a0ead677bde9856d16f78` |
| `r1-base-f4167536-ooc-8x8` | `f4167536` | the same | standalone synthesis, 8x8 | 0 | 10-03 19:25, 19:51 | 247475 | `db02bbc29a04e0906a0872a3c001bbcb61acea71fe9b8ead8fc639ad6d36a8c1` |
| `r1-head-3ab2e4da-ooc-8x8` | `3ab2e4da` | the same | standalone synthesis, 8x8 | 0 | 10-03 20:46, 21:09 | 315641 | `1908735e4c6b333e2dc50dbf9a66e37f2425f0985270cf0ad318fc9d8adcf1f4` |

The first 16 hex digits of each digest are the ones HANDOFF section 11 and R1b.9
published. "Round 1 standalone figures stand" (R1b.6) refers to the four `ooc` runs.

## Files in each directory

| File | Whole or extract | Source |
|---|---|---|
| `baseline_utilization.rpt` | whole | #638's `report_utilization` after the route (route) or synthesis (ooc): the whole-image figures |
| `baseline_hierarchy.rpt` | whole | #638's `report_utilization -hierarchical ... -hierarchical_min_primitive_count 0`: `u_notify`, `u_aecp/u_resp`, `u_aecp/u_d3` |
| `baseline_pp_utilization.rpt`, `baseline_scope_timing.tsv`, `baseline_images.json` | whole | #638's `KL_pp_shadow` scope report, per-scope internal slack, the six memory images' hashes |
| `alinx_ax7101_utilization_place.rpt`, `alinx_ax7101_utilization_hierarchical_place.rpt` | whole (route) | the LiteX flow's post-placement reports, for context; the figures come from #638's reports above |
| `alinx_ax7101_route_status.rpt` | whole (route) | `report_route_status` |
| `alinx_ax7101_signoff_grade.txt`, `alinx_ax7101_signoff_<corner>_negative.rpt` | whole (route) | the signoff corners and their (empty) negative-slack path lists |
| `timing-extract.txt` | extract | the "Design Timing Summary" of #638's `baseline_timing.rpt`, of the flow's `alinx_ax7101_timing.rpt` and of the four signoff corners (route); the "Intra Clock Table"; the worst setup and the worst hold path (the least slack over every clock group) |
| `log-extract.txt` | extract | `baseline.log`: tool identity lines; "Block RAM: Final Mapping Report" and "Distributed RAM: Final Mapping Report"; every `Synth 8-7186`, `8-4445` and `8-6901` line with its count; completion lines |
| `census.tsv` | derived | primitive counts from `baseline_cells.tsv` (every primitive cell and its type) for `u_notify`, `u_aecp/u_resp`, `u_aecp/u_d3` and four `u_notify` arrays; macro cells (`RAM32M`, `RAM64X1D`, `RAM32X1D`) and their leaf cells (`RAMD32`, `RAMS32`, `RAMD64E`) are both listed |
| `figures.json` | whole | the figures `pp_baseline.py` read from the run (round 1's file holds route, 1x1 and 8x8) |
| `sources.tsv` | | bytes and full sha256 of every raw file read |

`tools/vivado_extract.py` cut the extracts; `tools/rederive.py` re-derives every quoted
figure from this directory alone, and `rederive.txt` is its output
(`python3 tools/rederive.py`, rc 0).

## What a cold reviewer can re-derive (R453-1 F1 "Verification")

From `rederive.txt` (each figure read from the files above):

| Figure | Value | Where |
|---|---|---|
| Route at the round-1b merge, head - `main` | LUT 50,671 - 51,434 = **-763** (logic -1,625, memory +862); FF 57,660 - 59,691 = **-2,031**; slices -6; CARRY4 -150 | `baseline_utilization.rpt` of the two `r1b-*-route-1x1` directories |
| `u_notify`, head - `main` | LUT 2,343 - 3,270 = **-927**; LUTRAM 960 - 96; FF 1,287 - 3,299 = **-2,012** | `baseline_hierarchy.rpt:212` of each |
| `u_aecp/u_resp` | 345 LUT / 260 FF at both; 260 FF in all eight runs | `baseline_hierarchy.rpt:196` (route), `:41` (ooc 1x1) |
| `u_aecp/u_d3` | 1,897 -> 1,931 LUT, 581 FF at both | `baseline_hierarchy.rpt:194` |
| WNS / WHS, head | **+0.274** / +0.023 ns (`main` +0.079 / +0.014) | `timing-extract.txt` first block (`baseline_timing.rpt:135-147`) |
| Signoff corners, head | Slow 0 C and 85 C +0.274 / +0.050; Fast 0 C and 85 C +1.550 / +0.023; no negative-slack path at any corner | `timing-extract.txt` blocks 3 to 6; `*_negative.rpt` ("No timing paths found") |
| Worst setup path, head | `u_aecp/u_ucpu/uop_e_r_reg[imm][3]` -> `u_aecp/u_d3/deb_cnt_r_reg[1]/R`, 33 levels (CARRY4 13), slack 0.274 | `timing-extract.txt`, the "Max Delay Paths" block |
| Route status | head 104,326 of 104,326 routable nets fully routed, `main` 107,053 of 107,053; 0 with errors | `alinx_ax7101_route_status.rpt` |
| `rows_r` mapping, head | `\|u_notify \| rows_r_reg \| User Attribute \| 16 x 128 \| RAM32M x 64 \|` | `r1b-head-6e950fea-route-1x1/log-extract.txt:80` |
| Identity index, synthesis mapping report | 288 rows `... g_ix_chunk[j].mem_r_reg \| User Attribute \| 64 x 1 \| RAM64M x 1 \|` (first at `:81`) and 16 rows `... g_ix_chunk[18].mem_r_reg \| ... \| 16 x 1 \| RAM16X1D x 1 \|` (`:99` to `:384`) | `r1b-head-6e950fea-route-1x1/log-extract.txt` |
| Identity index, implemented cells after optimization | 288 RAM64X1D (576 LUTs) and 16 RAM32X1D (32 LUTs); with `rows_r`'s 64 and `cmdq_*`'s 24 RAM32M (88 x 4 = 352 LUTs) they make `u_notify`'s 960 LUTRAM | `census.tsv` (`u_notify` RAM32M 88, RAM64X1D 288, RAM32X1D 16; `u_notify g_ix_row` RAM64X1D 288, RAM32X1D 16; `u_notify rows_r_reg` RAM32M 64) |
| `cmdq_*` | `cmdq_excl_r_reg \| Implied \| 16 x 64 \| RAM32M x 11`, the other five 3 or 1 each: 24 | `log-extract.txt:388` and the rows above it |
| `Synth 8-7186` | **0** in every head run; 16 in every base and `main` run (`rows_r[0]` to `rows_r[15]`) | `log-extract.txt`, "## Synth 8-7186" |
| `Synth 8-4445` | 0 in every run (one echoed `set_msg_config` line) | `log-extract.txt`, "## Synth 8-4445" |
| `rows_r_reg` flip-flops | 2,048 FD cells at base and `main`, 0 at every head | `census.tsv`, `u_notify rows_r_reg` |
| `ctr_last_r_reg` flip-flops | 192 (1x1) and 640 (8x8) at base and head (lever 5 ruled (c)) | `census.tsv` |
| Round 1 route, head - base | LUT -650, FF -1,950, slices -15, WNS +0.116 -> +0.143 | `r1-*-route-1x1` |
| Standalone, head - base | 1x1 LUT -894, FF -2,042; 8x8 LUT -925, FF -2,175; `u_notify` 1x1 -933 / -2,046, 8x8 -450 / -2,046 | `r1-*-ooc-*` |

The standalone timing figures (`timing-extract.txt` of the `ooc` directories) are
synthesis estimates without I/O constraints, as #638 states.
