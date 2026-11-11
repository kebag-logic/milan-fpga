#!/bin/bash
# chainCd: every docs.yml job on its own fresh clone of the gate head, in turn (chain C's first half, re-run after the
# runner's missing skip list stopped it before any clone)
G=<scratch>/gates; export CPUS=104-107
$G/docs_jobs.sh
echo done > $G/chainCd.done
