#!/bin/sh
# R242 #423 design-review evidence, end to end (read-only against TRUSTED).
#   sh scripts/run_all.sh /path/to/trusted/checkout [OUTDIR] [WORKDIR]
# TRUSTED must be a clean checkout of dev 88e9276b2a220c716f64a843f7e1eb8f9265e896.
# Needs git >= 2.39, python3, an authenticated gh (public reads only), network
# for the public donor clone.  Writes only OUTDIR and WORKDIR.
set -eu
TRUSTED=$(cd "$1" && pwd)
HERE=$(cd "$(dirname "$0")/.." && pwd)
OUT=${2:-$HERE/rawlogs-rerun}
WORK=${3:-$(mktemp -d -t r242-423-XXXXXX)}
mkdir -p "$OUT" "$WORK"
CHECKER=$TRUSTED/scripts/check_merge_containment.py
PROTO=$WORK/prototype
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null

test "$(GIT_OPTIONAL_LOCKS=0 git -C "$TRUSTED" rev-parse HEAD)" = \
     88e9276b2a220c716f64a843f7e1eb8f9265e896
python3 -B "$HERE/scripts/integrity.py" snapshot "$TRUSTED" "$OUT/integrity-before.json" >/dev/null
python3 -B "$HERE/scripts/verify_published_manifest.py" \
    "$HERE/published-fixture-6181e900" > "$OUT/verify-published-manifest.log" 2>&1
python3 -B "$HERE/scripts/make_prototype.py" "$TRUSTED" "$PROTO" \
    > "$OUT/prototype.diff" 2> "$OUT/prototype-build.log"

mkdir -p "$WORK/selftest-cwd"
git -C "$WORK/selftest-cwd" init -q -b main
git -C "$WORK/selftest-cwd" -c user.name=r -c user.email=r@r commit -q --allow-empty -m seed
for which in unchanged prototype; do
  c=$CHECKER; [ "$which" = prototype ] && c=$PROTO/check_merge_containment.py
  (cd "$WORK/selftest-cwd" && python3 -B -I "$c" --selftest) \
      > "$OUT/$which-selftest.log" 2>&1 && echo "rc=0" >> "$OUT/$which-selftest.log" \
      || echo "rc=$?" >> "$OUT/$which-selftest.log"
done

python3 -B "$HERE/scripts/fixtures.py" "$CHECKER" "$PROTO/check_merge_containment.py" \
    "$WORK/fixtures" "$OUT/fixture-matrix.json" > "$OUT/fixture-matrix.log" 2>&1 || true
python3 -B "$HERE/scripts/mutations.py" "$PROTO/check_merge_containment.py" \
    "$WORK/fixtures" > "$OUT/mutations.log" 2>&1 || true

git clone -q --mirror https://github.com/Mister-M-alt/FPGA-gPTP.git "$WORK/donor.git"
python3 -B "$HERE/scripts/reconstruct_pr62.py" "$WORK/donor.git" "$CHECKER" \
    "$PROTO/check_merge_containment.py" "$OUT/pr62-reconstruction.json" \
    > "$OUT/pr62-reconstruction.log" 2>&1
for which in trusted prototype; do
  c=$CHECKER; [ "$which" = prototype ] && c=$PROTO/check_merge_containment.py
  (mkdir -p "$WORK/probe" && cd "$WORK/probe" && python3 -B \
      "$HERE/published-fixture-6181e900/probe/probe_ff_merge.py" "$c") \
      > "$OUT/published-probe-$which.json" 2>&1
done
python3 -B "$HERE/scripts/integrity.py" snapshot "$TRUSTED" "$OUT/integrity-after.json" >/dev/null
python3 -B "$HERE/scripts/integrity.py" compare "$OUT/integrity-before.json" "$OUT/integrity-after.json"
grep -h "RESULT\|selftest: " "$OUT"/*.log
