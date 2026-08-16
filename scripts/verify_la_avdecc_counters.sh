#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
fixture=${1:-"$repo_root/tb/verilator/milan_dp/reference/stream_output_counters_response.hex"}
la_commit=2fd57534ec7b32c66d9ada2c833e2c12dd5b95ea
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

frame="$fixture"
case "$fixture" in
    *.hex)
        frame="$work/response.bin"
        xxd -r -p "$fixture" "$frame"
        ;;
esac

if [[ -n ${LA_AVDECC_DIR:-} ]]; then
    la_src=$(realpath "$LA_AVDECC_DIR")
    actual=$(git -C "$la_src" rev-parse HEAD)
    if [[ $actual != "$la_commit" ]]; then
        echo "LA_AVDECC_DIR is at $actual, expected $la_commit" >&2
        exit 2
    fi
else
    la_src="$work/avdecc"
    git clone --quiet https://github.com/L-Acoustics/avdecc.git "$la_src"
    git -C "$la_src" checkout --quiet "$la_commit"
    git -C "$la_src" submodule update --init --recursive --quiet
fi

la_build="$work/build"
cmake -S "$la_src" -B "$la_build" -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_AVDECC_TESTS=OFF -DBUILD_AVDECC_CONTROLLER=OFF \
    -DBUILD_AVDECC_EXAMPLES=OFF -DBUILD_AVDECC_SWIG=OFF \
    -DBUILD_AVDECC_BINDINGS_C=OFF -DBUILD_C_BINDINGS=OFF \
    -DBUILD_NIH_TESTS=OFF -DBUILD_NIH_EXAMPLES=OFF \
    -DBUILD_NIH_SWIG=OFF >/dev/null
cmake --build "$la_build" --target la_avdecc_static --parallel >/dev/null

c++ -std=c++17 -O2 -DTARGET_SYSTEM_LINUX \
    -DHAVE_PROTOCOL_INTERFACE_SERIAL -DHAVE_PROTOCOL_INTERFACE_LOCAL \
    -DIGNORE_INVALID_CONTROL_DATA_LENGTH \
    -DIGNORE_INVALID_NON_SUCCESS_AEM_RESPONSES \
    -DALLOW_GET_AUDIO_MAP_UNSOL -DALLOW_RECV_BIG_AECP_PAYLOADS \
    -Dla_avdecc_static_STATICS -Dla_networkInterfaceHelper_static_STATICS \
    -I"$la_src/include" -I"$la_src/src" -I"$la_build/src" \
    -I"$la_src/externals/nih/include" \
    "$repo_root/scripts/la_avdecc_decode_counters.cpp" \
    -Wl,--start-group "$la_build/src/libla_avdecc_static.a" \
    "$la_build/externals/nih/src/libla_networkInterfaceHelper_static.a" \
    -Wl,--end-group -pthread -ldl -o "$work/decode-counters"

"$work/decode-counters" "$frame"
