#!/usr/bin/env bash
# Plant one fault in a scratch copy of a processor tree and run its
# syn/yosys/run.sh. Usage:
#   yosys_fault.sh <src-tree> <work-dir> <kind> <module> [<module2>]
# kinds:
#   inst      an instance of an undeclared module before <module>'s endmodule
#   port      an instance of declared module <module2> with a port it lacks
#   param     an instance of declared module <module2> with a parameter it lacks
#   drop      remove <module> from the tops array
#   bogus     add the name <module> (declared nowhere) to the tops array
#   allv      a syntax fault in all.v inside <module>, via an sv2v shim
#   newmod    add a new file declaring module <module> with "module" and its
#             name on separate lines, holding an undeclared instance
#   fatal     a module-scope $fatal guard that always fires, in <module>
#   killonce  SIGKILL the first parse-once yosys after <module>'s @@begin
#   rcone     yosys exits 1 after an otherwise clean elaboration run
# Writes <work-dir>/{gate.log,rc}. Extra env passes through (YOSYS_MALLOC).
set -u
src=$1 w=$2 kind=$3 m=${4-} m2=${5-}
rm -rf "$w"; mkdir -p "$w"; cp -a "$src" "$w/tree"; t="$w/tree"
file_of() { grep -rlE "^[[:space:]]*module[[:space:]]+$1\b" "$t/hdl" --include='*.sv' | head -1; }
plant_before_endmodule() { # file, module, text
  python3 - "$1" "$2" "$3" <<'PY'
import re, sys
f, mod, text = sys.argv[1:4]
s = open(f).read()
i = re.search(r'^\s*module\s+' + mod + r'\b', s, re.M).start()
j = s.index('endmodule', i)
s = s[:j] + text + '\n' + s[j:]
open(f, 'w').write(s)
PY
}
shim=""
case "$kind" in
  fatal) plant_before_endmodule "$(file_of $m)" $m "  if (1) begin : g_r449_fatal \$fatal(1, \"r449 planted\"); end" ;;
  inst)  for mm in $m $m2; do plant_before_endmodule "$(file_of $mm)" $mm "  r449_absent_module u_r449_absent ();"; done ;;
  port)  plant_before_endmodule "$(file_of $m)" $m "  $m2 u_r449_port (.r449_no_such_port(1'b0));" ;;
  param) plant_before_endmodule "$(file_of $m)" $m "  $m2 #(.R449_NO_SUCH_P(1)) u_r449_param ();" ;;
  drop)  sed -i -E "/^tops=\(/,/\)$/ s/(^|[ (])$m([ )])/\1\2/" "$t/syn/yosys/run.sh" ;;
  bogus) sed -i -E "s/^tops=\(/tops=($m /" "$t/syn/yosys/run.sh" ;;
  newmod) printf '%s\n' "module" "  $m (input wire clk_i);" "  r449_absent_module u_r449_absent ();" "endmodule" > "$t/hdl/top/$m.sv" ;;
  allv|killonce|rcone) shim="$w/shim"; mkdir -p "$shim" ;;
esac
case "$kind" in
  allv)
    cat > "$shim/sv2v" <<SH
#!/usr/bin/env bash
"$(command -v sv2v)" "\$@" | awk -v m="$m" '{print} \$0 ~ "^module "m"[^A-Za-z0-9_]" {getline; print; print "  @@@ r449 syntax fault"}'
exit \${PIPESTATUS[0]}
SH
    chmod +x "$shim/sv2v" ;;
  killonce)
    cat > "$shim/yosys" <<SH
#!/usr/bin/env bash
if [ "\${1-}" = -q ] && [ "\${2-}" = -s ] && [ ! -e "$w/killed" ]; then
  "$(command -v yosys)" "\$@" & p=\$!
  while kill -0 \$p 2>/dev/null; do
    if grep -qxF "@@begin $m" gate.log 2>/dev/null; then touch "$w/killed"; kill -9 \$p; break; fi
    sleep 0.05
  done
  wait \$p; exit \$?
fi
exec "$(command -v yosys)" "\$@"
SH
    chmod +x "$shim/yosys" ;;
  rcone)
    cat > "$shim/yosys" <<SH
#!/usr/bin/env bash
"$(command -v yosys)" "\$@"; r=\$?
if [ "\${1-}" = -q ] && [ "\${2-}" = -s ]; then exit 1; fi
exit \$r
SH
    chmod +x "$shim/yosys" ;;
esac
( [ -n "$shim" ] && export PATH="$shim:$PATH"; cd "$t" && ./syn/yosys/run.sh ) > "$w/gate.log" 2>&1
echo $? > "$w/rc"
