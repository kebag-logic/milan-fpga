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
#     BIT=<path>    bitstream for `flash-pair` and `check-images` (both bind
#                   the layout to its exact payload digest and FPGA part;
#                   other steps default to the newest gateware/alinx_ax7101.bit)
#     LAYOUT=<path> target flashboot_layout.json (required for flash-pair; other
#                   steps default to the newest build's)
#     AEM=<path>    target AEM descriptor image (defaults to the layout's
#                   sibling aem_desc.bin). The product image set is exactly
#                   the bare-metal {bitstream, aem} pair.
#     EXPECTED_GPTP_OWNER=fabric additionally binds a named build recipe to
#                   the owner compiled into LAYOUT (used by build.sh); every
#                   non-fabric owner is refused as retired.
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
# machine mode. The fabric, protocol processor, physical TDM capture and
# render-free talker datapath remain present.
# --gtx-tx-invert is REQUIRED on this board: the GMII TX FFs are IOB-packed (deterministic
# skew ~0 vs the forwarded gtx_clk), so edge-aligned sampling is hold-marginal at the
# RTL8211E — measured 25-40 % corrupt frames edge-aligned vs 0 % with mid-bit sampling.
# The protocol processor retains its dedicated CPU memory attachment; the
# cacheless CPU does not elaborate a cache-coherency hub.
MILAN_OPTS="--board ax7101 --cpu vexiiriscv --cpu-count 1 --xlen 32 --software-profile baremetal --full --milan-clk-freq 50e6 --with-spiflash --flashboot baremetal --gtx-tx-invert --timing-opt --floorplan --eth-port e1 --no-i2s-playback --no-render-lpf --audio-interface tdm8 --audio-interface-master --talker-wire-chans 8 --cbs-queues-mask 0x10 --loopback-lane --fabric-gptp --entity-gen-dir $HERE/../../configs/generated/endstation_ax7101_1x1_tdm8 --l2-bytes 0"
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
    local layout="${1:-$LAYOUT}" bit="${2:-$BIT}" aem="${3:-${AEM:-}}"
    [ -n "$layout" ] && [ -f "$layout" ] || {
        echo "[deploy] image check: no flashboot_layout.json (build --with-spiflash, or set LAYOUT=<path>)"; exit 2; }
    [ -n "$aem" ] || aem="$(dirname "$layout")/aem_desc.bin"
    # #116/#259 owner contract: the layout must record the fabric plane as the
    # image's one gPTP owner and must be a bare-metal {bitstream, aem} set.
    # Unsupported owners and missing metadata are hard errors. flash-pair runs this while
    # materializing the whole set, before its first write.
    # [R-parallel] on #228: this advertised standalone verdict once ran on
    # --layout alone, so a layout naming nonexistent artifacts (or none)
    # still printed "image preflight OK". The verdict now requires the
    # target artifacts themselves: the bitstream must exist non-empty and
    # bind (payload sha256 + FPGA part) through the owner-pair check, and
    # the complete non-bit target set is materialized and size-checked
    # below with zero programmer I/O, exactly as flash-pair consumes it.
    [ -n "$bit" ] && [ -f "$bit" ] && [ -s "$bit" ] || {
        echo "[deploy] image check REFUSED: set BIT=<target .bit> (a target set without its bitstream is not flashable)" >&2
        exit 2
    }
    local pair_args=(--layout "$layout" --bit "$bit" --aem "$aem"
        --expected-fpga-part "$FPGA_PART")
    [ -z "${EXPECTED_GPTP_OWNER:-}" ] || \
        pair_args+=(--expected-owner "$EXPECTED_GPTP_OWNER")
    "$PYTHON" "$HERE/check_gptp_owner_pair.py" "${pair_args[@]}" || {
        echo "[deploy] image check REFUSED: the layout is not a bound fabric-owned bare-metal image set." >&2
        exit 2
    }
    # The compiled CPU width is part of the artifact's identity binding: the
    # bare-metal firmware and its BIOS are XLEN-exact, and a layout that does
    # not state the width cannot be validated at all.
    local expected_xlen
    expected_xlen=$("$PYTHON" - "$layout" <<'PY'
import json, sys
value = json.load(open(sys.argv[1], encoding="utf-8")).get("cpu_xlen")
if type(value) is not int or value != 32:
    raise SystemExit("layout does not name the product cpu_xlen (32)")
print(value)
PY
    ) || {
        echo "[deploy] image check REFUSED: layout does not bind the compiled CPU width." >&2
        exit 2
    }
    local tmp rows
    tmp="$(mktemp -d)"; rows="$tmp/images.tsv"
    if ! materialize_images "$tmp" "$rows" "$layout" "$aem"; then
        rm -rf -- "$tmp"
        echo "[deploy] image check REFUSED: the target image set does not materialize inside its layout budgets." >&2
        exit 2
    fi
    rm -rf -- "$tmp"
    echo "[deploy] image preflight OK: $layout (bound to $bit and $aem, xlen $expected_xlen)"
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
    local tmp="$1" rows="$2" layout="${3:-$LAYOUT}"
    local bit="${4:-$BIT}" aem="${5:-${AEM:-}}"
    [ -n "$aem" ] || aem="$(dirname "$layout")/aem_desc.bin"
    # The full preflight (which itself materializes once, into its own tmp),
    # then the materialization whose rows the write loop consumes.
    do_check_images "$layout" "$bit" "$aem"
    materialize_images "$tmp" "$rows" "$layout" "$aem" || exit 2
}

