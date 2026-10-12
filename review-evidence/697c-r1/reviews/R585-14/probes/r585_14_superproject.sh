#!/usr/bin/env bash
# R585-14: the superproject side of the pin proof (ctrl_build.stack_gitlink), its own configuration naming
# programs for every key family the stack's allowlist refuses, as a partial clone with a sparse index.
# usage: r585_14_superproject.sh <superproject-checkout> <scratch-dir>
set -u
TOP=$(cd "$1" && pwd); D=$2; rm -rf "$D"; mkdir -p "$D"
PIN=$(git -C "$TOP" ls-files --stage -- third_party/tsn-c-stack | awk '{print $2}')
printf '#!/bin/sh\necho "$0 $*" >> "%s/ran"\nexit 1\n' "$D" > "$D/rec"; chmod +x "$D/rec"
git init -q "$D/sp"; git -C "$D/sp" update-index --add --cacheinfo "160000,$PIN,third_party/tsn-c-stack"
for k in core.fsmonitor core.sshCommand core.hooksPath core.pager core.askPass core.editor credential.helper \
         remote.origin.uploadpack gpg.program core.alternateRefsCommand; do git -C "$D/sp" config "$k" "$D/rec"; done
git -C "$D/sp" config core.repositoryformatversion 1; git -C "$D/sp" config extensions.partialClone origin
git -C "$D/sp" config remote.origin.url "$D/sp"; git -C "$D/sp" config remote.origin.promisor true
git -C "$D/sp" config index.sparse true; git -C "$D/sp" config core.untrackedCache true
cd "$TOP/sw/firmware/ctrl/test" && python3 -I -c '
import sys; sys.path.insert(0, ".")
from pathlib import Path
import ctrl_build
print("gitlink", ctrl_build.stack_gitlink(Path(sys.argv[1])))' "$D/sp" 2>&1 | tail -2
echo "superproject RAN=$( [ -f "$D/ran" ] && wc -l < "$D/ran" || echo 0)"
