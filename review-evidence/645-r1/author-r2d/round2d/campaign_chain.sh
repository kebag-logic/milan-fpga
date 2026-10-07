#!/bin/bash
# Round-2d campaigns at 3eee12dc, one driver at a time, four workers each:
# the 128-case quiet/arrival campaign, its quiet-distribution reader, then the
# INTERNAL pull-in sweep (16 feed phases x 52 and 56 us holds).
W=$VALIDATION_STORAGE/645-a531/round2d
R=$LANES/645-ring-slip
EXE=$W/candidate/model/Vfollow_ring
export PYTHONDONTWRITEBYTECODE=1
cd "$R/tb/verilator/follow_ring" || exit 2
python3 -B "$W/campaign.py" --repo "$R" --exe "$EXE" --out "$W/candidate/campaigns" --jobs 4 > "$W/candidate/campaign.log" 2>&1
echo $? > "$W/candidate/campaign.rc"
python3 -B quiet_distributions.py "$W/candidate/campaigns" --band 2 --out "$W/candidate/quiet-distributions.json" > "$W/candidate/quiet-distributions.log" 2>&1
echo $? > "$W/candidate/quiet-distributions.rc"
python3 -B sweep.py pullin --exe "$EXE" --out "$W/candidate/pullin" --jobs 4 --hold-us 52 56 > "$W/candidate/pullin.log" 2>&1
echo $? > "$W/candidate/pullin.rc"
