#!/usr/bin/env bash
# Disposable mutation probes for the #607 tests at a given head.
# Round-3 copy of the round-2 campaign (M00-M32 unchanged) plus M33+ against the #607 F2 fix.
# Usage: mutation_probe3.sh <clean-clone> <scratch-dir> <litex-python> [jobs] [name-regex]
# A spec may carry several old<US>new pairs separated by <GS> (\x1d); all must apply.
# Each mutant is applied to a fresh copy of the clone's working tree (including .git so
# submodule git queries resolve) and sw/builder/test_clock_constraints.py (the builder-bank
# entry, which now also runs test_shipping_clock_constraints.py) is run.
# KILLED = test rc != 0. M00 is the unmutated control and must SURVIVE (rc 0).
# Mutant names M01-M20 keep their round-1 meaning; M21+ are round-2 additions.
set -u
SRC=$1; WORK=$2; PY=$3; JOBS=${4:-8}; FILTER=${5:-.}
mkdir -p "$WORK"
export SRC WORK PY
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
S=$'\x1f'
SPECS="$WORK/specs"; : > "$SPECS"
G=$'\x1d'
add() { [[ $1 =~ $FILTER ]] || return 0; printf '%s\x1e%s\x1e%s\0' "$1" "$2" "$3" >> "$SPECS"; }  # name file old<US>new[<GS>old<US>new]
add M00-control-unmutated sw/litex/clock_constraints.py "# SPDX-License-Identifier: CERN-OHL-W-2.0${S}# SPDX-License-Identifier: CERN-OHL-W-2.0"
add M01-keep-generic-mask  sw/litex/clock_constraints.py "        commands.remove(generic)${S}        pass"
add M02-bound-80ns         sw/litex/clock_constraints.tcl "set_max_delay 8.000 -datapath_only -from \$eth -to \$clock${S}set_max_delay 80.000 -datapath_only -from \$eth -to \$clock"
add M03-swap-exclusions    sw/litex/clock_constraints.tcl "[list \$eth_mr \$part \$part_mr \$eth]${S}[list \$eth_mr \$eth \$part_mr \$part]"
add M04-drop-hold-fp       sw/litex/clock_constraints.tcl "        set_false_path -hold -from \$clock -to \$eth
${S}"
add M05-regex-no-critical  sw/litex/clock_constraints.py "(?:CRITICAL WARNING|WARNING|ERROR)${S}(?:WARNING|ERROR)"
add M06-drop-log-check     sw/litex/milan_soc.py "        check_implementation_log(Path(builder.gateware_dir) / \"vivado.log\")${S}        pass"
add M07-hook-wrong-board   sw/litex/milan_soc.py "                if board == \"ax7101\":
                    add_eth_constraints${S}                if board == \"ax7101-disabled\":
                    add_eth_constraints"
add M08-hook-fixed-port0   sw/litex/milan_soc.py "platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)${S}platform.lookup_request(\"eth_clocks\", 0).rx)"
add M09-milan-wrong-clkout sw/litex/milan_soc.py "            self.eth_bounded_clocks.append(pll.clkouts[pll.nclkouts - 1].clk)${S}            self.eth_bounded_clocks.append(pll.clkouts[0].clk)"
add M10-drop-idelay-async  sw/litex/milan_soc.py "            self.eth_async_clocks.append(pll.clkouts[pll.nclkouts - 1].clk)
            self.idelayctrl${S}            self.idelayctrl"
