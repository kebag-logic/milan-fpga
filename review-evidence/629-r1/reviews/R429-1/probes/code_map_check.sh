#!/bin/sh
# Review receipt generator (R429-1): print every path:line range the design page
# cites, at dev d4dd7426 (parent repo) and the processor pin b2db3a97, so a
# reader can check each cited fact. Usage: code_map_check.sh <milan-fpga checkout>
set -eu
cd "$1"
B=d4dd742679b902b2bc5eedf89d525066d59aafbb
PP=b2db3a970cedbbff2f8ba813acb96122c442bc58
show() { echo "=== $1:$2-$3"; git show "$B:$1" | sed -n "$2,$3p" | awk -v s="$2" '{printf "%d\t%s\n", s+NR-1, substr($0,1,240)}'; }
pshow() { echo "=== protocol-processor/$1:$2-$3 @${PP}"; git -C protocol-processor show "$PP:$1" | sed -n "$2,$3p" | awk -v s="$2" '{printf "%d\t%s\n", s+NR-1, substr($0,1,240)}'; }
show configs/endstation_ax7101_1x1_tdm8.yaml 128 128
show configs/endstation_ax7101_8x8.yaml 146 146
show configs/endstation_arty_8ch.yaml 132 132
show configs/endstation_arty_4x4.yaml 96 96
show configs/endstation_arty_current.yaml 166 166
show sw/builder/endstation_builder.py 134 141
show sw/builder/endstation_builder.py 2836 2853
show sw/builder/endstation_builder.py 3292 3301
show sw/builder/endstation_builder.py 3414 3419
show sw/builder/endstation_builder.py 3887 3902
show sw/builder/endstation_builder.py 3936 3971
show sw/builder/endstation_builder.py 4262 4267
show sw/builder/endstation_builder.py 5018 5045
echo "=== pre-#389 sw/builder/endstation_builder.py:4180-4203 @aea44c071^"
git show aea44c071^:sw/builder/endstation_builder.py | sed -n '4180,4203p'
show avdecc/aem_specs.py 22 35
show avdecc/aem_specs.py 234 241
show avdecc/aem_descriptors.py 428 482
show avdecc/aem_assemble.py 231 236
show avdecc/aem_emit.py 220 224
show configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh 54 55
pshow hdl/aecp/ucode/gen_ucode.py 1410 1440
pshow hdl/aecp/KL_aecp_nvm_writer.sv 86 90
pshow hdl/aecp/KL_aecp_dyn_state.sv 114 114
pshow hdl/aecp/KL_aecp_dyn_state.sv 352 352
pshow docs/architecture/07_memory_maps.md 135 135
pshow docs/architecture/07_memory_maps.md 343 343
pshow docs/architecture/07_memory_maps.md 479 479
pshow docs/00_MILAN_COMPLIANCE_REVIEW.md 377 377
pshow docs/00_MILAN_COMPLIANCE_REVIEW.md 420 420
D=hdl/milan/milan_datapath.sv
show $D 607 607
show $D 704 706
show $D 1554 1570
show $D 2576 2576
show $D 3108 3156
show $D 3180 3203
show $D 3469 3475
show $D 3492 3492
show $D 5418 5446
show $D 5508 5512
show $D 5537 5538
show $D 5576 5578
show $D 5608 5612
show $D 5713 5718
show $D 5733 5748
show $D 5756 5758
show $D 5858 5865
show $D 6079 6126
show $D 6153 6153
show $D 7529 7535
show hdl/ieee1722/crf/KL_crf_rx.sv 21 36
show hdl/ieee1722/crf/KL_crf_rx.sv 275 298
show hdl/ieee1722/crf/KL_crf_rx.sv 320 331
show hdl/ieee1722/crf/KL_crf_rx.sv 390 403
show hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 20 30
show hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 166 170
show hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 232 233
show hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 263 273
show hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 411 411
show hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 538 579
show hdl/ieee1722/crf/KL_mmcm_drp_servo.sv 609 615
show hdl/ieee1722/crf/KL_media_grid_align.sv 38 41
show hdl/ieee1722/crf/KL_media_grid_align.sv 95 100
show hdl/ieee1722/crf/KL_media_grid_align.sv 257 272
show hdl/ieee1722/crf/KL_crf_tx.sv 20 28
show hdl/ieee1722/avtp/KL_media_clock_restart.sv 211 264
show hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv 218 218
show hdl/ieee1722/aaf/KL_aaf_packetizer.sv 720 726
show hdl/common/csr/milan_csr.sv 396 396
show hdl/common/csr/milan_csr.sv 2562 2581
show docs/reference/FR_NFR.md 237 238
show docs/reference/REGISTER_MAP.md 1833 1833
show docs/design/TIME_SYNC.md 141 145
show docs/design/TIME_SYNC.md 198 198
