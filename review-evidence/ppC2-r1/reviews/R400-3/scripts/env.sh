# Source before any reviewer run. Needs R400_VERILATOR_ROOT = a Verilator 5.050
# install or source build (its bin/verilator). Pins that Verilator (build -j capped
# at 8 by verilator-j8) and keeps temporary trees under the packet's scratch/.
P="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
: "${R400_VERILATOR_ROOT:?set R400_VERILATOR_ROOT to a Verilator 5.050 root}"
export R400_VERILATOR_ROOT
mkdir -p "$P/scratch/bin" "$P/scratch/tmp"
ln -sf "$P/scripts/verilator-j8" "$P/scratch/bin/verilator"
export PATH="$P/scratch/bin:$PATH"
export VERILATOR="$P/scripts/verilator-j8"
export TMPDIR="$P/scratch/tmp"
