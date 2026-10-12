#!/bin/sh
# probe_ci_events.sh REPO WORKDIR: plant one resolution defect per copy of the head tree and require ci_events.py --check to refuse it.
set -u
REPO=$1; W=$2; HEAD=27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c
rm -rf "$W"; mkdir -p "$W"
fresh() { rm -rf "$W/t"; mkdir -p "$W/t"; git -C "$REPO" archive "$HEAD" | tar -x -C "$W/t"; }
probe() { label=$1; shift
  fresh; python3 -I - "$W/t/.github/workflows/rtl-fast.yml" "$@" <<'PY'
import sys
path, old, new, count = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
text = open(path).read()
assert text.count(old) >= count, (old, text.count(old))
parts = text.split(old)
# replace only the count-th occurrence
text = old.join(parts[:count]) + new + old.join(parts[count:])
open(path, "w").write(text)
PY
  python3 -I "$W/t/scripts/ci_events.py" --check --root "$W/t" > "$W/out.txt" 2>&1; rc=$?
  verdict=$([ $rc -ne 0 ] && echo REFUSED || echo ESCAPED)
  echo "$verdict rc=$rc $label :: $(grep -m1 -iE 'FAIL|differs|must|missing' "$W/out.txt" | cut -c1-170)"
}
fresh; python3 -I "$W/t/scripts/ci_events.py" --check --root "$W/t" > "$W/out.txt" 2>&1; echo "control (unplanted copy) rc=$? $(tail -1 "$W/out.txt")"
FETCH="third_party/lwSRP third_party/tsn-c-stack"
probe "firmware-unit fetch without tsn-c-stack" "$FETCH" "third_party/lwSRP" 1
probe "firmware-control-mutants fetch without tsn-c-stack" "$FETCH" "third_party/lwSRP" 2
probe "firmware-aecp-mutants fetch without tsn-c-stack" "$FETCH" "third_party/lwSRP" 3
probe "firmware-srp-mutants fetch without tsn-c-stack" "$FETCH" "third_party/lwSRP" 4
probe "firmware-boundary fetch without tsn-c-stack" "$FETCH" "third_party/lwSRP" 5
probe "firmware-verilator fetch without tsn-c-stack" "$FETCH" "third_party/lwSRP" 6
probe "aggregate needs without firmware-boundary" "firmware-srp-mutants, firmware-boundary, firmware-verilator]" "firmware-srp-mutants, firmware-verilator]" 1
probe "aggregate needs without firmware-verilator" "firmware-boundary, firmware-verilator]" "firmware-boundary]" 1
probe "aggregate needs without firmware-srp-mutants" "firmware-aecp-mutants, firmware-srp-mutants," "firmware-aecp-mutants," 1
probe "aggregate loop without firmware-verilator" '"firmware-boundary:$FIRMWARE_BOUNDARY_RESULT" \
            "firmware-verilator:$FIRMWARE_VERILATOR_RESULT"; do' '"firmware-boundary:$FIRMWARE_BOUNDARY_RESULT"; do' 1
probe "aggregate env without FIRMWARE_BOUNDARY_RESULT" '          FIRMWARE_BOUNDARY_RESULT: ${{ needs.firmware-boundary.result }}
' '' 1
probe "control shard step doubled into aecp job (--shard 1/4 in aecp)" "--shard 2/4" "--shard 1/4" 1
probe "boundary step dropped --require-rv32" "ctrl_boundary.py --require-rv32 --selftest --without" "ctrl_boundary.py --selftest --without" 1
probe "verilator boundary step dropped --selftest" "--require-rv32 --selftest --only verilator" "--require-rv32 --only verilator" 1
probe "firmware-boundary timeout raised to 31" "    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - name: Fetch RTL dependencies
        run: git submodule update --init third_party/verilog-axis protocol-processor gptp-processor $FETCH

      - name: Install GoogleTest and GoogleMock and print the versions
        run: |
          set -euo pipefail
          sudo apt-get update -qq
          sudo apt-get install -y --no-install-recommends libgtest-dev libgmock-dev
          python3 -m pip install --quiet pyyaml
          dpkg-query -W libgtest-dev libgmock-dev
          g++ --version | head -n 1

      - name: Cache the pinned RV32 SDK" "    timeout-minutes: 31
    steps:
      - uses: actions/checkout@v4
      - name: Fetch RTL dependencies
        run: git submodule update --init third_party/verilog-axis protocol-processor gptp-processor $FETCH

      - name: Install GoogleTest and GoogleMock and print the versions
        run: |
          set -euo pipefail
          sudo apt-get update -qq
          sudo apt-get install -y --no-install-recommends libgtest-dev libgmock-dev
          python3 -m pip install --quiet pyyaml
          dpkg-query -W libgtest-dev libgmock-dev
          g++ --version | head -n 1

      - name: Cache the pinned RV32 SDK" 1
