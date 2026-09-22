#!/usr/bin/env bash
# p6 (R220-3): where the tree states the content-pin residue or its trackers,
# at the head and at the base. Usage: p6_residue_claims_grep.sh <clone>
set -uo pipefail
cd "$1" || exit 2
pat='#439|content gap|remaining content|seven RTL jobs|#407'
echo "### git grep -i -E '$pat' at 5d45ecc0 (docs/archive excluded)"
git grep -n -i -E "$pat" 5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7 -- . ':!docs/archive' | cut -c1-260
echo "### same at base b17580b9"
git grep -n -i -E "$pat" b17580b91deb11f3441dfc5d7f9fafe539d929b8 -- . ':!docs/archive' | cut -c1-260
echo "### the removed F3 sentence at 5d45ecc0 (exit 1 = absent)"
git grep -n "The remaining content gap belongs to" 5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7 -- .; echo "exit=$?"
echo "### the removed F1 wording at 5d45ecc0 (exit 1 = absent)"
git grep -n "pinned yet" 5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7 -- .; echo "exit=$?"
