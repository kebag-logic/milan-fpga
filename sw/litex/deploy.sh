#!/usr/bin/env bash
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# Turnkey deploy for the Alinx AX7101: build the full Milan SoC bitstream, program it
# over JTAG, and open the console. Verified hardware wiring (identify by stable by-id;
# the /dev/ttyUSBn numbers flip on re-plug):
#   JTAG    = Digilent FT232H (0403:6014)  -> openFPGALoader -c ft232 (IDCODE = xc7a100t)
#   console = Silicon Labs CP2102N (10c4:ea60)
#
#   deploy.sh [all|build|load|flash-pair|check-images|flash|flash-images|console]
#             (default: all)
#   deploy.sh build --dry-run                                (print, do not build)
#     BAUD=115200   console baud (our SoC default; the factory demo is 9600)
#     BIT=<path>    bitstream for `flash-pair` (required there; other steps default
#                   to the newest gateware/alinx_ax7101.bit)
#     LAYOUT=<path> target flashboot_layout.json (required for flash-pair; other
#                   steps default to the newest build's)
#     AEM/KERNEL/OPENSBI/DTB/ROOTFS=<path> target manifest images (only the images
#                   named in the layout's manifest are required; no machine-specific defaults)
#     EXPECTED_GPTP_OWNER=fabric|software|none additionally binds a named build
#                   recipe to the owner compiled into LAYOUT (used by build.sh).
#     INSTALLED_LAYOUT=<path> + INSTALLED_BIT=<path> name the exact build
#                   currently in QSPI. flash-pair proves that claim by live
#                   offset-zero readback before choosing its write order.
#
#  load  = JTAG -> SRAM (volatile, fast; gone on power-cycle). Default; use for iteration.
#  flash-pair = the persistent entry point. It proves the installed bitstream,
#          prepares the whole target set, then orders verified writes so every
#          completed write prefix retains exactly one bootable gPTP owner.
#  flash / flash-images = deliberately refused unless ALLOW_NONATOMIC_FLASH=1;
#          they are recovery/bring-up primitives without the flash-pair guarantee.
#
# NOTE: `build` needs Vivado with Artix-7 device support. `load`/`flash-pair`/
# `check-images`/`console` work against built artifacts without Vivado.
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
    echo "usage: $0 [all|build|load|flash-pair|check-images|flash|flash-images|console] [--dry-run for build]" >&2
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
# Remember whether persistent target evidence was supplied explicitly before
# applying the iteration/recovery defaults below.  A transaction may never
# select its target from directory mtimes.
BIT_EXPLICIT="${BIT+x}"
LAYOUT_EXPLICIT="${LAYOUT+x}"
# newest built bitstream (override with BIT=...); `|| true` so an empty glob doesn't trip set -e
BIT="${BIT:-$(ls -t "$HERE"/*/gateware/alinx_ax7101.bit 2>/dev/null | head -1 || true)}"
# newest flash-boot layout (override with LAYOUT=...); Python with LiteX for crcfbigen
LAYOUT="${LAYOUT:-$(ls -t "$HERE"/*/flashboot_layout.json 2>/dev/null | head -1 || true)}"
INSTALLED_BIT="${INSTALLED_BIT:-}"
INSTALLED_LAYOUT="${INSTALLED_LAYOUT:-}"
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
do_check_images() {
    [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ] || {
        echo "[deploy] image check: no flashboot_layout.json (build --with-spiflash, or set LAYOUT=<path>)"; exit 2; }
    # #116 owner contract: inspect the ACTUAL rootfs archive against the owner
    # enum compiled into this gateware.  Missing/legacy metadata, unreadable
    # archives and either inverted marker state are hard errors. flash-pair
    # runs this while materializing the whole set, before its first write.
    local pair_args=(--layout "$LAYOUT")
    [ -z "${ROOTFS:-}" ] || pair_args+=(--rootfs "$ROOTFS")
    [ -z "${EXPECTED_GPTP_OWNER:-}" ] || \
        pair_args+=(--expected-owner "$EXPECTED_GPTP_OWNER")
    "$PYTHON" "$HERE/check_gptp_owner_pair.py" "${pair_args[@]}" || {
        echo "[deploy] image check REFUSED: gateware/rootfs gPTP owners do not form one-owner image." >&2
        exit 2
    }
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
    echo "[deploy] image preflight OK: $LAYOUT"
}

run_ofl() {
    local output
    if ! output=$($OFL "$@" 2>&1); then
        echo "$output" >&2
        return 1
    fi
    echo "$output"
    if echo "$output" | grep -qiE "error|can.t program"; then
        echo "[deploy] programmer reported failure despite a zero exit status" >&2
        return 1
    fi
}

