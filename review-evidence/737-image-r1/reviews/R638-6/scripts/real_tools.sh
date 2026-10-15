#!/usr/bin/env bash
# Run each persisted probe's workflow command with the image's own bash and make, offline.
# Usage: [DOCKER="docker"] real_tools.sh PROBE_DIR IMAGE_REF  -> prints one block per probe; brand_new_command is not installed,
# so "brand_new_command: command not found" / "No such file" proves the real tool executed it.
set -u
dir=$1; image=$2
for p in "$dir"/*/; do
  name=$(basename "$p")
  echo "=== $name"
  ${DOCKER:-docker} run --rm --network none --user 1000:1000 \
    --mount "type=bind,src=$p,dst=/w" --workdir /w "$image" \
    bash -e -o pipefail -c 'cp -a /w /tmp/w && cd /tmp/w && bash -e .probe-run.sh' 2>&1 | sed 's/^/    /' | head -12
  echo "    rc=${PIPESTATUS[0]}"
done
