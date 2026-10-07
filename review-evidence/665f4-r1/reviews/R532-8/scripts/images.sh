#!/bin/bash
# Build the SRP size fixture's runtime from the provisioned sources, check every
# input hash against the author's published runtime record, then link F3's
# ctrl_image.py images and F4's ctrl_srp_image.py at 1x1 and 8x8, IF=1 and IF=2.
. "$(dirname "$0")/env.sh"
L=${LITEX_ROOT:-$HOME/litex-milan}; RT=$S/runtime; IMG=$S/images; mkdir -p $RT $IMG
cd $R
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py \
  --picolibc $L/pythondata-software-picolibc/pythondata_software_picolibc/data \
  --compiler-rt $L/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data \
  --litex-software $L/litex/litex/soc/software --output $RT || exit 10
python3 -I - "$RT/provenance.json" "$P/scratch/pub-evidence/ROUND7-RUNTIME.json" "$L" "$RT" <<'PY' || exit 11
import json,sys
mine=json.load(open(sys.argv[1])); ref=json.load(open(sys.argv[2])); L,RT=sys.argv[3],sys.argv[4]
def norm(p): return p.replace(L,"$USER_DIRECTORY/litex-milan").replace(RT,"$RUNTIME")
# Archives embed member timestamps/uids (non-deterministic ar), so they are
# compared by size; every compiled source and header must match by SHA256.
key=lambda f:(f["size"],) if f["path"].endswith(".a") else (f["size"],f["sha256"])
a={norm(f["path"]):key(f) for f in mine["files"]}; b={f["path"]:key(f) for f in ref["files"]}
diff=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]
print("runtime inputs/outputs compared:",len(a),"published:",len(b),"differing:",sorted(diff))
sys.exit(1 if diff else 0)
PY
rc=0
for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do for i in 1 2; do
  python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$cfg.yaml --interfaces $i \
    --output $IMG/srp-$cfg-if$i --libc $RT/libc.a --compiler-runtime $RT/libcompiler_rt.a > $IMG/srp-$cfg-if$i.out 2>&1
  r=$?; echo "ctrl_srp_image $cfg IF=$i rc=$r ram_span=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))['ram_span'])" $IMG/srp-$cfg-if$i/size.json 2>/dev/null)"; [ $r = 0 ] || rc=1
done; done
python3 sw/firmware/ctrl/test/ctrl_image.py --out $IMG/f3 > $IMG/f3.out 2>&1; r=$?; echo "ctrl_image (F3) rc=$r"; [ $r = 0 ] || rc=1
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 > $IMG/f3-selftest.out 2>&1; r=$?; echo "ctrl_image_selftest rc=$r"; [ $r = 0 ] || rc=1
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32 > $IMG/rv32-selftest.out 2>&1; r=$?; echo "fw_rv32_selftest rc=$r"; [ $r = 0 ] || rc=1
exit $rc
