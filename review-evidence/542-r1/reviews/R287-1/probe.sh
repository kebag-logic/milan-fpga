#!/usr/bin/env bash
# R287-1 focused probes for PR #550 / issue #542 (milan_dp notification content bars).
# Usage: REPO=<clone root> V=<verilator 5.050> PKT=<packet dir> probe.sh <stage> [<leg> <tag> ...]
#   prep                 build the hex prerequisites and write the variant sources
#   build <leg> <tag>    build leg (notify|nxn|nxn8|nxndv|nxn4c) with variant tag
#   run   <leg> <tag>    run that binary, log to $PKT/receipts/<leg>_<tag>.log
#   clean                remove every untracked artifact this script created
# Tags: head (the tree as checked out), base (615b5a5 sim_nxn.cpp), old (766b6a1:
# the lever with the OLD checks), oldna (old, with the lever's await_aecp call
# removed), each optionally suffixed _lever (-DNOTIFY_REALLOC_TB=1) or
# _lasan (lever + AddressSanitizer).
set -euo pipefail
: "${REPO:?}" "${V:?}" "${PKT:?}"
DP="$REPO/tb/verilator/milan_dp"
R="$PKT/receipts"
mkdir -p "$R"
cd "$DP"
BASE=615b5a5d7de01b23f15502e3732c6f2cb81ce74b
LEVERC=766b6a14956a6efdb608c6d940c7ae380b73c91a

src_of() {
    case "$1" in
        head) echo sim_nxn.cpp ;;
        base) echo sim_nxn_r287base.cpp ;;
        old) echo sim_nxn_r287old.cpp ;;
        oldna) echo sim_nxn_r287oldna.cpp ;;
        mutempty) echo sim_nxn_r287mutempty.cpp ;;
        *) echo "unknown source $1" >&2; exit 2 ;;
    esac
}

recipe() {
    make -n VERILATOR="$V" VERILATOR_JOBS=8 run \
        | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' | grep -E -- "-o Vmilan_dp_$1\$"
}

case "$1" in
prep)
    make VERILATOR="$V" ltn_rom.hex ucode.hex gptp_ucode.hex > "$R/prep.log" 2>&1
    git -C "$REPO" rev-parse "$LEVERC" >/dev/null
    git -C "$REPO" show "$BASE:tb/verilator/milan_dp/sim_nxn.cpp" > sim_nxn_r287base.cpp
    git -C "$REPO" show "$LEVERC:tb/verilator/milan_dp/sim_nxn.cpp" > sim_nxn_r287old.cpp
    # oldna: drop ONLY await_aecp's lever call (the first one), keep drain_tx's
    awk 'BEGIN{d=0} /^        force_uns_log_realloc\(\);$/ && d==0 {d=1; next} {print}' \
        sim_nxn_r287old.cpp > sim_nxn_r287oldna.cpp
    diff sim_nxn_r287old.cpp sim_nxn_r287oldna.cpp > "$R/oldna.diff" || true
    # mutempty: the head, with notify_last() always answering "absent"
    sed 's|return last < uns_log.size() ? uns_log\[last\] : std::vector<uint8_t>();|return std::vector<uint8_t>();|' \
        sim_nxn.cpp > sim_nxn_r287mutempty.cpp
    diff sim_nxn.cpp sim_nxn_r287mutempty.cpp > "$R/mutempty.diff" || true
    sha256sum sim_nxn.cpp sim_nxn_r287base.cpp sim_nxn_r287old.cpp sim_nxn_r287oldna.cpp sim_nxn_r287mutempty.cpp > "$R/variant_sources.sha256"
    # the fix commit, as a diff of the old-check lever tree to the head tree
    git -C "$REPO" diff "$LEVERC" HEAD -- tb/verilator/milan_dp/sim_nxn.cpp > "$R/lever_to_head.diff"
    ;;
build)
    leg=$2; tag=$3; srcv=${tag%%_*}; mode=${tag#"$srcv"}
    src=$(src_of "$srcv")
    extra=""
    case "$mode" in
        "") ;;
        _lever) extra='-CFLAGS -DNOTIFY_REALLOC_TB=1' ;;
        _lasan) extra='-CFLAGS -DNOTIFY_REALLOC_TB=1 -CFLAGS "-fsanitize=address -fsanitize-recover=address -fno-omit-frame-pointer -g" -LDFLAGS "-fsanitize=address -fsanitize-recover=address"' ;;
        _asan) extra='-CFLAGS "-fsanitize=address -fsanitize-recover=address -fno-omit-frame-pointer -g" -LDFLAGS "-fsanitize=address -fsanitize-recover=address"' ;;
        *) echo "unknown mode $mode" >&2; exit 2 ;;
    esac
    c=$(recipe "$leg")
    c=${c/--Mdir obj_$leg/--Mdir obj_r287_${leg}_$tag}
    c=${c/ sim_nxn.cpp / $src }
    c=${c/ -o Vmilan_dp_$leg/ $extra -o Vmilan_dp_$leg}
    printf '%s\n' "$c" > "$R/build_${leg}_$tag.cmd"
    start=$(date +%s)
    if eval "$c" > "$R/build_${leg}_$tag.log" 2>&1; then rc=0; else rc=$?; fi
    echo "build $leg $tag rc=$rc seconds=$(( $(date +%s) - start ))" | tee -a "$R/builds.txt"
    ;;
run)
    leg=$2; tag=$3
    export ASAN_OPTIONS=halt_on_error=0:suppress_equal_pcs=0:detect_leaks=0
    start=$(date +%s)
    if "./obj_r287_${leg}_$tag/Vmilan_dp_$leg" > "$R/${leg}_$tag.log" 2>&1; then rc=0; else rc=$?; fi
    echo "run $leg $tag rc=$rc seconds=$(( $(date +%s) - start ))" | tee -a "$R/runs.txt"
    grep -E 'checks:|checks, ' "$R/${leg}_$tag.log" | tail -1 || true
    ;;
clean)
    rm -rf obj_r287_* sim_nxn_r287base.cpp sim_nxn_r287old.cpp sim_nxn_r287oldna.cpp sim_nxn_r287mutempty.cpp
    ;;
*) echo "unknown stage $1" >&2; exit 2 ;;
esac
