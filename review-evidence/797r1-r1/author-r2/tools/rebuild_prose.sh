#!/bin/sh
# Rebuild the descriptions and the design record from the round-1 descriptions, then regenerate.
set -e
R=$1; PY=$2; T=$(dirname "$0"); SRC=$3; ORDER=$4
"$PY" "$T/migrate_notes.py" "$R" "$SRC" "$ORDER"
"$PY" "$T/concise_fields.py" "$R"
"$PY" "$T/concise_notes.py" "$R"
cd "$R"
"$PY" scripts/gen_toc.py --write docs/design/CSR_REGISTER_NOTES.md
"$PY" "$T/fill_toc.py" "$R"
"$PY" scripts/gen_register_reference.py --write
