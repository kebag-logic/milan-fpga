#!/bin/sh
# R246-2 positive control for write_probe.py and snap.py: through a grandchild,
# touch a TRACKED header, rewrite an ignored shared file, and create/remove a
# transient mkdtemp-style directory, all from the suite dir like a real leg.
sh -c '
  touch ../../../configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh
  mkdir -p ../../../sw/builder/__pycache__
  echo planted > ../../../sw/builder/__pycache__/planted-shared.pyc
  d=$(mktemp -d "${TMPDIR:-/tmp}/milan_nxn_XXXXXX")
  echo x > "$d/image.bin"
  rm -rf "$d"
'
