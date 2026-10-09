#!/bin/sh
# Reviewer probe: sensitivity of dependency_selftest.py to reverted round-8 changes, and the
# behaviour of the package-flag build with GoogleTest 1.14.0 in a non-system prefix.
# usage: probe_dependency.sh HEAD_TREE WORK  (environment from env.sh; PC_PLAIN and PC_ISYSTEM dirs)
set -u
src=$1; work=$2; rm -rf "$work"; mkdir -p "$work"
variant() {  # name, python edit
  name=$1; edit=$2
  cp -a "$src" "$work/$name"
  python3 -c "$edit" "$work/$name" || { echo "$name: edit failed"; return; }
  (cd "$work/$name" && git diff --no-index --stat "$src" . 2>/dev/null | tail -1)
  (cd "$work/$name" && PKG_CONFIG_PATH=$PC_ISYSTEM python3 scripts/dependency_selftest.py --work "$work/$name-run" --jobs 16 > "$work/$name.log" 2>&1); rc=$?
  echo "$name: dependency_selftest rc=$rc; last error: $(grep -E 'RuntimeError|CalledProcessError|dependency control' "$work/$name.log" | tail -1)"
}
variant cmake-module-mode 'import sys,pathlib; p=pathlib.Path(sys.argv[1],"CMakeLists.txt"); s=p.read_text(); assert "EXACT CONFIG REQUIRED" in s; p.write_text(s.replace("EXACT CONFIG REQUIRED","EXACT REQUIRED"))'
variant mutation-no-cflags 'import sys,pathlib; p=pathlib.Path(sys.argv[1],"scripts/mutation.py"); s=p.read_text(); n=s.count("*test_cflags, "); assert n==3; p.write_text(s.replace("*test_cflags, ",""))'
variant mutation-old-libs 'import sys,pathlib; p=pathlib.Path(sys.argv[1],"scripts/mutation.py"); s=p.read_text(); n=s.count("*test_ldflags,"); assert n==2; p.write_text(s.replace("*test_ldflags,","\"-lgmock\", \"-lgtest\", \"-pthread\","))'
cp -a "$src" "$work/head"
(cd "$work/head" && PKG_CONFIG_PATH=$PC_ISYSTEM python3 scripts/dependency_selftest.py --work "$work/head-run" --jobs 16 > "$work/head.log" 2>&1); echo "unmodified head, -isystem package flags: dependency_selftest rc=$?"
(cd "$work/head" && PKG_CONFIG_PATH=$PC_PLAIN python3 scripts/dependency_selftest.py --work "$work/head-plain-run" --jobs 16 > "$work/head-plain.log" 2>&1); echo "unmodified head, upstream -I package flags (non-system prefix): dependency_selftest rc=$?"
grep -m3 -E "error:|RuntimeError" "$work/head-plain.log"
# How many test-side comparisons trip -Werror once the pinned headers are not system headers?
for f in test_adp.cpp test_acmp.cpp test_maap.cpp test_adp_reentry.cpp test_port.cpp test_maap_debug.cpp; do
  n=$(g++ -std=c++20 -Wall -Wextra -Werror -fmax-errors=0 $(PKG_CONFIG_PATH=$PC_PLAIN pkg-config --cflags gmock gtest) -I"$src/include" -I"$src/examples" -I"$src/tests" -DNDEBUG -fsyntax-only "$src/tests/$f" 2>&1 | grep -c "required from here")
  m=$(g++ -std=c++20 -Wall -Wextra -Werror $(PKG_CONFIG_PATH=$PC_ISYSTEM pkg-config --cflags gmock gtest) -I"$src/include" -I"$src/examples" -I"$src/tests" -DNDEBUG -fsyntax-only "$src/tests/$f" >/dev/null 2>&1; echo $?)
  echo "$f: -I instantiation errors=$n; -isystem rc=$m"
done
