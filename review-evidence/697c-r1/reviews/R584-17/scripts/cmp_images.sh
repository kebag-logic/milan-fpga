#!/bin/bash
# cmp_images.sh : compare-only step of compare_images.sh over the ELFs it built (byte, size, sha256)
set -u
. "$(dirname "$0")/env.sh"
S=$PACKET/scratch/images; n=0; bad=0
diff "$S/head/manifest.sha256" "$S/dev/manifest.sha256" > /dev/null && echo "manifests equal: $(sha256sum < "$S/head/manifest.sha256" | cut -c1-64)" || { echo "MANIFESTS DIFFER"; bad=1; }
while read -r _ f; do n=$((n+1))
  if cmp -s "$S/head/elf/$f" "$S/dev/elf/$f"; then echo "same $(stat -c %s "$S/head/elf/$f") $f"; else echo "BYTES DIFFER $f"; bad=$((bad+1)); fi
done < "$S/head/manifest.sha256"
echo "cmp: $n ELFs compared, $bad differ"
[ "$bad" = 0 ] && [ "$n" = 65 ]
