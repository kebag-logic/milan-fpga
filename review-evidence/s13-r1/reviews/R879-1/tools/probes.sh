#!/usr/bin/env bash
# probes.sh CLONE OUTDIR: disposable mutation probes of the flip's rules, each one planted defect in CLONE (a
# throwaway clone at the reviewed head), the check that must refuse it run, the file restored with git checkout, and
# the clone proven clean before the next. A probe is CAUGHT when the check exits non-zero and its log carries the words
# named; ESCAPED otherwise.
set -u
C=$(realpath "$1"); O=$(realpath -m "$2"); T=$(dirname "$(realpath "$0")")
source "$T/env.sh"
mkdir -p "$O"; cd "$C"
plant() {  # file old new: replace the one occurrence of old
  python3 - "$1" "$2" "$3" <<'EOF'
import sys
p, old, new = sys.argv[1:4]
s = open(p).read()
assert s.count(old) == 1, f"{p}: anchor occurs {s.count(old)} times"
open(p, "w").write(s.replace(old, new))
EOF
}
probe() {  # name file old new words cmd...
  local name=$1 file=$2 old=$3 new=$4 words=$5; shift 5
  plant "$file" "$old" "$new" || { echo "PROBE $name: SETUP FAILED"; return; }
  ( eval "$@" ) > "$O/$name.log" 2>&1; local rc=$?
  git checkout -q -- "$file"
  local dirty; dirty=$(git status --porcelain --untracked-files=no | wc -l)
  if [ $rc -ne 0 ] && grep -qF -- "$words" "$O/$name.log"; then v=CAUGHT; else v=ESCAPED; fi
  echo "PROBE $name: $v (rc $rc; words '$words'; tracked files dirty after restore: $dirty)"
}
B="cd sw/builder && python3 test_builder.py --require-elaboration --gates"

probe rtl-select-inverted hdl/common/csr/milan_csr.sv "(CTRL_SPLIT_P != 0) ?" "(CTRL_SPLIT_P == 0) ?" "FAIL" \
  "make -C tb/verilator/csr -j8 run"
probe rtl-split-minor-moved hdl/common/csr/milan_csr.sv "{VERSION_SPLIT_MAJOR, VERSION[15:0]}" "{VERSION_SPLIT_MAJOR, 16'h0061}" \
  "the split datapath reads VERSION 0x0003_0060" "make -C tb/verilator/milan_dp -j8 split"
probe builder-recipe-keeps-string sw/builder/endstation_builder.py \
  'entity = {**entity, "firmware_version": rtl_firmware_version(entity["firmware_rev"], placement)}' 'entity = dict(entity)' \
  "gate 23o" "$B test_placement_recipe,test_firmware_version_derived_from_rtl"
probe builder-entity-ignores-placement sw/builder/endstation_builder.py \
  'firmware_version=rtl_firmware_version(rev, placement),' 'firmware_version=rtl_firmware_version(rev),' \
  "!= '3.96.0'" "$B test_firmware_version_derived_from_rtl"
probe config-1x1-reverted configs/endstation_ax7101_1x1_tdm8.yaml "  placement: split" "  placement: all-fabric" \
  "ax7101_1x1_tdm8: a tracked config is" "$B test_control_placement_key"
probe identity-reads-allfabric sw/litex/check_image_identity.py \
  'placement = "split" if claimed is not None else "all-fabric"' 'placement = "all-fabric"' \
  "gate 23p" "$B test_image_identity_gate"
probe manifest-allfabric-version sw/litex/milan_soc.py \
  'major, minor = check_image_identity.rtl_version(placement="split")' 'major, minor = check_image_identity.rtl_version()' \
  "gate 23p" "$B test_image_identity_gate"
probe sweep-row-allfabric sw/litex/sweep.sh " --cpu-count 1 --ctrl-mailbox --ctrl-firmware sw/builder/out/endstation_ax7101_1x1_tdm8/ctrl_app.elf\"; L2=0;;" \
  " --cpu-count 1\"; L2=0;;" "gate" "$B test_current_shape_matches_sweep_flags,test_sweep_opts_fragments"
probe ledger-reads-allfabric-major scripts/check_feature_status.py \
  'actual = f"0x{split[0].upper()}_{matches[0][1].upper()}"' 'actual = f"0x{matches[0][0].upper()}_{matches[0][1].upper()}"' \
  "gateware version conflict" "python3 -B scripts/check_feature_status.py"
probe entity-shape-ignores-placement scripts/check_entity_shape.py \
  'g.firmware_version_string(rev, RTL.csr, cfg["control"]["placement"]))' 'g.firmware_version_string(rev, RTL.csr))' \
  "FAIL" "python3 -B scripts/check_entity_shape.py"
echo "final porcelain: $(git status --porcelain --untracked-files=no | wc -l) $(git rev-parse HEAD)"
echo PROBES_DONE