prepare_images() {
    # Materialize and size-check EVERY non-bit target before a single QSPI
    # write. A missing/oversized last image must not strand a partially updated
    # set merely because the old implementation discovered it inside its write
    # loop.
    local tmp="$1" rows="$2" manifest_rows
    manifest_rows="$tmp/layout-rows.tsv"
    : > "$rows"
    do_check_images
    # name<TAB>offset<TAB>ceiling for each manifest image. The ceiling is the
    # earliest of its declared budget, the next image/reservation, or 16 MiB.
    # Materialize this list synchronously: a failing process substitution is
    # otherwise invisible to the while-loop status and could look like an
    # empty, successfully prepared image set.
    "$PYTHON" - "$LAYOUT" "$FLASH_SIZE" > "$manifest_rows" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); fs = int(sys.argv[2])
imgs = d["images"]
res = d.get("reserved") or {}
res = list(res.values()) if isinstance(res, dict) else list(res)

def checked_offset(row, label, allow_end=False):
    if not isinstance(row, dict) or type(row.get("offset")) is not int:
        raise SystemExit(f"{label} needs an integer offset")
    off = row["offset"]
    top = fs if allow_end else fs - 1
    if off < 0 or off > top:
        raise SystemExit(f"{label} offset {off} is outside the QSPI device")
    return off

offsets = [checked_offset(row, f"image {row.get('name')!r}") for row in imgs]
if len(offsets) != len(set(offsets)):
    raise SystemExit("image offsets must be unique")
reserved_offsets = [checked_offset(row, "reserved region", allow_end=True)
                    for row in res]
if len(reserved_offsets) != len(set(reserved_offsets)):
    raise SystemExit("reserved region offsets must be unique")
collisions = sorted(set(offsets) & set(reserved_offsets))
if collisions:
    raise SystemExit(
        "image and reserved region share offset(s): " +
        ", ".join(str(offset) for offset in collisions))
bounds = sorted(set(offsets) | set(reserved_offsets) | {fs})

for row, off in sorted(zip(imgs, offsets), key=lambda pair: pair[1]):
    above = [bound for bound in bounds if bound > off]
    if not above:
        raise SystemExit(f"image {row.get('name')!r} has no upper boundary")
    top = min(above)
    declared = row.get("budget", row.get("size"))
    if declared is not None:
        if type(declared) is not int or declared <= 0:
            raise SystemExit(
                f"image {row.get('name')!r} needs a positive integer budget")
        top = min(top, off + declared)
    if top <= off:
        raise SystemExit(f"image {row.get('name')!r} has an empty slot")
    print("%s\t%d\t%d" % (row["name"], off, top))
PY
    while IFS=$'\t' read -r name off ceil; do
        local src wrap=1
        case "$name" in
            bitstream)
                # Native Xilinx configuration stream, not FBI-wrapped. The
                # transition planner validates its offset/budget separately.
                echo "[deploy]   bitstream slot @ 0x$(printf %06x "$off")"
                continue ;;
            kernel)
                src="${KERNEL:-}"
                # layout v3: the kernel slot expects the kernel build's
                # Image.xz (plain LZMA2; xz_embedded needs --check=crc32).
                # Given a raw Image, compress it here.
                if [ -n "$src" ] && [ -f "$src" ] && \
                        [ "$(head -c6 "$src" | od -An -tx1 | tr -d ' \n')" != "fd377a585a00" ]; then
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
            *) echo "[deploy]   unknown image '$name' in layout"; return 2 ;;
        esac
        local ev="${name^^}"
        [ -n "$src" ] && [ -f "$src" ] || {
            echo "[deploy]   image '$name': set $ev=<path> (got '${src:-unset}')"
            return 2; }
        case "$src" in *$'\t'*|*$'\n'*)
            echo "[deploy]   image '$name': path contains a tab/newline" >&2
            return 2;;
        esac
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
            echo "[deploy]   ERROR: '$name' ($sz B) exceeds its $budget B slot — slim it or move offsets (docs/integration/QSPI_FLASHBOOT.md)"
            return 2; }
        printf '%s\t%s\t%s\n' "$name" "$off" "$fbi" >> "$rows"
    done < "$manifest_rows"
    echo "[deploy] complete target image set prepared before programmer writes"
}

write_prepared_images() {
    local rows="$1" name off image
    while IFS=$'\t' read -r name off image; do
        echo "[deploy] write+verify $name @ 0x$(printf %06x "$off")"
        run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o "$off" \
            --write-flash --file-type raw --verify "$image"
    done < "$rows"
}

