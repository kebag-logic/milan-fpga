#!/bin/sh
# Spec-facing licence scenario: clean control and two missing-term mutants.
# Copies the tracked HEAD tree (git archive) into scratch so the clone
# is never edited. usage: bdd_arms.sh <clone>
set -u
CLONE=$1
PACKET=${PACKET:-$REVIEWS/551-r297-2-packet}
R=$PACKET/receipts/bdd; mkdir -p "$R"; : > "$R/summary.txt"
GATE_A='  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &'
for arm in clean active_only grant_only active_or_grant; do
  T=$PACKET/scratch/bdd_$arm; rm -rf "$T"; mkdir -p "$T"
  git -C "$CLONE" archive HEAD | tar -x -C "$T"
  F=$T/hdl/milan/milan_datapath.sv
  case $arm in
    active_only) python3 - "$F" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
a="  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];"
assert s.count(a)==1; open(p,"w").write(s.replace(a,"  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0];"))
EOF
    ;;
    grant_only) python3 - "$F" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
a="  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];"
assert s.count(a)==1; open(p,"w").write(s.replace(a,"  assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];"))
EOF
    ;;
    active_or_grant) python3 - "$F" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
a="  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
assert s.count(a)==1; open(p,"w").write(s.replace(a,"  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] |\n"))
EOF
    ;;
  esac
  (cd "$T/tests" && behave --no-capture -f plain features/milan_streaming_licence.feature) > "$R/$arm.log" 2>&1
  echo "$arm rc=$? $(grep -E '^[0-9]+ scenarios? passed' "$R/$arm.log" | head -1)" | tee -a "$R/summary.txt"
done
