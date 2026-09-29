#!/usr/bin/env bash
# Does anything dev landed (13eda870..79c36963) contradict or stale PR #622's
# 606/608 pages or its #75 row? Usage: staleness_check.sh <repo>
set -uo pipefail
cd "$1"
H=d62b1e1a3a37283ebad039880163873698a011db; O=13eda870d1a6cf3f946fc228a98862366b08d102; V=79c36963660c10e4c1c11a744fb5bff41a552b8b
P606=docs/findings/606_FIRST_BIND_MEASUREMENT.md; P608=docs/findings/608_75_WITHDRAWAL_AND_RESTART.md; B1=docs/findings/599_394_E1_LINK_CYCLES.md; GM=docs/findings/387_SOFTWARE_GM_STEP.md
echo "== C1 references to #606/#608/#75 pages or issues: tracked lines at OLDDEV vs DEV (dev added none)"
for r in $O $V; do echo "$r $(git grep -h -E '75_RECONNECT|606_FIRST|608_75|#60[68]([^0-9]|$)' $r -- . | wc -l)"; done
echo "-- dev-added lines naming #75/#606/#608 or the pages:"; git diff $O $V | grep -E '^\+.*(#75([^0-9]|$)|#60[68]([^0-9]|$)|75_RECONNECT|606_FIRST|608_75)' || echo "(only the lines below)"
echo "== C2 gitlinks OLDDEV vs DEV vs HEAD (processor pin c951a9ff unchanged, so '#133 pending adoption' stays true)"
for r in $O $V $H; do echo "$r $(git ls-tree $r protocol-processor gptp-processor external | awk '{print $3,$4}' | tr '\n' ' ')"; done
echo "== C3 image identity: B1 page (dev) vs 606 page (PR)"
for k in 0x00020060 acad92b9 d84bce7b 93742dd2 690d87e407bbb7f7 9b077636b1d42aca 7723d0b8129df7b7 020000fffe000001 f014c6f2bd80e462 bc41ab03e64198b1; do echo "$k B1=$(grep -c -- "$k" $B1) 606=$(grep -c -- "$k" $P606)"; done
echo "== C4 saved state: B1 final restore vs B2 identity gate"
grep -n -E 'Final restore|NVM slots|Commits ok|PP_STAT|PP_NVM_STAT' $B1 | head -6
grep -n -E 'Identity gate, |NVM slots|Commits ok|PP_STAT`, |PP_NVM_STAT` \|' $P606 | head -6
echo "== C5 timing: B1 restore unbind vs B2 first action sample (bind 1 claims > 1,800 s unbound)"
grep -n -E 'restore at [0-9:]+Z' $B1; grep -n -E 'action console samples run from' $P606; grep -n 'more than 1,800' $P606
python3 -c "print('06:22:05Z -> 06:53:46Z =', (6*3600+53*60+46)-(6*3600+22*60+5), 's')"
echo "== C6 DUT outputs bound by B1 (606 says Output 0 was never bound in B2 and its MAAP address predates the lane)"
grep -n -E 'Output [0-9] to input' $B1; grep -n -E 'Output 0|MAAP-range' $P606
echo "== C7 B1 disclaims a #75 verdict"
grep -n -E '#75|no #75 verdict' $B1
echo "== C8 peer configuration and as-found stream state"
grep -n -E 'configuration 1 at 48 kHz|eighteen queried|18 queried' $B1 $P606
echo "== C9 reset epoch"
grep -n -i 'reset epoch' $B1 $GM $P606 $P608 | head
echo "== C10 dev RTL touched (areas); PR pages measure the CRF talker bind/withdraw path on INTERNAL"
git diff --stat $O $V -- hdl | tail -20
grep -n -E 'clock source 0, INTERNAL|INTERNAL' $P606 | head -3
echo "== C11 VERSION unchanged by dev (identity rests on CRCs plus named source, not VERSION alone)"
git diff $O $V -- CHANGELOG.md | grep -n 'VERSION'
