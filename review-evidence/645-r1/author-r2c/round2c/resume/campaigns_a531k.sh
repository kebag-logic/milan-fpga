#!/bin/bash
# One supervisor for the three resume drivers; each keeps its own log and rc.
cd $VALIDATION_STORAGE/645-a531/round2c || exit 2
R=$LANES/645-ring-slip
W=$PWD
( python3 -B resume/campaign_resume.py --repo $R --exe $W/baseline/model/Vfollow_ring --out $W/baseline --jobs 2 >> resume/baseline-a531k.log 2>&1; echo $? > resume/baseline-a531k.rc ) &
( python3 -B resume/campaign_resume_sign.py --sign slow --repo $R --exe $W/candidate/model/Vfollow_ring --out $W/candidate/campaigns --jobs 4 >> resume/candidate-slow-a531k.log 2>&1; echo $? > resume/candidate-slow-a531k.rc ) &
( python3 -B resume/campaign_resume_sign.py --sign fast --repo $R --exe $W/candidate/model/Vfollow_ring --out $W/candidate/campaigns --jobs 4 >> resume/candidate-fast-a531k.log 2>&1; echo $? > resume/candidate-fast-a531k.rc ) &
wait
