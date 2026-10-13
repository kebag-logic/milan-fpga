#!/usr/bin/env bash
# Rebuild the five linked control images at base a0f39ad4 and at this head with
# the pinned SDK, inside a network-less bubblewrap boundary (candidate read-only).
# Usage: run_images.sh <full-clone-at-head> <writable-dir-holding-sdk.tar.xz> <log> <rcfile>
set -u
REPO="$1"; W="$2"; log="$3"; rcf="$4"
bwrap --unshare-all --die-with-parent --new-session --ro-bind / / --dev /dev --proc /proc \
  --tmpfs /tmp --tmpfs /home --tmpfs /run --bind "$W" /tmp/work --ro-bind "$REPO" /tmp/candidate \
  --setenv HOME /tmp/home --setenv TMPDIR /tmp --setenv PYTHONDONTWRITEBYTECODE 1 \
  bash -euc 'mkdir -p /tmp/home; rm -rf /tmp/work/tree /tmp/work/sdk /tmp/work/build
    git clone --quiet --shared /tmp/candidate /tmp/work/tree
    git -C /tmp/work/tree -c protocol.file.allow=always -c submodule.protocol-processor.url=/tmp/candidate/protocol-processor -c submodule.gptp-processor.url=/tmp/candidate/gptp-processor -c submodule.third_party/verilog-axis.url=/tmp/candidate/third_party/verilog-axis submodule update --quiet --init protocol-processor gptp-processor third_party/verilog-axis
    echo "tree head: $(git -C /tmp/work/tree rev-parse HEAD)"
    python3 /tmp/work/tree/scripts/ci_rv32_sdk.py --archive /tmp/work/sdk.tar.xz --destination /tmp/work/sdk
    export MILAN_RV32_CC=/tmp/work/sdk/bin/riscv32-linux-gcc; cd /tmp/work/tree
    python3 sw/firmware/ctrl/test/ctrl_image.py --shape endstation_arty_4x4 --shape endstation_arty_8ch --shape endstation_arty_current --shape endstation_ax7101_1x1_tdm8 --shape endstation_ax7101_8x8 --base a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0 --out /tmp/work/build' > "$log" 2>&1
echo $? > "$rcf"
