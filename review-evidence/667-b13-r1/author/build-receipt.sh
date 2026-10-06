#!/bin/sh
# Controller-side build from the pinned source export and dependencies.
set -eu
timeout 65s cmake -S /tmp/667-b13/source -B /tmp/667-b13/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_AVDECC_LIB_STATIC_RT_SHARED=OFF -DENABLE_AVDECC_FEATURE_JSON=ON -DINSTALL_AVDECC_HEADERS=OFF -DINSTALL_AVDECC_DOC=OFF
timeout 1200s cmake --build /tmp/667-b13/build --parallel 2
timeout 80s g++ -std=c++17 -O2 -Wall -Wextra -DENABLE_AVDECC_FEATURE_REDUNDANCY -DENABLE_AVDECC_STRICT_2018_REDUNDANCY -DENABLE_AVDECC_FEATURE_CBR -DENABLE_AVDECC_FEATURE_JSON -I/tmp/667-b13/source/include -I/tmp/667-b13/source/externals/nih/include -I/tmp/667-b13/source/externals/3rdparty/json/include /tmp/667-b13/probe.cpp -o /tmp/667-b13/probe -L/tmp/667-b13/build/src/controller -L/tmp/667-b13/build/src -lla_avdecc_controller_cxx -lla_avdecc_cxx -Wl,-rpath,/tmp/667-b13/build/src/controller:/tmp/667-b13/build/src -lpthread
