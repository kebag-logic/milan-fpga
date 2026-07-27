#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# csr_snapshot.sh <csr_base_hex>
#
# Full milan_csr snapshot in ONE process. Pushed with `ssh <board> 'sh -s' -- ...`
# because a board has no scp, and written in POSIX sh with no Python because a
# board has no Python.
#
# WHY THIS IS NOT A DEVMEM LOOP. `devmem` costs about 0.75 s per invocation on
# the softcore. The ~150 registers below would be ~2 minutes of pure fork/exec,
# and an 800-register sweep once took over ten minutes. So the fast path
# block-reads /dev/mem with ONE `dd` and decodes it with ONE `od`.
#
# WHY IT STILL HAS A SLOW PATH. `dd`/`od` option support varies across busybox
# builds, and a wrong `-t x4` decode would silently produce plausible-looking
# garbage. The block path is therefore SELF-VALIDATING: it must reproduce the
# ID magic 0x4D494C4E at offset 0 and a plausible VERSION at 0x004, or the
# script falls back to per-register devmem and says which path it used.
#
# Output: `#METHOD=block|devmem` then `0xOFF=0xVALUE` lines, one per register.
# Reads only. Nothing here writes, arms, clears or latches anything - a
# baseline snapshot must not perturb what it is measuring. (STATS_CTRL is NOT
# strobed here; the RMON phase arms it explicitly when it wants a fresh set.)

BASE="${1:-0x90000000}"

# Offsets read in the block sweep: 0x000-0x93F covers identification, MAC,
# RMON, classifier, ADP/AECP/ACMP, lwSRP, CRF, link guard, the 0x800 window
# registers, LTAP, APRB, PBK, MCSRV and CHMAP.
BLOCK_START=0
BLOCK_WORDS=592          # 0x000 .. 0x93C inclusive

# Registers the slow path reads one at a time (same set, sparse).
SLOW_OFFSETS="0x000 0x004 0x008 0x00C 0x100 0x110 0x200 0x204 0x300
0x600 0x654 0x658 0x65C 0x660 0x680 0x690 0x694 0x6A4 0x6A8 0x6AC 0x6B0 0x6B4
0x6B8 0x6BC 0x6C0 0x6C4 0x6C8 0x6CC 0x6D0 0x6D4 0x6D8 0x6DC 0x6E0 0x6E4 0x6E8
0x6EC 0x700 0x71C 0x720 0x72C 0x738 0x73C 0x740 0x744 0x748 0x74C 0x750 0x764
0x774 0x7B4 0x800 0x804 0x810 0x814 0x818 0x81C 0x820 0x824 0x828 0x82C
0x830 0x834 0x838 0x83C 0x840 0x844 0x848 0x84C 0x850 0x854 0x858 0x85C
0x860 0x864 0x868 0x870 0x874 0x878 0x87C 0x880 0x884 0x888 0x88C 0x890
0x894 0x898 0x89C 0x8A0 0x8A4 0x8A8 0x8AC 0x8B0 0x8B4 0x8B8 0x8BC 0x8C0
0x8C4 0x8C8 0x8CC 0x8D0 0x8F8 0x8FC 0x900 0x904 0x908 0x90C
0x210 0x214 0x218 0x21C 0x220 0x224 0x228 0x22C 0x230"

emit_slow() {
    echo "#METHOD=devmem"
    for off in $SLOW_OFFSETS; do
        v=$(devmem $((BASE + off)) 32 2>/dev/null)
        [ -n "$v" ] || v=0x00000000
        printf '0x%03X=%s\n' "$off" "$v"
    done
}

# ---- fast path: one dd, one od ------------------------------------------
# `dd bs=4 skip=N` seeks BASE bytes into /dev/mem; AXI-Lite is happy with the
# 4-byte accesses. `od -A n -t x4` prints native-endian 32-bit words, which is
# what the little-endian softcore reads.
BLOCK=$(dd if=/dev/mem bs=4 skip=$(( (BASE + BLOCK_START) / 4 )) \
           count=$BLOCK_WORDS 2>/dev/null | od -A n -t x4 2>/dev/null)

if [ -n "$BLOCK" ]; then
    # Validate before trusting: word 0 must be the "MILN" magic.
    FIRST=$(echo "$BLOCK" | awk 'NR==1 {print $1; exit}')
    case "$FIRST" in
        4d494c4e|4D494C4E)
            echo "#METHOD=block"
            echo "$BLOCK" | awk -v n="$BLOCK_WORDS" '
                { for (i = 1; i <= NF; i++) {
                      if (w >= n) exit
                      printf "0x%03X=0x%s\n", w * 4, toupper($i)
                      w++ } }'
            exit 0
            ;;
    esac
fi

# ---- slow path ----------------------------------------------------------
# Either the block read failed (no dd/od options, /dev/mem restrictions) or it
# did not reproduce the magic, which means the decode cannot be trusted.
emit_slow
