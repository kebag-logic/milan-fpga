#!/usr/bin/env bash
# Disposable mutation probes for #607 tests. Usage: mutation_probe.sh <clean-clone> <scratch-dir> <litex-python>
# Each mutant is applied to a fresh copy of the clone's working tree (including .git so submodule git queries resolve) and
# sw/builder/test_clock_constraints.py is run; KILLED = test rc != 0.
set -u
SRC=$1; WORK=$2; PY=$3
mkdir -p "$WORK"
run() {  # name file python-replacement-expression
  local name=$1 file=$2 expr=$3 dir="$WORK/m-$1"
  rm -rf "$dir"; mkdir -p "$dir"
  (cd "$SRC" && tar --exclude=sw/builder/out -cf - .) | (cd "$dir" && tar -xf -)
  if ! "$PY" - "$dir/$file" "$expr" <<'PYEOF'
import sys
p, spec = sys.argv[1], sys.argv[2]
old, new = spec.split("\x1f")
t = open(p).read()
if t.count(old) < 1:
    sys.exit("PATTERN NOT FOUND")
open(p, "w").write(t.replace(old, new, 1))
PYEOF
  then echo "$name: NOT-APPLIED"; return; fi
  (cd "$dir" && TMPDIR="$WORK" timeout 300 "$PY" -B sw/builder/test_clock_constraints.py > "$WORK/$name.log" 2>&1)
  local rc=$?
  if [ $rc -ne 0 ]; then echo "$name: KILLED (rc=$rc) $(grep -m1 -E 'Error|error|assert' "$WORK/$name.log" | cut -c1-120)"; else echo "$name: SURVIVED"; fi
  rm -rf "$dir"
}
S=$'\x1f'
run M00-control-unmutated sw/litex/clock_constraints.py "# SPDX-License-Identifier: CERN-OHL-W-2.0${S}# SPDX-License-Identifier: CERN-OHL-W-2.0"
run M01-keep-generic-mask  sw/litex/clock_constraints.py "        commands.remove(generic)${S}        pass"
run M02-bound-80ns         sw/litex/clock_constraints.tcl "set_max_delay 8.000 -datapath_only -from \$eth -to \$clock${S}set_max_delay 80.000 -datapath_only -from \$eth -to \$clock"
run M03-swap-exclusions    sw/litex/clock_constraints.tcl "[list \$eth_mr \$part \$part_mr \$eth]${S}[list \$eth_mr \$eth \$part_mr \$part]"
run M04-drop-hold-fp       sw/litex/clock_constraints.tcl "        set_false_path -hold -from \$clock -to \$eth
${S}"
run M05-regex-no-critical  sw/litex/clock_constraints.py "(?:CRITICAL WARNING|WARNING|ERROR)${S}(?:WARNING|ERROR)"
run M06-drop-log-check     sw/litex/milan_soc.py "        check_implementation_log(Path(builder.gateware_dir) / \"vivado.log\")${S}        pass"
run M07-hook-wrong-board   sw/litex/milan_soc.py "                if board == \"ax7101\":
                    add_eth_constraints${S}                if board == \"ax7101-disabled\":
                    add_eth_constraints"
run M08-hook-fixed-port0   sw/litex/milan_soc.py "platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)${S}platform.lookup_request(\"eth_clocks\", 0).rx)"
run M09-milan-wrong-clkout sw/litex/milan_soc.py "            self.eth_bounded_clocks.append(pll.clkouts[pll.nclkouts - 1].clk)${S}            self.eth_bounded_clocks.append(pll.clkouts[0].clk)"
run M10-drop-idelay-async  sw/litex/milan_soc.py "            self.eth_async_clocks.append(pll.clkouts[pll.nclkouts - 1].clk)
            self.idelayctrl${S}            self.idelayctrl"
run M11-platform-no-subclass sw/litex/platforms/alinx_ax7101.py "            self.toolchain = BoundedEthVivadoToolchain()${S}            pass"
run M12-unguarded-qs       sw/litex/clock_constraints.tcl "    if {[llength \$cells]} {${S}    if {1} {"
run M13-drop-other-fp      sw/litex/clock_constraints.tcl "    if {[llength \$other_mr]} {set_false_path -to \$other_mr}${S}"
run M14-hook-after-opt     sw/litex/clock_constraints.py "    toolchain.pre_optimize_commands.add(${S}    toolchain.pre_placement_commands.add("
run M15-no-datapath-only   sw/litex/clock_constraints.tcl "set_max_delay 8.000 -datapath_only -from \$clock -to \$eth${S}set_max_delay 8.000 -from \$clock -to \$eth"
run M16-no-async-group     sw/litex/clock_constraints.tcl "        set_clock_groups -asynchronous -group \$eth -group \$other${S}        puts skipped"
run M17-drop-inputs-fp     sw/litex/clock_constraints.tcl "        if {[llength \$inputs]} {set_false_path -from \$inputs -to \$targets}${S}"
run M18-ambiguous-accepted sw/litex/clock_constraints.tcl "        if {[llength \$clocks] != 1} {
            error${S}        if {[llength \$clocks] < 1} {
            error"
run M19-no-template-refusal sw/litex/clock_constraints.py "        if commands.count(generic) != 1:${S}        if commands.count(generic) > 1:"
run M20-drop-tdm-async     sw/litex/milan_soc.py "                self.eth_async_clocks.append(audio_tdm_raw)${S}                pass"
