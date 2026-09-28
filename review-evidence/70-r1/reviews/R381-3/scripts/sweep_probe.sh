#!/usr/bin/env bash
# Probe the D3 section 15.2 named sweep (extracted verbatim from the head) on
# synthetic wrapped statements. Usage: sweep_probe.sh <parent-clone> <scratch-dir>
set -u
C="$1"; S="$2"; HEAD=816c3b742940b9ac8d160ff03e05553a47e5e66d
PAT=$(git -C "$C" show "$HEAD:docs/design/SAVED_STATE_MATERIALIZATION.md" | grep -E "^rg -n -U -i -C 2 '" | sed -E "s/^rg -n -U -i -C 2 '(.*)' docs hdl tb$/\1/")
OLD='COMMIT.*NVM_MARK|aecp_dyn_dirty_o|nvm_unflushed_o|d3_unflushed_o|restore_(done|fail|blank)_o|T-NVM|RETRY_MAX_P|DEB_TICKS_P|entity_enable|Nothing in the processor|groups 6 and 7|integrating platform'
rm -rf "$S"; mkdir -p "$S"
w() { printf '%b' "$2" > "$S/$1"; }
w a_arb_slashslash.sv   '//  (manager 1, the saved-state writer of the integrating\n//  platform'"'"'s contract; tied idle until it lands)\n'
w b_arb_bang.sv         '  //! (manager 1, the saved-state writer of the integrating\n  //! platform'"'"'s contract)\n'
w c_top_plain.sv        '  //! nobody. Manager 1 is the platform'"'"'s saved-state writer;\n'
w d_top_wrap_bang.sv    '  //! nobody. Manager 1 is the platform'"'"'s\n  //! saved-state writer; until it lands here\n'
w e_md_wrap.md          'Manager 1 is the platform'"'"'s\nsaved-state writer.\n'
w f_rule_d_md.md        '- **(d)** NVM commits are asynchronous and never\n  delay responses.\n'
w g_rule_d_sv.sv        '//  NVM commits are asynchronous and never\n//  delay responses.\n'
w h_py_hash.py          '# commits are asynchronous to\n# protocol responses\n'
w i_mark_trigger.py     "    u('NVM_MARK', imm=7),   # naming persistence trigger\n"
echo "sweep pattern (verbatim from D3 at head)"
for f in $(ls "$S" | sort); do
  n=$(rg -c -U -i "$PAT" "$S/$f" 2>/dev/null || echo 0)
  o=$(rg -c -U -i "$OLD" "$S/$f" 2>/dev/null || echo 0)
  echo "$f | new sweep match lines: $n | round-2 sweep match lines: $o"
done
