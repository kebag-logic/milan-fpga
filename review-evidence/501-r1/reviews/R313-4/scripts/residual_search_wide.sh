#!/usr/bin/env bash
# Reviewer probe (R313-4), supplementary to the unchanged residual_search.sh:
# wider wording for any page that ties the capture-hold measurement, the hold
# margin, or the firmware capture copy to the donor / processor lane or to a
# stage release condition.
# Usage: residual_search_wide.sh <tree-root>
set -u
cd "$1" || exit 2
echo "head=$(git rev-parse HEAD)"
echo "--- any capture-hold / hold-margin / capture-copy mention (all tracked md, txt, c, py)"
git grep -n -i -E 'capture[- ]hold|hold margin|capture copy|nvm_capture\(\) cop|copy time' -- '*.md' '*.txt' | cut -c1-240
echo "--- links into SNAPSHOT_OWNERSHIP section 20 / 18 from other pages"
git grep -n -E 'SAVED_STATE_SNAPSHOT_OWNERSHIP\.md#(20|18)' -- '*.md' | cut -c1-240
echo "--- processor 61/83 in any spelling, near measure/hold/capture"
git grep -n -i -E '(processor|donor)[^.]{0,80}(measur|capture[- ]hold|hold margin)|(measur|capture[- ]hold|hold margin)[^.]{0,80}(processor ?(issue )?#?(61|83)|donor)' -- '*.md' | cut -c1-240
echo "--- stage-3 release conditions"
git grep -n -i -E 'release (still )?requires|released after' -- docs/design/SAVED_STATE_MATERIALIZATION.md | cut -c1-240
exit 0
