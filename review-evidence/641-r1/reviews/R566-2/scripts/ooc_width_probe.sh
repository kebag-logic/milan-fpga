#!/usr/bin/env bash
# Probe the documented example: OOC_CHPARAM TDATA_WIDTH=52 must fail and 64 must
# pass in syn/yosys/ooc.sh rx_mac_filter, under each converter version.
# ooc.sh prepends "$HOME/.local/bin" to PATH, so each run gets a disposable HOME
# whose .local/bin holds only the converter under test; the version ooc.sh
# actually resolved is printed from inside that environment.
# Also shows how each converter lowers the module's elaboration guard.
# Args: <sv2v-0.0.12 bin dir> <sv2v-0.0.13 bin dir> <work dir>
set -u
S12=$1; S13=$2; W=$3
mkdir -p "$W"
export PYTHONDONTWRITEBYTECODE=1
for pair in "0.0.12:$S12" "0.0.13:$S13"; do
  label=${pair%%:*}; bin=${pair#*:}
  home="$W/home.$label"; rm -rf "$home"; mkdir -p "$home/.local/bin"
  cp "$bin/sv2v" "$home/.local/bin/sv2v"
  echo "=== converter $label: resolved as $(HOME=$home PATH="$home/.local/bin:$PATH" sv2v --version)"
  "$home/.local/bin/sv2v" hdl/ieee8021q/filtering/rx_mac_filter.sv > "$W/rx_mac_filter.$label.v" 2>"$W/sv2v.$label.err"
  echo "sv2v rc=$?"
  echo "-- guard lowering (lines naming error/display/fatal):"
  grep -n -E '\$error|\$fatal|\$display' "$W/rx_mac_filter.$label.v" | cut -c1-140
  for width in 52 64; do
    rm -rf "$W/ooc.$label.$width"
    out=$(HOME="$home" OOC_TMP="$W/ooc.$label.$width" OOC_CHPARAM="TDATA_WIDTH=$width" \
          syn/yosys/ooc.sh rx_mac_filter 2>&1)
    rc=$?
    echo "-- ooc.sh rx_mac_filter TDATA_WIDTH=$width rc=$rc"
    printf '%s\n' "$out" | grep -E 'sv2v|rx_mac_filter|ERROR|FAIL|PASS' | cut -c1-200 | head -8
  done
done
