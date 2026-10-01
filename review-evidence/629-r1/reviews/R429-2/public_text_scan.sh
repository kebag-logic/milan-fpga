#!/bin/sh
# Reviewer R429-2: scan the added lines of the PR diff for addresses, home or
# temp paths, private-range IPv4 addresses (a four-part clause number such as
# 5.3.3.6 is not an address), private host/peer/switch/instrument names and the management checkout name.
# Usage: sh public_text_scan.sh <clone>   (prints hits; "hits: N" last)
set -u
C=${1:?clone}
git -C "$C" diff d4dd742679b902b2bc5eedf89d525066d59aafbb c554ae51b1dcc2285863f0f0117cb025971a594c -- . \
 | grep '^+' \
 | grep -niE '/home/|/tmp/|/data/|\b(10\.[0-9]{1,3}|127\.[0-9]{1,3}|169\.254|172\.(1[6-9]|2[0-9]|3[01])|192\.168)\.[0-9]{1,3}\.[0-9]{1,3}\b|hostname|\.local\b|motu|focusrite|presonus|l-acoustics|meyer|yamaha|behringer|cisco|netgear|luminex|raspberry|beaglebone|macbook|ssh |milan-fpga-management' > /tmp/r429_2_scan.$$ || true
cat /tmp/r429_2_scan.$$
echo "hits: $(wc -l < /tmp/r429_2_scan.$$)"
rm -f /tmp/r429_2_scan.$$
