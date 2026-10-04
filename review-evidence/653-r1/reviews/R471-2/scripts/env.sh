# Common environment for the R471-2 probes. Source from any script.
export CLONE=$REVIEWS/r471-2-653
export PKT=$REVIEWS/653-r471-2-packet
export SCR=$PKT/scratch
export REC=$PKT/receipts
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR=$SCR/tmp
mkdir -p "$TMPDIR"
HEAD_SHA=03895b63a3e8197353c2483593927b92efb73092
BASE_SHA=fea346e76c2a57ed5cd131af8fc68dfeff57f877
# run NAME CMD...: run in background, log to $REC/NAME.log, rc to $REC/NAME.rc
run() { local n=$1; shift; rm -f "$REC/$n.rc"; ( "$@" > "$REC/$n.log" 2>&1; echo $? > "$REC/$n.rc" ) & }
# mkcopy NAME: a byte copy of the clone's working tree (no .git, no build dirs)
mkcopy() {
  local d=$SCR/$1; rm -rf "$d"; mkdir -p "$d"
  rsync -a --exclude=.git --exclude='obj_*' "$CLONE"/ "$d"/
}
