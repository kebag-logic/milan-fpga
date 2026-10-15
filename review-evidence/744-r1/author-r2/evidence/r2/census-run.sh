#!/bin/bash
# Inside the capped scope: the generated budget step, then the generated census command at its bound,
# with every sv2v and Yosys wrapped to log its own maximum resident set size.
cd $LANES/744-slot-oom
D=$VALIDATION_STORAGE/744-a621/meas2
export TMPDIR=$VALIDATION_STORAGE/744-a621/tmp SV2V=$D/shim-sv2v YOSYS=$D/shim-yosys PATH=$VALIDATION_STORAGE/744-a621/venv/bin:$PATH
export GITHUB_ENV=$D/budget.env
: > "$GITHUB_ENV"
bash $D/budget-step.sh || exit 90
set -a; . "$GITHUB_ENV"; set +a
echo "CI_CENSUS_JOBS=$CI_CENSUS_JOBS"
/usr/bin/time -v -o $D/census-time.txt bash $D/census-step.sh
