#!/usr/bin/env bash
# Minimal repository with base-side rename cases for probe_r632_3.py.
# Usage: build_rename_cases.sh <shipping-tree> <empty-dir>
set -euo pipefail
ship="$1"; r="$2"; mkdir -p "$r/home"
export HOME="$r/home" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=p GIT_AUTHOR_EMAIL=p@x.invalid GIT_COMMITTER_NAME=p GIT_COMMITTER_EMAIL=p@x.invalid
export GIT_AUTHOR_DATE=2001-01-01T00:00:00+0000 GIT_COMMITTER_DATE=2001-01-01T00:00:00+0000
repo="$r/src"; mkdir -p "$repo"; g(){ git -C "$repo" "$@"; }
g init -q; mkdir -p "$repo/scripts" "$repo/docs" "$repo/hdl"
cp "$ship/scripts/ci_scope.py" "$ship/scripts/ci_scope_history.py" "$repo/scripts/"
printf 'line %s\n' $(seq 1 40) > "$repo/docs/page.md"
printf '// rtl line %s\n' $(seq 1 40) > "$repo/hdl/a.sv"
g add .; g commit -qm R; R=$(g rev-parse HEAD)
mkdir -p "$repo/docs/reference"; g mv docs/page.md docs/reference/REGISTER_MAP.md; g commit -qm "dev renames page into gate-read path"; L1=$(g rev-parse HEAD)
g checkout -q --detach $R; sed -i 's/line 20/line twenty/' "$repo/docs/page.md"; g commit -qam "PR edits page"; H1=$(g rev-parse HEAD)
g checkout -q --detach $R; g mv hdl/a.sv hdl/b.sv; g commit -qm "dev renames RTL"; L2=$(g rev-parse HEAD)
g checkout -q --detach $R; sed -i 's/rtl line 20/rtl line twenty/' "$repo/hdl/a.sv"; g commit -qam "PR edits old RTL path"; H2=$(g rev-parse HEAD)
g checkout -q --detach $R; g mv hdl/a.sv docs/a.md; g commit -qm "PR moves RTL file to docs"; H3=$(g rev-parse HEAD)
cat > "$r/cases.json" <<JSON
[{"label": "dev renames docs page into gate-read path, PR edits page", "live": "$L1", "head": "$H1"},
 {"label": "dev renames hdl/a.sv to hdl/b.sv, PR edits hdl/a.sv", "live": "$L2", "head": "$H2"},
 {"label": "PR renames RTL file into docs (deletion side)", "live": "$R", "head": "$H3"}]
JSON
