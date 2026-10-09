#!/bin/bash
# SPDX-License-Identifier: MIT
# Rebuild the core objects of two revisions at the SAME path with the CI
# configurations, recompile every core translation unit from compile_commands.json
# with -g0 (and -frandom-seed=0 for GCC), and compare hashes. Also compares
# the native -g objects and the test registration/results of the coverage build.
# usage: objcmp.sh <git-repo> <rev-a> <rev-b> <scratch-dir> <out-dir> [jobs]
set -u
REPO=$1; A=$2; B=$3; S=$4; OUT=$5; J=${6:-8}
TREE=$S/objtree
mkdir -p "$OUT"
for rev in "$A" "$B"; do
  rm -rf "$TREE"; mkdir -p "$TREE"
  git -C "$REPO" archive "$rev" | tar -x -C "$TREE"
  dest=$OUT/$rev; rm -rf "$dest"; mkdir -p "$dest"
  for cfg in gcc-coverage clang-sanitizers rv32-debug rv32-release; do
    b=$TREE/build-$cfg
    case $cfg in
      gcc-coverage) opts=(-DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DTSN_COVERAGE=ON);;
      clang-sanitizers) opts=(-DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DTSN_SANITIZERS=ON);;
      rv32-debug) opts=(-DCMAKE_TOOLCHAIN_FILE=$TREE/cmake/rv32.cmake -DCMAKE_BUILD_TYPE=Debug);;
      rv32-release) opts=(-DCMAKE_TOOLCHAIN_FILE=$TREE/cmake/rv32.cmake -DCMAKE_BUILD_TYPE=Release);;
    esac
    cmake -S "$TREE" -B "$b" "${opts[@]}" > "$dest/$cfg.configure.log" 2>&1 || { echo "configure $cfg $rev failed"; exit 2; }
    cmake --build "$b" -j"$J" > "$dest/$cfg.build.log" 2>&1 || { echo "build $cfg $rev failed"; exit 2; }
    # native objects as built (with -g)
    find "$b" -path '*CMakeFiles/*' \( -name 'adp.c.o*' -o -name 'acmp.c.o*' -o -name 'maap.c.o*' \) -type f ! -name '*.d' ! -name '*.gcno' ! -name '*.gcda' \
      | sort | while read -r o; do printf '%s  %s\n' "$(sha256sum < "$o" | cut -c1-64)" "${o#$TREE/}"; done > "$dest/$cfg.native.sha256"
    # -g0 recompiles from the compile database
    python3 -I - "$b/compile_commands.json" "$dest/$cfg.g0" "$TREE" <<'EOF'
import json, shlex, subprocess, sys, hashlib, os
db, outdir, tree = sys.argv[1:4]
os.makedirs(outdir, exist_ok=True)
lines = []
for e in json.load(open(db)):
    f = e['file']
    if os.path.dirname(f) != os.path.join(tree, 'src'):
        continue
    argv = e.get('arguments') or shlex.split(e['command'])
    o = argv[argv.index('-o') + 1]
    target = o.split('CMakeFiles/')[1].split('.dir/')[0]
    name = target + '__' + os.path.basename(f) + '.o'
    new = []
    i = 0
    while i < len(argv):
        if argv[i] == '-o':
            i += 2; continue
        if argv[i] in ('-MD', '-MMD'):
            i += 1; continue
        if argv[i] in ('-MF', '-MT', '-MQ'):
            i += 2; continue
        new.append(argv[i]); i += 1
    compiler = os.path.basename(new[0])
    extra = ['-g0'] + (['-frandom-seed=0'] if 'gcc' in compiler else [])
    # fixed output path inside the tree: coverage objects embed their own path
    fixed = os.path.join(tree, 'g0out', name)
    os.makedirs(os.path.dirname(fixed), exist_ok=True)
    subprocess.run(new + extra + ['-o', fixed], cwd=e['directory'], check=True)
    out = os.path.join(outdir, name)
    open(out, 'wb').write(open(fixed, 'rb').read())
    lines.append(hashlib.sha256(open(out, 'rb').read()).hexdigest() + '  ' + name)
open(outdir + '.sha256', 'w').write('\n'.join(sorted(lines, key=lambda l: l[66:])) + '\n')
print(len(lines), 'core objects')
EOF
    if [ $? -ne 0 ]; then echo "g0 recompile $cfg $rev failed"; exit 2; fi
  done
  # test results of the coverage build
  mkdir -p "$dest/xml"
  for t in adp_tests acmp_tests maap_tests port_tests adp_release adp_debug maap_debug; do
    env -u GTEST_FILTER "$TREE/build-gcc-coverage/$t" --gtest_output=xml:"$dest/xml/$t.xml" > "$dest/xml/$t.log" 2>&1; echo "$t rc $?" >> "$dest/xml/rcs.txt"
  done
  python3 -I - "$dest/xml" > "$dest/test-results.txt" <<'EOF'
import sys, glob, xml.etree.ElementTree as ET
for x in sorted(glob.glob(sys.argv[1] + '/*.xml')):
    r = ET.parse(x).getroot()
    for c in r.iter('testcase'):
        st = 'FAIL' if c.findall('failure') else c.get('result')
        print(x.rsplit('/', 1)[1], c.get('classname') + '.' + c.get('name'), c.get('status'), st)
EOF
done
echo "== compare -g0 objects"
for cfg in gcc-coverage clang-sanitizers rv32-debug rv32-release; do
  n=$(wc -l < "$OUT/$A/$cfg.g0.sha256")
  if cmp -s "$OUT/$A/$cfg.g0.sha256" "$OUT/$B/$cfg.g0.sha256"; then echo "$cfg: $n identical"; else echo "$cfg: DIFFER"; diff "$OUT/$A/$cfg.g0.sha256" "$OUT/$B/$cfg.g0.sha256"; fi
done
echo "== compare native (as-built, with debug info) objects"
for cfg in gcc-coverage clang-sanitizers rv32-debug rv32-release; do
  if cmp -s "$OUT/$A/$cfg.native.sha256" "$OUT/$B/$cfg.native.sha256"; then echo "$cfg: native identical ($(wc -l < "$OUT/$A/$cfg.native.sha256"))"; else echo "$cfg: native differ"; diff "$OUT/$A/$cfg.native.sha256" "$OUT/$B/$cfg.native.sha256" | head -20; fi
done
echo "== compare test results"
cmp -s "$OUT/$A/test-results.txt" "$OUT/$B/test-results.txt" && echo "test results identical ($(wc -l < "$OUT/$A/test-results.txt") cases)" || { echo "test results differ"; diff "$OUT/$A/test-results.txt" "$OUT/$B/test-results.txt" | head; }
cat "$OUT/$A/xml/rcs.txt" | tr '\n' ' '; echo; cat "$OUT/$B/xml/rcs.txt" | tr '\n' ' '; echo
