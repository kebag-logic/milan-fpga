#!/usr/bin/env bash
# Lane B11 (new): stage and build o653_probe.cpp on the controller host, against the bench's
# installed la_avdecc 4.3.1.1 (headers and shared libraries). The installed include tree lacks
# one header the controller API includes (internals/avdeccVirtualControlledEntityInterface.hpp);
# the host's source tree is the same tag (v4.3.1.1) and its other headers equal the installed
# ones, so that one file is copied from it into the staging overlay, and its hash is printed.
# Compile options are the libraries' interface options, without the JSON feature (it gates only
# free functions that need a JSON header the host does not have).
# The build touches no bench resource (no network I/O). The caller does not need the bench lock.
# usage: build_o653.sh <packet_dir>   (endpoints from the private file named by B11_ENV)
set -u
. "${B11_ENV:?}"
P=$1
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a535/inc/internals" && \
timeout 30 scp -q "$P/tools/o653_probe.cpp" "$CTL_HOST:/tmp/a535/"
echo "STAGE_RC=$?"
timeout 300 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" 'set -u; cd /tmp/a535 && \
  L=$HOME/<controller-library-install>; S=$HOME/<controller-library-source>; \
  cp $S/include/la/avdecc/controller/internals/avdeccVirtualControlledEntityInterface.hpp inc/internals/ && \
  git -C $S describe --tags --always; \
  diff -rq $L/include/la $S/include/la | grep -v "\.i$\|\.h$" ; \
  sha256sum o653_probe.cpp inc/internals/*.hpp; g++ --version | head -1; \
  g++ -std=c++17 -O2 -Wall -Wextra -DENABLE_AVDECC_FEATURE_REDUNDANCY -DENABLE_AVDECC_STRICT_2018_REDUNDANCY -DENABLE_AVDECC_FEATURE_CBR \
    -I$L/include -I/tmp/a535/inc o653_probe.cpp -o o653_probe -L$L/lib -lla_avdecc_controller_cxx -lla_avdecc_cxx -Wl,-rpath,$L/lib -lpthread; \
  echo GXX_RC=$?; sha256sum o653_probe; ldd o653_probe | grep -i avdecc; ls -la /tmp/a535'
echo "BUILD_RC=$?"
