#!/bin/sh
# Build the reviewer's extra dispatch probe patches from the exact-head engine.
# usage: make_probe_patches.sh <clone> <outdir>
set -eu
clone=$1; out=$2
eng=hdl/aecp/KL_aecp_engine.sv
mkdir -p "$out"
tmp=$(mktemp -d "$out/.tmp.XXXX")
mk() {  # name, python replacement expression (old, new)
  name=$1; old=$2; new=$3
  mkdir -p "$tmp/a/hdl/aecp" "$tmp/b/hdl/aecp"
  cp "$clone/$eng" "$tmp/a/$eng"
  python3 -I - "$tmp/a/$eng" "$tmp/b/$eng" "$old" "$new" <<'EOF'
import sys
src, dst, old, new = sys.argv[1:5]
text = open(src).read()
assert text.count(old) == 1, (old, text.count(old))
open(dst, "w").write(text.replace(old, new))
EOF
  (cd "$tmp" && diff -u --label "a/$eng" --label "b/$eng" "a/$eng" "b/$eng" > "$out/$name.patch") || true
  test -s "$out/$name.patch"
}
mk p-gate-ignores-bit12 \
  "else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NOTIMPL_C;" \
  "else if ((cfg_ix_r & 16'hEFFF) != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NOTIMPL_C;"
mk p-gate-on-desc-ty \
  "else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NOTIMPL_C;" \
  "else if (desc_ty_r != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NOTIMPL_C;"
mk p-wrong-type-arm-empty \
  "else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NOTIMPL_C;
                echo_r <= 1'b1;
              end else begin
                upc_r  <= UPC_GAVB_C;" \
  "else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin
              end else begin
                upc_r  <= UPC_GAVB_C;"
mk p-floor-15 \
  "if (cmd_r.cdl < 11'd16)                 upc_r <= UPC_BADARG_C;
              else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin" \
  "if (cmd_r.cdl < 11'd15)                 upc_r <= UPC_BADARG_C;
              else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin"
rm -rf "$tmp"
ls -l "$out"
