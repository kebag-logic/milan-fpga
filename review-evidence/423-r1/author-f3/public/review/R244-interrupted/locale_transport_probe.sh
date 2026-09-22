#!/usr/bin/env bash
# R244 probe: does the shared Git transport stay byte-exact when Python's
# filesystem encoding is not UTF-8?  The head decodes Git output as
# UTF-8/surrogateescape, while subprocess encodes str argv with
# sys.getfilesystemencoding().  Under an ISO-8859-1 locale those differ for
# valid multi-byte UTF-8 path names.
#
# Usage: locale_transport_probe.sh <review-clone> <workdir> <receipt-dir>
# Builds two tiny fixture repositories, then runs the head checker
# (df53dfa1) and the base checker (52711029), both extracted by git archive,
# under the default UTF-8 locale and under a scratch-compiled ISO-8859-1
# locale.  Nothing in the review clone is modified.
set -u
CLONE=$1
W=$2
R=$3
HEAD_SHA=df53dfa116b34816db0193230ad9833e67bf46dd
BASE_SHA=52711029f374650dc93830d5ea28e81cb5c8f410
mkdir -p "$W" "$R"
rm -rf "$W/lp"
mkdir -p "$W/lp/head" "$W/lp/base" "$W/lp/locale"
git -C "$CLONE" archive "$HEAD_SHA" scripts | tar -x -C "$W/lp/head"
git -C "$CLONE" archive "$BASE_SHA" scripts | tar -x -C "$W/lp/base"
localedef -i en_US -f ISO-8859-1 "$W/lp/locale/en_US.ISO-8859-1" 2>"$W/lp/localedef.err"
echo "localedef rc=$?"

export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
export GIT_AUTHOR_NAME=Probe GIT_AUTHOR_EMAIL=probe@example.invalid
export GIT_COMMITTER_NAME=Probe GIT_COMMITTER_EMAIL=probe@example.invalid
t=1790000000
g() { t=$((t + 60)); GIT_AUTHOR_DATE="@$t +0000" GIT_COMMITTER_DATE="@$t +0000" git "$@"; }
NAME=$(printf '\303\251.txt')   # U+00E9 LATIN SMALL LETTER E WITH ACUTE, valid UTF-8

# Fixture L: a linear branch whose only change is to a non-ASCII path that the
# base never received.  Correct answer: STRANDED (1 commit, nothing landed).
L="$W/lp/linear"
mkdir -p "$L" && cd "$L" || exit 2
g init -q -b main
printf 'keep\n' > keep.txt
printf 'v0\n' > "$NAME"
g add -A && g commit -qm O
g checkout -qb pr
printf 'v1 stranded work\n' > "$NAME"
g add -A && g commit -qm 'stranded edit of a non-ASCII path'
g checkout -q main
printf 'keep later\n' > keep.txt
g add -A && g commit -qm 'unrelated base work'

# Fixture M: the #423 G1 shape.  A (non-ASCII path edit) is merged with
# --no-ff, C edits mod.txt; both are replayed exactly on main; the tip then
# REVERTS the non-ASCII edit and makes a far extension.  Correct answer at the
# head: UNKNOWN (retention unproved on the reverted path).  The base has no
# redundant-merge arm, so STRANDED is its correct existing answer.
M="$W/lp/merge"
mkdir -p "$M" && cd "$M" || exit 2
g init -q -b main
for i in $(seq -w 1 40); do echo "line $i"; done > mod.txt
printf 'v0\n' > "$NAME"
g add -A && g commit -qm O
O=$(git rev-parse HEAD)
g checkout -qb incoming
printf 'v1 source work\n' > "$NAME"
g add -A && g commit -qm 'A edits the non-ASCII path'
A=$(git rev-parse HEAD)
g checkout -qb pr "$O"
g merge -q --no-ff -m 'M redundant merge' incoming
sed -i 's/^line 20$/line 20 changed by C/' mod.txt
g add -A && g commit -qm 'C edits mod.txt'
C=$(git rev-parse HEAD)
g checkout -q main
g cherry-pick "$A" >/dev/null
g cherry-pick "$C" >/dev/null
printf 'v0\n' > "$NAME"
sed -i 's/^line 35$/line 35 later/' mod.txt
g add -A && g commit -qm 'tip reverts the non-ASCII edit and extends mod.txt'

run() {  # run <label> <checker-root> <fixture> <locale-mode>
  local label=$1 root=$2 fx=$3 mode=$4 out rc enc
  cd "$fx" || return
  if [ "$mode" = latin1 ]; then
    enc=$(LOCPATH="$W/lp/locale" LC_ALL=en_US.ISO-8859-1 python3 -B -c 'import sys; print(sys.getfilesystemencoding())')
    out=$(LOCPATH="$W/lp/locale" LC_ALL=en_US.ISO-8859-1 python3 -B "$root/scripts/check_merge_containment.py" --no-fetch --base main pr 2>&1)
    rc=$?
  else
    enc=$(python3 -B -c 'import sys; print(sys.getfilesystemencoding())')
    out=$(python3 -B "$root/scripts/check_merge_containment.py" --no-fetch --base main pr 2>&1)
    rc=$?
  fi
  printf '%s fs=%s rc=%s | %s\n' "$label" "$enc" "$rc" "$(printf '%s' "$out" | head -1 | sed 's/^ *//')"
}

{
  for fx in linear merge; do
    for mode in utf8 latin1; do
      run "$fx/$mode/head-df53dfa1" "$W/lp/head" "$W/lp/$fx" "$mode"
      run "$fx/$mode/base-52711029" "$W/lp/base" "$W/lp/$fx" "$mode"
    done
  done
} | tee "$R/locale_transport_probe.txt"
