#!/bin/bash
# chainDc: every docs.yml job on its own fresh clone of the gate head, in turn
G=<scratch>/gates4; export CPUS=80-87
$G/docs_jobs.sh
echo done > $G/chainDc.done
