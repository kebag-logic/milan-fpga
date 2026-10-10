#!/usr/bin/env bash
# Run a command with the host's own GoogleTest (drop the 1.14 overrides of env.sh).
unset CPLUS_INCLUDE_PATH LIBRARY_PATH PKG_CONFIG_PATH
exec "$@"
