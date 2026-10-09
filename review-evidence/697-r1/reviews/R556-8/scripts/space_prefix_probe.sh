#!/bin/sh
# Run the template generator and one mutation arm with the same 1.14.0 install under a prefix containing a space.
# usage: space_prefix_probe.sh PACKET HEAD_TREE   (run under isolated.sh, which is then overridden here)
P=$1; T=$2; SP="$P/scratch/space prefix/gtest"
export PKG_CONFIG_PATH="$SP/lib/pkgconfig" CMAKE_PREFIX_PATH="$SP"
pkg-config --cflags --libs gmock gtest_main
cd "$T" || exit 2
python3 -B scripts/assertion_templates.py --check --work "$P/scratch/space-templates"; echo "assertion_templates --check rc=$?"
python3 -B scripts/mutation.py --work "$P/scratch/space-mutation" --select acmp-header-no-resp-2s --jobs 8 > "$P/scratch/space-mutation.log" 2>&1; echo "mutation --select rc=$?"
