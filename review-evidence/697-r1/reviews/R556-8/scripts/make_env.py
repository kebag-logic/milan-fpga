#!/usr/bin/env python3
"""Write scratch/environment.json and a clang-18 wrapper for an isolated GoogleTest 1.14.0 prefix."""
import json, os, pathlib, sys
packet = pathlib.Path(sys.argv[1]).resolve()
sdk = packet / 'scratch/sdk'
lib = sdk / 'root/usr/lib/x86_64-linux-gnu'
wrapper = packet / 'scratch/bin/clang-18'
wrapper.parent.mkdir(parents=True, exist_ok=True)
wrapper.write_text('#!/bin/sh\nLD_LIBRARY_PATH="%s" exec "%s" "$@"\n' % (lib, sdk / 'root/usr/lib/llvm-18/bin/clang'))
wrapper.chmod(0o755)
env = {'PKG_CONFIG_PATH': str(sdk / 'gtest/lib/pkgconfig'),
       'CMAKE_PREFIX_PATH': str(sdk / 'gtest'),
       'TSN_CLANG': str(wrapper)}
(packet / 'scratch/environment.json').write_text(json.dumps(env, indent=2) + '\n')
print(json.dumps(env, indent=2))
