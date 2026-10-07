#!/usr/bin/env bash
# Reviewer follow-up checks (run after campaigns.sh). Usage: extra_checks.sh <checkout> <packet>
# Produces: receipts/cgreen build (prerequisite), base-a4cbe41-{off,on}, upstream-merge-check.txt,
# hosted-check-runs.txt, sanitizer/, source-diff.txt, merge-cc.txt, clone-integrity.txt.
set -u
SRC=$1; PKT=$2; S=$PKT/scratch; R=$PKT/receipts; P=$S/cgreen-prefix
BASE=a4cbe41de1c80d43f26e0d348cbdb45075273a4f; HEAD_SHA=ced667d8ee35929ab5f9e77a1c5396e173a693d8
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$S" "$R/sanitizer"

# Prerequisite: unit framework in a scratch prefix (run once, before campaigns.sh).
if [ ! -e "$P/lib/libcgreen.so" ]; then
  git clone -q --depth 1 --branch 1.6.3 https://github.com/cgreen-devs/cgreen.git "$S/cgreen-src"
  cmake -S "$S/cgreen-src" -B "$S/cgreen-build" -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_INSTALL_PREFIX="$P" -DCGREEN_WITH_UNIT_TESTS=OFF -DCGREEN_WITH_XML=OFF \
    -DCGREEN_WITH_LIBXML2=OFF -DCMAKE_BUILD_TYPE=Release '-DCMAKE_C_FLAGS=-DGITREVISION="1.6.3"'
  make -C "$S/cgreen-build" -j16 install
fi

# Base commit counts in both profiles.
rm -rf "$S/base"; mkdir -p "$S/base"; git -C "$SRC" archive "$BASE" | tar -x -C "$S/base"
bash "$PKT/scripts/run_profile.sh" "$S/base" OFF "$S/base-build-off" "$R/base-a4cbe41-off" "$P" &
bash "$PKT/scripts/run_profile.sh" "$S/base" ON "$S/base-build-on" "$R/base-a4cbe41-on" "$P" &

# Sanitized unit runs in both profiles.
for prof in OFF ON; do
  ( cmake -S "$SRC" -B "$S/asan-$prof" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$prof -DCMAKE_PREFIX_PATH="$P" \
      "-DCMAKE_C_FLAGS=-fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=undefined" \
      > "$R/sanitizer/configure-$prof.log" 2>&1; echo "configure rc=$?"
    cmake --build "$S/asan-$prof" --parallel 4 > "$R/sanitizer/build-$prof.log" 2>&1; echo "build rc=$?"
    LD_LIBRARY_PATH="$P/lib" ASAN_OPTIONS=detect_leaks=1 "$S/asan-$prof/unit_tests" > "$R/sanitizer/unit-$prof.log" 2>&1
    echo "unit rc=$?" ) > "$R/sanitizer/rc-$prof.txt" &
done

# Upstream refs and a merge of the head into current main, in a separate bare clone.
( rm -rf "$S/upstream.git"; git clone -q --bare https://github.com/kebag-logic/lwSRP.git "$S/upstream.git"
  cd "$S/upstream.git" && git fetch -q origin '+refs/pull/15/head:refs/pr15'
  { git ls-remote origin main refs/pull/15/head; git log --format='%H %P %s' -3 main
    git rev-parse refs/pr15 'refs/pr15^{tree}'; git diff --name-status "$BASE" main
    t=$(git merge-tree --write-tree main refs/pr15); echo "merge-tree rc=$? $t"
    git diff --name-status refs/pr15 "$(echo "$t" | head -1)"; } > "$R/upstream-merge-check.txt" 2>&1 ) &

# Hosted contexts on the exact head (read-only).
( gh api "repos/kebag-logic/lwSRP/commits/$HEAD_SHA/check-runs" -q '.total_count, (.check_runs[] | "\(.name) | \(.status) | \(.conclusion)")'
  gh api "repos/kebag-logic/lwSRP/commits/$HEAD_SHA/status" -q '.state, .total_count' ) > "$R/hosted-check-runs.txt" 2>&1 &
wait

# History and source scope.
{ git -C "$SRC" diff --stat "$BASE" "$HEAD_SHA" -- src; git -C "$SRC" rev-parse "$BASE:src" "$HEAD_SHA:src"
  git -C "$SRC" diff --name-status "$BASE" "$HEAD_SHA"; } > "$R/source-diff.txt" 2>&1
git -C "$SRC" show --cc "$HEAD_SHA" > "$R/merge-cc.txt"

# Exact-head integrity of the checkout.
( cd "$SRC" && { git rev-parse HEAD 'HEAD^{tree}'; git status --porcelain=v1 --ignored --untracked-files=all
  git diff --exit-code >/dev/null; echo "diff rc=$?"; git diff --cached --exit-code >/dev/null; echo "cached rc=$?"
  git write-tree; git ls-files -s | awk '$1=="160000"'
  git ls-tree -r HEAD | while read -r mode type sha path; do
    [ "$(git hash-object --no-filters -- "$path")" = "$sha" ] || echo "BLOB MISMATCH $path"
    if [ -x "$path" ]; then am=100755; else am=100644; fi; [ "$am" = "$mode" ] || echo "MODE MISMATCH $path"
  done; echo verify-end; } ) > "$R/clone-integrity.txt" 2>&1
