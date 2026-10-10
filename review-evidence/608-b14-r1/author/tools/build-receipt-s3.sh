#!/bin/sh
# Controller-side build from the staged source export (lane B13's build line, staging directory /tmp/608-b14).
# usage: build-receipt.sh configure|build|probe
set -eu
case "$1" in
configure) timeout 65s cmake -S /tmp/608-b14/source -B /tmp/608-b14/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_AVDECC_LIB_STATIC_RT_SHARED=OFF -DENABLE_AVDECC_FEATURE_JSON=ON -DINSTALL_AVDECC_HEADERS=OFF -DINSTALL_AVDECC_DOC=OFF ;;
build) timeout 540s cmake --build /tmp/608-b14/build --parallel 2 ;;
probe) timeout 80s g++ -std=c++17 -O2 -Wall -Wextra -DENABLE_AVDECC_FEATURE_REDUNDANCY -DENABLE_AVDECC_STRICT_2018_REDUNDANCY -DENABLE_AVDECC_FEATURE_CBR -DENABLE_AVDECC_FEATURE_JSON -I/tmp/608-b14/source/include -I/tmp/608-b14/source/externals/nih/include -I/tmp/608-b14/source/externals/3rdparty/json/include /tmp/608-b14/probe.cpp -o /tmp/608-b14/probe -L/tmp/608-b14/build/src/controller -L/tmp/608-b14/build/src -lla_avdecc_controller_cxx -lla_avdecc_cxx -Wl,-rpath,/tmp/608-b14/build/src/controller:/tmp/608-b14/build/src -lpthread ;;
esac
