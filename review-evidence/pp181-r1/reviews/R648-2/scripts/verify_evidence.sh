#!/usr/bin/env bash
# Verify the published round-2 author receipts for issue #181 against the published manifests
# and extract the figures the PR cites.
# usage: verify_evidence.sh <evidence-root: .../review-evidence/pp181-r1> <processor-git-dir> <out-dir>
set -u
ev=$1; git_dir=$2; out=$3
r2=$ev/author-r2/receipts-r2
mkdir -p "$out"
{
  echo "## inner manifests (sha256sum -c sums/MANIFEST-*.sha256, in receipts-r2)"
  ( cd "$r2" && for m in sums/MANIFEST-*.sha256; do
      n=$(wc -l < "$m"); bad=$(sha256sum -c "$m" 2>/dev/null | grep -vc ': OK$')
      echo "$m entries=$n not-ok=$bad"; sha256sum -c "$m" 2>/dev/null | grep -v ': OK$'
    done )
  echo
  echo "## top-level MANIFEST.json, author-r2 entries"
  ( cd "$ev" && python3 -I - <<'PY'
import json, hashlib, os
m = {e["file"]: e for e in json.load(open("MANIFEST.json"))}
r2 = [k for k in m if k.startswith("author-r2/")]
bad = [k for k in r2 if hashlib.sha256(open(k, "rb").read()).hexdigest() != m[k]["published_sha256"]]
disk = {os.path.join(d, f) for d, _, fs in os.walk("author-r2") for f in fs}
print(f"entries={len(r2)} published-mismatch={len(bad)} unlisted-on-disk={len(disk - set(r2))}")
for k in sorted(r2):
    e = m[k]
    if e["path_redacted"] and e["original_sha256"] != e["published_sha256"]:
        print(f"redacted at publication: {k} original={e['original_sha256'][:16]} published={e['published_sha256'][:16]}")
PY
  )
  echo
  echo "## route-1x1 with #760 at head"
  sed -n 1,3p "$r2/route-head760/route.out"
  grep -E 'rc=|EXPORT-DONE|ROUTE-DONE' "$r2/route-head760/route.out"
  grep -E 'WNS_ns|WHS_ns|route status|RESULT' "$r2/route-head760/route-1x1-check.log"
  grep -E '760.patch|apply 760|revert 760|gitlink head' "$r2/route-head760/chain.txt"
  c=$r2/cone/head760/head760
  echo "cone.rpt (count->sel): $(grep -c 'No timing paths found' "$c/cone.rpt") 'No timing paths found'"
  for f in count_to_nempty nempty_to_sel clkout1_top10 to_sel; do
    echo "$f: $(grep -m1 -E '^Slack' "$c/$f.rpt" | tr -s ' ') | $(grep -m1 -E 'Logic Levels' "$c/$f.rpt" | tr -s ' ')"
    grep -m2 -E '^ *(Source|Destination):' "$c/$f.rpt" | tr -s ' '
  done
  echo
  echo "## OOC"
  cat "$r2/ooc/chain-ooc.txt"
  for d in base-1x1 head-1x1 base-8x8 head-8x8; do
    o=$r2/ooc/$d
    printf '%s: WNS %s | cone %s | nempty->sel %s\n' "$d" \
      "$(grep -m1 -E '^Slack' "$o/timing.rpt" | grep -oE '[-0-9.]+ns')" \
      "$( (grep -q 'No timing paths' "$o/cone.rpt" && echo 'no path') || grep -m1 'Logic Levels' "$o/cone.rpt" | tr -s ' ')" \
      "$( [ -f "$o/nempty_to_sel.rpt" ] && grep -m1 'Logic Levels' "$o/nempty_to_sel.rpt" | tr -s ' ' || echo -)"
  done
  echo
  echo "## proofs"
  cat "$r2/proofs/rc.txt"
  for d in "$r2"/proofs/run-*; do echo "$(basename "$d"): $(grep -hoE 'Of those cells [0-9]+ are proven and [0-9]+ are unproven|Found [0-9]+ unproven \$equiv cells\.' "$d"/* | tail -1)"; done
  for p in "head_KL_pp_event_router.sv c5afc0a42f200af01dd83e67b579dc3badc42601:hdl/packet_engine/KL_pp_event_router.sv" \
           "base_KL_pp_event_router.sv 08ae00130f096f241463172c4781885934400ee4:hdl/packet_engine/KL_pp_event_router.sv" \
           "head_KL_aecp_notify.sv c5afc0a42f200af01dd83e67b579dc3badc42601:hdl/aecp/KL_aecp_notify.sv"; do
    set -- $p; git -C "$git_dir" show "$2" | cmp -s - "$r2/proofs/src/$1" && echo "src/$1 == $2" || echo "src/$1 DIFFERS from $2"
  done
  echo
  echo "## processor gates"
  for s in head base; do echo "-- $s"; cat "$r2/logs/$s/env.txt"; cat "$r2/logs/$s/rc.txt"; tail -1 "$r2/logs/$s/run_suites.log"; cat "$r2/logs/$s/req_tags_executed.log"; done
  echo
  echo "## campaigns"
  for s in head base; do echo "-- $s"; cat "$r2/camp/$s"/rc-*.txt "$r2/camp/$s/done.txt"; tail -1 "$r2/camp/$s/notify.log"; done
  grep -E 'occupancy_' "$r2/camp/head/notify.log" | sort -u
  head -14 "$r2/camp/camp_compare_lines.out"
  echo
  echo "## parent consumer gates (rc only, base vs head)"
  diff <(sed -E 's/ secs=[0-9]+//' "$r2/pgates/base/summary.txt") <(sed -E 's/ secs=[0-9]+//' "$r2/pgates/head/summary.txt") && echo "rc tables identical"
  grep 'rc=1' "$r2/pgates/head/summary.txt"
  cat "$r2/pgates/base/gitlink.txt" "$r2/pgates/head/gitlink.txt"
  for g in check_submodule_docs measure_test_evidence measure_test_evidence_selftest; do
    cmp -s "$r2/pgates/base/$g.log" "$r2/pgates/head/$g.log" && echo "$g.log identical base/head"
  done
  diff <(grep '^+[0-9a-f]' "$r2/pgates/base/rom_digests.diff" | cut -f2,3) <(grep '^+[0-9a-f]' "$r2/pgates/head/rom_digests.diff" | cut -f2,3) && echo "ROM digests identical base/head"
} > "$out/evidence_check.txt" 2>&1
cat "$out/evidence_check.txt"
