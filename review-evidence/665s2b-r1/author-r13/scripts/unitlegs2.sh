#!/bin/bash
# The planted store step, the probe legs and the 8x8/1if point, 16 jobs each, in a unit of their own.
S=$MANAGEMENT/2026-09-23/665s2b-a683p/scripts; T=$VALIDATION_STORAGE/665s2b-a683p
JOBS=16 $S/leg.sh $T/C1 CTL-A8 8x8 all --mutation store-step-unbounded
JOBS=16 $S/leg.sh $T/CX X-A8 8x8 "y-links,x-links-same,x-save-0,x-save-1,x-save-2,x-save-3,x-save-4,x-save-5,y-save-0,y-save-1,y-save-2,y-save-3,y-save-4,y-save-5,y-save-6,y-save-7"
JOBS=16 $S/leg.sh $T/CX X-B8 8x8 y-links,x-links-same --variant answering-ports
JOBS=16 $S/leg.sh $T/CP P81-A8 8x8-1if backlog,backlog-adp,backlog-adp-refill,backlog-owed
