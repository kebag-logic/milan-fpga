#!/bin/sh
# Plant copies in a disposable clone of the head: the real page, the workflow's own --check and --write.
# Usage: probe_e2e.sh CLONE. The clone is reset between arms and has no submodules checked out.
T=$1
cd "$T" || exit 3
export PYTHONDONTWRITEBYTECODE=1
arm() {
	name=$1; text=$2
	git reset -q --hard HEAD; git clean -qfd
	printf '\n%b\n' "$text" >> docs/guides/BOARD_DEPLOYMENT.md
	git add docs/guides/BOARD_DEPLOYMENT.md
	python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; c1=$?
	python3 -I scripts/docs_inventory.py --write >/dev/null 2>&1
	python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; c2=$?
	row=$(grep -c '^| D0-[0-9]* | \[docs/guides/BOARD_DEPLOYMENT.md\]' docs/DOCUMENTATION_AUDIT.md)
	st=$(grep '^| \[docs/guides/BOARD_DEPLOYMENT.md\]' docs/DOCUMENTATION_AUDIT.md | awk -F'|' '{print $7}' | tr -d ' ')
	echo "$name: --check rc=$c1; after --write rc=$c2, rows on page=$row, status=$st"
}
git reset -q --hard HEAD; python3 -I scripts/docs_inventory.py --check; echo "unplanted, no submodules: rc=$?"
arm "exact README statement" "ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware."
arm "wrapped in a block quote" "> ADP, ACMP, AECP, MAAP\n> and SRP default to\n> bare-metal firmware."
arm "recorded also spelling" "Mark II defaults to firmware."
arm "underscore emphasis" "_ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware._"
arm "one word as a link" "ADP, ACMP, AECP, MAAP and SRP default to [bare-metal](../README.md) firmware."
arm "D0-025 sentence, full stop" "The protocol processor's NVM face is answered by a blank-flash responder."
arm "D0-035 sentence, full stop" "The AEM copy goes through the BIOS's \`copy_image_from_flash_to_ram\`."
arm "D0-059 clause, full stop" "It is **not met by this build**."
arm "D0-002 clause, comma" "Clock-source selection now reaches the media plane's wrapper, and stops."
git reset -q --hard HEAD; git clean -qfd
