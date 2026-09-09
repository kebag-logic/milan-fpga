#!/bin/bash
# build.sh - named-config bitstream launcher for the Milan SoC (two-board lab).
#
# usage:
#   ./build.sh <config> [<config> ...] [--sweep] [--dry-run] [-- <extra milan_soc.py args>]
#
#   ./build.sh ax7101                  # ship shape (cbsf lineage) -> work/build_ax7101_<tag>
#   ./build.sh arty                    # Arty A7-100 bring-up shape
#   ./build.sh ax7101 arty             # BOTH boards, parallel, 90 s stagger
#   ./build.sh --sweep ax7101          # 3-directive place sweep (epo/spr/etm), per the
#                                      # saturate-the-box rule (3 x 32 threads)
#   TAG=myrun ./build.sh arty          # output dir suffix (default: date +%m%d%H%M)
#   ./build.sh arty -- --sys-clk-freq 90e6   # append/override milan_soc.py args
#   ./build.sh ax8x8 --dry-run           # print the launch line, start nothing (the
#                                      # tracked-shape refusal is previewed, not enforced)
#   BUILD_CFG=configs/endstation_ax7101_8x8.yaml ./build.sh ax7101
#                                      # a named recipe's flow flags on another config
#                                      # under configs/ (sweep.sh: SWEEP_CFG)
#
# Discipline encoded here (docs/integration/BUILDING.md):
#   * every build: setsid nohup (harness task-kills must never reap Vivado),
#     --vivado-max-threads 32 (Vivado hard cap), launch log next to the outdir;
#   * parallel launches staggered 90 s (shared pythondata git checkout: two
#     concurrent LiteX elaborations race on index.lock and crash);
#   * at most 3 concurrent builds (3 x 32 = the 96-core box saturated).
#
# A named config is ONE end-station YAML (recipe_config) plus the flow flags
# its cfg_<name> function appends; the DESIGN argv is read from the builder's
# artefact of that config, never spelled here (#402, design_argv below).
# Everything else is functions too: the body is called from main() at the
# bottom, in the order board_serials -> (do_flash) -> parse_args
# -> check_entity_shapes -> expand_jobs -> launch_jobs. The state they hand
# each other (CONFIGS, EXTRA, SWEEP, DRY, JOBS) is deliberately global and
# MUST NOT be made `local`: each stage reads what the previous one set.
# MAINTAINER DOC: docs/integration/BUILDING.md (configs, discipline rationale, per-board
# load/console facts, gates). Update it when adding a config or a rule here.

set -euo pipefail
WORK=$HOME/litex-milan/work
SOC_DIR="$(cd "$(dirname "$0")" && pwd)"
TAG=${TAG:-$(date +%m%d%H%M)}
STAGGER=90
REPO_ROOT="$(cd "$SOC_DIR/../.." && pwd)"

board_serials() {
    # ---- per-board flash/JTAG facts (docs/integration/BUILDING.md section 4) --------------------
    # serial = FTDI serial (TWO cables on the bus: NEVER omit, a flash op picking the
    # wrong board is destructive). Serials are BENCH-LOCAL: set AX_FTDI/ARTY_FTDI in
    # the environment or in sw/litex/boards.local.sh (gitignored; template =
    # boards.local.sh.example). policy = what this board's QSPI holds:
    #   both boards "boot" (USER 2026-07-20: "to flash use qspi"): bitstream at
    #   offset 0 in a dedicated 4 MiB slot, followed by the raw AEM image at
    #   4 MiB per flashboot_layout.json. Every named config is bare-metal (#259).
    [ -f "$SOC_DIR/boards.local.sh" ] && . "$SOC_DIR/boards.local.sh"
    AX_FTDI="${AX_FTDI:-SET_AX_FTDI}"       # sentinel fails loudly in openFPGALoader
    ARTY_FTDI="${ARTY_FTDI:-SET_ARTY_FTDI}"
}
board_facts() {  # -> "serial cable fpga_part flash_policy bit_name"
    case "$1" in
        ax7101|ax8x8) echo "$AX_FTDI ft232    xc7a100tfgg484 boot      alinx_ax7101.bit";;
        arty)          echo "$ARTY_FTDI digilent xc7a100tcsg324 boot      digilent_arty.bit";;
        *)      return 1;;
    esac
}
gptp_owner_for_config() {
    # #259: the fabric plane is the one gPTP owner, so every named product
    # configuration must select it.
    case "$1" in
        ax7101|ax8x8|arty) echo fabric;;
        *)          return 1;;
    esac
}

