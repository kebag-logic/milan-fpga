#!/bin/sh
# SPDX-License-Identifier: MIT
# usage: clang18_shims.sh TOOLS OUT_DIR HOST_RT_DIR
# Writes clang, clang++, clang-18 and clang++-18 shims into OUT_DIR/bin that run the pinned clang 18.1.3
# under TOOLS/clang-18/root. The pinned install has no sanitizer runtime, so OUT_DIR/resource holds its
# headers plus links to the host's x86-64 sanitizer libraries in HOST_RT_DIR. -cc1 calls pass through
# unchanged. Then: export PATH=OUT_DIR/bin:TOOLS/clang-tidy-18/bin:$PATH and the gtest variables.
set -eu
tools=$1; out=$2; rt=$3; root=$tools/clang-18/root/usr; res=$out/resource
mkdir -p "$out/bin" "$res/lib/linux"; cp -a "$root/lib/llvm-18/lib/clang/18/include" "$res/"
for f in "$rt"/libclang_rt.*; do b=$(basename "$f"); n=${b%.a}; n=${n%.so}; ln -sf "$f" "$res/lib/linux/$n-x86_64${b#$n}"; done
for n in clang clang++ clang-18 clang++-18; do
  case $n in clang++*) t=clang++-18;; *) t=clang-18;; esac
  printf '#!/bin/sh\nexport LD_LIBRARY_PATH=%s/lib/x86_64-linux-gnu\nif [ "$1" = -cc1 ] || [ "$1" = -cc1as ]; then exec %s/bin/%s "$@"; fi\nexec %s/bin/%s -resource-dir %s "$@"\n' \
    "$root" "$root" "$t" "$root" "$t" "$res" > "$out/bin/$n"
  chmod +x "$out/bin/$n"
done
