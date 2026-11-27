#!/bin/bash
# units.sh <checkout> <work>: build and run unit_tests (and ctest) in every configuration, both profiles.
set -u
src=$1; work=$2
CG=$VALIDATION_STORAGE/977-a825/cgreen/prefix
export CMAKE_PREFIX_PATH=$CG LD_LIBRARY_PATH=$CG/lib
ES="-DLWSRP_ONE_PORT_MAP=1 -DLWSRP_LEAN_VALIDATE=1 -DLWSRP_RAPID_REPLACE=1 -DLWSRP_LEAN_COPY=1 -DLWSRP_LEAN_TX=1"
mkdir -p "$work"
status=0
while IFS='|' read -r name scale flags; do
  for milan in OFF ON; do
    b="$work/$name-milan$milan"
    cmake -S "$src" -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$milan -DLWSRP_SCALE=$scale \
      -DCMAKE_C_FLAGS="$flags" > "$b.configure.log" 2>&1 || { echo "$name milan $milan: configure FAIL"; status=1; continue; }
    cmake --build "$b" --parallel 4 > "$b.build.log" 2>&1 || { echo "$name milan $milan: build FAIL"; status=1; continue; }
    "$b/unit_tests" > "$b.unit.log" 2>&1; urc=$?
    ctest --test-dir "$b" --output-on-failure > "$b.ctest.log" 2>&1; crc=$?
    echo "$name milan $milan (scale $scale; flags '${flags}'): unit rc=$urc ctest rc=$crc; $(tail -n 1 "$b.unit.log")"
    [ $urc -eq 0 ] && [ $crc -eq 0 ] || status=1
  done
done <<EOF
default|OFF|
scale|ON|
end-station|ON|$ES
end-station-no-scale|OFF|$ES
one-port|OFF|-DLWSRP_ONE_PORT_MAP=1
lean-validate|OFF|-DLWSRP_LEAN_VALIDATE=1
rapid-replace|OFF|-DLWSRP_RAPID_REPLACE=1
lean-copy|OFF|-DLWSRP_LEAN_COPY=1
lean-tx|OFF|-DLWSRP_LEAN_TX=1
EOF
exit $status
