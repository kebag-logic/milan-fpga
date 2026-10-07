#!/bin/sh
# Usage: validate_head.sh <repo-clone> <head-sha> <work-dir> <cgreen-prefix> <python-with-kconfiglib-and-yaml>
# Exports the exact head tree, then runs: SPDX header audit, build, ctest, behave,
# Kconfig/YAML/Python/Gherkin parse checks and the documentation checks.
# Prints one "STEP <name> rc=<n>" line per step; logs go to <work-dir>/logs.
set -u
repo=$1; head=$2; work=$3; cg=$4; py=$5
logs=$work/logs; tree=$work/tree
rm -rf "$tree" "$logs"; mkdir -p "$tree" "$logs"
git -C "$repo" archive "$head" | tar -x -C "$tree"
export PYTHONDONTWRITEBYTECODE=1
step() { name=$1; shift; "$@" > "$logs/$name.log" 2>&1; rc=$?; echo "STEP $name rc=$rc"; }

spdx_audit() {
  fail=0
  for f in $(git -C "$repo" ls-tree -r --name-only "$head"); do
    case "$f" in LICENSE|NOTICE) continue;; esac
    first=$(git -C "$repo" show "$head:$f" | head -n 1)
    case "$first" in '#!'*) first=$(git -C "$repo" show "$head:$f" | sed -n 2p);; esac
    case "$f" in
      *.c|*.h) want='/* SPDX-License-Identifier: Apache-2.0 */';;
      *.md) want='<!-- SPDX-License-Identifier: Apache-2.0 -->';;
      *) want='# SPDX-License-Identifier: Apache-2.0';;
    esac
    if [ "$first" = "$want" ]; then echo "OK   $f"; else echo "FAIL $f: $first"; fail=1; fi
  done
  echo "other SPDX identifiers (must be none):"
  git -C "$repo" grep -h -o 'SPDX-License-Identifier:.*' "$head" | sort | uniq -c
  git -C "$repo" grep -h -o 'SPDX-License-Identifier:.*' "$head" | grep -v -q -E '^SPDX-License-Identifier: Apache-2.0( \*/| -->)?$' && fail=1
  return $fail
}
step spdx_audit spdx_audit
step cmake_configure cmake -S "$tree" -B "$tree/build" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$cg"
step cmake_build cmake --build "$tree/build" --parallel 16
step ctest env LD_LIBRARY_PATH="$cg/lib:$cg/lib64" ctest --test-dir "$tree/build" --output-on-failure -V
step behave sh -c "cd '$tree' && behave"
step behave_dry_run_gherkin sh -c "cd '$tree' && behave --dry-run --no-summary"
step kconfig_parse sh -c "cd '$tree' && '$py' -c 'import kconfiglib; k=kconfiglib.Kconfig(\"Kconfig.zephyr\"); print(sorted(k.syms)); assert \"LWSRP\" in k.syms'"
step module_yml_parse "$py" -c "import yaml,sys; d=yaml.safe_load(open('$tree/zephyr/module.yml')); print(d); assert d['build']['cmake']=='.' and d['build']['kconfig']=='Kconfig.zephyr'"
step behave_ini_parse "$py" -c "import configparser; c=configparser.ConfigParser(); c.read('$tree/behave.ini'); print(dict(c['behave']))"
step python_compile sh -c "cd '$tree' && for f in \$(find . -name '*.py' -not -path './build/*'); do '$py' -c \"import ast,sys; ast.parse(open('\$f').read(), '\$f'); print('ok', '\$f')\" || exit 1; done"
step build_sh_syntax bash -n "$tree/build.sh"
step doc_sentences sh -c "cd '$tree' && python3 doc/tools/check_sentences.py"
step doc_references sh -c "cd '$tree' && python3 doc/tools/check_references.py"
step doc_references_selftest sh -c "cd '$tree' && python3 doc/tools/check_references.py --self-test"
step doc_links_local sh -c "cd '$tree' && python3 doc/tools/check_links.py --local-only"
step doc_links_auth sh -c "cd '$repo' && python3 doc/tools/check_links.py --github-auth"
step licence_link_refs sh -c "cd '$tree' && grep -rn -E '\\]\\((\\.\\./)*(\\.\\./\\.\\./)?(LICENSE|NOTICE)\\)' --include='*.md' ."
