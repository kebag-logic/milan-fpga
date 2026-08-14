#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# load_entity_model.sh - write the AEM descriptor image into the DRAM window
#                        the gateware's descriptor store reads from.
#
# SUPERSEDED ON THE BOARD BY `aemi-load` (milan-tests-avb fpga/aemi-load).
# MEASURED 2026-08-13 on the AX7101, kernel 6.6 rv32: the `dd` path below
# FAULTS.
#
#     dd  -> /dev/mem   kernel trace, then EFAULT
#     mmap                 works (busybox `devmem` proves it)
#
# The window is a `no-map` reserved region, so the kernel builds NO linear
# mapping for it - but the pages are inside the /memory node, so `pfn_valid()`
# is true and /dev/mem's READ/WRITE path takes `xlate_dev_mem_ptr()` -> `__va()`
# and dereferences an address that was never mapped. `mmap()` goes through
# `remap_pfn_range()` and establishes a real one. `no-map` is still correct and
# still required; it is only the ACCESS METHOD that was wrong here.
#
# This script is kept as the zero-dependency reference for the FORMAT and the
# checks (manifest parse, pair check, read-back, magic), which `aemi-load`
# implements identically. Do not put it back on the boot path.
#
# ONE CHECK LIVES ONLY IN `aemi-load`: the PAIRING check (2026-08-14). The C
# loader also walks the image's index map to the ENTITY descriptor, reads the
# baked firmware_version at offset 116 (1722.1-2021 Table 7-2), and compares
# its "major.minor." prefix against the live VERSION CSR at the manifest's
# `csr_base` + 0x004 - exit 3 when the image describes a build the flashed
# gateware is not (a bitstream flash never refreshes the rootfs, so the two
# CAN diverge, and did: a 2.68 model served on 2.69 gateware, 2026-08-14).
# It is not mirrored here because this reference is also the zero-dependency
# fallback, and busybox `devmem` - the only way to read the CSR from sh - is
# exactly the kind of dependency it exists to not have.
#
# POSIX sh + busybox only (dd, cmp, od) - no python, no compiler.
#
# WHY THIS EXISTS. The protocol processor holds no descriptors on-die; it
# fetches them from main memory, at a base compiled into the bitstream. Until
# something puts the image there the store finds no AEMI header, refuses to
# serve, and every READ_DESCRIPTOR is answered BAD_ARGUMENTS - an end-station
# that looks broken rather than unprovisioned. This is the step that
# provisions it.
#
#   ./load_entity_model.sh <dir>      # dir holds aem_desc.bin + aem_desc.json,
#                                     # both written beside the bitstream by
#                                     # sw/litex/milan_soc.py
#
# THE BASE IS NEVER TYPED IN. It is read from aem_desc.json, which the SoC
# build wrote from the value it compiled into the gateware. A loader that
# restated the address would keep working right up until the memory map moved,
# and would then write the model somewhere the store never looks - leaving an
# entity that is silent with no error anywhere.
#
# The image may be (re)loaded at ANY time, including while the entity is up:
# the store answers an honest miss on an unvalidated image and re-arms its
# probe, so a late load heals with no reset. Loading is idempotent.
set -eu

usage() { echo "usage: $0 <dir-with-aem_desc.bin-and-aem_desc.json>" >&2; exit 2; }
[ $# -eq 1 ] || usage
DIR=$1
IMG="$DIR/aem_desc.bin"
MAN="$DIR/aem_desc.json"
[ -f "$IMG" ] || { echo "no image: $IMG" >&2; exit 2; }
[ -f "$MAN" ] || { echo "no manifest: $MAN" >&2; exit 2; }

# The manifest is machine-written JSON with one integer per line; this is a
# grep, not a JSON parser, and it is deliberately strict about what it accepts
# so a malformed manifest fails here instead of at a wrong address.
field() {
    v=$(sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p" "$MAN" | head -1)
    [ -n "$v" ] || { echo "manifest has no numeric '$1'" >&2; exit 2; }
    echo "$v"
}
BASE=$(field desc_base)
WINDOW=$(field window_bytes)
WANT=$(field image_bytes)

HAVE=$(wc -c < "$IMG")
[ "$HAVE" = "$WANT" ] || {
    echo "image is $HAVE bytes, manifest says $WANT - they are not a pair" >&2
    exit 2; }
[ "$HAVE" -le "$WINDOW" ] || {
    echo "image $HAVE bytes exceeds the $WINDOW-byte reserved window" >&2
    exit 2; }

PAGE=4096
[ $((BASE % PAGE)) -eq 0 ] || {
    echo "base $BASE is not page-aligned; dd cannot seek to it safely" >&2
    exit 2; }
SEEK=$((BASE / PAGE))
# Round UP to whole pages: dd's seek is in blocks, so a partial final block
# would otherwise be written at the wrong offset.
PAGES=$(( (HAVE + PAGE - 1) / PAGE ))

printf 'loading %s (%s B) at 0x%x\n' "$IMG" "$HAVE" "$BASE"
dd if="$IMG" of=/dev/mem bs=$PAGE seek=$SEEK count=$PAGES conv=notrunc 2>/dev/null || {
    echo "write to /dev/mem failed - EXPECTED on a no-map window (see the" >&2
    echo "  banner): the read/write path has no linear mapping to write" >&2
    echo "  through. Use aemi-load, which mmaps." >&2
    exit 1; }

# READ BACK AND COMPARE. A write to /dev/mem that lands nowhere does not fail:
# it is accepted and discarded. Only the read-back distinguishes "provisioned"
# from "wrote into a hole", and that distinction is the whole point of running
# this rather than trusting it.
TMP=$(mktemp 2>/dev/null || echo /tmp/aemi.$$)
trap 'rm -f "$TMP"' EXIT INT TERM
dd if=/dev/mem of="$TMP" bs=$PAGE skip=$SEEK count=$PAGES 2>/dev/null
if ! dd if="$TMP" bs=1 count="$HAVE" 2>/dev/null | cmp -s - "$IMG"; then
    echo "read-back MISMATCH: the window did not take the image" >&2
    exit 1
fi

# The magic is what the store itself checks, so print what it will see.
MAGIC=$(od -An -tx1 -N4 "$TMP" | tr -d ' \n')
[ "$MAGIC" = "41454d49" ] || {
    echo "read back magic 0x$MAGIC, expected 41454d49 (\"AEMI\")" >&2; exit 1; }
printf 'verified: AEMI image live at 0x%x, %s bytes\n' "$BASE" "$HAVE"
