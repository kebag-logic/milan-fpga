#!/bin/bash
# meas-all.sh: the two arms concurrently, A on 24-27 and B on 28-31 (the booking 24-31)
T=/data-2/milan/tmp/cicd-a839/r5/tools
$T/meas.sh A 24-27 mclk:0/4 make:follow_ring:clean+run make:media_phase:clean+run mdp:0/4 mdp:1/4 cc:0/4 cc:1/4 &
$T/meas.sh B 28-31 mclk:0/8 make:follow_ring:clean+build make:follow_ring:b8 make:follow_ring:pullin make:follow_ring:bind \
  make:follow_ring:small-pullin make:follow_ring:settle-control \
  make:media_phase:clean+pins make:media_phase:render make:media_phase:blend make:media_phase:ofs make:media_phase:det \
  make:media_phase:build make:media_phase:cases mdp:4/8 mdp:1/8 cc:0/8 cc:4/8 cc:5/8 &
wait
echo ALLDONE >> /data-2/milan/tmp/cicd-a839/r5/meas/progress
