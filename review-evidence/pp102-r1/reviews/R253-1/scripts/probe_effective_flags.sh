#!/bin/sh
# Effective-flag equivalence probe for the pp_top VID-fixture build.
# usage: probe_effective_flags.sh BASE_TREE HEAD_TREE OUTDIR
# Verilates (no C++ build) the fixture recipe of each tree exactly as its
# Makefile spells it (make -n prints the recipe; only the verilator line with
# --Mdir obj_vid is replayed, with --Mdir redirected into OUTDIR), then:
#  1. prints each generated VM_USER_CFLAGS;
#  2. asks the host C++ compiler which warnings are enabled under the full
#     Verilator-generated + user flag set (-Q --help=warnings) for each tree
#     and diffs the two answers.
# Requires VERILATOR (scoped 5.050 wrapper, jobs capped by the caller) and CXX.
set -eu
base=$1 head=$2 out=$3
mkdir -p "$out"
for side in base head; do
  eval tree=\$$side
  mdir="$out/obj_vid_$side"
  mkdir -p "$mdir"
  # The fixture recipe line as make would run it (VERILATOR substituted).
  # make -n keeps the recipe's backslash-newline continuations; join them.
  line=$(cd "$tree/tb/pp_top" && make -n run VERILATOR=VERILATOR_PLACEHOLDER \
         | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' | grep -- '--Mdir obj_vid')
  echo "[$side] recipe: $line"
  # Drop --build and --exe's build step: verilate only, into $mdir.
  cmd=$(printf '%s\n' "$line" | sed -e "s#^VERILATOR_PLACEHOLDER#\"\$VERILATOR\"#" \
        -e 's# --build # #' -e "s#--Mdir obj_vid#--Mdir '$mdir'#")
  (cd "$tree/tb/pp_top" && eval "$cmd" >"$out/verilate_$side.log" 2>&1)
  grep '^VM_USER_CFLAGS' -A6 "$mdir/Vpp_top_wrap.mk" | sed "s#$tree#<$side-tree>#g" \
    | tee "$out/vm_user_cflags_$side.txt"
  # Every flag the generated makefile hands the compiler for a model TU
  # (verilated.mk: $(CXX) $(OPT_FAST) $(CXXFLAGS) $(CPPFLAGS) ...).
  eval "set -- $(make -s -C "$mdir" -f Vpp_top_wrap.mk --eval='pflags: ; @echo $(OPT_FAST) $(CXXFLAGS) $(CPPFLAGS)' pflags)"
  printf '%s\n' "$@" | grep -E '^-(W|std|O|D)' | sed "s#$tree#<$side-tree>#g" > "$out/cxx_flags_$side.txt"
  ${CXX:-c++} "$@" -Q --help=warnings > "$out/enabled_warnings_$side.txt" 2>&1
  echo "[$side] enabled warnings (-Q --help=warnings '[enabled]' rows): $(grep -c '\[enabled\]' "$out/enabled_warnings_$side.txt")"
done
echo "== diff of compiler flag lists (base -> head)"
diff "$out/cxx_flags_base.txt" "$out/cxx_flags_head.txt" || true
echo "== diff of enabled-warning tables (base -> head)"
if diff "$out/enabled_warnings_base.txt" "$out/enabled_warnings_head.txt"; then
  echo "IDENTICAL: the fixture build's effective warning set is unchanged"
else
  echo "DIFFERENT"; exit 1
fi