materialize_images() {
    # Materialize and size-check EVERY non-bit target before a single QSPI
    # write. A missing/oversized last image must not strand a partially updated
    # set merely because the old implementation discovered it inside its write
    # loop. No programmer I/O happens here; check-images runs this too.
    local tmp="$1" rows="$2" layout="${3:-$LAYOUT}"
    local aem="${4:-${AEM:-}}" manifest_rows
    [ -n "$aem" ] || aem="$(dirname "$layout")/aem_desc.bin"
    manifest_rows="$tmp/layout-rows.tsv"
    : > "$rows"
    # name<TAB>offset<TAB>ceiling for each manifest image. The ceiling is the
    # earliest of its declared budget, the next image/reservation, or 16 MiB.
    # Materialize this list synchronously: a failing process substitution is
    # otherwise invisible to the while-loop status and could look like an
    # empty, successfully prepared image set.
    # The explicit status check matters twice over: this function is called
    # from an `if !` condition (check-images), where set -e is suppressed
    # for the whole call tree, so a failing manifest derivation would
    # otherwise leave an EMPTY rows file that reads as a successfully
    # prepared (and empty) image set.
    "$PYTHON" - "$layout" "$FLASH_SIZE" > "$manifest_rows" <<'PY' || return 2
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
            aem)
                src="$aem"
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
        if [ "$name" = aem ]; then
            "$PYTHON" "$HERE/qspi_owner_transition.py" validate-aem \
                --layout "$layout" --aem "$fbi" >/dev/null || {
                echo "[deploy]   image 'aem': materialized bytes do not match the layout binding" >&2
                return 2
            }
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

stage_artifact_pair() {
    # Snapshot every pathname that carries identity before planning or live
    # programmer I/O. A concurrent build may replace board.bit, the layout,
    # or aem_desc.bin in place; validating one inode and later reopening that
    # mutable path would flash bytes that never passed the binding checks.
    # The exclusive transaction directory gives every later phase one stable
    # set of regular files instead.
    local dest="$1" layout_src="$2" bit_src="$3" aem_src="${4:-}"
    [ -f "$layout_src" ] && [ -s "$layout_src" ] || {
        echo "[deploy] staging REFUSED: layout is missing or empty: $layout_src" >&2
        return 2
    }
    [ -f "$bit_src" ] && [ -s "$bit_src" ] || {
        echo "[deploy] staging REFUSED: bitstream is missing or empty: $bit_src" >&2
        return 2
    }
    mkdir -p "$dest/gateware" || return 2
    cp -- "$layout_src" "$dest/flashboot_layout.json" || return 2
    cp -- "$bit_src" "$dest/gateware/target.bit" || return 2
    if [ -n "$aem_src" ]; then
        [ -f "$aem_src" ] || {
            echo "[deploy] staging REFUSED: AEM image is missing: $aem_src" >&2
            return 2
        }
        cp -- "$aem_src" "$dest/aem_desc.bin" || return 2
    fi
    chmod a-w "$dest/flashboot_layout.json" "$dest/gateware/target.bit" || return 2
    [ -z "$aem_src" ] || chmod a-w "$dest/aem_desc.bin" || return 2
}


