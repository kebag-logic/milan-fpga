# Source me: the reviewer's environment (portable: override the two paths).
P=${P:-$REVIEWS/ppC3-r406-2-packet}
export PINNED_VERILATOR=${PINNED_VERILATOR:-$VALIDATION_STORAGE/ppC3-manager-20ec92b7/pinned-tool-bin/verilator}
mkdir -p "$P/scratch/bin" "$P/scratch/tmp"
ln -sf "$P/scripts/verilator-j8" "$P/scratch/bin/verilator"
export PATH="$P/scratch/bin:$PATH"
export TMPDIR="$P/scratch/tmp"
T=${T:-$P/scratch/tree}
