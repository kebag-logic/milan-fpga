#!/bin/sh
# Reproduce focused read-only checks. Requires installed Python, PyYAML, Perl, Node and Tcl.
set -eu
packet=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
checkout=${1:?Usage: replay.sh /absolute/path/to/exact-head-checkout}
export PYTHONDONTWRITEBYTECODE=1
python3 "$packet/fetch_evidence.py"
python3 "$packet/verify_evidence.py" "$checkout"
python3 "$packet/check_lists.py" "$checkout"
python3.12 "$packet/probe_inline.py" "$checkout"
python3.12 "$packet/probe_loader_error.py" "$checkout"
python3 "$packet/verify_tree.py" "$checkout"
