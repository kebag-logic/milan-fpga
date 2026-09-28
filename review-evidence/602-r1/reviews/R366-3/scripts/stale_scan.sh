#!/bin/sh
# R366-3 stale-document scan (round-2 scans 1-5 plus expression-level scans 6-9) (read-only). Usage: stale_scan.sh <clone>
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
echo "## scan 6: media_rebase_p_w and mcr_restart_p_w on one line (any order)"
git grep -n -E "media_rebase_p_w.{0,160}mcr_restart_p_w|mcr_restart_p_w.{0,160}media_rebase_p_w" HEAD $X
echo "## scan 7: the old census wording (three references / two readers / ungated step)"
git grep -n -i -E "media_rebase_p_w\`? has exactly three|two readers|step is ungated by clock selection|crf_mr_toggle_p_w\)\)? *\\\\?\| *media_rebase_p_w" HEAD $X
echo "## scan 8: restart request / restart_p_i with PHC, step or re-base on one line"
git grep -n -i -E "(restart_p_i|restart request|restart cause).{0,100}(phc|re-?base|settime|adjtime|step)|(phc|re-?base|settime|adjtime|step).{0,100}(restart_p_i|restart request|restart cause)" HEAD $X
echo "## scan 9: 'media re-base' / 'PHC step' near 'MEDIA_RESET' or 'mr' within three lines (markdown only)"
git grep -n -i -A3 -E "media re-?base|phc step|phc-only" HEAD -- '*.md' ':!docs/history' | grep -i -E "\bmr\b|\`mr\`|media_reset" 
