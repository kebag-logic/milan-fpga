#!/usr/bin/env bash
# Engine/ROM probes that need a build and a sweep of tb/aecp_cmds.
# Usage: probe_engine.sh TREE SCRATCH OUTDIR VERILATOR VARIANT
#   TREE      pristine head extraction (never written)
#   VARIANT   echo-hide | echo-control | step-12 | count1-overlength
# Each variant copies TREE to SCRATCH/VARIANT, plants its edit, and records
# rc and output of every step under OUTDIR/VARIANT.*.
set -u
TREE=$1; SCRATCH=$2; OUT=$3; VER=$4; V=$5
mkdir -p "$SCRATCH" "$OUT"
D="$SCRATCH/$V"
rm -rf "$D"; mkdir -p "$D"
(cd "$TREE" && tar --exclude=obj_dir --exclude='*.hex' --exclude=image.bin -cf - .) | tar -xf - -C "$D"
py() { python3 -I -c "$1" "$D"; }
drop_eavl_fields='
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / "hdl/aecp/ucode/gen_ucode.py"
s = p.read_text()
old = ("    u(\x27BUILD_FLD\x27, ra=3, fmt=FMT_D),             # flags                  @24\n"
       "    u(\x27BUILD_FLD\x27, ra=2, fmt=FMT_Q),             # acquired_controller_id @28\n"
       "    u(\x27BUILD_FLD\x27, ra=1, fmt=FMT_Q),             # locked_controller_id   @36\n")
assert s.count(old) == 1, "EAVL anchor"
p.write_text(s.replace(old, "    u(\x27NOP\x27),\n" * 3))
'
add_echo_eavl='
import sys, json, pathlib
p = pathlib.Path(sys.argv[1]) / "hdl/aecp/ucode/aecp_commands.json"
t = json.loads(p.read_text())
t["echo_entries"].append("EAVL")
p.write_text(json.dumps(t, indent=2) + "\n")
'
engine_edit() {  # $1 old, $2 new (python literals)
  py "
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / 'hdl/aecp/KL_aecp_engine.sv'
s = p.read_text(); old = $1; new = $2
assert s.count(old) == 1, 'engine anchor'
p.write_text(s.replace(old, new))
"
}
step() {  # name, dir, command...
  local n=$1 dir=$2; shift 2
  (cd "$dir" && "$@") > "$OUT/$V.$n.log" 2>&1; echo $? > "$OUT/$V.$n.rc"
  echo "$V $n rc=$(cat "$OUT/$V.$n.rc")"
}
case $V in
  echo-hide|echo-control)
    py "$drop_eavl_fields" || exit 3
    [ "$V" = echo-hide ] && { py "$add_echo_eavl" || exit 3; }
    step write "$D" python3 -B scripts/check_aecp_commands.py --write
    step record "$D/tb/aecp_cmds" make VERILATOR="$VER" record
    step gate "$D" python3 -B scripts/check_aecp_commands.py
    step suite "$D/tb/aecp_cmds" make VERILATOR="$VER" run
    ;;
  step-12)
    engine_edit '"                   != (19\x27d20 + ({3\x27d0, desc_ty_r} << 3)))"' \
                '"                   != (19\x27d20 + ({3\x27d0, desc_ty_r} * 19\x27d12)))"' || exit 3
    step suite "$D/tb/aecp_cmds" make VERILATOR="$VER" run
    step record "$D/tb/aecp_cmds" make VERILATOR="$VER" record
    ;;
  count1-overlength)
    # accept a count of one at any length from one record up (a count-dependent
    # over-length drift); the count-zero sweep is unaffected
    engine_edit '"if (({8\x27d0, cmd_r.cdl}\n                   != (19\x27d20 + ({3\x27d0, desc_ty_r} << 3)))"' \
                '"if (((desc_ty_r == 16\x27d1) ? ({8\x27d0, cmd_r.cdl} < 19\x27d28) : ({8\x27d0, cmd_r.cdl}\n                   != (19\x27d20 + ({3\x27d0, desc_ty_r} << 3))))"' || exit 3
    step suite "$D/tb/aecp_cmds" make VERILATOR="$VER" run
    ;;
  *) echo "unknown variant $V"; exit 2;;
esac
