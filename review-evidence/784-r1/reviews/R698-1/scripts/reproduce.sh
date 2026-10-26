#!/bin/sh
# Run from the packet; pass an isolated exact-head clone as the only argument.
set -eu
packet_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
repo_dir=$(CDPATH= cd -- "$1" && pwd)
mkdir -p "$packet_dir/scratch" "$packet_dir/receipts"
python3 -m venv --system-site-packages "$packet_dir/scratch/venv"
"$packet_dir/scratch/venv/bin/python" -m pip install --ignore-installed --require-hashes -r "$repo_dir/tools/markdown/requirements.txt"
# System Python must supply PyYAML; install no global packages.
python3 -I -c 'import yaml; print(yaml.__version__)'
python3 "$packet_dir/scripts/verify_tree.py" "$repo_dir"
python3 "$packet_dir/scripts/sandbox.py" "$repo_dir" runner-contract bash -c 'python3 scripts/act_ci.py --selftest; first=$?; install -m 0555 scripts/act_ci.py /work/act_ci.py; python3 -I /work/act_ci.py --selftest --worktree /repo; second=$?; printf "direct_rc=%s installed_rc=%s\n" "$first" "$second"; test "$first" -eq 0 && test "$second" -eq 0'
python3 "$packet_dir/scripts/sandbox.py" "$repo_dir" ci-events bash -c 'python3 scripts/ci_events.py --check && python3 scripts/ci_events.py --selftest'
python3 "$packet_dir/scripts/sandbox.py" "$repo_dir" docs-gates-complete python3 /review/docs_gates.py
python3 "$packet_dir/scripts/sandbox.py" "$repo_dir" label-probes python3 /review/label_probes.py
for mutation in drop-2404-from-platform-map map-2404-to-act-default-image accept-any-ubuntu-prefix; do
  python3 "$packet_dir/scripts/sandbox.py" "$repo_dir" "$mutation" python3 /review/mutate.py "$mutation"
done
python3 "$packet_dir/scripts/verify_tree.py" "$repo_dir"
