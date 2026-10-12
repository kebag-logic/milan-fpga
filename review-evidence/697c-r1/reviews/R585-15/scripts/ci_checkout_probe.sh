#!/bin/sh
# Emulate actions/checkout@v4's defaults (fetch-depth 1, persisted token header, gc.auto 0) and the firmware jobs'
# `git submodule update --init ... third_party/tsn-c-stack`, with the Git PATH names, then run the pin check CLI.
# usage: ci_checkout_probe.sh SOURCE_REPO HEAD WORK
set -eu
SRC=$1; HEAD=$2; W=$3
rm -rf "$W"; mkdir -p "$W"; cd "$W"
git --version
git init -q repo; cd repo
git remote add origin "file://$SRC"
git config --local gc.auto 0
# a dummy token value (base64 of "review-probe"), standing in for the one actions/checkout persists
git config --local http.https://github.com/.extraheader "AUTHORIZATION: basic cmV2aWV3LXByb2Jl"
git -c protocol.version=2 fetch -q --no-tags --prune --no-recurse-submodules --depth=1 origin "+$HEAD:refs/remotes/pull/705/merge"
git checkout -q --force refs/remotes/pull/705/merge
git submodule update -q --init third_party/tsn-c-stack third_party/lwSRP
echo "--- superproject local config"; git config --list --show-scope --local | sed 's/AUTHORIZATION.*/AUTHORIZATION: <probe token>/'
echo "--- stack config (system and global files not read, as the proof reads none)"; GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C third_party/tsn-c-stack config --list --show-scope
echo "--- shallow: $(test -f .git/shallow && echo yes || echo no)"
set +e
python3 -B sw/firmware/ctrl/test/ctrl_build.py --stack-pin; echo "pin check rc=$?"
