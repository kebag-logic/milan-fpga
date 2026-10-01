#!/bin/sh
# Scans the added lines of the PR diff for host paths, addresses and tool or
# private names, listing every distinct match; a planted line proves the
# pattern matches. Usage: public_text_scan.sh <checkout>
cd "$1"
PAT='/home/|/data/|/tmp/|([0-9]{1,3}\.){3}[0-9]{1,3}|([0-9a-f]{2}:){5}[0-9a-f]{2}|claude|anthropic|openai|codex|milan-fpga-management|\.local/'
printf '+planted <bench-address>.2 <home-path>\n' | grep -c -i -E "$PAT" | sed 's/^/positive control lines matched: /'
echo "distinct matches in added lines (count token):"
/usr/bin/git diff d4dd742679b902b2bc5eedf89d525066d59aafbb a463a1deb9d63614e8bd2134ccd7b2cd541c72ed \
  | grep '^+' | grep -v '^+++' | grep -i -E -o "$PAT" | sort | uniq -c | sort -rn
