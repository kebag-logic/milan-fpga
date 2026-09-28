#!/usr/bin/env bash
# R392-3 reviewer-owned search of the merged tree for statements the TDM8
# first-light page could falsify. Usage: stale_statement_search.sh <repo>
# Scope: tracked files at HEAD outside docs/history, the page itself and the
# submodules. Each block prints every hit; the report classifies them.
set -u
REPO=${1:?repo}; cd "$REPO" || exit 2
X=(':!docs/history' ':!docs/findings/451_TDM8_FIRST_LIGHT.md' ':!protocol-processor' ':!gptp-processor' ':!external' ':!third_party')
gg(){ git grep -n -I "$@" 2>/dev/null | cut -c1-260; }
echo "== S1 issue/page references (#451 #448 #617 first light)"
gg -E '#451\b|issues/451\b|#448\b|issues/448\b|#617\b|first[- ]light' -- "${X[@]}"
echo "== S2 bench-link vocabulary (PocketBeagle, McASP, AM62, J11, USB Audio)"
gg -i -E 'pocketbeagle|mcasp|am62|\bj11\b|usb audio' -- '*.md' '*.yaml' "${X[@]}"
echo "== S3 TDM/DOUT/DIN/render with negative-proof wording (docs)"
gg -i -E '(tdm|dout|render lane|j11)' -- '*.md' "${X[@]}" | grep -i -E 'not (yet )?(clocked|tested|measured|verified|proven|exercised|observed|run|wired|connected|validated)|never|untested|unverified|unproven|no (bench|silicon|hardware|physical)|silent|not physical|capture, not|simulation only|sim-only|not on hardware'
echo "== S4 TDM near silicon/hardware/bench/physical (md, yaml, py, sh)"
gg -i -E 'tdm' -- '*.md' '*.yaml' '*.py' '*.sh' "${X[@]}" | grep -i -E 'silicon|hardware|bench|physical|wire[- ]to|first light|dout.*(silent|low|zero)'
echo "== S5 capture frame coherence / atomicity claims"
gg -i -E 'coheren|atomic|same (tdm )?frame|frame-wide|whole frame|torn' -- '*.md' "${X[@]}" | grep -i -E 'capture|tdm|pair|hold|crossbar|talker|chan_map'
echo "== S6 TDM junction slip semantics"
gg -i -E 'slip|junction' -- '*.md' "${X[@]}" | grep -i -E 'tdm|capture|pair|frame'
echo "== S7 frame-rate offset figures"
gg -E '10\.64|47,?999\.4|1\.958' -- '*.md' "${X[@]}"
echo "== S8 front-end member status table"
sed -n '/^## Members/,/^## AES3/p' hdl/ieee1722/aaf/doc/audio_frontend_family.md | grep -E 'tdm|i2s' | cut -c1-200
