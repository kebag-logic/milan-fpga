#!/bin/sh
# Reviewer-owned sweep of the pinned processor tree (16be6768) for statements
# the accepted D3 contract supersedes, grouped by superseded contract, and the
# files with hits that have no row in D3 section 15.2.
# Run from the parent repository root (protocol-processor checked out at pin).
set -u
D3=docs/design/SAVED_STATE_MATERIALIZATION.md
PP=protocol-processor
awk '/^### 15\.2/{f=1;next} f&&/^## 16\./{exit} f' "$D3" | grep -E '^\| \[' | sed -E 's/^\| \[([^]]+)\].*/\1/' | sort -u > /tmp/r380_2_tbl_$$.txt
probe() {
  name=$1; pat=$2
  echo "## $name :: $pat"
  (cd "$PP" && grep -rn -I -i -E "$pat" docs hdl tb scripts README.md IEEE_1722_1_Hardware_Protocol_Processor.md \
      --include='*.md' --include='*.sv' --include='*.svh' --include='*.py' --include='*.svg' --include='*.drawio' 2>/dev/null) \
    | awk -F: '{print $1}' | sort | uniq -c | while read -r n f; do
        if grep -qx "$f" /tmp/r380_2_tbl_$$.txt; then t=ROW; else t=NO-ROW; fi
        printf '  %-6s %3s %s\n' "$t" "$n" "$f"
      done
}
probe A_pending_composition 'aecp_dyn_dirty_o|OR it with|dirty.{0,40}(pending|unflushed)'
probe B_groups67_owner 'groups? 6 (and|or) 7|Nothing in the processor|integrating platform|no record writer|record writer exists'
probe C_future_manager 'lands in P4|NVM-manager suite \(P4\)|second record writer|writer is not present|saved-state writer'
probe D_restore_verdicts 'restore_(done|fail|blank)_o'
probe E_boot_enable 'defaults.{0,40}then.{0,40}(release|enable)|releases? .?entity_enable|enable gated on'
probe F_retry 'RETRY_MAX_P|bounded (commit )?retr|retried'
probe G_marks_as_persistence 'persistence trigger|persist it|persist changed|COMMIT \+ NVM_MARK|NVM_MARK.{0,40}(dirty|persist)|marks? the .{0,30}persistence class dirty'
probe H_dyn_dirty_drives 'dirty.{0,60}NVM manager|drives the NVM|NVM manager.{0,60}dirty'
probe I_debounce 'T-NVM-DEBOUNCE|DEB_TICKS_P'
rm -f /tmp/r380_2_tbl_$$.txt
