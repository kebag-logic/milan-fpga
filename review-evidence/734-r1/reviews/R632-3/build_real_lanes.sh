#!/usr/bin/env bash
# Build REV-style lanes on top of real repository history in a disposable
# shared clone and write cases.json for probe_r632_3.py.
# Usage: build_real_lanes.sh <source-clone> <scratch-dir> <R> <current-dev> <pr-head>
set -euo pipefail
src="$1"; scratch="$2"; R="$3"; DEV="$4"; PRH="$5"
export HOME="$scratch/home" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@example.invalid GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@example.invalid
export GIT_AUTHOR_DATE=2001-01-01T00:00:00+0000 GIT_COMMITTER_DATE=2001-01-01T00:00:00+0000
mkdir -p "$HOME"; repo="$scratch/clone"
[ -d "$repo" ] || git clone --quiet --shared --no-checkout "$src" "$repo"
g() { git -C "$repo" "$@"; }
rtl=hdl/common/KL_link_guard.sv; other=hdl/common/axi_stream_if.sv; doc=docs/findings/README.md
edit() { g checkout --quiet --force --detach "$1"; printf '%s\n' "$3" >> "$repo/$2"; g add "$2"; g commit --quiet -m "$4"; g rev-parse HEAD; }
D=$(edit "$R" "$rtl" "// dev change D" "dev D edits RTL")
E=$(edit "$D" "$other" "// unrelated dev E" "dev E unrelated RTL")
L1=$(edit "$R" "$doc" "lane doc 1" "lane docs")
g checkout --quiet --force --detach "$L1"; g merge --quiet --no-ff --no-edit "$D"; L2=$(g rev-parse HEAD)
g checkout --quiet "$R" -- "$rtl"; g commit --quiet -m "restore RTL"; L3=$(g rev-parse HEAD)
L4=$(edit "$L3" "$doc" "lane doc 2" "lane docs 2")
# evil merge: merge D but keep R's RTL inside the merge commit itself
g checkout --quiet --force --detach "$L1"; g merge --quiet --no-ff --no-commit "$D" || true
g checkout --quiet "$R" -- "$rtl"; g commit --quiet -m "evil merge keeps old RTL"; EV=$(g rev-parse HEAD)
EV2=$(edit "$EV" "$doc" "lane doc 3" "lane docs 3")
# dev reverts D after the lane merged it; lane keeps D's content (landing changes nothing)
g checkout --quiet --force --detach "$E"; g revert --no-edit "$D" >/dev/null; DREV=$(g rev-parse HEAD)
# lane's own RTL change on stale base
OWN=$(edit "$R" "$other" "// lane own RTL" "lane own RTL")
OWN2=$(edit "$OWN" "$doc" "lane doc own" "lane docs after own RTL")
cat > "$scratch/cases.json" <<JSON
[
 {"label": "B16 actual landed merge 6c810c45", "live": "6c810c45^1", "head": "f1b2489f", "merge": "6c810c45ac4ac7d5b45797430753020c9ea31d86"},
 {"label": "B16 composed on recorded base 49da9fd9", "live": "49da9fd9", "head": "f1b2489f"},
 {"label": "B16 against current dev (already merged: empty)", "live": "$DEV", "head": "f1b2489f"},
 {"label": "this PR against live dev", "live": "$DEV", "head": "$PRH"},
 {"label": "REV real (live=D)", "live": "$D", "head": "$L4"},
 {"label": "REV+E real (live=E)", "live": "$E", "head": "$L4"},
 {"label": "evil merge restores RTL (live=E)", "live": "$E", "head": "$EV2"},
 {"label": "dev reverted D, lane kept D (landing changes nothing)", "live": "$DREV", "head": "$L2"},
 {"label": "own RTL on stale base then docs (live=E)", "live": "$E", "head": "$OWN2"},
 {"label": "docs-only on stale base (live=E)", "live": "$E", "head": "$L1"}
]
JSON
echo "D=$D E=$E L1=$L1 L2=$L2 L3=$L3 L4=$L4 EV=$EV EV2=$EV2 DREV=$DREV OWN=$OWN OWN2=$OWN2"
