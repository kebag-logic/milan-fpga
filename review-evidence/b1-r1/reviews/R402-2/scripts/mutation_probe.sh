#!/usr/bin/env bash
# Show that each round-2 check can fail: plant one defect per probe in a disposable copy
# and require the check to report it. Never touches the review clone or the retained raws.
# usage: mutation_probe.sh <packet-root> <review-clone> <raw-storage-dir> <author-r2-dir> <b1-r1-archive-dir> <round1-archive-dir>
set -u
P=$1; R=$2; S=$3; A=$4; B=$5; O=$6
W=$P/scratch/mut; rm -rf "$W"; mkdir -p "$W"
killed=0; total=0
probe() {  # name, expected-nonzero command...
  local name=$1; shift; total=$((total+1))
  if "$@" >/dev/null 2>&1; then echo "SURVIVED $name"; else echo "KILLED   $name"; killed=$((killed+1)); fi
}
# page copy with one raw-artifact hash digit changed
git -C "$R" worktree list >/dev/null
mkdir -p "$W/repo/docs/findings"
cp "$R"/docs/findings/599_394_E1_LINK_CYCLES.md "$R"/docs/findings/387_SOFTWARE_GM_STEP.md "$W/repo/docs/findings/"
sed -i '0,/| cycle05 | `console.jsonl` | 1031063 | `1/s//| cycle05 | `console.jsonl` | 1031063 | `2/' "$W/repo/docs/findings/599_394_E1_LINK_CYCLES.md"
probe "verify_retention: one page hash row altered" python3 -B "$P/scripts/verify_retention.py" "$S" "$W/repo" "$A"
probe "rederive_r2: one page hash row altered" python3 -B "$P/scripts/rederive_r2.py" "$S/raw" "$W/repo" "$A"
# a raw copy with one byte changed, fed to the author's extraction and to rederive_r2
mkdir -p "$W/raw"; cp -a "$S/raw/." "$W/raw/"; printf 'X' | dd of="$W/raw/gm03/console.jsonl" bs=1 seek=100 conv=notrunc status=none
probe "author extract_pdelay: one raw byte changed" python3 -B "$A/extract/extract_pdelay.py" "$W/raw" "$R"
probe "rederive_r2: one raw byte changed" python3 -B "$P/scripts/rederive_r2.py" "$W/raw" "$R" "$A"
# a planted private token in a packet copy (a line lifted from the unredacted round-1 port log)
mkdir -p "$W/pkt"; cp -a "$A/." "$W/pkt/"; head -1 "$O/author/bench/gm01/ptp4l-gm.log" >> "$W/pkt/r1/bench/gm01/ptp4l-gm.log"
probe "scrub_packet: one unredacted port-log line planted" python3 -B "$P/scripts/scrub_packet.py" --repo "$R" --private "$S/raw" --private "$O" --target planted="$W/pkt"
# the controller identity re-inserted into a redacted transcript copy
mkdir -p "$W/b1/author-r2"; cp -a "$B/." "$W/b1/"; rm -rf "$W/b1/reviews"
python3 - "$W/b1/author-r2/r1/bench/final/controller.jsonl" "$O/author/bench/final/controller.jsonl" <<'PY'
import sys
from pathlib import Path
Path(sys.argv[1]).write_bytes(Path(sys.argv[2]).read_bytes())
PY
probe "redaction_audit: one unredacted transcript restored" python3 -B "$P/scripts/redaction_audit.py" "$O" "$W/b1"
# a measurement-table cell changed between two commits (via a throwaway commit in a scratch clone)
git clone -q --no-checkout "$R" "$W/clone" && git -C "$W/clone" checkout -q 931c3edfced972e01356cd989b5092a1672de5a3 && \
  sed -i 's/| 3 | 20.88 | 2.31-2.56 |/| 3 | 20.89 | 2.31-2.56 |/' "$W/clone/docs/findings/599_394_E1_LINK_CYCLES.md" && \
  git -C "$W/clone" -c user.name=probe -c user.email=probe@invalid commit -qam probe
probe "table_identity: one per-cycle cell changed" bash -c "python3 -B '$P/scripts/table_identity.py' '$W/clone' 931c3edfced972e01356cd989b5092a1672de5a3 HEAD | grep -q '^  IDENTICAL (12 lines) | Cycle' && exit 0 || exit 1"
echo "killed $killed of $total"
rm -rf "$W"
[ "$killed" = "$total" ]
