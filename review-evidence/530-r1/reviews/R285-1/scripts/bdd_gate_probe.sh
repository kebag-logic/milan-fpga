#!/usr/bin/env bash
# Plant the pre-#530 gate source into milan_datapath.sv, run the streaming
# licence feature, then restore the file byte-for-byte and prove it.
set -uo pipefail
repo=$1; f="$repo/hdl/milan/milan_datapath.sv"; bak=$(mktemp)
cp -p "$f" "$bak"
sed -i 's/assign lwsrp_stream_gate = pp_cd_srp_active_w\[/assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[/' "$f"
grep -c "assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w" "$f"
(cd "$repo/tests" && behave --no-capture -f plain features/milan_streaming_licence.feature 2>&1 | grep -E "Assertion|expression is|scenarios passed|failed" | head -5)
cp -p "$bak" "$f"; rm -f "$bak"
git -C "$repo" diff --quiet -- hdl/milan/milan_datapath.sv && echo "restored: no diff"
