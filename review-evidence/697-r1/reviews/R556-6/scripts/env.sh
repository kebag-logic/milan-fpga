# Reviewer environment: Ubuntu noble clang-18 18.1.3-1ubuntu1 and googletest 1.14.0-1
# packages extracted under scratch/sdk (same package versions as the hosted runner).
# GTest_DIR forces CMake to the extracted 1.14.0 package config (headers and libraries together).
PACKET=${PACKET:?set PACKET to the review packet directory}
SDK=$PACKET/scratch/sdk
export PATH=$SDK/usr/bin:$PATH
export LD_LIBRARY_PATH=$SDK/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export PKG_CONFIG_PATH=$SDK/usr/lib/x86_64-linux-gnu/pkgconfig
export GTest_DIR=$SDK/usr/lib/x86_64-linux-gnu/cmake/GTest
export CMAKE_PREFIX_PATH=$GTest_DIR:$SDK/usr
export TSN_CLANG=$SDK/usr/bin/clang-18
# Drivers that call g++ directly (mutation campaign, conditional matrix) must also see 1.14.0 as system headers.
export CPLUS_INCLUDE_PATH=$SDK/usr/include
export LIBRARY_PATH=$SDK/usr/lib/x86_64-linux-gnu
# scratch/bin/g++ adds -L for the extracted 1.14.0 static libraries (host carries another version).
export PATH=$PACKET/scratch/bin:$PATH
export CXX=$PACKET/scratch/bin/g++
