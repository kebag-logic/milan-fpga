#!/bin/bash
# chainE: the assignment's named gates beyond the workflows (extra.sh) in a unit of their own, on CPUs chains A and C freed
G=<scratch>/gates; export CPUS=20-23,52-55
$G/extra.sh
echo done > $G/chainE.done
