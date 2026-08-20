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
#   deploy.sh build --dry-run                                (print, do not build)
#     BAUD=115200   console baud (our SoC default; the factory demo is 9600)
#     BIT=<path>    bitstream for `flash` (default: newest gateware/alinx_ax7101.bit)
#     LAYOUT=<path> flashboot_layout.json for `flash-images` (default: newest build's)
#     AEM/KERNEL/OPENSBI/DTB/ROOTFS=<path> manifest images for `flash-images` (only the images
#                   named in the layout's manifest are required; no machine-specific defaults)
#
#  load  = JTAG -> SRAM (volatile, fast; gone on power-cycle). Default; use for iteration.
#  flash = JTAG -> on-board QSPI flash (PERSISTENT bitstream at offset 0; the FPGA reloads it
#          on power-up when strapped for master-SPI boot, which the AX7101 is by default).
#          Writing flash does NOT reconfigure the running FPGA; power-cycle to boot from it.
#  flash-images = write the selected manifest into QSPI at the offsets compiled into
#          flashboot_layout.json. Linux images use LiteX FBI framing. The bare-metal AEM
#          image is raw because firmware verifies its generated length and CRC directly.
#
# NOTE: `build` needs Vivado with Artix-7 device support. `load`/`flash`/`flash-images`/
# `console` work against any built artifacts.
set -euo pipefail

HERE="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
STEP="${1:-all}"
DRY=0
if [ "${2:-}" = "--dry-run" ]; then
    [ "$STEP" = build ] || {
        echo "deploy: --dry-run is supported only with the build step" >&2
        exit 2
    }
    DRY=1
elif [ "$#" -gt 1 ]; then
    echo "usage: $0 [all|build|load|flash|flash-images|console] [--dry-run for build]" >&2
    exit 2
fi
BAUD="${BAUD:-115200}"
CABLE="${CABLE:-ft232}"       # FT232H JTAG on the AX7101
# TWO FTDI cables live on this bus since the Arty arrived (2026-07-11): always
# pin the cable by serial or a flash op can hit the WRONG BOARD. Default = the
# AX7101's cable; serials are bench-local (env SERIAL/AX_FTDI or
# sw/litex/boards.local.sh — gitignored; build.sh overrides per board).
[ -f "$HERE/boards.local.sh" ] && . "$HERE/boards.local.sh"
SERIAL="${SERIAL:-${AX_FTDI:-SET_AX_FTDI}}"
OFL="openFPGALoader --ftdi-serial $SERIAL"
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

