#!/bin/bash
# usage: headcheck.sh <pr> <full-sha>
gh_head=$(gh pr view "$1" --json headRefOid --jq .headRefOid)
if [ "$gh_head" = "$2" ]; then echo "PR #$1 GitHub head ${gh_head:0:8} == frozen ${2:0:8}: OK"; else echo "PR #$1 GitHub head ${gh_head:0:8} != frozen ${2:0:8}: MISMATCH"; exit 1; fi
