#!/usr/bin/env bash
# INFORMATIVE ONLY, not candidate validation (manager-owned, 41+5 bar): the
# three gate 36a functions and gate 32 on the tree git merge-tree computes
# for the reviewed head and live dev 52711029, in a throwaway scratch clone.
set -euo pipefail
SC=${SCRATCH:-/tmp/r222-478-r2-scratch}
R=$VALIDATION_STORAGE/reviews/r222-478-r2
G="$SC/base-sub"
HEAD_C=1496558d82cf35fc98dda0e781b2a1be643c301a
DEV=52711029f374650dc93830d5ea28e81cb5c8f410
TREE=93be2b5788c4b79e88bfe22fbaf985686bbdc8f2
C="$SC/cand-sub"
rm -rf "$C"
git clone -q --no-hardlinks --no-checkout "$G" "$C"
git -C "$C" fetch -q "$G" "$DEV" "$HEAD_C"
[ "$(git -C "$C" merge-tree --write-tree "$HEAD_C" "$DEV")" = "$TREE" ]
commit=$(GIT_AUTHOR_NAME=scratch GIT_AUTHOR_EMAIL=scratch@invalid GIT_COMMITTER_NAME=scratch \
  GIT_COMMITTER_EMAIL=scratch@invalid GIT_AUTHOR_DATE="1970-01-01T00:00:00Z" GIT_COMMITTER_DATE="1970-01-01T00:00:00Z" \
  git -C "$C" commit-tree "$TREE" -p "$HEAD_C" -p "$DEV" -m "scratch candidate (not published)")
git -C "$C" checkout -q --detach "$commit"
git -C "$C" submodule init -- third_party/verilog-axis protocol-processor gptp-processor
for p in third_party/verilog-axis protocol-processor gptp-processor; do
  git -C "$C" config "submodule.$p.url" "$R/.git/modules/$p"
done
git -C "$C" -c protocol.file.allow=always submodule update -q -- third_party/verilog-axis protocol-processor gptp-processor
echo "scratch candidate commit $commit tree $(git -C "$C" rev-parse 'HEAD^{tree}')"
git -C "$C" submodule status
cd "$C"
python3 -B - <<'PY'
import contextlib, io, sys
sys.path.insert(0, "sw/builder")
import test_builder as tb
for fn in (tb.test_audio_unit_rates_loader_contract, tb.test_audio_unit_shipping_rates,
           tb.test_pp_shadow_audio_unit_rates_match_config, tb.test_builder_doc_key_map):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn()
        print("PASS", fn.__name__)
    except BaseException as exc:
        print("FAIL", fn.__name__, type(exc).__name__, str(exc)[:200])
PY
echo "tracked changes after run: $(git -C "$C" status --porcelain --untracked-files=no | wc -l)"
