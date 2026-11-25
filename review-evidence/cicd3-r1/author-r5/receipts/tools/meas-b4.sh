#!/bin/bash
# meas-b4.sh: batch 4, C on 8-11 and D on 12-15 (the booking 8-15): the light legs against their old legs
T=/data-2/milan/tmp/cicd-a839/r5/tools
$T/meas.sh C 8-11 mdp:2/4 mdp:3/4 cc:2/4 cc:3/4 cc:6/8 cc:7/8 &
$T/meas.sh D 12-15 mdp:2/8 mdp:6/8 mdp:3/8 mdp:7/8 cc:2/8 cc:3/8 &
wait
echo B4DONE >> /data-2/milan/tmp/cicd-a839/r5/meas/progress
