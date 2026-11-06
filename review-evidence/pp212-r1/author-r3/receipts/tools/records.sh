#!/usr/bin/env bash
# records.sh <lane> <parent> <outdir>: the processor and scratch-parent records of round 3 (generated)
set -u
L=$1; P=$2; O=$3; mkdir -p $O
{
  echo "# processor records (generated)"
  echo "origin: $(git -C $L remote get-url origin)"
  echo "branch: $(git -C $L branch --show-current)"
  echo "base (main): a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645"
  echo "round-2 head: a2fce4326ebdaf398a1920d79a664d44e6f1e5dd"
  echo "head: $(git -C $L rev-parse HEAD)"
  echo "head tree: $(git -C $L rev-parse HEAD^{tree})"
  git -C $L merge-base --is-ancestor a2fce4326ebdaf398a1920d79a664d44e6f1e5dd HEAD && echo "round-2 head is an ancestor of head (no rebase): yes"
  echo "working tree: $(git -C $L status --porcelain | wc -l) changed entries"
  echo
  echo "## round-3 commits (subject; body)"
  for c in $(git -C $L rev-list --reverse a2fce4326ebdaf398a1920d79a664d44e6f1e5dd..HEAD); do
    echo "$c $(git -C $L log -1 --format=%s $c)"
    b=$(git -C $L log -1 --format=%b $c); echo "  body: ${b:-none}"
  done
  echo
  echo "## diff stat round-2 head..head"
  git -C $L diff --stat a2fce4326ebdaf398a1920d79a664d44e6f1e5dd HEAD
  echo
  echo "## files under hdl/ changed round-2 head..head"
  git -C $L diff --name-only a2fce4326ebdaf398a1920d79a664d44e6f1e5dd HEAD -- hdl/
  echo "## files under hdl/top/ changed main..head (empty: no top-level change)"
  git -C $L diff --name-only a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645 HEAD -- hdl/top/
  echo "## KL_srp_top module header, main vs head (sha256 of the lines up to the first ');')"
  for r in a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645 HEAD; do
    echo "$r $(git -C $L show $r:hdl/srp/KL_srp_top.sv | sed -n '1,/^);/p' | sha256sum | cut -c1-64)"
  done
} > $O/processor-records.txt
{
  echo "# scratch-parent records (generated)"
  echo "source: milan-fpga dev 604899c08ff1cd1830e1dd08b733109ef852400c (a local clone of the trusted dev lane)"
  echo "scratch parent head: $(git -C $P rev-parse HEAD) on local branch $(git -C $P branch --show-current)"
  echo "push URL: $(git -C $P remote get-url --push origin)"
  echo "never pushed: the only remote is the local source; the push URL is disabled"
  echo
  echo "## round-3 commits"
  git -C $P log --format='%H %s' 5761bf45d6a7f6e0a030d86b4d66a0e29f792db4..HEAD
  echo
  echo "## files changed 604899c0..HEAD"
  git -C $P diff --stat 604899c08ff1cd1830e1dd08b733109ef852400c HEAD
  echo
  echo "## rom_digests.tsv rows of this pin"
  pin=$(git -C $P ls-tree HEAD protocol-processor | awk '{print $3}')
  grep "^$pin" $P/syn/yosys/rom_digests.tsv
  echo "(main a9e84b66 rows, for comparison)"
  grep "^a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645" $P/syn/yosys/rom_digests.tsv
  echo
  echo "## submodules (top-level identity checked before every git command inside protocol-processor)"
  git -C $P submodule status
  test "$(git -C $P/protocol-processor rev-parse --show-toplevel)" = "$P/protocol-processor" && echo "protocol-processor toplevel: $P/protocol-processor"
  echo "protocol-processor HEAD: $(git -C $P/protocol-processor rev-parse HEAD)"
  echo
  echo "## working tree (tracked changes)"
  git -C $P status --porcelain --untracked-files=no
} > $O/parent-records.txt
{
  echo "verilator (sweep, lint 5050, campaigns): $(<toolchain>/verilator-v5.050/bin/verilator --version)"
  echo "verilator (lint 5052): $(env PATH=<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin verilator --version)"
  echo "yosys: $(yosys -V)"
  echo "sv2v (processor gates and area, first on their PATH): $(<home>/.local/bin/sv2v --version)"
  echo "sv2v (parent gates, pinned): $(<toolchain>/sv2v-v0.0.12/sv2v --version)"
  echo "python (parent venv): $(<venv>/bin/python --version)"
  echo "python (processor gates): $(python3 --version)"
  echo "g++: $(g++ --version | head -1)"
  echo "make: $(make --version | head -1)"
  echo "GoogleTest (parent firmware): 1.14.0 (headers on the system include path)"
} > $O/tool-versions.txt
