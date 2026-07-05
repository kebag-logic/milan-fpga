#!/usr/bin/env bash
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Turnkey deploy for the Alinx AX7101: build the full Milan SoC bitstream, program it
# over JTAG, and open the console. Verified hardware wiring (identify by stable by-id;
# the /dev/ttyUSBn numbers flip on re-plug):
#   JTAG    = Digilent FT232H (0403:6014)  -> openFPGALoader -c ft232 (IDCODE = xc7a100t)
#   console = Silicon Labs CP2102N (10c4:ea60)
#
#   deploy.sh [all|build|load|flash|flash-images|console]     (default: all)
#     BAUD=115200   console baud (our SoC default; the factory demo is 9600)
#     BIT=<path>    bitstream for `flash` (default: newest gateware/alinx_ax7101.bit)
#     LAYOUT=<path> flashboot_layout.json for `flash-images` (default: newest build's)
#     KERNEL/OPENSBI/DTB/ROOTFS=<path>   boot images for `flash-images` (only the images
#                   named in the layout's manifest are required; no machine-specific defaults)
#
#  load  = JTAG -> SRAM (volatile, fast; gone on power-cycle). Default; use for iteration.
#  flash = JTAG -> on-board QSPI flash (PERSISTENT bitstream at offset 0; the FPGA reloads it
#          on power-up when strapped for master-SPI boot, which the AX7101 is by default).
#          Writing flash does NOT reconfigure the running FPGA; power-cycle to boot from it.
#  flash-images = write the Linux BOOT IMAGES into QSPI flash so the BIOS flash-boots them
#          instead of the ~4-min serial upload (needs a --with-spiflash bitstream + the BIOS
#          patch, sw/litex/patches). Each image is wrapped as a LiteX FBI (crcfbigen -f -l)
#          and written at the offset the gateware was compiled with (flashboot_layout.json).
#          The default "kernel" manifest flashes the 14 MB kernel at offset 0, so it and the
#          `flash` bitstream are mutually exclusive on the 16 MB flash — flash-boot builds are
#          JTAG-`load`ed, not flash-booted. See docs/QSPI_FLASHBOOT.md.
#
# NOTE: `build` needs Vivado with Artix-7 device support. `load`/`flash`/`flash-images`/
# `console` work against any built artifacts.
set -euo pipefail

HERE="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
STEP="${1:-all}"
BAUD="${BAUD:-115200}"
CABLE="${CABLE:-ft232}"       # FT232H JTAG on the AX7101
CONSOLE="$(ls /dev/serial/by-id/*CP2102* 2>/dev/null | head -1 || echo /dev/ttyUSB0)"
# newest built bitstream (override with BIT=...); `|| true` so an empty glob doesn't trip set -e
BIT="${BIT:-$(ls -t "$HERE"/*/gateware/alinx_ax7101.bit 2>/dev/null | head -1 || true)}"
# newest flash-boot layout (override with LAYOUT=...); Python with LiteX for crcfbigen
LAYOUT="${LAYOUT:-$(ls -t "$HERE"/*/flashboot_layout.json 2>/dev/null | head -1 || true)}"
PYTHON="${PYTHON:-python3}"
FLASH_SIZE=$((16*1024*1024))  # N25Q128 = 16 MB
# openFPGALoader needs the FPGA part to pick its JTAG→SPI proxy when writing a RAW file
# (a bitstream carries the part; raw data doesn't → "missing device-package information").
FPGA_PART="${FPGA_PART:-xc7a100tfgg484}"

