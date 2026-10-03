#!/usr/bin/env bash
# R449-2: header-layout probes of the Yosys gate's census, in a scratch copy.
# Usage: census_probe.sh <src-tree> <work-dir> <form> [top]
# Adds hdl/top/KL_r449_<form>.sv declaring one module whose header uses <form>,
# holding an instance of an undeclared module, and runs that tree's
# syn/yosys/run.sh. With "top", the module's name is also added to `tops`.
# forms:
#   split      `module` alone on its line, the name on the next
#   auto       `module automatic` alone on its line, the name on the next
#   cmtblock   `module /* c */ NAME`
#   cmtline    `module // c` then the name on the next line
#   macro      `macromodule NAME`
#   attr       `(* keep_hierarchy = "yes" *)` before `module NAME`, same line
#   attrline   `(* keep_hierarchy = "yes" *)` on its own line, `module NAME` next
#   allvauto   `module automatic NAME`, in tops, plus a syntax fault that an
#              sv2v shim plants in all.v right after that module's header
# Writes <work-dir>/{gate.log,rc,module.sv,census.txt}.
set -u
src=$1 w=$2 form=$3 top=${4-}
rm -rf "$w"; mkdir -p "$w"; cp -a "$src" "$w/tree"; t="$w/tree"
m="KL_r449_$form"; body="  r449_absent_module u_r449_absent ();"
case "$form" in
  split)    hdr=$'module\n  '"$m"' (input wire clk_i);' ;;
  auto|allvauto) hdr=$'module automatic\n  '"$m"' (input wire clk_i);' ;;
  cmtblock) hdr="module /* r449 */ $m (input wire clk_i);" ;;
  cmtline)  hdr=$'module // r449\n  '"$m"' (input wire clk_i);' ;;
  macro)    hdr="macromodule $m (input wire clk_i);" ;;
  attr)     hdr="(* keep_hierarchy = \"yes\" *) module $m (input wire clk_i);" ;;
  attrline) hdr=$'(* keep_hierarchy = "yes" *)\nmodule '"$m"' (input wire clk_i);' ;;
  *) echo "unknown form $form" >&2; exit 2 ;;
esac
[ "$form" = allvauto ] && { top=top; body=""; }
printf '%s\n%s\nendmodule\n' "$hdr" "$body" > "$t/hdl/top/$m.sv"
cp "$t/hdl/top/$m.sv" "$w/module.sv"
[ -n "$top" ] && sed -i -E "s/^tops=\(/tops=($m /" "$t/syn/yosys/run.sh"
shim=""
if [ "$form" = allvauto ]; then
  shim="$w/shim"; mkdir -p "$shim"
  cat > "$shim/sv2v" <<SH
#!/usr/bin/env bash
"$(command -v sv2v)" "\$@" | awk -v m="$m" '{print} \$0 ~ "^module .*"m"[^A-Za-z0-9_]" {print "  @@@ r449 syntax fault"}'
exit \${PIPESTATUS[0]}
SH
  chmod +x "$shim/sv2v"
fi
# What the census regex sees in sv2v's lowering of this one file.
sv2v "$t/hdl/top/$m.sv" 2>&1 | grep -n 'module' > "$w/census.txt" || true
( [ -n "$shim" ] && export PATH="$shim:$PATH"; cd "$t" && ./syn/yosys/run.sh ) > "$w/gate.log" 2>&1
echo $? > "$w/rc"
