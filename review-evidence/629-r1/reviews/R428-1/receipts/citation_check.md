# R428-1 citation check: docs/design/MEDIA_CLOCK_FOLLOWING.md at 78d4fef2

Every `path:line` the page cites, re-read at dev `d4dd7426` (identical to the
head for every non-documentation path: the head changes only
`docs/design/MEDIA_CLOCK_FOLLOWING.md` and `docs/README.md`). Processor paths
at the pinned submodule `b2db3a97`. OK = the lines say what the page says.

## Builder and entity model

| Citation | Result |
|---|---|
| `configs/endstation_ax7101_1x1_tdm8.yaml:128`, `_ax7101_8x8.yaml:146`, `_arty_8ch.yaml:132`, `_arty_4x4.yaml:96`, `_arty_current.yaml:166` | OK, `[internal, crf]` in all five; no other config declares the key |
| `sw/builder/endstation_builder.py:3887-3902` | OK, `input_stream` refused by name, only internal/crf admitted; cites Milan 7.2.2 at :3898 |
| `:3956-3971` | OK |
| `:5018-5045` | OK, INTERNAL at 0 located on itself, CRF on STREAM_INPUT `len(L)`; docstring :5019-5028 cites Milan 7.2.2 |
| `:4180-4203` at `aea44c071^` | OK, INTERNAL, one per listener, then CRF |
| `:3414-3419` | OK |
| `:3292-3301` | OK |
| `:4262-4267` | OK |
| `:2836-2853` | OK |
| `:134-140` | OK (CLOCK_SOURCE_NAMES at :141); the `names.clock_sources.stream` refusal the change also needs is `_load_names`, :3784-3790, not listed |
| `:3936-3955` (Limits) | rule starts at :3937; :3936 is the preceding check |
| `avdecc/aem_specs.py:22`, `:35`, `:234-241` | OK; :240 cites Milan 7.2.2 |
| `avdecc/aem_descriptors.py:428-442`, `:445-462`, `:464-482` | OK, identity list |
| `avdecc/aem_assemble.py:231-236` | OK |
| `avdecc/aem_emit.py:220-224` | OK |
| `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh:54-55` | resolved by the path gate |

## Protocol processor (b2db3a97)

| Citation | Result |
|---|---|
| `hdl/aecp/ucode/gen_ucode.py:1410-1419`, `:1433-1440` | OK: rationale comment, then count read, `CHECK_ARG` index < count, `WRITE_ST`, `NVM_MARK`; refusal tail carries the current index |
| `hdl/aecp/KL_aecp_nvm_writer.sv:86-90` | banner text stating the rule; the implementing compare is `:501-503` (`rval_r[15:0] < sb_rdata_i[47:32]`) |
| `hdl/aecp/KL_aecp_dyn_state.sv:114`, `:352` | OK, domain 0 only |
| `docs/architecture/07_memory_maps.md:135`, `:343`, `:479` | OK; :135 also credits "IEEE 7.4.23.1" with the membership test |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:377`, `:420` | OK |

## Fabric

| Citation | Result |
|---|---|
| `hdl/milan/milan_datapath.sv:607` | OK, stale ("cannot select CRF") |
| `:704`, `:7529-7535` | OK |
| `:1554-1570` | OK, one registered compare, 0xFFFF fold |
| `:3108-3156` | OK, CRF lock-fall and received-toggle triggers gated by `crf_clk_selected_r` |
| `:3180-3203`; `KL_media_clock_restart.sv:211-213`, `:230` | OK |
| `:3469-3475`, `:3492` | OK; :3473-3475 record LOCKED = ~tu as a single clock-validity authority |
| `:5418-5446` | OK |
| `:5508-5572` (`:5537-5538`) | OK |
| `:5576-5578` | OK, stale ("hardwires INTERNAL against NONE") |
| `:5594-5627`, `:5608-5612` | OK |
| `:5713-5718` | OK, INTERNAL free-run by recorded rule |
| `:5733-5748`, `:5740`, `:5748` | OK |
| `:5756-5758` | OK |
| `:5858-5865` | OK |
| `:6079-6126`, `:6091-6092`, `:6115` | OK |
| `:6153` | OK |
| `:2576`; `KL_avtp_rx_monitor_ctx.sv:218`; `milan_csr.sv:396` | OK, stream-0 snapshot |
| `KL_crf_rx.sv:21-33`, `:34-36`, `:275-277`, `:296-298`, `:320-331`, `:390-403` | OK; jump bound derived at :279-294 (2,048 ns, "Arrival/network jitter is absent here") |
| `KL_mmcm_drp_servo.sv:20-30`, `:27-30`, `:166-170`, `:232-233`, `:263-273`, `:411`, `:538-551`, `:571-579` | OK; PI and lock held while the remote rate is invalid (:611-615) |
| `KL_media_grid_align.sv:38-41`, `:95-100`, `:257-272` | OK |
| `KL_crf_tx.sv:20-28` | OK |
| `KL_aaf_packetizer.sv:720-726` | OK |

## Documentation

| Citation | Result |
|---|---|
| `docs/reference/FR_NFR.md:155`, `:237`, `:238` | OK |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89` | OK, quote present; the row also cites "IEEE 7.4.23.1" for the range check |
| `docs/design/TIME_SYNC.md:141-145`, `:198` | OK |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:120`, `:175`, `:186`, `:187` | OK |
| `docs/ENDSTATION_BUILDER.md:990` | OK |
| `sw/builder/README-parameters.md:118-119` | OK |
| `docs/reference/REGISTER_MAP.md:1833` | OK |
| `docs/design/AREA_BUDGET.md` servo 814 LUT / 789 FF | quoted correctly; that record is shape-unknown, and `syn/yosys/ooc.sh KL_mmcm_drp_servo` at this head and the 1x1 TDM8 shape reports 871 LUT / 792 FF (receipt `ooc_KL_mmcm_drp_servo.log`) |

## Area basis

`OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8 syn/yosys/ooc.sh KL_crf_rx`
at this head: 433 LUT, 544 FF, 1 RAMB18, 147 CARRY4, rc 0 (receipt
`ooc_KL_crf_rx.log`). Reproduces the page's figures exactly.
