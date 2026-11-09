bash -c set -o pipefail; MAKEFLAGS=-j8 REQ_TAG_LOG=$SCRATCH/runs/final2/req-tags.txt bash scripts/run_suites.sh | tee $SCRATCH/runs/final2/suites.txt
