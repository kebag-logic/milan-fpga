#!/usr/bin/env bash
# Scratch: pack each tracked config through avdecc/gen_aemi_image.py (the CLI
# caller of build(), lint on by default), from a scratch parent root.
set -u
out=$(mktemp -d)
fail=0
for cfg in configs/endstation_*.yaml; do
  name=$(basename "$cfg" .yaml)
  python3 -B -c "
import json, sys
sys.path[:0] = ['.', 'sw/builder']
import endstation_builder as eb
json.dump(eb.emit_aem_overlay(eb.load_config('$cfg')), open('$out/$name.json', 'w'))"
  if python3 -B avdecc/gen_aemi_image.py --overlay "$out/$name.json" -o "$out/$name.bin" -m "$out/$name.map" > "$out/$name.log" 2>&1; then
    echo "$name: rc 0, $(grep -c '^  waiver ' "$out/$name.map") waiver(s) listed, $(grep '^semantic lint' "$out/$name.map")"
  else
    echo "$name: REFUSED"; cat "$out/$name.log"; fail=1
  fi
done
rm -rf "$out"
exit $fail