prepared_images_match() {
    local rows="$1" scratch="$2" name off image size
    while IFS=$'\t' read -r name off image; do
        size=$(stat -c%s "$image")
        run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o "$off" \
            --dump-flash --file-size "$size" "$scratch" || return 1
        if ! cmp -s "$image" "$scratch"; then
            echo "[deploy] target image readback mismatch: $name @ 0x$(printf %06x "$off")" >&2
            return 1
        fi
    done < "$rows"
}

prove_live_installed_rootfs() {
    # A live software/full or fabric/full bit is not by itself one-owner
    # evidence: the persistent rootfs marker is the other half of that state.
    # Read the FBI header first, bound its declared payload to the installed
    # layout slot, then CRC/decompress/inspect the exact live record.
    local tmp="$1" source_owner="$2"
    local slot="$tmp/installed-rootfs-slot.tsv"
    local header="$tmp/installed-rootfs-header.bin"
    local live_rootfs="$tmp/installed-rootfs.fbi"
    "$PYTHON" - "$INSTALLED_LAYOUT" "$FLASH_SIZE" > "$slot" <<'PY'
import json, sys
layout = json.load(open(sys.argv[1]))
flash_size = int(sys.argv[2])
rows = [row for row in layout.get("images", [])
        if isinstance(row, dict) and row.get("name") == "rootfs"]
if len(rows) != 1:
    raise SystemExit("installed full-Linux layout needs exactly one rootfs row")
row = rows[0]
off = row.get("offset")
budget = row.get("budget", row.get("size"))
if type(off) is not int or type(budget) is not int or off < 0 or budget <= 8:
    raise SystemExit("installed rootfs row needs a non-negative integer offset and budget > 8")
if off + budget > flash_size:
    raise SystemExit("installed rootfs slot exceeds the QSPI device")
print(f"{off}\t{budget}")
PY
    local off budget total
    IFS=$'\t' read -r off budget < "$slot"
    [ -n "$off" ] && [ -n "$budget" ] || {
        echo "[deploy] installed rootfs slot metadata is incomplete" >&2
        return 2
    }
    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o "$off" \
        --dump-flash --file-size 8 "$header"
    total=$("$PYTHON" - "$header" "$budget" <<'PY'
import struct, sys
raw = open(sys.argv[1], "rb").read()
budget = int(sys.argv[2])
if len(raw) != 8:
    raise SystemExit("live rootfs FBI header is short")
size, _crc = struct.unpack("<II", raw)
if size <= 0 or size + 8 > budget:
    raise SystemExit(
        f"live rootfs FBI length {size} exceeds installed slot budget {budget}")
print(size + 8)
PY
    )
    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o "$off" \
        --dump-flash --file-size "$total" "$live_rootfs"
    "$PYTHON" "$HERE/check_gptp_owner_pair.py" \
        --layout "$INSTALLED_LAYOUT" --bit "$INSTALLED_BIT" \
        --expected-fpga-part "$FPGA_PART" --rootfs "$live_rootfs" || {
            echo "[deploy] installed live rootfs does not complete its declared one-owner state" >&2
            return 2
        }
    echo "[deploy] live installed rootfs FBI CRC and owner marker match $source_owner"
}

write_target_bit() {
    echo "[deploy] write+verify bitstream @ 0x000000: $BIT"
    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -f --verify "$BIT"
}

refuse_nonatomic() {
    [ "${ALLOW_NONATOMIC_FLASH:-0}" = 1 ] && return 0
    echo "[deploy] $1 REFUSED: partial persistent writes do not prove the installed gPTP owner." >&2
    echo "[deploy] Use flash-pair with INSTALLED_LAYOUT and INSTALLED_BIT; recovery-only callers may explicitly set ALLOW_NONATOMIC_FLASH=1." >&2
    exit 2
}

do_flash() {
    refuse_nonatomic flash
    echo "[deploy] WARNING: non-atomic recovery bitstream write requested" >&2
    [ -n "$BIT" ] && [ -f "$BIT" ] || {
        echo "[deploy] flash: no bitstream (set BIT=<path/to/board.bit>)"; exit 2; }
    [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ] || {
        echo "[deploy] flash REFUSED: no flashboot_layout.json owner contract." >&2
        exit 2; }
    do_check_images
    local bit_build layout_build
    bit_build=$(realpath "$(dirname "$BIT")/..")
    layout_build=$(realpath "$(dirname "$LAYOUT")")
    [ "$bit_build" = "$layout_build" ] || {
        echo "[deploy] flash REFUSED: BIT and LAYOUT are from different build directories." >&2
        exit 2; }
    write_target_bit
}

