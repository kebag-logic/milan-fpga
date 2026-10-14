#!/usr/bin/env bash
# R638-4 independent cold rebuild: separate repository name, empty client config
# (no credentials), no push, no login.
# Usage: cold_rebuild.sh <clone> <prepared work dir> <log dir> <docker config dir with buildx v0.38.0>
set -u
cd "$1"
DOCKER_CONFIG="$4" python3 ci/image/build.py --work "$2" --no-cache --defer-lock --repository r638-4-cold \
  > "$3/cold-rebuild.log" 2>&1
echo $? > "$3/cold-rebuild.rc"
