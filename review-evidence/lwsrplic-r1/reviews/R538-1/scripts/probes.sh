#!/bin/sh
# Usage: probes.sh <repo-clone> <head-sha> <work-dir> <python-with-kconfiglib-and-yaml>
# Disposable mutation probes on an exported copy of the head tree. Each probe
# must make its check FAIL (expected nonzero) and the unmutated control must pass.
set -u
repo=$1; head=$2; work=$3; py=$4
export PYTHONDONTWRITEBYTECODE=1
fresh() { rm -rf "$work/p"; mkdir -p "$work/p"; git -C "$repo" archive "$head" | tar -x -C "$work/p"; }
probe() { name=$1; expect=$2; shift 2; ( cd "$work/p" && "$@" ) > "$work/$name.log" 2>&1; rc=$?
  if [ "$expect" = pass ] && [ $rc -eq 0 ]; then v=OK; elif [ "$expect" = fail ] && [ $rc -ne 0 ]; then v=OK; else v=UNEXPECTED; fi
  echo "PROBE $name expect=$expect rc=$rc $v"; }
links() { python3 doc/tools/check_links.py --local-only; }
kconf() { "$py" -c 'import kconfiglib; kconfiglib.Kconfig("Kconfig.zephyr")'; }
yml() { "$py" -c 'import yaml; d=yaml.safe_load(open("zephyr/module.yml")); assert set(d)=={"name","build"} and d["build"]["kconfig"]=="Kconfig.zephyr", sorted(d)'; }
gherkin() { behave --dry-run --no-summary; }
cc_hdr() { cc -fsyntax-only -std=c11 -Isrc/include src/ports/timer.c; }

fresh; probe control_links pass links
rm -f "$work/p/LICENSE"; probe no_license_links fail links
fresh; rm -f "$work/p/NOTICE"; probe no_notice_links fail links
fresh; probe control_kconfig pass kconf
sed -i '1s|^# |// |' "$work/p/Kconfig.zephyr"; probe kconfig_wrong_comment fail kconf
fresh; probe control_module_yml pass yml
sed -i '1s|^# \(.*\)$|/* \1 */|' "$work/p/zephyr/module.yml"; probe module_yml_wrong_comment fail yml
fresh; probe control_gherkin pass gherkin
sed -i '1s|^# |// |' "$work/p/tests/features/switch.feature"; probe gherkin_wrong_comment fail gherkin
fresh; probe control_c_header pass cc_hdr
sed -i '1s|^/\* \(.*\) \*/$|# \1|' "$work/p/src/ports/timer.c"; probe c_wrong_comment fail cc_hdr
fresh; probe control_build_sh_shebang pass sh -c 'head -c2 build.sh | grep -q "#!"'
rm -rf "$work/p"