do_flash_images() {
    refuse_nonatomic flash-images
    echo "[deploy] WARNING: non-atomic recovery image writes requested" >&2
    local tmp rows
    tmp="$(mktemp -d)"; rows="$tmp/images.tsv"
    trap 'rm -rf -- "$tmp"' RETURN
    prepare_images "$tmp" "$rows"
    write_prepared_images "$rows"
}

do_flash_pair() {
    [ -n "$BIT_EXPLICIT" ] && [ -n "$BIT" ] && [ -f "$BIT" ] || {
        echo "[deploy] flash-pair REFUSED: set BIT=<target .bit>" >&2; exit 2; }
    [ -n "$LAYOUT_EXPLICIT" ] && [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ] || {
        echo "[deploy] flash-pair REFUSED: set LAYOUT=<target layout>" >&2; exit 2; }
    [ -n "$INSTALLED_BIT" ] && [ -f "$INSTALLED_BIT" ] || {
        echo "[deploy] flash-pair REFUSED: set INSTALLED_BIT=<exact current .bit>" >&2; exit 2; }
    [ -n "$INSTALLED_LAYOUT" ] && [ -f "$INSTALLED_LAYOUT" ] || {
        echo "[deploy] flash-pair REFUSED: set INSTALLED_LAYOUT=<exact current layout>" >&2; exit 2; }

    local plan_args=(plan --installed-layout "$INSTALLED_LAYOUT"
        --installed-bit "$INSTALLED_BIT" --target-layout "$LAYOUT"
        --target-bit "$BIT" --expected-fpga-part "$FPGA_PART")
    [ -z "${EXPECTED_GPTP_OWNER:-}" ] || \
        plan_args+=(--expected-target-owner "$EXPECTED_GPTP_OWNER")
    local plan_line installed_owner installed_profile target_owner order
    local dump_bytes target_profile
    plan_line=$("$PYTHON" "$HERE/qspi_owner_transition.py" "${plan_args[@]}") || exit 2
    IFS=$'\t' read -r installed_owner installed_profile target_owner order \
        dump_bytes target_profile <<< "$plan_line"

    local tmp rows live state
    tmp="$(mktemp -d)"; rows="$tmp/images.tsv"; live="$tmp/qspi-offset-zero.bin"
    trap 'rm -rf -- "$tmp"' RETURN
    prepare_images "$tmp" "$rows"

    echo "[deploy] prove live QSPI bitstream on serial $SERIAL ($dump_bytes B)"
    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o 0 --dump-flash \
        --file-size "$dump_bytes" "$live"
    state=$("$PYTHON" "$HERE/qspi_owner_transition.py" identify \
        --dump "$live" --installed-bit "$INSTALLED_BIT" --target-bit "$BIT" \
        --expected-size "$dump_bytes") || exit 2
    echo "[deploy] live bit identity: $state artifact; $installed_owner -> $target_owner; $order"

    if [ "$state" = installed ] && [ "$installed_profile" != fabric-baremetal ]; then
        prove_live_installed_rootfs "$tmp" "$installed_owner"
    fi

    if [ "$state" = target ]; then
        if prepared_images_match "$rows" "$tmp/target-image-readback.bin"; then
            echo "[deploy] target bit and every target image already match"
        elif [ "$target_profile" = fabric-baremetal ]; then
            # A live bare-metal fabric commit bit ignores every Linux slot and
            # owns gPTP independently of AEM, so repairing AEM is safe.
            write_prepared_images "$rows"
        else
            echo "[deploy] flash-pair REFUSED: target $target_profile bit is live but its boot image set is not exact." >&2
            echo "[deploy] A full-Linux repair has no proven single-slot provenance; restore a proved fabric/baremetal bridge first." >&2
            exit 2
        fi
    elif [ "$order" = bit-first ]; then
        write_target_bit
        write_prepared_images "$rows"
    else
        write_prepared_images "$rows"
        write_target_bit
    fi
    echo "[deploy] flash-pair done. Power-cycle to boot the verified owner set."
}
do_console(){ echo "[deploy] console $CONSOLE @ $BAUD  (picocom; exit: Ctrl-a Ctrl-x)"; exec picocom -b "$BAUD" "$CONSOLE"; }

case "$STEP" in
    build)        do_build ;;
    load)         do_load ;;
    flash-pair)   do_flash_pair ;;
    flash)        do_flash ;;
    check-images) do_check_images ;;
    flash-images) do_flash_images ;;
    console)      do_console ;;
    all)          do_build; do_load; do_console ;;
    *) echo "usage: $0 [all|build|load|flash-pair|check-images|flash|flash-images|console]"; exit 2 ;;
esac
