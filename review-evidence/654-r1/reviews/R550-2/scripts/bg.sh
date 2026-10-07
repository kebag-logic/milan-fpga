#!/usr/bin/env bash
# Usage: bg.sh NAME DIR CMD... ; runs CMD with its log and rc under DIR (receipts).
name=$1 dir=$2; shift 2
mkdir -p "$dir"
( "$@" >"$dir/$name.log" 2>&1; echo $? >"$dir/$name.rc" ) &
