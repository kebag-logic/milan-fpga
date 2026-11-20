#!/bin/bash
# release_identity.sh OLD:NEW ...: the AX7101 shipping (all-fabric) export at two heads compared (R865-4-F2), each pair
# of release_export.sh outputs under $SCRATCH/r5rel12/<head>/ax7101, both elaborated in the same repository path
# ($REPO). For each pair:
#   - cmp_export.py: every file, each export's absolute roots replaced first; the counts, each differing file, and for
#     differing Verilog whether it is equal outside its comments;
#   - LOADED: the sha256 of each file the image loads, on both sides: the BIOS (software/bios/bios.bin), the AEM blob
#     (aem_desc.bin) and every memory init file (gateware/*.init: the ROM, SRAM and main memory);
#   - SOURCES: the files the two heads differ in (git diff --stat).
# Exit 0 when every loaded file is equal and every differing gateware file is equal outside its comments; 1 otherwise.
# Run it as: bash release_identity.sh A:B ... > LOG 2>&1; echo $? > LOG.rc
set -u
S=${SCRATCH:-<scratch>}
REPO=${REPO:-$S/clones/r8-gate}
LANE=${LANE:-<lane>}
echo "release_identity.sh $(date -Iseconds)"
# the repository an export was elaborated in, read from its dry run (its soc_params.json path), else $REPO
repo_of() { local r; r=$(grep -m1 -o '/[^ "]*/sw/builder/out/' "$1/ax7101-dry-run.log" 2>/dev/null | sed 's#/sw/builder/out/$##')
            echo "${r:-$REPO}"; }
rc=0
for pair in "$@"; do
  old=${pair%%:*} new=${pair#*:}
  A=$S/r5rel12/$old/ax7101 B=$S/r5rel12/$new/ax7101 RA=$(repo_of "$S/r5rel12/$old") RB=$(repo_of "$S/r5rel12/$new")
  echo "== $old -> $new (elaborated in $RA and $RB)"
  echo "-- SOURCES: git diff --shortstat $old $new; the release recipe's inputs it touches (hdl/, syn/, sw/litex/, configs/)"
  git -C "$LANE" diff --shortstat "$old" "$new"
  git -C "$LANE" diff --stat "$old" "$new" -- hdl syn sw/litex configs | tail -n 25
  echo "-- cmp_export.py"
  out=$(python3 -I "$S/bin/cmp_export.py" "$A" "$RA,$A" "$B" "$RB,$B"); r=$?
  echo "$out"
  [ $r = 0 ] || { echo "cmp_export rc=$r"; rc=1; }
  bad=$(echo "$out" | grep '^  differs: gateware/' | grep -v '(equal outside its comments)')
  if [ -n "$bad" ]; then echo "GATEWARE: a differing file not equal outside its comments: $bad"; rc=1
  else echo "GATEWARE: every differing gateware file is equal outside its comments"; fi
  echo "-- LOADED"
  for f in software/bios/bios.bin aem_desc.bin $(cd "$B" && find gateware -name '*.init' | sort); do
    a=$(sha256sum < "$A/$f" | cut -c1-64) b=$(sha256sum < "$B/$f" | cut -c1-64)
    if [ "$a" = "$b" ]; then v=EQUAL; else v=DIFFERS; rc=1; fi
    echo "LOADED $f $old $a $new $b $v"
  done
done
echo "END rc=$rc $(date -Iseconds)"
exit $rc
