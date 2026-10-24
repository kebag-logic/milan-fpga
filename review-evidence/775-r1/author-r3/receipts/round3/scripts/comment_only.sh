#!/bin/bash
# comment_only.sh <lane> <out>: KL_avtp_rx_monitor_ctx.sv at c2a080ae and 220b51f2,
# identical after comment stripping by two methods: verilator -E -P (blank lines
# dropped) and the reviewer's strip_sv_comments.py; plus the paths that changed
. <scratch>/scripts/env.sh
cd "$1" || exit 2
O=$2; mkdir -p "$O"; W=$(mktemp -d)
F=hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv
{
for rev in c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6; do
  git show "$rev:$F" > "$W/$rev.sv"
  verilator -E -P "$W/$rev.sv" | grep -v '^[[:space:]]*$' > "$W/$rev.pp"
  python3 -I <scratch>/packet/strip_sv_comments.py "$W/$rev.sv" > "$W/$rev.strip"
  echo "$rev verilator -E -P: $(wc -l < "$W/$rev.pp") lines sha256 $(sha256sum < "$W/$rev.pp" | cut -d' ' -f1)"
  echo "$rev strip_sv_comments.py: $(wc -l < "$W/$rev.strip") lines sha256 $(sha256sum < "$W/$rev.strip" | cut -d' ' -f1)"
done
echo "--- git diff c2a080ae 220b51f2 -- $F"
git diff c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 -- "$F"
echo "--- paths changed c2a080ae..220b51f2"
git diff --stat c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6
echo "--- hdl/ syn/ configs/ sw/ and gitlinks changed"
git diff --name-only c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 -- hdl syn configs sw
git diff --raw c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 | awk '$2=="160000"||$1==":160000"'
cmp "$W/c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83.pp" "$W/220b51f2eb50c32f830e0b5a8ee1ce138b218bb6.pp" && echo "verilator -E -P: IDENTICAL"
cmp "$W/c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83.strip" "$W/220b51f2eb50c32f830e0b5a8ee1ce138b218bb6.strip" && echo "strip_sv_comments.py: IDENTICAL"
} > "$O/comment-only.txt" 2>&1
rm -rf "$W"
cat "$O/comment-only.txt"
