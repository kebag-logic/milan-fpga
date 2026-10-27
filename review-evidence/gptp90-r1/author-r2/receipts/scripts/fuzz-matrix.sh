#!/bin/bash
# tsn_fuzz ptp at base (55680bff) without and with the campaign edit, then at
# the round-1 head (d27a1654) without it. Runs in the alternate parent clone.
set -u
P=<parent-explore>-alt; E=<scratch>/fuzz-edit.patch
export TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c
cd "$P" || exit 2
run() {
  echo "=== $1: gitlink $(git -C gptp-processor rev-parse HEAD), campaign edit: $2"
  make -C tb/verilator/tsn_fuzz clean > /dev/null
  make -C tb/verilator/tsn_fuzz ptp > "<scratch>/explore/fuzz-$1.log" 2>&1
  echo "rc=$?"
  grep -E '== gPTP|\[FAIL\]|freshness' "<scratch>/explore/fuzz-$1.log"
  git checkout -q hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md
}
test "$(git -C gptp-processor rev-parse --show-toplevel)" = "$P/gptp-processor" || exit 2
run base-unedited no
git apply "$E"; run base-edited yes; git checkout -q tb/verilator/tsn_fuzz/fuzz_ptp_timing.py
git -C gptp-processor checkout -q d27a1654285614ded5093cb58f58bceed551fdae
run round1-unedited no
git -C gptp-processor checkout -q 55680bff3b287b9a7b0c759f51471fa617c17335
git status --short
