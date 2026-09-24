#!/usr/bin/env bash
# R294 probe P1: does a changed Talker Failed FailureInformation (same
# registered type) make the SRP Listener applicant re-declare with New?
# Usage: probe_srp_redeclare.sh <extracted-tree> <log>
# Runs on a DISPOSABLE extracted tree (git archive), never on the clone.
set -euo pipefail
tree=$1; log=$2
here=$(cd "$(dirname "$0")" && pwd)
f=$tree/tb/srp_stream_fsms/sim_main.cpp
anchor='        "L AskingFailed rides New after the swap");'
grep -qF "$anchor" "$f"
python3 - "$f" "$anchor" <<'PY'
import sys
path, anchor = sys.argv[1], sys.argv[2]
src = open(path).read()
probe = anchor + r'''
  // ---- R294 probe P1 (disposable) ----
  for (int i = 0; i < 6; ++i) { h.clear_logs(); h.tick(); }
  h.clear_logs(); h.tick();
  printf("R294-P1 quiet-baseline pushes=%zu\n", h.l_push.size());
  h.clear_logs();
  h.inject(true, 2, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 999, 0xBBBB0000DDDDull, 9);
  printf("R294-P1 changed-failure: fcode=%u bridge=%llx reg_strobes=%d\n",
         h.l_fcode(0), (unsigned long long)h.l_fbridge(0), h.l_reg[0]);
  h.tick();
  printf("R294-P1 changed-failure next tick pushes=%zu", h.l_push.size());
  for (auto& p : h.l_push) printf(" [type=%u code=%u fp=%u]", p.type, p.code, p.fp);
  printf("\n");
  for (int i = 0; i < 6; ++i) { h.clear_logs(); h.tick(); }
  h.clear_logs();
  h.inject(true, 2, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 999, 0xBBBB0000DDDDull, 9);
  printf("R294-P1 unchanged-failure: reg_strobes=%d\n", h.l_reg[0]);
  h.tick();
  printf("R294-P1 unchanged-failure next tick pushes=%zu\n", h.l_push.size());
  h.clear_logs();
  // ---- end probe ----'''
assert src.count(anchor) == 1
open(path, "w").write(src.replace(anchor, probe))
PY
cd "$tree/tb/srp_stream_fsms"
rm -rf obj_dir
make VERILATOR="$here/verilator8" > "$log" 2>&1 || true
grep 'R294-P1' "$log"
