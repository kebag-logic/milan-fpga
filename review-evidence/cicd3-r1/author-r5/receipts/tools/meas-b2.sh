#!/bin/bash
# meas-b2.sh: batch 2, C on 8-11 and D on 12-15 (the booking 8-15)
T=/data-2/milan/tmp/cicd-a839/r5/tools
$T/meas.sh C 8-11 mclk:1/4 mclk:2/4 mdp:0/8 &
$T/meas.sh D 12-15 mclk:1/8 mclk:2/8 mclk:4/8 mdp:5/8 &
wait
echo B2DONE >> /data-2/milan/tmp/cicd-a839/r5/meas/progress
