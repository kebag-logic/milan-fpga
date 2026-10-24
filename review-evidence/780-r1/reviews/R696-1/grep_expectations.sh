#!/usr/bin/env bash
# Run from the exact-head parent checkout. Parent files only, no recursion.
set -eu
git grep -n -i -E 'GET_AVB_INFO|gavb|0x0027' -- . ':!protocol-processor' ':!gptp-processor'
git grep -n -E 'case 39|ask\(39|15,39|39,9|AECP_NOT_SUPPORTED' -- sw/firmware/ctrl/aecp sw/firmware/ctrl/test/test_aecp.cpp
