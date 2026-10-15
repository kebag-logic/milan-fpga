#!/usr/bin/env bash
# Run from any directory; argument 1 is the unmodified reviewed checkout.
# Requires Linux x86-64, Python 3.14+, cc with static libc, and network only for
# checksum-pinned public package/parser preparation. No Docker or installation.
set -euo pipefail
review_root=$(realpath "${1:?review checkout required}")
packet_dir=$(cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$packet_dir/scratch"
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$packet_dir/scratch"
python3 "$packet_dir/reference_tools.py" "$review_root"
python3 "$review_root/ci/image/prepare_parser.py" --output "$packet_dir/scratch/shfmt"
export CI_IMAGE_SHFMT="$packet_dir/scratch/shfmt"
reference_python="$packet_dir/scratch/reference/root/usr/bin/python3.12"
for script in run_controls.py independent_probes.py live_gap_probes.py drift_controls.py; do
  PYTHONHOME="$packet_dir/scratch/reference/root/usr" PYTHONPATH="$packet_dir/scratch/reference/python" "$reference_python" "$packet_dir/$script" "$review_root"
done
python3 "$packet_dir/audit_pip_probe.py" "$review_root"
python3 "$packet_dir/verify_tree.py" "$review_root"
