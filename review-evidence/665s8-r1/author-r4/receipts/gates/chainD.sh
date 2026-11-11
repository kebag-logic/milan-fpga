#!/bin/bash
# chainD: rtl.yml's local jobs and portability shards, then the assignment's named gates beyond the workflows
G=<scratch>/gates; export CPUS=112-115
$G/rtl.sh
$G/extra.sh
echo done > $G/chainD.done
