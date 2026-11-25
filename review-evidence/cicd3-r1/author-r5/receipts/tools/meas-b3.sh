#!/bin/bash
# meas-b3.sh: batch 3, G on 56-59 and H on 60-63 (the booking 56-63): capture_coherence 1/8 against 1/4
T=/data-2/milan/tmp/cicd-a839/r5/tools
$T/meas.sh G 56-59 cc:1/4 &
$T/meas.sh H 60-63 cc:1/8 &
wait
echo B3DONE >> /data-2/milan/tmp/cicd-a839/r5/meas/progress