# All fabric blocks (NIC+DMA+MAC+DDR3), datapath in its own 50 MHz domain so sys+DDR3
# close a clean 100 MHz (see docs/TROUBLESHOOTING.md §16); --timing-opt for margin.
# --gtx-tx-invert is REQUIRED on this board: the GMII TX FFs are IOB-packed (deterministic
# skew ~0 vs the forwarded gtx_clk), so edge-aligned sampling is hold-marginal at the
# RTL8211E — measured 25-40 % corrupt frames edge-aligned vs 0 % with mid-bit sampling.
# --coherent-dma is NOT implied by --all-blocks and is REQUIRED for a working NIC under
# Linux: without it the DMA masters bypass the NaxRiscv snooping dma_bus, so RX data is
# never CPU-visible (all-zero skbs -> stack drops every frame) and TX reads stale skb
# data (garbage dst MAC -> the peer NIC filters the frames; hardware-confirmed 2026-07-04).
MILAN_OPTS="--all-blocks --coherent-dma --milan-clk-freq 50e6 --gtx-tx-invert --timing-opt --l2-bytes 262144"
do_build()  { echo "[deploy] build  (Vivado P&R -> .bit)"; "$HERE/milan_soc.py" $MILAN_OPTS --build --uart-baudrate "$BAUD"; }
do_load()   { echo "[deploy] load   (JTAG -> SRAM, volatile)"; "$HERE/milan_soc.py" $MILAN_OPTS --load --uart-baudrate "$BAUD"; }
do_flash()  {
    [ -n "$BIT" ] && [ -f "$BIT" ] || { echo "[deploy] flash: no bitstream (set BIT=<path/to/alinx_ax7101.bit>)"; exit 2; }
    echo "[deploy] flash  (JTAG -> QSPI flash, PERSISTENT): $BIT"
    openFPGALoader -c "$CABLE" -f "$BIT"          # -f/--write-flash; add --reset to reboot from flash
}
do_flash_images() {
    [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ] || {
        echo "[deploy] flash-images: no flashboot_layout.json (build --with-spiflash, or set LAYOUT=<path>)"; exit 2; }
    echo "[deploy] flash-images  (JTAG -> QSPI flash): layout $LAYOUT"
    local tmp; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' RETURN
    # name<TAB>offset<TAB>ceiling  for each manifest image (ceiling = next offset or 16 MB)
    while IFS=$'\t' read -r name off ceil; do
        local src
        case "$name" in
            kernel)  src="${KERNEL:-}" ;;
            opensbi) src="${OPENSBI:-}" ;;
            dtb)     src="${DTB:-}" ;;
            rootfs)  src="${ROOTFS:-}" ;;
            *) echo "[deploy]   unknown image '$name' in layout"; exit 2 ;;
        esac
        local ev="${name^^}"
        [ -n "$src" ] && [ -f "$src" ] || { echo "[deploy]   image '$name': set $ev=<path> (got '${src:-unset}')"; exit 2; }
        local fbi="$tmp/$name.fbi"
        "$PYTHON" -m litex.soc.software.crcfbigen "$src" -f -l -o "$fbi"   # [length][crc32][data], LE header
        local sz budget; sz=$(stat -c%s "$fbi"); budget=$((ceil - off))
        printf "[deploy]   %-8s %9d B  -> flash @ 0x%06x  (budget %d B, from %s)\n" "$name" "$sz" "$off" "$budget" "$src"
        [ "$sz" -le "$budget" ] || {
            echo "[deploy]   ERROR: '$name' ($sz B) exceeds its $budget B slot — slim it or move offsets (docs/QSPI_FLASHBOOT.md)"; exit 2; }
        openFPGALoader -c "$CABLE" --fpga-part "$FPGA_PART" -o "$off" --write-flash --file-type raw --verify "$fbi"
    done < <("$PYTHON" - "$LAYOUT" "$FLASH_SIZE" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); fs = int(sys.argv[2])
imgs = sorted(d["images"], key=lambda i: i["offset"])
tops = [i["offset"] for i in imgs][1:] + [fs]
for i, top in zip(imgs, tops):
    print("%s\t%d\t%d" % (i["name"], i["offset"], top))
PY
)
    echo "[deploy] flash-images done. Reload the FPGA over JTAG ('deploy.sh load') and the BIOS will flash-boot."
}
do_console(){ echo "[deploy] console $CONSOLE @ $BAUD  (picocom; exit: Ctrl-a Ctrl-x)"; exec picocom -b "$BAUD" "$CONSOLE"; }

case "$STEP" in
    build)        do_build ;;
    load)         do_load ;;
    flash)        do_flash ;;
    flash-images) do_flash_images ;;
    console)      do_console ;;
    all)          do_build; do_load; do_console ;;
    *) echo "usage: $0 [all|build|load|flash|flash-images|console]"; exit 2 ;;
esac
