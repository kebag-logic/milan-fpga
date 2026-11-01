#!/bin/sh
# fetch one git blob by sha via the hosting API to a relative path
mkdir -p "$(dirname "$2")"
gh api -H 'Accept: application/vnd.github.raw' "repos/kebag-logic/milan-fpga/git/blobs/$1" > "$2"
