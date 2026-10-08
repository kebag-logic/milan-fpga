#!/bin/bash
# usage: images.sh PACKET REPO LITEX_ROOT
# Build the SRP size fixture's runtime from provisioned sources, link F4's
# ctrl_srp_image.py at 1x1 and 8x8, IF=1 and IF=2, and F3's ctrl_image.py,
# with the pinned RV32 SDK installed (offline, digest-checked) under PACKET/scratch/sdk.
P=$1; R=$2; L=$3; S=$P/scratch; RT=$S/runtime; IMG=$S/images; mkdir -p $RT $IMG $S/tmp
export MILAN_RV32_CC=$S/sdk/bin/riscv32-linux-gcc PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S/tmp
cd $R
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py \
  --picolibc $L/pythondata-software-picolibc/pythondata_software_picolibc/data \
  --compiler-rt $L/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data \
  --litex-software $L/litex/litex/soc/software --output $RT > $IMG/runtime.out 2>&1 || { echo "runtime rc=$?"; exit 10; }
rc=0
for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do for i in 1 2; do
  python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$cfg.yaml --interfaces $i \
    --output $IMG/srp-$cfg-if$i --libc $RT/libc.a --compiler-runtime $RT/libcompiler_rt.a > $IMG/srp-$cfg-if$i.out 2>&1
  r=$?; echo "ctrl_srp_image $cfg IF=$i rc=$r $(python3 -I -c "import json,sys;d=json.load(open(sys.argv[1]));print('ram_span',d.get('ram_span'),{k:d[k] for k in d if k in ('text','rodata','data','bss')})" $IMG/srp-$cfg-if$i/size.json 2>/dev/null)"; [ $r = 0 ] || rc=1
done; done
python3 sw/firmware/ctrl/test/ctrl_image.py --out $IMG/f3 > $IMG/f3.out 2>&1; r=$?; echo "ctrl_image (F3) rc=$r"; [ $r = 0 ] || rc=1
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 > $IMG/f3-selftest.out 2>&1; r=$?; echo "ctrl_image_selftest rc=$r"; [ $r = 0 ] || rc=1
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32 > $IMG/rv32-selftest.out 2>&1; r=$?; echo "fw_rv32_selftest rc=$r"; [ $r = 0 ] || rc=1
exit $rc