write_target_bit() {
    local bit="${1:-$BIT}"
    echo "[deploy] write+verify bitstream @ 0x000000: $bit"
    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -f --verify "$bit"
}

refuse_nonatomic() {
    [ "${ALLOW_NONATOMIC_FLASH:-0}" = 1 ] && return 0
    echo "[deploy] $1 REFUSED: partial persistent writes do not prove the installed gPTP owner." >&2
    echo "[deploy] Use flash-pair with INSTALLED_LAYOUT and INSTALLED_BIT; recovery-only callers may explicitly set ALLOW_NONATOMIC_FLASH=1." >&2
    exit 2
}

do_flash() (
    refuse_nonatomic flash
    echo "[deploy] WARNING: non-atomic recovery bitstream write requested" >&2
    [ -n "$BIT" ] && [ -f "$BIT" ] || {
        echo "[deploy] flash: no bitstream (set BIT=<path/to/board.bit>)"; exit 2; }
    [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ] || {
        echo "[deploy] flash REFUSED: no flashboot_layout.json owner contract." >&2
        exit 2; }
    local tmp target layout bit aem deploy_transaction_tmp
    tmp="$(mktemp -d)"; target="$tmp/target"
    deploy_transaction_tmp="$tmp"
    trap 'rm -rf -- "$deploy_transaction_tmp"' EXIT
    aem="${AEM:-$(dirname "$LAYOUT")/aem_desc.bin}"
    stage_artifact_pair "$target" "$LAYOUT" "$BIT" "$aem" || exit 2
    layout="$target/flashboot_layout.json"
    bit="$target/gateware/target.bit"
    aem="$target/aem_desc.bin"
    do_check_images "$layout" "$bit" "$aem"
    "$PYTHON" "$HERE/qspi_owner_transition.py" validate \
        --layout "$layout" --bit "$bit" --expected-fpga-part "$FPGA_PART" || {
            echo "[deploy] flash REFUSED: BIT payload hash/part is not bound to LAYOUT." >&2
            exit 2
        }
    write_target_bit "$bit"
)

do_flash_images() (
    refuse_nonatomic flash-images
    echo "[deploy] WARNING: non-atomic recovery image writes requested" >&2
    local tmp rows target layout bit aem deploy_transaction_tmp
    tmp="$(mktemp -d)"; rows="$tmp/images.tsv"; target="$tmp/target"
    deploy_transaction_tmp="$tmp"
    trap 'rm -rf -- "$deploy_transaction_tmp"' EXIT
    aem="${AEM:-$(dirname "$LAYOUT")/aem_desc.bin}"
    stage_artifact_pair "$target" "$LAYOUT" "$BIT" "$aem" || exit 2
    layout="$target/flashboot_layout.json"
    bit="$target/gateware/target.bit"
    aem="$target/aem_desc.bin"
    prepare_images "$tmp" "$rows" "$layout" "$bit" "$aem"
    write_prepared_images "$rows"
)

