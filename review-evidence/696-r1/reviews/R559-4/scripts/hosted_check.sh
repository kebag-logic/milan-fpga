#!/bin/sh
# Usage: hosted_check.sh <outdir> <scratchdir>   (read-only GitHub API queries)
set -u
O=$1; S=$2; R=kebag-logic/milan-fpga; RUN=38034648698; mkdir -p "$S"
{
echo "## runs at head 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f"
gh run list -R $R --commit 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f --json databaseId,name,status,conclusion,event --jq '.[]|[.databaseId,.name,.event,.status,.conclusion]|@tsv'
echo "## rtl-full run $RUN jobs"
gh run view $RUN -R $R --json headSha,status,conclusion,jobs --jq '"headSha=\(.headSha) status=\(.status) conclusion=\(.conclusion)", (.jobs[]|[.databaseId,.name,.status,.conclusion,.startedAt,.completedAt]|@tsv)'
echo "## merge ref tested (suite-logs TARGET_SHA) and its parents"
gh api repos/$R/commits/1ab24ec34c905d3c1f18076ce1a5b3138a49c62a --jq '[.sha,(.parents|map(.sha)|join(" ")),.commit.message]|@tsv'
} > "$O/hosted-status.tsv" 2>&1
id=$(gh api repos/$R/actions/runs/$RUN/artifacts --jq '.artifacts[]|select(.name=="suite-logs-1")|.id')
gh api repos/$R/actions/artifacts/$id/zip > "$S/sl1.zip"; rm -rf "$S/sl1"; mkdir -p "$S/sl1"; (cd "$S/sl1" && unzip -o -q ../sl1.zip)
{
echo "suite-logs-1 artifact id=$id zip sha256=$(sha256sum "$S/sl1.zip" | cut -d' ' -f1)"
echo "TARGET_SHA=$(cat "$S/sl1/TARGET_SHA")  maap.log sha256=$(sha256sum "$S/sl1/maap.log" | cut -d' ' -f1)"
grep -nE "KL_maap: [0-9]+ checks|maap mutants: checks|ESCAPED|non-files|m[345]_datapath|m4_reset" "$S/sl1/maap.log"
echo "[ok] rows: $(grep -c '^\[ok\]' "$S/sl1/maap.log")"
} > "$O/hosted-shard1-maap-excerpt.log" 2>&1
