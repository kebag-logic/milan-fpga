#!/bin/bash
# The lone save, measurement only: the clone CR logs each journal read and prints each pass that ran the flash port (receipts/measure/R-*/read-backs.patch).
# usage: unitread.sh NAME POINT
S=$MANAGEMENT/2026-09-23/665s2b-a683p/scripts; T=$VALIDATION_STORAGE/665s2b-a683p
JOBS=8 $S/leg.sh $T/CR "$1" "$2" save
