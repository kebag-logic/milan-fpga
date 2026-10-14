#!/bin/sh
# Probe wrapper passed to ci/image/build.py --docker-command: forward unchanged.
# DOCKER_PREFIX optionally names a privilege/group-switch prefix for docker.
exec ${DOCKER_PREFIX} docker "$@"