do_flash() {
    # ---- flash subcommand: ./build.sh flash <config>[:<builddir>] ... ---------------
    # Every persistent named-config write delegates to deploy.sh flash-pair. Supply
    # INSTALLED_LAYOUT + INSTALLED_BIT for the exact build currently in the board's
    # QSPI (or INSTALLED_BUILD=<dir> to derive both). The transaction proves that
    # bitstream by live readback, prepares the whole target set, then selects the
    # direction-safe verified write order.
    [ $# -gt 0 ] || { echo "usage: $0 flash <config>[:<builddir>] ..." >&2; exit 2; }
    for spec in "$@"; do
        c=${spec%%:*}; dir=${spec#*:}; [ "$dir" = "$spec" ] && dir=""
        facts=$(board_facts "$c") || { echo "unknown board config '$c'" >&2; exit 2; }
        read -r serial cable part policy bitname <<<"$facts"
        expected_owner=$(gptp_owner_for_config "$c") || {
            echo "[$c] no gPTP owner contract for this named config" >&2; exit 2; }
        if [ -z "$dir" ]; then
            # newest build dir containing the artifact this policy flashes
            # (|| true: an empty glob must reach the friendly error, not set -e)
            # boot/bitstream discover by the bit (json is reconstructed below if absent)
            want="flashboot_layout.json"; case "$policy" in bitstream|boot) want="gateware/$bitname";; esac
            dir=$( { ls -td "$WORK"/build_${c}*/ 2>/dev/null || true; } | while read -r d; do
                      [ -f "$d/$want" ] && { echo "$d"; break; }; done || true)
            [ -n "$dir" ] || { echo "[$c] no build containing $want under $WORK/build_${c}* (pass ${c}:<builddir>)" >&2; exit 2; }
        else
            case "$dir" in /*) ;; *) dir="$WORK/$dir";; esac
        fi
        dir=${dir%/}
        # sweep builds skip main()'s json export; reconstruct from the compiled
        # BIOS constants and bind them to the exact parsed bit payload.
        if [ ! -f "$dir/flashboot_layout.json" ] && [ -f "$dir/software/include/generated/soc.h" ]; then
            "${PYTHON:-python3}" "$SOC_DIR/layout_from_soch.py" "$dir" \
                --bit "$dir/gateware/$bitname"
        fi
        case "$policy" in
            boot)
                bit="$dir/gateware/$bitname"
                [ -f "$bit" ] || { echo "[$c] missing $bit" >&2; exit 2; }
                installed_layout="${INSTALLED_LAYOUT:-}"
                installed_bit="${INSTALLED_BIT:-}"
                if [ -z "$installed_layout" ] || [ -z "$installed_bit" ]; then
                    installed_build="${INSTALLED_BUILD:-}"
                    [ -n "$installed_build" ] || {
                        echo "[$c] flash REFUSED: set both INSTALLED_LAYOUT + INSTALLED_BIT, or INSTALLED_BUILD=<exact current build>." >&2
                        exit 2; }
                    case "$installed_build" in
                        /*) ;;
                        *) installed_build="$WORK/$installed_build" ;;
                    esac
                    installed_build=${installed_build%/}
                    installed_layout="$installed_build/flashboot_layout.json"
                    installed_bit="$installed_build/gateware/$bitname"
                fi
                [ -f "$installed_layout" ] || {
                    echo "[$c] missing installed layout $installed_layout" >&2; exit 2; }
                [ -f "$installed_bit" ] || {
                    echo "[$c] missing installed bitstream $installed_bit" >&2; exit 2; }
                echo "== flash-pair [$c] LIVE OWNER-STATE PROOF + ORDERED VERIFIED SET =="
                SERIAL="$serial" CABLE="$cable" FPGA_PART="$part" \
                    LAYOUT="$dir/flashboot_layout.json" \
                    BIT="$bit" \
                    INSTALLED_LAYOUT="$installed_layout" \
                    INSTALLED_BIT="$installed_bit" \
                    EXPECTED_GPTP_OWNER="$expected_owner" \
                    "$SOC_DIR/deploy.sh" flash-pair
                ;;
            images)
                echo "[$c] flash REFUSED: named persistent profiles must carry a complete bitstream+image set for flash-pair." >&2
                exit 2
                ;;
            bitstream)
                echo "[$c] flash REFUSED: named bitstream-only persistent writes cannot preserve an installed owner set." >&2
                exit 2
                ;;
        esac
    done
}

# ---- named configurations -----------------------------------------------------
# recipe_config binds a name to the end-station config it builds; cfg_<name>
# holds the FLOW flags only (Vivado directives here; the thread cap, --build
# and the output directory are launch_jobs'). Every DESIGN flag - board, CPU
# width and hart count, streams, audio interface, wire channels, the tier-1
# prunes, clocks, flash - comes from the config through design_argv, so a new
# builder flag reaches a launch with no edit here. Until #402 the three
# recipes restated that argv as shell literals kept equal to emit_soc_argv by
# scripts/check_sweep_shape.py: #155 repaired ten divergences at once and
# #157/#362 two more, which is what a copy costs.
recipe_config() {  # -> the end-station config named recipe "$1" builds
    # BUILD_CFG rebinds it for ONE call, the way SWEEP_CFG does in sweep.sh: a
    # config under configs/, named relative to the repository root, so that
    # its generated/ include dir is where design_argv points --entity-gen-dir.
    if [ -n "${BUILD_CFG:-}" ]; then
        [ -f "$REPO_ROOT/$BUILD_CFG" ] || { echo "BUILD_CFG=$BUILD_CFG: no such config under the repository root" >&2; return 1; }
        echo "$BUILD_CFG"; return
    fi
    case "$1" in
        ax7101) echo "configs/endstation_ax7101_1x1_tdm8.yaml";;
        ax8x8)  echo "configs/endstation_ax7101_8x8.yaml";;
        arty)   echo "configs/endstation_arty_current.yaml";;
        *)      echo "no end-station config is bound to '$1'" >&2; return 1;;
    esac
}
soc_params_for() {  # -> the builder artefact design_argv reads for config "$1"
    echo "$REPO_ROOT/sw/builder/out/$(basename "$1" .yaml)/soc_params.json"
}
design_argv() {
    # ---- the design argv of config "$1", read from the builder's artefact ----------
    # Regenerated HERE, the way sweep.sh's entity_defs does, so the artefact
    # can only be stale if this line goes; then read back out of
    # soc_params.json, the per-config emission every builder run writes. (The
    # per-board sweep fragment is written only under --write-fragment, and
    # the two AX recipes would fight over it.) --entity-gen-dir is a flow
    # flag: where THIS launch reads its generated entity definition from.
    cfg=$1
    python3 "$REPO_ROOT/sw/builder/endstation_builder.py" "$REPO_ROOT/$cfg" > /dev/null
    argv=$(python3 -c 'import json, pathlib, sys; print(" ".join(json.loads(pathlib.Path(sys.argv[1]).read_text())["argv"]))' "$(soc_params_for "$cfg")")
    echo "$argv --entity-gen-dir $REPO_ROOT/configs/generated/$(basename "$cfg" .yaml)"
}
cfg_ax7101() {   # shipping bare-metal shape (endstation_ax7101_1x1_tdm8): flow flags
    echo "--synth-directive AreaOptimized_high --opt-directive ExploreArea \
          --place-directive ExtraPostPlacementOpt"
}
cfg_ax8x8() {    # 8-stream (64ch) bare-metal shape (endstation_ax7101_8x8): flow flags
    # The deployed 0x00010022 gateware came from the x32f1_eto sweep; this
    # recipe has never produced a bitstream. Its design facts are the
    # config's: RV32 single hart (#157), the cacheless bare-metal product
    # (#259), the SPENT render-filter area lever (docs/design/AREA_BUDGET.md).
    # So is the Ethernet port (e1, the bench default). If the AX cable is on
    # e2, append `-- --eth-port e2`; AX42's guard reset scope covers either
    # PHY's tx/gtx path.
    echo "--synth-directive AreaOptimized_high --opt-directive ExploreArea \
          --place-directive AltSpreadLogic_high"
}
cfg_arty() {     # Arty A7-100 bare-metal (endstation_arty_current): Vivado defaults
    # -1 die: 100 MHz datapath does NOT close (measured -1.0 WNS); the config
    # runs the datapath at 50 MHz with sys 83.333 (VCO 1000; 90e6 has NO
    # solution with the 25 MHz eth ref). Proven to reach the Instance
    # (test_builder gate 23g), not built: the board is a retired DUT.
    echo ""
}

SWEEP_DIRECTIVES="ExtraPostPlacementOpt AltSpreadLogic_high ExtraTimingOpt"

parse_args() {
    # ---- arg parsing ----------------------------------------------------------------
    CONFIGS=(); SWEEP=0; DRY=0; EXTRA=()
    while [ $# -gt 0 ]; do
        case "$1" in
            --sweep)   SWEEP=1;;
            --dry-run) DRY=1;;
            --)        shift; EXTRA=("$@"); break;;
            *)         type "cfg_$1" >/dev/null 2>&1 || { echo "unknown config '$1' (have: $(declare -F | sed -n 's/.* cfg_/ /p' | tr -d '\n'))" >&2; exit 2; }
                       CONFIGS+=("$1");;
        esac
        shift
    done
    [ ${#CONFIGS[@]} -gt 0 ] || { echo "usage: $0 <config> [<config> ...] [--sweep] [--dry-run] [-- extra args]" >&2; exit 2; }
    [ -z "${BUILD_CFG:-}" ] || [ ${#CONFIGS[@]} -eq 1 ] || { echo "BUILD_CFG rebinds ONE named recipe: name one config" >&2; exit 2; }
}

check_entity_shapes() {
    # ---- entity-definition gate (HARD, not advisory) --------------------------------
    # The gateware `include-s a GENERATED entity definition: the ADPDU stream counts
    # in hdl/common/gen/adp_shape_defaults.svh, served read-only at 0x618/0x61C
    # and ALSO sizing the protocol processor's ACMP source/sink context arrays. It
    # comes from ONE end-station config via endstation_builder.py --write-rtl.
    # Until 2026-07-27 nothing checked WHICH config: the tree carried the 1x1 shape
    # and every build, 8x8 included, compiled it in - so the 8x8 board advertised 1
    # talker source. Refuse to launch if the tree is another shape's.
    # (The AEM descriptor ROM used to be the second half of this gate, and briefly
    #  had no successor: the deleted AECP/AEM engine took the in-gateware ROM with
    #  it. The descriptors are back, in DRAM - milan_soc.py builds the image for
    #  THIS config from the same out/ directory and writes it beside the bitstream,
    #  refusing to launch Vivado if the model is missing or unbuildable. So the
    #  shape check below still covers only the `svh`; the descriptors now police
    #  themselves, per build, and cannot be another config's.)
    for c in "${CONFIGS[@]}"; do
        ecfg=$(recipe_config "$c") || exit 2
        python3 "$REPO_ROOT/scripts/check_entity_shape.py" --built-config "$REPO_ROOT/$ecfg" && continue
        # A dry run launches nothing, so it previews the refusal beside the
        # launch line instead of stopping: the shape gate reads every recipe's
        # argv out of its dry run, whichever config owns the tree (#402).
        [ "$DRY" = 1 ] && { echo "DRY [$c] a launch would be REFUSED: the tracked entity definition is not $ecfg's"; continue; }
        echo "refusing to build '$c': the tracked entity definition is not $ecfg's" >&2; exit 2
    done
}

expand_jobs() {
    # ---- expand configs (x directives when sweeping) --------------------------------
    JOBS=()   # "name|args"
    for c in "${CONFIGS[@]}"; do
        cfg=$(recipe_config "$c") || exit 2
        design=$(design_argv "$cfg")
        base_args="$design $("cfg_$c")"
        echo "[$c] design argv from $(soc_params_for "$cfg") (regenerated from $cfg); flow flags from cfg_$c"
        if [ "$SWEEP" = 1 ]; then
            # SWEEP_DIRECTIVES is a LIST of Vivado directives: the split is the
            # point, one loop iteration per directive.
            for d in $SWEEP_DIRECTIVES; do  # shellcheck disable=SC2086
                short=$(echo "$d" | tr -dc 'A-Z' | tr 'A-Z' 'a-z')
                # strip any config-default place directive, then pin the sweep's
                args=$(echo "$base_args" | sed 's/--place-directive [A-Za-z_]*//')
                JOBS+=("${c}_${short}|$args --place-directive $d")
            done
        else
            JOBS+=("${c}|$base_args")
        fi
    done
    [ ${#JOBS[@]} -le 3 ] || { echo "refusing ${#JOBS[@]} parallel builds (box saturates at 3 x 32 threads); split the call" >&2; exit 2; }
}

launch_jobs() {
    # ---- launch ---------------------------------------------------------------------
    first=1
    for job in "${JOBS[@]}"; do
        name=${job%%|*}; args=${job#*|}
        out="$WORK/build_${name}_${TAG}"
        cmd="cd $SOC_DIR && source $HOME/Xilinx2/2026.1/Vivado/settings64.sh && "
        cmd+="export PATH=$HOME/litex-milan/venv/bin:\$PATH && "
        # Same seed as sweep.sh: LiteX spells the CPU ISA argument from a
        # Python set, the netlist cache hashes that spelling, and an unpinned
        # seed regenerates the core per process (#362; measured spread in
        # sweep.sh). The shape gate refuses a launch line without it.
        cmd+="export PYTHONHASHSEED=0 && "
        cmd+="exec python3 milan_soc.py $args ${EXTRA[*]:-} --vivado-max-threads 32 --build --output-dir $out"
        if [ "$DRY" = 1 ]; then
            echo "DRY [$name] -> $out"; echo "  $cmd" | tr -s ' '; continue
        fi
        [ "$first" = 1 ] || { echo "stagger ${STAGGER}s (shared pythondata checkout)"; sleep "$STAGGER"; }
        first=0
        setsid nohup bash -c "$cmd" > "$WORK/build_${name}_${TAG}.launch.log" 2>&1 &
        echo "LAUNCHED [$name] pid=$! out=$out log=$WORK/build_${name}_${TAG}.launch.log"
    done
}

main() {
    board_serials
    if [ "${1:-}" = "flash" ]; then
        shift
        do_flash "$@"
        exit 0
    fi
    parse_args "$@"
    check_entity_shapes
    expand_jobs
    launch_jobs
}
main "$@"
