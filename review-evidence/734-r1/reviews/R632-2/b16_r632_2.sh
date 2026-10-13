#!/usr/bin/env bash
# [R632] round 2: reproduce the issue #734 B16 case (PR #725 head f1b2489f,
# recorded base 49da9fd9) with the shipping scope step bodies at the head under
# review, against B16's live base (e81ce82f, the first parent of its merge
# 6c810c45) and against the current dev tip a0f39ad4.
# Usage: b16_r632_2.sh <shipping-checkout> <empty-scratch-dir> <python-with-yaml>
set -euo pipefail
ship="$(cd "$1" && pwd)"; work="$2"; py="$3"
head=f1b2489f5b1c929e81eeae79a469b2b27c47e340
rec=49da9fd974e8805d56c90e29dcfcb67994c2c430
live=e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c
landed=6c810c45ac4ac7d5b45797430753020c9ea31d86
mkdir -p "$work"; [ -z "$(ls -A "$work")" ]
git clone -q --no-checkout "$ship" "$work/repo"
repo="$work/repo"; g(){ git -c user.name=probe -c user.email=probe@example.invalid -C "$repo" "$@"; }
mkdir -p "$repo/scripts"
git -C "$ship" show HEAD:scripts/ci_scope.py > "$repo/scripts/ci_scope.py"
git -C "$ship" show HEAD:.gitmodules > "$repo/.gitmodules"
echo "shipping head: $(git -C "$ship" rev-parse HEAD)"
echo "two-dot (default renames) $rec $head: $(g diff --name-only $rec $head | wc -l)"
echo "two-dot (--no-renames)    $rec $head: $(g diff --no-renames --name-only $rec $head | wc -l)"
echo "three-dot (--no-renames)  $rec...$head: $(g diff --no-renames --name-only $rec...$head | wc -l)"
echo "landed merge $landed first parent: $(g rev-parse $landed^1)"
echo "landed merge ^1..merge files: $(g diff --no-renames --name-only $landed^1 $landed | tr '\n' ' ')"
for base in $live a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0; do
  tree="$(g merge-tree --write-tree $base $head | head -1)"
  merge="$(g commit-tree "$tree" -p $base -p $head -m 'GitHub-style merge')"
  g update-ref refs/remotes/origin/dev $base
  for wf in rtl.yml:full-ci-gate:gate rtl-fast.yml:changes:scope elaborate.yml:elaborate:scope; do
    IFS=: read -r f j s <<<"$wf"
    body="$("$py" -I -c 'import sys,yaml
d=yaml.safe_load(open(sys.argv[1]))
[st]=[x for x in d["jobs"][sys.argv[2]]["steps"] if x.get("id")==sys.argv[3]]
print(st["run"].replace("python3 scripts/ci_scope.py --selftest", ":"))' "$ship/.github/workflows/$f" "$j" "$s")"
    for mode in hosted replay; do
      tmp="$(mktemp -d "$work/run.XXXX")"
      if [ $mode = hosted ]; then sha=$merge; act=false; else sha=$head; act=true; fi
      (cd "$repo" && env -i PATH="$PATH" HOME="$tmp" ACT=$act EVENT_NAME=pull_request PR_DRAFT=false \
        PR_BASE_REF=dev PR_HEAD_SHA=$head GITHUB_SHA=$sha RUNNER_TEMP="$tmp" GITHUB_OUTPUT="$tmp/out" \
        bash -euo pipefail -c "$body" >/dev/null 2>&1)
      files="$(cat "$tmp"/changed* | tr '\n' ' ')"
      echo "base=${base:0:8} $f $mode: $(grep '^rtl=' "$tmp/out") files=[$files]"
    done
  done
done
