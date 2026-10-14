#!/bin/sh
# Probe wrapper passed to ci/image/build.py --docker-command: insert --no-cache
# after "buildx build" so the recipe is rebuilt without any BuildKit cache.
# DOCKER_PREFIX optionally names a privilege/group-switch prefix for docker.
if [ "$1" = buildx ] && [ "$2" = build ]; then
  shift 2
  exec ${DOCKER_PREFIX} docker buildx build --no-cache "$@"
fi
exec ${DOCKER_PREFIX} docker "$@"
