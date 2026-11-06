#!/usr/bin/env bash
set -u
bash <scratch>/tools/lane_gates.sh 519d9c2be139d2f777127a4aa19ea9ed251392a5 builder <scratch>/h-builder-wt <scratch>/gates-519d9c2be139d2f777127a4aa19ea9ed251392a5/builder
bash <scratch>/tools/lane_gates.sh 519d9c2be139d2f777127a4aa19ea9ed251392a5 builder-litex <scratch>/h-builder-litex-wt <scratch>/gates-519d9c2be139d2f777127a4aa19ea9ed251392a5/builder-litex
