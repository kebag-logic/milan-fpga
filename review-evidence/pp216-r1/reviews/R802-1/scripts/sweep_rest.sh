#!/usr/bin/env bash
# sweep_rest.sh TREE JOBS SUITE...: suite_one.sh over the given suites, JOBS at once
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}; tree=$1; j=$2; shift 2
printf '%s\n' "$@" | xargs -P "$j" -I{} bash -c '"$0/scripts/suite_one.sh" "$1" "$2" "$0/receipts/sweep-rest/$2.log" > "$0/receipts/sweep-rest/$2.verdict"' "$PKT" "$tree" {}
cat "$PKT"/receipts/sweep-rest/*.verdict
