#!/bin/sh
# usage: real_probes.sh <tree-copy>: plant one line set on a real page, print rc and copy findings, restore
T=$1; cd "$T" || exit 2
probe() { # label page text
  cp "$2" "$2.keep"; printf '\n%b\n' "$3" >> "$2"
  out=$(python3 -B scripts/check_docs.py 2>&1); rc=$?
  mv "$2.keep" "$2"
  printf '%s rc=%s %s\n' "$1" "$rc" "$(printf '%s' "$out" | grep -o "restates [A-Z_]*" | sort -u | tr '\n' ' ')"
}
G=docs/GLOSSARY.md; H=docs/HDL_DEVELOPER.md
for t in 'A 2.5 min hold.' 'A twenty-five minutes soak.' 'At least 5 minimum samples.' 'A 375 msec gap.' 'A 1375 ms gap.' 'snake_5_min'; do probe "noncopy[$t]" $G "$t"; done
probe "r740-4[long tilde]" $H '~~~~text\n~~~\n~~~~\n\nThe Sync receipt timeout is 125 ms.'
probe "r740-4[inner info]" $H '~~~text\n~~~example\n~~~\n\nThe Sync receipt timeout is 125 ms.'
probe "r740-4[_125 ms_]" $H 'The Sync receipt timeout is _125 ms_.'
probe "r740-4[_5 minutes_]" $H 'A _5 minutes_ countdown.'
probe "r740-4[_five minutes_]" $H 'A _five minutes_ countdown.'
probe "r740-4[*125 ms*]" $H 'The Sync receipt timeout is *125 ms*.'
probe "r739-4[_375 ms_]" $G 'The watch is _375 ms_.'
probe "r739-4[_5 minutes_]" $G 'After _5 minutes_ it ceases.'
probe "r739-4[_five minutes_]" $G 'After _five minutes_ it ceases.'
probe "control[fenced ok]" $G '~~~~\n~~~\nA 375 ms watch.\n~~~~'
probe "recorded[link real target]" $G 'A [375](README.md) ms watch.'
probe "recorded[decimal]" $G 'A 0.375 s watch.'
probe "recorded[html block]" $G '<pre>\n```\n</pre>\n\nA 375 ms watch.'
probe "recorded[lazy]" $G '- Item.\nlazy\n  ```\nA 375 ms watch.'
