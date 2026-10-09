#!/bin/bash
# SPDX-License-Identifier: MIT
# Recreate the reviewer toolchain extraction used by env.sh: the Ubuntu 24.04 packages the
# hosted runner installs (clang-18 1:18.1.3-1ubuntu1, googletest 1.14.0-1) plus the runtime
# libraries clang-18 needs on a non-Ubuntu host. Packages are unpacked, never installed.
# usage: PACKET=<packet dir> setup_sdk.sh
set -euo pipefail
PACKET=${PACKET:?}
D=$PACKET/scratch/debs; X=$PACKET/scratch/sdk; B=$PACKET/scratch/bin
mkdir -p "$D" "$X" "$B"; cd "$D"
U=http://archive.ubuntu.com/ubuntu/pool
for f in universe/l/llvm-toolchain-18/clang-18_18.1.3-1ubuntu1_amd64.deb \
         universe/l/llvm-toolchain-18/libclang-common-18-dev_18.1.3-1ubuntu1_amd64.deb \
         main/l/llvm-toolchain-18/libclang-cpp18_18.1.3-1ubuntu1_amd64.deb \
         main/l/llvm-toolchain-18/libllvm18_18.1.3-1ubuntu1_amd64.deb \
         universe/g/googletest/googletest_1.14.0-1_all.deb \
         universe/g/googletest/libgtest-dev_1.14.0-1_amd64.deb \
         universe/g/googletest/libgmock-dev_1.14.0-1_amd64.deb \
         main/libe/libedit/libedit2_3.1-20250104-1_amd64.deb \
         "main/libx/libxml2/libxml2_2.9.14+dfsg-1.3ubuntu3_amd64.deb" \
         main/i/icu/libicu74_74.2-1ubuntu3_amd64.deb; do
  curl -sSfO "$U/$f"
done
for f in *.deb; do bsdtar -xOf "$f" 'data.tar.*' | bsdtar -xf - -C "$X"; done
for f in "$X"/usr/lib/x86_64-linux-gnu/pkgconfig/*.pc; do
  sed -i "s#^libdir=/usr/lib/x86_64-linux-gnu#libdir=$X/usr/lib/x86_64-linux-gnu#; s#^includedir=/usr/include#includedir=$X/usr/include#" "$f"
done
printf '#!/bin/sh\n# g++ that links the extracted GoogleTest 1.14.0 static libraries before the host copy\nexec /usr/bin/g++ -L%s "$@"\n' \
  "$X/usr/lib/x86_64-linux-gnu" > "$B/g++"
chmod +x "$B/g++"
sha256sum *.deb
