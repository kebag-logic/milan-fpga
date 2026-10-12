#!/bin/sh
# Download upstream Git 2.43.0, verify it against kernel.org's signed sha256sums file, build it into $1/prefix.
set -eu
W=$1
cd "$W/dl"
[ -f git-2.43.0.tar.xz ] || curl -fsSLO https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.43.0.tar.xz
[ -f sha256sums.asc ] || curl -fsSLO https://mirrors.edge.kernel.org/pub/software/scm/git/sha256sums.asc
grep ' git-2.43.0.tar.xz$' sha256sums.asc > want.sha256
sha256sum -c want.sha256
cd "$W"
rm -rf src && mkdir src && tar -C src -xJf dl/git-2.43.0.tar.xz
cd src/git-2.43.0
make -j16 prefix="$W/prefix" CFLAGS="-O2 -std=gnu17 -w" NO_TCLTK=1 NO_GETTEXT=1 NO_PERL=1 NO_PYTHON=1 NO_EXPAT=1 all >/dev/null
make prefix="$W/prefix" CFLAGS="-O2 -std=gnu17 -w" NO_TCLTK=1 NO_GETTEXT=1 NO_PERL=1 NO_PYTHON=1 NO_EXPAT=1 install >/dev/null
"$W/prefix/bin/git" --version
