#!/usr/bin/env bash
# Disposable mutation probes on the #117 page and the recovery design page:
# each probe plants one defect in the working tree, runs the gate that should
# refuse it, records the exit status, and restores the exact original bytes.
# usage: mutation_probes.sh <clone> <scratch-dir>
set -u
clone=$1
scratch=$(cd "$2" && pwd) || exit 2  # absolute: the probes run from inside the clone
page=docs/findings/117_GPTP_SILICON_EVIDENCE.md
design=docs/design/GM_LOSS_RECOVERY.md
cd "$clone" || exit 2
cp -p "$page" "$scratch/page.orig"
cp -p "$design" "$scratch/design.orig"

restore() {
  cp -p "$scratch/page.orig" "$page"
  cp -p "$scratch/design.orig" "$design"
}

probe() {  # name, gate command...
  local name=$1
  shift
  "$@" >"$scratch/probe_$name.log" 2>&1
  local rc=$?
  printf '%-34s rc=%s  %s\n' "$name" "$rc" "$(tail -1 "$scratch/probe_$name.log" | cut -c1-150)"
  restore
}

# the host prefix is assembled from code points, as the repository gate does
prefix=$(python3 -c 'print("".join(map(chr,(97,109,120,45))))')
usb=$(python3 -c 'print("".join(map(chr,(115,101,114,105,97,108,47,98,121,45,105,100,47,117,115,98,45))))')

python3 - "$page" "$prefix" <<'EOF'
import sys; p, t = sys.argv[1], sys.argv[2]
s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace("- **Controller host.** It sits", "- **Controller host.** It is " + t + "pw1 and sits", 1))
EOF
probe P1_bench_host_prefix python3 scripts/docs_check.py

python3 - "$page" "$usb" <<'EOF'
import sys; p, t = sys.argv[1], sys.argv[2]
s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace("- **Capture point.** One", "- **Capture point.** Console on /dev/" + t + "Adapter0. One", 1))
EOF
probe P2_usb_by_id_path python3 scripts/docs_check.py

python3 - "$page" <<'EOF'
import sys; p = sys.argv[1]
s = open(p, encoding="utf-8").read()
assert "GM_LOSS_RECOVERY.md#recovery-bound)" in s
open(p, "w", encoding="utf-8").write(s.replace("GM_LOSS_RECOVERY.md#recovery-bound)", "GM_LOSS_RECOVERY.md#recovery-bounds)", 1))
EOF
probe P3_broken_cross_page_anchor python3 scripts/docs_check.py
python3 - "$page" <<'EOF'
import sys; p = sys.argv[1]
s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace("GM_LOSS_RECOVERY.md#recovery-bound)", "GM_LOSS_RECOVERY.md#recovery-bounds)", 1))
EOF
probe P3b_broken_anchor_verify_anchors python3 scripts/gen_toc.py --verify-anchors

python3 - "$design" <<'EOF'
import sys; p = sys.argv[1]
s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace("## Recovery bound\n", "## Recovery limit\n", 1))
EOF
probe P4_renamed_heading_toc python3 scripts/gen_toc.py --check

python3 - "$page" <<'EOF'
import sys; p = sys.argv[1]
s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace("(#grandmaster-change-across-the-loss-and-return)", "(#grandmaster-change-across-the-loss)", 1))
EOF
probe P5_broken_intra_page_anchor python3 scripts/docs_check.py
for g in "P5b_intra_page_anchor_verify_anchors:scripts/gen_toc.py --verify-anchors" "P5c_intra_page_anchor_toc_check:scripts/gen_toc.py --check"; do
  python3 - "$page" <<'EOF2'
import sys; p = sys.argv[1]
s = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(s.replace("(#grandmaster-change-across-the-loss-and-return)", "(#grandmaster-change-across-the-loss)", 1))
EOF2
  probe "${g%%:*}" python3 ${g#*:}
done

cmp -s "$scratch/page.orig" "$page" && cmp -s "$scratch/design.orig" "$design" && echo "restored: byte-identical" || echo "RESTORE FAILED"
