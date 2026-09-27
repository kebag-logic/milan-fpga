#!/usr/bin/env bash
# Disposable composition probes on a scratch export of the candidate.
# Usage: probes.sh <pristine-candidate-export> <probe-tree> <receipt-dir>
# Each probe plants one edit, runs the gate expected to catch it, and restores
# the file; the restore is verified by SHA-256 against the pristine export.
set -u
src=$1
tree=$2
out=$3
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
rm -rf "$tree"
cp -a "$src" "$tree"
rm -rf "$tree/sw/builder/out"
# Gates list tracked files with `git ls-files`, so the scratch copy and its
# submodule directories become throwaway local repositories (never pushed).
for d in gptp-processor protocol-processor third_party/verilog-axis .; do
    git -C "$tree/$d" init -q
    git -C "$tree/$d" -c user.name=probe -c user.email=probe@invalid add -A 2>/dev/null
    git -C "$tree/$d" -c user.name=probe -c user.email=probe@invalid commit -qm probe
done
mkdir -p "$out/probe-logs"
summary="$out/probes-summary.tsv"
printf 'probe\texpect\trc\tverdict\trestored\tdescription\n' > "$summary"
# probe <id> <expect: fail|pass> <file> <python-edit> <description> -- <gate argv...>
probe() {
    local id=$1 expect=$2 file=$3 edit=$4 desc=$5
    shift 6
    local log="$out/probe-logs/$id.log" before after rc verdict
    before=$(sha256sum "$tree/$file" | cut -d' ' -f1)
    python3 - "$tree/$file" "$edit" <<'PY' > "$log" 2>&1
import sys
path, edit = sys.argv[1], sys.argv[2]
old, new = edit.split('=>', 1)
text = open(path, encoding='utf-8').read()
assert text.count(old) == 1, f'anchor count {text.count(old)}: {old!r}'
open(path, 'w', encoding='utf-8').write(text.replace(old, new))
print(f'planted in {path}: {old!r} -> {new!r}')
PY
    if [ $? -ne 0 ]; then
        printf '%s\t%s\t-\tPLANT-FAILED\t-\t%s\n' "$id" "$expect" "$desc" >> "$summary"
        return
    fi
    (cd "$tree" && printf '$ %s\n' "$*" && "$@") >> "$log" 2>&1
    rc=$?
    cp "$src/$file" "$tree/$file"
    after=$(sha256sum "$tree/$file" | cut -d' ' -f1)
    rm -rf "$tree/sw/builder/out"
    if [ "$expect" = fail ]; then
        [ "$rc" -ne 0 ] && verdict=KILLED || verdict=SURVIVED
    else
        [ "$rc" -eq 0 ] && verdict=PASS || verdict=UNEXPECTED-FAIL
    fi
    local restored=no
    [ "$after" = "$(sha256sum "$src/$file" | cut -d' ' -f1)" ] && restored=yes
    printf '%s\t%s\t%d\t%s\t%s\t%s\n' "$id" "$expect" "$rc" "$verdict" "$restored" "$desc" >> "$summary"
}
recipe=tb/verilator/nvm_capture_cpu/recipe.py
builder=sw/builder/endstation_builder.py
taps=docs/AAF_LATENCY_TAPS.md
cfg8=configs/endstation_ax7101_8x8.yaml
# Controls: unmodified candidate export passes the two composed gates.
probe C0 pass "$recipe" 'CPU_HZ = 50_000_000=>CPU_HZ = 50_000_000' \
    'control: unmodified clock-contract test' -- python3 sw/builder/test_clock_contract.py
probe C1 pass "$recipe" 'CPU_HZ = 50_000_000=>CPU_HZ = 50_000_000' \
    'control: unmodified capture receipt gate' -- python3 scripts/check_nvm_capture.py
probe C2 pass "$recipe" 'CPU_HZ = 50_000_000=>CPU_HZ = 50_000_000' \
    'control: unmodified entity-shape gate (#571 unit counts)' -- python3 scripts/check_entity_shape.py
# The single definition is live on the composed tree: moving it refuses every
# tracked configuration in the builder and breaks the #580 capture receipt.
probe P1 fail "$recipe" 'CPU_HZ = 50_000_000=>CPU_HZ = 100_000_000' \
    'recipe clock moved: builder refuses a tracked config' -- \
    python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml
probe P2 fail "$recipe" 'CPU_HZ = 50_000_000=>CPU_HZ = 100_000_000' \
    'recipe clock moved: #580 capture receipt refuses' -- python3 scripts/check_nvm_capture.py
# The builder guard coexists with #571 header emission and is still tested.
probe P3 fail "$builder" '        if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:=>        if False:' \
    'builder clock guard removed' -- python3 sw/builder/test_clock_contract.py
probe P4 pass "$builder" '        if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:=>        if False:' \
    'builder clock guard removed: #571 unit-count gate independent' -- python3 scripts/check_entity_shape.py
# The #571 emission is still checked on the composed tree with #582 present.
probe P5 fail "$builder" '    a(f"  localparam int AEM_N_CONTROL_C    = {int(dc['"'"'CONTROL'"'"'])};")=>    pass' \
    '#571 AEM_N_CONTROL_C emission removed' -- python3 scripts/check_entity_shape.py
probe P6 pass "$builder" '    a(f"  localparam int AEM_N_CONTROL_C    = {int(dc['"'"'CONTROL'"'"'])};")=>    pass' \
    '#571 emission removed: #582 clock contract independent' -- python3 sw/builder/test_clock_contract.py
# A divergent configured clock is refused and the receipt census notices.
probe P7 fail "$cfg8" '    milan_clk_hz: 50000000 =>    milan_clk_hz: 100000000 ' \
    '8x8 declares 100 MHz: builder refuses' -- \
    python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml
probe P8 fail "$cfg8" '    milan_clk_hz: 50000000 =>    milan_clk_hz: 100000000 ' \
    '8x8 declares 100 MHz: capture receipt refuses' -- python3 scripts/check_nvm_capture.py
# The tap table remains checked against configurations.
probe P9 fail "$taps" '| `endstation_ax7101_8x8` | 50000000 | 20 | pruned |=>| `endstation_ax7101_8x8` | 50000000 | 20 | present |' \
    'tap presence row altered' -- python3 sw/builder/test_clock_contract.py
probe P10 fail "$taps" '| `endstation_ax7101_1x1_tdm8` | 50000000 | 20 | present |=>| `endstation_ax7101_1x1_tdm8` | 100000000 | 10 | present |' \
    'tap clock row restated at 100 MHz' -- python3 sw/builder/test_clock_contract.py
