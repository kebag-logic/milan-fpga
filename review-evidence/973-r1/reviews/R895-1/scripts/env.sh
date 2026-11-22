# Environment for the reviewer's probes (sourced): no bytecode in the reviewed clone, a fixed hash seed, temp files in
# the packet's scratch. Usage: R=<clone> P=<packet> . env.sh
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
export TMPDIR="$P/scratch/tmp"
mkdir -p "$TMPDIR"
