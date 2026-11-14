#!/bin/bash
# Planted defects of THE RETRY's round costs at 8x8/1if, each against the mailbox arm the lane selects there
# (aecp_arms.EIGHT_ONE), on a disposable clone; each plant is reverted and the clone checked clean after it.
# usage: probe_retry_charge.sh CLONE OUT
set -u
H=$1 O=$2
cd "$H" || exit 3
F="Mailbox.EveryNotice*:Mailbox.ARefusedAttemptIsChargedToItsRound:Mailbox.ARoundWithRoomPastARefusalGoesOnToTheNextPort"
plant() {  # name file old new
    local name=$1 file=$2 old=$3 new=$4
    python3 -I - "$file" "$old" "$new" <<'EOF'
import sys
from pathlib import Path
p, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = p.read_text()
assert t.count(old) == 1, (p, old)
p.write_text(t.replace(old, new))
EOF
    echo "## $name: $file"
    git diff --stat | tail -1
    python3 -B sw/firmware/ctrl/test/aecp_arms.py --mailbox --config configs/endstation_ax7101_8x8.yaml --interfaces 1 \
        --filter "$F" --output "$O/$name" > "$O/$name.log" 2>&1
    echo "rc=$?"
    grep -E '^\[  (FAILED|PASSED)  \]|\[FAIL\]' "$O/$name.log" | sort -u
    git checkout -q -- "$file"
    echo "clean after revert: $(git status --porcelain | wc -l) path(s) changed"
}
mkdir -p "$O"
plant core-charges-34 sw/firmware/ctrl/aecp/aecp.c $'\t\t\t\ta->round_us -= AECP_ATTEMPT_US;\n' $'\t\t\t\ta->round_us -= 34u;\n'
plant adapter-admits-at-85 sw/firmware/ctrl/aecp/aecp_mbx.c '(int32_t)left_us - (int32_t)AECP_ROUND_COLD_US' \
    '(int32_t)left_us - (int32_t)85u'
echo "## control: unplanted head"
python3 -B sw/firmware/ctrl/test/aecp_arms.py --mailbox --config configs/endstation_ax7101_8x8.yaml --interfaces 1 \
    --filter "$F" --output "$O/unplanted" > "$O/unplanted.log" 2>&1
echo "rc=$?"
grep -E '^\[  (FAILED|PASSED)  \]' "$O/unplanted.log" | sort -u
