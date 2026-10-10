#!/usr/bin/env bash
# Copy a log into the packet with host-specific paths replaced by neutral placeholders.
# usage: CHECKOUT=... PACKET=... GTEST_PREFIX=... PINNED_VERILATOR=... sanitize.sh <in> <out>
set -u
sed -e "s#${PACKET}/scratch#<scratch>#g" -e "s#${PACKET}#<packet>#g" -e "s#${CHECKOUT}#<checkout>#g" \
    -e "s#${GTEST_PREFIX}#<gtest-1.14.0>#g" -e "s#$(dirname "$PINNED_VERILATOR")#<verilator-5.050>#g" \
    -e "s#${HOME}/br-milan-rv32#<rv32-sdk>#g" -e "s#${HOME}#<home>#g" "$1" > "$2"
