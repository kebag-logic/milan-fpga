#!/bin/sh
# Disposable probe: plant one aecp_dispatch_mutations patch (or none) in a
# scratch export of the head, build the default bench, and run every section
# of the default build. Usage: probe_whole_default.sh REPO WORKDIR PATCH|none VERILATOR
set -eu
REPO="$1"; W="$2"; PATCH="$3"; V="$4"
rm -rf "$W"; mkdir -p "$W"
git -C "$REPO" archive 4a40b1798e463d09aafd74632408003229bcc673 | tar -x -C "$W"
if [ "$PATCH" != none ]; then
  (cd "$W" && git apply "tb/pp_top/aecp_dispatch_mutations/$PATCH.patch")
fi
make -C "$W/tb/pp_top" gsi-build VERILATOR="$V" > "$W/build.log" 2>&1
cd "$W/tb/pp_top" && ./obj_dir/Vpp_top_sim
