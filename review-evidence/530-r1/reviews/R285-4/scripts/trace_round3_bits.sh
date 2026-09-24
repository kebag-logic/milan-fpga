#!/bin/sh
# Print, from the git object store at the reviewed head, every RTL line the
# round-3 bit claims rest on: LWSRP_STATUS packing ([6] = |ACTIVE, [8] =
# source 0's gate), the CRF status bits, the 0x82C talker pack and the lobs
# vector (index 0 = registered Listener level, index > 0 = ACTIVE), and the
# AAF gates. Usage: trace_round3_bits.sh <repo>
set -eu
repo=$1
rev=f814d37d94e17435f3b6dcc424f8b2b606cdd3e9
dp=hdl/milan/milan_datapath.sv
csr=hdl/common/csr/milan_csr.sv
show() { git -C "$repo" show "$rev:$1" | sed -n "$2p" | sed "s#^#$1:#"; }
echo "--- lobs vector (index 0 vs index > 0)"
show $dp '1861,1862p;1879,1888'
echo "--- AAF gates (source 0 and index > 0)"
show $dp '1913,1916p;2020,2027'
echo "--- 0x82C window inputs: AAF indices only"
show $dp '2478p;2483'
show $csr '997p;2916,2920'
echo "--- LWSRP_STATUS packing, LSB last"
show $dp '1652,1657p;2502,2508'
echo "--- [6] and [8] sources"
show $dp '6637p;6652'
echo "--- CRF status [6]/[7]"
show $dp '5280,5281p;5305,5307p;5318,5319'
echo "--- REGISTER_MAP 0x82C row"
git -C "$repo" show "$rev:docs/reference/REGISTER_MAP.md" | grep -n '^| `0x82C`' | cut -c1-700
