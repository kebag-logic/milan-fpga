#!/bin/bash
# chainD: rtl.yml's local jobs and portability shards, then the assignment's named gates beyond the workflows
G=$VALIDATION_STORAGE/665s8-a758b/gates; export CPUS=124-127
$G/rtl.sh
$G/extra.sh
echo done > $G/chainD.done
