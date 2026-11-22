#!/bin/sh
# census_gptp_adj.sh CLONE REV...: live (non-// comment) references to gptp_adj_w in milan_datapath.sv per revision,
# against test_builder.py's reference census figure, and the gate 1c text the builder asserts absent from milan_soc.py
set -eu
C=$1; shift
cd "$C"
echo "test_builder.py pins: $(grep -n '"gptp_adj_w": ' sw/builder/test_builder.py | head -1)"
for r in "$@"; do
  n=$(git show "$r:hdl/milan/milan_datapath.sv" | sed 's#//.*##' | grep -ow 'gptp_adj_w' | wc -l)
  s=$(git show "$r:sw/litex/milan_soc.py" | grep -c 'self._gptp_owner = "software"' || true)
  echo "$r: gptp_adj_w live references $n; milan_soc.py 'self._gptp_owner = \"software\"' occurrences $s"
done
git show "${1}:hdl/milan/milan_datapath.sv" >/dev/null
