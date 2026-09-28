#!/bin/sh
# R366-2 stale-document scan (read-only). Usage: stale_scan.sh <clone>
# Scans the committed HEAD tree outside docs/history and the submodules for
# any statement that a PHC-only step or re-base toggles mr or counts MEDIA_RESET.
cd "$1" || exit 2
X="-- :!docs/history :!protocol-processor :!gptp-processor :!third_party"
echo "## scan 1: round-1 verification pattern"
git grep -n -i -E "PHC step toggles|toggles \`?mr\`? once|counts that toggle in MEDIA_RESET" HEAD $X
echo "## scan 2: PHC/step/re-base/settime/adjtime near mr or MEDIA_RESET (same line)"
git grep -n -i -E "(phc|step|re-?base|settime|adjtime).{0,80}(\bmr\b|\`mr\`|media_reset|media reset)|(\bmr\b|\`mr\`|media_reset).{0,80}(phc step|a step|the step|re-?base|settime|adjtime)" HEAD $X ':!*.svh'
echo "## scan 3: step/re-base near toggle/restart"
git grep -n -i -E "(phc|gm|grandmaster)[ -]step.{0,100}(toggl|restart)|(toggl|restart).{0,100}(phc|gm|grandmaster)[ -]step|re-?base.{0,60}(toggles|restart request)" HEAD $X
echo "## scan 4: MEDIA_RESET with a PHC/step word within one line either side (docs, sw, scripts, avdecc)"
git grep -n -i -B1 -A1 "media_reset\|media reset" HEAD -- '*.md' 'sw/*' 'scripts/*' 'avdecc/*' ':!docs/history' | grep -i -E "step|re-?base|phc|settime|adjtime"
echo "## scan 5: the superseded tkdiag claim"
git grep -n "ORs both onto restart_p_i" HEAD
echo "scan5 rc=$? (1 = no hits)"
