#!/bin/sh
# Reviewer stale-contract search; run from the clone root at the reviewed head.
EX='--exclude-dir=history --exclude-dir=findings --exclude-dir=.git --exclude=CHANGELOG.md'
SUBS='--exclude-dir=external --exclude-dir=gptp-processor --exclude-dir=protocol-processor --exclude-dir=third_party'
echo "## A: replaced target figures, Markdown outside dated records"
grep -rnE --include='*.md' $EX $SUBS '38,?040|37,?659|13,?972|10,?521|\b60 ?(%|percent)' . 
echo "## A2: replaced target figures, non-Markdown tracked text"
git grep -nE '38,?040|37,?659|13,?972|10,?521' -- ':!*.md' ':!*.json' ':!*.svg' ':!*.drawio' ':!*.rpt'
echo "## B: selectable, retained or permanent placement"
grep -rnEi --include='*.md' $EX $SUBS 'selectable|selects (each|the) control|selected (control )?owner|selected firmware|retained[- ]fabric|retains? fabric|fabric placement|all-fabric[^.]*(support|stay|remain|retain)|(remains|stays) supported|either placement|both placements|either control owner|permits firmware|default(s)? (control|to bare)|default is bare|unqualified functions|optional split|split target|per function' .
echo "## C: gPTP placement and ownership"
grep -rnEi --include='*.md' $EX $SUBS 'sole (product )?owner|only product time|gptp[^.|]*(in fabric|remain|retain|firmware[- ]independent|independent)|fabric gptp (owns|remains|stays)|(remain|stay)[^.|]*gptp' .
echo "## D: every Mark II line outside its own charter pages and dated records"
grep -rnE --include='*.md' $EX $SUBS 'Mark II|Mark 2|split (placement|target|build)|control placement|default flip' . | grep -vE '^./docs/design/(MARK_II_|AREA_BUDGET|MAILBOX_SPLIT|SPLIT_CONTROL)|^./docs/ARCHITECTURE_HW_SW_SPLIT|^./docs/reference/FR_NFR|^./REQUIREMENTS'
echo "## E: NFR-RES-01 and resource-target words outside dated records"
grep -rnE --include='*.md' $EX $SUBS 'NFR-RES-01|whole-image|headroom target|LUT (target|ceiling|bar)' . | grep -v '^./docs/reference/FR_NFR'
echo "## F: gPTP and firmware in one line, and other ownership wordings"
grep -rnEi --include='*.md' $EX $SUBS 'gptp[^|]*firmware|firmware[^|]*gptp|product time|time owner|keeps? (the )?gptp|fabric[- ](aecp|acmp|adp|srp)|bare-metal (control|default)|default(s)? .*bare-metal' . | grep -vE '^./docs/design/(MARK_II_|AREA_BUDGET|MAILBOX_SPLIT|SPLIT_CONTROL)|^./docs/ARCHITECTURE_HW_SW_SPLIT|^./docs/reference/FR_NFR|^./REQUIREMENTS|^./tb/|^./docs/testing/CI_WORKFLOWS'
