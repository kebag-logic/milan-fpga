#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Reviewer-owned firmware plant (R227-2, issue #504 / PR #521).
#
# Plants one hostile edit into a disposable shared clone's firmware, at the
# end of configure_fabric() (before the AEM decision), and runs the PR's
# compiled gate 1b on it. A sound gate must go RED (exit non-zero).
# PASSED = the gate accepted the plant.
#
# Usage: firmware_plant.sh <reviewed-clone> <sdk-prefix> <scratch> <receipts> <plant-id>...
set -euo pipefail
clone=$1 sdk=$2 scratch=$3 receipts=$4
shift 4
head=$(git -C "$clone" rev-parse HEAD)
for id in "$@"; do
  (
    work="$scratch/plant-$id"
    rm -rf "$work"
    git clone --quiet --shared --no-checkout "$clone" "$work"
    git -C "$work" checkout --quiet --detach "$head"
    for sub in third_party/verilog-axis protocol-processor gptp-processor; do
      git -C "$work" config "submodule.$sub.url" "$clone/.git/modules/$sub"
    done
    git -C "$work" -c protocol.file.allow=always submodule --quiet update --init \
      third_party/verilog-axis protocol-processor gptp-processor
    git -C "$work" submodule status third_party/verilog-axis protocol-processor gptp-processor \
      > "$work/.submodule-status"
    python3 - "$work/sw/firmware/milan_baremetal/milan_baremetal.c" "$id" <<'EOF'
import sys
from pathlib import Path
path, plant = Path(sys.argv[1]), sys.argv[2]
text = path.read_text()
types = ("typedef struct { volatile uint32_t ctrl; } *probe_r227_blk;\n"
         "static unsigned int probe_r227_page = 0x9000u;\n\n"
         "static int aem_loaded;")
bodies = {
    # a byte overwrite of a word slot at the slot's own offset
    "byte-overwrite": (
        "\t{\n\t\tunion { uint32_t w; uint8_t b; } milan_u;\n"
        "\t\tmilan_u.w = (probe_r227_page << 16) | MILAN_ADP_CTRL;\n"
        "\t\tmilan_u.b = 0u;\n"
        "\t\t((probe_r227_blk)milan_u.w)->ctrl = 1u;\n\t}\n"),
    # a half-word overwrite of a word slot at the slot's own offset
    "half-overwrite": (
        "\t{\n\t\tunion { uint32_t w; uint16_t h; } milan_u;\n"
        "\t\tmilan_u.w = (probe_r227_page << 16) | MILAN_ADP_CTRL;\n"
        "\t\tmilan_u.h = MILAN_ADP_CTRL;\n"
        "\t\t((probe_r227_blk)milan_u.w)->ctrl = 1u;\n\t}\n"),
    # a full-word overwrite through a pointer to the same frame slot
    "pointer-alias": (
        "\t{\n\t\tuint32_t milan_a = 0x80001000u;\n"
        "\t\tuint32_t *milan_pa = &milan_a;\n"
        "\t\t*milan_pa = (probe_r227_page << 16) | MILAN_ADP_CTRL;\n"
        "\t\t((probe_r227_blk)milan_a)->ctrl = 1u;\n\t}\n"),
    # the same overwrite spelled as a fixed-size builtin copy
    "memcpy-alias": (
        "\t{\n\t\tuint32_t milan_a = 0x80001000u;\n"
        "\t\tuint32_t milan_w = (probe_r227_page << 16) | MILAN_ADP_CTRL;\n"
        "\t\t__builtin_memcpy(&milan_a, &milan_w, sizeof milan_a);\n"
        "\t\t((probe_r227_blk)milan_a)->ctrl = 1u;\n\t}\n"),
    # a frame slot whose address escapes into an existing callee that
    # writes it (out of scope for #504; recorded for #408/#409)
    "call-escape": (
        "\t{\n\t\tuint64_t milan_v = 0u;\n"
        "\t\t(void)parse_u64(\"2415920640\", &milan_v);\n"
        "\t\t((probe_r227_blk)(uint32_t)milan_v)->ctrl = 1u;\n\t}\n"),
    # positive control: the same union with NO sub-word overwrite; the
    # resolver must refuse it on the resolved window address
    "no-overwrite": (
        "\t{\n\t\tunion { uint32_t w; uint8_t b; } milan_u;\n"
        "\t\tmilan_u.w = (probe_r227_page << 16) | MILAN_ADP_CTRL;\n"
        "\t\t((probe_r227_blk)milan_u.w)->ctrl = 1u;\n\t}\n"),
}
assert text.count("static int aem_loaded;") == 1
text = text.replace("static int aem_loaded;", types)
anchor = "static void configure_fabric(void)\n{"
start = text.index(anchor)
end = text.index("\n}\n", start)
text = text[:end] + "\n" + bodies[plant].rstrip("\n") + text[end:]
path.write_text(text)
EOF
    git -C "$work" diff -- sw/firmware > "$receipts/plant-$id.diff"
    set +e
    (cd "$work" && python3 -u sw/builder/test_firmware_compiler.py \
        --sdk-destination "$sdk" --audit "$work/argv.jsonl") \
        > "$receipts/plant-$id.log" 2>&1
    status=$?
    set -e
    verdict=PASSED
    [ "$status" -ne 0 ] && verdict=REFUSED
    echo "$verdict $id exit=$status" > "$receipts/plant-$id.verdict"
  ) &
done
wait
cat "$receipts"/plant-*.verdict
