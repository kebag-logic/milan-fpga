# Environment for the host-side firmware gates: a GoogleTest 1.14.0 prefix ahead of the host's (as system
# headers, as a distribution install is), and the pinned Verilator 5.050. Source it with GTEST_PREFIX and
# PINNED_VERILATOR set.
G=${GTEST_PREFIX:?set GTEST_PREFIX to a GoogleTest 1.14.0 install prefix}
export CPLUS_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib PKG_CONFIG_PATH=$G/lib/pkgconfig
export VERILATOR=${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned Verilator 5.050}