add M11-platform-no-subclass sw/litex/platforms/alinx_ax7101.py "            self.toolchain = BoundedEthVivadoToolchain()${S}            pass"
add M12-unguarded-qs       sw/litex/clock_constraints.tcl "    if {[llength \$cells]} {${S}    if {1} {"
add M13-drop-other-fp      sw/litex/clock_constraints.tcl "    if {[llength \$other_mr]} {set_false_path -to \$other_mr}${S}"
add M14-hook-after-opt     sw/litex/clock_constraints.py "    toolchain.pre_optimize_commands.add(${S}    toolchain.pre_placement_commands.add("
add M15-no-datapath-only   sw/litex/clock_constraints.tcl "set_max_delay 8.000 -datapath_only -from \$clock -to \$eth${S}set_max_delay 8.000 -from \$clock -to \$eth"
add M16-no-async-group     sw/litex/clock_constraints.tcl "        set_clock_groups -asynchronous -group \$eth -group \$other${S}        puts skipped"
add M17-drop-inputs-fp     sw/litex/clock_constraints.tcl "        if {[llength \$inputs]} {set_false_path -from \$inputs -to \$targets}${S}"
add M18-ambiguous-accepted sw/litex/clock_constraints.tcl "        if {[llength \$clocks] != 1} {
            error${S}        if {[llength \$clocks] < 1} {
            error"
add M19-no-template-refusal sw/litex/clock_constraints.py "        if commands.count(generic) != 1:${S}        if commands.count(generic) > 1:"
add M20-drop-tdm-async     sw/litex/milan_soc.py "                self.eth_async_clocks.append(audio_tdm_raw)${S}                pass"
# --- round 2 additions ---
add M21-call-deleted-in-guard sw/litex/milan_soc.py "                    add_eth_constraints(platform, self.crg,
                                        platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)${S}                    pass"
add M22-guard-and-not-mac  sw/litex/milan_soc.py "                if board == \"ax7101\":
                    add_eth_constraints${S}                if board == \"ax7101\" and not with_mac:
                    add_eth_constraints"
add M23-guard-board-arty   sw/litex/milan_soc.py "                if board == \"ax7101\":
                    add_eth_constraints${S}                if board == \"arty\":
                    add_eth_constraints"
add M24-hook-only-port-e1  sw/litex/milan_soc.py "                if board == \"ax7101\":
                    add_eth_constraints${S}                if board == \"ax7101\" and eth_phy_index == 0:
                    add_eth_constraints"
