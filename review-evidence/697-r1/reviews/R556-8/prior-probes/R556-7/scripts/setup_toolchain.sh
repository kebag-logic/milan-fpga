#!/bin/sh
# Reviewer toolchain: GoogleTest/GMock 1.14.0 built from the pinned commit, and the Ubuntu 24.04
# clang-18 package (with its two missing runtime libraries) extracted for the Clang 18 lexer.
# Everything is placed under $PACKET/scratch. usage: PACKET=/path/to/packet setup_toolchain.sh
set -eu
S=$PACKET/scratch; mkdir -p "$S/src" "$S/debs/x" "$S/bin" "$S/pc-isystem"
git clone -q https://github.com/google/googletest.git "$S/src/googletest"
git -C "$S/src/googletest" checkout -q f8d7d77c06936315286eb55f8de22cd23c188571
cmake -S "$S/src/googletest" -B "$S/gtest-build" -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$S/gtest-install" -DCMAKE_INSTALL_LIBDIR=lib
cmake --build "$S/gtest-build" -j16 && cmake --install "$S/gtest-build"
# Variant used for the bank: identical install, package Cflags with -isystem (as a /usr install behaves).
for f in gtest gmock gtest_main gmock_main; do
  sed 's/^Cflags: -I\${includedir}/Cflags: -isystem ${includedir}/' "$S/gtest-install/lib/pkgconfig/$f.pc" > "$S/pc-isystem/$f.pc"
done
U=https://archive.ubuntu.com/ubuntu/pool
cd "$S/debs"
for u in universe/l/llvm-toolchain-18/clang-18_18.1.3-1ubuntu1_amd64.deb \
         main/l/llvm-toolchain-18/libclang-cpp18_18.1.3-1ubuntu1_amd64.deb \
         main/l/llvm-toolchain-18/libllvm18_18.1.3-1ubuntu1_amd64.deb \
         main/libe/libedit/libedit2_3.1-20230828-1build1_amd64.deb \
         main/libx/libxml2/libxml2_2.9.14+dfsg-1.3ubuntu3.10_amd64.deb \
         main/i/icu/libicu74_74.2-1ubuntu3.1_amd64.deb \
         main/libb/libbsd/libbsd0_0.12.1-1build1_amd64.deb \
         main/libm/libmd/libmd0_1.1.0-2build1_amd64.deb; do curl -sSfO "$U/$u"; done
sha256sum *.deb > "$S/debs.sha256"
for d in *.deb; do (cd x && ar x "../$d" && tar xf data.tar.* && rm -f data.tar.* control.tar.* debian-binary); done
L=$S/debs/x/usr/lib/x86_64-linux-gnu:$S/debs/x/lib/x86_64-linux-gnu:$S/debs/x/usr/lib/llvm-18/lib
printf '#!/bin/sh\nLD_LIBRARY_PATH=%s exec -a "$0" %s "$@"\n' "$L" "$S/debs/x/usr/lib/llvm-18/bin/clang" > "$S/bin/clang-18"
chmod +x "$S/bin/clang-18"
"$S/bin/clang-18" --version
