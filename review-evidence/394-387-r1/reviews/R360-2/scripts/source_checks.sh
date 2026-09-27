#!/usr/bin/env bash
# Source facts behind the page's link-counter text. usage: source_checks.sh <clone-dir>
set -u; cd "$1" || exit 2
echo "== link_status CSR (MAC_STATUS 0x110) fields and resets"; grep -n -A2 'CSRField("link_up"\|CSRField("speed"\|CSRField("full_duplex"' sw/litex/milan_soc.py
echo "== reset value: link_up=1 | speed(gmii)=2<<1 | full_duplex=1<<3 = $(printf '0x%02x' $((1 | (2<<1) | (1<<3))))"
echo "== writers of link_status outside its definition (expect none)"; git -c core.pager=cat grep -n 'link_status' -- ':!docs' ':!*.md' | grep -v '^sw/litex/milan_soc.py:' || echo none
echo "== bare-metal firmware MDIO / link / MAC_STATUS references (expect none)"; grep -n -i -E 'mdio|link|0x110|mac_status' sw/firmware/milan_baremetal/milan_baremetal.c || echo none
echo "== counter link view"; grep -n -E 'assign eff_link_w|i_link_up & cfg_sw_link|cfg_linkg_dis \| linkg_est_w|ctr_avb_link_edge_w =|ctr_linkup_r <= ctr_linkup_r|ctr_linkdn_r <= ctr_linkdn_r' hdl/milan/milan_datapath.sv
echo "== guard estimate"; grep -n 'assign link_est_o' hdl/common/KL_link_guard.sv
echo "== registers"; grep -n -E '^\| `0x(110|71C|774)` ' docs/reference/REGISTER_MAP.md | cut -c1-220
