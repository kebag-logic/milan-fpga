#!/bin/bash
# mutants_r738.sh CLONE WORK RECEIPTS: reviewer-planted defects the author's fifteen do not plant, each in its own copy
# of the exact head, run concurrently. A mutant the self-test passes is an escape, reported rather than hidden.
C=$1; W=$2; R=$3; mkdir -p "$W" "$R"
IMG=sw/firmware/ctrl/test/ctrl_plat_image.py
plant() { # name python-replacement-script
  local n=$1; local d=$W/$n
  cp -a --reflink=auto "$C" "$d"
  python3 -I - "$d/$IMG" <<EOF
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text(); o=s
$2
assert s!=o, "anchor missing"
p.write_text(s)
EOF
  [ $? -eq 0 ] || { echo "$n: PLANT FAILED"; return; }
  ( cd "$d" && python3 -B sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 ) > "$R/$n.log" 2>&1
  echo $? > "$R/$n.rc"
}
plant exists-not-isfile 's=s.replace("(flash_map / name).is_file()","(flash_map / name).exists()")' &
plant partial-only-with-archives 's=s.replace("    if flash_map is not None:\n        missing","    if flash_map is not None and any(p.exists() for p in archives):\n        missing")' &
plant refusal-after-prepared 's=s.replace("        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n","").replace("    variant, inc = prepared(tree, args.interfaces, out, args.config)\n","    variant, inc = prepared(tree, args.interfaces, out, args.config)\n    refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n")' &
plant refusal-after-source-tree 's=s.replace("        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n","").replace("    tree = image.source_tree(args.ctrl_source.resolve(), STACK.resolve(), out)\n","    tree = image.source_tree(args.ctrl_source.resolve(), STACK.resolve(), out)\n    refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n")' &
wait
for f in "$R"/*.rc; do n=$(basename "$f" .rc); printf '%s rc=%s plat_green=%s last=%s\n' "$n" "$(cat "$f")" "$(grep -c '^PASS: plat' "$R/$n.log")" "$(tail -1 "$R/$n.log" | cut -c1-150)"; done
