#!/bin/sh
# Run on the controller host with source and dependencies staged at their pins.
set -eu
timeout 65s cmake -S /tmp/653-b12/source -B /tmp/653-b12/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_AVDECC_LIB_STATIC_RT_SHARED=OFF -DENABLE_AVDECC_FEATURE_JSON=ON -DINSTALL_AVDECC_HEADERS=OFF -DINSTALL_AVDECC_DOC=OFF
timeout 1200s cmake --build /tmp/653-b12/build --parallel 2
timeout 80s g++ -std=c++17 -O2 -Wall -Wextra -DENABLE_AVDECC_FEATURE_REDUNDANCY -DENABLE_AVDECC_STRICT_2018_REDUNDANCY -DENABLE_AVDECC_FEATURE_CBR -DENABLE_AVDECC_FEATURE_JSON -I/tmp/653-b12/source/include -I/tmp/653-b12/source/externals/nih/include -I/tmp/653-b12/source/externals/3rdparty/json/include /tmp/653-b12/probe.cpp -o /tmp/653-b12/probe -L/tmp/653-b12/build/src/controller -L/tmp/653-b12/build/src -lla_avdecc_controller_cxx -lla_avdecc_cxx -Wl,-rpath,/tmp/653-b12/build/src/controller:/tmp/653-b12/build/src -lpthread