do_flash_pair() (
    [ -n "$BIT_EXPLICIT" ] && [ -n "$BIT" ] && [ -f "$BIT" ] || {
        echo "[deploy] flash-pair REFUSED: set BIT=<target .bit>" >&2; exit 2; }
    [ -n "$LAYOUT_EXPLICIT" ] && [ -n "$LAYOUT" ] && [ -f "$LAYOUT" ] || {
        echo "[deploy] flash-pair REFUSED: set LAYOUT=<target layout>" >&2; exit 2; }
    [ -n "$INSTALLED_BIT" ] && [ -f "$INSTALLED_BIT" ] || {
        echo "[deploy] flash-pair REFUSED: set INSTALLED_BIT=<exact current .bit>" >&2; exit 2; }
    [ -n "$INSTALLED_LAYOUT" ] && [ -f "$INSTALLED_LAYOUT" ] || {
        echo "[deploy] flash-pair REFUSED: set INSTALLED_LAYOUT=<exact current layout>" >&2; exit 2; }

    local tmp rows live state target_stage installed_stage
    local target_layout target_bit target_aem installed_layout installed_bit
    local aem_src deploy_transaction_tmp
    tmp="$(mktemp -d)"; rows="$tmp/images.tsv"; live="$tmp/qspi-offset-zero.bin"
    target_stage="$tmp/target"; installed_stage="$tmp/installed"
    deploy_transaction_tmp="$tmp"
    trap 'rm -rf -- "$deploy_transaction_tmp"' EXIT
    aem_src="${AEM:-$(dirname "$LAYOUT")/aem_desc.bin}"
    stage_artifact_pair "$installed_stage" "$INSTALLED_LAYOUT" \
        "$INSTALLED_BIT" || exit 2
    stage_artifact_pair "$target_stage" "$LAYOUT" "$BIT" "$aem_src" || exit 2
    installed_layout="$installed_stage/flashboot_layout.json"
    installed_bit="$installed_stage/gateware/target.bit"
    target_layout="$target_stage/flashboot_layout.json"
    target_bit="$target_stage/gateware/target.bit"
    target_aem="$target_stage/aem_desc.bin"

    local plan_args=(plan --installed-layout "$installed_layout"
        --installed-bit "$installed_bit" --target-layout "$target_layout"
        --target-bit "$target_bit" --expected-fpga-part "$FPGA_PART")
    [ -z "${EXPECTED_GPTP_OWNER:-}" ] || \
        plan_args+=(--expected-target-owner "$EXPECTED_GPTP_OWNER")
    local plan_line installed_owner installed_profile target_owner order
    local dump_bytes target_profile
    plan_line=$("$PYTHON" "$HERE/qspi_owner_transition.py" "${plan_args[@]}") || exit 2
    IFS=$'\t' read -r installed_owner installed_profile target_owner order \
        dump_bytes target_profile <<< "$plan_line"

    prepare_images "$tmp" "$rows" "$target_layout" "$target_bit" "$target_aem"

    echo "[deploy] prove live QSPI bitstream on serial $SERIAL ($dump_bytes B)"
    run_ofl -c "$CABLE" --fpga-part "$FPGA_PART" -o 0 --dump-flash \
        --file-size "$dump_bytes" "$live"
    state=$("$PYTHON" "$HERE/qspi_owner_transition.py" identify \
        --dump "$live" --installed-bit "$installed_bit" --target-bit "$target_bit" \
        --expected-size "$dump_bytes") || exit 2
    echo "[deploy] live bit identity: $state artifact; $installed_owner -> $target_owner; $order"

    if [ "$state" = target ]; then
        if prepared_images_match "$rows" "$tmp/target-image-readback.bin"; then
            echo "[deploy] target bit and every target image already match"
        else
            # The planner admits only fabric-baremetal profiles (#259). A live
            # bare-metal fabric commit bit owns gPTP independently of AEM, so
            # repairing the AEM image beside it is safe.
            write_prepared_images "$rows"
        fi
    else
        # The one supported plan order: the old autonomous fabric owner stays
        # live until every target non-bit image has verified, then the target
        # bit commits.
        write_prepared_images "$rows"
        write_target_bit "$target_bit"
    fi
    echo "[deploy] flash-pair done. Power-cycle to boot the verified owner set."
)
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
