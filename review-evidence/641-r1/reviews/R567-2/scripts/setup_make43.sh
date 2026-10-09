#!/usr/bin/env bash
set -euo pipefail
work=$1
mkdir -p "$work"
cd "$work"
curl -fsSL https://ftp.gnu.org/gnu/make/make-4.3.tar.gz -o make-4.3.tar.gz
printf "%s  %s\n" e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19 make-4.3.tar.gz | sha256sum -c -
tar -xzf make-4.3.tar.gz
cd make-4.3
./configure
make -j16
./make --version
