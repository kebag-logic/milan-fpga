#!/bin/sh
# S3's split boot at both shapes and its self-test, then the reviewers' published probes and the pages' commands,
# on one clean clone; each step in sequence, because a boot's export writes the checkout's ignored outputs.
J="$MANAGEMENT/2026-09-23/665s4-a698h/scripts/job.sh"; C=$VALIDATION_STORAGE/scratch/665s4-a698h/wt-boot; S=$VALIDATION_STORAGE/scratch/665s4-a698h; R=$REVIEWS
RUN="python3 -B tb/verilator/ctrl_split_boot/run.py"
$J boot-1x1 $C $RUN --build-dir $S/boot-1x1
$J boot-8x8 $C $RUN --build-dir $S/boot-8x8 --shape endstation_ax7101_8x8
$J boot-selftest $C $RUN --build-dir $S/boot-selftest --self-test
$J placement-1x1 $C $RUN --build-dir $S/boot-1x1 --placement-controls
$J placement-8x8 $C $RUN --build-dir $S/boot-8x8 --shape endstation_ax7101_8x8 --placement-controls
$J nomap-probe $C bash $R/665s4-r738-4-packet/scripts/nomap_probe.sh $C $S/boot-1x1 $S/nomap-probe-out
$J page-plat $C python3 -I $MANAGEMENT/2026-09-23/665s4-a698h/scripts/page_probe.py $C sw/firmware/ctrl/plat/README.md $S/boot-1x1 $S/page-plat
$J map-8x8 $C python3 -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv $S/boot-8x8/split-soc/mapped/soc/csr.csv --csr-h $S/boot-8x8/split-soc/mapped/soc/software/include/generated/csr.h --out $S/map-8x8
$J page-design $C python3 -I $MANAGEMENT/2026-09-23/665s4-a698h/scripts/page_probe.py $C docs/design/SPLIT_CONTROL_MEMORY.md $S/boot-8x8 $S/page-design $S/map-8x8
$J refusal-probe $C python3 -B $R/665s4-r737-3-packet/scripts/refusal_probe.py $C $S/boot-1x1 $S/refusal-probe-out
$J nvm-capture $C python3 scripts/check_nvm_capture.py
$J py-idiom $C python3 scripts/check_py_idiom.py
$J image-selftest $C python3 -B sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
git -C $C status --porcelain --untracked-files=all --ignore-submodules=none > $S/wt-boot.status-after
