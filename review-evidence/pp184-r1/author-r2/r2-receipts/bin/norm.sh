#!/usr/bin/env bash
# norm.sh <log>: strip run-specific noise (headers, wall times, temp paths, tool timing lines, pin SHAs)
grep -v '^## ' "$1" \
 | grep -v -E 'Walltime|^- V e r i l a t i o n|Verilator: Built from|ccache|^g\+\+ |^make\[[0-9]+\]: (Entering|Leaving)' \
 | sed -E 's#/tmp/[A-Za-z0-9._/-]+#<TMP>#g; s/[0-9]+\.[0-9]+ ?(s|ms|sec|seconds)\b/<T>/g; s/in [0-9.]+s/in <T>/g; s/(5addf29759a22372ed6aa3e1d52a3aad29e3ecd7|88cb206135c23eb86488ad110fe19cfca5f341cf)/<PIN>/g; s/[0-9]+m[0-9.]+s/<T>/g; s/elapsed[ =:][^ ]+/elapsed=<T>/g'
