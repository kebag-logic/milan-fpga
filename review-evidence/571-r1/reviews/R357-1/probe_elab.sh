#!/usr/bin/env bash
# R357-1: Verilator elaboration of KL_pp_shadow, base vs head.
# Usage: probe_elab.sh <verilator> <scratch-root> <receipt-dir>
#   <scratch-root> holds disposable copies base/ (2a2a7bb6) and head/ (f8a52f91).
# Part 1 (identity): each copy's own tracked per-config header supplies the
#   shape parameters the datapath passes; --stats at AX 1x1 and 8x8, base vs head.
# Part 2 (propagation): distinct counts AUDIO_UNIT=2, CLK_DOM=3, CONTROL=4
#   forced on KL_pp_shadow; --json-only; report the parameter values the
#   elaborated KL_aecp_dyn_state instance actually carries.
set -u
V=$1; S=$(cd "$2" && pwd); OUT=$3; mkdir -p "$OUT"
"$V" --version > "$OUT/elab_verilator_version.txt"

hval() { grep -E "localparam int $2 *=" "$1" | sed -E 's/.*= *([0-9]+);.*/\1/'; }

args_for() {  # phase shape -> -G list
  local h="$S/$1/configs/generated/$2/gen/adp_shape_defaults.svh"
  printf -- '-GN_STREAM_IN_P=%s -GN_STREAM_OUT_P=%s -GN_SPORT_IN_P=%s -GN_SPORT_OUT_P=%s -GN_AUDIO_UNIT_P=%s -GN_CLK_DOM_P=%s -GDESC_NAME_ENTRIES_P=%s' \
    "$(hval $h ADP_LISTENER_SINK_C)" "$(hval $h ADP_TALKER_SRC_C)" \
    "$(hval $h ADP_DMAP_IN_NPORTS_C)" "$(hval $h ADP_DMAP_OUT_NPORTS_C)" \
    "$(hval $h AEM_N_AUDIO_UNIT_C)" "$(hval $h AEM_N_CLKDOM_C)" "$(hval $h AEM_NAME_ENTRIES_C)"
  if [ "$1" = head ]; then printf -- ' -GN_CONTROL_P=%s' "$(hval $h AEM_N_CONTROL_C)"; fi
}

srcs_for() {  # phase -> incdirs, define, sources from the repo's own emitter
  (cd "$S/$1" && bash syn/yosys/run.sh --emit KL_pp_shadow 2>/dev/null) | awk -F= '
    $1=="incdir"{printf "+incdir+%s ", $2} $1=="define"{printf "-D%s ", $2}
    $1=="src"{printf "%s ", $2}'
}

job() {  # phase shape mode
  local ph=$1 shp=$2 mode=$3 d="$S/elab/$1-$2-$3" g
  rm -rf "$d"; mkdir -p "$d"
  if [ "$mode" = stats ]; then
    g=$(args_for "$ph" "$shp")
    echo "$g" > "$OUT/elab_${ph}_${shp}_params.txt"
    (cd "$S/$ph" && timeout 1500 "$V" --cc --stats -Wno-fatal --top-module KL_pp_shadow \
        --Mdir "$d" $g $(srcs_for "$ph")) > "$d/log.txt" 2>&1
    echo "$ph $shp stats rc=$?"
  else
    g="$(args_for "$ph" "$shp" | sed -E 's/-GN_AUDIO_UNIT_P=[0-9]+/-GN_AUDIO_UNIT_P=2/; s/-GN_CLK_DOM_P=[0-9]+/-GN_CLK_DOM_P=3/') -GN_CONTROL_P=4"
    [ "$ph" = base ] && g=$(echo "$g" | sed -E "s/ -GN_CONTROL_P=4//")
    [ "$ph" = head ] && g=$(echo "$g" | sed -E 's/ -GN_CONTROL_P=1//')
    echo "$g" > "$OUT/prop_${ph}_${shp}_params.txt"
    (cd "$S/$ph" && timeout 1500 "$V" --json-only -Wno-fatal --top-module KL_pp_shadow \
        --Mdir "$d" $g $(srcs_for "$ph")) > "$d/log.txt" 2>&1
    echo "$ph $shp json rc=$?"
  fi
}
export -f job args_for srcs_for hval; export V S OUT
printf '%s\n' "base endstation_ax7101_1x1_tdm8 stats" "head endstation_ax7101_1x1_tdm8 stats" \
  "base endstation_ax7101_8x8 stats" "head endstation_ax7101_8x8 stats" \
  "base endstation_ax7101_1x1_tdm8 json" "head endstation_ax7101_1x1_tdm8 json" \
  | xargs -P 6 -L 1 bash -c 'job "$0" "$1" "$2"' | sort | tee "$OUT/elab_rc.txt"
