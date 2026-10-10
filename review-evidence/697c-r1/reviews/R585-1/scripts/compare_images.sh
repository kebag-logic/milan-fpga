#!/bin/bash
# Compare every linked ELF of the base and head image runs by SHA-256.
# usage: compare_images.sh <imgdir>   (holds base/ and head/ from images.sh)
cd "$1" || exit 2
same=0; diff=0
while read -r rel; do
  b=$(sha256sum "base/$rel" | cut -d' ' -f1); h=$(sha256sum "head/$rel" 2>/dev/null | cut -d' ' -f1)
  if [ "$b" = "$h" ]; then same=$((same+1)); echo "SAME $b $rel"; else diff=$((diff+1)); echo "DIFF base=$b head=$h $rel"; fi
done < <(cd base && find . -name '*.elf' | sed 's|^\./||' | sort)
nb=$(find base -name '*.elf' | wc -l); nh=$(find head -name '*.elf' | wc -l)
echo "elf: base $nb head $nh, same $same, different $diff"
[ "$diff" -eq 0 ] && [ "$nb" -eq "$nh" ] && [ "$nb" -gt 0 ]
