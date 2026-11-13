#!/bin/sh
# usage: make_probe.sh <engine-dir> [make args...]
# Prints the OBJCACHE/CCACHE_* environment the engine Makefile hands a
# recipe with the `run` target's own target-specific export, and a plain
# recipe (as `mutants` gets), without building anything.
d=$1; shift
make -s -C "$d" "$@" \
  --eval='run-probe: export CCACHE_BASEDIR ?= $(abspath ../../..)' \
  --eval='run-probe: ; @printenv | grep -E "^(OBJCACHE|CCACHE_)" | sort | sed "s/^/  run: /"; printf "  run: OBJCACHE is [%s]\n" "$${OBJCACHE-UNSET}"' \
  --eval='mut-probe: ; @printenv | grep -E "^(OBJCACHE|CCACHE_)" | sort | sed "s/^/  mutants: /"; printf "  mutants: OBJCACHE is [%s]\n" "$${OBJCACHE-UNSET}"' \
  run-probe mut-probe
