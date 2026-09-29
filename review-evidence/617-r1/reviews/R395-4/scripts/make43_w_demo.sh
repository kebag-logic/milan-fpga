#!/usr/bin/env bash
# Show what MAKEFLAGS a recipe inherits under `make -C <dir>` for make 4.3 and
# 4.4.1 (invoked as run_all_suites.sh does: `make -C <dir>`, no -s), and what a nested `make -s -C sub` then prints to stdout.
# Usage: make43_w_demo.sh <make-4.3 binary> <demo dir with Makefile + sub/Makefile>
set -u
m43=$1; d=$2
for m in "$m43" /usr/bin/make; do
  echo "== $($m --version | head -1): $m -C <demo>"
  mkdir -p "$d/.bin" && ln -sf "$m" "$d/.bin/make"
  env -u MAKEFLAGS PATH="$d/.bin:$PATH" "$m" -C "$d" all 2>&1
done