add M25-hook-duplicated    sw/litex/milan_soc.py "                    add_eth_constraints(platform, self.crg,
                                        platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)${S}                    add_eth_constraints(platform, self.crg,
                                        platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)
                    add_eth_constraints(platform, self.crg,
                                        platform.lookup_request(\"eth_clocks\", eth_phy_index).rx)"
add M26-bounded-sys-only   sw/litex/milan_soc.py "            self.eth_bounded_clocks.append(pll.clkouts[pll.nclkouts - 1].clk)${S}            pass"
add M27-hook-after-place   sw/litex/clock_constraints.py "    toolchain.pre_optimize_commands.add(${S}    toolchain.pre_routing_commands.add("
add M28-drop-5201-gate     sw/litex/clock_constraints.py "12-(?:4739|5201)${S}12-(?:4739)"
add M29-no-quarantine      sw/litex/clock_constraints.py "            bitstream.replace(rejected)${S}            pass"
add M30-quarantine-not-on-missing-log sw/litex/clock_constraints.py "    except (OSError, RuntimeError):${S}    except RuntimeError:"
add M31-quarantine-wrong-dir sw/litex/clock_constraints.py "        for bitstream in path.parent.glob(\"*.bit\"):${S}        for bitstream in path.parent.parent.glob(\"*.bit\"):"
add M32-toolchain-swap-dropped-late sw/litex/platforms/alinx_ax7101.py "        if toolchain == \"vivado\":
            # Replace${S}        if toolchain == \"vivado-disabled\":
            # Replace"

# --- round 3 additions: the F2 fix in sw/builder/test_shipping_clock_constraints.py ---
TS=sw/builder/test_shipping_clock_constraints.py
add M33-forward-bios-includes $TS "            super()._generate_includes(with_bios=False)${S}            super()._generate_includes(with_bios=with_bios)"
add M34-include-override-removed $TS "        def _generate_includes(self, with_bios: bool = True) -> None:${S}        def _generate_includes_unused(self, with_bios: bool = True) -> None:"
add M35-guard-not-installed $TS "    sys.meta_path.insert(0, FirmwareDataRefused())${S}    pass"
add M36-guard-not-installed-and-forward-bios $TS "    sys.meta_path.insert(0, FirmwareDataRefused())${S}    pass${G}            super()._generate_includes(with_bios=False)${S}            super()._generate_includes(with_bios=with_bios)"
add M37-guard-wrong-prefix-and-forward-bios $TS "        if name.startswith(\"pythondata_software_\"):${S}        if name.startswith(\"pythondata_softwar3_\"):${G}            super()._generate_includes(with_bios=False)${S}            super()._generate_includes(with_bios=with_bios)"
add M38-guard-appended-last-and-forward-bios $TS "    sys.meta_path.insert(0, FirmwareDataRefused())${S}    sys.meta_path.append(FirmwareDataRefused())${G}            super()._generate_includes(with_bios=False)${S}            super()._generate_includes(with_bios=with_bios)"
add M39-include-step-skipped $TS "            super()._generate_includes(with_bios=False)${S}            pass"
add M40-includes-assert-dropped $TS "            assert includes == [True], f\"builder bypassed the probed include step: {includes}\"${S}            pass"
add M41-includes-assert-dropped-and-step-skipped $TS "            assert includes == [True], f\"builder bypassed the probed include step: {includes}\"${S}            pass${G}            includes.append(with_bios)
            super()._generate_includes(with_bios=False)${S}            includes.append(with_bios)"
add M42-probe-bypasses-real-build $TS "            namespace = super().build(**kwargs)${S}            namespace = self.soc.build(build_dir=self.gateware_dir, **kwargs)"
add M44-include-override-removed-and-guard-not-installed $TS "        def _generate_includes(self, with_bios: bool = True) -> None:${S}        def _generate_includes_unused(self, with_bios: bool = True) -> None:${G}    sys.meta_path.insert(0, FirmwareDataRefused())${S}    pass"

one() {
  local spec=$1 name file expr dir
  name=${spec%%$'\x1e'*}; spec=${spec#*$'\x1e'}; file=${spec%%$'\x1e'*}; expr=${spec#*$'\x1e'}
  dir="$WORK/m-$name"
  rm -rf "$dir"; mkdir -p "$dir"
  (cd "$SRC" && tar --exclude=sw/builder/out -cf - .) | (cd "$dir" && tar -xf -)
  if ! "$PY" - "$dir/$file" "$expr" <<'PYEOF'
import sys
p, spec = sys.argv[1], sys.argv[2]
t = open(p).read()
for pair in spec.split("\x1d"):
    old, new = pair.split("\x1f")
    if t.count(old) < 1:
        sys.exit("PATTERN NOT FOUND")
    t = t.replace(old, new, 1)
open(p, "w").write(t)
PYEOF
  then echo "$name: NOT-APPLIED"; rm -rf "$dir"; return; fi
  mkdir -p "$WORK/tmp-$name"
  (cd "$dir" && TMPDIR="$WORK/tmp-$name" PATH="$(dirname "$PY"):/usr/bin:/bin" \
     timeout 2700 "$PY" -B sw/builder/test_clock_constraints.py > "$WORK/$name.log" 2>&1)
  local rc=$?
  if [ $rc -ne 0 ]; then
    echo "$name: KILLED (rc=$rc) $(grep -E 'AssertionError|RuntimeError|Error:' "$WORK/$name.log" | grep -v '^\[constraints\] quarantined' | tail -1 | cut -c1-160)"
  else echo "$name: SURVIVED"; fi
  rm -rf "$dir" "$WORK/tmp-$name"
}
export -f one
xargs -0 -P "$JOBS" -I{} bash -c 'one "$@"' _ {} < "$SPECS" | sort
