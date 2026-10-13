# Common environment for the R584-17 receipts. Usage: . env.sh  (set CLONE and PACKET first or take defaults)
: "${CLONE:=$REVIEWS/r584-17-697c}"
: "${PACKET:=$REVIEWS/697c-r584-17-packet}"
export TMPDIR="$PACKET/scratch/tmp"
export PATH="$PACKET/scratch/venv/bin:$PACKET/scratch/bin:$HOME/br-milan-rv32/host/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
