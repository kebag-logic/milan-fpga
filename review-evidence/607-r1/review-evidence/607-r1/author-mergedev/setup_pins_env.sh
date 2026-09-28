#!/bin/sh
# Build the pins-only elaboration environment the way .github/workflows/elaborate.yml
# builds it, isolated under physical data storage with its own HOME, so nothing from
# the bench interpreter, its data packages or its caches can be reached.
# Usage: setup_pins_env.sh <lane> <work root>
set -eu
lane=$1
work=$2
home="$work/pins-home"
venv="$work/pins-venv"
tools="$work/pins-tools"
mkdir -p "$home" "$tools" "$work/tmp"
export HOME="$home" TMPDIR="$work/tmp"
unset PYTHONPATH MILAN_LITEX_PYTHON VIRTUAL_ENV PIP_CACHE_DIR
cd "$lane"

echo "== interpreter (actions/setup-python 3.12 equivalent)"
$WORKSPACE_HOME/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/bin/python3.12 -m venv "$venv"
export PATH="$venv/bin:$tools/bin:/usr/bin:/bin"
python3 --version
python3 -c 'import sys; print(sys.prefix, sys.base_prefix, sys.flags.no_user_site)'

echo "== pinned sv2v release (Install the pinned sv2v release)"
ver=v0.0.12
sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00
curl -fsSL "https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip" -o "$work/tmp/sv2v.zip"
echo "${sha256}  $work/tmp/sv2v.zip" | sha256sum -c -
rm -rf "$work/tmp/sv2v"
unzip -q -o "$work/tmp/sv2v.zip" -d "$work/tmp/sv2v"
mkdir -p "$tools/bin"
install -m755 "$(find "$work/tmp/sv2v" -name sv2v -type f | head -1)" "$tools/bin/sv2v"
sv2v --version

echo "== Install LiteX at the pinned revisions"
python3 -m pip install --quiet pyyaml
python3 -m pip install --quiet -r sw/litex/litex_pins.txt
python3 -m pip freeze --all

echo "== Place the VexiiRiscv source at the revision LiteX pins"
python3 scripts/ci_litex_env.py

echo "== Apply the toolchain patch series"
sw/litex/patches/apply.sh

echo "== Install and verify the pinned RV32 SDK (offline archive, digest-checked)"
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host" \
  --archive $VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz

echo "== data packages visible to this interpreter"
python3 -c 'import importlib.util as u; [print(n, u.find_spec(n) is not None) for n in ("pythondata_software_picolibc", "pythondata_software_compiler_rt", "pythondata_cpu_vexiiriscv", "litex", "migen", "litex_boards")]'
echo "SETUP COMPLETE"
