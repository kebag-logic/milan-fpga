# Source this from bash: the review's pinned tools, outputs under the packet's scratch.
# Set REPO to a clone of the reviewed head and TOOLS to the directory holding pinned-verilator-5.050; a Python with
# PyYAML and the pinned LiteX/migen is taken from $HOME/litex-milan/venv, the RV32 SDK from $HOME/br-milan-rv32/host.
export PKT=${PKT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
export REPO=${REPO:?set REPO to a clone of the reviewed head}
export TOOLS=${TOOLS:?set TOOLS to the pinned tools directory}
export PATH=$HOME/litex-milan/venv/bin:$TOOLS/pinned-verilator-5.050:$HOME/br-milan-rv32/host/bin:$PATH
export MILAN_RV32_CC=$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc
export TMPDIR=$PKT/scratch/tmp
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$TMPDIR" "$PKT/receipts/runs"
# job NAME CMD...: run CMD detached in $REPO, its output in receipts/runs/NAME.log and rc in NAME.rc
job() {
  name=$1; shift
  rm -f "$PKT/receipts/runs/$name.rc"
  ( cd "$REPO" && setsid bash -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$PKT/receipts/runs/$name" "$@" ) </dev/null >/dev/null 2>&1 &
}
# waitall NAME...: wait up to ~9 min for every named rc file
waitall() {
  for i in $(seq 1 108); do
    left=0; for n in "$@"; do [ -f "$PKT/receipts/runs/$n.rc" ] || left=$((left+1)); done
    [ $left -eq 0 ] && break; sleep 5
  done
  for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$PKT/receipts/runs/$n.rc" 2>/dev/null || echo RUNNING)"; done
}