# Current AX7101 shipping profile: one cacheless RV32I VexiiRiscv hart in
# machine mode, no MMU or Linux, and no Linux sound-card rings. The fabric,
# NIC DMA, protocol processor, physical TDM capture and render-free talker
# datapath remain present.
# --gtx-tx-invert is REQUIRED on this board: the GMII TX FFs are IOB-packed (deterministic
# skew ~0 vs the forwarded gtx_clk), so edge-aligned sampling is hold-marginal at the
# RTL8211E — measured 25-40 % corrupt frames edge-aligned vs 0 % with mid-bit sampling.
# Direct DMA remains enabled, but no cache-coherency hub is elaborated because
# the CPU itself is cacheless.
MILAN_OPTS="--board ax7101 --cpu vexiiriscv --cpu-count 1 --xlen 32 --software-profile baremetal --all-blocks --coherent-dma --milan-clk-freq 50e6 --with-spiflash --flashboot baremetal --gtx-tx-invert --timing-opt --floorplan --eth-port e1 --no-i2s-playback --no-render-lpf --audio-interface tdm8 --audio-interface-master --talker-wire-chans 8 --cbs-queues-mask 0x10 --loopback-lane --fabric-gptp --entity-gen-dir $HERE/../../configs/generated/endstation_ax7101_1x1_tdm8 --l2-bytes 0 --rx-queues 2 --strip-probes --hs-page-bytes 16384"
run_milan_soc() {
    local label="$1"; shift
    # MILAN_OPTS is a trusted, fixed launcher recipe. Deliberate word splitting
    # preserves the historical command while making dry-run and execution share
    # the exact same final argv.
    set -- "$HERE/milan_soc.py" $MILAN_OPTS "$@"
    if [ "$DRY" = 1 ]; then
        printf "DRY [%s]\n  " "$label"
        printf "%q " "$@"
        printf "\n"
    else
        "$@"
    fi
}
do_build() {
    echo "[deploy] build  (Vivado P&R -> .bit)"
    run_milan_soc "deploy build" --build --uart-baudrate "$BAUD"
}
do_load() {
    echo "[deploy] load   (JTAG -> SRAM, volatile)"
    run_milan_soc "deploy load" --load --uart-baudrate "$BAUD"
}
do_flash()  {
    [ -n "$BIT" ] && [ -f "$BIT" ] || { echo "[deploy] flash: no bitstream (set BIT=<path/to/alinx_ax7101.bit>)"; exit 2; }
    # The build's layout owns the bitstream budget. Fall back to the current
    # 4 MiB slot only when an older standalone bitstream has no layout JSON.
    local sz budget; sz=$(stat -c%s "$BIT"); budget=$((4*1024*1024))
    if [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ]; then
        budget=$("$PYTHON" - "$LAYOUT" <<'PY'
import json, sys
layout = json.load(open(sys.argv[1]))
row = next(image for image in layout["images"] if image["name"] == "bitstream")
print(int(row.get("budget") or row.get("size")))
PY
)
    fi
    [ "$sz" -le "$budget" ] || {
        echo "[deploy] flash REFUSED: bitstream $sz B exceeds the $budget B gateware slot."
        exit 2; }
    echo "[deploy] flash  (JTAG -> QSPI flash @0x0, PERSISTENT, $sz B): $BIT"
    $OFL -c "$CABLE" -f "$BIT"          # -f/--write-flash; add --reset to reboot from flash
}
do_flash_images() {
    [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ] || {
        echo "[deploy] flash-images: no flashboot_layout.json (build --with-spiflash, or set LAYOUT=<path>)"; exit 2; }
    # A device tree from an older CSR layout kills the whole host plane with
    # perfect CSR readbacks (kl-eth maps reg windows by index) — refuse it here
    # rather than debug it on silicon again. The OPENSBI check is the decisive
    # one: the BIOS jumps a1=0, so the fdt EMBEDDED in opensbi (FW_FDT_PATH) is
    # the only tree the kernel sees. Skipped only if dtc is unavailable.
    local csrcsv img; csrcsv="$(dirname "$LAYOUT")/csr.csv"
    if [ -f "$csrcsv" ] && command -v dtc >/dev/null; then
        for img in "${DTB:-}" "${OPENSBI:-}"; do
            [ -n "$img" ] || continue
            "$PYTHON" "$HERE/check_dtb_csr.py" "$img" "$csrcsv" || {
                echo "[deploy] flash-images REFUSED: $img does not match this build's csr.csv."
                echo "[deploy] Rebuild it from the dts source (opensbi embeds the fdt — rebuild it too)."; exit 2; }
        done
    fi
    echo "[deploy] flash-images  (JTAG -> QSPI flash): layout $LAYOUT"
    local tmp; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' RETURN
    # name<TAB>offset<TAB>ceiling for each manifest image. The ceiling is the
    # earliest of its declared budget, the next image/reservation, or 16 MiB.
    while IFS=$'\t' read -r name off ceil; do
        local src wrap=1
        case "$name" in
            bitstream)
                # gateware slot: flashed via `deploy.sh flash` (native -f, raw
                # config stream, NOT fbi-wrapped) — skip it here
                echo "[deploy]   bitstream slot @ 0x$(printf %06x "$off") (flash via 'deploy.sh flash')"; continue ;;
            kernel)
                src="${KERNEL:-}"
                # layout v3: the kernel slot expects the kernel build's
                # Image.xz (plain LZMA2; xz_embedded needs --check=crc32).
                # Given a raw Image, compress it here.
                if [ -n "$src" ] && [ -f "$src" ] &&                    [ "$(head -c6 "$src" | od -An -tx1 | tr -d ' \n')" != "fd377a585a00" ]; then
                    echo "[deploy]   kernel: raw Image -> xz -9 --check=crc32 (slot expects Image.xz)"
                    xz -9 --check=crc32 -T0 -c "$src" > "$tmp/Image.xz"
                    src="$tmp/Image.xz"
                fi ;;
            opensbi) src="${OPENSBI:-}" ;;
            dtb)     src="${DTB:-}" ;;
            rootfs)  src="${ROOTFS:-}" ;;
            aem)
                src="${AEM:-$(dirname "$LAYOUT")/aem_desc.bin}"
                wrap=0 ;;
            *) echo "[deploy]   unknown image '$name' in layout"; exit 2 ;;
        esac
        local ev="${name^^}"
        [ -n "$src" ] && [ -f "$src" ] || { echo "[deploy]   image '$name': set $ev=<path> (got '${src:-unset}')"; exit 2; }
        local fbi="$tmp/$name.fbi"
        if [ "$wrap" -eq 1 ]; then
            "$PYTHON" -m litex.soc.software.crcfbigen "$src" -f -l -o "$fbi"   # [length][crc32][data], LE header
        else
            # Bare-metal firmware knows the generated AEM length+CRC at compile
            # time and copies the descriptor image verbatim into its paired DRAM
            # window. An FBI header here would shift the required "AEMI" magic.
            cp "$src" "$fbi"
        fi
        local sz budget; sz=$(stat -c%s "$fbi"); budget=$((ceil - off))
        printf "[deploy]   %-8s %9d B  -> flash @ 0x%06x  (budget %d B, from %s)\n" "$name" "$sz" "$off" "$budget" "$src"
        [ "$sz" -le "$budget" ] || {
            echo "[deploy]   ERROR: '$name' ($sz B) exceeds its $budget B slot — slim it or move offsets (docs/integration/QSPI_FLASHBOOT.md)"; exit 2; }
        $OFL -c "$CABLE" --fpga-part "$FPGA_PART" -o "$off" --write-flash --file-type raw --verify "$fbi"
    done < <("$PYTHON" - "$LAYOUT" "$FLASH_SIZE" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); fs = int(sys.argv[2])
imgs = sorted(d["images"], key=lambda i: i["offset"])

# A ceiling is the next thing that must not be overwritten - which is NOT just
# the next boot image. The writable slots (journal, /user) live under a
# separate "reserved" key, so treating the last image's ceiling as end-of-flash
# let an oversized rootfs pass the budget check and silently erase saved
# bindings and fault logs on the next reflash. Every boundary counts.
res = d.get("reserved") or {}
res = list(res.values()) if isinstance(res, dict) else list(res)
bounds = sorted({int(i["offset"]) for i in imgs} |
                {int(r["offset"]) for r in res} | {fs})

for i in imgs:
    off = int(i["offset"])
    above = [b for b in bounds if b > off]
    top = min(above) if above else fs
    # Generators historically called the slot limit either budget or size.
    # Honour both; the current layout uses budget.
    declared = i.get("budget", i.get("size"))
    if declared is not None:
        top = min(top, off + int(declared))
    print("%s\t%d\t%d" % (i["name"], off, top))
PY
)
    echo "[deploy] flash-images done. Power-cycle for QSPI self-boot, or JTAG-load for iteration."
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
