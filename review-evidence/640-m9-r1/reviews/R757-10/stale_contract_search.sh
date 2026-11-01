#!/bin/sh
# Stale-contract search over the tree at the working directory (run from the repository root).
# Each group lists every hit; the report classifies them.
g() { echo "== $1"; shift; git grep -n -I -E "$@" -- ':!docs/history/' ':!docs/findings/' ':!CHANGELOG.md' ':!review-evidence/' | cut -c1-240; }
g "G1 replaced LUT figures" '38,?040|37,?659|13,?972|10,?521|\b60 ?(%|percent)'
g "G2 selectable placement" 'selectable|selects? each|selects? firmware|select(s|ed)? control|either placement|both placements|placement.*(permit|option)|permits? firmware'
g "G3 all-fabric retained" '[Aa]ll-fabric.*(support|remain|stay|retain)|fabric (placement|option).*(remain|retain|stay)|[Uu]nqualified functions|retain(s|ed)? fabric'
g "G4 gPTP in fabric, unscoped" 'gPTP.*(remain|stay|retain|sole|only product|product owner|independent)|(remain|stay|retain)[a-z]* .*gPTP|[Ff]abric gPTP owns'
g "G5 Mark II default" 'Mark II.*default|default.*(bare-metal|firmware).*control|defaults? control'
d() { echo "== $1"; shift; git grep -n -I -E "$@" -- '*.md' ':!docs/history/' ':!docs/findings/' ':!CHANGELOG.md' | cut -c1-240; }
d "G6 gPTP owner and fabric lists, other spellings" 'only (product )?time owner|sole (product )?owner|product time|[Ff]raming.*gPTP|gPTP.*[Ff]raming|media and gPTP|gPTP and media|[Aa]udio and gPTP|gPTP,? (and )?(framing|timestamps|media)|gPTP.*(in|inside) (the )?fabric|fabric.*owns.*gPTP|fabric keeps'
d "G7 gPTP and firmware on one line" '[Gg][Pp][Tt][Pp].*([Ff]irmware|software)|([Ff]irmware|software).*[Gg][Pp][Tt][Pp]'
d "G8 other spellings of the placement claim" 'split target|Mark II placement|firmware or fabric|fabric or firmware|either (control )?owner|defaults? to bare-metal|default bare-metal|selected owner|retaining one'
echo "== G9 dated records naming the replaced target, not edited by this PR"
git grep -n -I -E 'NFR-RES-01' -- docs/findings/ | cut -c1-240
