#!/usr/bin/env bash
# Disposable probes: the byte-identity check and the link checker must reject licence regressions.
# Works on an exported copy of the head tree; never touches the checkout.
# Usage: licence_probes.sh <checkout> <canonical-text> <scratch-dir>
set -u
SRC=${1:?checkout}
CANON=${2:?canonical text}
WORK=${3:?scratch dir}
rm -rf "$WORK"
mkdir -p "$WORK/tree"
git -C "$SRC" archive f800a2bb920c543934d6286a47fe20dde3efa2c5 | tar -x -C "$WORK/tree"
echo "canonical_sha256=$(sha256sum < "$CANON" | cut -d' ' -f1) canonical_blob=$(git hash-object --no-filters "$CANON")"
echo "head_blob=$(git -C "$SRC" rev-parse f800a2bb920c543934d6286a47fe20dde3efa2c5:LICENSE)"
echo "gitattributes_files=$(git -C "$SRC" ls-files '*.gitattributes' | wc -l)"

probe() {
    local name=$1 expect=$2 file=$3
    cmp -s "$file" "$CANON"; local rc=$?
    local verdict=FAIL
    { [ "$expect" = same ] && [ $rc -eq 0 ]; } || { [ "$expect" = differ ] && [ $rc -ne 0 ]; } && verdict=PASS
    echo "PROBE cmp $name expect=$expect cmp_rc=$rc $verdict"
}

probe head same "$WORK/tree/LICENSE"
git -C "$SRC" show a4cbe41de1c80d43f26e0d348cbdb45075273a4f:LICENSE > "$WORK/base-LICENSE"
probe base-with-spdx differ "$WORK/base-LICENSE"
{ printf 'SPDX-License-Identifier: Apache-2.0\n'; cat "$CANON"; } > "$WORK/spdx-only"
probe spdx-line-only differ "$WORK/spdx-only"
head -c -1 "$CANON" > "$WORK/no-final-newline"
probe no-final-newline differ "$WORK/no-final-newline"
sed 's/$/\r/' "$CANON" > "$WORK/crlf"
probe crlf differ "$WORK/crlf"
sed 's/\[yyyy\]/2026/' "$CANON" > "$WORK/filled-appendix"
probe filled-appendix differ "$WORK/filled-appendix"

cd "$WORK/tree" || exit 2
python3 doc/tools/check_links.py --local-only > "$WORK/links-control.log" 2>&1
echo "PROBE links-local control rc=$? $(tail -n 1 "$WORK/links-control.log")"
mv LICENSE LICENSE.moved
python3 doc/tools/check_links.py --local-only > "$WORK/links-missing.log" 2>&1
rc=$?
echo "PROBE links-local LICENSE-removed rc=$rc $(grep -c 'LICENSE' "$WORK/links-missing.log") LICENSE-lines; $(tail -n 1 "$WORK/links-missing.log")"
[ $rc -ne 0 ] && echo "PROBE links-local LICENSE-removed PASS (checker rejects missing licence)" || echo "PROBE links-local LICENSE-removed FAIL"
mv LICENSE.moved LICENSE
