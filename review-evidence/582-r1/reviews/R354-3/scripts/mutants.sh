#!/usr/bin/env bash
# R354-3 disposable mutation probes. Usage:
#   mutants.sh <repo-root> <scratch-dir> <python-with-litex> <parent-commit>
# Each probe runs on a fresh copy of <repo-root> (with its .git) under <scratch-dir>;
# the reviewed tree is never edited. Prints one verdict line per probe.
set -u
repo=$1 scratch=$2 py=$3 parent=$4
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$scratch"

fresh() {  # fresh <name>: a pristine copy of the head tree
    rm -rf "$scratch/$1"
    rsync -a --exclude=__pycache__ "$repo/" "$scratch/$1/"
    cp "$parent_test" "$scratch/$1/sw/builder/parent_test_clock_contract.py"
    printf '%s\n' "$scratch/$1"
}

soc_test() {  # soc_test <tree> <test-file>: run only the SoC refusal arm
    (cd "$1/sw/builder" && "$py" -c "
import sys; sys.path.insert(0, '.')
import importlib.util
spec = importlib.util.spec_from_file_location('tcc', sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.test_soc_clock_contract()" "$2")
}

rom_test() {  # rom_test <tree> <test-file>: run only the ROM clock arm
    (cd "$1/sw/builder" && "$py" -c "
import sys; sys.path.insert(0, '.')
import importlib.util
spec = importlib.util.spec_from_file_location('tcc', sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.test_gptp_rom_clock()" "$2")
}

verdict() {  # verdict <label> <expect KILLED|SURVIVED|PASS> <rc>
    local got
    if [ "$3" -eq 0 ]; then got=SURVIVED; else got=KILLED; fi
    [ "$2" = PASS ] && { [ "$3" -eq 0 ] && got=PASS || got=FAIL; }
    local ok=MATCH; [ "$got" = "$2" ] || ok=MISMATCH
    printf 'PROBE %-44s expected=%-8s got=%-8s %s\n' "$1" "$2" "$got" "$ok"
}

parent_test="$scratch/parent_test_clock_contract.py.src"
git -C "$repo" show "$parent:sw/builder/test_clock_contract.py" > "$parent_test"

# --- E1: SoC clock refusal bypassed whenever --entity-gen-dir is given -------
t=$(fresh e1)
f="$t/sw/litex/milan_soc.py"
old='    if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:'
new='    if not args.entity_gen_dir and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:'
grep -qxF "$old" "$f" || { echo "E1 anchor missing"; exit 2; }
"$py" - "$f" "$old" "$new" <<'EOF'
import sys; p, o, n = sys.argv[1:]; s = open(p).read(); assert s.count(o) == 1; open(p, "w").write(s.replace(o, n))
EOF
soc_test "$t" "$t/sw/builder/test_clock_contract.py" > "$scratch/e1_head.log" 2>&1
verdict "E1 entity-gen-dir bypass vs head test" KILLED $?
soc_test "$t" "$t/sw/builder/parent_test_clock_contract.py" > "$scratch/e1_parent.log" 2>&1
verdict "E1 entity-gen-dir bypass vs parent test" SURVIVED $?

# --- R1 / R2: builder ROM clock dropped / system clock fed --------------------
line='             "--clk-hz", str(cfg["constraints"]["milan_clk_hz"])],'
for m in R1 R2; do
    t=$(fresh "$m")
    f="$t/sw/builder/endstation_builder.py"
    grep -qxF "$line" "$f" || { echo "$m anchor missing"; exit 2; }
    if [ "$m" = R1 ]; then rep='             ],'; else rep='             "--clk-hz", str(cfg["constraints"]["sys_clk_hz"])],'; fi
    "$py" - "$f" "$line" "$rep" <<'EOF'
import sys; p, o, n = sys.argv[1:]; s = open(p).read(); assert s.count(o) == 1; open(p, "w").write(s.replace(o, n))
EOF
    rom_test "$t" "$t/sw/builder/test_clock_contract.py" > "$scratch/${m}_head.log" 2>&1
    verdict "$m ROM clock mutant vs head test (tracked shapes)" KILLED $?
done

# --- EQ: a sixth configuration whose system clock equals its Milan clock -----
t=$(fresh eq)
"$py" - "$t/configs/endstation_ax7101_1x1_tdm8.yaml" "$t/configs/endstation_zz_equal_clock.yaml" <<'EOF'
import sys, re
src, dst = sys.argv[1:]
s = open(src).read()
s2, n = re.subn(r"(\n\s*sys_clk_hz:\s*)100000000", r"\g<1>50000000", s)
assert n == 1
open(dst, "w").write(s2)
EOF
rom_test "$t" "$t/sw/builder/test_clock_contract.py" > "$scratch/eq_head.log" 2>&1
rc=$?; verdict "EQ equal-clock shape vs head test" PASS $rc
grep -q 'endstation_zz_equal_clock: SKIP system-clock control: sys_clk_hz == milan_clk_hz' "$scratch/eq_head.log" \
    && echo "PROBE EQ named SKIP line present                              MATCH" \
    || echo "PROBE EQ named SKIP line present                              MISMATCH"
c=$(grep -c ': SKIP system-clock control' "$scratch/eq_head.log")
[ "$c" -eq 1 ] && echo "PROBE EQ exactly one SKIP (tracked shapes not skipped)        MATCH" \
               || echo "PROBE EQ exactly one SKIP (got $c)                              MISMATCH"
rom_test "$t" "$t/sw/builder/parent_test_clock_contract.py" > "$scratch/eq_parent.log" 2>&1
verdict "EQ equal-clock shape vs parent test (old failure)" KILLED $?
grep -q 'ROM clock control is insensitive' "$scratch/eq_parent.log" \
    && echo "PROBE EQ parent failure is the insensitive-control assertion   MATCH" \
    || echo "PROBE EQ parent failure is the insensitive-control assertion   MISMATCH"

# --- EQ+R1: the default-clock control still runs on the equal-clock shape ----
t2=$(fresh eqr1)
cp "$t/configs/endstation_zz_equal_clock.yaml" "$t2/configs/"
f="$t2/sw/builder/endstation_builder.py"
"$py" - "$f" "$line" '             ],' <<'EOF'
import sys; p, o, n = sys.argv[1:]; s = open(p).read(); assert s.count(o) == 1; open(p, "w").write(s.replace(o, n))
EOF
rom_test "$t2" "$t2/sw/builder/test_clock_contract.py" > "$scratch/eqr1_head.log" 2>&1
verdict "EQ+R1 ROM clock dropped, equal-clock shape present" KILLED $?

# --- Control: the unmutated copy passes both arms -----------------------------
t=$(fresh ctl)
soc_test "$t" "$t/sw/builder/test_clock_contract.py" > "$scratch/ctl_soc.log" 2>&1
verdict "CTL unmutated SoC arm" PASS $?
rom_test "$t" "$t/sw/builder/test_clock_contract.py" > "$scratch/ctl_rom.log" 2>&1
verdict "CTL unmutated ROM arm" PASS $?
soc_test "$t" "$t/sw/builder/parent_test_clock_contract.py" > "$scratch/ctl_parent_soc.log" 2>&1
verdict "CTL unmutated SoC arm, parent test" PASS $?
