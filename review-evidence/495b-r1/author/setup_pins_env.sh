#!/bin/bash
# Pins-only builder environment, following .github/workflows/elaborate.yml:
# Python 3.12, pyyaml pinned to the version the pinned Markdown environment
# carries, exactly sw/litex/litex_pins.txt, scripts/ci_litex_env.py and
# sw/litex/patches/apply.sh, plus the digest-checked sv2v v0.0.12.
# Own HOME, no PYTHONPATH, no host data packages.
# Usage: setup_pins_env.sh <lane> <work root> <python3.12>
set -euo pipefail
lane=$1; work=$2; py=$3
home="$work/pins-home"; venv="$work/pins-venv"; tools="$work/tools"
mkdir -p "$home" "$tools/bin" "$work/tmp"
export HOME="$home" TMPDIR="$work/tmp"
unset PYTHONPATH MILAN_LITEX_PYTHON VIRTUAL_ENV PIP_CACHE_DIR
cd "$lane"
ver=v0.0.12
sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00
curl -fsSL "https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip" -o "$work/tmp/sv2v.zip"
echo "${sha256}  $work/tmp/sv2v.zip" | sha256sum -c -
rm -rf "$work/tmp/sv2v"; unzip -q -o "$work/tmp/sv2v.zip" -d "$work/tmp/sv2v"
install -m755 "$(find "$work/tmp/sv2v" -name sv2v -type f | head -1)" "$tools/bin/sv2v"
"$py" -m venv "$venv"
export PATH="$venv/bin:$tools/bin:/usr/bin:/bin"
python3 --version
sv2v --version
python3 -m pip install --quiet pyyaml==6.0.3
python3 -m pip install --quiet -r sw/litex/litex_pins.txt
python3 -m pip freeze --all
python3 scripts/ci_litex_env.py
sw/litex/patches/apply.sh
python3 -c 'import importlib.util as u; [print(n, u.find_spec(n) is not None) for n in ("pythondata_software_picolibc", "pythondata_software_compiler_rt", "pythondata_cpu_vexiiriscv", "litex", "migen", "litex_boards", "yaml")]'
echo SETUP COMPLETE
